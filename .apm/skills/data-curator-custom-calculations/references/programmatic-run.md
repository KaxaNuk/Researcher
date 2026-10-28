# Running the curator programmatically

`Config/data_curator_parameters.xlsx` and `Config/custom_calculations.py` are one way to feed
`kaxanuk.data_curator.main()`, not a requirement: the README says the Curator is configurable "from
an Excel file, or directly in a Python script", and the documentation's Component Integrator
Workflow page builds the `Configuration` in Python. That page's examples use arguments 0.50.0
deprecated, so the call below is the one the worked example runs — `Data/curator.py` on 0.51.0,
its 2,199 listings and `SPY` in batches of 25, from emptied data folders on 2026-10-24, as its
`FINDINGS_1.md` records. Once a strategy is finalized it usually
migrates to files and the Excel surface, so the calculations themselves must be written to survive
that move unchanged — which they do, since nothing in the naming, `DataColumn` or composition rules
depends on the surface.

## The whole call

```python
import datetime
import logging

import kaxanuk.data_curator
import kaxanuk.data_curator.data_blocks.dividends
import kaxanuk.data_curator.data_blocks.market_daily
import kaxanuk.data_curator.data_blocks.splits
import kaxanuk.data_curator.data_providers
import kaxanuk.data_curator.entities
import kaxanuk.data_curator.output_handlers

market_data_block = kaxanuk.data_curator.data_blocks.market_daily.MarketDailyDataBlock
dividends_data_block = kaxanuk.data_curator.data_blocks.dividends.DividendsDataBlock
splits_data_block = kaxanuk.data_curator.data_blocks.splits.SplitsDataBlock
data_provider = kaxanuk.data_curator.data_providers.Sharadar(api_key=api_key)
output_handler = kaxanuk.data_curator.output_handlers.ParquetOutput(output_base_dir='Output')

configuration = kaxanuk.data_curator.entities.Configuration(
    start_date=datetime.date.fromisoformat("2020-01-01"),
    end_date=datetime.date.fromisoformat("2024-12-31"),
    period='quarterly',
    identifiers=('AAPL', 'MSFT'),
    columns=(
        'm_date',
        'm_close',
        'm_close_split_adjusted',
        'd_ex_dividend_date_dividend_split_adjusted',
        's_split_date_numerator',
        's_split_date_denominator',
        'c_example_golden_cross_signal',
    ),
)

kaxanuk.data_curator.main(
    configuration=configuration,
    data_block_providers={
        market_data_block: data_provider,
        dividends_data_block: data_provider,
        splits_data_block: data_provider,
    },
    master_clock_data_block=market_data_block,
    output_handlers=[output_handler],
    custom_calculation_modules=custom_calculation_modules,
    logger_level=logging.WARNING,
)
```

Notes that matter:

- `main()` is called by keyword, as the worked example does. Callers only instantiate the
  providers, as the worked example does too: the changelog (0.17, renamed in 0.39) gives each
  provider an `initialize()` for what runs before the identifiers are looped, and the example never
  calls it.
- `data_block_providers` maps each data block to the provider that fetches it (the changelog,
  0.50.0). The worked example maps the market daily block, `MarketDailyDataBlock`, and the
  dividends and splits blocks, `DividendsDataBlock` and `SplitsDataBlock`, all three to Sharadar,
  and passes the first as `master_clock_data_block`, the block the others are aligned to. A run
  that reads fundamentals (`f_*`, `fbs_*`, `fcf_*`, `fis_*`) maps that block too; its class is on
  no documentation page and in no recorded run: name it here only once a run has.
- `data_block_providers` needs kaxanuk-data-curator 0.50.0 or later, and 0.51.0 requires it. The
  `market_data_provider` and `fundamental_data_provider` arguments of earlier versions are
  deprecated (the changelog, 0.50.0): never pass them.
- **0.51.0 requires `data_block_providers`** (its changelog). The worked example passes
  `kaxanuk.data_curator.data_providers.Sharadar(api_key=api_key)`, with the key from
  `KNDC_API_KEY_SHARADAR`, as the documentation's Sharadar page names it; on FMP, on 0.50.0, it
  passed `FinancialModelingPrep(api_key=api_key)` the same way. With the dividends and splits
  blocks mapped, their columns are read under the joined names of `SKILL.md`'s 0.51.0 notes.
- **What `main()` returns is not what happened.** A refused batch is logged and `main()` returns
  normally (`SKILL.md`'s 0.51.0 notes), so the example adds a handler to the `kaxanuk` logger for
  the call, at error level, reads what it collected, and passes `logger_level=logging.WARNING` so
  the run's own lines stay readable. It also compares each file's modification time before and
  after the call to see which identifiers were written.
- Build the `Configuration` as the worked example does: `datetime.date` dates, a `period` of
  `annual` or `quarterly`, and `identifiers` and `columns` as tuples. Every identifier is processed
  with the same column selection.

## Selecting the columns

`columns` **is** the selection surface, the same as the `Output_Columns` sheet: the Component
Integrator page says the `Configuration` mirrors the settings of the workbook. The worked example's
runs wrote exactly those columns, in that order, and nothing else: its driver leaves a file alone
when its header equals `OUTPUT_COLUMNS` and it was fetched through the same end date, and a second
pass over a complete folder fetches nothing new.
Intermediate `c_*` columns are resolved as dependencies and need not be listed: the Custom
Calculations page says a function may be used "directly or as intermediate steps within other
calculations".

Always select `m_date`: the worked example's runs did, and the documentation does not say it is
added for you.

## Output handlers

Pass them as a list; the changelog (0.17) says `main()` runs all of them.

| Handler | Constructor | Result |
|---|---|---|
| `ParquetOutput` | `ParquetOutput(output_base_dir='Output')` | one `<identifier>.parquet` per identifier, as the worked example's runs on 0.51.0 wrote: prices as decimals of each file's own precision, volume as integers, so rewrite them into one schema before stacking two |
| `CsvOutput` | `CsvOutput(output_base_dir='Output')` | one `<identifier>.csv` per identifier, as the worked example's FMP runs on 0.50.0 wrote |
| `InMemoryOutput` | not documented | keeps the data in memory (the changelog, 0.41.0), and the README promises in-memory pandas DataFrames; how they come back is not documented, so check it by a run before a notebook relies on it |

## In-memory calculation modules — not checked by a run

A notebook could keep its `c_*` functions in a cell and pass `main()` a module object built at run
time instead of a file. **No run has checked this, and the documentation does not describe it.**
What a run has shown is the worked example's module, loaded from its file by path under a name of
the driver's own (`load_custom_calculations` in `Data/curator.py`). Before an experiment relies on
an in-memory module, run it once in a scratch copy with the module below, and record what came
out:

```python
import collections.abc
import types


def module_from_functions(
    module_name: str,
    functions: "collections.abc.Iterable[collections.abc.Callable]",
) -> "types.ModuleType":
    """
    Build an in-memory calculation module from already-defined functions.

    The module's name serves only its repr and debugging; each function, named `c_*`, is exposed
    under its own name.
    """
    module = types.ModuleType(module_name)
    for function in functions:
        setattr(
            module,
            function.__name__,
            function,
        )

    return module


custom_calculation_modules = [
    module_from_functions(
        'experiment_calculations',
        [
            c_example_golden_cross_signal,
        ]
    ),
]
```

Only the functions you list are in the module, so the exposed set stays explicit. Re-running the
cell rebuilds the module from the current function objects, so an edit needs no restart, while a
module Python has imported from a file stays cached until the process restarts.
