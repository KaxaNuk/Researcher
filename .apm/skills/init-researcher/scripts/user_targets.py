"""
Keep the researcher installed for every assistant it is used on: put the assistant in use on the
list APM keeps in `~/.apm/apm.yml`, check that the researcher's files are on disk for it, and find
the user's own skills, commands and agents that keep the package's of the same name out.

APM writes that list, `targets:`, only when an install creates the file, with the one assistant
that install named.  An install for a second assistant leaves the list as it is, and the next
install or update without `--target` deletes every file of the second as belonging to no listed
assistant, and still exits 0.  An assistant on the list keeps its files through every install and
update; a file with no list at all lets APM find every assistant whose folder exists, and delete
nothing.

Usage:
    uv run --no-project python user_targets.py add <assistant>
    uv run --no-project python user_targets.py check <assistant> <slug>
    uv run --no-project python user_targets.py clashes <assistant>
    uv run --no-project python user_targets.py keep-mine <assistant>

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

`clashes` reads, and changes nothing.  APM never overwrites a file it did not install: where the
user already has a skill, command or agent of their own under one of the package's names, the
install keeps theirs, leaves the package's out, warns in one line and still exits 0, and the
researcher runs without that part.  For each of the package's skills, commands and agents, read
from the installed package under `~/.apm/apm_modules`, it looks where APM puts it for the assistant
- the skills as `check` lists them, Claude Code's commands in `.claude/commands/`, the agent where
`check` looks for the researcher's - and names each one there that APM's lock file,
`~/.apm/apm.lock.yaml`, does not record as installed: the user's own.  Codex takes no commands;
for Copilot, Cursor, Gemini, OpenCode and Windsurf only the skills and the agent are looked for.

`keep-mine` renames each of those to `<name>-mine` - `-mine-2` and on when that is taken, never
over a file - a skill's folder, a command's or an agent's file, and the first `name:` line, or
`name =` in a TOML agent, that names it; nothing else in them changes, and nothing is deleted.  The
user's own then works under its new name, and the next install puts the package's where it was.

Exit code 0 when the assistant is listed, or needs no list, or the researcher is installed for it,
or none of the user's own files takes a name of the package's, or each was renamed; 1 when not; 2
for a command line that cannot be read.  The console is written in UTF-8, so a path
in any alphabet prints; the script's own words are ASCII.
"""
import argparse
import dataclasses
import itertools
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
# The kinds of file the package installs, as the package keeps them: a skill a folder holding
# SKILL.md, a command and an agent a file with this ending.
AGENT_ENDING = '.agent.md'
COMMAND_ENDING = '.prompt.md'
SKILL_FILE = 'SKILL.md'
# Where APM puts the package's commands, from the user's home folder: Claude Code's alone, checked
# by an install; Codex takes none.
COMMAND_FILES = {
    'claude': '.claude/commands/{name}.md',
}
# Where the package is installed for the user, under `~/.apm/apm_modules/`, newest name first: as
# KaxaNuk/Researcher, under its name before 1.25.0, or from an archive or a folder.
INSTALLED_PACKAGE_PATHS = [
    pathlib.Path('KaxaNuk') / 'Researcher',
    pathlib.Path('KaxaNuk') / 'KaxaNuk-Researcher',
    pathlib.Path('_local') / 'KaxaNuk-Researcher',
]
USER_SCOPE_MODULES = pathlib.Path('.apm') / 'apm_modules'
# APM's record of what it installed for the user, from the home folder; a path it installed is a
# list item or a value starting with a dot, as `.claude/skills/next`.
LOCK_FILE = pathlib.Path('.apm') / 'apm.lock.yaml'
MANAGED_PATH_PATTERN = re.compile(
    r'^\s*(?:-|value:)\s+(?P<path>\.\S+?)\s*$',
    re.MULTILINE,
)
# What `keep-mine` adds to the name of the user's own, and the line that names it: `name:` in a
# Markdown file's frontmatter, `name =` in a TOML agent, the name quoted or not.
MINE_SUFFIX = '-mine'
NAME_LINE_PATTERN = re.compile(
    r'(?P<key>name\s*[:=]\s*)(?P<quote>[\'"]?)(?P<name>[^\'"\s#]+)(?P=quote)(?P<rest>\s*(?:#.*)?)',
)
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
# The package's own folder seen from this file, scripts/ -> init-researcher/ -> skills/ -> .apm/,
# used when no installed package is found: this repository, in its tests.
SCRIPT_PACKAGE = pathlib.Path(__file__).resolve().parents[3]
# The two forms a list of assistants takes: lines starting `- ` below the key, or on the key's line.
BLOCK_FORM = 'block'
INLINE_FORM = 'inline'
# A researcher's slug: lowercase letters a to z and digits, single hyphens between them.
SLUG_PATTERN = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')


@dataclasses.dataclass(frozen=True)
class Clash:
    """
    One of the package's skills, commands or agents, and where APM puts it for the assistant: a
    clash when a file of the user's own is there.
    """
    kind: str
    name: str
    path: pathlib.Path


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


def clashes_report(
    home: pathlib.Path,
    target: str,
    package: pathlib.Path | None,
) -> int:
    """
    Name each of the user's own skills, commands and agents that keeps the package's of the same
    name out, and say how to keep both.
    """
    clashes = find_clashes(
        home,
        target,
        package,
    )

    if clashes is None:

        return 1

    if not clashes:
        print(f"None of your own skills, commands or agents takes a name of the package's for {target}.")

        return 0

    for clash in clashes:
        print(f"Yours, not the package's: {clash.kind} {clash.name} - {clash.path}")

    names = ', '.join(
        clash.name
        for clash
        in clashes
    )
    advice = ' '.join([
        f"The install kept your own {names} and left the package's out, so the researcher runs",
        f'without them. `user_targets.py keep-mine {target}` renames yours to <name>{MINE_SUFFIX};',
        'then install the package again, and both work.',
    ])
    print(advice)

    return 1


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


def find_clashes(
    home: pathlib.Path,
    target: str,
    package: pathlib.Path | None,
) -> list[Clash] | None:
    """
    The package's skills, commands and agents whose place holds a file of the user's own, one APM's
    lock file does not record as installed; None, said why, when the package or the lock file
    cannot be read.
    """
    if package is None:
        print(f'The package is not installed under {home / USER_SCOPE_MODULES}: install it, then run this.')

        return None

    managed = managed_paths(home / LOCK_FILE)

    if managed is None:
        print(f'{home / LOCK_FILE} could not be read: install the package, then run this.')

        return None

    places = package_places(
        home,
        target,
        package,
    )
    clashes = [
        place
        for place
        in places
        if place.path.exists()
        and place.path.relative_to(home).as_posix() not in managed
    ]

    return clashes


def free_name(
    clash: Clash,
) -> str:
    """
    The name the user's own takes: `<name>-mine`, or `-mine-2` and on while a file of that name is
    already there.
    """
    for number in itertools.count(1):
        suffix = MINE_SUFFIX if number == 1 else f'{MINE_SUFFIX}-{number}'
        mine_name = f'{clash.name}{suffix}'

        if not mine_place(clash, mine_name).exists():

            return mine_name


def installed_package(
    home: pathlib.Path,
) -> pathlib.Path | None:
    """
    The `.apm` folder of the package installed for the user, newest name first, or this file's own
    package when none is installed and it is one; None otherwise.
    """
    candidates = [
        home / USER_SCOPE_MODULES / package_path / '.apm'
        for package_path
        in INSTALLED_PACKAGE_PATHS
    ]
    installed = [
        candidate
        for candidate
        in candidates
        if (candidate / 'skills').is_dir()
    ]

    if installed:

        return installed[0]

    if (SCRIPT_PACKAGE / 'prompts').is_dir():

        return SCRIPT_PACKAGE

    return None


def keep_mine(
    home: pathlib.Path,
    target: str,
    package: pathlib.Path | None,
) -> int:
    """
    Rename each of the user's own skills, commands and agents that keeps the package's out to
    `<name>-mine`, and the line inside that names it, never over a file and deleting nothing.
    """
    clashes = find_clashes(
        home,
        target,
        package,
    )

    if clashes is None:

        return 1

    if not clashes:
        print(f"Nothing renamed: none of your own skills, commands or agents takes a name of the package's for {target}.")

        return 0

    not_renamed = []

    for clash in clashes:
        mine_name = free_name(clash)
        mine_path = mine_place(
            clash,
            mine_name,
        )
        named_file = mine_path / SKILL_FILE if clash.kind == 'skill' else mine_path

        try:
            clash.path.rename(mine_path)
            rename_in_file(
                named_file,
                clash.name,
                mine_name,
            )
        except (OSError, UnicodeDecodeError) as exception:
            print(f'Not renamed: your {clash.kind} {clash.name} - {clash.path}: {exception}')
            not_renamed.append(clash)

            continue

        print(f'Renamed your {clash.kind} {clash.name} to {mine_name}: {mine_path}')

    if not_renamed:

        return 1

    print("Now install the package again: each of the package's goes where yours was.")

    return 0


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
    Read the command line, then add the assistant to the user's list, check its files, name the
    user's own that keep the package's out, or rename them.
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

    if parsed.command == 'clashes':
        reported = clashes_report(
            home,
            parsed.target,
            installed_package(home),
        )

        return reported

    if parsed.command == 'keep-mine':
        renamed = keep_mine(
            home,
            parsed.target,
            installed_package(home),
        )

        return renamed

    checked = check_target(
        home,
        parsed.target,
        parsed.slug,
    )

    return checked


def managed_paths(
    lock_file: pathlib.Path,
) -> set[str] | None:
    """
    Every path APM's lock file records as installed, from the user's home folder, with forward
    slashes; None when the file cannot be read.
    """
    try:
        text = lock_file.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):

        return None

    paths = {
        path_match.group('path')
        for path_match
        in MANAGED_PATH_PATTERN.finditer(text)
    }

    return paths


def mine_place(
    clash: Clash,
    mine_name: str,
) -> pathlib.Path:
    """
    Where the user's own goes under its new name: beside it, its file's ending kept.
    """
    renamed = clash.path.name.replace(
        clash.name,
        mine_name,
        1,
    )
    place = clash.path.with_name(renamed)

    return place


def package_places(
    home: pathlib.Path,
    target: str,
    package: pathlib.Path,
) -> list[Clash]:
    """
    Where APM puts each of the package's skills, commands and agents for the assistant, skills
    first, each kind in the order of its names.
    """
    skill_folder = home / SKILL_FOLDERS[target]
    skill_places = [
        Clash(
            kind='skill',
            name=folder.name,
            path=skill_folder / folder.name,
        )
        for folder
        in sorted((package / 'skills').iterdir())
        if (folder / SKILL_FILE).is_file()
    ]
    command_names = [
        prompt.name.removesuffix(COMMAND_ENDING)
        for prompt
        in sorted(package.glob(f'prompts/*{COMMAND_ENDING}'))
    ]
    command_file = COMMAND_FILES.get(target)
    command_places = [
        Clash(
            kind='command',
            name=command_name,
            path=home / command_file.format(name=command_name),
        )
        for command_name
        in command_names
        if command_file is not None
    ]
    agent_names = [
        agent.name.removesuffix(AGENT_ENDING)
        for agent
        in sorted(package.glob(f'agents/*{AGENT_ENDING}'))
    ]
    agent_file = AGENT_FILES.get(target)
    agent_places = [
        Clash(
            kind='agent',
            name=agent_name,
            path=home / agent_file.format(slug=agent_name),
        )
        for agent_name
        in agent_names
        if agent_file is not None
    ]
    places = [
        *skill_places,
        *command_places,
        *agent_places,
    ]

    return places


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


def rename_in_file(
    path: pathlib.Path,
    old_name: str,
    new_name: str,
) -> None:
    """
    Put the new name in the first `name:` or `name =` line that holds the old one, its quotes, its
    comment and every other line as they were; a file with no such line is left as it is.
    """
    lines = read_lines(path)

    for index, line in enumerate(lines):
        name_match = NAME_LINE_PATTERN.fullmatch(_content(line))

        if name_match is None or name_match.group('name') != old_name:
            continue

        quote = name_match.group('quote')
        renamed_line = ''.join([
            name_match.group('key'),
            quote,
            new_name,
            quote,
            name_match.group('rest'),
            _ending(line),
        ])
        renamed_lines = [
            *lines[:index],
            renamed_line,
            *lines[index + 1:],
        ]
        renamed_text = ''.join(renamed_lines)
        path.write_bytes(renamed_text.encode('utf-8'))

        return


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
    The command line: `add`, `clashes` or `keep-mine` with an assistant, or `check` with an
    assistant and a slug.
    """
    targets = sorted(SKILL_FOLDERS)
    parser = argparse.ArgumentParser(
        description=' '.join([
            "Keep an assistant on APM's list in ~/.apm/apm.yml, check the researcher's files for it, or",
            "find and rename your own skills, commands and agents that keep the package's out.",
        ]),
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
    clashes_command = commands.add_parser(
        'clashes',
        help="name your own skills, commands and agents that keep the package's of the same name out",
    )
    clashes_command.add_argument(
        'target',
        choices=targets,
        help='the assistant in use',
    )
    keep_mine_command = commands.add_parser(
        'keep-mine',
        help="rename each of those to <name>-mine, so the next install puts the package's in its place",
    )
    keep_mine_command.add_argument(
        'target',
        choices=targets,
        help='the assistant in use',
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
