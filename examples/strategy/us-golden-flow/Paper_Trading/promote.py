"""
The promotion of an experiment to paper -- step 7 of 8.  Run once, when an experiment graduates --
every soundness and every performance criterion of the gate in `BITACORA.md` holds, and a person
has signed it there -- or when a person has signed it there as sound and regime-dependent, on
probation, its terms registered.  Never again for the same book.

In plain words: freeze the strategy.  Every file the book needs to go from raw prices to a priced
book is copied byte for byte, from the commit that graduated, into `Paper_Trading/Paper_Trading_N/`
in the strategy's own layout -- `Data/`, `Experiments/`, `Universe/` -- and `FREEZE.json` records
the commit, the date and the hash of each file.  Because every module here resolves its paths from
its own folder, the copies read and write inside the book's folder alone: an experiment under
construction can change the shared modules tomorrow, and the graduated book never moves.

What it copies is listed in `FROZEN_FILES`, and it refuses to run on a working tree with changes
to tracked files: a freeze of code nobody committed is a freeze nobody can reproduce.  It refuses
too unless the book's section of the committed `BITACORA.md`, headed `### Paper_Trading_N`, holds
exactly one sign-off line -- a person, a date and one of the two outcomes that put a book on
paper, graduating or sound and regime-dependent, on paper on probation -- and, for a book on
probation, the terms it is read against at its review.  It checks that a person signed, never what
the gate should have said, which is theirs.  The rule itself is not copied here -- it lives in a
cell of the experiment's marimo notebook -- so `paper_trading_N.py` carries it, written from the
experiment's cells and committed before the promotion.

Two things cannot be copied, because every book shares them: the raw price files, and the
calculations the Curator runs while it writes them.  `FREEZE.json` records the hash of those
calculations and the Curator's version, and `daily_update.py` refuses to run a book whose shared
inputs no longer match.

One frozen file is not in the commit: the security master, which the universe notebook writes from
the provider's data.  It is copied from disk and hashed like the rest, and `.gitignore` keeps the
book's copy out of git, as it keeps the one in `Universe/`: it stays on the machine that froze the
book, backed up with the record.

It produces `Paper_Trading_N/` with its frozen files and `FREEZE.json` -- the sign-off it froze on
among them -- committed by a person, all but the security master.

It prevents a graduated book changing because somebody improved the code it was frozen on.
"""

# --- example: begin ---

import argparse
import datetime
import hashlib
import importlib.metadata
import json
import pathlib
import re
import subprocess
import sys

__all__ = [
    "FROZEN_FILES",
    "main",
]

PAPER_TRADING_DIRECTORY = pathlib.Path(__file__).parent
REPOSITORY_ROOT = PAPER_TRADING_DIRECTORY.parent
BITACORA_PATH = "Paper_Trading/BITACORA.md"

# Everything between the raw price files and the priced book, from the commit: the refinery and its
# calculations, the reader of the desk's files, the shared modules the rule calls, and the seed.
FROZEN_FILES = (
    "Data/Refinery/custom_calculations.py",
    "Data/hand_supplied.py",
    "Data/refinery.py",
    "Data/time_series.py",
    "Experiments/backtest_engine.py",
    "Experiments/portfolio_construction.py",
    "Experiments/securities_panel.py",
    "Universe/Investable_Universe.csv",
)
# Written by the universe notebook from the provider's data, so never in a commit: copied from
# disk, hashed so the copy can be told from a later one, and kept out of git by `.gitignore`.
GENERATED_FILES = (
    "Universe/Security_Master.csv",
)
LIBRARIES = (
    "kaxanuk-backtest-engine",
    "kaxanuk-data-curator",
    "numpy",
    "pandas",
    "pyarrow",
)
# The two outcomes of the gate that put a book on paper, as a sign-off line in the book's section
# of `BITACORA.md` says them: "Signed off by <name> on <YYYY-MM-DD>, as <outcome>".
SIGN_OFF_OUTCOMES = (
    "graduating",
    "sound and regime-dependent, on paper on probation",
)
SIGN_OFF_PATTERN = re.compile(
    r"Signed off by (?P<person>[^*]+?) on (?P<date>\d{4}-\d{2}-\d{2}), as (?P<outcome>[^*.]+)",
)
# What a book on probation registers beside its sign-off, each a bold label in its section.
PROBATION_TERMS = (
    "**The regime prediction.**",
    "**The probation.**",
    "**The kill switch",
    "**The bands**",
)
SHARED_CALCULATIONS = "Data/Curator/custom_calculations.py"


def main() -> int:
    """
    Freeze book N and say what to commit.
    """
    parser = argparse.ArgumentParser(description="Freeze a graduated experiment as a paper book.")
    parser.add_argument(
        "number",
        type=int,
        help="the experiment's number, which the book takes",
    )
    parser.add_argument(
        "--freeze-date",
        default=datetime.date.today().isoformat(),
        help="the first day the book is on paper, ISO; today when omitted",
    )
    arguments = parser.parse_args()
    book_directory = PAPER_TRADING_DIRECTORY / f"Paper_Trading_{arguments.number}"
    rule_path = book_directory / f"paper_trading_{arguments.number}.py"
    freeze_path = book_directory / "FREEZE.json"

    if freeze_path.is_file():
        frozen_message = f"{freeze_path} exists: a frozen book is never frozen again"

        raise SystemExit(frozen_message)

    if not rule_path.is_file():
        missing_message = f"{rule_path} is missing: write it from the experiment, then commit"

        raise SystemExit(missing_message)

    changes = _git(
        "status",
        "--porcelain",
        "--untracked-files=no",
    )

    if changes.strip() != "":
        dirty_message = "the working tree has changes to tracked files: commit them before a freeze"

        raise SystemExit(dirty_message)

    sign_off = _read_sign_off(
        arguments.number,
        _git_bytes(f"HEAD:{BITACORA_PATH}").decode("utf-8"),
    )
    commit = _git(
        "rev-parse",
        "HEAD",
    ).strip()
    hashes = {}

    for relative in FROZEN_FILES:
        committed = _git_bytes(f"HEAD:{relative}")
        hashes[relative] = _write(
            book_directory / relative,
            committed,
        )

    for generated_relative in GENERATED_FILES:
        generated = (REPOSITORY_ROOT / generated_relative).read_bytes()
        hashes[generated_relative] = _write(
            book_directory / generated_relative,
            generated,
        )

    libraries = {
        name: importlib.metadata.version(name)
        for name in LIBRARIES
    }
    shared_bytes = (REPOSITORY_ROOT / SHARED_CALCULATIONS).read_bytes()
    shared_hash = hashlib.sha256(shared_bytes)
    freeze = {
        "book": arguments.number,
        "commit": commit,
        "freeze_date": arguments.freeze_date,
        "files": hashes,
        "libraries": libraries,
        "sign_off": sign_off,
        "shared_inputs": {
            SHARED_CALCULATIONS: shared_hash.hexdigest(),
            "kaxanuk-data-curator": libraries["kaxanuk-data-curator"],
        },
    }
    freeze_text = json.dumps(
        freeze,
        indent=1,
        sort_keys=True,
    )
    freeze_path.write_text(
        f"{freeze_text}\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"froze Paper_Trading_{arguments.number} at {commit[:12]}")
    print(f"on paper from {arguments.freeze_date}")
    print(f"signed off by {sign_off['person']} on {sign_off['date']}, as {sign_off['outcome']}")
    relative_book = book_directory.relative_to(REPOSITORY_ROOT)
    print(f"commit it: git add {relative_book.as_posix()}")
    generated_names = ", ".join(GENERATED_FILES)
    print(f"{generated_names} stays on this machine, out of git: back it up with the record")

    return 0


def _git(
    *arguments: str,
) -> str:
    """
    Run git in the repository and return what it printed.
    """
    completed = subprocess.run(
        [
            "git",
            *arguments,
        ],
        capture_output=True,
        check=True,
        cwd=REPOSITORY_ROOT,
        text=True,
    )

    return completed.stdout


def _git_bytes(
    revision_path: str,
) -> bytes:
    """
    A file's bytes as the commit holds them, never as the working tree does.
    """
    completed = subprocess.run(
        [
            "git",
            "show",
            revision_path,
        ],
        capture_output=True,
        check=True,
        cwd=REPOSITORY_ROOT,
    )

    return completed.stdout


def _read_sign_off(
    number: int,
    bitacora: str,
) -> dict[str, str]:
    """
    The sign-off of book N, read from its sections of the committed `BITACORA.md`, or a refusal.

    A section of book N is one headed `### Paper_Trading_N`, up to the next heading of its level or
    above; a folder retired and later reused keeps its earlier section, never edited, so there may
    be several.  Exactly one sign-off line must name a person, a date and one of the two outcomes
    that put a book on paper, its lines read as one, however the paragraph wraps; a book on
    probation must also carry, in that section, the terms it is read against at its review.
    """
    sections = _sections_of_book(
        number,
        bitacora,
    )
    signed = [
        (match, section)
        for section in sections
        for match in SIGN_OFF_PATTERN.finditer(section)
        if match.group("outcome").strip() in SIGN_OFF_OUTCOMES
    ]

    if len(signed) != 1:
        sign_off_message = " ".join([
            f"{BITACORA_PATH} holds no single sign-off for Paper_Trading_{number}, as graduating",
            "or as sound and regime-dependent, on paper on probation: a person signs first",
        ])

        raise SystemExit(sign_off_message)

    match, section = signed[0]
    sign_off = {
        "person": match.group("person").strip(),
        "date": match.group("date"),
        "outcome": match.group("outcome").strip(),
    }
    missing = [
        term
        for term in PROBATION_TERMS
        if term not in section
    ]

    if sign_off["outcome"] != SIGN_OFF_OUTCOMES[0] and len(missing) > 0:
        missing_terms = ", ".join(missing)
        terms_message = f"Paper_Trading_{number} is on probation and lacks {missing_terms}"

        raise SystemExit(terms_message)

    return sign_off


def _sections_of_book(
    number: int,
    bitacora: str,
) -> list[str]:
    """
    Every section of `BITACORA.md` headed for book N, each with its lines joined by single spaces.
    """
    heading = re.compile(rf"^### Paper_Trading_{number}(?!\d)")
    lines = bitacora.splitlines()
    boundaries = [
        position
        for position, line in enumerate(lines)
        if line.startswith("## ") or line.startswith("### ")
    ]
    ends = [
        *boundaries[1:],
        len(lines),
    ]
    sections = []

    for start, end in zip(
        boundaries,
        ends,
        strict=True,
    ):
        if not heading.match(lines[start]):
            continue

        joined = " ".join(lines[start:end])
        words = joined.split()
        sections.append(" ".join(words))

    return sections


def _write(
    path: "pathlib.Path",
    content: bytes,
) -> str:
    """
    Write one frozen file and return the hash of what was written.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_bytes(content)
    digest = hashlib.sha256(content)

    return digest.hexdigest()


if __name__ == "__main__":
    sys.exit(main())

# --- example: end ---
