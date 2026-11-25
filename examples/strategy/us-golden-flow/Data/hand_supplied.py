"""
The hand-supplied inputs -- step 3 of 8, beside the Curator.  The index a book is reported against
and the factor model attribution reads are not sold by any price provider: they arrive as files
from KaxaNuk's Analytics Factory (https://www.kaxanuk.mx/analytics; ask analytics@kaxanuk.mx for
them), and this module is the one place that reads them.

In plain words: set `KN_ANALYTICS_PATH` in `Config/.env` to the Factory's folder and the files are
read where they are, in the Factory's own names and headers -- nobody renames or re-heads a file.
Leave it empty, and the same files, dropped unchanged into `Data/Curator/Benchmarks/` and
`Data/Curator/Factors/`, are read from there.

The Factory's layout, its folders read under their current names first and under the older ones,
`Benchmarks/` and `Factors/`, where those are absent.  The files keep the same names and headers in
both, and the drop-in folders keep the older names:

    Benchmark Portfolios/KN_US_Equity_Benchmark_Holdings.csv
        m_date, ISO dates; one column per listing, its weight in the index that day
    Benchmark Portfolios/KN_US_Equity_Benchmark_Returns.csv
        m_date, day-first dates; kn600, the index's daily return
    Factor Models/<Name>.csv
        dates down in an unnamed first column, ISO; listings across

Four of the factor files are the model's own series rather than factors, and the attribution
library knows them by reserved lower-case names: `Market.csv` is `f_market`, and `Idyo_Returns`,
`Total_Excess_Returns` and `Total_Factor_Returns` become `f_idyo_returns`,
`f_total_excess_returns` and `f_total_factor_returns`.  Every other file is a factor named by its
file name in lower case.

**Two keys, one map.**  An index keys each listing by its own ticker, which can differ from the
identifier the experiment's provider prices it under -- `BRK.B` against `BRK-B`, or a symbol since
recycled.  A seed taken from an index carries both: `index_identifier`, the index's, and
`main_identifier`, the provider's.  This module is the one place that maps one to the other, so
the holdings and the factor files reach every reader keyed like the price files, and a listing
whose two keys differ is never silently read as a non-member.  The map comes from the strategy's
seed builder, or from the Analytics Factory when it supplies one.

`Data/curator.py` rebuilds the index as a price level from its returns; the universe notebook and
each experiment read the holdings for point-in-time membership; and
`Experiments/attribution_analysis.py` reads all three.  Each loads this file by path, because
`Data/` is a folder rather than a package.  A book frozen for paper trading carries its own copy
of this file and of the seed, and the copy resolves its paths from where it sits.

It prevents a renamed copy drifting from the Factory's file, a date read in the wrong order, and
a member dropped because its two keys differ.
"""

# --- example: begin ---

import os
import pathlib

import dotenv
import pandas

__all__ = [
    "ANALYTICS_PATH_KEY",
    "BENCHMARK_HOLDINGS_NAME",
    "BENCHMARK_MEMBERSHIP_NAME",
    "BENCHMARK_NAME",
    "BENCHMARK_RETURNS_NAME",
    "BENCHMARK_RETURNS_SERIES_NAME",
    "BENCHMARK_TICKERS_NAME",
    "FACTOR_DELIVERY_NAME",
    "INDEX_IDENTIFIER_COLUMN",
    "LIBRARY_DATE_HEADER",
    "benchmark_directory",
    "factor_directory",
    "factor_path",
    "read_benchmark_holdings",
    "read_benchmark_returns",
    "read_factor_returns",
    "read_idiosyncratic_returns",
    "read_listing_keys",
    "read_member_holdings",
    "report_missing",
]

ANALYTICS_PATH_KEY = "KN_ANALYTICS_PATH"
# The desk's folder names, newest first: the Analytics Factory's layout, then the one it replaced.
BENCHMARK_FOLDER_NAMES = (
    "Benchmark Portfolios",
    "Benchmarks",
)
# The benchmark a book is reported against, as its files name it, and the files themselves.
BENCHMARK_NAME = "Core"
BENCHMARK_HOLDINGS_NAME = f"KN_US_Equity_{BENCHMARK_NAME}_Holdings_Daily.csv"
BENCHMARK_MEMBERSHIP_NAME = f"KN_US_Equity_{BENCHMARK_NAME}_Membership_Daily.csv"
BENCHMARK_RETURNS_NAME = f"KN_US_Equity_{BENCHMARK_NAME}_Returns_Daily.csv"
# The index's return series is named for the index, as the attribution reports it.
BENCHMARK_RETURNS_SERIES_NAME = f"kn_us_equity_{BENCHMARK_NAME.lower()}"
BENCHMARK_TICKERS_NAME = f"KN_US_Equity_{BENCHMARK_NAME}_Tickers.csv"
DROP_IN_DIRECTORY = pathlib.Path(__file__).parent / "Curator"
ENVIRONMENT_PATH = pathlib.Path(__file__).parent.parent / "Config" / ".env"
# The factor model's delivery read, in its own folder under the factor folder, so the next delivery
# can sit beside it without a book reading two models at once.
FACTOR_DELIVERY_NAME = "KN_US_Equity_Factor_Model_2026-11-06"
# A factor file is `KN_US_Equity_Factor_<Name>_Daily.csv`; the factor returns file is not a factor.
FACTOR_FILE_PREFIX = "KN_US_Equity_Factor_"
FACTOR_FILE_SUFFIX = "_Daily"
FACTOR_FOLDER_NAMES = (
    "Factor Models",
    "Factors",
)
FACTOR_RETURNS_FILE_NAME = "KN_US_Equity_Factor_Model_Returns_Daily.csv"
# The seed's two keys: the price file's, and the desk's.
IDENTIFIER_COLUMN = "main_identifier"
INDEX_IDENTIFIER_COLUMN = "index_identifier"
SEED_PATH = pathlib.Path(__file__).parent.parent / "Universe" / "Investable_Universe.csv"

# The desk writes `m_date` in both benchmark files, ISO in both since the Core of 2026-10-22; the
# attribution library wants every frame's dates under one header of its own.
DESK_DATE_HEADER = "m_date"
FACTOR_DATE_FORMAT = "%Y-%m-%d"
HOLDINGS_DATE_FORMAT = "%Y-%m-%d"
LIBRARY_DATE_HEADER = "date_column"
RETURNS_DATE_FORMAT = "%Y-%m-%d"

# The model's own series, known to the library by these names and dropped from the percentage
# decomposition; a factor file is otherwise named by its file name in lower case.
RESERVED_FACTOR_NAMES = {
    "Idyo_Returns": "f_idyo_returns",
    "Market": "f_market",
    "Total_Excess_Returns": "f_total_excess_returns",
    "Total_Factor_Returns": "f_total_factor_returns",
}


def benchmark_directory() -> "pathlib.Path":
    """
    The folder the index's two files are read from: the desk's, or the drop-in beside the Curator.
    """
    analytics = _analytics_directory()

    if analytics is None:

        return DROP_IN_DIRECTORY / "Benchmarks"

    return _first_existing(
        analytics,
        BENCHMARK_FOLDER_NAMES,
    )


def factor_directory() -> "pathlib.Path":
    """
    The folder the factor model's delivery is read from, under the desk's factor folder or the
    drop-in.
    """
    analytics = _analytics_directory()

    if analytics is None:

        return DROP_IN_DIRECTORY / "Factors" / FACTOR_DELIVERY_NAME

    factor_folder = _first_existing(
        analytics,
        FACTOR_FOLDER_NAMES,
    )

    return factor_folder / FACTOR_DELIVERY_NAME


def factor_path(name: str) -> "pathlib.Path":
    """
    One factor's file in the delivery, by the factor's name as the model gives it -- `Market`,
    `Idyo_Returns` -- so a notebook never spells the naming standard itself.
    """

    return factor_directory() / f"{FACTOR_FILE_PREFIX}{name}{FACTOR_FILE_SUFFIX}.csv"


def read_benchmark_holdings() -> "pandas.DataFrame":
    """
    The index's daily holdings as the desk keys them: dates down, listings across, each a weight.

    A listing absent on a date weighs zero, never null, because both the membership rule and the
    attribution library read a missing weight as a hole rather than as a name that was not held.
    """
    path = benchmark_directory() / BENCHMARK_HOLDINGS_NAME
    holdings = pandas.read_csv(path)
    dates = pandas.to_datetime(
        holdings[DESK_DATE_HEADER],
        format=HOLDINGS_DATE_FORMAT,
    )
    weights = holdings.drop(columns=[DESK_DATE_HEADER])
    weights.index = pandas.DatetimeIndex(
        dates,
        name=LIBRARY_DATE_HEADER,
    )
    ordered = weights.sort_index()

    return ordered.fillna(0.0)


def read_benchmark_returns() -> "pandas.Series":
    """
    The index's daily return, in date order, under the index's own name.

    The dates are parsed with the format stated, never guessed: an earlier file wrote them day
    first, and the fourth of January and the first of April are the same string read two ways.
    """
    path = benchmark_directory() / BENCHMARK_RETURNS_NAME
    returns = pandas.read_csv(path)
    dates = pandas.to_datetime(
        returns[DESK_DATE_HEADER],
        format=RETURNS_DATE_FORMAT,
    )
    return_column = returns.columns[1]
    series = pandas.Series(
        returns[return_column].to_numpy(),
        index=pandas.DatetimeIndex(
            dates,
            name=LIBRARY_DATE_HEADER,
        ),
        name=BENCHMARK_RETURNS_SERIES_NAME,
    )

    return series.sort_index()


def read_factor_returns() -> dict[str, "pandas.DataFrame"]:
    """
    Every factor file of the delivery, each one named for the attribution library by the `<Name>`
    of `KN_US_Equity_Factor_<Name>_Daily.csv`.

    Every file of that pattern is read as a factor, so a stray one is a stray factor.  The date
    column arrives unnamed and as strings; a string date aligns with nothing and the factor
    attribution comes back with zero rows rather than an error, so it is parsed here.  The listings
    stay keyed as the desk keys them; `read_listing_keys` renames them where a caller needs the
    price files' keys.
    """
    factors = {}
    directory = factor_directory()

    factor_paths = [
        path
        for path in sorted(directory.glob(f"{FACTOR_FILE_PREFIX}*{FACTOR_FILE_SUFFIX}.csv"))
        if path.name != FACTOR_RETURNS_FILE_NAME
    ]

    for path in factor_paths:
        factor_name = path.stem[len(FACTOR_FILE_PREFIX):-len(FACTOR_FILE_SUFFIX)]
        name = RESERVED_FACTOR_NAMES.get(
            factor_name,
            factor_name.lower(),
        )
        frame = pandas.read_csv(path)
        dates = pandas.to_datetime(
            frame[frame.columns[0]],
            format=FACTOR_DATE_FORMAT,
        )
        values = frame.drop(columns=[frame.columns[0]])
        values.index = pandas.DatetimeIndex(
            dates,
            name=LIBRARY_DATE_HEADER,
        )
        factors[name] = values

    return factors


def read_idiosyncratic_returns() -> "pandas.DataFrame":
    """
    Each listing's daily specific return from the factor model, keyed by the price files.

    The specific return is what the model's factors do not explain on that day: the model takes
    each exposure at the close before and the factor returns from that day's cross-section, so a
    day's specific return uses nothing after that day's close.  A listing the seed does not map is
    left out, as `read_member_holdings` leaves it out; a day the model gives no return stays null.
    """
    frame = pandas.read_csv(factor_path("Idyo_Returns"))
    dates = pandas.to_datetime(
        frame[frame.columns[0]],
        format=FACTOR_DATE_FORMAT,
    )
    returns = frame.drop(columns=[frame.columns[0]])
    returns.index = pandas.DatetimeIndex(
        dates,
        name=LIBRARY_DATE_HEADER,
    )
    keys = read_listing_keys()
    mapped = [
        listing
        for listing in returns.columns
        if listing in keys
    ]
    keyed = returns[mapped]
    keyed.columns = [
        keys[listing]
        for listing in mapped
    ]

    if keyed.columns.has_duplicates:
        message = "two model listings map to one price file; the seed's map must be one to one"

        raise ValueError(message)

    return keyed.sort_index()


def read_listing_keys() -> dict[str, str]:
    """
    The desk's key for each listing the seed carries, mapped to the key of its price file.

    Read from the seed, the one place both keys are written.  A listing the seed does not carry --
    one Sharadar does not price, or the older half of a recycled symbol -- is absent from the map,
    and the caller decides what absence means; the universe notebook writes every such listing
    into `Universe/Data_Issues.csv`.
    """
    seed = pandas.read_csv(
        SEED_PATH,
        dtype=str,
        keep_default_na=False,
    )

    if INDEX_IDENTIFIER_COLUMN not in seed.columns:
        message = f"{SEED_PATH} has no {INDEX_IDENTIFIER_COLUMN} column to map the index by"

        raise KeyError(message)

    has_listing = seed[INDEX_IDENTIFIER_COLUMN].str.strip() != ""
    has_symbol = seed[IDENTIFIER_COLUMN].str.strip() != ""
    mapped = seed[has_listing & has_symbol]
    keys = dict(
        zip(
            mapped[INDEX_IDENTIFIER_COLUMN].str.strip(),
            mapped[IDENTIFIER_COLUMN].str.strip(),
            strict=True,
        )
    )

    return keys


def read_member_holdings() -> "pandas.DataFrame":
    """
    The index's daily holdings keyed by the price files: every listing renamed through the seed.

    Listings the seed does not map are left out, so the weights of a date sum to the share of the
    index this repository can price, not to one: the universe notebook publishes that share per
    date as the survivorship cost, and the attribution renormalises what it keeps.  Two listings
    can never land on one price file, because the seed's map is one to one and is checked so.
    """
    holdings = read_benchmark_holdings()
    keys = read_listing_keys()
    mapped = [
        listing
        for listing in holdings.columns
        if listing in keys
    ]
    members = holdings[mapped]
    members.columns = [
        keys[listing]
        for listing in mapped
    ]

    if members.columns.has_duplicates:
        message = "two index listings map to one price file; the seed's map must be one to one"

        raise ValueError(message)

    return members


def report_missing() -> list[str]:
    """
    Say which of the hand-supplied files is absent, in one pass, before anything is loaded.
    """
    missing = []
    holdings_path = benchmark_directory() / BENCHMARK_HOLDINGS_NAME
    returns_path = benchmark_directory() / BENCHMARK_RETURNS_NAME
    directory = factor_directory()
    factor_files = sorted(directory.glob("*.csv"))

    if not holdings_path.is_file():
        missing.append(f"no index holdings at {holdings_path}")

    if not returns_path.is_file():
        missing.append(f"no index returns at {returns_path}")

    if len(factor_files) == 0:
        missing.append(f"no factor files in {directory}")

    return missing


def _analytics_directory() -> "pathlib.Path | None":
    """
    The desk's folder when `KN_ANALYTICS_PATH` names one, taken from the environment first.

    `Config/.env` is loaded without overriding what the environment already holds, so a scheduler
    that sets the variable wins.  A path that does not exist is an error, not a fallback: reading
    the drop-in folder when the desk's was meant is how two sets of numbers start to circulate.
    """
    dotenv.load_dotenv(
        ENVIRONMENT_PATH,
        override=False,
    )
    configured = os.environ.get(ANALYTICS_PATH_KEY, "").strip()

    if configured == "":

        return None

    directory = pathlib.Path(configured)

    if not directory.is_dir():
        message = f"{ANALYTICS_PATH_KEY} names {directory}, which is not a folder"

        raise FileNotFoundError(message)

    return directory


def _first_existing(
    parent: "pathlib.Path",
    names: tuple[str, ...],
) -> "pathlib.Path":
    """
    The first of the names that is a folder under the parent, or the first name when none is.

    The desk renamed its folders once; reading both layouts keeps a strategy running across the
    change, and a missing folder is reported under the newest name.
    """
    for name in names:
        candidate = parent / name

        if candidate.is_dir():

            return candidate

    return parent / names[0]

# --- example: end ---
