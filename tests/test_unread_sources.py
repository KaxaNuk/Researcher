"""
Every source no note has read, unread_sources.py: a source a note's local_copy names is read, one no
note names is listed, whatever its name, and an unread one names its leads.
"""
import pathlib

import pytest

import library
import unread_sources

__all__ = []

BOOK_INDEX = 'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/INDEX.md'
BOOK_SOURCE = 'Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf'
CHAPTER_ONE = 'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/01_Introducción.md'
CHAPTER_THREE = 'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md'
OCR_COPY = 'Sources/Books/García, Luis (2019) Riesgo (2a ed.) (OCR).pdf'
PAPER_NOTE = 'Knowledge/Finance/Pérez_2021_Señales.md'
PAPER_SOURCE = 'Sources/Papers/Pérez, Ana (2021) Señales.pdf'
UNREAD_SOURCE = 'Sources/Papers/Nadie, Uno (2022) Sin leer, (borrador).pdf'


def test_a_scan_is_read_through_its_searchable_copy(
    tmp_path: pathlib.Path,
) -> None:
    """
    A scan and its searchable copy, `<its name> (OCR).pdf` beside it, read for both: a note on the
    copy covers the scan.
    """
    found = _home(
        tmp_path,
        {
            BOOK_INDEX: _note_text(OCR_COPY),
            BOOK_SOURCE: '',
            OCR_COPY: '',
        },
    )
    statuses = _statuses(found)

    assert _unread(found) == []
    assert statuses[BOOK_SOURCE].read_through == found.root / OCR_COPY
    assert statuses[OCR_COPY].read_through is None


def test_a_source_a_note_names_is_read_and_one_no_note_names_is_unread(
    tmp_path: pathlib.Path,
) -> None:
    """
    A source is read when a note's local_copy names it by its full path, its commas, parentheses,
    accents and backslashes as written; a source no note names is unread.
    """
    found = _home(
        tmp_path,
        {
            PAPER_NOTE: _note_text('Sources\\Papers\\Pérez, Ana (2021) Señales.pdf'),
            PAPER_SOURCE: '',
            UNREAD_SOURCE: '',
        },
    )
    readers = [
        library.relative_name(found, note.path)
        for note
        in _statuses(found)[PAPER_SOURCE].notes
    ]

    assert _unread(found) == [UNREAD_SOURCE]
    assert readers == [PAPER_NOTE]


def test_an_unread_source_names_a_note_of_its_first_author_and_year(
    tmp_path: pathlib.Path,
) -> None:
    """
    With no other copy read, an unread source names the notes of its first author and year that share
    a word of its title; one sharing no word is no lead.
    """
    found = _home(
        tmp_path,
        {
            'Knowledge/Finance/Pérez_2021_Señales_en_acciones.md': _note_text(
                'Sources/Papers/Pérez, Ana (2021) Señales en acciones.pdf',
            ),
            'Knowledge/Finance/Pérez_2021_Volatilidad.md': _note_text(
                'Sources/Papers/Pérez, Ana (2021) Volatilidad.pdf',
            ),
            'Sources/Papers/Pérez, Ana (2021) Señales de momentum, (borrador).pdf': '',
        },
    )
    unread = _statuses(found)['Sources/Papers/Pérez, Ana (2021) Señales de momentum, (borrador).pdf']

    assert unread.copies == []
    assert unread_sources.lead_texts(found, unread) == [
        ' '.join([
            'paper of the same first author and year, with a word of its title:',
            'Knowledge/Finance/Pérez_2021_Señales_en_acciones.md, whose local_copy is',
            'Sources/Papers/Pérez, Ana (2021) Señales en acciones.pdf',
        ]),
    ]


def test_an_unread_source_names_the_note_on_another_copy_of_its_name(
    tmp_path: pathlib.Path,
) -> None:
    """
    An unread copy of a name a note reads — a later copy, its date after the name — names that note,
    first and alone.
    """
    found = _home(
        tmp_path,
        {
            'Knowledge/Tools/Señal_2026_README.md': _note_text('Sources/Clippings/Señal_README.md'),
            'Sources/Clippings/Señal_README.md': '',
            'Sources/Clippings/Señal_README_2026-10-18.md': '',
        },
    )
    later = _statuses(found)['Sources/Clippings/Señal_README_2026-10-18.md']

    assert _unread(found) == ['Sources/Clippings/Señal_README_2026-10-18.md']
    assert later.namesakes == []
    assert unread_sources.lead_texts(found, later) == [
        ' '.join([
            'another copy of it is read: Knowledge/Tools/Señal_2026_README.md',
            'reads Sources/Clippings/Señal_README.md',
        ]),
    ]


def test_in_a_strategy_a_pdf_beside_its_note_is_read_and_a_clipping_is_a_source(
    tmp_path: pathlib.Path,
) -> None:
    """
    In a strategy, every file beside the notes in Papers/ and Books/ but a note is a source, and
    every file in Notes/; a PDF its note names from the note's own folder is read.
    """
    found = _strategy(
        tmp_path / 'Estrategia, (momentum)',
        {
            'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/García, Luis (2019) Riesgo (2a ed.).pdf': '',
            'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/INDEX.md': _note_text(
                'García, Luis (2019) Riesgo (2a ed.).pdf',
            ),
            'Bibliotheca/Notes/Recorte, (2020) Señales.md': '# A clipping\n',
            'Bibliotheca/Papers/Pérez, Ana (2021) Señales.pdf': '',
            'Bibliotheca/Papers/Pérez_2021_Señales.md': _note_text('Pérez, Ana (2021) Señales.pdf'),
        },
    )

    assert list(_statuses(found)) == [
        'Bibliotheca/Books/García_2019_Riesgo_(2a_ed.)/García, Luis (2019) Riesgo (2a ed.).pdf',
        'Bibliotheca/Notes/Recorte, (2020) Señales.md',
        'Bibliotheca/Papers/Pérez, Ana (2021) Señales.pdf',
    ]
    assert _unread(found) == ['Bibliotheca/Notes/Recorte, (2020) Señales.md']


def test_main_exits_one_when_the_folder_is_not_a_library(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A folder with neither RESEARCHER.md nor Bibliotheca/ is a usage mistake: exit 1.
    """
    exit_code = unread_sources.main([str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert 'holds neither RESEARCHER.md nor Bibliotheca/' in captured.err


def test_main_exits_two_and_names_each_unread_source(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    At least one source unread exits 2: the summary counts the sources, then one line names each
    unread one by its path from the home.
    """
    found = _home(
        tmp_path,
        {
            PAPER_NOTE: _note_text(PAPER_SOURCE),
            PAPER_SOURCE: '',
            UNREAD_SOURCE: '',
        },
    )
    exit_code = unread_sources.main([str(found.root)])
    lines = capsys.readouterr().out.splitlines()

    assert exit_code == 2
    assert lines == [
        f'home {found.root.as_posix()}: 2 sources, 1 read, 0 read through an OCR copy, 1 unread',
        f'unread: {UNREAD_SOURCE}',
    ]


def test_main_exits_zero_when_every_source_is_read_and_all_lists_each_one(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Every source read exits 0; --all lists each with the notes that read it, a book by its INDEX.md
    with its chapters counted.
    """
    found = _home(
        tmp_path,
        {
            BOOK_INDEX: _note_text(BOOK_SOURCE),
            BOOK_SOURCE: '',
            CHAPTER_ONE: _note_text(BOOK_SOURCE),
            CHAPTER_THREE: _note_text(BOOK_SOURCE),
            PAPER_NOTE: _note_text(PAPER_SOURCE),
            PAPER_SOURCE: '',
        },
    )
    exit_code = unread_sources.main([
        str(found.root),
        '--all',
    ])
    lines = capsys.readouterr().out.splitlines()

    assert exit_code == 0
    assert lines == [
        f'home {found.root.as_posix()}: 2 sources, 2 read, 0 read through an OCR copy, 0 unread',
        f'read: {BOOK_SOURCE} — {BOOK_INDEX}, 2 chapters',
        f'read: {PAPER_SOURCE} — {PAPER_NOTE}',
    ]


def test_what_a_file_manager_leaves_is_never_a_source(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A .gitkeep, what a file manager or a sync tool leaves, and a hidden file are never sources, so
    a home holding only them has nothing unread.
    """
    found = _home(
        tmp_path,
        {
            'Sources/Clippings/.gitkeep': '',
            'Sources/Papers/.DS_Store': '',
            'Sources/Papers/.~lock.Pérez, Ana (2021) Señales.odt#': '',
            'Sources/Papers/Thumbs.db': '',
            'Sources/Papers/desktop.ini': '',
        },
    )
    exit_code = unread_sources.main([str(found.root)])
    lines = capsys.readouterr().out.splitlines()

    assert exit_code == 0
    assert lines == [f'home {found.root.as_posix()}: 0 sources, 0 read, 0 read through an OCR copy, 0 unread']


def _home(
    folder: pathlib.Path,
    files: dict[str, str],
) -> library.Library:
    """
    A home holding RESEARCHER.md and these files, by their path from its root.
    """
    _write(
        folder / 'RESEARCHER.md',
        '# The researcher\n',
    )
    _write_files(
        folder,
        files,
    )
    home = library.find_library(folder)

    return home


def _note_text(
    local_copy: str,
) -> str:
    """
    A note whose frontmatter names a local copy, quoted as a path with commas is.
    """
    text = '\n'.join([
        '---',
        'source: https://example.com/fuente',
        'citation: Pérez, A. (2021). Señales. Link checked 2026-10-27.',
        f'local_copy: "{local_copy}"',
        'read: 2026-10-27, the whole work',
        '---',
        '',
        '# A note',
        '',
    ])

    return text


def _statuses(
    found: library.Library,
) -> dict[str, unread_sources.SourceStatus]:
    """
    Every source of a library with its status, by its path from the root, in the order they sort.
    """
    report = unread_sources.unread_report(
        found,
        library.library_files(found),
    )
    statuses = {
        library.relative_name(found, status.path): status
        for status
        in report.sources
    }

    return statuses


def _strategy(
    folder: pathlib.Path,
    files: dict[str, str],
) -> library.Library:
    """
    A strategy holding Bibliotheca/ and these files, by their path from its root.
    """
    (folder / 'Bibliotheca').mkdir(parents=True)
    _write_files(
        folder,
        files,
    )
    strategy = library.find_library(folder)

    return strategy


def _unread(
    found: library.Library,
) -> list[str]:
    """
    The sources of a library no note names, by their path from its root.
    """
    report = unread_sources.unread_report(
        found,
        library.library_files(found),
    )
    names = [
        library.relative_name(found, status.path)
        for status
        in report.unread
    ]

    return names


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


def _write_files(
    folder: pathlib.Path,
    files: dict[str, str],
) -> None:
    """
    Every file of a library, by its path from the folder, with its text.
    """
    for relative, text in files.items():
        _write(
            folder / relative,
            text,
        )
