"""
A deck as one HTML file, one_file.py: the page `present` serves with every script, stylesheet,
font, image and scene inside it, the deck in the player's `srcdoc`, the runtime the player's code
names put in the deck first, and what is still outside reported — all from a fake server, never
the network.
"""
import base64
import html
import re

import pytest

import one_file

__all__ = []

SERVER = 'http://localhost:3004/'
RUNTIME = 'https://cdn.example.org/npm/core@1.0.0/dist/runtime.iife.js'
FILES = {
    SERVER: ''.join([
        '<!doctype html><html><head>',
        '<script src="/player.js"></script>',
        '</head><body>',
        '<hyperframes-slideshow tabindex="0">',
        '<hyperframes-player interactive src="/composition/index.html"></hyperframes-player>',
        '<script type="application/hyperframes-slideshow+json">{"slides": []}</script>',
        '</hyperframes-slideshow>',
        '<script>var clips = [new Audio("/composition/sfx/advance.mp3"),',
        ' new Audio("/composition/sfx/back.mp3")];</script>',
        '</body></html>',
    ]),
    f'{SERVER}player.js': f'var q="{RUNTIME}";var end="</script>";',
    RUNTIME: 'window.__player = {};',
    f'{SERVER}composition/sfx/advance.mp3': 'ID3-sound',
    f'{SERVER}composition/index.html': ''.join([
        '<!doctype html><html><head>',
        '<script src="https://cdn.example.org/gsap.min.js"></script>',
        '<link rel="preconnect" href="https://fonts.example.org" />',
        '<link href="https://fonts.example.org/css2?family=Serif" rel="stylesheet" />',
        '</head><body>',
        '<div id="root" data-composition-id="main">',
        '<div id="intro" data-composition-id="intro" data-composition-src="compositions/intro.html">',
        '</div></div></body></html>',
    ]),
    'https://cdn.example.org/gsap.min.js': 'window.gsap = {};',
    'https://fonts.example.org/css2?family=Serif': ''.join([
        '@font-face { font-family: "Serif"; ',
        'src: url(https://fonts.example.org/s/serif.woff2); }',
    ]),
    'https://fonts.example.org/s/serif.woff2': 'wOF2-font',
    f'{SERVER}composition/compositions/intro.html': ''.join([
        '<template><div id="root" data-composition-id="intro">',
        '<img id="intro-logo" src="assets/logo.svg" alt="Logo" />',
        '</div></template>',
    ]),
    f'{SERVER}composition/assets/logo.svg': '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
}


def test_a_file_the_server_lacks_is_absent_and_an_internet_one_is_missing() -> None:
    """
    A sound the deck's own server does not have is left as it was and reported as absent, as
    under `present`; an address on the internet that gives no answer is reported as missing.
    """
    files = {
        address: content
        for address, content
        in FILES.items()
        if address != 'https://cdn.example.org/gsap.min.js'
    }
    reader = one_file.Reader(
        lambda address: _fake_fetch(address, files),
        one_file.Report(),
    )
    page = one_file.inline_page(
        files[SERVER],
        SERVER,
        reader,
    )

    assert reader.report.absent == [f'{SERVER}composition/sfx/back.mp3']
    assert reader.report.missing == ['https://cdn.example.org/gsap.min.js']
    assert '"/composition/sfx/back.mp3"' in page
    assert 'data:audio/mpeg;base64,' in page
    assert one_file.still_outside(page) == ['https://cdn.example.org/gsap.min.js']


def test_a_self_driven_deck_gets_no_runtime() -> None:
    """
    A deck that drives its own slides, setting `window.__hfSetTime` as the slideshow skill's
    standalone harness does, gets no runtime, which would take its slides over, and the note that
    keeps the player from fetching one into its `srcdoc` from the internet.
    """
    harness = '<script>window.__hfSetTime = function (time) {};</script>'
    files = {
        **FILES,
        f'{SERVER}composition/index.html': FILES[f'{SERVER}composition/index.html'].replace(
            '</head>',
            f'{harness}</head>',
        ),
    }
    reader = one_file.Reader(
        lambda address: _fake_fetch(address, files),
        one_file.Report(),
    )
    page = one_file.inline_page(
        files[SERVER],
        SERVER,
        reader,
    )
    deck = _deck_of(page)

    assert 'window.__player' not in deck
    assert '<head><!-- hyperframe.runtime.iife.js not needed -->' in deck
    assert 'window.__hfSetTime' in deck
    assert 'window.gsap' in deck


def test_inline_page_puts_everything_the_deck_loads_inside_one_file() -> None:
    """
    The player's script is inlined, the deck goes into its `srcdoc` with the runtime first, its
    script, stylesheet and font inside, its connection hint dropped and its scene a `data:`
    address whose image is read from the deck's folder; nothing on the internet is left.
    """
    reader = one_file.Reader(
        _fake_fetch,
        one_file.Report(),
    )
    page = one_file.inline_page(
        FILES[SERVER],
        SERVER,
        reader,
    )
    deck = _deck_of(page)
    scene = _scene_of(deck)

    assert 'src="/player.js"' not in page
    assert '<\\/script>' in page
    assert ' srcdoc="' in page
    assert 'src="/composition/index.html"' not in page
    assert deck.index('window.__player') < deck.index('window.gsap')
    assert 'preconnect' not in deck
    assert 'url("data:' in deck
    assert 'fonts.example.org' not in deck
    assert 'data:image/svg+xml;base64,' in scene
    assert reader.report.missing == []
    assert one_file.still_outside(page) == []


def test_is_local_names_the_loopback_hosts_only() -> None:
    """
    `localhost`, 127.0.0.1 and ::1 are on this computer; any other host is not.
    """
    assert one_file.is_local('http://localhost:3004/')
    assert one_file.is_local('http://127.0.0.1:3004/player.js')
    assert one_file.is_local('http://[::1]:3004/')
    assert not one_file.is_local('https://cdn.example.org/gsap.min.js')
    assert not one_file.is_local('file:///C:/deck.html')


def test_main_refuses_an_address_not_on_this_computer(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Only the deck's own `present` server on this computer is read: any other address exits 1.
    """
    exit_code = one_file.main([
        'https://example.org/',
        'deck.html',
    ])
    error = capsys.readouterr().err

    assert exit_code == 1
    assert 'not an address on this computer' in error


def _deck_of(
    page: str,
) -> str:
    """
    The deck written in a page's player's `srcdoc`.
    """
    match = re.search(r'\ssrcdoc="([^"]*)"', page)

    assert match is not None

    return html.unescape(match.group(1))


def _fake_fetch(
    address: str,
    files: dict[str, str] | None = None,
) -> one_file.Loaded | None:
    """
    A file from the fake server and internet, its media type guessed from its name.
    """
    served = FILES if files is None else files

    if address not in served:
        return None

    return one_file.Loaded(
        served[address].encode('utf-8'),
        one_file._media_type(address, ''),
    )


def _scene_of(
    deck: str,
) -> str:
    """
    The scene file a deck mounts, decoded from its `data:` address.
    """
    match = one_file.SCENE_DATA.search(deck)

    assert match is not None

    scene_bytes = base64.b64decode(match.group(1))

    return scene_bytes.decode('utf-8')
