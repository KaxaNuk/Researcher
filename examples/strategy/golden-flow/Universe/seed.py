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
- **Not in the catalogue.**  A member the catalogue does not list is still a row, under its own
  ticker, with no span: the Curator asks Sharadar for it anyway, the universe notebook finds it
  missing from the same catalogue, and it counts the index weight of every member left without
  prices as the survivorship cost.
- **Tickers and dates only.**  What a listing is -- its name, Sharadar's permanent identifier,
  its sector -- is the provider's data: the universe notebook reads it from the cached
  catalogue, and the seed, which is committed, never carries it.

The provider key comes from `Config/.env`, is read by name and is never printed.

It produces `Universe/Investable_Universe.csv`, tickers and dates only: `main_identifier`,
`index_identifier`, `valid_from`, `valid_to`.

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
]

CACHE_DIRECTORY = pathlib.Path(__file__).parent / "Provider_Cache"
HAND_SUPPLIED_PATH = pathlib.Path(__file__).parent.parent / "Data" / "hand_supplied.py"
SEED_PATH = pathlib.Path(__file__).parent / "Investable_Universe.csv"

# The catalogue's columns this seed reads, and nothing else: a lean request is a fast one.
CATALOGUE_COLUMNS = (
    "ticker",
    "isdelisted",
    "firstpricedate",
    "lastpricedate",
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
    rows = [
        _seed_row(
            listing,
            by_ticker,
        )
        for listing in members
    ]
    seed = pandas.DataFrame(
        rows,
        columns=list(SEED_COLUMNS),
    )
    seed.to_csv(
        SEED_PATH,
        index=False,
        lineterminator="\n",
    )
    not_catalogued = [
        listing
        for listing in members
        if listing not in by_ticker.index
    ]
    print(f"wrote {SEED_PATH.name}: {len(seed)} listings")
    print(f"not in the catalogue: {len(not_catalogued)} {not_catalogued}")

    return 0


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


def _seed_row(
    listing: str,
    by_ticker: "pandas.DataFrame",
) -> dict[str, str]:
    """
    One member's row: its keys, and the span the catalogue prices it over, or why it has none.
    """
    if listing not in by_ticker.index:

        return {
            "main_identifier": listing,
            "index_identifier": listing,
            "valid_from": "",
            "valid_to": "",
        }

    entry = by_ticker.loc[listing]
    still_listed = entry["isdelisted"] != "Y"
    valid_to = "" if still_listed else entry["lastpricedate"]

    return {
        "main_identifier": listing,
        "index_identifier": listing,
        "valid_from": entry["firstpricedate"],
        "valid_to": valid_to,
    }


if __name__ == "__main__":
    sys.exit(main())
