# Paper Trading — step 7 of 8

**In plain words:** a dress rehearsal on data nobody has seen yet. **It produces** out-of-sample
evidence and an operations checklist. **It prevents** finding the plumbing problems on day one of
funding.

A backtest tells you what a rule *would* have done; paper trading tells you what it *does* — on live
prices, with live universe changes, and with the delistings and corporate actions a historical file
has already tidied up.

This is the last step inside this repository. Step 8, Production, is not here: a strategy leaves
when it is funded — real capital, real monitoring, a real drawdown policy — and where it goes
depends on whose desk it is.

> **This file is the gate, not a log.** A `JOURNAL_N.md` is an append-only dated record inside an
> experiment folder. This file is a contract — what graduation means and what has to be true
> before it happens — and its different name keeps the two apart.

## What graduation means

An experiment is **promoted**, not copied, and only one that graduates.
`Paper_Trading/Paper_Trading_N/` mirrors the `Experiment_N` it came from, so the lineage of a
paper-traded book is never in question. The experiment notebook stays where it is, as the record of
how the rule was chosen.

## The gate

Strong backtest results are necessary and **not sufficient**, and they are read second. The gate
has two layers, read in order: **is the experiment done correctly**, and only then **does it earn
its place**. Every criterion is evidenced from the experiment's `FINDINGS_N.md` and from
[`../RESULTS.md`](../RESULTS.md).

### Soundness — is the experiment done correctly?

Each row cites its evidence; a row without evidence does not hold.

| # | Soundness criterion | Evidenced by |
| --- | --- | --- |
| S1 | **No survivorship bias** | the point-in-time universe: departed names kept in the seed, the security master, the usable date |
| S2 | **No look-ahead** | signals lagged, next-open fills, the blueprint's rule and predictions registered before any result |
| S3 | **No overfitting** | the trial count published, the sweep read as a curve, the control and the random books priced |
| S4 | **Costs and capacity stated** | turnover, commission, slippage, cash, and every assumption the engine does not model |
| S5 | **Reproducible** | the pipeline ran from a working copy whose data folders were emptied first, every Verify passing |

They are the five ways a backtest lies in [`../AGENTS.md`](../AGENTS.md), turned into what a reader
can check. A performance figure from an experiment that fails one of them means nothing: a
survivor-biased universe or a rule that saw the future beats its benchmark by construction.
Publishing the trial count is the minimum of S3, and the sign-off states whether the deflated
figure was also computed.

### Performance — does it earn its place?

| # | Performance criterion | Why it is on the list |
| --- | --- | --- |
| P1 | **Beats the benchmarks and its control on risk-adjusted return, over the whole window** — above every benchmark it reports against, *and* above its own control row. The control is the one its blueprint names: the same rule with one ingredient removed, trading on the rule's own rebalance dates | A strategy that only beats the index on raw return is usually just carrying more risk, and one that beats only a control trading on other dates has been compared on two things at once |
| P2 | **Attribution shows idiosyncratic alpha in both layers** — selection in the Brinson-Fachler cut, a residual the factor model cannot explain, and a selection story that survives the third pass on residual returns | If the return decomposes entirely into known factors, the honest product is a cheaper factor fund, not this |
| P3 | **Conclusions survive parameter perturbation** | A result that appears at one threshold and vanishes at the next is a sweep artefact. Read the direction across a sweep, never the single best cell |

### The outcomes

- **Graduates** — every soundness and performance criterion holds, and the owner signs it off in
  this file: the book is frozen and paper traded.
- **Sound and regime-dependent** — every soundness criterion holds; performance fails over the
  whole window but holds in named periods. The findings name the periods where it earned and where
  it failed, and the condition that tells them apart as far as the evidence goes. It may go to
  paper **on probation**, on the owner's sign-off: frozen unchanged, with its regime prediction, a
  period of at least 12 months and its review date registered in this file before day one, and
  read at the review against its index and its control — continue, stop, or a new experiment.
  **Paper alone never sends it to production.** Otherwise it may be paired with another signal in
  a later experiment, or used at a portfolio manager's discretion — the decision, and its risk, are
  theirs. Never a recommendation.
- **Not sound** — a soundness criterion fails: no conclusion is drawn; fix it and run again.

The sign-off stays a person's name and date. **Graduation is a decision, not a threshold that trips
automatically**, and the assistant never decides a gate. A named period is one the blueprint fixed
before the run, such as the sub-periods it judges the book on, never one cut afterwards around
where the book did well.

### P2 is evaluable here, and that is not universal

This stack has a real attribution stage, so "is this selection, or a factor tilt?" has an answer,
not an admission. A repository on a stack without step 6 has to substitute a beta-matched control
book or an explicit regression on the market, and name the substitute in the sign-off. **Here
there is no substitute to name, and so no excuse.**

Expect a *pass with a qualification* rather than a clean pass. A book whose excess return is
roughly half factor exposure and half idiosyncratic has passed P2, and has been told exactly how
much of it is not the idea. Surfacing that is what the criterion is for, not a reason to soften it.

## What a paper-trading run is

Unlike an experiment, this stage is **not** a notebook. It is a script that runs on a schedule and
asks what the book holds today, and how it is doing.

**A graduated book is the strategy, frozen.** `promote.py N` runs once, after the sign-off. From
the commit that graduated, it copies byte for byte into `Paper_Trading_N/`, in the strategy's own
layout, every file the book needs to go from raw prices to a priced book, and writes `FREEZE.json`
with the commit, the date and the hash of each file. The security master is the one file not taken
from the commit: it is the provider's data, so it is copied from disk, hashed like the rest and
kept out of git by `.gitignore`, as the one in `Universe/` is. The rule itself goes into
`paper_trading_N.py`, copied from the experiment's cells and committed first. Every module resolves
its paths from its own folder, so the copies read and write only inside the book's folder:
experiments under construction can change the shared modules, and a graduated book never moves. A
repository can hold several books on paper and several experiments under construction at once.

**`daily_update.py` runs every graduated book once a day**, after the market closes:

- refreshes the shared raw prices once, or reads them from a database another machine published;
- checks the newest day before any book reads it, and stops every book on a close with no fill
  price or a move no price can make: a book on broken data is worse than none. It checks that day
  only, so a security's file that ends before it, or a bad bar between two runs, passes unflagged;
- runs each frozen book — its frozen refinery, its frozen rule from the experiment's first day, and
  the engine — over the whole history, over the days after the experiment's window, and since the
  day it was frozen;
- writes the record — the book in force, the engine's daily values and statistics, what the book
  looked like that day — to local files, a DuckDB database, or both, as `Config/.env` says;
- flags every diagnostic outside the band registered below, every failed check, an input that
  lags the day, and a **restatement**: a past value the engine now prices differently, never
  overwritten;
- exits 0, 1 or 2 — clean, flagged, failed — so a scheduler can tell; a step that raises is a
  failed day, with its traceback in the day's log.

**A paper-trading script re-fits nothing**, and that is the whole point of the stage. A run that
tunes anything is a backtest wearing a costume, and it re-introduces exactly the search that
produces negative out-of-sample performance. The freeze makes the rule checkable: a book that
changed on paper has restarted its paper record.

**Months on paper cannot show skill.** Proving a good information ratio takes years, not a
quarter, so the daily record is read for whether the book behaves like its backtest — turnover,
holdings, exposure, costs — and never for a good month. What months can show is the plumbing,
which this step exists to find before money does.

## Running it daily

Once `Paper_Trading/promote.py N` has frozen a book, try `Paper_Trading/daily_update.py` by hand
first, from the strategy's folder:

```bash
uv run python Paper_Trading/daily_update.py --dry-run
uv run python Paper_Trading/daily_update.py
```

The first refreshes the prices, unless `--skip-refresh` is given, then checks, runs and prices
everything but writes no record. The second writes the record; running the same day twice replaces
that day's rows instead of adding to them.

**Where it reads and writes** is set in `Config/.env`:

| Line | Values | What it does |
| --- | --- | --- |
| `PAPER_TRADING_INPUT` | `provider` or `database` | `provider` downloads the day's prices here, with the data key; `database` reads the prices another machine published, with no download and no data key |
| `PAPER_TRADING_SINKS` | `local`, `database`, `local,database` | `local` writes the record as CSV files in `Paper_Trading/Record/`; `database` writes the same tables to the database |
| `PAPER_TRADING_DATABASE` | a file, or `postgres:<connection string>` | a DuckDB file, by default `Paper_Trading/paper_trading.duckdb`; or a PostgreSQL server, reached through DuckDB |
| `PAPER_TRADING_PUBLISH_DATA` | `true` or `false` | with the database sink, also writes the refreshed prices there, for the machines that read them |

`--input` and `--sinks` override the first two lines for one run; `--as-of` runs a past day, and
`--book` one book. **A local record is not a backup**: the provider restates its history, so a
day's inputs cannot be fetched again as they were. Keep the database sink on, or back the folder
up.

**A book's frozen security master travels by hand.** Kept out of git, it stays on the machine that
froze the book. Back it up with the record, and bring it across before the first run anywhere
else: the run checks every frozen file against its hash in `FREEZE.json`, and stops a book whose
files are missing or changed.

**Schedule it** after the US close, once the provider has the day. On Windows, run this once in
Command Prompt; in PowerShell, start it with `schtasks --%`, and in Git Bash with
`MSYS_NO_PATHCONV=1 schtasks`:

```bat
schtasks /Create /SC WEEKLY /D "MON,TUE,WED,THU,FRI" /ST 19:00 /TN "<strategy-name> daily update" /TR "cmd /c uv run --directory \"<full path of this folder>\" python Paper_Trading/daily_update.py >> \"<full path of this folder>\Paper_Trading\Logs\scheduled.log\" 2>&1"
```

On macOS or Linux, add one line with `crontab -e`, in the machine's own time zone. `cron` does not
read your shell's `PATH`, so give uv by its full path, which `command -v uv` prints.

```bash
0 19 * * 1-5 cd "<full path of this folder>" && "<full path of uv>" run python Paper_Trading/daily_update.py >> Paper_Trading/Logs/scheduled.log 2>&1
```

The run's log is in `Paper_Trading/Logs/`, one file per day. A day whose log does not end in
`done, exit code` is one to read. The redirect keeps in `scheduled.log` what the run prints outside
that log: the download, and an error raised before the log opens. The folder exists once the run
has been tried by hand, as above.

The licensed engine checks its licence online. Without the network, a saved check stands in for 3
days from Backtest Engine 0.67.0, or 7 on 0.66.0, so the machine needs the network that often, and
for its first run on 0.67.0, which does not read the older saved check.

> **For the agent.** Registering a scheduled task changes the machine: give the command and let
> the user run it. Never read the record's figures back as your own: they are the engine's, and
> you quote them with the file they came from.

## Before a book's first day

Each graduated book gets a section in *Current status*, written and committed before
`daily_update.py` first runs it, and never edited afterwards: a later observation is a new line
under it, dated. It holds:

- the experiment it mirrors, the variant, the commit and the freeze date;
- the gate, row by row, both layers, and the sign-off: a person's name and date, in one line,
  `Signed off by <name> on <YYYY-MM-DD>, as <outcome>`, the outcome *graduating* or *sound and
  regime-dependent, on paper on probation*: `promote.py` freezes no book without it;
- **the bands**: for each diagnostic `daily_update.py` reads, the range `FINDINGS_N.md` measured
  over the backtest, which the book's `BANDS` carries too;
- **the kill switch**: the result that retires the book instead of tuning it;
- for a book on probation, **the regime prediction** — where it should earn and where it should
  lag, from its findings — and **the probation**: its length, at least 12 months, its review date
  and the benchmarks it is read against, its index and its control. `promote.py` looks for each,
  the bands and the kill switch too, as a bold label in the section;
- the review dates, and the period it has to be watched before anyone proposes production;
- what the record cannot show, said before anyone is tempted to read it there.

## Current status

**In a new strategy, nothing has graduated and nothing has been tested.** The first reading
arrives when an experiment's `FINDINGS_N.md` reports.

<!-- example: begin -->

**Experiment 1 reads as sound and regime-dependent, and goes to paper on probation as
`Paper_Trading_1`, on the owner's sign-off of 2026-10-27.** It does not graduate: over 2000-01-03
to 2026-08-14 at the flat 5 bp row, every soundness criterion holds, P1 and P3 fail and P2 is not
evidenced; against the KN US Equity Core and its control the book earned in 2018–2026, lost to the
Core in 2000–2008 while it beat its control, and lost to both in 2009–2017. Its gate in both
layers, its regime prediction and the terms of its probation are registered in *Paper_Trading_1 —
Experiment 1, on paper on probation* below, before its first day; the gate as its blueprint wrote
it, five criteria read on 2026-10-24, follows that section.

**The periods, named before the run.** The blueprint judges the book in three sub-periods,
2000-01-03 to 2008-12-31, 2009 to 2017 and 2018 to 2026-08-14, each priced from its first
rebalance date; the flat row in brackets:

| Sub-period | Rule Sharpe | Control Sharpe | Core Sharpe | Rule CAGR | Core CAGR | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2000–2008 | −0.569 (−0.506) | −0.629 (−0.611) | −0.303 | −13.68% (−11.71%) | −3.41% | **failed**: beats its control, loses to the Core |
| 2009–2017 | 0.699 (0.763) | 0.805 (0.827) | 0.837 | 11.80% (12.83%) | 14.39% | **failed**: loses to its control and the Core |
| 2018–2026 | 0.772 (0.819) | 0.743 (0.764) | 0.579 | 24.91% (26.24%) | 14.19% | **earned**: beats its control and the Core |

**The condition that tells them apart, as far as the evidence goes: whether the most traded names
were the ones still rising.** The most traded members in 2000 were the technology and telecom
names of the bubble; ranked and weighted by what they traded, the book held them into the fall, and
a cross read once a month left late. Before any book, the analyzer had measured the same split: the
traded-value rank on the pool, over a year, read −0.0504 in 2000–2008 and +0.0825 in 2018–2026
(`RESULTS.md`, *Before any experiment*, row 8). That describes the window; it does not say which
period comes next.

<!-- example: end -->

When one does, record it here: which experiment, which variant, each criterion of both layers with
its evidence, and the outcome it reaches. Above all, record which criteria do not hold and why:
**the blocking items are the content of this section, not the passing ones.** A sound,
regime-dependent experiment names its periods and the condition between them, and its sign-off row
reads the owner's name and date when they put it on paper on probation, else *not sought*; one
that is not sound names the soundness row that failed and what will be
fixed.

**A frozen book's folder is named for the experiment it mirrors.** The template ships
`Paper_Trading_1/` as that contract: it becomes Experiment 1's frozen book if Experiment 1
graduates or goes on probation, a later experiment takes its own number, and until one does, the folder
holds the contract and nothing else.

<!-- example: begin -->

### Paper_Trading_1 — Experiment 1, on paper on probation

**Registered on 2026-10-27, before `daily_update.py` first runs the book, and never edited
afterwards: a later observation is a new line under it, dated.** The folder's earlier book, on FMP
data, retired on 2026-10-24, keeps its own section below.

- **What it mirrors.** Experiment 1 as `experiment_1_marimo.py` ran it on 2026-10-24, from
  `BLUEPRINT_1.md` of 2026-10-23: on the first trading day of each month, at the open, the KN US
  Equity Core members at the prior close with a 200-day history, the golden cross — the 50-day
  average above the 200-day — at 1, a 63-day traded value then and an open that day; ranked and
  weighted by 63-day traded value, none above 20%, added in rank order while the smallest weight
  stays at or above 1%; a held name whose target moved by half a point or less left as it drifted;
  the rest in US dollar cash, paid FRED's `DFF` less half a point; a delisted holding sold by the
  engine at its last price; `FPS`, `H1`, `ILA.A`, `MDLN`, `Q`, `SUNB` and `TXCCQ` excluded by name.
  Its control, the same rule without the cross's sign, on the rule's own dates under the same band,
  is priced beside it every day. **The variant is the flat 5 bp row**, the row the gate is read at:
  commission 1 bp of the notional, a flat 5 bp half-spread, a 1% cash reserve, on $1,000,000.
  **No regime filter**: the book is the experiment's, unchanged.
  `Paper_Trading_1/paper_trading_1.py` carries the rule; `Paper_Trading_1/FREEZE.json` names the
  commit it is frozen at — the commit of this section, which the first dated line under it
  records — the freeze date, 2026-10-27, the hash of every frozen file and the sign-off below.
- **The gate, both layers**, from
  [`../Experiments/Experiment_1/FINDINGS_1.md`](../Experiments/Experiment_1/FINDINGS_1.md), *The
  gate, in two layers*, read on 2026-10-27 from the run of 2026-10-24 on Backtest Engine 0.67.0 and
  Attribution Analysis 0.5.0, at the flat 5 bp row:

  | # | Criterion | Reading | Evidence, as the findings give it |
  | --- | --- | --- | --- |
  | S1 | No survivorship bias | **holds** | the universe is the KN US Equity Core's members as of each date, priced by Sharadar to each name's last trade; the share of the Core no price covers is 0.11% on its worst day; the window was fixed by the universe notebook's coverage rule before any rule existed, the Core priced and signalled at 96.5% on its worst day in the window. Stated, not settled: the Core's history before its live date is a backtest of its own rules |
  | S2 | No look-ahead | **holds** | everything the rule reads on a rebalance date is read at the close before it and filled at the next open; the blueprint, its rule and its predictions were written on 2026-10-23, before the rule cell held a line of this version; every invariant of the notebook's section 2.1 is raised in its Verify |
  | S3 | No overfitting | **holds**, with what it discloses | the trial count, 152 books, is published, the flat-row re-pricing named a forking path and **the deflated Sharpe not computed**; the sweep read as a curve, the cross's margin over its control positive at every setting, +0.06 to +0.12 Sharpe; 19 of the 20 random books priced whole, random book 17 excluded by name |
  | S4 | Costs and capacity stated | **holds** | one-way turnover 2.16 a year; commission, slippage and cash interest at the pre-registered, flat, stress and $100,000 rows; 348 engine orders a year; capacity at 1% of a name's 63-day traded value, the worst trade $25.9M; the rule at $100,000 excluded, a cash error on 2003-01-31 |
  | S5 | Reproducible | **holds** | the pipeline ran from a working copy whose data folders were emptied first, and every notebook reached the end of its Verify section, the experiment's 71 checks |
  | P1 | Beats the benchmarks and its control, over the whole window | **fails** | Sharpe 0.221 against the Core's 0.315 and `SPY`'s 0.313; the control margins, +0.105 Sharpe and +2.24 points of CAGR, and 2 of 3 sub-periods hold |
  | P2 | Idiosyncratic alpha in both layers | **not evidenced** | the first cut's benchmark reconciles to 0.22 points a year; the first cut's selection is −73.2, the idiosyncratic +285.0, residual selection +6.7; the rule beats 15 of the 19 random books priced whole, where the bar is 16 of 20 |
  | P3 | Survives perturbation | **fails** | 8 of 8 settings keep the sign of their margin over their own control; 0 of 8 beat the Core |

  **The outcome: sound and regime-dependent.**
- **The sign-off.** *Signed off by Arturo Aguilar on 2026-10-27, as sound and regime-dependent, on
  paper on probation.* The deflated Sharpe is not computed (S3).
- **The regime prediction.** From `FINDINGS_1.md`'s sub-periods at the flat row, each priced from
  its first rebalance date, and stated before the paper period:
  - **It should earn where the most traded names are the ones still rising**, as in 2018–2026: a
    Sharpe of 0.819 against the Core's 0.579 and the control's 0.764, 26.24% a year against 14.19%
    and 25.45%.
  - **It should lag the Core in a fall the most traded names lead**, as in 2000–2008, when the
    bubble's names were held into the fall and a monthly cross left late: −11.71% a year against
    the Core's −3.41%, a Sharpe of −0.506 against −0.303 — **and still beat its control**, −19.05%
    and −0.611, the cross cutting the drawdown over the window to −78.4% against −91.0%.
  - **It should lag both in a broad recovery**, as in 2009–2017, where the analyzer found the cross
    carrying almost nothing on the pool (−0.0027 and −0.0009 at 21 and 63 days): 12.83% a year
    against the control's 16.29% and the Core's 14.39%, a Sharpe of 0.763 against 0.827 and 0.837.
  - **It does not say which comes next.** The findings name these periods after the fact, and no
    condition that could be read in advance tells them apart: that is why the book goes on paper
    with no regime filter.
- **The probation.** 12 months on paper, from the freeze date, to **the review of 2027-10-27**,
  read against the KN US Equity Core and against its control, the same rule without the golden
  cross. **Paper alone never sends it to production**: at the review the owner reads the book
  against the index, the control and the regime prediction above, and decides — continue, stop, or
  a new experiment. The record's behaviour — holdings, orders, invested share, flags — is read on
  2027-01-27, 2027-04-27 and 2027-07-27, each reading a dated line under this section; no
  performance figure is read for a decision before 2027-10-27.
- **The bands**, which `BANDS` in `paper_trading_1.py` carries, from `FINDINGS_1.md`'s structural
  table: names held from 19 to 58; the invested share from 92.8% to 100%; at most 75 rule orders on
  a rebalance date; the largest target weight up to 20%, the rule's own cap; and no held name with
  its cross at 0 at the close before the last rebalance, which the experiment's invariants never
  allowed. The record keeps, with no band: effective names (24.1 on average over the backtest), the
  names the band left alone on the last rebalance date (a median of 31), the largest sector's
  share, the trade dates in the last 63 days, and whether the book traded that day.
- **The kill switch: the blueprint's falsifier, read on paper days, at the flat row.** The book is
  retired, never tuned, if over its paper days it misses its control by +0.03 of Sharpe or by +0.5
  points of CAGR. **Read first at the review of 2027-10-27**, and at each anniversary after if the
  owner continues it; before then no performance figure retires or promotes it, and the bands only
  flag. Proposed from `BLUEPRINT_1.md`'s *What would falsify it* and confirmed by the owner on
  2026-10-27.
- **What the record cannot show.** Skill: a year of paper cannot show an information ratio, as
  *What a paper-trading run is* says. The regime: a year is one draw of one market, and a year
  that looks like 2018–2026 or like 2000–2008 neither confirms the prediction nor says which
  regime comes next. What the backtest already priced: the book is priced from the experiment's
  first day, and every figure to 2026-08-14 is the experiment's own window; the record reports the
  days after it and the days since the freeze apart, each from its first rebalance date. The cost
  row: the flat 5 bp half-spread is an assumption, since the spread on the most traded US stocks is
  still open (`FINDINGS_1.md`, *What is open*, item 1). And the index as it is: the desk's files end
  on 2026-08-14, so until they are refreshed membership is held at that date and the book is
  priced against `SPY`, each day flagged; the frozen seed fixes the universe, so a name that joins
  the index after the freeze can never be held.

**2026-10-27.** Frozen by `promote.py 1` at commit `0041695`, the commit of this section, on paper
from 2026-10-27, the sign-off in `FREEZE.json`; `BOOKS` in `daily_update.py` names it from the
commit after.

*In this copy of the worked example*, the section above, registered in Golden Flow's own repository,
keeps its words. The earlier FMP book's section it points to stands there, at tag `0.15.2`, not in
this copy, which carries the book on probation alone.

### Experiment 1: the gate as its blueprint wrote it

`BLUEPRINT_1.md` registered the gate in the template's earlier form, five criteria, before the
two layers existed, and its rows map onto them: criterion 1 is P1, criterion 2 is P2, criterion 3
is P3 with S3's sweep, criterion 4 is S4 and criterion 5 is the sign-off; its success criterion 2,
the run from a wiped working copy, is S5. Read on 2026-10-24, as the record has it:

| # | Criterion | Pre-registered costs | Flat 5 bp re-pricing | What blocks it |
| --- | --- | --- | --- | --- |
| 1 | Beats the benchmarks and its control | **fails** | **fails** | the control limb holds (+0.065 / +0.105 Sharpe, 2 of 3 sub-periods); the book's Sharpe, 0.162 / 0.221, is below the Core's 0.315 and `SPY`'s 0.313, the whole shortfall in 2000–2008 |
| 2 | Idiosyncratic alpha in both layers | not evidenced | not evidenced | the reconciliation holds (0.22 points a year); by KN sector, compounded, the first cut's selection is −73, the idiosyncratic +285 and the residual selection +6.7, and the rule beats the 3 random books priced whole at the base costs and 15 of 19 at the flat row, against a bar of 16 of 20 (Attribution Analysis 0.5.0) |
| 3 | Survives perturbation | not evidenced | **fails** | every priced setting keeps its margin over its own control; none beats the Core on Sharpe |
| 4 | Costs and capacity stated | holds | holds | — |
| 5 | Sign-off | not asked | not asked | 1 and 3 fail |

**The owner reads the gate at the flat 5 bp row** (2026-10-24). Why a second row exists: the
pre-registered slippage read a megacap's daily range as spread (about 23 bp a trade), so every book
was priced again at the blueprint's own 5 bp fallback, a forking path counted in the trials. The
verdict does not depend on it: criterion 1 fails at both.

<!-- example: end -->
