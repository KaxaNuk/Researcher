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

# --- example: begin ---

# In US-Golden-Flow, this script's own description:
#
# Price the four books a reader compares once more, one run each, so the Backtest Engine writes its
# results workbook into `Backtest/` for the KaxaNuk app to import.
#
# In plain words: the notebook prices its books in the engine's batch mode, which returns tables and
# writes no workbook; the app reads a backtest only from a single run's workbook, imported with
# *Backtest -> Parameters -> Import results*. This re-prices the four weight files the notebook
# writes where the app lists them -- the rule, its control, equal weight and the rule without the
# sector cap -- at the flat 5 bp row, the row the gate is read at, with the notebook's settings, and
# adds no book and no number: the workbooks hold the figures `summary.csv` holds. Each workbook is
# renamed after its cost row, so it reads apart from an earlier version's in the app.
#
# Runs after `experiment_1_marimo.py`, from the repository root:
#
#     uv run python Experiments/Experiment_1/app_workbooks.py

import datetime
import os
import pathlib
import sys
import tempfile

__all__ = [
    'main',
]

CASH_RESERVE = 0.01
COMMISSION_BASIS_POINTS = 1.0
# The flat row alone, the row the gate is read at: the owner keeps only it in the app (2026-11-20).
COST_ROWS = {
    'flat_5bp': 'basis_points',
}
EXPERIMENT_DIRECTORY = pathlib.Path(__file__).parent
HEADLINE_BOOKS = (
    'portfolio_weights',
    'portfolio_weights_control',
    'portfolio_weights_equal_weight',
    'portfolio_weights_no_sector_cap',
)
INITIAL_CAPITAL = 1_000_000
REPOSITORY_ROOT = EXPERIMENT_DIRECTORY.parent.parent
# The pre-registered model's fallback half-spread and the flat row's slippage are both 5 bp.
SLIPPAGE_BASIS_POINTS = 5.0
WINDOW_END = datetime.date.fromisoformat('2026-10-31')
WINDOW_START = datetime.date.fromisoformat('1999-12-31')
WORKBOOK_SUFFIX = '_backtest_results.xlsx'


def main() -> int:
    """
    Price each headline book at each cost row in a single run; 0 when every run succeeds.
    """
    sys.path.insert(
        0,
        str(REPOSITORY_ROOT / 'Experiments'),
    )
    import kaxanuk.backtest_engine

    import backtest_engine

    kaxanuk.backtest_engine.load_config_env(backtest_engine.ENVIRONMENT_PATH)
    failed = []

    for portfolio_name in HEADLINE_BOOKS:
        for row_name, slippage_model in COST_ROWS.items():
            configuration = backtest_engine.build_configuration(
                EXPERIMENT_DIRECTORY,
                WINDOW_START,
                WINDOW_END,
                INITIAL_CAPITAL,
                COMMISSION_BASIS_POINTS,
                slippage_model,
                SLIPPAGE_BASIS_POINTS,
                CASH_RESERVE,
                portfolio_name,
            )
            before = set(_workbooks())
            succeeded = _run_in_scratch(
                backtest_engine,
                configuration,
            )
            after = set(_workbooks())
            written = sorted(after - before)

            if succeeded and len(written) == 1:
                renamed = _rename_after_row(
                    written[0],
                    portfolio_name,
                    row_name,
                )
                print(f'{portfolio_name}, {row_name}: {renamed.name}')
            else:
                print(f'{portfolio_name}, {row_name}: failed')
                failed.append(f'{portfolio_name}, {row_name}')

    return 0 if not failed else 1


def _rename_after_row(
    workbook: pathlib.Path,
    portfolio_name: str,
    row_name: str,
) -> pathlib.Path:
    """
    The engine's workbook, renamed with its cost row after the book's name.
    """
    stamp = workbook.name.removeprefix(f'{portfolio_name}_').removesuffix(WORKBOOK_SUFFIX)
    target = workbook.with_name(f'{portfolio_name}_{row_name}_{stamp}{WORKBOOK_SUFFIX}')

    return workbook.rename(target)


def _run_in_scratch(
    backtest_engine: object,
    configuration: object,
) -> bool:
    """
    One run in a folder of its own, because the engine draws its charts into a fixed file name.
    """
    home = pathlib.Path.cwd()

    with tempfile.TemporaryDirectory() as scratch:
        os.chdir(scratch)

        try:
            result = backtest_engine.run_backtest(
                EXPERIMENT_DIRECTORY,
                configuration,
            )
        finally:
            os.chdir(home)

    return bool(result.success)


def _workbooks() -> list[pathlib.Path]:
    """
    The engine's workbooks in `Backtest/`, top level only, as the app lists them.
    """
    directory = EXPERIMENT_DIRECTORY / 'Backtest'

    return sorted(directory.glob(f'*{WORKBOOK_SUFFIX}'))


if __name__ == '__main__':
    sys.exit(main())

# --- example: end ---
