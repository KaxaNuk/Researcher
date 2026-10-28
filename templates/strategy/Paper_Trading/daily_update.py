"""
The daily run over every book on paper -- step 7 of the KaxaNuk Strategy Template.

In plain words: once a day, after the market closes, refresh the data, run each frozen strategy
exactly as it was frozen, price it with the engine, and write down what happened --
how the book is doing over its whole history and since the day it was frozen, and anything that
does not look like the backtest said it would.

A book on paper, graduated or on probation, is a frozen copy of the strategy, made once by
`promote.py`: the files it needs, copied byte for byte into `Paper_Trading_N/` in the strategy's
own layout, with `FREEZE.json` naming the commit, the date and the hash of each.  Every path in
those copies resolves inside the book's folder, so an experiment under construction can change
the shared modules and the book never moves.  **A paper-trading run re-fits nothing**: a run
that tunes anything is a backtest wearing a costume, and it answers a question nobody asked.

What one run does, in order:

1. Takes a lock, so two runs never overlap -- a lock a killed run left for twelve hours is
   removed, and the log says so -- and writes its log to `Paper_Trading/Logs/`.
2. Refreshes the shared raw data once -- `Data/curator.py` with the day as its end date -- or,
   with `PAPER_TRADING_INPUT=database`, reads the panel another machine published.
3. Checks the newest day before any book reads it: a close with no fill price, a move no price can
   make, a cash or benchmark file behind the day, an index file behind it.  A check that fails
   stops every book before anything is written: a book on broken data is worse than none.  It
   reads that day alone: a security's file that ends before it, and a bad bar on a day between
   two runs, pass unflagged.
4. For each book in `BOOKS`: compares every frozen file with its hash in `FREEZE.json` -- the
   security master, which is never committed, among them -- and the Curator's calculations with
   the ones frozen, links the raw files into the book's folder, with the index and factor files
   from the drop zones beside them, and calls `paper_trading_N.run(as_of)`, which runs the frozen
   refinery and rule and prices the book and its control over the whole history, over the days
   after the experiment's window and since the freeze.  A frozen file missing or changed stops the
   book, as a changed calculation does.  The frozen `Data/hand_supplied.py` reads the drop zones
   in the book's folder when `KN_ANALYTICS_PATH` is empty.
5. Writes the record through `record.py`: the book in force, the engine's daily values and
   statistics, the diagnostics, and a flag for each diagnostic outside the band the book's
   section of `BITACORA.md` registered before its first day, each failed check and each
   restatement.
6. Exits 0 when clean, 1 when a flag was raised, 2 when a step failed, so a scheduler can tell.
   A step that raises is a failed day, with its traceback in the day's log: Python's own exit code
   for it, 1, would read as a flagged day, and a book flagged every day would hide the crash.

Configured in `Config/.env`: `PAPER_TRADING_INPUT` (`provider` or `database`),
`PAPER_TRADING_SINKS` (`local`, `database` or both), `PAPER_TRADING_DATABASE` and
`PAPER_TRADING_PUBLISH_DATA`; each has a flag that overrides it for one run.
`Paper_Trading/BITACORA.md` says how to schedule it.

Every performance figure it writes comes from the engine.  See `BITACORA.md` for the gate a book
passes to get here.
"""
