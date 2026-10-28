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
    # Data — analyzer

    **Block 3 of 3 in the Data stage, step 3 of 8.** The other two blocks *produce* data; this notebook
    is where it is *understood*, and where a feature either earns a backtest or is dropped before
    anybody spends a week on it.

    **In plain words:** build features and test whether they carry signal, before you model anything.

    **It produces** the charts and the information-coefficient table in `Data/Analyzer/`.

    **It prevents** a book built on a feature that never predicted anything.

    > **Runs after `Data/refinery.py`, and before any experiment** — the predictions an experiment's
    > blueprint makes are supposed to come from here.

    ```
    Data/curator.py    + Data/Curator/custom_calculations.py    ->  Curator/Time_Series/   m_* + c_*
    Data/refinery.py   + Data/Refinery/custom_calculations.py   ->  Refinery/Time_Series/  + r_*
    Data/analyzer_marimo.py                                     ->  Analyzer/  charts + the IC table
    ```

    `Universe/universe_marimo.py` profiles the *catalogue* — what exists, what is missing, when each
    security becomes usable. This notebook looks at the **content**: what the data says, and whether
    the signal built on it carries anything.

    **A marimo notebook, run as a script:** `uv run python Data/analyzer_marimo.py`, or cell by cell
    with `uv run marimo edit Data/analyzer_marimo.py`. Its outputs are never saved in the file.

    **In the template this notebook holds no code:** each section below says what is expected in it.
    Write the cells.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Setup

    Read the refined panel, and name **the columns this notebook reads, once, in this cell** — the
    eligibility column, the features it eats, the cross-sectional candidates to screen. Everything
    below re-runs unchanged when they change. Read the window the universe notebook fixed from the
    file it wrote, never retyped.

    | Column family | Built by | Scope |
    | --- | --- | --- |
    | `m_*` | the provider, via the Curator | raw market data |
    | `c_*` | `Curator/custom_calculations.py` | **per security** — one security's own history |
    | `r_*` | `Refinery/custom_calculations.py` | **cross-sectional**, or with a setting an experiment sweeps |
    | `current_*` | joined from the security master | today's classification, **not point-in-time** |

    **A new feature on the data already downloaded is an `r_*` column**, added to
    `Data/Refinery/custom_calculations.py` and read here once the refinery has run: never a widening
    of the Curator's columns and a second download.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · What each stage contributed

    The refined file is the Curator file plus columns, on its rows inside the span the seed gives the
    security, or all of them where it gives none. Confirming that here is what lets every section
    below read one folder and forget the Curator exists.

    Then **coverage**, per column. A column at 60% coverage is not quietly averaged over the 60%: say
    so, and decide whether the gap is a warm-up, a late listing or a broken input.

    Where the Curator rebuilt a provider's adjustment, measure here what the provider's prices are and
    what the rebuild changed, before any experiment: how coarse the provider's rounding is, where the
    rebuild departs from the provider's own series, and what the fill price keeps of the rounding.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · What diversification is actually available

    A strategy that chooses between securities is a bet that they do not all move together. Whether
    that is true is measurable, and it decides how much the strategy can possibly add: **if everything
    is one trade, choosing between them is theatre.**

    Buy-and-hold return, volatility and worst day per security; the correlation matrix; the mean
    off-diagonal correlation and the extreme pairs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Are the cross-sectional columns what they claim to be?

    The Refinery asserts one property that would be silent if broken: **every rank is a percentile
    taken inside a single date.** A rank computed over the pooled sample would drift as the universe's
    composition changed, and nothing would raise an error.

    Check it as an identity, not as a rule of thumb. A per-date percentile over *n* untied values has
    mean exactly `(n + 1) / (2n)` — 0.542 on twelve securities, 0.5006 on eight hundred. Testing
    against 0.5 looks like a small failure on every date of a narrow universe and passes on a wide one,
    which is the worst possible failure mode.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Information coefficient — which features predict returns

    **The section that decides things.** For each feature and horizon, the information coefficient is
    the cross-sectional rank correlation between the feature on date *t* and the forward return from
    *t* to *t+h*, computed **per date** and then averaged. Per date is what keeps it causal: the
    correlation only ever compares securities observable at the same moment.

    - **IC** — the mean daily correlation. The sign matters as much as the size: a negative IC means
      the feature works *inverted*.
    - **IR** = IC / IC standard deviation — the consistency of the edge, which is what survives into a
      portfolio.
    - **The share of dates with the expected sign**, beside the IR, and the overlap stated. A forward
      window of *h* days, measured every day, shares *h − 1* days with the next, so the dates are not
      independent observations and an IR counted over them overstates the evidence.

    Compute it over the whole panel and, separately, over the **eligible pool** the strategy actually
    selects from. The second is the one that matters: a feature can behave differently inside an
    already-filtered group.

    > **The IC table is a screening tool, not evidence.** An information ratio scales with the square
    > root of the number of independent bets, so on a narrow universe read these as directional. **A
    > feature that fails here does not get a book built on it**; one that passes has earned a backtest,
    > not a belief.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · The two questions any signal owes an answer to

    Sections 0 to 4 are what any strategy needs. What belongs beside them depends on your signal, and
    two are worth writing whatever it is.

    **Does the signal separate anything?** Split forward return *and* forward volatility by the
    signal's state. A signal can be worth trading on the second alone; it would not be the first.

    **If the signal is fitted, what is look-ahead worth?** Read the same model causally and smoothed
    and report the gap. It is the cheapest audit in the process and routinely the largest number in it:
    the two series agree on most days and differ exactly at the turning points, which is where the
    money is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Handoff

    | Output | Consumed by |
    | --- | --- |
    | `Data/Refinery/Time_Series/` | **`Experiments/` — read this one** |
    | `Data/Analyzer/` — the IC table | feature selection in every experiment |
    | `Data/Analyzer/Charts/` | `FINDINGS_N.md` |

    ## What to write in the blueprint before running an experiment

    **Write down what you expect before you run this.** A prediction made from the data and then
    confirmed by the engine is the strongest methodological result an experiment can report; a number
    found first and explained afterwards is a story.

    Put the predictions this notebook licenses in `BLUEPRINT_N.md` **before** the backtest, each with
    the section it came from and the observation that would falsify it. **Findings from this stage go
    straight into `RESULTS.md`**, under *Before any experiment* — a marimo notebook saves no output in
    its file, so a measurement living only in a cell's output does not survive the run.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Verify

    **Assertions that raise when this stage's output is wrong**, read back from what this notebook
    wrote to `Data/Analyzer/` rather than from the variables that wrote it. A notebook that reaches its
    last cell is then one whose tables can be quoted. At the least:

    - the coefficient table has a row for every feature, pool and horizon, each with a finite
      coefficient, ratio and share of dates with the expected sign;
    - no coefficient is averaged over no dates, nor over more dates than the panel has a forward
      return for at its horizon;
    - the pool the strategy selects from never counts more dates than the whole panel at the same
      horizon, because it is a part of it.
    """)
    return


if __name__ == "__main__":
    app.run()
