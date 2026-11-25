"""
The library's sizing methods, checked on this strategy's data -- step 4, run once per build of the
KaxaNuk Portfolio Construction library, beside the experiment notebook.

In plain words: before a book is sized by one of the library's methods, each is built on real
rebalance dates of the universe and its weights are held to the invariants every book here must
pass.

What is expected here, when a later experiment may size with the library:

- A few rebalance dates, and on each the names the rule would hold.
- Each method built once per date, on the history cut strictly before it, as the
  `portfolio-construction-runs` skill says, and its weights checked: they sum to at most one, none
  is negative, the cap holds.
- A method that fails, or behaves otherwise than its skill says, named with the call, the error's
  type and its message, to be reported as `AGENTS.md` says.

It produces a table beside this file, one row per method, setting and date; it is regenerated, so
ignored.  It checks weights, never returns.

It prevents a sizing method trusted on a universe it was never run on.
"""
