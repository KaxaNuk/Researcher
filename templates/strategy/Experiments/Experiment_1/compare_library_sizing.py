"""
The sizing, checked against the library -- step 4, beside the experiment notebook.  Sizes the rule's
book two ways on every rebalance date, by the strategy's own weigher in
`Experiments/portfolio_construction.py` and by the KaxaNuk Portfolio Construction library, and says
where they differ.

In plain words: the experiment sizes its book with its own function; the library, given the same
names, scores and bounds, should give the same weights.

What is expected here, when the rule sizes with a function of its own:

- Eligibility read exactly as the notebook reads it, for the rule and its control.
- The library's methods composed to the rule's sizing -- proportional to the score, then the caps
  the blueprint names -- and the two books compared name by name.
- It checks weights, never returns: no performance figure is computed here.

It produces a table beside this file, each date and book with the names each way and the largest
weight difference; it is regenerated, so ignored.

It prevents a hand-written weigher drifting from the library it stands in for.
"""
