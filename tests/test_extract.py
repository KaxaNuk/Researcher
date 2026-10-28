"""
The deterministic half of read, extract.py: a PDF's outline turned into chapters and their pages,
what --chapters and --split read, the names and the text it writes, and its exit codes on small PDFs
of blank pages built here.
"""
import pathlib
import types

import pypdf
import pytest

import extract

__all__ = []

PDF_NAME = 'Pérez, Ana (2021) Señales.pdf'


class OutlineReader:
    """
    A reader holding an outline of simple bookmarks, nested as pypdf nests them, each pointing to the
    page its title maps to.
    """

    def __init__(
        self,
        outline: list,
        pages: dict[str, int],
    ) -> None:
        """
        The outline, and the page of each bookmark by its title.
        """
        self.outline = outline
        self.pages = pages

    def get_destination_page_number(
        self,
        bookmark: types.SimpleNamespace,
    ) -> int:
        """
        The page a bookmark points to; a KeyError for one that points to none.
        """
        page = self.pages[bookmark.title]

        return page


class UnreadableOutlineReader:
    """
    A reader whose outline cannot be read, as a damaged PDF's.
    """

    @property
    def outline(self) -> list:
        """
        The outline, which raises as a damaged one does.
        """
        message = 'the outline is damaged'

        raise ValueError(message)


def test_chapters_from_outline_at_depth_two_end_each_chapter_at_the_next_part() -> None:
    """
    At depth 2 the chapters are the depth-2 entries, each running to the page before the next entry
    at its depth or shallower, a part's included; a depth with no entry gives no chapter.
    """
    entries = [
        *_entries(
            1,
            {
                'Parte I': 0,
                'Parte II': 7,
            },
        ),
        *_entries(
            2,
            {
                'Capítulo 1': 1,
                'Capítulo 2, (y medio)': 4,
                'Capítulo 3': 8,
            },
        ),
    ]
    chapters = extract.chapters_from_outline(
        entries,
        2,
        10,
    )
    deeper = extract.chapters_from_outline(
        entries,
        3,
        10,
    )

    assert _listed(chapters) == [
        '0. Front matter: p. 1',
        '1. Capítulo 1: p. 2–4',
        '2. Capítulo 2, (y medio): p. 5–7',
        '3. Capítulo 3: p. 9–10',
    ]
    assert deeper == []


def test_chapters_from_outline_runs_each_chapter_to_the_page_before_the_next() -> None:
    """
    Each chapter runs to the page before the next one, the last to the end; the pages before the
    first are chapter 0, front matter, and there is none when the first chapter opens the PDF.
    """
    entries = [
        *_entries(
            1,
            {
                'Introducción': 2,
                'Riesgo': 9,
                'Señales, (2021)': 5,
            },
        ),
        *_entries(
            2,
            {
                'Una sección': 3,
            },
        ),
    ]
    chapters = extract.chapters_from_outline(
        entries,
        1,
        12,
    )
    from_the_first_page = extract.chapters_from_outline(
        _entries(
            1,
            {
                'Dos': 1,
                'Uno': 0,
            },
        ),
        1,
        2,
    )

    assert _listed(chapters) == [
        '0. Front matter: p. 1–2',
        '1. Introducción: p. 3–5',
        '2. Señales, (2021): p. 6–9',
        '3. Riesgo: p. 10–12',
    ]
    assert _listed(from_the_first_page) == [
        '1. Uno: p. 1',
        '2. Dos: p. 2',
    ]


def test_clean_makes_line_endings_lf_drops_trailing_spaces_and_collapses_blank_runs() -> None:
    """
    A page's text with CRLF or CR endings, trailing spaces and tabs, and runs of blank lines comes
    out with LF endings and at most one blank line in a row, stripped.
    """
    cleaned = extract.clean('  Señales  \r\nde momentum\t\r\n\r\n\r\n\r\nfin\r')

    assert cleaned == 'Señales\nde momentum\n\nfin'


def test_flatten_outline_gives_each_bookmark_its_depth(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    pypdf nests a bookmark's children as a list after it: each comes out with its depth, in order; one
    with no title is untitled, and one pointing to no page is skipped with a note.
    """
    reader = OutlineReader(
        [
            _bookmark('Introducción'),
            [
                _bookmark('Prefacio, (2a ed.)'),
            ],
            _bookmark('Capítulo 1'),
            [
                _bookmark('Sección 1.1'),
                [
                    _bookmark('Un apartado'),
                ],
                _bookmark('Sin página'),
            ],
            _bookmark('  '),
        ],
        {
            '  ': 9,
            'Capítulo 1': 4,
            'Introducción': 0,
            'Prefacio, (2a ed.)': 1,
            'Sección 1.1': 5,
            'Un apartado': 6,
        },
    )
    entries = extract.flatten_outline(reader)
    captured = capsys.readouterr()

    assert _indented(entries) == [
        'Introducción @ 0',
        '  Prefacio, (2a ed.) @ 1',
        'Capítulo 1 @ 4',
        '  Sección 1.1 @ 5',
        '    Un apartado @ 6',
        '(untitled) @ 9',
    ]
    assert captured.err == "  outline entry without a page, skipped: 'Sin página'\n"


def test_flatten_outline_is_empty_when_the_outline_cannot_be_read(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    An outline that cannot be read gives no entry, and says why, so the PDF is read as one with none.
    """
    entries = extract.flatten_outline(UnreadableOutlineReader())
    captured = capsys.readouterr()

    assert entries == []
    assert captured.err == '  outline unreadable: the outline is damaged\n'


def test_main_exits_one_on_a_mistake_in_the_command(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A path that is not a file, a file that is not a PDF, and --split with --outline are mistakes in
    the command, never in the source: exit 1.
    """
    pdf_path = _pdf_with_bookmarks(tmp_path / PDF_NAME)
    not_a_pdf = tmp_path / 'Recorte, (2020).pdf'
    not_a_pdf.write_text(
        'a clipping saved as text',
        encoding='utf-8',
    )
    exit_codes = [
        extract.main(arguments)
        for arguments
        in [
            [str(tmp_path / 'No existe, (aún).pdf'), '--outline'],
            [str(not_a_pdf), '--outline'],
            [
                str(pdf_path),
                '--outline',
                '--split',
                'Introducción=1-2',
            ],
        ]
    ]
    captured = capsys.readouterr()

    assert exit_codes == [1] * 3
    assert 'not a file: ' in captured.err
    assert 'cannot open Recorte, (2020).pdf as a PDF' in captured.err
    assert '--split goes with --chapters or --all, not --outline' in captured.err


def test_main_exits_three_for_chapters_of_a_pdf_with_no_outline(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    --chapters on a PDF with no outline, and no --split, exits 3 with what to do, and writes nothing.
    """
    pdf_path = _pdf_without_outline(tmp_path / PDF_NAME)
    extracts = tmp_path / 'Extracts'
    exit_code = extract.main([
        str(pdf_path),
        '--chapters',
        '1',
        '--engine',
        'pypdf',
        '--out',
        str(extracts),
    ])
    captured = capsys.readouterr()

    assert exit_code == 3
    assert captured.err == f'{extract.NO_OUTLINE_MESSAGE}\n'
    assert not extracts.exists()


def test_main_prints_the_outline_of_a_pdf_with_bookmarks(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    --outline prints the page count, the entries per depth and the chapters --chapters numbers, each
    with its pages and its sections, and writes nothing.
    """
    pdf_path = _pdf_with_bookmarks(tmp_path / PDF_NAME)
    exit_code = extract.main([
        str(pdf_path),
        '--outline',
    ])
    lines = capsys.readouterr().out.splitlines()

    assert exit_code == 0
    assert lines == [
        f'{PDF_NAME}: 6 pages',
        '  outline entries: depth 1: 3, depth 2: 1',
        '  chapters at --depth 1 (the numbers --chapters takes):',
        '    1. Introducción  p. 1–2',
        '    2. Capítulo 1    p. 3–4',
        '         · Sección 1.1  (p. 4)',
        '    3. Capítulo 2    p. 5–6',
    ]
    assert sorted(tmp_path.iterdir()) == [pdf_path]


def test_main_writes_the_outline_and_no_chapter_for_a_pdf_with_no_text_layer(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A PDF with no text layer — a scan — gets its OUTLINE.md in Extracts/<slug>/ and no chapter, and
    the run exits 2, naming each chapter not written.
    """
    pdf_path = _pdf_with_bookmarks(tmp_path / PDF_NAME)
    extracts = tmp_path / 'Extracts'
    exit_code = extract.main([
        str(pdf_path),
        '--all',
        '--engine',
        'pypdf',
        '--out',
        str(extracts),
    ])
    captured = capsys.readouterr()
    folder = extracts / 'Perez_Ana_2021_Senales'
    outline_lines = (folder / 'OUTLINE.md').read_text(encoding='utf-8').splitlines()

    assert exit_code == 2
    assert sorted(folder.iterdir()) == [folder / 'OUTLINE.md']
    assert outline_lines[-3:] == [
        '| 1 | Introducción | 1–2 |',
        '| 2 | Capítulo 1 | 3–4 |',
        '| 3 | Capítulo 2 | 5–6 |',
    ]
    assert '  not written: 1. Introducción (p. 1–2) — 0 chars/page, no text layer' in captured.err
    assert extract.NOTHING_WRITTEN_MESSAGE in captured.err


@pytest.mark.xfail(
    strict=True,
    reason=' '.join([
        'parse_numbers reads a range written backwards, 5-3, as no chapter at all, so main writes',
        'nothing and exits 2 with the message for a scan, which the read skill takes for a PDF with',
        'no text layer, where a mistake in the command exits 1',
    ]),
)
def test_parse_numbers_exits_on_a_range_written_backwards() -> None:
    """
    A range written backwards names no chapter in order: it is a mistake in the command, refused as a
    number the outline lacks is.
    """
    with pytest.raises(SystemExit):
        extract.parse_numbers(
            '5-3',
            list(range(1, 6)),
        )


def test_parse_numbers_exits_on_a_token_or_a_number_it_cannot_take() -> None:
    """
    A token that is neither a number nor a range, and a number the outline does not have at this
    depth, stop the run with the reason.
    """
    with pytest.raises(SystemExit) as unreadable:
        extract.parse_numbers(
            '3, tres',
            list(range(1, 4)),
        )

    with pytest.raises(SystemExit) as missing:
        extract.parse_numbers(
            '2, 9-10',
            list(range(1, 4)),
        )

    assert unreadable.value.code == "--chapters: numbers and ranges only, got 'tres'"
    assert missing.value.code == '--chapters: no chapter [9, 10] at this depth; run --outline to see the numbers'


def test_parse_numbers_reads_numbers_and_ranges() -> None:
    """
    Numbers and inclusive ranges, with spaces and empty items, give the chapters' numbers sorted.
    """
    numbers = extract.parse_numbers(
        ' 3, 1-2,,7 ',
        list(range(8)),
    )

    assert numbers == [
        1,
        2,
        3,
        7,
    ]


def test_parse_split_exits_on_an_item_it_cannot_read() -> None:
    """
    An item with no `=`, a page range that is not numbers, and pages backwards or past the PDF's end
    each stop the run with the item.
    """
    refusals = [
        _split_refusal(specification)
        for specification
        in [
            'Introducción 1-12',
            'Introducción=uno-doce',
            'Introducción=12-1',
            'Introducción=1-99',
        ]
    ]

    assert refusals == [
        "--split: each item is Title=first-last, got 'Introducción 1-12'",
        "--split: bad page range 'uno-doce' in 'Introducción=uno-doce'",
        "--split: pages 12-1 outside 1-50 in 'Introducción=12-1'",
        "--split: pages 1-99 outside 1-50 in 'Introducción=1-99'",
    ]


def test_parse_split_reads_titles_and_one_based_pages() -> None:
    """
    Each `Title=first-last` is a chapter numbered in order, its pages 1-based and inclusive; a title
    may hold commas and parentheses, and an empty one is named by its number.
    """
    chapters = extract.parse_split(
        'Introducción, (y prefacio)=1-12; Capítulo 1 = 13 - 40 ;=41;',
        50,
    )

    assert _listed(chapters) == [
        '1. Introducción, (y prefacio): p. 1–12',
        '2. Capítulo 1: p. 13–40',
        '3. Part 3: p. 41',
    ]


def test_slugify_drops_accents_and_joins_words_with_underscores() -> None:
    """
    A title becomes ASCII words joined by underscores, its own capitals kept, cut at the limit with
    no underscore left at the end; a title with no word left is Untitled.
    """
    slugs = [
        extract.slugify('Pérez, Ana (2021) Señales: “momentum”'),
        extract.slugify('¿Qué? —'),
        extract.slugify('—'),
        extract.slugify('Abc def ghi', 4),
    ]

    assert slugs == [
        'Perez_Ana_2021_Senales_momentum',
        'Que',
        'Untitled',
        'Abc',
    ]


def test_write_chapter_puts_a_marker_before_every_page(
    tmp_path: pathlib.Path,
) -> None:
    """
    A chapter's extract: its frontmatter, its heading, then each page's cleaned text after a marker
    with its 1-based number, in a file named by its number and its title, with LF endings.
    """
    path = extract.write_chapter(
        tmp_path,
        'Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf',
        extract.Chapter(
            3,
            'Volatilidad, (y riesgo)',
            44,
            45,
        ),
        [
            'Calm follows calm.  \r\n\r\n\r\n\r\nIt clusters.',
            'Page 46.',
        ],
        'pypdf 6.0.0',
    )
    written = path.read_bytes().decode('utf-8')

    assert path == tmp_path / '03_Volatilidad_y_riesgo.md'
    assert written == '\n'.join([
        '---',
        'source: "Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf"',
        'chapter: 3',
        'title: "Volatilidad, (y riesgo)"',
        'pages: "45–46"',
        'engine: "pypdf 6.0.0"',
        '---',
        '',
        '# 3. Volatilidad, (y riesgo)',
        '',
        '<!-- p.45 -->',
        'Calm follows calm.',
        '',
        'It clusters.',
        '',
        '<!-- p.46 -->',
        'Page 46.',
        '',
    ])


def test_yaml_string_quotes_a_value_as_json_does_keeping_its_accents() -> None:
    """
    A frontmatter value is quoted the way JSON quotes it, its own quotes escaped and its accents kept.
    """
    quoted = extract.yaml_string('Señales: "momentum", (2021)')

    assert quoted == '"Señales: \\"momentum\\", (2021)"'


def _blank_writer() -> pypdf.PdfWriter:
    """
    A PDF of six blank pages, with no text layer.
    """
    writer = pypdf.PdfWriter()

    for _ in range(6):
        writer.add_blank_page(
            width=200,
            height=200,
        )

    return writer


def _bookmark(
    title: str,
) -> types.SimpleNamespace:
    """
    A bookmark with its title, as the outline reader below reads one.
    """
    bookmark = types.SimpleNamespace(title=title)

    return bookmark


def _entries(
    depth: int,
    pages: dict[str, int],
) -> list[extract.Entry]:
    """
    Outline entries at one depth, by their title, each with its 0-based page.
    """
    entries = [
        extract.Entry(
            depth,
            title,
            page,
        )
        for title, page
        in pages.items()
    ]

    return entries


def _indented(
    entries: list[extract.Entry],
) -> list[str]:
    """
    Outline entries as an indented list, two spaces a depth, each with its 0-based page.
    """
    lines = [
        f'{"  " * (entry.depth - 1)}{entry.title} @ {entry.page}'
        for entry
        in entries
    ]

    return lines


def _listed(
    chapters: list[extract.Chapter],
) -> list[str]:
    """
    Chapters as a reader writes them: the number, the title and the pages, 1-based.
    """
    lines = [
        f'{chapter.number}. {chapter.title}: p. {chapter.pages}'
        for chapter
        in chapters
    ]

    return lines


def _pdf_with_bookmarks(
    path: pathlib.Path,
) -> pathlib.Path:
    """
    Six blank pages whose bookmarks name three chapters, the second with one section.
    """
    writer = _blank_writer()
    writer.add_outline_item(
        'Introducción',
        0,
    )
    second_chapter = writer.add_outline_item(
        'Capítulo 1',
        2,
    )
    writer.add_outline_item(
        'Sección 1.1',
        3,
        parent=second_chapter,
    )
    writer.add_outline_item(
        'Capítulo 2',
        4,
    )
    writer.write(path)

    return path


def _pdf_without_outline(
    path: pathlib.Path,
) -> pathlib.Path:
    """
    Six blank pages with no bookmark.
    """
    writer = _blank_writer()
    writer.write(path)

    return path


def _split_refusal(
    specification: str,
) -> str:
    """
    Why parse_split stops on a specification, for a PDF of 50 pages.
    """
    with pytest.raises(SystemExit) as refused:
        extract.parse_split(
            specification,
            50,
        )

    message = str(refused.value.code)

    return message
