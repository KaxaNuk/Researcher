"""
Tests of user_targets.py, the init-researcher skill's script: it keeps the assistant in use on APM's
list in `~/.apm/apm.yml`, so that the next install or update keeps that assistant's files, and checks
that the package and the researcher are on disk for it.
"""
import functools
import pathlib

import pytest

import user_targets

__all__ = []

# The files the check looks for, from the user's home folder, for a researcher named Sofía, as the
# script's docstring lists them for each assistant.
EXPECTED_FILES = {
    'claude': [
        '.claude/skills/next/SKILL.md',
        '.claude/skills/sofia/SKILL.md',
        '.claude/agents/sofia.md',
    ],
    'codex': [
        '.agents/skills/next/SKILL.md',
        '.agents/skills/sofia/SKILL.md',
        '.codex/agents/sofia.toml',
    ],
    'copilot': [
        '.agents/skills/next/SKILL.md',
        '.agents/skills/sofia/SKILL.md',
        '.copilot/agents/sofia.agent.md',
    ],
    'cursor': [
        '.agents/skills/next/SKILL.md',
        '.agents/skills/sofia/SKILL.md',
        '.cursor/agents/sofia.md',
    ],
    'gemini': [
        '.agents/skills/next/SKILL.md',
        '.agents/skills/sofia/SKILL.md',
    ],
    'opencode': [
        '.config/opencode/skills/next/SKILL.md',
    ],
    'windsurf': [
        '.agents/skills/next/SKILL.md',
        '.agents/skills/sofia/SKILL.md',
    ],
}
# A manifest as APM writes it at user scope, naming the one assistant of its first install, and the
# same manifest once codex is added: every other line as it was, the dependency's list untouched.
MANIFEST_WITH_CLAUDE = '\n'.join([
    'name: sofia-perez',
    'version: 1.0.0',
    'targets:',
    '  - claude  # the first install named it',
    'dependencies:',
    '  apm:',
    '    - KaxaNuk/KaxaNuk-Researcher',
    '',
])
MANIFEST_WITH_CLAUDE_AND_CODEX = '\n'.join([
    'name: sofia-perez',
    'version: 1.0.0',
    'targets:',
    '  - claude  # the first install named it',
    '  - codex',
    'dependencies:',
    '  apm:',
    '    - KaxaNuk/KaxaNuk-Researcher',
    '',
])
# The researcher's name as its files take it: `sofia` for Sofía.
SLUG = 'sofia'


@pytest.mark.parametrize(
    'manifest_text',
    [
        'name: sofia-perez\ndependencies:\n  apm:\n    - KaxaNuk/KaxaNuk-Researcher\n',
        'dependencies:\n  apm:\n    - git: KaxaNuk/KaxaNuk-Researcher\n      targets:\n        - claude\n',
    ],
    ids=[
        'no list',
        "a dependency's own list",
    ],
)
def test_add_target_changes_nothing_in_a_manifest_without_a_list(
    capsys: pytest.CaptureFixture[str],
    manifest_text: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A manifest that names no assistants, at the start of a line, lets APM install for every
    assistant whose folder exists and delete nothing: it stays as it was, and that is no failure.
    """
    manifest = _manifest(
        tmp_path,
        manifest_text,
    )
    exit_code = user_targets.add_target(
        manifest,
        'codex',
    )

    assert exit_code == 0
    assert manifest.read_bytes() == manifest_text.encode('utf-8')
    assert 'names no assistants' in capsys.readouterr().out


def test_add_target_changes_nothing_when_already_listed(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    Adding an assistant twice lists it once: the second run says so and leaves the file as it was.
    """
    manifest = _manifest(
        tmp_path,
        MANIFEST_WITH_CLAUDE,
    )
    first_run = user_targets.add_target(
        manifest,
        'codex',
    )
    after_first_run = manifest.read_bytes()
    second_run = user_targets.add_target(
        manifest,
        'codex',
    )
    printed = capsys.readouterr().out

    assert first_run == 0
    assert after_first_run == MANIFEST_WITH_CLAUDE_AND_CODEX.encode('utf-8')
    assert second_run == 0
    assert manifest.read_bytes() == after_first_run
    assert f'codex is already listed in {manifest}; nothing changed.' in printed


@pytest.mark.parametrize(
    ('before', 'after'),
    [
        (MANIFEST_WITH_CLAUDE, MANIFEST_WITH_CLAUDE_AND_CODEX),
        (
            MANIFEST_WITH_CLAUDE.replace('\n', '\r\n'),
            MANIFEST_WITH_CLAUDE_AND_CODEX.replace('\n', '\r\n'),
        ),
        ("targets:\n- 'claude'\n- gemini\nname: sofia\n", "targets:\n- 'claude'\n- gemini\n- codex\nname: sofia\n"),
        ('targets:\n- claude', 'targets:\n- claude\n- codex'),
        ('targets: [claude, gemini]  # APM wrote it\n', 'targets: [claude, gemini, codex]  # APM wrote it\n'),
        ('target: claude\r\n', 'target: [claude, codex]\r\n'),
    ],
    ids=[
        'block list',
        'block list with CRLF',
        'block list with a quoted name',
        'block list ending the file without a line ending',
        'list in brackets with a comment',
        'one name under target',
    ],
)
def test_add_target_puts_the_assistant_last_on_the_list(
    after: str,
    before: str,
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    The assistant goes last on the list, every other line as it was: a line of its own after the last
    of a block list, indented and ended as that one, or the list in brackets on the key's line, its
    comment kept; one name under `target:` becomes a list in brackets.
    """
    manifest = _manifest(
        tmp_path,
        before,
    )
    exit_code = user_targets.add_target(
        manifest,
        'codex',
    )

    assert exit_code == 0
    assert manifest.read_bytes() == after.encode('utf-8')
    assert f'Added codex to {manifest}' in capsys.readouterr().out


@pytest.mark.parametrize(
    'manifest_text',
    [
        'targets: [claude,\n  gemini]\n',
        'targets: []\n',
        'targets:\nname: sofia\n',
        'targets:\n- claude\ntarget: gemini\n',
    ],
    ids=[
        'brackets over two lines',
        'brackets with no name',
        'a key with no name below it',
        'a list named twice',
    ],
)
def test_add_target_refuses_a_list_it_cannot_read(
    capsys: pytest.CaptureFixture[str],
    manifest_text: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A list in brackets over several lines, a list with no names, or a list named twice is left as it
    was, exit code 1, so that the install that follows is not run against a list it cannot trust.
    """
    manifest = _manifest(
        tmp_path,
        manifest_text,
    )
    exit_code = user_targets.add_target(
        manifest,
        'codex',
    )

    assert exit_code == 1
    assert manifest.read_bytes() == manifest_text.encode('utf-8')
    assert capsys.readouterr().out.startswith('Nothing changed:')


def test_add_target_refuses_a_missing_manifest(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    A manifest not made yet, which the package's install creates, is not made here: exit code 1.
    """
    manifest = tmp_path / 'Pérez, Sofía (2021)' / '.apm' / 'apm.yml'
    exit_code = user_targets.add_target(
        manifest,
        'codex',
    )

    assert exit_code == 1
    assert not manifest.exists()
    assert "the package's install creates it" in capsys.readouterr().out


def test_check_target_fails_when_the_list_leaves_the_assistant_out(
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
) -> None:
    """
    Every file on disk is not enough when the manifest lists other assistants and not this one: the
    next install or update would delete its files, so the check fails and says what to run.
    """
    home = tmp_path / 'Pérez, Sofía (2021)'
    _manifest(
        home,
        MANIFEST_WITH_CLAUDE,
    )
    _write_expected_files(
        home,
        'codex',
    )
    exit_code = user_targets.check_target(
        home,
        'codex',
        SLUG,
    )
    printed = capsys.readouterr().out

    assert exit_code == 1
    assert 'lists claude and not codex' in printed
    assert 'run `user_targets.py add codex` first' in printed


@pytest.mark.parametrize(
    'target',
    sorted(user_targets.SKILL_FOLDERS),
)
def test_check_target_passes_with_every_file_and_names_a_missing_one(
    capsys: pytest.CaptureFixture[str],
    target: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    For each assistant, the check passes once every file it expects is on disk and the manifest lists
    the assistant, and fails, naming the file, once one is missing.
    """
    home = tmp_path / 'Pérez, Sofía (2021)'
    _manifest(
        home,
        f'targets:\n- {target}\n',
    )
    written = _write_expected_files(
        home,
        target,
    )
    installed = user_targets.check_target(
        home,
        target,
        SLUG,
    )
    printed_installed = capsys.readouterr().out
    written[-1].unlink()
    missing_one = user_targets.check_target(
        home,
        target,
        SLUG,
    )
    printed_missing = capsys.readouterr().out

    assert installed == 0
    assert f'installed for {target}.' in printed_installed
    assert missing_one == 1
    assert f'Missing: {written[-1]} - ' in printed_missing
    assert f'Not installed for {target}.' in printed_missing


@pytest.mark.parametrize(
    'target',
    sorted(EXPECTED_FILES),
)
def test_expected_files_are_where_apm_puts_them(
    target: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    The check looks for the package's `next` skill, then the researcher's skill and agent, where APM
    puts them for each assistant; OpenCode takes the package alone, and Gemini and Windsurf no agent.
    """
    expected = user_targets.expected_files(
        tmp_path,
        target,
        SLUG,
    )
    relative_paths = [
        expected_file.path.relative_to(tmp_path).as_posix()
        for expected_file in expected
    ]

    assert relative_paths == EXPECTED_FILES[target]


def test_main_adds_to_the_list_and_checks_in_the_home_folder(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """
    From the command line, `add` reads the manifest in the `.apm` folder of the user's home folder,
    and `check` looks there for the researcher's files.
    """
    home = tmp_path / 'Pérez, Sofía (2021)'
    manifest = _manifest(
        home,
        MANIFEST_WITH_CLAUDE,
    )
    _use_home(
        monkeypatch,
        home,
    )
    _write_expected_files(
        home,
        'codex',
    )
    added = user_targets.main([
        'add',
        'codex',
    ])
    checked = user_targets.main([
        'check',
        'codex',
        SLUG,
    ])
    printed = capsys.readouterr().out

    assert added == 0
    assert manifest.read_bytes() == MANIFEST_WITH_CLAUDE_AND_CODEX.encode('utf-8')
    assert checked == 0
    assert 'The researcher, sofia, is installed for codex.' in printed


@pytest.mark.parametrize(
    'slug',
    [
        'Sofía',
        'sofia perez',
        'sofia--perez',
        'sofia-',
        'Sofia',
    ],
)
def test_main_refuses_a_slug_that_is_not_one(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    slug: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    A researcher's name as typed, with an accent, a space or a capital, is no slug: the command line
    is refused, exit code 2, and nothing is looked for.
    """
    _use_home(
        monkeypatch,
        tmp_path,
    )

    with pytest.raises(SystemExit) as raised:
        user_targets.main([
            'check',
            'claude',
            slug,
        ])

    assert raised.value.code == 2
    assert 'is not a slug' in capsys.readouterr().err


def _manifest(
    home: pathlib.Path,
    text: str,
) -> pathlib.Path:
    """
    Write the user's APM manifest in a home folder of the test's own, its line endings as given.
    """
    manifest = home / user_targets.MANIFEST_FILE
    manifest.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    manifest.write_bytes(text.encode('utf-8'))

    return manifest


def _use_home(
    monkeypatch: pytest.MonkeyPatch,
    home: pathlib.Path,
) -> None:
    """
    Make a folder of the test's own the user's home folder, however the script asks for it.
    """
    monkeypatch.setenv('HOME', str(home))
    monkeypatch.setenv('USERPROFILE', str(home))
    monkeypatch.setattr(
        pathlib.Path,
        'home',
        functools.partial(
            pathlib.Path,
            home,
        ),
    )


def _write_expected_files(
    home: pathlib.Path,
    target: str,
) -> list[pathlib.Path]:
    """
    Put every file the check expects for the assistant in the home folder, as an install would.
    """
    expected = user_targets.expected_files(
        home,
        target,
        SLUG,
    )
    written = [
        expected_file.path
        for expected_file in expected
    ]

    for path in written:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        path.write_bytes(b'---\nname: sofia\n---\n')

    return written
