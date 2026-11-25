"""
The library's sizing methods, checked on this strategy's data -- step 4, run once per build of the
KaxaNuk Portfolio Construction library, beside the experiment notebook.

In plain words: before a book is sized by one of the library's methods, each is built on real
rebalance dates of the universe and its weights are held to the invariants every book here must
pass.

What is expected here, when a later experiment may size with the library:

- A few rebalance dates, and on each the names the rule would hold.
- Each method built once per date, on the history cut strictly before it, as the
  `portfolio-construction-runs` skill says, and its weights checked: they sum to at most one, none
  is negative, the cap holds.
- A method that fails, or behaves otherwise than its skill says, named with the call, the error's
  type and its message, to be reported as `AGENTS.md` says.

It produces a table beside this file, one row per method, setting and date; it is regenerated, so
ignored.  It checks weights, never returns.

It prevents a sizing method trusted on a universe it was never run on.
"""

# --- example: begin ---

# In US-Golden-Flow, this script's own description:
#
# Validate every sizing method of the KaxaNuk Portfolio Construction library on the strategy's data
# -- a check of step 4, run once per library build, beside Experiment 1.
#
# In plain words: before a book is sized by one of the library's fourteen methods, each is built on
# real rebalance dates of the KN US Equity Core and its weights are held to the invariants every
# book in this repository must pass. A method that fails, or behaves otherwise than its skill says,
# is named with the call, the error's type and its message.
#
# Runs after `Data/refinery.py`. `--refinery` reads another strategy's refined files instead -- a
# folder of the same layout, read only -- so the check can run while this strategy's data is still
# being built, such as Golden-Flow's `Data/Refinery/Time_Series`:
#
#     uv run python Experiments/Experiment_1/validate_sizing_methods.py
#     uv run python Experiments/Experiment_1/validate_sizing_methods.py --refinery <folder>
#
# What it does, on each date in `CHECK_DATES` (moved to the first trading day on or after it):
#
# - The names are those the rule would hold: Core members whose 50-day average sits above their
#   200-day average at the close before the date, sized by `bounded_by_score` on the 63-day traded
#   value inside a 20% cap and a 1% floor.  Only names with a complete year of returns before the
#     date
#   are kept, so every returns-based method sees the same table.
# - Each method is built once per date, on the history cut strictly before it, as the skill's
#   section 4 says, and allocates the snapshot.  Long-only wherever a flag allows shorts.
# - The panel has no market capitalisation, so `black_litterman` and `kn_index` read the Core's own
#   weight on the day, which is proportional to it; only relative capitalisations enter either.
#   `kn_index`'s 252-day traded value is the average of `c_traded_value` over the year before.
#   `mean_variance` under `MAX_SHARPE` reads the trailing year's mean return as its expected return,
#   to exercise the method, never as a forecast.
#
# Every row of `sizing_methods_check.csv`, beside this file: the method, its setting, the date, ok
# or the failure, the names in and held, the sum, the largest and smallest weight, the effective
# number of names, whether any weight is negative, whether `Weights.cap(0.20)` holds, and the
# seconds taken.
#
# It checks weights, never returns: no performance figure is computed here.

import argparse
import dataclasses
import importlib.util
import pathlib
import sys
import time

import dotenv
import pandas
import pyarrow
import pyarrow.parquet

__all__ = [
    'CHECK_DATES',
    'MethodCase',
    'main',
]


@dataclasses.dataclass(frozen=True)
class MethodCase:
    """
    One method to check: its registry name, a label for its setting, and its configuration.
    """

    configuration: object
    label: str
    name: str


CAP = 0.20
CHECK_DATES = (
    '2008-10-01',
    '2015-01-02',
    '2020-04-01',
    '2026-08-03',
)
CLOSE_COLUMN = 'c_close_dividend_and_split_adjusted'
EXPERIMENT_DIRECTORY = pathlib.Path(__file__).parent
FLOOR = 0.01
HISTORY_DAYS = 252
INDEX_WEIGHT_COLUMN = 'r_index_weight'
OUTPUT_PATH = EXPERIMENT_DIRECTORY / 'sizing_methods_check.csv'
REPOSITORY_ROOT = EXPERIMENT_DIRECTORY.parent.parent
SCORE_COLUMN = 'r_traded_value_sma_63d'
SEED_PATH = REPOSITORY_ROOT / 'Universe' / 'Investable_Universe.csv'
TOLERANCE = 1e-9
TRADED_VALUE_COLUMN = 'c_traded_value'
TREND_COLUMN = 'r_trend_50_200'
PANEL_COLUMNS = (
    CLOSE_COLUMN,
    INDEX_WEIGHT_COLUMN,
    SCORE_COLUMN,
    TRADED_VALUE_COLUMN,
    TREND_COLUMN,
)


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Check every method on every date, write the table, and print a summary; 0 when all passed.
    """
    parser = argparse.ArgumentParser(description='Validate every Portfolio Construction method.')
    parser.add_argument(
        '--refinery',
        default=str(REPOSITORY_ROOT / 'Data' / 'Refinery' / 'Time_Series'),
        help='the folder of refined files to read; this strategy\'s own when omitted',
    )
    parsed = parser.parse_args(arguments)
    dotenv.load_dotenv(
        REPOSITORY_ROOT / 'Config' / '.env',
        override=False,
    )
    panel = _load_panel(pathlib.Path(parsed.refinery))
    closes = panel[CLOSE_COLUMN]
    print(f'panel: {closes.shape[1]} securities, {closes.shape[0]} days')
    rows = []

    for check_date in CHECK_DATES:
        date_rows = _check_date(
            panel,
            pandas.Timestamp(check_date),
        )
        rows.extend(date_rows)

    table = pandas.DataFrame(rows)
    table.to_csv(
        OUTPUT_PATH,
        index=False,
    )
    print(f'wrote {OUTPUT_PATH}')
    summary = table.groupby(['method', 'setting'])['status'].apply(_status_line)
    print(summary.to_string())
    failed = table[table['status'] != 'ok']

    return 0 if failed.empty else 1


def _cap_outcome(
    built: object,
) -> str:
    """
    Whether `Weights.cap(maximum=CAP)` holds on the book: `holds`, or the refusal's type.
    """
    try:
        capped = built.cap(maximum=CAP)
        capped_weights = capped.as_mapping()
        largest = max(capped_weights.values())
    except Exception as exception:
        refused = f'refused: {type(exception).__name__}'

        return refused

    return 'holds' if largest <= CAP + TOLERANCE else f'breached: {largest:.4f}'


def _cases(
    portfolio_construction: object,
    names: list[str],
) -> list[MethodCase]:
    """
    Every registry method, each in the setting this check builds it with.

    The three methods whose shorts the mandate governs are built three ways: with no mandate, as a
    user who names none gets them; long only; and long only with the 20% cap inside the solve.
    """
    sizing = portfolio_construction.sizing
    long_only = _mandate(
        portfolio_construction,
        names,
        1.0,
    )
    capped = _mandate(
        portfolio_construction,
        names,
        CAP,
    )
    objective = portfolio_construction.enums.optimization_objective.OptimizationObjective
    weighting = portfolio_construction.enums.weighting_method.WeightingMethod
    kn_index_module = sizing.kn_index_allocator

    return [
        MethodCase(
            configuration=sizing.BlackLittermanConfig(
                market_cap_column='market_cap',
                long_only=True,
            ),
            label='no views, long only, cap from the Core weight',
            name='black_litterman',
        ),
        MethodCase(
            configuration=sizing.CDaRConfig(),
            label='alpha 0.95, no mandate',
            name='cdar',
        ),
        MethodCase(
            configuration=sizing.CDaRConfig(mandate=long_only),
            label='alpha 0.95, long only',
            name='cdar',
        ),
        MethodCase(
            configuration=sizing.CDaRConfig(mandate=capped),
            label='alpha 0.95, long only, cap 20% in the solve',
            name='cdar',
        ),
        MethodCase(
            configuration=sizing.ConstrainedMeanVarianceConfig(objective=objective.MIN_VARIANCE),
            label='minimum variance, no mandate',
            name='constrained_mean_variance',
        ),
        MethodCase(
            configuration=sizing.ConstrainedMeanVarianceConfig(
                objective=objective.MIN_VARIANCE,
                mandate=long_only,
            ),
            label='minimum variance, long only',
            name='constrained_mean_variance',
        ),
        MethodCase(
            configuration=sizing.ConstrainedMeanVarianceConfig(
                objective=objective.MIN_VARIANCE,
                mandate=capped,
            ),
            label='minimum variance, long only, cap 20% in the solve',
            name='constrained_mean_variance',
        ),
        MethodCase(
            configuration=sizing.CVaRConfig(),
            label='alpha 0.95, no mandate',
            name='cvar',
        ),
        MethodCase(
            configuration=sizing.CVaRConfig(mandate=long_only),
            label='alpha 0.95, long only',
            name='cvar',
        ),
        MethodCase(
            configuration=sizing.CVaRConfig(mandate=capped),
            label='alpha 0.95, long only, cap 20% in the solve',
            name='cvar',
        ),
        MethodCase(
            configuration=None,
            label='default',
            name='equal_weight',
        ),
        MethodCase(
            configuration=sizing.FeatureWeightingAllocatorConfig(
                feature_column='score',
                method=weighting.PROPORTIONAL,
            ),
            label='proportional to the 63-day traded value',
            name='feature_weighting',
        ),
        MethodCase(
            configuration=None,
            label='default',
            name='herc',
        ),
        MethodCase(
            configuration=None,
            label='default',
            name='hrp',
        ),
        MethodCase(
            configuration=None,
            label='default',
            name='inverse_volatility',
        ),
        MethodCase(
            configuration=kn_index_module.KNIndexAllocatorConfig(
                zeta=0.5,
                min_weight=0.001,
                col_market_cap='market_cap',
                col_adtv_63d='adtv_63d',
                col_adtv_252d='adtv_252d',
            ),
            label='zeta 0.5, minimum 0.1% (0 refused), cap from the Core weight',
            name='kn_index',
        ),
        MethodCase(
            configuration=sizing.MaxDiversificationConfig(long_only=True),
            label='long only',
            name='max_diversification',
        ),
        MethodCase(
            configuration=sizing.MeanVarianceConfig(
                objective=objective.MIN_VARIANCE,
                long_only=True,
            ),
            label='minimum variance, long only',
            name='mean_variance',
        ),
        MethodCase(
            configuration=sizing.MeanVarianceConfig(
                objective=objective.MAX_SHARPE,
                expected_return_column='expected_return',
                long_only=True,
            ),
            label='maximum Sharpe on the trailing mean, long only',
            name='mean_variance',
        ),
        MethodCase(
            configuration=sizing.NCOConfig(long_only=True),
            label='long only',
            name='nco',
        ),
        MethodCase(
            configuration=None,
            label='default',
            name='risk_parity',
        ),
    ]


def _check_date(
    panel: dict[str, pandas.DataFrame],
    requested: pandas.Timestamp,
) -> list[dict[str, object]]:
    """
    Every method's row on the first trading day on or after the requested date.
    """
    import kaxanuk.portfolio_construction
    import kaxanuk.portfolio_construction.enums.optimization_objective
    import kaxanuk.portfolio_construction.enums.weighting_method
    import kaxanuk.portfolio_construction.sizing.kn_index_allocator

    calendar = panel[CLOSE_COLUMN].index
    date = calendar[calendar >= requested][0]
    position = calendar.get_loc(date)
    before = calendar[position - 1]
    names = _rule_names(
        panel,
        before,
    )
    returns = panel[CLOSE_COLUMN].pct_change(fill_method=None)
    history = returns.iloc[position - HISTORY_DAYS:position][names]
    has_full_year = history.notna().all()
    complete = list(history.columns[has_full_year])
    snapshot = _snapshot(
        panel,
        before,
        history[complete],
        complete,
    )
    history_table = pyarrow.Table.from_pandas(
        history[complete].rename_axis('date').reset_index(),
        preserve_index=False,
    )
    held_count = len(names)
    complete_count = len(complete)
    print(f'{date.date()}: {held_count} names the rule holds, {complete_count} with a full year')
    cases = _cases(
        kaxanuk.portfolio_construction,
        complete,
    )
    rows = [
        _run_case(
            case,
            date,
            snapshot,
            history_table,
            complete,
        )
        for case in cases
    ]

    return rows


def _load_panel(
    folder: pathlib.Path,
) -> dict[str, pandas.DataFrame]:
    """
    One wide `dates x securities` matrix per column the check reads, for the seed's securities.
    """
    seed = pandas.read_csv(SEED_PATH)
    seed_identifiers = seed['main_identifier'].astype(str)
    identifiers = sorted(set(seed_identifiers))
    columns = {
        column: {}
        for column in PANEL_COLUMNS
    }

    for identifier in identifiers:
        path = folder / f'{identifier}.parquet'

        if not path.is_file():
            continue

        table = pyarrow.parquet.read_table(
            path,
            columns=['m_date', *PANEL_COLUMNS],
        )
        frame = table.to_pandas().set_index('m_date')
        frame.index = pandas.to_datetime(frame.index)

        for column in PANEL_COLUMNS:
            columns[column][identifier] = frame[column]

    panel = {
        column: pandas.DataFrame(series).sort_index()
        for column, series in columns.items()
    }

    return panel


def _mandate(
    portfolio_construction: object,
    names: list[str],
    maximum_weight: float,
) -> object:
    """
    A long-only mandate over the names, each weight between zero and `maximum_weight`.
    """
    entities = portfolio_construction.entities
    classification = entities.Classification(
        assignments={
            name: {'book': 'Core'}
            for name in names
        },
    )
    mandate = entities.Mandate(
        classification=classification,
        default_bounds=entities.Bounds(
            minimum=0.0,
            maximum=maximum_weight,
        ),
    )

    return mandate


def _problems(
    weights: pandas.Series,
    names: list[str],
) -> list[str]:
    """
    Every invariant the book breaks: a NaN, a negative weight, a sum above one, a name not offered.
    """
    offered = set(names)
    unknown = sorted(set(weights.index) - offered)
    total = float(weights.sum())
    absolute = weights.abs()
    gross = float(absolute.sum())
    missing = weights.isna()
    has_nan = bool(missing.any())
    negative = weights < -TOLERANCE
    checks = [
        (has_nan, 'a weight is NaN'),
        (bool(negative.any()), 'a weight is negative'),
        (total > 1 + 1e-6, f'the weights sum to {total:.6f}'),
        (len(unknown) > 0, f'names not offered: {unknown[:5]}'),
        (gross <= TOLERANCE, 'the book is empty'),
    ]
    problems = [
        message
        for broken, message in checks
        if broken
    ]

    return problems


def _row(
    case: MethodCase,
    date: pandas.Timestamp,
    names_in: int,
    seconds: float,
) -> dict[str, object]:
    """
    The fields every row carries, before the method's own outcome.
    """
    return {
        'method': case.name,
        'setting': case.label,
        'date': date.date().isoformat(),
        'names_in': names_in,
        'seconds': round(seconds, 2),
    }


def _rule_names(
    panel: dict[str, pandas.DataFrame],
    before: pandas.Timestamp,
) -> list[str]:
    """
    The names the rule holds on the date after `before`: members in an uptrend, sized and floored.
    """
    sys.path.insert(
        0,
        str(REPOSITORY_ROOT / 'Experiments'),
    )
    import portfolio_construction

    member = panel[INDEX_WEIGHT_COLUMN].loc[before] > 0
    uptrend = panel[TREND_COLUMN].loc[before] > 0
    score = panel[SCORE_COLUMN].loc[before]
    eligible = score[member & uptrend].dropna()
    held = portfolio_construction.bounded_by_score(
        eligible,
        CAP,
        FLOOR,
    )

    return list(held.index)


def _run_case(
    case: MethodCase,
    date: pandas.Timestamp,
    snapshot: pyarrow.Table,
    history_table: pyarrow.Table,
    names: list[str],
) -> dict[str, object]:
    """
    Build one method on the date's history, allocate the snapshot, and hold the book to the checks.
    """
    import kaxanuk.portfolio_construction.entities
    import kaxanuk.portfolio_construction.sizing

    sizing = kaxanuk.portfolio_construction.sizing
    entities = kaxanuk.portfolio_construction.entities
    needs_history = sizing.requirements_for(case.name).history_input is not None
    started = time.perf_counter()

    try:
        allocator = sizing.build_allocator(
            name=case.name,
            config=case.configuration,
            returns=history_table if needs_history else None,
        )
        allocated = allocator.allocate(snapshot=entities.UniverseSnapshot(table=snapshot))
        built = entities.Weights.from_allocated(allocated=allocated)
        weights = pandas.Series(
            built.as_mapping(),
            dtype=float,
        )
        cap_outcome = _cap_outcome(built)
    except Exception as exception:
        failed = _row(
            case,
            date,
            len(names),
            time.perf_counter() - started,
        )
        failed['status'] = f'fail: {type(exception).__name__}: {str(exception)[:200]}'

        return failed

    row = _row(
        case,
        date,
        len(names),
        time.perf_counter() - started,
    )
    held = weights[weights.abs() > TOLERANCE]
    problems = _problems(
        weights,
        names,
    )
    total = float(weights.sum())
    largest = float(weights.max())
    smallest = held.min() if len(held) else None
    smallest_held = None if smallest is None else float(smallest)
    concentration = float((weights ** 2).sum())
    effective_names = 1 / concentration if len(held) else None
    negative = weights < -TOLERANCE
    row.update({
        'status': 'ok' if not problems else 'fail: ' + '; '.join(problems),
        'names_held': len(held),
        'sum': round(total, 6),
        'largest': round(largest, 6),
        'smallest_held': None if smallest_held is None else round(smallest_held, 6),
        'effective_names': None if effective_names is None else round(effective_names, 2),
        'any_negative': bool(negative.any()),
        'cap_0_20': cap_outcome,
    })

    return row


def _snapshot(
    panel: dict[str, pandas.DataFrame],
    before: pandas.Timestamp,
    history: pandas.DataFrame,
    names: list[str],
) -> pyarrow.Table:
    """
    The date's snapshot: each name with the columns the snapshot methods read, as they stood before.
    """
    traded_value = panel[TRADED_VALUE_COLUMN][names]
    yearly_traded_value = traded_value.loc[:before].tail(HISTORY_DAYS).mean()
    trailing_mean = history.mean() * HISTORY_DAYS
    snapshot = pyarrow.table({
        'ticker': names,
        'score': panel[SCORE_COLUMN].loc[before, names].to_numpy(dtype=float),
        'market_cap': panel[INDEX_WEIGHT_COLUMN].loc[before, names].to_numpy(dtype=float),
        'adtv_63d': panel[SCORE_COLUMN].loc[before, names].to_numpy(dtype=float),
        'adtv_252d': yearly_traded_value.to_numpy(dtype=float),
        'expected_return': trailing_mean.to_numpy(dtype=float),
    })

    return snapshot


def _status_line(
    statuses: pandas.Series,
) -> str:
    """
    How many of a method's dates passed, and the first failure where one did not.
    """
    failures = statuses[statuses != 'ok']
    passed_count = len(statuses) - len(failures)
    passed = f'{passed_count}/{len(statuses)} ok'

    return passed if failures.empty else f'{passed}; first: {failures.iloc[0][:150]}'


if __name__ == '__main__':
    if importlib.util.find_spec('kaxanuk.portfolio_construction') is None:
        print('Portfolio Construction is not installed: uv run python Config/install_libraries.py')
        sys.exit(1)

    sys.exit(main())

# --- example: end ---
