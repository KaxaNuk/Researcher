"""
Portfolio construction -- step 4 of 8, the second shared module.  Turns the set of securities a
rule calls eligible into the weights a book holds, calling the KaxaNuk Portfolio Construction
library where it is installed.

In plain words: how much of what, and how often you change your mind.

Runs inside an experiment notebook, from the rule in section 2, on the matrices the securities
panel built.

What is expected here is one function signature and a few things behind it:

- The signature.  Given the securities eligible today, a returns history that has already been
  cut off before today and, for a scheme that sizes by a feature, that feature as it stood before
  today, return one weight per security, summing to at most 1.0.  Every weighting scheme -- equal
  weight, proportional to a score, or any sizing method the library registers whose configuration
  has no required field: inverse volatility, risk parity, hierarchical risk parity -- is the same
  shape, so swapping one for another is one line in the rule cell and nothing else in the notebook
  moves.  That is what makes two experiments comparable rather than merely adjacent.
- The library inside the signature, never around it.  Build one of its methods per rebalance date,
  on the history already cut: a method that estimates from returns uses whatever history it was
  built with, and the library's own pipeline builds each method once for every date.  Import it
  inside a guard -- it is KaxaNuk's own library, installed by hand -- and stop with an error that
  names a method needing it when it is absent.  Equal weight needs nothing.
- At most one, not exactly one.  A strategy that can go to cash cannot satisfy the stricter form;
  what the weights leave is cash, which the engine holds and pays interest on.
- The constraints every scheme respects, as arguments of `build_weights`: a maximum weight and a
  minimum holding count.  One the blueprint does not name is switched off, and a lever a later
  experiment has to earn by beating the book without it.  Bounds the blueprint names -- a cap and a
  floor on each weight -- are the design, not levers to earn: the blueprint says whether a capped
  name's excess goes to cash or to the other names, and the control holds the same bounds.
- The timing helpers that cannot be forgotten if they live here: lag the eligibility so the set
  used on rebalance date t is the one observed at t-1; rebalance on a calendar -- the first trading
  day of each month, decided on the close before it -- or only on the dates that set changes; and a
  no-trade band, so a held name whose target barely moved is left as it drifted.  A weight that has
  not moved is not a reason to pay commission, nor an order anyone wants to place by hand.  The
  band is decided at the close and written at the next open, and what the kept names hold over
  their targets comes out of the traded names, so the book never exceeds one.
- No day of hindsight for a delisting.  The engine sells a position whose prices stop at its last
  price.  A gap inside a series, which the engine cannot price, is a blocking row of
  `Universe/Data_Issues.csv`, and the name is excluded by name from every book rather than traded
  around, so no book ever trades off its own dates.
- Causality by construction.  A weigher never sees a date, only a history -- and a score, where
  the scheme sizes by one -- already cut off before the date it sizes, so it cannot reach into the
  future even by accident.  The module makes that cut once, for the book and its control alike.

It produces the `REBALANCE_DATES x securities` target weights the rule cell hands to the
diagnostics and the weight file, and, under a band, the weights actually struck.

It prevents a good signal in a portfolio nobody could hold -- and a weighting difference that reads
as a signal difference because each notebook invented its own sizing.
"""
