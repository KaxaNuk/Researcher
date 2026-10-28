# Contributing to the KaxaNuk Researcher

This file is for anyone who installs the package by hand, or changes or forks it: the install in a
terminal, the path after it, what this repository holds, and how a change is checked. The rules for
changing the package (where work lands, versions and changelogs, keeping the template and the
worked example in step, forks) are in [`AGENTS.md`](AGENTS.md); read it before changing anything.
Using the researcher needs only the [`README.md`](README.md); its *What it is, and what it is not*
says what the package is for.

## Installing by hand, in a terminal

```bash
uv tool install apm-cli==0.33.0
uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/KaxaNuk-Researcher --target claude
```

For another assistant, put `codex`, `gemini`, `cursor` or another in place of `claude`. Claude Code
receives everything. *Troubleshooting* in [`SETUP.md`](SETUP.md) says what the others miss, and why
APM stays at 0.33.0, named in every command, and `apm self-update` is never run. A second assistant
installed this way keeps its files through the next update only once it is on APM's list in
`~/.apm/apm.yml`:

```bash
uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/KaxaNuk-Researcher/.apm/skills/init-researcher/scripts/user_targets.py" add codex
```

`uvx --from apm-cli==0.33.0 apm update -g` brings every new version. Then open a new session,
anywhere, and follow the path below. An assistant asked to install follows [`SETUP.md`](SETUP.md)
instead, all in one conversation. *Removing it*, in the README, undoes either.

## The path after the install

| | In | Run | It makes |
| --- | --- | --- | --- |
| 1 | anywhere | `init-researcher Arya` | the researcher's home, named after it, then the interview, which writes `RESEARCHER.md`, the agent and the researcher's skill, installs them for your user and saves a first version. The install in [`SETUP.md`](SETUP.md) runs this for you |
| 2 | the home | `read` | your first note: attach or name a document, copied into `Sources/` on your go; the first `read` asks which question it serves and keeps it as question 1 |
| 3 | the home | `philosophy`, `brief setup` | when you like: how you work or how you invest, in your words, and a daily brief |
| 4 | the home | `init-strategy fcf-yield-quality` | your first strategy, a repository of its own beside the home; its `SETUP.md` finishes the setup |
| 5 | the strategy | `objective` | the strategy's claims, before any paper; then the order of work, A to H, in the template's README, which the strategy's links to |

The reading map covers investment research; `philosophy` covers how the owner invests or how they
work, in any field, and a researcher for another field grows by reading.

## What is in here

```
.apm/skills/          every skill: the researcher's, the Investment Lab's and the house rules'
.apm/prompts/         the commands
.apm/instructions/    the house style: Bloom Code, PEP 8, filesystem boundaries
.apm/agents/          the one agent, blueprint-critic
templates/strategy/   the KaxaNuk Strategy Template — the eight steps as folders; its README is the
                      process, and the order of work a strategy follows
templates/researcher/ the researcher's home, empty
templates/python-library/
                      the KaxaNuk Python Library Template — a Python library laid out like the
                      KaxaNuk Data Curator, named for its owner by init-python-library
examples/<kind>/<name>/
                      the worked examples, one folder each, by kind as the templates are: today
                      one, a strategy worked through every folder of the template
tools/                the harness: check.py, every check a commit passes; install_check.py, the
                      install a release is tried with; release.py, the release; never installed
tests/                the tests of the skills' scripts and of tools/, which check.py runs
.githooks/pre-commit  runs check.py, the tests aside, before each commit, once a clone sets it
SETUP.md              the install, step by step — what an assistant follows when you paste the URL
USE-CASES.md          twelve ways to use the researcher, step by step
ONBOARDING.md         the onboarding and first read as approved, step by step — frozen
FROZEN.json           the fingerprints of the frozen files
apm.yml               the package: what apm install reads; it depends on nothing
pyproject.toml        the ruff settings for the skills' scripts, tools/ and tests/, and pytest's
AGENTS.md, CLAUDE.md  the rules for changing this repository
CONTRIBUTING.md       this file: the install by hand, this layout, and how a change is checked
CHANGELOG.md          one entry per version
LICENSE               MIT
.gitignore            what apm install and Python write per machine
```

**What this repository owns, and what a copy owns.** This repository owns what is written once and
copied or installed everywhere; a copy owns what its owner writes in it. A strategy or a Python
library made from a template is its owner's from the first commit and never merges back; the
skills keep updating with `uvx --from apm-cli==0.33.0 apm update -g`.

## Development

One command runs every check a commit passes, from the repository's root:

```bash
uv run --no-project python -I tools/check.py
```

Each check prints `ok` or `FAIL`, with what failed under it, and a failure never stops the next one:

- **ruff** at the root, which covers the skills' scripts, `tools/` and `tests/`, then in the
  strategy and Python library templates and in every example, each with its own settings;
- **the Bloom Code check** on the skills' scripts, `tools/` and `tests/` at its default 120 columns,
  then from inside each template and example, so it finds their own packages, at the line length
  each sets: 100 for a strategy, its template and its examples, 120 for the Python library template;
- **the frozen files**, each against its fingerprint in `FROZEN.json`, line endings aside;
- **the template and the example in step**, below;
- **the Markdown** added since `origin/dev`, committed or not: LF line endings, no literal tab, no
  section sign, and 100 columns but where `AGENTS.md` allows a longer line;
- **the versions**: each part's version agrees with its `CHANGELOG.md`, and a part changed since the
  last release's tag carries a new one — the package, the home template, the strategy template, each
  example and the Python library template's *Started from* sentence;
- **the private words**, below;
- **the tests** in `tests/`, by pytest, which `uv` brings with pypdf.

Everything runs through `uv`: no Python of your own is needed. There is no CI. Once per clone,

```bash
git config core.hooksPath .githooks
```

makes git run `tools/check.py --fast`, every check but the tests, before each commit, and refuse the
commit when one fails. Nothing else runs inside `templates/`: `uv sync`, `uv build` or Sphinx there
would write a `.venv/`, a `uv.lock` or a `dist/` into the package.

**The frozen files stay unchanged** unless the owner says otherwise, as `AGENTS.md` says under
*Rules*. When the check names one, revert it or show it to the owner; its fingerprint moves only on
the owner's word.

**The template and the example in step.** They are kept in step by hand, by the rules in
`AGENTS.md`, and the check compares them. For each Markdown, Python and notebook file
`git ls-files templates/strategy` lists that the example also holds, it drops the example's own
lines, marked as `AGENTS.md` says (in a notebook, also every marked block inside a cell, and every
example-only cell), and compares the rest with the template's copy, blank lines aside, notebooks
cell by cell, by cell id. The exceptions `AGENTS.md` lists are applied: the example's `README.md` is
its own, its `CHANGELOG.md` shares only what comes before its entries, the template's `OBJECTIVE.md`
body and its `AGENTS.md` status banner are what the example replaces. `SETUP.md`'s `init-example`
lines are recorded in `tools/parity_exceptions.json`; when a change to either copy moves them, the
check names each difference, and once each has been read and is one `AGENTS.md` allows,

```bash
uv run --no-project python -I tools/check.py --record-parity
```

records them anew. Any other difference is a fault.

**The private words.** `.git/info/private-names.txt` lists, one per line, what no tracked file,
commit message not yet on `origin/dev` or branch may hold: a client's name, a personal path. Git
never commits or sends that folder, so each clone writes its own; a clone without it is told the
check was skipped.

**To try a change** to a skill, a command, an instruction or the agent, install it at project scope
from a short scratch folder, with APM 0.33.0, **in a shell whose home is a short, empty throwaway
folder**. Never install the working tree with `-g`: on Windows that stages its ignored folders too,
past the path limit. A skill installed for your user wins over a project skill of the same name, so
without the throwaway home the check would run your installed copy, and the walk below would change
your real setup. From the repository's root:

```bash
K=C:/k   # an absolute, short path of your own: /tmp/k on macOS or Linux, never ~
mkdir -p "$K/home" "$K/check"
REV=$(git stash create)
git -c core.autocrlf=false archive --format=tar --prefix=KaxaNuk-Researcher/ "${REV:-HEAD}" | tar -x -C "$K"
export HOME="$K/home"
export USERPROFILE="$HOME"
git config --global user.name "Tester"; git config --global user.email "tester@example.invalid"
cd "$K/check"
uvx --from apm-cli==0.33.0 apm install "$K/KaxaNuk-Researcher" --target claude
```

`git stash create` takes your uncommitted changes to tracked files, and a new file once `git add`
has staged it, without touching them; with nothing uncommitted, the archive is `HEAD`. Either way
it holds the files the commit would, with LF endings and none of the working tree's ignored
folders. Open a new session in the `check` folder, from that shell.

**To try the Python library template**, before a release that changes it, `scaffold.py` or
`init-python-library`, build a copy of it under `$K`, in that throwaway shell: nothing else
catches a broken build. From the repository's root:

```bash
R=$(pwd)
uv run --no-project python .apm/skills/init-strategy/scripts/scaffold.py python-library "$K/lib"
cd "$K/lib"
uv sync
uv run ruff check . && uv run mypy && uv run pytest
uv run --no-project python "$R/.apm/skills/bloom-code-lint/scripts/bloom_code_check.py" . --max-line-length 120
uv run sphinx-build -W -b html docs/source docs/_build/html
uv build
```

Then the same in a second copy, `$K/lib2`, first named with the longest name it accepts by its
`scripts/name_library.py`, run as the `init-python-library` skill runs it. Every check passes there
too, and this prints nothing:

```bash
git -C "$K/lib2" grep -n -e kn_python_library_template -e kn-python-library-template -e KnPythonLibraryTemplate -e "KN Python Library Template" -e "KaxaNuk SC" -- ':!AGENTS.md'
```

**Before a release, `tools/install_check.py` makes the install above** on an archive of the commit,
and `tools/release.py` runs it:

```bash
uv run --no-project python -I tools/install_check.py
```

It checks a project-scope install for Claude: every skill, command, rule and agent the package
holds, today 27, 9, 3 and 1, deployed with no warning. Then a user-scope install in a new home:
Claude, then Codex put on APM's list by `user_targets.py add`, then Codex, then `apm update -g`,
with each assistant holding what the package holds. Last, the deployed `scaffold.py` makes a
strategy, a researcher's home and the worked example from that install. It works in a folder of
its own that it removes, `kn-<random>`, with `HOME` and `USERPROFILE` inside it. On Windows that
folder is in your user folder: without long paths, an `apm_modules/` deeper than 57 characters
fails with `WinError 3`, as APM stages a package 68 characters below it, and the temporary folder
is too deep. `--github KaxaNuk/Researcher#dev` installs from GitHub instead, as a newcomer does;
`--migrate-from <owner/name#ref>` installs that older package first and moves from it as `update`
does.

**Then install it for the user twice by hand**, as the interview needs a person: from the archive,
each time from a new shell whose `HOME`
and `USERPROFILE` are a new empty folder under `$K`: once Claude, then Codex; once Codex, then
Claude.

- On the first assistant, install the package as `SETUP.md`'s step 2 does, with the archive in
  place of `KaxaNuk/KaxaNuk-Researcher`. Run `init-researcher` there, which runs `interview`, for a
  researcher whose name has an accent, *Sofía*: its home under `$K`, its files deployed as `sofia`.
  The archive installs as `_local/KaxaNuk-Researcher`, so wherever the files name
  `$HOME/.apm/apm_modules/KaxaNuk/KaxaNuk-Researcher/`, tell the assistant to read
  `$HOME/.apm/apm_modules/_local/KaxaNuk-Researcher/` instead.
- On the second, install the package and the home for it, as `SETUP.md`'s *another assistant* does,
  then update:

```bash
S="$K/KaxaNuk-Researcher/.apm/skills/init-researcher/scripts/user_targets.py"
uvx --from apm-cli==0.33.0 apm install -g "$K/KaxaNuk-Researcher" --target <the second assistant>
uv run --no-project python "$S" add <the second assistant>
uvx --from apm-cli==0.33.0 apm install -g "<Sofía's home>"
uvx --from apm-cli==0.33.0 apm update -g --yes
uv run --no-project python "$S" check claude sofia
uv run --no-project python "$S" check codex sofia
```

Both checks pass. On disk, `~/.claude/` holds the package's 27 skills and `sofia` in `skills/`,
9 commands, 3 rules and 2 agents, `blueprint-critic.md` and `sofia.md`; `~/.agents/skills/` the same
28 skills; and `~/.codex/agents/` 2 agents, `blueprint-critic.toml` and `sofia.toml`.

**If the release changes a skill, a command or a script**, walk the rest of the newcomer's path by
hand on each run's first assistant, once in Spanish and once on Codex, an assistant with no question
tool: `next`, `read` on one clipping, a round of `philosophy` at Starter and one on how you work,
`brief setup` and `brief`, and `init-strategy`; and `init-python-library`, with `next` in the folder
it makes, `workshop` on one session, *Bootcamp S03*, and `known-answer` on one recipe, beside the
strategy `init-strategy` made, when the release changes them.

**When it changes `init-researcher` or `interview`**, last, say `init-researcher` there again: it
asks `Another?`, and *Make a second one*, named *Sofia*, makes a second home under `$K` whose files
take a name other than `sofia`, with Sofía's untouched. Try a second researcher there and only
there, never beside your own.

Delete the scratch folder afterwards: under the throwaway home, nothing the walk installed or
scheduled reached your own. A newer APM is adopted only when these installs pass with it, on
Windows.

**Branches.** Work is committed on `dev`; `main` is what every user installs. When `dev` holds a
release, it reaches `main` by a fast-forward and the release is tagged there, as `AGENTS.md` says,
by one command:

```bash
uv run --no-project python -I tools/release.py
```

says what would be released, or why not; with `--go` it releases. It refuses, before anything is
pushed, unless `dev` is checked out with nothing uncommitted; GitHub's `dev` and `main` are both in
its history, or it names the commits to merge into `dev` first; `apm.yml`'s version opens the
`CHANGELOG.md`, its entry opens with a sentence and no tag has that version yet; the security check
finds nothing to fix; and `tools/check.py` and `tools/install_check.py` pass. Then it pushes `dev`,
fast-forwards `main` to it, tags `vX.Y.Z` there with `X.Y.Z: <the entry's opening sentence>`, pushes
`main` and the tag, switches back to `dev`, and reads `main` and the tag back from GitHub to confirm
both name the release's commit. A step that fails after the first push says what was done and what
is left.
