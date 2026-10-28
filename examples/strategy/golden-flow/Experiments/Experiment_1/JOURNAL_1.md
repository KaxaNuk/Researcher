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

**What this copy of the journal holds.** Golden Flow's entries from 2026-10-05 to 2026-10-24, whole
and word for word, with the entry the package wrote on 2026-10-07, when it first copied the
strategy, in its place among them; then one entry of 2026-10-27, on the owner's decision about the
gate.

- **Left out:** every entry dated before 2026-10-05, including the 2026-09-23 entries that one
  entry below cites; the 2026-10-06 entry that retired `BRAINSTORMING_1.md`, with the brainstorming
  entries it quotes; and Golden Flow's later experiments, which this copy does not hold.
- **Replaced**, each by a description in square brackets: private names — another strategy's name,
  the name of the Analytics Factory's private repository and an issue in it, a person's name, a
  local path and a branch name — and four mentions of Golden Flow's next experiment. The owner's
  first name is written "the owner". Nothing else in an entry is changed.
- **A key to the entries:**
  - versions 0.13.0 and 0.14.0, and their tags, are Golden Flow's own earlier versions, run on
    another index; 0.15.0 to 0.15.2 are this experiment's earlier version, on FMP prices;
  - "the desk" is KaxaNuk's Analytics Factory;
  - "the worked example", in entries dated before 2026-10-07, is the package's earlier example;
  - `Paper_Trading_1`, the paper book of 0.15.2, was retired on 2026-10-24 and is not in this copy.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-05 — 0.14.0 reproduced, the night before it is replaced

- Idea / question: does the published 0.14.0 book still come out of its own code and data?
- What we tried / considered: the owner re-ran `Universe/universe.ipynb` and
  `Experiments/Experiment_1/experiment_1.ipynb` on 2026-10-05 against the files on disk, with the
  licensed engines validating online.
- Outcome / decision: **every published number came back exactly** — the rule at 24.69% and a
  0.9484 Sharpe with a −34.60% drawdown over 853 rebalances, the filter-off control at 23.42% and
  0.8403, the equalised control at 23.49% and 0.842, equal weight at 18.82% and 0.905, the random
  books from 7.55% to 22.29%, Brinson-Fachler alpha 93.22, 59.52 idiosyncratic points of 197.67,
  and 37.78 on the residual pass. The outputs themselves were discarded on 2026-10-06, as notebook
  outputs always are; this line is their record. The version is kept at tag `0.14.0`.
- Open threads: none for 0.14.0. It is the replaced version from the next entry on.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — Experiment 1 is rewritten: the owner's decisions, in his words

- Idea / question: the owner asked on 2026-10-05 for Golden Flow to become the Lab's example
  strategy for the researcher — *"a simple but elegant strategy that objective is to invest in the
  top 35 stocks ranked and weighted by traded value of 63d and use the 50 vs 200 sma golden cross
  signal to become elegible, our investable universe will be
  [the strategy's Data/Curator/Benchmarks/KN_US_Equity_Core_Holdings.csv]"* — brought to the
  latest KaxaNuk Researcher template and run end to end to the paper-trading gate. This is a
  **rewrite of Experiment 1**, which the template allows once the owner decides it: the rule, the
  universe, the benchmark and the window all change, so it is a different book, not a better
  version of the one at tag `0.14.0`.
- What we tried / considered: opening Experiment 2 beside the old benchmark, or editing Experiment 1
  in place. The owner chose a **clean slate**: the 0.14.0 version is kept at an annotated tag
  `0.14.0` on `ad9f8c0` and as a row of `RESULTS.md`; the blueprint of 2026-07-18 is replaced by a
  new `BLUEPRINT_1.md` that names it; the 0.13.0 and 0.14.0 runs are counted in this experiment's
  trials. Every decision below was taken in chat on 2026-10-05, before any file of this version
  moved, and is recorded here before any work it governs.
- Outcome / decision:
  - **Universe.** *"The one i added in this repository benchmarks folder"* — the file the owner added
    that evening landed in [another strategy]'s drop zone, not this one, and was copied here byte for byte:
    `KN_US_Equity_Core_Holdings.csv` (md5 `eba4bf64ffa8de5d650e4e2c4b21844d`) and
    `KN_US_Equity_Core_Returns.csv` (md5 `1668b564582f1871d7e4a6f39896e50a`). The holdings are the
    index's daily weights: about 600 names a day, 1,399 listings keyed by Sharadar ticker, `m_date`
    in ISO dates, 2000-01-03 to 2026-08-14. The returns are its daily series, `m_date` day first,
    the return under `kn600`. *"The correct name is KN US Equity Core"* — the index is called the
    **KN US Equity Core** everywhere in this repository from here on.
  - **Benchmarks.** *"Please also add SPY as benchmark"*; the owner chose **KN US Equity Core and
    SPY**, in that order, so every alpha is measured against the index. `QQQ` is set aside. The
    cash proxy stays `BIL`.
  - **Dead names.** **FMP only.** A member FMP does not carry is dropped, counted in
    `Universe/Data_Issues.csv`, and the share of index weight it held is published per date as the
    survivorship cost. This is lie 1 of `AGENTS.md`, accepted and quantified, not removed.
  - **Window.** **From 2015**, for the owner's reason: *"Fmp universe survivorshop biases is ok from
    that year"*. When the coverage measured before any download turned out to be about 87.5% of the
    index's weight on 2015-01-02, the owner chose **data sets the start**: the window opens on the
    later of 2015-01-02 and the first date on which members with an FMP price hold at least 90% of
    the index's weight, a date the universe notebook fixes before any rule exists. It closes on
    **2026-06-01**; everything from 2026-06-02 is unseen by every stage until the book is frozen.
    **This choice is a forking path and is counted as one**: it was made after the owner had seen
    0.14.0's 2017–2026 result and had been told that the package's worked example falsified a
    close cousin of this signal on 2002–2016 (equal weights, Sharpe 0.234 against a control at
    0.256).
  - **Sizing.** Asked why 35 names, the owner answered *"Maybe we can invest in the Top names
    meanwhile non weight more than 20% and less than 1%"*, and confirmed the reading **bounds set the
    count**: no fixed N. Names are taken in order of 63-day traded value, weighted in proportion to
    it, none above 20% — the excess spread pro rata over the rest — and the book stops adding names
    when the next one would leave the smallest weight under 1%. **"Top 35" is retired by the owner's
    own answer**, so no parameter is chosen for the count.
  - **The gate's margins, fixed before any number exists.** Criterion 1 and the falsifier: the book
    beats its control by **+0.03 Sharpe and +0.5 points of CAGR** over the window, and on both
    measures in **2 of 3** sub-periods. Criterion 3: **6 of 8** perturbed settings keep the sign of
    the margin over their own control on both measures, and all 8 beat the KN US Equity Core on
    Sharpe. Both were set knowing that 0.14.0 beat its control by 1.2 points a year on another
    universe.
  - **The thesis.** The owner skipped the seven questions before any backtest; the blueprint lists
    them under its open questions as not answered by him, and none is answered for him. The kill
    switch is proposed from the claim and labelled for him to confirm.
  - **The sign-off.** *"Sign in the morning"*: the night runs to the gate's verdict and tests the
    daily machinery in a scratch clone; criterion 5 is the owner's signature, given after 1 to 4 are
    evidenced, and nothing is frozen before it.
  - **Git.** A local branch, [a branch], a commit per stage, nothing pushed.
- Open threads: the blueprint's predictions are drafted after the analyzer, put to the
  `blueprint-critic` agent cold, and committed alone before the rule, under the owner's go of
  2026-10-05 on the plan that fixed everything above; the owner reads them in the morning. If he
  rejects the result, the branch is kept at a tag and its runs stay in the trial count.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — Choosing the benchmark

- Idea / question: what does the rewritten Experiment 1 have to beat?
- What we tried / considered: the **KN US Equity Core**, the index whose daily membership is the
  universe; **SPY**, the most liquid fund on the same market; **QQQ**, which 0.14.0 reported;
  the **KN US Equity 600** drop-in of 0.14.0, a hand-made file in a format the desk no longer
  writes; the **methodology-1.1 Core** in [the Analytics Factory's private repository], quarterly reviews keyed
  by permaticker and run there provisionally, not read; and an equal-weight book of the members.
- Outcome / decision: **KN US Equity Core first, SPY second**, the owner's choice. The index is the
  transparent one — the universe is its membership, so beating it says the rule chose well inside
  what it was given — and SPY is the liquid one an allocator can buy instead. The engine prices the
  book against both and reports every alpha against the first. QQQ is set aside as a sector bet,
  the 600 drop-in and the methodology-1.1 Core as files this repository does not read. The cash
  proxy is `BIL`.
- Open threads: the holdings and the returns file disagree with each other — the returns are dated
  a day before the current holdings, and the weights moved since — so the Brinson-Fachler
  benchmark built from the holdings will not reconcile exactly with the engine's index return. The
  blueprint states the tolerance before the run; the desk is asked about the file.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — Golden Flow becomes the reference example, and takes the example's code

- Idea / question: two recorded positions are reversed tonight, on the owner's word, and are
  written down so the reversal is a decision rather than a drift.
- What we tried / considered: the entry of 2026-09-23 on the clean version said Golden Flow stays
  its own strategy repository, not the template's example; the owner asked on 2026-10-05 to *"make
  all the changes needed to this strategy to become our example strategy for the researcher"* and
  to *"update the repo with the latest changes in the kaxanuk researcher example template"*. The
  template's `AGENTS.md` says nothing in a strategy is brought across from the worked example; this
  repository's own rules allow a look-across when it is asked for and written down first.
- Outcome / decision: **Golden Flow is presented as the Lab's reference example from 0.15.0**, while
  the package still ships `liquid-golden-cross` as its worked example — swapping it into the package
  is a later change to the package, not to this repository, and nothing here claims it has happened.
  **The look-across is lifted, by the owner's request**, for the code the template ships only as a
  contract: `Data/hand_supplied.py`, the curator's `--end-date` and resume, `Paper_Trading/promote.py`,
  `record.py` and `daily_update.py`, which are taken from the example 0.18.2 in package 0.31.0 with
  this strategy's constants, and `paper_trading_1.py`, written for this rule in the example's form.
  No choice of the example's — its parameters, its band, its benchmark — is taken.
- Open threads: the seams this repository added — the score argument in the sizing seam and the one
  calendar in the panel loader — are the first things the package would take if Golden Flow becomes
  its example.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The run starts from a wiped working copy

- Idea / question: the template commits a result only after the pipeline has re-run end to end from
  a wiped working copy. Can tonight's run be that run?
- What we tried / considered: a fresh clone doubles the night's download. Moving every ignored
  output aside gives the same starting state on this machine without a second download.
- Outcome / decision: before any stage ran, every gitignored output of 0.14.0 — the 791 curated and
  787 refined time series, the analyzer's table, the ten weight files and eighteen engine workbooks,
  the security master, the data-issues register and the provider cache — was **moved, not deleted**,
  to the session's scratch folder, 2.2 GB. Only the hand-supplied index and factor files stayed.
  Every number of 0.15.0 is therefore produced from a fresh download by this version's code.
- Open threads: the virtual environment was kept; a clone on another machine is the stronger test,
  and is what 1.0.0 waits for.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — What the engine charges for a commission setting, measured on a book that is not the rule

- Idea / question: the engine's `commission_cents` is not cents per share (the `backtest-engine-runs`
  skill measured the worked example's 0.1 at about eight cents). What does the setting this
  repository has used since 0.14.0, 0.05, actually charge, before the blueprint states it?
- What we tried / considered: a calibration book with no rule in it — one stock bought on
  2015-01-02 with the whole book and held to 2015-12-31 — priced by the engine in a scratch folder,
  on 0.14.0's price files, once on SPY and once on KO, the commission total divided by the shares
  the engine bought.
- Outcome / decision: **0.05 charges $0.041 a share on SPY (VWAP $205.72) and $0.035 on KO ($42.15);
  0.005 charges $0.0041 on SPY.** The charge is neither a flat amount per share nor a share of the
  price, so the blueprint states the setting and these two measurements, not a rate. The headline
  cost row stays at 0.05, 0.14.0's; the realistic row is set at **0.006**, about half a cent a share.
  The engine's licence validated online, so step 5 can run tonight.
- Open threads: how the engine computes the charge is not established by any page this repository
  has read; it is quoted as measured.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The data stage, from a wiped working copy: the window opens on the owner's floor

- Idea / question: build the seed, download, profile, refine and screen the KN US Equity Core
  universe, and let the data fix the window's first date before any rule exists.
- What we tried / considered: the FMP key in `Config/.env` was rejected from 00:30 to 06:30 (HTTP
  401) and nothing downloaded until the owner replaced it; the time went into the dry run recorded
  in 0.15.0's changelog. Then, from 06:32, in the template's order: `Universe/seed.py` (6 minutes);
  `Data/curator.py --end-date 2026-10-05`, one name at a time with its history pass (1 hour 37
  minutes for 892 names); the curator again, which asked FMP once more for every name with no file
  (2 minutes, nothing new); `Universe/universe.ipynb` (17 seconds); `Data/refinery.py` (3 minutes,
  803 securities); `Data/analyzer.ipynb`. A stale copy of the job waiting for the key started a
  second seed run at 06:36 and was killed within four minutes; the run that counts is the one
  started at 06:32. The first refinery run stopped on its own guard — the map from index tickers
  to FMP symbols kept the unmatched listings, so several mapped to one empty symbol — and ran again
  after the fix, as did the universe notebook.
- Outcome / decision:
  - **The seed:** 896 listings were members on some date from 2015-01-02; 888 have an FMP symbol
    (759 by CUSIP and 27 by CIK, every one of them priced; 102 unverified, of which FMP priced 19,
    each kept because its prices covered at least half the days it was a member).
    Eight have none: `AET`, `CBI`, `COL`, `CPN`, `CVC`, `EVHC`, whose tickers FMP now files under
    other companies, and `CY` and `NBL`, whose FMP prices contradicted their membership.
  - **FMP does not carry 83 more**, nearly all dead companies under the index's suffixed tickers —
    `AGN1`, `APC1`, `DD1`, `EMC1`, `MON2`, `TFCF`, `TWC`, `YHOO` among them. None was refused.
  - **Coverage:** the members FMP prices hold **92.97%** of the index's weight on 2015-01-02, 94.2% on
    average over 2015, 97.4% over 2017, 99.1% over 2019 and 100% from 2022; no window date is under
    90%. **The window opens on 2015-01-02, the owner's floor, and closes on 2026-06-01.** The
    survivorship cost is therefore at most 7% of the index early in the window, and concentrated in
    large dead companies.
  - **Excluded by name, before any rule:** the blocking rows of `Universe/Data_Issues.csv` — `MNKKQ`,
    `NE` and `PCP`, whose priced history inside their span is shorter than the cross's 200 days,
    and `RAI`, whose adjusted price is zero or negative and multiplies by more than six in a day.
    Twenty-eight files run outside their security's span and are read only inside it (`FTI` before
    TechnipFMC, `CIT`, `LIN` and others).
- Open threads: the analyzer's measurements go into `RESULTS.md`, *Before any experiment*, and the
  blueprint is drafted from them and from the notes.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The blueprint's draft, put to its critic cold, and what was done about each objection

- Idea / question: does the draft of `BLUEPRINT_1.md` say only what its sources license, before it
  is committed and can never change?
- What we tried / considered: the `blueprint-critic` agent read the draft cold, with `OBJECTIVE.md`,
  `RESULTS.md`, this journal, `AGENTS.md`, `BITACORA.md` and every note, told what the owner fixed
  on 2026-10-05 and not to argue with it. It returned twelve blocking objections and ten advisory.
- Outcome / decision — the blocking ones, each answered in the draft before its commit:
  1. *The falsifier and the claim table gave two verdicts for a book that meets the whole-window
     margins and misses the sub-periods, and "on both measures" could be read as the margins or as
     the sign.* One verdict now: that book is **falsified**. The sub-periods test the **sign** on
     both measures, as the owner's words of 2026-10-05 say ("beat the control on both measures in
     at least 2 of 3"); the margins apply to the whole window.
  2. *The thesis offered a risk gate and the falsifier asks for a CAGR margin.* Said in the thesis,
     plainly: no note predicts the return limb, the analyzer gives it a sign and no size, and a book
     that cuts drawdown at an equal return would confirm the notes' reading and still falsify claim
     1 as written. The owner's margin stands.
  3. *The control could hold names the book cannot — listings without 200 days of history.* The
     control keeps the history requirement, so the cross's sign is its one difference; the two
     sweep pairs keep theirs.
  4. *The trial count disagreed across three files, and left out 0.14.0's discarded random books.*
     **76 books**: 23 at 0.13.0, 14 at 0.14.0 — the nine reported and the five random books of its
     third attempt — and 39 here; `BITACORA.md` and `RESULTS.md` now say the same, and the window is
     listed as the one choice that is not a book. The commission calibration and the worker test
     priced one-stock books that are not the rule, and are said not to count.
  5. *Prediction 4, beating both benchmarks, had no source.* Now a lead; it is evaluated as part of
     success criterion 1.
  6. *The random books differ from the book in the cross and the ranking at once.* The lead says so
     and credits the two together; the gate's definition is the owner's and is unchanged.
  7. *The holding count and how often the cap binds had no measurement behind them.* Now a lead;
     both are reported in section 3 of `experiment_1.ipynb`. The line that the cap "binds rarely",
     and `BITACORA.md`'s "0 or 1 names", are gone.
  8. *The cost prediction had no source, and the 0.006 setting was never measured.* Now a lead; 0.006
     measured the same morning at $0.0049 a share on SPY and $0.0042 on KO.
  9. *The statuses misused `OBJECTIVE.md`'s vocabulary.* "Confirmed as a book" now needs both
     benchmarks beaten as well as the control; a better book that loses to its index is said in a
     sentence, since the vocabulary has no word for it; claim 2 is confirmed or falsified by its own
     prediction rather than parked at "measured".
  10. *The list of changes that may not rescue it was short.* It now names the trigger, the
      sub-period boundaries, the five-name `BIL` rule and the cash reserve.
  11. *No coefficient stated its overlap.* Each now does: 20, 62 and 251 days.
  12. *A clean clone cannot be evidenced tonight.* Success criterion 2 now reads the wiped working
      copy, with no manual step beyond `SETUP.md`'s drop-in of the desk's files — this run — and
      keeps a clone on another machine for 1.0.0.
- The advisory ones: the sizing's economic reason is now the attention argument, said to be in no
  note, with the notes against it named in the thesis and a key risk; the pool is said to be
  narrower than the book; the exit-lag and whipsaw risk names Han, Zhou & Zhu and Kaminski & Lo; the
  factor lead no longer expects momentum to carry much; the kill switch is distinguished from the
  paper book's and fires on either cost row; each threshold carries its reason; the margins are
  disclosed as set knowing 0.14.0's result; the traded value is stated as unadjusted dollars, so a
  dividend never scales it; "section 3" names its notebook. **Three predictions and five leads**
  remain.
- Open threads: the owner reads the predictions in the morning, unseen by him when committed, under
  his go of 2026-10-05.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The engine refuses a book that holds a name with no price; the owner's rule: sell at t−1

- Idea / question: the first run of the cycle priced 31 of its 47 engine runs and stopped. Why, and
  what does the rule do about it?
- What we tried / considered: the rule's own book, priced alone, was refused by the engine's data
  integrity check: on 2015-03-17, a rebalance date, the book held `AGN` (Allergan plc, then Actavis
  renaming itself) and FMP's file has no price for it — **a 62-day gap, 2015-03-17 to 2015-06-12, at
  the corporate event**. The engine will not trade a name it cannot price, and it checks every open
  position on every rebalance date, so a book holding a name through a gap cannot be re-struck at
  all. Measured across the seed, only `AGN` has a gap while an index member in the window (`BMRN`
  and `MNKKQ` have gaps outside membership). The universe register had no internal-gap check, which
  the `universe-point-in-time` skill lists. The two fixes put to the owner were excluding `AGN` by
  name or deferring re-strikes across the gap.
- Outcome / decision: **the owner's instruction, 2026-10-06, in his words: "when there is a
  corporate event and a company get delisted we need to trigger a rebalance in t-1 to sell that
  stock please include this knowledge into the flow of the template".** Implemented as one seam,
  `portfolio_construction.exit_before_price_stops`: a name is tradable on t only if it is priced on
  t and on t+1, so a name whose prices are about to stop — a delisting, or a corporate event that
  leaves a gap — drops out of the target on its last priced day, the held set changes, and the book
  re-strikes and sells it there at that day's VWAP. After the gap the name can be bought again. **It
  is one day of hindsight**: the leak `AGENTS.md` already names for a delisting exit, now applied to
  every stop in a price series, and said so in the seam, the notebook, the frozen book and
  `AGENTS.md`. It applies to every book alike — the rule, its control, the sweep, the equal-weight
  arm, the random books — so it is no difference between them.
- **What was seen before this decision, disclosed:** of the 31 runs that priced, the control over the
  window (19.73% a year, Sharpe 0.763), its realistic-cost row, its three sub-periods, the rule's
  2019–2022 and 2023–2026 sub-periods, five controls of the sweep, the 2% floor setting and its
  control, and eighteen random books. The rule's own whole-window run had not priced. **This is a
  change made after the blueprint, with part of the cycle seen**; it changes no parameter the
  blueprint names, and it is the owner's rule, not a choice made on those numbers. All 47 runs
  are priced again with it; **the 31 priced without it are excluded by name** in `RESULTS.md` and
  counted as trials, which brings the count to 107 books.
- Open threads: the template and its worked example sell a delisted name through the engine's
  `sell_at_last_price` and say nothing about gaps; the owner asked for this rule in the template's
  flow, which is a change to the package, prepared as a follow-up.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The cycle's second run: two errors its own checks caught

- Idea / question: the second run of the cycle, with the sell-at-t−1 rule, priced all 47 engine
  runs and attributed the books, and stopped in Verify. What failed?
- What we tried / considered: two errors, both in this repository's code, neither in a book.
  1. **The floor invariant was written wrong.** It compared the held weights against the 1% floor
     after masking the names not held to null, and a null compares false, so every date failed;
     the weigher's own output had never been below the floor. Rewritten as "not held, or at or
     above the floor".
  2. **The first cut's benchmark return came back infinite.** `RAI`, excluded from every book as a
     blocking row of the register — its adjusted price is zero or negative — was still in the
     index's holdings the attribution read, and a zero price gives an infinite return. 0.14.0
     dropped the excluded names from both sides; this version had not. Now `load_prices` reads a
     price of zero or below as no price, and the notebook drops the register's blocking names from
     the index and renormalises it. The reconciliation the blueprint made a precondition is what
     caught it: it read an infinite gap, and criterion 2 failed on it rather than passing on a
     broken first cut.
- Outcome / decision: the engine's prices are unchanged — every weight file is the same, and the
  engine runs are read from their cache. The attribution is computed again, and is now cached
  under the hash of its inputs as the engine's prices are. No figure from the failed run is
  quoted: the record is the next run's, which must reach the end of Verify.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The third run: criterion 2's precondition caught a one-day misalignment in attribution

- Idea / question: the third run reached the end of Verify, and criterion 2 failed on its
  precondition: the first cut's benchmark earned 21.23 points a year against the KN US Equity
  Core's own 14.30, a gap of 6.94 where the blueprint allows 1.0. Why?
- What we tried / considered: the engine's daily weights and the index's holdings are both struck
  at a day's close, after that day's return has moved them, and the attribution paired each with
  the same day's return. A weight that already holds a day's move, times that move, credits every
  book with the cross-section's daily variance. A check outside the engine, on the rule's book,
  confirmed it: with the weights moved one day on, the index side reads 14.85 against the index's
  14.30, a gap of 0.55, inside the tolerance; the book side falls by about as much. 0.14.0 shaped
  its attribution inputs the same way and never ran this check.
- Outcome / decision: `attribution_analysis.held_overnight` moves both tables one day on — the
  close of t−1 earns day t — and the notebook passes every book and the index through it. The
  engine's prices do not move; the attribution is computed again. The precondition the blueprint
  wrote before the run is what caught it, and it is kept as written.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The fourth run: the gate's criteria 1 to 4 pass, and attribution shrinks once aligned

- Idea / question: with the weights held overnight, does criterion 2's precondition hold, and what
  do the three passes say about the rule?
- What we tried / considered: the notebook ran headless to the end of its Verify section, 113
  checks on the book, its files and 47 engine runs; the engine's runs came from their cache,
  unchanged, and the 23 attribution books were computed again. The first cut's benchmark now earns
  14.85 points a year against the index's own 14.31, a gap of 0.54. **The misaligned third run had
  shown every limb of criterion 2 larger** — first-cut selection 24.46 points, the factor model's
  idiosyncratic return 61.02, the residual pass's selection 7.65 — and none of those figures is the
  record: they credited the book with the day's move its weights already held. Aligned, they are
  17.44, 13.84 and 2.70, and the rule's idiosyncratic return still beats all twenty random books.
- Outcome / decision: criteria 1 to 4 pass as the gate wrote them, criterion 3 exactly at its bar
  of 6 of 8, criterion 2 with every limb positive and none large. `FINDINGS_1.md` is the record.
  0.14.0 shaped its attribution inputs the same way, so its published split of 70% factor and 30%
  idiosyncratic is likely overstated on the idiosyncratic side; it stands at its tag as published,
  is not re-run here, and `RESULTS.md` says so beside it.
- Open threads: whether the worked example in the package pairs weights and returns the same way.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The owner signs criterion 5 and confirms the kill switch

- Idea / question: criteria 1 to 4 are evidenced in `FINDINGS_1.md`; does the owner sign, and does
  he confirm the kill switch the blueprint proposed for him?
- What we tried / considered: the gate was shown to him row by row, with criterion 2 passing thinly
  — nine tenths of the excess return factor exposure, the residual selection 2.70 points over the
  window — and the third run's larger, misaligned figures named beside the corrected ones. The
  kill switch was put to him as the blueprint's falsifier read on paper days, on either cost row,
  read first at the review of 2027-10-06.
- Outcome / decision: asked "Criterion 5: do you sign Experiment 1 into paper trading, frozen as of
  2026-10-06, with criterion 2 passing but thin?", he answered **"Sign it"**. Asked to confirm the
  kill switch, he answered **"Confirm as proposed"**. The book's section in `BITACORA.md` is
  written once with both, before its first day, and the book is frozen on 2026-10-06.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — Before the freeze: the paper book would have emptied when the desk's files ended

- Idea / question: the book's section in `BITACORA.md` says membership is held at the desk's last
  date once the index files fall behind, as `daily_update.py` flags. Does `paper_trading_1.py` do it?
- What we tried / considered: it did not. It read membership from the refinery's
  `r_index_weight`, which is never carried past the last date the desk wrote, 2026-08-14 — right
  for a backtest. On the 28 trading days after it the refinery reports no member at all, so the
  paper book would have sold every name on 2026-08-17 and held nothing until the desk refreshed
  its files. The worked example's paper book holds the last membership the desk wrote; this one
  had been written from the notebook's panel instead.
- Outcome / decision: `_load_panel` holds the membership of the desk's last date on every later
  day. Tested on the refined panel before any freeze: up to 2026-08-14 the membership is identical
  to the refinery's, so the rule the experiment ran is unchanged and no number moves; after it, 599
  members on each of the 28 days, where the refinery has none. The plumbing test is run again on
  the commit that carries it, and the freeze waits for it.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The published numbers, traced to the run before they are committed

- Idea / question: does every number in `FINDINGS_1.md`, `RESULTS.md`, `BITACORA.md`,
  `OBJECTIVE.md`, the banners and the changelog trace to the fourth run's printed output?
- What we tried / considered: an agent that had written none of them read each against the
  executed notebook, the universe notebook, the third run's notebook and the first run's log.
  Every engine and attribution figure matched. It found one wrong number — the members FMP does
  not price held up to **7.0%** of the index's weight in 2015, not 6% — the findings still reading
  criterion 5 as not given after the sign-off, the misaligned attribution called "the first
  attempt" where it was the third run's, "eleven years" for a window of 11.81, full coverage dated
  2022 where 2022 only rounds to it and 2023 is the first full year, and the random books cited for
  claim 2 alone when they differ from the rule in the cross and the ranking at once.
- Outcome / decision: each corrected before the commit, in `FINDINGS_1.md` first. **A correction
  to an earlier entry of this journal:** the entry on the sell-at-t−1 rule lists "five controls of
  the sweep, the 2% floor setting and its control", which reads as 32 runs; the 2% floor's control
  is one of the five, and the first run's log shows 16 of 47 runs failed, so 31 priced, as
  `RESULTS.md` says.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The plumbing test's dry run fails: the seed closed every live name on its source's last date

- Idea / question: the dry run in the scratch clone priced the book and its control over the
  whole history, then stopped on `KeyError: Timestamp('2026-10-05')` in the book's diagnostics.
  Why did a day the provider's files hold not exist in the book's calendar?
- What we tried / considered: the refined panel ended on 2026-09-24, while every curator file runs
  to 2026-10-05. `Universe/seed.py` wrote each listing's `valid_to` as its last price date in the
  desk's master — and for the 707 listings still trading, that is the day the master was last
  written, 2026-09-24, not an ending. The refinery reads each file only inside its span, so every
  live name stopped there. No stage of the experiment could notice: every one of them cuts at
  2026-06-01, where a span ending on 2026-09-24 and an open one read the same. A paper book is the
  first reader of the days after it. The book's own run for 2026-10-05, started beside the dry run,
  was stopped before it finished, and the uncommitted freeze was removed; nothing was committed.
- Outcome / decision: `seed.py` leaves `valid_to` empty for a listing still trading on the
  master's last date, which every reader of the seed already treats as an open span. The seed was
  rebuilt and the universe notebook run twice, as the data stage ran it — the first pass drops
  `CY` and `NBL` from the seed, the second writes the register from the seed without them. Against
  the committed versions, the seed and the master differ in `valid_to` on those 707 rows and in
  nothing else, and `Coverage.csv`, `Window.csv` and `Data_Issues.csv` are byte-identical: **no
  number of the experiment moves.** The refinery is re-run, and its rows up to 2026-09-24 are
  compared file by file with the panel the experiment read. The book is frozen again on the commit
  that carries the fix.
- Open threads: the template's seed contract says nothing about a span that ends on its source's
  last date; worth an issue upstream.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — Frozen, its first day run, and the first day checked before the freeze is committed

- Idea / question: is the frozen book the experiment's book, and is its first day right?
- What we tried / considered: the refinery, re-run on the seed with open spans, wrote rows up to
  2026-09-24 identical file by file to the panel the experiment read, all 803 files, and 705 of
  them now reach 2026-10-05. `promote.py 1` froze the book at `62256e6`; its first run, for
  2026-10-05, exited 1, flagged by the two stale-desk flags and nothing else. Five checks by agents
  that had written none of it, and a sixth set to find a reason not to commit: the frozen book's
  and its control's weights equal the experiment's on all 1,381 rebalance dates and the engine's
  daily values equal its headline runs on all 2,869 days, to the cent; the 30 names in force obey
  every condition of the rule, rebuilt independently to 1e-16; every hash in `FREEZE.json` holds,
  and nothing licensed or provided enters git.
- **What the days after the window show, read and set aside:** the engine has the book 24.9% below
  its 2026-06-22 peak on 2026-07-29, against 2.0% for `SPY`, in a sell-off of the memory, chip and
  optical names that held about seven tenths of its weight. The desk's own index returns agree with
  the provider's prices to 3.5 basis points a day through 2026-08-14: the market, not the data.
- **One bad input the checks found inside the window:** the provider's volume for `KLAC` is about
  ten times too high from 2026-05-13 to its 10-for-1 split of 2026-06-12, while its price stays
  unsplit, so its traded value — the rule's score — was inflated over the window's last 13 trading
  days. `KLAC` re-entered the book on 2026-05-14 and reached 2.6% by 2026-06-01, from about 1.1%.
  Prices are right; the weights of those days were chosen on a bad input. Not corrected — the
  rules are frozen — and written as caveat 7 of `FINDINGS_1.md` and a limitation in `RESULTS.md`.
- **One fault fixed before the commit:** `daily_update.py` let a step that raised exit 1, the code
  of a flagged day, and this book is flagged every day until the desk's files pass 2026-08-14, so a
  crash would have read as an ordinary day. It exits 2 now, with the traceback in the day's log,
  tested by injecting a failure; the scheduled command in `SETUP.md` keeps its output too.
- Outcome / decision: the freeze is committed with `BOOKS = ("Paper_Trading_1",)`. The rule file's
  hash at the freeze commit, which `FREEZE.json` does not cover, is written in `BITACORA.md`. Left
  for the owner, named there: the scheduled day has not run yet; the record and the frozen security
  master are on this machine only; the daily checks read only the newest day; a restatement flags
  again every day, and the day the desk's index reaches the day every past benchmark row will.
- Open threads: the branch reaches `main` when the owner has reviewed it; until then the schedule
  runs only on this branch. Upstream: the exit code, the seed's open span and the newest-day checks.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-06 — The owner merges 0.15.0 into `main`

- Idea / question: the previous entry left one thread open — the branch reaches `main` when the
  owner has reviewed it, and until then the schedule runs only on that branch.
- What we tried / considered: having read the gate row by row and signed it, registered the daily
  task himself, and seen the first day and its checks, the owner asked: **"merge it to main
  locally"**. `main` stood at 0.14.0's commit, an ancestor of the branch, so it was fast-forwarded
  without a merge commit and without touching the working tree while a dry run was reading it.
- Outcome / decision: `main` carries 0.15.0 and the frozen book, and the working copy the
  scheduled task runs is on `main`. Nothing is pushed: `main` is 18 commits ahead of `origin/main`
  until the owner pushes. The branch is deleted, as `AGENTS.md` asks of a merged one.
- Open threads: none.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-07 — The findings keep their promises, before the worked example is copied

- Idea / question: the KaxaNuk Researcher package is replacing its worked example with a curated
  copy of this repository, and a read of 0.15.0 against its own pre-registered gate found promises
  the findings had not kept, figures with no saved source, and a few wrong comments. Fix them here
  first, so the same book never has two findings files.
- What we tried / considered: every figure below was read from the record run's outputs on disk,
  untouched since 2026-10-06 — `Backtest/summary.csv` (sha256 `7d03a899…`), `sweep.csv`
  (`3b779305…`), `gate.csv` (`86d0c247…`), `benchmarks.csv` (`76aeb426…`),
  `Attribution/factor_model.csv` (`04bf9510…`), `brinson_fachler.csv` (`01368f11…`),
  `brinson_fachler_residual.csv` (`80c5214f…`) and `Portfolio/portfolio_weights.csv`
  (`d2a6ba17…`). The book's shape was recomputed in a read-only script from the engine's weight
  files: 1,381 rebalance dates of 2,869 days, a median of 37 names from 18 to 61, 19.0 effective
  positions, a largest weight of 15.0% on average, turnover 3.09 a year, the cap binding on 341
  dates at the notebook's tolerance, Technology from 19.9% to 60.7% and `KLAC`'s weights — every
  figure as published. The cap binds on 620 of 1,408 rebalance dates at 15% and on 141 of 1,358 at
  25%. The four falls in `BITACORA.md` and `CTVA`'s were traced to the price files of the
  download of 2026-10-06, before any refresh restates them.
- Outcome / decision: no number moved and no code behaves differently; nothing under
  `Paper_Trading/Paper_Trading_1/`, nor the shared `Data/Curator/custom_calculations.py`, nor the
  seed, was touched, so every hash `FREEZE.json` holds still matches.
  - `FINDINGS_1.md` publishes all twenty random books and the eight sweep cells, each with its
    control and the cap counts beside the two cap settings, as `BITACORA.md` promised before the
    run; says the shifted-entry timing arm was not run; says where each figure comes from; labels
    11.81 years as the engine's count, 2,976 weekday steps after the first day over 252, against
    11.41 calendar years; names the earlier versions without their tags; and signs "the owner".
  - `OBJECTIVE.md` quotes the owner's sentence with the "35" it had dropped, then the answer that
    retired the count.
  - `RESULTS.md` labels the engine's years and keeps the prior-close probe as an open item: this
    notebook checks that every holding had its cross at 1 at the prior close, and does not carry
    the probe.
  - `BITACORA.md`: the verdict row signs "the owner", and one dated line under the registered
    section records the traces; the section's earlier lines are as they were.
  - Comments only: the refinery's 63-day column names the analyzer, not the universe notebook,
    as the notebook that checks it; the weight writer says thirty weights, not forty; the sizing
    module no longer says no notebook writes a `.shift(1)`, since the rule cell lags eligibility
    itself; the analyzer's concentration comment says the cross members' traded value; the
    universe notebook's register lists *Spliced* once, not four times.
  - Three figures the run's own outputs correct, found by a trace of every figure before the copy:
    the realistic row adds 0.43 points of CAGR, not 0.42 — 20.7533% against 20.3279%, the margin
    taken before rounding as everywhere else; the members FMP does not price held at most 0.12% of
    the index's weight in 2022, on its first 37 trading days, not under 0.1% —
    `Universe/Coverage.csv`, 0.1161% on 2022-01-05; and the sell-at-t−1 rule changed every
    first-attempt book but two, the rule's and the control's 2023–2026 sub-periods, whose only
    engine runs are the first attempt's, written at 10:32 and read from the cache by every later
    run, so the engine priced 45 of the 47 weight files in the second run. No other figure moves,
    and the trial count stands.
  - Version 0.15.1, PATCH.
- Open threads: the entry of 2026-10-06 above says the owner registered the daily task; on
  2026-10-07 neither the machine's task scheduler nor the Claude app's scheduled tasks hold one,
  and no day after 2026-10-05 is logged. Registering it, as `SETUP.md` says, is the owner's act.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-07 — Copied into the KaxaNuk Researcher as its worked example

- Idea / question: the owner asked on 2026-10-05 for Golden Flow to become the example strategy for
  the researcher. How is a live strategy copied so a newcomer can read it, with nothing private in
  it and no figure changed?
- What we tried / considered: a mirror of the repository, or a curated copy. A curated copy: the
  strategy's own repository keeps its full history, and the package gets Experiment 1 as it stands,
  with no rule and no kept number lost. The source is Golden Flow 0.15.1, the version of the entry
  above. Golden Flow ran on template 0.13.2; the text this copy shares with the template is
  template 0.14.0.
- Outcome / decision:
  - **Documents.** Each keeps template 0.14.0's lines verbatim, but for the exceptions the
    package's `AGENTS.md` writes down — the status banner, `SETUP.md`'s `init-example` lines,
    `OBJECTIVE.md`'s body and `CHANGELOG.md`'s entries — and `README.md`, which is the
    example's own, whole. Golden Flow's lines sit inside example markers, after the template
    guidance they answer. The blueprint's lines are verbatim, with one marked key line under its
    blockquote; one of its lines is split where the template's sentence it repeats ends, before
    "Fixed now, as the owner approved them:". This journal keeps Golden Flow's entries from
    2026-10-05 whole, leaves out the entries its first note names, and makes four replacements
    in square brackets. Copied lines keep their length, so some run past 100 columns, and so do
    two lines a replacement lengthened.
  - **The index.** The example reads it under the Analytics Factory's own file names,
    `KN_US_Equity_Benchmark_Holdings.csv` and `KN_US_Equity_Benchmark_Returns.csv`. They are
    byte-identical to the `KN_US_Equity_Core_*` files the record ran on: md5
    `eba4bf64ffa8de5d650e4e2c4b21844d` and `1668b564582f1871d7e4a6f39896e50a`.
  - **Code.** It is Golden Flow 0.15.1's, with these differences:
    - the module docstrings are the template's; a short comment written for this copy, from
      what Golden Flow's docstrings and records say about the module, opens its marked code;
    - `Data/hand_supplied.py` reads the two index files under the names above;
    - "the desk" is written "the Analytics Factory" in comments, docstrings and one message, and a
      line this made longer than 100 columns is rewrapped;
    - `Universe/seed.py` takes `--index-master` as a required argument and names no machine path;
      its shorter docstring says it overwrites the committed seed;
    - the notebooks keep the template's markdown, with Golden Flow's paragraphs marked inside it,
      and every code cell starts `# EXAMPLE-ONLY CELL`.
  - **Byte for byte:** the seed, `Universe/Investable_Universe.csv`, and in
    `Paper_Trading/Paper_Trading_1/` the frozen copies and `FREEZE.json`, but for the frozen
    security master, the provider's data, which is not shipped.
  - **The figures** come from the record run of 2026-10-06, on Backtest Engine 0.66.0 and
    Attribution Analysis 0.2.0.
  - **The paper record** stands as of 2026-10-05, the only day logged; no scheduled day has run.
    In this copy the book does not run, and `Paper_Trading/BITACORA.md` says why.
- Open threads: the paper record continues in the strategy's own repository, and this copy does not
  follow it. The first kill-switch reading is at the review of 2027-10-06.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-07 — The package ships the copy

- Idea / question: the owner asked to tag and push the KaxaNuk Researcher 0.34.0, whose worked
  example is now a curated copy of this repository's 0.15.1, and this repository with it; the
  documents here still said the package shipped `liquid-golden-cross`.
- What we tried / considered: the README, `AGENTS.md` and `SETUP.md` lines that described the
  package; the journal and the changelog keep what they said when they were written.
- Outcome / decision: the three documents say the package ships the copy, `examples/golden-flow/`,
  from KaxaNuk Researcher 0.34.0, and that this repository stays the live strategy, which the copy
  does not follow. `main`, with the tags 0.13.0, 0.14.0 and 0.15.1, was pushed on 2026-10-07 at the
  owner's word. Version 0.15.2, PATCH.
- Open threads: the daily task, as the entry above says.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-23 — Experiment 1 is rewritten a second time: the owner's decisions, in his words

- Idea / question: the owner asked for the reference example to be brought to the KaxaNuk
  Researcher of the day and run end to end *"since 2000 (we should have factor data and benchmark
  since then)"*, on the new inputs — *"we have now sharadar and the new KN US Equity Core
  benchmark"*, and the factor model's new numbers — and for a paper to come out of it: *"tenemos
  que revisar que todo haga sentido y no estemos cometiendo ningun error o assumiendo cosas que se
  alejen de la realidad point in time"*. He added a constraint 0.15 did not meet: *"no quiero una
  estrategia que tenga demasiados rebalanceos y sea demasiado difícil de probar en mi cuenta de
  broker"* (in English: not too many rebalances, easy to test in his broker account). 0.15.2
  re-strikes on 1,381 of 2,869 trading days.
- What we tried / considered: an Experiment 2 beside 0.15.2, or a second rewrite of Experiment 1.
  The owner chose the **rewrite**, under the procedure `AGENTS.md` sets: this entry, a new
  `BLUEPRINT_1.md` naming the blueprint of 2026-10-06, 0.15.2 kept at its tag and as a row of
  `RESULTS.md`, and the runs of 0.13.0, 0.14.0 and 0.15.x counted in this experiment's trials. Every
  decision below was taken in chat on 2026-10-23, before any stage of this version ran.
- Outcome / decision:
  - **Universe.** The KN US Equity Core as the desk supplied it on 2026-10-22, from the owner's
    Downloads folder, byte for byte (the same files as the factor model's `Data/Supplied/`):
    `index_daily_holdings_1998.csv` (md5 `49e70b8537ad923ac2c1afc8b0ea1164`),
    `backtest_returns.csv` (md5 `b2c804f5a383b1fc5d9810a35f7f3aab`),
    `backtest_components_mask.csv` (md5 `d42becfb5f32e3befb02351a4cb65f1b`) and `tickers.csv`
    (md5 `e41397073f3a764ed8c88030a473d903`). 2,199 listings keyed by Sharadar ticker, 640 to 915
    members a day, 1998-12-31 to 2026-08-14; the weights sum to one within 3e-5 every day and the
    mask agrees with them on every cell. The returns file has ISO dates and a blank return header.
    It is a wider index than 0.15's Core, which held about 600 names from 2000.
  - **Prices.** **Sharadar**, through the Data Curator 0.51.0, the first release with its provider.
    Sharadar keeps delisted securities, so lie 1 of `AGENTS.md` is no longer accepted: it is close
    to removed, and what is left is measured. The download carries only the columns a stage reads.
  - **Window.** 2000-01-03, the factor model's first date, or the first date on which the members
    with a price and a signal hold 90% of the Core's weight, whichever is later; to 2026-08-14, the
    last date of the Core and the factor model. Nothing is held out: there is no later data.
  - **Factor model.** *"espero que el modelo de factores nuevo ya tenga la correcion en
    momentum"*: the KN US Equity Factor Model's Experiment 1, whose Momentum skips the latest
    month, by desk ticker, 2000-01-03 to 2026-08-14 (`factor_files/experiment_1/Desk/`, md5 of
    `Momentum.csv` `7724586d9165b3e154301086d4caa7b6`). Its repository says [the factor model's owner] has not
    reviewed it and every figure is provisional; so is every attribution here.
  - **Rebalance.** **Monthly, on a fixed date**: struck on the last trading day of each month and
    filled at the **next day's open**, a market-on-open order (Sharadar publishes no VWAP). A
    **no-trade band of 0.5 points**: a held name keeps its drifted weight unless its target differs
    by more than half a point; entries and exits always trade. The sweep tries 0.25 and 1.0, read on
    turnover only.
  - **Cash.** *"no usese bil, usa cash si llega a pasar"*, then *"inviertelo a una tasa usando datos
    de la fred de la tasa interbancaria o de reporte ... y que asuma costos como los de interactive
    brokers"*, and *"all this cost should be simulted using the backtest engine nothing outside"*:
    no cash fund. What the bounds cannot place is **USD cash**, paid by the engine at FRED's
    effective federal funds rate (`DFF`) less half a point, floored at zero, ACT/360, as
    Interactive Brokers pays on a dollar balance — the engine's `financing_benchmark_rate` rate file
    and `cash_interest_spread = -0.005`. The same rate is the risk-free rate of every Sharpe ratio
    the engine reports, so Sharpe ratios here are excess of cash, where 0.15's were not. SOFR was
    considered and set aside: it starts in 2018, and DFF is the rate IBKR's dollar benchmark follows.
  - **Costs.** *"we can increase in bases the transaction costs instead of cents"*: commission
    **1 basis point of notional** (`commission_model = "basis_points"`), about IBKR's fixed
    half-cent a share on a fifty-dollar share; slippage **`spread_plus_impact`**, a Corwin-Schultz
    half-spread from Sharadar's daily high and low plus square-root market impact from its volume.
    A stress row at 5 bp commission and 10 bp flat slippage. All inside the engine.
  - **Delistings.** With Sharadar, a delisted name has prices to its real last trade, often over the
    counter. The engine sells a held name there (`delisted_position_handling =
    "sell_at_last_price"`), which **drops 0.15's one stated leak**, the t−1 exit that needed a day of
    hindsight. The t−1 exit stays only for a gap inside a series, which the engine cannot price.
  - **Capital.** $1M as the headline, as in 0.15, and a $100k row for an account the owner can test.
  - **Sign-off.** The owner's approval of the plan of 2026-10-23 is the go on the blueprint's
    parameters above; the night stops at the gate's verdict: no signature, no freeze, no push.
- Open threads: the Sharadar account answered *"exceeded the API speed limit and your account has
  temporarily been disabled"* (HTTP 429) on the evening of 2026-10-23, before this version's
  download; the curator waits for it and asks in batches of 25 with a pause between. The seed
  reads Sharadar's catalogue as exported on 2026-09-24 (md5 `f26a268032658d0f7fba08d6c70dd947`),
  copied from the benchmark repository's provider cache rather than asked for again; four Core
  listings are not in it: ADRX1, SAGE, SKYD and WBA.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-23 — The data stage on Sharadar: what the provider is, and what the Curator rebuilds

- Idea / question: can the Core's 2,199 listings be priced from 1998 on Sharadar as the market
  priced them, before any rule exists?
- What we tried / considered:
  - **The account.** The startup subscription is served by Sharadar's own API,
    `api.sharadar.com/v1.0`, not Nasdaq Data Link: the evening's HTTP 429 "account temporarily
    disabled" came from asking `data.nasdaq.com` with this key. The seed's catalogue
    (`/data/tickers?years=full`, md5 `efdfffb59f3944a0062cfe4770accb4f`, fetched 2026-10-23) and
    the corporate actions (`/data/actions?years=full`) are taken whole from it; the Curator's
    provider already used it. Data Curator 0.51.0, ten seconds between batches of 25 at the
    owner's word ("maybe go slower in the download").
  - **Three decimals.** Sharadar rounds every price to three decimals, its adjusted ones included:
    its raw rows for AAPL on 1998-01-02 read close 16.25, split-adjusted close 0.145, adjusted close
    0.121. The Curator's dividend and split blocks would rebuild the adjustment, but with the
    Sharadar provider any `d_*` or `s_*` column stops a run ("Column not available under prefix"),
    so `Data/curator.py` rebuilds it after the download from the exact close and the actions bulk
    file: splits (a ratio, new to old), cash dividends and spin-offs (cash a share, in today's
    split-adjusted shares).
  - **Splits after the window.** NFE's 1-for-50 of 2026-09-14 is in every NFE price and dividend
    since 2019; the first rebuild dropped actions after the window's end and read NFE's dividends
    as 17% a quarter. Fixed: a split after the last day counts on every day.
  - **A factor no action records.** NVTP's split-adjusted prices are a hundred times its close with
    no action to say why; the rebuild takes Sharadar's constant wherever the two bases differ by
    one, so the rebuilt price, Sharadar's volume and its dividends stay on one basis.
  - **Volume adjusted twice.** The universe notebook's first split check flagged 316 names — its
    tolerance read any big liquidity move around a split as a fault. Measured split by split: at
    82 splits in 77 listings (BBWI 2000-05-31, FAST 2002-05-13, GILD 2002-03-08, EBAY, CLF, NVDA,
    NFLX…) traded value steps by the split's own factor while the shares the tape printed stay
    flat — the volume before the split was already in post-split shares, FMP's fault of
    Data-Curator #36 on Sharadar. The Curator divides the earlier volume by the factor where both
    hold (within 10% and 15% in logs, 30 days each side, splits of five for four or more); the
    universe check reads the same signature and finds none left.
- Outcome / decision:
  - **Checked file by file** against Sharadar wherever its decimals allow (prices of ten dollars or
    more): 2,199 files; three with a day off by more than 0.5% — BILL and IOT on 2025-06-03, a
    one-day glitch in Sharadar's adjusted close the rebuild does not share, and CXW in 1998,
    dividends Sharadar books on other dates than its actions table — and no split-adjusted close
    off Sharadar's. The open keeps Sharadar's rounding: 0.23 bp of the Core at most.
  - **The universe:** 2,198 listings priced (UB is not in Sharadar), the window opens on the floor,
    2000-01-03, at 98.1% of the Core priced and signalled and never below 96.5%; the share of the
    Core with no price is at most 0.11% on any day, against about 7% on FMP in 0.15. Excluded by
    name, the register's blocking rows: FPS, H1, ILA.A, MDLN, Q and SUNB, with less than 200 days of
    prices while members, and TXCCQ, whose adjusted price moves more than sixfold in a day.
  - **The analyzer** wrote `RESULTS.md`, *Before any experiment*, rows 1 to 17, and its section 1.1
    measures the provider's precision and what the Curator rebuilt.
  - **Issues filed at the owner's word** ("send the issues to each", "report all data issues to
    data curator and kn us equity benchmark"): Data-Curator #39 (dividend and split columns
    unreachable with Sharadar), #40 (`c_daily_traded_value` empty without a VWAP), #41 (rebuild the
    adjustment where a provider rounds), #42 (Sharadar's data faults found here); and
    [an issue in the Analytics Factory's private repository] (the Core's findings, and whether its construction reads the
    same double-counted volume).
- Open threads: the open fill keeps three decimals; the Core may carry the volume fault in its own
    construction (issue #10); the deflated Sharpe stays uncomputed.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-23 — The rule read back on one worked date, before its blueprint

- Idea / question: does the rule, as the owner decided it, do on a real date what its one sentence
  says? *On the first trading day of each month, at the open, hold the KN US Equity Core's members
  whose 50-day average sat above their 200-day one at the month's last close, each in proportion to
  its 63-day traded value, none above 20% and none below 1%; leave a held name alone when its
  target moved by half a point or less.*
- What we tried / considered: the book of 2026-08-03, struck on the close of 2026-07-31, computed in
  a scratch script with `portfolio_construction.bounded_by_score` on the refined panel — no rule
  cell holds code yet.
- Outcome / decision: 703 members, 456 in a golden cross, all 456 with a fill price; the bounds hold
  **28 names, fully invested**: MU 18.8%, NVDA 12.3%, SNDK 8.6%, AAPL 6.7%, AMD 6.2%, INTC 5.7%,
  AMZN 4.8%, GOOGL 4.6%, AVGO 4.0%, MRVL 4.0%, then AMAT, LITE, WDC, QCOM, STX, LRCX, BE, LLY, DELL,
  KLAC, JPM, GEV, CAT, CSCO, GLW, V, RKLB and TXN between 2.0% and 1.0%. The 29th, UNH, is out
  because adding it would put the smallest weight under 1%. The most traded members out on the
  cross are TSLA, MSFT, META, PLTR and ORCL, each with its 50-day average below its 200-day at the
  close. MU's $48.6bn a day over 63 days, above NVDA's $31.8bn, was checked against Sharadar's raw
  rows: about $800 to $1,200 a share on about 50 million shares a day, as published. No cap binds
  on this date; the book is a semiconductor and memory book this month, which the 20% cap does not
  prevent.
- Open threads: the owner's yes to this read-back is his approval of the plan of 2026-10-23, which
  fixed every element above before the run.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-23 — The blueprint's draft, put to its critic cold, and what was done about each objection

- Idea / question: what does a reader with no stake find wrong in the draft before it is committed?
- What we tried / considered: the `blueprint-critic` agent read the draft, `AGENTS.md`,
  `OBJECTIVE.md`, `RESULTS.md`, the three entries above and every note the draft cites, and wrote
  nothing. Six blocking objections and nineteen others.
- Outcome / decision, objection by objection:
  - **B1, the reason did not cover the falsifier's CAGR limb.** The thesis now takes the return
    limb from the analyzer: forward 21-day return on the pool 0.87% with the cross on against
    0.20% off, beside the volatility (rows 10 and 11), and the compounding argument; the single-name
    reading is labelled the blueprint's, the notes being on indices.
  - **B2, claim 1's status hung on a lead and a replaced version's status.** The table now reads
    the benchmark limb from success criterion 1, names the middle case "confirmed against its
    control only", and says `OBJECTIVE.md`'s status of 0.15 is rewritten from this version's
    findings, never kept.
  - **B3, claim 2 had no status; claim 3 broke under the band.** Claim 2 against equal weight is
    falsified as a source of Sharpe if prediction 3 holds, confirmed as a book if it fails; its
    random-draw half stays a lead. Claim 3 holds on targets, and the band's half-point excursions
    outside the bounds are reported in section 2.1.
  - **B4, trades off the monthly dates.** No book re-strikes between its dates: the engine's sale of
    a delisted name is a sale; a name the engine refuses for a gap inside a series is excluded by
    name from every book and the run priced again. Success criterion 3 now states tradeability,
    since twelve dates a year hold by construction.
  - **B5, the control's eligibility.** Written in full: every condition of the rule but the cross,
    the same bounds, band, cash, costs and delisting rule, on the rule's dates.
  - **B6, gaps in what may not rescue the falsifier.** Added: the universe and its files, the
    provider, the rebuild and the volume correction with its tolerances, the traded-value
    definition, the control's definition, the gap and delisting rules, the slippage model and its
    fallback.
  - **N1** Faber and Hurst now cited as context on indices. **N2** the Core's history as a backtest
    of its rules is a key risk, asked of the desk in issue #10. **N3** traded value is the
    rebuild's close times volume, and `OBJECTIVE.md` is brought to it with the findings. **N4** the
    open price on d is named as the one same-day condition, a small leak. **N5** the band is read
    back below. **N6** Sharpe ratios are excess of cash and not comparable with 0.15.2's; the flat
    spread is named a simplification. **N7** what the cost model does not do is stated: no
    per-order minimum, an undocumented window on the fill's day, integer shares on adjusted prices;
    `AGENTS.md`'s fourth lie is brought to the engine's basis-point commission in the documents
    pass. **N8** the window's floor is the owner's, chosen after 0.15's results, confirmed by the
    coverage rule. **N9** leads say what would have licensed them and are counted as leads, not
    trials. **N10** the findings report the share of months the book beat the control and the two
    books' overlap beside every margin. **N11** Han, Zhou & Zhu's wording corrected; Daniel &
    Moskowitz added against prediction 2. **N12** the equal-weight arm is capped at 20% with the rest
    in cash. **N13** lead 6 is now checkable: 15 to 60 names on most dates, the cap binding on fewer
    than a quarter. **N14** lead 8 follows Paleologo: momentum small. **N15** the 0.22% cites
    analyzer section 1.1, and 2009–2017 is "close to nothing" on the cross's rows only. **N16**
    folded into B4. **N17** random books draw from what the control may hold; the $100,000 rule and
    control are counted as books, the trial count 152. **N18** the over-the-counter sale is named a
    caveat with Shumway (1997); Kaminski & Lo's wording corrected. **N19** Daniel & Moskowitz is a
    key risk.
  - **The band, read back (N5)** with `portfolio_construction.banded_book` on the books of
    2026-07-01 and 2026-08-03: July held 30 names, August's target is 28; 16 held names keep their
    drifted weights, 12 orders go in — TXN and V enter, CRWV, UNH, WMT and XOM leave, six names
    resize — and 1.4% stays in cash. Kept names can drift under the floor: GLW is struck at 0.72%
    against a 1.11% target, within the half point. At weights near 1% the band is wide in relative
    terms; it was fixed for the number of orders, before any return.
- Open threads: none blocking; the blueprint is committed alone, next.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-24 — The cycle: three runs, what the engine charged, and the verdict

- Idea / question: does the monthly book of the blueprint of 2026-10-23 pass its gate, priced by the
  engine with every cost and the cash's interest inside it?
- What we tried / considered:
  - **First run.** The engine refused every book: `Configuration` requires `commission_cents` even
    with basis-point commission (`TypeError`). `build_configuration` now passes 0.0 — a defect for
    the Backtest Engine's issues.
  - **Second run.** 63 engine runs and the attribution; Verify raised. (a) The band's invariant
    checked the struck weight against its target within the band, but the rule scales traded names
    down when kept names hold more than their targets, as the blueprint says: rewritten as "no
    struck weight above its target by more than the band", then given one point of overnight
    allowance in the third run, since a kept name is decided at the close and written at the next
    open. (b) Twenty runs stopped valuing early — "Cash error on <date>" — at rebalances whose costs
    outran the 1% reserve: eighteen random books, two sweep settings, the rule at $100,000.
    (c) **The costs were not believable.** The rule paid $362,502 of slippage against $15,573 of
    commission at 1 bp: about 23 bp a trade on average, 40 to 55 bp on dates such as 2000-01-03 and
    2026-08-03, on AAPL, MSFT and NVDA. The stress row — 5 bp commission and 10 bp flat — was the
    cheaper of the two. The engine's Corwin–Schultz estimate reads a megacap's daily range as spread.
    One pricing of the rule with the engine's other estimator, Abdi–Ranaldo (reading the
    split-adjusted close as well), gave 7 to 40 bp a trade, median by year — no better.
  - **What was done, and what was not.** The pre-registered row stays the record, marked; **every
    book was priced again at a flat 5 bp, the blueprint's own fallback half-spread** — the same
    weights, no new book, a forking path counted beside the trials. Truncated runs are excluded by
    name in the notebook (`Backtest/excluded_runs.csv`) and every criterion that needs one reads "not
    evidenced"; Verify raises only if a run is neither read whole nor excluded with its reason, or if
    the rule, the control or equal weight is excluded. The cash reserve was not raised: it is on the
    blueprint's list of what may not rescue the falsifier.
  - **Third run**, 2026-10-24: 102 engine runs, 81 read, 21 excluded by name; Verify passes, 71
    checks.
- Outcome / decision:
  - **The falsifier does not fire**: the cross beats its control by +0.065 Sharpe and +1.30 points
    (flat: +0.105 and +2.24), on both measures in 2000–2008 and 2018–2026, losing in 2009–2017.
  - **The book does not graduate**: its Sharpe, 0.162 (flat 0.221), is below the Core's 0.308 and
    `SPY`'s 0.307; every sweep setting keeps its margin over its control and none beats the Core.
    Criteria 1 and 3 fail at both cost rows; 2 is not evidenced (13 of 19 random books at the flat
    row). The whole shortfall is 2000–2008, −13.7% a year against the Core's −3.4%: the bubble's
    most traded names, held into the fall, left late by a monthly cross.
  - **Tradeable by hand**: about twenty orders on each of twelve dates a year, turnover 2.16; 1,481
    orders under $100 are the band's residue, a kept name re-traded by a few dollars.
  - **Attribution**: four fifths of the excess return is factor exposure; momentum is the largest
    style (+31.9 points), against lead 8; idiosyncratic +43.2, residual selection +7.7. The first
    cut reconciles to 0.07 points a year.
  - `FINDINGS_1.md` rewritten; `RESULTS.md`, `OBJECTIVE.md` and `BITACORA.md` compiled from it.
- Open threads, for the owner: which cost row the gate is read at (it does not change the verdict);
  whether `Paper_Trading_1`, the 0.15.2 book, keeps running; a quoted-spread source for the
  `Bibliotheca/`; and the issues for each part of the Investment Lab this run found.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-24 — The owner reads the gate at the flat 5 bp row, and keeps it

- Idea / question: which cost row is Experiment 1's gate read at, and does the gate change after the
  book failed it?
- What we tried / considered: the pre-registered row, the engine's Corwin–Schultz spread, which
  charged megacaps 23 to 55 bp a trade; the flat 5 bp row, the blueprint's own fallback
  half-spread; and the owner's idea of graduating a book that works only in some periods, through the
  momentum and size exposures it carries.
- Outcome / decision: **the gate is read at the flat 5 bp row**, the Corwin–Schultz row reported
  beside it; **the gate is kept as it is**, five criteria and the same margins, for [the next experiment] as
  well — a book that works only in a declared regime is a later experiment with a gate of its own,
  written before its run. The verdict does not move: criteria 1 and 3 fail at the flat row.
- Open threads: [the next experiment, which this copy does not hold].

<!-- example: end -->

<!-- example: begin -->

## 2026-10-24 — The adjustment moves into the Curator's own calculations, and no number moves

- Idea / question: can the rebuilt adjustment be computed by the Data Curator itself, from
  Sharadar's dividends and splits, instead of a post-step over the actions bulk file?
- What we tried / considered: the entry of 2026-10-23 says the `d_*` and `s_*` columns stopped a
  run with the Sharadar provider. That was a wrong column name, not a limit of the library: once the
  dividend and split blocks are mapped to the provider, the joined names
  `d_ex_dividend_date_dividend_split_adjusted`, `s_split_date_numerator` and
  `s_split_date_denominator` are read (Data-Curator #39, closed). The rebuild is now eight `c_*`
  calculations in `Data/Curator/custom_calculations.py` — the split ratio, with Sharadar's constant
  basis where a factor has no split and a split after the window; the total-return close and its
  ratio; the open on both bases; the total log return; traded value with the volume counted twice
  corrected; and the total-return volume. The one action the dividend column does not carry is a
  spin-off (GE HealthCare, GE Vernova and 245 more files): `Data/curator.py` adds them after the
  download from Sharadar's actions file (Data-Curator #43). `c_daily_traded_value` and
  `c_log_returns_dividend_and_split_adjusted` are renamed `c_traded_value` and
  `c_log_returns_total`.
- Outcome / decision: ten reference names (AAPL, NFE, NVTP, FAST, GE, KO, LEHMQ, MSFT, CXW, BILL)
  match the earlier rebuild to 1e-14 or better. The full download, the refinery, the universe and the
  analyzer re-ran; the adjustment checks read as before (three files with a day off Sharadar's,
  none with a split-adjusted close off). Experiment 1's struck weights match the published ones
  except in 10 of 162,880 cells, by 1e-6, the sixth decimal of the weight file, where a difference of
  1e-14 lands on a rounding boundary. Every engine figure re-ran and matches FINDINGS_1 to its last
  digit (the rule's Sharpe 0.1620, flat 0.2214; the Core 0.3075; `SPY` 0.3070), and so do the rule's,
  the control's and equal weight's attribution (idiosyncratic +43.22, +29.65, −9.08; Brinson alpha
  +26.85, selection +18.71; residual selection +7.68). The random books' attribution was stopped
  before it finished: it is re-run on Attribution Analysis 0.5.0 next. No published number moves.
- Open threads: the run took over six hours, 98% of the engine's share of it loading CSVs one book
  at a time. Before [the next experiment] the pipeline moves to the engine's batch mode, Parquet read with
  PyArrow and Attribution Analysis 0.5.0, with Backtest Engine 0.67.0 (the owner's decision of
  today), and Experiment 1's attribution is read again on 0.5.0.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-24 — Attribution Analysis 0.5.0 by KN sector, linked; a faster pipeline; Paper_Trading_1 retired

- Idea / question: the pipeline took over six hours, and the attribution library was three
  releases behind. Before [the next experiment], every library on its newest build, every step fast enough to
  re-run end to end, and Experiment 1's attribution read again on the new library.
- What we tried / considered:
  - **Versions** (the owner's rule of today: check every library before a run). Data Curator 0.51.0,
    the newest; Backtest Engine 0.67.0, installed, which gives the six headline books the same
    Sharpe and CAGR as 0.66.0 to six decimals; Attribution Analysis 0.5.0, installed from the
    library's own repository at `1ed3b09` (0.5.0 with its unreleased by-year tables), because its
    licence index answered 503. The unified KaxaNuk licence server validates it with the owner's
    engine key; the key filed for attribution is the old server's.
  - **Where the time went.** 445 of the engine's 452 minutes were spent loading CSVs, once per
    book; the attribution sent each worker the whole universe's returns. Now: every per-security
    file is Parquet, written and read with PyArrow through `Data/time_series.py` (the universe
    notebook from about four minutes to 28 seconds, its four files byte-identical; the refinery's
    files equal to 1e-12; the panel loader twice as fast and bit-identical); the engine prices books
    in its batch mode, one load of the market data per batch, from a slim CSV copy of the eight
    columns it reads (its Parquet reader refuses these files on 0.66.0, reported); attribution
    runs through the library's own pipeline, `attribute()`, in about twenty seconds a book.
  - **The owner's decisions for Attribution Analysis 0.5.0, before its first run**: the textbook
    Brinson-Fachler (1985) by KN sector, so allocation is the sector bet and selection the names
    picked inside a sector, as `AGENTS.md` describes the first cut; and Carino linking, so every
    cumulative effect adds up to the compounded return over the 26 years. Each security's KN sector
    is read from the factor model's own sector files — one sector per security, the classification
    the second layer prices; 51 listings no sector file carries are `unclassified`. The cash the
    book leaves uninvested is a segment of its own at a zero return. The library computes the
    idiosyncratic residual itself, as the return its factors leave unexplained, instead of reading
    the model's residual file.
  - **`Paper_Trading_1` retired** (the owner's decision: Sharadar is the only provider kept, and no
    FMP file is). It recorded one day, the first run by hand on 2026-10-05; the daily task was
    never scheduled. Its frozen files stand at tag `0.15.2`.
- Outcome / decision: Experiment 1 is re-run end to end on the new pipeline and the new library.
  The engine's figures are expected not to move; every attribution figure will, because the formula
  and the linking changed: the published ones are simple sums of daily effects on the 0.3 formula.
  `FINDINGS_1.md` is rewritten from this run, and says which number moved and why.
- Open threads: the engine's Parquet reader; a load of about five minutes per batch, in the
  engine; the owner's `.env` line for the attribution licence.

<!-- example: end -->

<!-- example: begin -->

## 2026-10-27 — The gate has two layers, and Experiment 1 reads as sound and regime-dependent

- Idea / question: the entry of 2026-10-24 kept the gate as it was, five criteria, and set aside
  the owner's idea of a book that works only in some periods. Under it, Experiment 1 simply does
  not graduate. Does a book that was tested correctly, and fails over the whole window while it
  earns in named periods, have an outcome of its own?
- What we tried / considered: the five criteria as they stood; and a gate in two layers, which
  asks first whether the experiment was done correctly and then whether the book earns its place.
- Outcome / decision: the owner decided on 2026-10-27 that **the gate has two layers and three
  outcomes**, in `Paper_Trading/BITACORA.md` for every experiment from now on.
  - **Soundness**, each row with its evidence, a row without evidence not holding: S1 no
    survivorship bias, S2 no look-ahead, S3 no overfitting, S4 costs and capacity stated, S5
    reproducible. **Performance**, the former criteria 1 to 3: P1 beats the benchmarks and its
    control over the whole window, P2 idiosyncratic alpha in both layers, P3 survives perturbation.
  - **The outcomes**: *graduates*, when every row holds and the owner signs it off; *sound and
    regime-dependent*, when every soundness row holds and performance fails over the whole window
    but holds in named periods; *not sound*, when a soundness row fails — no conclusion is drawn,
    and the experiment is fixed and run again.
  - **Experiment 1 reads as sound and regime-dependent**, at the flat 5 bp row the gate is read at,
    on the run of 2026-10-24; no figure is computed again. S1 to S5 hold on the evidence
    `FINDINGS_1.md` quotes; P1 and P3 fail and P2 is not evidenced. Against its control the book
    earned in 2000–2008 and 2018–2026 and lost in 2009–2017; against the KN US Equity Core it
    earned in 2018–2026 only. `FINDINGS_1.md`'s gate section is rewritten in the two layers.
  - **It is not paper traded alone.** It may be paired with another signal in a later experiment,
    or used at a portfolio manager's discretion; the decision, and its risk, are theirs. Nothing
    here recommends either.
- Open threads: the condition that tells the periods apart. The evidence names them after the fact
  — the bubble's most traded names held into the fall of 2000–2008, left late by a monthly cross —
  and no signal that could be read in advance; a later experiment would have to find one.

<!-- example: end -->
