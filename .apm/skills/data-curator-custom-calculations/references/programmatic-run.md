# Running the curator programmatically

`Config/data_curator_parameters.xlsx` and `Config/custom_calculations.py` are one way to feed
`kaxanuk.data_curator.main()`, not a requirement: the README says the Curator is configurable "from
an Excel file, or directly in a Python script", and the documentation's Component Integrator
Workflow page builds the `Configuration` in Python. That page's examples use arguments 0.50.0
deprecated, so the call below is the one the worked example ran — `Data/curator.py`, 892
identifiers on 2026-10-06, as `JOURNAL_1.md` records. Once a strategy is finalized it usually
migrates to files and the Excel surface, so the calculations themselves must be written to survive
that move unchanged — which they do, since nothing in the naming, `DataColumn` or composition rules
depends on the surface.

## The whole call

```python
import datetime

import kaxanuk.data_curator
import kaxanuk.data_curator.data_blocks.market_daily
import kaxanuk.data_curator.data_providers
import kaxanuk.data_curator.entities
import kaxanuk.data_curator.output_handlers

market_data_block = kaxanuk.data_curator.data_blocks.market_daily.MarketDailyDataBlock
data_provider = kaxanuk.data_curator.data_providers.FinancialModelingPrep(api_key=api_key)
output_handler = kaxanuk.data_curator.output_handlers.CsvOutput(output_base_dir='Output')

configuration = kaxanuk.data_curator.entities.Configuration(
    start_date=datetime.date.fromisoformat("2020-01-01"),
    end_date=datetime.date.fromisoformat("2024-12-31"),
    period='quarterly',
    identifiers=('AAPL', 'MSFT'),
    columns=(
        'm_date',
        'm_close_dividend_and_split_adjusted',
        'c_simple_moving_average_63d_close_dividend_and_split_adjusted',
        'c_example_golden_cross_signal',
    ),
)

kaxanuk.data_curator.main(
    configuration=configuration,
    data_block_providers={
        market_data_block: data_provider,
    },
    master_clock_data_block=market_data_block,
    output_handlers=[output_handler],
    custom_calculation_modules=custom_calculation_modules,
)
```

Notes that matter:

- `main()` is called by keyword, as the worked example does. Callers only instantiate the
  providers, as the worked example does too: the changelog (0.17, renamed in 0.39) gives each
  provider an `initialize()` for what runs before the identifiers are looped, and the example never
  calls it.
- `data_block_providers` maps each data block to the provider that fetches it (the changelog,
  0.50.0). The worked example maps the market daily block, `MarketDailyDataBlock`, which is all its
  columns read, and passes it as `master_clock_data_block`, the block the others are aligned to. A
  run that reads fundamentals (`f_*`, `fbs_*`, `fcf_*`, `fis_*`), dividends (`d_*`) or splits
  (`s_*`) maps those blocks too; FMP's documentation page lists tags for all four. Their data-block
  classes are on no documentation page and in no recorded run: name them here only once a run has.
- `data_block_providers` needs kaxanuk-data-curator 0.50.0 or later, and 0.51.0 requires it. The
  `market_data_provider` and `fundamental_data_provider` arguments of earlier versions are
  deprecated (the changelog, 0.50.0): never pass them.
- **0.51.0 requires `data_block_providers`** (its changelog). A strategy's run on Sharadar,
  2026-10-23, passed `kaxanuk.data_curator.data_providers.Sharadar(api_key=api_key)` in place of
  `FinancialModelingPrep(...)`, mapped to `MarketDailyDataBlock` alone, with the key from
  `KNDC_API_KEY_SHARADAR`, as the documentation's Sharadar page names it. The same run mapped
  `DividendsDataBlock` and `SplitsDataBlock` to Sharadar too, and every `d_*` and `s_*` column
  still stopped it (`SKILL.md`'s 0.51.0 notes): map them only once that is fixed.
- Build the `Configuration` as the worked example does: `datetime.date` dates, a `period` of
  `annual` or `quarterly`, and `identifiers` and `columns` as tuples. Every identifier is processed
  with the same column selection.

## Selecting the columns

`columns` **is** the selection surface, the same as the `Output_Columns` sheet: the Component
Integrator page says the `Configuration` mirrors the settings of the workbook. The worked example's
run wrote exactly those columns, in that order, and nothing else: its second pass found every
file's header equal to its `OUTPUT_COLUMNS` and fetched nothing new (`JOURNAL_1.md`, 2026-10-06).
Intermediate `c_*` columns are resolved as dependencies and need not be listed: the Custom
Calculations page says a function may be used "directly or as intermediate steps within other
calculations".

Always select `m_date`: the worked example's runs did, and the documentation does not say it is
added for you.

## Output handlers

Pass them as a list; the changelog (0.17) says `main()` runs all of them.

| Handler | Constructor | Result |
|---|---|---|
| `CsvOutput` | `CsvOutput(output_base_dir='Output')` | one `<identifier>.csv` per identifier, as the worked example's run wrote |
| `InMemoryOutput` | not documented | keeps the data in memory (the changelog, 0.41.0), and the README promises in-memory pandas DataFrames; how they come back is not documented, so check it by a run before a notebook relies on it |
| Parquet | not documented | the README lists Parquet output; the Component Integrator page's handler predates 0.50.0, and no run has used one |

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
