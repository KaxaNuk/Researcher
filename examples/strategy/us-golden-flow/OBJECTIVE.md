# Objective

> **Step 1 of 8, with `Bibliotheca/`.** One idea, one objective, and the claims inside it with
> their status. The first thing a reader reads and the last thing that changes: a change here means
> a *different* strategy, not a better version of this one.
>
> **Write it before any paper is read, and before anything is measured.** The claims table is a set
> of predictions; a claim written after the reading, or added after a result, is an observation
> wearing a hypothesis's clothes.
>
> In a new strategy, everything in italics below is guidance: replace it, keep the plain text,
> then delete this blockquote.

<!-- example: begin -->

> **Written on 2026-11-23, after the fact, and said so.** The idea is the owner's, in their words
> for Golden-Flow, the strategy this one rebuilds in the Investment Lab: *"invest in the top 35
> stocks ranked and weighted by traded value of 63d and use the 50 vs 200 sma golden cross signal to
> become elegible"*; asked why 35, they retired the count: *"Maybe we can invest in the Top names
> meanwhile non weight more than 20% and less than 1%"* (the worked example's `OBJECTIVE.md`, in
> the KaxaNuk Researcher). This version adds, on their decisions of 2026-11-16, a cap of half the
> book on each KN sector and the signals as Data Curator `c_*` columns
> ([`BLUEPRINT_1.md`](Experiments/Experiment_1/BLUEPRINT_1.md)). The order this file asks for — the
> objective before any paper and any result — was not kept: the notes in `Bibliotheca/` were read
> for Golden-Flow, and Experiment 1 had reported three times before this was written. The claims are
> Golden-Flow's, word for word where the rule did not change; only their status and evidence are
> this repository's.

## The main idea

> **Own the KN US Equity Core stocks the market is trading most, while their trend is up, in
> proportion to what they trade** — none above a fifth of the book, none too small to matter, and
> no sector above half of it.

The signal is the **golden cross**: a member is eligible while its 50-day simple moving average sits
above its 200-day one, `c_golden_cross_50_200` at 1, read at the prior close. The sizing is
**traded value**: the 63-day average of each day's close times its volume, both split-adjusted —
the dollars traded — `c_traded_value_sma_63d`, which ranks the eligible names and weights them in
proportion. The book holds as many as fit the owner's bounds — no weight above 20%, none below 1%,
no KN sector above 50% — so the market's own distribution of trading sets how many names it owns,
and nobody chooses a count.

Neither half is clever, and that is the design. The name keeps Golden-Flow's — golden cross,
dollar-volume flow — and the two columns are named here so that attribution can say which half
earned the return.

## The objective

**Build a long-only US-equity book whose every decision can be explained in one sentence, and find
out how much of its return is the idea rather than the market.** The deliverable is not a number; it
is a rule simple enough that when it works, we can say *why*, and when it fails, we can say *which
part* failed — run end to end in the Investment Lab, from the Data Curator's columns to the Backtest
Engine and Attribution Analysis, so the KaxaNuk app shows what the rule reads.

Concretely, an acceptable end state is: *on any date, the strategy names the stocks it holds, gives
a one-sentence reason for each, and can point at an attribution that says how much of the return
came from the signal rather than from beta, size or sector.*

**The constraint is radical simplicity.** Complexity is added one lever at a time, and each addition
must beat the simpler baseline to earn its place.

## The claims inside that sentence

They are tested separately and **their status is not the same.** This table is the only place a
reader sees which parts of the idea have survived contact with the data, so it is kept honest.

| | Claim | Status |
| --- | --- | --- |
| **1. The signal** | Holding only members in a confirmed uptrend — the golden cross — produces a better book than the same rule without it | **falsified** inside the sector cap, as `BLUEPRINT_1.md` words it: over 1999-12-31 to 2026-10-30 the rule beats its control, a Sharpe of 0.143 against 0.102 net (0.207 against 0.124 at a flat 5 bp), but on both Sharpe and CAGR in only 1 of 3 sub-periods, where 2 were required, and it loses to the Core's 0.306 ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md)). In sample |
| **2. The sizing** | Ranking and weighting by 63-day traded value, inside the 20% and 1% bounds, tilts capital toward what the market is buying, and that is worth return | **confirmed against its control only**: 0.143 against 0.069 for the same names equally weighted (0.207 against 0.145 at a flat 5 bp), and the book loses to its benchmarks ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), prediction 3). Against random draws, not priced in this version. In sample |
| **3. The construction** | A trend filter is a value-trap screen — a falling stock can never enter — and the bounds guarantee no name above 20%, none below 1% and no KN sector above 50% | **true by construction on the targets**; under the half-point band, 572 struck weights sat outside the name bounds, and every struck sector was at or under 50% on all 323 rebalance dates. The sector cap held as a risk limit: lower volatility and drawdown than the same rule uncapped, at the same Sharpe ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), prediction 4). As a source of return the screen is measured only through claim 1's control |

Status vocabulary, so it means the same across strategies: **untested** · **measured** (the analyzer
says something; no book has been run) · **falsified** · **confirmed as a book** (it beats its
benchmarks through the engine) · **confirmed as a factor** (attribution assigns it the return) ·
**unexplained** (confirmed as a book, not as a factor — the usual state, and the interesting one) ·
**true by construction** · **confirmed against its control only** (it beats the same rule with the
claim's ingredient removed, and loses to its benchmarks).

### Claim 1 — the signal

**The question that settles it:** does the book beat the same rule with the golden cross switched
off — same bounds, same sector cap, same traded-value ranking, on the book's own rebalance dates —
by the margins `Experiments/Experiment_1/BLUEPRINT_1.md` fixes before the run? The control differs
in one ingredient, so the margin is the cross's and nothing else's.

**What the library says.** The trend-following notes — Faber's moving-average timing
([note](Bibliotheca/Papers/Faber_2007_Quantitative_Approach_To_Tactical_Asset_Allocation.md)), the
century of trend evidence
([note](Bibliotheca/Papers/Hurst_Ooi_Pedersen_2017_Century_Of_Evidence_On_Trend_Following.md)) and
time-series momentum
([note](Bibliotheca/Papers/Moskowitz_Ooi_Pedersen_2012_Time_Series_Momentum.md)) — find an absolute
trend rule earns its keep by cutting drawdowns more than by adding return. Relative momentum
([Jegadeesh &
Titman](Bibliotheca/Papers/Jegadeesh_Titman_1993_Returns_To_Buying_Winners_And_Selling_Losers.md))
is the contrast, not the support. **Against it:** a moving-average rule found to work is the maximum
of many tried ([Sullivan, Timmermann &
White](Bibliotheca/Papers/Sullivan_Timmermann_White_1999_Data_Snooping_Technical_Trading_Rules.md));
a stop whipsaws where prices mean-revert ([Kaminski &
Lo](Bibliotheca/Papers/Kaminski_Lo_2014_When_Do_Stop_Loss_Rules_Stop_Losses.md)); and after a panic
a trend filter misses the rebound ([Daniel &
Moskowitz](Bibliotheca/Papers/Daniel_Moskowitz_2016_Momentum_Crashes.md)).

**What the run found**, in [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), version
0.4.0. The rule beats its control by 0.040 of Sharpe and 0.66 points of CAGR at the pre-registered
costs, 0.083 and 1.62 at the flat 5 bp row, and beats it on both only in 1999–2008; in 2009–2017
the control wins, and in 2018–2026 the rule wins on Sharpe and loses on CAGR. The cross is a
drawdown control, as the trend notes say: −81.5% against the control's −90.6%. The experiment is
falsified on its sub-period limb, for the third time on the same limb.

### Claim 2 — the sizing

**The question that settles it:** does the rule's own selection, weighted by traded value, beat the
same selection equally weighted, and does the ranking beat random draws of the same size from the
same members? The analyzer measures the traded-value rank's information coefficient before any
book exists ([`RESULTS.md`](RESULTS.md), *Before any experiment*).

**What the library says.** Every note on liquidity finds the most traded names *underperform*
across the whole cross-section —
[Amihud](Bibliotheca/Papers/Amihud_2002_Illiquidity_And_Stock_Returns.md),
[Datar, Naik &
Radcliffe](Bibliotheca/Papers/Datar_Naik_Radcliffe_1998_Liquidity_And_Stock_Returns.md), [Ibbotson,
Chen, Kim & Hu](Bibliotheca/Papers/Ibbotson_Chen_Kim_Hu_2013_Liquidity_As_An_Investment_Style.md).
The argument for this sizing is that inside the most traded names, where the rule ranks, the sign
can differ, and a weight with no forecast behind it is still open to question — its source, a book,
is not in this example: a contradiction kept visible.

**What the run found**, in [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md). The book's
Sharpe is 0.143 against 0.069 for the same names equally weighted, 0.207 against 0.145 at the flat
row, more than the 0.03 the blueprint allowed, so its prediction 3 fails and the sizing wins.
Against random draws it is not evidenced: the twenty random books are not priced in this version.

### Claim 3 — the construction

True by construction: a name that is falling cannot pass the cross, so no valuation model is
needed, and the weigher cannot write a target outside the bounds or a sector above half the book
([Asness, Moskowitz &
Pedersen](Bibliotheca/Papers/Asness_Moskowitz_Pedersen_2013_Value_And_Momentum_Everywhere.md) for
why a trend filter screens out value traps). As a *source of return* the screen is measured only
through claim 1's control — what the screen excludes is what the control holds — and the sector cap
through the uncapped arm: 0.1428 against 0.1430 of Sharpe, with lower volatility and drawdown
([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md), prediction 4).

---

## What is not claimed

- **Not that the parameters are right.** The 50/200 pair is the most widely known one and has never
  been tuned; the 63-day window is the Curator's own; the 20% and 1% bounds and the 50% sector cap
  are the owner's numbers. None was chosen on the metric it is judged by. That is a defence against
  data-snooping, not evidence of optimality — and the window, the cap and its level were set after
  the first pass was seen, disclosed and counted among the 339 trials.
- **Not that this is out of sample.** Nothing is, until a book has days on paper after its freeze.
- **Not that the universe is free of survivorship.** The seed keeps the delisted; how much of the
  index the curated files price is measured in [`RESULTS.md`](RESULTS.md), *Before any experiment*.
- **Not that the sector map is point in time.** The cap reads today's KN sector for every date, a
  deliberate look-ahead, as a `current_*` column is.
- **Not that the sector cap earns return.** It is a risk limit, and was claimed as one.
- **Not that Golden-Flow's results carry over.** Golden-Flow's figures were measured with other
  rules, windows and code; this repository's are the only ones it quotes.

---

## Where each half is named

| Half | Column | Built by | Read by |
| --- | --- | --- | --- |
| the signal | `c_golden_cross_50_200` — 1 while the 50-day average of `c_close_dividend_and_split_adjusted` is above the 200-day, 0 otherwise; and `c_eligible_golden_cross_50_200` — 1 when the name was a Core member with the cross at 1 at the prior close | `Data/Curator/custom_calculations.py`, and again in `Data/curator.py`'s completion pass, which adds the membership | the rule's eligibility, and `Data/analyzer_marimo.py` |
| the sizing | `c_traded_value_sma_63d` — the 63-day simple average of `c_traded_value`, the close times the volume, both split-adjusted, with the volume Sharadar adjusted twice corrected | `Data/Curator/custom_calculations.py`, beside its 21- and 126-day siblings | the rule's ranking and weighting |
| the sector cap | the KN sector of the KN US Equity Factor Model, today's map for every date | `Experiments/attribution_analysis.py`, `kn_sectors` | the sizing's 50% cap |

Two columns for the two halves, built in the Curator so the KaxaNuk app charts what the rule reads,
and attribution and the counterfactual books can say which half earned the return.

<!-- example: end -->

---

## The five parts, and the job each does

| Part | Its job | The failure it prevents |
| --- | --- | --- |
| **The main idea** | one sentence somebody outside the team could repeat | a strategy nobody can explain is a strategy nobody can debug |
| **The objective** | the *capability* a finished version gives you, not a number | you cannot tell whether you have achieved "a Sharpe of 1.2" |
| **The claims** | the sentence broken into parts testable separately, each with a status | a strategy that half works reads as working, unless the halves are listed |
| **What is not claimed** | what a reader might assume and would be wrong to | the reader assumes it anyway if you do not say |
| **The named columns** | which `c_*` or `r_*` column carries each half | attribution cannot say which half earned the return unless the halves have names |

---

**Where this stands, with every number and its caveats: [`RESULTS.md`](RESULTS.md).**
How work is done here, and the bar a result has to clear: [`AGENTS.md`](AGENTS.md).
