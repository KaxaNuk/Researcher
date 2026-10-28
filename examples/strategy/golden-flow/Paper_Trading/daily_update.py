"""
The daily run over every graduated book -- step 7 of the KaxaNuk Strategy Template.

In plain words: once a day, after the market closes, refresh the data, run each frozen strategy
exactly as it was when it graduated, price it with the engine, and write down what happened --
how the book is doing over its whole history and since the day it was frozen, and anything that
does not look like the backtest said it would.

A graduated book is a frozen copy of the strategy, made once by `promote.py`: the files it needs,
copied byte for byte into `Paper_Trading_N/` in the strategy's own layout, with `FREEZE.json`
naming the commit, the date and the hash of each.  Every path in those copies resolves inside the
book's folder, so an experiment under construction can change the shared modules and the graduated
book never moves.  **A paper-trading run re-fits nothing**: a run that tunes anything is a
backtest wearing a costume, and it answers a question nobody asked.

What one run does, in order:

1. Takes a lock, so two runs never overlap -- a lock a killed run left for twelve hours is
   removed, and the log says so -- and writes its log to `Paper_Trading/Logs/`.
2. Refreshes the shared raw data once -- `Data/curator.py` with the day as its end date -- or,
   with `PAPER_TRADING_INPUT=database`, reads the panel another machine published.
3. Checks the newest day before any book reads it: a close with no fill price, a move no price can
   make, a cash or benchmark file behind the day, an index file behind it.  A check that fails
   stops every book before anything is written: a book on broken data is worse than none.  It
   reads that day alone: a security's file that ends before it, and a bad bar on a day between
   two runs, pass unflagged.
4. For each book in `BOOKS`: compares every frozen file with its hash in `FREEZE.json` -- the
   security master, which is never committed, among them -- and the Curator's calculations with
   the ones frozen, links the raw files into the book's folder, with the index and factor files
   from the drop zones beside them, and calls `paper_trading_N.run(as_of)`, which runs the frozen
   refinery and rule and prices the book and its control over the whole history, over the days
   after the experiment's window and since the freeze.  A frozen file missing or changed stops the
   book, as a changed calculation does.  The frozen `Data/hand_supplied.py` reads the drop zones
   in the book's folder when `KN_ANALYTICS_PATH` is empty.
5. Writes the record through `record.py`: the book in force, the engine's daily values and
   statistics, the diagnostics, and a flag for each diagnostic outside the band the book's
   section of `BITACORA.md` registered before its first day, each failed check and each
   restatement.
6. Exits 0 when clean, 1 when a flag was raised, 2 when a step failed, so a scheduler can tell.
   A step that raises is a failed day, with its traceback in the day's log: Python's own exit code
   for it, 1, would read as a flagged day, and a book flagged every day would hide the crash.

Configured in `Config/.env`: `PAPER_TRADING_INPUT` (`provider` or `database`),
`PAPER_TRADING_SINKS` (`local`, `database` or both), `PAPER_TRADING_DATABASE` and
`PAPER_TRADING_PUBLISH_DATA`; each has a flag that overrides it for one run.
`Paper_Trading/BITACORA.md` says how to schedule it.

Every performance figure it writes comes from the engine.  See `BITACORA.md` for the gate a book
passes to get here.
"""

# --- example: begin ---

# Golden Flow has no book on paper: its Experiment 1 reads as sound and regime-dependent, which is
# not paper traded alone, as `Paper_Trading/BITACORA.md` says.  This is the working daily run a
# book that graduates would take.

import argparse
import datetime
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import traceback
import types

import dotenv
import pandas

__all__ = [
    "BOOKS",
    "check_market_data",
    "main",
]

# The graduated books, by folder name.  A book is added here in the commit that freezes it, and
# removed in the commit that sends it to production or retires it.  None is on paper, as
# `BITACORA.md` records.
BOOKS = ()

PAPER_TRADING_DIRECTORY = pathlib.Path(__file__).parent
REPOSITORY_ROOT = PAPER_TRADING_DIRECTORY.parent
CURATOR_CALCULATIONS_PATH = REPOSITORY_ROOT / "Data" / "Curator" / "custom_calculations.py"
CURATOR_DIRECTORY = REPOSITORY_ROOT / "Data" / "Curator" / "Time_Series"
CURATOR_SCRIPT = REPOSITORY_ROOT / "Data" / "curator.py"
# The Analytics Factory's drop zones, linked into a book's folder beside the raw files, because the
# frozen reader of the Analytics Factory's files looks for them next to itself when
# `KN_ANALYTICS_PATH` is empty.
HAND_SUPPLIED_DIRECTORIES = (
    "Benchmarks",
    "Factors",
)
ENVIRONMENT_PATH = REPOSITORY_ROOT / "Config" / ".env"
HAND_SUPPLIED_PATH = REPOSITORY_ROOT / "Data" / "hand_supplied.py"
LOCK_PATH = PAPER_TRADING_DIRECTORY / "Logs" / "daily_update.lock"
LOG_DIRECTORY = PAPER_TRADING_DIRECTORY / "Logs"
RECORD_DIRECTORY = PAPER_TRADING_DIRECTORY / "Record"
RECORD_PATH = PAPER_TRADING_DIRECTORY / "record.py"
SEED_PATH = REPOSITORY_ROOT / "Universe" / "Investable_Universe.csv"

# The cash proxy and the benchmark every book is priced with.  A day they have not reached is a day
# no book can be valued on.
CASH_AND_BENCHMARK = (
    "BIL",
    "SPY",
)
DEFAULT_DATABASE = "Paper_Trading/paper_trading.duckdb"
EXIT_CLEAN = 0
EXIT_FAILED = 2
EXIT_FLAGGED = 1
# A price that multiplies or divides by more than this in a day is a bad print, not a return; the
# universe notebook's register uses the same threshold.
IMPOSSIBLE_MOVE = 6.0
# A sum of weights lands a billionth past its band's edge on a fully invested day; that is
# arithmetic, not a divergence.
BAND_TOLERANCE = 1e-9
# No run takes this long, so a lock older than this was left by a run that was killed.
STALE_LOCK_HOURS = 12
# The cash proxy and the benchmark may trail the day asked for by a weekend and a holiday.
STALE_PRICE_DAYS = 4
# The Analytics Factory's index files are refreshed by hand; older than this, membership is being
# held at their last date and every run says so.
STALE_INDEX_DAYS = 7
TAIL_BYTES = 16384


def check_market_data(
    as_of: "datetime.date",
) -> dict[str, object]:
    """
    Read the newest rows of every price file and say what is wrong with the day, before any book.

    Returns the day the books are run on -- the last day the cash proxy and the benchmark both
    reached, never later than the day asked for -- and the flags.  Only the last two rows of each
    file are read, so the check costs seconds, not the minutes a full read of the panel would.
    """
    flags = []
    newest_dates = []

    for identifier in CASH_AND_BENCHMARK:
        reference_rows = _read_last_rows(CURATOR_DIRECTORY / f"{identifier}.csv")
        newest_date = reference_rows["m_date"].max()
        newest_dates.append(newest_date.date())

    effective = min(
        min(newest_dates),
        as_of,
    )

    if effective < as_of - datetime.timedelta(days=STALE_PRICE_DAYS):
        flags.append(_flag(
            "stale-input",
            f"the cash proxy and the benchmark end {effective}, the day asked for is {as_of}",
            "flag",
        ))

    seed = pandas.read_csv(SEED_PATH)
    identifiers = seed["main_identifier"].dropna()

    for identifier in identifiers:
        path = CURATOR_DIRECTORY / f"{identifier}.csv"

        if not path.is_file():
            continue

        flags.extend(_check_newest_row(
            identifier,
            path,
            effective,
        ))

    hand_supplied = _load_module(
        "hand_supplied",
        HAND_SUPPLIED_PATH,
    )
    holdings = hand_supplied.read_benchmark_holdings()
    index_end = holdings.index.max().date()

    if index_end < effective - datetime.timedelta(days=STALE_INDEX_DAYS):
        flags.append(_flag(
            "stale-input",
            f"the index holdings end {index_end}: membership is held at that date",
            "flag",
        ))

    return {
        "as_of": effective,
        "flags": flags,
    }


def main() -> int:
    """
    Run the day, every book, and say how it went in the exit code.

    A step that raises is a failed day, exit code 2, with its traceback in the day's log: left to
    Python it would exit 1, which a scheduler reads as a flagged day, and on a book whose inputs
    flag every day a crash would look like any other.
    """
    parser = argparse.ArgumentParser(description="The daily paper-trading run.")
    parser.add_argument(
        "--as-of",
        default="",
        help="the day to run, ISO; today when omitted",
    )
    parser.add_argument(
        "--book",
        default="",
        help="one book of BOOKS; every book when omitted",
    )
    parser.add_argument(
        "--input",
        default="",
        help="provider or database, for this run",
    )
    parser.add_argument(
        "--sinks",
        default="",
        help="local, database or local,database, for this run",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run everything and write nothing",
    )
    parser.add_argument(
        "--skip-refresh",
        action="store_true",
        help="use the price files already on disk",
    )
    arguments = parser.parse_args()
    dotenv.load_dotenv(
        ENVIRONMENT_PATH,
        override=False,
    )
    os.chdir(REPOSITORY_ROOT)
    settings = _read_settings(arguments)
    requested = _requested_day(arguments.as_of)
    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    _clear_stale_lock(requested)

    try:
        LOCK_PATH.touch(exist_ok=False)
    except FileExistsError:
        _note(requested, f"another run holds {LOCK_PATH}; stopping")

        return EXIT_FAILED

    try:
        exit_code = _run_day(
            requested,
            settings,
            arguments,
        )
    except Exception:
        failure = traceback.format_exc()
        message = f"failed, exit code {EXIT_FAILED}: {failure}"
        _note(requested, message)

        return EXIT_FAILED
    finally:
        LOCK_PATH.unlink(missing_ok=True)

    return exit_code


def _band_flags(
    diagnostics: "pandas.DataFrame",
    bands: dict[str, tuple[float, float]],
) -> list[dict[str, str]]:
    """
    One flag for every diagnostic of the day outside the band its book registered.
    """
    flags = []

    for row in diagnostics.itertuples():
        if row.measure not in bands:
            continue

        low, high = bands[row.measure]

        if row.value < low - BAND_TOLERANCE or row.value > high + BAND_TOLERANCE:
            flags.append(_flag(
                "divergence",
                f"{row.measure} {row.value:.4f} outside {low:.4f} to {high:.4f}",
                "flag",
            ))

    return flags


def _benchmark_frame(
    book: str,
    window: str,
    benchmark_table: object,
) -> "pandas.DataFrame":
    """
    The engine's benchmark over the book's own window, as rows of the performance table.
    """
    frame = benchmark_table.to_pandas()
    dates = pandas.to_datetime(frame["date_column"])
    iso_dates = [
        timestamp.date().isoformat()
        for timestamp in dates
    ]

    return pandas.DataFrame({
        "book": book,
        "window": window,
        "series": "benchmark",
        "date": iso_dates,
        "value": frame["bench_value"].astype(float).to_numpy(),
        "daily_return": frame["daily_return"].astype(float).to_numpy(),
    })


def _check_newest_row(
    identifier: str,
    path: "pathlib.Path",
    effective: "datetime.date",
) -> list[dict[str, str]]:
    """
    The two checks a security's newest day has to pass: a fill price, and a possible move.
    """
    flags = []
    rows = _read_last_rows(path)
    newest = rows.iloc[-1]
    newest_date = newest["m_date"].date()

    if newest_date != effective:

        return flags

    if pandas.isna(newest["c_vwap_dividend_and_split_adjusted"]):
        flags.append(_flag(
            "missing-fill-price",
            f"{identifier} closed on {effective} with no fill price",
            "stop",
        ))

    if len(rows) > 1:
        previous_close = rows.iloc[-2]["m_close_dividend_and_split_adjusted"]
        ratio = newest["m_close_dividend_and_split_adjusted"] / previous_close

        if ratio > IMPOSSIBLE_MOVE or ratio < 1 / IMPOSSIBLE_MOVE:
            flags.append(_flag(
                "bad-print",
                f"{identifier} moved by a factor of {ratio:.2f} on {effective}",
                "stop",
            ))

    return flags


def _clear_stale_lock(
    requested: "datetime.date",
) -> None:
    """
    Remove a lock a killed run left behind, and say so; a lock younger than that is respected.
    """
    if not LOCK_PATH.is_file():

        return

    locked_at = datetime.datetime.fromtimestamp(LOCK_PATH.stat().st_mtime)
    age = datetime.datetime.now() - locked_at

    if age > datetime.timedelta(hours=STALE_LOCK_HOURS):
        LOCK_PATH.unlink()
        _note(requested, f"removed a lock left at {locked_at:%Y-%m-%d %H:%M} by a run that stopped")


def _engine_tables(
    book: str,
    run: object,
) -> dict[str, "pandas.DataFrame"]:
    """
    The engine's daily values and statistics for each window and series, as the record keys them.

    The benchmark is read from the book's own run, so it is priced on the same days.  Only numbers
    the engine returned are copied; nothing here computes one.
    """
    performance_frames = []
    statistic_rows = []
    as_of = run.as_of.isoformat()

    for (window, series), result in run.results.items():
        register = result.data["Register_df"]
        dates = [
            timestamp.date().isoformat()
            for timestamp in register.index
        ]
        performance_frames.append(pandas.DataFrame({
            "book": book,
            "window": window,
            "series": series,
            "date": dates,
            "value": register["Total_Portfolio_Value"].to_numpy(),
            "daily_return": register["Returns"].to_numpy(),
        }))
        if series == "book":
            performance_frames.append(_benchmark_frame(
                book,
                window,
                result.data["benchmark"],
            ))

        statistic_rows.extend(_statistic_rows(
            result.data["portfolio_stats"],
            [
                book,
                as_of,
                window,
                series,
            ],
        ))

        if series == "book":
            statistic_rows.extend(_statistic_rows(
                result.data["benchmark_stats"],
                [
                    book,
                    as_of,
                    window,
                    "benchmark",
                ],
            ))

    performance = pandas.concat(
        performance_frames,
        ignore_index=True,
    )

    return {
        "performance": performance,
        "statistics": pandas.DataFrame(statistic_rows),
    }


def _flag(
    kind: str,
    detail: str,
    severity: str,
) -> dict[str, str]:
    """
    One flag, before its book and day are known.
    """

    return {
        "kind": kind,
        "detail": detail,
        "severity": severity,
    }


def _frozen_differences(
    book_directory: "pathlib.Path",
) -> list[str]:
    """
    What the book must find unchanged: its frozen files, and what it cannot copy.

    Every file `FREEZE.json` hashes is checked on disk.  The security master is among them and is
    never committed -- it is the provider's data -- so a copy of the strategy on another machine
    lacks it until it is brought across from the one that froze the book.  The raw files are shared
    by every book, so the calculations that produce their `c_*` columns cannot be frozen per book;
    they are checked with the Curator's version.  A difference means today's inputs are not the
    ones the book was frozen on, and the book is not run until a person decides what that means.
    """
    freeze_text = (book_directory / "FREEZE.json").read_text(encoding="utf-8")
    freeze = json.loads(freeze_text)
    differences = []

    for relative, frozen_hash in freeze["files"].items():
        frozen_path = book_directory / relative

        if not frozen_path.is_file():
            differences.append(f"{relative} is not on this machine: bring the frozen copy across")
        elif _hash_file(frozen_path) != frozen_hash:
            differences.append(f"{relative} is not the copy frozen on {freeze['freeze_date']}")

    shared = freeze["shared_inputs"]
    frozen_version = shared["kaxanuk-data-curator"]
    calculations_hash = _hash_file(CURATOR_CALCULATIONS_PATH)
    curator_version = importlib.metadata.version("kaxanuk-data-curator")

    if shared["Data/Curator/custom_calculations.py"] != calculations_hash:
        differences.append("Data/Curator/custom_calculations.py changed since the freeze")

    if frozen_version != curator_version:
        differences.append(f"kaxanuk-data-curator is {curator_version}, frozen at {frozen_version}")

    return differences


def _git_commit() -> str:
    """
    The commit the run's code is at, for the manifest.
    """
    completed = subprocess.run(
        [
            "git",
            "rev-parse",
            "HEAD",
        ],
        capture_output=True,
        check=False,
        cwd=REPOSITORY_ROOT,
        text=True,
    )

    return completed.stdout.strip()


def _hash_file(
    path: "pathlib.Path",
) -> str:
    """
    The SHA-256 of a file's bytes.
    """
    digest = hashlib.sha256(path.read_bytes())

    return digest.hexdigest()


def _hash_inputs() -> str:
    """
    One digest over every raw price file of the day, the manifest's snapshot of what was read.
    """
    digest = hashlib.sha256()

    for path in sorted(CURATOR_DIRECTORY.glob("*.csv")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())

    return digest.hexdigest()


def _link_hand_supplied(
    book_directory: "pathlib.Path",
) -> int:
    """
    Give the book's folder the Analytics Factory's index and factor files, linked as the raw files
    are.

    The frozen `Data/hand_supplied.py` resolves its drop zones from where it sits, so a book reads
    the index from its own folder; the files are the Analytics Factory's and never the book's, which
    is why `.gitignore` keeps them out of git.
    """
    linked = []

    for folder in HAND_SUPPLIED_DIRECTORIES:
        source_directory = REPOSITORY_ROOT / "Data" / "Curator" / folder
        target = book_directory / "Data" / "Curator" / folder
        target.mkdir(
            parents=True,
            exist_ok=True,
        )

        for stale in target.glob("*.csv"):
            stale.unlink()

        for source in sorted(source_directory.glob("*.csv")):
            destination = target / source.name

            try:
                os.link(source, destination)
            except OSError:
                shutil.copy2(source, destination)

            linked.append(destination)

    return len(linked)


def _link_raw_files(
    book_directory: "pathlib.Path",
) -> int:
    """
    Give the book's folder the day's raw files, as hard links where the volume allows.

    A hard link costs no time and no space, and the book reads the shared files through it; a copy
    is the fallback on a volume that refuses links.
    """
    target = book_directory / "Data" / "Curator" / "Time_Series"
    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    for stale in target.glob("*.csv"):
        stale.unlink()

    sources = sorted(CURATOR_DIRECTORY.glob("*.csv"))

    for source in sources:
        destination = target / source.name

        try:
            os.link(source, destination)
        except OSError:
            shutil.copy2(source, destination)

    return len(sources)


def _load_module(
    name: str,
    path: "pathlib.Path",
) -> "types.ModuleType":
    """
    Import a file by path under a name of its own, so two books' copies of a module never collide.
    """
    specification = importlib.util.spec_from_file_location(
        name,
        path,
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)

    return module


def _note(
    as_of: "datetime.date",
    message: str,
) -> None:
    """
    Print a line and keep it in the day's log.
    """
    print(message, flush=True)
    log_path = LOG_DIRECTORY / f"{as_of.isoformat()}.log"
    now = datetime.datetime.now()
    stamp = now.isoformat(timespec="seconds")

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp} {message}\n")


def _read_last_rows(
    path: "pathlib.Path",
) -> "pandas.DataFrame":
    """
    The header and the last two rows of a price file, without reading the rest of it.
    """
    with path.open("rb") as handle:
        header_bytes = handle.readline()
        size = handle.seek(0, os.SEEK_END)
        handle.seek(max(0, size - TAIL_BYTES))
        tail_bytes = handle.read()

    header = header_bytes.decode("utf-8-sig")
    tail = tail_bytes.decode("utf-8", errors="replace")
    complete_lines = tail.splitlines()[1:]
    lines = [
        line
        for line in complete_lines
        if line.strip()
    ]
    body = "\n".join(lines[-2:])
    buffer = io.StringIO(f"{header}{body}\n")

    return pandas.read_csv(
        buffer,
        parse_dates=["m_date"],
    )


def _read_settings(
    arguments: "argparse.Namespace",
) -> dict[str, object]:
    """
    The run's configuration: `Config/.env` first, each flag given on the command line over it.
    """
    source = arguments.input or os.environ.get("PAPER_TRADING_INPUT", "provider")
    sinks_text = arguments.sinks or os.environ.get("PAPER_TRADING_SINKS", "local")
    sinks = tuple(
        sink.strip()
        for sink in sinks_text.split(",")
        if sink.strip()
    )
    database = os.environ.get("PAPER_TRADING_DATABASE", "") or DEFAULT_DATABASE
    publish_text = os.environ.get("PAPER_TRADING_PUBLISH_DATA", "false")
    publish = publish_text.strip().lower() == "true"

    return {
        "database": database,
        "input": source,
        "publish": publish,
        "sinks": sinks,
    }


def _refresh_data(
    requested: "datetime.date",
    settings: dict[str, object],
    record: "types.ModuleType",
    skip_refresh: bool,
) -> bool:
    """
    Bring the shared raw files to the day: download them, or read them from the database.

    Returns whether it succeeded.  With the database as input nothing is downloaded and no data key
    is needed; with the database as a sink and publishing on, this run's files are written there for
    the machines that read it.
    """
    if settings["input"] == "database":
        written = record.export_market_data(
            settings["database"],
            CURATOR_DIRECTORY,
        )
        _note(requested, f"read {written} price files from {settings['database']}")

        return written > 0

    if not skip_refresh:
        completed = subprocess.run(
            [
                sys.executable,
                str(CURATOR_SCRIPT),
                "--end-date",
                requested.isoformat(),
            ],
            check=False,
            cwd=REPOSITORY_ROOT,
        )

        if completed.returncode != 0:
            _note(requested, f"the Curator stopped with exit code {completed.returncode}")

            return False

    if settings["publish"] and "database" in settings["sinks"]:
        rows = record.publish_market_data(
            CURATOR_DIRECTORY,
            settings["database"],
        )
        _note(requested, f"published {rows} rows of prices to {settings['database']}")

    return True


def _requested_day(
    text: str,
) -> "datetime.date":
    """
    The day asked for on the command line, or today.
    """
    if text == "":

        return datetime.date.today()

    return datetime.date.fromisoformat(text)


def _rows_of_book(
    frame: "pandas.DataFrame",
    book: str,
) -> "pandas.DataFrame":
    """
    The rows of one book, from a table that may be empty.
    """
    if len(frame) == 0:

        return frame

    return frame[frame["book"] == book]


def _run_and_record(
    book: str,
    checked: dict[str, object],
    settings: dict[str, object],
    dry_run: bool,
    record: "types.ModuleType",
    context: dict[str, str],
) -> int:
    """
    Run one book on the checked day, write its rows to every sink, and return its exit code.

    A shared check that stops the day stops the book before it runs, and its flags are still
    written, so the record says why the day has no book.
    """
    as_of = checked["as_of"]
    shared_flags = checked["flags"]
    stopping = [
        flag
        for flag in shared_flags
        if flag["severity"] == "stop"
    ]
    outcome = {"flags": [], "run": None} if len(stopping) > 0 else _run_book(book, as_of)
    run = outcome["run"]
    flag_rows = [
        {
            "book": book,
            "as_of": as_of.isoformat(),
            **flag,
        }
        for flag in [*shared_flags, *outcome["flags"]]
    ]
    now = datetime.datetime.now()
    tables = {
        "runs": pandas.DataFrame([{
            "book": book,
            "as_of": as_of.isoformat(),
            "commit": context["commit"],
            "inputs_sha256": context["inputs_sha256"],
            "input": settings["input"],
            "status": "stopped" if run is None else "ran",
            "run_at": now.isoformat(timespec="seconds"),
        }]),
    }

    if run is not None:
        engine_tables = _engine_tables(book, run)
        previous = record.read_table(
            "performance",
            settings["sinks"],
            RECORD_DIRECTORY,
            settings["database"],
        )
        separated = record.separate_restatements(
            _rows_of_book(previous, book),
            engine_tables["performance"],
            as_of.isoformat(),
        )
        restatement_rows = separated["flags"].to_dict("records")
        flag_rows.extend(restatement_rows)
        tables["performance"] = separated["writable"]
        tables["statistics"] = engine_tables["statistics"]
        tables["books"] = run.books.assign(book=book, as_of=as_of.isoformat())
        tables["diagnostics"] = run.diagnostics.assign(book=book)

        for line in run.summary:
            _note(as_of, f"{book} {line}")

    tables["flags"] = pandas.DataFrame(flag_rows)

    for flag in flag_rows:
        _note(as_of, f"{book} {flag['severity']} {flag['kind']}: {flag['detail']}")

    if not dry_run:
        record.write_tables(
            tables,
            settings["sinks"],
            RECORD_DIRECTORY,
            settings["database"],
        )

    severities = {
        flag["severity"]
        for flag in flag_rows
    }

    if run is None or "stop" in severities:

        return EXIT_FAILED

    if len(severities) > 0:

        return EXIT_FLAGGED

    return EXIT_CLEAN


def _run_book(
    book: str,
    as_of: "datetime.date",
) -> dict[str, object]:
    """
    Run one frozen book for the day, and return its run with the flags it raised.
    """
    book_directory = PAPER_TRADING_DIRECTORY / book
    differences = _frozen_differences(book_directory)

    if len(differences) > 0:
        unfrozen = [
            _flag(
                "unfrozen-input",
                difference,
                "stop",
            )
            for difference in differences
        ]

        return {
            "flags": unfrozen,
            "run": None,
        }

    _link_raw_files(book_directory)
    _link_hand_supplied(book_directory)
    module_name = book.lower()
    module = _load_module(
        f"{module_name}_book",
        book_directory / f"{module_name}.py",
    )
    run = module.run(as_of)
    band_flags = _band_flags(
        run.diagnostics,
        module.BANDS,
    )

    return {
        "flags": [*run.flags, *band_flags],
        "run": run,
    }


def _run_day(
    requested: "datetime.date",
    settings: dict[str, object],
    arguments: "argparse.Namespace",
) -> int:
    """
    The run itself, inside the lock: the data once, then every book, then the exit code.
    """
    record = _load_module(
        "paper_trading_record",
        RECORD_PATH,
    )
    _note(requested, f"daily update for {requested}: {settings['input']} to {settings['sinks']}")
    refreshed = _refresh_data(
        requested,
        settings,
        record,
        arguments.skip_refresh,
    )

    if not refreshed:

        return EXIT_FAILED

    checked = check_market_data(requested)
    books = (arguments.book,) if arguments.book else BOOKS
    context = {
        "commit": _git_commit(),
        "inputs_sha256": _hash_inputs(),
    }
    exit_codes = [
        _run_and_record(
            book,
            checked,
            settings,
            arguments.dry_run,
            record,
            context,
        )
        for book in books
    ]
    exit_code = max(exit_codes, default=EXIT_CLEAN)
    _note(requested, f"done, exit code {exit_code}")

    return exit_code


def _statistic_rows(
    statistics: dict[str, object],
    labels: list[str],
) -> list[dict[str, object]]:
    """
    The engine's numeric summary figures, as rows keyed by book, day, window and series.
    """
    book, as_of, window, series = labels

    return [
        {
            "book": book,
            "as_of": as_of,
            "window": window,
            "series": series,
            "statistic": statistic,
            "value": float(value),
        }
        for statistic, value in statistics.items()
        if isinstance(value, (int, float))
    ]


if __name__ == "__main__":
    sys.exit(main())

# --- example: end ---
