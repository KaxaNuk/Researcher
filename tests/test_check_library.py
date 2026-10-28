"""
The checks `audit` makes on every run, check_library.py: a clean library gives no finding, each fault
planted in one is found with its file and line, and the exit code says which it was.
"""
import functools
import pathlib

import pytest

import check_library
import library

__all__ = []

BIBLIOGRAPHY_TEXT = '\n'.join([
    '# Bibliography',
    '',
    '## Part 1 — The core idea',
    '',
    '| Source | What it bears on |',
    '| --- | --- |',
    '| Pérez (2021) — *Señales* | momentum after costs, claim 1: [note](Papers/Pérez_2021_Señales.md) |',
    '| Ruiz (2020) — *Momentum, otra vez* | the other side of claim 1. No note yet |',
    '',
])
BOOK_INDEX_TEXT = '\n'.join([
    '---',
    'source: https://example.com/riesgo',
    'citation: García, L. (2019). Riesgo, 2a ed. Link checked 2026-10-27.',
    'local_copy: "Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf"',
    'read: 2026-10-27, chapter 3',
    '---',
    '',
    '# García (2019) — Riesgo, 2a ed.',
    '',
    '| # | Chapter | Pages | Status | Question | Note |',
    '| --- | --- | --- | --- | --- | --- |',
    '| 1 | Introducción | 1–24 | skipped | | |',
    '| 2 | Rendimientos | 25–44 | skimmed | Q1 | a survey, nothing chapter 3 does not carry |',
    '| 3 | Volatilidad | 45–71 | read | Q1 | [03_Volatilidad.md](03_Volatilidad.md) |',
    '| 4 | Correlación | 72–98 | to come | Q1 | |',
    '',
])
CHAPTER_TEXT = '\n'.join([
    '---',
    'source: https://example.com/riesgo',
    'citation: García, L. (2019). Riesgo, 2a ed. Link checked 2026-10-27.',
    'local_copy: "Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf"',
    'read: 2026-10-27, chapter 3',
    '---',
    '',
    '# Riesgo — 3. Volatilidad',
    '',
    '*Chapter 3, pages 45–71, from the extract.*',
    '',
    '## Volatility clusters',
    '',
    '- Calm follows calm (p. 52), as [Pérez (2021)](../Pérez_2021_Señales.md) finds for returns.',
    '',
    '> **For question 1:** size by volatility.',
    '',
])
CONCEPT_TEXT = '\n'.join([
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
    '- Calm follows calm ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
    '',
    "## For the owner's questions",
    '',
    '> **Question 1:** the signal is worth testing, sized by volatility.',
    '',
    '## Open',
    '',
    '- What momentum costs to trade.',
    '',
])
INDEX_TEXT = '\n'.join([
    '# Index',
    '',
    '## Finance',
    '',
    '### Concepts',
    '',
    '- [Señales de momentum](Finance/Señales_de_momentum.md) — a momentum signal, as the library holds it',
    '',
    '### Sources',
    '',
    '- [Pérez (2021) — Señales](Finance/Pérez_2021_Señales.md) — winners keep winning for a year',
    '- [García (2019) — Riesgo, 2a ed.](Finance/García_2019_Riesgo_(2a_ed.)/INDEX.md) — chapter 3 of 4',
    '  - [3. Volatilidad](Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md) — calm follows calm',
    '',
])
LOG_TEXT = '\n'.join([
    '# Log',
    '',
    '---',
    '',
    '## [2026-10-27] read | Pérez (2021), García (2019) chapter 3',
    '',
])
PAPER_TEXT = '\n'.join([
    '---',
    'source: https://example.com/senales',
    'citation: Pérez, A. (2021). Señales, (momentum) y riesgo. Link checked 2026-10-27.',
    'local_copy: "Sources/Papers/Pérez, Ana (2021) Señales.pdf"',
    'read: 2026-10-27, the whole paper',
    'tags: [momentum]',
    '---',
    '',
    '# Pérez (2021) — Señales',
    '',
    '*The whole paper, from the extract.*',
    '',
    '## Why it is here',
    '',
    'Question 1 — *Does momentum pay after costs?*',
    '',
    '## Momentum pays after costs',
    '',
    '- Winners keep winning for a year (p. 3).',
    '',
    '> **For question 1:** the signal is worth testing.',
    '',
    '## What it changes',
    '',
    '- A signal to test; it does not settle the costs.',
    '',
])
RESEARCHER_TEXT = '\n'.join([
    '# The researcher',
    '',
    '## The strategies and projects it works on',
    '',
    '| Strategy or project | Path | State |',
    '| --- | --- | --- |',
    '| *none listed* | — | — |',
    '',
])
STRATEGY_LOG_TEXT = '\n'.join([
    '# Log',
    '',
    '## [2026-10-27] read | Pérez (2021), for claim 1',
    '',
])
STRATEGY_PAPER_TEXT = '\n'.join([
    '---',
    'source: https://example.com/senales',
    'citation: Pérez, A. (2021). Señales, (momentum) y riesgo. Link checked 2026-10-27.',
    'local_copy: "Bibliotheca/Papers/Pérez, Ana (2021) Señales.pdf"',
    'read: 2026-10-27, the whole paper',
    '---',
    '',
    '# Pérez (2021) — Señales',
    '',
    '## Why it is here',
    '',
    'Claim 1 of `OBJECTIVE.md` — momentum pays after costs.',
    '',
    '## Momentum pays after costs',
    '',
    '- Winners keep winning for a year (p. 3).',
    '',
    '> **For claim 1:** the strategy keeps its signal.',
    '',
])
STUDY_TEXT = '\n'.join([
    '*idea, 2026-10-27*',
    '',
    '# Cómputo local',
    '',
    'What the owner wants to work out.',
    '',
])
UNLINKED_TEXT = '\n'.join([
    '---',
    'source: none',
    'citation: Suelto, S. (2020). Sin enlace, (borrador). No link to check.',
    'local_copy: none',
    'read: 2026-10-27, the abstract only',
    '---',
    '',
    '# Suelto (2020) — Sin enlace',
    '',
])
# The files of each library, by their path from its root, and the notes the tests name.
BOOK_INDEX = 'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/INDEX.md'
BOOK_SOURCE = 'Sources/Books/García, Luis (2019) Riesgo (2a ed.).pdf'
CHAPTER = 'Knowledge/Finance/García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md'
CONCEPT = 'Knowledge/Finance/Señales_de_momentum.md'
PAPER = 'Knowledge/Finance/Pérez_2021_Señales.md'
PAPER_SOURCE = 'Sources/Papers/Pérez, Ana (2021) Señales.pdf'
STRATEGY_PAPER = 'Bibliotheca/Papers/Pérez_2021_Señales.md'
UNREAD_SOURCE = 'Sources/Clippings/Nadie, Uno (2022) Sin leer, (borrador).pdf'
CLEAN_HOME = {
    BOOK_INDEX: BOOK_INDEX_TEXT,
    BOOK_SOURCE: '',
    CHAPTER: CHAPTER_TEXT,
    CONCEPT: CONCEPT_TEXT,
    PAPER: PAPER_TEXT,
    PAPER_SOURCE: '',
    'Knowledge/INDEX.md': INDEX_TEXT,
    'Knowledge/LOG.md': LOG_TEXT,
    'RESEARCHER.md': RESEARCHER_TEXT,
    'Sources/Clippings/.gitkeep': '',
    'Sources/Papers/.gitkeep': '',
    'Studies/Cómputo_local.md': STUDY_TEXT,
}
CLEAN_STRATEGY = {
    STRATEGY_PAPER: STRATEGY_PAPER_TEXT,
    'Bibliotheca/BIBLIOGRAPHY.md': BIBLIOGRAPHY_TEXT,
    'Bibliotheca/LOG.md': STRATEGY_LOG_TEXT,
    'Bibliotheca/Notes/.gitkeep': '',
    'Bibliotheca/Papers/Pérez, Ana (2021) Señales.pdf': '',
}


def test_a_book_row_that_links_a_note_but_is_not_marked_read_is_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    The row of a book's table that links its chapter's note is marked read; a status outside the
    four the convention names is found as well.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.root / BOOK_INDEX,
        '| read | Q1 | [03_Volatilidad.md]',
        '| leído | Q1 | [03_Volatilidad.md]',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.BOOK,
            line=14,
            message="a row that links a note but is marked 'leído'",
            path=BOOK_INDEX,
        ),
        check_library.Finding(
            kind=check_library.BOOK,
            line=None,
            message="statuses outside read, skimmed, skipped and to come: 'leído'",
            path=BOOK_INDEX,
        ),
    ]


def test_a_broken_link_is_found_at_its_line(
    tmp_path: pathlib.Path,
) -> None:
    """
    A link to a note that is not there is a broken link, at the line it opens on.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.root / PAPER,
        '- Winners keep winning for a year (p. 3).',
        '- Winners keep winning for a year (p. 3), as [Ruiz (2020)](Ruiz_2020_Momentum,_otra_vez.md) says.',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.BROKEN_LINK,
            line=19,
            message='links Ruiz_2020_Momentum,_otra_vez.md, which is not there',
            path=PAPER,
        ),
    ]


def test_a_chapter_no_page_names_and_a_claim_that_links_no_note_are_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    At home, every chapter note is named by a concept page, and every claim under What the sources say
    links the note it comes from.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.root / CONCEPT,
        '  - García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md\n',
        '',
    )
    _replace(
        found.root / CONCEPT,
        '- Calm follows calm ([García 2019, ch. 3, p. 52](García_2019_Riesgo_(2a_ed.)/03_Volatilidad.md)).',
        '- Calm follows calm, as García (2019) says (p. 52).',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.CONCEPT_PAGE,
            line=None,
            message='a chapter note no concept page names, in its sources or by a link',
            path=CHAPTER,
        ),
        check_library.Finding(
            kind=check_library.CONCEPT_PAGE,
            line=17,
            message='a claim under What the sources say that links no note',
            path=CONCEPT,
        ),
    ]


def test_a_clean_home_has_no_finding(
    tmp_path: pathlib.Path,
) -> None:
    """
    A home whose notes, pages, book, study and sources keep every convention gives no finding, with
    --verbose or without it.
    """
    found = _clean_home(tmp_path)
    files = library.library_files(found)
    verbose = check_library.check_library(
        found,
        files,
        True,
    )

    assert _findings(found) == []
    assert verbose == []


def test_a_clean_strategy_has_no_finding(
    tmp_path: pathlib.Path,
) -> None:
    """
    A strategy whose paper sits beside its PDF in Bibliotheca/Papers/, linked from BIBLIOGRAPHY.md,
    gives no finding: a strategy has no concept pages to check.
    """
    found = _clean_strategy(tmp_path / 'Estrategia, (momentum)')

    assert _findings(found) == []


def test_a_duplicate_is_found_when_two_notes_read_one_file(
    tmp_path: pathlib.Path,
) -> None:
    """
    Two notes, not chapters of one book, whose local_copy is the same file are a duplicate, named
    once with both notes.
    """
    found = _clean_home(tmp_path)
    _write(
        found.notes_root / 'Finance' / 'Pérez_2021_Señales_(copia).md',
        PAPER_TEXT,
    )
    _add_line(
        found.index,
        '- [Pérez (2021), a copy](Finance/Pérez_2021_Señales_(copia).md) — the same paper',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.DUPLICATE,
            line=None,
            message=', '.join([
                '2 notes read the same file: Knowledge/Finance/Pérez_2021_Señales.md',
                'Knowledge/Finance/Pérez_2021_Señales_(copia).md',
            ]),
            path=PAPER,
        ),
    ]


def test_a_link_out_of_the_strategy_is_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    A strategy's note that links a file of the researcher's home links out of its own repository.
    """
    _write(
        tmp_path / 'Home' / PAPER,
        PAPER_TEXT,
    )
    found = _clean_strategy(tmp_path / 'Estrategia, (momentum)')
    _replace(
        found.root / STRATEGY_PAPER,
        '- Winners keep winning for a year (p. 3).',
        '- Winners keep winning for a year (p. 3); [at home](../../../Home/Knowledge/Finance/Pérez_2021_Señales.md).',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.LINK_LEAVES,
            line=16,
            message='links ../../../Home/Knowledge/Finance/Pérez_2021_Señales.md, outside this repository',
            path=STRATEGY_PAPER,
        ),
    ]


def test_a_missing_copy_is_one_finding_with_its_counts(
    tmp_path: pathlib.Path,
) -> None:
    """
    A fresh clone holds no PDF: the notes whose local_copy is not on this computer are one finding,
    with the count of notes and of files; --verbose adds one finding per note.
    """
    found = _clean_home(tmp_path)
    (found.root / BOOK_SOURCE).unlink()
    summary = check_library.Finding(
        kind=check_library.MISSING_COPIES,
        line=None,
        message='local_copy not on this computer: 2 notes, 1 file; a fresh clone holds no PDF',
        path='Knowledge',
    )
    verbose = check_library.check_library(
        found,
        library.library_files(found),
        True,
    )

    assert _findings(found) == [summary]
    assert verbose == [
        summary,
        check_library.Finding(
            kind=check_library.MISSING_COPIES,
            line=None,
            message=f'local_copy {BOOK_SOURCE} is not there',
            path=CHAPTER,
        ),
        check_library.Finding(
            kind=check_library.MISSING_COPIES,
            line=None,
            message=f'local_copy {BOOK_SOURCE} is not there',
            path=BOOK_INDEX,
        ),
    ]


def test_a_note_naming_an_extract_and_a_page_linking_a_pdf_cite_an_extract(
    tmp_path: pathlib.Path,
) -> None:
    """
    Notes cite the source and its pages, never a file of Extracts/; a page cites notes, never a PDF.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.root / CHAPTER,
        '*Chapter 3, pages 45–71, from the extract.*',
        '*Chapter 3, pages 45–71, from `Extracts/Garcia_Luis_2019_Riesgo_2a_ed/03_Volatilidad.md`.*',
    )
    _replace(
        found.root / CONCEPT,
        'A momentum signal, as the library holds it today.',
        'A momentum signal, as [the paper](../../Sources/Papers/Pérez,%20Ana%20(2021)%20Señales.pdf) has it.',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.CITES_EXTRACT,
            line=12,
            message=f'links ../../{PAPER_SOURCE}: a page or a study cites notes, never a PDF',
            path=CONCEPT,
        ),
        check_library.Finding(
            kind=check_library.CITES_EXTRACT,
            line=10,
            message='names a file in Extracts/: notes cite the source and its pages',
            path=CHAPTER,
        ),
    ]


def test_an_orphan_is_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    A note no other file links to is an orphan; at home the index does not link it either.
    """
    found = _clean_home(tmp_path)
    unlinked = 'Knowledge/Finance/Suelto_2020_Sin_enlace,_(borrador).md'
    _write(
        found.root / unlinked,
        UNLINKED_TEXT,
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.ORPHAN,
            line=None,
            message='nothing else in the library links to it',
            path=unlinked,
        ),
        check_library.Finding(
            kind=check_library.INDEX,
            line=None,
            message='not linked from Knowledge/INDEX.md',
            path=unlinked,
        ),
    ]


def test_an_unread_source_is_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    A source no note's local_copy names is unread, whatever its name; a .gitkeep is never a source.
    """
    found = _clean_home(tmp_path)
    _write(
        found.root / UNREAD_SOURCE,
        '',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.UNREAD_SOURCE,
            line=None,
            message='no note names it in local_copy',
            path=UNREAD_SOURCE,
        ),
    ]


def test_bad_frontmatter_is_found(
    tmp_path: pathlib.Path,
) -> None:
    """
    A note lacking a field, carrying one beyond the convention's or with a read that is only a date,
    and a page lacking updated or naming a source that is not there, are each found.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.root / PAPER,
        '\n'.join([
            'citation: Pérez, A. (2021). Señales, (momentum) y riesgo. Link checked 2026-10-27.',
            'local_copy: "Sources/Papers/Pérez, Ana (2021) Señales.pdf"',
            'read: 2026-10-27, the whole paper',
        ]),
        '\n'.join([
            'local_copy: "Sources/Papers/Pérez, Ana (2021) Señales.pdf"',
            'read: 2026-10-27',
            'status: leído',
        ]),
    )
    _replace(
        found.root / CONCEPT,
        'updated: 2026-10-27\nsources:\n  - Pérez_2021_Señales.md\n',
        'sources:\n  - Pérez_2021_Señales,_(perdida).md\n',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.FRONTMATTER,
            line=None,
            message='missing citation',
            path=PAPER,
        ),
        check_library.Finding(
            kind=check_library.FRONTMATTER,
            line=None,
            message='carries status, beyond source, citation, local_copy, read and tags',
            path=PAPER,
        ),
        check_library.Finding(
            kind=check_library.FRONTMATTER,
            line=None,
            message='read is only a date, 2026-10-27: it says what was read',
            path=PAPER,
        ),
        check_library.Finding(
            kind=check_library.FRONTMATTER,
            line=None,
            message='missing updated',
            path=CONCEPT,
        ),
        check_library.Finding(
            kind=check_library.FRONTMATTER,
            line=None,
            message='sources names notes that are not there: Pérez_2021_Señales,_(perdida).md',
            path=CONCEPT,
        ),
    ]


def test_main_exits_one_when_the_folder_is_not_a_library(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A folder with neither RESEARCHER.md nor Bibliotheca/ is a usage mistake: exit 1, and nothing on
    standard output.
    """
    exit_code = check_library.main([str(tmp_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ''
    assert 'holds neither RESEARCHER.md nor Bibliotheca/' in captured.err


def test_main_exits_two_and_prints_each_finding_under_its_kind(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    At least one finding exits 2; the report names its kind with the count, then the finding with
    its file, and ends with the total.
    """
    found = _clean_home(tmp_path)
    _write(
        found.root / UNREAD_SOURCE,
        '',
    )
    exit_code = check_library.main([str(found.root)])
    lines = capsys.readouterr().out.splitlines()

    assert exit_code == 2
    assert lines[:3] == [
        f'home {found.root.as_posix()}: 3 notes, 1 page, 1 study file, 3 sources',
        'unread source — 1',
        f'  {UNREAD_SOURCE}: no note names it in local_copy',
    ]
    assert lines[-1] == '1 finding'


def test_main_exits_zero_and_names_every_check_on_a_clean_library(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    A clean library exits 0, its report naming every kind of check it found nothing for and the
    projects its clippings were checked against.
    """
    found = _clean_home(tmp_path)
    exit_code = check_library.main([
        str(found.root),
        '--verbose',
    ])
    lines = capsys.readouterr().out.splitlines()
    every_kind = ', '.join(check_library.FINDING_KINDS)

    assert exit_code == 0
    assert lines == [
        f'home {found.root.as_posix()}: 3 notes, 1 page, 1 study file, 2 sources',
        f'none of: {every_kind}',
        'clippings checked against 0 projects in the projects table',
        '0 findings',
    ]


def test_the_index_is_checked_against_the_notes(
    tmp_path: pathlib.Path,
) -> None:
    """
    At home, a line of Knowledge/INDEX.md whose note is gone, and a note it does not link, are each
    an index finding.
    """
    found = _clean_home(tmp_path)
    _replace(
        found.index,
        '- [Pérez (2021) — Señales](Finance/Pérez_2021_Señales.md) — winners keep winning for a year',
        '- [Ruiz (2020) — Momentum, otra vez](Finance/Ruiz_2020_Momentum.md) — a note no longer there',
    )

    assert _findings(found) == [
        check_library.Finding(
            kind=check_library.INDEX,
            line=11,
            message='links Finance/Ruiz_2020_Momentum.md, which is not there',
            path='Knowledge/INDEX.md',
        ),
        check_library.Finding(
            kind=check_library.INDEX,
            line=None,
            message='not linked from Knowledge/INDEX.md',
            path=PAPER,
        ),
    ]


def _add_line(
    path: pathlib.Path,
    line: str,
) -> None:
    """
    A line added at the end of a file.
    """
    text = path.read_text(encoding='utf-8')
    _write(
        path,
        f'{text}{line}\n',
    )


def _clean_home(
    folder: pathlib.Path,
) -> library.Library:
    """
    A home whose library keeps every convention: a paper, a book with one chapter read, a concept
    page, the index and the log, a study, and the sources each note reads.
    """
    _write_files(
        folder,
        CLEAN_HOME,
    )
    home = library.find_library(folder)

    return home


def _clean_strategy(
    folder: pathlib.Path,
) -> library.Library:
    """
    A strategy whose Bibliotheca/ keeps every convention: one paper's note beside its PDF, linked
    from BIBLIOGRAPHY.md, and the log.
    """
    _write_files(
        folder,
        CLEAN_STRATEGY,
    )
    strategy = library.find_library(folder)

    return strategy


def _findings(
    found: library.Library,
) -> list[check_library.Finding]:
    """
    Every finding check_library.py makes on a library, without --verbose.
    """
    findings = check_library.check_library(
        found,
        library.library_files(found),
        False,
    )

    return findings


@pytest.fixture(autouse=True)
def _home_in_the_test_folder(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    The stale-clipping check expands a `~` in RESEARCHER.md's projects table: Path.home(), HOME and
    USERPROFILE all lead to the test's own folder, so no test reads the real home.
    """
    monkeypatch.setenv(
        'HOME',
        str(tmp_path),
    )
    monkeypatch.setenv(
        'USERPROFILE',
        str(tmp_path),
    )
    monkeypatch.setattr(
        pathlib.Path,
        'home',
        staticmethod(functools.partial(pathlib.Path, tmp_path)),
    )


def _replace(
    path: pathlib.Path,
    old: str,
    new: str,
) -> None:
    """
    A file with one piece of its text replaced; the piece must be there, so no fault goes unplanted.
    """
    text = path.read_text(encoding='utf-8')

    assert old in text

    _write(
        path,
        text.replace(old, new),
    )


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
