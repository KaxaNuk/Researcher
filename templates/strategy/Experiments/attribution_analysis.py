"""
Attribution analysis -- step 6 of 8, the fourth shared module.  Shapes what the KaxaNuk Attribution
Analysis library needs, and says what is missing before it tries.

In plain words: which part of the return did you actually earn?

Runs inside an experiment notebook, section 5, after the backtest.

What is expected here:

- Say what is present.  The library needs four inputs: an index's daily holdings and its daily
  returns, one or more factor-return files, and the book from step 5.  The first three come from
  KaxaNuk's Analytics Factory, read in place by `Data/hand_supplied.py` from the folder
  `KN_ANALYTICS_PATH` names, or from the drop zones under `Data/Curator/`.  Check for them first
  and report the gap in a sentence, so a clone with no licence and no index files pays nothing
  to find out.
- Speak the book's language.  The index's holdings and the factor files key a listing by the
  index's own ticker; the book keys it by `main_identifier`, the identifier the experiment's
  provider prices it under.  Map one to the other through the seed's two keys, as
  `Data/hand_supplied.py` reads them, before any pass, so `BRK.B` and `BRK-B` are one security and
  a listing the seed does not price is left out rather than matched by accident.  The map comes
  from the strategy's seed builder, or from the Analytics Factory where it supplies one.
- Compare against the index the strategy can price.  On each date, a member with no price -- one
  the experiment's provider does not carry, or a date outside the span its file speaks for -- is
  dropped from the index's holdings and the rest renormalised, and the share dropped is reported
  per year: a member left in at a zero return hands its return to the book as alpha.
- Take the book as a daily series, from `Backtest/`, never from `Portfolio/portfolio_weights.csv`.
  The library rejects a weight file that is not daily once it spans a year, and the rebalance-date
  file the engine read is exactly what it refuses.  The book it attributes is the one the engine
  held each trading day, drift and its cash included; the benchmark's holdings follow the same
  rule.
- Hold both weight tables overnight.  The engine's daily weights and the index's holdings are
  struck at a day's close, after that day's return has moved them, and the library pairs a weight
  with the return of its own date.  Paired as they arrive, a weight that already holds a day's
  move earns that move again, and every book -- the index's too -- is credited with the
  cross-section's daily variance, several points a year, in every pass.  Move both tables one day
  on, so the close of t-1 earns day t, after the asset returns are read on the engine's own days.
- Reconcile the benchmark before any figure is read.  The first cut's benchmark return, mean daily
  times 252, against the index's own returns file over the same days: more than a point a year
  apart, and the benchmark the book was compared with is not the index -- weights a day out,
  members unpriced, a book not widened -- so the notebook's Verify section raises.  The returns
  file never enters the library, which is what makes it the check.
- Widen the book to the benchmark before handing it over: every benchmark constituent the book
  does not hold, added at zero weight, each with its own price series.  The library prices only
  the securities named in the book, and the first cut computes the benchmark's return from those
  prices alone -- the index's own return series is never one of its inputs.  A book that names only
  what it holds is compared against the fraction of the index it happens to own, and the
  difference is reported as alpha, most of it filed under interaction, where nobody looks.  Drop
  the engine's benchmark column on the way, which it returns at zero, and keep the cash position.
- Shape what the library reads in one place, never in a notebook: no nulls, each side's weights
  summing to one, and the cash the rule leaves uninvested a segment of its own, at a zero return,
  so the book's cash is neither dropped nor read as a security.  Where the library loads files, its
  loader decides the layout by **one cell**, the first header: `Ticker` means securities down and
  dates across; `date_column` means dates down and securities across; anything else -- `date`,
  `m_date`, the name a provider happened to use -- raises before a number is read.  Where it takes
  tables in memory, through its own pipeline, hand them over there and write nothing.
- Name the methodology once, as the owner chose it before the first run: the formula of the first
  cut, the groups it allocates across -- sectors, say, each security in the one the factor model
  classifies it in -- and how daily effects are carried over the window.  A sum of daily effects
  and a compounded, linked one differ by many points over decades, and a change of either moves
  every attribution figure while no engine figure moves.
- Say what the factor directory has to look like, because it holds nothing but factor files: one
  CSV per factor, named by its file name, a date column first -- its header may be empty -- and
  one column per security after it.  Four names belong to the model's own series, matched exactly
  and in lower case: `f_market`, `f_total_factor_returns`, `f_total_excess_returns` and
  `f_idyo_returns`.  The Analytics Factory ships them as `Market`, `Total_Factor_Returns`,
  `Total_Excess_Returns` and `Idyo_Returns`, and a model series attributed as an ordinary factor
  is a quiet way to double-count the market.  So `Data/hand_supplied.py` maps each file name to
  its name, once, and nothing is renamed on disk.
- Name the index's two files and their date convention once, in `Data/hand_supplied.py`, so
  switching to a different index is an edit there and no notebook names one of them.
- Keep the library's numbers as tables.  It writes no file: the first cut, the factor model and
  the third pass are read from the objects it builds, and the notebook writes each table
  `FINDINGS_N.md` quotes to `Attribution/`.  Its figures go to the screen; say whether they are
  kept -- saved to `Attribution/` beside the tables -- or left unshown under a non-interactive
  backend, so a headless run never waits on a window.

Expect two methodologies and a third pass, all reported.  Brinson-Fachler splits active return
into allocation, selection and interaction -- the lever that moved.  The factor model splits
excess return into compensated factor tilts and idiosyncratic alpha -- what was paid for, on
purpose or by accident.  Then Brinson-Fachler again on the residual, which says whether the
Sharpe survives once the factor turns.  Expect the answer to be partial -- an absolute rule is
close to invisible to a factor model built on relative factors -- and treat that as a finding.
The follow-ups are counterfactual books the engine can already price.  `AGENTS.md` has the
reasoning.

It produces `Attribution/` -- the tables of the two decompositions and the third pass, and the
figures where they are kept -- for `FINDINGS_N.md`, and the answer to the gate's performance
criterion P2.

It prevents selling factor beta as if it were alpha, crediting a book with a day's return its
weights already held or with an unpriced member's return, and a run that stops at its first file
because a header carries the name a provider gave it rather than the one the loader expects.
"""
