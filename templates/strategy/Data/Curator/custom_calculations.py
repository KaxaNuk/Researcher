"""
The `c_*` columns -- step 3 of 8, computed by the Data Curator while it downloads.

`c_*` means one security's own history and nothing else.  The Curator works one identifier at a
time, so anything that compares securities against each other belongs one stage later, in
`Data/Refinery/custom_calculations.py`, as an `r_*` column.

What is expected here is one function per column, named exactly as the column:

- Each function's parameters are named after the columns it reads -- a provider column, a dividend
  or split column, or another `c_*` column.  The Curator resolves the dependency order from the
  signatures, so the order of definition here does not matter.
- Each returns a column of the same length.  Prices arrive as fixed-point decimals; anything
  statistical casts to float once, at the boundary, and a value that is not finite is returned as
  a null.
- A column is registered by listing it among the output columns `Data/curator.py` requests.
  Nothing else registers it.
- Never give a column the name of one the library ships: which of two functions of one name a run
  uses is not documented, so a column of your own carries a name of its own.

The minimum a backtest needs -- and the first two are never removed:

- the cumulative split ratio and the dividend-and-split ratio, the factors between the day's quoted
  price and the split-adjusted and total-return series;
- the total-return close every signal, return and mark reads, and its one-day return, because
  nearly every feature is built on it;
- the price a book is filled at, unadjusted for the order ticket and on the total-return basis for
  the fill;
- the day's traded value, because capacity is a question every strategy has to answer, checked
  and corrected across every split: volume can arrive adjusted twice.

**Where the provider rounds its adjusted prices**, the ratios and the total-return close are
rebuilt here from the exact unadjusted close and the provider's own dividends and splits, read
through the joined column names the Curator writes for them.  A split after the requested window
is already in the provider's split-adjusted prices and dividends but not in the window's split
columns: take the constant between the two bases from the provider's own split-adjusted close, so
the rebuilt price, the provider's volume and its dividends stay on one basis.

Widening the schema changes every file's header, so the next run refetches every identifier.  That
is intended, because it is what stops the folder holding a mix of schemas, and it makes this the
wrong home for anything you intend to tune.  Put a model's frozen arithmetic inputs here and the
model itself in the Refinery: a sweep must never cost a download, and a new experiment's signal on
the data already downloaded is an `r_*` column, never a new `c_*` one.

It produces the `c_*` columns in every file under `Data/Curator/Time_Series/`.

It prevents a feature computed on a price basis it should not use -- a plausible number and no
error.
"""
