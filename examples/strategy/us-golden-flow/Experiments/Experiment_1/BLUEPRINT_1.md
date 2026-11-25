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

<!-- example: begin -->

**This copy** is Golden Flow's blueprint of 2026-10-23, word for word under each of the
template's headings; its opening blockquote is the template's. Versions 0.13.0 to 0.15.2 and their
tags are Golden Flow's own earlier versions and are not in this copy; "the desk" is KaxaNuk's
Analytics Factory; and one private name is replaced by a description in square brackets.

<!-- example: end -->

---

## Experiment 1 — the first rule against the benchmark

<!-- example: begin -->

## Experiment 1 — the most-traded KN US Equity Core members in a golden cross, by traded value, monthly

**Written 2026-10-23, before the rule cell held a line of this version.** Drafted with
KaxaNuk-Researcher 1.22.0 (template 0.19.4), Data Curator 0.51.0, Backtest Engine 0.66.0 and
Attribution Analysis 0.2.0.

**This blueprint replaces the one written on 2026-10-06** — the same idea on FMP prices from
2015-01-02 to 2026-06-01, re-struck whenever the held set changed, filled at the day's VWAP, with
`BIL` as cash and costs in cents a share — which is kept at tag `0.15.2` and as a row of
`RESULTS.md`. The owner decided this second rewrite on 2026-10-23, as `JOURNAL_1.md` records, and
every book priced under the earlier designs counts in the trials below.

**Its fixed elements are the owner's.** The universe, the prices, the window, the rebalance, the
fill, the band, the cash and its rate, the costs, the delisting rule, the capital, the factor model
and the gate's margins are the decisions of 2026-10-23, recorded in `JOURNAL_1.md` before any stage
ran; the rule was read back on one worked date, 2026-08-03, in the journal entry before this file.
The predictions were drafted from the analyzer and the notes under the owner's go on that plan, and
put to the `blueprint-critic` agent cold before this commit; its objections, and what was done
about each, are the journal entry that precedes this file's commit.

<!-- example: end -->

### Thesis

One paragraph: what book this rule produces, why it should beat the benchmark
`JOURNAL_1.md` chose, and why it is also a fair yardstick — sensible, liquid, low-complexity
— for judging whether any later idea adds value. **Be modest on purpose.** A first rule does not
assert its signal is the best of its kind, only that it is simple enough to be understood, liquid
enough to be traded, and stable enough to measure other things against.

<!-- example: begin -->

Once a month, own the KN US Equity Core members the market trades most while their fifty-day
average sits above their two-hundred-day one, each in proportion to what it trades, none above a
fifth of the book and none below a hundredth, and leave alone what barely moved.

**The economic reason is a risk gate that also pays in compound return.** A name falling through
its averages is one the market is selling; leaving it until the trend turns cuts the drawdowns a
book of the most traded names would otherwise ride through. The notes find that on indices and
asset classes, not on single names ranked against each other:
[Faber (2007)](../../Bibliotheca/Papers/Faber_2007_Quantitative_Approach_To_Tactical_Asset_Allocation.md)
says its filter does not license single names, and
[Hurst, Ooi & Pedersen (2017)](../../Bibliotheca/Papers/Hurst_Ooi_Pedersen_2017_Century_Of_Evidence_On_Trend_Following.md)
sizes by volatility, not liquidity. **The single-name reading is this blueprint's, and the analyzer
is its evidence**: on the pool, forward 21-day volatility is 31.8% with the cross on against 43.0%
off, and the forward 21-day return 0.87% against 0.20% (`RESULTS.md`, *Before any experiment*, rows
10 and 11). **That is where the owner's CAGR margin comes from**: a book that drops the names with
the lower forward return and the higher volatility gains on both counts in compound terms, since
a compound return falls with half the variance. The cross as a state ranks the pool at +0.0127,
+0.0189 and +0.0151 over 21, 63 and 252 days, positive on 52.7%, 53.0% and 52.4% of dates — strong
in 2000–2008, close to nothing at one and three months in 2009–2017 (rows 2 to 4): a sign, not a
size. Whether the edge is a premium or a mispricing is not answered here (open question 1).

**For the sizing, the evidence is against it.** Weighting by traded value buys capacity and an
explanation a reader can repeat. Inside the pool its rank is close to nothing over the window
(+0.0011, +0.0037 and +0.0130, rows 6 to 8), negative in 2000–2008 and positive since 2018; across
every member it points the wrong way (row 9), as
[Amihud (2002)](../../Bibliotheca/Papers/Amihud_2002_Illiquidity_And_Stock_Returns.md),
[Datar, Naik & Radcliffe (1998)](../../Bibliotheca/Papers/Datar_Naik_Radcliffe_1998_Liquidity_And_Stock_Returns.md)
and
[Ibbotson, Chen, Kim & Hu (2013)](../../Bibliotheca/Papers/Ibbotson_Chen_Kim_Hu_2013_Liquidity_As_An_Investment_Style.md)
find. Moving-average rules are also the class
[Sullivan, Timmermann & White (1999)](../../Bibliotheca/Papers/Sullivan_Timmermann_White_1999_Data_Snooping_Technical_Trading_Rules.md)
deflate.

**Why monthly, and why this version exists.** The owner asked for a book he can replicate in a
broker account: 0.15.2 re-struck on 1,381 of 2,869 trading days. A fixed monthly date with a band
is the simplest rule a person can follow by hand, and
[Novy-Marx & Velikov (2016)](../../Bibliotheca/Papers/NovyMarx_Velikov_2016_A_Taxonomy_Of_Anomalies_And_Their_Trading_Costs.md)
show costs decide the high-turnover anomalies. The trigger was chosen for tradeability, before any
return of this version existed, never on a Sharpe.

**It asserts nothing about being the best trend rule.** The seven questions before any backtest are
still the owner's, unanswered, under the open questions.

<!-- example: end -->

### The claim this moves

Which claim of `OBJECTIVE.md`, by number, this experiment exists to move, the status it reaches if
the predictions below hold, and the one it reaches if they fail. **One claim.** An experiment that
could beat every benchmark and settle nothing is a measurement, not a test.

<!-- example: begin -->

**Claim 1, the signal** (`OBJECTIVE.md`): holding only members in a confirmed uptrend makes a better
book than the same rule without it. Its test is prediction 1:

| Prediction 1 (the control margins and the sub-periods) | Success criterion 1's benchmark limb | Claim 1 becomes |
| --- | --- | --- |
| holds | holds | **confirmed as a book**, on the KN US Equity Core, 2000 to 2026, monthly, net |
| holds | fails | **confirmed against its control only**: a better book than the rule without the cross that loses to its index, said so in `OBJECTIVE.md` |
| fails | either | **falsified** as written, on this universe, window and trigger |

The benchmark limb is success criterion 1, scored there; the lead of the same name below only
records what the analyzer cannot measure beforehand. **The status `OBJECTIVE.md` gives today was
measured on the version this blueprint replaces**: it is rewritten from this version's findings,
whatever they are, and never kept.

**Claim 2, the sizing**, has two halves. Against equal weight it is prediction 3: **falsified** as
a source of Sharpe if prediction 3 holds (equal weight within 0.03 of the book or above it),
**confirmed as a book** if it fails. Against random draws, the ranking's half has no test of its
own here — the random books differ in the cross and the ranking together — and stays a lead.

**Claim 3, the construction**, holds on the **targets** by construction: no target above 20% or
below 1%, no name falling through its averages. Under the band, a struck weight can sit up to half
a point outside the bounds — a kept name drifted over the cap or under the floor, or a traded name
scaled down — and section 2.1 of the notebook reports how often and by how much.

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

- **Universe:** the KN US Equity Core's members as of each date, from the desk's daily holdings of
  2026-10-22 read by `Data/hand_supplied.py`, keyed by Sharadar's ticker, which is the price
  file's. A member Sharadar does not price (UB) is not in the universe; its weight is published per
  date in `Universe/Coverage.csv` (at most 0.11% of the Core on any day).
- **Prices:** Sharadar, through Data Curator 0.51.0, with the adjustment rebuilt from the exact
  unadjusted close and Sharadar's corporate actions (`Data/curator.py`, `rebuild_adjustments`):
  every signal, return and mark reads `c_close_dividend_and_split_adjusted`.
- **Signal:** the golden cross as a state — 1 while the 50-day simple average of that close is above
  the 200-day, 0 otherwise; `r_trend_50_200` above zero. The 50/200 pair was never tuned.
- **Traded value:** `r_traded_value_sma_63d`, the 63-day simple average of `c_daily_traded_value`,
  which `Data/curator.py`'s rebuild writes as the day's close times its volume, both split-adjusted
  — the dollars traded, invariant to later splits — with the volume the provider adjusted twice at
  82 splits corrected. Sharadar publishes no VWAP, so this replaces the VWAP times volume of 0.15
  that `OBJECTIVE.md` names; `OBJECTIVE.md` is brought to it with this version's findings.
- **Rebalance dates:** the first trading day of each month in the window, the window's first day
  included, for every book this experiment prices. Nothing re-strikes a book between them: no
  event, no drift trigger, no gap. The engine's sale of a delisted position at its last price is a
  sale, not a re-strike: the other weights drift.
- **Eligible on a rebalance date d:** a member at the close of the trading day before d, with a
  200-day history and the cross at 1 then, a traded value then, and an open price on d. **The open
  price is the one condition read on d**: a name that does not open — halted on news — cannot be
  filled by the engine, and a real market-on-open order would go unfilled; it is dropped and the
  others take its place, a small leak, stated.
- **Rank and sizing, the bounds set the count:** names in order of traded value at that close, each
  weighted as its traded value over the sum of the held names', capped at **20%**, the excess
  spread over the uncapped names in proportion until none is above the cap; names are added while
  the smallest weight stays at or above **1%**, and the book holds the last count that passed.
- **The band:** a name held since the last rebalance and still in the target keeps the weight it
  drifted to when its target differs from that weight, measured at the close before d, by **0.5
  points** or less; entries, exits and larger moves trade to target. What the kept names hold over
  their targets comes out of the traded names in proportion, so the book never exceeds one
  (`portfolio_construction.banded_book`).
- **Cash:** when fewer than five names are eligible the cap cannot place every dollar; the rest, and
  the engine's 1% cash reserve, are **US dollar cash**, paid by the engine at FRED's effective
  federal funds rate (`DFF`) less 0.5 points, floored at zero, ACT/360, as Interactive Brokers pays.
  The same rate is the risk-free rate of every Sharpe ratio the engine reports, **so these Sharpe
  ratios are excess of cash and are not comparable with 0.15.2's**, which were not. One flat spread
  is a simplification: a broker's published terms also depend on the balance and the account's
  size, which matter most in the $100,000 row.
- **The fill:** the open of d, dividend-and-split adjusted (`c_open_dividend_and_split_adjusted`), a
  market-on-open order; the open keeps Sharadar's three-decimal rounding, 0.23 bp of the Core at
  most.
- **Delistings:** a held name whose prices stop is sold by the engine at its last price
  (`sell_at_last_price`), Sharadar's last trade — over the counter where the exchange dropped it,
  which a hand-traded account may not reach, the open gap
  [Shumway (1997)](../../Bibliotheca/Papers/Shumway_1997_The_Delisting_Bias_In_CRSP_Data.md) names.
  This needs no day of hindsight. **A gap inside a series**, which the engine cannot price, is not
  traded around: a name the engine refuses for a gap is added to the register's blocking rows and
  excluded by name from every book, its weight published, and the run priced again — so no book
  ever trades off its monthly dates.
- **Excluded by name:** the blocking rows of `Universe/Data_Issues.csv` — FPS, H1, ILA.A, MDLN, Q and
  SUNB, with less than 200 days of prices while members, and TXCCQ, whose adjusted price moves more
  than sixfold in a day.
- **Costs, inside the engine:** commission **1 basis point** of the notional traded
  (`commission_model = "basis_points"`); slippage **`spread_plus_impact`** — a Corwin–Schultz
  half-spread from the day's split-adjusted high and low over 20 days, plus square-root impact from
  volume on the fill's basis, `slippage_basis_points = 5` as the half-spread where a range is
  missing; **$1,000,000**, integer shares, a 1% cash reserve. A **stress row** at 5 bp commission
  and 10 bp flat slippage, and a **$100,000 row** at the base costs, re-price the rule and the
  control. **What the cost model does not do:** a basis-point commission has no per-order minimum,
  so small tickets at $100,000 are under-charged against a broker's (the orders under $1,000 are
  counted, not priced); whether the engine's 20-day spread and volume windows include the fill's
  own day is not documented, and if they do, the fill's cost reads that day's range — a cost leak,
  not a selection one; integer shares are counted on the dividend-adjusted price, so in the early
  years they are not the lots a ticket would show.
- **Window:** 2000-01-03 to 2026-08-14. The floor is the owner's, chosen on 2026-10-23 after
  0.15's results were known, as the factor model's first date; the universe notebook's coverage
  rule (the members priced and signalled hold at least 90% of the Core on every date) confirmed it,
  at 98.1% on the floor, before any rule of this version existed. Nothing after 2026-08-14 exists
  in the Core or the factor model.
- **Control:** the same rule with the golden cross removed. Eligible on d: a member at the close
  before d, with a 200-day history and a traded value then, an open price on d, not excluded by
  name — every condition of the rule but the cross's sign. Ranked and weighted by traded value
  inside the same bounds, the same band, the same cash rule, rate and reserve, the same costs and
  delisting rule, **on the rule's own rebalance dates**. The history requirement is kept, so the
  cross's sign is the one difference.
- **Benchmarks:** the KN US Equity Core, then `SPY`; every alpha the engine reports is against the
  Core.
- **Screens deliberately absent:** no sector limit, no risk model, no stop-loss, no valuation
  screen. Each is a lever a later experiment has to earn.

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

**Predictions, fixed before the run.** Every source is a `Bibliotheca/` note or a row of
`RESULTS.md`, *Before any experiment*, which records `Data/analyzer_marimo.py` by section; the pool
is the fifty most traded members, the expected sign positive, consecutive windows sharing 20, 62
and 251 days. **Three rows are predictions and five are leads**: a lead is reported, not scored;
it is counted among the blueprint's leads, not among the trials, and says what would have licensed
it as a prediction.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | **The golden cross earns its keep**: the book beats its control by at least +0.03 Sharpe and +0.5 points of CAGR over the window, and beats it — any margin — on both in at least 2 of the 3 sub-periods | rows 2 to 4: the cross as a state on the pool, positive over the window at every horizon, on 52% to 53% of dates; a sign, not a size, and close to nothing in 2009–2017, so the sub-period limb is the one at risk | either margin missed over the window, or the control beaten on both measures in fewer than 2 sub-periods |
| 2 | **The cross is a drawdown control**: the book's maximum drawdown is shallower than its control's, and its volatility lower | row 11, forward 21-day volatility 31.8% on against 43.0% off. Context, not support: [Faber (2007)](../../Bibliotheca/Papers/Faber_2007_Quantitative_Approach_To_Tactical_Asset_Allocation.md), on indices. Against it: [Daniel & Moskowitz (2016)](../../Bibliotheca/Papers/Daniel_Moskowitz_2016_Momentum_Crashes.md) — after a panic the beaten-down names rip upward, and the control holds them while the book does not; read monthly, the cross also exits later than daily | the book's maximum drawdown deeper than the control's, or its volatility higher |
| 3 | **Weighting by traded value does not beat equal weight**: the equal-weight arm's Sharpe is within 0.03 of the book's or above it | rows 6 to 8, the traded-value rank on the pool close to nothing over the window, on about half the dates, negative in 2000–2008; row 9 and the three liquidity notes against the most traded names | the book's Sharpe above the equal-weight arm's by more than 0.03 |
| 4 | **Lead**: the book beats both benchmarks on Sharpe, net, over the window | a prediction would need a measurement of a book against an index, which the analyzer does not make; scored instead as success criterion 1 | counted as a lead |
| 5 | **Lead**: the rule's selection — the cross and the ranking together — beats chance, its idiosyncratic return above at least 16 of the 20 random books' | the random books draw from every member with a fill and differ from the book in the cross and the ranking at once; no row measures the two together | counted as a lead; part of gate criterion 2 |
| 6 | **Lead**: the bounds hold between 15 and 60 names on most rebalance dates — 28 on the read-back date — and the 20% cap binds on fewer than a quarter of them | a prediction would need the held names' own shares, which rows 12 and 13 do not measure (they measure all cross members'); run the read-back on every date to license it | counted as a lead; reported in section 3 of `experiment_1_marimo.py` |
| 7 | **Lead**: the monthly book with its band is tradeable by hand — a few dozen orders on each of its twelve dates a year, a one-way turnover under 2.0 a year — and the stress-cost row moves the CAGR by less than a point | [Novy-Marx & Velikov (2016)](../../Bibliotheca/Papers/NovyMarx_Velikov_2016_A_Taxonomy_Of_Anomalies_And_Their_Trading_Costs.md) on cost and turnover; a prediction would need this book's turnover, measured only by building it | counted as a lead |
| 8 | **Lead**: most of the excess return over the Core is factor exposure — market and beta — with momentum small, the factor model being close to blind to an absolute trend rule | [Paleologo (2021)](../../Bibliotheca/Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md), on a factor model's blindness to absolute signals; 0.15.2 found nine tenths of its excess was factor exposure on another window, a reading of another book, not a measurement of this one | counted as a lead |

**Watched, not predicted:** the book's early years, when Sharadar's rounding is coarsest (at most
0.22% of the Core with an adjusted price under a dollar, 2000 to 2004: analyzer section 1.1); and
2009–2017, where the cross's rows are close to nothing at one and three months (rows 2, 3 and 5).
**Beside every margin over the control**, the findings report the share of months the book beat
it and how much of the two books' weight overlapped, because two books holding the same names do
not make independent observations.

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

1. It beats the KN US Equity Core and SPY on Sharpe, net, over the window, **and its own control**
   as prediction 1 states: by at least **+0.03 Sharpe and +0.5 points of CAGR** over the window,
   and on both in at least **2 of 3** sub-periods — 2000-01-03 to 2008-12-31, 2009 to 2017, 2018
   to 2026-08-14.
2. Reproducible from a wiped working copy, through the pipeline, with no manual step beyond the ones
   `SETUP.md` names.
3. Tradeable as the owner asked, and stated, since its rebalance days are twelve a year by
   construction: orders a year, orders under $1,000 at $100,000, turnover, and every cost and the
   cash's interest as the engine priced them, by year.
4. Every prediction and lead above reported explicitly in `FINDINGS_1.md`, **including the ones that
   turn out wrong.**

**Success is necessary for graduation, not sufficient.** The gate's five criteria in
`Paper_Trading/BITACORA.md` decide it, and a person signs it:

| # | Criterion | Passes when |
| --- | --- | --- |
| 1 | Beats the benchmarks and its control | success criterion 1 |
| 2 | Idiosyncratic alpha in both layers | Brinson–Fachler selection above zero, the factor model's idiosyncratic return above zero, the third pass's selection above zero, and the book's idiosyncratic return above at least 16 of the 20 random books. **Precondition:** the first cut's benchmark return within 1.0 point a year of the Core's own returns file; if not, the two Brinson–Fachler rows read "not evidenced". The factor model is the KN US Equity Factor Model's Experiment 1, momentum skipping the latest month, **unreviewed by its owner and provisional**, and every attribution here says so |
| 3 | Survives perturbation | at least 6 of the 8 settings below keep the sign of the margin over their own control on both Sharpe and CAGR, and all 8 beat the KN US Equity Core on Sharpe |
| 4 | Costs and capacity stated | the base, stress and $100,000 rows; turnover; orders a year and orders under $1,000 at $100,000; the engine's commission, slippage and cash interest by year; capacity as a participation bound — the largest book at which the worst trade, the 1st percentile and the median stay within 1% and 5% of the name's 63-day traded value |
| 5 | Sign-off | the owner's name and date in `BITACORA.md`, after 1 to 4 are evidenced |

**The sweep, one setting at a time, each priced with its own control on the rule's dates:** cap at
15% and at 25%; floor at 0.5% and at 2%; traded-value window of 21 and of 126 days; the cross as
20/100 and as 100/300, each with its own history requirement. **The band at 0.25 and at 1.0
points** is priced too, with its control, and read on turnover and orders, not on the gate.

**The counterfactuals:** the rule's own selection equally weighted, on its dates, capped at 20%
with the rest in cash, under the same band — the sizing arm; twenty random books, each drawing on
every rebalance date as many names as the rule holds from the members the control may hold (a
200-day history, a traded value, an open on d, not excluded), sized by traded value under the 20%
cap with no floor walk, replacing as many names as entered the rule's book that day, under the
same band — the selection baseline. **The shifted-entry timing arm is not run.**

**The trial count: 152 books.** 107 priced before this version — 23 at 0.13.0, 14 at 0.14.0, 70
at 0.15.0 (39 the blueprint fixed and 31 of its first attempt), as `RESULTS.md` counts them — and
45 here: the rule, its control, the sixteen books of the sweep, the four of the band, the
equal-weight arm, the twenty random books, and the rule and control at $100,000, counted as books
because at that capital integer shares can change which positions exist. The cost rows and the
sub-period windows re-price these books and add none. **The window, the trigger and the costs are choices
taken after 0.15's results were seen**, listed here and in `RESULTS.md`. The deflated Sharpe is not
computed, and the sign-off says so.

<!-- example: end -->

### What would falsify it

**One condition for the whole experiment, fixed now.** Each prediction above has its own falsifier;
this is the result under which the experiment as a whole has failed — usually a margin against its
control, or a result that holds in one sub-period and not in the others. Then **the
changes that may not rescue it**: every setting that could be moved once the result is in — a
holding count, a trigger, a window, a threshold — by name. Moving one after the result is a new
experiment, and one more trial in the count.

<!-- example: begin -->

**The golden cross adds nothing on this universe, read monthly,** if prediction 1 fails: the book
misses the +0.03 Sharpe or the +0.5 points of CAGR over its control over the window, or beats the
control on both measures in fewer than 2 of the 3 sub-periods. This reads the backtest window; the
paper book's own kill switch is registered in `BITACORA.md` with the sign-off.

**The changes that may not rescue it:** the window and its sub-period boundaries; the universe,
the desk's files of 2026-10-22 and the price provider; the rebuild of the adjustment and the
Curator's correction of volume counted twice, with its tolerances; the traded-value definition and
its 63-day window; the 50/200 pair; the control's definition, its 200-day history included; the
monthly date, the open fill and the 0.5-point band; the 20% cap, the 1% floor and the five-name
cash rule; the cash rate and its spread; the 1% cash reserve; the 90% coverage rule; the exclusions
and the gap rule; the delisting rule; the base cost row, the slippage model and its 5 bp fallback.
Moving any of them after the result is a new experiment, and one more trial.

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

- **The provider's rounding and its faults.** Sharadar's adjusted prices are three decimals; the
  rebuild removes that from returns and signals but not from the open; 82 splits' volume was
  adjusted twice and corrected by a rule written from the data, which could miss or mistake one.
- **Concentration.** Traded value concentrates in a few names — 18.8% in MU on the read-back date —
  and the largest single share of the cross members' traded value rose from 2% in 2013 to 15% in
  2024 (row 13). The cap bounds a name, never a sector.
- **The signal is slow, and monthly makes it slower.** A month-end reading adds up to a month to
  every exit. [Kaminski & Lo (2014)](../../Bibliotheca/Papers/Kaminski_Lo_2014_When_Do_Stop_Loss_Rules_Stop_Losses.md)
  find stops help where returns trend and hurt where they mean-revert;
  [Han, Zhou & Zhu (2016)](../../Bibliotheca/Papers/Han_Zhou_Zhu_2016_Taming_Momentum_Crashes.md)
  compare a per-name stop with the death cross; and
  [Daniel & Moskowitz (2016)](../../Bibliotheca/Papers/Daniel_Moskowitz_2016_Momentum_Crashes.md)
  put momentum's crashes in the rebounds after a panic, when the names a trend filter has left are
  the ones that rise — 2009 opens the second sub-period.
- **The index's history is a backtest of its own rules.** Before its live date the Core's
  membership was computed by the desk from its methodology; whether every input it read was dated
  no later than the day it decided is the desk's to state, and is asked
  ([an issue in the Analytics Factory's private repository]).
- **The sizing may be a constraint dressed as a signal**, as rows 6 to 9 and the liquidity notes say.
- **The factor model is provisional**, its owner's review pending; attribution is read as such.
- **The index is not investable at its own costs.** The Core is priced gross; the book is net.
- **The window, the trigger and the margins were set knowing earlier results**, disclosed and
  counted.

<!-- example: end -->

### Open questions this experiment deliberately does not answer

Each is a later experiment, and each has to beat this one.

| # | Question | Why it is not answered here |
| --- | --- | --- |
| 1 | the question | why this experiment leaves it open |

<!-- example: begin -->

| # | Question | Why it is not answered here |
| --- | --- | --- |
| 1 | The seven questions before any backtest — why the edge exists, who is on the other side, risk premium or mispricing, how many independent bets a year, whether it survives costs and at what capital, when it fails and whether the owner would hold it, how many ideas came before | the owner's, unanswered; none is answered for him |
| 2 | A sector cap, a risk model, a different cross | each is a lever a later experiment has to earn against this one |
| 3 | Market impact beyond the engine's square-root model | the model is the engine's; capacity is stated as a participation bound beside it |
| 4 | Does the Core's own construction read Sharadar's double-counted volume? | the desk's question, [an issue in the Analytics Factory's private repository] |

<!-- example: end -->
