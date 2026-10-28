"""
The module the read skill's library scripts share, library.py: which library a folder is, what each
of its markdown files is, a file's frontmatter and its links, and the file a note's local_copy names.
"""
import pathlib

import library

__all__ = []

CONCEPT_PAGE = '\n'.join([
    '---',
    'type: concept',
    'updated: 2026-10-27',
    'sources:',
    '  - Finance/Pérez_2021_Señales.md',
    '  - "Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md"',
    'tags: [señales, momentum]',
    '---',
    '# Señales de momentum',
    '',
])
SYNTHESIS_PAGE = '\n'.join([
    '---',
    'type: Synthesis',
    '---',
    '# ¿Qué dice la biblioteca?',
    '',
])


def test_clean_target_reads_a_target_as_the_path_it_names() -> None:
    """
    Angle brackets, an anchor and a query are dropped and a percent escape is read, so a name with
    commas, parentheses and accents comes out as the file is named.
    """
    bracketed = library.clean_target('<Sources/Papers/Pérez, Ana (2021) Señales.pdf#page=3>')
    escaped = library.clean_target('Finance/Se%C3%B1ales%20(2021).md?plain=1')

    assert bracketed == 'Sources/Papers/Pérez, Ana (2021) Señales.pdf'
    assert escaped == 'Finance/Señales (2021).md'


def test_fenced_lines_hold_each_fence_and_what_it_encloses() -> None:
    """
    A block opened by backticks or by tildes holds its fences and every line between them; one never
    closed runs to the end.
    """
    lines = [
        'A paragraph.',
        '```python',
        '[not a link](x.md)',
        '```',
        'Between the blocks.',
        '  ~~~',
        'never closed',
    ]

    assert library.fenced_lines(lines) == frozenset({
        1,
        2,
        3,
        5,
        6,
    })


def test_file_kind_names_each_markdown_file_of_a_home(
    tmp_path: pathlib.Path,
) -> None:
    """
    At home: the index and the log at the top of Knowledge/, a paper or a page in a domain folder by
    its type, a book's index or a chapter one folder down, a stray file elsewhere, a study outside.
    """
    found = _home(tmp_path)
    concept = library.parse_frontmatter(CONCEPT_PAGE)
    plain = library.parse_frontmatter('# A note\n')
    synthesis = library.parse_frontmatter(SYNTHESIS_PAGE)
    fronts = {
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md': plain,
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/INDEX.md': plain,
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/Notas/Suelta.md': plain,
        'Knowledge/Finance/Pérez_2021_Señales.md': plain,
        'Knowledge/Finance/Qué_dice_la_biblioteca.md': synthesis,
        'Knowledge/Finance/Señales_de_momentum.md': concept,
        'Knowledge/INDEX.md': plain,
        'Knowledge/LOG.md': plain,
        'Knowledge/Léeme.md': plain,
        'Studies/Cómputo_local.md': plain,
    }
    kinds = {
        relative: library.file_kind(
            found,
            found.root / relative,
            front,
        )
        for relative, front
        in fronts.items()
    }

    assert kinds == {
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md': library.CHAPTER,
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/INDEX.md': library.BOOK_INDEX,
        'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/Notas/Suelta.md': library.STRAY,
        'Knowledge/Finance/Pérez_2021_Señales.md': library.PAPER,
        'Knowledge/Finance/Qué_dice_la_biblioteca.md': library.SYNTHESIS,
        'Knowledge/Finance/Señales_de_momentum.md': library.CONCEPT,
        'Knowledge/INDEX.md': library.INDEX,
        'Knowledge/LOG.md': library.LOG,
        'Knowledge/Léeme.md': library.STRAY,
        'Studies/Cómputo_local.md': library.STUDY,
    }


def test_file_kind_names_each_markdown_file_of_a_strategy(
    tmp_path: pathlib.Path,
) -> None:
    """
    In a strategy, by where it sits alone: the bibliography, the log, a paper in Papers/, a book's
    index or a chapter in Books/<book>/, and a stray file anywhere else; a strategy has no pages.
    """
    found = _strategy(tmp_path)
    concept = library.parse_frontmatter(CONCEPT_PAGE)
    plain = library.parse_frontmatter('# A note\n')
    fronts = {
        'Bibliotheca/BIBLIOGRAPHY.md': plain,
        'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md': plain,
        'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/INDEX.md': plain,
        'Bibliotheca/Books/Suelto.md': plain,
        'Bibliotheca/LOG.md': plain,
        'Bibliotheca/Notes/Recorte, (2020).md': plain,
        'Bibliotheca/Papers/Pérez_2021_Señales.md': concept,
    }
    kinds = {
        relative: library.file_kind(
            found,
            found.root / relative,
            front,
        )
        for relative, front
        in fronts.items()
    }

    assert kinds == {
        'Bibliotheca/BIBLIOGRAPHY.md': library.INDEX,
        'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md': library.CHAPTER,
        'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/INDEX.md': library.BOOK_INDEX,
        'Bibliotheca/Books/Suelto.md': library.STRAY,
        'Bibliotheca/LOG.md': library.LOG,
        'Bibliotheca/Notes/Recorte, (2020).md': library.STRAY,
        'Bibliotheca/Papers/Pérez_2021_Señales.md': library.PAPER,
    }


def test_find_library_gives_none_for_a_folder_that_is_neither(
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder with neither RESEARCHER.md nor Bibliotheca/ is not a library, a Knowledge/ in it or not.
    """
    (tmp_path / 'Knowledge').mkdir()

    assert library.find_library(tmp_path) is None


def test_find_library_reads_a_home_by_its_researcher_file(
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder holding RESEARCHER.md is a home, a Bibliotheca/ beside it or not: its index and its log
    in Knowledge/, its extracts at its root.
    """
    (tmp_path / 'Bibliotheca').mkdir()
    found = _home(tmp_path)
    root = tmp_path.resolve()

    assert found == library.Library(
        extracts=root / 'Extracts',
        index=root / 'Knowledge' / 'INDEX.md',
        kind='home',
        log=root / 'Knowledge' / 'LOG.md',
        notes_root=root / 'Knowledge',
        root=root,
    )


def test_find_library_reads_a_strategy_by_its_bibliotheca(
    tmp_path: pathlib.Path,
) -> None:
    """
    A folder holding Bibliotheca/ is a strategy: BIBLIOGRAPHY.md its index, its log and its extracts
    inside Bibliotheca/.
    """
    found = _strategy(tmp_path / 'Estrategia, (momentum) señales')
    root = (tmp_path / 'Estrategia, (momentum) señales').resolve()

    assert found == library.Library(
        extracts=root / 'Bibliotheca' / 'Extracts',
        index=root / 'Bibliotheca' / 'BIBLIOGRAPHY.md',
        kind='strategy',
        log=root / 'Bibliotheca' / 'LOG.md',
        notes_root=root / 'Bibliotheca',
        root=root,
    )


def test_is_local_target_reads_a_web_address_in_angle_brackets_as_an_address() -> None:
    """
    CommonMark lets a link's target sit between angle brackets: a web address there is still a web
    address, as clean_target reads it once the brackets are dropped.
    """
    assert not library.is_local_target('<https://example.com/a paper, (2021).pdf>')


def test_is_local_target_tells_a_file_from_an_address_or_an_anchor() -> None:
    """
    A relative path or a drive path is a file of this computer; a web or a mail address, an anchor in
    the same file and an empty target are not.
    """
    expected = {
        '': False,
        '  ': False,
        '#what-it-changes': False,
        '<Sources/Papers/Pérez, Ana (2021) Señales.pdf>': True,
        'D:/Research/Notas.md': True,
        'D:\\Research\\Notas.md': True,
        'Finance/Pérez_2021_Señales.md': True,
        'https://example.com/señales': False,
        'mailto:lab@example.com': False,
    }
    local = {
        target: library.is_local_target(target)
        for target
        in expected
    }

    assert local == expected


def test_link_path_reads_a_target_from_the_folder_of_the_linking_file(
    tmp_path: pathlib.Path,
) -> None:
    """
    A relative target is read from the folder of the file that holds the link, its `..` folded away,
    its anchor dropped and its escapes read; a drive path is kept as it is.
    """
    chapter = tmp_path / 'Knowledge' / 'Finance' / 'García_2019_Riesgo_(2a_ed.)' / '03_Volatilidad.md'
    climbing = library.link_path(
        chapter,
        '../Pérez_2021_Se%C3%B1ales.md#claims',
    )
    bracketed = library.link_path(
        chapter,
        '<../../Otros/Una nota, (borrador).md>',
    )
    drive = library.link_path(
        chapter,
        'D:/Research/Notas.md',
    )

    assert climbing == tmp_path / 'Knowledge' / 'Finance' / 'Pérez_2021_Señales.md'
    assert bracketed == tmp_path / 'Knowledge' / 'Otros' / 'Una nota, (borrador).md'
    assert drive == pathlib.Path('D:/Research/Notas.md')


def test_local_copy_path_is_none_when_a_note_names_no_copy(
    tmp_path: pathlib.Path,
) -> None:
    """
    `none`, in any case and quoted or not, an empty field and no field at all name no copy.
    """
    found = _home(tmp_path)
    copies = [
        library.local_copy_path(
            found,
            _note(
                found.notes_root / 'Finance' / 'Sin_copia.md',
                [field],
            ),
        )
        for field
        in [
            'local_copy: none',
            'local_copy: "None"',
            'local_copy:',
            'read: 2026-10-27, the abstract only',
        ]
    ]

    assert copies == [None] * 4


def test_local_copy_path_reads_from_the_root_then_from_the_notes_folder(
    tmp_path: pathlib.Path,
) -> None:
    """
    A path is read from the library's root first, then from the note's own folder — a strategy's PDF
    beside its note — the root's reading given when neither is on disk; a drive path is kept.
    """
    found = _strategy(tmp_path)
    papers = found.notes_root / 'Papers'
    _write(
        papers / 'Pérez, Ana (2021) Señales.pdf',
        '',
    )
    beside = library.local_copy_path(
        found,
        _note(
            papers / 'Pérez_2021_Señales.md',
            ['local_copy: "Pérez, Ana (2021) Señales.pdf"'],
        ),
    )
    from_root = library.local_copy_path(
        found,
        _note(
            papers / 'Pérez_2021_Señales.md',
            ['local_copy: Bibliotheca\\Papers\\Pérez, Ana (2021) Señales.pdf'],
        ),
    )
    nowhere = library.local_copy_path(
        found,
        _note(
            papers / 'Nadie_2022_Sin_copia.md',
            ['local_copy: "Nadie, Uno (2022) Sin copia.pdf"'],
        ),
    )
    drive = library.local_copy_path(
        found,
        _note(
            papers / 'Pérez_2021_Señales.md',
            ['local_copy: D:\\Research\\Sources\\Pérez, Ana (2021) Señales.pdf'],
        ),
    )

    assert beside == papers / 'Pérez, Ana (2021) Señales.pdf'
    assert from_root == papers / 'Pérez, Ana (2021) Señales.pdf'
    assert nowhere == found.root / 'Nadie, Uno (2022) Sin copia.pdf'
    assert drive == pathlib.Path('D:/Research/Sources/Pérez, Ana (2021) Señales.pdf')


def test_markdown_links_read_targets_with_commas_parentheses_and_accents() -> None:
    """
    A target may hold one level of parentheses, or anything between angle brackets; a title after it
    is left out, and each link carries the line it opens on.
    """
    text = '\n'.join([
        '# Señales',
        '',
        'See [Pérez (2021)](Finance/Pérez_2021_Señales.md) and [Markowitz](Finance/Markowitz_(1952).md).',
        'Its copy: [the PDF](<Sources/Papers/Pérez, Ana (2021) Señales.pdf> "the scan").',
    ])

    assert library.markdown_links(text) == [
        library.Link(
            line=3,
            target='Finance/Pérez_2021_Señales.md',
            text='Pérez (2021)',
        ),
        library.Link(
            line=3,
            target='Finance/Markowitz_(1952).md',
            text='Markowitz',
        ),
        library.Link(
            line=4,
            target='<Sources/Papers/Pérez, Ana (2021) Señales.pdf>',
            text='the PDF',
        ),
    ]


def test_markdown_links_skip_code_and_escapes_and_follow_a_wrapped_text() -> None:
    """
    No link opens in fenced code, in inline code or at an escaped bracket; a link's text may hold
    brackets and wrap onto the next line, and an image is a link too.
    """
    text = '\n'.join([
        'Not a link: \\[0.3.0](CHANGELOG.md), nor `[code](code.md)`.',
        '```markdown',
        '[fenced](fenced.md)',
        '```',
        'An entry *[0.3.0]* that',
        'wraps: [entry *[0.3.0]*',
        'of the changelog](CHANGELOG.md), and ![a figure](figura,_(1).png).',
    ])

    assert library.markdown_links(text) == [
        library.Link(
            line=6,
            target='CHANGELOG.md',
            text='entry *[0.3.0]*\nof the changelog',
        ),
        library.Link(
            line=7,
            target='figura,_(1).png',
            text='a figure',
        ),
    ]


def test_parse_frontmatter_is_empty_unless_the_file_opens_and_closes_it() -> None:
    """
    There is no frontmatter when the first line is not `---`, or when no later `---` closes it.
    """
    empty = library.Frontmatter(
        body_start=0,
        fields={},
        items={},
    )
    fronts = [
        library.parse_frontmatter(text)
        for text
        in [
            '',
            '# A note\n\ntype: concept\n',
            '---\ntype: concept\nupdated: 2026-10-27\n',
            'An opening line\n---\ntype: concept\n---\n',
        ]
    ]

    assert fronts == [empty] * 4


def test_parse_frontmatter_reads_fields_block_items_and_the_body_start() -> None:
    """
    Each field keeps the text after its colon; the items of a block list are read without their
    quotes; the body starts on the line after the closing `---`.
    """
    front = library.parse_frontmatter(CONCEPT_PAGE)

    assert front.fields == {
        'sources': '',
        'tags': '[señales, momentum]',
        'type': 'concept',
        'updated': '2026-10-27',
    }
    assert front.items == {
        'sources': [
            'Finance/Pérez_2021_Señales.md',
            'Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md',
        ],
        'tags': [],
        'type': [],
        'updated': [],
    }
    assert front.body_start == 8


def _home(
    folder: pathlib.Path,
) -> library.Library:
    """
    An empty home: a folder holding RESEARCHER.md.
    """
    _write(
        folder / 'RESEARCHER.md',
        '# The researcher\n',
    )
    home = library.find_library(folder)

    return home


def _note(
    path: pathlib.Path,
    fields: list[str],
) -> library.LibraryFile:
    """
    A paper's note at a path, its frontmatter holding these lines, read as the scripts read one.
    """
    text = '\n'.join([
        '---',
        *fields,
        '---',
        '# A note',
        '',
    ])
    note = library.LibraryFile(
        front=library.parse_frontmatter(text),
        kind=library.PAPER,
        path=path,
        text=text,
    )

    return note


def _strategy(
    folder: pathlib.Path,
) -> library.Library:
    """
    An empty strategy: a folder holding Bibliotheca/.
    """
    (folder / 'Bibliotheca').mkdir(parents=True)
    strategy = library.find_library(folder)

    return strategy


def _write(
    path: pathlib.Path,
    text: str,
) -> None:
    """
    A file written as UTF-8 with LF line endings, its folders made first.
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
