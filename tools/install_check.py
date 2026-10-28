"""
The install a release is tried with, in a throwaway home: what CONTRIBUTING.md asks before every
release, but the walk with a researcher, which needs a person to answer the interview.

    uv run --no-project python -I tools/install_check.py
    uv run --no-project python -I tools/install_check.py --github KaxaNuk/Researcher#dev
    uv run --no-project python -I tools/install_check.py --github KaxaNuk/Researcher --migrate-from KaxaNuk/KaxaNuk-Researcher#v1.23.2

What it installs: an archive of what a commit would hold, uncommitted changes to tracked files
included (`git stash create`, else HEAD, with LF endings), or, with --github, the package from
GitHub. With --migrate-from, the user-scope install first installs that older package for Claude,
then moves to the new one as `update` does: the old one uninstalled, the new one installed.

What it checks, each step printing `ok` or `FAIL`:
    project install   a project-scope install for Claude deploys every skill, command, rule and
                      agent the package holds, with no warning
    user install      a user-scope install in a new home, Claude, then Codex put on APM's list by
                      `user_targets.py add`, then Codex, then `apm update -g`: both assistants hold
                      what the package holds, with no warning but APM's notices for a user scope
    scaffold          the deployed `scaffold.py` makes a strategy, a researcher's home and the worked
                      example from that install, each a git repository with its first commit

--show also prints where APM put the package and what its lock file records, for the user scope.

Everything happens in a folder it makes and removes at the end: kn-<random>, in the user's own
folder on Windows, where the system's temporary folder is too deep for the paths APM stages, and in
that temporary folder elsewhere. HOME and USERPROFILE point inside it, so no APM or git setting of
the real home is read or written. It needs uv and git.

Exit codes: 0 every step passed · 1 a step failed.
"""
import argparse
import dataclasses
import io
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile

TOOLS = pathlib.Path(__file__).resolve().parent

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check  # noqa: E402 - found beside this file once its folder is on the path, `python -I` too.

__all__ = [
    'PackageParts',
    'check_project_install',
    'check_scaffold',
    'check_user_install',
    'main',
]

APM = [
    '--from',
    'apm-cli==0.33.0',
    'apm',
]
ARCHIVE_PREFIX = 'KaxaNuk-Researcher'
PACKAGE_NAME = 'name: kaxanuk-researcher'
# The notices APM prints that are no warning about the package: a newer APM, a package from GitHub
# installed without a tag, as SETUP.md installs it, and, for a user scope, which assistants take
# every kind of file, and the Codex agent's lossy compilation.
PROJECT_NOTICES = (
    'A new version of APM is available',
    'dependency unpinned',
)
USER_NOTICES = (
    *PROJECT_NOTICES,
    'User-scope primitives are fully supported by',
    'lossy agent compilation warning',
)
SCAFFOLDED = (
    'strategy',
    'researcher',
    'example',
)
# Where the scratch folder is made. APM stages a package's files 68 characters below apm_modules/,
# and the package's deepest file is 134 characters long: on Windows without long paths, an
# apm_modules/ folder deeper than 57 characters fails with WinError 3. The system's temporary
# folder is too deep for that, the user's own folder is not; elsewhere, the temporary folder serves.
SCRATCH_PARENT = str(pathlib.Path.home()) if sys.platform == 'win32' else None


@dataclasses.dataclass(frozen=True)
class PackageParts:
    """
    How many of each kind of file the package holds, or an assistant's folder holds once deployed.
    """
    agents: int
    commands: int
    rules: int
    skills: int


def check_project_install(
    scratch: pathlib.Path,
    source: str,
    uvx: str,
) -> check.CheckResult:
    """
    A project-scope install for Claude, as CONTRIBUTING.md shows it: every skill, command, rule and
    agent the package holds, deployed, and no warning.
    """
    home = scratch / 'project-home'
    project = scratch / 'project'
    home.mkdir()
    project.mkdir()
    completed = _apm(
        uvx,
        [
            'install',
            source,
            '--target',
            'claude',
        ],
        project,
        home,
    )

    if completed.returncode != 0:
        return _failed_result(
            'project install',
            completed,
        )

    package = _installed_package(project / 'apm_modules')

    if package is None:
        return _missing_package_result('project install')

    problems = [
        *_warnings(
            completed,
            PROJECT_NOTICES,
        ),
        *_part_problems(
            'Claude',
            _deployed_parts(project / '.claude'),
            _package_parts(package),
        ),
    ]
    result = check.CheckResult(
        name='project install',
        problems=problems,
    )

    return result


def check_scaffold(
    scratch: pathlib.Path,
) -> check.CheckResult:
    """
    The scaffold.py the user install deployed makes a strategy, a researcher's home and the worked
    example, each a git repository with its first commit: it finds the installed package.
    """
    home = scratch / 'home'
    script = home / '.claude' / 'skills' / 'init-strategy' / 'scripts' / 'scaffold.py'

    if not script.is_file():
        missing = check.CheckResult(
            name='scaffold',
            problems=['no scaffold.py deployed: the user install did not deploy init-strategy'],
        )

        return missing

    problems = [
        problem
        for kind in SCAFFOLDED
        for problem in _scaffold_problems(
            script,
            kind,
            scratch / f'new-{kind}',
        )
    ]
    result = check.CheckResult(
        name='scaffold',
        problems=problems,
    )

    return result


def check_user_install(
    scratch: pathlib.Path,
    source: str,
    uvx: str,
    migrate_from: str,
) -> check.CheckResult:
    """
    A user-scope install in a new home: the package for Claude, Codex put on APM's list by
    `user_targets.py add`, the package for Codex, then an update; both assistants hold what the
    package holds. With an older package to migrate from, that one is installed for both first, then
    moved from as `update` moves it: uninstalled, and the new one installed for every assistant
    on the list.
    """
    home = scratch / 'home'
    home.mkdir()
    _git_identity(home)
    first_source = migrate_from or source
    first = _apm_steps(
        uvx,
        [
            [
                'install',
                '-g',
                first_source,
                '--target',
                'claude',
            ],
        ],
        home,
    )

    if first.problems:
        return first

    first_package = _installed_package(home / '.apm' / 'apm_modules')

    if first_package is None:
        return _missing_package_result('user install')

    added = _add_target(
        home,
        first_package,
        'codex',
    )

    if added.returncode != 0:
        return _failed_result(
            'user install',
            added,
        )

    old_package = migrate_from.split('#')[0]
    moves = [
        [
            'uninstall',
            '-g',
            old_package,
        ],
        [
            'install',
            '-g',
            source,
        ],
    ] if migrate_from else []
    second = _apm_steps(
        uvx,
        [
            [
                'install',
                '-g',
                first_source,
                '--target',
                'codex',
            ],
            *moves,
            [
                'update',
                '-g',
                '--yes',
            ],
        ],
        home,
    )
    package = _installed_package(home / '.apm' / 'apm_modules') or first_package
    expected = _package_parts(package)
    codex_parts = PackageParts(
        agents=_count(home / '.codex' / 'agents'),
        commands=expected.commands,
        rules=expected.rules,
        skills=_count(home / '.agents' / 'skills'),
    )
    problems = [
        *first.problems,
        *second.problems,
        *_part_problems(
            'Claude',
            _deployed_parts(home / '.claude'),
            expected,
        ),
        *_part_problems(
            'Codex',
            codex_parts,
            expected,
        ),
        *_old_package_problems(
            home,
            old_package,
        ),
    ]
    result = check.CheckResult(
        name='user install',
        problems=problems,
        note=_relative_package(package),
    )

    return result


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, then install and check in a throwaway home that is removed at the end.
    """
    check.configure_console()
    parsed = _build_parser().parse_args(arguments)
    uvx = shutil.which('uvx')

    if uvx is None:
        print('uvx is not on the PATH: install uv')

        return 1

    with tempfile.TemporaryDirectory(
        dir=SCRATCH_PARENT,
        prefix='kn-',
        ignore_cleanup_errors=True,
    ) as scratch_name:
        scratch = pathlib.Path(scratch_name)
        source = parsed.github or _archive(scratch).as_posix()
        results = [
            check.print_result(
                check_project_install(
                    scratch,
                    source,
                    uvx,
                )
            ),
            check.print_result(
                check_user_install(
                    scratch,
                    source,
                    uvx,
                    parsed.migrate_from,
                )
            ),
            check.print_result(check_scaffold(scratch)),
        ]

        if parsed.show:
            _show(scratch / 'home')

    failed = [
        result.name
        for result in results
        if result.problems
    ]

    return 1 if failed else 0



def _add_target(
    home: pathlib.Path,
    package: pathlib.Path,
    target: str,
) -> subprocess.CompletedProcess:
    """
    Put an assistant on APM's list in the throwaway home, by the installed package's own script.
    """
    added = check.run(
        [
            sys.executable,
            '-I',
            '-B',
            str(package / '.apm' / 'skills' / 'init-researcher' / 'scripts' / 'user_targets.py'),
            'add',
            target,
        ],
        home,
        _environment(home),
    )

    return added

def _apm(
    uvx: str,
    arguments: list[str],
    folder: pathlib.Path,
    home: pathlib.Path,
) -> subprocess.CompletedProcess:
    """
    An APM 0.33.0 command run in a folder, with its home in the throwaway one.
    """
    completed = check.run(
        [
            uvx,
            *APM,
            *arguments,
        ],
        folder,
        _environment(home),
    )

    return completed


def _apm_steps(
    uvx: str,
    steps: list[list[str]],
    home: pathlib.Path,
) -> check.CheckResult:
    """
    APM commands run one after the other in the home, stopping at the first that fails; any warning
    but a user scope's notices is a problem too.
    """
    problems: list[str] = []

    for arguments in steps:
        completed = _apm(
            uvx,
            arguments,
            home,
            home,
        )

        if completed.returncode != 0:
            problems.extend(
                _failed_result(
                    'user install',
                    completed,
                ).problems
            )

            break

        problems.extend(
            _warnings(
                completed,
                USER_NOTICES,
            )
        )

    result = check.CheckResult(
        name='user install',
        problems=problems,
    )

    return result


def _archive(
    scratch: pathlib.Path,
) -> pathlib.Path:
    """
    What the commit would hold, uncommitted changes to tracked files included, extracted into the
    scratch folder with LF endings, as CONTRIBUTING.md makes it.
    """
    stashed = check.git([
        'stash',
        'create',
    ]).stdout.strip()
    archived = subprocess.run(
        [
            'git',
            '-c',
            'core.autocrlf=false',
            'archive',
            '--format=tar',
            f'--prefix={ARCHIVE_PREFIX}/',
            stashed or 'HEAD',
        ],
        capture_output=True,
        check=True,
        cwd=check.REPOSITORY,
    )

    with tarfile.open(fileobj=io.BytesIO(archived.stdout)) as archive:
        archive.extractall(
            scratch,
            filter='data',
        )

    return scratch / ARCHIVE_PREFIX


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: where the package comes from, an older one to migrate from, and --show.
    """
    parser = argparse.ArgumentParser(
        prog='install_check.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--github',
        default='',
        help='install the package from GitHub, owner/name#ref, instead of an archive of this commit',
    )
    parser.add_argument(
        '--migrate-from',
        default='',
        help='an older package, owner/name#ref, installed first at user scope, then migrated from',
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help="print where APM put the package and what the user scope's lock file records",
    )

    return parser


def _count(
    folder: pathlib.Path,
) -> int:
    """
    How many entries a folder holds, or none when it is missing.
    """
    if not folder.is_dir():
        return 0

    entries = sum(
        1
        for _entry in folder.iterdir()
    )

    return entries


def _deployed_parts(
    folder: pathlib.Path,
) -> PackageParts:
    """
    What an assistant's folder holds once deployed: its agents, commands, rules and skills.
    """
    parts = PackageParts(
        agents=_count(folder / 'agents'),
        commands=_count(folder / 'commands'),
        rules=_count(folder / 'rules'),
        skills=_count(folder / 'skills'),
    )

    return parts


def _environment(
    home: pathlib.Path,
) -> dict[str, str]:
    """
    This environment with its home in the throwaway one, and a git identity for the commits made
    there.
    """
    environment = {
        **os.environ,
        'GIT_AUTHOR_EMAIL': 'tester@example.invalid',
        'GIT_AUTHOR_NAME': 'Tester',
        'GIT_COMMITTER_EMAIL': 'tester@example.invalid',
        'GIT_COMMITTER_NAME': 'Tester',
        'HOME': str(home),
        'USERPROFILE': str(home),
    }

    return environment


def _failed_result(
    name: str,
    completed: subprocess.CompletedProcess,
) -> check.CheckResult:
    """
    A step whose command failed: its exit code, and the end of what it printed.
    """
    output_lines = (completed.stdout + completed.stderr).strip().splitlines()
    problems = [
        f'{completed.args[1:4]} exited with {completed.returncode}:',
        *[
            f'    {line}'
            for line in output_lines[-15:]
        ],
    ]
    result = check.CheckResult(
        name=name,
        problems=problems,
    )

    return result


def _git_identity(
    home: pathlib.Path,
) -> None:
    """
    A git identity in the throwaway home's own configuration, as CONTRIBUTING.md sets it.
    """
    for key, value in (
        ('user.name', 'Tester'),
        ('user.email', 'tester@example.invalid'),
    ):
        check.run(
            [
                'git',
                'config',
                '--global',
                key,
                value,
            ],
            home,
            _environment(home),
        )


def _installed_package(
    modules: pathlib.Path,
) -> pathlib.Path | None:
    """
    Where APM put the package under an apm_modules/ folder: the folder, two levels down, whose
    apm.yml names it.
    """
    packages = sorted(
        manifest.parent
        for manifest in modules.glob('*/*/apm.yml')
        if PACKAGE_NAME in manifest.read_text(encoding='utf-8')
    )

    return packages[0] if packages else None


def _matching(
    folder: pathlib.Path,
    pattern: str,
) -> int:
    """
    How many paths under a folder match a glob pattern.
    """
    matches = list(folder.glob(pattern))

    return len(matches)


def _missing_package_result(
    name: str,
) -> check.CheckResult:
    """
    A step whose install reported success but left no package where it is looked for.
    """
    missing = check.CheckResult(
        name=name,
        problems=['the install ran, but no apm_modules/<owner>/<name>/ holds the package'],
    )

    return missing


def _old_package_problems(
    home: pathlib.Path,
    old_package: str,
) -> list[str]:
    """
    After a migration, the older package is gone from the user scope's modules and from its list.
    """
    if not old_package:
        return []

    left = (home / '.apm' / 'apm_modules' / old_package).is_dir()
    manifest = (home / '.apm' / 'apm.yml').read_text(encoding='utf-8')
    listed = old_package.casefold() in manifest.casefold()
    problems = [
        *([f'{old_package} is still in ~/.apm/apm_modules after the migration'] if left else []),
        *([f'{old_package} is still listed in ~/.apm/apm.yml after the migration'] if listed else []),
    ]

    return problems


def _package_parts(
    package: pathlib.Path,
) -> PackageParts:
    """
    What the package holds: its agents, commands, rules, and skills with a SKILL.md.
    """
    parts = PackageParts(
        agents=_matching(package, '.apm/agents/*.agent.md'),
        commands=_matching(package, '.apm/prompts/*.prompt.md'),
        rules=_matching(package, '.apm/instructions/*.instructions.md'),
        skills=_matching(package, '.apm/skills/*/SKILL.md'),
    )

    return parts


def _part_problems(
    assistant: str,
    deployed: PackageParts,
    expected: PackageParts,
) -> list[str]:
    """
    Each kind of file an assistant holds a different number of than the package does.
    """
    problems = [
        f'{assistant}: {getattr(deployed, kind)} {kind} deployed, the package holds {getattr(expected, kind)}'
        for kind in (
            'agents',
            'commands',
            'rules',
            'skills',
        )
        if getattr(deployed, kind) != getattr(expected, kind)
    ]

    return problems


def _relative_package(
    package: pathlib.Path,
) -> str:
    """
    Where the package was installed, under ~/.apm/apm_modules/.
    """
    relative = f'installed as {package.parent.name}/{package.name}'

    return relative


def _scaffold_problems(
    script: pathlib.Path,
    kind: str,
    destination: pathlib.Path,
) -> list[str]:
    """
    One run of the deployed scaffold.py: it copies the starting point and commits it once.
    """
    home = script.parents[4]
    made = check.run(
        [
            sys.executable,
            '-I',
            '-B',
            str(script),
            kind,
            str(destination),
        ],
        home,
        _environment(home),
    )

    if made.returncode != 0:
        return _failed_result(
            'scaffold',
            made,
        ).problems

    logged = check.run(
        [
            'git',
            '-C',
            str(destination),
            'log',
            '-1',
            '--format=%s',
        ],
        home,
        _environment(home),
    )
    problems = [] if logged.returncode == 0 and logged.stdout.strip() else [f'{kind}: no first commit']

    return problems


def _show(
    home: pathlib.Path,
) -> None:
    """
    Where APM put each package in the user scope, and what its lock file records of each.
    """
    modules = home / '.apm' / 'apm_modules'
    installed = sorted(
        folder.relative_to(modules).as_posix()
        for folder in modules.glob('*/*')
        if folder.is_dir()
    )
    print(f'\nuser scope, apm_modules/: {", ".join(installed) or "nothing"}')
    lock = home / '.apm' / 'apm.lock.yaml'
    lock_text = lock.read_text(encoding='utf-8') if lock.is_file() else ''
    recorded = [
        line
        for line in lock_text.splitlines()
        if any(
            key in line
            for key in (
                'repo_url',
                'source:',
                'version:',
                'resolved_ref',
            )
        )
    ]
    print('apm.lock.yaml:')

    for line in recorded:
        print(f'    {line.strip()}')


def _warnings(
    completed: subprocess.CompletedProcess,
    notices: tuple[str, ...],
) -> list[str]:
    """
    Each warning or error line APM printed that is none of the notices expected.
    """
    output_lines = (completed.stdout + completed.stderr).splitlines()
    warnings = [
        f'APM warned: {line.strip()}'
        for line in output_lines
        if ('[!]' in line or '[x]' in line)
        and not any(
            notice in line
            for notice in notices
        )
    ]

    return warnings


if __name__ == '__main__':
    sys.exit(main())
