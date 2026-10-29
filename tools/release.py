"""
A release of the KaxaNuk Researcher package from dev to main, as AGENTS.md has it: nothing is pushed
until every check passes, and the release stops at the first step that fails.

    uv run --no-project python -I tools/release.py          say what would be released, or why not
    uv run --no-project python -I tools/release.py --go     release it

Before anything is pushed, in this order, each stopping the release when it fails:
    branch      on dev, with nothing uncommitted and no file git does not know
    GitHub      origin fetched; this dev holds everything dev and main hold there, so dev is pushed
                as it is and main moves by a fast-forward; else the commits to bring in are named
    version     apm.yml's version opens the CHANGELOG, its entry opens with a sentence, and no tag
                has that version yet, here or on GitHub
    security    the security check finds nothing to fix
    Lab         tools/lab_versions.py, each Lab library's newest release against the package's
                record; a library behind it is shown, and never stops the release
    checks      tools/check.py, every check, the tests too
    install     tools/install_check.py, on an archive of the release
With --go, then: dev is pushed, main fast-forwarded to it, the release tagged `vX.Y.Z` there with
`X.Y.Z: <that sentence>`, main and the tag pushed, dev checked out again, and both read back from
GitHub to confirm they name the release's commit.

Exit codes: 0 released, or ready to be with --go · 1 stopped before anything was pushed · 2 a step
after the first push failed, with what was done and what is left printed.
"""
import argparse
import dataclasses
import itertools
import pathlib
import subprocess
import sys

TOOLS = pathlib.Path(__file__).resolve().parent

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check  # noqa: E402 - found beside this file once its folder is on the path, `python -I` too.

__all__ = [
    'Release',
    'main',
    'opening_sentence',
]

SECURITY_CHECK = check.REPOSITORY / '.apm' / 'skills' / 'security' / 'scripts' / 'security_check.py'


@dataclasses.dataclass(frozen=True)
class Release:
    """
    What is released: the version, the commit that carries it, and the sentence its tag quotes.
    """
    commit: str
    sentence: str
    version: str

    @property
    def tag(self) -> str:
        """
        The release's tag, `vX.Y.Z`.
        """
        name = f'v{self.version}'

        return name

    @property
    def tag_message(self) -> str:
        """
        The tag's message: `X.Y.Z: <the CHANGELOG entry's opening sentence>`.
        """
        message = f'{self.version}: {self.sentence}'

        return message


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, pass every gate in order, then release on --go.
    """
    check.configure_console()
    parsed = _build_parser().parse_args(arguments)

    for gate in (
        _branch_gate,
        _github_gate,
        _version_gate,
        _security_gate,
        _lab_gate,
        _checks_gate,
        _install_gate,
    ):
        result = check.print_result(gate())

        if result.problems:
            print('\nNothing was pushed.')

            return 1

    release = _release()

    if not parsed.go:
        print(f'\nReady to release {release.version} at {release.commit[:7]}, tagged "{release.tag_message}".')
        print('Run again with --go to release it.')

        return 0

    return _publish(release)


def opening_sentence(
    changelog: str,
) -> str:
    """
    The opening sentence of a CHANGELOG's newest entry: its first paragraph, its lines joined.
    """
    heading = check.CHANGELOG_ENTRY.search(changelog)

    if heading is None:
        return ''

    entry = changelog[heading.end():].strip('\n')
    lines = entry.split('\n')
    paragraph = [
        line.strip()
        for line in itertools.takewhile(
            str.strip,
            lines,
        )
    ]

    return ' '.join(paragraph)


def _branch_gate() -> check.CheckResult:
    """
    On dev, with nothing uncommitted and no file git does not know.
    """
    branch = check.git([
        'rev-parse',
        '--abbrev-ref',
        'HEAD',
    ]).stdout.strip()
    status = check.git([
        'status',
        '--porcelain',
    ]).stdout.splitlines()
    problems = [
        f'not committed: {line}'
        for line in status[:10]
    ]

    if branch != 'dev':
        problems.insert(
            0,
            f'on {branch}, not dev: a release starts from dev',
        )

    result = check.CheckResult(
        name='branch',
        problems=problems,
    )

    return result


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: --go to release, else only what would be released.
    """
    parser = argparse.ArgumentParser(
        prog='release.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--go',
        action='store_true',
        help='release: push dev, fast-forward main, tag it and push both',
    )

    return parser


def _checks_gate() -> check.CheckResult:
    """
    Every check of tools/check.py, the tests too, its report shown as it runs.
    """
    print('--- tools/check.py', flush=True)
    passed = _run_tool('check.py') == 0
    result = check.CheckResult(
        name='checks',
        problems=[] if passed else ['tools/check.py failed: see its report above'],
    )

    return result


def _confirm(
    release: Release,
) -> int:
    """
    Read main and the tag back from GitHub: both must name the release's commit.
    """
    listed = check.git([
        'ls-remote',
        'origin',
        'refs/heads/main',
        f'refs/tags/{release.tag}^{{}}',
    ]).stdout.split()
    remote_commits = listed[0::2]

    if remote_commits != [release.commit, release.commit]:
        print(f'\nGitHub does not show main and {release.tag} at {release.commit[:7]}: {listed}')

        return 2

    print(f'\nReleased {release.version}: main and {release.tag} on GitHub name {release.commit[:7]}.')

    return 0


def _github_gate() -> check.CheckResult:
    """
    This dev holds everything dev and main hold on GitHub, so dev is pushed as it is and main moves
    by a fast-forward.
    """
    fetched = check.git([
        'fetch',
        '--quiet',
        'origin',
    ])

    if fetched.returncode != 0:
        failed = check.CheckResult(
            name='GitHub',
            problems=[f'git fetch origin failed: {fetched.stderr.strip()}'],
        )

        return failed

    problems = [
        problem
        for remote_branch in (
            'origin/dev',
            'origin/main',
        )
        for problem in _missing_commits(remote_branch)
    ]
    result = check.CheckResult(
        name='GitHub',
        problems=problems,
    )

    return result


def _install_gate() -> check.CheckResult:
    """
    The install a release is tried with, tools/install_check.py, its report shown as it runs.
    """
    print('--- tools/install_check.py', flush=True)
    passed = _run_tool('install_check.py') == 0
    result = check.CheckResult(
        name='install',
        problems=[] if passed else ['tools/install_check.py failed: see its report above'],
    )

    return result


def _lab_gate() -> check.CheckResult:
    """
    The record of the Lab's libraries against their changelogs, tools/lab_versions.py, its report
    shown as it runs; a library behind its record is said, and the release goes on.
    """
    print('--- tools/lab_versions.py', flush=True)
    exit_code = _run_tool('lab_versions.py')
    notes = {
        0: '',
        1: "a library is behind the package's record: see above",
        2: 'not every changelog could be read: see above',
    }
    result = check.CheckResult(
        name='Lab',
        problems=[],
        note=notes.get(exit_code, 'tools/lab_versions.py failed: see above'),
    )

    return result


def _missing_commits(
    remote_branch: str,
) -> list[str]:
    """
    The commits a branch on GitHub holds that this dev does not, to bring into dev first.
    """
    held = check.git([
        'merge-base',
        '--is-ancestor',
        remote_branch,
        'HEAD',
    ]).returncode == 0

    if held:
        return []

    missing = check.git([
        'log',
        '--oneline',
        f'HEAD..{remote_branch}',
    ]).stdout.splitlines()
    problems = [
        f'{remote_branch} holds commits dev does not; merge {remote_branch} into dev first:',
        *[
            f'    {line}'
            for line in missing[:10]
        ],
    ]

    return problems


def _publish(
    release: Release,
) -> int:
    """
    Push dev, fast-forward main to it, tag the release there, push main and the tag, switch back to
    dev, then read both back from GitHub.
    """
    steps = [
        [
            'push',
            'origin',
            'dev',
        ],
        [
            'switch',
            'main',
        ],
        [
            'merge',
            '--ff-only',
            'origin/main',
        ],
        [
            'merge',
            '--ff-only',
            'dev',
        ],
        [
            'tag',
            '-a',
            release.tag,
            '-m',
            release.tag_message,
        ],
        [
            'push',
            'origin',
            'main',
            f'refs/tags/{release.tag}',
        ],
        [
            'switch',
            'dev',
        ],
    ]

    for index, step in enumerate(steps):
        completed = check.git(step)

        if completed.returncode != 0:
            return _stopped(
                steps,
                index,
                completed,
            )

        print(f'git {" ".join(step[:3])} ... ok', flush=True)

    return _confirm(release)


def _release() -> Release:
    """
    The release the gates passed: apm.yml's version, the commit dev is at, and the sentence that
    opens the version's CHANGELOG entry.
    """
    manifest = (check.REPOSITORY / 'apm.yml').read_text(encoding='utf-8')
    found = check.APM_VERSION.search(manifest)
    version = found['version'] if found else ''
    changelog = (check.REPOSITORY / 'CHANGELOG.md').read_text(encoding='utf-8')
    release = Release(
        commit=check.git([
            'rev-parse',
            'HEAD',
        ]).stdout.strip(),
        sentence=opening_sentence(changelog),
        version=version,
    )

    return release


def _run_tool(
    name: str,
) -> int:
    """
    Run one of tools/ with this Python, its output straight to the console, and give its exit code.
    """
    completed = subprocess.run(
        [
            sys.executable,
            '-I',
            '-B',
            str(TOOLS / name),
        ],
        check=False,
        cwd=check.REPOSITORY,
    )

    return completed.returncode


def _security_gate() -> check.CheckResult:
    """
    The security check of the whole repository finds nothing to fix; things to look at are shown.
    """
    completed = check.run(
        [
            sys.executable,
            '-I',
            '-B',
            str(SECURITY_CHECK),
            str(check.REPOSITORY),
        ],
        check.REPOSITORY,
    )
    report = [
        f'    {line}'
        for line in (completed.stdout + completed.stderr).strip().splitlines()
    ]
    passed = completed.returncode in (
        0,
        3,
    )
    problems = [] if passed else [
        'the security check found something to fix:',
        *report,
    ]
    result = check.CheckResult(
        name='security',
        problems=problems,
        note='only things to look at' if completed.returncode == 3 else '',
    )

    return result


def _stopped(
    steps: list[list[str]],
    index: int,
    completed: subprocess.CompletedProcess,
) -> int:
    """
    A step after the first push failed: say what was done, what failed and what is left, and go back
    to dev.
    """
    done = [
        f'    done: git {" ".join(step)}'
        for step in steps[:index]
    ]
    left = [
        f'    left: git {" ".join(step)}'
        for step in steps[index + 1:]
    ]
    print('\n'.join([
        f'git {" ".join(steps[index])} failed:',
        f'    {(completed.stdout + completed.stderr).strip()}',
        *done,
        *left,
    ]))
    check.git([
        'switch',
        'dev',
    ])

    return 1 if index == 0 else 2


def _version_gate() -> check.CheckResult:
    """
    apm.yml's version opens the CHANGELOG, its entry opens with a sentence, and no tag has it yet.
    """
    release = _release()
    changelog = (check.REPOSITORY / 'CHANGELOG.md').read_text(encoding='utf-8')
    newest = check.CHANGELOG_ENTRY.search(changelog)
    newest_version = newest['version'] if newest else ''
    local_tag = check.git([
        'rev-parse',
        '--quiet',
        '--verify',
        f'refs/tags/{release.tag}',
    ]).returncode == 0
    remote_tag = bool(
        check.git([
            'ls-remote',
            '--tags',
            'origin',
            f'refs/tags/{release.tag}',
        ]).stdout.strip()
    )
    findings = {
        f'apm.yml says {release.version or "no version"}, the CHANGELOG opens with {newest_version}': (
            not release.version or newest_version != release.version
        ),
        'the CHANGELOG entry opens with no sentence ending in a period': not release.sentence.endswith('.'),
        f'{release.tag} is already a tag here': local_tag,
        f'{release.tag} is already a tag on GitHub': remote_tag,
    }
    problems = [
        problem
        for problem, found in findings.items()
        if found
    ]
    result = check.CheckResult(
        name='version',
        problems=problems,
        note=release.version,
    )

    return result


if __name__ == '__main__':
    sys.exit(main())
