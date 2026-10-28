"""
The harness's own rules, in tools/: the Markdown rules, the version order, how a shared file of the
strategy template and its example is compared, the sentence a release's tag quotes, and which APM
lines are a warning.
"""
import pathlib
import subprocess

import check
import install_check
import release

__all__ = []

CHANGELOG = '\n'.join([
    '# Changelog for KaxaNuk-Researcher',
    '',
    '## [1.24.0] - 2026-10-27',
    'The package now carries its own checks, in one command, and releases itself from dev to',
    'main.',
    '',
    '**What to do differently:** nothing.',
    '',
    '## [1.23.2] - 2026-10-27',
    'An older entry.',
    '',
])


def test_a_long_line_tab_or_section_sign_in_added_lines_is_a_problem() -> None:
    """
    An added line over 100 columns, a literal tab and the section sign are each named.
    """
    text = '\n'.join([
        'a' * 101,
        'a\ttab',
        'see \N{SECTION SIGN} 3',
        'fine',
    ])
    problems = check.markdown_problems(
        'notes.md',
        text,
        {
            1,
            2,
            3,
            4,
        },
    )

    assert problems == [
        'notes.md:1: 101 columns, over 100',
        'notes.md:2: a literal tab',
        'notes.md:3: the section sign; write "section"',
    ]


def test_a_long_line_where_agents_md_allows_one_is_no_problem() -> None:
    """
    A table row, a line with a link or URL, the frontmatter, a fenced block and a strategy's record
    may run past 100 columns.
    """
    long_text = 'x' * 120
    text = '\n'.join([
        '---',
        f'description: {long_text}',
        '---',
        f'| a table row {long_text} |',
        f'a link [here](https://example.com/{long_text})',
        '```text',
        long_text,
        '```',
        '',
    ])
    problems = check.markdown_problems(
        'notes.md',
        text,
        set(range(1, 9)),
    )
    record_problems = check.markdown_problems(
        'Experiments/Experiment_1/JOURNAL_1.md',
        long_text,
        {1},
    )

    assert problems == []
    assert record_problems == []


def test_apm_notices_are_no_warning_but_any_other_flagged_line_is() -> None:
    """
    APM's notice of a newer version is expected; a warning about the package is not.
    """
    completed = subprocess.CompletedProcess(
        args=['apm'],
        returncode=0,
        stdout='\n'.join([
            '[!] A new version of APM is available: 0.35.0 (current: 0.33.0)',
            '[!] skill backup replaced by another package',
            '[*] Installed 1 APM dependency',
        ]),
        stderr='',
    )
    warnings = install_check._warnings(
        completed,
        install_check.PROJECT_NOTICES,
    )

    assert warnings == ['APM warned: [!] skill backup replaced by another package']


def test_changelog_is_compared_up_to_its_first_entry(
    tmp_path: pathlib.Path,
) -> None:
    """
    A CHANGELOG's entries are each copy's own: only what comes before the first one is compared.
    """
    path = tmp_path / 'CHANGELOG.md'
    path.write_text(
        '\n'.join([
            '# Changelog',
            '',
            'Every notable change.',
            '',
            '## 0.17.9 (2026-10-27)',
            'An entry of its own.',
        ]),
        encoding='utf-8',
    )
    lines = check._comparable_lines(
        'CHANGELOG.md',
        path,
        is_template=False,
    )

    assert lines == [
        '# Changelog',
        'Every notable change.',
    ]


def test_hunks_name_each_place_two_copies_differ() -> None:
    """
    Each difference is the template's lines there and the example's, nothing for equal copies.
    """
    hunks = check._hunks(
        [
            'same',
            'template only',
            'same again',
        ],
        [
            'same',
            'example only',
            'same again',
        ],
    )
    no_hunks = check._hunks(
        ['same'],
        ['same'],
    )

    assert hunks == [
        {
            'example': ['example only'],
            'template': ['template only'],
        },
    ]
    assert no_hunks == []


def test_marked_lines_are_left_out_markers_too() -> None:
    """
    The lines between an example's begin and end markers, and the markers, are the example's own.
    """
    lines = [
        'shared',
        '<!-- example: begin -->',
        'the example only',
        '<!-- example: end -->',
        'shared again',
        '# --- example: begin ---',
        'more of its own',
        '# --- example: end ---',
    ]

    assert check._unmarked_lines(lines) == [
        'shared',
        'shared again',
    ]


def test_objective_template_body_and_agents_banner_are_left_out(
    tmp_path: pathlib.Path,
) -> None:
    """
    The template's OBJECTIVE body, up to the rule that closes it, and its AGENTS.md status banner
    are what the example replaces.
    """
    objective = tmp_path / 'OBJECTIVE.md'
    objective.write_text(
        '\n'.join([
            '# Objective',
            '## The main idea',
            '*What belongs here.*',
            '---',
            '## The five parts',
        ]),
        encoding='utf-8',
    )
    agents = tmp_path / 'AGENTS.md'
    agents.write_text(
        '\n'.join([
            '# Agents',
            '> **Status: the template.** No strategy yet.',
            '> Replace this banner.',
            'Rules.',
        ]),
        encoding='utf-8',
    )

    assert check._comparable_lines(
        'OBJECTIVE.md',
        objective,
        is_template=True,
    ) == [
        '# Objective',
        '---',
        '## The five parts',
    ]
    assert check._comparable_lines(
        'AGENTS.md',
        agents,
        is_template=True,
    ) == [
        '# Agents',
        'Rules.',
    ]


def test_opening_sentence_joins_the_entry_first_paragraph() -> None:
    """
    The sentence a release's tag quotes is the newest entry's first paragraph, its lines joined.
    """
    sentence = release.opening_sentence(CHANGELOG)

    assert sentence == ' '.join([
        'The package now carries its own checks, in one command, and releases itself from dev to',
        'main.',
    ])


def test_private_words_are_found_case_aside() -> None:
    """
    A private word is found in any case; a text without one is not flagged.
    """
    words = [
        'Secretname',
        'D:/Private',
    ]

    assert check._holds_any(
        'see d:/private/notes',
        words,
    )
    assert not check._holds_any(
        'nothing here',
        words,
    )


def test_release_tag_and_message_follow_the_version() -> None:
    """
    A release of 1.24.0 is tagged v1.24.0, its message the version and the sentence.
    """
    planned = release.Release(
        commit='0' * 40,
        sentence='The package now checks itself.',
        version='1.24.0',
    )

    assert planned.tag == 'v1.24.0'
    assert planned.tag_message == '1.24.0: The package now checks itself.'


def test_version_key_orders_versions_by_number() -> None:
    """
    1.10.0 comes after 1.9.2, which a comparison of the text would get wrong.
    """
    assert check.version_key('1.10.0') > check.version_key('1.9.2')
    assert check.version_key('1.23.2') == [
        1,
        23,
        2,
    ]
