"""
Data Refinery -- step 3 of 8, block 2 of 3.  The cross-sectional layer over the curated data.

In plain words: the Curator sees one security at a time; this stage sees all of them on one date.
It stacks every Curator file into one panel, computes the `r_*` columns across it, and writes the
files back out with more columns, each security's rows kept inside the span the seed gives it.

Runs after `Universe/universe_marimo.py`, because it joins the security master that notebook
writes, and before `Data/analyzer_marimo.py`, which reads what this writes.  Run too early it should
say which columns it is skipping and carry on -- the right behaviour and the wrong outcome.

    Data/Curator/Time_Series/<id>.parquet  m_* + c_*                       per security
            |
            v   stack, compute per date across the cross-section, join the master
    Data/Refinery/Time_Series/<id>.parquet m_* + c_* + r_* + current_*     rows in span, more cols

What is expected here is loading, ordering and writing, every file read and written through
`Data/time_series.py`.  The calculations live in `Data/Refinery/custom_calculations.py`.

- Membership is an allowlist taken from `Universe/Investable_Universe.csv`, so the cash rate and
  the benchmarks in the Curator folder never enter a rank.  There is no second list to forget.
- Keep each security's rows inside the span the seed gives it, `valid_from` to `valid_to`: outside
  it, a file under a reused identifier is another company's history, and no stage may read it.  A
  seed without spans keeps every row.
- Load only the columns the calculations read: a panel of hundreds of securities over decades then
  stays inside a few hundred megabytes.
- For a seed taken from an index, attach the index's weight on each date, read through
  `Data/hand_supplied.py` and keyed by the price files, so every cross-sectional column is taken
  over the day's members and a name outside the index never moves another name's rank.
- Resolve each `r_*` function by its parameter names against the columns already built -- the same
  convention the Curator uses -- and compute them in dependency order.
- Join the classification columns of `Universe/Security_Master.csv`, prefixed `current_`, because
  they are what a security is classified as today, not on the date of the row.  Skip them, and say
  so, when the master does not exist yet.
- Report per-column coverage on every run, so an all-null column cannot slip past.
- Delete refined files for securities no longer in the seed.  A stale file carries ranks taken
  against a universe that no longer exists, and anything reading the folder would average two
  incompatible cross-sections without raising an error.

This is the seam the KaxaNuk Data Refinery library replaces.  Keep the contract -- Curator files
in, `r_*` functions resolved by name, Refinery files out with each security's rows inside its
span -- and the swap is a one-file change.

It produces `Data/Refinery/Time_Series/`, the panel every experiment reads.

It prevents a rank or a breadth reading that was quietly taken over the wrong set of securities.
"""
