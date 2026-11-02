"""
A deck as a PDF, pdf_pages.py: the deck's main-line slides read from its own markup, each with the
moment its last step shows, branches left out, and only the deck's own server on this computer.
"""
import pathlib

import pdf_pages

__all__ = []

DECK = ''.join([
    '<html><body>',
    '<script type="application/hyperframes-slideshow+json">',
    '{"slides": [{"sceneId": "cover"}, {"sceneId": "plan, (draft)"}],',
    ' "slideSequences": [{"id": "more", "slides": [{"sceneId": "aside"}]}]}',
    '</script>',
    '<div id="cover" class="scene" data-composition-id="cover" data-start="0" data-duration="6"',
    ' data-width="1920" data-height="1080"></div>',
    '<div class="scene" data-start="6" data-composition-id="plan, (draft)" data-duration="9"></div>',
    '<div class="scene" data-composition-id="aside" data-start="15" data-duration="6"></div>',
    '</body></html>',
])


def test_a_deck_with_no_slide_list_has_no_slides() -> None:
    """
    A page with no slideshow island lists no slides.
    """
    assert pdf_pages.slides_of('<html><body></body></html>') == []


def test_an_address_off_this_computer_exits_one(
    tmp_path: pathlib.Path,
) -> None:
    """
    Only the deck's own `present` server on this computer is read: any other address exits 1.
    """
    exit_code = pdf_pages.main([
        'https://example.org/',
        str(tmp_path / 'deck.pdf'),
    ])

    assert exit_code == 1


def test_another_deck_is_told_apart_from_the_folders_own(
    tmp_path: pathlib.Path,
) -> None:
    """
    A PDF written to `<deck>/export/` belongs to the deck in `<deck>/index.html`: a server that
    serves another deck, as when `present` moved to another port, is told apart by its scenes; a
    folder with no deck in or above it is not compared.
    """
    deck_folder = tmp_path / 'Mi deck, (prueba)'
    export_folder = deck_folder / 'export'
    export_folder.mkdir(parents=True)
    (deck_folder / 'index.html').write_text(
        DECK,
        encoding='utf-8',
    )
    other = DECK.replace(
        'data-composition-id="cover"',
        'data-composition-id="portada"',
    )

    assert not pdf_pages.another_deck(
        DECK,
        export_folder,
    )
    assert pdf_pages.another_deck(
        other,
        export_folder,
    )
    assert not pdf_pages.another_deck(
        other,
        tmp_path,
    )


def test_slides_end_at_their_last_step_and_branches_are_left_out() -> None:
    """
    Each main-line slide is printed a moment before its scene ends, whatever the order of its
    attributes or the commas and parentheses in its id; a branch's slide is not printed.
    """
    slides = pdf_pages.slides_of(DECK)

    assert slides == [
        pdf_pages.Slide(
            scene_id='cover',
            last_moment=5.9,
        ),
        pdf_pages.Slide(
            scene_id='plan, (draft)',
            last_moment=14.9,
        ),
    ]
