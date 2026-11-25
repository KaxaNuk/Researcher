"""
Install every library this repository runs on -- step 2 of 8, once the keys are in `Config/.env`.

In plain words: one command brings the environment up to date.  The public libraries -- the Data
Curator, marimo and the rest of `pyproject.toml` -- come from `uv sync`.  The licensed KaxaNuk
libraries -- the Backtest Engine, Attribution Analysis and Portfolio Construction -- are not on
public PyPI: each installs from KaxaNuk's licensed index, with its licence key in the address.
This script reads each key and each index's host from `Config/.env` by name, asks `uv` to install
the library into `.venv/`, and never prints, logs or stores a key or an address that holds one:
whatever `uv` answers is shown with every key replaced by `***`.  Last, it names the build of every
KaxaNuk library now installed.

Run it from the repository's root:

    uv run python Config/install_libraries.py
    uv run python Config/install_libraries.py --upgrade
    uv run python Config/install_libraries.py kaxanuk-backtest-engine

What it reads from `Config/.env`, per licensed library -- one missing either line is skipped and
named, never guessed:

    kaxanuk-backtest-engine          KNBE_API_KEY_KAXANUK   KNBE_INDEX_HOST
    kaxanuk-attribution_analysis     KNAA_API_KEY_KAXANUK   KNAA_INDEX_HOST
    kaxanuk-portfolio-construction   KNPC_API_KEY_KAXANUK   KNPC_INDEX_HOST
        with its `solver` and `clustering` extras, which every sizing method needs between them

The host is the part of the address in the licence's welcome e-mail after the `@` and before
`/simple/`; a whole address pasted there works too, its scheme, credentials and `/simple/` dropped.
A host is not a secret, but it lives beside the key so the repository names no index.

`uv sync` runs with `--inexact` and the `notebook` group: a bare `uv sync` is exact and removes
every package the lockfile does not name, the licensed libraries among them.  Never add a licensed
library to `pyproject.toml`; this script is how each machine gets them.  Naming libraries on the
command line installs only those, and skips the sync.

It produces the libraries in `.venv/`, and one line per library: installed, skipped and why, or
failed with `uv`'s answer, keys hidden; then each KaxaNuk library's installed build.

It prevents a key typed into a shell's history, pasted into a chat, or left in a dependency file,
and a licensed library a bare `uv sync` removed without anyone noticing.
"""

import argparse
import contextlib
import dataclasses
import importlib.metadata
import pathlib
import subprocess
import sys

__all__ = [
    'LICENSED_LIBRARIES',
    'LicensedLibrary',
    'index_url',
    'main',
    'read_environment',
]


@dataclasses.dataclass(frozen=True)
class LicensedLibrary:
    """
    One licensed library: its distribution's name, the extras it installs with, and the two
    `Config/.env` lines it installs from.
    """

    distribution: str
    extras: str
    host_variable: str
    key_variable: str


ENVIRONMENT_PATH = pathlib.Path(__file__).parent / '.env'
HIDDEN = '***'
# Every KaxaNuk library a strategy may run on, public or licensed, whose build is reported last.
KAXANUK_DISTRIBUTIONS = (
    'kaxanuk-attribution_analysis',
    'kaxanuk-backtest-engine',
    'kaxanuk-data-curator',
    'kaxanuk-license-client',
    'kaxanuk-portfolio-construction',
)
LICENSED_LIBRARIES = (
    LicensedLibrary(
        distribution='kaxanuk-backtest-engine',
        extras='',
        host_variable='KNBE_INDEX_HOST',
        key_variable='KNBE_API_KEY_KAXANUK',
    ),
    LicensedLibrary(
        distribution='kaxanuk-attribution_analysis',
        extras='',
        host_variable='KNAA_INDEX_HOST',
        key_variable='KNAA_API_KEY_KAXANUK',
    ),
    LicensedLibrary(
        distribution='kaxanuk-portfolio-construction',
        # The solver serves the constrained mean-variance, CVaR and CDaR methods, and clustering
        # HRP, HERC and NCO: without them those methods fail when they are built or allocate.
        extras='[solver,clustering]',
        host_variable='KNPC_INDEX_HOST',
        key_variable='KNPC_API_KEY_KAXANUK',
    ),
)
# The quotes a `.env` value may be wrapped in, dropped when it is read.
QUOTES = "\"'"
REPOSITORY_ROOT = pathlib.Path(__file__).parent.parent
# How much of `uv`'s answer a failure shows, from its end, keys hidden.
SHOWN_ANSWER_LINES = 15
SYNC_COMMAND = (
    'uv',
    'sync',
    '--group',
    'notebook',
    '--inexact',
)


def index_url(
    host: str,
    key: str,
) -> str:
    """
    The licensed index's address for one key: `https://license:<key>@<host>/simple/`.

    A whole address pasted as the host is cut back to the host first.
    """
    without_scheme = host.strip().split('://')[-1]
    without_credentials = without_scheme.split('@')[-1]
    bare_host = without_credentials.split('/simple')[0].rstrip('/')
    address = f'https://license:{key}@{bare_host}/simple/'

    return address


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Sync the public libraries, install each licensed one `Config/.env` allows; 0 when none failed.
    """
    for console_stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(Exception):
            console_stream.reconfigure(
                encoding='utf-8',
                errors='replace',
            )

    parser = argparse.ArgumentParser(description='Install every library this repository runs on.')
    parser.add_argument(
        'distributions',
        nargs='*',
        help='the licensed libraries to install, by distribution name; everything when omitted',
    )
    parser.add_argument(
        '--upgrade',
        action='store_true',
        help='install the newest build of each licensed library, even where one is installed',
    )
    parsed = parser.parse_args(arguments)

    if not ENVIRONMENT_PATH.is_file():
        print(f'{ENVIRONMENT_PATH} is missing: copy Config/.env.template to it and fill it in')

        return 1

    environment = read_environment(ENVIRONMENT_PATH)
    known = {
        library.distribution
        for library in LICENSED_LIBRARIES
    }
    unknown = sorted(set(parsed.distributions) - known)

    if unknown:
        unknown_names = ', '.join(unknown)
        known_names = ', '.join(sorted(known))
        print(f'Not a licensed KaxaNuk library: {unknown_names}; known: {known_names}')

        return 2

    synced = _sync() if not parsed.distributions else 'skipped'

    chosen = [
        library
        for library in LICENSED_LIBRARIES
        if not parsed.distributions
        or library.distribution in parsed.distributions
    ]
    outcomes = [
        _install(
            library,
            environment,
            parsed.upgrade,
        )
        for library in chosen
    ]
    _report_builds()
    failed = [
        outcome
        for outcome in [synced, *outcomes]
        if outcome == 'failed'
    ]

    if failed:

        return 1

    return 0


def read_environment(
    path: pathlib.Path,
) -> dict[str, str]:
    """
    The `NAME=value` lines of a `.env` file, quotes dropped; comments and blank lines skipped.
    """
    environment: dict[str, str] = {}
    lines = path.read_text(encoding='utf-8').splitlines()

    for line in lines:
        stripped = line.strip()

        if stripped == '' or stripped.startswith('#') or '=' not in stripped:
            continue

        name, value = stripped.split(
            '=',
            1,
        )
        unquoted = value.strip().strip(QUOTES)
        environment[name.strip()] = unquoted

    return environment


def _hidden(
    text: str,
    secrets: list[str],
) -> str:
    """
    The text with every secret in it replaced by `HIDDEN`.
    """
    present = [
        secret
        for secret in secrets
        if secret
    ]
    pieces = [text]

    for secret in present:
        pieces.append(
            pieces[-1].replace(
                secret,
                HIDDEN,
            )
        )

    return pieces[-1]


def _install(
    library: LicensedLibrary,
    environment: dict[str, str],
    upgrade: bool,
) -> str:
    """
    Install one licensed library with `uv pip`, into the interpreter running this script.

    The outcome is `installed`, `skipped` or `failed`, and is said in one line.
    """
    key = environment.get(library.key_variable, '')
    host = environment.get(library.host_variable, '')
    missing = [
        variable
        for variable, value in ((library.key_variable, key), (library.host_variable, host))
        if value == ''
    ]

    if missing:
        missing_names = ' and '.join(missing)
        print(f'skipped    {library.distribution}: fill {missing_names} in Config/.env')

        return 'skipped'

    address = index_url(
        host,
        key,
    )
    command = [
        'uv',
        'pip',
        'install',
        '--python',
        sys.executable,
        '--extra-index-url',
        address,
        f'{library.distribution}{library.extras}',
    ]

    if upgrade:
        command.append('--upgrade')

    completed = subprocess.run(
        command,
        capture_output=True,
        check=False,
        encoding='utf-8',
        errors='replace',
    )

    if completed.returncode != 0:
        _show_answer(
            f'failed     {library.distribution}; uv answered:',
            completed,
            [address, key],
        )

        return 'failed'

    print(f'installed  {library.distribution}')

    return 'installed'


def _report_builds() -> None:
    """
    Name the build of each KaxaNuk library installed in this environment, or that it is absent.
    """
    print('KaxaNuk libraries in this environment:')

    for distribution in KAXANUK_DISTRIBUTIONS:
        try:
            build = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            build = 'not installed'

        print(f'    {distribution:34} {build}')


def _show_answer(
    heading: str,
    completed: subprocess.CompletedProcess,
    secrets: list[str],
) -> None:
    """
    Print a heading and the end of what a command answered, every secret hidden.
    """
    answer = _hidden(
        completed.stdout + completed.stderr,
        secrets,
    )
    answer_lines = answer.strip().splitlines()
    print(heading)

    for answer_line in answer_lines[-SHOWN_ANSWER_LINES:]:
        print(f'    {answer_line}')


def _sync() -> str:
    """
    Sync the public libraries of `pyproject.toml`, keeping what was installed by hand.

    The outcome is `installed` or `failed`, and is said in one line.
    """
    completed = subprocess.run(
        SYNC_COMMAND,
        capture_output=True,
        check=False,
        cwd=REPOSITORY_ROOT,
        encoding='utf-8',
        errors='replace',
    )

    if completed.returncode != 0:
        _show_answer(
            'failed     the public libraries (uv sync); uv answered:',
            completed,
            [],
        )

        return 'failed'

    print('installed  the public libraries of pyproject.toml (uv sync --group notebook --inexact)')

    return 'installed'


if __name__ == '__main__':
    sys.exit(main())
