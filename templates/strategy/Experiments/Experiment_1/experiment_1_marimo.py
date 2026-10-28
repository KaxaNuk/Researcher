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


if __name__ == "__main__":
    app.run()
