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

> **Written on 2026-10-05 from the owner's words:** *"invest in the top 35 stocks ranked and
> weighted by traded value of 63d and use the 50 vs 200 sma golden cross signal to become
> elegible"*. Asked why 35, the owner retired the count: *"Maybe we can invest in the Top names
> meanwhile non weight more than 20% and less than 1%"*. The notes in `Bibliotheca/` were read
> earlier — the papers on 2026-09-02, the book on 2026-08-25 — for an earlier form of the idea. An
> earlier version's result was known too, so the order this file's first lines ask for was not kept.
> The status column moved on 2026-10-24, when `FINDINGS_1.md` reported on the second rewrite, on
> Sharadar from 2000; no claim's wording changed.

## The main idea

> **Own the KN US Equity Core stocks the market is trading most, while their trend is up, in
> proportion to what they trade** — none above a fifth of the book, none too small to matter.

The signal is the **golden cross**: a member is eligible while its 50-day simple moving average sits
above its 200-day one, `r_trend_50_200` above zero, computed by the Refinery from the name's own
adjusted close. The sizing is **traded value**: the 63-day average of each day's close times its
volume, both split-adjusted — the dollars traded — `r_traded_value_sma_63d`, which ranks the
eligible names and weights them in proportion. The book holds as many as fit the owner's two bounds
— no weight above 20%, none below 1% — so the market's own distribution of trading sets how many
names it owns, and nobody chooses a count.

Neither half is clever, and that is the design. The strategy is named **Golden Flow** after the two
of them — golden cross, dollar-volume flow — and the two columns are named here so that attribution
can later say which half earned the return.

## The objective

**Build a long-only US-equity book whose every decision can be explained in one sentence, and find
out how much of its return is the idea rather than the market.** The deliverable is not a number; it
is a rule simple enough that when it works, we can say *why*, and when it fails, we can say *which
part* failed — and simple enough to be the Lab's reference example of the whole process, from the
first note to a book on paper.

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
| **1. The signal** | Holding only members in a confirmed uptrend — the golden cross — produces a better book than the same rule without it | **confirmed against its control only**, on the KN US Equity Core, 2000 to 2026, monthly, net: a Sharpe of 0.162 against its control's 0.097 (0.221 against 0.117 at a flat 5 bp), +1.30 points of CAGR (+2.24), beating it on both in 2000–2008 and 2018–2026 and losing in 2009–2017 — and losing to the Core's 0.315 ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md)). In sample. 0.15's "confirmed as a book" on FMP, 2015 to 2026, was measured on the version this one replaced, and no longer stands |
| **2. The sizing** | Ranking and weighting by 63-day traded value, inside the 20% and 1% bounds, tilts capital toward what the market is buying, and that is worth return | **confirmed as a book against equal weight**, 2000 to 2026: 0.162 against 0.087 for the same names equally weighted (0.221 against 0.157 at a flat 5 bp) ([`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md)). Against random draws, not evidenced. In sample |
| **3. The construction** | A trend filter is a value-trap screen — a falling stock can never enter — and the bounds guarantee no name above 20% and none below 1% | **true by construction on the targets**; under the half-point band, 556 struck weights over 26 years sat outside the bounds by at most the band and the overnight move; as a source of return it is measured only through claim 1's control |

Status vocabulary, so it means the same across strategies: **untested** · **measured** (the analyzer
says something; no book has been run) · **falsified** · **confirmed as a book** (it beats its
benchmarks through the engine) · **confirmed as a factor** (attribution assigns it the return) ·
**unexplained** (confirmed as a book, not as a factor — the usual state, and the interesting one) ·
**true by construction** · **confirmed against its control only** (it beats the same rule with the
claim's ingredient removed, and loses to its benchmarks).

### Claim 1 — the signal

**The question that settles it:** does the book beat the same rule with the golden cross switched
off — same bounds, same traded-value ranking, on the book's own rebalance dates — by the margins
`Experiments/Experiment_1/BLUEPRINT_1.md` fixes before the run? The control differs in one
ingredient, so the margin is the cross's and nothing else's.

**What the library says before the run.** The trend-following notes in
[`Bibliotheca/BIBLIOGRAPHY.md`](Bibliotheca/BIBLIOGRAPHY.md) — Faber's moving-average timing, the
century of trend evidence, the time-series momentum paper — find an absolute trend rule earns its
keep by cutting drawdowns more than by adding return, and the data-snooping papers warn that a
moving-average rule found to work is the maximum of many tried.

**What the run found**, in [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md). On the KN US
Equity Core, 2000 to 2026, monthly and net, the book's Sharpe is 0.162 against its control's 0.097,
and 0.221 against 0.117 at the flat 5 bp row; it beats the control on Sharpe and CAGR in 2000–2008
and 2018–2026, and loses in 2009–2017. Its drawdown is −82.6% against the control's −91.7%. It loses
to the Core's 0.315, so the claim is confirmed against its control only, in sample.

### Claim 2 — the sizing

**The question that settles it:** does the rule's own selection, weighted by traded value, beat the
same selection equally weighted, and does the ranking beat random draws of the same size from the
same members? The analyzer measures the traded-value rank's information coefficient inside the
eligible pool before any book exists.

**What the library says before the run.** The liquidity papers in the Bibliotheca find the most
traded names *underperform* across the whole cross-section; the argument for this sizing is that
inside the most traded names, where the rule ranks, the sign can differ. That is a measurement for
the analyzer, not an assumption.

**What the run found**, in [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md). The book's
Sharpe is 0.162 against 0.087 for the same names equally weighted, 0.221 against 0.157 at the flat
row, more than the 0.03 the blueprint allowed. Against random draws it is not evidenced: the rule
beats 15 of the 19 random books priced whole at the flat row, where the bar was 16 of 20.

### Claim 3 — the construction

True by construction: a name that is falling cannot pass the cross, so no valuation model is
needed, and the weigher cannot write a weight outside the bounds. As a *source of return* it is
measured only through claim 1's control — what the screen excludes is what the control holds.

---

## What is not claimed

- **Not that the parameters are right.** The 50/200 pair is the most widely known one and has never
  been tuned; the 63-day window is the Curator's own; the 20% and 1% bounds are the owner's words.
  None was chosen on the metric it is judged by, and the blueprint's sweep shows their neighbours.
  That is a defence against data-snooping, not evidence of optimality.
- **Not that this is out of sample.** Nothing is, until the book has days on paper after its freeze.
- **Not that the universe is free of survivorship.** Members Sharadar does not carry are dropped,
  and the share of the index they held is published per date beside every result.
- **Not that the earlier versions' results carry over.** They were measured on FMP from 2015, and
  before that on another index, with other rules and windows, and are rows of `RESULTS.md`.

---

## Where each half is named

| Half | Column | Built by | Read by |
| --- | --- | --- | --- |
| the signal | `r_trend_50_200` — the 50-day average of the adjusted close over the 200-day one, minus one; above zero is the golden cross | `Data/Refinery/custom_calculations.py`, because a sweep of the two windows must never cost a download | the rule's eligibility, and `Data/analyzer_marimo.py` |
| the sizing | `r_traded_value_sma_63d` — the 63-day simple average of `c_traded_value`, the close times the volume, both split-adjusted, as `Data/Curator/custom_calculations.py` writes it (Sharadar publishes no VWAP) | `Data/Refinery/custom_calculations.py`, beside its 21- and 126-day siblings, and checked by the analyzer against the 63-day average of the Curator's own column | the rule's ranking and weighting; `r_liquidity_rank`, its per-date percentile, is what the analyzer screens |

Two columns, two stages, so attribution and the counterfactual books can say which half earned the
return.

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
