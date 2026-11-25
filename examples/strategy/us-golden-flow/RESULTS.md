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

<!-- example: begin -->

> **In this example, what follows each template paragraph is Golden Flow's, measured.** Experiment 1
> ran end to end on 2026-10-24 from a working copy whose data folders were emptied first, on
> Backtest Engine 0.67.0 and Attribution Analysis 0.5.0, and is read here through the two-layer gate
> of `Paper_Trading/BITACORA.md`. Versions such as 0.15.0 and 0.16.0 below are Golden Flow's own;
> the earlier ones are not in this copy. A table whose row reads as an instruction is the template's
> shape, and Golden Flow's follows it.
>
> **0.22.0: Experiment 1 reads as sound and regime-dependent, and goes to paper on probation** as
> `Paper_Trading_1`, on the owner's sign-off of 2026-10-27 — the book as it is, no regime filter,
> at the flat 5 bp row, for 12 months to a review on 2027-10-27 against the KN US Equity Core and
> its control. No number moves: the gate in two layers is in
> [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), and the book's registration in
> [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md).

<!-- example: end -->

## The project in three sentences

Does Experiment 1's book beat its benchmark and its control, with its headline numbers. What
attribution says about where the return comes from. Which lever earned its place after Experiment 1,
and which was rejected.

<!-- example: begin -->

**The golden cross earns its keep against the same book without it, and the book still loses to its
index.** Over 2000-01-03 to 2026-08-14, net, monthly, the KN US Equity Core members whose 50-day
average sits above their 200-day, ranked and weighted by 63-day traded value inside 1% and 20%,
compound at 6.21% for a Sharpe of 0.162 at the pre-registered costs, 7.72% and 0.221 at a flat 5 bp
half-spread — against 4.91% and 0.097 for the same rule without the cross, and 8.12% and 0.315 for
the KN US Equity Core. Sharpe ratios are excess of cash.

**The whole shortfall is 2000–2008**, when the most traded names were the bubble's and the book lost
13.7% a year to the Core's 3.4%; since 2018 it beats the Core by about eleven points a year. By KN
sector its holdings compounded to 737% against the index's 805%, the sector bets costing the most;
three fifths of the holdings' return is factor exposure — the market, then momentum and technology —
and its idiosyncratic residual, +285 points compounded, does not separate from random books priced
whole (Attribution Analysis 0.5.0, textbook Brinson-Fachler by KN sector, Carino-linked).

**It reads as sound and regime-dependent, and it is tradeable.** Every soundness criterion of the
gate holds; over the whole window the book loses to its index at both cost rows, and it earned in
2018–2026 alone of the blueprint's three sub-periods. It goes to paper on probation as
`Paper_Trading_1`, on the owner's sign-off of 2026-10-27. Twelve dates a
year, about twenty orders on each, two turns a year.

<!-- example: end -->

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

<!-- example: begin -->

**0.16.0, measured on 2026-10-23 by `Data/analyzer_marimo.py`** over the KN US Equity Core of
2026-10-22 on Sharadar prices — 702 to 915 members a day, 2,198 securities priced — every matrix cut
at 2026-08-14, the last date of the Core and the factor model. The **pool** is the fifty most traded
members on each date, the neighbourhood the rule selects from; the **window** is 2000-01-03 to
2026-08-14, fixed by the universe notebook's coverage rule before any rule existed, and read in the
three thirds the blueprint judges the book on. The expected sign is positive throughout.
Consecutive windows share 20, 62 and 251 days at the three horizons, so the dates are not
independent and the ratios overstate the evidence. Every price read is the rebuilt total-return
close, `c_close_dividend_and_split_adjusted` (section 1.1).

| # | Measurement | The window | Dates with the expected sign | 2000–2008 | 2009–2017 | 2018–2026 | Section |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Mean pairwise correlation of daily returns, 1,992 members with 500 days in the window | 0.237 | — | | | | 2 |
| 2 | The cross as a state, 1 above and 0 below, information coefficient on the pool, 21 days | +0.0127 (IR 0.058) | 52.7% | +0.0259 | −0.0027 | +0.0150 | 4 |
| 3 | The same, 63 days | +0.0189 (IR 0.092) | 53.0% | +0.0312 | −0.0009 | +0.0270 | 4 |
| 4 | The same, 252 days | +0.0151 (IR 0.078) | 52.4% | +0.0411 | +0.0113 | −0.0112 | 4 |
| 5 | The trend distance `r_trend_50_200`, on the pool, 21 / 63 / 252 days | +0.0264 / +0.0322 / +0.0108 | 55.9% / 54.6% / 49.8% | +0.0440 / +0.0518 / +0.0230 | +0.0072 / +0.0099 / +0.0142 | +0.0279 / +0.0353 / −0.0078 | 4 |
| 6 | The traded-value rank `r_liquidity_rank`, on the pool, 21 days | +0.0011 (IR 0.006) | 50.6% | −0.0291 | +0.0111 | +0.0223 | 4 |
| 7 | The same, 63 days | +0.0037 (IR 0.021) | 49.3% | −0.0395 | +0.0100 | +0.0435 | 4 |
| 8 | The same, 252 days | +0.0130 (IR 0.073) | 51.0% | −0.0504 | +0.0178 | **+0.0825** | 4 |
| 9 | The traded-value rank on every member, 252 days | **−0.0391 (IR −0.311)** | **38.0%** | **−0.1115** | −0.0226 | +0.0271 | 4 |
| 10 | Forward 21-day return on the pool, cross on against off | 0.87% against 0.20% | — | | | | 5 |
| 11 | Forward 21-day volatility on the pool, cross on against off | 31.8% against 43.0% | — | | | | 5 |
| 12 | Golden-cross members holding at least 1% of the cross members' traded value, median by year | 8 to 21 | — | | | | 5 |
| 13 | The largest single share of the cross members' traded value, median by year | 2.0% (2013) to 14.9% (2024) | — | | | | 5 |
| 14 | The share of the Core no price covers, worst day | 0.11% (2008) | — | | | | universe 5 |
| 15 | The share of the Core priced and signalled, worst day in the window | 96.5% (2000) | — | | | | universe 5 |
| 16 | Splits at which Sharadar's volume was adjusted twice, corrected by the Curator | 82, in 77 listings | — | | | | 1.1 |
| 17 | The open's rounding the fills keep, weighted by the Core | 0.23 bp at most (2009), 0.03 bp in 2026 | — | | | | 1.1 |

**What it says, before any book.** Over the whole window the cross carries a small positive
coefficient on the pool at every horizon, strongest in 2000–2008, about nothing in 2009–2017, and
positive again since 2018 at one and three months; **it separates volatility far more than return**
— eleven points of forward volatility against seven tenths of a point of monthly return. The
traded-value rank inside the pool is close to nothing over the window: negative in 2000–2008,
positive since, strongly at a year after 2018. **Across every member it points the wrong way**
(−0.039 at a year, the expected sign on 38% of dates), as the three liquidity papers in
`Bibliotheca/` say, so nothing here licenses ranking the whole index by liquidity, and the rule does
not. The index's concentration rose across the window, the largest name's share of the cross
members' traded value going from 2% in 2013 to 15% in 2024, which is what the 20% cap exists for.

<!-- example: end -->

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

<!-- example: begin -->

| Exp | Book | CAGR | Sharpe | Max DD | Control Sharpe | vs control | Status | Claim moved | Findings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| **1** | KN US Equity Core members above the golden cross, ranked and weighted by 63-day traded value, cap 20%, floor 1%, **monthly**, next-open fill, a half-point band, cash at Fed funds less half a point; Sharadar, 2000–2026 | **6.21%** (flat 5 bp: 7.72%) | **0.162** (0.221) | −82.6% (−78.4%) | 0.097 (0.117) | **+0.065** (+0.105) | **sound and regime-dependent**: S1 to S5 hold; P1 and P3 fail at both cost rows and P2 is not evidenced; it earned in 2018–2026 and failed in 2000–2008 and 2009–2017; on paper on probation as `Paper_Trading_1` from 2026-10-27 | 1, the signal: **confirmed against its control only**; 2, the sizing: **confirmed as a book against equal weight**; 3: true on the targets | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |
| 1, earlier, on FMP | KN US Equity Core members above the golden cross, ranked and weighted by 63-day traded value, cap 20%, floor 1%, on change; FMP, 2015–2026 | 20.33% | 0.842 | −32.5% | 0.763 | +0.080 | replaced; under the gate's earlier form, criteria 1 to 4 passed and the owner signed it into paper trading on 2026-10-06; retired on 2026-10-24, when Sharadar became the only provider | 1 and 2 confirmed as a book on that window, which no longer stands | not part of this example |
| 1, earlier, another index | an earlier version, on another index | 24.69% | 0.948 | −34.6% | 0.842 | +0.106 | replaced | the objective of its time; none of it carries over | not part of this example |

**The 0.16.0 row is Experiment 1 rewritten a second time** (`BLUEPRINT_1.md` of 2026-10-23): on the
first trading day of each month, at the open, the KN US Equity Core's members with a golden cross at
the month's last close, a 200-day history, a traded value and an open, ranked and weighted by 63-day
traded value inside 1% and 20%, a held name left as it drifted when its target moved by half a point
or less; Sharadar prices, the adjustment rebuilt from the exact close; commission 1 bp and the
engine's slippage, cash paid at FRED's `DFF` less half a point, $1,000,000, integer shares, a 1%
reserve; 2000-01-03 to 2026-08-14. Its control is the same rule without the cross on the same dates.
Figures in brackets are the flat 5 bp re-pricing (*Excluded runs* and `FINDINGS_1.md` say why).

**The second and third rows are earlier versions of Experiment 1**: the first rewrite, on FMP
prices from 2015-01-02 to 2026-06-01, re-struck whenever the held set changed; and before it, a
version on another index. A rewrite keeps its earlier version as a row, and its books count in the
trials below. None of their numbers describes this rule, and their Sharpe ratios are not excess of
cash, so they do not compare with the first row's.

<!-- example: end -->

### Against the world

The same book measured against every benchmark it reports against, over one stated window.

<!-- example: begin -->

**0.16.0, 2000-01-03 to 2026-08-14, net, Sharpe excess of cash**, 27.56 years as the engine counts
them; from [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md):

| Book | CAGR | Volatility | Sharpe | Max drawdown |
| --- | ---: | ---: | ---: | ---: |
| **The rule, pre-registered costs** | **6.21%** | 25.73% | **0.162** | −82.6% |
| The rule, flat 5 bp | 7.72% | 25.65% | 0.221 | −78.4% |
| The control, the cross removed | 4.91% | 29.52% | 0.097 | −91.7% |
| The rule's names, equally weighted | 4.06% | 23.25% | 0.087 | −78.0% |
| The rule, stress costs | 7.15% | 25.66% | 0.199 | −79.8% |
| KN US Equity Core | 8.12% | 19.30% | 0.315 | −53.9% |
| `SPY` | 8.09% | 19.28% | 0.313 | −55.2% |

**By sub-period**, the three the blueprint fixed before the run, each priced from its first
rebalance date; from [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md):

| Sub-period | Rule Sharpe | Control Sharpe | Rule CAGR | Control CAGR | Core CAGR | Core Sharpe | Beats the control on both |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2000–2008 | −0.569 (flat −0.506) | −0.629 (−0.611) | −13.68% (−11.71%) | −19.77% (−19.05%) | −3.41% | −0.303 | yes |
| 2009–2017 | 0.699 (0.763) | 0.805 (0.827) | 11.80% (12.83%) | 15.88% (16.29%) | 14.39% | 0.837 | **no** |
| 2018–2026 | 0.772 (0.819) | 0.743 (0.764) | 24.91% (26.24%) | 24.85% (25.45%) | 14.19% | 0.579 | yes |

**Where the return comes from**, by KaxaNuk Attribution Analysis 0.5.0: the textbook
Brinson-Fachler by KN sector, every cumulative effect linked with Carino, so effects are points of
compounded return over the 26 years. The first cut's benchmark reconciles with the Core's own
returns file to 0.22 points a year, inside the blueprint's 1.0. At the flat row, the book's holdings
compounded to 736.7% against the index's 805.2%: allocation −201.9, selection −73.2, interaction
+206.6. The factor model, the KN US Equity Factor Model's Experiment 1, is provisional:

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

The random books' idiosyncratic return at the flat row runs from −57.7 to +679.8, median +117.6.
Once factors are stripped out, the third pass's selection is +6.7 for the rule, +22.3 for the
control and −19.0 for equal weight.

<!-- example: end -->

**Does it reproduce?** Re-run from a wiped working copy and state the drift. A Sharpe moving in the
third decimal is the re-pull's rebasing, limitation 5 below, not a strategy change.

<!-- example: begin -->

**Experiment 1 ran from a working copy whose data folders were emptied first** — download,
rebuild, universe, refinery, analyzer, experiment — and every notebook reached the end of its
Verify section, the experiment's with 71 checks
([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), success criterion 2). A clone on
another machine is the stronger test, and is still to be run.

<!-- example: end -->

### The trial count

**How many variants were ranked in each experiment, plus any excluded run**, published as item 3 of
the bar in `AGENTS.md` asks.

<!-- example: begin -->

**152 books**, as the blueprint fixed: 107 before this version and 45 here. The flat-row re-pricing,
the stress and sub-period rows and one test pricing of the rule with the Abdi–Ranaldo estimator
re-price these books and add none. **The flat row was added after the pre-registered result was
seen** — a forking path, listed here and in `RESULTS.md`. Twenty-one runs are excluded by name and
still count. The deflated Sharpe is not computed.

The 107 were priced by the two earlier versions of Experiment 1 in the experiments table, and 45
by this one: the rule, its control, the sixteen of the sweep, the four of the band, the
equal-weight arm, twenty random books, and the rule and control at $100,000. **Two choices are not
books and are counted beside them: the 2000 floor, and the flat 5 bp row.**

<!-- example: end -->

---

## What stands — reuse, do not rebuild

A result, a module or a method later work should start from rather than re-derive. One line each,
with its number.

<!-- example: begin -->

- **The control that differs in exactly one thing.** The same names, the same sizing, the rule's own
  dates, the golden cross off: on the KN US Equity Core from 2000 it measures the cross at +0.065
  of Sharpe and +1.30 points of CAGR at the pre-registered costs, +0.105 and +2.24 at the flat row,
  and a drawdown of −82.6% against −91.7%.
- **The random arm at the rule's turnover.** Twenty books draw the rule's count, on its dates, from
  the members the control may hold, sized by traded value under the cap and under the same band.
  At the flat row 19 were priced whole, and the rule's idiosyncratic return beats 15 of them.
- **Costs and cash inside the engine, with a second row beside the pre-registered one.** The
  engine's spread model read a megacap's daily range as spread, about 23 bp a trade; the flat 5 bp
  row, the blueprint's own fallback, re-prices the same weights and adds no book.
- **The reconciliation before the first cut, and weights held overnight.** The Brinson-Fachler
  benchmark is checked against the index's own returns before any pass is read: 0.22 points a year
  here. Both weight tables pair the close of t−1 with day t's return.
- **The band.** A held name is left as it drifted when its target moved by half a point or less:
  31 of 43 names left alone on a median date, 348 engine orders a year at $1,000,000, the Sharpe
  moving by less than 0.03 across a quarter, a half and a full point.

<!-- example: end -->

## What is closed — do not re-propose without a new argument

Each rejected idea, with the number that rejected it. This list is what stops the next person
repeating it.

<!-- example: begin -->

- **Equal weight as the better sizing.** Closed again from 2000: the same names equally weighted
  earn a Sharpe of 0.087 against the rule's 0.162, and 0.157 against 0.221 at the flat row.
- **The filter as a return-neutral drawdown shield.** Closed again: the golden cross adds 1.30
  points of CAGR as well as a drawdown 9.1 points shallower than the control's.
- **Attribution with each day's weights paired with that day's return.** Closed by an earlier
  version's reconciliation, which read the index 6.94 points a year above its own returns that way.
  Every pass pairs the close of t−1 with day t.
- **Ranking the whole universe by liquidity.** Across every member the traded-value rank over a
  year reads −0.0391, at an information ratio of −0.311 and the expected sign on 38.0% of dates
  (row 9 above), and the rule does not rank the whole index.

<!-- example: end -->

### The uncomfortable one

The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.

<!-- example: begin -->

**The book's whole shortfall against the index is one regime.** In 2000–2008 the most traded
members were the technology and telecom names of the bubble; ranked and weighted by what they
traded, the book held them into the fall, and a cross read once a month left late: it lost 13.68% a
year where the Core lost 3.41%. Since 2018 it beats the Core by about eleven points a year. Beside
it, **three fifths of the holdings' compounded return is factor exposure**, momentum the largest
style, and the residual does not separate from random books: 15 of 19 beaten, against a bar of 16
of 20. Claim 1 holds against its control and not against the index.

<!-- example: end -->

## Open leads, ranked

The single highest-value run outstanding, and what it would settle. Then the next.

<!-- example: begin -->

1. **The spread.** Neither of the engine's range-based estimators gives a believable spread on the
   most traded US stocks; a quoted-spread source in `Bibliotheca/` would settle which cost row the
   gate is read at.
2. **The random books at the pre-registered costs**, and the rule at $100,000: a cash reserve that
   fits a book's costs, or an engine that scales orders to the cash it has, would price them.
3. **2000–2008.** The book's loss to the index is one regime. A later experiment that leaves the
   bubble's most traded names sooner — a faster cross, a sector cap — or pairs the rule with
   another signal would have to earn it against this one, never as a change to it.
4. **The deflated Sharpe** against 152 trials. Publishing the count is the minimum, not the answer.
5. **The shifted-entry timing arm**, not run by the gate written before the run, so timing skill is
   not separated from selection.
6. **Paper days.** `Paper_Trading_1` is on paper on probation from 2026-10-27, to its review on
   2027-10-27; until it has days on paper, nothing here has an out-of-sample test.

<!-- example: end -->

## Excluded runs

Variants removed from the tables above, each by name with its reason, rather than reported with a
caveat. **A metric computed over a truncated or rejected run does not belong in the same column as
a complete one.**

| Variant | Why |
| --- | --- |
| | what went wrong, how it was caught, and what now prevents it |

<!-- example: begin -->

| Variant | Why |
| --- | --- |
| 0.16.0, at the pre-registered costs: random books 01–04, 07, 08 and 10–20; the 21-day traded-value setting; the 20/100 cross; the rule at $100,000 — twenty runs | **Truncated**: the engine stopped valuing at a rebalance whose costs outran the 1% cash reserve (a cash error): thirteen between September 2008 and May 2009, six between February 2000 and July 2002, and the rule at $100,000 on 2003-01-31. The engine's slippage there read a megacap's daily range as spread; at the flat 5 bp row all but one were priced whole. Listed in `Experiments/Experiment_1/Backtest/excluded_runs.csv` |
| 0.16.0, random book 17 at the flat 5 bp row | Truncated the same way, on 2011-02-28 |

<!-- example: end -->

## Known limitations

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing is out of sample** until a frozen book has days on paper after its freeze | Every number here is in-sample, and in-sample selection is what the deflation literature warns about |
| 2 | **A control arm differing in exactly one thing**, item 9 of the bar in `AGENTS.md`, is missing from any experiment that claims a margin | Which lever earned that margin is inferred from per-lever rows, not measured |
| 3 | Classification buckets use today's labels, not point-in-time | Anything reclassified mid-window is misattributed before its move — the `current_*` prefix marks exactly this |
| 4 | Delisting exits use one day of hindsight | A position is sold on the last day it still has a fill price, knowable only the day after |
| 5 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 6 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |

<!-- example: begin -->

**Limitations 1, 2, 4 and 6 hold here, with qualifications.**

- **1.** The book went to paper on probation only on 2026-10-27, and nothing after 2026-08-14
  exists in the Core or the factor model.
- **2.** The control that differs in exactly one thing exists: the golden cross off, on the rule's
  own dates. With the equal-weight arm and the random books, it separates the filter, the sizing and
  the selection. What is missing is the shifted-entry timing arm.
- **4.** Here the exit needs no hindsight: a delisted name is sold by the engine at Sharadar's last
  trade, over the counter where the exchange dropped it, which a hand-traded account may not reach.
- **6.** The deflated Sharpe of the rule against its 152 trials is not computed.

Six more, specific to this example:

| # | Limitation | Effect |
| --- | --- | --- |
| 7 | **The flat 5 bp row was added after the pre-registered result was seen** | A forking path, counted beside the trials; the verdict is the same at both rows |
| 8 | **The open each book is filled at keeps Sharadar's three-decimal rounding** | At most 0.23 bp of the Core (2009), 0.03 bp in 2026; the adjustment, signals and marks use the rebuilt exact close |
| 9 | **The cash spread is flat** | A broker's terms depend on the balance |
| 10 | **The KN US Equity Core's history before its live date is a backtest of its own rules** | Its membership was computed from its methodology; whether every input was dated no later than the day it decided is the Analytics Factory's to state |
| 11 | **The factor model is provisional**, its owner's review pending | Every second-layer and third-pass figure is read as such |
| 12 | **Capacity is stated as a participation bound** | At 1% of a name's 63-day traded value the worst trade allows a $25.9 million book, the median $3.25 billion; a bound on participation, not a model of market impact |

<!-- example: end -->

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**
