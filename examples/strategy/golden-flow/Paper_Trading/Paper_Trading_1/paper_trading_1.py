"""
The frozen book of Experiment 1 -- step 7 of 8.  `Paper_Trading_N` mirrors the `Experiment_N` it
was promoted from, so the lineage of a paper-traded book is never in question.

In plain words: the rule that went to paper, **copied out of the experiment notebook and then
left alone**.  The notebook is the record of how the rule was *chosen*, including everything tried
and rejected, and it stays free for the next piece of research.  This file is the record of what is
*being traded*, and a change to it is a change to a live book, not a change to an experiment.

What it holds, once its experiment graduates or a person puts it on paper on probation:

- the rule's settings, copied from the experiment notebook, and its costs;
- the rule itself, in the form the notebook ran it, with its control -- the same rule with one
  ingredient removed, which runs beside the book every day;
- `BANDS`: for each diagnostic, the range `FINDINGS_N.md` measured over the backtest, registered
  in this book's section of `../BITACORA.md` before its first day; a day outside one is a flag;
- `run(as_of)`, which `../daily_update.py` calls once a day.  It runs the frozen refinery in this
  folder over the raw files linked into `Data/Curator/Time_Series/`, applies the rule from the
  experiment's first day to `as_of`, writes the weight files, prices the book and its control with
  the frozen engine module -- over the whole history, over the days after the experiment's window
  and since the freeze date in `FREEZE.json` -- and returns what the record needs: the engine's
  results, the book in force, the day's diagnostics, the flags and a summary.

**Membership past the last date its source wrote is held at that date.**  An index's holdings,
read by `Data/hand_supplied.py`, are refreshed later than prices, and a membership built only from
the dates they hold -- in the rule, or as a refined column -- has no member past their last date:
right for a backtest, and a book that read it so would sell every name the day those files end.
The book holds the last membership they wrote, and `../daily_update.py` flags the files once they
fall behind the day; inside the experiment's window they cover every day, so the rule it ran is
unchanged.

Every module it imports is the copy `../promote.py` made in this folder, loaded by path under a
name of its own, never the shared one in `Experiments/`: that is what keeps it frozen.  It re-fits
nothing, and it computes no performance figure -- the engine does.

`../daily_update.py` calls into here; it never re-derives the rule itself.  A strategy with no
book on paper keeps this file as it is: the contract, with no logic.

See `../BITACORA.md` for the gate, and `../../RESULTS.md` for the numbers a candidate is judged on.
"""

# --- example: begin ---

import dataclasses
import datetime
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import types

import pandas

__all__ = [
    "BANDS",
    "BookRun",
    "run",
]

BOOK_DIRECTORY = pathlib.Path(__file__).parent
ENGINE_CACHE_DIRECTORY = BOOK_DIRECTORY / "Backtest" / "cache"
FREEZE_PATH = BOOK_DIRECTORY / "FREEZE.json"
REFINERY_SCRIPT = BOOK_DIRECTORY / "Data" / "refinery.py"
SECURITY_MASTER_PATH = BOOK_DIRECTORY / "Universe" / "Security_Master.csv"

# The rule's settings, as `experiment_1_marimo.py`'s setup cell holds them and `BLUEPRINT_1.md`
# fixed them; `FREEZE.json` records the commit.  The experiment's window opened on its first day
# and ended on the last day the Core and the factor model reach.
WINDOW_START = pandas.Timestamp("2000-01-03")
EXPERIMENT_END = pandas.Timestamp("2026-08-14")
MAXIMUM_WEIGHT = 0.20
MINIMUM_WEIGHT = 0.01
BAND = 0.005
TREND_COLUMN = "r_trend_50_200"
SCORE_COLUMN = "r_traded_value_sma_63d"
MEMBERSHIP_COLUMN = "r_index_weight"
FILL_COLUMN = "c_open_dividend_and_split_adjusted"
MARK_COLUMN = "c_close_dividend_and_split_adjusted"
# The blocking rows of `Universe/Data_Issues.csv` the experiment ran with, its
# `EXPECTED_EXCLUSIONS`: fixed here, because the register is regenerated and the book is not.
EXCLUDED_IDENTIFIERS = (
    "FPS",
    "H1",
    "ILA.A",
    "MDLN",
    "Q",
    "SUNB",
    "TXCCQ",
)

# The costs of the flat 5 bp row, the row the owner reads the gate at: commission in basis points
# of the notional, a flat half-spread, the 1% cash reserve, on $1,000,000.  The cash's rate and its
# spread are the frozen engine module's, as the experiment priced them.
INITIAL_CAPITAL = 1_000_000
COMMISSION_BASIS_POINTS = 1.0
SLIPPAGE_MODEL = "basis_points"
SLIPPAGE_BASIS_POINTS = 5.0
CASH_RESERVE = 0.01

# The index is priced while its returns reach the day; past their end, `SPY` alone, and the run
# says so.
FALLBACK_BENCHMARK = "SPY"
# The days a recent trade is counted over, the record's measure of how often the book trades.
RECENT_TRADING_DAYS = 63
WEIGHT_TOLERANCE = 1e-9

# For each diagnostic, the range outside which a day is flagged; a flag, not a stop.  Taken from
# `FINDINGS_1.md`'s structural table and registered in `../BITACORA.md` before the book's first
# day: names held 19 to 58, invested 92.8% at the lowest, at most 75 rule orders on a date.  The
# largest target's upper end is the rule's own cap, and a held name with its cross at 0 at the close
# before the last rebalance is what the experiment's invariants never allowed.
BANDS = {
    "holdings": (
        19.0,
        58.0,
    ),
    "invested share": (
        0.928,
        1.0,
    ),
    "largest target weight": (
        0.0,
        0.2,
    ),
    "names held with the cross at 0 at the close before the last rebalance": (
        0.0,
        0.0,
    ),
    "rule orders on the last rebalance date": (
        0.0,
        75.0,
    ),
}


@dataclasses.dataclass(frozen=True)
class BookRun:
    """
    One day's run of the book: what the record keeps, and what the log says.

    `results` maps a window and a series -- `("whole", "book")` -- to the frozen engine module's
    answer, a dictionary of plain pandas objects; `books` is the book and the control in force that
    day, one row per holding.
    """

    as_of: "datetime.date"
    books: "pandas.DataFrame"
    diagnostics: "pandas.DataFrame"
    flags: list[dict[str, str]]
    results: dict[tuple[str, str], dict[str, object]]
    summary: list[str]


@dataclasses.dataclass(frozen=True)
class Panel:
    """
    Everything the rule reads, on one calendar and one set of positions, up to the day.

    `cut` holds the refined matrices the rule cell reads, by column name; `membership`, `priced`
    and `allowed` are the notebook's own, and `rebalance_dates` its calendar.
    """

    allowed: "pandas.Series"
    cut: dict[str, "pandas.DataFrame"]
    membership: "pandas.DataFrame"
    priced: "pandas.DataFrame"
    rebalance_dates: "pandas.DatetimeIndex"


def run(
    as_of: "datetime.date",
) -> "BookRun":
    """
    Run the frozen book for one day: refine, rule, engine, and what the day looked like.
    """
    modules = _load_frozen_modules()
    _run_frozen_refinery()
    day = pandas.Timestamp(as_of)
    panel = _load_panel(
        modules,
        day,
    )
    construction = modules["portfolio_construction"]
    targets = _target_book(
        panel,
        construction,
        True,
    )
    book = _strike(
        panel,
        construction,
        targets,
    )
    control = _strike(
        panel,
        construction,
        _target_book(
            panel,
            construction,
            False,
        ),
    )
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    freeze_day = pandas.Timestamp(freeze["freeze_date"])
    benchmark = _choose_benchmarks(
        modules,
        day,
    )
    windows = _window_starts(
        panel.rebalance_dates,
        freeze_day,
        day,
    )
    results = {}
    flags = list(benchmark["flags"])
    shutil.rmtree(
        ENGINE_CACHE_DIRECTORY,
        ignore_errors=True,
    )
    modules["backtest_engine"].stage_market_data()

    for window, start in windows.items():
        answers = _price_window(
            modules,
            window,
            {
                "book": book,
                "control": control,
            },
            start,
            day,
            benchmark["identifiers"],
        )

        for series, answer in answers.items():
            results[(window, series)] = answer

            if not str(answer["window"]).startswith("complete"):
                flags.append({
                    "kind": "truncated-run",
                    "detail": f"{window} {series}: {answer['window']}",
                    "severity": "stop",
                })

    return BookRun(
        as_of=as_of,
        books=_books_table(
            book,
            control,
            modules,
        ),
        diagnostics=_diagnostics(
            panel,
            targets,
            book,
            day,
        ),
        flags=flags,
        results=results,
        summary=_summary(
            results,
            book,
            day,
        ),
    )


def _books_table(
    book: "pandas.DataFrame",
    control: "pandas.DataFrame",
    modules: dict[str, "types.ModuleType"],
) -> "pandas.DataFrame":
    """
    The book and the control in force on the day, by listing, one row per holding.
    """
    rows = []

    for series, weights in (("book", book), ("control", control)):
        latest = weights.iloc[[-1]]
        by_identifier = modules["securities_panel"].expand_to_identifiers(latest)
        held = by_identifier.iloc[-1]

        for identifier, weight in held[held > 0].items():
            rows.append({
                "series": series,
                "identifier": identifier,
                "weight": float(weight),
                "since": latest.index[-1].date().isoformat(),
            })

    return pandas.DataFrame(rows)


def _choose_benchmarks(
    modules: dict[str, "types.ModuleType"],
    day: "pandas.Timestamp",
) -> dict[str, object]:
    """
    The index and `SPY` when the index's series reaches the day, else `SPY` alone, flagged.
    """
    engine = modules["backtest_engine"]
    reader = modules["time_series"]
    index_path = reader.path_for(
        engine.CURATED_DIRECTORY,
        engine.INDEX_IDENTIFIER,
    )
    index_dates = reader.read_frame(
        index_path,
        ("m_date",),
    )["m_date"]
    index_end = pandas.Timestamp(index_dates.max())

    if index_end >= day:

        return {
            "flags": [],
            "identifiers": engine.BENCHMARK_IDENTIFIERS,
        }

    detail = " ".join([
        f"the index's returns end {index_end.date()}:",
        f"priced against {FALLBACK_BENCHMARK} until the desk's files reach the day",
    ])

    return {
        "flags": [
            {
                "kind": "benchmark-fallback",
                "detail": detail,
                "severity": "flag",
            },
        ],
        "identifiers": (FALLBACK_BENCHMARK,),
    }


def _diagnostics(
    panel: "Panel",
    targets: "pandas.DataFrame",
    book: "pandas.DataFrame",
    day: "pandas.Timestamp",
) -> "pandas.DataFrame":
    """
    What the book looked like on the day, from its last struck row: its shape, not its return.

    The orders and the names the band kept are counted as section 3 of the notebook counts them.
    """
    latest = book.iloc[-1]
    held = latest[latest > 0]
    last_rebalance = book.index[-1]
    master = pandas.read_csv(SECURITY_MASTER_PATH).set_index("main_identifier")
    sectors = master["sector"].reindex(held.index).fillna("unknown")
    sector_shares = held.groupby(sectors).sum()
    trend_before = panel.cut[TREND_COLUMN].shift(1).loc[last_rebalance]
    broken = [
        name
        for name in held.index
        if not float(trend_before.get(name, 0.0)) > 0
    ]
    previous_held = book.shift(1).fillna(0.0) > 0
    departed = (book - targets).abs() > WEIGHT_TOLERANCE
    kept = previous_held & (targets > 0) & departed
    touched = (book > 0) | previous_held
    orders = (touched & ~kept).sum(axis=1)
    calendar = panel.cut[MARK_COLUMN].index
    recent_days = calendar[calendar <= day][-RECENT_TRADING_DAYS:]
    recent_trades = book.index[book.index >= recent_days[0]]
    invested = float(held.sum())
    squares = latest.pow(2)
    squared = float(squares.sum())
    effective_names = 1.0 / squared if squared > 0 else 0.0
    largest_sector_weight = sector_shares.max() if len(sector_shares) > 0 else 0.0
    largest_share = float(largest_sector_weight)
    largest_sector = largest_share / invested if invested > 0 else 0.0
    measures = {
        "holdings": float(len(held)),
        "invested share": invested,
        "largest target weight": float(targets.iloc[-1].max()),
        "names held with the cross at 0 at the close before the last rebalance": float(len(broken)),
        "rule orders on the last rebalance date": float(orders.iloc[-1]),
        "held names kept by the band on the last rebalance date": float(kept.iloc[-1].sum()),
        "effective names": effective_names,
        "largest sector share": largest_sector,
        "trade dates in the last 63 days": float(len(recent_trades)),
        "traded today": float(last_rebalance == day),
    }

    return pandas.DataFrame({
        "date": day.date().isoformat(),
        "measure": list(measures),
        "value": list(measures.values()),
    })


def _eligibility(
    panel: "Panel",
    use_cross: bool,
) -> "pandas.DataFrame":
    """
    Who may be held on each rebalance date, decided at the prior close, as the rule cell decides.

    A member at the close before d with a 200-day history and the golden cross at 1 then, a traded
    value then, an open on d, not excluded by name.  The control keeps everything but the cross's
    sign.
    """
    trend_before = panel.cut[TREND_COLUMN].shift(1)
    member_before = panel.membership.shift(
        1,
        fill_value=False,
    )
    score_before = panel.cut[SCORE_COLUMN].shift(1)
    has_history = trend_before.notna()
    has_score = score_before.notna()
    eligible = member_before & has_history & has_score & panel.priced & panel.allowed
    in_cross = eligible & (trend_before > 0) if use_cross else eligible

    return in_cross.loc[panel.rebalance_dates]


def _load_frozen_modules() -> dict[str, "types.ModuleType"]:
    """
    The copies `promote.py` froze in this folder, each under a name no other book's copy uses.

    The engine and panel modules import `time_series` by name, from the folder beside them, so the
    frozen copy is registered under that name before they load: a shared copy imported earlier in
    the same process would otherwise be the one they found.
    """
    locations = {
        "time_series": BOOK_DIRECTORY / "Data" / "time_series.py",
        "hand_supplied": BOOK_DIRECTORY / "Data" / "hand_supplied.py",
        "securities_panel": BOOK_DIRECTORY / "Experiments" / "securities_panel.py",
        "portfolio_construction": BOOK_DIRECTORY / "Experiments" / "portfolio_construction.py",
        "backtest_engine": BOOK_DIRECTORY / "Experiments" / "backtest_engine.py",
    }
    modules = {}

    for name, path in locations.items():
        unique_name = f"{BOOK_DIRECTORY.name.lower()}_{name}"
        specification = importlib.util.spec_from_file_location(
            unique_name,
            path,
        )
        module = importlib.util.module_from_spec(specification)
        sys.modules[unique_name] = module

        if name == "time_series":
            sys.modules["time_series"] = module

        specification.loader.exec_module(module)
        modules[name] = module

    return modules


def _load_panel(
    modules: dict[str, "types.ModuleType"],
    day: "pandas.Timestamp",
) -> "Panel":
    """
    The refined panel up to the day, as section 1 of the notebook reads it, and the calendar.

    The refinery never carries membership past the last date the desk wrote, which is right for a
    backtest and would empty a paper book the day the desk's files fall behind: past that date the
    last membership the desk wrote is held, and `daily_update.py` flags every day it is.  Inside the
    experiment's window the desk covers every day, so the rule it ran is unchanged.
    """
    matrices = modules["securities_panel"].load_matrices((
        TREND_COLUMN,
        SCORE_COLUMN,
        MEMBERSHIP_COLUMN,
        FILL_COLUMN,
        MARK_COLUMN,
    ))
    cut = {
        name: matrix.loc[:day]
        for name, matrix in matrices.items()
    }
    weights = cut[MEMBERSHIP_COLUMN].fillna(0.0)
    desk_holdings = modules["hand_supplied"].read_benchmark_holdings()
    desk_end = desk_holdings.index.max()
    written = weights.loc[weights.index <= desk_end]
    held = written.reindex(
        weights.index,
        method="ffill",
    )
    calendar = cut[FILL_COLUMN].index
    window_days = calendar[(calendar >= WINDOW_START) & (calendar <= day)]
    rebalance_dates = modules["portfolio_construction"].first_trading_days_of_month(window_days)
    allowed = pandas.Series(
        ~cut[FILL_COLUMN].columns.isin(EXCLUDED_IDENTIFIERS),
        index=cut[FILL_COLUMN].columns,
    )

    return Panel(
        allowed=allowed,
        cut=cut,
        membership=held.fillna(0.0) > 0,
        priced=cut[FILL_COLUMN].notna(),
        rebalance_dates=rebalance_dates,
    )


def _price_window(
    modules: dict[str, "types.ModuleType"],
    window: str,
    books: dict[str, "pandas.DataFrame"],
    start: "pandas.Timestamp",
    end: "pandas.Timestamp",
    benchmark_identifiers: tuple[str, ...],
) -> dict[str, dict[str, object]]:
    """
    Write one window's weight files in this folder and price them in one batch of the frozen engine.

    Each book is written from the window's first rebalance date, as the notebook wrote its
    sub-periods, and the book and its control share every setting but their weights, so one load of
    the market data prices both.
    """
    engine = modules["backtest_engine"]
    tasks = []
    names = {}

    for series, weights in books.items():
        name = f"paper_{window}_{series}"
        inside = weights.loc[weights.index >= start]
        engine.write_weight_file(
            modules["securities_panel"].expand_to_identifiers(inside),
            BOOK_DIRECTORY,
            name,
        )
        tasks.append({
            "experiment_directory": str(BOOK_DIRECTORY),
            "portfolio_name": name,
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
            "initial_capital": INITIAL_CAPITAL,
            "commission_basis_points": COMMISSION_BASIS_POINTS,
            "slippage_model": SLIPPAGE_MODEL,
            "slippage_basis_points": SLIPPAGE_BASIS_POINTS,
            "cash_reserve_percentage": CASH_RESERVE,
            "benchmark_identifiers": tuple(benchmark_identifiers),
        })
        names[series] = name

    priced = engine.price_batch(tasks)
    answers = {}

    for series, name in names.items():
        answer = priced[name]

        if not answer["success"]:
            refused_message = f"the engine refused {name}: {answer['error']}"

            raise RuntimeError(refused_message)

        answers[series] = answer

    return answers


def _run_frozen_refinery() -> None:
    """
    Run the refinery frozen in this folder over the raw files linked into it.
    """
    completed = subprocess.run(
        [
            sys.executable,
            str(REFINERY_SCRIPT),
        ],
        check=False,
        cwd=BOOK_DIRECTORY,
    )

    if completed.returncode != 0:
        message = f"the frozen refinery stopped with exit code {completed.returncode}"

        raise RuntimeError(message)


def _strike(
    panel: "Panel",
    construction: "types.ModuleType",
    targets: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    The book struck on each date: the target, except where the band keeps a held name.
    """

    return construction.banded_book(
        targets,
        panel.cut[MARK_COLUMN].shift(1),
        panel.cut[FILL_COLUMN],
        BAND,
    )


def _summary(
    results: dict[tuple[str, str], dict[str, object]],
    book: "pandas.DataFrame",
    day: "pandas.Timestamp",
) -> list[str]:
    """
    The log's lines for the day: each window's engine figures for the book and its control.
    """
    lines = [
        f"traded today: {book.index[-1] == day}; last trade {book.index[-1].date()}",
    ]

    for (window, series), answer in results.items():
        statistics = answer["portfolio_stats"]
        lines.append(" ".join([
            f"{window} {series}:",
            f"CAGR {float(statistics['Annualized Return (CAGR)']):.4f},",
            f"Sharpe {float(statistics['Portfolio Sharpe Ratio']):.3f},",
            f"max drawdown {float(statistics['Max Drawdown']):.4f}",
        ]))

    return lines


def _target_book(
    panel: "Panel",
    construction: "types.ModuleType",
    use_cross: bool,
) -> "pandas.DataFrame":
    """
    The target on every rebalance date; the bounds set the count, the seam cuts the score.
    """

    return construction.bounded_book(
        _eligibility(
            panel,
            use_cross,
        ),
        panel.cut[SCORE_COLUMN],
        MAXIMUM_WEIGHT,
        MINIMUM_WEIGHT,
    )


def _window_starts(
    rebalance_dates: "pandas.DatetimeIndex",
    freeze_day: "pandas.Timestamp",
    day: "pandas.Timestamp",
) -> dict[str, "pandas.Timestamp"]:
    """
    The first rebalance date of each window the record keeps, for the windows that have begun.

    The whole history opens on the experiment's first rebalance date; the days after its window, on
    the first rebalance after 2026-08-14; the paper days, on the first rebalance on or after the
    freeze date.  A window whose first rebalance date has not passed yet is not priced.
    """
    candidates = {
        "whole": rebalance_dates[rebalance_dates >= WINDOW_START],
        "after_window": rebalance_dates[rebalance_dates > EXPERIMENT_END],
        "since_freeze": rebalance_dates[rebalance_dates >= freeze_day],
    }

    return {
        window: dates[0]
        for window, dates in candidates.items()
        if len(dates) > 0 and dates[0] < day
    }

# --- example: end ---
