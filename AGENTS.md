# Agents — how this repository is changed

This repository is the KaxaNuk Researcher: one APM package that carries every KaxaNuk skill,
instruction and command in `.apm/`, with its one agent, `blueprint-critic`, and the starting points
its `init-*` skills copy: `templates/strategy/`, `templates/researcher/`,
`templates/python-library/` and the worked examples, one folder each under
`examples/<kind>/<name>/` — today one, `examples/strategy/golden-flow/`. Read this before changing
anything. The rules a researcher works by in its home are in `templates/researcher/AGENTS.md`, a
strategy's in `templates/strategy/AGENTS.md`, and a Python library's in
`templates/python-library/AGENTS.md`. This file is about changing the package.

## What lives where

| Path | What it is | Changed how |
| --- | --- | --- |
| `.apm/skills/`, `.apm/prompts/`, `.apm/instructions/`, `.apm/agents/` | every skill, command, instruction and agent an install receives: the researcher's, the process's (`experiment-lifecycle`, `alpha-decomposition`), each Lab library's, the house rules and `blueprint-critic`, deployed for the user with the skills | edited here, then tried by a project-scope install of an archive of the tree, from a scratch folder in a shell whose home is a throwaway folder, and a new session there, as `CONTRIBUTING.md`'s *Development* shows; before a release, that install deploys exactly the counts given there, with no warning. Never `apm install -g <this folder>`: on Windows it stages the whole working tree, ignored folders included, past the path limit under HOME |
| the skills' `scripts/` | `scaffold.py`, `name_library.py`, `user_targets.py`, `extract.py`, `check_numbers.py`, `bloom_code_check.py`, `security_check.py`, and the library's tools beside `extract.py` — `unread_sources.py`, `check_library.py`, `render_pages.py`, `ocr_pdf.py`, `update_concept_pages.py`, and `library.py`, which the first, second and fifth import: what `init-*`, the install in `SETUP.md`, `interview`, `next`, `update`, `read`, `audit`, `bloom-code-lint`, `security` and `backup` run for every user. `security_check.py`, in `security`, reads a folder for what should not leave the computer and never prints a value. `read`'s `SKILL.md` names every one of them, and the home's `AGENTS.md` says what each is for. `user_targets.py`, in `init-researcher`, puts the assistant in use on APM's list in `~/.apm/apm.yml`, checks the researcher's files for it, and finds and renames to `<name>-mine` the user's own skills, commands and agents that keep the package's of the same name out; an assistant missing from that list loses its files to the next install or update without `--target`. A script also works under `python -I`, as a researcher runs it where `python` is not on the PATH — `uv run --no-project python -I` — which ignores `PYTHONIOENCODING` and leaves the script's folder off the path: it reconfigures its output to UTF-8, and puts its own folder on the path before it imports a neighbour | `tests/` tests them, and `tools/check.py` runs the tests; a change carries its test there. Before the commit, also try it by running the skill that uses it in a scratch folder — `user_targets.py` in a shell whose home is a throwaway folder, never against the real `~/.apm`; the library's tools and `security_check.py` on a small fake home and strategy, with names that hold commas, parentheses and accents, never on a real library; `security_check.py` also on planted fake keys, never on a real one, and a test builds each fake key from pieces, so no file holds one whole |
| `.apm/skills/experiment-lifecycle/references/` | the experiment documents and notebook, as the example's with its own lines stripped | by hand, in the same commit as the example's change |
| the `Bibliotheca/` index and log, the drivers, modules, notebooks and experiment and paper-trading files in `templates/strategy/` | the example's with its own lines stripped | by hand, in the same commit as the example's change |
| `templates/strategy/` | the KaxaNuk Strategy Template, copied into every new strategy | a change here is a template release: its `pyproject.toml`, which declares its version, and `CHANGELOG.md` move together |
| `examples/strategy/golden-flow/` | one strategy worked through the template | the same; it commits no `uv.lock`, so its library versions resolve when `uv sync` runs |
| `templates/researcher/` | the researcher's home, copied by `init-researcher` | its `apm.yml` version leads its `CHANGELOG.md`; `update` compares a home against it |
| `templates/python-library/` | the KaxaNuk Python Library Template, laid out like the KaxaNuk Data Curator, <https://github.com/KaxaNuk/Data-Curator>: copied by `init-python-library`, then named by its `name_library.py`, which only puts in the names, the holder and the one sentence the owner chose, and moves the package folder | a change here is a template release: the number in the first sentence of its `CHANGELOG.md`'s `## [Unreleased]` entry, *Started from the KaxaNuk Python Library Template X.Y.Z*, moves, and the root `CHANGELOG.md` says what changed; the rest of its `CHANGELOG.md`, and its `__version__`, 0.1.0, are the new library's own. A placeholder changed here changes `name_library.py` in the same commit, a change to its dependency groups updates `TOOL_DISTRIBUTIONS` and `TOOL_IMPORT_NAMES` there, and a change to its first-commit message, in `scaffold.py`'s `STARTING_POINTS`, updates `FIRST_COMMIT`. Ruff and the Bloom Code check, at 120, run in place; `uv sync`, the tests, the documentation and `uv build` only in a copy outside the repository, as `CONTRIBUTING.md` shows |
| `assets/readme/` | the README's images, drawn as SVG by hand: text, never a binary, each with its alt text and its `<title>` and `<desc>` | edited here; a picture of the package shows it as it is, and changes in the release that changes what it shows |
| `tools/`, `tests/` | the harness: `check.py`, every check a commit passes; `install_check.py`, the install a release is tried with; `release.py`, the release itself; `lab_versions.py`, each Lab library's newest release on GitHub against the package's record, which `release.py` shows and a weekly task runs; the tests of the skills' scripts and of the tools | edited here, never installed: APM deploys only `.apm/`. `tools/parity_exceptions.json` is written by `check.py --record-parity` only, after each difference it records has been read |

**The strategy template and the example share every file the example does not mark.** A change to
the template's description of a file changes the example's copy in the same commit. Only the lines
between `<!-- example: begin -->` and `<!-- example: end -->` — `# --- example: begin ---` and
`# --- example: end ---` in Python, a marimo notebook included — are the example's own; every other
line is the same in both copies. A marker stands alone on its line, at column 0. The only
exceptions are the example's status banner in `AGENTS.md`; the `init-example` lines of `SETUP.md`;
the body of `OBJECTIVE.md`; the entries of `CHANGELOG.md`; the name and version in
`pyproject.toml`; and, whole, the example's `README.md` (its own, as a strategy's is after
`SETUP.md` step 5), its seed CSV and every file only the example has — its notes and
`Universe/seed.py`. An example with a book on paper adds that book's `FREEZE.json` and the files it
hashes; `golden-flow` has one, `Paper_Trading_1`, on probation from 2026-10-27, whose seed copy
keeps tickers and dates only. `paper_trading_N.py` stays shared and marked.

## Rules

- **A file of a starting point is never written from memory** — not by a skill, not by the script,
  not by an agent helping here. `scaffold.py` copies byte for byte; `name_library.py` then only puts
  the owner's names and words into a Python library's copy.
- **No Lab library's code in the package.** A skill is written from the library's documentation,
  changelog and runs, never from its source, a wheel's contents, a clone or a source page its
  documentation site links to. It names only the public API: no private module, internal class,
  tolerance or copied pattern, and no account of which branch runs inside. A run settles any
  difference between the documentation and the library, and the skill then says *checked on
  <build> by running it*. The same holds for an agent helping here, and nothing of the Analytics
  Factory's files or KaxaNuk's research is copied into the package.
- **The onboarding and the first read are frozen**, as the package's owner approved them on
  2026-10-10, at 1.10.2. `ONBOARDING.md` is that run, step by step. `FROZEN.json` fingerprints it
  and the files that make the run: `SETUP.md`, `init-researcher`, `interview`, and `read` with its
  note convention, reading map and extractor. The home template, `templates/researcher/`, and the
  `philosophy` skill's `references/questions.md` stay free, by the owner's choice. A frozen file
  changes only when the owner asks for that change in words, never as the side effect of another:
  a sweep, a rename, a rewording, a version bump. Show the change against `ONBOARDING.md` first; on
  the owner's go, move its fingerprint in `FROZEN.json` in the same commit, update `ONBOARDING.md`
  where the run changes, and say so in the `CHANGELOG.md` entry. When the frozen-files check names
  a file, revert it or show it to the owner; never move its fingerprint to make the check pass.
- **Every change carries its `CHANGELOG.md` entry** and a version bump, in the same commit: in
  `apm.yml` for the package at the root and for the home, in `pyproject.toml` for the strategy
  template and the example, and in the *Started from* sentence of the Python library template's
  `CHANGELOG.md`. The entry opens with one plain sentence a newcomer understands; the researcher's
  weekly word on a new version quotes it. Its *What to do differently* says what the owner says
  (*say `update` in your home*), never the `apm` command `update` runs for them. Once the release's
  commit is on `main`, tag it `vX.Y.Z` with the message `X.Y.Z: <that sentence>`.
- **Work lands on `dev`; a release reaches `main`.** This repository keeps two branches, the
  long-lived `dev` the `how-we-work` skill allows where a repository says so. Every change is
  committed on `dev`, with its `CHANGELOG.md` entry and its version, as above. `main` is
  production: `apm update -g` installs it as it stands, so it receives `dev` only when a release is
  ready, by a fast-forward, `git merge --ff-only dev`, never by a pull request on GitHub, which
  would delete `dev` once merged; then the release is tagged on `main`. `tools/release.py --go`
  makes the release, never git commands typed by hand: it refuses while anything is uncommitted,
  while GitHub holds commits `dev` lacks, while a check or the install fails, or while the version
  is tagged already, and once it pushes it reads `main` and the tag back. A branch for a change you
  want reviewed, `issues/<number>`, is cut from `dev`, goes back into `dev` and is deleted once
  merged. `main` and `dev` are the only branches that stay, and GitHub refuses to delete either or
  force a push onto it.
- **Every KaxaNuk skill lives here.** A skill for a new Lab library is a folder in `.apm/skills/`.
  A change to a library's API changes its skill in the same release, and the worked example where
  it uses that library, with a new example version and a journal entry, re-run where a figure
  moves.
- **A new starting point** is built as `python-library` is: a folder under `templates/` that
  `scaffold.py` copies, a kind in its `STARTING_POINTS`, and an
  `init-<kind>` skill that runs it as `init-strategy` does. A copy that takes names gets them from a
  script of that skill's that only puts them in, as `init-python-library`'s `name_library.py` does.
  Its `AGENTS.md` names it in a marker line that survives its setup,
  `<!-- kaxanuk-starting-point: <kind> -->`, alone at column 0, and carries a `## Next` table,
  *Done when* and *The next thing*, that `next` reads for any kind but a strategy. No folder in it
  is named `Bibliotheca/`: that word is a strategy's only, and every skill that finds one reads the
  folder that holds it as a strategy.
- **A fork changes every line that names the package's repository**, `KaxaNuk/Researcher`, and its
  former name, `KaxaNuk-Researcher`, in either case —
  `git grep -i -e kaxanuk/researcher -e kaxanuk-researcher` finds them, `scaffold.py`'s
  `INSTALLED_PACKAGE_PATHS` included — and installs as the one researcher package on its user's
  machine. Two packages with skills or commands of the same names do not share a user: a `-g`
  install of the second replaces a same-named skill of the first, with a warning, and overwrites a
  same-named command silently. The last install wins.
- **`tools/check.py` passes before any commit**: ruff, the Bloom Code check, the frozen files, the
  template and the example in step, the Markdown rules below, the versions, the private words and
  the tests, as `CONTRIBUTING.md`'s *Development* shows, and `tools/release.py` runs it again before
  anything reaches `main`. There is no CI.
- **Markdown you write or change is wrapped at 100 columns**, with no literal tab and LF line
  endings. A line inside a fenced code block, a table row, a line carrying a URL, the YAML
  frontmatter at the top of a file and a line copied verbatim from a strategy's fixed or
  append-only record — a blueprint, a journal entry, a registered gate section — may run longer.
  Never use the section symbol; write "section".
- **No secrets, no binaries.** The worked example, `golden-flow`, is the only strategy this
  repository names, as a curated copy; nothing in it is taken from a live strategy repository after
  the copy. It was curated again from the live repository once, on the owner's word of 2026-10-27,
  Experiment 1 only; another curation takes the owner's word again.

## When a Lab library or an Analytics Factory file changes

`tools/lab_versions.py` names a library whose newest release the package's record lacks: it reads
each library's changelog on GitHub, never its code. `release.py` shows its report, and a task on
the owner's computer runs it every Monday.

1. **Read the library's changelog** from the build its skill names as `library_version` to the new
   one, `[Unreleased]` aside: what changes for the install, a caller, a key or a trap. Read its
   documentation too, never its code. Copy names and behaviour only; a private index, host or key
   stays a `{SERVER}` placeholder.
2. **Record the new build** in the *Latest* column of
   `.apm/skills/next/references/investment-lab.md`, which `next`'s weekly check in a strategy
   compares the installed builds against. In the library's skill, add a short *Changed in
   <build>* paragraph from its changelog, not yet checked by a run.
3. **Check it by a run** before `library_version` moves. In a scratch copy of the worked example, on
   a short path outside this repository, with the new build: re-check every line that says
   *checked*, *verified* or *measured on <old build>*
   (`git grep -n "<old build>" .apm templates examples`), and re-run the example from a wiped copy.
   Only then does `library_version` move and the paragraph become the skill's own text.
4. **One release carries it all**: the skill and its `references/`, `investment-lab.md`, the
   template's `pyproject.toml` floor or `Config/.env.template` key with the example's copy, and,
   where a figure moves, a new example version with its journal entry, `FINDINGS_1.md` and
   `RESULTS.md`, and every skill that quotes the figure. The CHANGELOG's *What to do differently*
   names the build to install.
5. **An Analytics Factory change** — a folder, a file name, a header, a date order — changes
   `Data/hand_supplied.py` in the template and the example (which keeps reading the older names),
   `attribution-analysis-runs` and `investment-lab.md`; a frozen book's copy, as `golden-flow`'s
   `Paper_Trading_1`, stays as it was.
6. **A library that replaces a hand-rolled stage** (the Data Refinery, the Data Analyzer) gets its
   own `*-runs` skill with a `library_version`, and the stage's seam file, `experiment-lifecycle`
   and `investment-lab.md` move with it.
7. **The worked example's seed follows its index.** When the KN US Equity Core's membership changes,
   rebuild `examples/strategy/golden-flow/Universe/Investable_Universe.csv` with its
   `Universe/seed.py`: every listing the index held, departed names included, by Sharadar's ticker,
   which is the index's own, with its first and last price dates in Sharadar's catalogue — the
   columns `main_identifier`, `index_identifier`, `valid_from` and `valid_to`, never a name, a
   permanent identifier or any other vendor field. It is an example release, re-run where a figure
   moves. An example with a frozen book, as `golden-flow` with `Paper_Trading_1`, keeps that
   book's seed as it is, tickers and dates only; never restore a hashed original to satisfy its
   `FREEZE.json`.
8. **A new worked example** — an ETF strategy, or one users ask for — is a folder of its own,
   `examples/<kind>/<name>/`, where `<kind>` is the template it is worked through, as
   `templates/<kind>/` names it: `examples/strategy/<name>/` for an ETF strategy. It is curated as
   `golden-flow` is: the template's shared lines, its own marked lines, a seed of tickers and dates
   only, and its own version and changelog. `init-example` offers it with nothing registered:
   `scaffold.py` finds every folder `examples/<kind>/<name>/` that holds a `README.md` and shows,
   for each, the line its README marks, `<!-- kaxanuk-example: <one line> -->` alone at column 0,
   or else its first paragraph's first sentence. Write that line so a newcomer choosing an example
   learns what it shows.
