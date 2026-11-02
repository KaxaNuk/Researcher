"""
A researcher's home at a glance: what slipped since last week, each line with the word that fixes
it. The brief writes it under *Health*, on *Week*'s day.

    uv run --no-project python health.py                  the home in this folder
    uv run --no-project python health.py "D:/Research/Arya"

What it checks, by running the package's own scripts from the skills beside this one
    unread      `read`'s unread_sources.py: sources no note has read yet         say `read`
    library     `read`'s check_library.py: broken links, the index, frontmatter    say `audit`
    security    `security`'s security_check.py: things to fix, things to look at   say `security`
    copy        git: saved versions not yet in the home's copy on GitHub, when it
                has one; never a fetch, so it counts what this computer knows        say `backup`

Each line gives a count and the word to say, never a file's name, a path inside the home or a
value: a brief is read on this computer, and a health line is safe to show anyone. A check that
cannot run — its script missing, git missing — says so in its line and is not a finding.

Exit codes: 0 nothing to do · 1 usage: not a home · 2 at least one line to act on.
It needs only the standard library and git, and writes nothing.
"""
import argparse
import dataclasses
import pathlib
import re
import subprocess
import sys

__all__ = [
    'CheckLine',
    'home_health',
    'main',
]

SKILLS_DIRECTORY = pathlib.Path(__file__).resolve().parents[2]
CHECK_LIBRARY = SKILLS_DIRECTORY / 'read' / 'scripts' / 'check_library.py'
SECURITY_CHECK = SKILLS_DIRECTORY / 'security' / 'scripts' / 'security_check.py'
UNREAD_SOURCES = SKILLS_DIRECTORY / 'read' / 'scripts' / 'unread_sources.py'

FINDINGS_LINE = re.compile(r'^(\d+) findings?$')
SECURITY_HEADING = re.compile(r'^(Fix before you share|Look at) \((\d+)\):$')
UNREAD_COUNT = re.compile(r'(\d+) unread')

SCRIPT_TIMEOUT_SECONDS = 600


@dataclasses.dataclass(frozen=True)
class CheckLine:
    """
    One line of the health block: what was checked, what it found, and whether to act on it.
    """
    act: bool
    text: str


def home_health(
    home: pathlib.Path,
) -> list[CheckLine]:
    """
    Every check, in the order the brief shows them.
    """
    lines = [
        _unread_line(home),
        _library_line(home),
        _security_line(home),
        _copy_line(home),
    ]

    return lines


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, check the home, and print one line per check.
    """
    _configure_console()
    parsed = _build_parser().parse_args(arguments)
    home = pathlib.Path(parsed.folder).resolve()

    if not (home / 'RESEARCHER.md').is_file():
        problem = f'not a home: {parsed.folder} holds no RESEARCHER.md'
        print(
            problem,
            file=sys.stderr,
        )

        return 1

    lines = home_health(home)

    for line in lines:
        print(line.text)
    to_act = [
        line
        for line in lines
        if line.act
    ]
    exit_code = 2 if to_act else 0

    return exit_code


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: the home's folder.
    """
    parser = argparse.ArgumentParser(
        prog='health.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'folder',
        nargs='?',
        default='.',
        help="the researcher's home (default: this folder)",
    )

    return parser


def _configure_console() -> None:
    """
    UTF-8 on the console, as under `python -I`, which ignores PYTHONIOENCODING.
    """
    for console_stream in (
        sys.stdout,
        sys.stderr,
    ):
        try:
            console_stream.reconfigure(
                encoding='utf-8',
                errors='replace',
            )
        except (AttributeError, ValueError):
            pass


def _copy_line(
    home: pathlib.Path,
) -> CheckLine:
    """
    Saved versions not yet in the home's copy on GitHub, as this computer last knew that copy.
    """
    upstream = _git(
        home,
        [
            'rev-parse',
            '--abbrev-ref',
            '@{upstream}',
        ],
    )

    if upstream is None:
        no_copy = CheckLine(
            act=False,
            text='Copy: none on GitHub yet.',
        )

        return no_copy

    ahead = _git(
        home,
        [
            'rev-list',
            '--count',
            '@{upstream}..HEAD',
        ],
    )

    if ahead is None or not ahead.isdigit():
        unknown = CheckLine(
            act=False,
            text='Copy: could not be checked.',
        )

        return unknown

    ahead_count = int(ahead)

    if ahead_count == 0:
        in_step = CheckLine(
            act=False,
            text='Copy: every saved version is on GitHub.',
        )

        return in_step

    behind = CheckLine(
        act=True,
        text=f'Copy: {_counted(ahead_count, "saved version")} not yet on GitHub — say `backup`.',
    )

    return behind


def _counted(
    count: int,
    noun: str,
) -> str:
    """
    A count and its noun, in the plural when it is not one.
    """
    plural = '' if count == 1 else 's'
    counted = f'{count} {noun}{plural}'

    return counted


def _git(
    home: pathlib.Path,
    arguments: list[str],
) -> str | None:
    """
    What a git command prints in the home, stripped, or None when git is missing or the command
    fails.
    """
    try:
        completed = subprocess.run(
            [
                'git',
                '-C',
                str(home),
                *arguments,
            ],
            capture_output=True,
            check=False,
            encoding='utf-8',
            errors='replace',
            timeout=SCRIPT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if completed.returncode != 0:
        return None

    output = completed.stdout.strip()

    return output


def _library_line(
    home: pathlib.Path,
) -> CheckLine:
    """
    How many findings check_library.py makes in the library.
    """
    output = _run_script(
        CHECK_LIBRARY,
        home,
    )

    if output is None:
        missing = CheckLine(
            act=False,
            text='Library: could not be checked.',
        )

        return missing

    matches = [
        FINDINGS_LINE.match(line.strip())
        for line in output.splitlines()
    ]
    counts = [
        int(match.group(1))
        for match in matches
        if match
    ]

    if not counts:
        unknown = CheckLine(
            act=False,
            text='Library: could not be checked.',
        )

        return unknown

    finding_count = counts[-1]

    if finding_count == 0:
        clean = CheckLine(
            act=False,
            text='Library: in order.',
        )

        return clean

    findings = CheckLine(
        act=True,
        text=f'Library: {_counted(finding_count, "thing")} to put in order — say `audit`.',
    )

    return findings


def _run_script(
    script: pathlib.Path,
    home: pathlib.Path,
) -> str | None:
    """
    What one of the package's scripts prints on the home, or None when it is not beside this skill
    or does not finish. Its exit code is its own: a finding exits 2, and the output is read either
    way.
    """
    if not script.is_file():
        return None

    try:
        completed = subprocess.run(
            [
                sys.executable,
                '-I',
                str(script),
                str(home),
            ],
            capture_output=True,
            check=False,
            encoding='utf-8',
            errors='replace',
            timeout=SCRIPT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if completed.returncode == 1:
        return None

    output = completed.stdout

    return output


def _security_line(
    home: pathlib.Path,
) -> CheckLine:
    """
    How many things security_check.py finds to fix, and to look at: counts only, never a value.
    """
    output = _run_script(
        SECURITY_CHECK,
        home,
    )

    if output is None:
        missing = CheckLine(
            act=False,
            text='Security: could not be checked.',
        )

        return missing

    matches = [
        SECURITY_HEADING.match(line.strip())
        for line in output.splitlines()
    ]
    counts = {}

    for match in matches:
        if match is None:
            continue

        heading = match.group(1)
        counts[heading] = int(match.group(2))
    fix_count = counts.get('Fix before you share', 0)
    look_count = counts.get('Look at', 0)

    if fix_count == 0 and look_count == 0:
        clean = CheckLine(
            act=False,
            text='Security: nothing to fix.',
        )

        return clean

    parts = [
        f'{_counted(fix_count, "thing")} to fix' if fix_count else '',
        f'{_counted(look_count, "thing")} to look at' if look_count else '',
    ]
    found = ', '.join(
        part
        for part in parts
        if part
    )
    findings = CheckLine(
        act=True,
        text=f'Security: {found} — say `security`.',
    )

    return findings


def _unread_line(
    home: pathlib.Path,
) -> CheckLine:
    """
    How many sources in Sources/ no note has read.
    """
    output = _run_script(
        UNREAD_SOURCES,
        home,
    )
    output_lines = output.splitlines() if output else []
    first_line = output_lines[0] if output_lines else ''
    match = UNREAD_COUNT.search(first_line)

    if match is None:
        unknown = CheckLine(
            act=False,
            text='Reading: could not be checked.',
        )

        return unknown

    unread_count = int(match.group(1))

    if unread_count == 0:
        clean = CheckLine(
            act=False,
            text='Reading: every source has its note.',
        )

        return clean

    unread = CheckLine(
        act=True,
        text=f'Reading: {_counted(unread_count, "source")} not read yet — say `read`.',
    )

    return unread


if __name__ == '__main__':
    sys.exit(main())
