import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Experiment 1 — the first rule against the benchmark

    **Steps 4, 5 and 6 of 8 — portfolio, backtest, attribution — for one idea.**

    **It produces** a book in `Portfolio/`, a track record in `Backtest/` and a breakdown of the
    return in `Attribution/`. **It prevents** a good signal in a portfolio nobody could hold, paper
    returns that real trading would have erased, and factor beta sold as alpha.

    Experiment 1 is the **first rule tested against the benchmark** `JOURNAL_1.md` chose, and the
    yardstick every later experiment is also measured against. It is not a null. It is a real
    strategy with a real return, and it can graduate like any other — **its rules freeze once
    `FINDINGS_1.md` reports**, because a change to them invalidates every comparison in
    `RESULTS.md`. Improvements go into a new experiment, unless the owner rewrites this one, as
    `AGENTS.md` says.

    The hypothesis is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md), **written before this notebook's
    rule**. The running log is [`JOURNAL_1.md`](JOURNAL_1.md); the results that survive are in
    [`FINDINGS_1.md`](FINDINGS_1.md).

    **A marimo notebook.** From the repository's root,
    `uv run python Experiments/Experiment_1/experiment_1_marimo.py` runs every cell as a script and
    saves no output in the file; `uv run marimo edit Experiments/Experiment_1/experiment_1_marimo.py`
    opens it cell by cell, and its session cache, `__marimo__/`, is never committed. **In the
    template it holds the cells every strategy runs** — marimo's own, and the setup that finds the
    repository and imports the shared modules — and, for each section, what is expected in it.
    Write the other cells beneath each section's description.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The rule is [`BLUEPRINT_1.md`](BLUEPRINT_1.md)'s, committed before this notebook held a line of
    it: on the first trading day of each month, at the open, the KN US Equity Core's members with a
    golden cross at the month's last close, ranked and weighted by 63-day traded value, no weight
    above 20% and none below 1%, a held name left alone when its target moved by half a point or
    less; cash paid at the Fed funds rate less half a point; every cost inside the engine; judged
    against the KN US Equity Core, `SPY` and the same rule without the cross, from 2000-01-03 to
    2026-08-14. **Every figure comes from the engine or the attribution library**; this notebook
    only writes books, asks for their prices and reads the answers.
    """)
    return


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Position in the pipeline

    This notebook is **only the strategy**. The universe and the data are built by earlier stages and
    are simply read here:

    ```
    Universe/universe_marimo.py   ->  Security_Master.csv, Data_Issues.csv
    Data/curator.py               ->  Data/Curator/Time_Series/     m_* + c_*
    Data/refinery.py              ->  Data/Refinery/Time_Series/    + r_*      <- read here
    Data/analyzer_marimo.py       ->  the measurements the blueprint's predictions came from
            |
            v
    experiment_1_marimo.py        ->  Portfolio/  ->  Backtest/  ->  Attribution/
    ```

    **What this notebook does not do.** It does not download anything, profile the universe, or
    compute a signal. A number about the data itself belongs in the Universe or Data stage, and a
    signal a new experiment needs, on data already downloaded, is an `r_*` calculation in the
    refinery, never a wider download — that separation is what keeps every experiment comparable,
    because all of them read the identical panel.

    **Four modules beside this notebook are shared by every experiment** — `securities_panel.py`,
    `portfolio_construction.py`, `backtest_engine.py` and `attribution_analysis.py`, one per Lab
    library — and no strategy column is named in any of them.

    ## The section contract

    Every experiment notebook has the same shape, so anyone who has read one can read all of them.

    | Section | Contains |
    | --- | --- |
    | 0 · Setup | the repository and the shared modules, then **the strategy's window, columns, bounds and costs** — the only strategy names outside the rule |
    | 1 · The panel | load the refined files, reshape them, and the rebalance calendar |
    | 2 · The rule | selection, sizing, timing, and the control. **The one cell you write** |
    | 2.1 · Invariants | what every rule must pass, whatever it is |
    | 3 · Construction | the book, the diagnostics a person would run it on, and every weight file |
    | 4 · Backtest | the engine, guarded; every cost and the cash priced inside it; every run read whole or excluded by name |
    | 5 · Attribution | where the return came from, guarded the same way |
    | 6 · Counterfactuals | the sweep, and the arms that price who earned the idiosyncratic share |
    | 7 · Verdict | what it concluded, **in words**, the gate read row by row, the handoff and the open items |
    | 8 · Verify | assertions that raise when the output is wrong |
    | 9 · Dashboards | optional: the engine's and the attribution library's own, to look at a run, never to quote |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Setup

    **The cell below is every strategy's.** It finds the repository's root, whichever folder the
    notebook started in, puts `Experiments/` and `Data/` on the import path, and imports the four
    shared modules and `Data/hand_supplied.py`. Then the strategy's own setup, in a cell of its own:
    the window, the columns, the bounds, the costs and the arms, as `BLUEPRINT_1.md` fixed them.
    **Declare them here, not in a shared module**, so a signal never becomes every later
    experiment's default without anyone deciding it. Read only the columns the strategy consumes.

    **And the exclusions**: the names the blocking rows of `Universe/Data_Issues.csv` list, read from
    the register and never typed — typed once more beside them, as the blueprint names them, only so
    section 8 can check that the two agree. A blocking row is a label until a stage reads it; this is
    the stage.

    **Three price columns do three different jobs** — the daily mark, the fill, and the price a
    commission ticket is written in — and getting them out of step is silent: the backtest P&L and
    the attribution would quietly run on different bases. The mark and the fill share one
    total-return basis, and the fill is a price a real order gets.

    **The costs and the cash are settings of the engine**, named here once: commission in basis
    points; the engine's spread-and-impact slippage and the half-spread it falls back on; the flat
    half-spread every book is priced again at; a stress row and a small account beside the base; the
    cash reserve; and how much of its window a run must value to be read.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three price columns do **three different jobs**, and getting them out of step is silent:

    | Role | Column | Why |
    | --- | --- | --- |
    | Daily mark | `c_close_dividend_and_split_adjusted` | the total-return close the Curator rebuilt from the exact close and the actions |
    | Fill | `c_open_dividend_and_split_adjusted` | the next day's open, a market-on-open order, on the same basis |
    | Commission price | `c_open` | the open a ticket shows; commission itself is basis points of the notional |

    Every cost is the engine's: commission in basis points, slippage from its spread-and-impact model
    on the day's range and volume, and the interest on cash from FRED's `DFF` less half a point,
    which is also the risk-free rate of every Sharpe ratio below.
    """)
    return


# --- example: end ---


@app.cell
def _():
    import os
    import pathlib
    import sys

    import numpy
    import pandas

    # Every path below is relative to the repository root, whichever folder the notebook started in.
    NOTEBOOK_DIRECTORY = pathlib.Path.cwd()
    REPOSITORY_ROOT = next(
        folder
        for folder in (NOTEBOOK_DIRECTORY, *NOTEBOOK_DIRECTORY.parents)
        if (folder / "Experiments").is_dir() and (folder / "Universe").is_dir()
    )
    os.chdir(REPOSITORY_ROOT)
    sys.path.insert(0, str(REPOSITORY_ROOT / "Experiments"))
    sys.path.insert(0, str(REPOSITORY_ROOT / "Data"))

    import attribution_analysis  # noqa: E402 - the paths above have to exist first
    import backtest_engine  # noqa: E402
    import hand_supplied  # noqa: E402
    import portfolio_construction  # noqa: E402
    import securities_panel  # noqa: E402

    EXPERIMENT_DIRECTORY = REPOSITORY_ROOT / "Experiments" / "Experiment_1"
    return (
        EXPERIMENT_DIRECTORY,
        attribution_analysis,
        backtest_engine,
        hand_supplied,
        numpy,
        pandas,
        portfolio_construction,
        securities_panel,
    )


# --- example: begin ---


@app.cell
def _(attribution_analysis, backtest_engine, pandas):
    # The window, the bounds, the band and the columns, as BLUEPRINT_1.md fixed them.
    WINDOW_START = pandas.Timestamp("2000-01-03")
    WINDOW_END = pandas.Timestamp("2026-08-14")
    SUB_PERIODS = (
        ("2000 to 2008", WINDOW_START, pandas.Timestamp("2008-12-31")),
        ("2009 to 2017", pandas.Timestamp("2009-01-01"), pandas.Timestamp("2017-12-31")),
        ("2018 to 2026", pandas.Timestamp("2018-01-01"), WINDOW_END),
    )
    MAXIMUM_WEIGHT = 0.20
    MINIMUM_WEIGHT = 0.01
    BAND = 0.005
    TREND_COLUMN = "r_trend_50_200"
    SCORE_COLUMN = "r_traded_value_sma_63d"
    MEMBERSHIP_COLUMN = "r_index_weight"
    FILL_COLUMN = "c_open_dividend_and_split_adjusted"
    MARK_COLUMN = "c_close_dividend_and_split_adjusted"
    EXPECTED_EXCLUSIONS = (
        "FPS",
        "H1",
        "ILA.A",
        "MDLN",
        "Q",
        "SUNB",
        "TXCCQ",
    )

    # The costs every verdict is read at, the stress row and the small account beside them.
    INITIAL_CAPITAL = 1_000_000
    SMALL_CAPITAL = 100_000
    COMMISSION_BASIS_POINTS = 1.0
    SLIPPAGE_MODEL = "spread_plus_impact"
    SLIPPAGE_BASIS_POINTS = 5.0
    STRESS_COMMISSION_BASIS_POINTS = 5.0
    STRESS_SLIPPAGE_MODEL = "basis_points"
    STRESS_SLIPPAGE_BASIS_POINTS = 10.0
    # Every book priced again at the blueprint's own fallback half-spread, flat: the engine's
    # range-based spread estimates read a megacap's daily range as spread (JOURNAL_1, 2026-10-24).
    FLAT_SLIPPAGE_MODEL = "basis_points"
    FLAT_SLIPPAGE_BASIS_POINTS = 5.0
    FLAT_SUFFIX = ", flat 5 bp"
    CASH_RESERVE = 0.01
    # A run the engine stopped valuing before its window's end is excluded by name, never read.
    VALUED_SHARE_REQUIRED = 0.99
    UNVALUED_DAYS_AT_END_ALLOWED = 5

    # The sweep, one setting at a time; the band, read on turnover; the seeds; the workers.
    SWEEP = (
        ("cap 15%", {"maximum_weight": 0.15}),
        ("cap 25%", {"maximum_weight": 0.25}),
        ("floor 0.5%", {"minimum_weight": 0.005}),
        ("floor 2%", {"minimum_weight": 0.02}),
        ("traded value over 21 days", {"score_column": "r_traded_value_sma_21d"}),
        ("traded value over 126 days", {"score_column": "r_traded_value_sma_126d"}),
        ("cross 20/100", {"trend_column": "r_trend_20_100"}),
        ("cross 100/300", {"trend_column": "r_trend_100_300"}),
    )
    BAND_SWEEP = (
        ("band 0.25 points", 0.0025),
        ("band 1.0 point", 0.01),
    )
    RANDOM_SEEDS = tuple(range(1, 21))
    # Engine batches at once: each loads the whole universe, so more than six compete for the disk.
    WORKERS = 6
    # Attribution books at once: each holds the universe's returns and the factor files in memory.
    ATTRIBUTION_WORKERS = 4

    # The window is the universe notebook's, and the exclusions are its register's blocking rows: the
    # blueprint fixed both, and a run on anything else is not this experiment.
    window_written = pandas.read_csv("Universe/Window.csv")
    issues = pandas.read_csv("Universe/Data_Issues.csv").fillna("")
    blocking = issues[
        (issues["severity"] == "blocking") & ~issues["check"].str.startswith("missing file")
    ]
    EXCLUDED = tuple(sorted({
        identifier
        for identifiers in blocking["identifiers"]
        for identifier in str(identifiers).split()
    }))
    print(f"window {WINDOW_START.date()} to {WINDOW_END.date()}; the universe notebook's: "
          f"{window_written['window_start'].iloc[0]} to {window_written['window_end'].iloc[0]}")
    print(f"excluded by name: {', '.join(EXCLUDED)}")
    print(f"engine installed: {backtest_engine.ENGINE_INSTALLED}; "
          f"attribution installed: {attribution_analysis.LIBRARY_INSTALLED}")
    return (
        ATTRIBUTION_WORKERS,
        BAND,
        BAND_SWEEP,
        CASH_RESERVE,
        COMMISSION_BASIS_POINTS,
        EXCLUDED,
        EXPECTED_EXCLUSIONS,
        FILL_COLUMN,
        FLAT_SLIPPAGE_BASIS_POINTS,
        FLAT_SLIPPAGE_MODEL,
        FLAT_SUFFIX,
        INITIAL_CAPITAL,
        MARK_COLUMN,
        MAXIMUM_WEIGHT,
        MEMBERSHIP_COLUMN,
        MINIMUM_WEIGHT,
        RANDOM_SEEDS,
        SCORE_COLUMN,
        SLIPPAGE_BASIS_POINTS,
        SLIPPAGE_MODEL,
        SMALL_CAPITAL,
        STRESS_COMMISSION_BASIS_POINTS,
        STRESS_SLIPPAGE_BASIS_POINTS,
        STRESS_SLIPPAGE_MODEL,
        SUB_PERIODS,
        SWEEP,
        TREND_COLUMN,
        UNVALUED_DAYS_AT_END_ALLOWED,
        VALUED_SHARE_REQUIRED,
        WINDOW_END,
        WINDOW_START,
        WORKERS,
        window_written,
    )


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · The panel

    Load the refined files through `securities_panel.py`, resolve **one position per security**, and
    reshape them to `dates x securities` matrices, one per column the setup names, on one calendar.
    Nothing after the window's last day is read by any cell below.

    A point-in-time universe contains renamed securities: two identifiers sharing one identity, each
    carrying part of the history. Left alone they are two independent positions and the book
    double-counts at the changeover; the panel stitches them.

    Then the calendar the book trades on — the first trading day of each month, say, each decided on
    the close before it — from `portfolio_construction.py`, so every book of the experiment trades on
    the same dates.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Load the refined files, resolve **one position per security**, and reshape to `dates x
    securities` matrices. Then the calendar: **the first trading day of each month**, the day the
    orders go in, each decided on the close before it.
    """)
    return


@app.cell
def _(
    EXCLUDED,
    FILL_COLUMN,
    MARK_COLUMN,
    MEMBERSHIP_COLUMN,
    SCORE_COLUMN,
    TREND_COLUMN,
    WINDOW_END,
    WINDOW_START,
    pandas,
    portfolio_construction,
    securities_panel,
):
    COLUMNS = (
        TREND_COLUMN,
        "r_trend_20_100",
        "r_trend_100_300",
        SCORE_COLUMN,
        "r_traded_value_sma_21d",
        "r_traded_value_sma_126d",
        MEMBERSHIP_COLUMN,
        FILL_COLUMN,
        MARK_COLUMN,
    )
    matrices = securities_panel.load_matrices(COLUMNS)
    # Nothing after the window's last day is read by any cell below.
    cut = {
        name: matrix.loc[:WINDOW_END]
        for name, matrix in matrices.items()
    }
    membership = cut[MEMBERSHIP_COLUMN].fillna(0.0) > 0
    # A name is tradable on a day it has an open to fill at; a delisted name's last price is the
    # engine's to sell at, so no day of hindsight is taken here.
    priced = cut[FILL_COLUMN].notna()
    allowed = pandas.Series(
        ~cut[FILL_COLUMN].columns.isin(EXCLUDED),
        index=cut[FILL_COLUMN].columns,
    )
    calendar = cut[FILL_COLUMN].index
    window_days = calendar[(calendar >= WINDOW_START) & (calendar <= WINDOW_END)]
    REBALANCE_DATES = portfolio_construction.first_trading_days_of_month(window_days)
    print(f"panel: {len(calendar)} dates x {len(allowed)} positions; window: {len(window_days)} days")
    print(f"rebalance dates: {len(REBALANCE_DATES)}, the first {REBALANCE_DATES[0].date()}, "
          f"the last {REBALANCE_DATES[-1].date()}")
    print(f"members per window day: {int(membership.loc[window_days].sum(axis=1).min())} "
          f"to {int(membership.loc[window_days].sum(axis=1).max())}")
    return REBALANCE_DATES, allowed, cut, membership, priced, window_days


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · The rule — the one cell you write

    Three statements, in order: **who is eligible**, **how much of each**, and **when to trade**.
    Everything below reads what this cell produces: `REBALANCE_DATES`, the days the book is struck;
    `target_weights`, `REBALANCE_DATES x securities`, its rows summing to **at most** 1.0; and, under
    a no-trade band, `struck_weights`, the book actually struck — the target, except where the band
    leaves a held name as it drifted. The control is written here too, on the rule's own dates.

    **Rows sum to at most one, not to exactly one.** A book that must be fully invested cannot express
    a defensive strategy. What the weights leave is cash, which the engine pays interest on.

    **Sizing is a seam, not a decision buried in the rule.** Hand the eligible set and a history
    already cut off before today to a weighting function in `portfolio_construction.py`, and
    swapping equal weight for inverse volatility, hierarchical risk parity or any other method of the
    KaxaNuk Portfolio Construction library is one line. That is what makes two experiments comparable
    rather than merely adjacent.

    ### The look-aheads, stated plainly

    **The lag.** Everything the rule reads on a rebalance date *d* is read at the close of the trading
    day before it, and the fill is at *d*'s price. A condition read on *d* itself — a price to fill
    at — is named as the one same-day condition.

    **No delisting exit.** The engine sells a position whose prices stop at its last price, so the
    rule takes no day of hindsight for it. A gap inside a series, which the engine cannot price, is a
    blocking row of the register, and the name is excluded by name.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Object | Type | Meaning |
    | --- | --- | --- |
    | `REBALANCE_DATES` | a date index | the first trading day of each month |
    | `target_weights` | `REBALANCE_DATES x securities`, rows at most 1.0 | the target on each date |
    | `struck_weights` | the same shape | the book actually struck: the target, except where the band leaves a held name as it drifted |

    **Rows sum to at most one.** The rest is dollar cash, which the engine pays the cash rate.

    ### The look-aheads, stated

    **The lag.** Everything the rule reads on a rebalance date d — membership, the cross, the traded
    value, the band's drifted weights — is read at the close of the trading day before d; the fill is
    d's open. **The one condition read on d** is that the name has an open to fill at.

    **No delisting exit.** A held name whose prices stop is sold by the engine at its last price; the
    rule takes no day of hindsight for it.
    """)
    return


@app.cell
def _(
    BAND,
    FILL_COLUMN,
    MARK_COLUMN,
    MAXIMUM_WEIGHT,
    MINIMUM_WEIGHT,
    REBALANCE_DATES,
    SCORE_COLUMN,
    TREND_COLUMN,
    allowed,
    cut,
    membership,
    portfolio_construction,
    priced,
):
    # The rule, from BLUEPRINT_1.md. Who may be held on a rebalance date d: a member at the close
    # before d with a 200-day history and the golden cross at 1 then, a traded value then, an open
    # on d, not excluded by name. The control keeps everything but the cross's sign.
    def eligibility(
        trend_column: str,
        use_cross: bool,
        score_column: str,
    ) -> "pandas.DataFrame":
        """Who may be held on each rebalance date, decided at the prior close."""
        trend_before = cut[trend_column].shift(1)
        member_before = membership.shift(1, fill_value=False)
        score_before = cut[score_column].shift(1)
        eligible = member_before & trend_before.notna() & score_before.notna() & priced & allowed

        if use_cross:
            eligible = eligible & (trend_before > 0)

        return eligible.loc[REBALANCE_DATES]

    def target_book(
        trend_column: str = TREND_COLUMN,
        score_column: str = SCORE_COLUMN,
        maximum_weight: float = MAXIMUM_WEIGHT,
        minimum_weight: float = MINIMUM_WEIGHT,
        use_cross: bool = True,
    ) -> "pandas.DataFrame":
        """The target on every rebalance date; the bounds set the count, the seam cuts the score."""
        return portfolio_construction.bounded_book(
            eligibility(trend_column, use_cross, score_column),
            cut[score_column],
            maximum_weight,
            minimum_weight,
        )

    def strike(
        targets: "pandas.DataFrame",
        band: float = BAND,
    ) -> "pandas.DataFrame":
        """The book struck on each date: the target, except where the band keeps a held name."""
        return portfolio_construction.banded_book(
            targets,
            cut[MARK_COLUMN].shift(1),
            cut[FILL_COLUMN],
            band,
        )

    target_weights = target_book()
    struck_weights = strike(target_weights)
    # The control: the same rule without the cross's sign, on the rule's dates, under the same band.
    control_targets = target_book(use_cross=False)
    control_weights = strike(control_targets)
    held_counts = (target_weights > 0).sum(axis=1)
    print(f"rebalance dates: {len(REBALANCE_DATES)}")
    print(f"target holdings per date: {int(held_counts.min())} to {int(held_counts.max())}, "
          f"median {float(held_counts.median()):.0f}")
    print(f"invested, struck: {float(struck_weights.sum(axis=1).min()):.3f} to "
          f"{float(struck_weights.sum(axis=1).max()):.3f}")
    return (
        control_targets,
        control_weights,
        eligibility,
        strike,
        struck_weights,
        target_book,
        target_weights,
    )


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.1 · Invariants

    Cheap to check here, expensive to discover inside a P&L. **Every rule must pass these unchanged**,
    whatever the strategy is; this section prints them and section 8 raises on them:

    - no book is more than fully invested, and none is negatively invested;
    - no negative weights, if the strategy is long-only;
    - no target outside the bounds the blueprint names;
    - **every security paid for today had its signal on the prior close** — check the signal itself,
      not the composed eligibility, because the signal is the thing that had to exist in advance;
    - every security bought has a price to fill at on the day it is bought;
    - no name a blocking row of the register lists is ever held;
    - under a band, every struck weight is its target or a held name's drift within the band, and
      the struck weights the band leaves outside the bounds are counted;
    - the control trades only on the rule's dates.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Cheap to check here, expensive to discover inside a P&L. On the **targets**: never more than
    fully invested, no negative weight, no weight above the cap or under the floor, every holding a
    member with its cross at 1 at the prior close and an open on its date, no excluded name. On the
    **struck book**: never more than fully invested, and every weight either its target or a held
    name's drift within half a point of it — the band's excursions outside the bounds counted, as
    the blueprint's claim 3 says.
    """)
    return


@app.cell
def _(
    BAND,
    EXCLUDED,
    MAXIMUM_WEIGHT,
    MINIMUM_WEIGHT,
    REBALANCE_DATES,
    TREND_COLUMN,
    control_weights,
    cut,
    membership,
    priced,
    struck_weights,
    target_weights,
):
    held = target_weights > 0
    trend_yesterday = cut[TREND_COLUMN].shift(1).reindex_like(held)
    member_yesterday = membership.shift(1, fill_value=False).reindex_like(held)
    priced_today = priced.reindex_like(held)
    struck_held = struck_weights.reindex_like(target_weights).fillna(0.0)
    departed = (struck_held - target_weights).abs() > 1e-9
    struck_invested = struck_held.sum(axis=1)
    outside_bounds = struck_held.where(struck_held > 0)
    band_excursions = int(
        ((outside_bounds > MAXIMUM_WEIGHT + 1e-9) | (outside_bounds < MINIMUM_WEIGHT - 1e-9)).sum().sum()
    )
    invariants = {
        "no target more than fully invested": bool((target_weights.sum(axis=1) <= 1.0 + 1e-9).all()),
        "no negative target": bool((target_weights >= -1e-12).all().all()),
        "no target above the cap": bool((target_weights <= MAXIMUM_WEIGHT + 1e-9).all().all()),
        "no held target below the floor": bool(
            (~held | (target_weights >= MINIMUM_WEIGHT - 1e-9)).all().all()
        ),
        "every holding had its cross at 1 at the prior close": bool(
            (~held | (trend_yesterday > 0)).all().all()
        ),
        "every holding was a member at the prior close": bool((~held | member_yesterday).all().all()),
        "every holding has an open on its date": bool((~held | priced_today).all().all()),
        "no excluded name is ever held": not bool(
            held[[name for name in EXCLUDED if name in held]].any().any()
        ),
        "no struck book more than fully invested": bool((struck_invested <= 1.0 + 1e-6).all()),
        "no negative struck weight": bool((struck_held >= -1e-12).all().all()),
        # A kept name is decided at the close and written at the next open, so the overnight move can
        # carry it past the band: one point of allowance, and the largest excess printed below.
        "no struck weight above its target by more than the band and a point overnight": bool(
            (struck_held <= target_weights + BAND + 0.01).all().all()
        ),
        "no entry struck above its target": bool(
            (struck_held <= target_weights + 1e-9)
            .where(struck_held.shift(1, fill_value=0.0) <= 0, True).all().all()
        ),
        "the control trades only on the rule's dates": bool(
            control_weights.index.equals(REBALANCE_DATES)
        ),
    }

    for _name, _passed in invariants.items():
        print(f"{'PASS' if _passed else 'FAIL'}  {_name}")

    print(f"struck weights the band left outside the 1% to 20% bounds: {band_excursions}")
    print(f"largest struck weight above its target: {float((struck_held - target_weights).max().max()):.4f}")
    return band_excursions, invariants


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Construction — is this a book you would actually run?

    **This is where step 4, Portfolio Construction, lives.** Four properties, each with a failure mode
    a performance chart would hide: the invested share over time, the orders and the turnover, the
    holdings and their concentration, and any drift into one group. Turnover measured here is target
    to target; the engine's own orders and daily weights, in section 4, are the figures quoted.

    > **The blueprint's predictions about the *shape* of the book, rather than about its return, are
    > settled here — before any backtest.** They are the first ones that can be wrong, and the
    > cheapest to be wrong about.

    Then **every book the experiment prices is written** — the rule, its control, every arm and every
    sweep setting — before any is priced, through `backtest_engine.write_weight_file`: wide, keyed by
    the identifier the market-data files are named by, its columns summing to at most one.
    **Capacity** is read here too: each trade's size against the name's traded value at the prior
    close.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Property | What a bad value would mean |
    | --- | --- |
    | Invested share over time | the eligibility column is not doing what the analyzer says |
    | Orders and turnover | a book nobody could follow by hand at a broker |
    | Holdings and concentration | a "diversified" label on a book that is one or two positions |
    | Group drift | a disguised bet on one group |

    The orders here are the rule's own: every name that enters, leaves, or is traded back to target.
    The engine's own orders, in section 4, are the ones quoted.
    """)
    return


@app.cell
def _(
    MAXIMUM_WEIGHT,
    REBALANCE_DATES,
    SCORE_COLUMN,
    WINDOW_END,
    WINDOW_START,
    cut,
    numpy,
    pandas,
    struck_weights,
    target_weights,
):
    years = (WINDOW_END - WINDOW_START).days / 365.25
    holdings_count = (struck_weights > 0).sum(axis=1)
    effective_positions = 1 / struck_weights.pow(2).sum(axis=1).replace(0, numpy.nan)
    previous_held = (struck_weights.shift(1).fillna(0.0) > 0)
    kept = previous_held & (target_weights > 0) & ((struck_weights - target_weights).abs() > 1e-9)
    touched = (struck_weights > 0) | previous_held
    orders_per_date = (touched & ~kept).sum(axis=1)
    turnover = struck_weights.diff().abs().sum(axis=1) / 2
    turnover.iloc[0] = struck_weights.iloc[0].sum() / 2
    cap_binding = (target_weights >= MAXIMUM_WEIGHT - 1e-9).any(axis=1)
    construction = pandas.Series({
        "rebalance dates": len(REBALANCE_DATES),
        "rule orders per date, median": float(orders_per_date.median()),
        "rule orders per date, largest": int(orders_per_date.max()),
        "held names kept by the band per date, median": float(kept.sum(axis=1).median()),
        "holdings, median": float(holdings_count.median()),
        "holdings, minimum": int(holdings_count.min()),
        "holdings, maximum": int(holdings_count.max()),
        "share of dates holding 15 to 60 names": round(float(holdings_count.between(15, 60).mean()), 3),
        "effective positions, mean": round(float(effective_positions.mean()), 1),
        "share of rebalance dates the cap binds": round(float(cap_binding.mean()), 3),
        "mean invested share": round(float(struck_weights.sum(axis=1).mean()), 3),
        "lowest invested share": round(float(struck_weights.sum(axis=1).min()), 3),
        "annual turnover, one way, struck to struck": round(float(turnover.sum() / years), 2),
    })
    print(construction.to_string())
    print("\nmedian holdings and rule orders, by year:")
    print(pandas.DataFrame({
        "holdings": holdings_count.groupby(holdings_count.index.year).median(),
        "orders": orders_per_date.groupby(orders_per_date.index.year).sum(),
    }).to_string())

    # Capacity, gate criterion 4: every trade's size against the name's 63-day traded value at the
    # prior close; the largest book at which a trade stays within a share of that value.
    traded_weight = struck_weights.diff().abs()
    traded_weight.iloc[0] = struck_weights.iloc[0]
    traded_value_before = cut[SCORE_COLUMN].shift(1).reindex(
        index=struck_weights.index,
        columns=struck_weights.columns,
    )
    room = traded_value_before / traded_weight.where(traded_weight > 1e-9)
    capacity_rows = {}

    for _participation in (0.01, 0.05):
        _trade_capacity = (room * _participation).stack().dropna()
        capacity_rows[f"{_participation:.0%} of the name's 63-day traded value"] = {
            "worst trade": float(_trade_capacity.min()),
            "1st percentile of trades": float(_trade_capacity.quantile(0.01)),
            "median trade": float(_trade_capacity.median()),
        }

    capacity = pandas.DataFrame(capacity_rows).T
    print("\ncapacity -- the largest book, in dollars, at which a trade stays within the share:")
    print(capacity.map(lambda value: f"{value:,.0f}").to_string())

    master = pandas.read_csv("Universe/Security_Master.csv").set_index("main_identifier")
    sector_of = master["sector"].reindex(struck_weights.columns).fillna("unknown")
    by_sector = struck_weights.T.groupby(sector_of).sum().T
    yearly_sector = by_sector.groupby(by_sector.index.year).mean()
    top_sectors = yearly_sector.mean().sort_values(ascending=False).head(6).index
    print("\naverage weight by sector (today's labels, indicative), by year:")
    print(yearly_sector[top_sectors].round(3).to_string())
    return capacity, construction


@app.cell
def _(
    BAND_SWEEP,
    EXPERIMENT_DIRECTORY,
    MAXIMUM_WEIGHT,
    RANDOM_SEEDS,
    REBALANCE_DATES,
    SCORE_COLUMN,
    SWEEP,
    allowed,
    backtest_engine,
    control_targets,
    control_weights,
    cut,
    membership,
    numpy,
    pandas,
    portfolio_construction,
    priced,
    securities_panel,
    strike,
    struck_weights,
    target_book,
    target_weights,
):
    # Every book this experiment prices, written before any is priced: the rule and its control, the
    # sweep with a control for each setting, the band at two other widths with theirs, the
    # equal-weight arm and the random books, every one on the rule's dates under its band.
    score_before = cut[SCORE_COLUMN].shift(1)
    pool = (
        membership.shift(1, fill_value=False)
        & cut["r_trend_50_200"].shift(1).notna()
        & score_before.notna()
        & priced
        & allowed
    ).loc[REBALANCE_DATES]

    def random_targets(seed: int) -> "pandas.DataFrame":
        """As many members as the rule holds, drawn at random; as many redrawn as entered its book."""
        generator = numpy.random.default_rng(seed)
        rows = {}
        held_names = []
        previous_rule = set()

        for date in REBALANCE_DATES:
            rule_names = set(target_weights.columns[target_weights.loc[date] > 0])
            entrants = len(rule_names - previous_rule)
            available = list(pool.columns[pool.loc[date].to_numpy()])
            still_available = [name for name in held_names if name in set(available)]
            generator.shuffle(still_available)
            keep = max(0, min(len(still_available), len(rule_names) - entrants))
            kept_names = still_available[:keep]
            candidates = sorted(set(available) - set(kept_names))
            drawn = list(generator.choice(candidates, len(rule_names) - len(kept_names), replace=False))
            held_names = sorted(kept_names + drawn)
            rows[date] = portfolio_construction.bounded_by_score(
                score_before.loc[date, held_names],
                MAXIMUM_WEIGHT,
                0.0,
            )
            previous_rule = rule_names

        frame = pandas.DataFrame.from_dict(rows, orient="index")

        return frame.reindex(columns=target_weights.columns).fillna(0.0)

    equal_targets = (target_weights > 0).astype(float)
    equal_targets = equal_targets.div(equal_targets.sum(axis=1).replace(0, numpy.nan), axis=0)
    equal_targets = equal_targets.fillna(0.0).clip(upper=MAXIMUM_WEIGHT)
    books = {
        "rule": struck_weights,
        "control": control_weights,
        "equal weight": strike(equal_targets),
    }

    for _setting, _arguments in SWEEP:
        books[f"sweep, {_setting}"] = strike(target_book(**_arguments))
        books[f"sweep, {_setting}, control"] = strike(target_book(**_arguments, use_cross=False))

    for _setting, _band in BAND_SWEEP:
        books[_setting] = strike(target_weights, _band)
        books[f"{_setting}, control"] = strike(control_targets, _band)

    for _seed in RANDOM_SEEDS:
        books[f"random {_seed:02d}"] = strike(random_targets(_seed))

    file_names = {
        _label: "portfolio_weights_" + _label.replace(", ", "_").replace(" ", "_").replace("%", "pct").replace("/", "_").replace(".", "_")
        for _label in books
    }
    file_names["rule"] = "portfolio_weights"

    for _label, _weights in books.items():
        backtest_engine.write_weight_file(
            securities_panel.expand_to_identifiers(_weights),
            EXPERIMENT_DIRECTORY,
            file_names[_label],
        )

    print(f"books written: {len(books)}")
    return books, file_names


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Backtest — KaxaNuk Backtest Engine

    **In plain words:** run the rules over history, with costs, without peeking ahead.

    **This is the only backtest in the repository**, and results are accepted **net** or not at all.
    Every cost and the cash are the engine's: commission in basis points of the notional, slippage
    from its spread-and-impact model, the interest the cash earns at a rate file's rate less a
    broker's spread, a delisted name sold at its last price. **Every book is priced again at a flat
    half-spread** beside the model, so a verdict that rides on the spread estimate shows it. The books
    go to the engine together, in its batch mode, each answer cached by its weight file and settings.

    **Every run is read whole or excluded by name.** A run the engine stopped valuing before its
    window's end — a cash error at a rebalance whose costs outran the reserve, say — can still return
    figures over the stub. Count the days each run valued against the trading days of its window,
    exclude a short one **by name, with its reason**, write the list to
    `Backtest/excluded_runs.csv`, and let no cell below read it. A criterion that needs an excluded
    run reads "not evidenced".

    > **Guard the import.** The engine installs from KaxaNuk's licensed index rather than PyPI, so
    > this section reports what is missing and skips without it. Everything in `Portfolio/` is
    > already written and does not depend on the engine — a clone with no licence gets a real book
    > and no numbers, by design.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The only backtest in the repository**, and results are accepted **net** or not at all. The
    engine fills at the open, holds integer shares and a 1% cash reserve, charges commission in basis
    points and slippage from its own spread-and-impact model, pays the cash the Fed funds rate less
    half a point, sells a delisted name at its last price, and marks the book daily. Every book is
    priced at the base costs over the window; the rule and the control are priced again at the
    stress costs, at $100,000, and over each sub-period from its first rebalance date.
    """)
    return


@app.cell
def _(
    CASH_RESERVE,
    COMMISSION_BASIS_POINTS,
    EXPERIMENT_DIRECTORY,
    INITIAL_CAPITAL,
    REBALANCE_DATES,
    SLIPPAGE_BASIS_POINTS,
    SLIPPAGE_MODEL,
    SMALL_CAPITAL,
    STRESS_COMMISSION_BASIS_POINTS,
    STRESS_SLIPPAGE_BASIS_POINTS,
    STRESS_SLIPPAGE_MODEL,
    SUB_PERIODS,
    FLAT_SLIPPAGE_BASIS_POINTS,
    FLAT_SLIPPAGE_MODEL,
    FLAT_SUFFIX,
    UNVALUED_DAYS_AT_END_ALLOWED,
    VALUED_SHARE_REQUIRED,
    WINDOW_END,
    WINDOW_START,
    WORKERS,
    backtest_engine,
    books,
    file_names,
    pandas,
    securities_panel,
    window_days,
):
    def task(
        portfolio_name: str,
        start: "pandas.Timestamp",
        end: "pandas.Timestamp",
        commission_basis_points: float = COMMISSION_BASIS_POINTS,
        slippage_model: str = SLIPPAGE_MODEL,
        slippage_basis_points: float = SLIPPAGE_BASIS_POINTS,
        initial_capital: int = INITIAL_CAPITAL,
    ) -> dict:
        """One engine run's settings."""
        return {
            "experiment_directory": str(EXPERIMENT_DIRECTORY),
            "portfolio_name": portfolio_name,
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
            "initial_capital": initial_capital,
            "commission_basis_points": commission_basis_points,
            "slippage_model": slippage_model,
            "slippage_basis_points": slippage_basis_points,
            "cash_reserve_percentage": CASH_RESERVE,
        }

    def from_start(
        weights: "pandas.DataFrame",
        start: "pandas.Timestamp",
        end: "pandas.Timestamp",
    ) -> "pandas.DataFrame":
        """The book from a sub-period's first rebalance date to its end, on its own dates."""
        inside = REBALANCE_DATES[(REBALANCE_DATES >= start) & (REBALANCE_DATES <= end)]

        return weights.loc[inside]

    first_day = REBALANCE_DATES[0]
    tasks = [
        task(file_names[_label], first_day, WINDOW_END)
        for _label in books
    ]
    runs_by_label = {
        _label: file_names[_label]
        for _label in books
    }

    # Every book again at the flat half-spread: the same weights under another name, so the engine's
    # cache keeps the two pricings apart.
    for _label in books:
        _flat_name = f"{file_names[_label]}_flat"
        backtest_engine.write_weight_file(
            securities_panel.expand_to_identifiers(books[_label]),
            EXPERIMENT_DIRECTORY,
            _flat_name,
        )
        tasks.append(task(
            _flat_name,
            first_day,
            WINDOW_END,
            slippage_model=FLAT_SLIPPAGE_MODEL,
            slippage_basis_points=FLAT_SLIPPAGE_BASIS_POINTS,
        ))
        runs_by_label[f"{_label}{FLAT_SUFFIX}"] = _flat_name

    for _label in ("rule", "control"):
        _stress_name = f"{file_names[_label]}_stress"
        _small_name = f"{file_names[_label]}_small_account"

        for _name in (_stress_name, _small_name):
            backtest_engine.write_weight_file(
                securities_panel.expand_to_identifiers(books[_label]),
                EXPERIMENT_DIRECTORY,
                _name,
            )

        tasks.append(task(
            _stress_name,
            first_day,
            WINDOW_END,
            STRESS_COMMISSION_BASIS_POINTS,
            STRESS_SLIPPAGE_MODEL,
            STRESS_SLIPPAGE_BASIS_POINTS,
        ))
        runs_by_label[f"{_label}, stress costs"] = _stress_name
        tasks.append(task(
            _small_name,
            first_day,
            WINDOW_END,
            initial_capital=SMALL_CAPITAL,
        ))
        runs_by_label[f"{_label}, $100,000"] = _small_name

        for _period, _start, _end in SUB_PERIODS:
            _period_name = f"{file_names[_label]}_{_period.replace(' ', '_')}"
            _period_book = from_start(books[_label], _start, _end)
            backtest_engine.write_weight_file(
                securities_panel.expand_to_identifiers(_period_book),
                EXPERIMENT_DIRECTORY,
                _period_name,
            )
            tasks.append(task(_period_name, _period_book.index[0], _end))
            runs_by_label[f"{_label}, {_period}"] = _period_name
            _flat_period_name = f"{_period_name}_flat"
            backtest_engine.write_weight_file(
                securities_panel.expand_to_identifiers(_period_book),
                EXPERIMENT_DIRECTORY,
                _flat_period_name,
            )
            tasks.append(task(
                _flat_period_name,
                _period_book.index[0],
                _end,
                slippage_model=FLAT_SLIPPAGE_MODEL,
                slippage_basis_points=FLAT_SLIPPAGE_BASIS_POINTS,
            ))
            runs_by_label[f"{_label}, {_period}{FLAT_SUFFIX}"] = _flat_period_name

    priced_runs = backtest_engine.price_books(tasks, WORKERS)
    all_runs = {
        _label: priced_runs[_name]
        for _label, _name in runs_by_label.items()
    }
    _tasks_by_name = {
        _settings["portfolio_name"]: _settings
        for _settings in tasks
    }
    # A run the engine stopped valuing early -- a cash error at a rebalance whose costs outran the
    # reserve -- is excluded by name with its reason, and no cell below reads it.
    excluded_runs = {}

    for _label, _run in all_runs.items():
        if not _run["success"]:
            excluded_runs[_label] = f"the engine refused it: {str(_run['error'])[:200]}"

            continue

        _settings = _tasks_by_name[runs_by_label[_label]]
        _run_days = window_days[
            (window_days >= pandas.Timestamp(_settings["start"]))
            & (window_days <= pandas.Timestamp(_settings["end"]))
        ]
        _valued_days = pandas.DatetimeIndex(_run["register"].index)
        _valued_share = len(_run_days.intersection(_valued_days)) / len(_run_days)
        _unvalued_at_end = len(_run_days[_run_days > _valued_days.max()])

        if _valued_share < VALUED_SHARE_REQUIRED or _unvalued_at_end > UNVALUED_DAYS_AT_END_ALLOWED:
            excluded_runs[_label] = (
                f"truncated: valued {_valued_share:.1%} of its trading days, to "
                f"{_valued_days.max().date()}"
            )

    runs = {
        _label: _run
        for _label, _run in all_runs.items()
        if _label not in excluded_runs
    }
    print(f"engine runs: {len(all_runs)}, read: {len(runs)}, excluded by name: {len(excluded_runs)}")

    for _label, _reason in excluded_runs.items():
        print(f"  {_label}: {_reason}")

    pandas.Series(excluded_runs, name="reason").to_csv(
        EXPERIMENT_DIRECTORY / "Backtest" / "excluded_runs.csv"
    )
    return all_runs, excluded_runs, runs, runs_by_label, tasks


@app.cell
def _(EXPERIMENT_DIRECTORY, SUB_PERIODS, pandas, runs):
    # Every figure below comes from the engine. There is no second simulator in this repository.
    STATISTICS = {
        "CAGR": "Annualized Return (CAGR)",
        "volatility": "Annualized Volatility",
        "Sharpe": "Portfolio Sharpe Ratio",
        "Sortino": "Portfolio Sortino Ratio",
        "max drawdown": "Max Drawdown",
    }
    rows = {}

    for _label, _run in runs.items():
        if not _run["success"]:
            continue

        _statistics = _run["portfolio_stats"]
        rows[_label] = {
            name: _statistics.get(key)
            for name, key in STATISTICS.items()
        }
        rows[_label]["alpha vs the index"] = _statistics.get("Alpha")
        rows[_label]["information ratio"] = _statistics.get("Information Ratio")
        rows[_label]["commissions"] = _statistics.get("Total Commissions")
        rows[_label]["slippage"] = _statistics.get("Total Slippage Costs")
        rows[_label]["financing"] = _statistics.get("Total Financing Costs")
        rows[_label]["risk-free rate"] = _run.get("risk_free_rate")
        rows[_label]["window"] = _run["window"]

    summary = pandas.DataFrame(rows).T
    benchmark_rows = {}
    _benchmark_labels = ("rule",) + tuple(
        f"rule, {_period}"
        for _period, _, _ in SUB_PERIODS
    )

    for _label in _benchmark_labels:
        if _label not in runs:
            continue

        for _identifier, _statistics in runs[_label]["benchmarks_stats"].items():
            benchmark_rows[f"{_identifier}, as priced beside {_label}"] = {
                name: _statistics.get(key)
                for name, key in STATISTICS.items()
            }

    benchmarks = pandas.DataFrame(benchmark_rows).T
    headline = [
        _label
        for _label in (
            "rule",
            "control",
            "equal weight",
            "rule, flat 5 bp",
            "control, flat 5 bp",
            "equal weight, flat 5 bp",
            "rule, stress costs",
            "control, stress costs",
            "rule, $100,000",
            "control, $100,000",
        )
        if _label in summary.index
    ]
    print(summary.loc[headline, list(STATISTICS)].astype(float).round(4).to_string())
    print()
    print(benchmarks.astype(float).round(4).to_string())
    print()
    print(summary.loc[headline, ["alpha vs the index", "information ratio", "commissions", "slippage", "financing", "risk-free rate", "window"]].to_string())
    EXPERIMENT_DIRECTORY.joinpath("Backtest").mkdir(exist_ok=True)
    summary.to_csv(EXPERIMENT_DIRECTORY / "Backtest" / "summary.csv")
    benchmarks.to_csv(EXPERIMENT_DIRECTORY / "Backtest" / "benchmarks.csv")
    return STATISTICS, summary


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tradeability, from the engine's own orders

    What a person following the book at a broker would do: the orders the engine placed on each
    rebalance date, their size in dollars, and the one-way turnover from the engine's daily weights —
    the weight each name held the day before a rebalance against the day after. The small account is
    where order sizes and integer shares matter.
    """)
    return


@app.cell
def _(EXPERIMENT_DIRECTORY, FILL_COLUMN, cut, numpy, pandas, runs):
    def tradeability(label: str) -> dict:
        """Orders, their sizes and the turnover of one engine run, from its own tables."""
        run = runs[label]
        orders = run["orders"].copy()
        orders.index = pandas.to_datetime(orders.index)
        shares = orders.select_dtypes("number")
        prices = cut[FILL_COLUMN].reindex(index=shares.index, columns=shares.columns)
        notional = (shares.abs() * prices).where(shares.abs() > 0)
        orders_per_date = notional.notna().sum(axis=1)
        daily = run["daily_weights"].copy()
        daily.index = pandas.to_datetime(daily.index)
        holdings = daily.drop(columns=["CASH_RESERVE"], errors="ignore").fillna(0.0)
        change = holdings.diff().abs().sum(axis=1) / 2
        traded_days = change.reindex(shares.index).fillna(0.0)
        years = (holdings.index.max() - holdings.index.min()).days / 365.25

        return {
            "rebalance dates with orders": int((orders_per_date > 0).sum()),
            "orders a year": round(float(orders_per_date.sum() / years), 1),
            "orders per date, median": float(orders_per_date[orders_per_date > 0].median()),
            "orders under $1,000": int((notional < 1000).sum().sum()),
            "orders under $100, the band's residue": int((notional < 100).sum().sum()),
            "median order, dollars": round(float(numpy.nanmedian(notional.to_numpy())), 0),
            "one-way turnover a year": round(float(traded_days.sum() / years), 2),
        }

    tradeability_rows = {
        _label: tradeability(_label)
        for _label in (
            "rule",
            "control",
            "rule, flat 5 bp",
            "control, flat 5 bp",
            "rule, $100,000",
            "control, $100,000",
        )
        if _label in runs
    }
    tradeability_table = pandas.DataFrame(tradeability_rows).T
    print(tradeability_table.to_string())
    tradeability_table.to_csv(EXPERIMENT_DIRECTORY / "Backtest" / "tradeability.csv")
    return (tradeability_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The book in pictures

    The flat 5 bp row, the one the gate is read at: the value of US$1 million in the rule, its
    control, the KN US Equity Core and `SPY`, on a log scale; each one's drawdown from its peak; and
    each calendar year's return. Every line is the engine's own daily value, as its batch returned
    it for the run, so nothing here is simulated a second time.
    """)
    return


@app.cell
def _(
    FLAT_SUFFIX,
    SUB_PERIODS,
    mo,
    pandas,
    runs,
):
    import matplotlib.pyplot
    import matplotlib.ticker

    def engine_values(label: str) -> "pandas.DataFrame":
        """The daily values the engine returned for one run: the book's and every benchmark's."""
        answer = runs[label]
        register = answer["register"]
        values = pandas.DataFrame({
            "Total_Portfolio_Value": register["Total_Portfolio_Value"].astype(float),
        })
        values.index = pandas.to_datetime(register.index)

        for _identifier, _table in answer["benchmark_values"].items():
            _dated = _table.set_index(pandas.to_datetime(_table["date_column"]))
            values[f"{_identifier}_Value"] = _dated["bench_value"].astype(float)

        return values

    def calendar_returns(values: "pandas.Series") -> "pandas.Series":
        """Each calendar year's return, from the last value of the year before, or the first."""
        year_ends = values.groupby(values.index.year).last()
        year_starts = year_ends.shift(1).fillna(values.iloc[0])

        return year_ends / year_starts - 1

    _rule_values = engine_values(f"rule{FLAT_SUFFIX}")
    _control_values = engine_values(f"control{FLAT_SUFFIX}")
    book_values = pandas.DataFrame({
        "rule": _rule_values["Total_Portfolio_Value"],
        "control": _control_values["Total_Portfolio_Value"],
        "KN US Equity Core": _rule_values["KN_US_Equity_Core_Value"],
        "SPY": _rule_values["SPY_Value"],
    })
    _colours = {
        "rule": "#e84328",
        "control": "#56534e",
        "KN US Equity Core": "#121110",
        "SPY": "#a9a59c",
    }
    _figure, _axes = matplotlib.pyplot.subplots(
        3,
        1,
        figsize=(11, 13),
    )

    for _name, _series in book_values.items():
        _axes[0].plot(
            _series.index,
            _series,
            color=_colours[_name],
            label=_name,
            linewidth=1.4,
        )
        _drawdown = _series / _series.cummax() - 1
        _axes[1].plot(
            _drawdown.index,
            _drawdown,
            color=_colours[_name],
            label=_name,
            linewidth=1.0,
        )

    for _period, _start, _end in SUB_PERIODS:
        _axes[0].axvline(
            _start,
            color="#e4e1da",
            linewidth=1.0,
        )

    _axes[0].set_yscale("log")
    _axes[0].set_title("Value of US$1 million, flat 5 bp, net of every cost")
    _axes[0].legend()
    _axes[1].set_title("Drawdown from the peak")
    _axes[1].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    _years = pandas.DataFrame({
        _name: calendar_returns(book_values[_name])
        for _name in ("rule", "KN US Equity Core")
    })
    _positions = range(len(_years))
    _axes[2].bar(
        [
            _position - 0.2
            for _position in _positions
        ],
        _years["rule"],
        width=0.4,
        color=_colours["rule"],
        label="rule",
    )
    _axes[2].bar(
        [
            _position + 0.2
            for _position in _positions
        ],
        _years["KN US Equity Core"],
        width=0.4,
        color=_colours["KN US Equity Core"],
        label="KN US Equity Core",
    )
    _axes[2].set_xticks(
        list(_positions),
        [
            str(_year)
            for _year in _years.index
        ],
        rotation=90,
    )
    _axes[2].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    _axes[2].axhline(
        0.0,
        color="#121110",
        linewidth=0.8,
    )
    _axes[2].set_title("Calendar-year return")
    _axes[2].legend()
    _figure.tight_layout()
    mo.as_html(_figure)
    return book_values, matplotlib


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Attribution — KaxaNuk Attribution Analysis

    **In plain words:** which part of the return did you actually earn?

    - **Brinson-Fachler**, the first cut: active return into **allocation** — being overweight the
      right groups — **selection** inside them, and their **interaction**.
    - **A factor model**, the second layer: excess return into **compensated factor tilts** and
      **idiosyncratic** alpha, what was earned on purpose rather than by accident.
    - **Brinson-Fachler again, on the residual**, the third pass: whether the selection survives once
      the factors are taken out.

    **What it settles and what it does not** is in [`../../AGENTS.md`](../../AGENTS.md).

    **The book arrives daily**, as the engine held it, from `Backtest/` — never the weight file,
    which holds only the rebalance dates. **Every weight is held overnight**, so the close of t−1
    earns day t. **The first cut's benchmark is reconciled** against the index's own returns file
    before any figure is read, and section 8 raises unless the two come within a point a year. **The
    attribution window** is bound by the supplied files, usually shorter than the backtest's: record
    both in `FINDINGS_1.md`.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Brinson–Fachler**, the first cut; **the KN US Equity Factor Model**, the second layer — its
    Experiment 1, momentum skipping the latest month, **unreviewed by its owner and provisional**;
    and **Brinson–Fachler on the residual**, the third pass. The book arrives daily, as the engine
    held it, both weight tables held overnight. The first cut's benchmark is reconciled against the
    Core's own returns file before any figure is read.
    """)
    return


@app.cell
def _(
    ATTRIBUTION_WORKERS,
    EXCLUDED,
    EXPERIMENT_DIRECTORY,
    FLAT_SUFFIX,
    RANDOM_SEEDS,
    attribution_analysis,
    backtest_engine,
    hand_supplied,
    membership,
    pandas,
    runs,
    window_days,
):
    missing = attribution_analysis.report_missing_inputs()
    ATTRIBUTION_READY = len(missing) == 0 and "rule" in runs

    if not ATTRIBUTION_READY:
        print("step 6 skipped:", "; ".join(missing))
    else:
        market_factor = pandas.read_csv(hand_supplied.factor_directory() / "Market.csv", usecols=[0])
        factor_dates = pandas.DatetimeIndex(pandas.to_datetime(market_factor.iloc[:, 0]))
        rule_days = pandas.DatetimeIndex(runs["rule"]["daily_weights"].index)
        window = window_days[
            (window_days >= max(factor_dates.min(), rule_days.min()))
            & (window_days <= factor_dates.max())
        ]
        members_ever = membership.loc[window].columns[membership.loc[window].any(axis=0)]
        print(f"backtest window:    {rule_days.min().date()} to {rule_days.max().date()}")
        print(f"attribution window: {window.min().date()} to {window.max().date()}")

    def attribution_task(label: str, layers: tuple[str, ...]) -> dict:
        """One book's inputs for the library: widened to the index, every name priced, no nulls."""
        daily_weights = runs[label]["daily_weights"].reindex(window).fillna(0.0)
        book = attribution_analysis.widen_to_benchmark(
            daily_weights,
            index_weights,
            backtest_engine.BENCHMARK_IDENTIFIERS,
        ).drop(columns=list(EXCLUDED), errors="ignore")
        benchmark = index_weights.reindex(columns=book.columns).fillna(0.0)
        book_overnight = attribution_analysis.held_overnight(book)
        benchmark_overnight = attribution_analysis.held_overnight(benchmark)

        return {
            "name": label,
            "book": book_overnight,
            "benchmark": benchmark_overnight,
            "asset_returns": all_returns.reindex(
                index=book_overnight.index,
                columns=book_overnight.columns,
            ).fillna(0.0),
            "layers": layers,
            "cache_directory": str(EXPERIMENT_DIRECTORY / "Attribution" / "cache"),
        }

    if ATTRIBUTION_READY:
        _labels = ["rule", "control", "equal weight"] + [
            f"random {_seed:02d}"
            for _seed in RANDOM_SEEDS
        ]
        attributed_labels = [
            _label
            for _label in _labels + [f"{_name}{FLAT_SUFFIX}" for _name in _labels]
            if _label in runs
        ]
        names_held = set(members_ever)

        for _label in attributed_labels:
            names_held = names_held | set(runs[_label]["daily_weights"].columns)

        all_prices = attribution_analysis.load_prices(tuple(sorted(names_held)), window)
        all_returns = attribution_analysis.load_asset_returns(all_prices)
        priced_index = attribution_analysis.load_benchmark_weights(window, all_prices).drop(
            columns=list(EXCLUDED),
            errors="ignore",
        )
        index_weights = priced_index.div(priced_index.sum(axis=1), axis=0).fillna(0.0)
        FULL = (
            "brinson",
            "factor",
            "residual",
        )
        attribution_tasks = [
            attribution_task(_label, FULL if not _label.startswith("random") else ("factor",))
            for _label in attributed_labels
        ]
        coverage = attribution_analysis.benchmark_coverage(window, all_prices)
        print("share of the whole index the first cut can price, by year:")
        print(coverage.groupby(coverage.index.year).mean().round(4).to_string())
        attributed = attribution_analysis.attribute_books(attribution_tasks, ATTRIBUTION_WORKERS)
        errors = {
            _name: _answer["error"]
            for _name, _answer in attributed.items()
            if "error" in _answer
        }
        print(f"books attributed: {len(attributed)}, failed: {len(errors)} {errors}")
    else:
        attributed = {}
        window = window_days
    return ATTRIBUTION_READY, attributed, attribution_task, window


@app.cell
def _(ATTRIBUTION_READY, attributed, hand_supplied, window):
    # First cut: Brinson-Fachler, per asset, as the library computes it. Then the reconciliation the
    # blueprint makes a precondition: the first cut's benchmark against the Core's own returns file.
    brinson_totals = None
    reconciliation_gap = None

    if ATTRIBUTION_READY and "brinson_totals" in attributed.get("rule", {}):
        rule_answer = attributed["rule"]
        brinson_totals = rule_answer["brinson_totals"]
        print("Brinson-Fachler on the rule, summed over the window, in points:")
        print(brinson_totals.round(2).to_string())
        brinson_daily = rule_answer["brinson_daily"]
        benchmark_columns = [
            column
            for column in brinson_daily.columns
            if "bench" in column.lower() and "return" in column.lower()
        ]
        index_returns = hand_supplied.read_benchmark_returns().reindex(window[1:])

        if len(benchmark_columns) > 0:
            first_cut_annual = float(brinson_daily[benchmark_columns[0]].mean() * 252 * 100)
            index_annual = float(index_returns.mean() * 252 * 100)
            reconciliation_gap = abs(first_cut_annual - index_annual)
            print(f"first cut's benchmark, mean daily return a year: {first_cut_annual:.2f} points")
            print(f"the KN US Equity Core's own, same window:       {index_annual:.2f} points")
            print(f"gap: {reconciliation_gap:.2f} points a year (tolerance 1.0)")
        else:
            print("the library returned no benchmark return column: the reconciliation cannot be read")
    return brinson_totals, reconciliation_gap


@app.cell
def _(ATTRIBUTION_READY, EXPERIMENT_DIRECTORY, attributed, pandas):
    # Second layer: the factor model, on every book this experiment attributes.
    decomposition = pandas.DataFrame()

    if ATTRIBUTION_READY:
        decomposition = pandas.DataFrame({
            _name: _answer["factor_totals"]
            for _name, _answer in attributed.items()
            if "factor_totals" in _answer
        })
        reserved = [
            "f_total_excess_returns",
            "f_total_factor_returns",
            "f_idyo_returns",
        ]
        priced_factors = [
            _name
            for _name in decomposition.index
            if _name not in reserved
        ]
        print("factor model on the rule, the control and equal weight, in points:")
        print(decomposition.loc[priced_factors, ["rule", "control", "equal weight"]]
              .round(2).sort_values("rule", ascending=False).to_string())
        print()
        print(decomposition.loc[[_name for _name in reserved if _name in decomposition.index]]
              .round(2).T.to_string())
        decomposition.to_csv(EXPERIMENT_DIRECTORY / "Attribution" / "factor_model.csv")
    return (decomposition,)


@app.cell
def _(ATTRIBUTION_READY, EXPERIMENT_DIRECTORY, attributed, pandas):
    # Third pass: Brinson-Fachler on the residual, on the books attributed in full.
    residual_table = pandas.DataFrame()

    if ATTRIBUTION_READY:
        residual_table = pandas.DataFrame({
            _name: _answer["residual_totals"]
            for _name, _answer in attributed.items()
            if "residual_totals" in _answer
        })
        print("Brinson-Fachler on the residual, in points:")
        print(residual_table.round(2).to_string())
        print()
        print("share of each book the factor model covers:", {
            _name: round(_answer["covered_share"], 3)
            for _name, _answer in attributed.items()
            if "covered_share" in _answer
        })
        brinson_table = pandas.DataFrame({
            _name: _answer["brinson_totals"]
            for _name, _answer in attributed.items()
            if "brinson_totals" in _answer
        })
        brinson_table.to_csv(EXPERIMENT_DIRECTORY / "Attribution" / "brinson_fachler.csv")
        residual_table.to_csv(EXPERIMENT_DIRECTORY / "Attribution" / "brinson_fachler_residual.csv")
    return (residual_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Attribution in pictures

    At the flat 5 bp row. Left, the second layer: the rule's excess return over the risk-free rate,
    split into the market, each style, each KN sector and the idiosyncratic part no factor explains.
    Right, that idiosyncratic part beside its control, equal weight and every random book the engine
    priced whole: alpha is its *expected* value, so it is read as alpha only where it stands clear of
    the random books. Below, the first cut against the Core, and the same cut on the residual.
    """)
    return


@app.cell
def _(
    ATTRIBUTION_READY,
    FLAT_SUFFIX,
    brinson_totals,
    decomposition,
    matplotlib,
    mo,
    residual_table,
):
    mo.stop(
        not ATTRIBUTION_READY or decomposition.empty,
        mo.md("Step 6 was skipped in section 5: there is no attribution to draw."),
    )
    _book = f"rule{FLAT_SUFFIX}" if f"rule{FLAT_SUFFIX}" in decomposition.columns else "rule"
    _totals = [
        "f_total_excess_returns",
        "f_total_factor_returns",
    ]
    _sources = decomposition[_book].drop(index=_totals, errors="ignore").dropna()
    _parts = _sources.rename(index={
        "f_market": "market",
        "f_idyo_returns": "idiosyncratic",
    }).sort_values()
    _figure, _axes = matplotlib.pyplot.subplot_mosaic(
        [
            ["factors", "random"],
            ["brinson", "brinson"],
        ],
        figsize=(13, 11),
        height_ratios=[3, 1.2],
    )
    _axes["factors"].barh(
        _parts.index,
        _parts,
        color=[
            "#e84328" if _name == "idiosyncratic" else "#3a3833"
            for _name in _parts.index
        ],
    )
    _axes["factors"].axvline(
        0.0,
        color="#121110",
        linewidth=0.8,
    )
    _axes["factors"].set_title(
        f"Excess return {decomposition.loc['f_total_excess_returns', _book]:.1f} points, by source"
    )
    _idiosyncratic = decomposition.loc["f_idyo_returns"]
    _random = _idiosyncratic[[
        _name
        for _name in _idiosyncratic.index
        if _name.startswith("random") and _name.endswith(FLAT_SUFFIX)
    ]].dropna()
    _axes["random"].scatter(
        _random,
        [0] * len(_random),
        s=120,
        color="#c9c6be",
        edgecolor="#56534e",
        label=f"{len(_random)} random books",
    )

    for _offset, (_name, _colour) in enumerate((
        (_book, "#e84328"),
        (f"control{FLAT_SUFFIX}", "#56534e"),
        (f"equal weight{FLAT_SUFFIX}", "#121110"),
    )):
        if _name in _idiosyncratic.index:
            _axes["random"].scatter(
                [_idiosyncratic[_name]],
                [0.25 + 0.25 * _offset],
                s=220,
                color=_colour,
                label=_name,
            )

    _axes["random"].axvline(
        0.0,
        color="#121110",
        linestyle="--",
        linewidth=0.8,
    )
    _axes["random"].set_yticks([])
    _axes["random"].set_ylim(-0.5, 1.5)
    _axes["random"].set_title("Idiosyncratic return, points: the rule against chance")
    _axes["random"].legend(loc="upper left", fontsize=8)
    _brinson = {}

    if brinson_totals is not None:
        _brinson.update({
            f"first cut: {_name}": float(_value)
            for _name, _value in brinson_totals.items()
        })

    if "rule" in residual_table.columns:
        _brinson.update({
            f"residual: {_name}": float(_value)
            for _name, _value in residual_table["rule"].items()
        })

    _axes["brinson"].bar(
        list(_brinson),
        list(_brinson.values()),
        color=[
            "#e84328" if "selection" in _name else "#3a3833"
            for _name in _brinson
        ],
    )
    _axes["brinson"].axhline(
        0.0,
        color="#121110",
        linewidth=0.8,
    )
    _axes["brinson"].tick_params(axis="x", rotation=30)
    _axes["brinson"].set_title("Brinson-Fachler against the Core, and on the residual, points (the rule, engine's spread row)")
    _figure.tight_layout()
    mo.as_html(_figure)
    return


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Counterfactuals — the sweep, and who earned the idiosyncratic share

    The factor model leaves part of the book's excess return unexplained. That is a number, not an
    answer. **Each counterfactual removes exactly one of the book's choices and keeps the rest** —
    the control, the same names equally weighted, random books at the same sizes — and the engine
    prices them all. **The sweep is read as a curve**, each setting against its own control on the
    rule's dates, never as a search for its best cell. Beside every margin over the control: the
    share of months the book beat it, and how much of the two books' weight overlapped, because two
    books holding the same names do not make independent observations.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sweep is read as a curve, each setting against its own control. The band at two other widths
    is read on turnover and orders, never on the gate. Beside the rule's margin over its control:
    the share of months the book beat it, and how much of the two books' weight overlapped, because
    two books holding the same names do not make independent observations.
    """)
    return


@app.cell
def _(
    ATTRIBUTION_READY,
    BAND_SWEEP,
    EXPERIMENT_DIRECTORY,
    FLAT_SUFFIX,
    RANDOM_SEEDS,
    STATISTICS,
    SWEEP,
    backtest_engine,
    books,
    decomposition,
    numpy,
    pandas,
    runs,
):
    def statistic(label: str, name: str) -> float:
        """One engine figure for one run, or nothing for a run excluded by name."""
        if label not in runs:

            return numpy.nan

        return float(runs[label]["portfolio_stats"][STATISTICS[name]])

    def index_sharpe(label: str) -> float:
        """The Core's Sharpe ratio as the engine priced it beside one run."""
        if label not in runs:

            return numpy.nan

        return float(
            runs[label]["benchmarks_stats"][backtest_engine.INDEX_IDENTIFIER][STATISTICS["Sharpe"]]
        )

    def sweep_table(suffix: str) -> "pandas.DataFrame":
        """Each setting against its own control, under one pricing; an excluded run reads empty."""
        rows = {}

        for setting, _ in SWEEP:
            book_label = f"sweep, {setting}{suffix}"
            control_label = f"sweep, {setting}, control{suffix}"
            rows[setting] = {
                "Sharpe": statistic(book_label, "Sharpe"),
                "control Sharpe": statistic(control_label, "Sharpe"),
                "CAGR": statistic(book_label, "CAGR"),
                "control CAGR": statistic(control_label, "CAGR"),
                "index Sharpe": index_sharpe(book_label),
            }

        table = pandas.DataFrame(rows).T
        table["Sharpe margin"] = table["Sharpe"] - table["control Sharpe"]
        table["CAGR margin"] = table["CAGR"] - table["control CAGR"]
        table["priced"] = table[["Sharpe", "control Sharpe"]].notna().all(axis=1)
        table["keeps the sign on both"] = (table["Sharpe margin"] > 0) & (table["CAGR margin"] > 0)
        table["beats the index on Sharpe"] = table["Sharpe"] > table["index Sharpe"]

        return table

    sweeps = {
        "pre-registered": sweep_table(""),
        "flat 5 bp": sweep_table(FLAT_SUFFIX),
    }

    for _pricing, _table in sweeps.items():
        print(f"the sweep, {_pricing}:")
        print(_table.round(4).to_string())
        print()
        _table.to_csv(EXPERIMENT_DIRECTORY / "Backtest" / f"sweep_{_pricing.replace(' ', '_')}.csv")

    band_rows = {}

    for _setting, _ in (("rule", None),) + BAND_SWEEP:
        for _suffix in ("", FLAT_SUFFIX):
            _label = f"{_setting}{_suffix}"

            if _label not in runs:
                continue

            _orders = runs[_label]["orders"].select_dtypes("number")
            _years = len(runs[_label]["daily_weights"]) / 252
            band_rows[_label] = {
                "orders a year": round(float((_orders.abs() > 0).sum().sum() / _years), 1),
                "Sharpe": statistic(_label, "Sharpe"),
                "CAGR": statistic(_label, "CAGR"),
            }

    print("the band, read on orders:")
    print(pandas.DataFrame(band_rows).T.round(4).to_string())

    def months_beaten(rule_label: str, control_label: str) -> float:
        """The share of months the rule's value grew more than its control's."""
        if rule_label not in runs or control_label not in runs:

            return numpy.nan

        register = runs[rule_label]["register"]
        value_columns = [
            column
            for column in register.columns
            if "value" in column.lower()
        ]

        if len(value_columns) == 0:

            return numpy.nan

        rule_value = runs[rule_label]["register"][value_columns[0]]
        control_value = runs[control_label]["register"][value_columns[0]]
        rule_value.index = pandas.to_datetime(rule_value.index)
        control_value.index = pandas.to_datetime(control_value.index)
        rule_monthly = rule_value.resample("ME").last().pct_change().dropna()
        control_monthly = control_value.resample("ME").last().pct_change().dropna()

        return float((rule_monthly > control_monthly.reindex(rule_monthly.index)).mean())

    months = {
        "pre-registered": months_beaten("rule", "control"),
        "flat 5 bp": months_beaten(f"rule{FLAT_SUFFIX}", f"control{FLAT_SUFFIX}"),
    }
    overlap = float(
        numpy.minimum(books["rule"], books["control"].reindex_like(books["rule"]).fillna(0.0))
        .sum(axis=1).mean()
    )
    print(f"\nshare of months the rule beat its control: {months}")
    print(f"weight the rule and its control share, mean over rebalance dates: {overlap:.3f}")
    random_rows = {}

    for _seed in RANDOM_SEEDS:
        _label = f"random {_seed:02d}"
        random_rows[_label] = {
            "Sharpe": statistic(_label, "Sharpe"),
            "CAGR": statistic(_label, "CAGR"),
            "Sharpe, flat 5 bp": statistic(f"{_label}{FLAT_SUFFIX}", "Sharpe"),
            "CAGR, flat 5 bp": statistic(f"{_label}{FLAT_SUFFIX}", "CAGR"),
        }

    random_table = pandas.DataFrame(random_rows).T

    if ATTRIBUTION_READY:
        random_table["idiosyncratic"] = [
            float(decomposition.loc["f_idyo_returns", _label])
            if _label in decomposition.columns
            else numpy.nan
            for _label in random_table.index
        ]
        random_table["idiosyncratic, flat 5 bp"] = [
            float(decomposition.loc["f_idyo_returns", f"{_label}{FLAT_SUFFIX}"])
            if f"{_label}{FLAT_SUFFIX}" in decomposition.columns
            else numpy.nan
            for _label in random_table.index
        ]

    print()
    print(random_table.round(4).to_string())
    return months, overlap, random_table, statistic, sweeps


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Verdict

    **In words.** A notebook that ends in a number and no sentence gets read as whatever the reader
    hoped. The record is [`FINDINGS_1.md`](FINDINGS_1.md); **this notebook is the method.**

    The cell below reads the gate of `Paper_Trading/BITACORA.md` from the numbers above, row by row,
    at every pricing the blueprint or the owner named. **Soundness first** — no survivorship bias,
    no look-ahead, no overfitting, costs and capacity stated, reproducible — then **performance** —
    beats the benchmarks and its control over the whole window, idiosyncratic alpha in both layers,
    conclusions that survive perturbation. A row that needs an excluded run reads "not evidenced".
    The outcome — graduates, sound and regime-dependent, or not sound — and the sign-off are a
    person's, never this cell's.

    Then the handoff, what each output feeds, and the open items to carry forward. If sections 4 and
    5 reported "not installed", this notebook has produced a book and no result, which is the honest
    outcome and not a failure.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In words**, in [`FINDINGS_1.md`](FINDINGS_1.md) — **that file is the record, this notebook is
    the method.** The cell below reads the gate's criteria 1 to 4 and the predictions from the
    numbers above, row by row, **once for each pricing**: the pre-registered costs, which the
    blueprint fixed, and the flat 5 bp half-spread, the blueprint's own fallback, priced after the
    engine's range-based spread was found to read a megacap's daily range as spread. Which of the two
    the gate is read at is the owner's decision, recorded in the journal. A criterion that needs a
    run excluded by name reads "not evidenced". Criterion 5 is a person's signature, never this
    cell's.

    ## Handoff

    | Output | Consumed by |
    | --- | --- |
    | `Portfolio/portfolio_weights.csv` | the backtest engine |
    | `Backtest/` — summaries, the sweeps, tradeability, the gates, the excluded runs | `FINDINGS_1.md` |
    | `Attribution/` | `FINDINGS_1.md` |

    ## Open items to carry forward

    | # | Item | Why it matters |
    | --- | --- | --- |
    | 1 | **The open keeps Sharadar's rounding.** | 0.23 bp of the Core at most; noise in the fills, not a bias |
    | 2 | **A delisted name is sold at its last trade**, often over the counter. | A hand-traded account may not reach that venue |
    | 3 | **The factor model is provisional.** | Its owner's review is pending |
    | 4 | **The spread model.** | The engine's range-based estimates read volatility as spread on the most traded names; a quoted-spread source would settle the cost row |
    """)
    return


@app.cell
def _(
    ATTRIBUTION_READY,
    EXPERIMENT_DIRECTORY,
    FLAT_SUFFIX,
    STATISTICS,
    SUB_PERIODS,
    attributed,
    decomposition,
    numpy,
    pandas,
    random_table,
    reconciliation_gap,
    residual_table,
    runs,
    statistic,
    sweeps,
):
    def read_gate(suffix: str, pricing: str) -> dict:
        """The gate's criteria 1 to 4 and the three predictions under one pricing."""
        rule_label = f"rule{suffix}"
        control_label = f"control{suffix}"
        rule_sharpe = statistic(rule_label, "Sharpe")
        rule_cagr = statistic(rule_label, "CAGR")
        control_sharpe = statistic(control_label, "Sharpe")
        control_cagr = statistic(control_label, "CAGR")
        benchmark_sharpes = {
            identifier: float(statistics[STATISTICS["Sharpe"]])
            for identifier, statistics in runs[rule_label]["benchmarks_stats"].items()
        }
        period_rows = {}

        for period, _, _ in SUB_PERIODS:
            period_rows[period] = {
                "rule Sharpe": statistic(f"rule, {period}{suffix}", "Sharpe"),
                "control Sharpe": statistic(f"control, {period}{suffix}", "Sharpe"),
                "rule CAGR": statistic(f"rule, {period}{suffix}", "CAGR"),
                "control CAGR": statistic(f"control, {period}{suffix}", "CAGR"),
            }

        periods = pandas.DataFrame(period_rows).T
        periods["beats the control on both"] = (
            (periods["rule Sharpe"] > periods["control Sharpe"])
            & (periods["rule CAGR"] > periods["control CAGR"])
        )
        margins_met = rule_sharpe - control_sharpe >= 0.03 and rule_cagr - control_cagr >= 0.005
        periods_met = int(periods["beats the control on both"].sum()) >= 2
        benchmarks_met = all(
            rule_sharpe > sharpe
            for sharpe in benchmark_sharpes.values()
        )
        sweep = sweeps[pricing]
        sweep_priced = bool(sweep["priced"].all())
        criterion_3 = (
            int(sweep["keeps the sign on both"].sum()) >= 6
            and bool(sweep["beats the index on Sharpe"].all())
        ) if sweep_priced else "not evidenced"
        criterion_2 = "not evidenced"
        random_beaten = 0
        rule_idiosyncratic = numpy.nan

        random_column = "idiosyncratic" if suffix == "" else f"idiosyncratic{suffix}"
        random_attributed = 0

        if ATTRIBUTION_READY and rule_label in decomposition.columns:
            rule_idiosyncratic = float(decomposition.loc["f_idyo_returns", rule_label])
            random_beaten = int((random_table[random_column] < rule_idiosyncratic).sum())
            random_attributed = int(random_table[random_column].notna().sum())
            residual_selection = (
                float(residual_table.loc["selection", rule_label])
                if "selection" in residual_table.index and rule_label in residual_table.columns
                else numpy.nan
            )
            brinson_selection = (
                float(attributed[rule_label]["brinson_totals"].get("selection", numpy.nan))
                if "brinson_totals" in attributed.get(rule_label, {})
                else numpy.nan
            )
            reconciled = reconciliation_gap is not None and reconciliation_gap <= 1.0
            criterion_2 = (
                reconciled
                and brinson_selection > 0
                and rule_idiosyncratic > 0
                and residual_selection > 0
                and random_beaten >= 16
            ) if random_attributed == 20 else "not evidenced"

        gate = pandas.DataFrame([
            {
                "pricing": pricing,
                "criterion": "1, beats the benchmarks and its control",
                "passes": margins_met and periods_met and benchmarks_met,
                "evidence": (
                    f"Sharpe {rule_sharpe:.3f} against {benchmark_sharpes} and the control's "
                    f"{control_sharpe:.3f}; CAGR margin {(rule_cagr - control_cagr) * 100:+.2f} "
                    f"points; sub-periods beaten on both: "
                    f"{int(periods['beats the control on both'].sum())} of 3"
                ),
            },
            {
                "pricing": pricing,
                "criterion": "2, idiosyncratic alpha in both layers",
                "passes": criterion_2,
                "evidence": (
                    f"reconciliation gap {reconciliation_gap}; idiosyncratic {rule_idiosyncratic:.2f}; "
                    f"random books beaten {random_beaten} of {random_attributed} attributed"
                ),
            },
            {
                "pricing": pricing,
                "criterion": "3, survives perturbation",
                "passes": criterion_3,
                "evidence": (
                    f"{int(sweep['keeps the sign on both'].sum())} of {int(sweep['priced'].sum())} "
                    f"priced keep the sign on both; {int(sweep['beats the index on Sharpe'].sum())} "
                    f"beat the index"
                ),
            },
            {
                "pricing": pricing,
                "criterion": "4, costs and capacity stated",
                "passes": True,
                "evidence": "the cost rows, tradeability and the participation bound above",
            },
        ])
        predictions = pandas.Series({
            "1, the cross earns its keep": margins_met and periods_met,
            "2, a drawdown control": (
                statistic(rule_label, "max drawdown") > statistic(control_label, "max drawdown")
                and statistic(rule_label, "volatility") < statistic(control_label, "volatility")
            ),
            "3, traded value does not beat equal weight": (
                statistic(f"equal weight{suffix}", "Sharpe") >= rule_sharpe - 0.03
            ),
        }, name=pricing)

        return {
            "gate": gate,
            "periods": periods,
            "predictions": predictions,
        }

    readings = {
        "pre-registered": read_gate("", "pre-registered"),
        "flat 5 bp": read_gate(FLAT_SUFFIX, "flat 5 bp"),
    }

    for _pricing, _reading in readings.items():
        print(f"== {_pricing}")
        print(_reading["periods"].round(4).to_string())
        print(_reading["gate"].to_string(index=False))
        print(_reading["predictions"].to_string())
        print()

    pandas.concat([_reading["gate"] for _reading in readings.values()]).to_csv(
        EXPERIMENT_DIRECTORY / "Backtest" / "gate.csv",
        index=False,
    )
    pandas.concat({
        _pricing: _reading["periods"]
        for _pricing, _reading in readings.items()
    }).to_csv(EXPERIMENT_DIRECTORY / "Backtest" / "sub_periods.csv")
    return (readings,)


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8 · Verify

    **Assertions that raise when this experiment's output is wrong.** Section 2.1 prints its
    invariants; this section raises on them, and on what the notebook wrote, so a run that reaches
    the last cell is one whose book and numbers hold. At the least:

    - every invariant of section 2.1 holds, and the window and the exclusions are the blueprint's;
    - **no name a blocking row of `Universe/Data_Issues.csv` lists is held by any book** — the rule,
      the control or any arm;
    - every weight file, read back, has one column per rebalance date, none summing to more than one
      and no weight negative;
    - **every engine run is read whole or excluded by name, with its reason**: counted against the
      trading days of its own window — never against a fixed floor, which a run that stopped years
      early can clear — it is read, or it is excluded and written to `Backtest/excluded_runs.csv`.
      This raises only if a run is neither read nor excluded, or if a book the verdict stands on —
      the rule, its control, the arms the blueprint names — is excluded. Skipped, as section 4 is,
      when the engine is not installed;
    - **the first cut's benchmark is the index**: its return, the mean day times 252, within a point
      a year of the index's own returns file over the same days. Wider, and the weights were paired
      with a return they already held, members went unpriced or the book was not widened, and no
      attribution figure stands until it closes;
    - the attribution window lies inside the backtest's, and every arm has an idiosyncratic figure.
      Both are skipped, as section 5 is, when attribution did not run.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Assertions that raise when this experiment's output is wrong**: every invariant of section
    2.1; the window and the exclusions the blueprint's; every weight file read back with one column
    per rebalance date, none over one, none negative; **no name a blocking register row lists held by
    any book**; every engine run valued the trading days of the window it was asked for; and, when
    attribution ran, its window inside the backtest's, every arm with an idiosyncratic figure, and
    **the first cut's benchmark within a point a year of the Core's own returns file**.
    """)
    return


@app.cell
def _(
    ATTRIBUTION_READY,
    EXCLUDED,
    EXPECTED_EXCLUSIONS,
    EXPERIMENT_DIRECTORY,
    FLAT_SUFFIX,
    REBALANCE_DATES,
    WINDOW_START,
    all_runs,
    books,
    decomposition,
    excluded_runs,
    file_names,
    invariants,
    pandas,
    reconciliation_gap,
    runs,
    window,
    window_days,
    window_written,
):
    verifications = {
        f"invariant: {_name}": _passed
        for _name, _passed in invariants.items()
    }
    verifications["the window is the universe notebook's"] = (
        window_written["window_start"].iloc[0] == WINDOW_START.date().isoformat()
    )
    verifications["the exclusions are the blueprint's"] = EXCLUDED == EXPECTED_EXCLUSIONS

    for _label, _weights in books.items():
        _held = _weights.columns[(_weights > 0).any(axis=0)]
        verifications[f"{_label}: no blocking name is ever held"] = len(set(_held) & set(EXCLUDED)) == 0

    _weight_file = pandas.read_csv(
        EXPERIMENT_DIRECTORY / "Portfolio" / f"{file_names['rule']}.csv",
        index_col=0,
    )
    verifications["the weight file has one column per rebalance date"] = (
        _weight_file.shape[1] == len(REBALANCE_DATES)
    )
    verifications["no weight-file column sums to more than one"] = bool(
        (_weight_file.sum(axis=0) <= 1.0 + 1e-6).all()
    )
    verifications["no weight in the file is negative"] = bool((_weight_file >= 0).all().all())

    # Every run is read whole or excluded by name with its reason; the books the verdict stands on
    # are never among the excluded.
    verifications["every run is read or excluded by name, with its reason"] = (
        set(runs) | set(excluded_runs) == set(all_runs)
        and all(len(_reason) > 0 for _reason in excluded_runs.values())
    )
    _written = pandas.read_csv(EXPERIMENT_DIRECTORY / "Backtest" / "excluded_runs.csv", index_col=0)
    verifications["the excluded runs are written to Backtest/excluded_runs.csv"] = (
        set(_written.index) == set(excluded_runs)
    )

    for _label in ("rule", "control", "equal weight", f"rule{FLAT_SUFFIX}", f"control{FLAT_SUFFIX}"):
        verifications[f"{_label}: valued whole, never excluded"] = _label in runs

    if ATTRIBUTION_READY:
        verifications["the attribution window lies inside the backtest's"] = bool(
            window.min() >= window_days.min() and window.max() <= window_days.max()
        )
        verifications["every attributed arm has an idiosyncratic figure"] = bool(
            decomposition.loc["f_idyo_returns"].notna().all()
        )
        verifications["the first cut's benchmark reconciles within a point a year"] = (
            reconciliation_gap is not None and reconciliation_gap <= 1.0
        )

    _failed = [
        _name
        for _name, _passed in verifications.items()
        if not _passed
    ]

    if len(_failed) > 0:
        _message = f"the experiment failed verification: {'; '.join(_failed)}"

        raise AssertionError(_message)

    print(f"verified: {len(verifications)} checks; {len(runs)} engine runs read, "
          f"{len(excluded_runs)} excluded by name")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9 · Dashboards — to look, not to report

    Two buttons, one server each: the engine's dashboard for the rule on port 8052, and the
    attribution library's for the rule against the KN US Equity Core on port 8050. Nothing here is a
    number the experiment reports: those come from sections 4 and 5.
    """)
    return


@app.cell
def _(mo):
    backtest_button = mo.ui.run_button(label="Open the backtest dashboard (port 8052)")
    attribution_button = mo.ui.run_button(label="Open the attribution dashboard (port 8050)")
    mo.hstack([backtest_button, attribution_button], justify="start")
    return attribution_button, backtest_button


@app.cell
def _(
    CASH_RESERVE,
    COMMISSION_BASIS_POINTS,
    EXPERIMENT_DIRECTORY,
    INITIAL_CAPITAL,
    REBALANCE_DATES,
    SLIPPAGE_BASIS_POINTS,
    SLIPPAGE_MODEL,
    WINDOW_END,
    backtest_button,
    backtest_engine,
    file_names,
    mo,
):
    import threading

    mo.stop(not backtest_button.value)
    backtest_configuration = backtest_engine.build_configuration(
        EXPERIMENT_DIRECTORY,
        REBALANCE_DATES[0].date(),
        WINDOW_END.date(),
        INITIAL_CAPITAL,
        COMMISSION_BASIS_POINTS,
        SLIPPAGE_MODEL,
        SLIPPAGE_BASIS_POINTS,
        CASH_RESERVE,
        portfolio_name=file_names["rule"],
    )
    threading.Thread(
        target=backtest_engine.open_dashboard,
        args=(EXPERIMENT_DIRECTORY, backtest_configuration, 8052),
        daemon=True,
    ).start()
    mo.md("Pricing the rule; the backtest dashboard opens at <http://127.0.0.1:8052> in a minute.")
    return (threading,)


@app.cell
def _(
    ATTRIBUTION_READY,
    attribution_analysis,
    attribution_button,
    attribution_task,
    mo,
    threading,
):
    mo.stop(not attribution_button.value)
    mo.stop(
        not ATTRIBUTION_READY,
        mo.md("Step 6 was skipped in section 5: there is no attribution to show."),
    )
    threading.Thread(
        target=attribution_analysis.open_dashboard,
        args=(attribution_task("rule", ("brinson", "factor")), 8050),
        daemon=True,
    ).start()
    mo.md("Reading the factor files; the attribution dashboard opens at <http://127.0.0.1:8050>.")
    return


# --- example: end ---


if __name__ == "__main__":
    app.run()
