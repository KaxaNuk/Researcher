# Findings — Experiment 1

> **Latest valuable results only.** This file is rewritten when a result changes, not appended to —
> the running history is in [`JOURNAL_1.md`](JOURNAL_1.md), and the hypothesis this tested is in
> [`BLUEPRINT_1.md`](BLUEPRINT_1.md).
>
> **[`../../RESULTS.md`](../../RESULTS.md) is compiled from this file.** When a finding here
> changes, change it here first, then update the summary.

<!-- example: begin -->

> The current answer, rewritten whenever the result changes. The hypothesis is
> [`BLUEPRINT_1.md`](BLUEPRINT_1.md); how it was reached is [`JOURNAL_1.md`](JOURNAL_1.md). Every
> figure below comes from the KaxaNuk Backtest Engine or KaxaNuk Attribution Analysis, through
> `experiment_1_marimo.py`, run on 2026-10-24 on Backtest Engine 0.67.0 and Attribution Analysis
> 0.5.0; nothing is computed here.

---

<!-- example: end -->

## Status

**Until the first run, *Not yet run*.** After it: one line saying whether the rule beat the
benchmark and its control by what the blueprint required, and which outcome of the gate below it
reads as — a success is necessary for graduation, not sufficient. Then **the claim it moved**: the
claim of `OBJECTIVE.md` the blueprint named, and the status it reached — or why it reached none.

<!-- example: begin -->

**Experiment 1, rewritten on Sharadar from 2000 with a monthly rule, ran end to end on 2026-10-24
and does not graduate.** The golden cross earns its keep against its control — the falsifier does
not fire — but the book **loses to the KN US Equity Core and to `SPY` on Sharpe over 2000–2026**,
under both cost rows, and so does every setting of the sweep: gate criteria 1 and 3 fail.
Criterion 2 is not evidenced, because the random books the gate needs were truncated by the engine
at the pre-registered costs and one is still truncated at the flat row. **The book is tradeable by
hand**: twelve dates a year, about twenty orders on each, two turns a year.

**The claims it moved** (`OBJECTIVE.md`):

- **Claim 1, the signal: confirmed against its control only.** Prediction 1 holds — +0.065 Sharpe
  and +1.30 points of CAGR over the control at the pre-registered costs, +0.105 and +2.24 at the
  flat row, both on Sharpe and CAGR in 2000–2008 and 2018–2026 — and the benchmark limb of success
  criterion 1 fails. A better book than the rule without the cross that loses to its index.
- **Claim 2, the sizing: confirmed as a book against equal weight.** Prediction 3 failed:
  traded-value weighting beats the same names equally weighted by +0.075 Sharpe (pre-registered) and
  +0.064 (flat), more than the 0.03 the blueprint allowed. Its random-draw half is not evidenced.
- **Claim 3, the construction:** holds on the targets by construction; under the band, 556 struck
  weights over the window sat outside the 1%–20% bounds, by at most half a point plus the overnight
  move.

**The success criteria `BLUEPRINT_1.md` set:**

1. **Fails.** The control limb holds; the benchmark limb does not (0.162 and 0.221 against 0.315).
2. **Holds:** the pipeline ran from a working copy whose data folders were emptied first —
   download, rebuild, universe, refinery, analyzer, experiment — and every notebook reached the end
   of its Verify section (the experiment's: 71 checks).
3. **Holds:** 320 rebalance dates, orders, turnover, costs and cash interest stated below.
4. **Holds:** every prediction and lead is reported below, the ones that failed included.

**Two things the blueprint did not foresee, and what was done** (`JOURNAL_1.md`, 2026-10-24):

- **The pre-registered slippage model reads a megacap's daily range as spread.** The engine's
  Corwin–Schultz estimate charged the rule $362,502 of slippage against $15,573 of commission at
  1 bp — about 23 bp a trade, 40 to 55 bp on dates such as 2000-01-03 and 2026-08-03, on AAPL,
  MSFT and NVDA. The stress row (5 bp commission and 10 bp flat slippage) came out cheaper than the
  base. The engine's other estimator, Abdi–Ranaldo, was no better (7 to 40 bp, median by year).
  **The pre-registered row stays the record.** Every book was priced again at the blueprint's own
  fallback half-spread, **a flat 5 bp**, as a re-pricing of the same weights: no new book, and the
  choice of which row the gate is read at is the owner's, a forking path counted as one.
- **Twenty-one engine runs stopped valuing early** — a cash error at a rebalance whose costs outran
  the 1% reserve — and are **excluded by name** (`Backtest/excluded_runs.csv`): at the
  pre-registered costs, eighteen of the twenty random books, the 21-day traded-value setting, the
  20/100 cross and the rule at $100,000; at the flat row, random book 17.

<!-- example: end -->

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
  evidence goes. It may go to paper on probation, on the owner's sign-off, as `BITACORA.md` says;
  paper alone never sends it to production. Otherwise it may be paired with another signal in a
  later experiment, or used at a portfolio manager's discretion — the decision, and its risk, are
  theirs. Never a recommendation.
- **Not sound** — a soundness criterion fails: no conclusion is drawn; fix it and run again.

The sign-off stays a person's name and date. The assistant never decides a gate: it reads each row
from its evidence and says which outcome the rows describe.

<!-- example: begin -->

**Read on 2026-10-27 in the gate's two layers**, by the owner's decision of that date
(`JOURNAL_1.md`), from the run of 2026-10-24: no figure here is computed again. **The gate is read
at the flat 5 bp row** (`JOURNAL_1.md`, 2026-10-24); the pre-registered row is reported beside it.
The run read the gate's former five criteria: criteria 1 to 3 are P1 to P3 below, and criterion 4
is S4.

**Soundness — is the experiment done correctly?**

| # | Soundness criterion | Holds? | The evidence here |
| --- | --- | --- | --- |
| S1 | No survivorship bias | **holds** | the universe is the KN US Equity Core's members as of each date, from the desk's daily holdings, priced by Sharadar to each name's last trade, where the engine sells a delisted holding (`BLUEPRINT_1.md`, *Rules*; *Caveats* below); the share of the Core no price covers is 0.11% on its worst day, and the window was fixed by the universe notebook's coverage rule before any rule existed, the Core priced and signalled at 96.5% on its worst day in the window (`RESULTS.md`, rows 14 and 15); the first cut can price 99.9% to 100% of the Core's weight every year. Stated, not settled: the Core's history before its live date is a backtest of its own rules (*Caveats*) |
| S2 | No look-ahead | **holds** | everything the rule reads on a rebalance date is read at the close before it and filled at the next open, the open price on the date the one condition read that day (`BLUEPRINT_1.md`, *Rules*); the blueprint, its rule and its predictions were written on 2026-10-23, before the rule cell held a line of this version, and committed alone after its critic's objections were answered (`JOURNAL_1.md`, 2026-10-23); every invariant of the notebook's section 2.1 is raised in its Verify |
| S3 | No overfitting | **holds**, with what it discloses | the trial count, **152 books**, is published, the flat-row re-pricing named a forking path and the deflated Sharpe not computed (*The trial count*); the sweep is read as a curve, the cross's margin over its control positive at every setting, +0.06 to +0.12 Sharpe at the flat row; the control is priced, and 19 of the 20 random books whole at the flat row, random book 17 excluded by name. At the pre-registered costs eighteen random books were truncated, and there this row is not evidenced |
| S4 | Costs and capacity stated | **holds** | one-way turnover 2.16 a year; commission, slippage and cash interest by book at the pre-registered, flat, stress and $100,000 rows; 348 engine orders a year, 1,481 under $100; capacity at 1% of a name's 63-day traded value, the worst trade $25.9M; what the engine does not model, in `BLUEPRINT_1.md`'s *Costs* and the *Caveats* below. The rule at $100,000 is excluded, a cash error on 2003-01-31 |
| S5 | Reproducible | **holds** | success criterion 2: the pipeline ran from a working copy whose data folders were emptied first — download, rebuild, universe, refinery, analyzer, experiment — and every notebook reached the end of its Verify section (the experiment's: 71 checks); twenty-one engine runs excluded by name, each with its reason, in `Backtest/excluded_runs.csv` |

**Performance — does it earn its place?**

| # | Performance criterion | Pre-registered costs | Flat 5 bp | The evidence here |
| --- | --- | --- | --- | --- |
| P1 | Beats the benchmarks and its control on risk-adjusted return, over the whole window | **fails** | **fails** | Sharpe 0.162 / 0.221 against the Core's 0.315 and `SPY`'s 0.313; the control margins, +0.065 / +0.105 Sharpe and +1.30 / +2.24 points of CAGR, and 2 of 3 sub-periods hold |
| P2 | Attribution shows idiosyncratic alpha in both layers | not evidenced | not evidenced | the first cut's benchmark reconciles to 0.22 points a year; the first cut's selection is −73.2 (by KN sector, compounded), the idiosyncratic +285.0, residual selection +6.7 — and the rule beats 15 of the 19 random books priced whole at the flat row, where the bar is 16 of 20 |
| P3 | Conclusions survive parameter perturbation | not evidenced (6 of 6 priced keep the sign; 2 excluded) | **fails** (8 of 8 keep the sign; 0 of 8 beat the Core) | `Backtest/sweep_*.csv` |

**The outcome: sound and regime-dependent.** Every soundness criterion holds; performance fails
over the whole window, 2000-01-03 to 2026-08-14, and holds in named periods. At the flat row, each
sub-period priced from its first rebalance date:

| Sub-period | Rule Sharpe | Control Sharpe | Core Sharpe | Rule CAGR | Control CAGR | Core CAGR | Against its control | Against the Core |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2000–2008 | −0.506 | −0.611 | −0.303 | −11.71% | −19.05% | −3.41% | **earned** | failed |
| 2009–2017 | 0.763 | 0.827 | 0.837 | 12.83% | 16.29% | 14.39% | failed | failed |
| 2018–2026 | 0.819 | 0.764 | 0.579 | 26.24% | 25.45% | 14.19% | **earned** | **earned** |

The findings report `SPY` over the whole window only.

**What tells the periods apart, as far as the evidence goes.** Against the Core, the book's whole
shortfall is 2000–2008: the most traded members in 2000 were the bubble's technology and telecom
names, which the book held into the fall and a cross read once a month left late; since 2018 it
beats the Core by about eleven points a year. Against its control, the book earned where the
analyzer found the cross carrying information on the pool and failed where it found almost none:
+0.0259 and +0.0312 at 21 and 63 days in 2000–2008, +0.0150 and +0.0270 in 2018–2026, −0.0027 and
−0.0009 in 2009–2017 (`RESULTS.md`, rows 2 and 3). Both readings name the periods after the fact;
neither is a condition that could be read in advance.

**It is not paper traded alone.** It may be paired with another signal in a later experiment, or
used at a portfolio manager's discretion — the decision, and its risk, are theirs. This is not a
recommendation, and no sign-off is asked.

<!-- example: end -->

## The predictions, evaluated

**Every prediction in the blueprint gets a row, including the ones that were wrong.** A falsified
prediction is worth more than a correct one: it says something about the strategy that nobody knew,
and it cost one run to find out.

| # | Prediction | Outcome | What it changed |
| --- | --- | --- | --- |
| 1 | as written in the blueprint | confirmed or falsified, with the number | what is now understood differently |

<!-- example: begin -->

| # | Prediction | Result | Holds? |
| --- | --- | --- | --- |
| 1 | The cross beats its control by +0.03 Sharpe and +0.5 CAGR points, and on both in 2 of 3 sub-periods | +0.065 Sharpe, +1.30 points (flat: +0.105, +2.24); beats it on both in 2000–2008 and 2018–2026, loses in 2009–2017 | **yes**, both rows |
| 2 | The cross is a drawdown control: shallower maximum drawdown and lower volatility than the control | −82.6% against −91.7%, 25.7% against 29.5% volatility (flat: −78.4% against −91.0%) | **yes** |
| 3 | Traded-value weighting does not beat equal weight by more than 0.03 Sharpe | the book beats equal weight by 0.075 (flat: 0.064) | **no** |
| 4 | Lead: beats both benchmarks on Sharpe | 0.162 / 0.221 against 0.315 | no |
| 5 | Lead: the selection beats chance, 16 of 20 random books | 15 of 19 priced whole at the flat row | not evidenced |
| 6 | Lead: 15 to 60 names on most dates, the cap binding on fewer than a quarter | 19 to 58 names on every date, median 43; the cap binds on 19.7% of dates | yes |
| 7 | Lead: tradeable by hand — a few dozen orders on each date, one-way turnover under 2.0, the stress row moving CAGR by less than a point | about 20 orders a date (median 23 placed by the engine, 17 by the rule), turnover 2.16 a year, the stress row +0.9 points *above* the base | turnover misses 2.0; the rest holds |
| 8 | Lead: most excess return is market and beta, momentum small | 400 of 685 points of the holdings' compounded return are factor exposure, the market 540; **momentum +90 is the largest style**, technology +85, beta −208 | partly: momentum is not small, and the idiosyncratic share is two fifths |

<!-- example: end -->

## The book, priced by the engine

Record the date of the last full re-run from a wiped working copy, the engine version, and the
window. Then the book against every benchmark it reports against, and against the control its
blueprint names, on the rule's own rebalance dates: CAGR, volatility, Sharpe, Sortino, maximum
drawdown — at every cost row the blueprint names, with the commission, the slippage and the cash
interest the engine charged and paid, and every sub-period, each priced from its first rebalance
date. Name the runs excluded by name, and the cash rate Sharpe ratios are measured in excess of.

<!-- example: begin -->

**2000-01-03 to 2026-08-14, net**, 27.56 years as the engine counts them, $1,000,000, integer
shares, a 1% cash reserve; Sharpe ratios are **excess of cash** (the engine's risk-free rate, FRED's
`DFF` averaged over the window, 2.04%), so they are **not comparable with 0.15.2's**.

| Book | CAGR | Volatility | Sharpe | Max drawdown | Alpha vs the Core | Commission | Slippage | Cash interest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **The rule, pre-registered costs** | **6.21%** | 25.73% | **0.162** | −82.6% | −1.91% | $15,573 | $362,502 | $11,937 |
| The control, the cross removed | 4.91% | 29.52% | 0.097 | −91.7% | −3.21% | $3,164 | $113,971 | $7,216 |
| The rule's names, equally weighted | 4.06% | 23.25% | 0.087 | −78.0% | −4.06% | $15,751 | $375,369 | $10,816 |
| **The rule, flat 5 bp** | **7.72%** | 25.65% | **0.221** | −78.4% | −0.40% | $20,474 | $62,984 | $16,997 |
| The control, flat 5 bp | 5.48% | 29.48% | 0.117 | −91.0% | −2.64% | $3,497 | $14,267 | $8,505 |
| Equal weight, flat 5 bp | 5.67% | 23.16% | 0.157 | −72.9% | −2.45% | $20,594 | $67,293 | $15,268 |
| The rule, stress costs | 7.15% | 25.66% | 0.199 | −79.8% | −0.97% | $92,527 | $112,920 | $14,957 |
| The control, stress costs | 5.32% | 29.48% | 0.111 | −91.1% | −2.80% | $17,015 | $27,704 | $8,174 |
| The control, $100,000 | 5.21% | 29.05% | 0.109 | −90.9% | −2.92% | $312 | $11,459 | $1,145 |
| KN US Equity Core | 8.12% | 19.30% | 0.315 | −53.9% | — | — | — | — |
| `SPY` | 8.09% | 19.28% | 0.313 | −55.2% | — | — | — | — |

The benchmarks' statistics are the engine's own metrics over the daily series the engine returns for
each benchmark, on the book's window, years and risk-free rate; until 0.16.2 they were the figures
the engine reported beside a single run, whose volatility (19.76%), Sharpe (0.308) and drawdown
(−51.4%) no series of the index reproduces — the index's own returns file gives 19.30% and −53.9%.
The CAGRs agree to the last digit. The verdict does not depend on it.

The rule at $100,000 is excluded: a cash error on 2003-01-31.

**By sub-period**, each priced from its first rebalance date:

| Sub-period | Rule Sharpe | Control Sharpe | Rule CAGR | Control CAGR | Core CAGR | Core Sharpe | Beats the control on both |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2000–2008 | −0.569 (flat −0.506) | −0.629 (−0.611) | −13.68% (−11.71%) | −19.77% (−19.05%) | −3.41% | −0.303 | yes |
| 2009–2017 | 0.699 (0.763) | 0.805 (0.827) | 11.80% (12.83%) | 15.88% (16.29%) | 14.39% | 0.837 | **no** |
| 2018–2026 | 0.772 (0.819) | 0.743 (0.764) | 24.91% (26.24%) | 24.85% (25.45%) | 14.19% | 0.579 | yes |

**The book's whole shortfall against the index is 2000–2008.** The most traded members in 2000 were
the technology and telecom names of the bubble; ranked and weighted by what they traded, the book
held them into the fall, and a cross read once a month left late. It lost 13.7% a year where the
Core lost 3.4%. Since 2018 it beats the Core by about eleven points a year.

**The sweep, criterion 3**, each setting with its own control on the rule's dates:

| Setting | Sharpe (pre-registered) | Control | Sharpe (flat 5 bp) | Control | Margin keeps its sign (flat) | Beats the Core (flat) |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| cap 15% | 0.165 | 0.108 | 0.224 | 0.128 | yes | no |
| cap 25% | 0.153 | 0.083 | 0.212 | 0.102 | yes | no |
| floor 0.5% | 0.184 | 0.106 | 0.242 | 0.123 | yes | no |
| floor 2% | 0.173 | 0.095 | 0.233 | 0.116 | yes | no |
| traded value over 21 days | excluded | 0.052 | 0.210 | 0.089 | yes | no |
| traded value over 126 days | 0.168 | 0.096 | 0.227 | 0.112 | yes | no |
| cross 20/100 | excluded | 0.099 | 0.228 | 0.118 | yes | no |
| cross 100/300 | 0.147 | 0.102 | 0.186 | 0.122 | yes | no |

**Read as a curve:** the cross's margin over its control is positive at every setting, cap, floor,
traded-value window and cross alike, between +0.06 and +0.12 Sharpe at the flat row; the level of
every setting sits a third below the index's.

**The band**, read on orders: 348 engine orders a year at half a point, 398 at a quarter, 317 at a
full point, the Sharpe moving by less than 0.03 across the three.

<!-- example: end -->

## What the book is, structurally — and can a person trade it?

Rebalance frequency, orders and turnover, holdings, concentration, invested share, and any
structural tilt — each with a reading of what a bad value would have meant, and whether a person
could follow the book by hand at a broker.

<!-- example: begin -->

| Measure | Value |
| --- | ---: |
| Rebalance dates | 320, the first trading day of each month |
| Names held, median (range) | 43 (19 to 58) |
| Effective positions, mean | 24.1 |
| Dates the 20% cap binds | 19.7% |
| Invested, mean (lowest) | 98.7% (92.8%) |
| Rule orders per date, median (largest) | 17 (75) |
| Held names the band left alone per date, median | 31 |
| Engine orders a year, $1M | 348 — a median of 23 a date, a median order of $4,446 |
| Engine orders under $100 over the window | 1,481 — the band's residue: a kept name re-traded by a few dollars |
| One-way turnover a year, engine's daily weights | 2.16 (control 0.75) |
| Capacity at 1% of a name's 63-day traded value | worst trade $25.9M, 1st percentile $69.6M, median $3.25bn |

**A person can follow it**: one date a month, about twenty tickets, most of them a few thousand
dollars at a million. The band does what it was for — 31 of 43 names left alone on a median date —
and leaves dust the engine still trades, which the Backtest Engine cannot skip today.

<!-- example: end -->

## The trial count

How many variants were ranked to reach the book above, and every run excluded by name with its
reason, as `Backtest/excluded_runs.csv` lists them. `RESULTS.md` compiles this: a reader cannot
discount a best-of-N result without knowing N, and soundness criterion S3 says whether the deflated
figure was also computed.

<!-- example: begin -->

**152 books**, as the blueprint fixed: 107 before this version and 45 here. The flat-row re-pricing,
the stress and sub-period rows and one test pricing of the rule with the Abdi–Ranaldo estimator
re-price these books and add none. **The flat row was added after the pre-registered result was
seen** — a forking path, listed here and in `RESULTS.md`. Twenty-one runs are excluded by name and
still count. The deflated Sharpe is not computed.

<!-- example: end -->

## Attribution — is this the signal, or a factor exposure wearing its name?

Brinson-Fachler: allocation, selection, interaction. The factor model: factor against idiosyncratic.
State the window, which is bound by the supplied files' coverage and is usually shorter than the
backtest.

**What it settles**, and **what it does not** — naming the counterfactual book that would settle
what is left: the same holdings with the signal off, positions equalised, a random draw at the same
sizes, entry dates shifted.

<!-- example: begin -->

**KaxaNuk Attribution Analysis 0.5.0**, by the owner's decisions of 2026-10-24: the textbook
Brinson–Fachler (1985) **by KN sector** — each security in the sector the factor model classifies it
in, 51 listings no sector file carries as `unclassified`, the book's cash a segment of its own — and
every cumulative effect **linked with Carino**, so effects add up to the compounded return over the
26 years. Figures are points of compounded return. **The KN US Equity Factor Model's Experiment 1**,
momentum skipping the latest month — **unreviewed by its owner and provisional**; the library
computes the idiosyncratic residual itself, as the return its factors leave unexplained. Both weight
tables held overnight. The first cut can price 99.9% to 100% of the Core's weight every year.

**The precondition holds:** the first cut's benchmark earns 10.19 points a year against the Core's
own returns file's 9.97 — a gap of **0.22**, inside the blueprint's 1.0.

**First cut, Brinson–Fachler by KN sector**, at the flat row: the book's holdings 736.7, the index's
805.2, **alpha −68.5**: allocation −201.9, **selection −73.2**, interaction +206.6. The control's
alpha −414.6 (selection −69.0), equal weight's −395.9 (selection −260.1). The base row moves none of
these by more than five points.

**Second layer, the factor model**, at the flat row:

| | Rule | Control | Equal weight |
| --- | ---: | ---: | ---: |
| Holdings return | 685.4 | 361.6 | 378.2 |
| Factor return | 400.4 | 194.5 | 290.3 |
| **Idiosyncratic** | **+285.0** | +167.1 | +87.8 |
| Market | 539.8 | 354.9 | 396.0 |
| Momentum | +90.5 | +75.9 | +57.9 |
| Technology | +85.0 | +71.7 | +46.3 |
| Size | +23.5 | −3.5 | +23.5 |
| Beta | −207.6 | −209.9 | −124.7 |
| Residual volatility | −47.8 | −22.3 | −45.8 |
| Value | −40.1 | −27.4 | −14.8 |
| Financials | −32.7 | −28.4 | −23.4 |

The base row moves none of these by more than three points (rule idiosyncratic +283.8). The random
books' idiosyncratic return at the flat row runs from −57.7 to +679.8, median +117.6.

**Third pass, Brinson–Fachler on the residual**: the rule's residual alpha +49.6 — selection
**+6.7**, interaction +41.3, allocation +1.6; the control's selection +22.3, equal weight's −19.0.

**What attribution says.** The first cut now says plainly what the summed figures of 0.16.0 hid: the
book's holdings compounded to 737% against the index's 805%, and the shortfall is **the sector
bets** (allocation −202) and the picks inside sectors (selection −73), offset by their interaction
(+207) — the book is heavy where its picks did well. In the second layer three fifths of the
holdings' compounded return is factor exposure — the market above all, then momentum and technology,
against a negative beta, value and residual volatility. **Momentum is the largest style**, as in
0.16.0. The idiosyncratic residual is larger than the summed figure, +285 compounded against +43
summed: summing daily effects understates what compounds over 26 years, and the residual is now the
library's own, not the model's file. The random books, 15 of 19 beaten against a bar of 16 of 20, do
not separate it from chance, and the residual pass's selection, +6.7, is small: **criterion 2 is not
evidenced**.

**What moved from 0.16.0, and why.** Every attribution figure: the library went from 0.2.0 to 0.5.0,
the first cut from the per-asset formula to the textbook one by KN sector, every cumulative from a
sum to a Carino link, and the residual from the model's file to the library's. No engine figure of
the book moved; the benchmarks' volatility, Sharpe and drawdown did, as the cost table says.

<!-- example: end -->

## What is open, ranked

The single highest-value run outstanding, and what it would settle.

<!-- example: begin -->

1. **The spread.** Neither of the engine's range-based estimators gives a believable spread on the
   most traded US stocks; a quoted-spread source in `Bibliotheca/` would settle which cost row the
   gate is read at. Filed for the Backtest Engine.
2. **The random books at the pre-registered costs**, and the rule at $100,000: a cash reserve that
   fits a book's costs, or an engine that scales orders to the cash it has, would price them.
3. **2000–2008.** The book's loss to the index is one regime. A later experiment that leaves the
   bubble's most traded names sooner — a faster cross, a sector cap — would have to earn it against
   this one.
4. **The deflated Sharpe** against 152 trials.

<!-- example: end -->

## Caveats

| # | Caveat | Effect |
| --- | --- | --- |
| 1 | what a reader must know before quoting a number above | what it does to that number |

<!-- example: begin -->

- In sample, every figure; nothing after 2026-08-14 exists in the Core or the factor model.
- The open each book is filled at keeps Sharadar's three-decimal rounding (0.23 bp of the Core at
  most); the adjustment, signals and marks use the rebuilt exact close.
- A delisted name is sold at Sharadar's last trade, over the counter where the exchange dropped it,
  which a hand-traded account may not reach.
- The cash spread is flat; a broker's terms depend on the balance.
- The KN US Equity Core's history before its live date is a backtest of its own rules
  ([an issue in the Analytics Factory's private repository]).
- The factor model is provisional.

<!-- example: end -->
