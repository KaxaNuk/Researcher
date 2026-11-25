"""
Backtest engine -- step 5 of 8, the third shared module.  The one path from a book of weights to a
performance number, through the KaxaNuk Backtest Engine.

In plain words: the simulation, run by the engine, with costs and without peeking ahead.

Runs inside an experiment notebook, section 4, after the book has been written to `Portfolio/`.

What is expected here:

- Write the weight file the engine reads: `Portfolio/portfolio_weights.csv`, wide, keyed by the
  identifier the market-data files are named by, dates across the columns, every column summing to
  at most 1.0.  Since 0.16.0 there is no cash fund: what the rule leaves uninvested stays as **US
  dollar cash** in the engine, which pays it the cash rate named below, less the spread a broker
  keeps, as Interactive Brokers pays on a dollar balance.  A security that changed identifier
  mid-history occupies two rows, each non-zero only while that listing was live.
- Price every cost inside the engine, never beside it: commission in basis points of the notional
  traded, slippage from the engine's own spread-and-impact model on the day's high, low and volume,
  the interest the cash earns from a rate file in the market-data folder, and a delisted position
  sold at its last price.
- Run the licensed engine and read its results back: the daily series it marks, the book's daily
  weights as it held them -- the input step 6 needs -- and its summary statistics.  Import it
  inside a guard -- it installs from a licensed index, not PyPI -- and report and skip when it is
  absent, so a clone without a licence still produces everything except the numbers.
- Name the benchmarks a strategy is reported against, in one place, and clip the window to the
  shortest of them up front rather than discovering it as an error.
- Align every variant of an experiment onto one common window before ranking them.  A variant that
  starts a year later is not comparable on its own dates.

There is deliberately no second, lighter simulator here or anywhere.  One that disagrees with the
engine lets the reader pick the number they prefer, and every figure quoted in `RESULTS.md` comes
through this module.

It produces `Backtest/` -- the engine's workbook and the series drawn from it, the daily weights
among them -- for `FINDINGS_N.md` to record and `attribution_analysis.py` to read.

It prevents paper returns that real trading would have erased, and a difference in cost model or
window showing up as strategy skill.
"""


import concurrent.futures
import dataclasses
import datetime
import decimal
import enum
import hashlib
import importlib.util
import json
import os
import pathlib
import sys
import tempfile

import pandas
import pyarrow.csv
import pyarrow.parquet

# Every per-security file is read through the one module that writes it, in `Data/`.
DATA_DIRECTORY = pathlib.Path(__file__).parent.parent / "Data"
sys.path.insert(0, str(DATA_DIRECTORY))

import time_series  # noqa: E402 - the path above has to exist first

__all__ = [
    "BENCHMARK_IDENTIFIERS",
    "CASH_INTEREST_SPREAD",
    "CASH_RATE_IDENTIFIER",
    "COMMISSION_PRICE_COLUMN",
    "ENGINE_INSTALLED",
    "EXECUTION_PRICE_COLUMN",
    "INDEX_IDENTIFIER",
    "MARKET_DATA_DIRECTORY",
    "align_variants",
    "build_configuration",
    "describe_window",
    "earliest_priceable_date",
    "open_dashboard",
    "price_book",
    "price_books",
    "price_batch",
    "read_daily_weights",
    "run_backtest",
    "stage_market_data",
    "write_weight_file",
]

# The benchmarks the book is reported against -- the KN US Equity Core first, staged into the
# market-data folder as a price series, then SPY.  Named here and nowhere else, so switching either
# is one edit and no notebook carries a file name.  The engine takes several benchmarks as one
# comma-separated name, and the first is the one every alpha and information ratio it reports is
# measured against; attribution compares the book against that index and no other.
BENCHMARK_IDENTIFIERS = (
    "KN_US_Equity_Core",
    "SPY",
)
# The rate the engine pays the book's cash at, and the risk-free rate of its Sharpe ratios: FRED's
# effective federal funds rate, staged by `Data/curator.py` as a rate file beside the prices.
CASH_RATE_IDENTIFIER = "DFF"
# Interactive Brokers pays a dollar balance the benchmark rate less half a point, never below zero.
CASH_INTEREST_SPREAD = -0.005
# The engine installs from a licensed index rather than PyPI, so a clone without it still runs
# every other step and says which one it skipped.
ENGINE_INSTALLED = importlib.util.find_spec("kaxanuk.backtest_engine") is not None
# The fill, on the total-return series every return in the experiment uses: the day's open, a
# market-on-open order on the first trading day after the signal's close.  Commission and the order
# ticket are written in the unadjusted open.
COMMISSION_PRICE_COLUMN = "c_open"
EXECUTION_PRICE_COLUMN = "c_open_dividend_and_split_adjusted"
# The day's range and volume the engine's spread and impact model reads: the range is a ratio, so
# split-adjusted prices give the same estimate as the tape, and the volume is on the fill's basis.
CLOSE_COLUMN = "m_close_split_adjusted"
HIGH_COLUMN = "m_high_split_adjusted"
LOW_COLUMN = "m_low_split_adjusted"
VOLUME_COLUMN = "c_volume_dividend_and_split_adjusted"
INDEX_IDENTIFIER = BENCHMARK_IDENTIFIERS[0]
# The books one batch prices: the engine loads the market data once per batch, then prices each
# book in about ten seconds, so a batch is sized to keep a load worth its books while several run
# side by side.
BOOKS_PER_BATCH = 12
# The curated files, Parquet, and the engine's copy of them: the columns it reads, as CSV, because
# its Parquet reader refuses these files on 0.66.0 (reported to the engine).  The copy is written
# again whenever a curated file is newer than it.
CURATED_DIRECTORY = DATA_DIRECTORY / "Curator" / "Time_Series"
MARKET_DATA_DIRECTORY = DATA_DIRECTORY / "Curator" / "Engine"
# The columns the engine reads, in its roles below, and the cash rate's own.
MARKET_DATA_COLUMNS = (
    "m_date",
    "c_open",
    "c_open_dividend_and_split_adjusted",
    "c_close_dividend_and_split_adjusted",
    "m_close_split_adjusted",
    "m_high_split_adjusted",
    "m_low_split_adjusted",
    "c_volume_dividend_and_split_adjusted",
    "rate",
)
# The licence file, loaded by its own path before a worker leaves the repository's folder.
ENVIRONMENT_PATH = pathlib.Path(__file__).parent.parent / "Config" / ".env"
# The engine parses weights as fixed-scale decimals and refuses a value it cannot hold exactly, so
# a third written as 0.3333333333333333 fails before the first fill.  Six places is a hundredth of
# a basis point, far below anything a book can trade.
WEIGHT_DECIMALS = 6


def align_variants(
    returns_by_variant: dict[str, "pandas.Series"],
) -> dict[str, "pandas.Series"]:
    """
    Clip every variant to the window they all share, before any of them are ranked.

    A variant that starts a year later is not comparable on its own dates, and the difference shows
    up as skill.
    """
    first_dates = [
        series.index.min()
        for series in returns_by_variant.values()
    ]
    last_dates = [
        series.index.max()
        for series in returns_by_variant.values()
    ]
    common_start = max(first_dates)
    common_end = min(last_dates)

    return {
        name: series.loc[common_start:common_end]
        for name, series in returns_by_variant.items()
    }


def build_configuration(
    experiment_directory: "pathlib.Path",
    start_date: "datetime.date",
    end_date: "datetime.date",
    initial_capital: int,
    commission_basis_points: float,
    slippage_model: str,
    slippage_basis_points: float,
    cash_reserve_percentage: float,
    portfolio_name: str = "portfolio_weights",
    benchmark_identifiers: tuple[str, ...] = BENCHMARK_IDENTIFIERS,
    execution_price_column: str = EXECUTION_PRICE_COLUMN,
    spread_estimator: str = "corwin_schultz",
) -> object:
    """
    Describe the simulation, including which column of the market data plays which role.

    The roles are declared rather than inferred from a column's name, which is what lets commission
    be charged on the unadjusted price while the fill and the mark run on the total-return series.
    Costs are arguments because a result is accepted net or not at all, and a default nobody chose
    is how a cost assumption goes unexamined.  Commission is in basis points of the notional, and
    slippage is either the engine's spread-and-impact model, with `slippage_basis_points` as the
    half-spread it falls back on where a day's range is missing, or a flat number of basis points.

    The cash reserve is an argument for a different reason: weights summing to exactly one leave
    nothing to pay commission with, and the engine fails at the first rebalance rather than
    quietly overdrawing.  A real book holds the same buffer for the same reason, and here it earns
    the cash rate like any other dollar of cash.

    The benchmarks are an argument for a paper book: the index arrives by hand and can lag the day,
    and a run past its last date has to be priced against a benchmark that reached it.  The fill
    price is one so the same configuration can price a check filled at the close.
    """
    import kaxanuk.backtest_engine.entities

    return kaxanuk.backtest_engine.entities.Configuration(
        initial_capital=initial_capital,
        start_date=start_date,
        end_date=end_date,
        cash_reserve_percentage=cash_reserve_percentage,
        commission_basis_points=commission_basis_points,
        # The engine asks for a per-share rate whatever the model; basis points leave it unused.
        commission_cents=0.0,
        commission_model="basis_points",
        market_data_input_format="csv",
        portfolio_name=portfolio_name,
        portfolio_input_format="csv",
        benchmark_file_name=",".join(benchmark_identifiers),
        input_market_data_directory=str(MARKET_DATA_DIRECTORY),
        input_portfolio_directory=str(experiment_directory / "Portfolio"),
        backtest_results_output_directory=str(experiment_directory / "Backtest"),
        user_column_date="m_date",
        # Commission and the order's share count are written in the price a person paid that day.
        user_column_commission_price=COMMISSION_PRICE_COLUMN,
        # Fills and marks run on the total-return series every return in the experiment uses.
        user_column_trade_execution_price=execution_price_column,
        user_column_mark_to_market_price="c_close_dividend_and_split_adjusted",
        # A rebalance date that is not a trading day moves to the next one rather than failing.
        rebalance_date_handling="next_trading_day",
        # A position in a security whose prices stop is sold at its last price.  With Sharadar that
        # is the last trade, often over the counter after the exchange dropped the name, and the
        # sale is booked on that day: no day of hindsight is needed.
        delisted_position_handling="sell_at_last_price",
        slippage_model=slippage_model,
        slippage_basis_points=slippage_basis_points,
        user_column_high=HIGH_COLUMN,
        user_column_low=LOW_COLUMN,
        user_column_volume=VOLUME_COLUMN,
        # The spread estimate, from the day's range; Abdi and Ranaldo's also reads the close.
        spread_estimator=spread_estimator,
        user_column_close=CLOSE_COLUMN,
        # The cash rate, read from the file of that name in the market-data folder, the last
        # observation on or before each day; the spread is what the broker keeps.
        financing_benchmark_rate=CASH_RATE_IDENTIFIER,
        cash_interest_spread=CASH_INTEREST_SPREAD,
    )


def describe_window(
    result: object,
    end_date: "datetime.date",
) -> str:
    """
    Compare the window the engine actually valued with the one it was asked for.

    A run that stops valuing the book partway still returns success and still summarises cleanly
    over the stub.  This is the check that catches it, and a variant that fails it is excluded by
    name with its reason rather than quietly dropped.
    """
    valued_end = result.data.get("end_date")
    years = result.data.get("years")

    if valued_end is None:

        return "the engine returned no end date: treat every figure from this run as unverified"

    valued_date = pandas.Timestamp(valued_end).date()

    if valued_date < end_date - datetime.timedelta(days=7):

        return f"TRUNCATED: valued to {valued_date}, asked for {end_date} ({years} years)"

    return f"complete: valued to {valued_date} ({years} years)"


def earliest_priceable_date() -> "pandas.Timestamp":
    """
    The first date on which every benchmark has a price and the cash rate has an observation.

    A book cannot start before the instruments it is measured against, nor before the rate its cash
    earns: the engine fails on a position it cannot price, and it fails in the middle of a
    data-integrity check rather than at the window it was given.  Clipping here means the window
    is a decision rather than a crash — and the reason is a fact about an instrument, not about
    the strategy.
    """
    first_dates = []

    for identifier in (*BENCHMARK_IDENTIFIERS, CASH_RATE_IDENTIFIER):
        path = time_series.path_for(CURATED_DIRECTORY, identifier)
        dates = time_series.read_frame(
            path,
            ("m_date",),
        )["m_date"]
        first_dates.append(dates.min())

    return max(first_dates)


def open_dashboard(
    experiment_directory: "pathlib.Path",
    configuration: object,
    port: int = 8052,
) -> object:
    """
    Price one book again and serve the engine's own dashboard for it, until the kernel stops.

    It is a way to look at a run, never a source of numbers: the figures the experiment reports
    come from `run_backtest`, and this blocks, so no pipeline calls it.
    """
    if not ENGINE_INSTALLED:
        missing_engine_message = "the KaxaNuk Backtest Engine is not installed: no dashboard"

        raise ModuleNotFoundError(missing_engine_message)

    import matplotlib

    # The engine draws its report's figures too; off the main thread a window would fail.
    matplotlib.use("Agg")

    import kaxanuk.backtest_engine
    import kaxanuk.backtest_engine.input_handlers

    kaxanuk.backtest_engine.load_config_env()
    csv_input = kaxanuk.backtest_engine.input_handlers.CsvInput(
        input_dir=str(MARKET_DATA_DIRECTORY),
    )
    portfolio_input = kaxanuk.backtest_engine.input_handlers.CsvPortfolioInputHandler(
        str(experiment_directory / "Portfolio"),
    )

    return kaxanuk.backtest_engine.main(
        configuration=configuration,
        input_handlers=[csv_input],
        portfolio_handlers=[portfolio_input],
        logger_file=None,
        launch_dashboard=True,
        dashboard_port=port,
    )


def price_batch(
    tasks: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    """
    Price books that share every setting but their weights, in one run of the engine's batch mode.

    Written to run in a worker process: it takes and returns plain objects.  The weights travel
    inline, read from the files the notebook wrote, so the engine reads no portfolio file; every
    book's answer is cached under the hash of its weight file and its settings.
    """
    import kaxanuk.backtest_engine
    import kaxanuk.backtest_engine.backtest
    import kaxanuk.backtest_engine.config_handlers
    import kaxanuk.backtest_engine.input_handlers.csv_input

    first = tasks[0]
    experiment_directory = pathlib.Path(str(first["experiment_directory"]))
    end_date = datetime.date.fromisoformat(str(first["end"]))
    configuration = build_configuration(
        experiment_directory,
        datetime.date.fromisoformat(str(first["start"])),
        end_date,
        int(first["initial_capital"]),
        float(first["commission_basis_points"]),
        str(first["slippage_model"]),
        float(first["slippage_basis_points"]),
        float(first["cash_reserve_percentage"]),
        str(first["portfolio_name"]),
        tuple(first.get("benchmark_identifiers", BENCHMARK_IDENTIFIERS)),
        str(first.get("execution_price_column", EXECUTION_PRICE_COLUMN)),
        str(first.get("spread_estimator", "corwin_schultz")),
    )
    defaults = _batch_defaults(configuration)
    portfolios = [
        {
            "name": str(task["portfolio_name"]),
            "inline_weights": _inline_weights(_weight_path(task)),
        }
        for task in tasks
    ]
    kaxanuk.backtest_engine.load_config_env(ENVIRONMENT_PATH)
    home = pathlib.Path.cwd()

    # The engine draws into its working folder; each batch gets a folder of its own, and the
    # batch's output folder is there too, since no report is asked of it.
    with tempfile.TemporaryDirectory() as scratch:
        os.chdir(scratch)

        try:
            parser = kaxanuk.backtest_engine.config_handlers.BatchConfigParser
            batch_configuration = parser.parse_dict({
                "global_defaults": defaults,
                "portfolios": portfolios,
                "output": {
                    "directory": scratch,
                    "batch_name": "batch",
                    "ranking_metric": "sharpe_ratio",
                },
            })
            market_data = kaxanuk.backtest_engine.input_handlers.csv_input.CsvInput(
                input_dir=str(MARKET_DATA_DIRECTORY),
            )
            backtester = kaxanuk.backtest_engine.backtest.MultiPortfolioBacktester(
                input_handlers=[market_data],
                portfolio_handlers=[],
            )
            results = backtester.run(batch_config=batch_configuration)
        finally:
            os.chdir(home)

    tasks_by_name = {
        str(task["portfolio_name"]): task
        for task in tasks
    }
    priced = {}

    for entry in results["entries"]:
        name = str(entry.name)
        answer = _priced_entry(
            entry,
            end_date,
        )

        if answer["success"]:
            pandas.to_pickle(
                answer,
                _task_cache_path(tasks_by_name[name]),
            )

        priced[name] = answer

    return priced


def price_book(
    task: dict[str, object],
) -> dict[str, object]:
    """
    Price one weight file in the engine and hand back its tables as plain pandas objects.

    Written to run in a worker process, so a notebook can price many books at once: everything it
    takes and returns can be pickled.  The answer is cached under the hash of the weight file and
    the settings, so a notebook re-run after a late failure skips the books already priced -- and a
    weight file that changed by one digit is priced again, because its hash changed.
    """
    experiment_directory = pathlib.Path(str(task["experiment_directory"]))
    portfolio_name = str(task["portfolio_name"])
    weight_path = experiment_directory / "Portfolio" / f"{portfolio_name}.csv"
    cache_path = _cache_path(
        experiment_directory,
        weight_path,
        task,
    )

    if cache_path.is_file():

        return pandas.read_pickle(cache_path)

    end_date = datetime.date.fromisoformat(str(task["end"]))
    configuration = build_configuration(
        experiment_directory,
        datetime.date.fromisoformat(str(task["start"])),
        end_date,
        int(task["initial_capital"]),
        float(task["commission_basis_points"]),
        str(task["slippage_model"]),
        float(task["slippage_basis_points"]),
        float(task["cash_reserve_percentage"]),
        portfolio_name,
        tuple(task.get("benchmark_identifiers", BENCHMARK_IDENTIFIERS)),
        str(task.get("execution_price_column", EXECUTION_PRICE_COLUMN)),
        str(task.get("spread_estimator", "corwin_schultz")),
    )
    # The engine draws its report's charts into a file of one fixed name in the working folder, so
    # two engines in one folder overwrite each other's; each run gets a folder of its own, after the
    # licence is loaded from the repository's.
    import kaxanuk.backtest_engine

    kaxanuk.backtest_engine.load_config_env(ENVIRONMENT_PATH)
    home = pathlib.Path.cwd()

    with tempfile.TemporaryDirectory() as scratch:
        os.chdir(scratch)

        try:
            result = run_backtest(
                experiment_directory,
                configuration,
            )
        finally:
            os.chdir(home)

    if not result.success:
        failed = {
            "error": str(result.error),
            "name": portfolio_name,
            "success": False,
        }

        return failed

    data = result.data
    priced = {
        "benchmark_stats": dict(data.get("benchmark_stats") or {}),
        "benchmarks_stats": _plain_benchmarks(data.get("benchmarks_stats")),
        "commissions": _to_pandas(data["Commission_df"]),
        "daily_weights": _to_pandas(data["Daily_Weights"]),
        "end_date": str(data.get("end_date")),
        "error": None,
        "execution_costs": _to_pandas(data["Execution_costs_df"]),
        "financing": _to_pandas(data["Financing_df"]),
        "name": portfolio_name,
        "orders": _to_pandas(data["orders_df"]),
        "portfolio_stats": dict(data["portfolio_stats"]),
        "register": _to_pandas(data["Register_df"]),
        "risk_free_rate": data.get("Risk_free_rate"),
        "slippage": _to_pandas(data["Slippage_df"]),
        "start_date": str(data.get("start_date")),
        "success": True,
        "window": describe_window(
            result,
            end_date,
        ),
        "years": data.get("years"),
    }
    pandas.to_pickle(
        priced,
        cache_path,
    )

    return priced


def price_books(
    tasks: list[dict[str, object]],
    workers: int,
) -> dict[str, dict[str, object]]:
    """
    Price many weight files, keyed by portfolio name, loading the market data once per batch.

    The engine's own batch mode prices every book of a batch against one load of the market data;
    run one book at a time, it loaded the same files once per book, and a run of eighty-eight books
    spent its afternoon reading them.  Books share a batch when every setting but their weights is
    the same -- the window, the costs, the capital -- and a large group is cut into batches that
    run side by side.  A book already priced with the same weights and settings is read from the
    cache; a batch whose run raises hands every one of its books back with the error, and the
    caller decides.
    """
    stage_market_data()
    priced = {}
    pending = []

    for task in tasks:
        cache_path = _task_cache_path(task)

        if cache_path.is_file():
            cached = pandas.read_pickle(cache_path)
            priced[str(task["portfolio_name"])] = _with_benchmark_statistics(cached)
        else:
            pending.append(task)

    batches = _batches(pending)

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(price_batch, batch): batch
            for batch in batches
        }

        for future in concurrent.futures.as_completed(futures):
            batch = futures[future]

            try:
                priced.update(future.result())
            except Exception as error:  # noqa: BLE001 - one batch's failure must not stop the rest
                for task in batch:
                    name = str(task["portfolio_name"])
                    priced[name] = {
                        "error": f"{type(error).__name__}: {error}",
                        "name": name,
                        "success": False,
                    }

    return priced


def read_daily_weights(
    result: object,
) -> "pandas.DataFrame":
    """
    Read the book as the engine held it each trading day, which is what step 6 attributes.

    The weight file holds the rebalance dates alone; this is the drifted book between them, and the
    attribution library refuses the former once it spans a year.
    """
    daily_weights = result.data["Daily_Weights"]

    if hasattr(daily_weights, "to_pandas"):

        return daily_weights.to_pandas()

    return pandas.DataFrame(daily_weights)


def run_backtest(
    experiment_directory: "pathlib.Path",
    configuration: object,
) -> object:
    """
    Run the licensed engine over the weight file already written, and hand back its result.

    Every performance figure in this repository comes through here: there is deliberately no second
    simulator, because one that disagreed would only let a reader pick the number they preferred.
    """
    if not ENGINE_INSTALLED:
        missing_engine_message = "the KaxaNuk Backtest Engine is not installed: step 5 skipped"

        raise ModuleNotFoundError(missing_engine_message)

    import kaxanuk.backtest_engine
    import kaxanuk.backtest_engine.input_handlers

    kaxanuk.backtest_engine.load_config_env()
    output_directory = experiment_directory / "Backtest"
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )
    csv_input = kaxanuk.backtest_engine.input_handlers.CsvInput(
        input_dir=str(MARKET_DATA_DIRECTORY),
    )
    portfolio_input = kaxanuk.backtest_engine.input_handlers.CsvPortfolioInputHandler(
        str(experiment_directory / "Portfolio"),
    )

    return kaxanuk.backtest_engine.main(
        configuration=configuration,
        input_handlers=[csv_input],
        portfolio_handlers=[portfolio_input],
        logger_file=None,
        launch_dashboard=False,
        dashboard_port=8050,
    )


def stage_market_data() -> int:
    """
    Write the engine's copy of every curated file it may read, where the copy is older or missing.

    The copy holds the columns the engine reads and nothing else, as CSV, so a batch loads a
    fraction of what the curated file carries.  Returns the number of files written.
    """
    MARKET_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    written = []

    for source in sorted(CURATED_DIRECTORY.glob(f"*{time_series.SUFFIX}")):
        target = MARKET_DATA_DIRECTORY / f"{source.stem}.csv"
        source_time = source.stat().st_mtime
        current = target.is_file() and target.stat().st_mtime >= source_time

        if current:
            continue

        carried = time_series.read_column_names(source)
        columns = [
            column
            for column in MARKET_DATA_COLUMNS
            if column in carried
        ]
        table = pyarrow.parquet.read_table(
            source,
            columns=columns,
        )
        pyarrow.csv.write_csv(
            table,
            target,
        )
        written.append(source.stem)

    return len(written)


def write_weight_file(
    weights: "pandas.DataFrame",
    experiment_directory: "pathlib.Path",
    name: str = "portfolio_weights",
) -> "pathlib.Path":
    """
    Write the book in the layout the engine detects: identifiers down, rebalance dates across.

    Whatever the rule left uninvested stays out of the file: the engine holds it as dollar cash and
    pays it the cash rate, as a broker does.  Every column is checked to sum to at most one before
    the file is written, because a column over one is leverage the rule never asked for.
    """
    portfolio_directory = experiment_directory / "Portfolio"
    portfolio_directory.mkdir(
        parents=True,
        exist_ok=True,
    )
    # Each weight is rounded down, never to the nearest: weights rounded to six places can sum to a
    # few millionths over one -- thirty did, by two -- and the engine refuses a column whose gross
    # exposure is above one by a millionth.  Rounding down leaves the remainder in cash, where it
    # belongs.
    scale = 10 ** WEIGHT_DECIMALS
    transposed = weights.transpose()
    scaled = transposed.mul(scale)
    held = scaled.floordiv(1).div(scale)
    totals = held.sum(axis=0)
    over_one = totals[totals > 1.0 + 10 ** -WEIGHT_DECIMALS]

    if len(over_one) > 0:
        over_one_message = f"{len(over_one)} rebalance dates sum to more than 1.0"

        raise ValueError(over_one_message)

    named = held.copy()
    named.index.name = "Ticker"
    formatted_columns = []

    for column in named.columns:
        timestamp = pandas.Timestamp(column)
        rebalance_date = timestamp.date()
        formatted_columns.append(rebalance_date.isoformat())

    named.columns = formatted_columns
    path = portfolio_directory / f"{name}.csv"
    named.to_csv(
        path,
        float_format=f"%.{WEIGHT_DECIMALS}f",
    )

    return path


def _batch_defaults(
    configuration: object,
) -> dict[str, object]:
    """
    The configuration as the batch parser reads it: plain numbers, strings and ISO dates.

    The engine's configuration holds some numbers as PyArrow decimals and some settings as enums,
    and the batch parser compares them as floats; the capital it takes as an integer.
    """
    fields = dataclasses.asdict(configuration)
    defaults = {
        name: _plain_value(value)
        for name, value in fields.items()
        if value is not None
    }
    defaults["initial_capital"] = int(defaults["initial_capital"])
    defaults["input_market_data_directory"] = str(MARKET_DATA_DIRECTORY)
    defaults["market_data_input_format"] = "csv"

    return defaults


def _batches(
    tasks: list[dict[str, object]],
) -> list[list[dict[str, object]]]:
    """
    The tasks grouped by every setting but the book, each group cut into batches of a few books.
    """
    groups = {}

    for task in tasks:
        settings = {
            key: str(value)
            for key, value in sorted(task.items())
            if key != "portfolio_name"
        }
        key = json.dumps(
            settings,
            sort_keys=True,
        )
        groups.setdefault(key, []).append(task)

    return [
        group[start:start + BOOKS_PER_BATCH]
        for group in groups.values()
        for start in range(
            0,
            len(group),
            BOOKS_PER_BATCH,
        )
    ]


def _benchmark_statistics(
    values: "pandas.DataFrame",
    years: float,
    risk_free_rate: float,
) -> dict[str, float]:
    """
    A benchmark's statistics, by the engine's own metrics, over the series the engine returned.

    The engine's batch mode returns each benchmark's daily value and return beside the book, but
    not their statistics; these are its `compute_portfolio_statistics` over that series, on the
    book's window, years and risk-free rate, so the benchmark and the book are measured alike.
    """
    import kaxanuk.backtest_engine.modules.metrics

    dates = pandas.to_datetime(values["date_column"])
    levels = pandas.Series(
        values["bench_value"].astype(float).to_numpy(),
        index=dates,
    )
    returns = pandas.Series(
        values["daily_return"].astype(float).to_numpy(),
        index=dates,
    )
    metrics = kaxanuk.backtest_engine.modules.metrics
    statistics = metrics.compute_portfolio_statistics(
        float(levels.iloc[0]),
        float(levels.iloc[0]),
        float(levels.iloc[-1]),
        returns,
        levels,
        years,
        risk_free_rate=risk_free_rate,
    )

    return {
        str(name): value
        for name, value in statistics.items()
    }


def _cache_path(
    experiment_directory: "pathlib.Path",
    weight_path: "pathlib.Path",
    task: dict[str, object],
) -> "pathlib.Path":
    """
    Where one engine run's answer is kept: named by the hash of its weight file and its settings.
    """
    settings = {
        key: str(value)
        for key, value in sorted(task.items())
        if key != "experiment_directory"
    }
    digest = hashlib.sha256()
    digest.update(weight_path.read_bytes())
    settings_text = json.dumps(
        settings,
        sort_keys=True,
    )
    digest.update(settings_text.encode("utf-8"))
    cache_directory = experiment_directory / "Backtest" / "cache"
    cache_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return cache_directory / f"{digest.hexdigest()}.pkl"


def _describe_valued_window(
    data: dict[str, object],
    end_date: "datetime.date",
) -> str:
    """
    Compare the window the engine valued with the one it was asked for, from a batch's answer.
    """
    valued_end = data.get("end_date")
    years = data.get("years")

    if valued_end is None:

        return "the engine returned no end date: treat every figure from this run as unverified"

    valued_date = pandas.Timestamp(valued_end).date()

    if valued_date < end_date - datetime.timedelta(days=7):

        return f"TRUNCATED: valued to {valued_date}, asked for {end_date} ({years} years)"

    return f"complete: valued to {valued_date} ({years} years)"


def _inline_weights(
    weight_path: "pathlib.Path",
) -> dict[str, dict[str, float]]:
    """
    A weight file as the batch takes it: each rebalance date's names and their non-zero weights.

    A name absent on a date is held at zero, as a zero in the file is.
    """
    weights = pandas.read_csv(
        weight_path,
        index_col=0,
    )

    return {
        str(column): {
            str(identifier): float(weight)
            for identifier, weight in weights[column].items()
            if weight > 0
        }
        for column in weights.columns
    }


def _plain_benchmarks(
    benchmarks: object,
) -> dict[str, dict]:
    """
    The engine's statistics for every benchmark, as plain dictionaries, empty when it gave none.
    """
    if not isinstance(benchmarks, dict):

        return {}

    return {
        str(identifier): dict(statistics)
        for identifier, statistics in benchmarks.items()
        if isinstance(statistics, dict)
    }


def _plain_value(
    value: object,
) -> object:
    """
    A configuration value as plain Python: a decimal as a float, an enum as its value, a date ISO.
    """
    unwrapped = value.as_py() if hasattr(value, "as_py") else value

    if isinstance(unwrapped, decimal.Decimal):

        return float(unwrapped)

    if isinstance(unwrapped, enum.Enum):

        return unwrapped.value

    if isinstance(unwrapped, datetime.date):

        return unwrapped.isoformat()

    return unwrapped


def _priced_entry(
    entry: object,
    end_date: "datetime.date",
) -> dict[str, object]:
    """
    One book of a batch as plain pandas objects, in the shape every notebook reads.
    """
    name = str(entry.name)

    if not entry.success:

        return {
            "error": str(entry.error_message),
            "name": name,
            "success": False,
        }

    data = entry.result
    benchmarks = data.get("benchmarks") or {}
    benchmark_values = {
        str(identifier): _to_pandas(table)
        for identifier, table in benchmarks.items()
    }
    benchmarks_stats = {
        identifier: _benchmark_statistics(
            values,
            float(data["years"]),
            float(data.get("Risk_free_rate") or 0.0),
        )
        for identifier, values in benchmark_values.items()
    }

    return {
        "benchmark_stats": dict(data.get("benchmark_stats") or {}),
        "benchmark_values": benchmark_values,
        "benchmarks_stats": benchmarks_stats,
        "commissions": _to_pandas(data["Commission_df"]),
        "daily_weights": _to_pandas(data["Daily_Weights"]),
        "end_date": str(data.get("end_date")),
        "error": None,
        "execution_costs": _to_pandas(data["Execution_costs_df"]),
        "financing": _to_pandas(data["Financing_df"]),
        "name": name,
        "orders": _to_pandas(data["orders_df"]),
        "portfolio_stats": dict(data["portfolio_stats"]),
        "register": _to_pandas(data["Register_df"]),
        "risk_free_rate": data.get("Risk_free_rate"),
        "slippage": _to_pandas(data["Slippage_df"]),
        "start_date": str(data.get("start_date")),
        "success": True,
        "window": _describe_valued_window(
            data,
            end_date,
        ),
        "years": data.get("years"),
    }


def _task_cache_path(
    task: dict[str, object],
) -> "pathlib.Path":
    """
    Where one book's answer is kept, from its task: the hash of its weight file and its settings.
    """
    experiment_directory = pathlib.Path(str(task["experiment_directory"]))

    return _cache_path(
        experiment_directory,
        _weight_path(task),
        task,
    )


def _to_pandas(
    table: object,
) -> "pandas.DataFrame":
    """
    An engine table as a pandas frame, whichever library the engine built it with.
    """
    if hasattr(table, "to_pandas"):

        return table.to_pandas()

    return pandas.DataFrame(table)


def _weight_path(
    task: dict[str, object],
) -> "pathlib.Path":
    """
    The weight file a task prices, which the notebook wrote before asking.
    """
    experiment_directory = pathlib.Path(str(task["experiment_directory"]))
    portfolio_name = str(task["portfolio_name"])

    return experiment_directory / "Portfolio" / f"{portfolio_name}.csv"


def _with_benchmark_statistics(
    answer: dict[str, object],
) -> dict[str, object]:
    """
    A cached answer with its benchmarks' statistics, computed where an earlier seam left none.
    """
    values = answer.get("benchmark_values") or {}
    computed = answer.get("benchmarks_stats")
    missing = answer.get("success") and len(values) > 0 and not computed

    if not missing:

        return answer

    statistics = {
        identifier: _benchmark_statistics(
            frame,
            float(answer["years"]),
            float(answer.get("risk_free_rate") or 0.0),
        )
        for identifier, frame in values.items()
    }

    return {
        **answer,
        "benchmarks_stats": statistics,
    }
