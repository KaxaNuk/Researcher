"""
Tests of bloom_code_check.py, the bloom-code-lint skill's script: it reports each violation of the
mechanical Bloom Code rules by its rule's code and its line, and passes a clean file.
"""
import io
import pathlib
import sys

import pytest

import bloom_code_check

__all__ = []

# A module as the house rules write one, a string holding a comma, parentheses and accents.
CLEAN_SOURCE = '\n'.join([
    '"""',
    'A module of the house style.',
    '"""',
    'import pathlib',
    '',
    '__all__ = [',
    '    "file_name",',
    ']',
    '',
    'HOLDER = "Pérez, Ana (2021)"',
    '',
    '',
    'def file_name(',
    '    path: pathlib.Path,',
    ') -> str:',
    '    """',
    '    The name of a file, without its folder.',
    '    """',
    '    name = path.name',
    '',
    '    return name',
    '',
])
# A module that binds one name twice, the second time on its second line.
REASSIGNED_SOURCE = '\n'.join([
    'total = 1',
    'total = 2',
    '',
])


def test_check_source_allows_a_from_import_of_a_local_package_only() -> None:
    """
    `from x import y` is for the project's own packages: allowed for a local one, reported for any
    other.
    """
    source = 'from fcf_screen import screens\n'
    local = _found(
        source,
        local_packages=frozenset({'fcf_screen'}),
    )
    foreign = _found(source)

    assert local == []
    assert foreign == [(1, 'BLOOM003')]


def test_check_source_counts_the_branches_of_an_if_once() -> None:
    """
    A name bound once in each branch of an `if` is one concept, not a reassignment.
    """
    source = '\n'.join([
        'def label(',
        '    ready: bool,',
        ') -> str:',
        '    """',
        '    A word for a state.',
        '    """',
        '    if ready:',
        '        word = "listo"',
        '    else:',
        '        word = "pendiente"',
        '',
        '    return word',
        '',
    ])

    assert _found(source) == []


def test_check_source_passes_a_clean_module() -> None:
    """
    A module written as the house rules ask is clean: a comma inside a string is no item.
    """
    assert _found(CLEAN_SOURCE) == []


def test_check_source_reads_two_items_and_two_calls_literally_when_strict() -> None:
    """
    By default two items, or two calls, may share a line; strict, the rules are read literally and
    both are reported.
    """
    source = '\n'.join([
        'pair = [1, 2]',
        'size = len(str(12))',
        '',
    ])
    lenient = _found(source)
    strict = _found(
        source,
        strict=True,
    )

    assert lenient == []
    assert strict == [(1, 'BLOOM010'), (2, 'BLOOM012')]


def test_check_source_reports_a_syntax_error_as_bloom000() -> None:
    """
    A file Python cannot parse is reported once, as BLOOM000 on the line of the error, and no rule of
    style is read.
    """
    violations = bloom_code_check.check_source(
        'def broken(:\n',
        'broken.py',
        frozenset(),
    )
    found = [
        (violation.line, violation.code)
        for violation in violations
    ]

    assert found == [(1, 'BLOOM000')]
    assert violations[0].message.startswith(bloom_code_check.RULE_MESSAGES['BLOOM000'])


@pytest.mark.parametrize(
    (
        'code',
        'line',
        'lines',
    ),
    [
        (
            'BLOOM001',
            2,
            [
                'def outer() -> None:',
                '    def inner() -> None:',
                '        pass',
            ],
        ),
        (
            'BLOOM002',
            1,
            ['import json as serializer'],
        ),
        (
            'BLOOM003',
            1,
            ['from json import dumps'],
        ),
        (
            'BLOOM004',
            1,
            ['from __future__ import annotations'],
        ),
        (
            'BLOOM005',
            1,
            [
                'for ix in range(3):',
                '    print(ix)',
            ],
        ),
        (
            'BLOOM006',
            2,
            [
                'total = 1',
                'total = 2',
            ],
        ),
        (
            'BLOOM007',
            2,
            [
                'def bounds() -> tuple[int, int]:',
                '    return (0, 1)',
            ],
        ),
        (
            'BLOOM008',
            1,
            ['greeting = "Hola, " "Sofía"'],
        ),
        (
            'BLOOM009',
            5,
            [
                'def zeta() -> None:',
                '    pass',
                '',
                '',
                'def alpha() -> None:',
                '    pass',
            ],
        ),
        (
            'BLOOM010',
            1,
            ['names = ["Pérez, Ana", "Sofía", "Łucja"]'],
        ),
        (
            'BLOOM011',
            1,
            [
                'def doubled(number):',
                '    return number * 2',
            ],
        ),
        (
            'BLOOM012',
            1,
            ['size = len(str(abs(-12)))'],
        ),
        (
            'BLOOM013',
            2,
            [
                'def refuse() -> None:',
                '    raise ValueError("not a name")',
            ],
        ),
        (
            'BLOOM014',
            1,
            ['point = 1, 2'],
        ),
        (
            'BLOOM015',
            3,
            [
                'def doubled(number: int) -> int:',
                '    result = number * 2',
                '    return result',
            ],
        ),
        (
            'BLOOM016',
            1,
            ['squares = [number * number for number in range(4)]'],
        ),
        (
            'BLOOM017',
            2,
            [
                'def nothing() -> None:',
                '    """Do nothing.',
                '',
                '    Not even that.',
                '    """',
            ],
        ),
    ],
)
def test_check_source_reports_each_rule_by_its_code(
    code: str,
    line: int,
    lines: list[str],
) -> None:
    """
    A snippet that breaks one rule is reported once, on the line that breaks it, with the rule's code
    and its message.
    """
    violations = bloom_code_check.check_source(
        '\n'.join([
            *lines,
            '',
        ]),
        'snippet.py',
        frozenset(),
    )
    expected = bloom_code_check.Violation(
        line=line,
        code=code,
        message=bloom_code_check.RULE_MESSAGES[code],
    )

    assert violations == [expected]


def test_check_source_splits_two_items_on_a_line_over_the_length_limit() -> None:
    """
    Two items may share a line up to the project's line length, and must split on a longer line.
    """
    source = 'authors = ["Pérez, Ana (2021)", "Sofía"]\n'
    within_the_limit = _found(source)
    over_the_limit = _found(
        source,
        maximum_line_length=30,
    )

    assert within_the_limit == []
    assert over_the_limit == [(1, 'BLOOM010')]


def test_main_passes_a_clean_folder_and_skips_the_folders_it_never_reads(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder is searched for Python files below it, but for virtual environments, caches, git's own
    folder and installed modules, whose files are never read: a clean folder passes, exit code 0.
    """
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / 'Data' / 'curator.py', CLEAN_SOURCE)

    for ignored_folder in sorted(bloom_code_check.IGNORED_FOLDER_NAMES):
        _write(folder / ignored_folder / 'reassigned.py', REASSIGNED_SOURCE)

    monkeypatch.chdir(tmp_path)
    exit_code = bloom_code_check.main([str(folder)])

    assert exit_code == 0
    assert capsys.readouterr().out == '[ok] 1 file(s) clean\n'


def test_main_prints_each_violation_and_exits_one(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    Each violation is printed on a line of its own, `path:line: CODE message`, then their count, exit
    code 1.
    """
    path = tmp_path / 'strategy' / 'reassigned.py'
    _write(path, REASSIGNED_SOURCE)
    monkeypatch.chdir(tmp_path)
    exit_code = bloom_code_check.main([str(path)])
    message = bloom_code_check.RULE_MESSAGES['BLOOM006']

    assert exit_code == 1
    assert capsys.readouterr().out.splitlines() == [
        f'{path}:2: BLOOM006 {message}',
        '[x] 1 Bloom Code violation(s) in 1 file(s)',
    ]


@pytest.mark.xfail(
    strict=True,
    raises=UnicodeEncodeError,
    reason=' '.join([
        'main prints each path as given, though the checker promises ASCII output: a path holding a',
        'character the console cannot write, such as the first letter of Łucja through a pipe on',
        'Windows, raises UnicodeEncodeError instead of printing the report',
    ]),
)
def test_main_reports_a_path_outside_ascii_on_any_console(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    The report is ASCII, as the checker promises, so a console that cannot write a character of a
    path still gets every violation, rather than a traceback.
    """
    path = tmp_path / 'Łucja' / 'reassigned.py'
    _write(path, REASSIGNED_SOURCE)
    console = io.TextIOWrapper(
        io.BytesIO(),
        encoding='ascii',
    )
    monkeypatch.setattr(
        sys,
        'stdout',
        console,
    )
    monkeypatch.chdir(tmp_path)
    exit_code = bloom_code_check.main([str(path)])
    console.flush()
    printed = console.buffer.getvalue().decode(
        'ascii',
        errors='replace',
    )

    assert exit_code == 1
    assert 'reassigned.py:2: BLOOM006' in printed


def _found(
    source: str,
    local_packages: frozenset[str] = frozenset(),
    strict: bool = False,
    maximum_line_length: int = bloom_code_check.DEFAULT_MAXIMUM_LINE_LENGTH,
) -> list[tuple[int, str]]:
    """
    Each violation the checker reports in a source, as its line and its rule's code.
    """
    violations = bloom_code_check.check_source(
        source,
        'snippet.py',
        local_packages,
        strict,
        maximum_line_length,
    )
    found = [
        (violation.line, violation.code)
        for violation in violations
    ]

    return found


def _write(
    path: pathlib.Path,
    text: str,
) -> None:
    """
    Write a text file as UTF-8, making the folders it needs.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_bytes(text.encode('utf-8'))
