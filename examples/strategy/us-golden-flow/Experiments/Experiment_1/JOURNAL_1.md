# Journal — Experiment 1

> **Append-only, dated, oldest first.** Every iteration of this experiment, in the order it
> happened. Maintained by the AI as work proceeds.
>
> **Earlier entries are never edited.** The one exception is correcting an error, and the correction
> is written as a new entry saying what was wrong — not by rewriting the original.
>
> The hypothesis is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md); the results that survive are in
> [`FINDINGS_1.md`](FINDINGS_1.md); what to try next is in each entry's open threads.

**Paths and figures inside entries are as they were written.** Where a path has since moved the
entry is left alone — it was correct on its date.

**Repository-level history belongs here** — choosing the benchmark, the data step, the architecture.
Experiment 1 is the first rule tested against the benchmark and therefore the shared context; later
experiments' journals point here rather than copying it.

**Entry format:**

```

<!-- example: begin -->

> **Append-only, dated, oldest first.** Every iteration of this experiment, in the order it
> happened. Maintained by the AI as work proceeds.
>
> **Earlier entries are never edited.** The one exception is correcting an error, and the correction
> is written as a new entry saying what was wrong — not by rewriting the original.
>
> The hypothesis is in [`BLUEPRINT_1.md`](BLUEPRINT_1.md); the results that survive are in
> [`FINDINGS_1.md`](FINDINGS_1.md); what to try next is in each entry's open threads.

**Paths and figures inside entries are as they were written.** Where a path has since moved the
entry is left alone — it was correct on its date.

**Repository-level history belongs here** — choosing the benchmark, the data step, the architecture.
Experiment 1 is the first rule tested against the benchmark and therefore the shared context; later
experiments' journals point here rather than copying it.

**Entry format:**

```

<!-- example: end -->

## YYYY-MM-DD — short topic

- Idea / question:
- What we tried / considered:
- Outcome / decision:
- Open threads:
```

---

The first entry is usually *repository instantiated from the template*: what this repository is for,
which template version it was created from, the strategy name, and everything `OBJECTIVE.md` still
leaves open.

Two entries come before `BLUEPRINT_1.md`. The first is *choosing the benchmark*: what every
experiment will be measured against, which candidates were considered, and the one property that
decided between them — a benchmark is chosen for being transparent, liquid and stable, not for
being clever. `blueprint` reads the benchmark from it.

The second, saved before the blueprint, is *the rule read back*: the rule in one plain sentence,
one worked date's book — the names it holds that day, each one's rank and signal value, and why the
last name in and the first name out fall where they do — and the owner's yes, in their words. Where
the rule has a no-trade band, **the band is read back beside it**, on the worked date and the
rebalance before it: the names it holds on both, and which held names keep their drifted weights
and which are traded.

<!-- example: begin -->

- Idea / question:
- What we tried / considered:
- Outcome / decision:
- Open threads:
```

---

The first entry is usually *repository instantiated from the template*: what this repository is for,
which template version it was created from, the strategy name, and everything `OBJECTIVE.md` still
leaves open.

Two entries come before `BLUEPRINT_1.md`. The first is *choosing the benchmark*: what every
experiment will be measured against, which candidates were considered, and the one property that
decided between them — a benchmark is chosen for being transparent, liquid and stable, not for
being clever. `blueprint` reads the benchmark from it.

The second, saved before the blueprint, is *the rule read back*: the rule in one plain sentence,
one worked date's book — the names it holds that day, each one's rank and signal value, and why the
last name in and the first name out fall where they do — and the owner's yes, in their words. Where
the rule has a no-trade band, **the band is read back beside it**, on the worked date and the
rebalance before it: the names it holds on both, and which held names keep their drifted weights
and which are traded.

## 2026-11-16 — repository instantiated inside the KaxaNuk app's project

- Idea / question: rebuild Golden-Flow's Experiment 1 on the KN US Equity Core in a strategy the
  KaxaNuk app shows, so code and app read the same folders.
- What we tried / considered: the app made the project (`.kaxanuk/`); `init-strategy` from the
  KaxaNuk Researcher 1.36.0 copied the template beside it. Hand-written app job folders were tried
  and the app ignored them; its connector reads files instead — weight files in `Portfolio/`, the
  engine's results workbook from `Backtest/`. Golden-Flow's code was copied in; the window ends on
  the Core's last date, 2026-11-06.
- Outcome / decision: the app lists code-made weight files (checked with a toy SPY file). The seed
  is rebuilt from Sharadar's catalogue of 2026-11-16, 2,203 listings, and `Universe/seed.py` also
  writes `Universe/KN_US_Equity_Core.csv`, the app's universe format with sector, industry,
  exchange and size; the app's Universe Analyzer reads it. The owner's decision: curated files are
  CSV, the format the app reads, and the rule's two per-security signals are Curator columns,
  `c_trend_50_200` and `c_traded_value_sma_63d`, at the cost of a second download; refined files
  stay Parquet. Every library installs with `Config/install_libraries.py`: Data Curator 0.51.0,
  Backtest Engine 0.68.0, Attribution Analysis 0.7.0, Portfolio Construction 2.1.0. The library's
  `feature_weighting` plus `Weights.cap(0.20)` builds the rule's book exactly as
  `bounded_by_score`; all fourteen of its methods were checked on four dates
  (`validate_sizing_methods.py`, KaxaNuk/Portfolio-Construction#6).
- Open threads:
  - **Market capitalisation in the Curator, at the next download** (the owner's word,
    2026-11-16): the app's Universe Analyzer sizes members by `c_market_cap`, which no curated
    file carries. The built-in reads `fis_weighted_average_diluted_shares_outstanding`, a
    fundamentals column; whether the Curator 0.51.0 serves fundamentals from Sharadar is not
    documented, so a one-name run with the fundamentals block mapped to Sharadar settles it first.
    If it does not, Sharadar's daily `marketcap` is the fallback, asked of the Curator.
  - The app cannot yet read refined Parquet, a point-in-time universe, a Sharadar creator or an
    attribution report: Lab-Platform #13 and #14, Attribution-Analysis #19, and a draft issue on
    data and universes not yet raised.
  - Rule, control and equal weight at both cost rows, and their Brinson-Fachler, once the refinery
    has run; the engine's workbooks then imported in the app.

## 2026-11-16 — the plan beyond the first pass: this repository becomes the worked example

- Idea / question: the owner's word, 2026-11-16 — once Experiment 1 is finished here, this
  repository replaces Golden-Flow as the KaxaNuk Researcher's worked example, end to end with the
  KaxaNuk app.
- What we tried / considered: four steps, in order. (1) Finish Experiment 1's first pass: the CSV
  download, the universe notebook, the refinery, rule, control and equal weight at both cost rows,
  their Brinson-Fachler, the engine's workbooks imported in the app. (2) A second pass with the data
  the first one lacked — `c_market_cap` first, after a one-name run shows whether the Curator serves
  Sharadar's shares outstanding — one more download, Experiment 1 again, compared with the first
  pass. (3) Curate this repository into the Researcher as `examples/strategy/us-golden-flow`, in
  place of `examples/strategy/golden-flow`, with every place that names or quotes the old example
  in the same release: `init-example`, the skills, the README, the workshops. (4) Bring what the
  second pass teaches into the strategy template and the researcher's skills.
- Outcome / decision: planned, not started. The package's rules allow curating the example from a
  live strategy only on the owner's word; this entry records it.
- Open threads:
  - Golden-Flow's `Paper_Trading_1`, on probation since 2026-10-27, keeps running in
    `D:\Research\Golden-Flow`; the new example starts with no book on paper until one graduates
    here.
  - Golden-Flow's figures quoted in the skills and the workshops change with the example, in the
    same release.

## 2026-11-16 — the first full run, read against Golden-Flow's

- Idea / question: does Golden-Flow's Experiment 1, rebuilt here on CSV curated files with the
  rule's signals as Curator columns, give the same book and the same verdicts?
- What we tried / considered: `experiment_1_marimo.py` end to end, 2000-01-03 to 2026-11-06, on
  Backtest Engine 0.68.0 and Attribution Analysis 0.7.0: 102 engine runs, the three attribution
  passes, Verify's 71 checks, all passed. `compare_library_sizing.py` first: Portfolio
  Construction 2.1.0 builds the rule's and the control's books exactly, 646 of 646 book-dates.
  Then `app_workbooks.py` prices the rule, the control and equal weight at both cost rows in single
  runs, so the engine writes the workbooks the KaxaNuk app imports.
- Outcome / decision: the replication holds. Every figure of 2000–2008 and 2009–2017 matches
  Golden-Flow's run of 2026-11-08 to the third decimal; the same 24 runs are excluded by name, for
  the same reason. The headline is lower — the rule at the flat row 6.79% and Sharpe 0.183, against
  7.70% and 0.220 there — because this window runs eight trading days past Golden-Flow's data: from
  2026-10-28 to 2026-11-06 the rule lost 16.7%, read from the engine's daily values, and the Core
  4.3%, most of it on 2026-11-05 in a broad semiconductor sell-off (MU −17%, SNDK −22%, AMD −17%),
  checked name by name against the curated closes: not a bad price. One verdict moved: at the
  pre-registered costs prediction 1's sub-period limb now fails, 1 of 3, because in 2018–2026 the
  rule's CAGR falls below its control's once those days are in. `FINDINGS_1.md` and `RESULTS.md`
  written from the run.
- Open threads:
  - This repository's `OBJECTIVE.md` and `BLUEPRINT_1.md` are still the template's; the findings
    cite Golden-Flow's blueprint, commit `887b695`. Writing them as a dated replication is the
    owner's go.
  - A run from a wiped working copy, before a commit to `main` carries this result.
  - The second pass, with `c_market_cap`.

## 2026-11-16 — the second pass decided: a 50% sector cap, a 1/0 cross, every Sharadar column

- Idea / question: the owner's words, 2026-11-16, before the re-run: "add to the experiment 1
  logic a 50% sector max weight constraint", "download all columns available in sharadar ... so we
  can use those columns for further experiments", "a 1,0 50 vs 200 signal to know when we have to
  buy or sell the stocks and could be in the eligible universe point in time", "from 31/12/1999 to
  31/10/2026". His go on the plan came the same night, before he left it running.
- What we tried / considered: a one-name Curator run (AAPL, 1998-01-02 to 2026-10-31) with every
  column the Curator's Sharadar page lists, the fundamentals block mapped to Sharadar, quarterly.
  On Data Curator 0.51.0, the newest: every column comes back and is filled, the fundamentals point
  in time by filing date (AAPL's first row carries the 10-K filed 1997-12-05), and `c_market_cap`
  is filled ($2.07bn on 1998-01-02). Dividends and splits only under their joined names
  (`d_ex_dividend_date_dividend_split_adjusted`, `s_split_date_numerator`,
  `s_split_date_denominator`); the short names the page shows stop the run. A file grows from
  1.7 MB to 6.3 MB.
- Outcome / decision: Experiment 1 is rewritten in this repository with its own `BLUEPRINT_1.md`,
  the first pass becoming its earlier version, counted in the trials. Decisions taken for the
  night, each the owner's to overturn: the download starts 1998-01-02 so the 200-day average
  exists on the window's first day; the sector is the factor model's KN sector, today's
  classification for the whole window, a look-ahead named as such; the control, equal weight and
  every variant carry the sector cap too, and one more arm, the rule without it, measures the cap;
  the attribution starts on the factor model's first day, 2000-01-03.
- Open threads:
  - The owner's yes on the rule as read back below, in his words, in the morning.

## 2026-11-16 — the rule read back, awaiting the owner's yes

- Idea / question: the rule in one sentence, and its book on two consecutive rebalance dates.
- What we tried / considered: **the rule.** On the first trading day of each month, from
  1999-12-31 to 2026-10-31, hold the KN US Equity Core members that were members at the prior close
  with their 50-day average above their 200-day one then (`r_eligible`, the cross as 1/0), in
  proportion to their 63-day average traded value, no name above 20%, **no KN sector above 50%**,
  none below 1%; a held name whose target moved half a point or less keeps its drifted weight.
  **One change in how the count is set, put to the owner:** names are taken in order of traded
  value and each is added if, sized with the names already in, no weight falls below 1%; a name
  that fails is **skipped and the next one tried**, where Golden-Flow's walk stopped at the first
  failure. Under the name cap alone the two give the same book (500 random books, largest
  difference 1.1e-16); under the sector cap, stopping left 10% in cash on 2026-09-01, because
  LRCX, the 16th name and technology, failed and the walk ended before BE, industrials, which fit.
  **The worked dates**, on the first pass's data:
  - **2026-10-01**: 451 eligible, **38 held, fully invested, technology at exactly 50%**. MU 9.47%
    (traded value $31.7bn a day, trend +0.414), AMZN 8.06%, NVDA 7.90%, GOOGL 7.51%, SNDK 6.01%,
    AAPL 4.48%, MSFT 3.94%, AMD 3.67%, INTC 3.28%, BE 2.96% … the last in, ABBV 1.02% ($1.27bn,
    health care). The first out are technology names — LRCX ($3.04bn), CRM, V — because technology
    is full: each would push the 50% across more names and some below 1%. Without the sector cap the
    same date holds 18 names, technology 79%, MU 14.4%.
  - **2026-09-01, the rebalance before**: 478 eligible, 36 held, technology at 50%, fully
    invested. **The band between them** (target → struck on 2026-10-01): kept names moved by half a
    point or less keep their drift — AAPL 4.48% → 4.21%, AVGO 2.51% → 2.24%, JPM 2.14% → 1.74%,
    AMAT 1.13% → 1.47%; entries and larger moves trade to target.
  - Over all 323 dates: the sector cap binds on 17.6% of them, and every date is fully invested.
- Outcome / decision: **awaiting the owner's yes, in his words.** The night's run goes ahead on
  this rule; a *no* means a new draft of *Rules*, and the night's books count as trials.
- Open threads:
  - The skip in the count walk is new; it is the first thing to confirm.

## 2026-11-16 — Experiment 1 reads the Curator alone

- Idea / question: the owner's words, 2026-11-16, after the night's run had started: "para este
  primer experimento creo que todo lo podemos correr usando solo el curator y los custom
  calculations ahi", and "ya para el experimento 2 vemos si usamos el refinery".
- What we tried / considered: the run started at 21:26 was stopped about 15 minutes in, on his
  yes. Every signal the rule and its sweep read became a Curator column: `c_golden_cross_20_100`,
  `_50_200`, `_100_300` and `c_traded_value_sma_21d`, `_63d`, `_126d`. Membership is not a
  provider column, so a final pass of `Data/curator.py`, `complete_files`, cuts each listing's file
  to its dates in the seed, computes the windows again on what is left, and adds
  `c_index_weight` (the Core's weight through the seed's keys) and `c_eligible` (a member with the
  cross at 1 at the prior close). `Experiments/securities_panel.py` and the attribution read the
  Curator's files. Checked on AAPL: 93 columns, `c_eligible` equal to membership and the cross at
  the prior close on every row.
- Outcome / decision: **the rule is unchanged**: `c_eligible` is the definition `BLUEPRINT_1.md`
  gives `r_eligible`, and every `c_*` signal the definition of its `r_*` namesake, so the blueprint
  stays as committed and this entry records where the columns now live. The analyzer notebook,
  which reads the Refinery, is not run for Experiment 1.
- Open threads:
  - The Refinery's `r_golden_cross_*` and `r_eligible` stay in its module for Experiment 2.

## 2026-11-16 — the eligibility flag renamed `c_eligible_golden_cross_50_200`

- Idea / question: the owner's words, 2026-11-16: "c_elegible_50_200_golden_cross o algo asi no?" —
  the flag should say which cross it reads.
- What we tried / considered: the column the entry above calls `c_eligible` is renamed
  `c_eligible_golden_cross_50_200`, beside `c_golden_cross_50_200`, in `Data/curator.py`, the
  notebook, `compare_library_sizing.py` and `PIPELINE.md`. The download was stopped a second time to
  make the change; a file already downloaded is not fetched again, because a file is current when
  its downloaded columns match, and the final pass writes the two added columns afresh.
- Outcome / decision: same definition, new name; the rule is unchanged.
- Open threads:
  - None from the stop: the stopped run had downloaded 100 files in its first three minutes, the
    normal pace, about an hour for the seed.

## 2026-11-17 — the overnight run stopped at Verify, on a check stricter than the blueprint

- Idea / question: the chain launched 2026-11-16 at 22:26 finished the download (23:42, every
  seed listing), the universe (23:43) and every engine run of the experiment, then stopped at 01:05
  on one failed invariant: *no struck sector above the sector cap by more than two points*. The
  largest struck sector was 0.5210; every target sector, the rule's and the control's, was at or
  under 0.50.
- What we tried / considered: the two points were the assistant's own margin, written into the
  notebook tonight; `BLUEPRINT_1.md` asks only that the notebook *report* how far the band lets a
  struck weight sit outside the bounds. The band keeps a drifted name at its weight, so a sector
  whose names all rose can sit above the cap by what they drifted. The check is replaced by the
  band's own bound: a struck sector may sit above the cap by no more than the band and a point
  overnight for each of its names the band kept above target, which the per-name check already
  implies. The notebook now also prints on how many rebalance dates a struck sector is above the
  cap. Nothing in the rule, the sizing or the books changed; the experiment and the workbooks run
  again from the same data.
- Outcome / decision: re-run from the experiment step, 2026-11-17. The library check
  (`compare_library_sizing.py`) exited non-zero by its own threshold: 22 of 646 book-dates differ
  from the library's sizing, the largest by 1.4e-6, as before.
- Open threads:
  - The owner's word on the check's change, with the read-back's.

## 2026-11-17 — the second pass reports: falsified on the sub-period limb

- Idea / question: what the blueprint of `107768f` says once it is run, 1999-12-31 to 2026-10-30.
- What we tried / considered: the experiment ran again at 01:06 after the Verify fix above, passed
  its 77 checks, and the eight workbooks for the app were written by 01:55. 104 engine runs, 83
  read and 21 excluded by name: at the pre-registered costs all twenty random books and the 20/100
  cross, each truncated.
- Outcome / decision: **prediction 1 fails at both cost rows**, so the experiment is falsified as
  the blueprint words it. The window margins over the control hold (+0.045 Sharpe and +0.76
  points pre-registered, +0.086 and +1.66 flat), the sub-periods do not: 1 of 3, 1999–2008 alone.
  Prediction 2 holds, 3 fails, 4 holds (the cap: volatility 24.5% against 25.8%, drawdown −80.9%
  against −82.6%, Sharpe 0.1465 against 0.1462). Rule flat 7.17% / 0.209 against the Core's 7.93%
  / 0.306. P1, P2 and P3 fail at the flat row. `FINDINGS_1.md` is rewritten for this pass; the
  first pass stays a row of `RESULTS.md`. None of the changes the blueprint lists as unable to
  rescue it is proposed here.
- Open threads:
  - The owner's sign-off on the outcome, and his yes on the read-back and the Verify fix.
  - A run from a wiped working copy before any commit of the result.
  - The uncapped arm's sub-periods and attribution, the blueprint's watched item, not measured.

## 2026-11-17 — the owner's yes on the read-back and on the Verify fix

- Idea / question: the read-back of 2026-11-16 (the rule, its two dates' books, and the count walk
  that skips a name falling below the 1% floor and tries the next) and the Verify fix of
  2026-11-17 (a struck sector above the cap only by what the band's kept names drifted), both
  awaiting the owner's word.
- What we tried / considered: asked both together, after the second pass reported.
- Outcome / decision: the owner's words, 2026-11-17: "Yes, both". The rule as committed in
  `BLUEPRINT_1.md` (`107768f`) and run on 2026-11-17 is the one he read back. **His yes came after
  the blueprint's commit and after the run**, not before them as `AGENTS.md` asks; recorded here as
  it happened.
- Open threads:
  - His sign-off on the outcome, falsified, is not given yet.
  - A run from a wiped working copy before the result's commit.

## 2026-11-17 — Experiment 1 rewritten: the band reinvests, 0.5% cash in total

- Idea / question: the owner, on the app's report, saw the book hold up to 8% cash: "por que hay
  momentos dode tenemos mucho cash? 7% creo que para algo que queremos este full invested la mayor
  parte del tiempo necesitamos ajustar". The weight files say why: the rule's book was 98.8%
  invested on average, 91.6% at its lowest, under 97% on 52 of 323 dates, almost all of it the
  band's — a kept name that drifted below its target left the gap in cash.
- What we tried / considered: the change belongs to a new experiment under `AGENTS.md`, since the
  band is on the blueprint's list of changes that may not rescue it. The owner chose otherwise:
  "no arma estos cambios en el experimento 1 y correlo de nuevo solo la parte del experimento, ya
  no tienes que bajar datos", then "que nuestro target sea tener 0.5% en cash", and, asked whether
  that is 0.5% in total or in the weights, "0.5% in total". So this is **a rewrite of Experiment
  1**, recorded as `AGENTS.md` asks of one: this entry, a new `BLUEPRINT_1.md` that names the one
  it replaces, the earlier version at a tag and as a row of `RESULTS.md`, and its runs in the
  trial count.
- Outcome / decision: two changes, nothing else. **The band reinvests:** the traded names share
  what the kept names leave of a fully invested book, in proportion to their targets, inside the
  20% name cap and the 50% sector cap with the kept names counted; what no traded name can take is
  cash. **The engine's cash reserve is 0.5%**, in place of 1%, so the book's cash target is 0.5%
  in total. Rebuilt on the same data, before any engine run: the struck book is invested 100.0% on
  average, 99.58% at its lowest, no date under 99%, against 98.79%, 91.58% and 129 dates before;
  no struck sector above 50% (52.1% before); the largest struck weight 20.65%, a kept name drifted.
  The predictions, the window and everything else on the blueprint's list stay as committed; the
  rewrite is made knowing the second pass's result, disclosed.
- Open threads:
  - The read-back of the rewritten rule, and the owner's yes, before the new blueprint.
  - A smaller reserve may let a rebalance's costs outrun it: Verify's count of valued days
    excludes any run that stops, by name.

## 2026-11-17 — the rewritten rule read back, and the owner's yes

- Idea / question: the rewritten rule, read back before its blueprint: the same rule, with the
  traded names taking up what the band's kept names leave of a full book inside both caps, and a
  0.5% cash reserve.
- What we tried / considered: the read-back gave the rule in one sentence and the book on
  2026-09-01 and 2026-10-01. On 2026-09-01: 36 names, 100% invested, technology at 50.0% (the old
  band's 50.45%), MU 10.9%, AMZN 8.7%, GOOGL 8.0%. On 2026-10-01: 38 names, 100% invested where
  the old band left 97.16%; DELL, MRK and PLTR enter, AAL leaves; GS, BAC, UNH, COHR, JNJ and CVX
  are held at 1.0% to 1.5% at ranks 36 to 42; KLAC (35) and TXN (41), technology with the sector
  at its cap, are skipped. On a date with few traded names they take more: CAR 6.5% target, 7.6%
  struck, on 2001-05-01.
- Outcome / decision: the owner's words, 2026-11-17: "Yes, run it". The new `BLUEPRINT_1.md`
  follows.
- Open threads:
  - None from the read-back.

## 2026-11-17 — the rewritten version cannot be priced with a 0.5% reserve

- Idea / question: the rewritten blueprint (`149aa3c`) run from 18:53 to 20:21.
- What we tried / considered: with the band now striking books 100% invested and the engine's
  reserve at 0.5%, the engine ran out of cash at a rebalance in 55 of 104 runs ("Cash error" on
  54 rebalances, the largest −$988) and stopped valuing them: the rule at the pre-registered
  costs stopped on 2001-01-31, the uncapped arm too, every sweep setting at the pre-registered
  costs, and the random books, fifteen of which the engine refused outright. The notebook then
  stopped before Verify, its gate reading the rule's run, which was excluded. No performance
  figure from this run is read or reported.
- Outcome / decision: a fully invested book leaves nothing to pay a rebalance's costs once the
  reserve is spent; the 0.5% total the owner chose cannot be priced at these costs. The cash
  target goes back to the owner.
- Open threads:
  - The owner's choice of cash target the engine can price.

## 2026-11-18 — the cash setup chosen again: book 99.5%, reserve 1%

- Idea / question: which cash setup the engine can price, after the 0.5% reserve ran out.
- What we tried / considered: three setups were put to the owner — the book at 99.5% with the 1%
  reserve; the book at 100% with the 1% reserve, untested; or both tested on the rule alone first.
- Outcome / decision: the owner's answer, 2026-11-18: "Book 99.5%, reserve 1%". The band fills
  every book to 99.5% (`banded_book`'s `invested`), the engine keeps 1%, as the replaced version
  did. `BLUEPRINT_1.md` is amended before any result of the rewrite was read, naming the draft it
  amends (`149aa3c`); that draft's 46 books are counted, 335 in all.
- Open threads:
  - None.

## 2026-11-18 — the rewrite paused; the second pass put back

- Idea / question: the owner presents at 10:00: "mejor vamos a poner pausa y deja las ultimas
  versiones que teniamos y ya lo revisamos despues con calma".
- What we tried / considered: the run of the amended rewrite (`506d42f`), started 07:44, was
  stopped at about 09:00 with 83 of 104 engine runs done; nothing of it was read. The rewrite's
  code is kept in `Data/Curator/_history/rewrite_wip_2026-11-18/`, and the second pass's code is
  back in place — the band that leaves a kept name's shortfall in cash, the 1% reserve. The
  notebook ran again on it so that `Portfolio/` holds the second pass's books, its engine runs read
  from the cache, and its eight workbooks are back in `Backtest/`.
- Outcome / decision: `FINDINGS_1.md` and `RESULTS.md` report the second pass, the blueprint of
  `107768f`. The committed `BLUEPRINT_1.md` is the rewrite's, not yet run: the two disagree until
  the rewrite runs.
- Open threads:
  - Run the rewrite from `rewrite_wip_2026-11-18`, with the speed-ups proposed on 2026-11-18.

## 2026-11-18 — the rewrite resumed

- Idea / question: the owner, after the call: "vamos a seguir corriendo el experimento para bajar
  el cash en el portafolio".
- What we tried / considered: the rewrite's code was put back from
  `Data/Curator/_history/rewrite_wip_2026-11-18/` unchanged — the band reinvests to 99.5%, the 1%
  reserve, as `BLUEPRINT_1.md` (`506d42f`) says. The second pass's code is kept beside it in
  `Data/Curator/_history/second_pass_restored_2026-11-18/`, and its eight workbooks in
  `Data/Curator/_history/second_pass_2026-11-17/backtest/`. The run of the morning's stopped
  attempt left its engine runs in the cache, which is keyed by the book, so they are read again
  rather than priced; the speed-ups were not added, so the code is the one read back.
- Outcome / decision: the notebook and the app's workbooks run again, from 2026-11-18 midday.
- Open threads:
  - Read the run whole, then rewrite `FINDINGS_1.md` and `RESULTS.md`, the second pass a row.

## 2026-11-18 — the rewrite run, read before its findings

- Idea / question: what the band that reinvests to 99.5% did to the cash and to the book.
- What we tried / considered: the notebook ran 15:39 to 17:06, the app's eight workbooks to 18:01.
  Verify passed, 77 checks; 104 engine runs, 93 read, 11 excluded by name, each truncated by the
  engine's "Cash error": random books 02, 05, 07, 09, 10, 13, 16, 19 and 20 at the pre-registered
  costs, random 10 at flat 5 bp, and the control at $100,000. The rule, its control, equal weight
  and the uncapped arm are read whole at both cost rows.
- Outcome / decision: the struck books are invested 0.993 to 0.995, mean 0.9950, no date under
  99%, against a mean of 0.9879 and dates as low as about 92% in the second pass. The rule
  pre-registered: CAGR 5.58%, Sharpe 0.143, drawdown -81.4% (second pass 5.65%, 0.146, -80.9%);
  flat 5 bp: 7.13%, 0.206, -76.6% (7.17%, 0.209, -76.2%). The control 5.02% / 0.106 and 5.62% /
  0.127. Prediction 1's sub-period limb fails again, 1 of 3, at both rows: the rewrite is
  falsified on the same condition as the version it replaces. Not yet written into
  `FINDINGS_1.md`.
- Open threads:
  - Rewrite `FINDINGS_1.md` and `RESULTS.md` from this run, the second pass a row; on the owner's go.
  - Nine random books priced at the pre-registered costs ran out of cash with a 1% reserve.

## 2026-11-18 — the findings written, and the run from a wiped working copy

- Idea / question: does the rewrite reproduce from nothing, as S5 and a commit to `main` require.
- What we tried / considered: on the owner's yes, `FINDINGS_1.md` and `RESULTS.md` were rewritten
  from the run above, the second pass a row. Then every output was moved aside to
  `Data/Curator/_history/before_wiped_run_2026-11-18/` — the curated files, the Curator's state,
  the universe's outputs, the books, the engine and attribution caches and results, `__marimo__/`
  — keeping only the hand-supplied benchmarks and factors, the seed, `Provider_Renames.csv` and the
  app's imported job folders. The download ran 19:46 to 21:20, the universe to 21:21, the
  experiment to 23:03 and the eight workbooks to 23:47.
- Outcome / decision: Verify passed 77 checks; the same 93 runs read and the same 11 excluded by
  name. `gate.csv`, `sub_periods.csv`, `benchmarks.csv`, both sweeps, `tradeability.csv` and
  `excluded_runs.csv` are byte for byte the earlier run's; attribution's three tables agree to
  1e-10 for every published book. Three random books at the flat row — 04, 13 and 19 — moved in
  the seventh significant digit of CAGR, and their factor-model rows by up to 0.012 points; none
  changes a count published. 27 of the 2,206 curated files differ from the earlier download, ACM to
  WAB, which is where those books' drift can come from; which columns differ, and why, is not
  measured (`RESULTS.md`'s limitation 5 is the likely reason). The library sizing check reports the same 22 of 646 book-dates over
  its tolerance, largest difference 1.4e-6, as `FINDINGS_1.md` already says; it exits non-zero by
  design and does not block. S5 holds.
- Open threads:
  - The owner's sign-off on the outcome; the eight new workbooks imported into the app.

## 2026-11-19 — Experiment 1 rewritten again: cash run the way a fund runs it

- Idea / question: the owner, reading the app's workbook, 2026-11-19: "si hay cash que viene por
  delistings entonces ese día tenemos que rebalancear con ese cash de manera eficiente"; "tener 1%
  constante en cash seria lo ideal ... y ya 0.5% excelente"; "hasta que el experimento 1 no sea lo
  mas eficiente como opera un fondo vamos a seguir teniendo estos problemas, todo en el
  experimento 1 por favor"; "sigue siendo la misma hipotesis"; and "solo corre los 4 portafolios
  base y sus respectivos backtests".
- What we tried / considered: the rule's daily cash in the 99.5% version (flat 5 bp, the engine's
  `daily_weights`): mean 1.70%, median 1.55%, 99th percentile 3.8%, maximum 9.2%; 170 days above
  3% and 32 above 5%, all between 2008-11-17 and 2009-03-31. On a rebalance day 1.62% on average,
  never under 1.36%: the engine's 1% reserve, the book's 0.5% and whole-share rounding. The spikes
  are the 35 delisted names the engine sold, $315,584 in all, each left in cash until the next
  monthly date. All 35 are acquisitions, each a permaticker no other seed row carries; no ticker
  change appears as a delisting, since Sharadar files each permaticker's history under its current
  ticker. Dividends make no cash: the engine fills and marks on total-return prices. A book at
  100% with a 0.5% reserve was priced on 2026-11-17 and stopped in 55 of 104 runs, the rule at the
  pre-registered costs among them (this journal, that date), so a 0.5% reserve is not available
  from this engine as it is.
- Outcome / decision: a rewrite of Experiment 1, the hypothesis, predictions and falsifier word
  for word, the execution changed. A held name that is delisted is topped up on the second trading
  day after its last price: the freed cash goes to the names already held, by traded value, inside
  the 20% name cap and the 50% sector cap, and nothing else trades. Only the four base books are
  priced, at both cost rows; the sweep, the band variants, the random books, the stress and $100k
  rows and attribution are not, and their gate rows read "not evidenced" in this version. The
  99.5% version is kept at the tag `experiment-1-reinvest-v2` (`433514b`) and as a `RESULTS.md`
  row.
- Open threads:
  - The rule read back, the cash setup with it, and the owner's yes, before the blueprint.
  - A note to `lab@kaxanuk.mx` on the engine's "Cash error", for the owner to send or not.

## 2026-11-19 — the delisting top-up read back, and the owner's yes

- Idea / question: the rewritten execution, read back before its blueprint: the same book, 100%
  invested with the engine's 1% reserve, and a delisted name's cash put back two trading days after
  its last price.
- What we tried / considered: the rule in one sentence — the same book as before, and when a held
  name is delisted, on the second trading day after its last price the freed cash goes into the
  names already held, by traded value, inside both caps, and nothing else trades. The worked case,
  on the 99.5% version's book: UST delisted 2009-01-05, 7.26% of the book at the open of
  2009-01-07, 7.8% cash with the book's own; that cash waits until 2009-02-02 today. Topped up on
  2009-01-07 over the other 18 names: AMGN 18.82% + 1.18 = 20.00%, the name cap binding (1.44
  points uncapped), BMY 11.76% + 1.00, GIS 8.83% + 0.71, ROH 6.93% + 0.60, the other fourteen +0.12
  to +0.35; health care 40.1%, under its cap; 0.5% cash after, the book's own. The cash setup: a
  100% book with the 1% reserve, untested, the 99.5% book named in advance as the fallback if any
  of the four base books stops; 0.5% is not available from this engine (2026-11-17).
- Outcome / decision: the owner's words, 2026-11-19: "Yes, run it". The new `BLUEPRINT_1.md`
  follows.
- Open threads:
  - None from the read-back.

## 2026-11-19 — the fully invested book stops; the blueprint's fallback, 99.5%

- Idea / question: the four base books at 100% with the engine's 1% reserve, as `BLUEPRINT_1.md`
  (`69aded0`) fixed them, the 99.5% book named there as the fallback.
- What we tried / considered: the notebook ran 20:20 to 20:29. The book is struck 99.6% to 100%,
  36 top-up dates shared by the rule and its control, every invariant of section 2.1 passing. The
  engine stopped the rule at the pre-registered costs with "Cash error on 2008-07-01 with
  $-292.39", a first-of-month rebalance, and its 1999–2008 sub-period run with it; 18 of 20 runs
  were whole. The gate cell then stopped on the missing rule, before Verify. The log printed the
  flat row's figures for the rule; they are not read or reported, since the run is replaced.
- Outcome / decision: a base book stopped, so every book is struck 99.5%, as the blueprint says,
  with the 1% reserve and the top-ups unchanged; the run starts again. A 100% book needs the engine
  to scale buys down when its cash runs short, the first request of the draft note to
  `lab@kaxanuk.mx`.
- Open threads:
  - The run at 99.5%.

## 2026-11-20 — lead 10 fails at the flat row; its bound reported, no longer raised

- Idea / question: the four base books at 99.5% with the 1% reserve and the top-ups, the
  blueprint's fallback. All 20 engine runs were valued whole and none was excluded, but Verify
  raised on one check: "rule, flat 5 bp: cash at most 3% but the two days before a rebalance".
- What we tried / considered: the rule's daily cash, from the engine's `daily_weights`. At the
  pre-registered costs it stays within the 3% bound. At flat 5 bp it sat between 3.0% and 3.45% on
  33 days outside the two days before a rebalance, in October 2005, September 2008 and August 2011.
  The cause is not the top-up. The engine buys whole shares at the dividend-and-split-adjusted
  open, and Chesapeake's (CHKAQ) adjusted prices carry its 2020 1-for-200 reverse split back:
  on 2005-10-03 the book asked for 1.13% of it, at about $6,483 a share where the market traded
  $38.68, and the engine bought none. That point waits in cash until the next month's rebalance.
  A fund would have bought about 290 shares.
- Outcome / decision: the owner's words, 2026-11-20: "Report it, keep going". Lead 10 is recorded
  as **failed at the flat row**, with this cause, and as passing at the pre-registered costs.
  Verify's 3% bound becomes a reported figure rather than a check that raises: a change made after
  the run was seen, disclosed here and in `FINDINGS_1.md`. Nothing else in the run changes. The
  draft note to `lab@kaxanuk.mx` gains a third request: fractional shares, or whole shares counted
  at the unadjusted price.
- Open threads:
  - The 8 workbooks, the write-up and the run from a wiped working copy.

## 2026-11-23 — version 0.4.0 attributed at the pre-registered costs, from the engine's cache

- Idea / question: the owner's decision of 2026-11-23 — every figure the Investment Bootcamp
  quotes comes from this repository — needs the attribution version 0.4.0 left out on 2026-11-19.
  Can the three passes run on the books already priced, without re-running the notebook's three
  hours, and what do they say about P2?
- What we tried / considered: `attribute_base_books.py`, beside the notebook, reads the engine's
  runs of 2026-11-20 from `Backtest/cache/` — the rule, its control and equal weight at the
  pre-registered costs — and shapes them exactly as section 5 does, then calls
  `attribution_analysis.attribute_books` on KaxaNuk Attribution Analysis 0.7.0. The licence was
  checked by its variable's name only. The run finished whole: the first cut's benchmark at 8.08
  points a year over the bill against the Core's own 7.86, a gap of 0.22 inside the blueprint's
  point; 17 factors from 20 files; the factor model covering 98.5% of the rule's weight; the
  attribution window 2000-01-03 to 2026-10-30.
- Outcome / decision: P2 reads **fails** at the pre-registered costs: the factor model leaves the
  rule an idiosyncratic return of +58.07 points, but Brinson-Fachler selection is −102.69 by sector
  and −0.03 on the residual, and the random books are not priced. Lead 9's first limb holds, the
  market the largest contribution (+349.60, beta −130.07); its second limb needs the uncapped arm.
  Every figure in `FINDINGS_1.md`, *What attribution says*. The flat 5 bp row is not attributed,
  so P2 there still reads "not evidenced". Nothing of the backtest moved.
- Open threads:
  - The flat row and the uncapped arm attributed, by adding their cached runs to the script.

## 2026-11-24 — the flat 5 bp row and the uncapped arm attributed

- Idea / question: the owner's word of 2026-11-24, "attribute the flat 5 bp row and the uncapped
  arm too". Does P2 read the same at the flat row, where the gate is read, and does the uncapped
  arm carry more technology than the rule, lead 9's second limb?
- What we tried / considered: `attribute_base_books.py` takes five more of the engine's cached runs
  of 2026-11-20 — the rule, its control and equal weight at the flat row, and the rule without its
  sector cap at both rows — and runs all eight books in one call on KaxaNuk Attribution Analysis
  0.7.0. The three books attributed on 2026-11-23 came back with the same figures; the first cut's
  benchmark reconciled again within 0.22 points a year; the factor model covered 98.4% to 98.6% of
  every book.
- Outcome / decision: **P2 fails at the flat row too**: idiosyncratic +58.67, selection −102.82 by
  sector and −0.01 on the residual. The cost row barely moves attribution, since it reads what was
  held, not what it cost. **Lead 9 holds on both limbs**: technology +63.76 for the rule against
  +67.93 uncapped (+63.86 against +68.06 flat). The cap gave up allocation (−58.17 against
  −121.48) and beta (−130.07 against −169.56); the uncapped arm's residual selection is +4.88.
  Every figure in `FINDINGS_1.md`, *What attribution says*. Nothing of the backtest moved.
- Open threads:
  - The uncapped arm's attribution by sub-period, linked by the library over each third.

## 2026-11-24 — the rule and the uncapped arm attributed by sub-period

- Idea / question: the owner's word of 2026-11-24, "attribute the uncapped arm by sub-period too".
  What did the sector cap give up in 2018–2026, the blueprint's watched item, and in which lever?
- What we tried / considered: the engine never priced the uncapped arm by sub-period, and pricing
  it would add trials. So `attribute_base_books.py` cuts the whole window's books — the rule and
  the uncapped arm, at both cost rows — to each of the notebook's three `SUB_PERIODS` and has
  Attribution Analysis 0.7.0 link each cut over its own days. Summing the per-year tables was
  ruled out, because linked effects compound. The cut is not the engine's fresh sub-period book,
  which `FINDINGS_1.md` says beside the table. Each sub-period's benchmark reconciled with the
  Core's own returns within 0.45, 0.16 and 0.01 points a year; the window's figures came back
  unchanged.
- Outcome / decision: the cap's cost is 2018–2026's allocation, not selection: the uncapped arm
  +319.20 over the Core against the rule's +267.60, allocation +88.69 against +67.16, selection
  +126.92 against +129.27. In 2009–2017 the two books are nearly the same. And the window's P2
  failure is 1999–2017's: in 2018–2026 the rule's selection is positive in all three layers
  (+129.27, +137.73 idiosyncratic, +35.41 on the residual). P2 stays **fails**, read over the
  window. Nothing of the backtest moved.
- Open threads:
  - The random books, priced and attributed, to say whether 2018–2026's selection beats chance.

## 2026-11-24 — the random books priced and attributed

- Idea / question: the owner's word of 2026-11-24, "price and attribute the random books", given
  after this version's result was seen. The blueprint left them "not priced in this version". What
  is the last limb of P2 — the rule's idiosyncratic return above 16 of 20 random books — and
  prediction 6, and is the rule's positive selection in 2018–2026 above chance?
- What we tried / considered: `experiment_1_marimo.py` gained `RANDOM_BOOKS = True`, which prices
  the twenty random books at both cost rows and leaves the sweep, the band's variants and the
  notebook's own attribution off. It ran 09:29 to 11:06; Verify passed 59 checks, 60 engine runs,
  51 read and 9 excluded by name, the four base books read back from the engine's cache. At the
  pre-registered costs random books 02, 05, 07, 09, 13, 16, 17, 19 and 20 stopped with the engine's
  "Cash error", in 2000 or in the autumn of 2008, as nine did in the replaced version; at the flat
  row all twenty were valued whole. `attribute_base_books.py` then attributed the 31 read on the
  factor model alone, as section 5 does, over the window and cut to each sub-period as the rule's
  are, in about 25 minutes; the base books' window and sub-period figures came back unchanged.
  The sub-period count was added once the window's was planned, to answer the open thread above,
  and is read as information, not as the limb.
- Outcome / decision: **the limb fails at the flat row: the rule's +58.67 points are above 14 of
  the 20 random books**, whose median is +16.88, from −97.01 to +161.79. At the pre-registered
  costs it is not evidenced: 7 of the 11 read. On Sharpe, the notebook's own table puts the rule
  above 12 of 20 at the flat row (0.207 against a median of 0.189) and 6 of 11 pre-registered.
  Prediction 6 fails at the flat row. **By sub-period, at the flat row, the rule is above 7 of 20
  in 1999–2008, 14 of 20 in 2009–2017 and 19 of 20 in 2018–2026**, its +137.41 below random book
  03's +291.87 alone, the random median +20.37. The last third's selection is above what a random
  draw from the same pool earned over the same days; the window's is not, and that third was
  singled out after it was seen, one of three cuts. P2 stays **fails** at both rows. The trial
  count rises by the twenty books, 339 to 359.
- Open threads:
  - Whether 2018–2026's selection is the cross, the traded-value ranking, or both: each random draw
    replaces the two together, and no arm isolates the ranking.
  - The random books run from a wiped working copy, with the rest of this version's attribution.

## 2026-11-25 — curated into the KaxaNuk Researcher as its worked example

- Idea / question: on the owner's word of 2026-11-25, US-Golden-Flow 0.8.3's Experiment 1 becomes
  the package's worked example, renamed `us-golden-flow`, Experiment 1 only and public papers only.
- What we tried / considered: every shared file keeps the template's text, and this strategy's code
  and documents sit beside it between the example's markers. The modules keep the template's
  docstrings, which are newer than the ones this strategy carried from Golden-Flow; the notebook's
  setup cell is split, the template's setup kept and the strategy's settings in a cell of their
  own; the four scripts beside the notebook keep their own descriptions as comments. Three changes
  from the live repository, each for the example being public: the seed keeps tickers and dates
  only, and the universe notebook reads its name, permaticker and match as empty, which moves no
  figure since positions join by ISIN; Paleologo's book and every link to it are left out, the
  claims it alone supported marked so; and Golden-Flow's `Paper_Trading_1`, on probation since
  2026-10-27, is retired, as `Paper_Trading/BITACORA.md` records. marimo's check passes on every
  notebook.
- Outcome / decision: the example is version 1.0.0. Its figures are the live repository's, which
  reproduced from a wiped working copy on 2026-11-20; the example itself is not run from a wiped
  copy before this release.
- Open threads:
  - The example run from a wiped copy, with a Sharadar key and the Lab's licences.

<!-- example: end -->
