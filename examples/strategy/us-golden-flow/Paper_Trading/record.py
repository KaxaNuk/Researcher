"""
The paper-trading record -- step 7 of 8.  Where each run of `daily_update.py` writes what it saw,
and the one place that decides how a record is kept: in files, in a database, or both.

In plain words: a paper book's history is evidence only if nobody can quietly rewrite it.  Every
row is keyed, so a second run of the same day replaces that day's rows instead of adding to them,
and a past value the engine now prices differently is flagged as a restatement, never overwritten.

Six tables, each keyed by the columns named here:

    runs         book, as_of                              the commit, the status, the manifest
    books        book, as_of, series, identifier          the target weights in force that day
    performance  book, window, series, date               the engine's daily value and return
    statistics   book, as_of, window, series, statistic   the engine's summary figures
    diagnostics  book, date, measure                      what the book looked like that day
    flags        book, as_of, kind, detail                everything outside its band, every
                                                          failed check, every restatement

`window` is `whole`, from the experiment's first day, `after_window`, from the day after its last,
or `since_freeze`, from the day the book was frozen; `series` is `book`, `control` or `benchmark`.

Two sinks, chosen in `Config/.env` by `PAPER_TRADING_SINKS`: `local` writes the tables as CSV files
under `Paper_Trading/Record/`, and `database` writes them to the DuckDB database that
`PAPER_TRADING_DATABASE` names -- a file, or a PostgreSQL server reached through DuckDB's
`postgres` extension, written `postgres:<connection string>`.  A local record is not regenerable:
the provider restates its history, so a day's inputs cannot be fetched again as they were.  Local
alone is not a backup.

With `PAPER_TRADING_PUBLISH_DATA`, the refreshed price files go into the database too, as the
table `market_data`, so a machine with `PAPER_TRADING_INPUT=database` runs every book from them
without a download or a data key.

Nothing here computes a performance figure: `performance` and `statistics` hold what the engine
returned, and nothing else.
"""

# --- example: begin ---

import pathlib

import duckdb
import pandas

__all__ = [
    "RESTATEMENT_TOLERANCE",
    "TABLE_KEYS",
    "export_market_data",
    "publish_market_data",
    "read_table",
    "separate_restatements",
    "write_tables",
]

MARKET_DATA_TABLE = "market_data"
POSTGRES_PREFIX = "postgres:"
# A past daily value may move by rounding when the provider rebases an adjusted price -- integer
# share counts are recomputed from it -- and by nothing else.  A move larger than this is a
# restatement: the provider changed a price the book was already valued on.
RESTATEMENT_TOLERANCE = 0.001
TABLE_KEYS = {
    "books": (
        "book",
        "as_of",
        "series",
        "identifier",
    ),
    "diagnostics": (
        "book",
        "date",
        "measure",
    ),
    "flags": (
        "book",
        "as_of",
        "kind",
        "detail",
    ),
    "performance": (
        "book",
        "window",
        "series",
        "date",
    ),
    "runs": (
        "book",
        "as_of",
    ),
    "statistics": (
        "book",
        "as_of",
        "window",
        "series",
        "statistic",
    ),
}
# A day's flags and holdings are replaced whole when the day is run again: a flag the new run no
# longer raises, or a name it no longer holds, must not survive from the earlier run.
DAY_REPLACED_TABLES = (
    "books",
    "flags",
)
DAY_KEY = (
    "book",
    "as_of",
)


def export_market_data(
    database: str,
    directory: "pathlib.Path",
) -> int:
    """
    Write the published price files back out, one per identifier, where the stages read them.

    This is the input side of a machine that does not download: the files are the ones another
    run published, in their columns, so every stage downstream reads what it always reads.
    """
    connection = _connect(database)
    table = _qualified(database, MARKET_DATA_TABLE)
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
    listed = connection.execute(f"SELECT DISTINCT identifier FROM {table} ORDER BY identifier")
    identifiers = [
        row[0]
        for row in listed.fetchall()
    ]

    for identifier in identifiers:
        selected = connection.execute(
            f"SELECT * EXCLUDE (identifier) FROM {table} WHERE identifier = ? ORDER BY m_date",
            [identifier],
        )
        frame = selected.df()
        frame.to_csv(
            directory / f"{identifier}.csv",
            index=False,
        )

    connection.close()

    return len(identifiers)


def publish_market_data(
    directory: "pathlib.Path",
    database: str,
) -> int:
    """
    Replace the database's copy of the price files with this run's, and say how many rows it holds.
    """
    connection = _connect(database)
    table = _qualified(database, MARKET_DATA_TABLE)
    pattern = (directory / "*.csv").as_posix()
    statement = " ".join([
        f"CREATE OR REPLACE TABLE {table} AS",
        "SELECT parse_filename(filename, true) AS identifier, * EXCLUDE (filename)",
        f"FROM read_csv('{pattern}', filename = true, union_by_name = true, header = true)",
    ])
    connection.execute(statement)
    counted = connection.execute(f"SELECT count(*) FROM {table}")
    rows = counted.fetchone()[0]
    connection.close()

    return rows


def read_table(
    name: str,
    sinks: tuple[str, ...],
    record_directory: "pathlib.Path",
    database: str,
) -> "pandas.DataFrame":
    """
    What the record already holds for one table, from the database when it is a sink.

    The database is read first because it is the durable copy; the local files are read when it is
    not configured.  An empty frame means the book has no history yet.
    """
    if "database" in sinks:

        return _read_database_table(
            name,
            database,
        )

    path = record_directory / f"{name}.csv"

    if not path.is_file():

        return pandas.DataFrame()

    return pandas.read_csv(
        path,
        dtype=str,
    )


def separate_restatements(
    previous: "pandas.DataFrame",
    current: "pandas.DataFrame",
    as_of: str,
) -> dict[str, "pandas.DataFrame"]:
    """
    Split today's performance rows into those that may be written and the restatements.

    A row whose key the record already holds, and whose value moved by more than the tolerance, is
    a restatement: it is flagged, and it is kept out of what is written, so the record goes on
    holding the value it held.  Every other row is written, which is how a new day enters and how
    an unchanged day is replaced by itself.
    """
    keys = list(TABLE_KEYS["performance"])

    if len(previous) == 0:

        return {
            "flags": pandas.DataFrame(),
            "writable": current,
        }

    earlier = previous[keys + ["value"]].rename(columns={"value": "recorded"})
    typed = earlier.astype({"recorded": float})
    joined = current.merge(
        typed,
        on=keys,
        how="left",
    )
    ratio = joined["value"] / joined["recorded"]
    moved = (ratio - 1).abs() > RESTATEMENT_TOLERANCE
    restated_mask = joined["recorded"].notna() & moved
    restated = joined[restated_mask]
    details = [
        " ".join([
            f"{row.window} {row.series} {row.date}:",
            f"recorded {row.recorded:.2f}, now {row.value:.2f}",
        ])
        for row in restated.itertuples()
    ]
    flags = pandas.DataFrame({
        "book": restated["book"],
        "as_of": as_of,
        "kind": "restatement",
        "detail": details,
        "severity": "flag",
    })
    writable = joined[~restated_mask].drop(columns=["recorded"])

    return {
        "flags": flags,
        "writable": writable,
    }


def write_tables(
    tables: dict[str, "pandas.DataFrame"],
    sinks: tuple[str, ...],
    record_directory: "pathlib.Path",
    database: str,
) -> None:
    """
    Upsert every table into every configured sink: rows with a key already held are replaced, and a
    day's flags and holdings are replaced whole when the day is run again.
    """
    for name, frame in tables.items():
        if len(frame) == 0:
            continue

        key_types = dict.fromkeys(
            TABLE_KEYS[name],
            str,
        )
        text_frame = frame.astype(key_types)

        if "local" in sinks:
            _write_local(
                name,
                text_frame,
                record_directory,
            )

        if "database" in sinks:
            _write_database(
                name,
                text_frame,
                database,
            )


def _connect(
    database: str,
) -> "duckdb.DuckDBPyConnection":
    """
    Open the database: a DuckDB file, or a PostgreSQL server attached through DuckDB as `paper`.
    """
    if database.startswith(POSTGRES_PREFIX):
        server_connection = duckdb.connect()
        server_connection.execute("INSTALL postgres")
        server_connection.execute("LOAD postgres")
        connection_string = database.removeprefix(POSTGRES_PREFIX)
        server_connection.execute(
            "ATTACH ? AS paper (TYPE postgres)",
            [connection_string],
        )

        return server_connection

    path = pathlib.Path(database)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return duckdb.connect(str(path))


def _qualified(
    database: str,
    name: str,
) -> str:
    """
    A table's name as a query writes it: inside the attached server, or in the file itself.
    """
    if database.startswith(POSTGRES_PREFIX):

        return f"paper.{name}"

    return name


def _read_database_table(
    name: str,
    database: str,
) -> "pandas.DataFrame":
    """
    One table from the database, or an empty frame before the table's first row.
    """
    connection = _connect(database)
    table = _qualified(database, name)

    try:
        selected = connection.execute(f"SELECT * FROM {table}")
        frame = selected.df()
    except duckdb.CatalogException:
        frame = pandas.DataFrame()

    connection.close()

    return frame


def _replace_rows(
    name: str,
    existing: "pandas.DataFrame",
    arriving: "pandas.DataFrame",
) -> "pandas.DataFrame":
    """
    The rows on file whose keys do not arrive, followed by every row that does.
    """
    keys = list(_replacement_keys(name))
    arriving_keys = arriving[keys].apply(tuple, axis=1)
    held_keys = existing[keys].apply(tuple, axis=1)
    replaced = held_keys.isin(set(arriving_keys))
    kept = existing[~replaced]

    return pandas.concat(
        [
            kept,
            arriving,
        ],
        ignore_index=True,
    )


def _replacement_keys(
    name: str,
) -> tuple[str, ...]:
    """
    The columns a row is replaced by: the whole day for a day's flags and holdings, else its key.
    """
    if name in DAY_REPLACED_TABLES:

        return DAY_KEY

    return TABLE_KEYS[name]


def _write_database(
    name: str,
    frame: "pandas.DataFrame",
    database: str,
) -> None:
    """
    Upsert one table in the database: delete the rows whose keys arrive, then insert them.
    """
    connection = _connect(database)
    table = _qualified(database, name)
    connection.register("incoming", frame)
    connection.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM incoming WHERE false")
    matches = " AND ".join([
        f"{table}.{key} = incoming.{key}"
        for key in _replacement_keys(name)
    ])
    connection.execute(f"DELETE FROM {table} USING incoming WHERE {matches}")
    connection.execute(f"INSERT INTO {table} BY NAME SELECT * FROM incoming")
    connection.unregister("incoming")
    connection.close()


def _write_local(
    name: str,
    frame: "pandas.DataFrame",
    record_directory: "pathlib.Path",
) -> None:
    """
    Upsert one table in its CSV file: the rows whose keys arrive replace the ones on file.
    """
    record_directory.mkdir(
        parents=True,
        exist_ok=True,
    )
    path = record_directory / f"{name}.csv"

    if path.is_file():
        existing = pandas.read_csv(
            path,
            dtype=str,
        )
        combined = _replace_rows(
            name,
            existing,
            frame.astype(str),
        )
    else:
        combined = frame

    combined.to_csv(
        path,
        index=False,
    )

# --- example: end ---
