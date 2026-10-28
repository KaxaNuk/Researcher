---
name: how-we-work
description: >
  Load this skill whenever work in a KaxaNuk repository is about to be committed, branched, merged,
  versioned or released. Use it when the user asks where work lands, how to name a branch, what to
  check before a commit, how to write a changelog entry, which version number a change takes, or
  how to publish a release. It covers where work lands — on `main`, a branch only when a review
  is wanted — the `issues/<number>` branch name, the checklist before a commit and which saves
  made on the owner's go skip it, the changelog format and Semantic Versioning as KaxaNuk applies
  it. It does NOT cover the research process itself (use `experiment-lifecycle`) or Python style
  (the `python-bloom-code` and `python-pep8` instructions).
metadata:
  version: 0.6.1
---

# How we work — issues, branches, changelogs, versions

The same procedure in every KaxaNuk repository, so nobody has to explain it before sharing a tool.
Fewer meetings, more commits with their reasoning attached: a change that carries its changelog
entry is reviewable at any hour; a change proposed in a call is not.

## 1. Work lands on `main`

Work is committed on `main`: small commits whose messages say what moved and why, each
change-set with its `CHANGELOG.md` entry and its version bump. An issue, a branch and a pull
request are tools for a change you want a second pair of eyes on, or for two lines of work that
must not mix — never a gate. Nobody opens an issue to fix a sentence.

When you do want them:

1. **Open the issue.** State the question or the problem, not the solution.
2. **Cut the branch** from `main`: `git switch -c issues/<number> main` — `issues/27-B` and
   `issues/27-C` for a second attempt or a parallel line of work on the same issue.
3. **Work**, committing against the issue.
4. **Open the pull request into `main`**, and delete the branch once it is merged or abandoned:
   `main` is the only branch that stays.

A long-lived branch other than `main`, such as a deployed `dev`, exists only where a repository's
`AGENTS.md` or `README.md` says so: read its rule before merging into one.

## 2. Before any commit to `main`

- **The linter passes.** For Python, `uvx ruff check .`, notebooks included; the repository's own
  configuration decides the rules.
- **A notebook's outputs are never committed.** The committed notebook is the method; the record
  lives in a document. A marimo notebook, as a KaxaNuk strategy's are, saves none in itself, so
  there is nothing to strip; its cache, `__marimo__/`, is ignored. A Jupyter notebook in another
  repository has its outputs stripped first.
- **The `CHANGELOG.md` entry is part of the change-set**, not a follow-up. If you cannot write the
  entry, the change-set is not finished.
- **No secrets, no binaries.** Nothing from a `.env` file, no keys in a notebook output or a log
  line, no charts, workbooks or PDFs unless the repository explicitly keeps them. Before a push,
  the `security` skill's check finds nothing to fix in the folder.
- **Code is written in English** — names, docstrings, comments and commit messages — whatever
  language its owner speaks, and so are folder and file names and every heading or label a skill
  or a tool reads by name. A repository's prose documents — a strategy's `OBJECTIVE.md`, its
  blueprints, journal entries and notes, a library's guides — are in its owner's language, unless
  its `AGENTS.md` names one language for the team; a source's terms and quotes stay as written.
- **If a published number or a public interface moved, the commit message says which** — the
  pull request too, when there is one — and the documents that cite it changed in the same
  change-set.

**A version saved on the owner's go is not a change-set.** At a researcher's home, the versions its
skills save take no changelog entry or version bump. In a strategy, a document the researcher
writes on the owner's go — a note, `OBJECTIVE.md`, `BLUEPRINT_N.md`, a `JOURNAL_N.md` entry, a
line in `Bibliotheca/LOG.md` — is saved as its own version on that go, with no `CHANGELOG.md`
entry, version bump or ruff gate. The next change-set's entry names it. The blueprint is saved
alone, before any rule is coded.

## 3. The changelog

One entry per change-set, newest first:

```
## X.Y.Z (YYYY-MM-DD)

**One sentence saying what a reader has to do differently.**

### Added
### Changed
### Deprecated
### Fixed
### Removed
```

A repository whose `CHANGELOG.md` names another format in its header keeps it: the KaxaNuk
Researcher's own root `CHANGELOG.md`, the KaxaNuk Data Curator's and that of a Python library
made with `init-python-library` use Keep a Changelog, `## [X.Y.Z] - YYYY-MM-DD`. Every strategy
made from the template, and every researcher's home, uses the one above.

Each item is written for somebody who was not in the room: **say what moved and why, not what file
you touched**. "The regime model lives in the Refinery so a penalty sweep costs no download" is an
entry; "updated custom_calculations.py" is a diff. Name anything that invalidates a number or breaks
a caller, and say which. A removal is a change-set too.

## 4. Version numbers

[Semantic Versioning](https://semver.org/spec/v2.0.0.html), read for what the repository's users
actually depend on:

| Repository kind | MAJOR | MINOR | PATCH |
| --- | --- | --- | --- |
| **A library** (public API) | a caller has to change code | new capability, callers untouched | a fix; nothing observable changes except the bug |
| **A research repository** (results and the pipeline) | published results are invalidated and must be re-derived | a new experiment, signal, stage or document; existing results stand | tooling, documentation, hygiene; no result changes |
| **An APM package** (AI primitives) | a skill's contract or a file name changes so a consumer must re-read | a new skill, prompt or instruction | wording, references, fixes with the same contract |

Three conventions follow. A result or contract that changes is MAJOR even if the diff was one line —
severity is what a reader has to throw away, not the size of the diff. Re-running a pipeline on
refreshed data is not a bump. While on `0.x`, a breaking change bumps MINOR, and `1.0.0` is reserved
for the first version somebody outside the team depends on — for a research repository, its first
book on paper trading, its results reproduced from a clean clone.

## 5. Releasing

1. Bump the version where the repository keeps it — `pyproject.toml`, `apm.yml`, or both, or the
   package's `__init__.py`, as a Python library laid out like the KaxaNuk Data Curator keeps it —
   in the same commit as the changelog entry. Run `uv lock` where the repository commits a
   `uv.lock`.
2. Tag on `main` once the version's commit is there, and push the tag:

   ```bash
   git tag -a vX.Y.Z -m "X.Y.Z: <the entry's first sentence>"
   git push origin vX.Y.Z
   ```

   One tag per release, `v` and the version the repository declares at its root: the KaxaNuk
   Researcher tags its package's, while its templates, example and home keep their own numbers.
   The message is the version and the first sentence of its `CHANGELOG.md` entry, word for word.
3. **Tag the commit where the version became the state of `main`** — when a branch was used, the
   merge, not the commit on the branch that wrote the bump: a tag cannot be corrected in place once
   somebody has pinned to it.
4. For a package published to an index, the release job builds from the tag, never from a working
   copy.

## 6. Two things never to do

- **Never rewrite pushed history on a shared branch.** Fix forward with a new commit; the exception
  is a branch only you have ever pushed.
- **Never print a secret to find out whether it is set.** Check for its presence, report *set* or
  *missing*, and stop there. An exposed key is rotated, not edited out of a file: the `security`
  skill's *A key leaked* walks through it.
