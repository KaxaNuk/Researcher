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

# --- example: begin ---

import csv
import importlib.util
import inspect
import pathlib
import sys
import types

import pandas

# Every per-security file is written and read through one module, so it lives beside this one.
DATA_DIRECTORY = pathlib.Path(__file__).parent
sys.path.insert(0, str(DATA_DIRECTORY))

import time_series  # noqa: E402 - the path above has to exist first

__all__ = [
    "attach_index_weight",
    "attach_security_master",
    "load_custom_calculations",
    "load_panel",
    "main",
    "read_investable_identifiers",
    "refine_panel",
    "remove_stale_files",
    "write_panel",
]

CURATOR_DIRECTORY = pathlib.Path(__file__).parent / "Curator" / "Time_Series"
CUSTOM_CALCULATIONS_PATH = pathlib.Path(__file__).parent / "Refinery" / "custom_calculations.py"
DATE_COLUMN = "m_date"
HAND_SUPPLIED_PATH = pathlib.Path(__file__).parent / "hand_supplied.py"
IDENTIFIER_COLUMN = "main_identifier"
INDEX_WEIGHT_COLUMN = "r_index_weight"
REFINERY_DIRECTORY = pathlib.Path(__file__).parent / "Refinery" / "Time_Series"
# What a security is classified as **today**, joined for grouping and reporting only.  The prefix
# is the warning: a sector attributed before a reclassification is wrong, and nothing raises.
SECURITY_MASTER_COLUMNS = {
    "industry": "current_industry",
    "sector": "current_sector",
}
SECURITY_MASTER_PATH = pathlib.Path(__file__).parent.parent / "Universe" / "Security_Master.csv"
SEED_PATH = pathlib.Path(__file__).parent.parent / "Universe" / "Investable_Universe.csv"


def attach_index_weight(
    panel: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    Map the index's weight on each date onto the panel, zero for a name not in the index that day.

    The holdings arrive keyed by the index's tickers and are renamed through the seed, so a listing
    whose two names differ is still a member.  A date the holdings do not cover -- before the file
    starts, or after it ends -- carries no weight: membership is never carried forward past the
    last date the desk wrote.
    """
    specification = importlib.util.spec_from_file_location(
        "hand_supplied",
        HAND_SUPPLIED_PATH,
    )
    hand_supplied = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(hand_supplied)
    holdings = hand_supplied.read_member_holdings()
    stacked = holdings.stack()
    long_weights = stacked.rename(INDEX_WEIGHT_COLUMN).reset_index()
    long_weights.columns = [
        DATE_COLUMN,
        IDENTIFIER_COLUMN,
        INDEX_WEIGHT_COLUMN,
    ]
    joined = panel.merge(
        long_weights,
        on=[
            DATE_COLUMN,
            IDENTIFIER_COLUMN,
        ],
        how="left",
        validate="one_to_one",
    )
    joined[INDEX_WEIGHT_COLUMN] = joined[INDEX_WEIGHT_COLUMN].fillna(0.0)

    return joined


def attach_security_master(
    panel: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    Map the master's columns onto the panel by identifier, as `current_*`.

    A mapping rather than a merge, so no row can be duplicated or dropped by a join key nobody
    checked.  A master that has not been written yet is not an error: the columns are simply
    absent, and the refinery still runs.
    """
    if not SECURITY_MASTER_PATH.is_file():
        print(f"{SECURITY_MASTER_PATH.name} not written yet: no current_* columns")

        return panel

    with SECURITY_MASTER_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        master_rows = {
            row[IDENTIFIER_COLUMN]: row
            for row in reader
        }

    for source_column, output_column in SECURITY_MASTER_COLUMNS.items():
        values = {
            identifier: row.get(source_column) or None
            for identifier, row in master_rows.items()
        }
        panel[output_column] = panel[IDENTIFIER_COLUMN].map(values)

    return panel


def load_custom_calculations() -> "types.ModuleType":
    """
    Import the `r_*` functions by path, the same way the curator imports its own.

    A function is found by the column's name and fed by its parameters' names, so a new column
    needs no registration beyond being defined and listed in `REFINERY_COLUMNS`.
    """
    specification = importlib.util.spec_from_file_location(
        "refinery_custom_calculations",
        CUSTOM_CALCULATIONS_PATH,
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def load_panel(
    columns: tuple[str, ...],
) -> "pandas.DataFrame":
    """
    Stack the curated files of the seed's identifiers into one frame, columns kept to a minimum.

    Membership comes from the seed, so the cash proxy and the benchmark sitting in the same folder
    can never reach a cross-section: a benchmark ranked against its own constituents would be
    meaningless, and the cash proxy would sit at the bottom of every liquidity rank.  Only the
    columns the calculations actually read are loaded, which keeps a panel of hundreds of
    securities over twenty-five years inside a few hundred megabytes.
    """
    investable = read_investable_identifiers()
    spans = read_valid_spans()
    frames = []

    for path in sorted(CURATOR_DIRECTORY.glob(f"*{time_series.SUFFIX}")):
        if path.stem not in investable:
            continue

        full_frame = time_series.read_frame(
            path,
            columns,
        )
        frame = _inside_span(
            full_frame,
            spans.get(path.stem, {}),
        )
        frame.insert(
            0,
            IDENTIFIER_COLUMN,
            path.stem,
        )
        frames.append(frame)

    if len(frames) == 0:
        message = f"no curated files in {CURATOR_DIRECTORY}: run Data/curator.py first"

        raise FileNotFoundError(message)

    panel = pandas.concat(
        frames,
        ignore_index=True,
    )
    ordered = panel.sort_values([
        DATE_COLUMN,
        IDENTIFIER_COLUMN,
    ])

    return ordered.reset_index(drop=True)


def main() -> int:
    """
    Build the cross-sectional columns and write one refined file per security.

    Runs after `Universe/universe_marimo.py`, whose security master it joins, and before
    `Data/analyzer_marimo.py`, which reads what it writes.
    """
    calculations = load_custom_calculations()
    inputs = set()

    for column in calculations.REFINERY_COLUMNS:
        function = getattr(calculations, column)
        parameters = inspect.signature(function).parameters
        inputs.update(parameters)

    built_columns = {
        name
        for name in inputs
        if name.startswith("r_")
    }
    panel_columns = tuple(
        sorted(inputs - built_columns - {IDENTIFIER_COLUMN})
    )
    panel = load_panel(panel_columns)
    securities = panel[IDENTIFIER_COLUMN].nunique()
    print(f"panel: {len(panel):,} rows from {securities} securities")
    weighted = attach_index_weight(panel)
    enriched = attach_security_master(weighted)
    refined = refine_panel(
        enriched,
        calculations,
    )
    written = write_panel(refined)
    removed = remove_stale_files(refined)
    print(f"wrote {written} files to {REFINERY_DIRECTORY}, removed {removed} stale")

    return 0


def read_investable_identifiers() -> frozenset[str]:
    """Read the seed, which is the only thing that decides what belongs in a cross-section."""
    with SEED_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        identifiers = {
            row[IDENTIFIER_COLUMN].strip()
            for row in reader
            if row.get(IDENTIFIER_COLUMN, "").strip()
        }

    return frozenset(identifiers)


def read_valid_spans() -> dict[str, dict[str, str]]:
    """
    The first and last date the seed lets each price file speak for its security.

    An empty bound is no bound: a security whose identity the index's master does not date is read
    over the whole file.
    """
    with SEED_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        spans = {
            row[IDENTIFIER_COLUMN].strip(): {
                "valid_from": (row.get("valid_from") or "").strip(),
                "valid_to": (row.get("valid_to") or "").strip(),
            }
            for row in reader
            if row.get(IDENTIFIER_COLUMN, "").strip()
        }

    return spans


def refine_panel(
    panel: "pandas.DataFrame",
    calculations: "types.ModuleType",
) -> "pandas.DataFrame":
    """
    Build each listed column in order, feeding every function the columns its parameters name.

    Order is the dependency declaration: a column may read anything built before it.  A parameter
    naming a column that is not there is a hard error rather than a silently missing column,
    because an absent input is almost always a typo that would surface much later.
    """
    for column in calculations.REFINERY_COLUMNS:
        function = getattr(calculations, column)
        parameters = inspect.signature(function).parameters
        missing = [
            name
            for name in parameters
            if name not in panel.columns
        ]

        if len(missing) > 0:
            message = f"{column} needs columns the panel does not have: {missing}"

            raise ValueError(message)

        arguments = {
            name: panel[name]
            for name in parameters
        }
        panel[column] = function(**arguments)
        populated = panel[column].notna().sum()
        print(f"{column}: {populated:,} of {len(panel):,} rows populated")

    return panel


def remove_stale_files(
    refined: "pandas.DataFrame",
) -> int:
    """
    Delete refined files for securities the seed no longer holds, naming each one.

    A stale file carries ranks taken against a universe that no longer exists, and anything reading
    the folder would average two incompatible cross-sections without raising.
    """
    current = set(refined[IDENTIFIER_COLUMN].unique())
    stale_paths = [
        path
        for path in sorted(REFINERY_DIRECTORY.glob(f"*{time_series.SUFFIX}"))
        if path.stem not in current
    ]

    for path in stale_paths:
        print(f"removing stale {path.name}")
        path.unlink()

    return len(stale_paths)


def write_panel(
    refined: "pandas.DataFrame",
) -> int:
    """
    Write one file per security: its curated columns, then `current_*`, then the new `r_*` ones.

    Each file is rewritten from its curated original, so a refined file stays a drop-in replacement
    for the file it came from, with the same rows in the same order.
    """
    REFINERY_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    added_columns = [
        column
        for column in refined.columns
        if column.startswith(("current_", "r_"))
    ]
    written_identifiers = []

    for identifier, group in refined.groupby(IDENTIFIER_COLUMN):
        curated = time_series.read_frame(time_series.path_for(CURATOR_DIRECTORY, identifier))
        additions = group[[DATE_COLUMN, *added_columns]]
        # An inner join keeps only the rows inside the security's span, which the panel already
        # cut: a date outside it is another company's price under the same symbol.
        output = curated.merge(
            additions,
            on=DATE_COLUMN,
            how="inner",
        )
        time_series.write_frame(
            output,
            time_series.path_for(REFINERY_DIRECTORY, identifier),
        )
        written_identifiers.append(identifier)

    return len(written_identifiers)


def _inside_span(
    frame: "pandas.DataFrame",
    span: dict[str, str],
) -> "pandas.DataFrame":
    """
    The rows of one security's file that fall inside its span, both ends included.
    """
    dates = frame[DATE_COLUMN]
    first_date = dates.min()
    last_date = dates.max()
    start = pandas.Timestamp(span.get("valid_from") or first_date)
    end = pandas.Timestamp(span.get("valid_to") or last_date)
    inside = (dates >= start) & (dates <= end)

    return frame.loc[inside].reset_index(drop=True)


if __name__ == "__main__":
    sys.exit(main())

# --- example: end ---
