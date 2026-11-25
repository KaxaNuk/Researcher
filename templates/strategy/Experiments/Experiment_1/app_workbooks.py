"""
The KaxaNuk app's backtests -- step 5, beside the experiment notebook.  Prices the experiment's
headline books once more, one single run each, so the KaxaNuk Backtest Engine writes the results
workbook the app imports.

In plain words: the notebook prices its books in the engine's batch mode, which returns tables and
writes no workbook; the app reads a backtest only from a single run's workbook.

What is expected here is a short script, run after the notebook from the repository root:

- The books it prices are the weight files the notebook writes where the app lists them, in
  `Portfolio/`, and nothing else: it adds no book and no number.  The workbooks hold the figures the
  notebook's summary holds, at the cost row the gate is read at.
- The engine's settings are the notebook's -- the window, the capital, the commission, the slippage
  and the cash reserve -- named once, so a workbook never disagrees with `FINDINGS_N.md`.
- Each workbook is renamed after its book and cost row, so two pricings read apart in the app.

It produces the engine's workbooks in `Backtest/`, which the app imports with *Import results*.
None is committed.

It prevents a backtest in the app that is not the one the findings report.
"""
