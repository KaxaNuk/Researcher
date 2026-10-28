"""
Keep the researcher installed for every assistant it is used on: put the assistant in use on the
list APM keeps in `~/.apm/apm.yml`, and check that the researcher's files are on disk for it.

APM writes that list, `targets:`, only when an install creates the file, with the one assistant
that install named.  An install for a second assistant leaves the list as it is, and the next
install or update without `--target` deletes every file of the second as belonging to no listed
assistant, and still exits 0.  An assistant on the list keeps its files through every install and
update; a file with no list at all lets APM find every assistant whose folder exists, and delete
nothing.

Usage:
    uv run --no-project python user_targets.py add <assistant>
    uv run --no-project python user_targets.py check <assistant> <slug>

The assistant is claude, codex, copilot, cursor, gemini, opencode or windsurf; the slug is the
researcher's name as its files take it, `sofia` for Sofía.  In a conversation where the
init-researcher skill is not loaded yet, run it from the installed package, `<package>` standing
for `$HOME/.apm/apm_modules/KaxaNuk/Researcher` — `$HOME`, never `~`, which a program
handed it does not expand:
    uv run --no-project python "<package>/.apm/skills/init-researcher/scripts/user_targets.py" add codex

`add` reads `apm.yml` in the `.apm` folder of the user's home folder.  When it names its
assistants, under `targets:` or the older `target:` — a list of lines starting `- `, a list in
brackets, or one name — and the assistant is not among them, it is added to that list: a line of
its own after the last, or the bracketed list rewritten on its line, and every other line stays as
it was, its line endings included.  An assistant already listed, or a file that names none, changes
nothing.  A missing file, which the package's install creates, a list that cannot be read here —
brackets over several lines, or no names — or a list named twice changes nothing either, and
exits 1.

`check` looks in the user's home folder for the package's `next` skill and the researcher's skill
and agent, where APM puts them for the assistant:

    assistant           the skills, next and <slug>   the researcher's agent
    claude              .claude/skills/               .claude/agents/<slug>.md
    codex               .agents/skills/               .codex/agents/<slug>.toml
    copilot             .agents/skills/               .copilot/agents/<slug>.agent.md
    cursor              .agents/skills/               .cursor/agents/<slug>.md
    gemini, windsurf    .agents/skills/               none: neither takes an agent
    opencode            .config/opencode/skills/      none: next alone

OpenCode receives the package but never the researcher, which the home leaves out by design.  Each
missing file is named on a line of its own.  The check also fails when `apm.yml` lists assistants
and not this one, since the next install or update would delete the files it found.

Exit code 0 when the assistant is listed, or needs no list, or the researcher is installed for it;
1 when not; 2 for a command line that cannot be read.  The console is written in UTF-8, so a path
in any alphabet prints; the script's own words are ASCII.
"""
import argparse
import dataclasses
import pathlib
import re
import sys

# The user's APM manifest, from the home folder, and the keys that name its assistants: `targets:`,
# which APM writes, and `target:`, which it still reads.  Only a key at the start of a line counts:
# one indented further belongs to a dependency.
LIST_ITEM_PATTERN = re.compile(r'(?P<indent> *)-(?:\s+(?P<item>.*))?')
LIST_KEY_PATTERN = re.compile(r'(?P<key>targets|target):(?P<value>(?:\s.*)?)')
MANIFEST_FILE = pathlib.Path('.apm') / 'apm.yml'
# A file's lines, each with its own line ending, so a file written with CRLF keeps them.
LINE_PATTERN = re.compile(r'[^\n]*\n|[^\n]+')
# Where APM puts each assistant's files, from the user's home folder: the researcher's agent, from
# its slug, for the four assistants that take one; and the folder of skills, Claude Code's and
# OpenCode's their own, the others' shared.  OpenCode is left out of the home, since it rejects the
# agent APM writes for it, and the package's `next` skill stands for the package.
AGENT_FILES = {
    'claude': '.claude/agents/{slug}.md',
    'codex': '.codex/agents/{slug}.toml',
    'copilot': '.copilot/agents/{slug}.agent.md',
    'cursor': '.cursor/agents/{slug}.md',
}
OPENCODE = 'opencode'
PACKAGE_SKILL = 'next'
SKILL_FOLDERS = {
    'claude': '.claude/skills',
    'codex': '.agents/skills',
    'copilot': '.agents/skills',
    'cursor': '.agents/skills',
    'gemini': '.agents/skills',
    'opencode': '.config/opencode/skills',
    'windsurf': '.agents/skills',
}
# The two forms a list of assistants takes: lines starting `- ` below the key, or on the key's line.
BLOCK_FORM = 'block'
INLINE_FORM = 'inline'
# A researcher's slug: lowercase letters a to z and digits, single hyphens between them.
SLUG_PATTERN = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')


@dataclasses.dataclass(frozen=True)
class ExpectedFile:
    """
    A file the check looks for, and in words what it is.
    """
    path: pathlib.Path
    role: str


@dataclasses.dataclass(frozen=True)
class Listing:
    """
    Where a manifest names its assistants: the list's form, the lines of a block list, the key and
    its line, and each name without its quotes and as written.
    """
    form: str
    item_indexes: tuple[int, ...]
    key: str
    key_index: int
    names: tuple[str, ...]
    written_names: tuple[str, ...]


def add_target(
    manifest: pathlib.Path,
    target: str,
) -> int:
    """
    Put the assistant on the manifest's list of assistants, and say what was done.
    """
    if not manifest.is_file():
        print(f"{manifest} does not exist yet: the package's install creates it. Install the package, then run this.")

        return 1

    try:
        lines = read_lines(manifest)
    except (OSError, UnicodeDecodeError) as exception:
        print(f'Nothing changed: {manifest} could not be read: {exception}')

        return 1

    key_indexes = list_key_indexes(lines)

    if not key_indexes:
        no_list = ' '.join([
            f'Nothing changed: {manifest} names no assistants, so APM installs for every assistant whose',
            'folder exists and deletes nothing.',
        ])
        print(no_list)

        return 0

    if len(key_indexes) > 1:
        twice = ' '.join([
            f'Nothing changed: {manifest} names its assistants more than once, under targets: or target:,',
            'which APM refuses. Keep one list, then run this again.',
        ])
        print(twice)

        return 1

    listing = read_listing(
        lines,
        key_indexes[0],
    )

    if listing is None:
        unreadable = ' '.join([
            f'Nothing changed: the list of assistants in {manifest} could not be read here - brackets',
            f'over several lines, or no names. Add {target} to it by hand.',
        ])
        print(unreadable)

        return 1

    if target in listing.names:
        print(f'{target} is already listed in {manifest}; nothing changed.')

        return 0

    changed_lines = with_target(
        lines,
        listing,
        target,
    )
    changed_text = ''.join(changed_lines)

    try:
        manifest.write_bytes(changed_text.encode('utf-8'))
    except OSError as exception:
        reason = exception.strerror or str(exception)
        print(f'Nothing changed: {manifest} could not be written: {reason}')

        return 1

    names = ', '.join([
        *listing.names,
        target,
    ])
    print(f'Added {target} to {manifest}: {names}. Installs and updates now keep each of them.')

    return 0


def check_target(
    home: pathlib.Path,
    target: str,
    slug: str,
) -> int:
    """
    Say whether the package and the researcher are on disk for the assistant, and stay listed for it.
    """
    expected = expected_files(
        home,
        target,
        slug,
    )
    missing = [
        expected_file
        for expected_file
        in expected
        if not expected_file.path.is_file()
    ]
    unlisted = unlisted_problem(
        home / MANIFEST_FILE,
        target,
    )

    if target == OPENCODE:
        print('The researcher is not deployed to OpenCode, by design; only the package is looked for.')

    for missing_file in missing:
        print(f'Missing: {missing_file.path} - {missing_file.role}')

    if unlisted is not None:
        print(unlisted)

    if missing or unlisted is not None:
        print(f'Not installed for {target}.')

        return 1

    installed = 'The package is' if target == OPENCODE else f'The researcher, {slug}, is'
    print(f'{installed} installed for {target}.')

    return 0


def expected_files(
    home: pathlib.Path,
    target: str,
    slug: str,
) -> list[ExpectedFile]:
    """
    The files that show the package, and the researcher, installed for the assistant: the package's
    `next` skill, then the researcher's skill and its agent where the assistant takes one.
    """
    skill_folder = home / SKILL_FOLDERS[target]
    package_skill = ExpectedFile(
        path=skill_folder / PACKAGE_SKILL / 'SKILL.md',
        role=f"the package's {PACKAGE_SKILL} skill",
    )

    if target == OPENCODE:

        return [package_skill]

    researcher_skill = ExpectedFile(
        path=skill_folder / slug / 'SKILL.md',
        role="the researcher's skill",
    )
    files = [
        package_skill,
        researcher_skill,
    ]
    agent_file = AGENT_FILES.get(target)

    if agent_file is not None:
        researcher_agent = ExpectedFile(
            path=home / agent_file.format(slug=slug),
            role="the researcher's agent",
        )
        files.append(researcher_agent)

    return files


def list_key_indexes(
    lines: list[str],
) -> list[int]:
    """
    The index of each line that starts a list of assistants, `targets:` or `target:` at the start
    of the line.
    """
    indexes = [
        index
        for index, line
        in enumerate(lines)
        if LIST_KEY_PATTERN.fullmatch(_content(line)) is not None
    ]

    return indexes


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Read the command line, then add the assistant to the user's list, or check its files.
    """
    for console_stream in (sys.stdout, sys.stderr):
        try:
            console_stream.reconfigure(
                encoding='utf-8',
                errors='replace',
            )
        except Exception:
            pass

    parser = _build_parser()
    parsed = parser.parse_args(arguments)
    home = pathlib.Path.home()

    if parsed.command == 'add':
        added = add_target(
            home / MANIFEST_FILE,
            parsed.target,
        )

        return added

    checked = check_target(
        home,
        parsed.target,
        parsed.slug,
    )

    return checked


def read_lines(
    path: pathlib.Path,
) -> list[str]:
    """
    A UTF-8 file's lines, each with its own line ending, the last without one when the file ends
    without one.
    """
    text = path.read_bytes().decode('utf-8')
    lines = LINE_PATTERN.findall(text)

    return lines


def read_listing(
    lines: list[str],
    key_index: int,
) -> Listing | None:
    """
    The assistants the key's line names, or None when they cannot be read here: brackets that run
    past their line, or a list with no names.

    With nothing after the key but a comment, the list is the lines below it that start with `- `,
    blank lines and comments between them; otherwise it is on the key's line, in brackets, or one
    name — several between commas, as `target:` takes them.
    """
    key_match = LIST_KEY_PATTERN.fullmatch(_content(lines[key_index]))
    value = _without_comment(key_match.group('value'))

    if not value:
        block = _block_listing(
            lines,
            key_index,
            key_match.group('key'),
        )

        return block

    bracketed = value.startswith('[')

    if bracketed and not value.endswith(']'):

        return None

    inside = value[1:-1] if bracketed else value
    written_names = tuple(
        part.strip()
        for part
        in inside.split(',')
        if part.strip()
    )

    if not written_names:

        return None

    names = tuple(
        _unquoted(written_name)
        for written_name
        in written_names
    )
    inline = Listing(
        form=INLINE_FORM,
        item_indexes=(),
        key=key_match.group('key'),
        key_index=key_index,
        names=names,
        written_names=written_names,
    )

    return inline


def unlisted_problem(
    manifest: pathlib.Path,
    target: str,
) -> str | None:
    """
    Why the next install or update would delete the assistant's files — a list of assistants that
    leaves it out — or None: listed, no list, or no manifest to read.
    """
    try:
        lines = read_lines(manifest)
    except (OSError, UnicodeDecodeError):

        return None

    key_indexes = list_key_indexes(lines)

    if len(key_indexes) != 1:

        return None

    listing = read_listing(
        lines,
        key_indexes[0],
    )

    if listing is None or target in listing.names:

        return None

    names = ', '.join(listing.names)
    problem = ' '.join([
        f'{manifest} lists {names} and not {target}, so the next install or update deletes its files:',
        f'run `user_targets.py add {target}` first.',
    ])

    return problem


def with_target(
    lines: list[str],
    listing: Listing,
    target: str,
) -> list[str]:
    """
    The manifest's lines with the assistant added to its list, every other line as it was.

    A block list gains a line after its last name, indented as that name and ending as it ended; a
    last name that ended the file without a line ending takes the key line's.  A list in brackets,
    or one name, becomes a list in brackets with the assistant last, on the key's line, its comment
    kept.
    """
    if listing.form == BLOCK_FORM:
        last_index = listing.item_indexes[-1]
        last_line = lines[last_index]
        last_ending = _ending(last_line)
        last_item = LIST_ITEM_PATTERN.fullmatch(_content(last_line))
        closed_last = last_line if last_ending else f'{last_line}{_ending(lines[listing.key_index])}'
        added_line = f"{last_item.group('indent')}- {target}{last_ending}"
        block_lines = [
            *lines[:last_index],
            closed_last,
            added_line,
            *lines[last_index + 1:],
        ]

        return block_lines

    key_line = lines[listing.key_index]
    key_content = _content(key_line)
    code, comment_sign, _ = key_content.partition('#')
    comment = key_content[len(code.rstrip()):] if comment_sign else ''
    names = ', '.join([
        *listing.written_names,
        target,
    ])
    rewritten = f'{listing.key}: [{names}]{comment}{_ending(key_line)}'
    inline_lines = [
        *lines[:listing.key_index],
        rewritten,
        *lines[listing.key_index + 1:],
    ]

    return inline_lines


def _block_listing(
    lines: list[str],
    key_index: int,
    key: str,
) -> Listing | None:
    """
    The block list below the key's line: each line that starts with `- ` until the first line
    that is neither one, nor blank, nor a comment; None when it holds no name.
    """
    item_indexes = []
    written_names = []

    for index in range(key_index + 1, len(lines)):
        content = _content(lines[index])
        stripped = content.strip()

        if not stripped or stripped.startswith('#'):
            continue

        item_match = LIST_ITEM_PATTERN.fullmatch(content)

        if item_match is None:
            break

        item_text = item_match.group('item') or ''
        item_indexes.append(index)
        written_names.append(_without_comment(item_text))

    names = tuple(
        _unquoted(written_name)
        for written_name
        in written_names
        if written_name
    )

    if not names:

        return None

    block = Listing(
        form=BLOCK_FORM,
        item_indexes=tuple(item_indexes),
        key=key,
        key_index=key_index,
        names=names,
        written_names=tuple(written_names),
    )

    return block


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: `add` with an assistant, or `check` with an assistant and a slug.
    """
    targets = sorted(SKILL_FOLDERS)
    parser = argparse.ArgumentParser(
        description="Keep an assistant on APM's list in ~/.apm/apm.yml, or check the researcher's files for it.",
    )
    commands = parser.add_subparsers(
        dest='command',
        required=True,
    )
    add_command = commands.add_parser(
        'add',
        help='put the assistant on the list in ~/.apm/apm.yml, when the file has one',
    )
    add_command.add_argument(
        'target',
        choices=targets,
        help='the assistant in use',
    )
    check_command = commands.add_parser(
        'check',
        help="check the package's and the researcher's files for the assistant",
    )
    check_command.add_argument(
        'target',
        choices=targets,
        help='the assistant in use',
    )
    check_command.add_argument(
        'slug',
        type=_slug,
        help="the researcher's name as its files take it, such as sofia",
    )

    return parser


def _content(
    line: str,
) -> str:
    """
    A line without its line ending.
    """
    content = line.rstrip('\r\n')

    return content


def _ending(
    line: str,
) -> str:
    """
    A line's line ending, LF or CRLF, or an empty string for a last line without one.
    """
    ending = line[len(_content(line)):]

    return ending


def _slug(
    text: str,
) -> str:
    """
    A researcher's slug from the command line, refused unless it is one.
    """
    if SLUG_PATTERN.fullmatch(text) is None:
        not_a_slug = f'"{text}" is not a slug: lowercase letters a to z and digits, single hyphens between them'

        raise argparse.ArgumentTypeError(not_a_slug)

    return text


def _unquoted(
    text: str,
) -> str:
    """
    A name as APM reads it: without the spaces around it and the quotes it may be written in.
    """
    stripped = text.strip()
    unquoted = stripped.strip('\'"')

    return unquoted


def _without_comment(
    text: str,
) -> str:
    """
    A value without the comment after it, and without spaces around it: an assistant's name never
    holds a `#`.
    """
    code = text.partition('#')[0]
    value = code.strip()

    return value


if __name__ == '__main__':
    sys.exit(main())
