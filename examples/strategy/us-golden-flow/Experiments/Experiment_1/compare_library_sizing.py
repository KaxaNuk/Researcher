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

# --- example: begin ---

# In US-Golden-Flow, this script's own description:
#
# Compare the rule's book sized two ways -- by `bounded_by_score_and_sector` and by the KaxaNuk
# Portfolio Construction library -- on every rebalance date of Experiment 1, the rule and its
# control.
#
# In plain words: the experiment sizes its book with its own function,
# `bounded_by_score_and_sector`. The library's `feature_weighting`, proportional to the score, then
# `Weights.cap` and `Weights.cap_groups` in turn, should give the same names the same weights; this
# says on how many dates it does, and by how much it differs where it does not. It checks weights,
# never returns.
#
# Runs after `Data/curator.py`, from the repository root:
#
#     uv run python Experiments/Experiment_1/compare_library_sizing.py
#
# Eligibility is the notebook's, read the same way: a Core member with a 200-day history and a score
# at the close before the date, an open on the date, not excluded by the register's blocking rows;
# the rule adds `c_eligible_golden_cross_50_200`, the control drops it.
#
# It writes `library_sizing_check.csv` beside this file: each date and book, the names each way, the
# names in one book only, and the largest weight difference.

import functools
import pathlib
import sys

import pandas

__all__ = [
    'main',
]

EXPERIMENT_DIRECTORY = pathlib.Path(__file__).parent
REPOSITORY_ROOT = EXPERIMENT_DIRECTORY.parent.parent
FILL_COLUMN = 'c_open_dividend_and_split_adjusted'
MAXIMUM_WEIGHT = 0.20
MEMBERSHIP_COLUMN = 'c_index_weight'
MINIMUM_WEIGHT = 0.01
OUTPUT_PATH = EXPERIMENT_DIRECTORY / 'library_sizing_check.csv'
SCORE_COLUMN = 'c_traded_value_sma_63d'
TOLERANCE = 1e-9
CROSS_COLUMN = 'c_golden_cross_50_200'
ELIGIBLE_COLUMN = 'c_eligible_golden_cross_50_200'
SECTOR_MAXIMUM = 0.50
WINDOW_END = pandas.Timestamp('2026-10-31')
WINDOW_START = pandas.Timestamp('1999-12-31')


def main() -> int:
    """
    Size the rule and its control both ways on every rebalance date; 0 when every date agrees.
    """
    sys.path.insert(
        0,
        str(REPOSITORY_ROOT / 'Experiments'),
    )
    import attribution_analysis
    import portfolio_construction
    import securities_panel

    sectors = attribution_analysis.kn_sectors(attribution_analysis.load_factor_returns())
    notebook_weigher = functools.partial(
        portfolio_construction.bounded_by_score_and_sector,
        sectors=sectors,
        sector_maximum=SECTOR_MAXIMUM,
    )
    library_weigher = functools.partial(
        portfolio_construction.bounded_by_score_and_sector_with_library,
        sectors=sectors,
        sector_maximum=SECTOR_MAXIMUM,
    )
    matrices = securities_panel.load_matrices((
        CROSS_COLUMN,
        ELIGIBLE_COLUMN,
        SCORE_COLUMN,
        MEMBERSHIP_COLUMN,
        FILL_COLUMN,
    ))
    cut = {
        name: matrix.loc[:WINDOW_END]
        for name, matrix in matrices.items()
    }
    calendar = cut[FILL_COLUMN].index
    window_days = calendar[(calendar >= WINDOW_START) & (calendar <= WINDOW_END)]
    rebalance_dates = portfolio_construction.first_trading_days_of_month(window_days)
    excluded = _excluded()
    rows = []

    for book, use_cross in (('rule', True), ('control', False)):
        eligibility = _eligibility(
            cut,
            rebalance_dates,
            excluded,
            use_cross,
        )
        notebook_book = portfolio_construction.bounded_book(
            eligibility,
            cut[SCORE_COLUMN],
            MAXIMUM_WEIGHT,
            MINIMUM_WEIGHT,
            notebook_weigher,
        )
        library_book = portfolio_construction.bounded_book(
            eligibility,
            cut[SCORE_COLUMN],
            MAXIMUM_WEIGHT,
            MINIMUM_WEIGHT,
            library_weigher,
        )
        book_rows = _compare(
            book,
            notebook_book,
            library_book,
        )
        rows.extend(book_rows)

    table = pandas.DataFrame(rows)
    table.to_csv(
        OUTPUT_PATH,
        index=False,
    )
    weights_differ = table['largest_difference'] > TOLERANCE
    names_differ = table['names_in_one_only'] > 0
    disagreeing = table[weights_differ | names_differ]
    largest = float(table['largest_difference'].max())
    compared = len(table)
    print(f'{compared} book-dates; {len(disagreeing)} disagree; largest difference {largest:.2e}')
    print(f'wrote {OUTPUT_PATH}')

    return 0 if disagreeing.empty else 1


def _compare(
    book: str,
    notebook_book: pandas.DataFrame,
    library_book: pandas.DataFrame,
) -> list[dict[str, object]]:
    """
    One row per rebalance date: the names each way, those in one book only, the largest gap.
    """
    rows = []

    for date in notebook_book.index:
        notebook_row = notebook_book.loc[date]
        library_row = library_book.loc[date]
        notebook_names = set(notebook_row.index[notebook_row > 0])
        library_names = set(library_row.index[library_row > 0])
        difference = (notebook_row - library_row).abs()
        rows.append({
            'book': book,
            'date': date.date().isoformat(),
            'names_notebook': len(notebook_names),
            'names_library': len(library_names),
            'names_in_one_only': len(notebook_names ^ library_names),
            'largest_difference': float(difference.max()),
        })

    return rows


def _eligibility(
    cut: dict[str, pandas.DataFrame],
    rebalance_dates: pandas.DatetimeIndex,
    excluded: set[str],
    use_cross: bool,
) -> pandas.DataFrame:
    """
    Who may be held on each rebalance date, decided at the prior close, as the notebook decides it.
    """
    crossed_before = cut[CROSS_COLUMN].shift(1)
    membership = cut[MEMBERSHIP_COLUMN].fillna(0.0) > 0
    member_before = membership.shift(
        1,
        fill_value=False,
    )
    score_before = cut[SCORE_COLUMN].shift(1)
    priced = cut[FILL_COLUMN].notna()
    allowed = ~cut[FILL_COLUMN].columns.isin(sorted(excluded))
    eligible = member_before & crossed_before.notna() & score_before.notna() & priced & allowed
    crossed = eligible & (cut[ELIGIBLE_COLUMN] == 1) if use_cross else eligible

    return crossed.loc[rebalance_dates]


def _excluded() -> set[str]:
    """
    The names the register's blocking rows exclude, its missing-file check aside, as the notebook's.
    """
    issues = pandas.read_csv(REPOSITORY_ROOT / 'Universe' / 'Data_Issues.csv').fillna('')
    blocking = issues[
        (issues['severity'] == 'blocking') & ~issues['check'].str.startswith('missing file')
    ]
    excluded = {
        identifier
        for identifiers in blocking['identifiers']
        for identifier in str(identifiers).split()
    }

    return excluded


if __name__ == '__main__':
    sys.exit(main())

# --- example: end ---
