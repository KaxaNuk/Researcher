"""
Data Curator -- step 3 of 8, block 1 of 3.  The only file in this repository that downloads time
series from a data provider.  A strategy's seed builder, where it has one, reads the same
provider's catalogue of what each security *is* -- its name, its price dates -- and caches it in
`Universe/Provider_Cache/`; nothing else talks to a provider.

In plain words: you describe the data you want -- provider, identifiers, dates and columns -- and
the KaxaNuk Data Curator fetches it, aligns the calendar, handles splits and dividends, and writes
one file per identifier, the same way every run.

Runs first, after the seed exists, and before `Universe/universe_marimo.py`, which profiles what
this writes.  Nothing else has to exist before it except `Universe/Investable_Universe.csv` and a
provider key in `Config/.env`.

What is expected here is a short driver, not a framework:

- Read the identifiers from `Universe/Investable_Universe.csv`, column `main_identifier`, the
  identifier the experiment's provider prices each security under.  The seed is the authority on
  what exists, so it drives the download.
- Build one Data Curator configuration, or one per batch where the provider answers several
  identifiers in one request: the date window, those identifiers, and the output columns -- the
  provider's `m_*` columns plus the `c_*` columns defined in `Data/Curator/custom_calculations.py`.
  Fix the end date rather than using today, so two people running a week apart get comparable
  files.
- Take a later end date as an argument, `--end-date`, for the callers that need newer data, such
  as `Paper_Trading/daily_update.py`.  A refresh refetches each file whole, because a fresh pull
  rebases every adjusted column from the present, and remembers the date each file was fetched
  through, so a run that stops half way resumes where it stopped.
- Call the public library -- `kaxanuk-data-curator`, already installed by `uv sync` from
  `pyproject.toml`, imported as `kaxanuk.data_curator` -- with each data block the columns read
  mapped to the provider, so each name gets its own answer and its own file.
- Record the provider's answer for each name.  A name it does not carry is then told from one it
  refused today -- a rate limit, a timeout -- and only the second is asked again, after a pause.
- Point its output at `Data/Curator/Time_Series/`, one Parquet file per identifier, written and
  read through `Data/time_series.py`.  The library's default folder is `Output/`; here every stage
  has one home, and this is the Curator's.
- A provider's history can stop where its coverage does: a name that left the market years ago may
  be missing from it altogether.  Fetch such names from a second provider that carries them, into
  the same files and columns, and say in the strategy's documents which names came from where and
  how any column the second provider lacks was filled.  Or leave them out and publish what that
  costs, the survivorship cost, beside every result.  Either is a decision the journal records.

**The columns are the ones the pipeline reads, and no more.**  Widening the tuple changes every
file's header and refetches every identifier, so a column is added when a stage reads it, never on
speculation.  A new experiment's signal on the data already downloaded is an `r_*` column of the
refinery, never a wider download.

Three adjustment families arrive from the provider and each does a different job:

    unadjusted            the price actually quoted; the order ticket is written in it
    split-adjusted        traded value, which is liquidity in today's share terms, checked
                          across every split before it is ranked on: volume can arrive split twice
    dividend-and-split    the total-return series a signal, a return and the backtest P&L run on

**Where the provider rounds its adjusted prices, rebuild the adjustment from the exact close.**  A
provider that keeps a few decimals on every adjusted price makes an early series of a name split
many times move in steps of a percent.  The unadjusted close is exact, so the split ratio and the
total-return close are rebuilt from it and the provider's own dividends and splits, as `c_*`
calculations in `Data/Curator/custom_calculations.py`, with any split after the window counted on
every day.  A corporate action the dividend column does not carry, such as a spin-off, is added
after the download from the provider's own record of it.  Then every file is read back and the
rebuilt series compared with the provider's own wherever its decimals are fine enough, into a table
of checks beside the time series; a disagreement is named, never smoothed over.

**Volume can arrive adjusted twice at a split**: traded value steps by the split's own factor while
the shares the tape printed stay flat.  Correct it in the `c_*` traded value, and let the universe
notebook's register read the same signature, so a name the correction missed is named there.

More series ride along in the same folder although they are not in the seed: the benchmarks the
strategy is reported against, and the rate the engine pays on the book's cash, a daily series the
engine reads beside the prices.  The backtest engine reads everything from one directory, so a
series filed anywhere else is one it cannot read.  None enters the cross-section, because
`Data/refinery.py` takes membership from the seed.

An index's daily holdings and returns, and a factor model's returns, are not sold by any price
provider: they arrive from KaxaNuk's Analytics Factory, and `Data/hand_supplied.py` reads them --
in place, from the folder `KN_ANALYTICS_PATH` names, or from the drop zones `Benchmarks/` and
`Factors/` beside the time series.  Without them this script still downloads every price and says
the index was not staged; the notebooks stop where they first read it.

Credentials come from `Config/.env` and are never printed -- not into a log line, a notebook
output or a commit.  An exposed key is rotated, not edited out.

It produces `Data/Curator/Time_Series/<identifier>.parquet`, `m_*` plus `c_*`, read by the universe
notebook, `Data/refinery.py` and the engine; and in `Data/Curator/` the provider's last answer for
each name and the date each file was fetched through.

It prevents beautiful results that came from broken inputs -- and a dataset nobody else can
rebuild.
"""
