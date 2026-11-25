# Findings — Experiment 1

> **Latest valuable results only.** This file is rewritten when a result changes, not appended to —
> the running history is in [`JOURNAL_1.md`](JOURNAL_1.md), and the hypothesis this tested is in
> [`BLUEPRINT_1.md`](BLUEPRINT_1.md).
>
> **[`../../RESULTS.md`](../../RESULTS.md) is compiled from this file.** When a finding here
> changes, change it here first, then update the summary.

<!-- example: begin -->

> The current answer, rewritten whenever the result changes. How it was reached is
> [`JOURNAL_1.md`](JOURNAL_1.md). Every figure below comes from the KaxaNuk Backtest Engine 0.68.0,
> through `experiment_1_marimo.py`, run on 2026-11-20 on the Curator's files of 2026-11-16; the
> twenty random books on 2026-11-24, by the same notebook on the same files, the four base books
> read back from the engine's cache.
> Every attribution figure comes from KaxaNuk Attribution Analysis 0.7.0, through
> `attribute_base_books.py`, run on 2026-11-23 and, with the flat row, the uncapped arm and the
> sub-periods, on 2026-11-24, on those same engine runs, read from their cache; the random books,
> on the factor model, the same day.
> Nothing is computed here.

**The hypothesis is this repository's `BLUEPRINT_1.md`** (commit `69aded0`, written before this
version ran): the same rule, predictions and falsifier as the version it replaces (`506d42f`, tag
`experiment-1-reinvest-v2`), with the cash run the way a fund runs it. **A delisted name's cash is
put back two trading days after its last price** into the names already held, by traded value,
inside the 20% name cap and the 50% sector cap. Every book is struck fully invested beside the
engine's 1% reserve, and only the four base books are priced. The 100% book stopped the engine
on 2008-07-01, so every book is struck **99.5%**, the fallback the blueprint named
(`JOURNAL_1.md`, 2026-11-19). The replaced version, the second pass and the first pass are kept
as rows of `RESULTS.md` and in the journal.

---

<!-- example: end -->

## Status

**Until the first run, *Not yet run*.** After it: one line saying whether the rule beat the
benchmark and its control by what the blueprint required, and which outcome of the gate below it
reads as — a success is necessary for graduation, not sufficient. Then **the claim it moved**: the
claim of `OBJECTIVE.md` the blueprint named, and the status it reached — or why it reached none.

<!-- example: begin -->

**Falsified, as the blueprint words it, for the third time on the same limb: the golden cross adds
nothing on this universe, read monthly, inside a sector cap.** Putting the delisting cash back to
work changed the cash and almost nothing else.

Prediction 1 fails at both cost rows on its sub-period limb. Over the window the rule clears both
margins over its control: +0.040 Sharpe and +0.66 points of CAGR at the pre-registered costs, and
+0.083 and +1.62 at flat 5 bp. But it beats the control on both Sharpe and CAGR in only 1 of the 3
sub-periods (1999–2008), and the blueprint asked for 2. The rule beat its control in 51.2% of its
months (52.5% at the flat row).

The book also **loses to the KN US Equity Core and to `SPY` on Sharpe** at both rows (0.143 and
0.207, against 0.306 and 0.303). P1 fails at both rows. **P2 fails at both rows** (attributed on
2026-11-23 and 2026-11-24): the factor model leaves the rule an idiosyncratic return of +58.07
points, but its selection is −102.69 by sector and −0.03 on the residual (+58.67, −102.82 and
−0.01 at the flat row), and at the flat row it is above 14 of the 20 random books, not the 16
the blueprint asks. P3 is not evidenced in this version. The outcome is the owner's to sign, never
the assistant's.

**What the rewrite was for — the cash — held at the pre-registered costs and not at the flat row.**
The rule's daily cash, as the engine held it:

| | Replaced version, flat 5 bp | This version, pre-registered | This version, flat 5 bp |
| --- | ---: | ---: | ---: |
| Mean | 1.70% | **1.49%** | 1.63% |
| Median | 1.55% | 1.45% | 1.55% |
| 99th percentile | 3.8% | 2.7% | 3.0% |
| Largest | 9.2% | 8.3% (2009-01-06) | 8.7% (2009-01-06) |
| Days above 3% | 170 | 25 | 67 |
| Days above 5% | 32 | 6 | 6 |
| Lead 10: days above 3% outside the two days before a rebalance | — | **0, holds** | **33, fails** |

The six days above 5% are the two before the UST top-up of 2009-01-07: that cash now waits two
days, not a month. **Lead 10 fails at the flat row** on whole shares: the engine buys whole shares
at the dividend-and-split-adjusted open, and Chesapeake's (CHKAQ) adjusted prices carry its 2020
1-for-200 reverse split back. On 2005-10-03 the book asked for 1.13% of it, at about $6,483 a share
where the market traded $38.68, and the engine bought none; the point waited in cash for the month.
The same holds in September 2008 and August 2011. **The blueprint had Verify raise on this bound;
on the owner's go of 2026-11-20 it reports it instead**, a change made after the run was seen and
disclosed here (`JOURNAL_1.md`, 2026-11-20).

**What held:**

- **The cap is a risk limit, at no cost to Sharpe** (prediction 4). The capped book has lower
  volatility (24.7% against 26.0%) and a shallower drawdown (−81.5% against −83.2%) than the same
  rule uncapped. Its Sharpe is 0.1428 against 0.1430.
- **The cross is a drawdown control** (prediction 2): −81.5% against the control's −90.6%.

**What failed besides prediction 1:** traded-value weighting beats equal weight by more than the
0.03 allowed (prediction 3).

**The claims it moved** (this repository's `OBJECTIVE.md` is not written; Golden-Flow's claims):

- **Claim 1, the signal: rejected inside the sector cap.** The window margins over the control
  hold, the sub-periods do not.
- **Claim 2, the sizing:** traded value beats equal weight by +0.074 Sharpe (pre-registered) and
  +0.061 (flat), and the factor model leaves it an idiosyncratic return of +58.07 points against
  −29.76 equally weighted (+58.67 against −29.77 at the flat row). Twenty random books drawn from
  the control's members and sized the same way, priced after the result was seen, leave a median of
  +16.88 at the flat row; the rule is above 14 of them.
- **Claim 3, the construction:** holds by construction:
  - every target sector is at or under 50%, the rule's and the control's;
  - every struck sector is at or under 50% on all 323 rebalance dates, at most 50.0%;
  - every top-up stays inside both caps, buys no name the book did not hold and sells none still
    priced;
  - 572 struck weights sat outside the 1%–20% bounds, the largest 2.45 points above its target.

## The gate, in two layers

**Read at the flat 5 bp row**, as Golden-Flow's owner decided on 2026-10-24; the pre-registered
row beside it.

**Soundness — is the experiment done correctly?**

| # | Soundness criterion | Holds? | The evidence here |
| --- | --- | --- | --- |
| S1 | No survivorship bias | **holds** | The Core's members as of each date, from its daily holdings. The seed's 2,203 listings keep the delisted; each of the 35 forced liquidations of the replaced version is a real exit with its own permaticker |
| S2 | No look-ahead | **holds, with two disclosed** | Membership, cross and score are read at the prior close and filled at the next open. Verify checks that every holding was a member with its cross at 1 at the prior close and had an open on its date. `c_eligible_golden_cross_50_200` agrees with membership and the cross on all 711,569 name-dates. **The sector map is today's KN sector for every date.** **A top-up on L+2 needs one day of hindsight**: that a price series stopped on L is known at the close of L+1, which is why the top-up waits to L+2, as the blueprint states |
| S3 | No overfitting | **holds**, with what it discloses | Trial count 359, published, the twenty random books priced after the result was seen among them. The sweep is not priced in this version; the replaced version's was read as a curve. The window, the cap and its 50% were set after the first pass was seen, the band's reinvestment after the second, the top-up and the 100% after the replaced version, and the 3% bound turned from a raise into a report after this run, as disclosed |
| S4 | Costs and capacity stated | **holds** | One-way turnover 2.27 a year by the engine. 365 engine orders a year, 1,320 of them under $100. Commission, slippage and financing by book are below. Capacity at 1% of a name's 63-day traded value: the worst trade allows $6.4M, the first percentile $71M |
| S5 | Reproducible | **holds** | Run again from a wiped working copy on 2026-11-20 — every output moved aside, the download, the universe, the experiment and the workbooks from nothing: Verify passed 39 checks, the same 20 runs read and none excluded, and the summary, sub-period, gate and tradeability tables and the four weight files equal byte for byte. The random books, priced on 2026-11-24, are not yet run from a wiped copy; the replaced version's reproduced from one, their factor-model rows within 0.012 points |

**Performance — does it earn its place?**

| # | Performance criterion | Pre-registered costs | Flat 5 bp | The evidence here |
| --- | --- | --- | --- | --- |
| P1 | Beats the benchmarks and its control on risk-adjusted return, over the whole window | **fails** | **fails** | Sharpe 0.143 / 0.207 against the Core's 0.306 and `SPY`'s 0.303. Control margins +0.040 / +0.083 Sharpe and +0.66 / +1.62 points of CAGR. Sub-periods beaten on both: 1 / 1 of 3 |
| P2 | Attribution shows idiosyncratic alpha in both layers | **fails** | **fails** | Brinson-Fachler selection −102.69 / −102.82 points, the factor model's idiosyncratic return +58.07 / +58.67, selection on the residual −0.03 / −0.01; above 7 of the 11 random books read / 14 of 20. Below, *What attribution says* |
| P3 | Conclusions survive parameter perturbation | not evidenced | not evidenced | The sweep is not priced in this version; in the replaced version 0 of 8 settings beat the Core |

A criterion that is not run reads *not evidenced*, which is not *holds*.

### Where it earned and where it failed

| Sub-period | Rule Sharpe | Control Sharpe | Core Sharpe | Rule CAGR | Control CAGR | Core CAGR | Against its control | Against the Core |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1999–2008 | −0.523 | −0.642 | −0.310 | −11.15% | −18.01% | −3.41% | **earned** | failed |
| 2009–2017 | 0.750 | 0.833 | 0.855 | 12.74% | 16.36% | 14.35% | failed | failed |
| 2018–2026 | 0.728 | 0.705 | 0.564 | 23.04% | 23.41% | 13.48% | failed on CAGR | **earned** |

This is the flat 5 bp row; at the pre-registered costs the pattern is the same (−0.595 against
−0.664, 0.686 against 0.811, 0.679 against 0.685).

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

## The predictions, evaluated

**Every prediction in the blueprint gets a row, including the ones that were wrong.** A falsified
prediction is worth more than a correct one: it says something about the strategy that nobody knew,
and it cost one run to find out.

| # | Prediction | Outcome | What it changed |
| --- | --- | --- | --- |
| 1 | as written in the blueprint | confirmed or falsified, with the number | what is now understood differently |

<!-- example: begin -->

| # | Prediction (`BLUEPRINT_1.md`) | Result, pre-registered (flat 5 bp) | Holds? |
| --- | --- | --- | --- |
| 1 | The cross beats its control by +0.03 Sharpe and +0.5 CAGR points, and on both in 2 of 3 sub-periods | +0.040 Sharpe, +0.66 points, 1 of 3 (+0.083, +1.62, 1 of 3) | **no**, at both rows: the experiment is falsified |
| 2 | The cross is a drawdown control: shallower drawdown and lower volatility than the control | −81.5% against −90.6%; 24.7% against 28.0% (−76.6% against −89.8%; 24.6% against 27.9%) | **yes** |
| 3 | Traded-value weighting does not beat equal weight by more than 0.03 Sharpe | beats it by 0.074 (0.061) | **no** |
| 4 | The sector cap is a risk limit: lower volatility and drawdown than the uncapped arm, Sharpe within 0.03 | 24.7% against 26.0%, −81.5% against −83.2%, Sharpe 0.1428 against 0.1430 (24.6% against 25.9%, −76.6% against −78.9%, 0.207 against 0.202) | **yes** |
| 5 | Lead: beats both benchmarks on Sharpe | 0.143 (0.207) against 0.306 and 0.303 | no |
| 6 | Lead: the selection beats chance, 16 of 20 random books | idiosyncratic return above 7 of the 11 read, nine truncated; Sharpe above 6 of 11 (14 of 20; Sharpe above 12 of 20) | **no** at the flat row; not evidenced at the pre-registered costs |
| 7 | Lead: 20 to 60 names on most dates, the cap binding on fewer than a quarter | 18 to 58 names, median 43; the sector cap binds on 17.6% of dates, the 20% cap on 17.0% | **yes** |
| 8 | Lead: tradeable by hand — a few dozen orders a date, turnover under 2.5 | median 22 orders a date placed by the engine, 15 by the rule; turnover 2.27 | **yes** |
| 9 | Lead: most excess return is market and beta; technology smaller than the uncapped arm's | the market is the largest contribution, +349.60 points, beta −130.07, of an excess return of +312.29; technology +63.76 against the uncapped arm's +67.93 (+351.16, −130.06, +314.81; +63.86 against +68.06) | **yes**, both limbs, at both rows |
| 10 | Lead: the rule's daily cash at most 3% but a delisting's wait, near the 1% reserve on average | mean 1.49%, 0 days outside the bound (mean 1.63%, 33 days outside it, CHKAQ's whole shares) | **yes** at the pre-registered costs, **no** at the flat row |

## The books

| Book | CAGR | Volatility | Sharpe | Max drawdown | Alpha vs the Core | Commission | Slippage | Financing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **The rule, pre-registered costs** | **5.58%** | 24.69% | **0.143** | −81.5% | −2.34% | $17,578 | $414,716 | −$9,168 |
| The control, the cross removed | 4.93% | 27.97% | 0.102 | −90.6% | −3.00% | $3,667 | $135,638 | −$7,574 |
| The rule's names, equally weighted | 3.60% | 22.35% | 0.069 | −77.1% | −4.33% | $17,504 | $425,929 | −$6,715 |
| The rule without the sector cap | 5.78% | 26.03% | 0.143 | −83.2% | −2.15% | $16,043 | $376,154 | −$9,140 |
| **The rule, flat 5 bp** | **7.14%** | 24.60% | **0.207** | −76.6% | −0.79% | $23,462 | $74,744 | −$13,902 |
| The control, flat 5 bp | 5.53% | 27.93% | 0.124 | −89.8% | −2.40% | $4,093 | $17,406 | −$8,934 |
| Equal weight, flat 5 bp | 5.30% | 22.27% | 0.145 | −71.4% | −2.63% | $23,397 | $79,163 | −$10,420 |
| No sector cap, flat 5 bp | 7.31% | 25.94% | 0.202 | −78.9% | −0.62% | $21,224 | $65,944 | −$13,625 |
| KN US Equity Core | 7.93% | 19.19% | 0.306 | −54.0% | — | — | — | — |
| `SPY` | 7.89% | 19.22% | 0.303 | −55.2% | — | — | — | — |

The terms of the run:

- $1,000,000, each book struck to 99.5% on the monthly dates, a 1% cash reserve and 1 bp
  commission.
- 36 top-up dates shared by the rule and its control, on which a delisted name's cash goes into the
  names held; the uncapped and equal-weight arms top up on their own delistings.
- Cash earns the effective federal funds rate less half a point.
- 1999-12-31 to 2026-10-30, 323 monthly rebalance dates.
- The pre-registered slippage model reads a megacap's daily range as spread.

The rule and its control share 63.0% of their weight on the mean rebalance date. Their monthly
returns overlap that much, so the 51.2% of months the rule won is read as the share it is, not as
323 independent draws.

**Not priced in this version**, by the owner's decision of 2026-11-19: the sweep, the band's
variants, the stress row and the $100,000 rows. Their figures in the replaced
version are that version's, in `RESULTS.md` and at the tag `experiment-1-reinvest-v2`. The
attribution, left out on the same day, was run on the owner's decision of 2026-11-23 on the books
already priced, at the pre-registered costs (`JOURNAL_1.md`, 2026-11-23). **The 20 random books
were priced after all, on the owner's word of 2026-11-24, after this version's result was
seen**, and are counted in the trials (`JOURNAL_1.md`, 2026-11-24).

## What attribution says

**The run.** KaxaNuk Attribution Analysis 0.7.0, on 2026-11-23, through `attribute_base_books.py`,
which shapes the inputs as section 5 of the notebook does and reads the engine's runs of 2026-11-20
from `Backtest/cache/`, pricing nothing again. Three books at the pre-registered costs: the rule,
its control and equal weight. Each is the book the engine held every trading day, widened to every
Core member at zero weight, both weight tables held overnight, every return over the factor model's
implied bill. Brinson-Fachler is the textbook formula by KN sector, the book's cash a segment of its
own; every cumulative figure is linked with Carino, in points of compounded return over the bill.
The same three books at the flat 5 bp row and the rule without its sector cap at both rows were
added on 2026-11-24, in one run of all eight that gave the first three's figures again unchanged.
The factor model is the KN US Equity Factor Model's Experiment 1, provisional: 17 factors — the
market, five styles and the eleven KN sectors — from 20 files, three of them its own totals. It
covers 98.5% of the rule's weight (98.4% of the control's, 98.6% of equal weight's, 98.4% to 98.5%
of every book at the flat row and of the uncapped arm). **Attribution
window: 2000-01-03 to 2026-10-30**, the factor model's first day, against the backtest's
1999-12-31.

**The benchmark reconciles.** The first cut's benchmark earns 8.08 points a year over the bill,
mean daily times 252, against 7.86 for the Core's own returns file: a gap of 0.22, inside the
blueprint's point. The first cut prices the whole index on every year. The library reports 3,136
sector-dates of the rule (3,178 of the control at both rows, 3,136 of every other book) on which
one side held weight with no return, the other side's return used, so no selection was credited
there.

**First cut — Brinson-Fachler by KN sector**, in points:

| | The rule | The control | Equal weight |
| --- | ---: | ---: | ---: |
| The book | +340.06 | +186.25 | +173.66 |
| The KN US Equity Core | +426.26 | +426.26 | +426.26 |
| **Active return** | **−86.20** | −240.01 | −252.60 |
| Allocation | −58.17 | −124.07 | −67.83 |
| Selection | −102.69 | −73.42 | −181.09 |
| Interaction | +74.67 | −42.52 | −3.68 |

The rule loses to the Core through both levers: the sectors it leans into (allocation −58.17) and
the names it picks inside them (selection −102.69), with interaction +74.67 offsetting part of it —
the book is heavier where its picks did better. The control, the same rule without the cross, loses
−240.01 to the Core: that is the exclusion-filter test, the measurement this rule's factor reading
cannot give.

**Second layer — the factor model**, in points:

| | The rule | The control | Equal weight |
| --- | ---: | ---: | ---: |
| Excess return of the holdings | +312.29 | +169.33 | +156.43 |
| **Factors** | **+254.21** | +139.48 | +186.19 |
| **Idiosyncratic** | **+58.07** | +29.86 | −29.76 |
| The market | +349.60 | +253.53 | +268.44 |
| Beta | −130.07 | −146.44 | −84.83 |
| Momentum | +42.48 | +52.34 | +22.70 |
| Size | +14.70 | −3.18 | +14.67 |
| Value | −21.93 | −17.92 | −8.65 |
| Residual volatility | −33.19 | −12.51 | −29.76 |
| Technology | +63.76 | +53.11 | +35.64 |
| Health care | +11.26 | +8.83 | +7.23 |
| Financials | −16.47 | −18.10 | −11.54 |
| Communication | −19.16 | −22.43 | −15.30 |
| Every other KN sector, each | between −5.99 and +4.89 | between −6.01 and +2.32 | between −5.77 and +1.71 |

Most of the rule's excess return is factor exposure: the market +349.60, less beta −130.07, then
technology and momentum. The cross is close to invisible to the model, as an absolute rule is to a
relative factor: the control, without it, reads more momentum (+52.34) than the rule (+42.48), and
nearly the same beta. **Traded-value sizing moves the residual**: +58.07 for the rule against
−29.76 for the same names equally weighted.

**Third pass — Brinson-Fachler on the residual**, in points:

| | The rule | The control | Equal weight |
| --- | ---: | ---: | ---: |
| The book's residual | +32.05 | +21.99 | −15.35 |
| The Core's residual | −2.54 | −2.54 | −2.54 |
| Active | +34.59 | +24.53 | −12.81 |
| Allocation | +4.28 | +3.15 | −2.10 |
| Selection | **−0.03** | +19.79 | −20.36 |
| Interaction | +30.35 | +1.58 | +9.64 |

The residual here is the factor model's own idiosyncratic file over the holdings, run through the
first cut, so its book total is not the second layer's idiosyncratic figure. Once factors are
stripped out, the rule's selection is nothing (−0.03); what it keeps over the Core is interaction,
+30.35: weight that sat where the residual was good, sector by sector. The control's residual
selection, +19.79, is larger than the rule's.

**At the flat 5 bp row, and without the sector cap**, in points; the pre-registered rule beside
them:

| | The rule | The rule, flat | The control, flat | Equal weight, flat | Uncapped | Uncapped, flat |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| First cut: active return | −86.20 | −83.56 | −239.18 | −250.55 | −81.25 | −78.49 |
| Allocation | −58.17 | −57.33 | −123.45 | −66.49 | −121.48 | −121.34 |
| Selection | −102.69 | −102.82 | −73.08 | −181.23 | −82.16 | −81.56 |
| Interaction | +74.67 | +76.59 | −42.66 | −2.83 | +122.39 | +124.42 |
| Factor model: excess return | +312.29 | +314.81 | +170.13 | +158.38 | +317.01 | +319.65 |
| Factors | +254.21 | +256.14 | +140.23 | +188.15 | +234.33 | +236.06 |
| **Idiosyncratic** | **+58.07** | **+58.67** | +29.91 | −29.77 | +82.68 | +83.59 |
| The market | +349.60 | +351.16 | +254.08 | +270.03 | +349.31 | +350.51 |
| Beta | −130.07 | −130.06 | −146.39 | −84.75 | −169.56 | −169.61 |
| Momentum | +42.48 | +42.75 | +52.37 | +22.85 | +54.81 | +55.30 |
| Technology | +63.76 | +63.86 | +53.19 | +35.72 | +67.93 | +68.06 |
| Residual pass: active | +34.59 | +34.81 | +24.51 | −12.75 | +50.16 | +50.54 |
| Residual selection | **−0.03** | **−0.01** | +19.83 | −20.31 | +4.88 | +5.03 |
| Residual interaction | +30.35 | +30.52 | +1.51 | +9.67 | +44.92 | +45.10 |

The cost row barely moves attribution: it reads the holdings' returns over the bill, and the two
rows differ only where costs changed what the engine held. Every reading of the pre-registered row
holds at the flat row. **The sector cap gave up allocation and gained beta**: the uncapped arm
loses −121.48 to the Core by sector against the rule's −58.17, but carries more beta (−169.56
against −130.07), more momentum and more technology (+67.93 against +63.76), the second limb of
lead 9. Its idiosyncratic return is larger (+82.68), and so is its residual selection (+4.88
against −0.03), though its first-cut selection is still negative (−82.16).

**By sub-period, the rule against the uncapped arm**, at the pre-registered costs, in points.
Each column is the whole window's book cut to the sub-period's days, as the notebook's
`SUB_PERIODS` set them, every effect linked by the library over those days alone. It is not the
engine's sub-period book, which starts fresh on the sub-period's first day, and the three columns
of a book do not add up to its window figure: linked effects compound. Each sub-period's first-cut
benchmark reconciles with the Core's own returns, by 0.45, 0.16 and 0.01 points a year.

| | Rule, 1999–2008 | Uncapped | Rule, 2009–2017 | Uncapped | Rule, 2018–2026 | Uncapped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| The book | −73.60 | −75.73 | +210.77 | +210.85 | +418.49 | +470.08 |
| The KN US Equity Core | −42.11 | −42.11 | +246.95 | +246.95 | +150.89 | +150.89 |
| **Active return** | −31.49 | −33.61 | −36.17 | −36.09 | **+267.60** | **+319.20** |
| Allocation | −12.37 | −18.74 | +3.88 | +3.89 | +67.16 | +88.69 |
| Selection | −13.63 | −10.54 | −72.29 | −72.20 | +129.27 | +126.92 |
| Interaction | −5.48 | −4.34 | +32.23 | +32.21 | +71.17 | +103.59 |
| Factor model: excess return | −75.27 | −77.25 | +209.49 | +209.57 | +424.66 | +476.87 |
| Factors | −55.88 | −60.91 | +194.20 | +194.25 | +286.93 | +313.64 |
| **Idiosyncratic** | −19.39 | −16.34 | +15.30 | +15.33 | **+137.73** | **+163.22** |
| The market | −28.31 | −27.88 | +226.39 | +226.42 | +217.94 | +230.55 |
| Beta | −23.61 | −30.36 | −2.91 | −2.89 | −34.81 | −45.23 |
| Momentum | +8.26 | +10.94 | −20.05 | −20.07 | +40.98 | +42.95 |
| Technology | −1.00 | −2.16 | +9.34 | +9.34 | +65.91 | +80.78 |
| Residual selection | −14.28 | −10.91 | −9.37 | −9.34 | +35.41 | +36.11 |
| Residual interaction | −4.54 | −1.48 | +12.88 | +12.87 | +25.95 | +36.23 |

**What the cap gave up is in 2018–2026, and it is allocation, not selection.** In 2009–2017 the
two books are nearly the same book: the cap barely bound. In 1999–2008 the capped book loses a
little less to the Core (−31.49 against −33.61). In 2018–2026 the uncapped arm earns +319.20 over
the Core against the rule's +267.60, through allocation (+88.69 against +67.16) and interaction
(+103.59 against +71.17), with more technology (+80.78 against +65.91) and more beta; its
selection is about the rule's (+126.92 against +129.27).

**The window's P2 failure is 1999–2017's.** In 2018–2026 the rule's selection is positive in all
three layers — +129.27 by sector, +137.73 idiosyncratic, +35.41 on the residual — and negative in
both selections in each earlier third. P2 is read over the window, so it still fails; whether the
last third's selection is above chance is what the random books, below, say.

The flat row reads the same: the rule's 2018–2026 idiosyncratic return is +137.41 there, against
+137.73; every figure is in `Attribution/` `*_by_sub_period.csv`.

**Against twenty random books**, the blueprint's counterfactual for selection. Each draws, on
every rebalance date, as many names from the control's members as the rule holds, sized by
traded value inside the same caps, so it replaces the golden cross and the ranking together.
They were priced on 2026-11-24, after this version's result was seen. At the pre-registered
costs nine stopped with the engine's "Cash error" and are excluded by name, so the flat row is
the one read whole. Each is attributed on the factor model alone, as section 5 of the notebook
does, over the window and cut to each sub-period as the rule's are; the factor model covers
98.4% to 98.5% of their weight over the window (98.5% to 98.6% at the pre-registered costs).
Idiosyncratic return, in points:

| | Window | 1999–2008 | 2009–2017 | 2018–2026 |
| --- | ---: | ---: | ---: | ---: |
| The rule, flat | +58.67 | −19.37 | +15.35 | +137.41 |
| Random books the rule is above, flat | **14 of 20** | 7 of 20 | 14 of 20 | **19 of 20** |
| Their median | +16.88 | −9.57 | −2.13 | +20.37 |
| Their range | −97.01 to +161.79 | −33.39 to +20.93 | −47.54 to +100.54 | −38.23 to +291.87 |
| The rule, pre-registered | +58.07 | −19.39 | +15.30 | +137.73 |
| Random books it is above, of the 11 read | 7 | 2 | 9 | 10 |

**The limb fails over the window**: the rule is above 14 of the 20, and the blueprint asks 16.
On Sharpe the notebook's own table puts it above 12 of 20 at the flat row, 0.207 against a
median of 0.189, and above 6 of the 11 read pre-registered. **2018–2026 is the exception**: the
rule is above 19 of 20, random book 03 alone above it. That third was singled out after it was
seen, one cut of three, so the count is information, not the limb. In 1999–2008 the rule's
residual is below most random draws', in 2009–2017 above 14 of 20, as over the window, and since
2018 above nearly all of them.
Whether that is the cross or the traded-value ranking a random draw cannot say: it replaces
both. Every figure is in `Attribution/random_books.csv` and
`random_books_against_the_rule.csv`.

**What it settles for P2, at both rows: fails.** The blueprint's P2 needs
Brinson-Fachler selection, the idiosyncratic return and the residual selection all above zero, and
the book above 16 of 20 random books. The idiosyncratic return is positive; both selections are not;
the rule is above 14 of the 20 random books at the flat row, and above 7 of the 11 read at the
pre-registered costs, where the limb is not evidenced. The flat row reads the same, signs and all.
The library's relative statistics, over the same days: the rule's information ratio against the Core
0.038, its tracking error 12.9%, its beta to the Core 1.09 (0.039, 12.8% and 1.09 at the flat row;
the uncapped arm 0.060, 14.6% and 1.12).

**Not attributed:** timing — the shifted-entry arm — is not priced. The counterfactuals counted
here are three: the control, equal weight and the twenty random books.

<!-- example: end -->

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

<!-- example: begin -->

**359 books**, as the blueprint counts them: Golden-Flow's 152, the first pass's 45, the second
pass's 46, the first rewrite's first draft's 46 (priced and never read), the replaced version's 46
and this version's 24: its four base books, and the twenty random books priced on the owner's word
of 2026-11-24, after the result was seen. The 100% attempt and its 99.5% fallback are this
version's four books, the fallback named before the run. The run of 2026-11-20: 20 engine runs,
all read; that of 2026-11-24: 40 more, 31 read and 9 excluded by name. The deflated Sharpe is not
computed.

## Excluded runs

**Nine runs of 2026-11-24, at the pre-registered costs: random books 02, 05, 07, 09, 13, 16, 17, 19
and 20**, each truncated by the engine's "Cash error" — 17 valued to 2000-06-30, 02 and 19 to
2000-10-31, the other six to between 2008-09-30 and 2008-11-28 — caught by Verify's count of
valued days against the window's and listed in `Backtest/excluded_runs.csv`. Nothing of them is
read; at the flat row all twenty are whole.

The run at 100% that stopped on 2008-07-01 is replaced by its fallback, as the
blueprint says, and nothing of it is read (`JOURNAL_1.md`, 2026-11-19).

The register's blocking rows exclude 8 names by rule: ARXS, CBRS, FDXF, FPS, H1, ILA.A, PS and
SUNB.

## Against the earlier versions

| | First pass, 2026-11-16 | Second pass, 2026-11-17 | Replaced version, 2026-11-18 | This version, 2026-11-20 |
| --- | ---: | ---: | ---: | ---: |
| Sector cap | none | 50% | 50% | 50% |
| The band | leaves a kept name's shortfall in cash | the same | reinvests it, to 99.5% | the same |
| A delisted name's cash | waits for the month | waits | waits | put back on L+2 |
| Rule, flat: daily cash mean / days above 5% | — | — | 1.70% / 32 | 1.63% / 6 |
| Rule, flat: CAGR / Sharpe | 6.79% / 0.183 | 7.17% / 0.209 | 7.13% / 0.206 | 7.14% / 0.207 |
| Rule, pre-registered: CAGR / Sharpe | 5.30% / 0.125 | 5.65% / 0.146 | 5.58% / 0.143 | 5.58% / 0.143 |
| Prediction 1, flat | holds, 2 of 3 sub-periods | fails, 1 of 3 | fails, 1 of 3 | fails, 1 of 3 |

**Putting the delisting cash back to work moved the headline by a thousandth of Sharpe.** The
cash it saves is real — 32 days above 5% become 6 — but it is a few points of the book for a few
weeks at a time, invested in the names the book already held.

<!-- example: end -->

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

<!-- example: begin -->

- **Look-ahead.** The sector map is today's KN sector for every date. A top-up on L+2 uses the one
  day of hindsight a stopped price series needs.
- **Whole shares at adjusted prices.** A name split in reverse later carries an inflated adjusted
  price into the past; CHKAQ's left a point of the book in cash for a month at a time. A fund
  would hold it. The draft note to `lab@kaxanuk.mx` asks for fractional shares, or whole shares
  counted at the unadjusted price.
- **A stock-for-stock deal becomes cash.** The engine sells an acquired name at its last price;
  the top-up puts the cash back into the names held, not into the acquirer.
- **A top-up date trades more than the freed cash.** Every held name's weight is written as it
  drifted, and the engine rounds each to whole shares, so small orders appear; they are counted.
- **The flat row.** The pre-registered slippage model reads a megacap's daily range as spread. The
  flat row is the re-pricing Golden-Flow's owner chose to read the gate at, a forking path counted
  as one.
- **What the engine does not model:** borrow, market impact beyond its model, taxes, and the venue
  of a delisted name's last trade.
- **The Core before its live date.** Its history there is a backtest of its own rules.

## Open

- **The owner's sign-off** on the outcome: falsified, the third time on the same limb.
- **The four flat 5 bp workbooks imported** into the app with *Import results*; the owner keeps
  only the flat row in the app (2026-11-20).
- **What 2018–2026's selection is**: the golden cross, the traded-value ranking, or both. A random
  draw replaces the two together, and no arm isolates the ranking.
- **The random books from a wiped working copy**, with the rest of this version's attribution.

<!-- example: end -->
