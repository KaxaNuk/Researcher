"""
Concept pages brought up to date from a spec, update_concept_pages.py: what each part of a block adds
and where, what a page already holds is skipped, and nothing is written without --write, or when any
page of the spec cannot take its block.
"""
import io
import pathlib
import sys

import pytest

import update_concept_pages

__all__ = []

DATE = '2026-10-27'
PAGE = '\n'.join([
    '---',
    'type: concept',
    'updated: 2026-09-11',
    'sources:',
    '  - Pérez_2021_Señales.md',
    'tags: [momentum]',
    '---',
    '',
    '# Señales de momentum',
    '',
    'A momentum signal, as the library holds it today.',
    '',
    '## What the sources say',
    '',
    '- Winners keep winning for a year',
    '  ([Pérez 2021, p. 3](Pérez_2021_Señales.md)).',
    '',
    '> [!WARNING]',
    '> Where two sources disagree, both claims stay.',
    '',
    "## For the owner's questions",
    '',
    '> **Question 1:** the signal is worth testing.',
    '',
    '## Open',
    '',
    '- What momentum costs to trade.',
    '',
])
PAGE_PATH = 'Finance/Señales_de_momentum.md'
SPEC = '\n'.join([
    '@@FILE Finance/Señales_de_momentum.md',
    '@@SOURCES',
    'García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
    '@@BULLETS',
    '- Calm follows calm, so size by volatility',
    '  ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
    '@@QUOTE',
    "> **Question 2:** volatility sizing keeps the signal's Sharpe ratio.",
    '@@OPEN',
    '- Whether volatility sizing survives costs.',
    '@@END',
    '',
])
SYNTHESIS_PAGE = '\n'.join([
    '---',
    'type: synthesis',
    'updated: 2026-09-11',
    'sources:',
    '  - Pérez_2021_Señales.md',
    '---',
    '',
    '# ¿Qué dice la biblioteca?',
    '',
    '## Open',
    '',
    '- What momentum costs to trade.',
    '',
])
SYNTHESIS_PATH = 'Finance/Qué_dice_la_biblioteca.md'
UPDATED_PAGE = '\n'.join([
    '---',
    'type: concept',
    'updated: 2026-10-27',
    'sources:',
    '  - Pérez_2021_Señales.md',
    '  - García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
    'tags: [momentum]',
    '---',
    '',
    '# Señales de momentum',
    '',
    'A momentum signal, as the library holds it today.',
    '',
    '## What the sources say',
    '',
    '- Winners keep winning for a year',
    '  ([Pérez 2021, p. 3](Pérez_2021_Señales.md)).',
    '- Calm follows calm, so size by volatility',
    '  ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
    '',
    '> [!WARNING]',
    '> Where two sources disagree, both claims stay.',
    '',
    "## For the owner's questions",
    '',
    '> **Question 1:** the signal is worth testing.',
    '',
    "> **Question 2:** volatility sizing keeps the signal's Sharpe ratio.",
    '',
    '## Open',
    '',
    '- What momentum costs to trade.',
    '- Whether volatility sizing survives costs.',
    '',
])


def test_apply_edit_adds_each_part_where_the_page_holds_it() -> None:
    """
    `updated` takes the date; a source joins the sources list, a claim follows the last claim before
    the callout, a quote ends the questions' section after a blank line, a line ends Open.
    """
    edits = update_concept_pages.parse_spec(SPEC)
    updated = update_concept_pages.apply_edit(
        PAGE,
        edits[0],
        DATE,
    )

    assert updated == UPDATED_PAGE


def test_apply_edit_adds_updated_after_type_when_the_page_has_none() -> None:
    """
    A page with no `updated` gets one after its `type`, and a block with no part changes nothing else.
    """
    undated = PAGE.replace(
        'updated: 2026-09-11\n',
        '',
    )
    bare = update_concept_pages.parse_spec(f'@@FILE {PAGE_PATH}\n')
    dated = update_concept_pages.apply_edit(
        undated,
        bare[0],
        DATE,
    )

    assert dated == PAGE.replace(
        'updated: 2026-09-11',
        'updated: 2026-10-27',
    )


def test_apply_edit_refuses_a_page_without_the_frontmatter_or_the_section_a_part_needs() -> None:
    """
    A page with no frontmatter, no sources field or no Open section cannot take a block that adds to
    them, and the edit says which.
    """
    edit = update_concept_pages.parse_spec(SPEC)[0]
    no_frontmatter = PAGE.replace(
        '---\n',
        '',
        1,
    )
    no_sources = PAGE.replace(
        'sources:\n  - Pérez_2021_Señales.md\n',
        '',
    )
    no_open = PAGE.replace(
        '## Open\n\n- What momentum costs to trade.\n',
        '',
    )

    assert _edit_problem(no_frontmatter, edit) == 'Finance/Señales_de_momentum.md has no frontmatter'
    assert _edit_problem(no_sources, edit) == 'Finance/Señales_de_momentum.md has no sources field in its frontmatter'
    assert _edit_problem(no_open, edit).startswith('Finance/Señales_de_momentum.md has no section headed as')


def test_apply_edit_rewrites_an_inline_sources_list_as_a_block_list() -> None:
    """
    A sources list written inline becomes a block list once a note joins it; a note already in it,
    quoted or not, is skipped.
    """
    inline = PAGE.replace(
        'sources:\n  - Pérez_2021_Señales.md\n',
        'sources: [Pérez_2021_Señales.md, "Ruiz_2020_Momentum.md"]\n',
    )
    spec = '\n'.join([
        f'@@FILE {PAGE_PATH}',
        '@@SOURCES',
        '- "Ruiz_2020_Momentum.md"',
        'García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
        '@@END',
    ])
    updated = update_concept_pages.apply_edit(
        inline,
        update_concept_pages.parse_spec(spec)[0],
        DATE,
    )

    assert updated.splitlines()[:9] == [
        '---',
        'type: concept',
        'updated: 2026-10-27',
        'sources:',
        '  - Pérez_2021_Señales.md',
        '  - Ruiz_2020_Momentum.md',
        '  - García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
        'tags: [momentum]',
        '---',
    ]


def test_apply_edit_skips_what_the_page_already_holds() -> None:
    """
    A source, a claim word for word, a quote and an Open line the page holds already are skipped:
    the block applied twice gives the page it gave once.
    """
    edit = update_concept_pages.parse_spec(SPEC)[0]
    again = update_concept_pages.apply_edit(
        UPDATED_PAGE,
        edit,
        DATE,
    )

    assert again == UPDATED_PAGE


def test_main_exits_one_on_a_date_or_a_folder_it_cannot_take(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A date that is not YYYY-MM-DD, and a Knowledge folder that is not there, are usage mistakes: exit
    1, nothing written.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: PAGE,
        },
    )
    spec = _write_spec(
        tmp_path,
        SPEC,
    )

    with pytest.raises(SystemExit) as bad_date:
        update_concept_pages.main([
            *_arguments(spec, knowledge),
            '--date',
            '27/10/2026',
        ])

    with pytest.raises(SystemExit) as no_folder:
        update_concept_pages.main(_arguments(spec, tmp_path / 'Conocimiento'))

    captured = capsys.readouterr()

    assert bad_date.value.code == 1
    assert no_folder.value.code == 1
    assert '--date 27/10/2026 is not YYYY-MM-DD' in captured.err
    assert 'no such folder' in captured.err
    assert _read(knowledge / PAGE_PATH) == PAGE


def test_main_reads_the_spec_from_standard_input(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    `-` reads the spec from standard input, as the read skill pipes it, never a file in the library.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: PAGE,
        },
    )
    monkeypatch.setattr(
        sys,
        'stdin',
        io.StringIO(SPEC),
    )
    exit_code = update_concept_pages.main([
        '-',
        '--knowledge',
        str(knowledge),
        '--date',
        DATE,
        '--write',
    ])

    assert exit_code == 0
    assert _read(knowledge / PAGE_PATH) == UPDATED_PAGE


def test_main_with_write_writes_each_page_as_utf8_with_lf_endings(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    With --write, a page saved with a byte order mark and CRLF endings, as a Windows editor may save
    it, is written as UTF-8 with LF endings, and the run says so.
    """
    knowledge = _knowledge(
        tmp_path,
        {},
    )
    windows_page = '﻿' + PAGE.replace('\n', '\r\n')
    (knowledge / 'Finance').mkdir()
    (knowledge / PAGE_PATH).write_bytes(windows_page.encode('utf-8'))
    spec = _write_spec(
        tmp_path,
        SPEC,
    )
    exit_code = update_concept_pages.main([
        *_arguments(spec, knowledge),
        '--write',
    ])
    lines = capsys.readouterr().out.splitlines()
    written = (knowledge / PAGE_PATH).read_bytes()

    assert exit_code == 0
    assert written == UPDATED_PAGE.encode('utf-8')
    assert lines == [
        'updated Knowledge/Finance/Señales_de_momentum.md',
        '1 page written, 0 holding everything already',
    ]


def test_main_without_write_prints_the_diff_and_writes_nothing(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Without --write, the run prints the diff of every page it would change and leaves every page as
    it was, byte for byte.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: PAGE,
        },
    )
    spec = _write_spec(
        tmp_path,
        SPEC,
    )
    before = (knowledge / PAGE_PATH).read_bytes()
    exit_code = update_concept_pages.main(_arguments(spec, knowledge))
    lines = capsys.readouterr().out.splitlines()
    after = (knowledge / PAGE_PATH).read_bytes()

    assert exit_code == 0
    assert after == before
    assert lines[:2] == [
        '--- a/Knowledge/Finance/Señales_de_momentum.md',
        '+++ b/Knowledge/Finance/Señales_de_momentum.md',
    ]
    assert '-updated: 2026-09-11' in lines
    assert '+updated: 2026-10-27' in lines
    assert '+- Whether volatility sizing survives costs.' in lines
    assert lines[-1] == '1 page to change, 0 holding everything already'


def test_main_writes_nothing_when_one_page_cannot_be_updated(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Every page is checked before any is written: a block for a page that is not a concept page stops
    the run with exit 1, and the page an earlier block changed stays as it was.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: PAGE,
            SYNTHESIS_PATH: SYNTHESIS_PAGE,
        },
    )
    spec = _write_spec(
        tmp_path,
        '\n'.join([
            SPEC,
            f'@@FILE {SYNTHESIS_PATH}',
            '@@OPEN',
            '- A gap the synthesis names.',
            '',
        ]),
    )
    exit_code = update_concept_pages.main([
        *_arguments(spec, knowledge),
        '--write',
    ])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.err == ''.join([
        'nothing written: spec line 13: Finance/Qué_dice_la_biblioteca.md is not a concept page',
        ' — its type is synthesis\n',
    ])
    assert _read(knowledge / PAGE_PATH) == PAGE
    assert _read(knowledge / SYNTHESIS_PATH) == SYNTHESIS_PAGE


def test_parse_spec_reads_each_block_and_its_parts() -> None:
    """
    Each @@FILE opens a block that runs to @@END, to the next @@FILE or to the end; each part keeps
    its lines, blank ones at either end trimmed, and a source loses its list mark and its quotes.
    """
    spec = '\n'.join([
        SPEC,
        '@@FILE Finance/Otra página, (2).md',
        '@@SOURCES',
        '',
        '- "Pérez_2021_Señales.md"',
        '',
        '@@OPEN',
        '- A gap.',
    ])

    assert update_concept_pages.parse_spec(spec) == [
        update_concept_pages.PageEdit(
            bullets=[
                '- Calm follows calm, so size by volatility',
                '  ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
            ],
            file=PAGE_PATH,
            line=1,
            open_lines=['- Whether volatility sizing survives costs.'],
            quote=["> **Question 2:** volatility sizing keeps the signal's Sharpe ratio."],
            sources=['García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md'],
        ),
        update_concept_pages.PageEdit(
            bullets=[],
            file='Finance/Otra página, (2).md',
            line=13,
            open_lines=['- A gap.'],
            quote=[],
            sources=['Pérez_2021_Señales.md'],
        ),
    ]


def test_parse_spec_refuses_a_spec_it_cannot_read() -> None:
    """
    An unknown marker, text before the first @@FILE or before a block's first part, a @@FILE naming
    no page, and a spec naming none, each stop the run with the line to fix.
    """
    problems = [
        _spec_problem(spec)
        for spec
        in [
            f'@@FILE {PAGE_PATH}\n@@NOTE\n- A gap.\n',
            f'A stray line\n@@FILE {PAGE_PATH}\n@@OPEN\n- A gap.\n',
            f'@@FILE {PAGE_PATH}\nloose text\n@@OPEN\n- A gap.\n',
            '@@FILE\n@@OPEN\n- A gap.\n',
            '\n\n',
        ]
    ]

    assert problems == [
        'line 2: @@NOTE is not a marker',
        'line 1: the spec opens with no @@FILE',
        'spec line 2: text before any @@SOURCES, @@BULLETS, @@QUOTE or @@OPEN',
        'spec line 1: @@FILE names no page',
        'the spec names no page: it needs @@FILE <path under Knowledge/>',
    ]


def test_updated_pages_applies_two_blocks_on_one_page_in_order(
    tmp_path: pathlib.Path,
) -> None:
    """
    Two blocks for one page apply in order, the second to what the first made, and the page's text
    before both is kept as its original.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: PAGE,
        },
    )
    spec = '\n'.join([
        f'@@FILE {PAGE_PATH}',
        '@@SOURCES',
        'García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
        '@@BULLETS',
        '- Calm follows calm, so size by volatility',
        '  ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
        f'@@FILE {PAGE_PATH}',
        '@@QUOTE',
        "> **Question 2:** volatility sizing keeps the signal's Sharpe ratio.",
        '@@OPEN',
        '- Whether volatility sizing survives costs.',
    ])
    changed = update_concept_pages.updated_pages(
        knowledge,
        update_concept_pages.parse_spec(spec),
        DATE,
    )

    assert changed == {
        knowledge / PAGE_PATH: update_concept_pages.PageText(
            original=PAGE,
            updated=UPDATED_PAGE,
        ),
    }


def test_updated_pages_leaves_out_a_page_that_already_holds_everything(
    tmp_path: pathlib.Path,
) -> None:
    """
    A page that holds every part of its block already, dated today, is not among the pages to change.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            PAGE_PATH: UPDATED_PAGE,
        },
    )
    changed = update_concept_pages.updated_pages(
        knowledge,
        update_concept_pages.parse_spec(SPEC),
        DATE,
    )

    assert changed == {}


def test_updated_pages_refuses_a_page_it_cannot_update(
    tmp_path: pathlib.Path,
) -> None:
    """
    A page that is not a concept page, one that is not there — a new page is written whole — a path
    out of Knowledge/ and a file that is not markdown are each refused, with the spec's line.
    """
    knowledge = _knowledge(
        tmp_path,
        {
            SYNTHESIS_PATH: SYNTHESIS_PAGE,
        },
    )
    problems = [
        _update_problem(
            knowledge,
            f'@@FILE {page}\n@@OPEN\n- A gap.\n',
        )
        for page
        in [
            SYNTHESIS_PATH,
            'Finance/No_existe, (aún).md',
            '../Fuera.md',
            'Finance/Notas.txt',
        ]
    ]

    assert problems == [
        'spec line 1: Finance/Qué_dice_la_biblioteca.md is not a concept page — its type is synthesis',
        'spec line 1: Finance/No_existe, (aún).md is not there; a new page is written whole, never here',
        'spec line 1: ../Fuera.md is not a path under Knowledge/',
        'spec line 1: Finance/Notas.txt is not a markdown page',
    ]


def _arguments(
    spec: pathlib.Path,
    knowledge: pathlib.Path,
) -> list[str]:
    """
    The command line for a spec file and a Knowledge folder, dated as the tests date every page.
    """
    arguments = [
        str(spec),
        '--knowledge',
        str(knowledge),
        '--date',
        DATE,
    ]

    return arguments


def _edit_problem(
    page: str,
    edit: update_concept_pages.PageEdit,
) -> str:
    """
    What apply_edit says of a page that cannot take a block.
    """
    with pytest.raises(update_concept_pages.EditProblem) as refused:
        update_concept_pages.apply_edit(
            page,
            edit,
            DATE,
        )

    problem = str(refused.value)

    return problem


def _knowledge(
    folder: pathlib.Path,
    pages: dict[str, str],
) -> pathlib.Path:
    """
    A home's Knowledge/ folder holding these pages, by their path under it.
    """
    knowledge = folder / 'Knowledge'
    knowledge.mkdir()

    for relative, text in pages.items():
        page_path = knowledge / relative
        page_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        page_path.write_text(
            text,
            encoding='utf-8',
            newline='\n',
        )

    return knowledge


def _read(
    path: pathlib.Path,
) -> str:
    """
    A page's text as UTF-8.
    """
    text = path.read_text(encoding='utf-8')

    return text


def _spec_problem(
    spec: str,
) -> str:
    """
    What parse_spec says of a spec it cannot read.
    """
    with pytest.raises(update_concept_pages.EditProblem) as refused:
        update_concept_pages.parse_spec(spec)

    problem = str(refused.value)

    return problem


def _update_problem(
    knowledge: pathlib.Path,
    spec: str,
) -> str:
    """
    What updated_pages says of a block whose page it cannot update.
    """
    with pytest.raises(update_concept_pages.EditProblem) as refused:
        update_concept_pages.updated_pages(
            knowledge,
            update_concept_pages.parse_spec(spec),
            DATE,
        )

    problem = str(refused.value)

    return problem


def _write_spec(
    folder: pathlib.Path,
    text: str,
) -> pathlib.Path:
    """
    A spec file outside the library, as UTF-8.
    """
    spec = folder / 'spec, (borrador).txt'
    spec.write_text(
        text,
        encoding='utf-8',
        newline='\n',
    )

    return spec
