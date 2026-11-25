"""
Attribution apart from the notebook -- step 6, beside the experiment notebook.  Attributes books the
notebook has already priced, from the engine's answers it cached, without pricing anything again.

In plain words: which part of each book's return was earned, and which part was the market's, when
the notebook's own attribution section did not run or would take too long to run again.

What is expected here, when a strategy needs it, and nothing when it does not:

- The books and the cost rows are the blueprint's and the owner's, named at the top, each with the
  decision that added it.
- The engine's answers are read from `Backtest/cache/`, under the hash of each weight file, and a
  cached run that is not the one the findings read raises.
- Each book is shaped exactly as the notebook's attribution section shapes it -- the daily book as
  the engine held it, widened to every benchmark member at zero weight, both weight tables held
  overnight -- before `attribution_analysis` attributes it.
- The first cut's benchmark is reconciled with the index's own returns, and a gap above the
  blueprint's tolerance raises.

It produces the same tables the notebook's attribution writes, in `Attribution/`, none committed,
and prints what `FINDINGS_N.md` quotes.

It prevents an attribution that shapes the book differently from the notebook's.
"""
