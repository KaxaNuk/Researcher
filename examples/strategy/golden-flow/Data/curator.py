"""
Data Curator -- step 3 of 8, block 1 of 3.  The only file in this repository that downloads time
series from a data provider.  A strategy's seed builder, where it has one, reads the same
provider's catalogue of what each security *is* -- its name, its price dates -- and caches it in
`Universe/Provider_Cache/`; nothing else talks to a provider.

In plain words: you describe the data you want -- provider, identifiers, dates and columns -- and
the KaxaNuk Data Curator fetches it, aligns the calendar, handles splits and dividends, and writes
one file per identifier, the same way every run.

Runs first, after the seed exists, and before `Universe/universe_marimo.py`, which profiles what
this writes.  Nothing else has to exist before it except `Universe/Investable_Universe.csv` and a
provider key in `Config/.env`.

What is expected here is a short driver, not a framework:

- Read the identifiers from `Universe/Investable_Universe.csv`, column `main_identifier`, the
  identifier the experiment's provider prices each security under.  The seed is the authority on
  what exists, so it drives the download.
- Build one Data Curator configuration, or one per batch where the provider answers several
  identifiers in one request: the date window, those identifiers, and the output columns -- the
  provider's `m_*` columns plus the `c_*` columns defined in `Data/Curator/custom_calculations.py`.
  Fix the end date rather than using today, so two people running a week apart get comparable
  files.
- Take a later end date as an argument, `--end-date`, for the callers that need newer data, such
  as `Paper_Trading/daily_update.py`.  A refresh refetches each file whole, because a fresh pull
  rebases every adjusted column from the present, and remembers the date each file was fetched
  through, so a run that stops half way resumes where it stopped.
- Call the public library -- `kaxanuk-data-curator`, already installed by `uv sync` from
  `pyproject.toml`, imported as `kaxanuk.data_curator` -- with each data block the columns read
  mapped to the provider, so each name gets its own answer and its own file.
- Record the provider's answer for each name.  A name it does not carry is then told from one it
  refused today -- a rate limit, a timeout -- and only the second is asked again, after a pause.
- Point its output at `Data/Curator/Time_Series/`, one Parquet file per identifier, written and
  read through `Data/time_series.py`.  The library's default folder is `Output/`; here every stage
  has one home, and this is the Curator's.
- A provider's history can stop where its coverage does: a name that left the market years ago may
  be missing from it altogether.  Fetch such names from a second provider that carries them, into
  the same files and columns, and say in the strategy's documents which names came from where and
  how any column the second provider lacks was filled.  Or leave them out and publish what that
  costs, the survivorship cost, beside every result.  Either is a decision the journal records.

**The columns are the ones the pipeline reads, and no more.**  Widening the tuple changes every
file's header and refetches every identifier, so a column is added when a stage reads it, never on
speculation.  A new experiment's signal on the data already downloaded is an `r_*` column of the
refinery, never a wider download.

Three adjustment families arrive from the provider and each does a different job:

    unadjusted            the price actually quoted; the order ticket is written in it
    split-adjusted        traded value, which is liquidity in today's share terms, checked
                          across every split before it is ranked on: volume can arrive split twice
    dividend-and-split    the total-return series a signal, a return and the backtest P&L run on

**Where the provider rounds its adjusted prices, rebuild the adjustment from the exact close.**  A
provider that keeps a few decimals on every adjusted price makes an early series of a name split
many times move in steps of a percent.  The unadjusted close is exact, so the split ratio and the
total-return close are rebuilt from it and the provider's own dividends and splits, as `c_*`
calculations in `Data/Curator/custom_calculations.py`, with any split after the window counted on
every day.  A corporate action the dividend column does not carry, such as a spin-off, is added
after the download from the provider's own record of it.  Then every file is read back and the
rebuilt series compared with the provider's own wherever its decimals are fine enough, into a table
of checks beside the time series; a disagreement is named, never smoothed over.

**Volume can arrive adjusted twice at a split**: traded value steps by the split's own factor while
the shares the tape printed stay flat.  Correct it in the `c_*` traded value, and let the universe
notebook's register read the same signature, so a name the correction missed is named there.

More series ride along in the same folder although they are not in the seed: the benchmarks the
strategy is reported against, and the rate the engine pays on the book's cash, a daily series the
engine reads beside the prices.  The backtest engine reads everything from one directory, so a
series filed anywhere else is one it cannot read.  None enters the cross-section, because
`Data/refinery.py` takes membership from the seed.

An index's daily holdings and returns, and a factor model's returns, are not sold by any price
provider: they arrive from KaxaNuk's Analytics Factory, and `Data/hand_supplied.py` reads them --
in place, from the folder `KN_ANALYTICS_PATH` names, or from the drop zones `Benchmarks/` and
`Factors/` beside the time series.  Without them this script still downloads every price and says
the index was not staged; the notebooks stop where they first read it.

Credentials come from `Config/.env` and are never printed -- not into a log line, a notebook
output or a commit.  An exposed key is rotated, not edited out.

It produces `Data/Curator/Time_Series/<identifier>.parquet`, `m_*` plus `c_*`, read by the universe
notebook, `Data/refinery.py` and the engine; and in `Data/Curator/` the provider's last answer for
each name and the date each file was fetched through.

It prevents beautiful results that came from broken inputs -- and a dataset nobody else can
rebuild.
"""

# --- example: begin ---

# **Sharadar is the only price provider, by the owner's decision of 2026-10-23,** and the KN US
# Equity Core is built on it, so every member is asked for under the index's own ticker.  Sharadar
# keeps delisted securities, which is what lets the window open in 2000 without a survivorship hole.
# A member it does not price is dropped, and the universe notebook counts the share of the index it
# held, per date, as the survivorship cost.  Sharadar answers several tickers in one request, so the
# seed is asked for in batches: fewer requests, inside the provider's rate limit, and a batch it
# refuses is asked again after a pause.
#
# **The columns are the ones the pipeline reads, and no more.**  Sharadar publishes open, high, low,
# close and volume split-adjusted, the close also unadjusted and dividend-and-split adjusted, and no
# VWAP.  Widening the tuple changes every file's header and refetches every identifier, so a column
# is added when a stage reads it, never on speculation.
#
# **Sharadar rounds every price to three decimals, its adjusted ones included,** and only its
# unadjusted close is exact.  So the adjustment is rebuilt by the Curator itself, as `c_*`
# calculations in `Data/Curator/custom_calculations.py`, from the exact close and Sharadar's own
# dividends and splits, which the Curator reads through their joined column names --
# `d_ex_dividend_date_dividend_split_adjusted`, `s_split_date_numerator` and
# `s_split_date_denominator` -- once the dividend and split blocks are mapped to the provider.
#
# **The one action the Curator's dividend column does not carry is a spin-off** (GE's GE HealthCare
# and GE Vernova): `apply_spin_offs` adds Sharadar's `spinoffdividend` values, from its actions bulk
# file cached in `Data/Curator/Actions/`, to the files that had one.  After that,
# `check_adjustments` reads every file back and compares the rebuilt series with Sharadar's own
# wherever its decimals allow, into `Data/Curator/adjustment_checks.csv`; it writes
# nothing else.
#
#     m_close                               exact; the order ticket is written in it
#     m_*_split_adjusted                    three decimals; the open, the engine's range and volume
#     c_close_dividend_and_split_adjusted   the rebuilt total-return close: signals, returns, marks
#     c_open, c_open_dividend_and_split_adjusted   the next day's open, unadjusted and on that basis
#     c_traded_value                        the day's dollars traded, volume counted twice corrected
#
# The open, high and low exist only split-adjusted, at three decimals, so the open the book is
# filled at keeps that rounding -- an error in either direction, not a bias -- and the engine's
# spread estimate reads a range that is coarse wherever a security's split-adjusted price is low.
#
# Two more series ride along in the same folder although they are not in the seed: `SPY`, the
# exchange-traded benchmark the book is reported against beside the index, and `DFF`, the Federal
# Reserve's effective federal funds rate from FRED, the rate the engine pays on the book's cash, as
# Interactive Brokers pays on a dollar balance, and the risk-free rate of every Sharpe ratio.  The
# engine reads everything from one directory, so a series filed anywhere else is one it cannot read.
# Neither enters the cross-section, because `Data/refinery.py` takes membership from the seed.  The
# Data Curator will read FRED in a later release; until then `stage_cash_rate` fetches FRED's own
# published file, which needs no key.
#
# It produces `Data/Curator/Time_Series/<identifier>.parquet`, `m_*` plus `c_*`, in the schema
# `Data/time_series.py` keeps, read by the universe notebook, `Data/refinery.py` and the engine;
# `DFF.parquet` and `KN_US_Equity_Core.parquet` beside them;
# `Data/Curator/fetch_outcomes.json`, the last answer the provider gave for each name; and
# `Data/Curator/adjustment_checks.csv`.

import argparse
import csv
import datetime
import importlib.util
import io
import json
import logging
import os
import pathlib
import socket
import sys
import time
import types
import urllib.request
import zipfile

import numpy
import pandas

import kaxanuk.data_curator
import kaxanuk.data_curator.data_blocks.dividends
import kaxanuk.data_curator.data_blocks.market_daily
import kaxanuk.data_curator.data_blocks.splits
import kaxanuk.data_curator.data_providers
import kaxanuk.data_curator.entities
import kaxanuk.data_curator.output_handlers

# Every per-security file is written and read through one module, so it lives beside this one.
DATA_DIRECTORY = pathlib.Path(__file__).parent
sys.path.insert(0, str(DATA_DIRECTORY))

import time_series  # noqa: E402 - the path above has to exist first

__all__ = [
    "apply_spin_offs",
    "check_adjustments",
    "download_batch",
    "load_custom_calculations",
    "load_hand_supplied",
    "main",
    "read_fetched_through",
    "read_identifiers",
    "read_provider_key",
    "stage_cash_rate",
    "stage_spin_offs",
    "stage_index_price_series",
]

# Sharadar's spin-offs, from the bulk file of its actions table: the one corporate action the
# Curator's dividend column does not carry.  `value` is the spin-off's cash value a share, in
# today's split-adjusted shares, on its ex-date.
ACTIONS_DIRECTORY = pathlib.Path(__file__).parent / "Curator" / "Actions"
ACTIONS_URL = "https://api.sharadar.com/v1.0/data/actions?years=full"
SPIN_OFF_ACTION = "spinoffdividend"
ADJUSTMENT_CHECKS_PATH = pathlib.Path(__file__).parent / "Curator" / "adjustment_checks.csv"
# Where Sharadar's three decimals are fine enough to be compared: a price of ten dollars or more,
# a rounding of five parts in a hundred thousand.  A day whose rebuilt return differs from
# Sharadar's by more than this is a day one of the two adjusted for something the other did not.
CHECK_PRICE_FLOOR = 10.0
CHECK_RETURN_TOLERANCE = 0.005
# A rebuilt split-adjusted close more than this far from Sharadar's is a split one side missed.
SPLIT_CHECK_TOLERANCE = 0.02
# The exchange-traded benchmark the book is reported against beside the index.  It rides in the
# same folder as the universe because the engine prices every identifier from one directory, and
# it never enters the cross-section, because the refinery takes membership from the seed.
BENCHMARK_IDENTIFIERS = ("SPY",)
# Tickers per request: Sharadar answers a batch in one call, and a smaller batch loses less when
# one is refused.
BATCH_SIZE = 25
# The pause between two batches, which keeps a full run well inside the provider's rate limit:
# the account was locked for its speed limit on 2026-10-23, before this run began.
BATCH_PAUSE_SECONDS = 10
# The engine's cash rate: FRED's daily effective federal funds rate, in percent.
CASH_RATE_IDENTIFIER = "DFF"
CASH_RATE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF"
CUSTOM_CALCULATIONS_PATH = pathlib.Path(__file__).parent / "Curator" / "custom_calculations.py"
# A batch the provider refused is asked again after a pause, this many times in all.  A rate
# limit disables the account for minutes, so the pause is long.
DOWNLOAD_ATTEMPTS = 4
# Fixed, not `today`, so two people running a week apart get the same files.  It is the last date
# of the KN US Equity Core and of the factor model the strategy reads.
END_DATE = datetime.date(
    2026,
    8,
    14,
)
# The date each file was last fetched through, so a refresh knows what it has already done.
FETCHED_THROUGH_PATH = pathlib.Path(__file__).parent / "Curator" / "fetched_through.json"
# The provider's last word on each name: `downloaded`, `not carried`, or what refused it.
FETCH_OUTCOMES_PATH = pathlib.Path(__file__).parent / "Curator" / "fetch_outcomes.json"
HAND_SUPPLIED_PATH = pathlib.Path(__file__).parent / "hand_supplied.py"
IDENTIFIER_COLUMN = "main_identifier"
# The index the book is reported against, under the name the engine prices it by. No price
# provider sells it, so it arrives by hand as a daily return series and is rebuilt here as a level
# the engine can price like any other file.
INDEX_IDENTIFIER = "KN_US_Equity_Core"
# Prices are the only block this strategy reads, and they also set the calendar every other column
# is aligned to.
MARKET_DATA_BLOCK = kaxanuk.data_curator.data_blocks.market_daily.MarketDailyDataBlock
# The provider's dividends and splits, which the `c_*` calculations rebuild the adjustment from.
DIVIDENDS_DATA_BLOCK = kaxanuk.data_curator.data_blocks.dividends.DividendsDataBlock
SPLITS_DATA_BLOCK = kaxanuk.data_curator.data_blocks.splits.SplitsDataBlock
OUTPUT_DIRECTORY = pathlib.Path(__file__).parent / "Curator" / "Time_Series"
PROVIDER_KEY_VARIABLE = "KNDC_API_KEY_SHARADAR"
# The words the library logs when a whole batch was refused, as opposed to a name it has no data
# for: an answer about the moment, worth asking again.
REFUSED_BATCH_PHRASES = (
    "could not be downloaded",
    "speed limit",
    "code 429",
)
# The library opens its connections with no timeout of its own, so one that hangs would hang the
# run; this makes it raise instead, and the batch is asked again.
REQUEST_TIMEOUT_SECONDS = 120
RETRY_PAUSE_SECONDS = 600
SEED_PATH = pathlib.Path(__file__).parent.parent / "Universe" / "Investable_Universe.csv"
# Two years before the window opens, so the 200-day average is warm on the first day that counts.
START_DATE = datetime.date(
    1998,
    1,
    2,
)
# The outcomes that leave a name without a file.
UNANSWERED_OUTCOMES = (
    "not carried",
    "refused",
)
# What the pipeline reads, and nothing else: see the module's docstring for each column's job.
OUTPUT_COLUMNS = (
    "m_date",
    "m_open_split_adjusted",
    "m_high_split_adjusted",
    "m_low_split_adjusted",
    "m_close",
    "m_close_split_adjusted",
    "m_close_dividend_and_split_adjusted",
    "m_volume_split_adjusted",
    "d_ex_dividend_date_dividend_split_adjusted",
    "c_split_ratio",
    "c_dividend_and_split_ratio",
    "c_close_dividend_and_split_adjusted",
    "c_open",
    "c_open_dividend_and_split_adjusted",
    "c_log_returns_total",
    "c_traded_value",
    "c_volume_dividend_and_split_adjusted",
)


class _MessageCollector(logging.Handler):
    """
    Keep what the library logs at error level or above during one call, to read why it failed.
    """

    def __init__(self) -> None:
        """
        Start with no messages, at the error level.
        """
        super().__init__(level=logging.ERROR)
        self.messages = []

    def emit(
        self,
        record: "logging.LogRecord",
    ) -> None:
        """
        Keep the formatted message.
        """
        self.messages.append(record.getMessage())


def apply_spin_offs(
    identifier: str,
    spin_offs: "pandas.DataFrame",
) -> bool:
    """
    Add a file's spin-offs to its total return, the way the Curator's calculations add dividends.

    A spin-off pays its holders shares of a new company; Sharadar records their value a share, in
    today's split-adjusted shares, on the ex-date, and leaves it out of the dividend column.  It is
    added to that day's payment, and every column built on the total return is written again with
    the same arithmetic `Data/Curator/custom_calculations.py` uses.  A spin-off dated before or
    after the file's rows changes nothing, and the file is left untouched.
    """
    path = time_series.path_for(OUTPUT_DIRECTORY, identifier)
    frame = time_series.read_frame(path)
    dates = frame["m_date"]
    rows = dates.searchsorted(pandas.to_datetime(spin_offs["date"]))
    inside = (rows > 0) & (rows < len(dates))

    if not inside.any():

        return False

    values = pandas.to_numeric(
        spin_offs["value"],
        errors="coerce",
    ).fillna(0.0)
    spin_off_values = pandas.Series(
        values.to_numpy()[inside],
        index=rows[inside],
    )
    spin_off_by_row = spin_off_values.groupby(level=0).sum()
    spin_off_on_row = spin_off_by_row.reindex(
        range(len(frame)),
        fill_value=0.0,
    )
    close = frame["m_close"].astype(float)
    split_adjusted_close = close * frame["c_split_ratio"].astype(float)
    dividends = pandas.to_numeric(
        frame["d_ex_dividend_date_dividend_split_adjusted"],
        errors="coerce",
    ).fillna(0.0)
    paid = dividends + spin_off_on_row.to_numpy()
    gross_return = (split_adjusted_close + paid) / split_adjusted_close.shift(1)
    clean_return = gross_return.where(
        numpy.isfinite(gross_return) & (gross_return > 0),
        1.0,
    )
    log_return = numpy.log(clean_return.to_numpy())
    log_after = numpy.append(
        numpy.cumsum(log_return[::-1])[::-1][1:],
        0.0,
    )
    total_return_close = pandas.Series(split_adjusted_close.iloc[-1] * numpy.exp(-log_after))
    total_return_ratio = total_return_close / close
    frame["c_close_dividend_and_split_adjusted"] = total_return_close
    frame["c_dividend_and_split_ratio"] = total_return_ratio
    frame["c_open_dividend_and_split_adjusted"] = frame["c_open"].astype(float) * total_return_ratio
    frame["c_log_returns_total"] = numpy.log(total_return_close / total_return_close.shift(1))
    frame["c_volume_dividend_and_split_adjusted"] = (
        frame["c_traded_value"].astype(float) / total_return_close
    )
    time_series.write_frame(
        frame,
        path,
    )

    return True


def check_adjustments(
    identifier: str,
) -> dict[str, object]:
    """
    Read one file back and compare its rebuilt adjustment with Sharadar's own, writing nothing.

    On the days both of Sharadar's prices are at least `CHECK_PRICE_FLOOR` -- where its three
    decimals are fine enough -- it counts the days the rebuilt daily return differs from Sharadar's
    by more than `CHECK_RETURN_TOLERANCE`, a dividend or split one side has and the other has not,
    and the days the rebuilt split-adjusted close is more than `SPLIT_CHECK_TOLERANCE` off
    Sharadar's, a split one side missed.  It also says where the rebuild took Sharadar's constant
    basis and where it corrected volume counted twice.
    """
    frame = time_series.read_frame(time_series.path_for(OUTPUT_DIRECTORY, identifier))
    close = frame["m_close"].astype(float)
    provider_total = frame["m_close_dividend_and_split_adjusted"].astype(float)
    provider_split_close = frame["m_close_split_adjusted"].astype(float)
    rebuilt_total = frame["c_close_dividend_and_split_adjusted"].astype(float)
    split_ratio = frame["c_split_ratio"].astype(float)
    precise = (provider_total >= CHECK_PRICE_FLOOR) & (provider_total.shift(1) >= CHECK_PRICE_FLOOR)
    provider_return = provider_total / provider_total.shift(1)
    rebuilt_return = rebuilt_total / rebuilt_total.shift(1)
    difference = (rebuilt_return - provider_return).abs()
    split_precise = provider_split_close >= CHECK_PRICE_FLOOR
    split_gap = (close * split_ratio / provider_split_close - 1).abs()
    provider_traded_value = provider_split_close * frame["m_volume_split_adjusted"].astype(float)
    volume_factor = (frame["c_traded_value"].astype(float) / provider_traded_value).round(6)
    ratio_change = (split_ratio / split_ratio.shift(1) - 1).abs()
    split_changes = int((ratio_change > 0.01).sum())
    distinct_factors = volume_factor.dropna().nunique()
    volume_corrections = int(distinct_factors - 1)
    largest_difference = (
        float(difference[precise].max())
        if precise.any()
        else 0.0
    )

    return {
        "identifier": identifier,
        "rows": len(frame),
        "splits": split_changes,
        "volume_corrections": volume_corrections,
        "days_compared": int(precise.sum()),
        "days_disagreeing": int((difference[precise] > CHECK_RETURN_TOLERANCE).sum()),
        "largest_difference": largest_difference,
        "split_days_disagreeing": int((split_gap[split_precise] > SPLIT_CHECK_TOLERANCE).sum()),
    }


def download_batch(
    identifiers: tuple[str, ...],
    custom_calculations: "types.ModuleType",
    end_date: "datetime.date",
    fetched_through: dict[str, str],
) -> dict[str, str]:
    """
    Fetch a batch through the end date and say, per identifier, what happened.

    A file with the right header already fetched through this end date is left alone, `skipped`.
    The rest are asked for in one call; a file written is `downloaded`.  When the provider refused
    the batch as a whole -- a rate limit, a timeout -- it is asked again after a pause, and a name
    still without a file after the last attempt is `refused`.  A name missing from a batch the
    provider answered is `not carried`: Sharadar said it has nothing for it.
    """
    outcomes = {}
    pending = []

    for identifier in identifiers:
        if _is_current(
            identifier,
            end_date,
            fetched_through,
        ):
            outcomes[identifier] = "skipped"
        else:
            pending.append(identifier)

    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        if len(pending) == 0:
            break

        before = {
            identifier: _modified_time(identifier)
            for identifier in pending
        }
        logged = _fetch_once(
            tuple(pending),
            custom_calculations,
            end_date,
        )
        written = [
            identifier
            for identifier in pending
            if _modified_time(identifier) not in (None, before[identifier])
        ]

        for identifier in written:
            # The library writes Sharadar's prices as decimals of each file's own precision; one
            # schema for every file is what lets them stack.
            time_series.normalize_file(time_series.path_for(OUTPUT_DIRECTORY, identifier))
            outcomes[identifier] = "downloaded"
            fetched_through[identifier] = end_date.isoformat()

        missing = [
            identifier
            for identifier in pending
            if identifier not in written
        ]
        refused = any(
            phrase in logged
            for phrase in REFUSED_BATCH_PHRASES
        )

        if not refused:
            for identifier in missing:
                outcomes[identifier] = "not carried"

            pending.clear()
            break

        pending[:] = missing
        print(f"batch of {len(pending)} refused, attempt {attempt}: {logged[:160]}", flush=True)

        if attempt < DOWNLOAD_ATTEMPTS:
            time.sleep(RETRY_PAUSE_SECONDS)

    for identifier in pending:
        outcomes[identifier] = "refused"

    return outcomes


def load_custom_calculations() -> "types.ModuleType":
    """
    Import the `c_*` functions by path, because `Data/` is a folder rather than a package.

    The curator resolves a column to a function by attribute name on this module, so nothing here
    registers anything: defining `c_foo` and asking for the column `c_foo` is the whole contract.
    """
    specification = importlib.util.spec_from_file_location(
        "curator_custom_calculations",
        CUSTOM_CALCULATIONS_PATH,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def load_hand_supplied() -> "types.ModuleType":
    """
    Import the reader of the desk's files by path, for the same reason.
    """
    specification = importlib.util.spec_from_file_location(
        "hand_supplied",
        HAND_SUPPLIED_PATH,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def main() -> int:
    """
    Download every identifier in the seed and the benchmark, stage the cash rate and the index.

    Failures are named rather than counted: an identifier the provider does not carry is a hole in
    the panel, and the universe notebook writes it into `Universe/Data_Issues.csv` from the
    outcomes this writes.
    """
    parser = argparse.ArgumentParser(description="Download the seed's time series.")
    parser.add_argument(
        "--end-date",
        default=END_DATE.isoformat(),
        help="the last date to fetch through, ISO; the experiment's end date when omitted",
    )
    parser.add_argument(
        "--refresh-actions",
        action="store_true",
        help="download Sharadar's actions again, not the newest cached file",
    )
    parser.add_argument(
        "--identifiers",
        default="",
        help="a comma-separated subset of the seed; the whole seed when omitted",
    )
    arguments = parser.parse_args()
    end_date = datetime.date.fromisoformat(arguments.end_date)
    kaxanuk.data_curator.load_config_env()
    socket.setdefaulttimeout(REQUEST_TIMEOUT_SECONDS)
    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    custom_calculations = load_custom_calculations()
    requested = tuple(
        identifier.strip()
        for identifier in arguments.identifiers.split(",")
        if identifier.strip()
    )
    everything = read_identifiers() + BENCHMARK_IDENTIFIERS
    identifiers = requested if len(requested) > 0 else everything
    fetched_through = read_fetched_through()
    fetch_outcomes = _read_fetch_outcomes()
    counts = {
        "downloaded": 0,
        "not carried": 0,
        "refused": 0,
        "skipped": 0,
    }

    for start in range(
        0,
        len(identifiers),
        BATCH_SIZE,
    ):
        batch = identifiers[start:start + BATCH_SIZE]
        outcomes = download_batch(
            batch,
            custom_calculations,
            end_date,
            fetched_through,
        )

        for identifier, outcome in outcomes.items():
            counts[outcome] += 1

            if outcome != "skipped":
                fetch_outcomes[identifier] = outcome

        _write_json(
            FETCH_OUTCOMES_PATH,
            fetch_outcomes,
        )
        _write_json(
            FETCHED_THROUGH_PATH,
            fetched_through,
        )
        done = min(
            start + BATCH_SIZE,
            len(identifiers),
        )
        print(f"{done}/{len(identifiers)} through {end_date}: {counts}", flush=True)

        any_work = any(
            outcome != "skipped"
            for outcome in outcomes.values()
        )

        if any_work:
            time.sleep(BATCH_PAUSE_SECONDS)

    unanswered = [
        identifier
        for identifier in identifiers
        if fetch_outcomes.get(identifier) in UNANSWERED_OUTCOMES
    ]

    if len(unanswered) > 0:
        names = ", ".join(
            f"{identifier} ({fetch_outcomes[identifier]})"
            for identifier in unanswered
        )
        print(f"no file for {len(unanswered)}: {names}")

    # Second pass: the spin-offs the Curator's dividend column does not carry, added to the files
    # that had one, then every file read back and checked against Sharadar's own adjustment.
    spin_offs = stage_spin_offs(arguments.refresh_actions)
    spin_offs_grouped = spin_offs.groupby("ticker")
    spin_offs_by_ticker = dict(tuple(spin_offs_grouped))
    adjusted = [
        identifier
        for identifier in identifiers
        if identifier in spin_offs_by_ticker
        and apply_spin_offs(identifier, spin_offs_by_ticker[identifier])
    ]
    adjusted_names = " ".join(adjusted)
    print(f"spin-offs added to {len(adjusted)} files: {adjusted_names}")
    checks = [
        check_adjustments(identifier)
        for identifier in identifiers
        if time_series.path_for(OUTPUT_DIRECTORY, identifier).is_file()
    ]
    checks_table = pandas.DataFrame(checks)
    checks_table.to_csv(
        ADJUSTMENT_CHECKS_PATH,
        index=False,
    )
    disagreeing = checks_table[checks_table["days_disagreeing"] > 0]
    split_disagreeing = checks_table[checks_table["split_days_disagreeing"] > 0]
    summary = "".join([
        f"adjustment checks: {len(checks_table)} files, {len(disagreeing)} with a day that ",
        "disagrees with Sharadar's own adjusted close by more than ",
        f"{CHECK_RETURN_TOLERANCE:.1%}, {len(split_disagreeing)} whose split-adjusted close is ",
        "off Sharadar's",
    ])
    print(summary)
    rate_path = stage_cash_rate(end_date)
    print(f"staged the cash rate as {rate_path.name}, from FRED")
    # The index is KaxaNuk's own and arrives by hand, so a copy without it is told what it lacks
    # rather than handed a traceback after every price has downloaded.
    hand_supplied = load_hand_supplied()
    missing_inputs = hand_supplied.report_missing()
    returns_missing = [
        line
        for line in missing_inputs
        if "index returns" in line
    ]

    if len(returns_missing) == 0:
        index_path = stage_index_price_series(hand_supplied)
        print(f"staged the index as {index_path.name}, rebuilt from its own daily returns")
    else:
        print(f"{INDEX_IDENTIFIER} not staged: {returns_missing[0]}")

    return 0


def read_fetched_through() -> dict[str, str]:
    """
    The date each file was last fetched through, empty before the first refresh.
    """
    if not FETCHED_THROUGH_PATH.is_file():

        return {}

    return json.loads(FETCHED_THROUGH_PATH.read_text(encoding="utf-8"))


def read_identifiers() -> tuple[str, ...]:
    """
    Read the seed, which is the authority on what exists and therefore on what is downloaded.

    Reading it here rather than reading the security master keeps this runnable before the universe
    notebook has ever run -- and that notebook needs these files to profile.
    """
    with SEED_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        identifiers = [
            row[IDENTIFIER_COLUMN].strip()
            for row in reader
            if row.get(IDENTIFIER_COLUMN, "").strip()
        ]

    if len(identifiers) == 0:
        message = f"{SEED_PATH} has no rows: nothing to download"

        raise ValueError(message)

    return tuple(dict.fromkeys(identifiers))


def read_provider_key() -> str:
    """
    Take the provider key from the environment `load_config_env` filled, by name only.

    It is never printed, logged or returned anywhere else: an exposed key is rotated, not edited
    out of a commit.
    """
    api_key = os.environ.get(PROVIDER_KEY_VARIABLE, "")

    if api_key == "":
        message = f"{PROVIDER_KEY_VARIABLE} is empty; fill it in Config/.env"

        raise RuntimeError(message)

    return api_key


def stage_cash_rate(
    end_date: "datetime.date",
) -> "pathlib.Path":
    """
    Write FRED's effective federal funds rate as the engine's rate file, an annual decimal a day.

    FRED publishes it in percent on every calendar day; the engine reads the last observation on or
    before each trading day, so no day sees a rate published after it.  The spread Interactive
    Brokers takes off it, half a point, is the engine's `cash_interest_spread`, not baked in here,
    so the file is FRED's number and nothing else.
    """
    with urllib.request.urlopen(CASH_RATE_URL, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        text = response.read().decode("utf-8")

    published = pandas.read_csv(io.StringIO(text))
    dates = pandas.to_datetime(published[published.columns[0]])
    percent = pandas.to_numeric(
        published[CASH_RATE_IDENTIFIER],
        errors="coerce",
    )
    window = (dates >= pandas.Timestamp(START_DATE)) & (dates <= pandas.Timestamp(end_date))
    staged = pandas.DataFrame({
        "m_date": dates[window].dt.date,
        "rate": (percent[window] / 100).round(6),
    })
    complete = staged.dropna()
    path = time_series.path_for(OUTPUT_DIRECTORY, CASH_RATE_IDENTIFIER)
    time_series.write_frame(
        complete,
        path,
    )

    return path


def stage_index_price_series(
    hand_supplied: "types.ModuleType",
) -> "pathlib.Path":
    """
    Rebuild the index as a price level from its own daily returns, beside the securities.

    The backtest engine resolves every identifier against one market-data directory, so a benchmark
    filed anywhere else is a benchmark it cannot price.  The level starts at 100 and means nothing
    on its own: only its returns are ever read.  A benchmark is never traded, so the two open
    columns the engine asks for by name are the level itself.
    """
    returns = hand_supplied.read_benchmark_returns()
    growth = 1 + returns.fillna(0.0)
    level = growth.cumprod() * 100
    staged = pandas.DataFrame({
        "m_date": returns.index.date,
        "m_close": level.to_numpy(),
        "m_close_dividend_and_split_adjusted": level.to_numpy(),
        "c_close_dividend_and_split_adjusted": level.to_numpy(),
        "c_open": level.to_numpy(),
        "c_open_dividend_and_split_adjusted": level.to_numpy(),
    })
    path = time_series.path_for(OUTPUT_DIRECTORY, INDEX_IDENTIFIER)
    time_series.write_frame(
        staged,
        path,
    )

    return path


def stage_spin_offs(
    refresh: bool,
) -> "pandas.DataFrame":
    """
    Sharadar's spin-offs: the newest cached actions file, or today's from its bulk download.

    The bulk file is the whole actions table, cached under the date it was fetched in
    `Data/Curator/Actions/`, so a rebuild reads the same answer; only its spin-offs are read.  The
    key travels in a header.
    """
    cached = sorted(ACTIONS_DIRECTORY.glob("sharadar_actions_*.csv"))

    if len(cached) > 0 and not refresh:
        everything = pandas.read_csv(
            cached[-1],
            dtype=str,
            keep_default_na=False,
        )

        return everything[everything["action"] == SPIN_OFF_ACTION]

    request = urllib.request.Request(
        ACTIONS_URL,
        headers={"x-api-key": read_provider_key()},
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS * 5) as response:
        archive = response.read()

    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        member = bundle.namelist()[0]

        with bundle.open(member) as handle:
            downloaded = pandas.read_csv(
                handle,
                dtype=str,
                keep_default_na=False,
            )

    ACTIONS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    downloaded.to_csv(
        ACTIONS_DIRECTORY / f"sharadar_actions_{datetime.date.today().isoformat()}.csv",
        index=False,
        lineterminator="\n",
    )

    return downloaded[downloaded["action"] == SPIN_OFF_ACTION]


def _fetch_once(
    identifiers: tuple[str, ...],
    custom_calculations: "types.ModuleType",
    end_date: "datetime.date",
) -> str:
    """
    One call to the library for a batch, returning what it logged at error level, or nothing.

    The library logs a provider's refusal and returns normally, so the call is read through what it
    logged.  A connection that raises is reported the same way, by its type.
    """
    configuration = kaxanuk.data_curator.entities.Configuration(
        start_date=START_DATE,
        end_date=end_date,
        period="quarterly",
        identifiers=identifiers,
        columns=OUTPUT_COLUMNS,
    )
    provider = kaxanuk.data_curator.data_providers.Sharadar(
        api_key=read_provider_key(),
    )
    output_handler = kaxanuk.data_curator.output_handlers.ParquetOutput(
        output_base_dir=str(OUTPUT_DIRECTORY),
    )
    collector = _MessageCollector()
    library_logger = logging.getLogger("kaxanuk")
    library_logger.addHandler(collector)

    try:
        kaxanuk.data_curator.main(
            configuration=configuration,
            output_handlers=[output_handler],
            custom_calculation_modules=[custom_calculations],
            data_block_providers={
                MARKET_DATA_BLOCK: provider,
                DIVIDENDS_DATA_BLOCK: provider,
                SPLITS_DATA_BLOCK: provider,
            },
            master_clock_data_block=MARKET_DATA_BLOCK,
            logger_level=logging.WARNING,
        )
    except OSError as error:

        return f"could not be downloaded: {type(error).__name__}"
    finally:
        library_logger.removeHandler(collector)

    return " ".join(collector.messages)


def _is_current(
    identifier: str,
    end_date: "datetime.date",
    fetched_through: dict[str, str],
) -> bool:
    """
    Whether the file on disk already has this schema and was fetched through this end date.
    """
    output_path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

    if not output_path.is_file():

        return False

    header = time_series.read_column_names(output_path)
    remembered = fetched_through.get(
        identifier,
        "",
    )

    return tuple(header) == OUTPUT_COLUMNS and remembered == end_date.isoformat()


def _modified_time(
    identifier: str,
) -> float | None:
    """
    When the identifier's file was last written, or None when there is none.
    """
    output_path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

    if not output_path.is_file():

        return None

    return output_path.stat().st_mtime


def _read_fetch_outcomes() -> dict[str, str]:
    """
    The provider's last word on each name, empty before the first run.
    """
    if not FETCH_OUTCOMES_PATH.is_file():

        return {}

    return json.loads(FETCH_OUTCOMES_PATH.read_text(encoding="utf-8"))


def _write_json(
    path: "pathlib.Path",
    content: dict[str, str],
) -> None:
    """
    Write a small record as sorted JSON, so a rerun's diff reads as what changed.
    """
    text = json.dumps(
        content,
        indent=1,
        sort_keys=True,
    )
    path.write_text(
        text,
        encoding="utf-8",
    )


if __name__ == "__main__":
    sys.exit(main())

# --- example: end ---
