# /// script
# requires-python = ">=3.11"
# dependencies = ["yt-dlp"]
# ///
"""
A video's transcript as Markdown, for the `watch` skill.

Two ways in:

- ``transcript.py <link>`` asks yt-dlp for the video's details and its captions — never the video
  itself — and writes one Markdown file: the details, the description, and the transcript under
  the video's chapters (or ten-minute parts), a ``[m:ss]`` marker about every thirty seconds. A
  YouTube link in any of its forms is read — ``watch``, ``youtu.be``, ``shorts``, ``embed``,
  ``live`` — and so is a Google search link that carries a video's ``vid:`` id.
- ``transcript.py <link> --paste <file> --title <title>`` builds the same file from text the
  owner copied out of YouTube's *Show transcript* panel, a timestamp line before each caption.

The file is written outside the library — the system's temporary folder by default — and never
inside a folder named ``Sources``: copying it into the library is the skill's step, on the owner's
go. The outline is printed for the skill's plan.

Exit codes: 0 written; 1 yt-dlp could not read the video; 2 a mistake in the command; 3 YouTube
refused (a sign-in or bot check, a 403, a 429, a private or removed video) — the owner fetches the
transcript, nothing is retried; 4 the video has no captions in the language asked for.
"""

import argparse
import dataclasses
import datetime
import json
import pathlib
import re
import sys
import tempfile


__all__ = []

EXIT_NO_CAPTIONS = 4
EXIT_REFUSED = 3
EXIT_UNREADABLE = 1

PARAGRAPH_SECONDS = 30
PART_SECONDS = 600

REFUSAL_MARKERS = (
    "confirm your age",
    "http error 403",
    "http error 429",
    "members-only",
    "not a bot",
    "private video",
    "sign in to confirm",
    "too many requests",
    "video unavailable",
)

TIMESTAMP_LINE = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})$")
VIDEO_IDENTIFIER_PATTERNS = (
    re.compile(r"(?:youtube\.com|youtube-nocookie\.com)/(?:shorts|embed|live|v)/([\w-]{11})"),
    re.compile(r"youtu\.be/([\w-]{11})"),
    re.compile(r"[?&#]v=([\w-]{11})"),
    re.compile(r"vid:([\w-]{11})"),
)


@dataclasses.dataclass
class Caption:
    """
    One caption, or a paragraph of them: its start, in seconds, and its text.
    """

    start: float
    text: str


@dataclasses.dataclass
class Chapter:
    """
    One chapter of the video: its start, its end, and its title.
    """

    start: float
    end: float
    title: str


@dataclasses.dataclass
class Fetched:
    """
    What a fetch brings back: the video's details, its captions, and how they were fetched.
    """

    captions: list[Caption]
    fetched_by: str
    video: "Video"


@dataclasses.dataclass
class Track:
    """
    The caption track to read: human-made or auto-generated, its language key, its json3 address.
    """

    kind: str
    language: str
    url: str


@dataclasses.dataclass
class Video:
    """
    What the transcript file says about the video.
    """

    captions_kind: str
    channel: str
    chapters: list[Chapter]
    description: str
    duration: float
    language: str
    title: str
    uploaded: str
    url: str


def canonical_url(link: str) -> str:
    """
    The video's watch address when the link names a YouTube video, else the link as given.
    """
    identifier = video_identifier(link)

    if identifier is None:
        return link

    return f"https://www.youtube.com/watch?v={identifier}"


def clock(seconds: float) -> str:
    """
    Seconds as ``m:ss``, or ``h:mm:ss`` from an hour on.
    """
    hours, rest = divmod(int(seconds), 3600)
    minutes, remaining_seconds = divmod(rest, 60)

    if hours:
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"

    return f"{minutes}:{remaining_seconds:02d}"


def is_refusal(message: str) -> bool:
    """
    Whether yt-dlp's error says YouTube refused, rather than the command being wrong.
    """
    lowered = message.lower()

    return any(
        marker in lowered
        for marker in REFUSAL_MARKERS
    )


def main() -> None:
    """
    Parse the command, build the transcript, write it outside the library, print the outline.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = _parser()
    arguments = parser.parse_args()
    if _inside_sources(arguments.out):
        parser.error("--out is inside a Sources folder: the skill copies the file in, on the go")

    if arguments.paste:
        fetched = _from_paste(parser, arguments)
    elif arguments.url:
        fetched = _fetch(
            canonical_url(arguments.url),
            arguments.lang,
        )
    else:
        parser.error("give the video's link, with --paste and --title for a pasted transcript")

    markdown = render_markdown(
        fetched.video,
        fetched.captions,
        fetched.fetched_by,
    )
    arguments.out.mkdir(parents=True, exist_ok=True)
    target = arguments.out / f"{_file_stem(fetched.video)}.md"
    target.write_text(
        markdown,
        encoding="utf-8",
        newline="\n",
    )
    _print_summary(fetched, target)


def paragraphs(captions: list[Caption]) -> list[Caption]:
    """
    Captions joined into paragraphs of about thirty seconds, each keeping its start.
    """
    joined = []
    for caption in captions:
        if joined and caption.start - joined[-1].start < PARAGRAPH_SECONDS:
            joined[-1].text = f"{joined[-1].text} {caption.text}"
        else:
            joined.append(Caption(caption.start, caption.text))

    return joined


def parse_json3(raw: bytes) -> list[Caption]:
    """
    YouTube's json3 caption events as captions, empty and newline-only events dropped.
    """
    data = json.loads(raw)
    captions = []
    for event in data.get("events", []):
        segments = event.get("segs")
        if not segments:
            continue

        joined = "".join(
            segment.get("utf8", "")
            for segment in segments
        )
        text = " ".join(joined.split())
        if text:
            start = event.get("tStartMs", 0) / 1000
            captions.append(Caption(start, text))

    return captions


def parse_paste(text: str) -> list[Caption]:
    """
    Text copied from YouTube's *Show transcript* panel: a timestamp line, then its caption.
    """
    captions = []
    starts = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = TIMESTAMP_LINE.match(line)
        if match:
            starts.append(_seconds(match))
        elif line and starts:
            captions.append(Caption(starts[-1], line))

    return captions


def parts(video: Video, captions: list[Caption]) -> list[Chapter]:
    """
    The video's chapters, or ten-minute parts when it has none.
    """
    if video.chapters:
        return video.chapters

    last_caption = captions[-1].start + 1 if captions else 0
    end = max(video.duration, last_caption)
    count = max(1, -(-int(end) // PART_SECONDS))

    return [
        Chapter(
            index * PART_SECONDS,
            min((index + 1) * PART_SECONDS, end),
            f"Part {index + 1}",
        )
        for index in range(count)
    ]


def render_markdown(
    video: Video,
    captions: list[Caption],
    fetched_by: str,
) -> str:
    """
    The transcript file: the details, the description, then each chapter's paragraphs.
    """
    today = datetime.date.today().isoformat()
    length = clock(video.duration) if video.duration else "not given"
    lines = [
        f"# {video.title}",
        "",
        f"- url: {video.url}",
        f"- channel: {video.channel or 'not given'}",
        f"- uploaded: {video.uploaded or 'not given'}",
        f"- length: {length}",
        f"- captions: {video.captions_kind}, {video.language}",
        f"- fetched: {today}, {fetched_by}",
        "",
    ]
    description = video.description.strip()
    if description:
        lines.extend([
            "## Description",
            "",
            description,
            "",
        ])

    lines.extend(["## Transcript", ""])
    for chapter in parts(video, captions):
        lines.extend([f"### [{clock(chapter.start)}] {chapter.title}", ""])
        for paragraph in paragraphs(_inside(chapter, captions)):
            lines.extend([f"[{clock(paragraph.start)}] {paragraph.text}", ""])

    return "\n".join(lines)


def render_outline(video: Video, captions: list[Caption]) -> list[str]:
    """
    One line per chapter: its number, its times, its word count and its title.
    """
    outline = []
    for number, chapter in enumerate(parts(video, captions), start=1):
        words = sum(
            len(caption.text.split())
            for caption in _inside(chapter, captions)
        )
        span = f"{clock(chapter.start):>8}-{clock(chapter.end):<8}"
        outline.append(f"{number:>3}  {span}  {words:>6} words  {chapter.title}")

    return outline


def slug(text: str) -> str:
    """
    The first eight ASCII words of a text joined by underscores, in its own capitals.
    """
    words = re.findall(r"[A-Za-z0-9]+", text)

    return "_".join(words[:8])


def video_identifier(link: str) -> str | None:
    """
    The eleven-character YouTube id a link names, in any of YouTube's or Google's forms, or None.
    """
    for pattern in VIDEO_IDENTIFIER_PATTERNS:
        match = pattern.search(link)

        if match:
            return match.group(1)

    return None


def _download_error_code(message: str) -> int:
    """
    The exit code for a yt-dlp error: a refusal, or the video could not be read.
    """
    return EXIT_REFUSED if is_refusal(message) else EXIT_UNREADABLE


def _download_error_message(message: str) -> str:
    """
    What to tell the skill about a yt-dlp error.
    """
    if not is_refusal(message):
        return f"yt-dlp could not read the video: {message.strip()}"

    advice = " ".join([
        "Nothing is retried. Ask the owner to copy the transcript from YouTube's",
        "'Show transcript' panel into a text file, then run --paste.",
    ])

    return f"YouTube refused: {message.strip()}\n{advice}"


def _exit(message: str, code: int) -> None:
    """
    Print the message to standard error and leave with the code.
    """
    print(message, file=sys.stderr)

    raise SystemExit(code)


def _fetch(url: str, language: str) -> Fetched:
    """
    The video's details and captions from yt-dlp, the video itself never downloaded.
    """
    import yt_dlp

    options = {
        "no_warnings": True,
        "noplaylist": True,
        "quiet": True,
        "skip_download": True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=False)
            track = _pick_track(info, language)
            if track is None:
                _exit(_no_captions_message(info, language), EXIT_NO_CAPTIONS)

            raw = downloader.urlopen(track.url).read()
    except yt_dlp.utils.DownloadError as error:
        message = str(error)
        _exit(
            _download_error_message(message),
            _download_error_code(message),
        )

    version = yt_dlp.version.__version__
    video = _video_from_info(
        info,
        url,
        track,
    )

    return Fetched(
        captions=parse_json3(raw),
        fetched_by=f"by watch's transcript.py with yt-dlp {version}",
        video=video,
    )


def _file_stem(video: Video) -> str:
    """
    The transcript file's name in the temporary folder: the video's id, or its title's words.
    """
    identifier = video_identifier(video.url)

    return identifier if identifier else slug(video.title)


def _from_paste(parser: argparse.ArgumentParser, arguments: argparse.Namespace) -> Fetched:
    """
    The video's details from the command and its captions from the owner's pasted transcript.
    """
    if not (arguments.url and arguments.title):
        parser.error("--paste needs the video's link and --title")

    if not arguments.paste.is_file():
        parser.error(f"{arguments.paste} is not a file")

    captions = parse_paste(arguments.paste.read_text(encoding="utf-8"))
    if not captions:
        parser.error(f"{arguments.paste} holds no timestamp line followed by text")

    video = Video(
        captions_kind="copied by the owner from YouTube's transcript panel",
        channel=arguments.channel,
        chapters=[],
        description="",
        duration=captions[-1].start + 1,
        language=arguments.lang,
        title=arguments.title,
        uploaded=arguments.uploaded,
        url=canonical_url(arguments.url),
    )

    return Fetched(
        captions=captions,
        fetched_by=f"from {arguments.paste.name}, pasted by the owner",
        video=video,
    )


def _inside(chapter: Chapter, captions: list[Caption]) -> list[Caption]:
    """
    The captions that start inside a chapter.
    """
    return [
        caption
        for caption in captions
        if chapter.start <= caption.start < chapter.end
    ]


def _inside_sources(folder: pathlib.Path) -> bool:
    """
    Whether a folder is, or sits inside, a folder named Sources.
    """
    resolved = folder.resolve()

    return any(
        part.lower() == "sources"
        for part in resolved.parts
    )


def _json3_url(formats: list[dict]) -> str | None:
    """
    The address of a track's json3 format, if it offers one.
    """
    for item in formats:
        if item.get("ext") == "json3":
            return item.get("url")

    return None


def _no_captions_message(info: dict, language: str) -> str:
    """
    What to tell the skill when the video has no captions in the language asked for.
    """
    human_made = sorted(info.get("subtitles") or {})
    original = info.get("language") or "not given"

    return " ".join([
        f"no captions in '{language}': human-made {human_made};",
        f"the video's language is {original}.",
        "Ask the owner for the transcript, or pass --lang.",
    ])


def _parser() -> argparse.ArgumentParser:
    """
    The command's arguments.
    """
    summary = __doc__.strip().split("\n")[0]
    parser = argparse.ArgumentParser(description=summary)
    parser.add_argument(
        "url",
        nargs="?",
        help="the video's link",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="caption language (default: en)",
    )
    parser.add_argument(
        "--paste",
        type=pathlib.Path,
        help="a text file copied from 'Show transcript'",
    )
    parser.add_argument("--title", help="with --paste: the video's title, as YouTube shows it")
    parser.add_argument(
        "--channel",
        default="",
        help="with --paste: the channel",
    )
    parser.add_argument(
        "--uploaded",
        default="",
        help="with --paste: the upload date, YYYY-MM-DD",
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=pathlib.Path(tempfile.gettempdir()) / "watch",
        help="the folder to write in, outside the library (default: the temporary folder)",
    )

    return parser


def _pick_track(info: dict, language: str) -> Track | None:
    """
    The caption track to read, human-made first.

    An auto-generated track is taken only in the video's own language, never a machine
    translation of it.
    """
    manual = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}
    original = info.get("language") or language

    for key, formats in manual.items():
        manual_url = _json3_url(formats)
        in_language = key == language or key.startswith(f"{language}-")

        if manual_url and in_language:
            return Track(
                "human-made",
                key,
                manual_url,
            )

    for key in (f"{language}-orig", language):
        own_language = key.endswith("-orig") or original.startswith(language)
        automatic_url = _json3_url(automatic.get(key, []))

        if automatic_url and own_language:
            return Track(
                "auto-generated",
                key,
                automatic_url,
            )

    return None


def _print_summary(fetched: Fetched, target: pathlib.Path) -> None:
    """
    The details, a name hint, where the file was written, and the outline, for the skill's plan.
    """
    video = fetched.video
    year = video.uploaded[:4] if video.uploaded else "ND"
    chapters = "the video's own" if video.chapters else "none; ten-minute parts"
    hint = f"{slug(video.channel or 'Channel')}_{year}_{slug(video.title)}"
    summary = [
        f"title:     {video.title}",
        f"channel:   {video.channel or 'not given'}",
        f"uploaded:  {video.uploaded or 'not given'}",
        f"length:    {clock(video.duration)}",
        f"captions:  {video.captions_kind}, {video.language}",
        f"chapters:  {chapters}",
        f"name hint: {hint}",
        f"written:   {target}",
        "",
    ]
    outline = render_outline(video, fetched.captions)
    print("\n".join(summary + outline))


def _seconds(match: re.Match) -> int:
    """
    A timestamp line's match as seconds.
    """
    hours, minutes, seconds = (
        int(part) if part else 0
        for part in match.groups()
    )

    return hours * 3600 + minutes * 60 + seconds


def _uploaded(info: dict) -> str:
    """
    The upload date as YYYY-MM-DD, or empty when yt-dlp gives none.
    """
    raw = info.get("upload_date") or ""

    if len(raw) != 8:
        return raw

    return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"


def _video_from_info(
    info: dict,
    url: str,
    track: Track,
) -> Video:
    """
    The video's details from yt-dlp's info.
    """
    duration = float(info.get("duration") or 0)
    chapters = [
        Chapter(
            float(item["start_time"]),
            float(item.get("end_time") or duration),
            item["title"],
        )
        for item in info.get("chapters") or []
    ]

    return Video(
        captions_kind=track.kind,
        channel=info.get("channel") or info.get("uploader") or "",
        chapters=chapters,
        description=info.get("description") or "",
        duration=duration,
        language=track.language,
        title=info.get("title") or "untitled",
        uploaded=_uploaded(info),
        url=info.get("webpage_url") or url,
    )


if __name__ == "__main__":
    main()
