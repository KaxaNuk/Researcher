---
source: "not recorded. Add it the next time this source is opened; a wrong link is worse than none."
citation: "Journal of Portfolio Management 40(5), 94-107. Cited from the journal reference only; this entry has not been link-checked."
local_copy: none
read: "2026-09-02; what was read: not recorded"
---

# Bailey & López de Prado (2014) — *The Deflated Sharpe Ratio*

## What it says

Provides a Sharpe ratio corrected for the number of trials attempted, for non-normality, and for
track-record length. The maximum Sharpe across N backtests is a biased estimate of the best
strategy's true Sharpe, and the bias grows with N.

## What it implies for Golden Flow

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **Claims 1 and 2 rest on one book that came after others, and this paper says what that costs.**
> The rule's parameters were fixed before its run. The trial count is 152 books across this
> strategy's versions, and two choices are counted beside them: the 2000 floor, and the flat 5 bp
> row, added after the pre-registered result was seen
> ([`FINDINGS_1.md`](../../Experiments/Experiment_1/FINDINGS_1.md), *The trial count*).
>
> This paper asks how much of the rule's Sharpe of 0.162, against its control's 0.097, survives that
> search. The book already loses to the KN US Equity Core's 0.315, so deflation cannot rescue the
> whole window; what it would test is the margin over the control. The deflated Sharpe is not
> computed: open item 4 of `FINDINGS_1.md`.
