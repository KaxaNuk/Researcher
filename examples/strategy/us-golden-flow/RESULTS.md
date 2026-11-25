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

> **Executive summary of everything this repository has measured.**
>
> Experiment sections are compiled from the `FINDINGS_N.md` files and cite each one. **When a number
> changes, change it in `FINDINGS_N.md` first**, then here, as `AGENTS.md` says. The one exception
> is step 3, `Data/analyzer_marimo.py`: its findings go straight into *Before any experiment*
> below, because a notebook saves no output.
>
> Every performance figure comes from the **KaxaNuk Backtest Engine**, the only backtest here.

<!-- example: end -->

## The project in three sentences

Does Experiment 1's book beat its benchmark and its control, with its headline numbers. What
attribution says about where the return comes from. Which lever earned its place after Experiment 1,
and which was rejected.

---

<!-- example: begin -->

Experiment 1, the most-traded KN US Equity Core members in a golden cross with no sector above half
the book, 99.5% invested, a delisted name's cash put back two days after its last price,
1999-12-31 to 2026-10-30, is **falsified as its blueprint words it**, for the third time on the
same limb: the cross beats its control over the window (Sharpe 0.207 against 0.124 at the flat
5 bp row) but on both Sharpe and CAGR in only 1 of 3 sub-periods, where 2 were required. The book
loses to the Core (0.306) and to `SPY` (0.303). Running the cash as a fund would cut the days the
rule held over 5% cash from 32 to 6 and its mean cash to 1.5%–1.6%, and moved the headline by a
thousandth of Sharpe; the sector cap did what it was for, lower volatility and drawdown than the
same rule uncapped, at the same Sharpe.

---

<!-- example: end -->

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

<!-- example: begin -->

Findings from step 3, `Data/analyzer_marimo.py`: whether a candidate feature carries information,
over what horizon and with which sign, and anything else measured about the signal that needs no
book. Cite the section each number came from.

### The universe, as `Universe/` holds it

Read on 2026-11-23 from the files as they are — the seed, and what `Universe/universe_marimo.py`
wrote on 2026-11-20 from the Curator's files of 2026-11-16 — with no download and no rebuild. Every
file named here but the seed is regenerable and gitignored.

| # | Measurement | Value | Source |
| --- | --- | ---: | --- |
| U1 | Listings in the seed, one row each, every one with its own Sharadar permaticker | 2,203 | `Universe/Investable_Universe.csv`; `Universe/Security_Master.csv` |
| U2 | Of them, delisted by Sharadar's catalogue (`is_delisted` Y) — the seed keeps them | 1,148 (52.1%) | `Universe/Security_Master.csv` |
| U3 | Listings whose last price comes before the panel ends — delisted, acquired or halted | 1,145 | `Universe/Data_Issues.csv`, *early end* |
| U4 | Listings with no price when the floor opens — listed later | 750 | `Universe/Data_Issues.csv`, *late start* |
| U5 | Core members a day, 1999-12-31 to 2026-10-30, 6,749 trading days | 694 to 916, median 815 — the fewest on 2026-10-30, the most on 2014-09-22 | `Universe/Coverage.csv` |
| U6 | Members priced, every day | all of them: priced weight at least 99.997% of the Core's, survivorship cost 0 | `Universe/Coverage.csv` |
| U7 | Members priced and with 200 days of history behind them, as a share of the Core's weight | at least 96.74% (2000-03-20); 98.30% on the floor, 1999-12-31, against the 90% the window requires | `Universe/Coverage.csv`; `Universe/Window.csv` |
| U8 | The window | 1999-12-31 to 2026-10-31 | `Universe/Window.csv` |
| U9 | Index listings Sharadar does not list, or does not carry | 0 and 0 | `Universe/Data_Issues.csv` |
| U10 | Blocking rows — excluded by name from every book: history shorter than the warm-up | 8: ARXS, CBRS, FDXF, FPS, H1, ILA.A, PS, SUNB | `Universe/Data_Issues.csv` |
| U11 | A listing Sharadar files under another ticker: Six Flags Entertainment (permaticker 198958, delisted 2024-07-01), the index's `SIX`, fetched as `SIX1`; a fetch of `SIX` had returned another listing's rows | 1 | `Universe/Provider_Renames.csv` |
| U12 | Splits the Curator's rebuilt adjustment carries | 1,988, in 1,063 listings | `Data/Curator/adjustment_checks.csv` |
| U13 | Days the rebuilt total-return close moves more than 0.5% off Sharadar's own; days a split leaves the rebuilt split-adjusted close more than 2% off | 7 days, in BILL, CXW and IOT (largest 2.3%, BILL); 0 | `Data/Curator/adjustment_checks.csv` |
| U14 | Spin-offs in Sharadar's actions file inside a seed listing's span, the ones the Curator's dividend column leaves out and `Data/curator.py` adds to the total-return close | 339, on 252 listings (GE's of Wabtec, GE HealthCare and GE Vernova among them) | `Data/Curator/Actions/sharadar_actions_2026-11-20.csv` |

### The analyzer's screen

`Data/analyzer_marimo.py`, run on 2026-11-23 on the Curator's files of 2026-11-16 as they are
(Data Curator 0.51.0), with marimo 0.25.2, pandas 2.3.3, NumPy 2.5.5 and SciPy 1.18.1; its Verify
passed 16 checks. It reads the Curator's `c_*` columns alone, as Experiment 1 does: the panel is the
Core's members on each date, the pool the fifty most traded of them by `c_traded_value_sma_63d`
(the rule holds 18 to 58 names), and both are read over the window, 1999-12-31 to 2026-10-30, and
in the blueprint's three sub-periods. It was run after Experiment 1 had reported, so it licenses
nothing that experiment predicted; it is the screen a later blueprint starts from.

**State the horizon and the overlap**, item 11 of the bar in `AGENTS.md`: a coefficient over *h*
days, measured every day, shares *h − 1* days with the next one. Beside any coefficient or ratio,
report the share of dates on which it had the sign the hypothesis expects — positive, for every
feature here. The crosses are 1/0 states, so a rank coefficient on them is directional.

| # | Measurement | Value | Dates with the expected sign | Section |
| --- | --- | ---: | ---: | --- |
| A1 | Member-days with a usable `c_golden_cross_50_200` — the gap is the 200-day warm-up of a late listing | 99.4% | — | 1 |
| A2 | Members with more than 500 daily returns in the window; their mean pairwise correlation | 1,994; 0.236 | — | 2 |
| A3 | The same members: median annualised volatility; median worst day | 43.3%; −24.8% | — | 2 |
| A4 | The traded-value rank is a percentile inside each date; `c_traded_value_sma_63d` is the 63-day average of `c_traded_value`; `c_eligible_golden_cross_50_200` is membership and the cross at the prior close | exact on all 7,001 dates; a largest gap of 0; 0 disagreements in 5,606,947 member-dates | — | 3 |
| A5 | IC of the 50/200 cross on the pool, 21 days, overlap 20 — IR 0.056; by sub-period +0.0266, −0.0026, +0.0126 | +0.0122 | 52.5% | 4 |
| A6 | The same, 63 days, overlap 62 — IR 0.088; by sub-period +0.0345, +0.0004, +0.0192 | +0.0180 | 53.0% | 4 |
| A7 | The same, 252 days, overlap 251 — IR 0.088; by sub-period +0.0447, +0.0130, −0.0103 | +0.0171 | 52.7% | 4 |
| A8 | IC of the 50/200 cross on every member, 63 days — IR 0.118 | +0.0158 | 55.4% | 4 |
| A9 | The sweep's neighbours on the pool, 63 days: the 20/100 cross (IR 0.059); the 100/300 cross (IR 0.164) | +0.0123; +0.0345 | 54.1%; 57.8% | 4 |
| A10 | IC of the traded-value rank on the pool, 252 days — IR 0.076; by sub-period −0.0481, +0.0184, +0.0789 | +0.0136 | 50.8% | 4 |
| A11 | IC of the traded-value rank on every member, 252 days — IR −0.324; by sub-period −0.1151, −0.0251, +0.0255 | −0.0411 | 37.2% | 4 |
| A12 | IC of the traded-value rank on the pool, 21 days — IR 0.012 | +0.0021 | 50.5% | 4 |
| A13 | On the pool, over the window: mean 21-day forward return with the cross on and off (215,068 and 120,911 observations) | +0.87% and +0.20% | — | 5 |
| A14 | The same split, mean 21-day forward volatility, annualised | 31.9% and 43.1% | — | 5 |
| A15 | Traded value among the golden-cross members: the largest member's share, yearly median; members holding at least 1% of it, yearly median | 2.0% to 14.9%; 8 to 21 | — | 5 |
| A16 | **Buy and hold against the cross, stock by stock, over the window**: stocks analysed — a member at the prior close with the cross there, at least 252 such days — and those on which holding only while the cross was on returned more | **1,845; the cross returned more on 735 (39.8%)** | — | 5.1 |
| A17 | The same stocks: the cross fell less at its worst; moved less | 80.3%; 99.7% | — | 5.1 |
| A18 | The same stocks, medians, buy and hold against the cross: annual return; worst decline; volatility | 5.12% against 2.75%; −69.5% against −52.1%; 38.6% against 24.8% | — | 5.1 |
| A19 | The same stocks: the cross's annual return less buy and hold's, at the 10th, 50th and 90th percentiles; the median share of days the cross was on | −10.96, −2.26 and +24.88 points; 60.4% | — | 5.1 |
| A20 | Stocks on which the cross returned more, by sub-period: 1999–2008; 2009–2017; 2018–2026 | 665 of 1,145 (58.1%); 224 of 1,157 (19.4%); 284 of 1,048 (27.1%) | — | 5.1 |

**What it allows a blueprint to say, and what it forbids.** The 50/200 cross carries a small
positive coefficient inside the pool at every horizon, and nothing in 2009–2017 at 21 and 63 days;
at 21 and 63 days the slower 100/300 reads higher than the 50/200 and the faster 20/100 lower, and
at 252 days the order breaks — a curve, not a cell to pick. The cross separates risk more than
return: forward volatility of 31.9% with the cross on against 43.1% with it off (A14), and on 99.7%
of stocks the cross moved less than holding (A17), while it returned more on only 39.8% (A16) — a
drawdown control, as `FINDINGS_1.md` prediction 2 found, not a return engine. Across every member
the traded-value rank points the way the liquidity notes say, the most traded earning less (A11);
inside the pool its sign turns with the period (A10), so no blueprint may predict its sign over the
window from this. Section 5.1 is a teaching measurement: cash earns nothing, no trade costs
anything, and no book is built.

---

<!-- example: end -->

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
| **1** | most-traded Core members in a golden cross, by traded value, no sector above half, 99.5% invested, monthly, a delisted name's cash put back on L+2 — flat 5 bp | 7.14% | 0.207 | −76.6% | 0.124 | **+0.083** | **falsified**: prediction 1 fails, 1 of 3 sub-periods; P1 fails; P2 fails at both cost rows, the rule above 14 of 20 random books at the flat row; P3 not evidenced; the sign-off is the owner's | Golden-Flow's claim 1, rejected inside the sector cap | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |
| 1 | the same, pre-registered costs | 5.58% | 0.143 | −81.5% | 0.102 | +0.040 | as above | | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |
| 1 | the same rule without the sector cap, flat 5 bp — the cap's own control | 7.31% | 0.202 | −78.9% | — | — | the cap holds as a risk limit: Sharpe within 0.005, volatility and drawdown lower capped | | [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) |
| 1, replaced version | the same rule, its band reinvesting to 99.5%, a delisted name's cash waiting for the month, run of 2026-11-18 — flat 5 bp | 7.13% | 0.206 | −76.6% | 0.127 | +0.079 | falsified on the same limb, 1 of 3 sub-periods; P1, P2, P3 fail; rewritten by the blueprint of `69aded0`, kept at the tag `experiment-1-reinvest-v2` | Golden-Flow's claim 1 | `JOURNAL_1.md`, 2026-11-18 |
| 1, replaced version | the same, pre-registered costs | 5.58% | 0.143 | −81.4% | 0.106 | +0.037 | as above | | `JOURNAL_1.md`, 2026-11-18 |
| 1, second pass | the same rule, its band leaving a kept name's shortfall in cash (mean invested 98.8%), run of 2026-11-17 — flat 5 bp | 7.17% | 0.209 | −76.2% | 0.124 | +0.086 | falsified on the same limb, 1 of 3 sub-periods; rewritten by the blueprint of `506d42f`, kept at the tag `experiment-1-sector-cap-v1` | Golden-Flow's claim 1 | `JOURNAL_1.md`, 2026-11-17 |
| 1, second pass | the same, pre-registered costs | 5.65% | 0.146 | −80.9% | 0.101 | +0.045 | as above | | `JOURNAL_1.md`, 2026-11-17 |
| 1, first pass | Golden-Flow's design replicated, no sector cap, 2000-01-03 to 2026-11-06, run of 2026-11-16 — flat 5 bp | 6.79% | 0.183 | −78.4% | 0.085 | +0.098 | superseded by the blueprint of `107768f`; kept as a row, as `AGENTS.md` asks of a rewrite | | `JOURNAL_1.md`, 2026-11-16 |

<!-- example: end -->

### Against the world

The same book measured against every benchmark it reports against, over one stated window.

**Does it reproduce?** Re-run from a wiped working copy and state the drift. A Sharpe moving in the
third decimal is the re-pull's rebasing, limitation 5 below, not a strategy change.

<!-- example: begin -->

The same book measured against every benchmark it reports against, over one stated window.

| Book, 1999-12-31 to 2026-10-30 | CAGR | Volatility | Sharpe | Max DD |
| --- | ---: | ---: | ---: | ---: |
| The rule, flat 5 bp | 7.14% | 24.60% | 0.207 | −76.6% |
| KN US Equity Core | 7.93% | 19.19% | 0.306 | −54.0% |
| `SPY` | 7.89% | 19.22% | 0.303 | −55.2% |

**Does it reproduce?** Yes: run again from a wiped working copy on 2026-11-20, Verify passed 39
checks, and the summary, sub-period, gate and tradeability tables and the four weight files came
out equal byte for byte. The twenty random books, priced on 2026-11-24, are not yet run from a
wiped copy.

<!-- example: end -->

### The trial count

**How many variants were ranked in each experiment, plus any excluded run**, published as item 3 of
the bar in `AGENTS.md` asks.

---

<!-- example: begin -->

**How many variants were ranked in each experiment, plus any excluded run**, published as item 3 of
the bar in `AGENTS.md` asks.

- **Experiment 1:** 359 books, as `BLUEPRINT_1.md` counts them — Golden-Flow's 152, the first
  pass's 45, the second pass's 46, the first rewrite's first draft's 46 (priced, never read: the
  engine ran out of cash), the replaced version's 46 and this version's 24: its four base books
  and the twenty random books, priced on the owner's word of 2026-11-24 after the result was seen.
  The run of 2026-11-20: 20 engine runs, all read; that of 2026-11-24: 40 more, 31 read and 9
  excluded by name. The window, the sector cap and its 50% were set after the first pass was seen,
  the band's reinvestment after the second, the top-up and the 100% after the replaced version,
  and the cash bound turned from a check into a report after this run, disclosed. The deflated
  Sharpe is not computed.

---

<!-- example: end -->

## What stands — reuse, do not rebuild

A result, a module or a method later work should start from rather than re-derive. One line each,
with its number.

<!-- example: begin -->

A result, a module or a method later work should start from rather than re-derive. One line each,
with its number.

- **The rule's sizing is the library's**: Portfolio Construction 2.1.0's proportional weights,
  then `Weights.cap_groups` by KN sector at 50% and `Weights.cap(0.20)`, equal
  `bounded_by_score_and_sector` on 646 book-dates, largest difference 1.4e-6
  (`Experiments/Experiment_1/library_sizing_check.csv`).
- **Every signal Experiment 1 reads is a Curator column**: `c_golden_cross_50_200` (and 20/100,
  100/300), `c_traded_value_sma_63d` (and 21, 126 days), `c_index_weight` and
  `c_eligible_golden_cross_50_200`, which agrees with membership and the cross at the prior close
  on all 711,569 name-dates. The KaxaNuk app charts what the rule reads.
- **A book struck to 99.5% invested**: `portfolio_construction.banded_book` with `invested`
  reinvests what the band's kept names leave, inside the name and sector caps; the rule's book
  holds 99.3% to 99.6% on every rebalance date.
- **A delisted name's cash put back in two days**: `portfolio_construction.delisting_top_up_dates`
  and `banded_book`'s `top_up_dates` pour it into the names held, inside both caps, buying nothing
  new and selling nothing priced; the rule's daily cash averages 1.49% at the pre-registered costs,
  6 days above 5% where the replaced version had 32.
- **Every Sharadar column is downloaded**, 87 of them, fundamentals by filing date, for later
  experiments.
- **Attribution from the engine's cache**: `Experiments/Experiment_1/attribute_base_books.py` runs
  section 5's three passes on the four base books already priced, at both cost rows, and on the
  rule and the uncapped arm by sub-period, and the factor model on the twenty random books, over
  the window and each sub-period; its first cut's benchmark reconciles with the Core
  within 0.22 points a year ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md),
  *What attribution says*).

<!-- example: end -->

## What is closed — do not re-propose without a new argument

Each rejected idea, with the number that rejected it. This list is what stops the next person
repeating it.

<!-- example: begin -->

Each rejected idea, with the number that rejected it. This list is what stops the next person
repeating it.

- **The golden cross alone, as a book to beat the index**: 0 of 8 sweep settings beat the Core on
  Sharpe at the flat row, uncapped (best 0.204 against 0.302) or capped (best 0.248 against 0.306,
  0.242 with the book filled to 99.5%).
- **The golden cross as the lever, inside a sector cap**: prediction 1 fails at both cost rows,
  the control beaten on both Sharpe and CAGR in 1 of 3 sub-periods, with the band's cash left
  (second pass) or reinvested (this version).
- **Reinvesting the band's cash as a lever**: 0.7 points more invested on average moved the rule's
  Sharpe from 0.209 to 0.206 at the flat row.
- **Putting a delisted name's cash back at once, as a lever**: it moved the rule's Sharpe from
  0.206 to 0.207 at the flat row. It is how a fund runs the book, not where the return comes from.

<!-- example: end -->

### The uncomfortable one

The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.

<!-- example: begin -->

The finding that qualifies the idea itself rather than a lever — the claim in `OBJECTIVE.md` that
turned out weaker than stated. Every honest project has one; write it here rather than letting it
sit in a findings file.

The cross earns its keep against its control over the window and not inside it: once the sector cap
stops the book riding a few large technology names, its margin over the control lives in
1999–2008 alone, and the book still loses to the index. Attribution, at both cost rows, says the
same from the other side: most of the rule's excess return is the market and its tilts, and once
the factors are stripped out its selection is −0.03 points (−0.01 at the flat row), against +19.79
for the control. Against twenty random books drawn from the control's members and sized the same
way, its idiosyncratic return is above 14 at the flat row, two short of the blueprint's 16; only
in 2018–2026 is it above nearly all of them, 19 of 20, a third singled out after it was seen
([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), *What attribution says*).

<!-- example: end -->

## Open leads, ranked

The single highest-value run outstanding, and what it would settle. Then the next.

<!-- example: begin -->

The single highest-value run outstanding, and what it would settle. Then the next.

1. **What 2018–2026's selection is: the golden cross, the traded-value ranking, or both.** There
   the rule's idiosyncratic return, +137.41 at the flat row, is above 19 of 20 random books, whose
   median is +20.37; over the window it is above 14, and P2 fails. Each random draw replaces the
   cross and the ranking together. Random books drawn from the names in a golden cross alone,
   sized the same way, would isolate the ranking: a new arm, counted as trials, and a new
   experiment, since Experiment 1's rules are frozen
   ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), *What attribution says*).

<!-- example: end -->

## Excluded runs

Variants removed from the tables above, each by name with its reason, rather than reported with a
caveat. **A metric computed over a truncated or rejected run does not belong in the same column as
a complete one.**

| Variant | Why |
| --- | --- |
| | what went wrong, how it was caught, and what now prevents it |

<!-- example: begin -->

Variants removed from the tables above, each by name with its reason, rather than reported with a
caveat. **A metric computed over a truncated or rejected run does not belong in the same column as
a complete one.**

| Variant | Why |
| --- | --- |
| Experiment 1, this version, run of 2026-11-24, nine runs — at the pre-registered costs random books 02, 05, 07, 09, 13, 16, 17, 19 and 20 | **Truncated**: the engine stopped valuing with a "Cash error", in 2000 or in the autumn of 2008, caught by Verify's count of valued days against the window's. Listed in `Experiments/Experiment_1/Backtest/excluded_runs.csv`; at the flat row all twenty are whole |
| Experiment 1, this version at 100% invested, run of 2026-11-19 — the rule at the pre-registered costs and its 1999–2008 sub-period | **Truncated**: "Cash error" on 2008-07-01; every book struck 99.5% instead, the fallback the blueprint named, and nothing of the 100% run read (`JOURNAL_1.md`, 2026-11-19) |
| Experiment 1, replaced version, run of 2026-11-18, eleven runs — at the pre-registered costs random books 02, 05, 07, 09, 10, 13, 16, 19 and 20; at the flat row random book 10; the control at $100,000 | **Truncated**: the engine stopped valuing with a "Cash error", caught by Verify's count of valued days against the window's. Listed in `Experiments/Experiment_1/Backtest/excluded_runs.csv` |
| Experiment 1, second pass, run of 2026-11-17, twenty-one runs — at the pre-registered costs all twenty random books and the 20/100 cross | **Truncated**: the engine stopped valuing at a rebalance, caught by Verify's count of valued days against the window's |
| Experiment 1, the rewrite's first draft, run of 2026-11-17, all 104 runs — 55 of them out of cash, the rule's included | **Not read**: the book at 100% with a 0.5% reserve; the blueprint was amended before any result was read (`JOURNAL_1.md`, 2026-11-17) |
| Experiment 1, first pass, run of 2026-11-16, twenty-four runs — at the pre-registered costs random books 01–08 and 10–20, the 21-day traded-value setting, the 20/100 cross, and the rule and the control at $100,000; at the flat row random book 12 | **Truncated**, as above; the same twenty-four as Golden-Flow's run of 2026-11-08 |

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

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**

<!-- example: begin -->

| # | Limitation | Effect |
| --- | --- | --- |
| 1 | **Nothing is out of sample** until a frozen book has days on paper after its freeze | Every number here is in-sample, and in-sample selection is what the deflation literature warns about |
| 2 | **A control arm differing in exactly one thing**, item 9 of the bar in `AGENTS.md`, is missing from any experiment that claims a margin | Which lever earned that margin is inferred from per-lever rows, not measured |
| 3 | Classification buckets use today's labels, not point-in-time | Anything reclassified mid-window is misattributed before its move — the `current_*` prefix marks exactly this |
| 4 | A delisted holding is sold at its last price | The engine books the sale on Sharadar's last trade, often over the counter, a venue the account may not reach |
| 5 | Curator output is not reproducible across download dates | Dividend adjustment is computed from the present, so a re-pull rebases every adjusted column |
| 6 | The Deflated Sharpe Ratio has never been computed | The one number that would say whether a winner survives its own trial count |
| 7 | The engine buys whole shares at the dividend-and-split-adjusted price | A name split in reverse later looks dear in the past and can be left unbought: CHKAQ left a point of the rule's book in cash for a month at a time, 33 days above the 3% bound at the flat row |

> **Under the bar in [`AGENTS.md`](AGENTS.md), most numbers above are a reason to run an experiment
> rather than a result.**

<!-- example: end -->
