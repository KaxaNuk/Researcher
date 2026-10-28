# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf[crypto]>=4.0"]
# ///
"""
The figures a note states, looked up on the pages it cites: the check `audit deep` runs.

For every figure a note writes beside a page citation, it opens the extract of the note's
`local_copy` — the folder `extract.py` writes — and looks for the figure on the cited pages, then
on every other page of the extract. It reads; it never edits a note or an extract, and it has no
opinion about whether a figure is right: one on its cited page may still be quoted out of context,
and one found nowhere may be the note's own arithmetic. It says where to look.

    uv run check_numbers.py Knowledge                       every note under Knowledge/, extracts in ./Extracts
    uv run check_numbers.py NOTE.md BOOK_FOLDER --extracts Bibliotheca/Extracts
    uv run check_numbers.py Knowledge/Finance --verbose     every figure, not only those not found

What it reads
    a note      a markdown file; a folder is walked for *.md, leaving out INDEX.md, LOG.md and the
                concept and synthesis pages, whose frontmatter carries `type:`
    its source  the frontmatter's `local_copy`, a PDF, whose extract is <extracts>/<slug>/ — the
                slug made by extract.py's own slugify — every chapter file there split at its
                `<!-- p.N -->` markers
    a citation  p. 93 · pp. 12–13 · pp. 12-13 · pp. 5, 9, 12 · (p. 7), outside a markdown link
    a figure    a number of two digits or more in the same paragraph, list item, heading or table
                row as a citation: decimals, thousands separators, a percent, a minus of any kind.
                Not a number inside a markdown link, inline code or a URL, not the citation itself,
                and not the section number opening a heading. Not a year either, four bare digits
                from 1500 to 2099, nor a number its label names as a reference — an equation, a
                section, a table, a figure, a chapter, a page, a footnote, in English or Spanish:
                eq. (12), section 4.2, Table 3, sección 2.1, \\tag{7}. Compared without separators,
                percent or sign: a PDF's minus comes out as a hyphen, a dash or a glyph of its own

Each figure is on page (a cited page holds it), elsewhere (another page does, listed), or not found.
When at least three of the lines holding a note's figures found elsewhere, and most of them, sit at
one offset from the cited page, the note seems to cite printed pages, not the extract's PDF pages:
the report says so once, with the offset, and every figure found at exactly that offset is counted
at offset, not elsewhere. A figure whose cited pages — shifted by the offset, too, when there is
one — are none of them in the extract, and that no page holds, is counted as not extracted. A block
with figures and no citation is counted, not checked. A note whose local_copy is not a PDF, or
whose extract is not on disk, is unchecked, with the reason and the extract.py command that would
regenerate it.

Options
    --extracts DIR  the extracts root (default ./Extracts)
    --verbose       every figure with its outcome, not only those not found

Exit codes: 0 no figure not found · 1 usage: a path that does not exist, no note to read, or a
command line the parser rejects · 2 at least one figure not found.
Without uv: pip install "pypdf[crypto]", then python check_numbers.py ... — extract.py, beside
this file, needs it.
"""
import argparse
import collections
import dataclasses
import itertools
import pathlib
import re
import sys
import typing

SCRIPT_DIRECTORY = pathlib.Path(__file__).resolve().parent

if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import extract  # noqa: E402 - found beside this file once its folder is on the path.

# A page or a range, as a citation writes it: `12`, `12-13`, `12–13`.
PAGE_OR_RANGE = r'\d+(?:\s*[–-]\s*\d+)?'
# Citations: one page or range after `p.`, a list of them after `pp.`.
CITATION = re.compile(
    rf'\bp\.\s*{PAGE_OR_RANGE}|\bpp\.\s*{PAGE_OR_RANGE}(?:\s*,\s*{PAGE_OR_RANGE})*',
)
CITED_PAGE = re.compile(r'(\d+)(?:\s*[–-]\s*(\d+))?')
# A figure in a note: a minus only where no letter or digit comes before it, so a range is two
# figures, and never part of a word, a longer number or a dotted section number.
FIGURE = re.compile(
    r'(?:(?<![\w.,])[-−–])?(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w]|[.,]\d)',
)
# A number on an extracted page: no boundaries asked, since a PDF's text runs words into numbers.
PAGE_NUMBER = re.compile(r'\d+(?:,\d{3})*(?:\.\d+)?')
PAGE_MARKER = re.compile(r'<!--\s*p\.(\d+)\s*-->')
# The markdown a note is split and cleaned by.
# What opens or closes a fenced code block, after any indent: backticks or tildes.
FENCE_OPENINGS = (
    '```',
    '~~~',
)
FRONTMATTER_FIELD = re.compile(r'^(\w+):\s*(.*)$')
HEADING = re.compile(r'^#{1,6}\s')
HEADING_NUMBER = re.compile(r'^(#{1,6}\s+)(?:[A-Z]\.)?\d+(?:\.\d+)*\.?(?=\s)')
INLINE_CODE = re.compile(r'`[^`]*`')
LATEX_TAG = re.compile(r'\\tag\{[^}]*\}')
LIST_ITEM = re.compile(r'^\s*(?:[-*+]|\d+[.)])\s+')
MARKDOWN_LINK = re.compile(r'!?\[[^\]]*\]\([^)]*\)')
TABLE_ROW = re.compile(r'^\s*\|')
URL = re.compile(r'https?://\S+')
MINUS_SIGNS = '-−–'
# A number a label names as a reference, never a figure: `eq. (12)`, `section 4.2`, `Table 3`,
# `chapters 3 and 4`, `sección 2.1`. One reference, then any more joined by a comma or a word.
REFERENCE_LABELS = [
    'appendix',
    'apéndice',
    'cap',
    'capítulo',
    'capítulos',
    'ch',
    'chapter',
    'chapters',
    'col',
    'column',
    'columna',
    'columns',
    'cuadro',
    'ec',
    'ecuación',
    'ecuaciones',
    'eq',
    'eqs',
    'equation',
    'equations',
    'exhibit',
    'fig',
    'figs',
    'figura',
    'figure',
    'figures',
    'fila',
    'footnote',
    'footnotes',
    'lemma',
    'nota',
    'note',
    'page',
    'pages',
    'panel',
    'part',
    'parte',
    'página',
    'páginas',
    'proposition',
    'proposición',
    'row',
    'rows',
    'sec',
    'section',
    'sections',
    'sección',
    'secciones',
    'tabla',
    'tablas',
    'table',
    'tables',
    'teorema',
    'theorem',
]
REFERENCE_NUMBER = r'\(?[A-Z]?\d+(?:\.\d+)*[a-z]?\)?(?:\s?[–-]\s?\(?\d+(?:\.\d+)*[a-z]?\)?)?'
REFERENCE = re.compile(
    ''.join([
        r'\b(?:',
        '|'.join(REFERENCE_LABELS),
        r')\.?\s*',
        REFERENCE_NUMBER,
        r'(?:\s*(?:,|&|\band\b|\bor\b|\by\b|\bo\b)\s*',
        REFERENCE_NUMBER,
        r')*',
    ]),
    re.IGNORECASE,
)
YEAR_RANGE = range(
    1500,
    2100,
)
# At least this many lines of a note, and most of those holding a figure found elsewhere, at one
# offset from the cited page, and the note may cite printed pages. Lines, not figures: one sentence
# quoting four numbers from another page is one cross-reference, not four.
MINIMUM_OFFSET_LINES = 3
SKIPPED_NOTE_NAMES = frozenset({
    'INDEX.md',
    'LOG.md',
})
OUTCOMES = [
    'on page',
    'at offset',
    'elsewhere',
    'not found',
    'not extracted',
]


@dataclasses.dataclass(frozen=True)
class Block:
    """
    A paragraph, list item, heading or table row of a note: each of its lines with its number in the
    file, and whether it is a heading.
    """
    lines: list[tuple[int, str]]
    is_heading: bool


@dataclasses.dataclass(frozen=True)
class Figure:
    """
    One figure a note states: its line, its text as written, the value it is compared by, and the
    pages its block cites.
    """
    line: int
    text: str
    value: str
    cited_pages: frozenset[int]


@dataclasses.dataclass(frozen=True)
class FigureOutcome:
    """
    Where a figure was found — one of `OUTCOMES` — and, when not on a cited page, the pages that hold it.
    """
    figure: Figure
    outcome: str
    other_pages: list[int]


@dataclasses.dataclass(frozen=True)
class NoteReport:
    """
    What the check found in one note: every cited figure's outcome, the uncited count and the offset
    its citations seem to sit at, or why the note was unchecked.
    """
    path: pathlib.Path
    outcomes: list[FigureOutcome]
    uncited_figures: int
    unchecked_reason: str | None
    offset: int | None = None


class CommandLineParser(argparse.ArgumentParser):
    """
    The argument parser, exiting 1 on a command line it rejects, so that 2 means a figure not found.
    """

    def error(
        self,
        message: str,
    ) -> typing.NoReturn:
        """
        Print the usage and the problem, and exit 1.
        """
        self.print_usage(sys.stderr)
        problem = f'{self.prog}: error: {message}'
        print(problem, file=sys.stderr)
        sys.exit(1)


def check_note(
    note_path: pathlib.Path,
    extracts_root: pathlib.Path,
) -> NoteReport:
    """
    Every cited figure of one note against its extract, or the reason it cannot be checked.
    """
    text = note_path.read_text(encoding='utf-8-sig')
    fields = frontmatter_fields(text)
    raw_local_copy = fields.get('local_copy', '')
    local_copy = raw_local_copy.strip().strip('"\'')
    unchecked_reason = _unchecked_source(
        local_copy,
        extracts_root,
    )

    if unchecked_reason is not None:
        unchecked = NoteReport(
            path=note_path,
            outcomes=[],
            uncited_figures=0,
            unchecked_reason=unchecked_reason,
        )

        return unchecked

    pages = load_pages(extracts_root / extract_slug(local_copy))

    if not pages:
        folder = _extract_folder(
            local_copy,
            extracts_root,
        )
        no_markers = NoteReport(
            path=note_path,
            outcomes=[],
            uncited_figures=0,
            unchecked_reason=f'the extract in {folder} has no page markers',
        )

        return no_markers

    figures = [
        figure
        for block
        in split_blocks(text)
        for figure
        in figures_in_block(block)
    ]
    page_values = {
        page: _values_on_page(page_text)
        for page, page_text
        in pages.items()
    }
    located = [
        locate_figure(
            figure,
            page_values,
        )
        for figure
        in figures
        if figure.cited_pages
    ]
    offset = consistent_offset(located)
    outcomes = located if offset is None else [
        relocate_at_offset(
            outcome,
            offset,
            page_values,
        )
        for outcome
        in located
    ]
    report = NoteReport(
        path=note_path,
        outcomes=outcomes,
        uncited_figures=len(figures) - len(outcomes),
        unchecked_reason=None,
        offset=offset,
    )

    return report


def cited_pages(
    text: str,
) -> frozenset[int]:
    """
    Every page the citations in a text name, ranges expanded.
    """
    pages = frozenset(
        page
        for citation
        in CITATION.findall(text)
        for match
        in CITED_PAGE.finditer(citation)
        for page
        in _page_range(match)
    )

    return pages


def consistent_offset(
    outcomes: list[FigureOutcome],
) -> int | None:
    """
    The one offset, found page less cited page, that most lines holding a figure found elsewhere
    share; None when fewer than `MINIMUM_OFFSET_LINES` share one, or when they are not most of them.
    """
    elsewhere = [
        outcome
        for outcome
        in outcomes
        if outcome.outcome == 'elsewhere'
    ]
    line_offsets = {
        (outcome.figure.line, offset)
        for outcome
        in elsewhere
        for offset
        in _offsets(outcome)
    }
    counts = collections.Counter(
        offset
        for _, offset
        in line_offsets
    )
    elsewhere_lines = {
        outcome.figure.line
        for outcome
        in elsewhere
    }

    if not counts:

        return None

    largest_count = max(counts.values())
    best_offset = min(
        (
            offset
            for offset, count
            in counts.items()
            if count == largest_count
        ),
        key=abs,
    )
    shared = largest_count >= MINIMUM_OFFSET_LINES and largest_count * 2 > len(elsewhere_lines)
    offset = best_offset if shared else None

    return offset


def extract_slug(
    local_copy: str,
) -> str:
    """
    The extract folder's name for a PDF, made exactly as extract.py makes it.
    """
    stem = pathlib.PurePosixPath(local_copy.replace('\\', '/')).stem
    slug = extract.slugify(
        stem,
        80,
    )

    return slug


def figures_in_block(
    block: Block,
) -> list[Figure]:
    """
    The figures a block states, each with the pages the block cites; links, inline code, URLs, the
    citations and a heading's opening number are left out.
    """
    joined = ' '.join(
        line_text
        for _, line_text
        in block.lines
    )
    pages = cited_pages(_without_links(joined))
    first_line = block.lines[0][0]
    figures = [
        Figure(
            line=line_number,
            text=match.group(0),
            value=normalise(match.group(0)),
            cited_pages=pages,
        )
        for line_number, line_text
        in block.lines
        for match
        in FIGURE.finditer(_figure_text(
            line_text,
            block.is_heading and line_number == first_line,
        ))
        if _digit_count(match.group(0)) >= 2
        and not _is_year(match.group(0))
    ]

    return figures


def frontmatter_fields(
    text: str,
) -> dict[str, str]:
    """
    The top-level fields of a note's YAML frontmatter, each as the text after its colon.
    """
    lines = text.splitlines()
    body_start = _body_start(lines)
    matches = [
        FRONTMATTER_FIELD.match(line)
        for line
        in lines[1:max(body_start - 1, 1)]
    ]
    fields = {
        match.group(1): match.group(2)
        for match
        in matches
        if match is not None
    }

    return fields


def load_pages(
    extract_folder: pathlib.Path,
) -> dict[int, str]:
    """
    Every page of an extract, by its number, from the chapter files' page markers.
    """
    chapter_files = sorted(
        path
        for path
        in extract_folder.glob('*.md')
        if path.name != 'OUTLINE.md'
    )
    pages = {
        page: page_text
        for path
        in chapter_files
        for page, page_text
        in _chapter_pages(path).items()
    }

    return pages


def locate_figure(
    figure: Figure,
    page_values: dict[int, frozenset[str]],
) -> FigureOutcome:
    """
    Where a figure is: on a cited page, on other pages, nowhere, or on no page while none it cites was
    extracted.
    """
    holding_pages = sorted(
        page
        for page, values
        in page_values.items()
        if figure.value in values
    )
    on_cited_page = any(
        page in figure.cited_pages
        for page
        in holding_pages
    )
    any_cited_extracted = any(
        page in page_values
        for page
        in figure.cited_pages
    )

    if on_cited_page:
        outcome = 'on page'
    elif holding_pages:
        outcome = 'elsewhere'
    elif any_cited_extracted:
        outcome = 'not found'
    else:
        outcome = 'not extracted'

    located = FigureOutcome(
        figure=figure,
        outcome=outcome,
        other_pages=[] if on_cited_page else holding_pages,
    )

    return located


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Parse the command line, check every note, print the report, and give the exit code.
    """
    arguments = _build_parser().parse_args(argv)
    given_paths = [
        pathlib.Path(path)
        for path
        in arguments.paths
    ]
    missing = [
        path
        for path
        in given_paths
        if not path.exists()
    ]

    if missing:
        print(f'no such file or folder: {missing[0]}', file=sys.stderr)

        return 1

    note_paths = [
        note_path
        for path
        in given_paths
        for note_path
        in note_files(path)
    ]

    if not note_paths:
        print('no note to read: every file given is an index, a log or a page', file=sys.stderr)

        return 1

    extracts_root = pathlib.Path(arguments.extracts)
    reports = [
        check_note(
            note_path,
            extracts_root,
        )
        for note_path
        in note_paths
    ]

    for report in reports:
        print_report(
            report,
            arguments.verbose,
        )

    print_totals(reports)
    not_found = any(
        outcome.outcome == 'not found'
        for report
        in reports
        for outcome
        in report.outcomes
    )
    exit_code = 2 if not_found else 0

    return exit_code


def normalise(
    text: str,
) -> str:
    """
    A number as it is compared: no sign, no thousands separators, no percent.
    """
    unsigned = text.lstrip(MINUS_SIGNS)
    plain = unsigned.replace(',', '').rstrip('%')

    return plain


def note_files(
    path: pathlib.Path,
) -> list[pathlib.Path]:
    """
    The notes a path names: the file itself, or every markdown file under a folder, indexes, logs and
    pages left out.
    """
    markdown_files = path.rglob('*.md') if path.is_dir() else [path]
    candidates = sorted(markdown_files)
    notes = [
        candidate
        for candidate
        in candidates
        if candidate.name not in SKIPPED_NOTE_NAMES
        and 'type' not in frontmatter_fields(candidate.read_text(encoding='utf-8-sig'))
    ]

    return notes


def print_report(
    report: NoteReport,
    verbose: bool,
) -> None:
    """
    One note's summary line, its figures not found, and, with `verbose`, every other figure.
    """
    name = report.path.as_posix()

    if report.unchecked_reason is not None:
        print(f'{name}: unchecked — {report.unchecked_reason}')

        return

    summary = _outcome_counts(report.outcomes)
    print(f'{name}: {len(report.outcomes)} cited figures — {summary}; {report.uncited_figures} uncited')
    shown = [
        outcome
        for outcome
        in report.outcomes
        if verbose or outcome.outcome == 'not found'
    ]

    for outcome in shown:
        print(_outcome_line(outcome))

    if report.offset is not None:
        at_offset = sum(
            1
            for outcome
            in report.outcomes
            if outcome.outcome == 'at offset'
        )
        offset_line = ' '.join([
            f'  offset {report.offset:+d}: {at_offset} figures sit on the PDF page {report.offset:+d}',
            'from the one cited, so the note seems to cite printed pages; a book\'s INDEX.md says its',
            'offset once',
        ])
        print(offset_line)


def print_totals(
    reports: list[NoteReport],
) -> None:
    """
    The run's totals: notes checked and unchecked, and figures by outcome.
    """
    checked = [
        report
        for report
        in reports
        if report.unchecked_reason is None
    ]
    outcomes = [
        outcome
        for report
        in checked
        for outcome
        in report.outcomes
    ]
    unchecked_count = len(reports) - len(checked)
    totals = _outcome_counts(outcomes)
    checked_count = len(checked)
    print(f'{len(reports)} notes: {checked_count} checked, {unchecked_count} unchecked; figures {totals}')


def relocate_at_offset(
    outcome: FigureOutcome,
    offset: int,
    page_values: dict[int, frozenset[str]],
) -> FigureOutcome:
    """
    A figure's outcome once its note's offset is known: found elsewhere at exactly the offset from a
    cited page, it is at offset; found nowhere, it is not found when a cited page, or one shifted by
    the offset, is in the extract, and not extracted otherwise.
    """
    shifted = {
        page + offset
        for page
        in outcome.figure.cited_pages
    }
    holding_shifted = shifted & set(outcome.other_pages)
    at_offset = outcome.outcome == 'elsewhere' and bool(holding_shifted)
    unlocated = outcome.outcome in {'not found', 'not extracted'}
    any_extracted = any(
        page in page_values
        for page
        in shifted | outcome.figure.cited_pages
    )

    if at_offset:
        new_outcome = 'at offset'
    elif unlocated:
        new_outcome = 'not found' if any_extracted else 'not extracted'
    else:
        new_outcome = outcome.outcome

    relocated = FigureOutcome(
        figure=outcome.figure,
        outcome=new_outcome,
        other_pages=outcome.other_pages,
    )

    return relocated


def split_blocks(
    text: str,
) -> list[Block]:
    """
    A note's body, after its frontmatter and outside fenced code, as paragraphs, list items, headings
    and table rows.
    """
    lines = text.splitlines()
    fenced = _fenced_lines(lines)
    blocks = []
    current = []

    body_start = _body_start(lines)

    for index in range(body_start, len(lines)):
        line = lines[index]
        is_blank = index in fenced or not line.strip()
        is_heading = not is_blank and bool(HEADING.match(line))
        is_table_row = not is_blank and bool(TABLE_ROW.match(line))
        starts_block = is_blank or is_heading or is_table_row or bool(LIST_ITEM.match(line))

        if starts_block and current:
            blocks.append(_make_block(current))
            current.clear()

        if is_blank:

            continue

        current.append((index + 1, line))

        if is_heading or is_table_row:
            blocks.append(_make_block(current))
            current.clear()

    if current:
        blocks.append(_make_block(current))

    return blocks


def _blank(
    match: re.Match[str],
) -> str:
    """
    As many spaces as the match is long, so the positions after it stay put.
    """
    spaces = ' ' * len(match.group(0))

    return spaces


def _body_start(
    lines: list[str],
) -> int:
    """
    The index of the first line after the frontmatter; 0 when there is none.
    """
    if not lines or lines[0].strip() != '---':

        return 0

    closing = next(
        (
            position
            for position
            in range(1, len(lines))
            if lines[position].strip() == '---'
        ),
        None,
    )
    start = 0 if closing is None else closing + 1

    return start


def _build_parser() -> CommandLineParser:
    """
    The command line: the notes or folders, the extracts root, and verbose.
    """
    parser = CommandLineParser(
        prog='check_numbers.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'paths',
        nargs='+',
        help='notes, or folders walked for them',
    )
    parser.add_argument(
        '--extracts',
        default='Extracts',
        help='extracts root (default ./Extracts)',
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='list every figure with its outcome',
    )

    return parser


def _chapter_pages(
    path: pathlib.Path,
) -> dict[int, str]:
    """
    One chapter file's pages, by number: the text after each `<!-- p.N -->` marker, up to the next.
    """
    parts = PAGE_MARKER.split(path.read_text(encoding='utf-8'))
    marker_positions = range(
        1,
        len(parts) - 1,
        2,
    )
    pages = {
        int(parts[position]): parts[position + 1]
        for position
        in marker_positions
    }

    return pages


def _digit_count(
    text: str,
) -> int:
    """
    How many digits a figure has.
    """
    count = sum(
        1
        for character
        in text
        if character.isdigit()
    )

    return count


def _extract_folder(
    local_copy: str,
    extracts_root: pathlib.Path,
) -> str:
    """
    The extract folder of a PDF, as a path to print.
    """
    folder = extracts_root / extract_slug(local_copy)
    printed = f'{folder.as_posix()}/'

    return printed


def _fenced_lines(
    lines: list[str],
) -> frozenset[int]:
    """
    The indexes of the lines that open, hold or close a fenced code block, fenced with backticks or
    tildes.
    """
    fence_flags = [
        line.lstrip().startswith(FENCE_OPENINGS)
        for line
        in lines
    ]
    fences_so_far = list(itertools.accumulate(fence_flags))
    fenced = frozenset(
        index
        for index, is_fence
        in enumerate(fence_flags)
        if is_fence or fences_so_far[index] % 2 == 1
    )

    return fenced


def _figure_text(
    line: str,
    opens_heading: bool,
) -> str:
    """
    A line with what never holds a figure blanked out: links, inline code, URLs, citations and a
    heading's opening number.
    """
    without_number = HEADING_NUMBER.sub(r'\1', line) if opens_heading else line
    without_links = _without_links(without_number)
    without_citations = CITATION.sub(
        _blank,
        without_links,
    )
    without_references = REFERENCE.sub(
        _blank,
        without_citations,
    )
    without_tags = LATEX_TAG.sub(
        _blank,
        without_references,
    )

    return without_tags


def _is_year(
    text: str,
) -> bool:
    """
    Whether a figure is a year: four bare digits, no sign, separator, decimal or percent, from 1500
    to 2099.
    """
    is_four_digits = len(text) == 4 and text.isdigit()
    is_year = is_four_digits and int(text) in YEAR_RANGE

    return is_year


def _make_block(
    lines: list[tuple[int, str]],
) -> Block:
    """
    A block of the lines gathered so far, a copy of them, marked when its first line is a heading.
    """
    block = Block(
        lines=list(lines),
        is_heading=bool(HEADING.match(lines[0][1])),
    )

    return block


def _offsets(
    outcome: FigureOutcome,
) -> set[int]:
    """
    Every offset, found page less cited page, one figure found elsewhere could sit at.
    """
    offsets = {
        found - cited
        for found
        in outcome.other_pages
        for cited
        in outcome.figure.cited_pages
    }

    return offsets


def _outcome_counts(
    outcomes: list[FigureOutcome],
) -> str:
    """
    How many figures had each outcome, as the summary line writes it.
    """
    counts = collections.Counter(
        outcome.outcome
        for outcome
        in outcomes
    )
    summary = ', '.join(
        f'{counts[name]} {name}'
        for name
        in OUTCOMES
    )

    return summary


def _outcome_line(
    outcome: FigureOutcome,
) -> str:
    """
    One figure as the report lists it: outcome, line, figure, cited pages, and the pages that hold it.
    """
    cited = ', '.join(
        str(page)
        for page
        in sorted(outcome.figure.cited_pages)
    )
    others = ', '.join(
        str(page)
        for page
        in outcome.other_pages
    )
    found_on = f' — found on p. {others}' if others else ''
    figure = outcome.figure
    line = f'  {outcome.outcome}: line {figure.line} "{figure.text}" (cites p. {cited}){found_on}'

    return line


def _page_range(
    match: re.Match[str],
) -> range:
    """
    The pages one cited number or range names, inclusive.
    """
    first_page = int(match.group(1))
    last_text = match.group(2) or match.group(1)
    last_page = int(last_text)
    pages = range(first_page, last_page + 1)

    return pages


def _unchecked_source(
    local_copy: str,
    extracts_root: pathlib.Path,
) -> str | None:
    """
    Why a note's source cannot be checked, or None when its extract is on disk.
    """
    if not local_copy or local_copy.lower() == 'none':

        return 'no local_copy'

    if not local_copy.lower().endswith('.pdf'):
        not_pdf = f'local_copy is not a PDF: {local_copy}'

        return not_pdf

    if (extracts_root / extract_slug(local_copy)).is_dir():

        return None

    folder = _extract_folder(
        local_copy,
        extracts_root,
    )
    command = f'uv run extract.py "{local_copy}" --all --out "{extracts_root.as_posix()}"'
    no_extract = f'no extract on disk at {folder}; regenerate it with {command}'

    return no_extract


def _values_on_page(
    page_text: str,
) -> frozenset[str]:
    """
    Every number on an extracted page, as it is compared.
    """
    values = frozenset(
        normalise(number)
        for number
        in PAGE_NUMBER.findall(page_text)
    )

    return values


def _without_links(
    text: str,
) -> str:
    """
    A text with markdown links, inline code and URLs blanked out: a link names another note, and its
    target is a path.
    """
    without_links = MARKDOWN_LINK.sub(
        _blank,
        text,
    )
    without_code = INLINE_CODE.sub(
        _blank,
        without_links,
    )
    without_urls = URL.sub(
        _blank,
        without_code,
    )

    return without_urls


if __name__ == '__main__':
    sys.exit(main())
