"""
Backtest engine -- step 5 of 8, the third shared module.  The one path from a book of weights to a
performance number, through the KaxaNuk Backtest Engine.

In plain words: the simulation, run by the engine, with costs and without peeking ahead.

Runs inside an experiment notebook, section 4, after the book has been written to `Portfolio/`.

What is expected here:

- Write the weight file the engine reads: `Portfolio/portfolio_weights.csv`, wide, keyed by the
  identifier the market-data files are named by, dates across the columns, every column summing to
  at most 1.0.  There is no cash fund: what the rule leaves uninvested stays as cash in the engine,
  which pays it interest, so going to cash earns what a broker pays on a balance, as it does in
  life.  A security that changed identifier mid-history occupies two rows, each non-zero only while
  that listing was live.
- Price every cost and the cash inside the engine, never beside it.  Commission in basis points of
  the notional traded.  Slippage from the engine's spread-and-impact model, on the day's high, low
  and volume, and every book priced again beside it at a flat half-spread in basis points: a spread
  estimated from the day's range reads a large, volatile name's range as spread, and the flat row
  says how much of a verdict rides on that estimate.  The cash's interest from a rate file staged
  in the market-data folder, the last observation on or before each day, less the spread a broker
  keeps.  A position whose prices stop, sold by the engine at its last price, so no day of
  hindsight is needed.  Name each setting once, as an argument, never as a default nobody chose,
  and let the findings say what the engine does not model.
- Run the licensed engine and read its results back: the daily series it marks, the book's daily
  weights as it held them -- the input step 6 needs -- and its summary statistics.  Import it
  inside a guard -- it installs from a licensed index, not PyPI -- and report and skip when it is
  absent, so a clone without a licence still produces everything except the numbers.
- Price an experiment's books together, in the engine's batch mode, which loads the market data
  once for a batch of books that share every setting but their weights, and cache each book's
  answer under the hash of its weight file and its settings, so a re-run prices only what changed.
- Say whether each run valued the window it was asked for.  A run the engine stopped valuing early
  can still return a summary over the stub; the notebook counts the days each run valued against
  the trading days of its window, and excludes a short one by name, with its reason.
- Name the benchmarks a strategy is reported against, in one place, and clip the window to the
  shortest of them, and to the cash rate's first observation, up front rather than discovering it
  as an error.
- Align every variant of an experiment onto one common window before ranking them.  A variant that
  starts a year later is not comparable on its own dates.

There is deliberately no second, lighter simulator here or anywhere.  One that disagrees with the
engine lets the reader pick the number they prefer, and every figure quoted in `RESULTS.md` comes
through this module.

It produces `Backtest/` -- the engine's workbook and the series drawn from it, the daily weights
among them -- for `FINDINGS_N.md` to record and `attribution_analysis.py` to read.

It prevents paper returns that real trading would have erased, a cost or a cash yield computed
beside the engine where nobody checks it, and a difference in cost model or window showing up as
strategy skill.
"""
