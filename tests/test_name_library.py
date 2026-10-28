"""
Tests of name_library.py, the init-python-library skill's script: it checks a Python library's name,
and puts the names the owner chose into a fresh copy of the KaxaNuk Python Library Template, which
scaffold.py makes.

PyPI is never asked: a test that reaches the question answers it with a stand-in, and one that
reaches it without one fails.
"""
import datetime
import pathlib
import subprocess
import typing
import unittest.mock

import pytest

import name_library
import scaffold

__all__ = []

REPOSITORY = pathlib.Path(__file__).resolve().parent.parent
# The owner's words for the library: the holder the licence names, and one sentence on what it does.
DESCRIPTION = 'Screens stocks by free cash flow, the way Sofía (2021) taught it.'
HOLDER = 'Pérez, Ana (2021)'
# What git is given, so that each test runs it as a newcomer's git with no settings of its own: an
# identity for the first commit, in the alphabets a researcher may write a name in.
GIT_IDENTITY = {
    'GIT_AUTHOR_EMAIL': 'sofia@example.com',
    'GIT_AUTHOR_NAME': 'Sofía Pérez',
    'GIT_COMMITTER_EMAIL': 'sofia@example.com',
    'GIT_COMMITTER_NAME': 'Sofía Pérez',
}
# The template's own names, which no file of a named copy holds but AGENTS.md, which quotes them.
TEMPLATE_NAMES = [
    name_library.TEMPLATE_DESCRIPTION,
    name_library.TEMPLATE_DISTRIBUTION,
    name_library.TEMPLATE_ERROR_PREFIX,
    name_library.TEMPLATE_HOLDER,
    name_library.TEMPLATE_IMPORT,
    name_library.TEMPLATE_TITLE,
]


def test_copy_problem_refuses_a_copy_with_a_change_not_saved(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    A copy with a change not saved is not named, so that `git reset --hard` can always put it back as
    it was copied.
    """
    copy = _fresh_copy(
        monkeypatch,
        tmp_path,
    )
    readme = copy / 'README.md'
    changed_readme = readme.read_bytes() + 'Notas de Sofía.\n'.encode('utf-8')
    readme.write_bytes(changed_readme)
    problem = name_library.copy_problem(
        copy,
        name_library.derive_names('fcf-screen', None),
    )

    assert problem is not None
    assert problem.startswith('a change not saved:')
    assert 'README.md' in problem


def test_copy_problem_refuses_the_template_inside_the_package(
    tmp_path: pathlib.Path,
) -> None:
    """
    The template itself, inside the package, is never named: it is not the top of a git repository of
    its own. Nor is a folder that is not there.
    """
    names = name_library.derive_names(
        'fcf-screen',
        None,
    )
    missing_folder = tmp_path / 'Sofía (2021)'
    inside_the_package = name_library.copy_problem(
        REPOSITORY / 'templates' / 'python-library',
        names,
    )
    missing = name_library.copy_problem(
        missing_folder,
        names,
    )

    assert inside_the_package is not None
    assert 'is not the top of a git repository of its own' in inside_the_package
    assert missing == f'{missing_folder} is not a folder'


def test_derive_names_gives_four_names_from_one() -> None:
    """
    One name gives the other three: hyphens become underscores to import it, and its words are
    capitalised, joined for its error and spaced for its title, unless a title is given.
    """
    derived = name_library.derive_names(
        'fcf-screen',
        None,
    )
    titled = name_library.derive_names(
        'fcf-screen',
        'FCF Screen',
    )
    with_digits = name_library.derive_names(
        'kn2-value-factor',
        None,
    )

    assert derived == name_library.LibraryNames(
        distribution='fcf-screen',
        error_prefix='FcfScreen',
        import_name='fcf_screen',
        title='Fcf Screen',
    )
    assert titled.title == 'FCF Screen'
    assert titled.import_name == 'fcf_screen'
    assert with_digits.error_prefix == 'Kn2ValueFactor'
    assert with_digits.import_name == 'kn2_value_factor'


def test_first_commit_is_the_one_scaffold_saves() -> None:
    """
    Naming takes only a copy whose history is the first commit scaffold.py saves for this template,
    so both scripts name that commit alike.
    """
    assert scaffold.STARTING_POINTS['python-library'][1] == name_library.FIRST_COMMIT


@pytest.mark.parametrize(
    'state',
    [
        name_library.PYPI_TAKEN,
        name_library.PYPI_UNKNOWN,
    ],
)
def test_main_check_name_keeps_a_name_pypi_holds_for_a_library_never_published(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    state: str,
) -> None:
    """
    With `--unpublished`, for a Python library never published, a name PyPI holds, or could not be
    asked about, can be used.
    """
    monkeypatch.setattr(
        name_library,
        '_ask_pypi',
        _pypi_answering(state),
    )
    checked = name_library.main([
        '--check-name',
        'fcf-screen',
        '--unpublished',
    ])

    assert checked == 0
    assert 'Refused' not in capsys.readouterr().out


@pytest.mark.parametrize(
    (
        'state',
        'exit_code',
        'verdict',
    ),
    [
        (
            name_library.PYPI_FREE,
            0,
            'PyPI: free - no project holds the name',
        ),
        (
            name_library.PYPI_TAKEN,
            1,
            'Refused: another project holds fcf-screen on PyPI.',
        ),
        (
            name_library.PYPI_UNKNOWN,
            1,
            'Refused: PyPI could not be asked whether the name is taken',
        ),
    ],
)
def test_main_check_name_refuses_a_name_pypi_holds_or_could_not_check(
    capsys: pytest.CaptureFixture[str],
    exit_code: int,
    monkeypatch: pytest.MonkeyPatch,
    state: str,
    verdict: str,
) -> None:
    """
    `--check-name` prints the four names one name gives and asks PyPI once: a free name can be used,
    and one another project holds, or one PyPI could not be asked about, is refused.
    """
    asked = _pypi_answering(state)
    monkeypatch.setattr(
        name_library,
        '_ask_pypi',
        asked,
    )
    checked = name_library.main([
        '--check-name',
        'fcf-screen',
    ])
    printed = capsys.readouterr().out

    assert checked == exit_code
    assert verdict in printed
    assert 'fcf_screen' in printed
    assert 'FcfScreenError' in printed
    assert 'Fcf Screen' in printed
    asked.assert_called_once_with('fcf-screen')


def test_main_dry_run_prints_the_plan_and_writes_nothing(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    `--dry-run` prints the move and each file naming would rewrite, and writes nothing; a `uv.lock`
    that `uv sync` wrote before the naming does not stop it.
    """
    copy = _fresh_copy(
        monkeypatch,
        tmp_path,
    )
    (copy / 'uv.lock').write_bytes(b'version = 1\n')
    asked = _pypi_answering(name_library.PYPI_FREE)
    monkeypatch.setattr(
        name_library,
        '_ask_pypi',
        asked,
    )
    named = name_library.main([
        str(copy),
        '--name',
        'fcf-screen',
        '--holder',
        HOLDER,
        '--dry-run',
    ])
    printed = capsys.readouterr().out

    assert named == 0
    assert 'Would move src/kn_python_library_template/ to src/fcf_screen/' in printed
    assert 'Would rewrite LICENSE' in printed
    assert 'Would rewrite pyproject.toml' in printed
    assert 'Would rewrite src/fcf_screen/__init__.py' in printed
    assert 'Nothing was written: --dry-run' in printed
    assert _git(copy, ['status', '--porcelain']) == '?? uv.lock\n'
    assert (copy / 'src' / 'kn_python_library_template' / '__init__.py').is_file()
    asked.assert_called_once_with('fcf-screen')


def test_main_names_a_fresh_copy(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    Naming moves the package folder to the import name and puts the names in every file but
    AGENTS.md, which stays as it was; it leaves a `uv.lock` written before it unsaved, and says how to
    save the naming. Once that is saved the copy is no longer fresh, and naming it again is refused.
    """
    copy = _fresh_copy(
        monkeypatch,
        tmp_path,
    )
    agents_before = (copy / 'AGENTS.md').read_bytes()
    (copy / 'uv.lock').write_bytes(b'version = 1\n')
    monkeypatch.setattr(
        name_library,
        '_ask_pypi',
        _pypi_answering(name_library.PYPI_FREE),
    )
    naming = [
        str(copy),
        '--name',
        'fcf-screen',
        '--title',
        'FCF Screen',
        '--holder',
        HOLDER,
        '--description',
        DESCRIPTION,
    ]
    named = name_library.main(naming)
    printed = capsys.readouterr().out
    leftovers = [
        f'{relative_path}: {template_name}'
        for relative_path in _tracked_files(copy)
        if relative_path != 'AGENTS.md'
        for template_name in TEMPLATE_NAMES
        if template_name.encode('utf-8') in (copy / relative_path).read_bytes()
    ]
    _git(
        copy,
        [
            'commit',
            '--all',
            '--quiet',
            '-m',
            'Name the library fcf-screen',
        ],
    )
    named_again = name_library.main(naming)
    printed_again = capsys.readouterr().out

    assert named == 0
    assert (copy / 'src' / 'fcf_screen' / '__init__.py').is_file()
    assert not (copy / 'src' / 'kn_python_library_template').exists()
    assert (copy / 'AGENTS.md').read_bytes() == agents_before
    assert leftovers == []
    assert f'git -C "{copy}" commit --all -m "Name the library fcf-screen"' in printed
    assert 'uv.lock, written before the naming' in printed
    assert named_again == 1
    assert 'Nothing was named: not a fresh copy' in printed_again


@pytest.mark.parametrize(
    'name',
    [
        'json',
        'Fcf-Screen',
        'kn-python-library-template',
    ],
)
def test_main_refuses_a_bad_name_before_asking_pypi(
    capsys: pytest.CaptureFixture[str],
    name: str,
) -> None:
    """
    A name that cannot be used is refused, exit code 1, before PyPI is asked.
    """
    checked = name_library.main([
        '--check-name',
        name,
    ])

    assert checked == 1
    assert capsys.readouterr().out.startswith('Refused: ')


@pytest.mark.parametrize(
    ('arguments', 'reason'),
    [
        (['--holder', 'Ana "Sofía" Pérez'], 'the holder holds a double quote'),
        (['--holder', 'Pérez\\Ana'], 'the holder holds a double quote, a backslash'),
        (['--holder', ' Pérez, Ana (2021)'], 'the holder is empty, or starts or ends with a space'),
        (
            [
                '--holder',
                HOLDER,
                '--description',
                'x' * 201,
            ],
            'the description is 201 characters; it takes at most 200',
        ),
        (
            [
                '--holder',
                HOLDER,
                '--description',
                'Screens "cheap" stocks.',
            ],
            'the description holds a double quote',
        ),
    ],
    ids=[
        'holder with a double quote',
        'holder with a backslash',
        'holder starting with a space',
        'description too long',
        'description with a double quote',
    ],
)
def test_main_refuses_an_unsafe_holder_or_description(
    arguments: list[str],
    capsys: pytest.CaptureFixture[str],
    reason: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A holder or a description that would break the TOML string it lands in is refused, exit code 1,
    before the folder is read or PyPI asked.
    """
    named = name_library.main([
        str(tmp_path),
        '--name',
        'fcf-screen',
        *arguments,
    ])

    assert named == 1
    assert f'Refused: {reason}' in capsys.readouterr().out


@pytest.mark.parametrize(
    'arguments',
    [
        [],
        [
            '--name',
            'fcf-screen',
            '--holder',
            HOLDER,
        ],
        [
            '--check-name',
            'fcf-screen',
            '--name',
            'fcf-screen',
        ],
    ],
    ids=[
        'nothing',
        'no folder to name',
        'a name to check and one to name',
    ],
)
def test_main_takes_a_name_to_check_or_a_folder_to_name(
    arguments: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    The command line takes either a name to check, or a folder with its name and holder: anything
    else is refused, exit code 2.
    """
    with pytest.raises(SystemExit) as raised:
        name_library.main(arguments)

    assert raised.value.code == 2
    assert 'error:' in capsys.readouterr().err


@pytest.mark.parametrize(
    ('name', 'title'),
    [
        ('fcf-screen', None),
        ('fcf-screen', 'FCF Screen (2021), v2'),
        ('kn2-value-factor', None),
        ('a' * 40, None),
    ],
)
def test_name_problem_accepts_a_name_python_can_import_and_a_plain_title(
    name: str,
    title: str | None,
) -> None:
    """
    A name of lowercase letters, digits and single hyphens, of 40 characters at most, that hides
    nothing Python or the template's tools use, and a title in plain ASCII, can be used.
    """
    names = name_library.derive_names(
        name,
        title,
    )

    assert name_library.name_problem(names) is None


@pytest.mark.parametrize(
    ('name', 'reason'),
    [
        ('Fcf-Screen', 'is not a name'),
        ('fcf_screen', 'is not a name'),
        ('fcf--screen', 'is not a name'),
        ('2fcf', 'is not a name'),
        ('fcf-screen-' + 'x' * 30, 'a name takes at most 40'),
        ('kn-python-library-template', "the template's own name"),
        ('docs', 'a folder of the template'),
        ('tests', 'a folder of the template'),
        ('class', 'a word of Python itself'),
        ('match', 'a word of Python itself'),
        ('json', 'the module of that name Python comes with'),
        ('zip', 'the built-in of that name'),
        ('pytest', "a distribution the template's tools install"),
        ('requests', "a distribution the template's tools install"),
        ('yaml', "a module the template's tools install"),
        ('con', 'Windows keeps for a device'),
        ('com1', 'Windows keeps for a device'),
    ],
)
def test_name_problem_refuses_a_bad_name(
    name: str,
    reason: str,
) -> None:
    """
    A name Python cannot import, or that would hide one of its modules or built-ins, a folder of the
    template, a tool the template installs or a module one brings, a device Windows keeps, or one of
    over 40 characters is refused, saying why.
    """
    names = name_library.derive_names(
        name,
        None,
    )
    problem = name_library.name_problem(names)

    assert problem is not None
    assert reason in problem


@pytest.mark.parametrize(
    ('title', 'reason'),
    [
        ('', 'the title is empty'),
        (' FCF Screen', 'starts or ends with a space'),
        ('FCF Screen ', 'starts or ends with a space'),
        ('F' * 81, 'it takes at most 80'),
        ('Sofía Screen', 'outside plain ASCII'),
        ('FCF Screen \N{EM DASH} v2', 'outside plain ASCII'),
        ('FCF "Screen"', 'which would break the Python it lands in'),
        ("Ana's Screen", 'which would break the Python it lands in'),
        ('FCF `Screen`', 'which would break the Python it lands in'),
    ],
)
def test_name_problem_refuses_a_bad_title(
    reason: str,
    title: str,
) -> None:
    """
    A title that is empty, padded with spaces, over 80 characters, outside plain ASCII, or holding a
    quote, a backtick or a backslash, which would break the strings it lands in, is refused.
    """
    names = name_library.derive_names(
        'fcf-screen',
        title,
    )
    problem = name_library.name_problem(names)

    assert problem is not None
    assert reason in problem


def test_plan_naming_puts_the_names_in_and_writes_nothing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    The plan covers every file git tracks but AGENTS.md: the package's files at the import name, none
    of the template's names left, the holder in pyproject.toml alone and on the licence's first line
    with this year, the owner's sentence in place of the template's, each file's line endings as they
    were; and planning writes nothing.
    """
    copy = _fresh_copy(
        monkeypatch,
        tmp_path,
    )
    tracked = _tracked_files(copy)
    names = name_library.derive_names(
        'fcf-screen',
        'FCF Screen',
    )
    rewrites = name_library.plan_naming(
        copy,
        names,
        HOLDER,
        DESCRIPTION,
    )
    planned = {
        rewrite.path.as_posix(): rewrite.after
        for rewrite in rewrites
    }
    expected_paths = sorted(
        relative_path.replace('src/kn_python_library_template/', 'src/fcf_screen/')
        for relative_path in tracked
        if relative_path != 'AGENTS.md'
    )
    leftovers = [
        f'{path}: {template_name}'
        for path, after in planned.items()
        for template_name in TEMPLATE_NAMES
        if template_name.encode('utf-8') in after
    ]
    holders = sorted(
        path
        for path, after in planned.items()
        if HOLDER.encode('utf-8') in after
    )
    changed_endings = [
        rewrite.path.as_posix()
        for rewrite in rewrites
        if rewrite.after.count(b'\r\n') != rewrite.before.count(b'\r\n')
        or rewrite.after.count(b'\n') != rewrite.before.count(b'\n')
    ]
    licence_lines = planned['LICENSE'].decode('utf-8').splitlines()
    this_year = datetime.date.today().year

    assert sorted(planned) == expected_paths
    assert leftovers == []
    assert holders == [
        'LICENSE',
        'pyproject.toml',
    ]
    assert licence_lines[0] == f'Copyright since {this_year} {HOLDER}'
    assert b'name = "fcf-screen"' in planned['pyproject.toml']
    assert DESCRIPTION.encode('utf-8') in planned['pyproject.toml']
    assert changed_endings == []
    assert _git(copy, ['status', '--porcelain']) == ''


def _fresh_copy(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> pathlib.Path:
    """
    A fresh copy of the Python library template, as `scaffold.py python-library` makes one, its first
    version saved, in a folder named with an accent, a comma and parentheses.
    """
    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    copy = tmp_path / 'Sofía, librería (2021)'
    exit_code = scaffold.main([
        'python-library',
        str(copy),
        '--package',
        str(REPOSITORY),
    ])

    assert exit_code == 0

    return copy


def _git(
    folder: pathlib.Path,
    arguments: list[str],
) -> str:
    """
    What a git command prints in a folder; a command that fails fails the test.
    """
    completed = subprocess.run(
        [
            'git',
            '-C',
            str(folder),
            *arguments,
        ],
        capture_output=True,
        check=True,
        encoding='utf-8',
    )

    return completed.stdout


def _isolate_git(
    monkeypatch: pytest.MonkeyPatch,
    home: pathlib.Path,
) -> None:
    """
    Run git as a newcomer's: a home folder of the test's own, no system or global settings, and an
    identity for the first commit.
    """
    global_settings = home / '.gitconfig'
    global_settings.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    global_settings.write_bytes(b'')
    environment = {
        **GIT_IDENTITY,
        'GIT_CONFIG_GLOBAL': str(global_settings),
        'GIT_CONFIG_NOSYSTEM': '1',
        'HOME': str(home),
        'USERPROFILE': str(home),
        'XDG_CONFIG_HOME': str(home / '.config'),
    }

    for variable, value in environment.items():
        monkeypatch.setenv(variable, value)


@pytest.fixture(autouse=True)
def _offline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Keep every test offline: PyPI is never asked, and a test that reaches the question without a
    stand-in of its own fails.
    """
    monkeypatch.setattr(
        name_library,
        '_ask_pypi',
        _pypi_never_asked,
    )


def _pypi_answering(
    state: str,
) -> unittest.mock.Mock:
    """
    A stand-in for the question to PyPI that gives one answer, and keeps each name it was asked about.
    """
    answer = name_library.PypiAnswer(
        state=state,
        detail=f'a stand-in for PyPI said {state}',
    )
    stand_in = unittest.mock.Mock(return_value=answer)

    return stand_in


def _pypi_never_asked(
    distribution: str,
) -> typing.NoReturn:
    """
    The question to PyPI, refused: a test reached it without a stand-in of its own.
    """
    pytest.fail(f'PyPI was asked about {distribution}; the tests stay offline')


def _tracked_files(
    folder: pathlib.Path,
) -> list[str]:
    """
    The files git tracks in a folder, as sorted POSIX paths from it.
    """
    listed = _git(folder, ['ls-files', '-z'])
    tracked = sorted(
        relative_path
        for relative_path in listed.split('\0')
        if relative_path
    )

    return tracked
