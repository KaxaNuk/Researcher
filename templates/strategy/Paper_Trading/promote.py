"""
The promotion of an experiment to paper -- step 7 of 8.  Run once, when an experiment graduates --
every soundness and every performance criterion of the gate in `BITACORA.md` holds, and a person
has signed it there -- or when a person has signed it there as sound and regime-dependent, on
probation, its terms registered.  Never again for the same book.

In plain words: freeze the strategy.  Every file the book needs to go from raw prices to a priced
book is copied byte for byte, from the commit that graduated, into `Paper_Trading/Paper_Trading_N/`
in the strategy's own layout -- `Data/`, `Experiments/`, `Universe/` -- and `FREEZE.json` records
the commit, the date and the hash of each file.  Because every module here resolves its paths from
its own folder, the copies read and write inside the book's folder alone: an experiment under
construction can change the shared modules tomorrow, and the graduated book never moves.

What it copies is listed in `FROZEN_FILES`, and it refuses to run on a working tree with changes
to tracked files: a freeze of code nobody committed is a freeze nobody can reproduce.  The rule
itself is not copied here -- it lives in a cell of the experiment's marimo notebook -- so
`paper_trading_N.py` carries it, written from the experiment's cells and committed before the
promotion.

Two things cannot be copied, because every book shares them: the raw price files, and the
calculations the Curator runs while it writes them.  `FREEZE.json` records the hash of those
calculations and the Curator's version, and `daily_update.py` refuses to run a book whose shared
inputs no longer match.

One frozen file is not in the commit: the security master, which the universe notebook writes from
the provider's data.  It is copied from disk and hashed like the rest, and `.gitignore` keeps the
book's copy out of git, as it keeps the one in `Universe/`: it stays on the machine that froze the
book, backed up with the record.

It produces `Paper_Trading_N/` with its frozen files and `FREEZE.json`, committed by a person, all
but the security master.

It prevents a graduated book changing because somebody improved the code it was frozen on.
"""
