---
name: alpha-decomposition
description: >
  Load this skill when a KaxaNuk Investment Lab strategy beats its benchmark and the question
  becomes "is the signal doing anything, or is this a factor exposure wearing the signal's name?".
  Use it to read Attribution Analysis output in two layers and a third pass — Brinson-Fachler, the
  factor model, Brinson-Fachler again on the residual — to decompose idiosyncratic return into
  selection, sizing and timing by building counterfactual books the Backtest Engine can price, to
  run the exclusion-filter test when the factor model is blind to an absolute rule, and to evidence
  graduation criterion 2. It does NOT run the engine or the attribution library for you — it says
  which books to price and how to read the numbers that come back. Shaping the attribution library's
  inputs and calling it is `attribution-analysis-runs`; pricing a book is `backtest-engine-runs`.
metadata:
  version: 0.4.4
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

**Know what the library calls allocation.** KaxaNuk's Attribution Analysis computes the three
effects **per asset and per date** — its methodology page gives the formulas, and
`attribution-analysis-runs` repeats them — not by group. An allocation number is a statement about
groups only when the inputs were aggregated to groups first; `FINDINGS_N.md` says which was run.

**Check the benchmark is whole and aligned before reading any of it.** The first cut prices only
the securities the book's weight file names, so a book that lists only its holdings is compared
with the part of the index it owns. In the run that proved it, that part was 6% of the index's
return, with alpha five times too large and the excess filed under interaction. And a weight struck
at a day's close earns the next day's return, the close of t−1 earning day t: paired with its own
day, every pass reads larger — in the worked example, an idiosyncratic return of 61.02 points
against the 13.84 that stands. Compare the first cut's `benchmark_returns` with the index's own
return over the same window; if they are not close, the book was not widened to every constituent
or not held overnight (`attribution-analysis-runs`, section 3) and no row of the table can be read
yet.

Two readings, both of which count as answers:

- **Allocation ≈ 0 with selection and interaction positive**, on inputs aggregated to groups, means
  a large group tilt is *not* where the money comes from. Say so plainly; it is the opposite of what
  the tilt makes a reader assume.
- **A roughly even factor / idiosyncratic split** is a *pass with a qualification* on criterion 2.
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
contribution. All three read the objects the experiment notebook already has: `selected_matrix`,
`REBALANCE_DATES`, `target_weights`, and the eligibility matrix the rule built them from, lagged as
the rule lagged it and called `eligible_matrix` below. Price each new `target_weights` the way the
worked example's notebook prices its arms: `securities_panel.expand_to_identifiers`, then
`backtest_engine.write_weight_file` under a name of its own, then `backtest_engine.price_books`
with the real book's window and costs, which runs `build_configuration` and `run_backtest` for
each.

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
# `eligible & (trend_before > 0)` loses its last term, which is `daily_book(use_cross=False)`
eligible_without_signal = tradable_matrix                               # signal removed
# then re-run the experiment's own selection and weighting on this eligibility matrix
```

Same ranking column, same holding count or the bounds that set it, same weighting, same trigger —
only the eligibility condition changes. Price both. **Sharpe(with signal) − Sharpe(without) is what
the signal contributes as a filter**, which a factor model cannot measure.

**What a null result means.** If the two books are close, the signal is not adding beyond the
sizing rule's own selection, and the honest description of the strategy is "top-N by the sizing
column". That is worth knowing and belongs in `OBJECTIVE.md` as a falsified claim.

## 5. The worked example — `golden-flow`

The KaxaNuk Strategy Template works one strategy through the process in its worked example,
`examples/strategy/golden-flow/` in `KaxaNuk/Researcher`, which `init-example` copies into a
folder of its own. Its strategy, **Golden Flow**, owns the KN US Equity Core members whose 50-day
simple moving average is above the 200-day, ranked and weighted by 63-day traded value, none above
20% and none below 1%, re-struck only when the held set changes. Steps 1 to 7 have run: criteria 1
to 4 of the gate passed, and the book was signed into paper trading on 2026-10-06. So the numbers
below are measured, not made up for illustration: the example's in-sample backtest, priced by the
engine and attributed by Attribution Analysis over 2015-01-02 to 2026-06-01, and reported in
`Experiments/Experiment_1/FINDINGS_1.md`; hypothetical, never traded.

| Arm | What it removes | CAGR | Sharpe | **Idiosyncratic** |
| --- | --- | ---: | ---: | ---: |
| The rule | — | 20.33% | 0.842 | **+13.84** |
| The control | the golden cross | 19.73% | 0.763 | **−9.48** |
| Equal weight | traded-value sizing | 14.53% | 0.722 | **−30.03** |
| Random, twenty seeds | the cross and the ranking together | 6.55% to 15.76% | 0.330 to 0.782 | **−84.50 to −3.77** |

What the arms teach this skill:

- **The signal the book is named after cuts beta.** Against the control, the golden cross more
  than halves the beta exposure, 10.39 points against 22.15, and turns the idiosyncratic return
  from −9.48 to +13.84: the control earns more from factors and loses it in the residual. Read the
  arms, not the name, before saying what a signal does.
- **The control prices a filter whatever the model shows.** Here the cross shows in the factor
  model as that cut in beta, with a little momentum added — the model is not blind to it, so
  section 2's case stays as theory in this example. The exclusion-filter test of section 4 answers
  either way: +0.080 of Sharpe and +0.60 points of CAGR over the control.
- **The rule beats every random book, for two reasons at once.** Its +13.84 is above all twenty,
  every one of them negative. Each draw replaces both the cross and the ranking, so section 3b
  credits the two together; no arm isolated the ranking.
- **Sizing is measured here, not assumed.** Traded-value weighting against the same names equally
  weighted: 0.842 against 0.722 of Sharpe, +13.84 against −30.03 idiosyncratic. A rule that weights
  equally across whatever passes its screen has sizing skill zero by construction — report it as
  zero, not as a finding.
- **Timing was never priced, and the findings say so.** No shifted-entry arm was run, so section 3c
  reports nothing. An arm you did not run is reported as not run, never inferred from the ones you
  did.
- **Read the sub-periods, not only the window.** Over the window the rule beats its control on
  return and on Sharpe, with a drawdown 13.85 points shallower, and it loses 2023 to 2026 by 11.4
  points a year. A filter can as well lose on return and win on Sharpe; a decomposition that read
  return alone, or the whole window alone, would misjudge either.
- **Nine tenths of the excess return is factor exposure.** Of the factor model's 137.35 points,
  123.50 are factors, 88.10 of them the market, and 13.84 idiosyncratic: a market-and-trend book
  with a thin residual edge. Report both parts, as section 1 asks.
- **Interaction, not selection, carries most of each Brinson-Fachler pass**: 77.05 of 96.87 points
  in the first cut, 40.67 of 43.71 in the third. Per asset, heavy weights in names that then rose
  are not split cleanly into choosing and sizing; say so beside any selection figure.

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
  `golden-flow` as the package ships it, never from a live strategy repository.
