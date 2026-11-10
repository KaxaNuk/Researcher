"""
A video's transcript, transcript.py in watch: a link in any of its forms names the video, YouTube's
caption events and a pasted transcript both become captions, a refusal is told from a mistake, and
the Markdown keeps its chapters and its markers.
"""
import json
import pathlib
import subprocess
import sys

import pytest

import transcript

__all__ = []

SCRIPT = pathlib.Path(transcript.__file__)
VIDEO = 'UF8uR6Z6KLc'


def test_a_link_with_no_video_is_kept_as_given() -> None:
    """
    A link that names no YouTube video goes to yt-dlp as it is.
    """
    link = 'https://vimeo.com/76979871'

    assert transcript.canonical_url(link) == link


def test_a_paste_is_written_outside_the_library_and_never_inside_sources(
    tmp_path: pathlib.Path,
) -> None:
    """
    `--paste` writes the transcript where `--out` says, and refuses a folder named Sources.
    """
    pasted = tmp_path / 'pasted.txt'
    pasted.write_text('0:00\nHello.\n0:31\nAgain.\n', encoding='utf-8')
    arguments = [
        sys.executable,
        '-I',
        str(SCRIPT),
        '--paste',
        str(pasted),
        f'https://youtu.be/{VIDEO}',
        '--title',
        'A talk',
    ]

    written = subprocess.run(
        [
            *arguments,
            '--out',
            str(tmp_path / 'out'),
        ],
        capture_output=True,
        check=False,
        encoding='utf-8',
    )
    refused = subprocess.run(
        [
            *arguments,
            '--out',
            str(tmp_path / 'Sources' / 'Videos'),
        ],
        capture_output=True,
        check=False,
        encoding='utf-8',
    )

    assert written.returncode == 0, written.stderr
    assert (tmp_path / 'out' / f'{VIDEO}.md').read_bytes().count(b'\r') == 0
    assert refused.returncode == 2
    assert not (tmp_path / 'Sources').exists()


def test_a_pasted_transcript_becomes_captions() -> None:
    """
    YouTube's *Show transcript* text, a timestamp line before its caption, hours included.
    """
    pasted = '\n'.join([
        '0:00',
        'Truth be told,',
        'I never graduated.',
        '',
        '1:02:03',
        'Stay hungry.',
        'Stay foolish.',
    ])

    captions = transcript.parse_paste(pasted)

    assert captions == [
        transcript.Caption(0, 'Truth be told,'),
        transcript.Caption(0, 'I never graduated.'),
        transcript.Caption(3723, 'Stay hungry.'),
        transcript.Caption(3723, 'Stay foolish.'),
    ]


@pytest.mark.parametrize(
    (
        'message',
        'refused',
    ),
    [
        ('ERROR: [youtube] x: Sign in to confirm you are not a bot', True),
        ('ERROR: unable to download webpage: HTTP Error 429: Too Many Requests', True),
        ('ERROR: [youtube] x: Private video', True),
        ('ERROR: Unsupported URL: https://example.invalid/', False),
    ],
)
def test_a_refusal_is_told_from_a_mistake(
    message: str,
    refused: bool,
) -> None:
    """
    A sign-in or bot check, a 429 or a private video is YouTube's refusal; anything else is not.
    """
    assert transcript.is_refusal(message) is refused


@pytest.mark.parametrize(
    'link',
    [
        f'https://www.youtube.com/watch?v={VIDEO}',
        f'https://www.youtube.com/watch?feature=share&v={VIDEO}&t=42',
        f'https://youtu.be/{VIDEO}?si=abc',
        f'https://www.youtube.com/shorts/{VIDEO}',
        f'https://www.youtube.com/embed/{VIDEO}',
        f'https://www.youtube.com/live/{VIDEO}',
        f'https://www.google.com/search?q=steve+jobs&udm=vids#fpstate=ive&vld=cid:c5191734,vid:{VIDEO},st:0',
    ],
)
def test_every_form_of_a_link_names_the_video(
    link: str,
) -> None:
    """
    YouTube's forms, and a Google search link carrying `vid:`, give the same watch address.
    """
    canonical = transcript.canonical_url(link)

    assert canonical == f'https://www.youtube.com/watch?v={VIDEO}'


def test_json3_events_become_captions() -> None:
    """
    Caption events become captions with their start in seconds; newline-only events are dropped.
    """
    events = {
        'events': [
            {'tStartMs': 0, 'dDurationMs': 900},
            {
                'tStartMs': 1500,
                'segs': [
                    {'utf8': 'Stay'},
                    {'utf8': ' hungry.'},
                ],
            },
            {'tStartMs': 2000, 'segs': [{'utf8': '\n'}]},
            {'tStartMs': 61000, 'segs': [{'utf8': 'Stay  foolish.'}]},
        ],
    }
    raw = json.dumps(events).encode('utf-8')

    captions = transcript.parse_json3(raw)

    assert captions == [
        transcript.Caption(1.5, 'Stay hungry.'),
        transcript.Caption(61.0, 'Stay foolish.'),
    ]


def test_only_the_videos_own_language_is_taken_from_auto_captions() -> None:
    """
    Human-made captions come first; an auto-generated track is taken in the video's own language,
    never as a machine translation.
    """
    auto_only = {
        'automatic_captions': {
            'en': [{'ext': 'json3', 'url': 'https://example.invalid/en'}],
            'es': [{'ext': 'json3', 'url': 'https://example.invalid/es'}],
        },
        'language': 'en',
    }
    with_manual = {
        **auto_only,
        'subtitles': {'en-GB': [{'ext': 'json3', 'url': 'https://example.invalid/manual'}]},
    }

    assert transcript._pick_track(auto_only, 'es') is None
    assert transcript._pick_track(auto_only, 'en').kind == 'auto-generated'
    assert transcript._pick_track(with_manual, 'en').url == 'https://example.invalid/manual'


def test_the_markdown_keeps_chapters_and_markers() -> None:
    """
    Without chapters of its own a video is cut in ten-minute parts, and every paragraph keeps its
    marker.
    """
    video = transcript.Video(
        captions_kind='human-made',
        channel='Stanford',
        chapters=[],
        description='',
        duration=650,
        language='en',
        title='A talk',
        uploaded='2008-03-08',
        url=f'https://www.youtube.com/watch?v={VIDEO}',
    )
    captions = [
        transcript.Caption(5, 'First.'),
        transcript.Caption(20, 'Still first.'),
        transcript.Caption(40, 'Second.'),
        transcript.Caption(605, 'Part two.'),
    ]

    markdown = transcript.render_markdown(
        video,
        captions,
        'by a test',
    )

    assert '### [0:00] Part 1' in markdown
    assert '[0:05] First. Still first.' in markdown
    assert '[0:40] Second.' in markdown
    assert '### [10:00] Part 2' in markdown
    assert '[10:05] Part two.' in markdown
