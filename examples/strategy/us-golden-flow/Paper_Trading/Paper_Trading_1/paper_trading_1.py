"""
The frozen book of Experiment 1 -- step 7 of 8.  `Paper_Trading_N` mirrors the `Experiment_N` it
was promoted from, so the lineage of a paper-traded book is never in question.

In plain words: the rule that went to paper, **copied out of the experiment notebook and then
left alone**.  The notebook is the record of how the rule was *chosen*, including everything tried
and rejected, and it stays free for the next piece of research.  This file is the record of what is
*being traded*, and a change to it is a change to a live book, not a change to an experiment.

What it holds, once its experiment graduates or a person puts it on paper on probation:

- the rule's settings, copied from the experiment notebook, and its costs;
- the rule itself, in the form the notebook ran it, with its control -- the same rule with one
  ingredient removed, which runs beside the book every day;
- `BANDS`: for each diagnostic, the range `FINDINGS_N.md` measured over the backtest, registered
  in this book's section of `../BITACORA.md` before its first day; a day outside one is a flag;
- `run(as_of)`, which `../daily_update.py` calls once a day.  It runs the frozen refinery in this
  folder over the raw files linked into `Data/Curator/Time_Series/`, applies the rule from the
  experiment's first day to `as_of`, writes the weight files, prices the book and its control with
  the frozen engine module -- over the whole history, over the days after the experiment's window
  and since the freeze date in `FREEZE.json` -- and returns what the record needs: the engine's
  results, the book in force, the day's diagnostics, the flags and a summary.

**Membership past the last date its source wrote is held at that date.**  An index's holdings,
read by `Data/hand_supplied.py`, are refreshed later than prices, and a membership built only from
the dates they hold -- in the rule, or as a refined column -- has no member past their last date:
right for a backtest, and a book that read it so would sell every name the day those files end.
The book holds the last membership they wrote, and `../daily_update.py` flags the files once they
fall behind the day; inside the experiment's window they cover every day, so the rule it ran is
unchanged.

Every module it imports is the copy `../promote.py` made in this folder, loaded by path under a
name of its own, never the shared one in `Experiments/`: that is what keeps it frozen.  It re-fits
nothing, and it computes no performance figure -- the engine does.

`../daily_update.py` calls into here; it never re-derives the rule itself.  A strategy with no
book on paper keeps this file as it is: the contract, with no logic.

See `../BITACORA.md` for the gate, and `../../RESULTS.md` for the numbers a candidate is judged on.
"""
