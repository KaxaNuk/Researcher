---
name: paper-trading-gate
description: >
  Load this skill whenever a KaxaNuk Strategy Template repository asks whether an experiment
  graduates to paper trading, step 7 — `Paper_Trading/BITACORA.md`, `promote.py`, `daily_update.py`,
  `record.py` and `Paper_Trading_N/paper_trading_N.py`. Use it when the user asks what the
  graduation gate is, how its soundness criteria S1 to S5 and its performance criteria P1 to P3 are
  evidenced, which of its three outcomes a `FINDINGS_N.md` reaches — graduates, sound and
  regime-dependent, or not sound — how a graduated book is frozen, what the daily run does and where
  it writes, what is registered before day one, why the parameters are frozen, what a promoted
  experiment's folder is named, or what the gate's status section should hold. It covers both
  layers and the usual ways each criterion fails, the outcomes, the freeze, the daily run, and what
  the assistant never decides. It does NOT cover the cycle that produces the findings (use
  `backtest-engine-runs`, `attribution-analysis-runs`, `alpha-decomposition`), the documents of an
  experiment (use `experiment-lifecycle`), or step 8, Production, which is outside the repository.
metadata:
  version: 0.5.0
---

# The paper-trading gate — what graduation means, and what has to be true first

**In plain words:** a dress rehearsal on data nobody has seen yet. **It produces** out-of-sample
evidence and an operations checklist. **It prevents** finding the plumbing problems on day one of
funding.

A backtest says what a rule *would* have done; paper trading says what it *does*, on live prices,
with live universe changes, and with the delistings and corporate actions a historical file has
already tidied up. `Paper_Trading/BITACORA.md` is **the gate, not a log** — a contract that says
what graduation means and what has to be true before it happens. It is named apart from
`JOURNAL_N.md` so the two are never confused. Step 8, Production, is not here: a strategy leaves
the repository when it is funded.

## When to Use

- The user asks whether Experiment N graduates, or what would have to be true for it to.
- The user is filling the gate's *Current status* section, or writing a `paper_trading_N.py`.
- A `FINDINGS_N.md` reports, and the question turns to what comes next — whether it beats its
  benchmarks or not, since a book that loses over the whole window can still be sound.
- The KaxaNuk Researcher's `challenge` command reaches the gate: it reads `BITACORA.md` only when
  graduation is being claimed, and this skill is how the criteria are read.

## The gate: two layers, three outcomes

Strong backtest results are necessary and **not sufficient**, and they are read second. The gate
asks two questions in order: **is the experiment done correctly**, and only then **does it earn
its place**. Every criterion is evidenced from the experiment's `FINDINGS_N.md` and from
`RESULTS.md`; **a row without evidence does not hold.**

### Soundness — is the experiment done correctly?

Each row cites its evidence; a row without evidence does not hold.

| # | Soundness criterion | Evidenced by | The usual way it fails |
| --- | --- | --- | --- |
| S1 | **No survivorship bias** | the point-in-time universe: departed names kept in the seed, the security master, the usable date | a seed of today's members; departed names the provider does not price dropped without their share of the index published; a window opened before the date the universe can be priced |
| S2 | **No look-ahead** | signals lagged, next-open fills, the blueprint's rule and predictions registered before any result | a signal struck on the same close it trades at; a `current_*` column selected on; a blueprint committed with or after the rule cell, or a prediction added once a number was seen |
| S3 | **No overfitting** | the trial count published, the sweep read as a curve, the control and the random books priced | a count nobody wrote down; a single best cell read instead of the curve; a setting the blueprint said may not rescue the experiment moved after the result and counted as an edit rather than a trial; a control on its own dates, which differs in two things; random books truncated and never priced whole |
| S4 | **Costs and capacity stated** | turnover, commission, slippage, cash, and every assumption the engine does not model | costs modelled, capacity not stated; a cost model that misreads the book's names, with no second row beside it; borrow cost of a long/short book in a footnote |
| S5 | **Reproducible** | the pipeline ran from a working copy whose data folders were emptied first, every Verify passing | a figure from a run on yesterday's cache; a Verify section skipped, or one that prints rather than raises; a truncated engine run neither read whole nor excluded by name |

### Performance — does it earn its place?

| # | Performance criterion | Evidenced by | The usual way it fails |
| --- | --- | --- | --- |
| P1 | **Beats the benchmarks and its control on risk-adjusted return, over the whole window** | the ranking table of `FINDINGS_N.md`, and the control `BLUEPRINT_N.md` names in its *Rules* — the same rule with one ingredient removed — on the rule's own rebalance dates | a pass on Sharpe alone while the control earns more a year on the same dates; a book that beats its control and loses to its index, which holds the control limb and fails the criterion |
| P2 | **Attribution shows idiosyncratic alpha in both layers** — selection in the Brinson-Fachler cut, a residual the factor model cannot explain, and a selection story that survives the third pass on residual returns | the attribution section of `FINDINGS_N.md`, read with `alpha-decomposition` | the residual is there but random books of the same shape earn most of it; the third pass was never run. Expect *a pass with a qualification*: a book half factor, half idiosyncratic has passed and been told how much of it is not the idea |
| P3 | **Conclusions survive parameter perturbation** | each setting of the blueprint's sweep, priced with its own control | the margin keeps its sign at every setting and no setting beats the benchmark; one setting carries the result and its neighbours do not |

Soundness is read first because a performance criterion on an unsound experiment means nothing:
a survivor-biased universe or a rule that saw the future produces a P1 pass by construction.
**S3 is where the trial count lives**, the minimum against overfitting; the sign-off states whether
the deflated figure was also computed.

P2 is evaluable here because the stack has a real attribution stage. A repository without one would
have to name a substitute — a beta-matched control book, a regression on the market — and here there
is no substitute to name, which means there is also no excuse.

### The outcomes

- **Graduates** — every soundness and performance criterion holds, and the owner signs it off in
  `BITACORA.md`: the book is frozen and paper traded.
- **Sound and regime-dependent** — every soundness criterion holds; performance fails over the
  whole window but holds in named periods. The findings name the periods where it earned and where
  it failed, and the condition that tells them apart as far as the evidence goes. It may go to
  paper **on probation**, on the owner's sign-off: frozen unchanged, with its regime prediction, a
  period of at least 12 months and its review date registered in `BITACORA.md` before day one, and
  read at the review against its index and its control — continue, stop, or a new experiment.
  **Paper alone never sends it to production.** Otherwise it may be paired with another signal in
  a later experiment, or used at a portfolio manager's discretion — the decision, and its risk, are
  theirs. Never a recommendation.
- **Not sound** — a soundness criterion fails: no conclusion is drawn; fix it and run again.

The sign-off stays a person's name and date. The assistant never decides a gate.

**A named period is one the blueprint or the analyzer fixed before the result** — the thirds a
blueprint judges sub-periods on, say — never one cut afterwards around where the book did well. A
period chosen after the result is a forking path: it goes in the trial count, and the reading says
so. The condition that tells the periods apart is stated as far as the evidence goes — what the
book held, what the market did — and never as a forecast of which regime comes next.

## The promotion

An experiment is **promoted, not copied**: one that graduates, or one a person signed off as sound
and regime-dependent, on probation.
`Paper_Trading/Paper_Trading_N/` mirrors the `Experiment_N` it came from, so the lineage of a
paper-traded book is never in question; the experiment's notebook stays where it is, as the record
of how the rule was chosen. The template ships `Paper_Trading_1/` as the contract of a frozen book,
named for the experiment it would mirror: it becomes Experiment 1's book if Experiment 1 graduates
or goes on probation, and a later experiment takes its own number. The worked example has no book on
paper: its Experiment 1 reads as sound and regime-dependent.

A strategy's `1.0.0` waits for more than its first graduation: the changelog reserves it for this
strategy's first book on paper trading, its results reproduced from a clean clone.

## The freeze

A graduated book is the strategy, frozen. After the sign-off, the rule is written into
`Paper_Trading_N/paper_trading_N.py` from the experiment's cells and committed. Then
`Paper_Trading/promote.py N`, on a clean tree, copies byte for byte from that commit every file the
book needs — the refinery and its calculations, the reader of the Analytics Factory's files, the
shared modules the rule calls and the seed — into `Paper_Trading_N/` in the strategy's own layout,
with the security master from disk. It writes `FREEZE.json`: the commit, the freeze date, the hash
of every file, the library versions, and the hash of what it cannot copy, the Curator's
calculations. The security master is the provider's data, so `.gitignore` keeps the book's copy out
of git: it stays on the machine that froze the book, backed up with the record, and is brought
across by hand to any other machine that runs it. Every module resolves its paths from its own
folder, so the copies read and write inside the book's folder: an experiment under construction can
change the shared modules and the book never moves. A frozen book is never frozen again; a new
freeze is a new book, with its own number.

**The days after the window are the first any code reads**, so the book is tried once before the
real freeze — frozen in a scratch clone, never committed, and run with `--dry-run` for a day past
the window — and two faults show only there. Membership built only from the dates an index's
holdings cover has no member past their last date, so a book reading it that way sells every name
the day those files end: it holds the last membership they wrote, as `paper_trading_N.py`'s
contract says. And a seed span closed on its source's last date stops every live name on that
date: `universe-point-in-time` says why a live listing's span stays open.

## What a paper-trading run is

Not a notebook: `daily_update.py`, run on a schedule after the close, because the question is no
longer *what would this have done* but *what does it hold today, and how is it doing*. It refreshes
the shared raw prices once, or reads what another machine published. It checks the newest day and
stops every book on a close with no fill price or a move no price can make. It runs each book in
`BOOKS` — its frozen refinery, its frozen rule from the experiment's first day, and the engine
three times, over the whole history, the days after the experiment's window and since the freeze.
It writes the record through `record.py` to local CSV files, a DuckDB database or both, as
`Config/.env` says. It exits 0, 1 or 2 — clean, flagged, failed. A step that raises is a failed
day, exit 2 with its traceback in the day's log: Python's own exit code for it is 1, which a
scheduler reads as flagged. A frozen file missing or changed, or a shared input that no longer
matches `FREEZE.json`, stops the book with `unfrozen-input`.

**A library upgrade is a change to every frozen book.** The Data Curator's version is a shared
input: upgrading it in the strategy stops every frozen book with `unfrozen-input`. The Backtest
Engine's version is recorded in `FREEZE.json` but not enforced, so an engine upgrade reprices the
record, and what it moves shows as restatements. Neither upgrade is made without the owner's go,
and a book that must move to a new build is frozen again as a new book, with its own number.

**What the checks do not see.** They read each file's newest day alone: a security's file that
ends before the day, or a bad bar on a day between two runs — an unadjusted corporate action, say —
passes unflagged, and the book reads it. And a book flagged every day, by a hand-supplied file
behind the day, hides a new flag among the old ones: read the flags, not only the exit code.

The record has six tables — runs, books, performance, statistics, diagnostics, flags — keyed so a
second run of a day replaces that day's rows. A past value the engine now prices differently is a
**restatement**: flagged, never overwritten. The template ships these files as their contract in a
docstring; the worked example carries them working, with no book in `BOOKS`.

**A paper-trading script re-fits nothing.** A run that tunes anything is a backtest wearing a
costume, and it re-introduces exactly the search that produces negative out-of-sample performance.
And **months on paper cannot show skill**: the daily record is read for whether the book behaves
like its backtest — turnover, holdings, exposure, costs — never for a good month.

## Before a book's first day

`BITACORA.md` gets a section for the book, committed before its first run and never edited. It
holds the experiment, variant, commit and freeze date; the gate row by row, both layers, with the
sign-off; the bands for each diagnostic, from `FINDINGS_N.md`'s structural table and carried as
`BANDS` in the book; the kill switch; the review dates and the period to watch before production;
and what the record cannot show.

**A book on probation registers more**, in the same section, before day one: its regime
prediction — where it should earn and where it should lag, each with the figure from
`FINDINGS_N.md` it rests on; its period, at least 12 months unless the owner registers another, and
the review date; the benchmarks it is read against, its index and its control; and that paper
alone never sends it to production. At the review the owner reads it against those and decides:
continue, stop, or a new experiment. The prediction is the findings', stated before the paper
period, never cut afterwards around where the book did well.

## The status section

*Current status* in `BITACORA.md` is the gate's record. Until an experiment reports it says so —
*nothing has graduated and nothing has been tested*. When one reports, record which experiment,
which variant, each criterion of both layers with its evidence, and the outcome it reaches. Above
all, record **which criteria do not hold and why: the blocking items are the content of this
section, not the passing ones.**

- **Graduates:** every row holds, and the sign-off is a person's name and date.
- **Sound and regime-dependent:** every S row holds; each P row that fails says so, and beside it
  the named periods where it earned and where it failed, and the condition that tells them apart.
  The sign-off row reads the owner's name and date when they put it on paper on probation, with
  the probation's terms; else *not sought*.
- **Not sound:** the S row that fails, and what will be fixed before the next run. No P row is
  read.

The worked example's *Current status*, Experiment 1 read row by row with its evidence, is the shape
to follow for the second outcome.

## What the assistant never does here

- **Decide a gate.** The assistant lays both layers out, each row evidenced or not, names the
  outcome the rows reach and stops; the reading and the sign-off are a person's.
- **Recommend a sound, regime-dependent book** — for probation, for a portfolio, or for a period it
  might earn in. Probation is the owner's decision; pairing it with another signal is a later
  experiment's blueprint; using it at discretion is a portfolio manager's decision and risk.
- **Move a book on probation toward production.** Paper alone never does: at its review the owner
  decides to continue, stop, or start a new experiment.
- **Compute a performance number**, a deflated Sharpe included. Every figure is quoted from
  `FINDINGS_N.md` or `RESULTS.md` with its source; a missing one is a re-run to ask for, never a
  value to supply.
- **Read a criterion as met on a number the findings do not carry.** Capacity not stated is S4
  *not met*, not *probably fine*.
- **Name a period after the result** to make a book regime-dependent.
- **Re-fit, re-tune or widen a rule** in a paper-trading script, whatever the reason offered.
- **Freeze a book before the sign-off, or freeze one twice.**
- **Register the scheduled task.** It changes the machine: the command is given, the user runs it.
- **Read the record's figures back as its own.** They are the engine's, quoted with their file.
- **Touch step 8.** Nothing here deploys, executes or moves money.

## References

- `Paper_Trading/BITACORA.md` in the worked example, `examples/strategy/golden-flow/` in the KaxaNuk
  Researcher package — the gate read once, both layers, every row evidenced from `FINDINGS_1.md`:
  S1 to S5 hold; P1 and P3 fail over 2000–2026 and P2 is not evidenced; the book earned in
  2018–2026 and lost in 2000–2008. Sound and regime-dependent, read on the owner's word of
  2026-10-27, and not paper traded. Its `promote.py`, `daily_update.py` and `record.py` are the
  working step-7 scripts, with no book in `BOOKS`. The template's copies are the same files with
  the example's lines removed.
- The strategy's `AGENTS.md`, *Research integrity — the five ways a backtest lies* and *What
  attribution must report*, which S1 to S4 and P2 rest on.
- `CHANGELOG.md` in the strategy, *What a version number means here* — `1.0.0` and the gate.
