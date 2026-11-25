---
source: "not recorded. Add it the next time this source is opened; a wrong link is worse than none."
citation: "Journal of Financial Economics 104(2), 228-250. Cited from the journal reference only;
this entry has not been link-checked." local_copy: none
read: "2026-09-02; what was read: not recorded"
---

# Moskowitz, Ooi & Pedersen (2012) — *Time Series Momentum*

## What it says

Distinguishes *time-series* momentum — an asset's own past excess return predicting its own future
return — from the cross-sectional kind, and finds it across dozens of futures and forward contracts,
strongest at roughly a twelve-month lookback and reversing beyond that.

## What it implies for US-Golden-Flow

> Written on 2026-11-23 for this strategy, after `FINDINGS_1.md` reported on version 0.4.0,
> run of 2026-11-20.
>
> **Claim 1, the signal: this, not Jegadeesh-Titman, is the family the golden cross belongs to.**
> The cross, `c_golden_cross_50_200`, asks whether a name's 50-day average is above its own 200-day
> one. It never asks how the name ranks against its peers.
>
> A factor model built on relative momentum should see little of the cross itself, so the cross is
> measured by the control instead: the rule leads it by 0.040 of Sharpe and 0.66 points of CAGR a
> year at the pre-registered costs, 0.083 and 1.62 at the flat 5 bp row, and beat it in 51.2% of
> months. The two books share 63.0% of their weight on the mean rebalance date, so those months are
> not independent draws, and the margin holds in only 1 of 3 sub-periods
> ([`FINDINGS_1.md`](../../Experiments/Experiment_1/FINDINGS_1.md)).
