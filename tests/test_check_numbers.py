"""
The figures a note states, looked up on the pages it cites, check_numbers.py: how a note is split
and its citations and figures read, where a figure is found in an extract extract.py wrote, and the
offset of a note that cites printed pages.
"""
import pathlib

import pytest

import check_numbers
import extract

__all__ = []

LOCAL_COPY = 'Sources/Papers/Pérez, Ana (2021) Señales.pdf'


def test_check_note_finds_each_figure_on_its_page_elsewhere_or_nowhere(
    tmp_path: pathlib.Path,
) -> None:
    """
    A cited figure is on its page, elsewhere in the extract with the pages that hold it, or not
    found; a figure in a block with no citation is counted, not checked.
    """
    extracts = tmp_path / 'Extracts'
    _write_extract(
        extracts,
        12,
        [
            'The premium was 4.5% a year over 1927-2020.',
            'Its volatility was 18.2% a year.',
        ],
    )
    note = _write_note(
        tmp_path / 'Knowledge' / 'Finance' / 'Pérez_2021_Señales.md',
        LOCAL_COPY,
        [
            '# Pérez (2021) — Señales',
            '',
            '- The premium was 4.5% a year (p. 12).',
            '- Its volatility was 18.2% (p. 12).',
            '- The worst year lost 33.3% (p. 13).',
            '',
            'An uncited 77.7% that no citation backs.',
        ],
    )
    report = check_numbers.check_note(
        note,
        extracts,
    )

    assert report.unchecked_reason is None
    assert report.offset is None
    assert report.uncited_figures == 1
    assert _outcomes(report) == [
        '4.5% on page []',
        '18.2% elsewhere [13]',
        '33.3% not found []',
    ]


def test_check_note_finds_the_offset_of_a_note_that_cites_printed_pages(
    tmp_path: pathlib.Path,
) -> None:
    """
    Three lines whose figures sit two pages after the one cited make an offset: those figures are at
    offset, and one whose pages, shifted or not, are not in the extract is not extracted.
    """
    extracts = tmp_path / 'Extracts'
    _write_extract(
        extracts,
        12,
        [
            'A gain of 11.1% here.',
            'A gain of 22.2% here.',
            'A gain of 33.3% here.',
        ],
    )
    note = _write_note(
        tmp_path / 'Pérez_2021_Señales.md',
        LOCAL_COPY,
        [
            '- A gain of 11.1% (p. 10).',
            '- A gain of 22.2% (p. 11).',
            '- A gain of 33.3% (p. 12).',
            '- A gain of 44.4% (p. 30).',
        ],
    )
    report = check_numbers.check_note(
        note,
        extracts,
    )

    assert report.offset == 2
    assert _outcomes(report) == [
        '11.1% at offset [12]',
        '22.2% at offset [13]',
        '33.3% at offset [14]',
        '44.4% not extracted []',
    ]


def test_check_note_is_unchecked_without_a_pdf_or_its_extract(
    tmp_path: pathlib.Path,
) -> None:
    """
    A note with no local_copy, one whose copy is not a PDF, one whose extract is not on disk — with
    the command that regenerates it — and one whose extract has no page marker are unchecked.
    """
    extracts = tmp_path / 'Extracts'
    unmarked = extracts / 'Garcia_Luis_2019_Riesgo_2a_ed'
    unmarked.mkdir(parents=True)
    (unmarked / '01_Introducción.md').write_text(
        '# 1. Introducción\n\nText with no page marker.\n',
        encoding='utf-8',
    )
    local_copies = [
        'none',
        'Sources/Clippings/Recorte, (2020).md',
        LOCAL_COPY,
        'Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf',
    ]
    reports = [
        check_numbers.check_note(
            _write_note(
                tmp_path / f'Nota_{number}.md',
                local_copy,
                ['- A gain of 11.1% (p. 10).'],
            ),
            extracts,
        )
        for number, local_copy
        in enumerate(local_copies)
    ]
    reasons = [
        report.unchecked_reason
        for report
        in reports
    ]
    root = extracts.as_posix()

    assert reasons == [
        'no local_copy',
        'local_copy is not a PDF: Sources/Clippings/Recorte, (2020).md',
        ' '.join([
            f'no extract on disk at {root}/Perez_Ana_2021_Senales/; regenerate it with',
            f'uv run extract.py "{LOCAL_COPY}" --all --out "{root}"',
        ]),
        f'the extract in {root}/Garcia_Luis_2019_Riesgo_2a_ed/ has no page markers',
    ]


@pytest.mark.xfail(
    strict=True,
    reason=' '.join([
        'check_note and note_files read a note as plain UTF-8, so a byte order mark hides its',
        'frontmatter and the note is unchecked, no local_copy; library.py reads every file as',
        'utf-8-sig',
    ]),
)
def test_check_note_reads_a_note_saved_with_a_byte_order_mark(
    tmp_path: pathlib.Path,
) -> None:
    """
    A note saved with a byte order mark, as some Windows editors save one, is read like any other.
    """
    extracts = tmp_path / 'Extracts'
    _write_extract(
        extracts,
        12,
        ['The premium was 4.5% a year.'],
    )
    note = _write_note(
        tmp_path / 'Pérez_2021_Señales.md',
        LOCAL_COPY,
        ['- The premium was 4.5% a year (p. 12).'],
    )
    marked = b'\xef\xbb\xbf' + note.read_bytes()
    note.write_bytes(marked)
    report = check_numbers.check_note(
        note,
        extracts,
    )

    assert report.unchecked_reason is None
    assert _outcomes(report) == ['4.5% on page []']


def test_cited_pages_expand_ranges_and_lists() -> None:
    """
    `p. 7`, `p.93`, `pp. 12–13` with an en dash or a hyphen and `pp. 5, 9, 20-21` name their pages,
    ranges expanded; `app. 4` is no citation.
    """
    pages = check_numbers.cited_pages('As (p. 7), (p.93), pp. 12–13 and pp. 5, 9, 20-21, not app. 4.')

    assert pages == frozenset({
        5,
        7,
        9,
        12,
        13,
        20,
        21,
        93,
    })


def test_consistent_offset_needs_three_lines_and_most_of_them() -> None:
    """
    An offset is the one that at least three lines holding a figure found elsewhere share, when they
    are most of those lines.
    """
    offsets = {
        'no figure elsewhere': check_numbers.consistent_offset([]),
        'three at +2 and one at +5': check_numbers.consistent_offset(_outcomes_at([2] * 3 + [5])),
        'three at +2 and three at +5': check_numbers.consistent_offset(_outcomes_at([2] * 3 + [5] * 3)),
        'three at +2': check_numbers.consistent_offset(_outcomes_at([2] * 3)),
        'two at +2': check_numbers.consistent_offset(_outcomes_at([2] * 2)),
    }

    assert offsets == {
        'no figure elsewhere': None,
        'three at +2 and one at +5': 2,
        'three at +2 and three at +5': None,
        'three at +2': 2,
        'two at +2': None,
    }


def test_extract_slug_names_the_folder_extract_writes() -> None:
    """
    The extract of a local copy is looked for in the folder extract.py names for it, whichever way
    the path's slashes lean.
    """
    slugs = {
        check_numbers.extract_slug(LOCAL_COPY),
        check_numbers.extract_slug(LOCAL_COPY.replace('/', '\\')),
        extract.slugify('Pérez, Ana (2021) Señales', 80),
    }

    assert slugs == {'Perez_Ana_2021_Senales'}


def test_figures_in_block_leave_out_the_number_opening_a_heading() -> None:
    """
    A heading's section number is no figure; a figure after it is, with the pages the heading cites.
    """
    block = check_numbers.Block(
        lines=[(5, '## 4.2 Returns of 37.5% a year (p. 9)')],
        is_heading=True,
    )

    assert check_numbers.figures_in_block(block) == [
        check_numbers.Figure(
            line=5,
            text='37.5%',
            value='37.5',
            cited_pages=frozenset({9}),
        ),
    ]


def test_figures_in_block_leave_out_years_references_links_code_urls_and_citations() -> None:
    """
    A year, a numbered reference, a number in a link, in inline code or in a web address, and the
    citation itself are no figures; a percent and a signed number with separators are.
    """
    block = check_numbers.Block(
        lines=[
            (9, 'In 2021 the premium was 4.5% (p. 12), see Table 3 and eq. (12),'),
            (10, '[note 77](Notes_77.md), `code 99`, https://example.com/88, and −1,250.5 bps.'),
        ],
        is_heading=False,
    )

    assert check_numbers.figures_in_block(block) == [
        check_numbers.Figure(
            line=9,
            text='4.5%',
            value='4.5',
            cited_pages=frozenset({12}),
        ),
        check_numbers.Figure(
            line=10,
            text='−1,250.5',
            value='1250.5',
            cited_pages=frozenset({12}),
        ),
    ]


def test_frontmatter_fields_read_the_top_level_fields_only() -> None:
    """
    The fields between the opening and the closing `---`, each with the text after its colon; none
    in the body, and none when the frontmatter is missing or never closed.
    """
    text = '\n'.join([
        '---',
        f'local_copy: "{LOCAL_COPY}"',
        'read: 2026-10-27, the whole paper',
        'tags:',
        '  - señales',
        '---',
        '# Pérez (2021)',
        'citation: not a field, the body',
    ])

    assert check_numbers.frontmatter_fields(text) == {
        'local_copy': f'"{LOCAL_COPY}"',
        'read': '2026-10-27, the whole paper',
        'tags': '',
    }
    assert check_numbers.frontmatter_fields('# Pérez (2021)\nlocal_copy: none\n') == {}
    assert check_numbers.frontmatter_fields('---\nlocal_copy: none\n') == {}


def test_locate_figure_tells_where_a_figure_is() -> None:
    """
    On a cited page; elsewhere, with the pages that hold it; not found while a cited page is in the
    extract; not extracted when none is.
    """
    page_values = {
        12: frozenset({
            '1927',
            '4.5',
        }),
        13: frozenset({'18.2'}),
    }
    located = [
        check_numbers.locate_figure(
            _figure(
                value,
                cited,
            ),
            page_values,
        )
        for value, cited
        in [
            ('4.5', {12}),
            ('18.2', {12}),
            ('33.3', {13}),
            ('33.3', {30}),
        ]
    ]
    outcomes = [
        f'{outcome.outcome} {outcome.other_pages}'
        for outcome
        in located
    ]

    assert outcomes == [
        'on page []',
        'elsewhere [13]',
        'not found []',
        'not extracted []',
    ]


def test_main_exits_one_on_a_missing_path_or_no_note(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A path that does not exist, a folder holding only an index, a log and a page, and a command line
    with no path are usage mistakes: exit 1.
    """
    knowledge = tmp_path / 'Knowledge'
    (knowledge / 'Finance').mkdir(parents=True)
    (knowledge / 'INDEX.md').write_text(
        '# Index\n',
        encoding='utf-8',
    )
    (knowledge / 'LOG.md').write_text(
        '# Log\n',
        encoding='utf-8',
    )
    (knowledge / 'Finance' / 'Señales_de_momentum.md').write_text(
        '---\ntype: concept\n---\n# Señales de momentum\n\n- A gain of 11.1% (p. 10).\n',
        encoding='utf-8',
    )
    exit_codes = [
        check_numbers.main([str(tmp_path / 'No existe, (aún).md')]),
        check_numbers.main([str(knowledge)]),
    ]

    with pytest.raises(SystemExit) as no_path:
        check_numbers.main([])

    captured = capsys.readouterr()

    assert exit_codes == [1] * 2
    assert no_path.value.code == 1
    assert 'no such file or folder: ' in captured.err
    assert 'no note to read: every file given is an index, a log or a page' in captured.err


def test_main_exits_two_on_a_figure_not_found_and_zero_once_every_figure_is_found(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A figure not found exits 2, the report naming its line and cited page; once the note states
    what its page holds, the run exits 0.
    """
    extracts = tmp_path / 'Extracts'
    _write_extract(
        extracts,
        12,
        [
            'The premium was 4.5% a year.',
            'The worst year lost 33.3%.',
        ],
    )
    note_path = tmp_path / 'Knowledge' / 'Finance' / 'Pérez_2021_Señales.md'
    arguments = [
        str(tmp_path / 'Knowledge'),
        '--extracts',
        str(extracts),
    ]
    _write_note(
        note_path,
        LOCAL_COPY,
        [
            '- The premium was 4.5% a year (p. 12).',
            '- The worst year lost 35.5% (p. 13).',
        ],
    )
    not_found = check_numbers.main(arguments)
    first_lines = capsys.readouterr().out.splitlines()
    _write_note(
        note_path,
        LOCAL_COPY,
        [
            '- The premium was 4.5% a year (p. 12).',
            '- The worst year lost 33.3% (p. 13).',
        ],
    )
    found = check_numbers.main(arguments)
    second_lines = capsys.readouterr().out.splitlines()

    assert not_found == 2
    assert first_lines == [
        ''.join([
            f'{note_path.as_posix()}: 2 cited figures — 1 on page, 0 at offset, 0 elsewhere, 1 not found,',
            ' 0 not extracted; 0 uncited',
        ]),
        '  not found: line 8 "35.5%" (cites p. 13)',
        '1 notes: 1 checked, 0 unchecked; figures 1 on page, 0 at offset, 0 elsewhere, 1 not found, 0 not extracted',
    ]
    assert found == 0
    assert second_lines[-1] == ''.join([
        '1 notes: 1 checked, 0 unchecked; figures 2 on page, 0 at offset, 0 elsewhere, 0 not found,',
        ' 0 not extracted',
    ])


def test_normalise_drops_the_sign_the_separators_and_the_percent() -> None:
    """
    A figure is compared with no sign of any kind, no thousands separator and no percent.
    """
    values = [
        check_numbers.normalise(text)
        for text
        in [
            '−1,250.5%',
            '–12',
            '-0.35',
            '1,000,000',
        ]
    ]

    assert values == [
        '1250.5',
        '12',
        '0.35',
        '1000000',
    ]


@pytest.mark.xfail(
    strict=True,
    reason=' '.join([
        'split_blocks knows only backtick fences, so a figure in code fenced with tildes is checked',
        "as the note's own; library.py's fenced_lines reads a tilde fence as a fence too",
    ]),
)
def test_split_blocks_leaves_out_code_fenced_with_tildes() -> None:
    """
    A fence of tildes opens fenced code as one of backticks does, and no line inside it is a block.
    """
    text = '\n'.join([
        '# Señales',
        '~~~',
        'The premium was 45.5% (p. 3).',
        '~~~',
    ])
    blocks = check_numbers.split_blocks(text)

    assert blocks == [
        check_numbers.Block(
            lines=[(1, '# Señales')],
            is_heading=True,
        ),
    ]


def test_split_blocks_splits_paragraphs_items_headings_and_rows() -> None:
    """
    After the frontmatter, a heading and a table row are a block each, a paragraph or a list item
    runs over its lines to the next block, and fenced code is left out.
    """
    text = '\n'.join([
        '---',
        'local_copy: none',
        '---',
        '# Señales, (2021)',
        'A paragraph that',
        'wraps (p. 3).',
        '',
        '- An item',
        '  that wraps.',
        '- Another item.',
        '| a | row |',
        '| another | row |',
        '```',
        'fenced 99.9%',
        '```',
        'After the code.',
    ])
    blocks = check_numbers.split_blocks(text)
    numbers = [
        [
            number
            for number, _
            in block.lines
        ]
        for block
        in blocks
    ]
    headings = [
        block.is_heading
        for block
        in blocks
    ]

    assert numbers == [
        [4],
        [5, 6],
        [8, 9],
        [10],
        [11],
        [12],
        [16],
    ]
    assert headings == [True] + [False] * 6


def _figure(
    value: str,
    cited: set[int],
) -> check_numbers.Figure:
    """
    A figure as a note states it, with the pages its block cites.
    """
    figure = check_numbers.Figure(
        line=1,
        text=f'{value}%',
        value=value,
        cited_pages=frozenset(cited),
    )

    return figure


def _outcomes(
    report: check_numbers.NoteReport,
) -> list[str]:
    """
    Each cited figure of a report, with its outcome and the other pages that hold it.
    """
    outcomes = [
        f'{outcome.figure.text} {outcome.outcome} {outcome.other_pages}'
        for outcome
        in report.outcomes
    ]

    return outcomes


def _outcomes_at(
    offsets: list[int],
) -> list[check_numbers.FigureOutcome]:
    """
    One figure found elsewhere per line, each cited on page 10 and found at its offset from it.
    """
    outcomes = [
        check_numbers.FigureOutcome(
            figure=check_numbers.Figure(
                line=line,
                text='12.5%',
                value='12.5',
                cited_pages=frozenset({10}),
            ),
            outcome='elsewhere',
            other_pages=[10 + offset],
        )
        for line, offset
        in enumerate(offsets, start=1)
    ]

    return outcomes


def _write_extract(
    extracts: pathlib.Path,
    first_page: int,
    pages: list[str],
) -> None:
    """
    The extract of the notes' local copy as extract.py writes it: one chapter from its first page,
    a marker before every page.
    """
    folder = extracts / check_numbers.extract_slug(LOCAL_COPY)
    folder.mkdir(parents=True)
    extract.write_chapter(
        folder,
        LOCAL_COPY,
        extract.Chapter(
            1,
            'Señales',
            first_page - 1,
            first_page + len(pages) - 2,
        ),
        pages,
        'pypdf',
    )


def _write_note(
    path: pathlib.Path,
    local_copy: str,
    body: list[str],
) -> pathlib.Path:
    """
    A note naming a local copy, its body on the lines after a frontmatter of six lines.
    """
    text = '\n'.join([
        '---',
        'source: https://example.com/senales',
        'citation: Pérez, A. (2021). Señales. Link checked 2026-10-27.',
        f'local_copy: "{local_copy}"',
        'read: 2026-10-27, the whole paper',
        '---',
        *body,
        '',
    ])
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_text(
        text,
        encoding='utf-8',
        newline='\n',
    )

    return path
