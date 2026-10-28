"""
What the library scripts beside this file read alike: which library a folder is, its markdown files
and its sources, their frontmatter and their links.

A library is a researcher's home — the folder that holds `RESEARCHER.md`, with its notes in
`Knowledge/`, its sources in `Sources/` and its studies in `Studies/` — or a strategy, the folder
that holds `Bibliotheca/`, whose notes sit beside their PDFs in `Bibliotheca/Papers/` and
`Bibliotheca/Books/`, with its clippings in `Bibliotheca/Notes/`. `unread_sources.py`,
`check_library.py` and `update_concept_pages.py` import it; it has no command line of its own, needs
only the standard library, and writes nothing.
"""
import argparse
import dataclasses
import itertools
import os
import pathlib
import re
import string
import sys
import typing
import unicodedata
import urllib.parse

# What each markdown file of a library is, as `file_kind` names it.
BOOK_INDEX = 'book index'
CHAPTER = 'chapter'
CONCEPT = 'concept'
INDEX = 'index'
LOG = 'log'
PAPER = 'paper'
STRAY = 'stray'
STUDY = 'study'
SYNTHESIS = 'synthesis'
# The kinds that are notes on a source, and the pages built from them.
NOTE_KINDS = frozenset({
    BOOK_INDEX,
    CHAPTER,
    PAPER,
})
PAGE_KINDS = frozenset({
    CONCEPT,
    SYNTHESIS,
})
# Files a file manager, a sync tool or git leaves in a folder: never a source.
IGNORED_FILE_NAMES = frozenset({
    '.DS_Store',
    '.gitkeep',
    'Thumbs.db',
    'desktop.ini',
})
# The pieces a link is read by, as CommonMark reads them: a backslash before an ASCII punctuation
# mark makes it a plain character, so `\[` opens no link and `\]` closes none; a character of a
# link's text is such a mark, a backslash before anything else, a line break that is not a blank
# line, or any character but a bracket.
ASCII_PUNCTUATION = f'[{re.escape(string.punctuation)}]'
ESCAPED_PUNCTUATION = rf'\\{ASCII_PUNCTUATION}'
LINK_TEXT_CHARACTER = rf'(?:{ESCAPED_PUNCTUATION}|\\(?!{ASCII_PUNCTUATION})|\n(?![ \t]*\n)|[^\[\]\\\n])'
# The markdown a file is read by.
FENCE = re.compile(r'^\s*(```|~~~)')
FRONTMATTER_FIELD = re.compile(r'^([A-Za-z_][\w-]*):\s*(.*)$')
FRONTMATTER_ITEM = re.compile(r'^\s+-\s*(.*)$')
INLINE_CODE = re.compile(r'`[^`\n]*`')
# A link, or an escaped mark, which a scan from the left steps over so that no link opens at it. A
# link's text may hold one level of balanced brackets, `entry *[0.3.0]*`, and run over a line
# break, as a wrapped paragraph does, but never over a blank line; its target may hold one level of
# balanced parentheses, `Markowitz_(1952).md`, or anything between angle brackets,
# `<A paper, with commas.md>`.
MARKDOWN_LINK = re.compile('|'.join([
    rf'(?P<escaped>{ESCAPED_PUNCTUATION})',
    ''.join([
        rf'!?\[(?P<text>(?:{LINK_TEXT_CHARACTER}|\[{LINK_TEXT_CHARACTER}*\])*)\]',
        r'\((?P<target><[^>\n]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+"[^"\n]*")?\)',
    ]),
]))
QUOTES = '"\''
URL_SCHEME = re.compile(r'^[A-Za-z][A-Za-z0-9+.-]*:')
WINDOWS_DRIVE = re.compile(r'^[A-Za-z]:[\\/]')
WORD = re.compile(r'[A-Za-z0-9]+')


@dataclasses.dataclass(frozen=True)
class Frontmatter:
    """
    A markdown file's YAML frontmatter, read only as deep as the notes write it: each top-level field
    with the text after its colon, the items of a field written as a block list, and where the body
    starts.
    """
    body_start: int
    fields: dict[str, str]
    items: dict[str, list[str]]


@dataclasses.dataclass(frozen=True)
class Library:
    """
    A home or a strategy: its root, its kind, and the folders and files its library is made of.
    """
    extracts: pathlib.Path
    index: pathlib.Path
    kind: str
    log: pathlib.Path
    notes_root: pathlib.Path
    root: pathlib.Path


@dataclasses.dataclass(frozen=True)
class LibraryFile:
    """
    One markdown file of a library: its path, what it is, its text and its frontmatter.
    """
    front: Frontmatter
    kind: str
    path: pathlib.Path
    text: str


@dataclasses.dataclass(frozen=True)
class Link:
    """
    One markdown link: the line it is on, its text, and its target as written.
    """
    line: int
    target: str
    text: str


class CommandLineParser(argparse.ArgumentParser):
    """
    The argument parser the library scripts share: it exits 1 on a command line it rejects, so that
    2 keeps the meaning each script gives it — a source unread, a finding.
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


def clean_target(
    target: str,
) -> str:
    """
    A link's target as a path: angle brackets, an anchor and a query dropped, percent escapes read.
    """
    bare = target.strip()
    unbracketed = bare[1:-1] if bare.startswith('<') and bare.endswith('>') else bare
    without_anchor = unbracketed.split('#', 1)[0]
    without_query = without_anchor.split('?', 1)[0]
    cleaned = urllib.parse.unquote(without_query)

    return cleaned


def collapsed(
    path: pathlib.Path,
) -> pathlib.Path:
    """
    A path with its `..` and `.` folded away, without touching the disk: on Windows a path that
    climbs out and back in can pass 260 characters, and is then not found, though the file is there.
    """
    folded = os.path.normpath(path)
    collapsed_path = pathlib.Path(folded)

    return collapsed_path


def comparable_path(
    path: pathlib.Path,
) -> str:
    """
    A path as two paths to one file compare equal: absolute, normalised, in one Unicode form, and in
    the case the platform folds to.
    """
    absolute = os.path.abspath(path)
    composed = unicodedata.normalize(
        'NFC',
        absolute,
    )
    normalised = os.path.normpath(composed)
    comparable = os.path.normcase(normalised)

    return comparable


def configure_console() -> None:
    """
    Print UTF-8 whatever the console's code page, so a name in any alphabet — Łucja, Sofía, a title
    with an en dash — prints under `python -I`, which ignores `PYTHONIOENCODING`.
    """
    for console_stream in (sys.stdout, sys.stderr):
        try:
            console_stream.reconfigure(
                encoding='utf-8',
                errors='replace',
            )
        except (AttributeError, ValueError):
            pass


def counted(
    count: int,
    noun: str,
) -> str:
    """
    A count and its noun, the noun plural but for one: `1 note`, `3 notes`.
    """
    plural = '' if count == 1 else 's'
    text = f'{count} {noun}{plural}'

    return text


def fenced_lines(
    lines: list[str],
) -> frozenset[int]:
    """
    The indexes of the lines that open, hold or close a fenced code block; one never closed runs to
    the end.
    """
    fence_indexes = [
        index
        for index, line
        in enumerate(lines)
        if FENCE.match(line)
    ]
    closings = fence_indexes[1::2] + [len(lines) - 1]
    pairs = zip(
        fence_indexes[0::2],
        closings,
    )
    fenced = frozenset(
        index
        for opening, closing
        in pairs
        for index
        in range(opening, closing + 1)
    )

    return fenced


def field_value(
    front: Frontmatter,
    name: str,
) -> str:
    """
    A frontmatter field's text, its quotes and spaces stripped; empty when the field is absent.
    """
    raw = front.fields.get(name, '')
    value = unquoted(raw)

    return value


def file_kind(
    library: Library,
    path: pathlib.Path,
    front: Frontmatter,
) -> str:
    """
    What a markdown file of the library is, from where it sits and its `type` field.
    """
    if library.kind == 'home':
        kind = _home_kind(
            library,
            path,
            front,
        )
    else:
        kind = _strategy_kind(
            library,
            path,
        )

    return kind


def find_library(
    folder: pathlib.Path,
) -> Library | None:
    """
    The library whose root is this folder — a home when it holds `RESEARCHER.md`, a strategy when it
    holds `Bibliotheca/` — or None.
    """
    root = folder.resolve()

    if (root / 'RESEARCHER.md').is_file():
        home = Library(
            extracts=root / 'Extracts',
            index=root / 'Knowledge' / 'INDEX.md',
            kind='home',
            log=root / 'Knowledge' / 'LOG.md',
            notes_root=root / 'Knowledge',
            root=root,
        )

        return home

    if (root / 'Bibliotheca').is_dir():
        strategy = Library(
            extracts=root / 'Bibliotheca' / 'Extracts',
            index=root / 'Bibliotheca' / 'BIBLIOGRAPHY.md',
            kind='strategy',
            log=root / 'Bibliotheca' / 'LOG.md',
            notes_root=root / 'Bibliotheca',
            root=root,
        )

        return strategy

    return None


def is_local_target(
    target: str,
) -> bool:
    """
    Whether a link's target is a file of this computer: not a web address, a mail address or an
    anchor in the same file.
    """
    stripped = target.strip()
    is_bracketed = stripped.startswith('<') and stripped.endswith('>')
    bare = stripped[1:-1].strip() if is_bracketed else stripped
    is_anchor = bare.startswith('#') or not bare
    is_drive = bool(WINDOWS_DRIVE.match(bare))
    has_scheme = bool(URL_SCHEME.match(bare)) and not is_drive
    local = not is_anchor and not has_scheme

    return local


def library_files(
    library: Library,
) -> list[LibraryFile]:
    """
    Every markdown file of the library, read: at home every file under `Knowledge/` and `Studies/`;
    in a strategy `BIBLIOGRAPHY.md`, `LOG.md` and every file under `Bibliotheca/Papers/` and
    `Bibliotheca/Books/`.
    """
    if library.kind == 'home':
        folders = [
            library.notes_root,
            library.root / 'Studies',
        ]
        loose_files = []
    else:
        folders = [
            library.notes_root / 'Papers',
            library.notes_root / 'Books',
        ]
        loose_files = [
            library.index,
            library.log,
        ]

    walked = {
        path
        for folder
        in folders
        if folder.is_dir()
        for path
        in folder.rglob('*.md')
        if path.is_file()
    }
    loose = {
        path
        for path
        in loose_files
        if path.is_file()
    }
    files = [
        _read_file(
            library,
            path,
        )
        for path
        in sorted(walked | loose)
    ]

    return files


def link_path(
    file_path: pathlib.Path,
    target: str,
) -> pathlib.Path:
    """
    The file a local link's target names, from the folder of the file that holds the link.
    """
    cleaned = clean_target(target)
    given = pathlib.Path(cleaned)
    names_drive = WINDOWS_DRIVE.match(cleaned) is not None
    is_absolute = given.is_absolute() or names_drive
    joined = given if is_absolute else file_path.parent / given
    resolved = collapsed(joined)

    return resolved


def local_copy_path(
    library: Library,
    note: LibraryFile,
) -> pathlib.Path | None:
    """
    The file a note's `local_copy` names, or None when it names none. A path is read from the
    library's root first, then from the note's own folder — a strategy's PDF beside its note — and
    the first that exists is the one; when neither does, the root's reading is given.
    """
    value = field_value(
        note.front,
        'local_copy',
    )

    if not value or value.casefold() == 'none':

        return None

    forward = value.replace('\\', '/')
    given = pathlib.Path(forward)

    if given.is_absolute() or WINDOWS_DRIVE.match(forward):

        return collapsed(given)

    candidates = [
        collapsed(library.root / given),
        collapsed(note.path.parent / given),
    ]
    existing = [
        candidate
        for candidate
        in candidates
        if candidate.is_file()
    ]
    found = existing[0] if existing else candidates[0]

    return found


def markdown_links(
    text: str,
) -> list[Link]:
    """
    Every markdown link in a text, outside fenced code and inline code, with the number of the line
    it opens on — a link whose text wraps onto the next line, or holds brackets, included; an
    escaped bracket, `\\[`, opens none.
    """
    lines = text.splitlines()
    fenced = fenced_lines(lines)
    visible_lines = [
        '' if index in fenced else INLINE_CODE.sub('', line)
        for index, line
        in enumerate(lines)
    ]
    visible = '\n'.join(visible_lines)
    links = [
        Link(
            line=_line_number(
                visible,
                match.start(),
            ),
            target=match.group('target'),
            text=match.group('text'),
        )
        for match
        in MARKDOWN_LINK.finditer(visible)
        if match.group('escaped') is None
    ]

    return links


def parse_frontmatter(
    text: str,
) -> Frontmatter:
    """
    A file's frontmatter: the lines between a first line `---` and the next `---`; none when the
    file does not open with one, or never closes it.
    """
    lines = text.splitlines()
    opens = bool(lines) and lines[0].strip() == '---'
    closing = next(
        (
            position
            for position
            in range(1, len(lines))
            if lines[position].strip() == '---'
        ),
        None,
    ) if opens else None

    if closing is None:
        empty = Frontmatter(
            body_start=0,
            fields={},
            items={},
        )

        return empty

    body_lines = lines[1:closing]
    field_matches = [
        FRONTMATTER_FIELD.match(line)
        for line
        in body_lines
    ]
    line_fields = [
        None if match is None else match.group(1)
        for match
        in field_matches
    ]
    owners = list(itertools.accumulate(
        line_fields,
        _later_field,
    ))
    fields = {
        match.group(1): match.group(2)
        for match
        in field_matches
        if match is not None
    }
    items = {
        name: [
            unquoted(item_match.group(1))
            for line, owner
            in zip(body_lines, owners)
            if owner == name
            for item_match
            in [FRONTMATTER_ITEM.match(line)]
            if item_match is not None
        ]
        for name
        in fields
    }
    front = Frontmatter(
        body_start=closing + 1,
        fields=fields,
        items=items,
    )

    return front


def relative_name(
    library: Library,
    path: pathlib.Path,
) -> str:
    """
    A path as the reports print it: from the library's root, with forward slashes, when it is
    inside the root; otherwise in full.
    """
    try:
        inside = path.resolve().relative_to(library.root)
    except ValueError:

        return path.as_posix()

    name = inside.as_posix()

    return name


def source_files(
    library: Library,
) -> list[pathlib.Path]:
    """
    Every source of the library: at home, every file under `Sources/`; in a strategy, every file
    under `Bibliotheca/Papers/` and `Bibliotheca/Books/` that is not a note, and every file under
    `Bibliotheca/Notes/`. What a file manager leaves, and a hidden file, is never a source.
    """
    if library.kind == 'home':
        folders_and_note_rule = [
            (library.root / 'Sources', False),
        ]
    else:
        folders_and_note_rule = [
            (library.notes_root / 'Papers', True),
            (library.notes_root / 'Books', True),
            (library.notes_root / 'Notes', False),
        ]

    sources = sorted(
        path
        for folder, notes_beside
        in folders_and_note_rule
        if folder.is_dir()
        for path
        in folder.rglob('*')
        if path.is_file()
        and _is_source_name(
            path,
            notes_beside,
        )
    )

    return sources


def unquoted(
    text: str,
) -> str:
    """
    A frontmatter value without the spaces and the quotes around it.
    """
    stripped = text.strip()
    without_quotes = stripped.strip(QUOTES)
    value = without_quotes.strip()

    return value


def without_links(
    text: str,
) -> str:
    """
    A text with each markdown link replaced by its text, as it reads once rendered:
    `[Backtest Engine](../Lab/Backtest-Engine)` gives `Backtest Engine`.
    """
    plain = MARKDOWN_LINK.sub(
        _shown_text,
        text,
    )

    return plain


def words(
    text: str,
) -> list[str]:
    """
    A text's words in plain ASCII, accents dropped and case folded: `López de Prado` gives `lopez`,
    `de`, `prado`.
    """
    decomposed = unicodedata.normalize(
        'NFKD',
        text,
    )
    ascii_bytes = decomposed.encode(
        'ascii',
        'ignore',
    )
    ascii_text = ascii_bytes.decode('ascii')
    found = [
        word.casefold()
        for word
        in WORD.findall(ascii_text)
    ]

    return found


def _home_kind(
    library: Library,
    path: pathlib.Path,
    front: Frontmatter,
) -> str:
    """
    What a markdown file at home is: the index or the log at the top of `Knowledge/`, a paper or a
    page in a domain folder, a book's index or a chapter one folder down, a study under `Studies/`.
    """
    try:
        parts = path.relative_to(library.notes_root).parts
    except ValueError:

        return STUDY

    raw_type = field_value(
        front,
        'type',
    )
    page_type = raw_type.casefold()
    top_names = {
        'INDEX.md': INDEX,
        'LOG.md': LOG,
    }

    if len(parts) == 1:
        kind = top_names.get(parts[0], STRAY)
    elif len(parts) == 2:
        kind = page_type if page_type in PAGE_KINDS else PAPER
    elif len(parts) == 3:
        kind = BOOK_INDEX if parts[2] == 'INDEX.md' else CHAPTER
    else:
        kind = STRAY

    return kind


def _is_source_name(
    path: pathlib.Path,
    notes_beside: bool,
) -> bool:
    """
    Whether a file could be a source: not what a file manager leaves, not hidden, and, in a folder
    whose notes sit beside their sources, not a note.
    """
    is_left_behind = path.name in IGNORED_FILE_NAMES or path.name.startswith('.')
    is_note = notes_beside and path.suffix.lower() == '.md'
    is_source = not is_left_behind and not is_note

    return is_source


def _later_field(
    previous: str | None,
    current: str | None,
) -> str | None:
    """
    The field a frontmatter line belongs to: its own when it opens one, else the one before it.
    """
    owner = previous if current is None else current

    return owner


def _line_number(
    text: str,
    position: int,
) -> int:
    """
    The number of the line a position of a text falls on, counted from 1.
    """
    breaks_before = text.count(
        '\n',
        0,
        position,
    )
    number = breaks_before + 1

    return number


def _read_file(
    library: Library,
    path: pathlib.Path,
) -> LibraryFile:
    """
    One markdown file, read as UTF-8 with any byte order mark dropped, and its kind.
    """
    text = path.read_text(
        encoding='utf-8-sig',
        errors='replace',
    )
    front = parse_frontmatter(text)
    kind = file_kind(
        library,
        path,
        front,
    )
    read_file = LibraryFile(
        front=front,
        kind=kind,
        path=path,
        text=text,
    )

    return read_file


def _shown_text(
    match: re.Match[str],
) -> str:
    """
    What a match of a link, or of an escaped mark, shows once rendered: the link's text, or the
    escape as written.
    """
    escaped = match.group('escaped')
    shown = match.group('text') if escaped is None else escaped

    return shown


def _strategy_kind(
    library: Library,
    path: pathlib.Path,
) -> str:
    """
    What a markdown file of a strategy's `Bibliotheca/` is: its bibliography, its log, a paper's note
    in `Papers/`, a book's index or a chapter in `Books/<book>/`.
    """
    parts = path.relative_to(library.notes_root).parts

    if parts == ('BIBLIOGRAPHY.md',):
        kind = INDEX
    elif parts == ('LOG.md',):
        kind = LOG
    elif len(parts) == 2 and parts[0] == 'Papers':
        kind = PAPER
    elif len(parts) == 3 and parts[0] == 'Books':
        kind = BOOK_INDEX if parts[2] == 'INDEX.md' else CHAPTER
    else:
        kind = STRAY

    return kind
