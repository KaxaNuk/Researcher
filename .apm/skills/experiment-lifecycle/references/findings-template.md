# Findings — Experiment N

> **Latest valuable results only.** This file is rewritten when a result changes, not appended to —
> the running history is in [`JOURNAL_N.md`](JOURNAL_N.md), and the hypothesis this tested is in
> [`BLUEPRINT_N.md`](BLUEPRINT_N.md).
>
> **[`../../RESULTS.md`](../../RESULTS.md) is compiled from this file.** When a finding here
> changes, change it here first, then update the summary.

## Status

**Until the first run, *Not yet run*.** After it: one line saying whether the rule beat the
benchmark and its control by what the blueprint required, and which outcome of the gate below it
reads as — a success is necessary for graduation, not sufficient. Then **the claim it moved**: the
claim of `OBJECTIVE.md` the blueprint named, and the status it reached — or why it reached none.

## The gate

**Two layers, read in order, each row with its evidence: a row without evidence does not hold.**
The gate is `Paper_Trading/BITACORA.md`'s; this section reads it for this experiment, at each
pricing the blueprint or the owner named, and says which pricing the reading stands on.

**Soundness — is the experiment done correctly?**

| # | Soundness criterion | Evidenced by | Holds? | The evidence here |
| --- | --- | --- | --- | --- |
| S1 | **No survivorship bias** | the point-in-time universe: departed names kept in the seed, the security master, the usable date | holds, or does not | the figure, file or section that shows it |
| S2 | **No look-ahead** | signals lagged, next-open fills, the blueprint's rule and predictions registered before any result | | |
| S3 | **No overfitting** | the trial count published, the sweep read as a curve, the control and the random books priced | | |
| S4 | **Costs and capacity stated** | turnover, commission, slippage, cash, and every assumption the engine does not model | | |
| S5 | **Reproducible** | the pipeline ran from a working copy whose data folders were emptied first, every Verify passing | | |

**Performance — does it earn its place?**

| # | Performance criterion | Holds? | The evidence here |
| --- | --- | --- | --- |
| P1 | Beats the benchmarks and its control on risk-adjusted return, over the whole window | | |
| P2 | Attribution shows idiosyncratic alpha in both layers | | |
| P3 | Conclusions survive parameter perturbation | | |

A criterion that needs a run excluded by name reads *not evidenced*, which is not *holds*.

**The outcome, one of three:**

- **Graduates** — every soundness and performance criterion holds, and the owner signs it off in
  `BITACORA.md`: the book is frozen and paper traded.
- **Sound and regime-dependent** — every soundness criterion holds; performance fails over the
  whole window but holds in named periods. Name the periods where it earned and where it failed,
  against its control and its benchmarks, and the condition that tells them apart as far as the
  evidence goes. It is not paper traded alone. It may be paired with another signal in a later
  experiment, or used at a portfolio manager's discretion — the decision, and its risk, are
  theirs. Never a recommendation.
- **Not sound** — a soundness criterion fails: no conclusion is drawn; fix it and run again.

The sign-off stays a person's name and date. The assistant never decides a gate: it reads each row
from its evidence and says which outcome the rows describe.

## The predictions, evaluated

**Every prediction in the blueprint gets a row, including the ones that were wrong.** A falsified
prediction is worth more than a correct one: it says something about the strategy that nobody knew,
and it cost one run to find out.

| # | Prediction | Outcome | What it changed |
| --- | --- | --- | --- |
| 1 | as written in the blueprint | confirmed or falsified, with the number | what is now understood differently |

## The book, priced by the engine

Record the date of the last full re-run from a wiped working copy, the engine version, and the
window. Then the book against every benchmark it reports against, and against the control its
blueprint names, on the rule's own rebalance dates: CAGR, volatility, Sharpe, Sortino, maximum
drawdown — at every cost row the blueprint names, with the commission, the slippage and the cash
interest the engine charged and paid, and every sub-period, each priced from its first rebalance
date. Name the runs excluded by name, and the cash rate Sharpe ratios are measured in excess of.

## What the book is, structurally — and can a person trade it?

Rebalance frequency, orders and turnover, holdings, concentration, invested share, and any
structural tilt — each with a reading of what a bad value would have meant, and whether a person
could follow the book by hand at a broker.

## The trial count

How many variants were ranked to reach the book above, and every run excluded by name with its
reason, as `Backtest/excluded_runs.csv` lists them. `RESULTS.md` compiles this: a reader cannot
discount a best-of-N result without knowing N, and soundness criterion S3 says whether the deflated
figure was also computed.

## Attribution — is this the signal, or a factor exposure wearing its name?

Brinson-Fachler: allocation, selection, interaction. The factor model: factor against idiosyncratic.
State the window, which is bound by the supplied files' coverage and is usually shorter than the
backtest.

**What it settles**, and **what it does not** — naming the counterfactual book that would settle
what is left: the same holdings with the signal off, positions equalised, a random draw at the same
sizes, entry dates shifted.

## What is open, ranked

The single highest-value run outstanding, and what it would settle.

## Caveats

| # | Caveat | Effect |
| --- | --- | --- |
| 1 | what a reader must know before quoting a number above | what it does to that number |
