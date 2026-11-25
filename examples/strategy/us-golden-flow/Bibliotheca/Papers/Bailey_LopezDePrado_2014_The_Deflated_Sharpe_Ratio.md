---
source: "not recorded. Add it the next time this source is opened; a wrong link is worse than none."
citation: "Journal of Portfolio Management 40(5), 94-107. Cited from the journal reference only;
this entry has not been link-checked." local_copy: none
read: "2026-09-02; what was read: not recorded"
---

# Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio*

## What it says

Provides a Sharpe ratio corrected for the number of trials attempted, for non-normality, and for
track-record length. The maximum Sharpe across N backtests is a biased estimate of the best
strategy's true Sharpe, and the bias grows with N.

## What it implies for US-Golden-Flow

> Written on 2026-11-23 for this strategy, after `FINDINGS_1.md` reported on version 0.4.0,
> run of 2026-11-20.
>
> **Claims 1 and 2 rest on one book that came after others, and this paper says what that costs.**
> The trial count is 339 books across Golden-Flow's and this strategy's versions, published beside
> the result ([`FINDINGS_1.md`](../../Experiments/Experiment_1/FINDINGS_1.md), *The trial count*).
>
> The rule's Sharpe is 0.143 at the pre-registered costs and 0.207 at the flat 5 bp row, against its
> control's 0.102 and 0.124. The book already loses to the KN US Equity Core's 0.306, so deflation
> cannot rescue the whole window; what it would test is the margin over the control, and that margin
> already fails the blueprint's sub-period limb. The deflated Sharpe is not computed: limitation 6
> of [`RESULTS.md`](../../RESULTS.md).
