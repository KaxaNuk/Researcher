"""
The brief's health lines, health.py: each check a count and the word that fixes it, run on a small
home with names that hold commas, parentheses and accents, never a value or a path printed.
"""
import pathlib
import subprocess

import health

__all__ = []

PLANTED_KEY = ''.join([
    'sk-',
    'ant-',
    'x1' * 20,
])
REPOSITORY = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_GITIGNORE = REPOSITORY / 'templates' / 'researcher' / '.gitignore'
UNREAD_SOURCE = 'Sources/Papers/Nadie, Uno (2022) Señales, borrador.pdf'


def test_a_clean_home_has_nothing_to_act_on(
    tmp_path: pathlib.Path,
) -> None:
    """
    A home with no source, no finding and no copy on GitHub: every line says so, and none asks for
    a word.
    """
    home = _home(tmp_path)
    lines = health.home_health(home)
    texts = [
        line.text
        for line in lines
    ]

    to_act = [
        line
        for line in lines
        if line.act
    ]

    assert not to_act
    assert 'Reading: every source has its note.' in texts
    assert 'Security: nothing to fix.' in texts
    assert 'Copy: none on GitHub yet.' in texts


def test_a_folder_that_is_no_home_exits_one(
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder without RESEARCHER.md is a usage mistake: exit 1.
    """
    exit_code = health.main([str(tmp_path)])

    assert exit_code == 1


def test_a_planted_key_is_counted_never_shown(
    tmp_path: pathlib.Path,
) -> None:
    """
    A key written in a note is one thing to fix, and the line names `security` without the key, its
    file or its first characters.
    """
    home = _home(tmp_path)
    _write(
        home / 'Knowledge' / 'Notas (borrador), útiles.md',
        f'Una llave pegada por error: {PLANTED_KEY}\n',
    )
    security_line = health.home_health(home)[2]

    assert security_line.act
    assert '1 thing to fix' in security_line.text
    assert '`security`' in security_line.text
    assert PLANTED_KEY[:4] not in security_line.text
    assert 'Notas' not in security_line.text


def test_an_unread_source_names_read(
    tmp_path: pathlib.Path,
) -> None:
    """
    A source no note names is one source not read yet, and the line says `read` without its name.
    """
    home = _home(tmp_path)
    _write(
        home / UNREAD_SOURCE,
        '',
    )
    unread_line = health.home_health(home)[0]

    assert unread_line.act
    assert unread_line.text == 'Reading: 1 source not read yet — say `read`.'


def test_versions_not_on_github_name_backup(
    tmp_path: pathlib.Path,
) -> None:
    """
    A home with a copy it has not sent its last two versions to: two saved versions, and `backup`.
    """
    remote = tmp_path / 'copia, remota.git'
    home = _home(tmp_path / 'Arya (casa)')
    _run_git(
        tmp_path,
        [
            'init',
            '--bare',
            str(remote),
        ],
    )
    _commit(
        home,
        'First',
    )
    _run_git(
        home,
        [
            'remote',
            'add',
            'origin',
            str(remote),
        ],
    )
    _run_git(
        home,
        [
            'push',
            '--set-upstream',
            'origin',
            'HEAD',
        ],
    )

    for message in (
        'Second',
        'Third',
    ):
        _commit(
            home,
            message,
        )
    copy_line = health.home_health(home)[3]

    assert copy_line.act
    assert copy_line.text == 'Copy: 2 saved versions not yet on GitHub — say `backup`.'


def _commit(
    home: pathlib.Path,
    message: str,
) -> None:
    """
    One saved version of the home, with a file of its own so the commit is never empty.
    """
    _write(
        home / 'Studies' / f'{message}.md',
        f'*{message}*\n',
    )
    _run_git(
        home,
        [
            'add',
            '--all',
        ],
    )
    _run_git(
        home,
        [
            '-c',
            'user.name=Prueba',
            '-c',
            'user.email=<>',
            'commit',
            '--quiet',
            '--message',
            message,
        ],
    )


def _home(
    folder: pathlib.Path,
) -> pathlib.Path:
    """
    A home as git sees one: RESEARCHER.md, the template's .gitignore, an empty library, and a
    repository.
    """
    _write(
        folder / '.gitignore',
        TEMPLATE_GITIGNORE.read_text(encoding='utf-8'),
    )
    _write(
        folder / 'RESEARCHER.md',
        '# The researcher\n',
    )
    _write(
        folder / 'Knowledge' / 'INDEX.md',
        '# Index\n',
    )
    _run_git(
        folder,
        [
            'init',
            '--quiet',
        ],
    )

    return folder


def _run_git(
    folder: pathlib.Path,
    arguments: list[str],
) -> None:
    """
    A git command in the folder, which must succeed.
    """
    subprocess.run(
        [
            'git',
            '-C',
            str(folder),
            *arguments,
        ],
        capture_output=True,
        check=True,
    )


def _write(
    path: pathlib.Path,
    text: str,
) -> None:
    """
    A file with its folders, in UTF-8 with LF endings.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_text(
        text,
        encoding='utf-8',
        newline='\n',
    )
