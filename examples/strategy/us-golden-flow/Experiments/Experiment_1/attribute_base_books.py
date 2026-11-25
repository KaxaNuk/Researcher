"""
Attribution apart from the notebook -- step 6, beside the experiment notebook.  Attributes books the
notebook has already priced, from the engine's answers it cached, without pricing anything again.

In plain words: which part of each book's return was earned, and which part was the market's, when
the notebook's own attribution section did not run or would take too long to run again.

What is expected here, when a strategy needs it, and nothing when it does not:

- The books and the cost rows are the blueprint's and the owner's, named at the top, each with the
  decision that added it.
- The engine's answers are read from `Backtest/cache/`, under the hash of each weight file, and a
  cached run that is not the one the findings read raises.
- Each book is shaped exactly as the notebook's attribution section shapes it -- the daily book as
  the engine held it, widened to every benchmark member at zero weight, both weight tables held
  overnight -- before `attribution_analysis` attributes it.
- The first cut's benchmark is reconciled with the index's own returns, and a gap above the
  blueprint's tolerance raises.

It produces the same tables the notebook's attribution writes, in `Attribution/`, none committed,
and prints what `FINDINGS_N.md` quotes.

It prevents an attribution that shapes the book differently from the notebook's.
"""

# --- example: begin ---

# In US-Golden-Flow, this script's own description:
#
# Step 6 for Experiment 1 version 0.4.0 -- the three passes of section 5 of
# `experiment_1_marimo.py`, run on the base books the engine priced on 2026-11-20, without pricing
# anything again.
#
# In plain words: which part of the rule's return did it earn, and which part was the market's?
#
# Version 0.4.0 priced only the four base books, and its notebook skipped attribution by the owner's
# decision of 2026-11-19 (`BASE_BOOKS_ONLY`). On the owner's decisions of 2026-11-23 and 2026-11-24
# the four are attributed after all, at both cost rows: the rule, beside its control and the equal-
# weight arm, the two counterfactuals `alpha-decomposition` reads it against, and the rule without
# its sector cap, which prediction 9 compares on technology. On the owner's word of 2026-11-24 the
# rule and the uncapped arm are also attributed over each of the notebook's three sub-periods, at
# both cost rows: the whole window's book cut to the sub-period's days, its effects linked by the
# library over those days alone -- not a fresh book struck on the sub-period's first day, as the
# engine's sub-period runs are, and not a sum of the per-year tables. On the owner's word of
# 2026-11-24 the notebook prices the twenty random books too, and they are attributed here on the
# factor model alone, as section 5 attributes them: the rule's idiosyncratic return is read against
# theirs over the window, the last limb of P2, and over each sub-period, cut as the rule's are, to
# say whether 2018-2026's selection is above chance. The notebook's own run takes about three hours;
# this script reads the engine's answers from `Backtest/cache/`, where the notebook left them under
# the hash of each weight file, and shapes them exactly as section 5 does -- the daily book as the
# engine held it, widened to every Core member at zero weight, both weight tables held overnight,
# every return over the factor model's implied bill -- before handing them to
# `attribution_analysis.attribute_books`.
#
# It writes `Attribution/brinson_fachler.csv`, `factor_model.csv`, `brinson_fachler_residual.csv`,
# the per-year tables, `reconciliation.csv`, the same three passes `by_sub_period` and
# `random_books.csv`, all regenerable and none committed, and prints what `FINDINGS_1.md` quotes. It
# raises when an input is missing, when a cached run is not the one the findings read, or when the
# first cut's benchmark does not reconcile with the Core's own returns within the blueprint's
# tolerance, a point a year.
#
# Run from the repository root: `uv run python Experiments/Experiment_1/attribute_base_books.py`.

import pathlib
import sys

import pandas

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "Experiments"))
sys.path.insert(0, str(REPOSITORY_ROOT / "Data"))

import attribution_analysis  # noqa: E402 - the paths above have to exist first
import backtest_engine  # noqa: E402
import hand_supplied  # noqa: E402
import securities_panel  # noqa: E402

__all__ = [
    "main",
]

ATTRIBUTION_WORKERS = 2
# Each book by the name its weight file gave the engine's cached answer.
BOOKS = {
    "control": "portfolio_weights_control",
    "control flat": "portfolio_weights_control_flat",
    "equal weight": "portfolio_weights_equal_weight",
    "equal weight flat": "portfolio_weights_equal_weight_flat",
    "rule": "portfolio_weights",
    "rule flat": "portfolio_weights_flat",
    "uncapped": "portfolio_weights_no_sector_cap",
    "uncapped flat": "portfolio_weights_no_sector_cap_flat",
}
EXPERIMENT_DIRECTORY = REPOSITORY_ROOT / "Experiments" / "Experiment_1"
CACHE_DIRECTORY = EXPERIMENT_DIRECTORY / "Backtest" / "cache"
LAYERS = (
    "brinson",
    "factor",
    "residual",
)
MEMBERSHIP_COLUMN = "c_index_weight"
# The notebook's label for a book priced at the flat row, as `excluded_runs.csv` names it.
NOTEBOOK_FLAT_SUFFIX = ", flat 5 bp"
OUTPUT_DIRECTORY = EXPERIMENT_DIRECTORY / "Attribution"
# The random books the notebook prices, by its seeds, and how many the rule must beat for P2.
RANDOM_BOOKS_TO_BEAT = 16
RANDOM_SEEDS = tuple(range(1, 21))
# The blueprint's tolerance for the first cut's benchmark against the Core's own returns.
RECONCILIATION_TOLERANCE_POINTS = 1.0
# What the script keeps of each cached engine run: the rest is the engine's tables, unread here.
RUN_KEYS = (
    "daily_weights",
    "end_date",
    "name",
    "start_date",
    "success",
)
# The books attributed sub-period by sub-period, and the sub-periods as the notebook fixes them.
SUB_PERIOD_BOOKS = (
    "rule",
    "rule flat",
    "uncapped",
    "uncapped flat",
)
SUB_PERIODS = {
    "1999 to 2008": ("1999-12-31", "2008-12-31"),
    "2009 to 2017": ("2009-01-01", "2017-12-31"),
    "2018 to 2026": ("2018-01-01", "2026-10-31"),
}
TRADING_DAYS_A_YEAR = 252


def main() -> None:
    """Attribute the books and write the tables `FINDINGS_1.md` quotes."""
    missing = attribution_analysis.report_missing_inputs()

    if len(missing) > 0:
        missing_message = f"step 6 cannot run: {'; '.join(missing)}"

        raise RuntimeError(missing_message)

    by_name = _runs_by_name()
    runs = _cached_runs(by_name)
    random_runs = _cached_random_runs(by_name)
    window_file = pandas.read_csv(REPOSITORY_ROOT / "Universe" / "Window.csv")
    window_start = pandas.Timestamp(window_file["window_start"].iloc[0])
    window_end = pandas.Timestamp(window_file["window_end"].iloc[0])
    excluded = _excluded_names()
    membership_matrix = securities_panel.load_matrices((MEMBERSHIP_COLUMN,))[MEMBERSHIP_COLUMN]
    membership = membership_matrix.loc[:window_end].fillna(0.0) > 0
    calendar = membership.index
    window_days = calendar[(calendar >= window_start) & (calendar <= window_end)]
    market_factor = pandas.read_csv(hand_supplied.factor_path("Market"), usecols=[0])
    factor_dates = pandas.DatetimeIndex(pandas.to_datetime(market_factor.iloc[:, 0]))
    rule_days = pandas.DatetimeIndex(runs["rule"]["daily_weights"].index)
    first_day = max(
        factor_dates.min(),
        rule_days.min(),
    )
    last_day = factor_dates.max()
    window = window_days[(window_days >= first_day) & (window_days <= last_day)]
    backtest_start = rule_days.min().date()
    backtest_end = rule_days.max().date()
    attribution_start = window.min().date()
    attribution_end = window.max().date()
    print(f"backtest window:    {backtest_start} to {backtest_end}")
    print(f"attribution window: {attribution_start} to {attribution_end}")
    members_in_window = membership.loc[window]
    members_ever = members_in_window.columns[members_in_window.any(axis=0)]
    base_runs = list(runs.values())
    every_run = base_runs + list(random_runs.values())
    names_held = set(members_ever).union(*[
        set(run["daily_weights"].columns)
        for run in every_run
    ])
    sorted_names = tuple(sorted(names_held))
    all_prices = attribution_analysis.load_prices(sorted_names, window)
    bill = attribution_analysis.implied_bill(all_prices)
    all_returns = attribution_analysis.load_excess_returns(all_prices, bill)
    loaded_index = attribution_analysis.load_benchmark_weights(window, all_prices)
    priced_index = loaded_index.drop(
        columns=list(excluded),
        errors="ignore",
    )
    index_totals = priced_index.sum(axis=1)
    index_weights = priced_index.div(index_totals, axis=0).fillna(0.0)
    coverage = attribution_analysis.benchmark_coverage(window, all_prices)
    coverage_by_year = coverage.groupby(coverage.index.year).mean()
    lowest_share = float(coverage_by_year.min())
    lowest_coverage = round(lowest_share, 4)
    print(f"share of the whole index the first cut can price, lowest year: {lowest_coverage}")
    tasks = [
        _task(
            label,
            runs[label],
            window,
            index_weights,
            all_returns,
            excluded,
        )
        for label in BOOKS
    ]
    attributed = attribution_analysis.attribute_books(tasks, ATTRIBUTION_WORKERS)
    errors = {
        name: answer["error"]
        for name, answer in attributed.items()
        if "error" in answer
    }

    if len(errors) > 0:
        error_message = f"attribution failed: {errors}"

        raise RuntimeError(error_message)

    _write_tables(
        attributed,
        bill,
        window,
    )
    sub_period_tasks = [
        _task(
            f"{label}, {period}",
            runs[label],
            window[(window >= start) & (window <= end)],
            index_weights,
            all_returns,
            excluded,
        )
        for label in SUB_PERIOD_BOOKS
        for period, (start, end) in SUB_PERIODS.items()
    ]
    attributed_by_sub_period = attribution_analysis.attribute_books(
        sub_period_tasks,
        ATTRIBUTION_WORKERS,
    )
    sub_period_errors = {
        name: answer["error"]
        for name, answer in attributed_by_sub_period.items()
        if "error" in answer
    }

    if len(sub_period_errors) > 0:
        sub_period_message = f"attribution by sub-period failed: {sub_period_errors}"

        raise RuntimeError(sub_period_message)

    _write_sub_period_tables(
        attributed_by_sub_period,
        bill,
        window,
    )
    random_periods = {"window": window} | {
        period: window[(window >= start) & (window <= end)]
        for period, (start, end) in SUB_PERIODS.items()
    }
    random_tasks = [
        _task(
            f"{label} | {period}",
            run,
            days,
            index_weights,
            all_returns,
            excluded,
            ("factor",),
        )
        for period, days in random_periods.items()
        for label, run in random_runs.items()
    ]
    attributed_random = attribution_analysis.attribute_books(
        random_tasks,
        ATTRIBUTION_WORKERS,
    )
    random_errors = {
        name: answer["error"]
        for name, answer in attributed_random.items()
        if "error" in answer
    }

    if len(random_errors) > 0:
        random_message = f"attribution of the random books failed: {random_errors}"

        raise RuntimeError(random_message)

    rule_answers = {
        f"{rule_label} | {period}": (
            attributed[rule_label]
            if period == "window"
            else attributed_by_sub_period[f"{rule_label}, {period}"]
        )
        for rule_label in ("rule", "rule flat")
        for period in random_periods
    }
    idiosyncratic = attribution_analysis.load_factor_returns()["f_idyo_returns"]
    random_coverage = {
        task["name"]: _factor_coverage(task["book"], idiosyncratic)
        for task in random_tasks
    }
    _write_random_table(
        attributed_random,
        rule_answers,
        random_coverage,
    )


def _cached_random_runs(
    by_name: dict[str, dict[str, object]],
) -> dict[str, dict[str, object]]:
    """
    The random books the engine priced, at both cost rows, keyed by the notebook's labels.

    A run the notebook excluded by name, in `Backtest/excluded_runs.csv`, is left out and said, so
    the count of random books the rule beats is always over the books read; one neither excluded
    nor cached means the notebook has not priced them, and raises.
    """
    excluded_file = pandas.read_csv(
        CACHE_DIRECTORY.parent / "excluded_runs.csv",
        index_col=0,
    )
    reasons = excluded_file["reason"].to_dict()
    random_runs = {}

    for seed in RANDOM_SEEDS:
        for label_suffix, name_suffix in (("", ""), (NOTEBOOK_FLAT_SUFFIX, "_flat")):
            label = f"random {seed:02d}{label_suffix}"
            name = f"portfolio_weights_random_{seed:02d}{name_suffix}"

            if label in reasons:
                print(f"{label}: excluded by the notebook, {reasons[label]}")

                continue

            run = by_name.get(name)

            if run is None or not run.get("success", False):
                random_message = f"no successful cached run named {name} in {CACHE_DIRECTORY}"

                raise FileNotFoundError(random_message)

            random_runs[label] = run

    random_books_priced = 2 * len(RANDOM_SEEDS)
    print(f"random books read: {len(random_runs)} of {random_books_priced}")

    return random_runs


def _cached_runs(
    by_name: dict[str, dict[str, object]],
) -> dict[str, dict[str, object]]:
    """
    The engine's answers for the eight books, read from the cache the notebook wrote.

    Each must be the whole window's run at its cost row, valued to its end, or the
    attribution would describe a book the findings do not.
    """
    runs = {}

    for label, name in BOOKS.items():
        run = by_name.get(name)

        if run is None or not run.get("success", False):
            run_message = f"no successful cached engine run named {name} in {CACHE_DIRECTORY}"

            raise FileNotFoundError(run_message)

        runs[label] = run
        print(f"{label}: {name}, {run['start_date']} to {run['end_date']}")

    return runs


def _excluded_names() -> tuple[str, ...]:
    """The blocking rows of the register, read as the notebook reads them."""
    issues = pandas.read_csv(REPOSITORY_ROOT / "Universe" / "Data_Issues.csv").fillna("")
    blocking = issues[
        (issues["severity"] == "blocking") & ~issues["check"].str.startswith("missing file")
    ]
    names = {
        identifier
        for identifiers in blocking["identifiers"]
        for identifier in str(identifiers).split()
    }

    return tuple(sorted(names))


def _factor_coverage(
    book: "pandas.DataFrame",
    idiosyncratic: "pandas.DataFrame",
) -> float:
    """
    The mean daily share of a book's weight in names the factor model has a residual for.

    It is the share `attribution_analysis` reports for a book given the residual pass; the random
    books are attributed on the factor model alone, which does not report it, and a factor
    attribution is read beside the part of the book it describes.
    """
    book_residuals = idiosyncratic.reindex(
        index=book.index,
        columns=book.columns,
    )
    covered_columns = book_residuals.columns[book_residuals.notna().any()]
    covered_weight = book[covered_columns].sum(axis=1)

    return float(covered_weight.mean())


def _runs_by_name() -> dict[str, dict[str, object]]:
    """
    Every cached engine run, by the name of its weight file, keeping only what attribution reads.

    The cache holds sixty runs of the engine's whole tables; kept whole, they would sit in memory
    beside every price the attribution loads.
    """
    by_name = {}

    for path in sorted(CACHE_DIRECTORY.glob("*.pkl")):
        cached = pandas.read_pickle(path)
        by_name[cached.get("name")] = {
            key: cached.get(key)
            for key in RUN_KEYS
        }

    return by_name


def _task(
    label: str,
    run: dict[str, object],
    window: "pandas.DatetimeIndex",
    index_weights: "pandas.DataFrame",
    all_returns: "pandas.DataFrame",
    excluded: tuple[str, ...],
    layers: tuple[str, ...] = LAYERS,
) -> dict[str, object]:
    """
    One book's inputs for the library, as section 5's `attribution_task` builds them.

    The window may be a sub-period's days alone: the index's weights are cut to the same days, so
    the first cut's benchmark is the Core over the sub-period and nothing else.
    """
    daily_weights = run["daily_weights"].reindex(window).fillna(0.0)
    window_index_weights = index_weights.reindex(window).fillna(0.0)
    book = attribution_analysis.widen_to_benchmark(
        daily_weights,
        window_index_weights,
        backtest_engine.BENCHMARK_IDENTIFIERS,
    ).drop(
        columns=list(excluded),
        errors="ignore",
    )
    benchmark = window_index_weights.reindex(columns=book.columns).fillna(0.0)
    book_overnight = attribution_analysis.held_overnight(book)
    benchmark_overnight = attribution_analysis.held_overnight(benchmark)
    asset_returns = all_returns.reindex(
        index=book_overnight.index,
        columns=book_overnight.columns,
    ).fillna(0.0)

    return {
        "name": label,
        "book": book_overnight,
        "benchmark": benchmark_overnight,
        "asset_returns": asset_returns,
        "layers": layers,
        "cache_directory": str(OUTPUT_DIRECTORY / "cache"),
    }


def _write_random_table(
    attributed_random: dict[str, dict[str, object]],
    rule_answers: dict[str, dict[str, object]],
    coverage: dict[str, float],
) -> None:
    """
    Write and print each random book's idiosyncratic return, and how many the rule's exceeds.

    The blueprint's P2 limb is the rule above 16 of the 20 random books over the window; it is
    counted at each cost row over the books read, and the count says how many were read.  The same
    count over each sub-period is information, not the limb: it says whether the rule's positive
    selection in 2018-2026 is above what a random draw from the same pool earned over those days.
    The answers and the coverage are keyed `<book> | <period>`, the period `window` or a
    sub-period's name.
    """
    rows = {}
    counts = {}

    for rule_key, rule_answer in rule_answers.items():
        rule_label, period = rule_key.split(" | ")
        flat_rule = rule_label.endswith("flat")
        rule_idiosyncratic = float(rule_answer["factor_totals"]["f_idyo_returns"])
        random_values = {}
        random_coverages = {}

        for name, answer in attributed_random.items():
            book_label, book_period = name.split(" | ")
            flat_book = book_label.endswith(NOTEBOOK_FLAT_SUFFIX)

            if book_period == period and flat_book == flat_rule:
                seed_label = book_label.removesuffix(NOTEBOOK_FLAT_SUFFIX)
                random_values[seed_label] = float(answer["factor_totals"]["f_idyo_returns"])
                random_coverages[seed_label] = coverage[name]

        random_idiosyncratic = pandas.Series(
            random_values,
            dtype=float,
        )
        random_coverage = pandas.Series(
            random_coverages,
            dtype=float,
        )
        rows[rule_key] = random_idiosyncratic
        beaten = int((random_idiosyncratic < rule_idiosyncratic).sum())
        counts[rule_key] = {
            "rule_idiosyncratic": rule_idiosyncratic,
            "random_books_read": len(random_idiosyncratic),
            "random_books_beaten": beaten,
            "random_median": float(random_idiosyncratic.median()),
            "random_lowest": float(random_idiosyncratic.min()),
            "random_highest": float(random_idiosyncratic.max()),
            "random_lowest_factor_coverage": float(random_coverage.min()),
            "random_highest_factor_coverage": float(random_coverage.max()),
            "limb_holds": (
                beaten >= RANDOM_BOOKS_TO_BEAT
                and len(random_idiosyncratic) == len(RANDOM_SEEDS)
            ),
        }

    random_table = pandas.concat(rows, axis=1)
    count_table = pandas.DataFrame(counts)
    random_table.to_csv(OUTPUT_DIRECTORY / "random_books.csv")
    count_table.to_csv(OUTPUT_DIRECTORY / "random_books_against_the_rule.csv")
    rounded_random = random_table.round(2)
    print("idiosyncratic return of each random book, linked over each period, in points:")
    print(rounded_random.to_string())
    print("the rule against the random books:")
    print(count_table.to_string())


def _write_sub_period_tables(
    attributed: dict[str, dict[str, object]],
    bill: "pandas.Series",
    window: "pandas.DatetimeIndex",
) -> None:
    """
    Write and print the three passes for each book and sub-period.

    Each sub-period's first-cut benchmark is set beside the Core's own returns over the same days,
    so a sub-period whose benchmark does not reconcile is seen before any of its rows is read.
    """
    brinson_table = pandas.DataFrame({
        name: answer["brinson_totals"]
        for name, answer in attributed.items()
    })
    factor_table = pandas.DataFrame({
        name: answer["factor_totals"]
        for name, answer in attributed.items()
    })
    residual_table = pandas.DataFrame({
        name: answer["residual_totals"]
        for name, answer in attributed.items()
    })
    excess_index = hand_supplied.read_benchmark_returns() - bill
    reconciliation_rows = {}

    for period, (start, end) in SUB_PERIODS.items():
        period_days = window[(window >= start) & (window <= end)]
        rule_daily = attributed[f"rule, {period}"]["brinson_daily"]
        benchmark_column = next(
            column
            for column in rule_daily.columns
            if "bench" in column.lower() and "return" in column.lower()
        )
        first_cut_daily = rule_daily[benchmark_column]
        index_returns = excess_index.reindex(period_days[1:])
        first_cut_annual = float(first_cut_daily.mean() * TRADING_DAYS_A_YEAR * 100)
        index_annual = float(index_returns.mean() * TRADING_DAYS_A_YEAR * 100)
        reconciliation_rows[period] = {
            "first_cut_benchmark_points_a_year": first_cut_annual,
            "core_less_bill_points_a_year": index_annual,
            "gap_points_a_year": abs(first_cut_annual - index_annual),
            "first_day": str(period_days[0].date()),
            "last_day": str(period_days[-1].date()),
        }

    reconciliation = pandas.DataFrame(reconciliation_rows).T
    brinson_table.to_csv(OUTPUT_DIRECTORY / "brinson_fachler_by_sub_period.csv")
    factor_table.to_csv(OUTPUT_DIRECTORY / "factor_model_by_sub_period.csv")
    residual_table.to_csv(OUTPUT_DIRECTORY / "brinson_fachler_residual_by_sub_period.csv")
    reconciliation.to_csv(OUTPUT_DIRECTORY / "reconciliation_by_sub_period.csv")
    rounded_brinson = brinson_table.T.round(2)
    rounded_factors = factor_table.T.round(2)
    rounded_residual = residual_table.T.round(2)
    print("Brinson-Fachler by KN sector, by sub-period, linked over each, in points:")
    print(rounded_brinson.to_string())
    print("factor model, by sub-period, linked over each, in points:")
    print(rounded_factors.to_string())
    print("Brinson-Fachler on the residual, by sub-period, in points:")
    print(rounded_residual.to_string())
    print("each sub-period's first-cut benchmark against the Core's own, points a year:")
    print(reconciliation.to_string())


def _write_tables(
    attributed: dict[str, dict[str, object]],
    bill: "pandas.Series",
    window: "pandas.DatetimeIndex",
) -> None:
    """Write and print the three passes, and raise if the first cut does not reconcile."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    brinson_table = pandas.DataFrame({
        name: answer["brinson_totals"]
        for name, answer in attributed.items()
    })
    factor_table = pandas.DataFrame({
        name: answer["factor_totals"]
        for name, answer in attributed.items()
    })
    residual_table = pandas.DataFrame({
        name: answer["residual_totals"]
        for name, answer in attributed.items()
    })
    covered_share = pandas.Series({
        name: answer["covered_share"]
        for name, answer in attributed.items()
    })
    relative_stats = pandas.DataFrame({
        name: answer["relative_stats"]
        for name, answer in attributed.items()
    })
    brinson_table.to_csv(OUTPUT_DIRECTORY / "brinson_fachler.csv")
    factor_table.to_csv(OUTPUT_DIRECTORY / "factor_model.csv")
    residual_table.to_csv(OUTPUT_DIRECTORY / "brinson_fachler_residual.csv")
    relative_stats.to_csv(OUTPUT_DIRECTORY / "relative_stats.csv")

    for name, answer in attributed.items():
        file_stem = name.replace(" ", "_")
        answer["brinson_by_year"].to_csv(
            OUTPUT_DIRECTORY / f"brinson_fachler_by_year_{file_stem}.csv",
            index=False,
        )
        answer["factor_by_year"].to_csv(
            OUTPUT_DIRECTORY / f"factor_model_by_year_{file_stem}.csv",
            index=False,
        )

    rule_daily = attributed["rule"]["brinson_daily"]
    benchmark_columns = [
        column
        for column in rule_daily.columns
        if "bench" in column.lower() and "return" in column.lower()
    ]

    if len(benchmark_columns) == 0:
        column_message = "the library returned no benchmark return column: nothing to reconcile"

        raise RuntimeError(column_message)

    excess_index = hand_supplied.read_benchmark_returns() - bill
    index_returns = excess_index.reindex(window[1:])
    first_cut_daily = rule_daily[benchmark_columns[0]]
    first_cut_annual = float(first_cut_daily.mean() * TRADING_DAYS_A_YEAR * 100)
    index_annual = float(index_returns.mean() * TRADING_DAYS_A_YEAR * 100)
    reconciliation_gap = abs(first_cut_annual - index_annual)
    window_start = window.min().date()
    window_end = window.max().date()
    reconciliation = pandas.Series({
        "first_cut_benchmark_points_a_year": first_cut_annual,
        "core_less_bill_points_a_year": index_annual,
        "gap_points_a_year": reconciliation_gap,
        "window_start": str(window_start),
        "window_end": str(window_end),
    })
    reconciliation.to_csv(OUTPUT_DIRECTORY / "reconciliation.csv", header=False)
    pandas.set_option("display.width", 200)
    sorted_factors = factor_table.sort_values("rule", ascending=False)
    diagnostics = {
        name: answer.get("diagnostics")
        for name, answer in attributed.items()
    }
    tolerance = RECONCILIATION_TOLERANCE_POINTS
    rounded_brinson = brinson_table.round(2)
    rounded_factors = sorted_factors.round(2)
    rounded_residual = residual_table.round(2)
    rounded_coverage = covered_share.round(3)
    print("Brinson-Fachler by KN sector, linked over the window, in points:")
    print(rounded_brinson.to_string())
    print("factor model, linked over the window, in points:")
    print(rounded_factors.to_string())
    print("Brinson-Fachler on the residual, in points:")
    print(rounded_residual.to_string())
    print("share of each book the factor model covers:")
    print(rounded_coverage.to_string())
    print("relative statistics:")
    print(relative_stats.to_string())
    print(f"diagnostics: {diagnostics}")
    print(f"first cut's benchmark, mean daily return a year: {first_cut_annual:.2f} points")
    print(f"the KN US Equity Core's own less the bill:      {index_annual:.2f} points")
    print(f"gap: {reconciliation_gap:.2f} points a year (tolerance {tolerance})")

    if reconciliation_gap > RECONCILIATION_TOLERANCE_POINTS:
        gap_message = (
            f"the first cut's benchmark misses the Core by {reconciliation_gap:.2f} points a year"
        )

        raise AssertionError(gap_message)


if __name__ == "__main__":
    main()

# --- example: end ---
