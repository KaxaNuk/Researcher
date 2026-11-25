---
name: alpha-decomposition
description: >
  Load this skill when a KaxaNuk Investment Lab strategy beats its benchmark and the question
  becomes "is the signal doing anything, or is this a factor exposure wearing the signal's name?".
  Use it to read Attribution Analysis output in two layers and a third pass — Brinson-Fachler, the
  factor model, Brinson-Fachler again on the residual — to decompose idiosyncratic return into
  selection, sizing and timing by building counterfactual books the Backtest Engine can price, to
  run the exclusion-filter test when the factor model is blind to an absolute rule, and to evidence
  the gate's performance criterion P2. It does NOT run the engine or the attribution library for
  you — it says which books to price and how to read the numbers that come back. Shaping the
  attribution library's inputs and calling it is `attribution-analysis-runs`; pricing a book is
  `backtest-engine-runs`.
metadata:
  version: 0.5.0
---

# Alpha decomposition — is the signal doing anything?

A book that beats its benchmark has not been understood. It has been observed. This skill is the
procedure that turns "the book went up" into "here is the part of the return that is the idea, and
here is the part that is beta, size, sector and luck". That is the question `RESULTS.md` has to
answer before a strategy can graduate, and one this stack can actually answer because step 6
exists.

The method is Paleologo's (*Advanced Portfolio Management*, 2021, chapter 8): split total return
into factor and idiosyncratic, then split the idiosyncratic part three ways **by counterfactual
books, never by formula**. The book is listed in Part 0 of the template's
`Bibliotheca/BIBLIOGRAPHY.md` as provenance, not as a note; write its note before citing it in a
findings file. Every counterfactual below is a weight file, so the same
`Experiments/backtest_engine.py` that priced the real book prices it, over the same window, at the
same costs. When a counterfactual is attributed as well, the attribution reads *its* daily weights
from *its* backtest, never the real book's.

Work in the experiment's notebook, section 5 or a section after it. Record every number in
`FINDINGS_N.md`, then `RESULTS.md`. Publish the count of counterfactuals run.

## 1. First, two layers and a third pass — read what step 6 reports

Step 6 says where a book's return came from; the return alone shows neither the process nor the
thesis behind it. Run both methodologies (the experiment notebook's attribution cell does this) and
record:

| Layer | From | Numbers to record | The question it answers |
| --- | --- | --- | --- |
| **First cut** | Brinson-Fachler | cumulative alpha; **allocation**, **selection**, **interaction** | is the return the groups the book leans into, or the names it picks inside them? The exact lever that moved |
| **Second layer** | the factor model | total excess; **factor** contribution by factor — beta, size, value, momentum, residual volatility, liquidity, industries — and the **idiosyncratic** residual | which systematic premia paid, on purpose or by accident? How much of this is a factor fund wearing the strategy's name? |
| **Third pass** | Brinson-Fachler on the residual | allocation and selection of the return left after factor exposure is stripped | does the selection story survive — and would the Sharpe survive once that factor turns? |

The third pass is what the first cut alone cannot give: a book that looks like skilful stock-picking
in Brinson-Fachler can be a persistent low-beta or momentum tilt that happened to pay over the
sample. The attribution library does not run Brinson-Fachler on residual returns directly, so build
the residual series from the factor model's output: `calc_pct_area()` names it `f_idio_returns`,
`cummulative_pct_decomp()` names it `idio_returns`. Run the first cut on it in the notebook, and
say in `FINDINGS_N.md` that it was done that way. Getting those tables out at all is
`attribution-analysis-runs`.

**Know what the library calls allocation.** On 0.2.0, KaxaNuk's Attribution Analysis computes the
three effects **per asset and per date** — its methodology page gives the formulas, and
`attribution-analysis-runs` repeats them — not by group; the worked example, on 0.5.0, runs the
textbook formula by KN sector, the book's cash a segment of its own. An allocation number is a
statement about groups only when the effects were computed by group; `FINDINGS_N.md` says which was
run, and whether its cumulative figures are summed daily effects or linked, compounded ones.

**Check the benchmark is whole and aligned before reading any of it.** The first cut prices only
the securities the book's weight file names, so a book that lists only its holdings is compared
with the part of the index it owns. In the run that proved it, that part was 6% of the index's
return, with alpha five times too large and the excess filed under interaction. And a weight struck
at a day's close earns the next day's return, the close of t−1 earning day t: paired with its own
day, every pass reads larger — in the worked example's earlier Experiment 1, on Attribution
Analysis 0.2.0, an idiosyncratic return of 61.02 points against the 13.84 that stood. Compare the
first cut's `benchmark_returns` with the index's own
return over the same window; if they are not close, the book was not widened to every constituent
or not held overnight (`attribution-analysis-runs`, section 3) and no row of the table can be read
yet.

Two readings, both of which count as answers:

- **Allocation ≈ 0 with selection and interaction positive**, on inputs aggregated to groups, means
  a large group tilt is *not* where the money comes from. Say so plainly; it is the opposite of what
  the tilt makes a reader assume.
- **A roughly even factor / idiosyncratic split** is a *pass with a qualification* on the gate's
  performance criterion P2.
  There is real idiosyncratic alpha, and half the excess is exposure available more cheaply
  elsewhere. Report both halves with equal weight.

State the attribution window beside the backtest window — it is bound by factor-file coverage and
benchmark-holdings start, and is usually shorter. Record how many factor files the run used;
attribution numbers are only comparable across runs when the factor set is identical.

## 2. When the factor model is blind — the absolute-versus-relative problem

**Momentum in a factor model is relative**: a name ranked against its peers. **A trend or regime
rule is absolute**: a name against its own history. The two produce different books from the same
names, and a factor model built on the relative kind is close to invisible to an absolute rule. So a
strategy can beat every benchmark while the model assigns roughly nothing to the factor its thesis
is named after.

**That is a finding, not a failure**, and it is the expected state for any threshold signal — a
moving-average cross, a breakout, a regime label, a drawdown gate. When you see it:

1. Say so in `FINDINGS_N.md`, in those terms.
2. Do not conclude the signal is weak. Conclude the model cannot see it, and go to section 4.
3. Rename the pillar in `OBJECTIVE.md` if it is called "momentum" and is a trend rule. The
   distinction predicts which factor model will see the strategy and which will not.

## 3. Then, the idiosyncratic part three ways — counterfactual books

Before any of them: **drop economically insignificant positions** from both the real book and the
counterfactuals, or the comparison is dominated by residual slivers nobody was betting on.

Each counterfactual keeps everything about the real book except one thing. The Sharpe difference
between the real book and the counterfactual, over the same engine window, is that one thing's
contribution. All three read the objects the experiment notebook already has: `REBALANCE_DATES`,
`target_weights`, and the eligibility matrix the rule built them from, lagged as the rule lagged it
and called `eligible_matrix` below. Under a no-trade band, strike each counterfactual's targets
under the same band, as the rule's `struck_weights` were, so the band is no difference between
them. Price each new book the way the worked example's notebook prices its arms:
`securities_panel.expand_to_identifiers`, then `backtest_engine.write_weight_file` under a name of
its own, then `backtest_engine.price_books` with the real book's window and costs, which prices
them in the engine's batch mode, each answer cached under its weight file and settings. A run the
engine stopped early is excluded by name, and a reading that needs it is "not evidenced".

### 3a. Sizing skill — equalise positions within each date

Same names, same dates, every held position at equal weight. Side and gross unchanged.

```python
held_positions = target_weights > 0
held_counts = held_positions.sum(axis=1)
held_indicator = held_positions.astype(float)
equal_weights = held_indicator.div(held_counts, axis=0)
sizing_counterfactual = equal_weights.fillna(0.0)
```

**Sharpe(real) − Sharpe(equal-weighted) is what sizing contributed.** Positive means the big
positions were the good ones. This is the cheapest counterfactual and often already exists: an
equal-weight variant in the same experiment *is* this book — and for a benchmark that is already
equal weight, sizing skill is zero by construction and should be reported as such.

### 3b. Selection skill — a random draw from the eligible pool at the same sizes

Same dates, same number of names, same weight vector — but the names are drawn at random from
what was eligible that day. Repeat K times (`draw_count`); K is a trial count and is published.

```python
random_generator = numpy.random.default_rng(seed)
random_books = []
for draw_number in range(draw_count):
    drawn_rows = []
    for rebalance_date in REBALANCE_DATES:
        real_row = target_weights.loc[rebalance_date]
        real_sizes = real_row[real_row > 0]
        size_values = real_sizes.to_numpy()
        descending_sizes = numpy.sort(size_values)[::-1]
        eligible_row = eligible_matrix.loc[rebalance_date]
        eligible_names = eligible_row.index[eligible_row]
        picked_names = random_generator.choice(
            eligible_names,
            size=real_sizes.size,
            replace=False,
        )
        drawn_row = pandas.Series(
            descending_sizes,
            index=picked_names,
            name=rebalance_date,
        )
        drawn_rows.append(drawn_row)
    drawn_frame = pandas.DataFrame(drawn_rows)
    widened_frame = drawn_frame.reindex(columns=target_weights.columns)
    random_book = widened_frame.fillna(0.0)
    random_books.append(random_book)
```

Price every draw. **The real book's percentile among the K random books is the selection skill**;
the mean random Sharpe is what the eligibility rule plus the sizing scheme earn *without* picking.
Report the percentile and K, as a permutation test reports a p-value.

### 3c. Timing skill — the same names with entry dates shifted

Same selections, same weights, every re-strike moved by a fixed lag (5, 21 days) or to a random
date inside a window around the real one. If moving the entries costs nothing, the rule has no
timing skill — it is a selection rule that happens to fire on some day.

```python
shifted_dates = REBALANCE_DATES + pandas.tseries.offsets.BDay(lag)
timing_counterfactual = target_weights.set_axis(shifted_dates)
```

Clip to trading days that exist in the panel and drop any shifted date past the sample's end.

### Reading the three together

| Counterfactual | Sharpe gap to the real book | Reading |
| --- | --- | --- |
| equal-weighted | small positive | sizing helps a little — say "a little", in Sharpe |
| random draw (mean) | large positive | the names matter; the rule is selecting, not just filtering |
| random draw (mean) | ≈ 0 | the eligibility filter plus sizing is the whole strategy |
| shifted entries | ≈ 0 | no timing skill; do not claim any |

Sizing plus selection plus timing does not have to sum to the idiosyncratic return — the
counterfactuals overlap. They are three questions, not a partition.

## 4. The exclusion-filter test — the counterfactual for an absolute rule

The direct test of whether a threshold signal earns its keep, and the fallback when section 2
applies: **the same book with the signal switched off.**

```python
# the rule's eligibility with only the signal's condition dropped; in the worked example
# `eligible & (trend_before > 0)` loses its last term, which is `target_book(use_cross=False)`
eligible_without_signal = tradable_matrix                               # signal removed
# then re-run the experiment's own selection and weighting on this eligibility matrix
```

Same ranking column, same holding count or the bounds that set it, same weighting, same trigger —
only the eligibility condition changes. Price both. **Sharpe(with signal) − Sharpe(without) is what
the signal contributes as a filter**, which a factor model cannot measure.

**What a null result means.** If the two books are close, the signal is not adding beyond the
sizing rule's own selection, and the honest description of the strategy is "top-N by the sizing
column". That is worth knowing and belongs in `OBJECTIVE.md` as a falsified claim.

## 5. The worked example — `us-golden-flow`

The KaxaNuk Strategy Template works one strategy through the process in its worked example,
`examples/strategy/us-golden-flow/` in `KaxaNuk/Researcher`, which `init-example` copies into a
folder of its own. Its strategy, **US-Golden-Flow**, owns once a month the KN US Equity Core
members whose 50-day simple moving average is above the 200-day, ranked and weighted by 63-day
traded value, none above 20%, none below 1% and no KN sector above half the book, a held name left
alone when its target moved by half a point or less. Steps 1 to 6 have run, and the experiment is
**falsified as its blueprint words it**: the cross beats its control over the window but in only
one of three sub-periods, and the book loses to its index. So the numbers below are measured, not
made up for illustration: the example's in-sample backtest over 1999-12-31 to 2026-10-30, priced by
the engine at the flat 5 bp half-spread the gate is read at, and attributed by Attribution Analysis
0.7.0 over 2000-01-03 to 2026-10-30 — Brinson-Fachler by KN sector, every cumulative effect linked,
in points of compounded return over the bill — as reported in
`Experiments/Experiment_1/FINDINGS_1.md`; hypothetical, never traded.

| Arm | What it removes | CAGR | Sharpe | **Idiosyncratic** |
| --- | --- | ---: | ---: | ---: |
| The rule | — | 7.14% | 0.207 | **+58.67** |
| The control | the golden cross | 5.53% | 0.124 | **+29.91** |
| Equal weight | traded-value sizing | 5.30% | 0.145 | **−29.77** |
| Random, twenty seeds | the cross and the ranking together | — | — | **−97.01 to +161.79**, median +16.88 |

What the arms teach this skill:

- **The control prices a filter whatever the model shows.** The golden cross adds +0.083 of Sharpe
  and +1.62 points of CAGR over the control, with a maximum drawdown of −76.6% against −89.8%. In
  the factor model the rule carries less negative beta than the control, −130.06 against −146.39,
  and less momentum, +42.75 against +52.37: the exclusion-filter test of section 4 measured what
  the factor split does not show. Read the arms, not the name, before saying what a signal does.
- **A positive residual is not yet selection.** The rule's +58.67 is above 14 of the 20 random
  books, short of the gate's 16, and the random books' own residuals run from −97.01 to +161.79.
  Alpha is the residual's *expected* value: read it against the random books, never by its level.
  Each draw replaces both the cross and the ranking, so section 3b credits the two together; no arm
  isolated the ranking.
- **Sizing is measured here, not assumed.** Traded-value weighting against the same names equally
  weighted: 0.207 against 0.145 of Sharpe, +58.67 against −29.77 idiosyncratic. A rule that weights
  equally across whatever passes its screen has sizing skill zero by construction — report it as
  zero, not as a finding.
- **Timing was never priced, and the findings say so.** No shifted-entry arm was run, so section 3c
  reports nothing. An arm you did not run is reported as not run, never inferred from the ones you
  did.
- **Read the sub-periods, not only the window.** The rule beats its control on both Sharpe and
  CAGR in 1999–2008 only, which is why the experiment is falsified. Its residual is above 19 of the
  20 random books in 2018–2026 and below most of them in 1999–2008: a decomposition that read the
  whole window alone would miss both. A period singled out after it was seen is information, never
  the test.
- **Four fifths of the holdings' return is factor exposure.** Of 314.81 compounded points over the
  bill, 256.14 are factors — the market 351.16, technology +63.86, momentum +42.75 the largest
  style, beta −130.06 — and 58.67 idiosyncratic. Report both parts, as section 1 asks.
- **By sector, interaction offsets the bets**: allocation −57.33, selection −102.82, interaction
  +76.59 in the first cut — the book is heavier where its picks did better — and the third pass's
  selection is −0.01. A positive idiosyncratic return beside a negative selection is not a
  contradiction: the two layers ask different questions. Say so beside any selection figure.

## What this skill will not let you do

- **Call a strategy understood on the factor split alone.** The split says how much is
  idiosyncratic; the counterfactuals say what the idiosyncratic part is made of.
- **Run one random draw.** K is a trial count. Publish it, and report the percentile, not the best
  draw.
- **Tune on the counterfactuals.** They measure the rule you stated in `BLUEPRINT_N.md`. A rule
  changed to look better against its own counterfactual is a new experiment with a new blueprint.
- **Quote a number that did not come from the engine.** Every counterfactual is priced by
  `backtest_engine.run_backtest` over the shared window, never approximated.
- **Use a live KaxaNuk strategy as a worked example.** Examples in this package come only from
  `us-golden-flow` as the package ships it, never from a live strategy repository.
