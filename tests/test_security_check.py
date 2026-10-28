"""
Tests of security_check.py, the security skill's script: it reads a home, a strategy or a library for
what should not leave the computer, and never prints a value.

Every secret and personal address below is joined from pieces when the tests run, so that no line of
this file is shaped like one: the check scans this repository before every release, and a key-shaped
line here would stop the release.
"""
import json
import pathlib
import subprocess

import pytest

import security_check

__all__ = []

# What git is given, so that each test runs it as a newcomer's git with no settings of its own: an
# identity for a commit, at an address an example uses.
GIT_IDENTITY = {
    'GIT_AUTHOR_EMAIL': 'sofia@example.com',
    'GIT_AUTHOR_NAME': 'Sofía Pérez',
    'GIT_COMMITTER_EMAIL': 'sofia@example.com',
    'GIT_COMMITTER_NAME': 'Sofía Pérez',
}
# A person's own address, joined at run time.
PERSONAL_ADDRESS = ''.join([
    'sofia.perez',
    '@',
    'gmail.com',
])
# Planted secrets: one of each kind the check knows by its shape, and one written beside its name.
PLANTED_SECRETS = {
    'ai-provider-key': ''.join([
        'sk-',
        'ant-',
        'x1' * 20,
    ]),
    'aws-access-key': ''.join([
        'AKIA',
        'Q7W2' * 4,
    ]),
    'github-token': ''.join([
        'ghp_',
        'Tq7' * 12,
    ]),
    'google-api-key': ''.join([
        'AIza',
        'Sy9' * 11,
        'Bc',
    ]),
    'named-secret': ''.join([
        'Kq7mZ',
        '4vX9' * 3,
    ]),
    'password-in-a-web-address': ''.join([
        'postgresql://sofia:',
        'Zq8vPw3nTk',
        '@db.internal/prices',
    ]),
    'private-key': ''.join([
        '-----BEGIN ',
        'RSA PRIVATE KEY-----',
    ]),
    'slack-token': ''.join([
        'xoxb-',
        '2048-',
        'Kp4' * 6,
    ]),
}
# The lines of an environment template, every value a placeholder.
TEMPLATE_LINES = '\n'.join([
    '# Copy this file to .env and put your own keys in place of the placeholders.',
    'FMP_API_KEY=<your FMP key>',
    'KAXANUK_LICENSE_KEY=your_licence_key_2024',
    '',
])


@pytest.mark.parametrize(
    'relative_path',
    [
        '.env',
        '.env.local',
        'Config/.env',
        'Data/prices.env',
        '.kaxanuk_license',
        'credentials.json',
        'id_ed25519',
        'Config/server.pem',
        'deploy.key',
    ],
)
def test_check_file_finds_a_file_of_keys_by_its_name(
    relative_path: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A file that holds keys by its kind is to fix before sharing, whatever it holds: a `.env` at any
    depth, a licence file, a private key, credentials.
    """
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / relative_path, TEMPLATE_LINES)
    findings = security_check.check_file(
        folder,
        relative_path,
    )
    found = [
        (finding.level, finding.location)
        for finding in findings
    ]

    assert found == [(security_check.FIX, relative_path)]


@pytest.mark.parametrize(
    ('outputs', 'levels'),
    [
        ([], []),
        (
            [
                {
                    'name': 'stdout',
                    'output_type': 'stream',
                    'text': ['Pérez, Ana (2021)\n'],
                },
            ],
            [security_check.LOOK],
        ),
    ],
    ids=[
        'cleared',
        'saved with its outputs',
    ],
)
def test_check_file_takes_a_notebook_saved_with_outputs_to_look_at(
    levels: list[str],
    outputs: list[dict],
    tmp_path: pathlib.Path,
) -> None:
    """
    A notebook saved with its outputs may show data or a value: it is one to look at, and a cleared
    one is no finding.
    """
    folder = tmp_path / 'Sofía'
    _write(folder / 'analyzer.ipynb', _notebook(outputs))
    findings = security_check.check_file(
        folder,
        'analyzer.ipynb',
    )
    found = [
        finding.level
        for finding in findings
    ]

    assert found == levels


def test_check_file_takes_a_placeholder_for_no_secret(
    tmp_path: pathlib.Path,
) -> None:
    """
    A placeholder is never a finding, though it stands where a key would and has a key's shape: a
    name in angle brackets or braces, a variable, `your_api_key`, `xxxx`, `...`, a row of stars.
    """
    folder = tmp_path / 'Pérez, Ana (2021)'
    _write(
        folder / 'SETUP.md',
        '\n'.join([
            'FMP_API_KEY=<your FMP key>',
            'FMP_API_KEY=your_api_key_2024',
            'password: xxxx-2024-xxxx',
            'licence_key: $KAXANUK_LICENCE_2024',
            'token=abc...789',
            'secret_key: ********9',
            'Connect to postgresql://sofia:<password>@{SERVER}/prices',
            ''.join([
                'OPENAI_API_KEY=',
                'sk-',
                'proj-',
                'your-key-',
                '0' * 24,
            ]),
            ''.join([
                'AWS_KEY=',
                'AKIA',
                'X' * 16,
            ]),
            ''.join([
                'GITHUB_TOKEN=',
                'ghp_',
                'x' * 36,
            ]),
            '',
        ]),
    )
    findings = security_check.check_file(
        folder,
        'SETUP.md',
    )

    assert findings == []


@pytest.mark.parametrize(
    'relative_path',
    [
        '.env.example',
        '.env.sample',
        '.env.template',
        'Config/.env.template',
    ],
)
def test_check_file_takes_an_environment_template_for_no_finding(
    relative_path: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    An environment template is not a file of keys: `Config/.env.template` ships in every strategy,
    its values placeholders.
    """
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / relative_path, TEMPLATE_LINES)
    findings = security_check.check_file(
        folder,
        relative_path,
    )

    assert findings == []


def test_check_folder_in_git_finds_a_gitignore_that_lets_a_key_file_in(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    In a git repository, a `.gitignore` that would let `.env` in, at the root or in `Config/`, is to
    fix before sharing, once for each.
    """
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / '.gitignore', '.venv/\n')
    _write(folder / 'README.md', 'Sofía buys what trades the most.\n')
    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    _git(
        folder,
        [
            'init',
            '--quiet',
            '--initial-branch=main',
        ],
    )
    findings = security_check.check_folder(folder)
    found = [
        (finding.level, finding.location)
        for finding in findings
    ]

    assert found == [
        (security_check.FIX, '.gitignore'),
        (security_check.FIX, '.gitignore'),
    ]
    assert findings[0].what.startswith('does not keep .env out')
    assert findings[1].what.startswith('does not keep Config/.env out')


def test_check_folder_in_git_reads_what_git_would_save(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    In a git repository, the check reads every file git tracks or would add: a key in a new file is
    found, and a `.env` that `.gitignore` keeps out is never read.
    """
    secret = PLANTED_SECRETS['named-secret']
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / '.gitignore', '.env\n')
    _write(folder / 'Config' / '.env', f'FMP_API_KEY={secret}\n')
    _write(folder / 'Data' / 'connect.py', f'api_key = "{secret}"\n')
    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    _git(
        folder,
        [
            'init',
            '--quiet',
            '--initial-branch=main',
        ],
    )
    findings = security_check.check_folder(folder)
    found = [
        (finding.level, finding.location)
        for finding in findings
    ]

    assert found == [(security_check.FIX, 'Data/connect.py:1')]


def test_check_folder_in_git_takes_a_personal_address_signing_a_version_to_look_at(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    A personal address that signs a saved version is one to look at, as a copy on GitHub shows it,
    and is shown masked; an example's address signs as nothing.
    """
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / '.gitignore', '.env\n')
    _write(folder / 'README.md', 'Sofía buys what trades the most.\n')
    _isolate_git(
        monkeypatch,
        tmp_path / 'home',
    )
    monkeypatch.setenv('GIT_AUTHOR_EMAIL', PERSONAL_ADDRESS)
    _git(
        folder,
        [
            'init',
            '--quiet',
            '--initial-branch=main',
        ],
    )
    _git(folder, ['add', '--all'])
    _git(
        folder,
        [
            'commit',
            '--quiet',
            '-m',
            'Start from the KaxaNuk Strategy Template',
        ],
    )
    findings = security_check.check_folder(folder)
    found = [
        (finding.level, finding.location)
        for finding in findings
    ]

    assert found == [(security_check.LOOK, 'the saved versions')]
    assert 'so…@gmail.com' in findings[0].what
    assert PERSONAL_ADDRESS not in findings[0].what


@pytest.mark.parametrize(
    ('marker', 'kind'),
    [
        ('RESEARCHER.md', 'home'),
        ('Bibliotheca/BIBLIOGRAPHY.md', 'strategy'),
        ('pyproject.toml', 'library'),
        ('Notas de Sofía.md', 'folder'),
    ],
)
def test_folder_kind_tells_a_home_a_strategy_and_a_library_apart(
    kind: str,
    marker: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A home holds RESEARCHER.md, a strategy a Bibliotheca/ folder, a library a pyproject.toml: a copy
    on GitHub that is public is to fix for a home alone.
    """
    folder = tmp_path / 'Pérez, Ana (2021)'
    _write(folder / marker, '')

    assert security_check.folder_kind(folder) == kind


@pytest.mark.parametrize(
    'kind_of_secret',
    sorted(PLANTED_SECRETS),
)
def test_main_finds_a_planted_key_and_never_prints_it(
    capsys: pytest.CaptureFixture[str],
    kind_of_secret: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A secret in a file is to fix before sharing, exit code 2, and its value is never printed: only
    its first four characters and its length, beside the file and the line.
    """
    secret = PLANTED_SECRETS[kind_of_secret]
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / 'Pérez, Ana (2021).md', f'Kept here by mistake:\nFMP_API_KEY={secret}\n')
    exit_code = security_check.main([str(folder)])
    printed = capsys.readouterr().out
    shown_pieces = [
        secret[start:start + 8]
        for start in range(len(secret) - 7)
        if secret[start:start + 8] in printed
    ]

    assert exit_code == 2
    assert 'Fix before you share (' in printed
    assert 'Pérez, Ana (2021).md:2' in printed
    assert f'{secret[:4]}…' in printed
    assert shown_pieces == []
    assert printed.splitlines()[-1].startswith('No value was printed.')


def test_main_reads_a_folder_without_git_but_its_skipped_folders(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    In a folder without git, every file is read, in folders of any name, but for those never read: a
    virtual environment, a cache, installed modules.
    """
    secret = PLANTED_SECRETS['named-secret']
    folder = tmp_path / 'Sofía, estrategia (2021)'
    _write(folder / 'Notas de Sofía' / 'claves (2021).md', f'FMP_API_KEY={secret}\n')

    for skipped_folder in sorted(security_check.SKIPPED_FOLDERS - {'.git'}):
        _write(folder / skipped_folder / 'settings.md', f'FMP_API_KEY={secret}\n')

    exit_code = security_check.main([str(folder)])
    printed = capsys.readouterr().out

    assert exit_code == 2
    assert 'Fix before you share (1):' in printed
    assert 'Notas de Sofía/claves (2021).md:1' in printed


def test_main_refuses_what_is_not_a_folder(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder that is not there is said on the error stream, exit code 1, and nothing is read.
    """
    missing = tmp_path / 'Sofía (2021)'
    exit_code = security_check.main([str(missing)])

    assert exit_code == 1
    assert capsys.readouterr().err == f'not a folder: {missing}\n'


def test_main_says_nothing_to_fix_in_a_clean_folder(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder with nothing to fix or look at, without git, says so in one line, exit code 0.
    """
    folder = tmp_path / 'Sofía, casa (2021)'
    _write(folder / 'README.md', 'Sofía reads on momentum, as Pérez, Ana (2021) did.\n')
    _write(folder / 'Config' / '.env.template', TEMPLATE_LINES)
    exit_code = security_check.main([str(folder)])
    printed = capsys.readouterr().out

    assert exit_code == 0
    assert printed == f'Nothing to fix in {folder}: no secret, no key file, no personal address found.\n'


def test_main_takes_a_personal_address_to_look_at_and_a_mailbox_for_nothing(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A personal e-mail address in a file is one to look at, exit code 3, shown masked; a generic
    mailbox, an example's address and GitHub's private one are no finding.
    """
    folder = tmp_path / 'Pérez, Ana (2021)'
    _write(
        folder / 'README.md',
        '\n'.join([
            f'Written by {PERSONAL_ADDRESS}.',
            'Questions to support@fcf-screen.org or lab@kaxanuk.mx.',
            'Examples write to sofia@example.com, ana@mail.test or 12345+sofia@users.noreply.github.com.',
            '',
        ]),
    )
    exit_code = security_check.main([str(folder)])
    printed = capsys.readouterr().out

    assert exit_code == 3
    assert 'Look at (1):' in printed
    assert 'README.md:1  a personal e-mail address, so…@gmail.com' in printed
    assert PERSONAL_ADDRESS not in printed


def test_mask_shows_four_characters_and_the_length() -> None:
    """
    A value is shown by its first four characters and its length, never more.
    """
    assert security_check.mask('Pérez, Ana (2021)') == 'Pére… (17 characters)'


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
    Run git as a newcomer's: a home folder of the test's own, no system or global settings, such as
    a global ignore file, and an identity for a commit.
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


def _notebook(
    outputs: list[dict],
) -> str:
    """
    A notebook of one code cell, saved with the outputs given.
    """
    notebook = {
        'cells': [
            {
                'cell_type': 'code',
                'outputs': outputs,
                'source': ['print("Sofía")'],
            },
        ],
        'nbformat': 4,
    }

    return json.dumps(notebook)


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
