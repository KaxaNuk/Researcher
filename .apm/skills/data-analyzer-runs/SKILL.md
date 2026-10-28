---
name: data-analyzer-runs
description: >
  Load this skill whenever the Analyzer block of a KaxaNuk Strategy Template repository is
  written, run, read or debugged — `Data/analyzer_marimo.py`, the last block of step 3, where a
  feature earns a backtest or is dropped before any book is built. Use it when the user asks
  whether a feature carries signal, how to compute an information coefficient or information
  ratio, over which horizons, on which pool, how to check coverage, diversification or a
  cross-sectional rank, what a fitted signal's look-ahead costs, what to write in `RESULTS.md`
  under *Before any experiment*, where a new experiment's signal is computed, or which predictions
  the analyzer allows a blueprint to make. It covers the
  notebook's sections, the traps that make a clean screen wrong, and where the numbers go. It does
  NOT cover the `c_*` and `r_*` columns it reads (`data-curator-custom-calculations`), the
  security master (`universe-point-in-time`), sizing (`portfolio-construction-runs`), the engine
  (`backtest-engine-runs`), or the documents around the stage (`experiment-lifecycle`).
metadata:
  version: 0.3.0
---

# The Data Analyzer — where a feature earns a backtest or is dropped

**In plain words:** build features and test whether they carry signal, before you model anything.
**It produces** the charts and the information-coefficient table in `Data/Analyzer/`, and the
measurements that go into `RESULTS.md` under *Before any experiment*. **It prevents** a book built
on a feature that never predicted anything.

The Analyzer is the third block of step 3: one of the two Lab modules still hand-rolled, and the
only one in a notebook, until its library lands. It runs **after `Data/refinery.py` and before any
experiment**: the predictions an experiment's blueprint makes are supposed to come from here. The
notebook is a marimo notebook, run as a script — `uv run python Data/analyzer_marimo.py`, or cell by
cell with `uv run marimo edit Data/analyzer_marimo.py` — which saves no output in its file.

```
Data/curator.py    + Data/Curator/custom_calculations.py    ->  Curator/Time_Series/   m_* + c_*
Data/refinery.py   + Data/Refinery/custom_calculations.py   ->  Refinery/Time_Series/  + r_*
Data/analyzer_marimo.py                                     ->  Analyzer/  charts + the IC table
```

`Universe/universe_marimo.py` profiles the *catalogue* — what exists, what is missing, when each
security becomes usable. The analyzer looks at the **content**: what the data says, and whether the
signal built on it carries anything. It builds no book, runs no engine and sizes nothing.

## When to Use

- The user asks whether a feature predicts returns, over what horizon and with which sign; how to
  compute an information coefficient; whether to screen on the whole panel or the eligible pool.
- The user is writing or debugging `Data/analyzer_marimo.py`, or asks what a section of it is for.
- A blueprint needs a prediction and nothing supports it yet: the analyzer measurement that would
  is the lead to run first.
- The user asks what goes into `RESULTS.md` before any experiment, or where an analyzer number is
  cited from.

## The notebook, section by section

The template ships `Data/analyzer_marimo.py` as its markdown cells — each section says what is
expected in it — and the worked example, `examples/strategy/golden-flow/` in the KaxaNuk Researcher
package, fills every one. Read the example's copy before writing a cell; `init-example` puts it in a
folder of its own. Sections 0 to 4 are what any strategy needs; 5 depends on the signal; 7, Verify,
ends every one. A strategy made from a template before 0.20.0 has a Jupyter notebook,
`Data/analyzer.ipynb`: the marimo one comes back through `init-strategy`'s script, run from the
strategy's root, `scaffold.py strategy . --only Data/analyzer_marimo.py`, and the old cells are
moved into it by hand, then the old file deleted.

| Section | Measures | The trap it catches |
| --- | --- | --- |
| 0 · Setup | the refined panel, and **the columns this notebook reads, named once in this cell** — eligibility, the features, the candidates to screen — and the window, read from the file the universe notebook wrote | a column named in three cells is three places to change; a window retyped is one that drifts from the universe's |
| 1 · What each stage contributed | the refined file is the curator file plus columns, its rows inside each security's span; then **coverage per column**; where the Curator rebuilt a provider's adjustment, what the provider's rounding is and what the rebuild changed — the example's section 1.1 | a column at 60% coverage quietly averaged over the 60%; say whether the gap is a warm-up, a late listing or a broken input; a provider's rounding read as the market |
| 2 · What diversification is available | buy-and-hold return, volatility and worst day per security; the correlation matrix, its mean off-diagonal and the extreme pairs | **if everything is one trade, choosing between securities is theatre** — this is the measurement that says how much a selection rule can possibly add |
| 3 · Are the cross-sectional columns what they claim | that every rank is a percentile **inside a single date**, checked as an identity: a per-date percentile over *n* untied values has mean exactly `(n + 1) / (2n)` | a rank pooled across dates drifts as the universe changes and raises no error; testing against 0.5 fails on every date of a narrow universe and passes on a wide one |
| 4 · Information coefficient | for each feature and horizon, the cross-sectional **rank** correlation between the feature at *t* and the forward return *t* to *t+h*, **per date, then averaged**; the IC, and the IR as IC over its standard deviation; beside it the share of dates with the expected sign, and the overlap, *h − 1* days, that consecutive windows share; on the whole panel and, separately, on the **eligible pool** the rule selects from | a correlation pooled over dates compares securities that were never observable together; a feature that behaves on the panel and not inside the filtered pool; an IR over overlapping windows read as if every date were an independent observation |
| 5 · The two questions any signal owes an answer to | **does the signal separate anything** — forward return *and* forward volatility split by the state the rule reads; **if the signal is fitted, what look-ahead is worth** — the same model read causally and smoothed, and the gap | a signal worth trading on volatility alone mistaken for a return signal; a fitted signal whose in-sample fit is the whole edge |
| 6 · Handoff | what each output feeds: the refined panel to `Experiments/`, the IC table to feature selection, the charts to `FINDINGS_N.md` | a measurement living only in a cell output |
| 7 · Verify | reads back `Data/Analyzer/information_coefficient.csv` and **raises**: a row for every pool and horizon; a finite coefficient, ratio and share of dates with the expected sign on each, the share between 0 and 1; every row averaged over at least one date and over no more dates than have a forward return at its horizon; the eligible pool never counting more dates than the whole panel | a notebook that stopped partway still looks executed; a check that prints *PASS* is one somebody has to read |

## Rules

1. **Per date, never pooled.** Every cross-sectional statistic — a rank, a correlation, a
   percentile — is taken inside one date and then averaged. That is what keeps it causal.
2. **A gap stays a gap.** `pct_change(fill_method=None)`: padding a halt turns the first price
   after it into one enormous return that then dominates every statistic.
3. **Screen on the pool the rule selects from.** Compute on the whole panel for context and on
   the eligible pool for the decision; the second is the one that matters.
4. **The IC table is a screening tool, not evidence.** An information ratio scales with the square
   root of the number of independent bets, so on a narrow universe read it as directional. A
   feature that fails here does not get a book built on it; one that passes has earned a backtest,
   not a belief. Orders of magnitude, from the example's measurement of 2026-10-23, over
   2000-01-03 to 2026-08-14: on the pool its rule selects from, the fifty most traded members, the
   golden cross as a state reads an IC of +0.0127 at 21 days (IR 0.058), with the expected sign on
   52.7% of dates, and +0.0259, −0.0027 and +0.0150 in the window's three thirds. The traded-value
   rank, on the same pool, reads +0.0130 at 252 days over the window, −0.0504 in 2000–2008 and
   +0.0825 in 2018–2026; across every member it reads −0.0391, with the expected sign on 38.0% of
   dates. A third of the window can say the opposite of the whole.
5. **Never choose a parameter on the metric it will be judged by.** A window, a threshold or a
   lookback is chosen on a property of the signal — persistence, coverage, turnover — and the
   sweep is published as a curve, never as its best cell. That rule is the bar's sixth point in
   the strategy's `AGENTS.md`.
6. **If the signal is fitted, measure what look-ahead costs before anything else.** The causal and
   the smoothed series agree on most days and differ exactly at the turning points, which is where
   the money is. It is the cheapest audit in the process and routinely the largest number in it.
7. **No book is built here, and no performance number is quoted.** A forward return split by
   signal state is a measurement of the data; a Sharpe is the Backtest Engine's, later.
8. **Write down what you expect before running it.** A prediction made from the data and then
   confirmed by the engine is the strongest result an experiment can report; a number found first
   and explained afterwards is a story.
9. **A new feature on the data already downloaded is an `r_*` column.** When a new experiment can
   use what the Curator wrote, its signals are computed in the Data Refinery, as `r_*` columns in
   `Data/Refinery/custom_calculations.py`, and screened here once the refinery has run — never by
   widening the Curator's columns and downloading again.

## Where the numbers go

- **`RESULTS.md`, *Before any experiment*** — every measurement worth keeping, in a table with the
  section it came from: what the signal predicts, over what horizon, with which sign, and what it
  does not; what the findings allow a blueprint to predict and what they forbid. It also records
  the caveats the data carries — a security with no file, a bad print excluded by name, series that
  end early.
  Findings from this stage go there **directly**, the one exception to *findings first*: a marimo
  notebook saves no output in its file, so a measurement living only in a cell's output does not
  survive the run.
- **`BLUEPRINT_N.md`** — each prediction's *where it comes from* is *analyzer section Y*, by
  number, or a `Bibliotheca/` note. A prediction with neither is a lead: *run analyzer section Y
  before predicting this.* The `blueprint` command of the KaxaNuk Researcher probes `RESULTS.md`
  for these, not `Data/Analyzer/`, which git ignores.
- **`Data/Analyzer/`** — the IC table as `information_coefficient.csv` and the charts, gitignored,
  regenerated by the notebook.

## What this stage does not settle

Whether the feature earns money in a book, net of costs, inside position and turnover limits — that
is steps 4 to 6. Whether the return it earns is the feature's or a factor exposure wearing its name
— that is attribution, read with `alpha-decomposition`. And how many features were screened to find
the one that passed: count them, and publish the count beside the winner.

## References

- `Data/analyzer_marimo.py` in the worked example, `examples/strategy/golden-flow/` in the KaxaNuk
  Researcher package — every section filled, with the strategy's own cells between
  `# --- example: begin ---` and `# --- example: end ---`. The template's copy is the same notebook
  without them.
- `RESULTS.md` in the same example, *Before any experiment* — what a filled table looks like.
- The strategy's `AGENTS.md`, *The bar any new signal must clear* and *Research integrity — the
  five ways a backtest lies*, which this stage serves.
