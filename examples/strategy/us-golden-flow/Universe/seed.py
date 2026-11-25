"""
The seed builder -- step 2 of 8, before the Curator.  Writes `Universe/Investable_Universe.csv`,
the seed every later stage grows from, out of the index's own membership.

In plain words: the KN US Equity Core says which listings were members on each date, keyed by
Sharadar's tickers; this script writes one row for each listing that was a member at any time from
the floor on, with the span Sharadar prices it over.

Why a script and not the notebook: the universe notebook profiles the price files the Curator
downloaded, so it runs after the Curator; the seed tells the Curator what to download, so it has
to exist first.  This is the one step of the universe stage that runs before any price exists.

**Since 0.16.0 the index and the prices speak one language.**  The Core is built on Sharadar and
keys every listing by Sharadar's ticker -- `DD1` for a symbol since reused, `AAMRQ` for a name
filed under the ticker it ended with -- so the price file's key, `main_identifier`, is the index's
own, `index_identifier`.  The two columns stay apart so a second provider is one more column, not a
rewrite of every reader.  What 0.15 had to prove by CUSIP is now true by construction, and what
this script checks instead is that Sharadar's catalogue knows each listing at all.

- **The catalogue.**  Sharadar's `TICKERS` table for its equity prices (`SEP`), cached in
  `Universe/Provider_Cache/` under the date it was fetched.  The newest cached catalogue is read,
  so a rerun reads the same answer and a reader can see which day's catalogue a seed came from;
  `--refresh` asks Sharadar for today's.  The cache may hold the full export, every table and
  column, as Sharadar writes it: only the `SEP` rows and the columns named here are read.
- **The span.**  `valid_from` and `valid_to` are the listing's first and last price dates in that
  catalogue; outside them a file under the same symbol is another security's history, and the
  panel reads no price there.  A listing Sharadar does not mark as delisted has no `valid_to`: its
  last price date is the day the catalogue was fetched, not an ending.
- **A ticker the provider gave away.**  When Sharadar gives a delisted listing's ticker to another
  security, it files the older one under a new ticker -- `SIX1` for Six Flags since 2026-11 --
  and a fetch under the index's key returns the newer security's prices.  `Provider_Renames.csv`
  beside this script records each such case by hand, with its evidence: the listing keeps its
  `index_identifier` and the catalogue's span, its `main_identifier` becomes the provider's ticker
  now, and the row is used only if the permaticker in the catalogue is the one recorded.
- **Not in the catalogue.**  A member the catalogue does not list is still a row, under its own
  ticker, `match` saying so: the Curator asks Sharadar for it anyway, and the universe notebook
  counts the index weight of every member left without prices as the survivorship cost.

The provider key comes from `Config/.env`, is read by name and is never printed.

It produces `Universe/Investable_Universe.csv`: `main_identifier`, `index_identifier`,
`valid_from`, `valid_to`.  The worked example's seed is public, so it holds tickers and dates only,
never a name, a permanent identifier or another vendor field; the name, the permaticker and the
match it builds each row from stay in memory and in the app's universe, which git ignores.

It prevents a member silently missing from the download, and a dead company's prices read past the
day it stopped trading.
"""

import argparse
import datetime
import importlib.util
import io
import os
import pathlib
import sys
import time
import types
import urllib.error
import urllib.request
import zipfile

import pandas

import kaxanuk.data_curator

__all__ = [
    "fetch_catalogue",
    "main",
    "write_app_universe",
]

CACHE_DIRECTORY = pathlib.Path(__file__).parent / "Provider_Cache"
HAND_SUPPLIED_PATH = pathlib.Path(__file__).parent.parent / "Data" / "hand_supplied.py"
RENAMES_PATH = pathlib.Path(__file__).parent / "Provider_Renames.csv"
SEED_PATH = pathlib.Path(__file__).parent / "Investable_Universe.csv"
# The seed as the KaxaNuk app reads a saved universe from `Universe/`: a `symbol` column first, then
# the name, as the app's own Creator saves one, and each listing's span, so the app can read it
# point in time once it does.  Named after the index, so the app lists it by what it is.
APP_UNIVERSE_PATH = pathlib.Path(__file__).parent / "KN_US_Equity_Core.csv"
APP_UNIVERSE_COLUMNS = {
    "main_identifier": "symbol",
    "name": "company_name",
    "index_identifier": "index_identifier",
    "valid_from": "valid_from",
    "valid_to": "valid_to",
}
# What the catalogue says each listing is, under the names the app's own universes use, so its
# Universe Analyzer can group by them.
APP_CLASSIFICATION_COLUMNS = {
    "exchange": "exchange",
    "category": "instrument_type",
    "sector": "sector",
    "industry": "industry",
    "scalemarketcap": "size",
    "currency": "currency",
}
LINE_END = "\n"

# The catalogue's columns this seed reads, and nothing else: a lean request is a fast one.
CATALOGUE_COLUMNS = (
    "ticker",
    "permaticker",
    "name",
    "isdelisted",
    "firstpricedate",
    "lastpricedate",
    "exchange",
    "category",
    "sector",
    "industry",
    "scalemarketcap",
    "currency",
)
# Sharadar's own API, which the startup subscription is served from, never Nasdaq Data Link's.
CATALOGUE_URL = "https://api.sharadar.com/v1.0/data/tickers?years=full"
# The first date whose members the seed carries: the Core's first file date.
MEMBERSHIP_FLOOR = datetime.date(
    1998,
    12,
    31,
)
# A busy server is asked again after a pause.
REQUEST_ATTEMPTS = 4
REQUEST_PAUSE_SECONDS = 30
SEED_COLUMNS = (
    "main_identifier",
    "index_identifier",
    "name",
    "permaticker",
    "valid_from",
    "valid_to",
    "match",
)
# The columns the seed file keeps: tickers and dates only, since the example's seed is public.
WRITTEN_COLUMNS = (
    "main_identifier",
    "index_identifier",
    "valid_from",
    "valid_to",
)


def fetch_catalogue(
    api_key: str,
    refresh: bool,
) -> "pandas.DataFrame":
    """
    Sharadar's catalogue of equity listings: the newest cached one, or today's from the provider.

    The cache is named by the date it was fetched, so the seed of a given day can be rebuilt from
    the same answer, and a newer catalogue is a new file rather than an edit of the old one.
    """
    cached = sorted(CACHE_DIRECTORY.glob("sharadar_tickers_*.csv"))

    if len(cached) > 0 and not refresh:
        print(f"catalogue read from {cached[-1].name}", flush=True)
        catalogue = pandas.read_csv(
            cached[-1],
            dtype=str,
            keep_default_na=False,
        )
        equities = catalogue[catalogue["table"] == "SEP"] if "table" in catalogue else catalogue

        return equities[list(CATALOGUE_COLUMNS)]

    cache_path = CACHE_DIRECTORY / f"sharadar_tickers_{datetime.date.today().isoformat()}.csv"
    archive = _download_catalogue(api_key)

    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        member = bundle.namelist()[0]

        with bundle.open(member) as handle:
            downloaded = pandas.read_csv(
                handle,
                dtype=str,
                keep_default_na=False,
            )

    CACHE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    downloaded.to_csv(
        cache_path,
        index=False,
        lineterminator="\n",
    )
    downloaded_equities = (
        downloaded[downloaded["table"] == "SEP"]
        if "table" in downloaded
        else downloaded
    )

    return downloaded_equities[list(CATALOGUE_COLUMNS)]


def main() -> int:
    """
    Build the seed from the index's members since the floor, and say how many the catalogue knows.
    """
    parser = argparse.ArgumentParser(description="Build the seed from the index's members.")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="ask Sharadar for today's catalogue instead of reading the newest cached one",
    )
    arguments = parser.parse_args()
    kaxanuk.data_curator.load_config_env()
    api_key = os.environ.get("KNDC_API_KEY_SHARADAR", "").strip()

    if api_key == "":
        message = "KNDC_API_KEY_SHARADAR is empty; fill it in Config/.env"

        raise RuntimeError(message)

    hand_supplied = _load_hand_supplied()
    holdings = hand_supplied.read_benchmark_holdings()
    floor = pandas.Timestamp(MEMBERSHIP_FLOOR)
    since_floor = holdings.loc[holdings.index >= floor]
    members = sorted(since_floor.columns[(since_floor > 0).any(axis=0)])
    print(f"{len(members)} listings were members on some date from {MEMBERSHIP_FLOOR}", flush=True)
    catalogue = fetch_catalogue(
        api_key,
        arguments.refresh,
    )
    by_ticker = catalogue.drop_duplicates("ticker").set_index("ticker")
    renames = _read_renames()
    rows = [
        _seed_row(
            listing,
            by_ticker,
            renames,
        )
        for listing in members
    ]
    seed = pandas.DataFrame(
        rows,
        columns=list(SEED_COLUMNS),
    )
    seed[list(WRITTEN_COLUMNS)].to_csv(
        SEED_PATH,
        index=False,
        lineterminator="\n",
    )
    write_app_universe(
        seed,
        catalogue,
    )
    match_counts = seed["match"].value_counts()
    print(f"wrote {SEED_PATH.name}: {len(seed)} listings")
    print(match_counts.to_string())

    return 0


def write_app_universe(
    seed: "pandas.DataFrame",
    catalogue: "pandas.DataFrame",
) -> pathlib.Path:
    """
    Write the seed as the KaxaNuk app reads a saved universe, and return where.

    Every listing the index held is a row, departed ones included, with the span Sharadar prices it
    over: the app's saved universes are lists of names today, and the span is what a point-in-time
    read of the same file needs.  Beside each name, what Sharadar's catalogue says it is -- its
    exchange, category, sector, industry and size bucket -- so the app's Universe Analyzer can group
    by any of them.  They are what the listing is classified as today, not on each date.  The seed
    stays the authority; this is a view of it, written again each time the seed is.
    """
    by_ticker = catalogue.drop_duplicates("ticker").set_index("ticker")
    view = seed[list(APP_UNIVERSE_COLUMNS)].rename(columns=APP_UNIVERSE_COLUMNS)
    described = view.join(
        by_ticker[list(APP_CLASSIFICATION_COLUMNS)].rename(columns=APP_CLASSIFICATION_COLUMNS),
        on="symbol",
    )
    described.insert(
        2,
        "asset_class",
        "equity",
    )
    described.insert(
        3,
        "country",
        "US",
    )
    described.to_csv(
        APP_UNIVERSE_PATH,
        index=False,
        lineterminator=LINE_END,
    )
    listing_count = len(described)
    print(f"wrote {APP_UNIVERSE_PATH.name}: {listing_count} listings, as the KaxaNuk app reads it")

    return APP_UNIVERSE_PATH


def _download_catalogue(
    api_key: str,
) -> bytes:
    """
    Sharadar's whole catalogue, as the zip its bulk download serves, asked again when busy.

    The catalogue publishes only a full snapshot, so it is taken whole, as Sharadar's documentation
    says to.  The key travels in a header, never in the address, and nothing here prints either.
    """
    request = urllib.request.Request(
        CATALOGUE_URL,
        headers={"x-api-key": api_key},
    )

    for attempt in range(1, REQUEST_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:

                return response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"catalogue, attempt {attempt}: {type(error).__name__}", flush=True)
            time.sleep(REQUEST_PAUSE_SECONDS)

    message = "Sharadar's catalogue did not answer; nothing was written"

    raise RuntimeError(message)


def _load_hand_supplied() -> "types.ModuleType":
    """
    Import the reader of the desk's files by path, because `Data/` is a folder, not a package.
    """
    specification = importlib.util.spec_from_file_location(
        "hand_supplied",
        HAND_SUPPLIED_PATH,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def _read_renames() -> dict[str, dict[str, str]]:
    """
    The listings whose ticker the provider gave away, by the index's key, each with the
    permaticker it must carry and the ticker the provider files it under now.
    """
    if not RENAMES_PATH.is_file():

        return {}

    renames = pandas.read_csv(
        RENAMES_PATH,
        dtype=str,
        keep_default_na=False,
    )

    return {
        row["index_identifier"]: {
            "permaticker": row["permaticker"],
            "provider_ticker": row["provider_ticker"],
        }
        for _, row in renames.iterrows()
    }


def _seed_row(
    listing: str,
    by_ticker: "pandas.DataFrame",
    renames: dict[str, dict[str, str]],
) -> dict[str, str]:
    """
    One member's row: its keys, and the span the catalogue prices it over, or why it has none.

    A listing in `Provider_Renames.csv` keeps the index's key and the catalogue's span, and takes
    the provider's ticker now as the key its prices are fetched under -- only when the catalogue's
    permaticker is the one the file records, so a rename never moves one security's prices onto
    another's.
    """
    rename = renames.get(listing)
    # A renamed listing is looked up under the ticker the provider files it under now first: once
    # the provider has given the index's ticker away, the catalogue may no longer list it at all.
    candidates = [listing] if rename is None else [rename["provider_ticker"], listing]
    found = [
        candidate
        for candidate in candidates
        if candidate in by_ticker.index
    ]

    if len(found) == 0:

        return {
            "main_identifier": listing,
            "index_identifier": listing,
            "name": "",
            "permaticker": "",
            "valid_from": "",
            "valid_to": "",
            "match": "not in catalogue",
        }

    entry = by_ticker.loc[found[0]]
    still_listed = entry["isdelisted"] != "Y"
    valid_to = "" if still_listed else entry["lastpricedate"]

    if rename is not None and rename["permaticker"] != entry["permaticker"]:
        message = " ".join([
            f"{listing}: Provider_Renames.csv records permaticker {rename['permaticker']},",
            f"the catalogue has {entry['permaticker']}; the rename is not applied",
        ])

        raise ValueError(message)

    main_identifier = listing if rename is None else rename["provider_ticker"]
    match = "sharadar ticker" if rename is None else "sharadar ticker, renamed by the provider"

    return {
        "main_identifier": main_identifier,
        "index_identifier": listing,
        "name": entry["name"],
        "permaticker": entry["permaticker"],
        "valid_from": entry["firstpricedate"],
        "valid_to": valid_to,
        "match": match,
    }


if __name__ == "__main__":
    sys.exit(main())
