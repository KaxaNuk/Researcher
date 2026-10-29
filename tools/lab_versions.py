"""
Whether the package's record of the KaxaNuk Investment Lab is current: each library's newest release,
read from the first dated entry of its CHANGELOG.md on GitHub, against the *Latest* column of
`.apm/skills/next/references/investment-lab.md` and its skill's `library_version`.

    uv run --no-project python -I tools/lab_versions.py

It reads each changelog with `gh api`, as the owner's GitHub account can, and never the library's
code. It writes nothing. AGENTS.md's *When a Lab library or an Analytics Factory file changes* says
what to do with a gap it finds: record the new build, add a *Changed in* paragraph from the
changelog, and check it by a run before `library_version` moves.

What it reports, one line per library
    behind      the newest release on GitHub is newer than *Latest*: the package is out of date
    ahead       *Latest* names a build the changelog has no entry for
    coming      *Latest* says *coming* while the changelog has a release: the owner says when it ships
    skill       the skill's `library_version` is older than *Latest*: a run is due, as AGENTS.md says
    ok          *Latest* is the newest release, and the skill was checked on it

Exit codes: 0 no library is behind · 1 one is behind · 2 a changelog or the record could not be read.
"""
import dataclasses
import pathlib
import re
import subprocess
import sys

TOOLS = pathlib.Path(__file__).resolve().parent

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check  # noqa: E402 - found beside this file once its folder is on the path, `python -I` too.

__all__ = [
    'Library',
    'Reading',
    'main',
    'newest_release',
    'reading',
    'recorded_latest',
    'skill_version',
]

# The record, and each library: its name in the record's table, its repository under KaxaNuk on
# GitHub, and its skill, when it has one.
INVESTMENT_LAB = check.REPOSITORY / '.apm' / 'skills' / 'next' / 'references' / 'investment-lab.md'
SKILLS = check.REPOSITORY / '.apm' / 'skills'
# A changelog's dated release, `## [X.Y.Z] - YYYY-MM-DD`; `[Unreleased]` and undated entries are not.
RELEASE_HEADING = re.compile(r'^## \[(?P<version>\d+\.\d+\.\d+)\] - (?P<date>\d{4}-\d{2}-\d{2})\s*$', re.M)
# A skill's frontmatter line naming the build its traps were checked on.
SKILL_VERSION = re.compile(r'^\s*library_version:\s*(?P<version>\d+\.\d+\.\d+)\s*$', re.M)
# The *Latest* cell of the record's table: a version, with its date, or *coming*.
LATEST_VERSION = re.compile(r'(?P<version>\d+\.\d+\.\d+)')
COMING = 'coming'


@dataclasses.dataclass(frozen=True)
class Library:
    """
    One of the Lab's libraries: its name in the record, its repository and its skill's folder.
    """
    name: str
    repository: str
    skill: str


@dataclasses.dataclass(frozen=True)
class Reading:
    """
    What was read for one library, and how its record stands against it.
    """
    library: Library
    newest: str
    recorded: str
    skill_version: str
    state: str

    @property
    def line(self) -> str:
        """
        The report's line for the library.
        """
        skill_part = f'skill checked on {self.skill_version}' if self.skill_version else 'no skill'
        line = ' '.join([
            f'{self.state:<8}',
            f'{self.library.name:<24}',
            f'GitHub {self.newest or "none":<8}',
            f'recorded {self.recorded:<8}',
            skill_part,
        ])

        return line


LIBRARIES = [
    Library(
        name='Data Curator',
        repository='Data-Curator',
        skill='data-curator-custom-calculations',
    ),
    Library(
        name='Data Refinery',
        repository='Data-Refinery',
        skill='',
    ),
    Library(
        name='Data Analyzer',
        repository='Data-Analyzer',
        skill='',
    ),
    Library(
        name='Portfolio Construction',
        repository='Portfolio-Construction',
        skill='portfolio-construction-runs',
    ),
    Library(
        name='Backtest Engine',
        repository='Backtest-Engine',
        skill='backtest-engine-runs',
    ),
    Library(
        name='Attribution Analysis',
        repository='Attribution-Analysis',
        skill='attribution-analysis-runs',
    ),
]


def main() -> int:
    """
    Read every library's changelog and the package's record, print one line each, and say whether
    any library is behind.
    """
    check.configure_console()

    try:
        record = INVESTMENT_LAB.read_text(encoding='utf-8')
    except OSError as exception:
        print(f'{INVESTMENT_LAB} could not be read: {exception}')

        return 2

    readings = []
    unread = []

    for library in LIBRARIES:
        changelog = _changelog(library.repository)

        if changelog is None:
            unread.append(library.name)

            continue

        skill_text = _skill_text(library.skill)
        library_reading = reading(
            library,
            changelog,
            record,
            skill_text,
        )
        readings.append(library_reading)
        print(library_reading.line)

    for name in unread:
        print(f'unread   {name}: its changelog could not be read with gh api; is gh signed in?')

    behind = [
        library_reading.library.name
        for library_reading
        in readings
        if library_reading.state == 'behind'
    ]

    if behind:
        names = ', '.join(behind)
        print(f'Behind: {names}. AGENTS.md, *When a Lab library or an Analytics Factory file changes*, says what to do.')

        return 1

    if unread:

        return 2

    print('No library is behind its record.')

    return 0


def newest_release(
    changelog: str,
) -> str:
    """
    The version of a changelog's first dated release, or an empty string when it has none.
    """
    heading = RELEASE_HEADING.search(changelog)
    version = '' if heading is None else heading.group('version')

    return version


def reading(
    library: Library,
    changelog: str,
    record: str,
    skill_text: str,
) -> Reading:
    """
    How the record of one library stands against its changelog and its skill.
    """
    newest = newest_release(changelog)
    recorded = recorded_latest(
        record,
        library.name,
    )
    checked_on = skill_version(skill_text)
    released_versions = {
        heading.group('version')
        for heading
        in RELEASE_HEADING.finditer(changelog)
    }

    if recorded == COMING:
        state = COMING if newest else 'ok'
    elif newest and check.version_key(newest) > check.version_key(recorded):
        state = 'behind'
    elif recorded not in released_versions:
        state = 'ahead'
    elif checked_on and check.version_key(checked_on) < check.version_key(recorded):
        state = 'skill'
    else:
        state = 'ok'

    library_reading = Reading(
        library=library,
        newest=newest,
        recorded=recorded,
        skill_version=checked_on,
        state=state,
    )

    return library_reading


def recorded_latest(
    record: str,
    name: str,
) -> str:
    """
    The *Latest* the record's table gives a library: its version, `coming`, or an empty string when
    the table has no row for it.
    """
    rows = [
        line
        for line
        in record.splitlines()
        if line.startswith(f'| **{name}** |')
    ]

    if not rows:

        return ''

    cells = rows[0].split('|')
    latest_cell = cells[4]
    version_match = LATEST_VERSION.search(latest_cell)

    if version_match is not None:

        return version_match.group('version')

    latest = COMING if COMING in latest_cell else ''

    return latest


def skill_version(
    skill_text: str,
) -> str:
    """
    The `library_version` a skill's frontmatter names, or an empty string.
    """
    version_match = SKILL_VERSION.search(skill_text)
    version = '' if version_match is None else version_match.group('version')

    return version


def _changelog(
    repository: str,
) -> str | None:
    """
    A library's CHANGELOG.md from its default branch on GitHub, or None when it cannot be read.
    """
    try:
        completed = subprocess.run(
            [
                'gh',
                'api',
                f'repos/KaxaNuk/{repository}/contents/CHANGELOG.md',
                '-H',
                'Accept: application/vnd.github.raw',
            ],
            capture_output=True,
            check=False,
            encoding='utf-8',
            errors='replace',
        )
    except OSError:

        return None

    changelog = completed.stdout if completed.returncode == 0 else None

    return changelog


def _skill_text(
    skill: str,
) -> str:
    """
    A skill's SKILL.md, or an empty string for a library with no skill.
    """
    if not skill:

        return ''

    text = (SKILLS / skill / 'SKILL.md').read_text(encoding='utf-8')

    return text


if __name__ == '__main__':
    sys.exit(main())
