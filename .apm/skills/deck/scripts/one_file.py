"""
A deck as one HTML file that opens with a double click and works without internet: the page
HyperFrames' `present` serves, saved with everything it loads inside it.

    uv run --no-project python -I one_file.py http://localhost:3004 "D:/Decks/Q3 review/Q3 review.html"

What it does
    the page      reads the page `present` serves at the address — on this computer only — and puts
                  each script and stylesheet it loads inside it
    the deck      reads the deck the page's player loads, puts its scripts, stylesheets, fonts,
                  images, sounds and scene files inside it as text or data, and writes it into the
                  player's `srcdoc` in place of its `src`
    the runtime   a script the page's own code names by its address, as the player names the
                  runtime it adds to a deck that lacks one, goes into the deck ahead of the deck's
                  scripts, so nothing is fetched when the file opens
    the check     lists every address on the internet the file would still fetch or that gave no
                  answer, and every file the deck names that its own server does not have, which
                  it lacks under `present` too, such as a sound effect it never added

It reads from the deck's `present` server and from the addresses the deck itself loads — a font, a
script — as the browser does when the deck is presented; it sends nothing and writes only the file
named. Exit codes: 0 written, nothing outside it · 1 usage: an address not on this computer, no
answer there, or a folder that does not exist · 2 written, with something still outside it.
"""
import argparse
import base64
import dataclasses
import functools
import html
import mimetypes
import pathlib
import re
import sys
import typing
import urllib.error
import urllib.parse
import urllib.request

# Google Fonts answers each browser with the font files it reads; this asks as a recent Chrome
# does, for WOFF2.
BROWSER_AGENT = ' '.join([
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/130.0.0.0 Safari/537.36',
])
LOCAL_HOSTS = frozenset({
    '127.0.0.1',
    '::1',
    'localhost',
})
# Attributes whose value is a file the page loads as it opens.
LOADED_ATTRIBUTES = (
    'poster',
    'src',
)
# A reference that is no file to read: already data, a fragment, or made by the page.
NOT_A_FILE = (
    '#',
    'about:',
    'blob:',
    'data:',
)
# A scene a deck mounts from its own file, as HyperFrames' composition format writes it.
SCENE_ATTRIBUTE = 'data-composition-src'
# A `<link>` the browser follows only to warm a connection: dropped, as nothing is fetched.
CONNECTION_HINTS = frozenset({
    'dns-prefetch',
    'preconnect',
    'prefetch',
})
# A script or style block, kept whole, and the markup between them.
RAW_BLOCK = re.compile(
    r'(<(script|style)\b[^>]*>)(.*?)(</\2\s*>)',
    re.IGNORECASE | re.DOTALL,
)
START_TAG = re.compile(r'<([a-zA-Z][\w-]*)(\s[^<>]*?)?(/?)>')
ATTRIBUTE = re.compile(r'([^\s=/>]+)(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s"\'>]+))?')
CSS_URL = re.compile(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)')
CSS_IMPORT = re.compile(r'@import\s+(?:url\(\s*)?(["\'])([^"\']+)\1\s*\)?\s*;')
# A quoted address in a script: an absolute one, or a path on the server that ends in a file kind
# a page loads.
SCRIPT_ADDRESS = re.compile(''.join([
    r'(["\'])((?:https?://|/)[^"\'\s<>]+?\.',
    r'(?:js|mjs|css|mp3|wav|ogg|m4a|mp4|webm|png|jpe?g|gif|svg|webp|woff2?|ttf|otf))\1',
]))
SCENE_DATA = re.compile(rf'\s{SCENE_ATTRIBUTE}="data:text/html[^,"]*;base64,([^"]*)"')
SRCDOC = re.compile(r'\ssrcdoc="([^"]*)"')
STILL_OUTSIDE = re.compile(
    r'(?:\b(?:src|href|poster)\s*=\s*["\']?|url\(\s*["\']?)(https?://[^"\'\s)>]+)',
    re.IGNORECASE,
)
# Addresses that name a format, never a file the page fetches.
FORMAT_NAMES = (
    'http://www.w3.org/',
    'https://www.w3.org/',
)


@dataclasses.dataclass(frozen=True, slots=True)
class Loaded:
    """
    A file read from its address: its bytes and its media type.
    """

    content: bytes
    media_type: str


@dataclasses.dataclass(slots=True)
class Report:
    """
    What could not be put inside the file: files the deck's own server does not have, which the
    deck lacks under `present` too, and addresses on the internet that gave no answer.
    """

    absent: list[str] = dataclasses.field(default_factory=list)
    missing: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True, slots=True)
class Reader:
    """
    How files are read, and where what gave no answer is reported.
    """

    fetch: typing.Callable[[str], Loaded | None]
    report: Report


class CommandLineParser(argparse.ArgumentParser):
    """
    The argument parser, exiting 1 on a command line it rejects, so that 2 means something outside.
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

        raise SystemExit(1)


def data_address(
    loaded: Loaded,
) -> str:
    """
    A file as a `data:` address, its bytes in base64.
    """
    encoded = base64.b64encode(loaded.content).decode('ascii')

    return f'data:{loaded.media_type};base64,{encoded}'


def inline_css(
    css: str,
    base_address: str,
    reader: Reader,
) -> str:
    """
    A stylesheet with each `@import` put in its place and each `url()` it names made a `data:`
    address, a font's included.
    """
    with_imports = CSS_IMPORT.sub(
        functools.partial(
            _imported_css,
            base_address=base_address,
            reader=reader,
        ),
        css,
    )

    return CSS_URL.sub(
        functools.partial(
            _css_url_as_data,
            base_address=base_address,
            reader=reader,
        ),
        with_imports,
    )


def inline_page(
    page: str,
    base_address: str,
    reader: Reader,
    runtime_scripts: tuple[str, ...] = (),
) -> str:
    """
    A page with every script, stylesheet and file it loads inside it, and the deck a player loads
    in its `srcdoc`. The scripts named in `runtime_scripts` go in first, ahead of the page's own.
    """
    page_scripts: list[str] = []
    inlined = _rebuilt(
        page,
        functools.partial(
            _inline_markup,
            base_address=base_address,
            reader=reader,
        ),
        functools.partial(
            _inline_block,
            base_address=base_address,
            reader=reader,
            page_scripts=page_scripts,
        ),
    )
    with_runtime = _put_first_in_head(
        inlined,
        runtime_scripts,
        reader,
    )

    return _inline_players(
        with_runtime,
        base_address,
        reader,
        tuple(page_scripts),
    )


def is_local(
    address: str,
) -> bool:
    """
    Whether an address is a server on this computer.
    """
    parts = urllib.parse.urlsplit(address)

    return parts.scheme in {'http', 'https'} and parts.hostname in LOCAL_HOSTS


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Parse the command line, write the deck as one file, and give the exit code.
    """
    _configure_console()
    arguments = _build_parser().parse_args(argv)
    address = arguments.address.rstrip('/') + '/'
    output = pathlib.Path(arguments.output)

    if not is_local(address):
        print(
            f'not an address on this computer: {arguments.address} — give the one `present` printed',
            file=sys.stderr,
        )

        return 1

    if not output.parent.is_dir():
        print(f'no such folder: {output.parent}', file=sys.stderr)

        return 1

    reader = Reader(
        read_address,
        Report(),
    )
    page = _fetch_reported(address, reader)

    if page is None:
        print(
            f'no answer at {address} — start the deck with `npx hyperframes present <folder>`',
            file=sys.stderr,
        )

        return 1

    one_file = inline_page(
        _text(page),
        address,
        reader,
    )
    output.write_text(
        one_file,
        encoding='utf-8',
        newline='\n',
    )
    outside = still_outside(one_file)
    size = len(one_file.encode('utf-8')) / 1_000_000
    print(f'wrote {output} — {size:.1f} MB')

    for absent in reader.report.absent:
        print(f'  not in the deck, as under `present`, left as it was: {absent}')

    for missing in reader.report.missing:
        print(f'  no answer, left as it was: {missing}')

    for remote in outside:
        print(f'  still fetched when it opens: {remote}')

    if reader.report.missing or outside:
        return 2

    print('  nothing outside it: it opens without internet')

    return 0


def read_address(
    address: str,
) -> Loaded | None:
    """
    A file read from an address, or None when it gives no answer or an error.
    """
    request = urllib.request.Request(
        address,
        headers={'User-Agent': BROWSER_AGENT},
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            header_type = response.headers.get_content_type()
    except (
        urllib.error.URLError,
        TimeoutError,
        ValueError,
    ):
        return None

    return Loaded(
        content,
        _media_type(address, header_type),
    )


def still_outside(
    page: str,
) -> list[str]:
    """
    Every address on the internet the page, its deck and its scenes included, would still fetch as
    it opens.
    """
    deck_texts = [
        html.unescape(match.group(1))
        for match
        in SRCDOC.finditer(page)
    ]
    scene_texts = [
        _decoded_scene(match)
        for text
        in deck_texts
        for match
        in SCENE_DATA.finditer(text)
    ]
    found = {
        match.group(1)
        for text
        in [
            page,
            *deck_texts,
            *scene_texts,
        ]
        for match
        in STILL_OUTSIDE.finditer(text)
        if not match.group(1).startswith(FORMAT_NAMES)
    }

    return sorted(found)


def _attribute_value(
    attributes: str,
    name: str,
) -> str | None:
    """
    The value of one attribute of a tag, unescaped, or None when the tag lacks it.
    """
    values = [
        _unquoted(match.group(2))
        for match
        in ATTRIBUTE.finditer(attributes)
        if match.group(1).lower() == name
    ]

    return values[0] if values else None


def _build_parser() -> CommandLineParser:
    """
    The command line: the address `present` printed, and the file to write.
    """
    parser = CommandLineParser(
        prog='one_file.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'address',
        help='the address `npx hyperframes present` printed, such as http://localhost:3004',
    )
    parser.add_argument(
        'output',
        help='the file to write, <deck-name>.html in the deck\'s folder',
    )

    return parser


def _configure_console() -> None:
    """
    Print in UTF-8 whatever the console's own encoding, as `python -I` ignores PYTHONIOENCODING.
    """
    for console_stream in (
        sys.stdout,
        sys.stderr,
    ):
        try:
            console_stream.reconfigure(
                encoding='utf-8',
                errors='replace',
            )
        except (AttributeError, ValueError):
            pass


def _css_url_as_data(
    match: re.Match[str],
    base_address: str,
    reader: Reader,
) -> str:
    """
    A stylesheet's `url()` made a `data:` address, or left as it was when it gives no answer.
    """
    reference = match.group(2).strip()

    if reference.startswith(NOT_A_FILE):
        return match.group(0)

    loaded = _fetch_reported(
        urllib.parse.urljoin(base_address, reference),
        reader,
    )

    if loaded is None:
        return match.group(0)

    return f'url("{data_address(loaded)}")'


def _deck_in_player(
    match: re.Match[str],
    base_address: str,
    reader: Reader,
    runtime_scripts: tuple[str, ...],
) -> str:
    """
    A player's start tag with the deck its `src` names read, inlined, and written into its
    `srcdoc`; any other start tag as it was.
    """
    attributes = match.group(2) or ''
    source = _attribute_value(attributes, 'src')

    if match.group(1).lower() != 'hyperframes-player' or source is None:
        return match.group(0)

    address = urllib.parse.urljoin(base_address, source)
    loaded = _fetch_reported(address, reader)

    if loaded is None:
        return match.group(0)

    deck = inline_page(
        _text(loaded),
        address,
        reader,
        runtime_scripts,
    )

    return _with_attributes(
        match.group(0),
        {'srcdoc': deck},
        ('src',),
    )


def _decoded_scene(
    match: re.Match[str],
) -> str:
    """
    A scene file's text, decoded from its `data:` address.
    """
    scene_bytes = base64.b64decode(match.group(1))

    return scene_bytes.decode('utf-8', errors='replace')


def _fetch_reported(
    address: str,
    reader: Reader,
) -> Loaded | None:
    """
    A file read from its address, its address added to the report when it gives no answer: as
    absent when the deck's own server lacks it, as missing when it is on the internet.
    """
    loaded = reader.fetch(address)
    unanswered = reader.report.absent if is_local(address) else reader.report.missing

    if loaded is None and address not in unanswered:
        unanswered.append(address)

    return loaded


def _imported_css(
    match: re.Match[str],
    base_address: str,
    reader: Reader,
) -> str:
    """
    A stylesheet's `@import` replaced by the stylesheet it names, inlined in turn.
    """
    address = urllib.parse.urljoin(base_address, match.group(2))
    loaded = _fetch_reported(address, reader)

    if loaded is None:
        return match.group(0)

    return inline_css(
        _text(loaded),
        address,
        reader,
    )


def _inline_block(
    block: re.Match[str],
    base_address: str,
    reader: Reader,
    page_scripts: list[str],
) -> str:
    """
    A script or style block with what it loads inside it: a script's file, a stylesheet's `url()`s,
    and the files an inline script names by a quoted address. Each script's text is kept in
    `page_scripts`.
    """
    opening = block.group(1)
    kind = block.group(2)
    body = block.group(3)
    closing = block.group(4)
    attributes = opening[len(kind) + 1:-1]
    source = _attribute_value(attributes, 'src')
    script_type = (_attribute_value(attributes, 'type') or '').lower()

    if kind.lower() == 'style':
        style = inline_css(
            body,
            base_address,
            reader,
        )

        return opening + style + closing

    if source is not None:
        return _inline_script_source(
            block,
            urllib.parse.urljoin(base_address, source),
            reader,
            page_scripts,
        )

    if script_type and 'javascript' not in script_type and script_type != 'module':
        return block.group(0)

    page_scripts.append(body)
    script = SCRIPT_ADDRESS.sub(
        functools.partial(
            _script_file_as_data,
            base_address=base_address,
            reader=reader,
        ),
        body,
    )

    return opening + script + closing


def _inline_link(
    tag: str,
    attributes: str,
    base_address: str,
    reader: Reader,
) -> str:
    """
    A `<link>`: a stylesheet made a `<style>` with what it loads inside it, a connection hint
    dropped, an icon made a `data:` address, anything else left as it was.
    """
    relation_text = _attribute_value(attributes, 'rel') or ''
    relation_words = relation_text.lower().split()
    relations = set(relation_words)
    reference = _attribute_value(attributes, 'href')

    if relations & CONNECTION_HINTS:
        return ''

    if not reference or reference.startswith(NOT_A_FILE):
        return tag

    address = urllib.parse.urljoin(base_address, reference)

    if not relations & {'icon', 'stylesheet'}:
        return tag

    loaded = _fetch_reported(address, reader)

    if loaded is None:
        return tag

    if 'stylesheet' in relations:
        style = inline_css(
            _text(loaded),
            address,
            reader,
        )

        return f'<style>{style}</style>'

    return _with_attributes(
        tag,
        {'href': data_address(loaded)},
    )


def _inline_markup(
    markup: str,
    base_address: str,
    reader: Reader,
) -> str:
    """
    Markup with each start tag inlined by `_inline_tag`.
    """
    return START_TAG.sub(
        functools.partial(
            _inline_tag,
            base_address=base_address,
            reader=reader,
        ),
        markup,
    )


def _inline_players(
    page: str,
    base_address: str,
    reader: Reader,
    page_scripts: tuple[str, ...],
) -> str:
    """
    The page with each player's deck written into its `srcdoc`; the scripts the page's own code
    names by an absolute address go into the deck first.
    """
    runtime_scripts = tuple(sorted({
        match.group(2)
        for script
        in page_scripts
        for match
        in SCRIPT_ADDRESS.finditer(script)
        if match.group(2).startswith(('http://', 'https://'))
        and match.group(2).endswith(('.js', '.mjs'))
    }))
    players = functools.partial(
        START_TAG.sub,
        functools.partial(
            _deck_in_player,
            base_address=base_address,
            reader=reader,
            runtime_scripts=runtime_scripts,
        ),
    )

    return _rebuilt(
        page,
        players,
        _whole_block,
    )


def _inline_script_source(
    block: re.Match[str],
    address: str,
    reader: Reader,
    page_scripts: list[str],
) -> str:
    """
    A `<script src>` block with the script it names inside it, kept in `page_scripts` too.
    """
    loaded = _fetch_reported(address, reader)

    if loaded is None:
        return block.group(0)

    script = _text(loaded)
    page_scripts.append(script)
    opening = _with_attributes(
        block.group(1),
        {},
        ('src',),
    )

    return opening + _safe_script(script) + block.group(4)


def _inline_tag(
    match: re.Match[str],
    base_address: str,
    reader: Reader,
) -> str:
    """
    A start tag with each file it loads, or its `style` attribute names, made a `data:` address,
    and a scene file inlined in turn, its paths read from the deck's folder, as HyperFrames reads
    them. A stylesheet `<link>` becomes a `<style>`; a player's `src` is left for
    `_inline_players`.
    """
    tag = match.group(1).lower()
    attributes = match.group(2) or ''

    if tag == 'link':
        return _inline_link(
            match.group(0),
            attributes,
            base_address,
            reader,
        )

    if tag == 'hyperframes-player':
        return match.group(0)

    loaded_files = {
        name: _fetch_reported(urllib.parse.urljoin(base_address, reference), reader)
        for name
        in LOADED_ATTRIBUTES
        if (reference := _attribute_value(attributes, name))
        and not reference.startswith(NOT_A_FILE)
    }
    file_values = {
        name: data_address(loaded)
        for name, loaded
        in loaded_files.items()
        if loaded is not None
    }
    scene_value = _scene_as_data(
        _attribute_value(attributes, SCENE_ATTRIBUTE),
        base_address,
        reader,
    )
    style = _attribute_value(attributes, 'style')
    style_value = {
        'style': inline_css(
            style,
            base_address,
            reader,
        ),
    } if style and 'url(' in style else {}

    return _with_attributes(
        match.group(0),
        file_values | scene_value | style_value,
    )


def _media_type(
    address: str,
    header_type: str,
) -> str:
    """
    A file's media type: the one its server gave, else the one its name suggests.
    """
    if header_type and header_type not in {'application/octet-stream', 'text/plain'}:
        return header_type

    guessed, _ = mimetypes.guess_type(urllib.parse.urlsplit(address).path)

    return guessed or header_type or 'application/octet-stream'


def _put_first_in_head(
    page: str,
    scripts: tuple[str, ...],
    reader: Reader,
) -> str:
    """
    A page with each script read from its address and put at the top of its `<head>`.
    """
    loaded_scripts = [
        _fetch_reported(address, reader)
        for address
        in scripts
    ]
    blocks = ''.join(
        f'<script>{_safe_script(_text(loaded))}</script>'
        for loaded
        in loaded_scripts
        if loaded is not None
    )
    head = re.search(
        r'<head\b[^>]*>',
        page,
        re.IGNORECASE,
    )
    insert_at = head.end() if head else 0

    return page[:insert_at] + blocks + page[insert_at:]


def _rebuilt(
    page: str,
    rewrite_markup: typing.Callable[[str], str],
    rewrite_block: typing.Callable[[re.Match[str]], str],
) -> str:
    """
    A page rewritten piece by piece: the markup between its script and style blocks by
    `rewrite_markup`, each block by `rewrite_block`, in the page's order.
    """
    blocks = list(RAW_BLOCK.finditer(page))
    block_ends = [
        block.end()
        for block
        in blocks
    ]
    block_starts = [
        block.start()
        for block
        in blocks
    ]
    starts = [
        0,
        *block_ends,
    ]
    ends = [
        *block_starts,
        len(page),
    ]
    markups = [
        rewrite_markup(page[start:end])
        for start, end
        in zip(
            starts,
            ends,
            strict=True,
        )
    ]
    block_texts = [
        rewrite_block(block)
        for block
        in blocks
    ]
    rewritten_blocks = [
        *block_texts,
        '',
    ]

    return ''.join(
        markup + block
        for markup, block
        in zip(
            markups,
            rewritten_blocks,
            strict=True,
        )
    )


def _safe_script(
    script: str,
) -> str:
    """
    A script's text made safe inside a `<script>` block: no `</script` closes it early.
    """
    return re.sub(
        r'</(script)',
        r'<\\/\1',
        script,
        flags=re.IGNORECASE,
    )


def _scene_as_data(
    scene: str | None,
    base_address: str,
    reader: Reader,
) -> dict[str, str]:
    """
    A scene file's attribute as a `data:` address of the scene inlined, its paths read from the
    deck's folder; nothing when there is no scene to read.
    """
    if not scene or scene.startswith(NOT_A_FILE):
        return {}

    loaded = _fetch_reported(
        urllib.parse.urljoin(base_address, scene),
        reader,
    )

    if loaded is None:
        return {}

    scene_page = inline_page(
        _text(loaded),
        base_address,
        reader,
    )
    scene_file = Loaded(
        scene_page.encode('utf-8'),
        'text/html;charset=utf-8',
    )

    return {SCENE_ATTRIBUTE: data_address(scene_file)}


def _script_file_as_data(
    match: re.Match[str],
    base_address: str,
    reader: Reader,
) -> str:
    """
    A sound, image or font an inline script names by a quoted path on the server, made a `data:`
    address; a script, an address on the internet, or a path that gives no answer left as it was.
    """
    reference = match.group(2)

    if reference.startswith(('http://', 'https://')) or reference.endswith(('.js', '.mjs')):
        return match.group(0)

    loaded = _fetch_reported(
        urllib.parse.urljoin(base_address, reference),
        reader,
    )

    if loaded is None:
        return match.group(0)

    quote = match.group(1)

    return f'{quote}{data_address(loaded)}{quote}'


def _text(
    loaded: Loaded,
) -> str:
    """
    A text file's content, read as UTF-8.
    """
    return loaded.content.decode('utf-8', errors='replace')


def _unquoted(
    value: str | None,
) -> str:
    """
    An attribute's value without its quotes, its character references unescaped.
    """
    bare = (value or '').strip('"\'')

    return html.unescape(bare)


def _whole_block(
    block: re.Match[str],
) -> str:
    """
    A script or style block as it was.
    """
    return block.group(0)


def _with_attributes(
    tag: str,
    values: dict[str, str],
    removed: tuple[str, ...] = (),
) -> str:
    """
    A start tag with some attributes set to values, escaped for double quotes, and others removed.
    """
    pattern = re.compile(
        ''.join([
            r'\s(?:',
            '|'.join(
                re.escape(name)
                for name
                in [*values, *removed]
            ),
            r')(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s"\'>]+))?(?=[\s/>])',
        ]),
        re.IGNORECASE,
    )
    without = pattern.sub('', tag) if values or removed else tag
    closing = '/>' if without.endswith('/>') else '>'
    added = ''.join(
        f' {name}="{html.escape(value, quote=True)}"'
        for name, value
        in values.items()
    )

    return without[:-len(closing)].rstrip() + added + closing


if __name__ == '__main__':
    sys.exit(main())
