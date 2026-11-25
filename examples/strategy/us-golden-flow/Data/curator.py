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
- Point its output at `Data/Curator/Time_Series/`, one CSV file per identifier -- the format the
  KaxaNuk app and the engine read -- written and read through `Data/time_series.py`.  The library's
  default folder is `Output/`; here every stage has one home, and this is the Curator's.
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

It produces `Data/Curator/Time_Series/<identifier>.csv`, `m_*` plus `c_*`, read by the universe
notebook, `Data/refinery.py`, the engine and the KaxaNuk app; and in `Data/Curator/` the provider's
last answer for each name and the date each file was fetched through.

It prevents beautiful results that came from broken inputs -- and a dataset nobody else can
rebuild.
"""

# --- example: begin ---

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
import kaxanuk.data_curator.data_blocks.fundamentals
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
    "complete_files",
    "download_batch",
    "load_custom_calculations",
    "load_hand_supplied",
    "main",
    "read_fetched_through",
    "read_identifiers",
    "read_provider_key",
    "read_spans",
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
# of the window the owner set on 2026-11-16, inside the KN US Equity Core and the factor model.
END_DATE = datetime.date(
    2026,
    10,
    31,
)
# Where the price files are written: the experiments' folder, or the one a caller names in
# `CURATOR_OUTPUT_DIRECTORY` so that its refresh never moves the experiments' inputs.
OUTPUT_DIRECTORY = pathlib.Path(
    os.environ.get(
        "CURATOR_OUTPUT_DIRECTORY",
        str(pathlib.Path(__file__).parent / "Curator" / "Time_Series"),
    )
)
# The date each file was last fetched through, so a refresh knows what it has already done; it
# lives beside the folder it describes.
FETCHED_THROUGH_PATH = OUTPUT_DIRECTORY.parent / "fetched_through.json"
# The provider's last word on each name: `downloaded`, `not carried`, or what refused it.
FETCH_OUTCOMES_PATH = OUTPUT_DIRECTORY.parent / "fetch_outcomes.json"
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
# The quarterly statements, downloaded for later experiments and for `c_market_cap`.
FUNDAMENTALS_DATA_BLOCK = kaxanuk.data_curator.data_blocks.fundamentals.FundamentalsDataBlock
SPLITS_DATA_BLOCK = kaxanuk.data_curator.data_blocks.splits.SplitsDataBlock
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
# The checks of each file's rebuilt adjustment, beside the folder they check.
ADJUSTMENT_CHECKS_PATH = OUTPUT_DIRECTORY.parent / "adjustment_checks.csv"
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
    "s_split_date_numerator",
    "s_split_date_denominator",
    # The statements' dates: the filing a row carries, and the period it reports.
    "f_filing_date",
    "f_fiscal_period",
    "f_fiscal_year",
    "f_period_end_date",
    "f_reported_currency",
    "fis_basic_earnings_per_share",
    "fis_basic_net_income_available_to_common_stockholders",
    "fis_cost_of_revenue",
    "fis_depreciation_and_amortization",
    "fis_diluted_earnings_per_share",
    "fis_discontinued_operations_income_after_tax",
    "fis_earnings_before_interest_and_tax",
    "fis_earnings_before_interest_tax_depreciation_and_amortization",
    "fis_gross_profit",
    "fis_income_before_tax",
    "fis_income_tax_expense",
    "fis_interest_expense",
    "fis_net_income",
    "fis_net_income_deductions",
    "fis_operating_expenses",
    "fis_operating_income",
    "fis_research_and_development_expense",
    "fis_revenues",
    "fis_selling_general_and_administrative_expense",
    "fis_weighted_average_basic_shares_outstanding",
    "fis_weighted_average_diluted_shares_outstanding",
    "fbs_accumulated_other_comprehensive_income_after_tax",
    "fbs_assets",
    "fbs_cash_and_cash_equivalents",
    "fbs_current_accounts_payable",
    "fbs_current_assets",
    "fbs_current_liabilities",
    "fbs_current_net_receivables",
    "fbs_deferred_revenue",
    "fbs_investments",
    "fbs_liabilities",
    "fbs_longterm_debt",
    "fbs_longterm_investments",
    "fbs_net_intangible_assets_including_goodwill",
    "fbs_net_inventory",
    "fbs_net_property_plant_and_equipment",
    "fbs_noncurrent_assets",
    "fbs_noncurrent_deferred_tax_assets",
    "fbs_noncurrent_deferred_tax_liabilities",
    "fbs_noncurrent_liabilities",
    "fbs_retained_earnings",
    "fbs_shortterm_debt",
    "fbs_shortterm_investments",
    "fbs_stockholder_equity",
    "fbs_total_debt_including_capital_lease_obligations",
    "fcf_capital_expenditure",
    "fcf_cash_and_cash_equivalents_change",
    "fcf_cash_exchange_rate_effect",
    "fcf_depreciation_and_amortization",
    "fcf_dividend_payments",
    "fcf_free_cash_flow",
    "fcf_net_business_acquisition_payments",
    "fcf_net_cash_from_financing_activities",
    "fcf_net_cash_from_investing_activities",
    "fcf_net_cash_from_operating_activities",
    "fcf_net_common_stock_issuance_proceeds",
    "fcf_net_debt_issuance_proceeds",
    "fcf_net_income",
    "fcf_other_investing_activities",
    "fcf_stock_based_compensation",
    # The library's own market capitalisation, which the KaxaNuk app sizes a universe by.
    "c_market_cap",
    "c_split_ratio",
    "c_dividend_and_split_ratio",
    "c_close_dividend_and_split_adjusted",
    "c_open",
    "c_open_dividend_and_split_adjusted",
    "c_log_returns_total",
    "c_traded_value",
    "c_volume_dividend_and_split_adjusted",
    # Every signal Experiment 1 reads, per security, so the KaxaNuk app shows them beside the
    # prices: the rule's cross and score, and their sweep neighbours.
    "c_golden_cross_20_100",
    "c_golden_cross_50_200",
    "c_golden_cross_100_300",
    "c_traded_value_sma_21d",
    "c_traded_value_sma_63d",
    "c_traded_value_sma_126d",
)
# What `complete_files` adds after the download, from the index's holdings, which no provider
# serves: the Core's weight that day, and the book's point-in-time universe.
COMPLETION_COLUMNS = (
    "c_index_weight",
    "c_eligible_golden_cross_50_200",
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


def complete_files() -> int:
    """
    Finish every seed listing's file with what no provider serves; the count of files finished.

    Three things, in order, on every run, whether a file was downloaded now or before:

    - **Cut to the listing's dates in the seed**, both ends included, so a ticker another company
      took before or after never speaks for this one.
    - **The window columns computed again on the cut file**, with the same helpers the Curator's
      `c_*` functions use, so no average reaches across the cut, and every cross reads the close
      the spin-offs left.
    - **`c_index_weight`**, the KN US Equity Core's weight that day through the seed's keys, 0 on a
      day it is not a member or the holdings do not cover; and
      **`c_eligible_golden_cross_50_200`**, 1 when the listing was a member with
      `c_golden_cross_50_200` at 1 at its prior close -- the book's point-in-time universe on that
      day, read from nothing on the day itself.

    A column an earlier version of this pass wrote, and this one does not, is dropped: the file
    ends with exactly the downloaded columns and these two.

    The benchmarks and the cash rate are not in the seed and are left as downloaded.
    """
    calculations = load_custom_calculations()
    hand_supplied = load_hand_supplied()
    holdings = hand_supplied.read_member_holdings()
    holdings.index = pandas.to_datetime(holdings.index)
    spans = read_spans()
    completed = []

    for identifier in read_identifiers():
        path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

        if not path.is_file():
            continue

        weights = holdings[identifier] if identifier in holdings.columns else None
        _complete_file(
            path,
            spans.get(identifier, ("", "")),
            weights,
            calculations,
        )
        completed.append(identifier)

    return len(completed)


def download_batch(
    identifiers: tuple[str, ...],
    custom_calculations: "types.ModuleType",
    end_date: "datetime.date",
    fetched_through: dict[str, str],
    spans: dict[str, tuple[str, str]],
) -> dict[str, str]:
    """
    Fetch a batch through the end date and say, per identifier, what happened.

    A file with the right header already fetched through this end date is left alone, `skipped`;
    a delisted listing whose file already reaches the end of its span is left alone, `final`.
    The rest are asked for in one call; a file written is `downloaded`, unless the listing is
    delisted and the file holds no date inside its span, when the earlier file is put back and the
    outcome is `recycled ticker`.  When the provider refused
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
        elif _is_final(
            identifier,
            spans,
        ):
            outcomes[identifier] = "final"
        else:
            pending.append(identifier)

    kept = {
        identifier: _read_bytes(identifier)
        for identifier in pending
    }

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

            if _outside_span(identifier, spans):
                _restore(identifier, kept[identifier])
                outcomes[identifier] = "recycled ticker"
                print(f"{identifier}: no row inside its span; another security's file, refused")

                continue

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
    spans = read_spans()
    counts = {
        "downloaded": 0,
        "final": 0,
        "not carried": 0,
        "recycled ticker": 0,
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
            spans,
        )

        for identifier, outcome in outcomes.items():
            counts[outcome] += 1

            if outcome not in ("skipped", "final"):
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
            outcome not in ("skipped", "final")
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
    # Third pass: every listing's file cut to its dates in the seed, its windows computed again on
    # what is left, and the index's weight and the book's universe added.
    completed = complete_files()
    print(f"completed {completed} files: cut to their spans, with {', '.join(COMPLETION_COLUMNS)}")
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


def read_spans() -> dict[str, tuple[str, str]]:
    """
    Each listing's span in the seed, `valid_from` and `valid_to`, the second empty while it trades.

    A listing with a `valid_to` is delisted: its history no longer moves, and its ticker is one the
    provider may give to another company.
    """
    with SEED_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        spans = {
            row[IDENTIFIER_COLUMN].strip(): (
                row.get("valid_from", "").strip(),
                row.get("valid_to", "").strip(),
            )
            for row in reader
            if row.get(IDENTIFIER_COLUMN, "").strip()
        }

    return spans


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


def _complete_file(
    path: "pathlib.Path",
    span: tuple[str, str],
    weights: "pandas.Series | None",
    calculations: "types.ModuleType",
) -> None:
    """
    One file finished, as `complete_files` says: cut, windows again, weight and universe added.
    """
    frame = time_series.read_frame(path)
    dates = pandas.to_datetime(frame["m_date"])
    valid_from, valid_to = span
    start = pandas.Timestamp(valid_from) if valid_from else dates.min()
    end = pandas.Timestamp(valid_to) if valid_to else dates.max()
    inside = (dates >= start) & (dates <= end)
    cut = frame.loc[inside].reset_index(drop=True)
    cut_dates = dates.loc[inside].reset_index(drop=True)
    prices = cut["c_close_dividend_and_split_adjusted"].astype(float)
    traded_value = cut["c_traded_value"].astype(float)

    for column, (short_window, long_window) in calculations.GOLDEN_CROSS_WINDOWS.items():
        cut[column] = calculations.golden_cross_of_closes(
            prices,
            short_window,
            long_window,
        )

    for column, window in calculations.TRADED_VALUE_WINDOWS.items():
        cut[column] = calculations.traded_value_average(
            traded_value,
            window,
        )

    if weights is None:
        index_weight = pandas.Series(0.0, index=cut.index)
    else:
        on_dates = weights.reindex(cut_dates.to_numpy())
        weight_values = on_dates.to_numpy()
        index_weight = pandas.Series(weight_values, index=cut.index).fillna(0.0)

    cut["c_index_weight"] = index_weight
    member_and_crossed = (index_weight > 0) & (cut["c_golden_cross_50_200"] == 1)
    before = member_and_crossed.shift(
        1,
        fill_value=False,
    )
    cut["c_eligible_golden_cross_50_200"] = before.astype(float)
    finished = cut[[*OUTPUT_COLUMNS, *COMPLETION_COLUMNS]]
    time_series.write_frame(
        finished,
        path,
    )


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
    output_handler = kaxanuk.data_curator.output_handlers.CsvOutput(
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
                FUNDAMENTALS_DATA_BLOCK: provider,
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

    # The downloaded columns decide it; what `complete_files` adds after them it writes again.
    downloaded = tuple(header[:len(OUTPUT_COLUMNS)])

    return downloaded == OUTPUT_COLUMNS and remembered == end_date.isoformat()


def _is_final(
    identifier: str,
    spans: dict[str, tuple[str, str]],
) -> bool:
    """
    Whether a delisted listing's file, with this schema, already reaches the end of its span.
    """
    valid_to = spans.get(
        identifier,
        ("", ""),
    )[1]
    output_path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

    if valid_to == "" or not output_path.is_file():

        return False

    header = time_series.read_column_names(output_path)

    if tuple(header) != OUTPUT_COLUMNS:

        return False

    dates = time_series.read_frame(output_path)["m_date"].astype(str)

    return len(dates) > 0 and dates.max() >= valid_to


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


def _outside_span(
    identifier: str,
    spans: dict[str, tuple[str, str]],
) -> bool:
    """
    Whether a delisted listing's file holds no date inside its span: another security's answer.
    """
    valid_from, valid_to = spans.get(
        identifier,
        ("", ""),
    )

    if valid_to == "":

        return False

    dates = time_series.read_frame(time_series.path_for(OUTPUT_DIRECTORY, identifier))["m_date"]
    text_dates = dates.astype(str)
    inside = (text_dates >= (valid_from or "0000")) & (text_dates <= valid_to)

    return not bool(inside.any())


def _read_bytes(
    identifier: str,
) -> bytes | None:
    """
    A file's bytes before a fetch, so an answer that is not this listing's can be undone.
    """
    output_path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

    if not output_path.is_file():

        return None

    return output_path.read_bytes()


def _read_fetch_outcomes() -> dict[str, str]:
    """
    The provider's last word on each name, empty before the first run.
    """
    if not FETCH_OUTCOMES_PATH.is_file():

        return {}

    return json.loads(FETCH_OUTCOMES_PATH.read_text(encoding="utf-8"))


def _restore(
    identifier: str,
    content: bytes | None,
) -> None:
    """
    Put a file back as it was before a fetch, or remove the one a fetch wrote where none was.
    """
    output_path = time_series.path_for(OUTPUT_DIRECTORY, identifier)

    if content is None:
        output_path.unlink(missing_ok=True)

        return

    output_path.write_bytes(content)


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
