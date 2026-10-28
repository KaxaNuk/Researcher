---
source: "not recorded. Add it the next time this source is opened; a wrong link is worse than none."
citation: "Journal of Finance 52(1), 327-340. Cited from the journal reference only; this entry has not been link-checked."
local_copy: none
read: "2026-09-02; what was read: not recorded"
---

# Shumway (1997) — *The Delisting Bias in CRSP Data*

## What it says

Delisting returns are frequently missing from standard databases, and the missing ones are
disproportionately bad — performance-related delistings. Ignoring them biases measured returns
upward.

## What it implies for Golden Flow

> Rewritten on 2026-10-27 for this copy, after FINDINGS_1.md reported on Sharadar.
>
> **Claims 1 to 3 inherit the gap this paper names, narrowed.** A delisted name is sold by the
> engine at Sharadar's last trade, which needs no hindsight. That trade may be over the counter,
> where the exchange dropped the name, and a hand-traded account may not reach it
> ([`FINDINGS_1.md`](../../Experiments/Experiment_1/FINDINGS_1.md), *Caveats*).
>
> A name with a gap inside its series is excluded by name from every book, and
> `Universe/Data_Issues.csv` names it. [`AGENTS.md`](../../AGENTS.md) lists the last day of a
> delisted name under lie 1, as what the process still does not audit.
