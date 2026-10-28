"""
Tests of scaffold.py, the init-strategy skill's script that every init-* skill runs: it finds the
KaxaNuk Researcher package, copies one of its starting points byte for byte into a new folder and
saves the copy's first version with git, or lists the worked examples.
"""
import pathlib
import subprocess

import pytest

import scaffold

__all__ = []

REPOSITORY = pathlib.Path(__file__).resolve().parent.parent
# A starting point's files: those every copy carries, and those no copy carries, at any depth, as a
# checkout, an install, a build or an agent leaves them there, or as they hold a key.
COPIED_FILES = [
    '.github/workflows/main.yml',
    '.gitignore',
    'Config/.env.template',
    'README.md',
    'Sofía/Pérez, Ana (2021).md',
]
LEFT_BEHIND_FILES = [
    '.claude/settings.json',
    '.kaxanuk_license',
    '.venv/pyvenv.cfg',
    'Config/.env',
    'Data/.ipynb_checkpoints/analyzer-checkpoint.ipynb',
    'Data/Prices.ENV',
    '__pycache__/module.cpython-313.pyc',
    'apm_modules/KaxaNuk/KaxaNuk-Researcher/apm.yml',
    'dist/fcf_screen-0.1.0.tar.gz',
    'docs/_build/index.html',
    'uv.lock',
]
# What git is given, so that each test runs it as a newcomer's git with no settings of its own: an
# identity for the first commit, in the alphabets a researcher may write a name in.
GIT_IDENTITY = {
    'GIT_AUTHOR_EMAIL': 'sofia@example.com',
    'GIT_AUTHOR_NAME': 'Sofía Pérez',
    'GIT_COMMITTER_EMAIL': 'sofia@example.com',
    'GIT_COMMITTER_NAME': 'Sofía Pérez',
}
# The first commit of a whole copy of each template, as the init skills and name_library.py read it.
TEMPLATE_FIRST_COMMITS = {
    'python-library': 'Start from the KaxaNuk Python Library Template',
    'researcher': 'Start from the KaxaNuk Researcher template',
    'strategy': 'Start from the KaxaNuk Strategy Template',
}
UNTRACKED_HINT = 'a copy carries the files git tracks in the starting point, and only those: add or remove the others'


@pytest.mark.parametrize(
    'installed_path',
    scaffold.INSTALLED_PACKAGE_PATHS,
    ids=pathlib.PurePath.as_posix,
)
def test_find_package_finds_an_install_above_the_start_folder(
    installed_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    Run as a deployed skill, outside any checkout, the script finds the package an install put under
    `apm_modules/` in a folder above the one it runs from, at each path APM puts it.
    """
    project = tmp_path / 'Sofía, proyecto (2021)'
    start = project / 'Data' / 'Curator'
    start.mkdir(parents=True)
    _outside_a_checkout(
        monkeypatch,
        tmp_path / 'home' / '.apm' / 'apm_modules',
    )
    package = _fake_package(project / 'apm_modules' / installed_path)
    found = scaffold.find_package(
        None,
        start,
    )

    assert found == package


@pytest.mark.parametrize(
    'installed_path',
    scaffold.INSTALLED_PACKAGE_PATHS,
    ids=pathlib.PurePath.as_posix,
)
def test_find_package_finds_an_install_at_user_scope(
    installed_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    With no install above the folder it runs from, the script finds the package `apm install -g` put
    under `~/.apm/apm_modules/`, at each path APM puts it.
    """
    user_modules = tmp_path / 'home' / '.apm' / 'apm_modules'
    start = tmp_path / 'Pérez, Ana (2021)'
    start.mkdir()
    _outside_a_checkout(
        monkeypatch,
        user_modules,
    )
    package = _fake_package(user_modules / installed_path)
    found = scaffold.find_package(
        None,
        start,
    )

    assert found == package


def test_find_package_finds_the_checkout_it_runs_from(
    tmp_path: pathlib.Path,
) -> None:
    """
    Run from a checkout of the package, the script finds that checkout, whatever folder it runs from.
    """
    found = scaffold.find_package(
        None,
        tmp_path,
    )

    assert found == REPOSITORY


def test_find_package_takes_a_given_folder_only_when_it_is_a_package(
    tmp_path: pathlib.Path,
) -> None:
    """
    `--package` names the package outright: a folder holding every starting point is taken as given,
    and one that does not is refused, even from a checkout.
    """
    package = _fake_package(tmp_path / 'Sofía (fork)')
    not_a_package = tmp_path / 'Pérez, Ana (2021)'
    (not_a_package / 'templates' / 'strategy').mkdir(parents=True)

    assert scaffold.find_package(package, REPOSITORY) == package
    assert scaffold.find_package(not_a_package, REPOSITORY) is None


@pytest.mark.parametrize(
    'starting_point',
    sorted(scaffold.STARTING_POINTS),
)
def test_main_copies_a_starting_point_byte_for_byte_and_saves_its_first_version(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    starting_point: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A whole copy holds every file git tracks in the starting point, byte for byte, and nothing else;
    it is a git repository on `main` whose one commit, named for the starting point, holds them all.
    """
    source = _source_folder(starting_point)
    tracked = _tracked_files(source)
    destination = tmp_path / 'Pérez, Ana (2021)'
    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    exit_code = scaffold.main(_starting_point_arguments(
        starting_point,
        destination,
    ))
    printed = capsys.readouterr().out
    different = [
        relative_path
        for relative_path in tracked
        if (destination / relative_path).read_bytes() != (source / relative_path).read_bytes()
    ]
    history = _git(destination, ['log', '--format=%s'])
    status = _git(
        destination,
        [
            'status',
            '--porcelain',
            '--branch',
        ],
    )

    assert exit_code == 0
    assert f'Copied {len(tracked)} files from {source} to {destination}' in printed
    assert _copied_files(destination) == tracked, UNTRACKED_HINT
    assert different == []
    assert history.splitlines() == [_first_commit(starting_point)]
    assert status == '## main\n'
    assert _tracked_files(destination) == tracked


def test_main_examples_lists_each_example_by_its_line(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    `examples` lists each folder `examples/<kind>/<name>/` holding a README.md, by kind then name,
    with the line its README marks, or else its first paragraph's first sentence, links and emphasis
    made plain; `--kind` narrows the list, and a kind with no example lists what the package holds.
    The first line names the package and its version, so that a copy from a stale install shows it.
    """
    package = _fake_package(tmp_path / 'Sofía (paquete)')
    examples = package / 'examples'
    package_line = f'The package at {package}, version 9.8.7'
    listed_lines = [
        'etf/sofía-rotation — Rotates between two ETFs, as Sofía does (2024).',
        'strategy/golden-flow — Golden Flow buys what trades the most, while its trend is up.',
        'strategy/pérez-value — Pérez Value buys cheap stocks of the index, as Pérez, Ana (2021) did.',
    ]
    held_lines = [
        f'  {line}'
        for line in listed_lines
    ]
    listing = [
        'examples',
        '--package',
        str(package),
    ]
    _write(package / 'apm.yml', 'name: kaxanuk-researcher\nversion: 9.8.7\n')
    _write(
        examples / 'etf' / 'sofía-rotation' / 'README.md',
        '\n'.join([
            '# Sofía rotation',
            '',
            '<!-- kaxanuk-example: Rotates between two ETFs, as Sofía does (2024). -->',
            '',
            'Its first paragraph. It is not its line.',
            '',
        ]),
    )
    _write(
        examples / 'strategy' / 'golden-flow' / 'README.md',
        '\n'.join([
            '<!-- example: begin -->',
            '',
            '# Golden Flow',
            '',
            'Golden Flow buys what trades the most, while its trend is up. It cut',
            'its losses in crashes.',
            '',
        ]),
    )
    _write(
        examples / 'strategy' / 'pérez-value' / 'README.md',
        '\n'.join([
            '# Pérez value',
            '',
            '[![Works with](https://img.shields.io/badge/works-Claude-blue)](#install)',
            '',
            '> **Hypothetical results.** Nothing here was traded.',
            '',
            'Pérez Value buys **cheap** stocks of [the index](https://example.com/index), as Pérez, Ana',
            '(2021) did. It sells them later.',
            '',
        ]),
    )
    _write(examples / 'strategy' / 'sin-readme' / 'notes.md', 'No README, so no example.\n')
    _write(examples / 'strategy' / '.oculto' / 'README.md', 'A hidden folder.\n')
    _write(examples / '__pycache__' / 'cached' / 'README.md', 'A cache.\n')
    listed_all = scaffold.main(listing)
    printed_all = capsys.readouterr().out
    listed_strategies = scaffold.main([
        *listing,
        '--kind',
        'strategy',
    ])
    printed_strategies = capsys.readouterr().out
    listed_none = scaffold.main([
        *listing,
        '--kind',
        'researcher',
    ])
    printed_none = capsys.readouterr().out

    assert listed_all == 0
    assert printed_all.splitlines() == [
        package_line,
        *listed_lines,
    ]
    assert listed_strategies == 0
    assert printed_strategies.splitlines() == [
        package_line,
        *listed_lines[1:],
    ]
    assert listed_none == 1
    assert printed_none.splitlines() == [
        package_line,
        'No example of kind researcher is in the package; it holds:',
        *held_lines,
    ]


def test_main_examples_lists_every_example_of_this_package(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    `examples` lists every folder `examples/<kind>/<name>/` of this package holding a README.md, each
    with a line that tells a newcomer choosing one what it shows.
    """
    expected = sorted(
        f'{readme.parent.parent.name}/{readme.parent.name}'
        for readme in REPOSITORY.glob('examples/*/*/README.md')
    )
    exit_code = scaffold.main([
        'examples',
        '--package',
        str(REPOSITORY),
    ])
    listed = capsys.readouterr().out.splitlines()[1:]
    listed_paths = [
        line.partition(' — ')[0]
        for line in listed
    ]
    without_a_line = [
        line
        for line in listed
        if not line.partition(' — ')[2]
    ]

    assert exit_code == 0
    assert listed_paths == expected
    assert without_a_line == []


def test_main_no_git_leaves_the_same_files_and_no_repository(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    With `--no-git`, the copy is the same files, byte for byte, and no git repository.
    """
    source = _source_folder('researcher')
    tracked = _tracked_files(source)
    destination = tmp_path / 'Sofía'
    exit_code = scaffold.main([
        *_starting_point_arguments(
            'researcher',
            destination,
        ),
        '--no-git',
    ])
    printed = capsys.readouterr().out
    different = [
        relative_path
        for relative_path in tracked
        if (destination / relative_path).read_bytes() != (source / relative_path).read_bytes()
    ]

    assert exit_code == 0
    assert 'git repository' not in printed
    assert not (destination / '.git').exists()
    assert _copied_files(destination) == tracked, UNTRACKED_HINT
    assert different == []


def test_main_only_copies_one_path_and_never_overwrites(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    `--only` copies one path of the starting point into an existing folder, as a strategy's lost file
    comes back: a file already there with the same content is skipped, and one with other content
    stops the run before anything is written.
    """
    strategy = tmp_path / 'Sofía, estrategia (2021)'
    strategy.mkdir()
    only = [
        'strategy',
        str(strategy),
        '--only',
        'Data/analyzer.ipynb',
        '--package',
        str(REPOSITORY),
    ]
    template_file = REPOSITORY / 'templates' / 'strategy' / 'Data' / 'analyzer.ipynb'
    copied_file = strategy / 'Data' / 'analyzer.ipynb'
    first_run = scaffold.main(only)
    copied = copied_file.read_bytes()
    second_run = scaffold.main(only)
    printed_second = capsys.readouterr().out
    copied_file.write_bytes(b'{"cells": []}\n')
    third_run = scaffold.main(only)
    printed_third = capsys.readouterr().out

    assert first_run == 0
    assert copied == template_file.read_bytes()
    assert second_run == 0
    assert '1 were already there, identical' in printed_second
    assert third_run == 1
    assert 'Nothing was copied; these files already exist with other content:' in printed_third
    assert copied_file.read_bytes() == b'{"cells": []}\n'
    assert _copied_files(strategy) == ['Data/analyzer.ipynb']


@pytest.mark.parametrize(
    ('only', 'reason'),
    [
        ('../SETUP.md', 'leads outside the starting point or the folder'),
        ('Data/../../SETUP.md', 'leads outside the starting point or the folder'),
        ('Config/.env', 'is never copied'),
        ('Notas de Sofía (2021).md', 'is not part of this starting point'),
    ],
)
def test_main_only_refuses_a_path_outside_missing_or_never_copied(
    capsys: pytest.CaptureFixture[str],
    only: str,
    reason: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    `--only` copies nothing, and says why, for a path that leads outside the starting point or the
    folder, one the starting point does not hold, or one no copy carries, such as a key file.
    """
    package = _fake_package(tmp_path / 'paquete')
    template = package / 'templates' / 'strategy'
    strategy = tmp_path / 'Sofía, estrategia (2021)'
    strategy.mkdir()
    _write(template / 'SETUP.md', 'Setup.\n')
    _write(template / 'Config' / '.env', 'FMP_API_KEY=<your FMP key>\n')
    _write(package / 'templates' / 'SETUP.md', 'Outside the template.\n')
    exit_code = scaffold.main([
        'strategy',
        str(strategy),
        '--only',
        only,
        '--package',
        str(package),
    ])
    printed = capsys.readouterr().out

    assert exit_code == 1
    assert f'{only} {reason}' in printed
    assert list(strategy.iterdir()) == []


def test_main_refuses_a_destination_that_holds_files(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A whole copy goes only into a new folder or an empty one: a folder holding a file of the owner's
    is refused and left as it was, and so is a file in the folder's place.
    """
    destination = tmp_path / 'Pérez, Ana (2021)'
    owner_file = destination / 'Notas de Sofía.md'
    file_in_place = tmp_path / 'Sofía.md'
    _write(owner_file, 'Mías.\n')
    _write(file_in_place, 'Un archivo.\n')
    into_folder = scaffold.main([
        'strategy',
        str(destination),
        '--package',
        str(REPOSITORY),
    ])
    printed_folder = capsys.readouterr().out
    into_file = scaffold.main([
        'strategy',
        str(file_in_place),
        '--package',
        str(REPOSITORY),
    ])
    printed_file = capsys.readouterr().out

    assert into_folder == 1
    assert f'{destination} is not empty; choose a new folder' in printed_folder
    assert _copied_files(destination) == ['Notas de Sofía.md']
    assert owner_file.read_bytes() == 'Mías.\n'.encode('utf-8')
    assert into_file == 1
    assert f'{file_in_place} exists and is not a folder' in printed_file


def test_main_says_how_to_install_the_package_when_none_is_found(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A `--package` that is not the package copies nothing and says how to install it, exit code 1.
    """
    destination = tmp_path / 'Sofía'
    exit_code = scaffold.main([
        'strategy',
        str(destination),
        '--package',
        str(tmp_path / 'Pérez, Ana (2021)'),
    ])
    printed = capsys.readouterr().out

    assert exit_code == 1
    assert printed.startswith('The researcher package was not found. Install it with')
    assert not destination.exists()


def test_main_takes_a_folder_holding_only_what_a_file_manager_leaves(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder made in Finder or Explorer, holding only what they leave in it, counts as empty: the copy
    goes in, and those files stay on disk and out of the first commit.
    """
    tracked = _tracked_files(REPOSITORY / 'templates' / 'researcher')
    destination = tmp_path / 'Sofía, casa (2021)'
    file_manager_files = sorted(scaffold.FILE_MANAGER_FILES)

    for name in file_manager_files:
        _write(destination / name, name)

    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    exit_code = scaffold.main([
        'researcher',
        str(destination),
        '--package',
        str(REPOSITORY),
    ])
    still_there = [
        name
        for name in file_manager_files
        if (destination / name).is_file()
    ]

    assert exit_code == 0
    assert still_there == file_manager_files
    assert _tracked_files(destination) == tracked


def test_plan_copy_leaves_behind_caches_agents_and_keys(
    tmp_path: pathlib.Path,
) -> None:
    """
    A copy plans every file of the starting point, at the same path in the destination, but for what
    a checkout, an install, a build or an agent leaves there and every key file, at any depth; one
    folder planned alone, for `--only`, is judged from the starting point's root, so its key file
    stays behind too.
    """
    source = tmp_path / 'Sofía (plantilla)'
    destination = tmp_path / 'Pérez, Ana (2021)'

    for relative_path in [
        *COPIED_FILES,
        *LEFT_BEHIND_FILES,
    ]:
        _write(source / relative_path, relative_path)

    plan = scaffold.plan_copy(
        source,
        destination,
        source,
    )
    config_plan = scaffold.plan_copy(
        source / 'Config',
        destination / 'Config',
        source,
    )
    planned = [
        origin.relative_to(source).as_posix()
        for origin, _ in plan.files
    ]
    misplaced = [
        origin.relative_to(source).as_posix()
        for origin, landing in plan.files
        if landing != destination / origin.relative_to(source)
    ]
    config_planned = [
        origin.relative_to(source).as_posix()
        for origin, _ in config_plan.files
    ]

    assert sorted(planned) == sorted(COPIED_FILES)
    assert misplaced == []
    assert config_planned == ['Config/.env.template']


def _copied_files(
    folder: pathlib.Path,
) -> list[str]:
    """
    Every file in a folder, outside git's own, as sorted POSIX paths from the folder.
    """
    copied = sorted(
        path.relative_to(folder).as_posix()
        for path in folder.rglob('*')
        if path.is_file() and '.git' not in path.relative_to(folder).parts
    )

    return copied


def _fake_package(
    root: pathlib.Path,
) -> pathlib.Path:
    """
    A folder holding every starting point's folder, as the package does, with nothing in them.
    """
    for relative_source, _ in scaffold.STARTING_POINTS.values():
        (root / relative_source).mkdir(
            parents=True,
            exist_ok=True,
        )

    return root


def _first_commit(
    starting_point: str,
) -> str:
    """
    The message of a whole copy's first commit: a template's own, or the example's, which names its
    kind and its name as scaffold.py's docstring says.
    """
    if starting_point != 'example':
        return TEMPLATE_FIRST_COMMITS[starting_point]

    example = _repository_example()
    message = f'Start from the KaxaNuk example {example.kind}, {example.name}'

    return message


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
    _write(global_settings, '')
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


def _outside_a_checkout(
    monkeypatch: pytest.MonkeyPatch,
    user_modules: pathlib.Path,
) -> None:
    """
    Run the script as a deployed skill does, from no checkout of the package, with a folder of the
    test's own as the user scope's `apm_modules/`.
    """
    monkeypatch.setattr(
        scaffold,
        'SOURCE_PACKAGE',
        user_modules.parent / 'a deployed skill',
    )
    monkeypatch.setattr(
        scaffold,
        'USER_SCOPE_MODULES',
        user_modules,
    )


def _repository_example() -> scaffold.Example:
    """
    The first worked example this repository holds, as the script finds it.
    """
    examples = scaffold.find_examples(REPOSITORY)

    return examples[0]


def _source_folder(
    starting_point: str,
) -> pathlib.Path:
    """
    The folder of this repository that a whole copy of a starting point comes from.
    """
    if starting_point == 'example':
        return _repository_example().folder

    relative_source = scaffold.STARTING_POINTS[starting_point][0]

    return REPOSITORY / relative_source


def _starting_point_arguments(
    starting_point: str,
    destination: pathlib.Path,
) -> list[str]:
    """
    The command line that copies a starting point of this repository: the example by its kind and its
    name, since the package may hold several.
    """
    arguments = [
        starting_point,
        str(destination),
        '--package',
        str(REPOSITORY),
    ]

    if starting_point != 'example':
        return arguments

    example = _repository_example()
    example_arguments = [
        *arguments,
        '--name',
        f'{example.kind}/{example.name}',
    ]

    return example_arguments


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


def _write(
    path: pathlib.Path,
    text: str,
) -> None:
    """
    Write a text file as UTF-8 with its line endings as given, making the folders it needs.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_bytes(text.encode('utf-8'))
