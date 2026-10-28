# Results

> **Executive summary of everything this repository has measured.**
>
> Experiment sections are compiled from the `FINDINGS_N.md` files and cite each one. **When a number
> changes, change it in `FINDINGS_N.md` first**, then here, as `AGENTS.md` says. The one exception
> is step 3, `Data/analyzer_marimo.py`: its findings go straight into *Before any experiment*
> below, because a notebook saves no output.
>
> Every performance figure comes from the **KaxaNuk Backtest Engine**, the only backtest here.
>
> Until the first experiment reports, every table below except *Known limitations* is empty: the
> shape is fixed, and the numbers come from the pipeline.

## The project in three sentences

Does Experiment 1's book beat its benchmark and its control, with its headline numbers. What
attribution says about where the return comes from. Which lever earned its place after Experiment 1,
and which was rejected.

---

## Before any experiment: what the data already says

Findings from step 3, `Data/analyzer_marimo.py`: whether a candidate feature carries information,
over what horizon and with which sign, and anything else measured about the signal that needs no
book. Cite the section each number came from.

**State the horizon and the overlap**, item 11 of the bar in `AGENTS.md`: a coefficient over *h*
days, measured every day, shares *h − 1* days with the next one. Beside any coefficient or ratio,
report the share of dates on which it had the sign the hypothesis expects.

| # | Measurement | Value | Dates with the expected sign | Section |
| --- | --- | ---: | ---: | --- |
| 1 | what was measured, over which horizon, on which pool | the number | for a coefficient or a ratio, the share of dates with the sign the hypothesis expects | the analyzer section |

---

## The experiments

Each experiment ranks its variants over **one window shared by all of them**; windows can differ
between experiments.

> **Compare a winner's Sharpe with its own experiment's control**, never with another experiment's
> headline. Across experiments, compare the `vs control` column.

**Each row names the claim it moved**: the claim of `OBJECTIVE.md` its blueprint set out to move,
and the status it reached. A row that beats its benchmarks and moves no claim is a number, not a
finding. **Its status is the gate's outcome**, as `Paper_Trading/BITACORA.md` reads it: graduates,
sound and regime-dependent with its periods named, or not sound with the soundness row that failed.

| Exp | Book | CAGR | Sharpe | Max DD | Control Sharpe | vs control | Status | Claim moved | Findings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| **1** | the first rule, in five words | | | | — | — | the gate's outcome | the claim's number, and its new status | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |

### Against the world

The same book measured against every benchmark it reports against, over one stated window.

**Does it reproduce?** Re-run from a wiped working copy and state the drift. A Sharpe moving in the
third decimal is the re-pull's rebasing, limitation 5 below, not a strategy change.

### The trial count

**How many variants were ranked in each experiment, plus any excluded run**, published as item 3 of
the bar in `AGENTS.md` asks.

---

## What stands — reuse, do not rebuild

A result, a module or a method later work should start from rather than re-derive. One line each,
with its number.

## What is closed — do not re-propose without a new argument

Each rejected idea, with the number that rejected it. This list is what stops the next person
repeating it.

### The uncomfortable one

The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.

## Open leads, ranked

The single highest-value run outstanding, and what it would settle. Then the next.

## Excluded runs

Variants removed from the tables above, each by name with its reason, rather than reported with a
caveat. **A metric computed over a truncated or rejected run does not belong in the same column as
a complete one.**

| Variant | Why |
| --- | --- |
| | what went wrong, how it was caught, and what now prevents it |

## Known limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing is out of sample** until a frozen book has days on paper after its freeze | Every number here is in-sample, and in-sample selection is what the deflation literature warns about |
| 2 | **A control arm differing in exactly one thing**, item 9 of the bar in `AGENTS.md`, is missing from any experiment that claims a margin | Which lever earned that margin is inferred from per-lever rows, not measured |
| 3 | Classification buckets use today's labels, not point-in-time | Anything reclassified mid-window is misattributed before its move — the `current_*` prefix marks exactly this |
| 4 | Delisting exits use one day of hindsight | A position is sold on the last day it still has a fill price, knowable only the day after |
| 5 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 6 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**
