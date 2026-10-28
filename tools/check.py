"""
Every check a commit of the KaxaNuk Researcher package passes, in one command, from the repository's
root:

    uv run --no-project python -I tools/check.py                   every check
    uv run --no-project python -I tools/check.py --fast            every check but the tests
    uv run --no-project python -I tools/check.py --record-parity   record SETUP.md's own lines

The checks, in the order they run. Each prints `ok` or `FAIL` with what failed, and a failure never
stops the next one:
    ruff            the root, each template with Python and each example, with its own settings
    bloom code      the skills' scripts, tools/ and tests/ at 120 columns; each template and example
                    from inside it, at the line length its kind sets
    frozen files    every file FROZEN.json fingerprints, unchanged but for its line endings
    parity          a template and each example worked through it share every line the example does
                    not mark, but for the exceptions AGENTS.md lists
    markdown        each line of Markdown added since origin/dev: LF, no tab, no section sign, and
                    100 columns but where AGENTS.md allows a longer line
    versions        each version agrees with its CHANGELOG, and each part changed since the last
                    release's tag carries a new one
    private names   no tracked file, commit not yet on origin/dev or branch names a word listed in
                    the clone's own .git/info/private-names.txt, which git never shares
    tests           tests/, by pytest, which uv brings with pypdf

Of the parity exceptions, the example's README.md is its own, its CHANGELOG.md shares only what
comes before its entries, its OBJECTIVE.md only what comes before its body, and the template's
AGENTS.md has a status banner the example replaces. SETUP.md's init-example lines are recorded in
tools/parity_exceptions.json: --record-parity writes them anew, to be run only once each recorded
difference has been read and is one AGENTS.md allows.

Exit codes: 0 every check passed · 1 a check failed · 2 usage.
It writes nothing but, with --record-parity, tools/parity_exceptions.json.
"""
import argparse
import dataclasses
import difflib
import hashlib
import itertools
import json
import operator
import pathlib
import re
import shutil
import subprocess
import sys

__all__ = [
    'CheckResult',
    'check_bloom_code',
    'check_frozen_files',
    'check_markdown',
    'check_parity',
    'check_private_names',
    'check_ruff',
    'check_tests',
    'check_versions',
    'configure_console',
    'git',
    'main',
    'markdown_problems',
    'print_result',
    'record_parity',
    'run',
    'version_key',
]

REPOSITORY = pathlib.Path(__file__).resolve().parent.parent

APM_VERSION = re.compile(r'^version:\s*(?P<version>\S+)\s*$', re.M)
BLOOM_CHECKER = REPOSITORY / '.apm' / 'skills' / 'bloom-code-lint' / 'scripts' / 'bloom_code_check.py'
# A CHANGELOG entry's heading: the package's `## [X.Y.Z] - date`, a template's `## X.Y.Z (date)`.
CHANGELOG_ENTRY = re.compile(r'^## \[?(?P<version>\d+\.\d+\.\d+)\]?(?: - | \()\d{4}-\d{2}-\d{2}\)?\s*$', re.M)
EXAMPLE_BEGIN_MARKERS = frozenset({
    '# --- example: begin ---',
    '<!-- example: begin -->',
})
EXAMPLE_END_MARKERS = frozenset({
    '# --- example: end ---',
    '<!-- example: end -->',
})
EXAMPLE_ONLY_CELL = '# EXAMPLE-ONLY CELL'
# The header of each hunk of `git diff -U0`: where the added lines start in the new file, and how
# many there are, one when the count is left out.
HUNK_HEADER = re.compile(r'^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,(?P<count>\d+))? @@', re.M)
# The line length of the Bloom Code check in a template of each kind, and in its examples.
LINE_LENGTHS = {
    'python-library': 120,
    'strategy': 100,
}
# A marked block inside a notebook cell, markers included.
MARKED_BLOCK = re.compile(
    ''.join([
        r'^(<!-- example: begin -->|# --- example: begin ---)$.*?',
        r'^(<!-- example: end -->|# --- example: end ---)$\n?',
    ]),
    re.M | re.S,
)
MARKDOWN_COLUMNS = 100
PARITY_EXCEPTIONS = REPOSITORY / 'tools' / 'parity_exceptions.json'
PARITY_SUFFIXES = frozenset({
    '.ipynb',
    '.md',
    '.py',
})
PROJECT_VERSION = re.compile(r'^version = "(?P<version>[^"]+)"', re.M)
# The shared files whose example-only lines are recorded, rather than marked, in PARITY_EXCEPTIONS.
RECORDED_PARITY_FILES = frozenset({
    'SETUP.md',
})
# A strategy's fixed or append-only records, whose lines may run longer than MARKDOWN_COLUMNS.
RECORD_FILE = re.compile(r'^(?:BLUEPRINT_\d+|JOURNAL_\d+|BITACORA)\.md$')
SECTION_HEADING = re.compile(r'^## ')
SECTION_SIGN = '\N{SECTION SIGN}'
STARTED_FROM_VERSION = re.compile(r'Started from the KaxaNuk Python Library Template (?P<version>\d+\.\d+\.\d+)')


@dataclasses.dataclass(frozen=True)
class CheckResult:
    """
    One check's outcome: its name, each thing that failed, and why it was skipped, when it was.
    """
    name: str
    problems: list[str]
    note: str = ''


@dataclasses.dataclass(frozen=True)
class PythonFolder:
    """
    A template or an example with Python of its own, checked from inside it.
    """
    folder: pathlib.Path
    line_length: int


@dataclasses.dataclass(frozen=True)
class VersionedPart:
    """
    A part of the repository with a version of its own: where the version is read, and the CHANGELOG
    it agrees with, when it has one.
    """
    changelog: str
    folder: str
    name: str
    version_file: str
    version_pattern: re.Pattern


def check_bloom_code() -> CheckResult:
    """
    The Bloom Code check: the skills' scripts, tools/ and tests/ at its default 120 columns, then each
    template and example from inside it, so it finds their own packages.
    """
    own_folders = [
        folder.relative_to(REPOSITORY).as_posix()
        for folder in [
            *sorted(REPOSITORY.glob('.apm/skills/*/scripts')),
            REPOSITORY / 'tools',
            REPOSITORY / 'tests',
        ]
        if folder.is_dir()
    ]
    problems = _bloom_problems(
        REPOSITORY,
        own_folders,
        120,
    )

    for python_folder in _python_folders():
        problems.extend(
            _bloom_problems(
                python_folder.folder,
                ['.'],
                python_folder.line_length,
            )
        )

    result = CheckResult(
        name='bloom code',
        problems=problems,
    )

    return result


def check_frozen_files() -> CheckResult:
    """
    Every frozen file still matches its fingerprint in FROZEN.json, its line endings aside.
    """
    listing = json.loads((REPOSITORY / 'FROZEN.json').read_text(encoding='utf-8'))
    problems = [
        f'frozen file changed: {relative_path}'
        for relative_path, fingerprint in listing['files'].items()
        if _fingerprint(REPOSITORY / relative_path) != fingerprint
    ]
    result = CheckResult(
        name='frozen files',
        problems=problems,
    )

    return result


def check_markdown() -> CheckResult:
    """
    Each line of Markdown added since origin/dev, committed or not, keeps the house rules.
    """
    base = git([
        'merge-base',
        'HEAD',
        'origin/dev',
    ])

    if base.returncode != 0:
        skipped = CheckResult(
            name='markdown',
            problems=[],
            note='skipped: no origin/dev to compare with',
        )

        return skipped

    base_commit = base.stdout.strip()
    changed = git([
        'diff',
        '--name-only',
        '-z',
        '--no-ext-diff',
        '--diff-filter=AMR',
        base_commit,
        '--',
        '*.md',
    ])
    changed_paths = sorted(
        relative_path
        for relative_path in changed.stdout.split('\0')
        if relative_path
    )
    problems = [
        problem
        for relative_path in changed_paths
        for problem in _changed_markdown_problems(
            base_commit,
            relative_path,
        )
    ]
    result = CheckResult(
        name='markdown',
        problems=problems,
    )

    return result


def check_parity() -> CheckResult:
    """
    Each example shares every line of its template's Markdown, Python and notebooks that it does not
    mark, but for the exceptions AGENTS.md lists.
    """
    recorded = _recorded_parity()
    problems = [
        problem
        for example in _examples()
        for relative_path in _tracked_files(REPOSITORY / 'templates' / example.parent.name)
        if pathlib.PurePosixPath(relative_path).suffix in PARITY_SUFFIXES
        and (example / relative_path).is_file()
        for problem in _parity_problems(
            example,
            relative_path,
            recorded,
        )
    ]
    result = CheckResult(
        name='parity',
        problems=problems,
    )

    return result


def check_private_names() -> CheckResult:
    """
    No tracked file, commit not yet on origin/dev or branch names a word from the clone's own list.
    """
    listing = REPOSITORY / git([
        'rev-parse',
        '--git-path',
        'info/private-names.txt',
    ]).stdout.strip()

    if not listing.is_file():
        skipped = CheckResult(
            name='private names',
            problems=[],
            note='skipped: this clone has no .git/info/private-names.txt',
        )

        return skipped

    words = [
        line.strip()
        for line in listing.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')
    ]
    problems = [
        *_private_files(words),
        *_private_commits(words),
        *_private_branches(words),
    ]
    result = CheckResult(
        name='private names',
        problems=problems,
    )

    return result


def check_ruff() -> CheckResult:
    """
    Ruff at the root and in each template and example with Python, each with its own settings.
    """
    uvx = shutil.which('uvx')

    if uvx is None:
        missing = CheckResult(
            name='ruff',
            problems=['uvx is not on the PATH: install uv'],
        )

        return missing

    problems: list[str] = []

    for folder in [
        REPOSITORY,
        *[
            python_folder.folder
            for python_folder in _python_folders()
        ],
    ]:
        completed = run(
            [
                uvx,
                'ruff',
                'check',
                '.',
                '--quiet',
                '--output-format',
                'concise',
            ],
            folder,
        )

        if completed.returncode != 0:
            problems.append(f'in {_relative(folder)}:')
            problems.extend(_indented(completed.stdout + completed.stderr))

    result = CheckResult(
        name='ruff',
        problems=problems,
    )

    return result


def check_tests() -> CheckResult:
    """
    The tests in tests/, by pytest, with pypdf for the PDF scripts; uv brings both.
    """
    uv_command = shutil.which('uv')

    if uv_command is None:
        missing = CheckResult(
            name='tests',
            problems=['uv is not on the PATH: install it'],
        )

        return missing

    completed = run(
        [
            uv_command,
            'run',
            '--no-project',
            '--with',
            'pytest',
            '--with',
            'pypdf[crypto]>=4.0',
            'python',
            '-I',
            '-B',
            '-m',
            'pytest',
            '-q',
            'tests',
        ],
        REPOSITORY,
    )
    output_lines = (completed.stdout + completed.stderr).strip().splitlines()
    summary = output_lines[-1] if output_lines else 'no output'
    problems = [] if completed.returncode == 0 else _indented('\n'.join(output_lines[-40:]))
    result = CheckResult(
        name='tests',
        problems=problems,
        note=summary.strip('= '),
    )

    return result


def check_versions() -> CheckResult:
    """
    Each version agrees with its CHANGELOG, and each part changed since the last release's tag
    carries a new version.
    """
    described = git([
        'describe',
        '--tags',
        '--abbrev=0',
        '--match',
        'v[0-9]*',
        'HEAD',
    ])
    last_tag = described.stdout.strip() if described.returncode == 0 else ''
    problems = [
        problem
        for part in _versioned_parts()
        for problem in _version_problems(
            part,
            last_tag,
        )
    ]
    result = CheckResult(
        name='versions',
        problems=problems,
        note='' if last_tag else 'no release tag to compare with',
    )

    return result


def configure_console() -> None:
    """
    Print in UTF-8 whatever the console's own encoding, as `python -I` ignores PYTHONIOENCODING.
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


def git(
    arguments: list[str],
) -> subprocess.CompletedProcess:
    """
    A git command run at the repository's root.
    """
    completed = run(
        [
            'git',
            *arguments,
        ],
        REPOSITORY,
    )

    return completed


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, then run every check, or record SETUP.md's own lines.
    """
    configure_console()
    parsed = _build_parser().parse_args(arguments)

    if parsed.record_parity:
        return record_parity()

    checks = [
        check_ruff,
        check_bloom_code,
        check_frozen_files,
        check_parity,
        check_markdown,
        check_versions,
        check_private_names,
    ]

    if not parsed.fast:
        checks.append(check_tests)

    results = [
        print_result(check())
        for check in checks
    ]
    failed = [
        result.name
        for result in results
        if result.problems
    ]
    failed_count = len(failed)
    failed_names = ', '.join(failed)
    check_count = len(results)

    if failed:
        print(f'\n{failed_count} of {check_count} checks failed: {failed_names}.')

        return 1

    print(f'\nEvery check passed: {check_count} of them.')

    return 0


def markdown_problems(
    relative_path: str,
    text: str,
    added_line_numbers: set[int],
) -> list[str]:
    """
    What breaks the house rules for Markdown in a file: line endings in the whole file, and a tab, a
    section sign or a line over 100 columns, where no exception allows it, in the added lines.
    """
    lines = text.split('\n')
    long_allowed = _long_lines_allowed(
        relative_path,
        lines,
    )
    problems = [f'{relative_path}: CRLF line endings, not LF'] if '\r' in text else []

    for number in sorted(added_line_numbers):
        line = lines[number - 1] if number <= len(lines) else ''

        if '\t' in line:
            problems.append(f'{relative_path}:{number}: a literal tab')

        if SECTION_SIGN in line:
            problems.append(f'{relative_path}:{number}: the section sign; write "section"')

        if len(line) > MARKDOWN_COLUMNS and not long_allowed[number - 1]:
            problems.append(f'{relative_path}:{number}: {len(line)} columns, over {MARKDOWN_COLUMNS}')

    return problems


def print_result(
    result: CheckResult,
) -> CheckResult:
    """
    Print one check's line, and what failed under it, as soon as it has run.
    """
    status = 'FAIL' if result.problems else 'ok'
    note = f'  ({result.note})' if result.note else ''
    print(
        f'{result.name:<15} {status}{note}',
        flush=True,
    )

    for problem in result.problems:
        print(
            f'    {problem}',
            flush=True,
        )

    return result


def record_parity() -> int:
    """
    Write SETUP.md's own lines, as they differ today, to tools/parity_exceptions.json, and show them.
    """
    recorded = {
        _relative(example / relative_path): _file_hunks(
            example,
            relative_path,
        )
        for example in _examples()
        for relative_path in sorted(RECORDED_PARITY_FILES)
        if (example / relative_path).is_file()
    }
    listing = json.dumps(
        recorded,
        ensure_ascii=False,
        indent=2,
    )
    PARITY_EXCEPTIONS.write_bytes(f'{listing}\n'.encode('utf-8'))

    for example_path, hunks in recorded.items():
        print(f'{example_path}: {len(hunks)} differences recorded')

        for hunk in hunks:
            print(_hunk_text(hunk))

    return 0


def run(
    command: list[str],
    folder: pathlib.Path,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    """
    A command's run in a folder, its output kept, its failure left to the caller; in the given
    environment, when there is one, else in this one.
    """
    completed = subprocess.run(
        command,
        capture_output=True,
        check=False,
        cwd=folder,
        encoding='utf-8',
        env=environment,
        errors='replace',
    )

    return completed


def version_key(
    version: str,
) -> list[int]:
    """
    A version's numbers, compared in order: 1.10.0 comes after 1.9.2.
    """
    numbers = [
        int(number)
        for number in version.split('.')
    ]

    return numbers


def _before(
    lines: list[str],
    heading: re.Pattern,
) -> list[str]:
    """
    The lines before the first one the heading matches, or all of them when none does.
    """
    first = next(
        (
            index
            for index, line in enumerate(lines)
            if heading.match(line)
        ),
        len(lines),
    )

    return lines[:first]


def _bloom_problems(
    folder: pathlib.Path,
    paths: list[str],
    line_length: int,
) -> list[str]:
    """
    The Bloom Code check's report on some paths, run from a folder, or nothing when it passes.
    """
    completed = run(
        [
            sys.executable,
            '-I',
            '-B',
            str(BLOOM_CHECKER),
            *paths,
            '--max-line-length',
            str(line_length),
        ],
        folder,
    )

    if completed.returncode == 0:
        return []

    problems = [
        f'in {_relative(folder)}:',
        *_indented(completed.stdout + completed.stderr),
    ]

    return problems


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: --fast to leave out the tests, --record-parity to record SETUP.md's own lines.
    """
    parser = argparse.ArgumentParser(
        prog='check.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument(
        '--fast',
        action='store_true',
        help='every check but the tests, as the pre-commit hook runs it',
    )
    choice.add_argument(
        '--record-parity',
        action='store_true',
        help="record SETUP.md's own lines in tools/parity_exceptions.json, after reading each one",
    )

    return parser


def _cell_lines(
    cell: dict,
) -> list[str]:
    """
    A notebook cell compared as its id, its type and its non-blank lines outside marked blocks.
    """
    source = ''.join(cell['source'])
    unmarked = MARKED_BLOCK.sub(
        '',
        source,
    )
    lines = [
        str(cell.get('id')),
        cell['cell_type'],
        *_non_blank(unmarked.splitlines()),
    ]

    return lines


def _changed_markdown_problems(
    base_commit: str,
    relative_path: str,
) -> list[str]:
    """
    The house rules' problems in one changed Markdown file, its lines added since the base commit.
    """
    diff = git([
        'diff',
        '-U0',
        '--no-color',
        '--no-ext-diff',
        base_commit,
        '--',
        relative_path,
    ])
    added_line_numbers = {
        number
        for header in HUNK_HEADER.finditer(diff.stdout)
        for number in range(
            int(header['start']),
            int(header['start']) + int(header['count'] or '1'),
        )
    }
    text = (REPOSITORY / relative_path).read_bytes().decode('utf-8', errors='replace')
    problems = markdown_problems(
        relative_path,
        text,
        added_line_numbers,
    )

    return problems


def _comparable_lines(
    relative_path: str,
    path: pathlib.Path,
    is_template: bool,
) -> list[str]:
    """
    A shared file's non-blank lines outside the example's marked blocks, less the part AGENTS.md
    leaves to the example: a CHANGELOG's entries, and the template's OBJECTIVE body and status banner.
    """
    text = path.read_text(encoding='utf-8')
    unmarked = _unmarked_lines(text.split('\n'))

    if relative_path == 'CHANGELOG.md':
        return _non_blank(_before(unmarked, CHANGELOG_ENTRY))

    if relative_path == 'OBJECTIVE.md' and is_template:
        return _non_blank(_without_body(unmarked))

    if relative_path == 'AGENTS.md' and is_template:
        return _non_blank(_without_status_banner(unmarked))

    return _non_blank(unmarked)


def _examples() -> list[pathlib.Path]:
    """
    Every worked example, examples/<kind>/<name>/ with a README.md, whose kind has a template.
    """
    examples = sorted(
        readme.parent
        for readme in REPOSITORY.glob('examples/*/*/README.md')
        if (REPOSITORY / 'templates' / readme.parent.parent.name).is_dir()
    )

    return examples


def _file_hunks(
    example: pathlib.Path,
    relative_path: str,
) -> list[dict]:
    """
    Each place one shared file of an example differs from its template's copy.
    """
    hunks = _hunks(
        _comparable_lines(
            relative_path,
            REPOSITORY / 'templates' / example.parent.name / relative_path,
            is_template=True,
        ),
        _comparable_lines(
            relative_path,
            example / relative_path,
            is_template=False,
        ),
    )

    return hunks


def _fingerprint(
    path: pathlib.Path,
) -> str:
    """
    A file's SHA-256 with its line endings made LF, or nothing when it is missing.
    """
    if not path.is_file():
        return ''

    content = path.read_bytes().replace(b'\r\n', b'\n')
    fingerprint = hashlib.sha256(content).hexdigest()

    return fingerprint


def _holds_any(
    text: str,
    words: list[str],
) -> bool:
    """
    Whether a text holds any of the words, case aside.
    """
    folded = text.casefold()
    found = any(
        word.casefold() in folded
        for word in words
    )

    return found


def _hunk_text(
    hunk: dict,
) -> str:
    """
    One recorded difference, shown as the template's lines then the example's.
    """
    text = '\n'.join([
        *[
            f'    - {line}'
            for line in hunk['template']
        ],
        *[
            f'    + {line}'
            for line in hunk['example']
        ],
        '',
    ])

    return text


def _hunks(
    template_lines: list[str],
    example_lines: list[str],
) -> list[dict]:
    """
    Each place the two copies differ: the template's lines there, and the example's.
    """
    matcher = difflib.SequenceMatcher(
        None,
        template_lines,
        example_lines,
        autojunk=False,
    )
    # Each opcode is the operation, then where it starts and ends in the template, then in the
    # example.
    hunks = [
        {
            'example': example_lines[opcode[3]:opcode[4]],
            'template': template_lines[opcode[1]:opcode[2]],
        }
        for opcode in matcher.get_opcodes()
        if opcode[0] != 'equal'
    ]

    return hunks


def _indented(
    text: str,
) -> list[str]:
    """
    A tool's output as lines indented under the check that ran it.
    """
    lines = [
        f'    {line}'
        for line in text.strip().splitlines()
    ]

    return lines


def _long_lines_allowed(
    relative_path: str,
    lines: list[str],
) -> list[bool]:
    """
    For each line, whether AGENTS.md lets it run past 100 columns: in a fenced code block, a table
    row, a line carrying a URL or a link, the YAML frontmatter, or a strategy's fixed record.
    """
    if RECORD_FILE.match(pathlib.PurePosixPath(relative_path).name):
        return [True] * len(lines)

    fence_lines = [
        line.lstrip().startswith(('```', '~~~'))
        for line in lines
    ]
    inside_fence_after = list(
        itertools.accumulate(
            fence_lines,
            operator.xor,
        )
    )
    frontmatter_end = next(
        (
            index
            for index in range(1, len(lines))
            if lines[0] == '---' and lines[index] == '---'
        ),
        -1,
    )
    allowed = [
        fence_lines[index]
        or (index > 0 and inside_fence_after[index - 1])
        or index <= frontmatter_end
        or line.lstrip().startswith('|')
        or '://' in line
        or '](' in line
        for index, line in enumerate(lines)
    ]

    return allowed


def _marker_state(
    inside: bool,
    marker: bool | None,
) -> bool:
    """
    Whether the next line is inside a marked block: a begin marker opens one, an end marker closes
    it, and any other line leaves it as it was.
    """
    state = inside if marker is None else marker

    return state


def _non_blank(
    lines: list[str],
) -> list[str]:
    """
    The lines that hold anything but white space.
    """
    kept = [
        line
        for line in lines
        if line.strip()
    ]

    return kept


def _notebook_cells(
    path: pathlib.Path,
) -> list[list[str]]:
    """
    A notebook compared cell by cell, its example-only cells left out.
    """
    notebook = json.loads(path.read_text(encoding='utf-8'))
    cells = [
        _cell_lines(cell)
        for cell in notebook['cells']
        if not ''.join(cell['source']).startswith(EXAMPLE_ONLY_CELL)
    ]

    return cells


def _parity_problems(
    example: pathlib.Path,
    relative_path: str,
    recorded: dict,
) -> list[str]:
    """
    How one shared file of an example differs from its template's copy, beyond what is allowed.
    """
    template_file = REPOSITORY / 'templates' / example.parent.name / relative_path
    example_file = example / relative_path
    example_path = example_file.relative_to(REPOSITORY).as_posix()

    if relative_path == 'README.md':
        return []

    if relative_path.endswith('.ipynb'):
        same_notebook = _notebook_cells(template_file) == _notebook_cells(example_file)

        return [] if same_notebook else [f'differs from the template, cell by cell: {example_path}']

    hunks = _file_hunks(
        example,
        relative_path,
    )
    allowed = recorded.get(example_path, []) if relative_path in RECORDED_PARITY_FILES else []
    unexpected = [
        f'differs from the template: {example_path}\n{_hunk_text(hunk)}'
        for hunk in hunks
        if hunk not in allowed
    ]
    stale = [
        hunk
        for hunk in allowed
        if hunk not in hunks
    ]
    gone = [f'a recorded difference is gone from {example_path}: record again once read'] if stale else []

    return [
        *unexpected[:3],
        *gone,
    ]


def _private_branches(
    words: list[str],
) -> list[str]:
    """
    The local branches whose name holds a private word.
    """
    branches = git([
        'for-each-ref',
        '--format=%(refname:short)',
        'refs/heads',
    ]).stdout.split()
    problems = [
        f'a branch is named with a private word: {branch}'
        for branch in branches
        if _holds_any(branch, words)
    ]

    return problems


def _private_commits(
    words: list[str],
) -> list[str]:
    """
    The commits not yet on origin/dev whose message holds a private word.
    """
    listed = git([
        'log',
        '--format=%h %B%x00',
        'origin/dev..HEAD',
    ])
    problems = [
        f'a commit message holds a private word: {message.strip().split()[0]}'
        for message in listed.stdout.split('\0')
        if message.strip() and _holds_any(message, words)
    ]

    return problems


def _private_files(
    words: list[str],
) -> list[str]:
    """
    The tracked files that hold a private word, in their text or their path.
    """
    patterns = [
        argument
        for word in words
        for argument in ['-e', word]
    ]
    in_text = git([
        'grep',
        '-I',
        '-i',
        '-F',
        '-l',
        '-z',
        *patterns,
    ]).stdout.split('\0')
    in_path = [
        tracked
        for tracked in git([
            'ls-files',
            '-z',
        ]).stdout.split('\0')
        if _holds_any(tracked, words)
    ]
    problems = [
        f'a tracked file holds a private word: {tracked}'
        for tracked in sorted({*in_text, *in_path})
        if tracked
    ]

    return problems


def _python_folders() -> list[PythonFolder]:
    """
    Each template with Python of its own, and each example worked through one, with its line length.
    """
    templates = [
        PythonFolder(
            folder=REPOSITORY / 'templates' / kind,
            line_length=line_length,
        )
        for kind, line_length in sorted(LINE_LENGTHS.items())
        if (REPOSITORY / 'templates' / kind).is_dir()
    ]
    examples = [
        PythonFolder(
            folder=example,
            line_length=LINE_LENGTHS[example.parent.name],
        )
        for example in _examples()
        if example.parent.name in LINE_LENGTHS
    ]

    return [
        *templates,
        *examples,
    ]


def _recorded_parity() -> dict:
    """
    The recorded example-only lines of SETUP.md, by example, or none when nothing is recorded.
    """
    if not PARITY_EXCEPTIONS.is_file():
        return {}

    recorded = json.loads(PARITY_EXCEPTIONS.read_text(encoding='utf-8'))

    return recorded


def _relative(
    path: pathlib.Path,
) -> str:
    """
    A path as the repository names it, its root as `.`.
    """
    relative = path.relative_to(REPOSITORY).as_posix()

    return relative


def _tracked_files(
    folder: pathlib.Path,
) -> list[str]:
    """
    The files git tracks under a folder, relative to it.
    """
    prefix = f'{_relative(folder)}/'
    listed = git([
        'ls-files',
        '-z',
        '--',
        prefix,
    ])
    relative_paths = sorted(
        tracked.removeprefix(prefix)
        for tracked in listed.stdout.split('\0')
        if tracked
    )

    return relative_paths


def _unmarked_lines(
    lines: list[str],
) -> list[str]:
    """
    The lines outside the example's marked blocks, the markers left out too, as the snippet in
    CONTRIBUTING.md reads them: a begin marker opens a block and an end marker closes it.
    """
    markers = [
        True if line in EXAMPLE_BEGIN_MARKERS else False if line in EXAMPLE_END_MARKERS else None
        for line in lines
    ]
    inside = list(
        itertools.accumulate(
            markers,
            _marker_state,
            initial=False,
        )
    )
    kept = [
        line
        for index, line in enumerate(lines)
        if not inside[index + 1] and markers[index] is None
    ]

    return kept


def _version_at(
    reference: str,
    part: VersionedPart,
) -> str:
    """
    A part's version at a tag or commit, or nothing when its file did not exist there.
    """
    shown = git([
        'show',
        f'{reference}:{part.version_file}',
    ])
    found = part.version_pattern.search(shown.stdout) if shown.returncode == 0 else None
    version = found['version'] if found else ''

    return version


def _version_problems(
    part: VersionedPart,
    last_tag: str,
) -> list[str]:
    """
    A part's version against its CHANGELOG's newest entry, and against its version at the last tag
    when anything in it changed since.
    """
    found = part.version_pattern.search((REPOSITORY / part.version_file).read_text(encoding='utf-8'))

    if found is None:
        return [f'{part.name}: no version found in {part.version_file}']

    version = found['version']
    problems: list[str] = []

    if part.changelog:
        newest = CHANGELOG_ENTRY.search((REPOSITORY / part.changelog).read_text(encoding='utf-8'))
        newest_version = newest['version'] if newest else 'none'

        if newest_version != version:
            problems.append(
                f'{part.name}: {part.version_file} says {version}, its CHANGELOG {newest_version}'
            )

    if last_tag:
        tagged_version = _version_at(
            last_tag,
            part,
        )
        changed = git([
            'diff',
            '--quiet',
            '--no-ext-diff',
            last_tag,
            '--',
            part.folder,
        ]).returncode == 1

        if changed and tagged_version == version:
            problems.append(
                f'{part.name}: changed since {last_tag}, but {part.version_file} still says {version}'
            )

        if tagged_version and version_key(version) < version_key(tagged_version):
            problems.append(f'{part.name}: {version} is behind {tagged_version}, the version at {last_tag}')

    return problems


def _versioned_parts() -> list[VersionedPart]:
    """
    Each part of the repository with a version of its own, as AGENTS.md lists them.
    """
    parts = [
        VersionedPart(
            changelog='CHANGELOG.md',
            folder='.',
            name='the package',
            version_file='apm.yml',
            version_pattern=APM_VERSION,
        ),
        VersionedPart(
            changelog='templates/researcher/CHANGELOG.md',
            folder='templates/researcher',
            name='the home template',
            version_file='templates/researcher/apm.yml',
            version_pattern=APM_VERSION,
        ),
        VersionedPart(
            changelog='templates/strategy/CHANGELOG.md',
            folder='templates/strategy',
            name='the strategy template',
            version_file='templates/strategy/pyproject.toml',
            version_pattern=PROJECT_VERSION,
        ),
        *[
            VersionedPart(
                changelog=f'{_relative(example)}/CHANGELOG.md',
                folder=_relative(example),
                name=f'the example {example.name}',
                version_file=f'{_relative(example)}/pyproject.toml',
                version_pattern=PROJECT_VERSION,
            )
            for example in _examples()
            if (example / 'pyproject.toml').is_file()
        ],
        VersionedPart(
            changelog='',
            folder='templates/python-library',
            name='the Python library template',
            version_file='templates/python-library/CHANGELOG.md',
            version_pattern=STARTED_FROM_VERSION,
        ),
    ]

    return parts


def _without_body(
    lines: list[str],
) -> list[str]:
    """
    A template's OBJECTIVE.md without its body, from its first section to the rule that closes the
    body, `---`: the example's own body is its marked block.
    """
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if SECTION_HEADING.match(line)
        ),
        len(lines),
    )
    end = next(
        (
            index
            for index in range(start, len(lines))
            if lines[index] == '---'
        ),
        len(lines),
    )
    kept = [
        *lines[:start],
        *lines[end:],
    ]

    return kept


def _without_status_banner(
    lines: list[str],
) -> list[str]:
    """
    A template's AGENTS.md without its status banner, the quoted paragraph that opens with
    `> **Status:`, which every strategy, the example too, replaces with its own.
    """
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if line.startswith('> **Status:')
        ),
        None,
    )

    if start is None:
        return lines

    length = next(
        (
            offset
            for offset, line in enumerate(lines[start:])
            if not line.startswith('>')
        ),
        len(lines) - start,
    )
    kept = [
        *lines[:start],
        *lines[start + length:],
    ]

    return kept


if __name__ == '__main__':
    sys.exit(main())
