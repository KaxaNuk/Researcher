# Blueprint — Experiment 1

> **The hypothesis, fixed once written.** Thesis, the claim it moves, rules, predictions, success
> criteria, what would falsify it and key risks, recorded *before* any code runs.
>
> **This file does not change when results arrive.** A hypothesis edited after its test is no longer
> a hypothesis — that is the whole reason it is kept apart from the result. What the experiment
> actually produced is in [`FINDINGS_1.md`](FINDINGS_1.md); the running log, the thinking
> before this blueprint included, in [`JOURNAL_1.md`](JOURNAL_1.md).
>
> In a new strategy, record the date it was written and delete this blockquote.

---

<!-- example: begin -->

> **The hypothesis, fixed once written.** Thesis, the claim it moves, rules, predictions, success
> criteria, what would falsify it and key risks, recorded *before* any code runs. What the
> experiment produced is in [`FINDINGS_1.md`](FINDINGS_1.md); the running log, the thinking before
> this blueprint included, in [`JOURNAL_1.md`](JOURNAL_1.md).

---

## Experiment 1 — the most-traded KN US Equity Core members in a golden cross, by traded value, no sector above half, fully invested, monthly, a delisted name's cash put back in two days

**Rewritten 2026-11-19, before this version was run.** It **replaces the blueprint of 2026-11-18**
(commit `506d42f`; its run and findings at `433514b`, kept at the tag `experiment-1-reinvest-v2`),
whose run reported on 2026-11-18 — falsified on prediction 1's sub-period limb — and was seen
before this file was written. That run is kept as a row of `RESULTS.md`, and its books count in the
trials. **The hypothesis, the predictions and the falsifier are that version's, word for word**
(the owner: "sigue siendo la misma hipotesis"); **what changes is how the book is run, on the
owner's words of 2026-11-19** ("si hay cash que viene por delistings entonces ese día tenemos que
rebalancear con ese cash de manera eficiente", "tener 1% constante en cash seria lo ideal", "todo
en el experimento 1"): **a delisted name's cash is put back into the names held two trading days
after its last price; every book is struck 100% invested, the engine keeping its 1% reserve; and
only the four base books are priced** ("solo corre los 4 portafolios base y sus respectivos
backtests"). The top-up was read back on UST, 2009-01-07, and the owner said "Yes, run it"
(`JOURNAL_1.md`, 2026-11-19), before this file. Everything below is the replaced version's but for
the title, this paragraph, the band's 100%, the top-up, the cash, the rebalance dates, the scope,
the trial count, the Verify bound and the disclosures.

**The version before it was rewritten 2026-11-17, before it was run.** It **replaces the
blueprint of 2026-11-16**
(commit `107768f`, kept at the tag `experiment-1-sector-cap-v1`), whose run reported on 2026-11-17
— falsified on prediction 1's sub-period limb — and was seen before this file was written. That
run is kept as a row of `RESULTS.md`, and its books count in the trials. **What changes, on the
owner's words of 2026-11-17** ("no arma estos cambios en el experimento 1", "que nuestro target sea
tener 0.5% en cash", "0.5% in total"), and nothing else: **the band reinvests** what its kept names
leave of the book. The rewritten rule was read back on 2026-09-01 and 2026-10-01 and the owner said
"Yes, run it" (`JOURNAL_1.md`, 2026-11-17), before this file. **Amended 2026-11-18, before any
result was read:** the first draft of this rewrite (commit `149aa3c`) filled every book to 100%
with a 0.5% engine reserve, and the engine ran out of cash for costs in 55 of its 104 runs, the
rule's included, so nothing of it could be read (`JOURNAL_1.md`, 2026-11-17). The owner then
chose "Book 99.5%, reserve 1%": the band fills each book to **99.5%**, the engine keeps its
**1%** reserve, as in the replaced version. Everything below is the replaced version's but for
the band, the cash, the trial count and the disclosures.

**The replaced version was written 2026-11-16, before the rule cell held a line of it.** KaxaNuk Researcher
1.37.1 (template 0.22.1), Data Curator 0.51.0, Backtest Engine 0.68.0, Attribution Analysis 0.7.0,
Portfolio Construction 2.1.0.

**This version adapts Golden-Flow's Experiment 1** — its `BLUEPRINT_1.md` of 2026-10-23, commit
`887b695` in that repository — whose rule, predictions and bar it keeps, and whose sources it cites
from there; this repository holds no notes of its own yet. **It replaces this repository's first
pass of 2026-11-16**, Golden-Flow's rule replicated unchanged on 2000-01-03 to 2026-11-06, whose
results were seen before this file was written (`JOURNAL_1.md`, 2026-11-16): that pass is kept as a
row of `RESULTS.md`, and its books count in the trials. **What changes, on the owner's words of
2026-11-16:** a 50% cap on each KN sector; the golden cross as a 1/0 column and a point-in-time
eligible flag; every column Sharadar serves, downloaded once for later experiments; the window
1999-12-31 to 2026-10-31. That rule was read back on 2026-09-01 and 2026-10-01, and the owner's
yes came on 2026-11-17, after its run.

<!-- example: end -->

## Experiment 1 — the first rule against the benchmark

### Thesis

One paragraph: what book this rule produces, why it should beat the benchmark
`JOURNAL_1.md` chose, and why it is also a fair yardstick — sensible, liquid, low-complexity
— for judging whether any later idea adds value. **Be modest on purpose.** A first rule does not
assert its signal is the best of its kind, only that it is simple enough to be understood, liquid
enough to be traded, and stable enough to measure other things against.

<!-- example: begin -->

Once a month, own the KN US Equity Core members the market trades most while their fifty-day
average sits above their two-hundred-day one, each in proportion to what it trades, none above a
fifth of the book, **no sector above half of it**, none below a hundredth, and leave alone what
barely moved.

**The economic reason for the cross is Golden-Flow's**: a risk gate that also pays in compound
return — a name falling through its averages is one the market is selling, and leaving it cuts
the drawdowns a book of the most traded names rides through. Its evidence and its sources are in
Golden-Flow's blueprint, *Thesis*.

**The reason for the sector cap is concentration.** Ranking by traded value piles the book into
whichever sector the market trades most: on 2026-10-01 the uncapped rule held 79% technology, and
in the eight trading days after 2026-10-27 it lost 16.7% while the Core lost 4.3%, in a
semiconductor sell-off (`FINDINGS_1.md` of the first pass, *What moved*). A half-book cap keeps the
signal's ranking inside each sector and spreads the rest over the next most traded names, so one
sector's crash cannot take most of the book. It is a risk limit, not a source of return: the claim
is that it lowers volatility and drawdown, not that it raises the Sharpe.

**It asserts nothing about being the best trend rule**, nor the best cap: 50% is the owner's
number, never tuned.

<!-- example: end -->

### The claim this moves

Which claim of `OBJECTIVE.md`, by number, this experiment exists to move, the status it reaches if
the predictions below hold, and the one it reaches if they fail. **One claim.** An experiment that
could beat every benchmark and settle nothing is a measurement, not a test.

<!-- example: begin -->

**Claim 1, the signal** (Golden-Flow's `OBJECTIVE.md`; this repository's is not written yet):
holding only members in a confirmed uptrend makes a better book than the same rule without it. Its
test is prediction 1, read as Golden-Flow's blueprint reads it: confirmed as a book if prediction 1
and success criterion 1's benchmark limb hold; confirmed against its control only if the benchmark
limb fails; falsified if prediction 1 fails. **Claim 2, the sizing**, is prediction 3. **Claim 3,
the construction**, holds on the targets by construction — no target above 20% or below 1%, no
sector above 50%, no name out of its uptrend — and the notebook reports how far the band lets a
struck weight sit outside them.

<!-- example: end -->

### Rules

- **Selection:** the eligibility condition, naming the column it reads.
- **Sizing:** the weighting scheme, and any bounds it sizes inside — a cap and a floor on each
  weight, and whether a capped name's excess goes to cash or to the other names. Named bounds are
  the design, and the control holds them too; every other constraint is switched off, a lever a
  later experiment has to earn.
- **Cash:** what the weights leave uninvested is cash, which the engine holds and pays interest
  on: name the rate file, the spread a broker keeps below it, and the cash reserve. The same rate
  is the risk-free rate of every Sharpe ratio the engine reports.
- **Costs, inside the engine:** commission in basis points of the notional; the slippage model and
  the half-spread it falls back on; and, registered now so it is never a forking path later, the
  flat half-spread every book is priced again at beside the model, a stress row and a small
  account. Then **what the cost model does not do**, by name.
- **Delistings and gaps:** a position whose prices stop is sold by the engine at its last price; a
  gap inside a series, which the engine cannot price, is a blocking row of the register, excluded
  by name from every book.
- **Timing:** calendar, or event-driven on a stated trigger. Say what happens between triggers,
  and name any no-trade band: how far a held name's target may move before it is traded, read
  back beside the rule in `JOURNAL_1.md` before this file is written.
- **Lag:** how many days between the signal and the fill, and what the engine adds on top.
- **Control:** the same rule with exactly one ingredient removed — name which — trading on this
  rule's own rebalance dates, so that the ingredient is the only difference. A control left to find
  its own dates differs in when it trades as well.
- **Screens deliberately absent**, and why each is redundant under the rules above.

<!-- example: begin -->

- **Universe:** the KN US Equity Core's members as of each date, from the desk's daily holdings
  (`Data/Curator/Benchmarks/`), keyed by Sharadar's ticker through the seed's two keys; the seed's
  2,203 listings keep the delisted.
- **Prices and data:** Sharadar, through Data Curator 0.51.0, from 1998-01-02 so the 200-day
  average exists on the window's first day, to 2026-10-31; one CSV per listing in
  `Data/Curator/Time_Series/`, with every column the Curator serves from Sharadar — prices,
  dividends, splits and quarterly fundamentals point in time by filing date — and `c_market_cap`.
  The rule reads none of the fundamentals: they are downloaded for later experiments. Every signal,
  return and mark reads `c_close_dividend_and_split_adjusted`.
- **Signal:** the golden cross as a 1/0 state, `c_golden_cross_50_200` in the Curator and
  `r_golden_cross_50_200` in the Refinery: 1 while the 50-day simple average of that close is above
  the 200-day, 0 otherwise, empty before the 200th day. Never tuned.
- **Eligible on a rebalance date d** — `r_eligible`, the book's point-in-time universe: a member at
  the close of the trading day before d, with the cross at 1 then, a traded value then, and an open
  price on d; not excluded by name.
- **Traded value:** `r_traded_value_sma_63d`, the 63-day simple average of the day's close times its
  volume, both split-adjusted, with the volume the provider adjusted twice corrected.
- **Sector:** the KN sector of the KN US Equity Factor Model, the classification attribution reads
  (`attribution_analysis.kn_sectors`): eleven sectors, one per security for the whole window, a
  name the model does not carry its own group, `unclassified`. **This is today's classification
  read into the past, a deliberate look-ahead**, as a `current_*` column is: a name reclassified
  inside the window is capped under its present sector before its move.
- **Rank and sizing:** names in order of traded value at the prior close, ties by name. A name is
  added if, sized with the names already in, no weight falls below **1%**; a name that fails is
  skipped and the next tried (under the name cap alone this is Golden-Flow's walk, to 1e-16).
  A book is sized by filling: each weight proportional to traded value, a name above **20%** held
  at it, **a sector above 50% scaled down to it**, what either frees spread over the names still
  free (`portfolio_construction.bounded_by_score_and_sector`). What no free name can take is cash.
- **Rebalance dates:** the first trading day of each month in the window, the window's first day
  included, for every book, **and the top-up dates below**.
- **The top-up:** when a held name's prices stop — its last price on day L, the engine selling it
  there — the book is topped up on the second trading day after L, the first on which the missing
  price is known at the prior close. **Only the freed cash moves**: it goes to the names the book
  still holds, in proportion to the book's own sizing (traded value at the prior close; equally in
  the equal-weight arm), into what each name has left under the 20% cap and each sector under the
  50% cap; every other held name keeps the weight it drifted to at the fill, and nothing is sold.
  What no held name can take is cash. Two delistings on the same day are topped up together; a
  top-up that falls on a monthly date is that date's rebalance.
- **The band:** a name held since the last rebalance and still in the target keeps the weight it
  drifted to when its target differs from that weight, at the close before d, by **0.5 points** or
  less. **Every other name in the target is traded, and the traded names share what the kept names
  leave of a book invested to 100%, in proportion to their targets**, inside the 20% name cap and the
  50% sector cap with the kept names counted; what no traded name can take is cash
  (`portfolio_construction.banded_book`). A traded name can therefore sit above its target, never
  above a cap. Every book that has a band, the controls and counterfactuals included, strikes this
  way, each under its own name cap and sector cap.
- **Cash:** what the caps leave and the engine's 1% reserve — every book struck 100% invested, by
  the owner's decision of 2026-11-19; **if any of the four base books stops with the engine's
  "Cash error", every book is struck 99.5% instead, the fallback named here before the run** — are
  US dollar cash at FRED's
  effective federal funds rate (`DFF`) less 0.5 points, floored at zero; the same rate is the
  risk-free rate of every Sharpe ratio.
- **The fill:** the open of d, dividend-and-split adjusted, a market-on-open order.
- **Delistings and gaps:** a held name whose prices stop is sold by the engine at its last price; a
  gap inside a series is a blocking row of `Universe/Data_Issues.csv`, excluded by name from every
  book.
- **Costs, inside the engine:** commission 1 basis point of the notional; slippage
  `spread_plus_impact`, Corwin–Schultz from the day's range, 5 bp where a range is missing;
  $1,000,000, integer shares, a 1% cash reserve. **Every book is priced again at a flat 5 bp**,
  the row Golden-Flow's owner chose to read the gate at. The stress row and the $100,000 row are
  not priced in this version. What the cost model does not do
  is Golden-Flow's list, *Rules*, *Costs*.
- **Window:** 1999-12-31 to 2026-10-31, the owner's. Attribution starts on the factor model's first
  day, 2000-01-03. Sub-periods: 1999-12-31 to 2008-12-31, 2009 to 2017, 2018 to 2026-10-31.
- **Control:** the same rule with the golden cross removed — every condition of `r_eligible` but the
  cross, the 200-day history kept — sized inside the same bounds, **the sector cap included**, the
  same band, cash, costs and delisting rule, **on the rule's own rebalance dates**: the monthly
  dates and the top-up dates of the rule and of the control together, so neither book waits a
  month on its own delisting's cash, and on a date where a book lost nothing it keeps what it
  drifted to.
- **The cap's own control:** the rule with the sector cap removed, everything else the same, on the
  monthly dates and its own top-up dates. **Equal weight**, the rule's names equally weighted
  inside the same caps, the same.
- **Scope, by the owner's decision of 2026-11-19:** four books — the rule, its control, equal
  weight and the uncapped arm — each at the pre-registered costs and the flat row, eight engine
  runs, and the sub-periods read from them.
- **Benchmarks:** the KN US Equity Core, then `SPY`.
- **Screens deliberately absent:** no risk model, no stop-loss, no valuation screen; the
  fundamentals downloaded are not read.

<!-- example: end -->

### What this experiment should show

**Predictions, fixed before the run.** Each cites a `Bibliotheca/` note or a section of
`Data/analyzer_marimo.py`, which measures the signal but builds no book. Getting these right is
worth more than a good Sharpe; getting them wrong is worth more than a bad one.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | what the book should do | a `Bibliotheca/` note, or the analyzer section and its number | the observation that would refute it |

Note anything you are watching but cannot predict, because nothing licenses a prediction about it.
Costs usually belong here.

<!-- example: begin -->

**Predictions, fixed before the run.** Rows 1 to 3 are Golden-Flow's, unchanged, with its sources;
row 4 is this version's. A lead is reported, not scored.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | **The golden cross earns its keep**: the book beats its control by at least +0.03 Sharpe and +0.5 points of CAGR over the window, and on both in at least 2 of the 3 sub-periods | Golden-Flow's blueprint, prediction 1; its first pass here held at the flat row (+0.098, +2.22, 2 of 3) and failed the sub-period limb at the pre-registered costs | either margin missed over the window, or the control beaten on both in fewer than 2 sub-periods |
| 2 | **The cross is a drawdown control**: the book's maximum drawdown shallower than its control's, its volatility lower | Golden-Flow's prediction 2 | either deeper or higher |
| 3 | **Weighting by traded value does not beat equal weight** by more than 0.03 Sharpe | Golden-Flow's prediction 3, which failed there and in the first pass here (+0.066 at the flat row); kept as written | the book's Sharpe above the equal-weight arm's by more than 0.03 |
| 4 | **The sector cap is a risk limit**: the capped book's volatility and maximum drawdown are both below the uncapped arm's, and its Sharpe within 0.03 of it either way | the read-back: technology 79% uncapped on 2026-10-01; the first pass's 16.7% loss in eight days of a semiconductor sell-off | the capped book's volatility or drawdown above the uncapped arm's, or its Sharpe more than 0.03 away |
| 5 | **Lead**: the book beats both benchmarks on Sharpe, net, over the window | Golden-Flow's lead 4 | counted as a lead |
| 6 | **Lead**: the selection beats chance, 16 of 20 random books — **not priced in this version** | Golden-Flow's lead 5 | counted as a lead |
| 7 | **Lead**: 20 to 60 names on most dates — 36 and 38 on the read-back dates — the sector cap binding on fewer than a quarter (17.6% of dates in the read-back) | the read-back | counted as a lead |
| 8 | **Lead**: tradeable by hand — a few dozen orders a date, one-way turnover under 2.5 a year | Golden-Flow's lead 7; the first pass's turnover was 2.15 | counted as a lead |
| 9 | **Lead**: most excess return is market and beta; technology's factor contribution smaller than the uncapped arm's — **not run in this version** | Golden-Flow's lead 8 | counted as a lead |
| 10 | **Lead**: the cash a fund would hold — the rule's daily cash at most 3% on every day but a delisting's L to its top-up, and near the 1% reserve on average | the owner's "1% constante", 2026-11-19 | counted as a lead; Verify raises on the 3% bound |

**Watched, not predicted:** how much of the uncapped arm's 2018–2026 margin over the Core the cap
gives up; 2009–2017, where the cross's rows are close to nothing.

<!-- example: end -->

### Success criteria

What the experiment has to show to count as a success, fixed now. At the least:

1. It beats the benchmark `JOURNAL_1.md` chose **and its own control** on risk-adjusted
   return, net, over the same window — performance criterion P1 of the gate in
   `Paper_Trading/BITACORA.md`.
2. Reproducible from a working copy whose data folders were emptied first, through the pipeline,
   with no manual step, every Verify passing — soundness criterion S5.
3. A tradeable trigger frequency — not a rule that fires every day.
4. Every prediction above evaluated explicitly in `FINDINGS_1.md`, **including the ones that turn
   out wrong.**

**Success is necessary for graduation, not sufficient.** The gate in `Paper_Trading/BITACORA.md`
decides it, in two layers — soundness, S1 to S5, then performance, P1 to P3 — and a person signs
it. Name here what will evidence each soundness row: the trial count and the sweep, the control
and the random books, the cost rows, the run from emptied data folders. A row without its evidence
does not hold, and a book whose soundness fails yields no conclusion at all.

<!-- example: begin -->

1. It beats the KN US Equity Core and `SPY` on Sharpe, net, over the window, **and its own control**
   as prediction 1 states.
2. Reproducible from a wiped working copy, through the pipeline, every Verify passing.
3. Tradeable and stated: orders a year, turnover, and every cost and the cash's interest as the
   engine priced them; orders under $1,000 at $100,000 are not priced in this version.
4. Every prediction and lead above reported in `FINDINGS_1.md`, **including the ones that turn out
   wrong.**

**Success is necessary for graduation, not sufficient**: the gate in `Paper_Trading/BITACORA.md`,
soundness S1 to S5 then performance P1 to P3, read as Golden-Flow's blueprint sets its margins —
P2 needs Brinson-Fachler selection, the idiosyncratic return and the residual selection above zero
and the book above 16 of the 20 random books; P3 needs at least 6 of the 8 sweep settings to keep
the sign of their margin over their own control on both Sharpe and CAGR, and all 8 to beat the Core
on Sharpe. A person signs it. **In this version P2 and P3 read "not evidenced"**: attribution,
the random books and the sweep are not run.

**Not priced in this version, by the owner's decision of 2026-11-19; the replaced version's are
that version's.** **The sweep, each with its own control on the rule's dates, the sector cap in
every one:** cap at
15% and 25%; floor at 0.5% and 2%; traded value over 21 and 126 days; the cross as 20/100 and
100/300. **The band at 0.25 and 1.0 points**, read on turnover and orders. **The counterfactuals:**
the rule's names equally weighted inside the same caps; twenty random books drawn from the
control's members, sized by traded value inside the same caps.

**The trial count: 339 books.** Golden-Flow's 152; the first pass here, 45, Golden-Flow's design
priced again on this data; the second pass's 46; the first rewrite's first draft, 46, which the
engine could not price whole and of which nothing was read; the replaced version's 46; and this
version's 4 — the rule, its control, equal weight and the uncapped arm. The cost rows and
sub-periods re-price books and add none. **The window, the sector cap and its 50% were set after
the first pass's results were seen, the band's reinvestment after the second pass's, and the
top-up and the 100% after the replaced version's**, disclosed here; the replaced version's list of
changes that may not rescue it named the 99.5% and the reserve, so this version is a rescue the
owner chose, counted as one. The deflated Sharpe is not
computed.

<!-- example: end -->

### What would falsify it

**One condition for the whole experiment, fixed now.** Each prediction above has its own falsifier;
this is the result under which the experiment as a whole has failed — usually a margin against its
control, or a result that holds in one sub-period and not in the others. Then **the
changes that may not rescue it**: every setting that could be moved once the result is in — a
holding count, a trigger, a window, a threshold — by name. Moving one after the result is a new
experiment, and one more trial in the count.

<!-- example: begin -->

**The golden cross adds nothing on this universe, read monthly, inside a sector cap,** if
prediction 1 fails.

**The changes that may not rescue it:** the window and its sub-periods; the universe and the price
provider; the traded-value definition and its 63-day window; the 50/200 pair; the control's
definition; the monthly date, the open fill and the 0.5-point band; the 20% cap, the 1% floor, the
50% sector cap and the KN sector map; the cash rate, its spread, the 100%, its 99.5% fallback
and the 1% reserve; the top-up, its two days and its sizing; the exclusions
and the gap rule; the delisting rule; the base cost row and the flat row. Moving any of them after
the result is a new experiment, and one more trial.

<!-- example: end -->

### Key risks

- **Survivorship and point-in-time integrity.** The universe must include delisted names; step 2
  quantifies how many.
- **The signal's known weakness** — slow exits, whipsaw, regime dependence — named here, and either
  handled by the rules above or accepted on simplicity grounds and left to a later experiment.
- **Concentration.** How the weighting concentrates, and which diagnostics measure it.
- **The signal may not be what earns the return.** If the book beats its benchmarks because of a
  factor exposure rather than the signal, the honest product is a cheaper factor fund. That is what
  step 6 exists to answer.

<!-- example: begin -->

- **The sector map looks ahead.** Today's KN sector, for every date; a name that moved sector is
  capped in the wrong group before its move.
- **The cap may cost the return that concentration earned** in 2018–2026; prediction 4 bounds it.
- **The provider's rounding and faults**, as in Golden-Flow's blueprint: three-decimal adjusted
  prices, volume adjusted twice at some splits.
- **The signal is slow, and monthly makes it slower.**
- **A stock-for-stock deal becomes cash.** The engine sells an acquired name at its last price
  rather than delivering the acquirer's shares; the top-up puts that cash back two days later,
  in the names already held, not in the acquirer.
- **A top-up date trades more than the freed cash.** Every held name's weight is written as it
  drifted to the fill, and the engine rounds each to whole shares, so small orders appear; they are
  counted.
- **The index's history before its live date is a backtest of its own rules.**
- **The factor model is provisional.**
- **The window, the cap and its level were set knowing the first pass's results**, disclosed and
  counted.

<!-- example: end -->

### Open questions this experiment deliberately does not answer

Each is a later experiment, and each has to beat this one.

| # | Question | Why it is not answered here |
| --- | --- | --- |
| 1 | the question | why this experiment leaves it open |
