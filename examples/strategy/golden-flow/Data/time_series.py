"""
Time series -- step 3 of 8: how every per-security file is stored, and the one way it is read.

In plain words: every price file, curated or refined, is a Parquet file read and written with
PyArrow, so a step reads only the columns it asks for and never parses text.

Runs inside every stage that touches a per-security file: `Data/curator.py`, `Data/refinery.py`,
the universe and analyzer notebooks, and the experiments' seams.  Each imports it from `Data/`, a
folder rather than a package, so each puts `Data/` on the import path first.

What is expected here:

- One schema for every file: the date as `date32`, every other numeric column as `float64`, and a
  text column -- an identifier, a `current_*` classification -- kept as text.  The Data Curator can
  write a provider's prices as decimals whose precision changes from file to file, and its volume
  as integers; read as they come, two files would not stack, and the engine and pandas would each
  read them their own way.  So every file the Curator writes is rewritten in the shared schema
  before anything reads it.  A decimal cast to `float64` is the same number a CSV of it parsed to.
- One place that names a file: the identifier and the suffix, `<identifier>.parquet`, in the
  folder of the stage that wrote it.
- Read only the columns asked for, from the file's footer first.  A file of eighteen columns read
  for two is the difference between a step that loads a quarter of a century in seconds and one
  that loads it in minutes.  A caller stacking many files stacks them as Arrow tables and converts
  to pandas once.
- Name a missing column in the error, before anything is read.

It produces nothing of its own: it is how `Data/Curator/Time_Series/` and
`Data/Refinery/Time_Series/` are written and read.

It prevents two stages reading the same file two ways, and a run that spends its hours parsing
text instead of computing.
"""

# --- example: begin ---

import pathlib

import pandas
import pyarrow
import pyarrow.compute
import pyarrow.parquet

__all__ = [
    "DATE_COLUMN",
    "SUFFIX",
    "normalize_file",
    "path_for",
    "read_column_names",
    "read_frame",
    "read_table",
    "write_frame",
]

# Snappy is PyArrow's default: fast to read, and the files stay a fraction of their CSV size.
COMPRESSION = "snappy"
DATE_COLUMN = "m_date"
# The column types read as `float64`: decimals and integers as the Curator writes them, floats, and
# a column with no value at all, which PyArrow types as null.
NUMERIC_TYPES = (
    pyarrow.types.is_decimal,
    pyarrow.types.is_floating,
    pyarrow.types.is_integer,
    pyarrow.types.is_null,
)
SUFFIX = ".parquet"


def normalize_file(
    path: "pathlib.Path",
) -> None:
    """
    Rewrite one file in the shared schema: the date as `date32`, every other column as `float64`.

    The Data Curator writes Sharadar's prices as decimals of the precision each file needs and its
    volume as integers, so this is the step that makes two of its files stack.
    """
    table = pyarrow.parquet.read_table(path)
    normalized = _normalized(table)
    pyarrow.parquet.write_table(
        normalized,
        path,
        compression=COMPRESSION,
    )


def path_for(
    directory: "pathlib.Path",
    identifier: str,
) -> "pathlib.Path":
    """
    The file that holds one identifier's series in a directory.
    """
    return directory / f"{identifier}{SUFFIX}"


def read_column_names(
    path: "pathlib.Path",
) -> tuple[str, ...]:
    """
    A file's columns, read from its footer without reading a row.
    """
    schema = pyarrow.parquet.read_schema(path)

    return tuple(schema.names)


def read_frame(
    path: "pathlib.Path",
    columns: tuple[str, ...] | None = None,
) -> "pandas.DataFrame":
    """
    Read a file, or only some of its columns, with the date as a pandas timestamp.

    A column the file does not carry is named in the error before any row is read.
    """
    table = read_table(
        path,
        columns,
    )

    return table.to_pandas()


def read_table(
    path: "pathlib.Path",
    columns: tuple[str, ...] | None = None,
) -> "pyarrow.Table":
    """
    Read a file, or only some of its columns, as a PyArrow table, the date as a timestamp.

    A caller stacking many files stacks the tables and converts once: converting every file to
    pandas on its own costs more than reading it.  A column the file does not carry is named in the
    error before any row is read.
    """
    if columns is not None:
        carried = read_column_names(path)
        missing = [
            column
            for column in columns
            if column not in carried
        ]

        if len(missing) > 0:
            message = f"{path.name} does not carry {missing}"

            raise KeyError(message)

    table = pyarrow.parquet.read_table(
        path,
        columns=None if columns is None else list(columns),
    )

    if DATE_COLUMN not in table.column_names:

        return table

    position = table.column_names.index(DATE_COLUMN)
    timestamps = pyarrow.compute.cast(
        table.column(DATE_COLUMN),
        pyarrow.timestamp("ns"),
    )

    return table.set_column(
        position,
        DATE_COLUMN,
        timestamps,
    )


def write_frame(
    frame: "pandas.DataFrame",
    path: "pathlib.Path",
) -> None:
    """
    Write a frame in the shared schema, its index dropped.
    """
    table = pyarrow.Table.from_pandas(
        frame,
        preserve_index=False,
    )
    normalized = _normalized(table)
    pyarrow.parquet.write_table(
        normalized,
        path,
        compression=COMPRESSION,
    )


def _normalized(
    table: "pyarrow.Table",
) -> "pyarrow.Table":
    """
    The same table with the date as `date32` and every other numeric column as `float64`.

    Text columns -- an identifier, a `current_*` classification -- are kept as they are.
    """
    columns = []

    for name, column in zip(table.column_names, table.columns):
        numeric = any(
            is_type(column.type)
            for is_type in NUMERIC_TYPES
        )

        if name == DATE_COLUMN:
            dated = pyarrow.compute.cast(
                column,
                pyarrow.date32(),
            )
            columns.append(dated)
        elif numeric:
            floats = pyarrow.compute.cast(
                column,
                pyarrow.float64(),
            )
            columns.append(floats)
        else:
            columns.append(column)

    return pyarrow.Table.from_arrays(
        columns,
        names=table.column_names,
    )

# --- example: end ---
