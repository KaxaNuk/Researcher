"""
Copy a KaxaNuk starting point into a new folder: a researcher's home, a strategy, an example, or a Python library.

The starting points ship inside the KaxaNuk Researcher package — `templates/researcher/`,
`templates/strategy/`, `templates/python-library/` and the worked examples, one folder each under
`examples/<kind>/<name>/` — and this script copies one of them byte for byte, so every folder made
from the same package version starts identical.  Nothing is written from memory and nothing is
generated; what a checkout, an install, a build or an agent may leave in a starting point — a cache
folder, an agent's folder, `apm_modules/`, `uv.lock`, `dist/`, `docs/_build/` — is left behind, by a
whole copy and by `--only` alike, and so is a key file at any depth: `Config/.env`, any other `.env`
or `*.env`, and `.kaxanuk_license`.

Usage:
    uv run --no-project python scaffold.py researcher <destination>
    uv run --no-project python scaffold.py strategy <destination>
    uv run --no-project python scaffold.py example <destination>
    uv run --no-project python scaffold.py example <destination> --name golden-flow
    uv run --no-project python scaffold.py examples
    uv run --no-project python scaffold.py examples --kind strategy
    uv run --no-project python scaffold.py python-library <destination>
    uv run --no-project python scaffold.py strategy <strategy root> --only Data/analyzer.ipynb
    uv run --no-project python scaffold.py example <a folder of its own> --only Experiments/Experiment_1

An example is a folder `examples/<kind>/<name>/` that holds a `README.md`: its kind is what it is
an example of, `strategy` for `examples/strategy/golden-flow/`, and its name is its own.  `examples`
lists them, one line each, `<kind>/<name> — <its line>`: the line its README marks, alone at
column 0 as `<!-- kaxanuk-example: <its line> -->`, or else its first paragraph's first sentence,
links and emphasis made plain.  `--kind` lists one kind only.  `example` copies the one example
that `--kind` and `--name` leave — the package's only one when neither is given; a name alone, or
`<kind>/<name>` where two kinds share it — and when several are left, or none, it copies nothing
and lists them.  A whole copy's first commit names it:
`Start from the KaxaNuk example <kind>, <name>`.

Without `--only`, the destination must not exist or must be an empty folder — one holding only
what Finder or Explorer leaves, `FILE_MANAGER_FILES`, counts as empty, and those files stay on disk
and out of the commit; the copy is then made a git repository on branch `main` with one first
commit, unless `--no-git`.  With `--only`, one path of the starting point is copied into an
existing folder: a file already there with the same content is skipped, and one with other content
stops the run before anything is written, so nothing is overwritten.  The path is relative and
stays inside both the starting point and the folder: one that is absolute, or that leads outside
either through `..`, is refused before anything is read.  A piece of the example goes into a folder
of its own, never into a strategy, whose file of the same name is the template's.

The package is found beside this script when it runs from a checkout of the package, then
under `apm_modules/` in the folder it runs from or any folder above it, then under `~/.apm/`, where
`apm install -g` puts it.  `--package` names it outright.  A destination or a `--package` that
starts with `~` starts in the user's home folder.  The first line printed names the package found
and the version its `apm.yml` gives, so a copy from a stale install shows it.

On Windows, unless long paths are enabled, a path stops at 259 characters and a folder at 247.  A
copy whose longest path would reach 260 characters, or whose deepest folder would reach 248, is
refused before anything is written, exit code 1: the message names that path and how short a
destination would do.  Where the platform allows long paths, or is not Windows, there is no check.

Exit code 0 when the copy was made, or when `examples` listed one at least; 1 when not; 2 for a
command line it cannot read, such as `examples` given a destination or `strategy` a `--name`.  A
copy the operating system stops partway — a full disk, a file it refuses — is reported in one line
with the file and the system's reason: a new folder's partial copy can be deleted, and a run with
`--only` run again, skipping what it copied.  A git step that fails — git not installed, no
identity for the commit — leaves the copy in place and the exit code 0, and is reported with every
command that finishes the repository by hand, from the failed step on.  git's output is decoded as
UTF-8 and printed as ASCII; the script's own messages are ASCII, but for paths, an example's line
and the dash before it, and the console is written in UTF-8, so a path in any alphabet prints.
"""
import argparse
import ctypes
import dataclasses
import pathlib
import re
import shutil
import subprocess
import sys

# Folders never copied, at any depth: every folder made from one version of the package must start
# identical, so no run may carry a cache, a build's output, an agent's settings or an install it
# happens to hold.
AGENT_FOLDERS = frozenset({
    '.agents',
    '.claude',
    '.codex',
    '.cursor',
    '.gemini',
    '.opencode',
    '.windsurf',
    'apm_modules',
})
CACHE_FOLDERS = frozenset({
    '.ipynb_checkpoints',
    '.mypy_cache',
    '.pdm-build',
    '.pytest_cache',
    '.ruff_cache',
    '.venv',
    '__pycache__',
    '_build',
    'dist',
})
# Files Finder or Explorer leaves in a folder it shows: a folder holding only these is still empty,
# and the first commit leaves them out, since a strategy's .gitignore before template 0.13.4 does
# not name them.
FILE_MANAGER_FILES = frozenset({
    '.DS_Store',
    'Thumbs.db',
    'desktop.ini',
})
# Key files, never copied at any depth, as a file or a folder: a key never leaves the folder it was
# typed into.  These are the names the starting points' .gitignore files keep out of git: `.env`
# and any `*.env`, wherever it sits, and the licence the Lab's libraries can read.
KEY_FILE_NAMES = frozenset({
    '.kaxanuk_license',
})
KEY_FILE_SUFFIX = '.env'
# Files never copied, as POSIX paths from a starting point's root: the lock `uv sync` writes on one
# machine.
NEVER_COPIED_FILES = frozenset({
    'uv.lock',
})
# Each starting point: where it sits inside the package, and the first commit of a copy of it.  The
# example's is the folder holding every example, one per `examples/<kind>/<name>/`, and its message
# takes the kind and the name of the one copied.  The python-library message must equal
# `FIRST_COMMIT` in the init-python-library skill's `name_library.py`, which names only a copy whose
# history is that commit alone, so the two change together.
STARTING_POINTS = {
    'researcher': (
        'templates/researcher',
        'Start from the KaxaNuk Researcher template',
    ),
    'strategy': (
        'templates/strategy',
        'Start from the KaxaNuk Strategy Template',
    ),
    'example': (
        'examples',
        'Start from the KaxaNuk example {kind}, {name}',
    ),
    'python-library': (
        'templates/python-library',
        'Start from the KaxaNuk Python Library Template',
    ),
}
# The starting point that is chosen among the examples, the word that lists them instead of copying
# one, and the file every example holds, which gives its line.
EXAMPLE = 'example'
EXAMPLE_README = 'README.md'
LIST_EXAMPLES = 'examples'
# How an example's README gives its line: a line it marks, or else its first paragraph's first
# sentence.  Headings and lines that are a comment, such as the example's own markers, are taken out
# first; the first paragraph is then the first run of lines between blank lines that opens as none
# of a table, a quote, HTML, a fence, a badge or an image, a list or a rule.  A sentence ends at
# `.`, `!` or `?` before a space and a capital letter; a link keeps its text, and emphasis its words.
EMPHASIS = re.compile(r'(?P<mark>\*{1,2}|_{2})(?P<text>\S(?:.*?\S)?)(?P=mark)')
EXAMPLE_LINE_MARKER = re.compile(
    r'^<!-- kaxanuk-example: (?P<line>.+?) -->[ \t]*$',
    re.MULTILINE,
)
HEADING_OR_COMMENT_LINE = re.compile(
    r'^(?:#{1,6}(?:[ \t].*)?|<!--.*-->[ \t]*)$',
    re.MULTILINE,
)
LINK = re.compile(r'!?\[(?P<text>[^\]]*)\]\([^)]*\)')
NOT_A_PARAGRAPH = re.compile(r'(?:[|>#<]|`{3}|~{3}|!\[|\[!\[|(?:[-*+]|\d+[.)])\s|(?P<rule>[-*_])(?P=rule){2,}\s*$)')
PARAGRAPH_BREAK = re.compile(r'\n[ \t]*\n')
SENTENCE_BREAK = re.compile(r'[.!?]\s+(?=\S)')
# Where APM puts the package, relative to an `apm_modules/` folder: from GitHub; from GitHub under
# the repository's name before 1.25.0, KaxaNuk-Researcher, until `update` moves it; then from a path.
INSTALLED_PACKAGE_PATHS = [
    pathlib.Path('KaxaNuk') / 'Researcher',
    pathlib.Path('KaxaNuk') / 'KaxaNuk-Researcher',
    pathlib.Path('_local') / 'KaxaNuk-Researcher',
]
# The package root seen from this file: scripts/ -> init-strategy/ -> skills/ -> .apm/ -> the root.
SCRIPT_PATH = pathlib.Path(__file__).resolve()
SOURCE_PACKAGE = SCRIPT_PATH.parents[4]
USER_SCOPE_MODULES = pathlib.Path.home() / '.apm' / 'apm_modules'
# What is said when git cannot be run at all, and the version the first line gives a package whose
# `apm.yml` names none.
GIT_NOT_FOUND = 'git was not found on this computer; install it first'
UNKNOWN_VERSION = 'unknown'
# Windows without long paths: a path of 260 characters, its terminating null included, is too long,
# and a folder takes 12 fewer, room for a short file name inside it.
WINDOWS_MAX_PATH = 260
WINDOWS_FOLDER_MARGIN = 12
MISSING_PACKAGE = ' '.join([
    'The researcher package was not found. Install it with',
    '`uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher --target <agent>`,',
    'or pass --package.',
])
NO_EXAMPLES = 'The package holds no example: no folder examples/<kind>/<name>/ in it holds a README.md'


@dataclasses.dataclass(frozen=True)
class CopyPlan:
    """
    What one run copies: every source file and the path it lands at.
    """
    source_root: pathlib.Path
    destination_root: pathlib.Path
    files: tuple[tuple[pathlib.Path, pathlib.Path], ...]


@dataclasses.dataclass(frozen=True)
class Example:
    """
    One worked example in the package: its folder, `examples/<kind>/<name>/`, and the line its README gives.
    """
    folder: pathlib.Path
    kind: str
    name: str
    summary: str


@dataclasses.dataclass(frozen=True)
class StartingPoint:
    """
    The folder one run copies from, and the first commit a whole copy of it is saved with.
    """
    first_commit: str
    root: pathlib.Path


def copy_files(
    plan: CopyPlan,
) -> str | None:
    """
    Copy every file in the plan, creating the folders it needs: None when every file was copied,
    otherwise the path the operating system stopped the copy at, and its reason.
    """
    for source, target in plan.files:
        try:
            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            shutil.copy2(
                source,
                target,
            )
        except OSError as exception:
            failed_path = exception.filename or target
            reason = exception.strerror or str(exception)
            failure = f'{failed_path}: {reason}'

            return failure

    return None


def find_examples(
    package: pathlib.Path,
) -> list[Example]:
    """
    Every example in the package, by kind then name: each folder `examples/<kind>/<name>/` that holds a
    `README.md`, leaving aside a hidden folder and one no copy carries, such as `__pycache__/`.
    """
    examples_root = package / STARTING_POINTS[EXAMPLE][0]
    example_folders = [
        example_folder
        for kind_folder
        in _listed_folders(examples_root)
        for example_folder
        in _listed_folders(kind_folder)
        if (example_folder / EXAMPLE_README).is_file()
    ]
    examples = [
        Example(
            folder=example_folder,
            kind=example_folder.parent.name,
            name=example_folder.name,
            summary=_readme_line(example_folder / EXAMPLE_README),
        )
        for example_folder
        in example_folders
    ]

    return examples


def find_package(
    explicit: pathlib.Path | None,
    start: pathlib.Path,
) -> pathlib.Path | None:
    """
    The KaxaNuk Researcher package's root: the one given, the checkout this script sits in, or an install.
    """
    if explicit is not None:
        given = explicit if _is_package(explicit) else None

        return given

    candidates = [
        SOURCE_PACKAGE,
        *_installed_candidates(start),
    ]
    packages = [
        candidate
        for candidate
        in candidates
        if _is_package(candidate)
    ]
    found = packages[0] if packages else None

    return found


def main(
    arguments: list[str] | None = None,
) -> int:
    """
    Parse the command line, check the destination, copy, and make the copy a git repository.

    `examples` lists the examples instead, and copies nothing.
    """
    # A path in any alphabet — Łucja, Sofía — prints, whatever the console's own code page.
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
    usage_problem = _usage_problem(parsed)

    if usage_problem is not None:
        parser.error(usage_problem)

    package = find_package(
        parsed.package,
        pathlib.Path.cwd(),
    )

    if package is None:
        print(MISSING_PACKAGE)

        return 1

    version = _package_version(package)
    print(f'The package at {package.resolve()}, version {version}')

    if parsed.starting_point == LIST_EXAMPLES:
        listed = _list_examples(
            package,
            parsed.kind,
        )

        return listed

    starting_point = _chosen_starting_point(
        package,
        parsed.starting_point,
        parsed.kind,
        parsed.name,
    )

    if starting_point is None:

        return 1

    source_root = starting_point.root
    destination = parsed.destination.resolve()

    if parsed.only is not None:
        exit_code = _copy_one_path(
            source_root,
            destination,
            parsed.only,
        )

        return exit_code

    problem = _destination_problem(destination)

    if problem is not None:
        print(problem)

        return 1

    plan = plan_copy(
        source_root,
        destination,
        source_root,
    )
    too_long = _long_path_problem(
        plan,
        destination,
    )

    if too_long is not None:
        print(too_long)

        return 1

    failure = copy_files(plan)

    if failure is not None:
        print(f'The copy stopped at {failure}. Anything it wrote is in {destination}, which can be deleted.')

        return 1

    print(f'Copied {len(plan.files)} files from {source_root} to {destination}')

    if not parsed.no_git:
        _make_repository(
            destination,
            starting_point.first_commit,
        )

    return 0


def plan_copy(
    source_root: pathlib.Path,
    destination_root: pathlib.Path,
    starting_point: pathlib.Path,
) -> CopyPlan:
    """
    Every file under the source, in a stable order, paired with the path it lands at.

    The source is the starting point, or one folder of it for `--only`; a file `_is_left_behind`
    names is left out, judged from the starting point's root either way.
    """
    sources = sorted(
        path
        for path
        in source_root.rglob('*')
        if path.is_file()
        and not _is_left_behind(
            path,
            starting_point,
        )
    )
    files = tuple(
        (
            source,
            destination_root / source.relative_to(source_root),
        )
        for source
        in sources
    )
    plan = CopyPlan(
        source_root=source_root,
        destination_root=destination_root,
        files=files,
    )

    return plan


def _as_ascii(
    text: str,
) -> str:
    """
    Text as the console gets it: stripped, every character outside ASCII a question mark.
    """
    encoded = text.encode(
        'ascii',
        errors='replace',
    )
    ascii_text = encoded.decode('ascii').strip()

    return ascii_text


def _as_typed(
    command: list[str],
) -> str:
    """
    A command as a person types it: an argument holding a space inside double quotes.
    """
    words = [
        f'"{word}"' if ' ' in word else word
        for word
        in command
    ]
    typed = ' '.join(words)

    return typed


def _asked_for(
    kind: str | None,
    name: str | None,
) -> str:
    """
    What `--kind` and `--name` asked for, as a message puts it after "examples": ` of kind strategy`.
    """
    of_kind = f' of kind {kind}' if kind is not None else ''
    named = f' named {name}' if name is not None else ''
    asked = f'{of_kind}{named}'

    return asked


def _build_parser() -> argparse.ArgumentParser:
    """
    The command line: which starting point, or `examples` to list them, where to, and the options.
    """
    parser = argparse.ArgumentParser(
        description='Copy a KaxaNuk starting point into a new folder, or list the examples.',
    )
    parser.add_argument(
        'starting_point',
        choices=sorted([
            *STARTING_POINTS,
            LIST_EXAMPLES,
        ]),
        help='researcher, strategy, example or python-library; examples lists the examples',
    )
    parser.add_argument(
        'destination',
        nargs='?',
        type=_expanded_path,
        default=None,
        help='the new folder; with --only, the existing folder to copy into; none for examples',
    )
    parser.add_argument(
        '--kind',
        default=None,
        help='example and examples: only the examples of this kind, such as strategy',
    )
    parser.add_argument(
        '--name',
        default=None,
        help='example: the example to copy, by its name, or as <kind>/<name>',
    )
    parser.add_argument(
        '--only',
        type=pathlib.PurePosixPath,
        default=None,
        help='copy one file or folder of the starting point into an existing folder',
    )
    parser.add_argument(
        '--no-git',
        action='store_true',
        help='leave the copy as plain files, with no git repository',
    )
    parser.add_argument(
        '--package',
        type=_expanded_path,
        default=None,
        help='the researcher package folder, when it cannot be found on its own',
    )

    return parser


def _chosen_example(
    examples: list[Example],
    kind: str | None,
    name: str | None,
) -> Example | None:
    """
    The one example that `--kind` and `--name` leave, or None once it has said why there is not one.
    """
    candidates = [
        example
        for example
        in examples
        if _example_matches(
            example,
            kind,
            name,
        )
    ]

    if len(candidates) == 1:

        return candidates[0]

    problem = _example_problem(
        examples,
        candidates,
        kind,
        name,
    )
    print(problem)

    return None


def _chosen_starting_point(
    package: pathlib.Path,
    kind_of_copy: str,
    example_kind: str | None,
    example_name: str | None,
) -> StartingPoint | None:
    """
    Where the copy comes from and its first commit: a template's folder, or the one example chosen.

    None when no one example is chosen, once it has said why.
    """
    relative_source, first_commit = STARTING_POINTS[kind_of_copy]

    if kind_of_copy != EXAMPLE:
        template = StartingPoint(
            first_commit=first_commit,
            root=package / relative_source,
        )

        return template

    examples = find_examples(package)
    example = _chosen_example(
        examples,
        example_kind,
        example_name,
    )

    if example is None:

        return None

    example_commit = first_commit.format(
        kind=example.kind,
        name=example.name,
    )
    chosen = StartingPoint(
        first_commit=example_commit,
        root=example.folder,
    )

    return chosen


def _copy_one_path(
    source_root: pathlib.Path,
    destination: pathlib.Path,
    only: pathlib.PurePosixPath,
) -> int:
    """
    Copy one file or folder of the starting point into an existing folder, overwriting nothing.

    A path that is absolute, or that leads outside the starting point or the folder once `..` and
    links are resolved, is refused before anything is read; so is one `_is_left_behind` names, and
    a folder's copy leaves out what it names inside.
    """
    source = source_root / only
    target = destination / only

    if not destination.is_dir():
        print(f'{destination} is not an existing folder; --only copies into one')

        return 1

    is_absolute = pathlib.PurePath(only).anchor != ''
    leads_outside = (
        is_absolute
        or _leads_outside(
            source_root,
            source,
        )
        or _leads_outside(
            destination,
            target,
        )
    )

    if leads_outside:
        print(f'{only} leads outside the starting point or the folder; nothing was copied')

        return 1

    if not source.exists():
        print(f'{only} is not part of this starting point')

        return 1

    left_behind = _is_left_behind(
        source,
        source_root,
    )

    if left_behind:
        print(f'{only} is never copied: no copy of a starting point carries it')

        return 1

    if source.is_file():
        plan = CopyPlan(
            source_root=source.parent,
            destination_root=target.parent,
            files=((source, target),),
        )
    else:
        plan = plan_copy(
            source,
            target,
            source_root,
        )

    different = [
        str(landing.relative_to(destination))
        for origin, landing
        in plan.files
        if _differs(
            origin,
            landing,
        )
    ]

    if different:
        print('Nothing was copied; these files already exist with other content:')

        for path in different:
            print(f'  {path}')

        return 1

    missing = tuple(
        (origin, landing)
        for origin, landing
        in plan.files
        if not landing.exists()
    )
    missing_plan = CopyPlan(
        source_root=plan.source_root,
        destination_root=plan.destination_root,
        files=missing,
    )
    too_long = _long_path_problem(
        missing_plan,
        destination,
    )

    if too_long is not None:
        print(too_long)

        return 1

    failure = copy_files(missing_plan)

    if failure is not None:
        print(f'The copy stopped at {failure}. Run it again once that is fixed: what it copied is skipped.')

        return 1

    already_there = len(plan.files) - len(missing)
    print(f'Copied {len(missing)} files into {target}; {already_there} were already there, identical')

    return 0


def _destination_problem(
    destination: pathlib.Path,
) -> str | None:
    """
    Why the destination cannot take a new copy, or None when it can.

    A folder holding only `FILE_MANAGER_FILES` counts as empty: one the owner made in Finder or
    Explorer still takes the copy.
    """
    if not destination.exists():

        return None

    if not destination.is_dir():
        not_a_folder = f'{destination} exists and is not a folder'

        return not_a_folder

    contents = [
        entry
        for entry
        in destination.iterdir()
        if entry.name not in FILE_MANAGER_FILES
    ]

    if contents:
        not_empty = f'{destination} is not empty; choose a new folder'

        return not_empty

    return None


def _differs(
    origin: pathlib.Path,
    landing: pathlib.Path,
) -> bool:
    """
    Whether a file already sits where a copy would land, with content other than the copy's.
    """
    if not landing.exists():

        return False

    same = landing.read_bytes() == origin.read_bytes()

    return not same


def _example_line(
    example: Example,
) -> str:
    """
    An example as `examples` lists it: `<kind>/<name> — <its line>`, or the path alone when its README gives none.
    """
    path = f'{example.kind}/{example.name}'
    line = f'{path} — {example.summary}' if example.summary else path

    return line


def _example_matches(
    example: Example,
    kind: str | None,
    name: str | None,
) -> bool:
    """
    Whether an example is of the kind asked for and has the name asked for, as `<name>` or `<kind>/<name>`.
    """
    kind_matches = kind is None or example.kind == kind
    names = {
        example.name,
        f'{example.kind}/{example.name}',
    }
    name_matches = name is None or name in names
    matches = kind_matches and name_matches

    return matches


def _example_problem(
    examples: list[Example],
    candidates: list[Example],
    kind: str | None,
    name: str | None,
) -> str:
    """
    Why no one example was chosen, listing what the package holds: none at all, none that matches, or several.
    """
    if not examples:

        return NO_EXAMPLES

    asked = _asked_for(
        kind,
        name,
    )

    if candidates:
        several = [
            f'The package holds {len(candidates)} examples{asked}; name one with --name <name>, or <kind>/<name>:',
            *(
                f'  {_example_line(example)}'
                for example
                in candidates
            ),
        ]
        choose_one = '\n'.join(several)

        return choose_one

    held = [
        f'No example{asked} is in the package; it holds:',
        *(
            f'  {_example_line(example)}'
            for example
            in examples
        ),
    ]
    none_matches = '\n'.join(held)

    return none_matches


def _expanded_path(
    text: str,
) -> pathlib.Path:
    """
    A path from the command line, a leading `~` turned into the user's home folder.

    A path in quotes reaches the script with its `~` as typed, and PowerShell never expands one.
    """
    path = pathlib.Path(text).expanduser()

    return path


def _first_sentence(
    markdown: str,
) -> str:
    """
    The first sentence of a Markdown text's first paragraph, links and emphasis made plain; empty when it has none.

    How a paragraph and a sentence are told apart is said where `NOT_A_PARAGRAPH` and
    `SENTENCE_BREAK` are declared.
    """
    prose = HEADING_OR_COMMENT_LINE.sub(
        '',
        markdown,
    )
    paragraphs = [
        ' '.join(block.split())
        for block
        in PARAGRAPH_BREAK.split(prose)
        if block.strip()
        and NOT_A_PARAGRAPH.match(block.strip()) is None
    ]

    if not paragraphs:

        return ''

    linked = LINK.sub(
        r'\g<text>',
        paragraphs[0],
    )
    paragraph = EMPHASIS.sub(
        r'\g<text>',
        linked,
    )
    sentence_ends = [
        found.start() + 1
        for found
        in SENTENCE_BREAK.finditer(paragraph)
        if paragraph[found.end()].isupper()
    ]
    sentence = paragraph[:sentence_ends[0]] if sentence_ends else paragraph

    return sentence


def _installed_candidates(
    start: pathlib.Path,
) -> list[pathlib.Path]:
    """
    Where an install may have put the package: in `apm_modules/` at or above `start`, then at user scope.
    """
    module_folders = [
        folder / 'apm_modules'
        for folder
        in [start.resolve(), *start.resolve().parents]
    ]
    module_folders.append(USER_SCOPE_MODULES)
    candidates = [
        modules / package_path
        for modules
        in module_folders
        for package_path
        in INSTALLED_PACKAGE_PATHS
    ]

    return candidates


def _is_left_behind(
    path: pathlib.Path,
    starting_point: pathlib.Path,
) -> bool:
    """
    Whether no copy carries this file or folder: one inside a folder of `AGENT_FOLDERS` or
    `CACHE_FOLDERS`, a key file — a name in `KEY_FILE_NAMES` or ending in `KEY_FILE_SUFFIX`, at any
    depth — or one of `NEVER_COPIED_FILES`.

    The path is read from the starting point's root, whatever `--only` named, once `..`, links and
    the name Windows opens are resolved, and with case ignored, so `--only Config` and
    `--only config/.ENV` both leave `Config/.env` behind.  A link that leads outside the starting
    point is read as it is spelled.
    """
    resolved_root = starting_point.resolve()
    resolved_path = path.resolve()
    relative_path = (
        resolved_path.relative_to(resolved_root)
        if resolved_path.is_relative_to(resolved_root)
        else path.relative_to(starting_point)
    )
    relative = relative_path.as_posix().casefold()
    never_copied = {
        file_path.casefold()
        for file_path
        in NEVER_COPIED_FILES
    }
    parts = relative.split('/')
    in_left_folder = any(
        part in AGENT_FOLDERS or part in CACHE_FOLDERS
        for part
        in parts
    )
    is_key_file = any(
        part in KEY_FILE_NAMES or part.endswith(KEY_FILE_SUFFIX)
        for part
        in parts
    )
    left_behind = in_left_folder or is_key_file or relative in never_copied

    return left_behind


def _is_package(
    candidate: pathlib.Path,
) -> bool:
    """
    Whether a folder holds every starting point: each template, and the folder of the examples.
    """
    holds_all = all(
        (candidate / relative_source).is_dir()
        for relative_source, _
        in STARTING_POINTS.values()
    )

    return holds_all


def _leads_outside(
    root: pathlib.Path,
    path: pathlib.Path,
) -> bool:
    """
    Whether a path lands outside the folder it must stay under, once `..` and links are resolved.
    """
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    inside = resolved_path.is_relative_to(resolved_root)

    return not inside


def _list_examples(
    package: pathlib.Path,
    kind: str | None,
) -> int:
    """
    Print one line per example, of one kind when `--kind` names it: 0 when one is listed at least, else 1.
    """
    examples = find_examples(package)
    listed = [
        example
        for example
        in examples
        if _example_matches(
            example,
            kind,
            None,
        )
    ]

    if not listed:
        problem = _example_problem(
            examples,
            listed,
            kind,
            None,
        )
        print(problem)

        return 1

    for example in listed:
        print(_example_line(example))

    return 0


def _listed_folders(
    parent: pathlib.Path,
) -> list[pathlib.Path]:
    """
    The folders inside one, by name, but for a hidden folder and one no copy carries: an agent's or a cache.
    """
    if not parent.is_dir():

        return []

    folders = sorted(
        entry
        for entry
        in parent.iterdir()
        if entry.is_dir()
        and not entry.name.startswith('.')
        and entry.name not in AGENT_FOLDERS | CACHE_FOLDERS
    )

    return folders


def _long_path_problem(
    plan: CopyPlan,
    destination: pathlib.Path,
) -> str | None:
    """
    Why the plan's paths are too long for this machine, or None when they fit.

    Only Windows without long paths has a limit: a path reaching `WINDOWS_MAX_PATH` characters, or
    a folder reaching `WINDOWS_MAX_PATH` less `WINDOWS_FOLDER_MARGIN`, cannot be written.  The
    message names the path that goes furthest past it and the longest destination that would fit.
    """
    if not plan.files or not _path_limit_applies():

        return None

    targets = [
        target
        for _, target
        in plan.files
    ]
    longest = max(
        targets,
        key=_windows_reach,
    )
    excess = _windows_reach(longest) - WINDOWS_MAX_PATH + 1

    if excess <= 0:

        return None

    room = len(str(destination)) - excess
    shorter = pathlib.Path(destination.anchor) / destination.name
    place = (
        f'such as {shorter}'
        if len(str(shorter)) <= room
        else 'nearer the root of a drive'
    )
    path_limit = WINDOWS_MAX_PATH - 1
    folder_limit = WINDOWS_MAX_PATH - WINDOWS_FOLDER_MARGIN - 1
    path_length = len(str(longest))
    folder_length = len(str(longest.parent))
    problem = '\n'.join([
        f'Nothing was copied: on Windows, without long paths, a path stops at {path_limit} characters',
        f'and a folder at {folder_limit}, and this copy would write',
        f'  {longest}',
        f'({path_length} characters, its folder {folder_length}).',
        f'Choose a destination of at most {room} characters, {place}.',
    ])

    return problem


def _make_repository(
    destination: pathlib.Path,
    first_commit: str,
) -> None:
    """
    Make the copy a git repository on branch `main` with one first commit, and say so.

    What Finder or Explorer left in the folder, `FILE_MANAGER_FILES`, is taken back out of the
    commit and stays on disk.  A failed step — git not installed, no identity for the commit — is
    reported with every command that finishes the repository by hand, from the failed step on.
    """
    commands = [
        [
            'git',
            'init',
            '--quiet',
            '--initial-branch=main',
        ],
        [
            'git',
            'add',
            '--all',
        ],
        [
            'git',
            'rm',
            '--cached',
            '--quiet',
            '--ignore-unmatch',
            '--',
            *sorted(FILE_MANAGER_FILES),
        ],
        [
            'git',
            'commit',
            '--quiet',
            '-m',
            first_commit,
        ],
    ]

    for position, command in enumerate(commands):
        failure = _run_git(
            command,
            destination,
        )

        if failure is not None:
            step = ' '.join(command[:2])
            remaining = [
                _as_typed(still_to_run)
                for still_to_run
                in commands[position:]
            ]
            print(f'`{step}` failed; the files are copied, the repository is not finished:')
            print(failure)
            print('Finish it in that folder with:')

            for typed in remaining:
                print(f'  {typed}')

            return

    print(f'Made it a git repository, first commit: "{first_commit}"')


def _package_version(
    package: pathlib.Path,
) -> str:
    """
    The version the package's `apm.yml` names on its top-level `version:` line, or `unknown`.

    The line is read as text: the script runs with no project, so no YAML library is at hand.
    """
    try:
        manifest = (package / 'apm.yml').read_text(encoding='utf-8')
    except OSError:

        return UNKNOWN_VERSION

    versions = [
        line.removeprefix('version:').strip()
        for line
        in manifest.splitlines()
        if line.startswith('version:')
    ]
    version = versions[0] if versions else UNKNOWN_VERSION

    return version


def _path_limit_applies() -> bool:
    """
    Whether this process stops a path at `WINDOWS_MAX_PATH`: on Windows, unless long paths are enabled.

    Windows answers for the process itself, so the registry setting and Python's own manifest both
    count; a Windows too old to answer has the limit.
    """
    if sys.platform != 'win32':

        return False

    try:
        long_paths = ctypes.windll.ntdll.RtlAreLongPathsEnabled()
    except (AttributeError, OSError):

        return True

    applies = not long_paths

    return applies


def _readme_line(
    readme: pathlib.Path,
) -> str:
    """
    The line an example's README gives on what it shows: the one it marks, or else its first paragraph's first sentence.

    Empty when it gives neither, or cannot be read.
    """
    try:
        markdown = readme.read_text(
            encoding='utf-8',
            errors='replace',
        )
    except OSError:

        return ''

    marked = EXAMPLE_LINE_MARKER.search(markdown)

    if marked is not None:
        marked_line = marked['line'].strip()

        return marked_line

    sentence = _first_sentence(markdown)

    return sentence


def _run_git(
    command: list[str],
    destination: pathlib.Path,
) -> str | None:
    """
    Run one git command in the copy: None when it succeeded, otherwise what went wrong, in ASCII.

    The output is decoded as UTF-8 with replacement, so a localised or undecodable message cannot
    raise; a git that writes nothing to its error stream is quoted from its output instead.
    """
    try:
        completed = subprocess.run(
            command,
            cwd=destination,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            check=False,
        )
    except FileNotFoundError:

        return GIT_NOT_FOUND

    if completed.returncode == 0:

        return None

    message = completed.stderr or completed.stdout
    failure = _as_ascii(message)

    return failure


def _usage_problem(
    parsed: argparse.Namespace,
) -> str | None:
    """
    Why the command line asks for something the script does not do, or None when it does not.

    `examples` takes no destination and copies nothing, so neither `--name` nor `--only`; every
    other starting point needs a destination, and only `example` and `examples` take `--kind` or
    `--name`.
    """
    lists_examples = parsed.starting_point == LIST_EXAMPLES

    if lists_examples and parsed.destination is not None:
        listing_has_destination = 'examples lists the examples and takes no destination; --kind narrows the list'

        return listing_has_destination

    if lists_examples and (parsed.name is not None or parsed.only is not None):
        listing_copies = 'examples copies nothing, so it takes neither --name nor --only; --kind narrows the list'

        return listing_copies

    if not lists_examples and parsed.destination is None:
        no_destination = f'{parsed.starting_point} needs a destination: the new folder, or with --only an existing one'

        return no_destination

    chooses_example = parsed.starting_point in {
        EXAMPLE,
        LIST_EXAMPLES,
    }

    if not chooses_example and (parsed.kind is not None or parsed.name is not None):
        not_an_example = f'--kind and --name choose an example; {parsed.starting_point} takes neither'

        return not_an_example

    return None


def _windows_reach(
    target: pathlib.Path,
) -> int:
    """
    How far a target goes against Windows' limit: its own length, or its folder's plus the margin.
    """
    reach = max(
        len(str(target)),
        len(str(target.parent)) + WINDOWS_FOLDER_MARGIN,
    )

    return reach


if __name__ == '__main__':
    sys.exit(main())
