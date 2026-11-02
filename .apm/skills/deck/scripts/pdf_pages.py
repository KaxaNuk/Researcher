"""
A deck as a PDF, one page a slide, each slide at its last step: printed by Chrome or Edge, with no
window, from the deck `present` serves.

    uv run --no-project --with playwright --with pypdf python -I pdf_pages.py http://localhost:3004 "D:/Decks/Q3 review/Q3 review.pdf"

What it does
    the slides    reads the deck the page's player loads, its list of slides and each slide's
                  start and length, as the deck's own markup gives them
    each page     opens the deck in Chrome or Edge, already on this computer, with no window; moves
                  it to the end of each slide, so every reveal shows; and prints that moment as one
                  page the deck's size, backgrounds on
    the file      joins the pages in the slides' order, branches left out, into the PDF named

It moves a deck that drives its own slides, setting `window.__hfSetTime` as the slideshow skill's
standalone harness does; a deck without one is printed from the browser, by hand. It reads only
the deck's `present` server on this computer, sends nothing and writes only the file named.
Exit codes: 0 written · 1 usage: an address not on this computer, no answer there, no browser, a
folder that does not exist, or a deck that does not drive its own slides.
"""
import argparse
import dataclasses
import html
import io
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

import typing

import pypdf

__all__ = [
    'Slide',
    'main',
    'slides_of',
]

BROWSER_CHANNELS = (
    'chrome',
    'msedge',
)
ISLAND = re.compile(
    r'<script[^>]*type=["\']application/hyperframes-slideshow\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
LOCAL_HOSTS = frozenset({
    '127.0.0.1',
    '::1',
    'localhost',
})
PLAYER_SOURCE = re.compile(r'<hyperframes-player\b[^>]*\ssrc=["\']([^"\']+)["\']', re.IGNORECASE)
SCENE_TAG = re.compile(r'<[a-zA-Z][\w-]*\s[^<>]*\bdata-composition-id=["\']([^"\']+)["\'][^<>]*>')
SELF_DRIVEN = 'typeof window.__hfSetTime === "function"'
# How far before a slide's end its last step is printed, in seconds, and how long each move waits
# for the entrance effects that run in real time, a typed line among them.
SETTLE_SECONDS = 0.1
SETTLE_MILLISECONDS = 1700
LOAD_MILLISECONDS = 1500


@dataclasses.dataclass(frozen=True)
class Slide:
    """
    One slide of the deck's main line: its scene, and the moment its last step shows.
    """
    scene_id: str
    last_moment: float


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, read the deck's slides, and print them into one PDF.
    """
    _configure_console()
    parsed = _build_parser().parse_args(arguments)
    address = parsed.address.rstrip('/') + '/'
    output = pathlib.Path(parsed.output)
    problem = _usage_problem(
        address,
        output,
    )

    if problem:
        print(
            problem,
            file=sys.stderr,
        )

        return 1

    page = _fetch_text(address)
    player = PLAYER_SOURCE.search(page or '')

    if page is None or player is None:
        no_deck = f'no deck at {address}: is `npx hyperframes present` serving it?'
        print(
            no_deck,
            file=sys.stderr,
        )

        return 1

    player_source = html.unescape(player.group(1))
    deck_address = urllib.parse.urljoin(
        address,
        player_source,
    )
    deck = _fetch_text(deck_address) or ''
    slides = slides_of(deck)

    if not slides:
        no_slides = f'no slides in the deck at {deck_address}'
        print(
            no_slides,
            file=sys.stderr,
        )

        return 1

    size = _deck_size(deck)
    pages = _printed_pages(
        deck_address,
        slides,
        size,
    )

    if pages is None:
        return 1

    writer = pypdf.PdfWriter()

    for printed in pages:
        printed_stream = io.BytesIO(printed)
        writer.append(pypdf.PdfReader(printed_stream))

    with output.open('wb') as handle:
        writer.write(handle)
    written = f'wrote {output} — {len(pages)} pages, one a slide'
    print(written)

    return 0


def slides_of(
    deck: str,
) -> list[Slide]:
    """
    The deck's main-line slides, in order, each with the moment its last step shows: its scene's
    start plus its length, less a moment; branches are left out.
    """
    island_match = ISLAND.search(deck)

    if island_match is None:
        return []

    island = json.loads(island_match.group(1))
    timings = _scene_timings(deck)
    slides = [
        Slide(
            scene_id=slide['sceneId'],
            last_moment=round(
                timings[slide['sceneId']] - SETTLE_SECONDS,
                3,
            ),
        )
        for slide in island.get('slides', [])
        if slide.get('sceneId') in timings
    ]

    return slides


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: the address `present` printed, and the PDF to write.
    """
    parser = argparse.ArgumentParser(
        prog='pdf_pages.py',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'address',
        help='the address `npx hyperframes present` printed, such as http://localhost:3004',
    )
    parser.add_argument(
        'output',
        help='the PDF to write, in a folder that exists',
    )

    return parser


def _configure_console() -> None:
    """
    UTF-8 on the console, as under `python -I`, which ignores PYTHONIOENCODING.
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


def _deck_size(
    deck: str,
) -> tuple:
    """
    The deck's width and height in pixels, from its first scene, 1920 by 1080 when it names none.
    """
    width = re.search(r'\bdata-width=["\'](\d+)["\']', deck)
    height = re.search(r'\bdata-height=["\'](\d+)["\']', deck)
    size = (
        int(width.group(1)) if width else 1920,
        int(height.group(1)) if height else 1080,
    )

    return size


def _fetch_text(
    address: str,
) -> str | None:
    """
    The text at an address on this computer, or None when it gives no answer.
    """
    try:
        with urllib.request.urlopen(address, timeout=30) as response:
            body = response.read()
    except (OSError, urllib.error.URLError):
        return None

    text = body.decode(
        'utf-8',
        errors='replace',
    )

    return text


def _launched(
    playwright: typing.Any,
    browser_error: type[Exception],
) -> typing.Any:
    """
    Chrome, else Edge, already on this computer, with no window; None when neither is there.
    """
    for channel in BROWSER_CHANNELS:
        try:
            browser = playwright.chromium.launch(channel=channel)
        except browser_error:
            continue

        return browser

    return None


def _move_to(
    page: typing.Any,
    moment: float,
) -> None:
    """
    The deck moved to a moment: every timeline it registers sought there, and its own slides shown
    for it, twice, so a scene that only starts on the first move settles on the second.
    """
    script = ''.join([
        '(moment) => { for (const timeline of Object.values(window.__timelines || {})) ',
        '{ timeline.pause(); timeline.seek(moment, false); } window.__hfSetTime(moment); }',
    ])

    for _ in range(2):
        page.evaluate(
            script,
            moment,
        )
        page.wait_for_timeout(SETTLE_MILLISECONDS)


def _printed_pages(
    deck_address: str,
    slides: list[Slide],
    size: tuple,
) -> list[bytes] | None:
    """
    One printed page a slide, at its last step; None, said on the console, when no browser opens
    or the deck does not drive its own slides.
    """
    # Playwright is loaded here only, so the slides can be read, and tested, without a browser.
    import playwright.sync_api  # noqa: PLC0415 - loaded only where a browser is opened.

    width, height = size

    with playwright.sync_api.sync_playwright() as browser_driver:
        browser = _launched(
            browser_driver,
            playwright.sync_api.Error,
        )

        if browser is None:
            no_browser = 'neither Chrome nor Edge opens here: print the deck from the browser'
            print(
                no_browser,
                file=sys.stderr,
            )

            return None

        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(deck_address)
        page.evaluate('document.fonts.ready')
        page.wait_for_timeout(LOAD_MILLISECONDS)

        if not page.evaluate(SELF_DRIVEN):
            browser.close()
            not_driven = 'the deck does not drive its own slides: print it from the browser'
            print(
                not_driven,
                file=sys.stderr,
            )

            return None

        page.emulate_media(media='screen')
        pages = []

        for slide in slides:
            _move_to(
                page,
                slide.last_moment,
            )
            pages.append(page.pdf(
                width=f'{width}px',
                height=f'{height}px',
                print_background=True,
                page_ranges='1',
            ))
        browser.close()

    return pages


def _scene_timings(
    deck: str,
) -> dict[str, float]:
    """
    Each scene's end, its start plus its length, by its id, from the scene's own start tag.
    """
    timings = {}

    for match in SCENE_TAG.finditer(deck):
        start = re.search(r'\bdata-start=["\']([\d.]+)["\']', match.group(0))
        duration = re.search(r'\bdata-duration=["\']([\d.]+)["\']', match.group(0))

        if start is None or duration is None or match.group(1) in timings:
            continue

        scene_id = match.group(1)
        start_seconds = float(start.group(1))
        timings[scene_id] = start_seconds + float(duration.group(1))

    return timings


def _usage_problem(
    address: str,
    output: pathlib.Path,
) -> str:
    """
    What is wrong with the command line, or an empty string.
    """
    host = urllib.parse.urlparse(address).hostname or ''

    if host not in LOCAL_HOSTS:
        not_local = f'not on this computer: {address}; give the address `present` printed'

        return not_local

    if not output.parent.is_dir():
        no_folder = f'no such folder: {output.parent}'

        return no_folder

    return ''


if __name__ == '__main__':
    sys.exit(main())
