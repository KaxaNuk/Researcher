# Changelog for KaxaNuk-Researcher

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases are
tagged `vX.Y.Z`.

## [1.26.0] - 2026-10-27
The worked example, Golden Flow, now shows a strategy done correctly that earns only in some
markets, and every strategy's notebooks are marimo.

**What to do differently:** say `update` in your home. A strategy you have already made keeps its
own files; `init-strategy` starts a new one from the new template, and `init-example` gives a fresh
copy of Golden Flow.
### Changed
- **The graduation gate has two layers** (`paper-trading-gate` 0.5.0, the template's findings,
  `BITACORA.md` and `promote.py`). Soundness first: no survivorship bias, no look-ahead, no
  overfitting, costs and capacity stated, reproducible from emptied data folders, each row with its
  evidence. Then performance, the former criteria 1 to 3. Three outcomes: **graduates**, frozen and
  paper traded; **sound and regime-dependent**, its findings naming where it earned and where it
  failed, which may go to paper **on probation** on the owner's sign-off — its regime prediction,
  at least 12 months and its review registered before day one, read against its index and its
  control, paper alone never sending it to production — or be paired with another signal in a
  later experiment, or used at a portfolio manager's discretion, theirs to decide; **not sound**, no
  conclusion drawn.
- **The strategy template 0.20.0** adopts the proposals of issue KaxaNuk/Researcher#41: marimo
  notebooks and no Jupyter; Sharadar in the curator; the adjustment rebuilt from the exact close;
  every per-security file in Parquet through `Data/time_series.py`; every cost and the cash inside
  the engine; a Verify that excludes a truncated run by name; the band read back beside the rule;
  and a new experiment's signal on data already downloaded as an `r_*` refinery calculation.
  `experiment-lifecycle` 0.15.0 and its references follow, its section contract the notebook's.
- **The worked example, Golden Flow 0.18.0**, is curated again from its live repository at 0.21.0,
  Experiment 1 only, on the owner's decision of 2026-10-27, which sets aside once `AGENTS.md`'s
  rule that nothing is taken from a live strategy after the copy: Sharadar from 1998, a monthly
  rule, every cost inside the engine. Its Experiment 1 reads as sound and regime-dependent;
  `Paper_Trading_1`, the earlier FMP book, leaves it; its seed holds tickers and dates only. Its
  step 6 needs Attribution Analysis 0.5.0.
- **The Lab's skills follow it**: `universe-point-in-time` 0.4.0 and `data-analyzer-runs` 0.3.0;
  `data-curator-custom-calculations` 0.7.0, its `library_version` 0.51.0, checked by Golden Flow's
  run of 2026-10-24 from emptied data folders; `backtest-engine-runs` 0.5.0, its `library_version`
  0.67.0, with the batch mode and the costs and the cash in the engine;
  `portfolio-construction-runs` 0.6.0, with the band; `attribution-analysis-runs` 0.6.0, its
  `library_version` still 0.2.0, since Golden Flow ran 0.5.0 from the library's repository, not a
  release; `alpha-decomposition` 0.5.0, with the example's new figures. `blueprint`, `challenge`
  and `blueprint-critic` name the marimo notebook, the band read back and the two-layer gate.
- **`known-answer` 0.2.0** writes a marimo notebook, `known_answer_marimo.py`, in place of a
  Jupyter one: the owner opens it in marimo's editor to read every figure, or runs it as a script,
  which shows whether Verify passed and exits 1 on a raise. Tried end to end on recipe 1, the
  AR(1)'s half-life, with marimo 0.25.2: it passed, raised once the method's intercept was dropped,
  and left both folders unchanged.
- **`bloom-code-lint` 0.3.0**: the checker skips a marimo notebook, whose cells marimo generates.
  `scaffold.py` leaves `__marimo__/` out of a copy, and `tools/check.py` runs ruff without a cache.
- `init-example` 0.5.4, `init-strategy` 0.4.4, `how-we-work` 0.6.1, `next` 1.10.2, `query` 0.10.1
  and `philosophy` 1.3.6 carry the marimo names and the two-layer gate, and move the versions 1.25.0
  left behind. The example notebook's verdict cell says how the table it prints, numbered as the
  gate the run was registered under, maps onto the two layers.
### Removed
- **`.githooks/pre-commit`**, on the owner's word: `tools/release.py` runs every check, the tests
  and the install before anything reaches `main`, and a hook guarded only a clone that set it up.
  `AGENTS.md` and `CONTRIBUTING.md` say to run `tools/check.py` before a commit.

## [1.25.1] - 2026-10-27
Your researcher's own skill now knows the package's new address too, and `update` brings it.

**What to do differently:** say `update` in your home; `next` reminds you, as your researcher's
skill is now behind the package.
### Changed
- **`interview`**, the researcher's skill template: 0.5.2. Its *which version are you?* reads the
  package's lock entry under `kaxanuk/researcher` or the former `kaxanuk/kaxanuk-researcher`, and a
  command on an assistant with none is read under the new folder, as 1.25.0 left them, so `update`
  writes a home's skill again, its owner's own lines kept. A frozen file, changed on the owner's
  word of 2026-10-27 to finish the move; its fingerprint in `FROZEN.json` moves with it.

## [1.25.0] - 2026-10-27
Your researcher now installs from the package's new address on GitHub, KaxaNuk/Researcher, and
moves an older install there when you say `update`.

**What to do differently:** say `update` in your home: it moves the package to its new address,
asking first. Nothing else changes, and a researcher installed before keeps working until then.
### Changed
- **The address**: the package's repository on GitHub is now `KaxaNuk/Researcher` (the former
  `KaxaNuk/KaxaNuk-Researcher` redirects there). Every link, install line and lookup names it:
  `README.md`, `SETUP.md`, `CONTRIBUTING.md`, `ONBOARDING.md`, the home, strategy and Python
  library templates, the worked example, and the skills and commands that read the package's
  newest tag and changelog on GitHub. `apm.yml`'s `name:`, `kaxanuk-researcher`, is unchanged.
- **Where the package is found**: a new install lands in `~/.apm/apm_modules/KaxaNuk/Researcher/`.
  `scaffold.py`'s `INSTALLED_PACKAGE_PATHS`, the files `SETUP.md`, `init-researcher`, `interview`,
  `next`, `philosophy`, `blueprint`, `challenge` and `update` follow, and the home's `AGENTS.md`
  look there first, then under the former `KaxaNuk/KaxaNuk-Researcher/`, which an install from
  before 1.25.0 keeps until `update` moves it; a lock entry's `repo_url` is matched under either
  name.
- **`update`** moves an install under the former address: the assistant in use put on APM's list,
  the former package uninstalled and `KaxaNuk/Researcher` installed for every assistant on the
  list, the home's own package left installed. `tools/install_check.py --migrate-from` tries that
  move: from 1.23.2 under the former name, both assistants held every file afterwards and nothing
  of the former package was left.
- **The frozen files**, on the owner's word of 2026-10-27, to clean the onboarding while keeping its
  flow and its questions: `SETUP.md`, `init-researcher` with `user_targets.py`, `interview` and
  `ONBOARDING.md` take the new address and name the former folder; their fingerprints in
  `FROZEN.json` move with them.
- **`AGENTS.md`**: a fork changes every line naming `KaxaNuk/Researcher` or `KaxaNuk-Researcher`.
- **The home template** 0.32.1, **the strategy template** 0.19.5, **the worked example** 0.17.9
  and **the Python library template** 0.1.3 carry the new address.
### Fixed
- **`check_library.py`** (`audit`): a link written in angle brackets to a web address,
  `[x](<https://…>)`, is no longer reported as a broken link.
- **`check_numbers.py`** (`read`): a note saved with a byte order mark keeps its frontmatter, and a
  figure in code fenced with tildes is no longer checked as the note's own.
- **`bloom_code_check.py`**: the report stays in ASCII when a path holds a character the console
  cannot write, `Łucja` written `\u0141ucja`, instead of stopping with `UnicodeEncodeError`.

## [1.24.0] - 2026-10-27
Every release of your researcher is now tested and installed before it reaches you, by checks the
package runs on itself.

**What to do differently:** nothing.
### Added
- **`tools/check.py`**: every check a commit passes, in one command, each `ok` or `FAIL` — ruff, the
  Bloom Code check, the frozen files, the strategy template and the example in step with the
  exceptions `AGENTS.md` lists, the Markdown rules on the lines added since `origin/dev`, each
  version against its CHANGELOG and against the last release's tag, the private words of
  `.git/info/private-names.txt`, which no clone shares, and the tests. `--fast` leaves the tests
  out; `--record-parity` records `SETUP.md`'s `init-example` lines in
  `tools/parity_exceptions.json`, once each has been read.
- **`tools/install_check.py`**: the install a release is tried with, from an archive of the commit
  or, with `--github`, from GitHub — project scope for Claude, user scope for Claude then Codex,
  and the deployed `scaffold.py` making a strategy, a home and the example — each counted against
  what the package holds, in a throwaway home it removes. On Windows that home is in the user's
  folder: APM stages a package 68 characters below `apm_modules/`, so the temporary folder is too
  deep for the 260-character limit. `--migrate-from` tries a move from an older package.
- **`tools/release.py`**: the release from `dev` to `main`. It refuses until nothing is
  uncommitted, GitHub's `dev` and `main` are in `dev`'s history, the version opens the CHANGELOG
  with a sentence and has no tag, the security check finds nothing to fix and both tools above
  pass; then, with `--go`, it pushes, fast-forwards, tags and reads `main` and the tag back from
  GitHub.
- **`tests/`**: 267 tests of the skills' scripts and of the tools, by pytest, which
  `tools/check.py` runs, every fake key in them built from pieces; five strict xfails each mark a
  bug the tests found. And **`.githooks/pre-commit`**, which runs `tools/check.py --fast` before
  each commit once a clone sets `git config core.hooksPath .githooks`.
### Changed
- **`AGENTS.md`** and **`CONTRIBUTING.md`**: the checks, the install and the release name these
  tools in place of the commands typed by hand; the skills' scripts have tests, and a change to one
  carries its test.

## [1.23.2] - 2026-10-27
The README now opens with how to install your researcher, right under its first paragraph.

**What to do differently:** nothing.
### Changed
- **`README.md`**: *Install — three steps, no coding* follows the opening paragraph, with a line
  pointing to *What it is, and what it is not*, which says where what it reads goes. The picture,
  the two examples, *Why not just use Claude or Codex?*, *Take it with you* and *What it is, and
  what it is not* follow under a heading of their own, *What your researcher does*. The package and
  the Data Curator are called open source, no longer free.

## [1.23.1] - 2026-10-26
The README's install lines now give the repository's new address,
<https://github.com/KaxaNuk/Researcher>.

**What to do differently:** nothing. The old address still leads to the same repository.
### Changed
- **`README.md`**: the two lines to paste, to set up a researcher and to bring one back, name
  `https://github.com/KaxaNuk/Researcher`, and so does the licence badge. Every other mention of the
  old address stays for now.

## [1.23.0] - 2026-10-23
Your researcher now knows the Data Curator 0.51.0 and its new Sharadar provider, and what to work
around when a strategy uses it.

**What to do differently:** say `update` in your home. Before a strategy moves to Sharadar, ask
your researcher what 0.51.0 changes: a dividend or split column stops a Sharadar run for now.
### Changed
- **`data-curator-custom-calculations`** (0.6.0): a *Changed in 0.51.0* section, from the
  Curator's changelog — `main()` requires `data_block_providers`, `ExcelConfigurator` needs
  `data_blocks`, an older workbook is updated with `kaxanuk.data_curator update excel`, pyarrow
  26 or later, prefixes checked against the run's data blocks — not yet checked by a run of the
  worked example, so `library_version` stays 0.50.0. Beside it, what a strategy's Sharadar run
  measured on 2026-10-23: any `d_*` or `s_*` column stops the run
  (<https://github.com/KaxaNuk/Data-Curator/issues/39>); `c_daily_traded_value` is empty, with
  split-adjusted close times split-adjusted volume in its place
  (<https://github.com/KaxaNuk/Data-Curator/issues/40>); the startup subscription's key is served
  by `api.sharadar.com`, not Nasdaq Data Link, whose 429 locks the account. *Known provider
  faults* gains Sharadar's three-decimal prices and the rebuild of the adjusted close from the
  unadjusted close and Sharadar's `actions` table
  (<https://github.com/KaxaNuk/Data-Curator/issues/41>). `references/input-columns.md` adds the
  Sharadar page, what Sharadar fills and its tickers; `references/programmatic-run.md` the
  Sharadar call.
- **`next`** (1.10.1): `references/investment-lab.md` names Data Curator 0.51.0
  (2026-10-23) as the latest.
- **`workshop`** (0.4.2): the app is the Lab Platform, its new name, no longer the Investment Lab
  app; the Investment Lab is the whole product.

## [1.22.0] - 2026-10-23
Your researcher now makes interactive presentations from your own work with the new `deck` skill:
every claim cited, every figure quoted from its file, built with HyperFrames.

**What to do differently:** say `update` in your home. Then say `deck` and what you want to
present — a study, a strategy's results, your notes: your researcher asks the message and the
audience, shows the outline for your go, and builds the deck in a folder of its own.
### Added
- **`deck`** (0.1.0), a skill, so Codex has it too. It writes a `BRIEF.md` and an outline, slide by
  slide, from the files you name — a study, notes, a strategy's `OBJECTIVE.md`, `RESULTS.md` or
  `FINDINGS_N.md` — for your go, then builds the deck with HyperFrames' `slideshow` skill,
  <https://github.com/heygen-com/hyperframes>, open source: slides in a browser with reveals,
  branches and a presenter view, and a PDF to send. Every claim is cited in the presenter notes,
  every figure quoted from its file, never computed, a backtest's marked hypothetical; nothing
  that is not yours to show goes in without your go, and no slide advises. Node.js and `slideshow`
  are installed on your go, `slideshow` from HyperFrames' own source, never copied into the
  package. The deck lives in a folder of its own, beside your home unless you say otherwise; the
  `security` check runs before it leaves your computer, and `hyperframes publish`, which uploads
  it to HeyGen with a private link, runs only when you ask.
- **`README.md`**: `deck` in *You want to* and in *Every skill and command*.
### Changed
- **`CONTRIBUTING.md`**: the install deploys 27 skills.
- **The home template** (0.32.0): `AGENTS.md` names `deck` among the skills run by name.

## [1.21.3] - 2026-10-22
The README now shows, in one picture, what your researcher adds to a plain Claude or Codex.

**What to do differently:** nothing.
### Changed
- **`README.md`**, *Why not just use Claude or Codex?*: the table becomes a picture,
  `assets/readme/why-not-just-an-assistant.svg`, drawn by hand as the README's other pictures are:
  a plain assistant beside your researcher, row by row — your library, you, portability, KaxaNuk's
  knowledge and a method — with its alt text, `<title>` and `<desc>`.

## [1.21.2] - 2026-10-22
The README's investing example now shows how a strategy starts, with its objective, instead of a
backtest's result, and a table shows what your researcher adds to a plain Claude or Codex.

**What to do differently:** nothing.
### Changed
- **`README.md`**, *And when you invest*: you ask Arya how to build an investment strategy, Arya
  names the steps and starts with the objective, and your idea, stocks with a positive trend and
  rising profits, becomes two claims that `init-strategy` and `objective` put in `OBJECTIVE.md` on
  your go. The earlier example jumped to a backtest and its verdict, which read as a promise of
  results.
- **`README.md`**, *Why not just use Claude or Codex?*: a table, a plain assistant beside your
  researcher, row by row — your library, you, portability, KaxaNuk's knowledge and a method — in
  place of three bullets.

## [1.21.1] - 2026-10-22
Your researcher now names only the Investment Bootcamp among the Training Workshops; the others
join as each is published.

**What to do differently:** say `update` in your home.
### Changed
- **`workshop`** (0.4.1) names the Investment Bootcamp alone in its table of workshops. A workshop
  joins it once it is published; one the course map lists under `pillars` with `public: false` is
  not named or offered, and its sessions are not read. The starter sessions, `ai_role: doer`, work
  as 1.21.0 says, for any course that has them. Its examples say *Bootcamp S03*.
- **`known-answer`** (0.1.1) loads when a session of a KaxaNuk Training Workshop names it, and its
  recipes no longer cite a course for their numbers.
- **`CHANGELOG.md`**: the earlier entries name no workshop but the Bootcamp.

## [1.21.0] - 2026-10-22
Your researcher now walks you through a workshop's starter sessions, where it does the session's
task with you: you predict first, it builds, and you check every number.

**What to do differently:** say `update` in your home. Then, in a starter session, name it: your
researcher offers the deck's prompts in order, and does the task once you have made your prediction
and said go.
### Added
- **Starter sessions in `workshop`** (0.4.0): short first sessions for someone who starts from
  zero. `workshop` reads two keys of a
  session in the course map: `level: starter`, beside *beginner*, *intermediate* and *advanced*,
  and `ai_role`. With `ai_role: doer`, the new section *A starter session* applies: the deck's
  prediction with the AI off and its checkpoint stay held as before; the tutor offers the deck's
  ready prompts in order, word for word, for the owner to paste; on the owner's go, after their
  prediction, it does the task in the chat — the table, the chart, the note or the file the deck
  asks for — from the data the deck names, never invented; each figure is shown with its source,
  and the owner checks every number and explains it back. The file is written only where the owner
  says, the one exception to *Write a file*, and the task's figures are the one exception to *No
  figure of the tutor's own*. With `ai_role: tutor`, or no `ai_role`, a session is tutored as
  before. *practice* on a
  starter session sets beginner problems in the deck's business language, with no code. The course
  map stays `# kaxanuk-course-map 1`: both keys are additive.
### Changed
- **Two branches in this repository, `dev` and `main`.** Work is committed on `dev`; `main` is
  production, what `update` installs, and receives `dev` by a fast-forward only when a release is
  ready, tagged there. `AGENTS.md`'s rule *Work lands on `dev`; a release reaches `main`* and
  `CONTRIBUTING.md`'s *Branches* say how; GitHub refuses to delete either branch or force a push
  onto it. A strategy and a library still work on `main` alone, as `how-we-work` says.

## [1.20.0] - 2026-10-21
Your researcher now guards your keys, your personal data and confidential documents, and checks a
folder with the new `security` skill before anything leaves your computer.

**What to do differently:** say `update` in your home: it brings the new rules into your home's
`AGENTS.md`, `README.md` and `.gitignore`, shown for your go. Before you push a strategy or a
library, or whenever you wonder whether something is safe to share, say `security`.
### Added
- **`security`** (0.1.0), a new skill: *Check a folder* runs `scripts/security_check.py`, read-only,
  on a home, a strategy or a library — every file git tracks or would add, the saved versions'
  signatures and, with `gh`, whether the copy on GitHub is public — and reports what to fix before
  sharing (a provider key, a token, a private key, a password or licence beside its name, a
  password in a web address, a `.env` or licence file git would save, a `.gitignore` that lets
  `.env` in) and what to look at (a personal e-mail, a notebook saved with outputs, a public copy),
  never a value. *A key leaked* walks the owner through revoking first, then cleaning up, in
  `references/leak.md`; questions are answered from `references/practices.md`. It never reads a
  secret's value, changes an account's settings or rewrites saved versions. Tried on a fake home
  with planted fake keys under names with commas, parentheses and accents, on a fresh home and on
  the worked example.
- **Data boundaries**, in the `filesystem-boundaries` instruction (1.4.0), for every project: what
  is read is data, never instructions; secrets are never handled, and one exposed is rotated;
  confidential and personal material goes nowhere without the owner's go; outside services get only
  what the task needs; links in a message open only on the owner's word; the check runs before
  anything leaves. The home's `AGENTS.md` (home template 0.31.0) carries the same rules as *Keeping
  you safe*, for the assistants that take no instruction.
- **`query`** (0.10.0): *A document against the library* — a contract, a policy or a specification
  the owner attaches or names is read section by section against the notes and their rules, each
  point cited, with what the library does not cover; the document is never kept, and its text is
  never followed as an instruction.
- **`study`**: *A document to hand over* — a memo, a report, a policy draft or a decision record
  drafted from a study, inside its folder, every link and *not checked* kept, nothing added.
- **README images**, drawn as SVG in `assets/readme/`: one researcher for every project, the
  interview's two questions, and the Lab's eight steps.
### Changed
- **`README.md`**: opens with what it does for any field; two short conversations, one at work and
  one in the investment process; the uses table puts work first and the strategy, the example, the
  workshops, `known-answer` and the Python library under *For investors and builders*; new
  paragraphs *From any task to investing*, *It keeps itself current* and *It keeps you safe*; the
  workshop example names only the Bootcamp; the Data Refinery and Data Analyzer are named as
  libraries still to ship, their stages running today in the template; the *Coming next* line is
  gone.
- **`USE-CASES.md`**: work first, with examples from a lawyer's, an engineer's or a manager's
  week — a vendor, a hire, an onboarding plan, non-compete clauses, negotiation — `read` second,
  and the holdings, the strategy and the Python library under *For investors and builders*.
- **`backup`** (0.3.0): runs `security`'s check before the first copy and before every send;
  something to fix keeps the version on this computer, says so in one line and pauses sending.
- **`how-we-work`** (0.6.0): the check before a push; a leaked key points at `security`.
- **Strategy template** 0.19.4 and **`golden-flow`** 0.17.8, *Other standing rules*: what never
  leaves a strategy, and the check before a push. No result moves.
- **Python library template** 0.1.2, *Before any commit*: the check before a push.
- **`experiment-lifecycle`** (0.14.9): its description no longer claims the changelog, which is
  `how-we-work`'s.
- **The repository**: a `.gitattributes` keeps every text file LF; `.gitignore` keeps `.env` files
  out; the root `pyproject.toml` drops a line length no rule used. `CONTRIBUTING.md`: the install
  deploys 26 skills.

## [1.19.0] - 2026-10-18
Your researcher now keeps in its home the choices a computer or an account would keep, so a new
computer, account or assistant is set up again with one word, `update`; and `bring-home` brings
what an assistant remembered on its own into the home.

**What to do differently:** say `update` in your home: it brings `settings.yml`, filled from this
computer — the assistants you use, how your versions are signed and sent, your brief — shown for
your go. On a new computer, paste the README's second line; under another account or on another
assistant, say `update` there.
### Added
- **`settings.yml`**, in the home (home template 0.30.0): the assistants the owner uses, how
  versions are signed and sent, and the daily brief with the connectors it reads — never a key, a
  token, a password or a holding. Three skills write it, each its own part, on its own go:
  `backup`, `brief setup` and `update`.
- **`bring-home`** (0.1.0), a new skill: reads what the assistant in use remembered on its own —
  Claude Code's auto memory and user instructions, Codex's memories and `AGENTS.md`, Gemini's
  `GEMINI.md`, Copilot's instruction files; Copilot Memory and Cursor's rules pasted by the owner —
  for the folder the session is in, sorts each item as the home's *What is learned goes home* does,
  and writes the ones the owner picks into `RESEARCHER.md`, plan first. It never edits the
  assistant's memory, never opens another project's, a transcript, a credential or a settings
  file, and never brings a secret or a holding. The locations are from each assistant's
  documentation on 2026-10-18; Claude Code's layout was also checked on a computer that day.
- **A way back** (`SETUP.md`, on the owner's word): a second line to paste,
  *bring back my researcher from my private copy on GitHub*, which installs the package and
  follows `backup`'s *Step 10* — clone, then `update` — instead of making a new home. *Later*
  splits into *Another assistant* and *A new machine*. The README's *Install* gives the line.
### Changed
- **`update`**: *Step 2* reads `settings.yml` against this place — a home without the file gets
  it, filled from this computer; the assistant in use is added; each listed assistant missing here
  is installed for; the git settings the home's own git config lacks are set — a global e-mail,
  which a new computer's setup writes, does not count; a brief with no task here is scheduled again
  by `brief setup`, which follows with only its go; each connector the session lacks is named with
  its fix. *Step 4* gains item 6, *This place, from `settings.yml`*.
- **`brief`** (1.2.0): `brief setup` writes its choices to `settings.yml` and saves that file alone
  when they changed; saved choices that can all run here skip its questions, leaving only the go; a
  connector the file names and the session lacks is named. `brief` by name follows the file where
  nothing is scheduled, in place of *the choices are kept nowhere*.
- **`backup`** (0.2.0): `versions:` and `assistants:` go in `settings.yml`, saved and sent to the
  copy — a first copy too, whatever *Send?* chose, since its first send comes before the e-mail and
  that choice; *Step 10* clones and runs `update` in the same session, which sets the new computer
  up from the file, so the e-mail and *Send?* are asked again only when it leaves them empty.
- **`next`** (1.10.0): a new row 4, *this place matches `settings.yml`*, names `update`, or a
  connector to connect again after a new account; an empty value names nothing, so a new home
  passes, and the e-mail and sending choice count only in the home's own git config. Rows 4 to 6
  are now 5 to 7, and *setup: all good* counts all eight.
- **`README.md`**: *Take it with you* says `update` and the second line; *What stays behind* names
  the skills turned on in an account and `bring-home`; the skills table gains `bring-home`.
- **`CONTRIBUTING.md`**: the install deploys 25 skills.
- **Frozen files**, on the owner's word: `SETUP.md`, as above; `ONBOARDING.md`'s header gains one
  sentence saying so, its run unchanged, since a newcomer never reaches the new lines;
  `FROZEN.json` moves both fingerprints and names the change in its note.

## [1.18.3] - 2026-10-18
The README now says how your researcher moves to another Claude account, another computer or
another assistant, and what stays behind.

**What to do differently:** nothing.
### Changed
- **`README.md`**: *Take it with you*, after *Why not just use Claude or Codex?*: why the home
  moves, and what you do for another Claude account on the same computer, another computer and
  another assistant, each as the file that does it says — `brief setup`, `backup`'s *Step 10* with
  `update`, and `SETUP.md`'s *One researcher per person* — and what stays with an account.
  The bullet *You.* points to it, in place of *moving from Claude to Codex keeps all of it*.

## [1.18.2] - 2026-10-18
The changelog now dates 1.18.0 and 1.18.1 on the day they were released.

**What to do differently:** nothing.
### Fixed
- **`CHANGELOG.md`**: 1.18.0 and 1.18.1 read 2026-10-19; both were released and tagged on
  2026-10-18.

## [1.18.1] - 2026-10-18
`audit`'s library check no longer raises four more false alarms a real library showed: on a link
whose text holds brackets, on a bracket you escaped, on a note kept beside a newer one, and on a
version that belongs to another project.

**What to do differently:** say `update` in your home.
### Fixed
- **A link whose text holds brackets** (`library.py`, and so every check that reads links). A
  changelog entry is named so, `[… entry *[0.3.0]*, *Changed*](…)`, and CommonMark and GitHub
  read it as a link; the check read none, so a claim ending in one was reported as linking no note.
  A link's text may now hold one level of balanced brackets; the projects table is read the same
  way.
- **An escaped bracket opens no link** (`library.py`). `\[X′X/n − X′ΩX/n](X′X/n)⁻¹`, escaped as
  1.17.4's hint asks, was still reported as a broken link, with that same hint. A backslash before
  a punctuation mark now makes it plain text, as GitHub renders it; after an escaped backslash,
  `\\[`, the bracket still opens a link.
- **A clipping kept beside a newer one is not behind its project** (`check_library.py`). Of the
  notes on copies of one file — `README.md`, `README_2026-10-18.md`, `README_2.0.1.md`, by their
  `local_copy`'s name with any date, time or version after it taken off — only those stating the
  highest version are checked: the old note, kept under its `> [!WARNING]`, is no longer reported,
  and a newest one still behind is reported alone. A note states the highest version its citation
  names: one on 0.66.0 that records the same text at 0.67.0 has read 0.67.0.
- **A version that is another project's** (`check_library.py`). A note is matched to a project
  only when its file name names it — every word of the project's name or its folder's, or two or
  more of their distinctive words — or its citation or `source` names the project's repository,
  `KaxaNuk/Backtest-Engine` or its web address. A library a README only pins, or another
  project's package whose name shares one word with it, no longer counts.
- **`audit`**, *Step 1*: how a note is matched to its project and which copy is checked; a new
  clipping comes in under the old copy's name with its date or version after it; and, left to
  judgement, an older note the check passes over with no `> [!WARNING]` naming the newer one.

## [1.18.0] - 2026-10-18
Your tutor follows the four Training Workshops as they now publish: a deck at the repository's root
or in its session's folder, each language's own deck, and the code a session ships beside it.

**What to do differently:** say `update` in your home.
### Changed
- **The workshops' new layout** (`workshop` 0.3.0): a session with no `folder` in the course map
  has its deck at the root, as the Investment Bootcamp's six decks are since 2026-10-18; each
  language's branch names its own deck. The session's code — a notebook, `exercises/` with
  `solutions/`, or an example module — is read from its folder and run by the owner as the
  course's README says, a solution opened only after their own attempt. The map's
  `pillar_sessions` name each other workshop's session the course links to. The live blocks have
  no drill any more; the checkpoint is the example of an AI-off block.
- **A clone is read on the course's branch** (`workshop` 0.3.0): the owner's language, else
  `english`, through `git show`, which changes nothing, so a clone left on an older `main` no
  longer gives an earlier edition's session; a file the clone lacks comes from the public
  repository. A `deck` that already holds its folder is not prefixed twice; with no folder, the
  README's own section for the session stands beside the deck. A session's `state`, `prework` and
  the course's `dates` are read — a sealed window is never opened early —, a course's own track
  names stand, and a rule the course's README sets on the assistant holds over a block's `ai`.

## [1.17.5] - 2026-10-18
The worked example's notes on its one book now name its chapter 11 rightly: the quantitative
appendix, not a chapter on hedging and optimisation.

**What to do differently:** nothing.
### Fixed
- **Paleologo's `INDEX.md` in the worked example** (example 0.17.6 to 0.17.7): *What this book does
  not settle* called chapters 7 and 11 "the hedging and optimisation chapters". The publisher's
  contents, which the chapter table follows since 1.17.3, title chapter 7 *Manage Factor Risk* and
  chapter 11 *Appendix*, the book's quantitative appendix. The line now names each so, and still
  says both are out of reach while the factor model is not inside portfolio construction.

## [1.17.4] - 2026-10-18
`audit`'s library check no longer raises four false alarms a first run on a real library showed,
and finds a clipping behind its project when your projects table names a folder of them.

**What to do differently:** say `update` in your home.
### Fixed
- **An unread source's leads, short and to the point** (`unread_sources.py`, and so
  `check_library.py`). A note reading another copy of the same name — `Deck_2026-10-04_0936.pdf`
  for `Deck.pdf`, an earlier or a later copy — is named first and alone. With none, a note of the
  same first author and year is named only when it shares a word of the source's title, at most
  three, those sharing the most first: an organisation's clippings of one year no longer list every
  note of that year, each line thousands of characters long.
- **A clipping behind its project, when a projects-table row names a folder of projects**
  (`check_library.py`). A row whose path holds no `CHANGELOG.md` of its own is read as one project
  per folder inside it that holds one — still that one file of each, never its code — and the
  report names the rows it could not check, so *none of: stale clipping* no longer reads as all
  clear when nothing was checked. A one-word project name must be in the note's file name. A
  version at the end of a sentence, `version 0.66.0.`, is now read: it was missed before.
- **Cites an extract** flags a link into `Extracts/` or the path of a file there,
  `Extracts/<slug>/<file>`, no longer a mention of the folder, *`Extracts/` is gitignored*.
- **A claim that links no note** reads the whole claim: every indented line after its first, a
  blank line between them included, and a link whose text wraps onto the next line. Every link the
  library check reads, in any note, may now wrap so.
- **A broken link that is not a file** — text in brackets followed by brackets, as an equation
  writes `[X′X/n](X′X/n)⁻¹` — adds a hint: if it is not a link, escape its bracket, `\[`.
- **`audit`**, *Step 1*: a row naming a folder of projects, and the rows the check could not read.

## [1.17.3] - 2026-10-18
The worked example's one book now lists its chapters, each marked read or skipped, as every book's
index does, so checking the example's library finds nothing.

**What to do differently:** nothing; a copy of the example you made before keeps its own index.
### Fixed
- **Paleologo's `INDEX.md` in the worked example** (example 0.17.6) has the chapter table
  `references/note.md` gives a book's index: its eleven chapters, from the publisher's contents;
  chapters 3, 5, 6, 8 and 9 *read*, the ones its sections cite, each row linked to its sections and
  the claims they bear on; the other six *skipped*. No copy of the book is kept, so the table has
  no pages. The sections, written before the convention, are kept word for word. The library check
  `check_library.py`, new in 1.16.0, reported it as the example's only finding, and reports none
  now. The example's `Bibliotheca/LOG.md` records the fix.

## [1.17.2] - 2026-10-18
Your researcher now knows Portfolio Construction 2.0.1, which adds the library's documentation and
changes nothing you do with it.

**What to do differently:** say `update` in your home. A strategy on Portfolio Construction 2.0.0
needs nothing new: 2.0.1 changes no code.
### Changed
- **`references/investment-lab.md`** (`next` 1.9.1): Portfolio Construction's *Latest* is 2.0.1
  (2026-10-06). The Backtest Engine's 0.67.0 is still its newest.
- **`portfolio-construction-runs`** (0.5.3) gains a *Changed in 2.0.1* paragraph, from the
  library's changelog and not yet checked by a run here: a documentation site the README links,
  which did not answer on 2026-10-18; three behaviours its User Guide states — a rebalance date
  absent from the data gives a snapshot of nulls, the KN Index applies `min_weight` only when
  `max_constituents` is empty, and `min_constituents` is validated but not enforced; HRP's and
  HERC's registry text, where the Methodology follows the code instead; and the README agreeing with
  the changelog on `calendars`, input files and `examples/`. Its `library_version` stays 1.28.0, the
  build its traps were checked on.

## [1.17.1] - 2026-10-18
Keeping a copy on GitHub now offers to keep your e-mail empty, as your researcher saves it since
1.15.2, and the list of uses says every write made without asking.

**What to do differently:** say `update` in your home.
### Fixed
- **`backup`** (0.1.7), *Step 6*: since the researcher asks no e-mail, the address a version is
  signed with is usually empty, `<>`. The question `E-mail` now offers *Keep it empty* (*the
  versions show your name alone*) when it is, and *Keep the one I have* only when there is one,
  beside *Use GitHub's private address (recommended)*.
- **`USE-CASES.md`**: the writes made without a go of their own include the one line `audit` adds
  to the library's log, as the home's `AGENTS.md` says.

## [1.17.0] - 2026-10-18
Your researcher can now read a scanned book or paper: it makes a searchable copy of the scan, on
your go, and reads a page's image where the text alone falls short.

**What to do differently:** say `update` in your home; a scan you could not read before can be
read now — say `read` and name it.
### Added
- **`ocr_pdf.py`**, in the `read` skill's `scripts/`: a scan's searchable copy, `<its name>
  (OCR).pdf`, beside it, never over a file. Each page is rendered at 200 dpi in shades of grey and
  read by RapidOCR on this computer, with its angle classifier off — on, it turned about one line in
  ten upside down. Each line is laid over the page as invisible Helvetica, at its place and sized
  to it, so the copy looks exactly like the scan and `extract.py` reads it like any PDF; a rotated
  page is laid the right way. `--pages` reads only some pages, for a book only some of whose
  chapters are scanned; a PDF that has a text layer already is refused. It needs only `uv`: the
  engine and its models, about 100 MB, download on its first run. pypdfium2 renders, pypdf writes;
  no PyMuPDF, whose AGPL licence the package avoids.
### Changed
- **`read`** (0.13.0), **on the owner's word**, the frozen first read:
  - *Step 2*: a PDF with no text layer is offered a searchable copy, `Scan`: *Make a searchable
    copy*, *Leave it unread*; on the go, `ocr_pdf.py` makes it, the copy is read like any PDF, and
    the note's `local_copy` names it. Without the go, the source is reported unreadable, as before.
    Scanned chapters in a book that has text get a copy of those pages. The copy is, with the copy
    of an attachment, the only write into `Sources/`. The unread sources are listed by
    `unread_sources.py`; the contents pages a PDF reader cannot show — on Windows, with no
    Poppler — are read as images from `render_pages.py`.
  - *Step 4*, **Page images**: a table, an equation or a figure the extract dropped or garbled, and
    any figure, name or formula from an OCR copy, is read from its page's image; the note cites the
    page as any other, and what an image does not make clear is quoted as unclear. Delegates'
    drafts are staged outside the library and checked against the extract before the plan.
  - *Step 6*: an existing concept page is updated through `update_concept_pages.py`, its diff
    checked against the plan; a new page is written whole.
  - *References* names every script in its folder; *What this skill will not let you do* names the
    page images and the searchable copy as the exceptions they are.
- **`read`'s `references/note.md`**: `local_copy` names a scan's searchable copy, and *Where the
  text came from* — the provenance line says *from an OCR copy*, and which pages came from an image.
- **`extract.py`**: a scan's message points to `ocr_pdf.py`, and so does a chapter not written for
  want of a text layer when others were.
- **`ONBOARDING.md`** records the change; the approved run is unchanged, its paper having a text
  layer. **`FROZEN.json`** holds the new fingerprints of `read`'s `SKILL.md`, `note.md`,
  `extract.py` and `ONBOARDING.md`.
- **The home's `AGENTS.md`** (home template 0.29.0): a scan's searchable copy is the second write
  into `Sources/`, and the tools include `ocr_pdf.py`.
- **`AGENTS.md`** and **`README.md`** name `ocr_pdf.py` and the searchable copy.

## [1.16.0] - 2026-10-18
Your researcher now finds every source you have not read yet, whatever its name, checks your
library the same way on every `audit`, and can show you a page of a PDF as an image.

**What to do differently:** say `update` in your home.
### Added
- **`unread_sources.py`**, in the `read` skill's `scripts/`: every file under `Sources/` — in a
  strategy, every PDF and clipping in `Bibliotheca/` — that no note's `local_copy` names, matched
  by its full path, so a name with commas, parentheses, spaces or accents is safe, and filtered by
  nothing, date included. A searchable copy of a scan, `<name> (OCR).pdf`, reads for its scan. An
  unread source beside a note of the same first author and year is named with it, since it may be
  that note's under another path. `next` (1.9.0) runs it for its row 4, and `audit` through the
  library check.
- **`check_library.py`**, beside it: `audit`'s every-run checks as a script, the same way each time
  — links broken or leaving the repository, extracts and PDFs cited, orphans, the index against the
  notes, each book's `INDEX.md` against its chapter files, frontmatter fields and a `read` that is
  only a date, two notes on one file, chapters no concept page names, a page's claim that links no
  note, a study with no state line, stray files, unread sources, and the notes whose `local_copy` is
  not on this computer, as one line. `audit` runs it first and reports what it prints, then makes
  only the checks that need judgement.
- **A clipping behind its project**, a new `audit` finding: a note on a project in `RESEARCHER.md`'s
  projects table — a KaxaNuk library, say — that states a version older than the newest in the
  `CHANGELOG.md` at the project's path. The script opens that one file of the project, never its
  code. The fix is the new README and CHANGELOG brought in as clippings, then `read`.
- **`render_pages.py`**, beside it: a PDF's pages, or a part of one, as PNG images, at the dpi
  asked, in the system's temporary folder, never in a library. It renders with PDFium, through
  `pypdfium2`, so it needs no Poppler and no `pdftoppm`, which Windows lacks and the assistant's PDF
  reader needs. `audit deep` looks at a cited page with it before it calls a figure in a table or an
  equation *not found*, and the home's `AGENTS.md` names it for the contents pages `read` reads of a
  PDF with no outline.
- **`update_concept_pages.py`**, beside it: concept pages brought up to date in one pass from a spec
  of what each gains — sources, claims, the blockquote for the owner's questions, lines under
  *Open* — with `updated` set and nothing else touched. It shows the diff unless told `--write`,
  checks every page before writing any, skips what a page already holds, and never creates a page.
  The home's `AGENTS.md` makes it how `read` and an approved `audit` fix update an existing page.
- **The home's `AGENTS.md`** (home template 0.28.0): the library's tools, what each is for; a
  delegate's draft staged outside the home and checked against its extract before the plan; and a
  download behind a login, a refusal, a busy server or a bot check, such as Cloudflare's, is the
  owner's to fetch in their browser, never got past.
### Changed
- **`check_numbers.py`** leaves out years and the numbers of equations, sections, tables, figures,
  chapters, pages and footnotes, in English and Spanish, which were most of its *not found*. A note
  whose figures sit at one offset from the pages it cites is reported once, with the offset, and
  those figures are counted *at offset*, no longer each *elsewhere*. `audit deep` reports such a
  note as one finding: it cites printed pages, where `references/note.md` cites the extract's.
- **`audit`**: *Step 1* runs the library check and lists only what it leaves to judgement; *Step 2*
  no longer repeats the bibliography and link checks the script makes.
- **`AGENTS.md`**: the library's tools among the skills' scripts, and every script works under
  `python -I`: it prints UTF-8 and finds its neighbours itself.
- **`read`'s `SKILL.md`, its note convention and its extractor are unchanged**, as frozen; its
  version stays 0.12.7, and `FROZEN.json` holds the same fingerprints.
### Fixed
- **Every save that finds no name in git asks only for a name**, as since 1.15.2: `teach`,
  `refresh-index`, `objective`, `challenge` and `blueprint` still asked for a name and an e-mail,
  and so did the strategy template's `SETUP.md` (template 0.19.3, example 0.17.5).
- **`experiment-lifecycle`** (0.14.8): `references/structure.md` names the template version its tree
  matches, 0.19.3, and the three templates an experiment copies, not four.
- **`backup`** (0.1.6): on a new computer, the name is asked again at the first save; *Step 6* sets
  only the e-mail.
- **The home's `AGENTS.md`**: the researcher's skills include `workshop` and `known-answer`.

## [1.15.3] - 2026-10-16
Reading a document no longer asks for your e-mail either: when git has no name, it asks only your
name, or what you'd like it to call you.

**What to do differently:** say `update` in your home.
### Changed
- **The first read, on the owner's word** (`read` 0.12.7): a save refused for want of a name asks
  the same open question as every other save since 1.15.2 — *What's your name, or what would you
  like me to call you?* — with no options and no e-mail, and git gets the empty address `<>`.
  `ONBOARDING.md` records it, and `FROZEN.json` holds the new fingerprints.

## [1.15.2] - 2026-10-16
Your researcher no longer asks for your e-mail: it asks only your name, or what you'd like it to
call you, in your own words.

**What to do differently:** say `update` in your home.
### Changed
- **The onboarding, on the owner's word** (`init-researcher` 0.8.7, `interview` 2.12.6): when git
  has no name, `SETUP.md`'s step 1 asks for it in one open chat message, with no box and no
  options — *What's your name, or what would you like me to call you?* — and asks no e-mail: git
  gets the address `<>`, which it saves as an empty one, so every version is signed with the name
  alone. `<>` and not `""`, which Windows PowerShell drops on the way to git. Question 1 asks the
  name the same way when git has none, *First, your name, or what you'd like me to call you*, and a
  failed save at the end of the interview takes the name question 1 gave, asking nothing.
  `ONBOARDING.md` records it, and `FROZEN.json` holds the new fingerprints.
- **Every save that finds no name in git** asks the same open question and no e-mail:
  `init-strategy` (0.4.3), `init-python-library` (0.2.2), `init-example` (0.5.3), `next` (1.8.8),
  `philosophy` (1.3.5), `query` (0.9.6), and the `audit`, `refine`, `study` and `update` commands.
  `backup` still asks for GitHub's private address when you keep a copy there.

## [1.15.1] - 2026-10-16
A new researcher's first question about you is now a plain message with nothing to pick: you tell
it what you do, and the projects and topics you will work on together.

**What to do differently:** say `update` in your home; the interview you already did stays as it
is.
### Changed
- **The onboarding, on the owner's word** (`interview` 2.12.5, `init-researcher` 0.8.6): question
  1 is one open chat message on every assistant, with no box and no options, which read as a choice
  to make beside the text field, and no number; its question alone: *Tell me more about yourself:
  what you do, and the kinds of projects and topics we'll be working on together.* (*Cuéntame más
  de ti: qué haces, a qué te dedicas y con qué tipo de proyectos y temas vamos a trabajar
  juntos.*) *I'm just starting*, *nothing yet* and *later*, typed in any language, still work as
  answers. A short name for the files, when one is needed, is a line of the same message, and a
  re-run under `force` asks in the same way to keep the current lines or say what changed. Question
  2 is unchanged, *2 of 2* included. `SETUP.md` and `ONBOARDING.md` record the run, and
  `FROZEN.json` holds the new fingerprints.

## [1.15.0] - 2026-10-14
Before you trust a method with real data, you can now test it on simulated data whose right answer
you set, and see how it fails: say *known-answer test for my half-life estimate*.

**What to do differently:** say `update` in your home.
### Added
- **`known-answer`** (0.1.0), a skill, so Codex has it too. It loads when you ask to check a method
  before it touches real data, or when a workshop session names it, even where the
  course still calls it coming. It asks your prediction first — what the method should give back,
  and what a failure will do to it — then plans one notebook and, on your go, writes it in a new
  folder you name beside your strategy: data simulated from a model whose truth is set and seeded,
  your method run on it unchanged, and a Verify section that raises when the method misses the
  truth by more than a tolerance stated before the run. It also shows one way the method fails —
  too few observations, a look-ahead, a pooled rank — so you see the check bite. You run the
  notebook, on either track of a workshop; your researcher writes and lints it, never runs it, and
  never states, confirms or corrects a figure it prints.
- **Nine recipes**, in its `references/recipes.md`: an AR(1) and its half-life, a geometric
  Brownian motion's drift and volatility, a regression's beta, a factor model's loadings, a planted
  signal's information coefficient, clusters with known members, a two-state regime, a GARCH(1,1)
  and its forecast, and a logistic classifier's coefficients, AUC and calibration. Each gives the
  model, its true parameters, a seed, the estimator to check, the tolerance and why, and the
  failure to show, in prose and formulas, with no code; each figure was checked by simulation on
  2026-10-14. A short sample — a half-life of three months over ten years of months — has a rule of
  its own, since there the usual tolerance stops checking anything.
- **It keeps to simulated data.** Every figure in the notebook is a teaching computation on
  simulated data, never one about a book or your data. It writes that one notebook and nothing
  else: nothing in your strategy, which it imports from without writing in, nor in a course's clone
  or your home, and it saves no version. A tolerance is never widened after a miss, and your method
  is never rewritten to pass.
### Changed
- **`README.md`** gains a row in *What you can use it for* and in the table of skills.
  **`CONTRIBUTING.md`**: a release deploys 24 skills, and 25 with the researcher's own skill beside
  them, and the walk by hand tries `known-answer` on one recipe when a release changes it.

## [1.14.0] - 2026-10-14
Your tutor in a KaxaNuk Training Workshop can now set you practice problems from a session, at
your level: say *practice Bootcamp S03, beginner*.

**What to do differently:** say `update` in your home.
### Added
- **`workshop`** (0.2.0) **gains *Practice***: problems drawn from the session's deck at the level
  you name — beginner, intermediate or advanced — each naming the slide it comes from, with new
  numbers so no answer can be read off the deck; one at a time, your prediction first, hints in
  three levels, the worked answer only after your own attempt. A problem of pure mathematics is
  checked in full, with one line of SymPy or a small bump for a derivative; one on a book's figures
  by its steps only, as before. Every third problem comes back from an earlier session, the ones
  the session builds on first. Asked to explain a formula, it takes it symbol by symbol, with its
  unit and the session that defined it, and works it once with two invented numbers. Never in a
  block with the AI off, and never the checkpoint's own questions.
- **`workshop` reads a course's levels and data**: a session's `module`, `level` and `needs`, the
  course's `modules`, and its `data` — what the case needs, the KaxaNuk tool tried first, its
  state, and the outside source used `instead` until the tool covers it, which the tutor names as
  the course's stand-in and never as its own pick.
### Changed
- **`README.md`** names *practice* beside the workshop rows.

## [1.13.0] - 2026-10-12
Your brief can now write your weekly update, ready to paste into team chat, and tells you how to
fix a connector that is connected but cannot read.

**What to do differently:** say `update` in your home, then `brief setup` to add *Week*.
### Added
- **`brief`** (1.1.0) **gains *Week***, a fourth part, written one day a week: what you did last
  week, from your commits in every repository of your projects table and from the calendar's work
  meetings, demos and talks; the open problems the repositories show; and this week's next steps
  and meetings. In your language, inside one code block, as plain text that pastes into Slack or
  Teams as it stands — a `•` bullet per project, `◦` sub-bullets for the detail, one blank
  line between the three sections and no markup — with as many bullets as the work needs. It quotes no
  email address, commit message or private path. `brief setup` asks its day, and any folder beyond
  the projects table to read too, such as another client's repositories, which adds no row to
  `RESEARCHER.md` unless you say so.
### Changed
- **Today's brief can be corrected.** Ask by name the same day — *brief, add the calendar*,
  *brief, no asterisks* — and only that file changes. The scheduled task still never edits a
  brief, and no brief of an earlier day is ever edited; a change for every day or every week is
  `brief setup`. The home's `AGENTS.md` says the same (home template 0.27.0).
- **`README.md`** and **`USE-CASES.md`** name *Week* among the parts.
### Fixed
- **A connector that cannot read is caught at setup.** A Google connector granted fewer permissions
  than it asks shows as connected yet answers every call with *requires additional permissions*,
  and a brief ran without the calendar for weeks. `brief setup` now makes one harmless read with
  each connector, keeps nothing of it, and names one that refuses with its fix: in claude.ai,
  *Settings → Connectors*, disconnect it and connect it again, ticking every permission. A brief
  that meets the same refusal says the same in its *Work* part.

## [1.12.0] - 2026-10-11
Your researcher can now be your tutor in a KaxaNuk Training Workshop: name the session, such as
*Bootcamp S03*, and it follows the course with you.

**What to do differently:** say `update` in your home; then, in a workshop, tell your researcher
the session you are on.
### Added
- **`workshop`** (0.1.0), a skill, so Codex has it too. It loads when you say you are working
  through a session of the Investment Bootcamp, or ask for help with one. Each time, it reads the
  course map at the end of the workshop's `README.md` and the session's deck, from your clone or the
  public repository, on the branch in your language where there is one, and never keeps a copy of
  the course: the course changes, and the tutor follows it. Where the map is not published yet, it
  reads the course's other files and says so; a workshop it cannot reach, not yet published or
  private, it says so and asks for your clone or the deck.
- **It tutors as the course asks.** It places you in the session's block, from the course's own
  list of blocks, and on your track, no code or code. Your prediction comes first, and hints come in
  three levels: a nudge, a pointer to the file or skill, then a worked step. While the AI is off it
  holds your question for later, with no hint, no code and no answer, since only what you can do
  and explain with the AI off is assessed. It computes no performance number and gives no
  investment advice.
- **It hands the hard parts on**: an idea to `teach` with the session's topics, your own reading to
  `query`, Golden-Flow's file for the step to `init-example`, and each tool to its step's skill.
  While a Lab module is still coming, the no-code track works the Golden-Flow file the course map
  names instead.
- **The workshops are named in this skill alone**, by the owner's choice: their names and
  repositories, never a session's content, deck or page. The reading map and `philosophy`'s
  question bank still name no course, as since 1.11.0.
### Changed
- **`README.md`** gains a row in *What you can use it for* and in the table of skills.
  **`CONTRIBUTING.md`**: a release deploys 23 skills, 24 with a researcher's own on Codex, and the
  walk by hand tries `workshop` on one session when a release changes it.

## [1.11.2] - 2026-10-11
Your researcher never gives investment advice and now says so when a new one is set up, and the
worked example's figures carry their caveat.

**What to do differently:** say `update` in your home.
### Changed
- **The onboarding, on the owner's word** (`init-researcher` 0.8.5): after the welcome, one line in
  the user's language, said even when a name comes with the command: *It's for research and
  learning, never investment advice: it can be wrong, every decision is yours, and what you share
  with it goes to the company behind your assistant.* Every question is unchanged.
  `ONBOARDING.md` records the line, and `FROZEN.json` holds the new fingerprints.
- **The researcher never advises** (`interview` 2.12.4): the agent and the researcher's skill it
  writes never say buy, sell, trim, add or hold, nor suggest or place an order. The skill's
  template moves to 0.5.1, so `next` and `update` bring a home's skill forward.
- **One list of words in the rules**, buy, sell, trim, add or hold: in `study`, in `philosophy`
  (1.3.4) and its question bank, and in the home's `AGENTS.md`. `teach` and `query` (0.9.5) gain
  the rule. The disclaimer's own wording waits for counsel.
- **The worked example's figures carry their caveat** (example 0.17.4): a backtest on the past
  prices the strategy was designed on, one of 107 portfolios tested, with modelled costs, against
  KaxaNuk's own index, and the drawdown just after the window. `alpha-decomposition` (0.4.4) and
  `portfolio-construction-runs` (0.5.2) label the figures they quote as the example's in-sample
  backtest.
- **Coming next** stays open: more tools and starting points will join your researcher over time,
  with none named yet.
- **One place to write to us.** `README.md` and the home's `README.md` end with *Contact*, one
  address for each kind of question: the Investment Lab's libraries and licences, or a problem
  with your researcher, `lab@kaxanuk.mx`; the Analytics Factory's data sets,
  `analytics@kaxanuk.mx`; Research Models such as the worked example, `research@kaxanuk.mx`;
  Training Workshops, `workshops@kaxanuk.mx`; anything else, `info@kaxanuk.mx`. The other
  mentions are gone, the disclaimer's *Questions* among them. The researcher's own list is in
  `investment-lab.md` (`next` 1.8.7), and `attribution-analysis-runs` (0.5.2), `init-example`
  (0.5.2), the strategy template (0.19.2) and the example ask `analytics@kaxanuk.mx` for the
  Analytics Factory's files.
- **The disclaimer names the companies** that receive what your researcher reads: Anthropic for
  Claude, OpenAI for Codex, Google for Gemini. The rest of its wording waits for counsel.
- **Why not just use Claude or Codex?** The README answers it under its opening example: your
  researcher runs on them, and adds your library, you, kept in your own files on every assistant,
  and a method.
- **The README's opening example** shows a research model from idea to verdict. Arya teaches each
  step and its tool: the claims, the reading for and against, the data and a screen of the
  signal, and a blueprint with what would prove you wrong and a control, all before any
  backtest. Then `challenge` reads the result against that blueprint, the trial count, the
  control and the attribution.
- **`README.md`**: keys are kept on your computer, in a file never saved in git and never read by
  your researcher; a brief quotes the rules the day's news bears on, with no verdict. Its
  *Licence*, and the home's (home template 0.26.1), say the MIT licence grants no right in
  KaxaNuk's names, the Investment Lab's libraries, the Analytics Factory's files, KaxaNuk's
  Research Models or Training Workshops.

## [1.11.1] - 2026-10-11
Nothing changes for you: a new home, strategy or library is never copied with a key file, wherever
one sits.

**What to do differently:** nothing.
### Changed
- **`scaffold.py`** (`init-strategy` 0.4.2), which copies every starting point, leaves every key
  file behind at any depth: `Config/.env` as before, and now any other `.env` or `*.env` and
  `.kaxanuk_license`, the names the starting points' `.gitignore` files keep out of git. `--only`
  refuses one. Only a working copy of the package could hold one: an install from GitHub carries no
  ignored file.

## [1.11.0] - 2026-10-10
Your researcher reads more simply, says plainly what it is for and what it is not, and keeps
nothing confidential in the package.

**What to do differently:** say `update` in your home.
### Added
- **What it is, and what it is not**: one plain statement in `README.md`, in the home's
  `README.md` and in the worked example's `README.md`. The researcher is a research and learning
  tool, never investment advice: it never trades or moves money, and every decision, and its risk,
  is yours. What it reads goes to the company behind your assistant, never to KaxaNuk. It is MIT,
  as is; the example's figures come from a backtest, shown to teach the method. `USE-CASES.md`, the
  strategy template's `README.md` and `SETUP.md`, and `CONTRIBUTING.md` link to it.
- **`study`** lays out the case for and against a choice, and what would settle it; it never says
  buy, sell or hold.
### Changed
- **Each idea is said once, in one place**, and the other files point to it; long sentences are
  split, and history that changes nothing for a reader is gone. Every rule, command, path and
  condition is kept. `README.md` folds its skills tables, `CONTRIBUTING.md` keeps what a
  contributor does, and `AGENTS.md`'s table points to `CONTRIBUTING.md` for the install check.
- **The onboarding and the first read, trimmed on the owner's word** (`init-researcher` 0.8.4,
  `interview` 2.12.3, `read` 0.12.6): repeats and history are gone from `SETUP.md`, the three
  skills and `read`'s note convention. Every question, option and message a new user sees, and
  their order, is unchanged, checked against `ONBOARDING.md` and by a replay of the approved run.
  `ONBOARDING.md` is trimmed the same way, and `FROZEN.json` holds the new fingerprints.
- **The reading map and `philosophy`'s question bank name no course** (`read` 0.12.6,
  `philosophy` 1.3.3): the papers, the questions and their links stay; the course they were
  distilled from and its page numbers are gone.
- **Where your data goes, said accurately**: `brief` (1.0.4) and `USE-CASES.md` say nothing is
  sent on your behalf and what the brief reads passes through your assistant; `backup` (0.1.5)
  says the copy is private to you and anyone you invite.
- **`portfolio-construction-runs`** (0.5.1): its API reference names the imports the library's
  README shows and its licence client, and no longer the library's inner modules.
- **Neutral examples**: `interview` shows `marta` as a git handle, `init-researcher` `arya` beside
  `Arya`.
- **A light pass on every other skill and command**, exact repeats and overlong sentences only:
  `alpha-decomposition` 0.4.3, `attribution-analysis-runs` 0.5.1, `backtest-engine-runs` 0.4.1,
  `bloom-code-lint` 0.2.1, `data-analyzer-runs` 0.2.5, `data-curator-custom-calculations` 0.5.1,
  `experiment-lifecycle` 0.14.7, `how-we-work` 0.5.4, `init-example` 0.5.1, `init-python-library`
  0.2.1, `init-strategy` 0.4.1, `next` 1.8.6, `paper-trading-gate` 0.4.3, `query` 0.9.4 and
  `universe-point-in-time` 0.3.3, the commands and `blueprint-critic`.
- **The home template 0.26.0, the strategy template 0.19.1 and the worked example 0.17.3** read
  the same way. A strategy's `.gitignore` keeps a `.kaxanuk_license` file out of git, and the
  example's headline figures say they come from a backtest.
- **The KaxaNuk Python Library Template 0.1.1**: its `AGENTS.md` and `README.md` say each thing
  once; nothing a new library builds or runs changes.

## [1.10.3] - 2026-10-10
Nothing changes for you: the way your researcher is set up and reads its first document is now
frozen as it was tested and approved, so it cannot change by mistake.

**What to do differently:** nothing.
### Added
- **`ONBOARDING.md`**: the onboarding and the first read as the package's owner approved them,
  every question and message a new user sees, from the language to the end of the first read, on
  1.10.2.
- **`FROZEN.json`**: the fingerprints of the files that make that run — `SETUP.md`,
  `init-researcher`, `interview`, and `read` with its note convention, reading map and extractor —
  and of `ONBOARDING.md`; the home template and `philosophy`'s question bank stay free. `AGENTS.md`
  says a frozen file changes only on the owner's word, shown against `ONBOARDING.md` first, and
  `CONTRIBUTING.md`'s *Development* has the check, run before every commit, that fails on a frozen
  file that changed.

## [1.10.2] - 2026-10-10
Your interview's first question is shorter: tell me about yourself, what you do and what you're
working on.

**What to do differently:** say `update` in your home.
### Changed
- **Question 1 asks one short thing** (`interview` 2.12.2): *Tell me about yourself in a few lines:
  what you do and what you're working on. Write it below.* (*Cuéntame de ti en unas líneas: a qué te
  dedicas y en qué estás trabajando. Escríbelo abajo.*). It no longer asks what you'd like a hand
  with, where you are with markets, or what to stay out of; *Out of scope for now* stays *None yet*
  until you say something to stay out of. What you are here for is still proposed from your
  answer, *help with your work and your projects* whenever you name something you are working on.
  `SETUP.md` and the home template (0.25.2, its `README.md`) say the same.

## [1.10.1] - 2026-10-10
Your interview's first question box now asks you to write about yourself, with two short, quiet
options for when you'd rather not yet.

**What to do differently:** say `update` in your home.
### Changed
- **The box's text field is the answer** (`interview` 2.12.1). Question 1 now ends *Write it below,
  in your own words* (*Escríbelo abajo, con tus palabras*), and its options are short ways out that
  never compete with writing: *Nothing yet* (*Nada aún*), *I'm just starting*, a complete answer;
  and *Later* (*Después*), which starts with your name alone. They replace *I'm just starting* and
  *I'll tell you later*, and write the same lines. On a re-run, *Nothing yet* replaces *I'm just
  starting* beside *Keep them*.

## [1.10.0] - 2026-10-10
Your first interview is quicker: on Claude, its question about you opens a box to answer in, the
second question asks only how your researcher should talk to you, and at the end it tells you
everything it can do.

**What to do differently:** say `update` in your home.
### Changed
- **Question 1 of the interview is a question box** (`interview` 2.12.0), as question 2 already
  was. Its header is `About you` (`Sobre ti`), it opens with *1 of 2*, asks the same four things,
  and ends *Write it in your own words, or pick one*. Your own words, typed in the box, are still
  the answer: they write *Works for* and *Out of scope for now*, and everything else is proposed
  from them. Its two options need no typing: *I'm just starting*, and *I'll tell you later*, which
  starts with your name alone. A box you close is not a stop: what you type next in chat is the
  answer. On a re-run, *Keep them* keeps both lines word for word.
- **What crowded that message moves into the box.** When git has only a handle for you, the box
  asks your name first, and the line before it no longer says *I'll work for you*. When your
  researcher needs another short name for its files, it is a second question in the same box,
  `Short name` (`Nombre corto`), with names to pick. Questions 1 and 2 are never asked together.
- **No more *What brings you here?*** Question 2 asks only the voice. What you are here for — help
  with your work and projects, learning to invest, building a strategy, writing down how you invest
  — is proposed from what you said in question 1, like your domains and projects, and named at the
  hand-over for you to change on a word. Every skill that reads it reads it as before.
- **The hand-over ends with everything you can ask for**, now with *learn to invest from scratch*
  among them.
- **Codex and Gemini ask as before**: question 1 stays one open chat message, never a numbered
  list, and *later* or *skip* counts as *I'll tell you later*. `init-researcher` (0.8.3),
  `SETUP.md`, `update` and the home template (0.25.1, its `README.md` and `AGENTS.md`) say the
  same.

## [1.9.0] - 2026-10-10
Your researcher now learns KaxaNuk's tools only from their documentation and from running them, and
never opens, quotes or copies their code.

**What to do differently:** say `update` in your home.
### Changed
- **A tool's code is never read, quoted or copied.** KaxaNuk's tools — the Investment Lab's
  libraries and the Analytics Factory — are known from their skills, documentation, changelogs and
  runs, never from a library's installed files, a clone, a wheel or a source page its documentation
  links to. No part of that code, no copy of the Factory's files and nothing of KaxaNuk's research
  goes into a note, a clipping, a strategy, an issue or a message, and an error is told by the call,
  its type and its message, never by the library's traceback lines. In a Lab library's own
  repository, its rules govern its code, and none of it leaves. The rule is in the home's
  `AGENTS.md` (home template 0.25.0), in your researcher's skill (0.5.0, which `update` brings),
  in the agent `interview` writes, in a strategy's `AGENTS.md` (strategy template 0.19.0, example
  0.17.2) and in the filesystem-boundaries instruction (1.3.0).
- **The library skills say only what the documentation, the changelog or a run says**
  (`attribution-analysis-runs` 0.5.0, `portfolio-construction-runs` 0.5.0,
  `data-curator-custom-calculations` 0.5.0, `backtest-engine-runs` 0.4.0). Every statement taken
  from a library's code is gone — internal names, module paths, tolerances, how a loader works
  inside, steps that open the installed package — and a trap no document or run supports is
  dropped until a run shows it again. Each skill now says where its knowledge comes from, and
  `library_version` does not move. A trap found in a library is told by behaviour, as an issue in
  the package or to `lab@kaxanuk.mx`.
- **For maintainers**, `AGENTS.md` and `CONTRIBUTING.md`: a library's skill is written from its
  documentation, changelog and runs, never from its code, and names only its public API.
- **The example researcher is Arya** (`init-researcher` 0.8.2, `interview` 2.11.0), in the README,
  `CONTRIBUTING.md` and the home's README.
- **Earlier versions of the library skills leave this repository's history**, rewritten so every
  commit holds the text above.

## [1.8.0] - 2026-10-09
When you start a strategy or a Python library without a name, your researcher asks what it is about
and suggests a few names for you to pick, or you type your own.

**What to do differently:** say `update` in your home.
### Changed
- **The name is always yours, and suggested from your idea** (`init-strategy` 0.4.0,
  `init-python-library` 0.2.0). With no name given, and nothing said yet on what it is about, the
  first message asks what the strategy is about, or what the Python library will do, in a sentence
  or two — nothing else is asked or run first — then offers names made from your words; *Other*
  takes your own. A name of yours, typed with the command or in any form, is put in the folder's
  form (*Contabilidad Project* becomes `contabilidad-project`) and shown in the plan; no name is
  ever made up for you, nor a placeholder kept. The place is beside the folder you are in, unless
  you say another.
- **A Python library's suggestions are checked on PyPI first**; only free ones are offered, or,
  offline, all of them marked *not checked*. Your sentence on what it does becomes its description,
  checked before the copy, never shortened for you.
- **A folder already there** is said before the plan, and another name or place asked for, never a
  `-2` added; a copy refused later asks the same way.
- **The strategy template** (0.18.4): its `SETUP.md` note for the agent hands step 1 to
  `init-strategy`.

## [1.7.1] - 2026-10-09
When your interview ends, your researcher first recommends a document to read together, and tells
you everything else it can do only at the end.

**What to do differently:** say `update` in your home.
### Changed
- **The hand-over recommends a first document, and keeps the rest for the end** (`interview`
  2.10.0). After who and where, the one question, `First step`, opens with *My first
  recommendation: give me something to read*, says where your `Sources` folder is, and offers *I
  have a document (recommended)*, *Suggest a reading* (with Finance among your domains) and
  *Later*. Only once that is done or put off does it list what else you can ask for, the link to
  `USE-CASES.md`, the one next thing — a `philosophy` round named for a new conversation — and
  `next`. `philosophy` (1.3.2), the reading map (`read` 0.12.5) and `SETUP.md` follow.

## [1.7.0] - 2026-10-09
Your first interview no longer asks for a go: it writes your researcher once you answer its two
questions, and then invites your first books and papers into its library.

**What to do differently:** say `update` in your home.
### Changed
- **No *Write it?* on a first interview** (`interview` 2.9.0): choosing the home, or running the
  interview by name, and the two answers are the go. It writes `RESEARCHER.md`, the agent, the
  researcher's skill, its settings, the copyright and the README's opening, sets itself up and
  saves, then names in the hand-over what it wrote and proposed — your domains, your projects, the
  README's opening — to change on your word; a change asked for there is written and saved at once.
  `interview force`, which rewrites words already yours, keeps its preview and its `Go?`.
- **The hand-over's last question is *First step*** (*Primer paso*), never a bare *Start?*: it
  invites you to put the books, papers, articles and notes you want read in your home's `Sources`
  folder — in `Books`, `Papers` or `Clippings`, its full path written out — or to attach them, one
  at a time read with you; *I have a document* always comes first, and *Later* says how to add them
  any time. `philosophy` (1.3.1), its question bank and `SETUP.md` follow the new name;
  `init-researcher` (0.8.1) says at `Where?` that *Go* also sets the researcher up.
- **The home's rules, the README and `USE-CASES.md`** say the first interview writes on its two
  answers (home template 0.24.1).

## [1.6.0] - 2026-10-09
After you name your researcher and choose its folder, the interview starts by itself again.

**What to do differently:** say `update` in your home. If you already have a researcher, saying
`init-researcher` now asks whether to use it here or make a second one.
### Fixed
- **No stop between *Go* and the interview's first question.** `init-researcher` (0.8.0) runs the
  update, the copy and the interview in the same turn: the first message after *Go* is question 1,
  never a report that the home is made or an offer to stop. Its progress notes go out with a
  command; a failed update or `add` is a note, then it goes on; a folder refused, or copied into
  already, is answered at once; a file it cannot find is looked for, never a stop. The interview
  (2.8.0), handed over, checks without a word of its own, takes the name already chosen, and asks a
  missing owner name inside question 1, reading and writing the new home by its full path wherever
  the session is open. `SETUP.md` says the same.
### Changed
- **A researcher already made is offered first.** `init-researcher` and `SETUP.md` look for one
  and ask once, `Another?`: *Use <Name>* (installs it for this assistant), *Make a second one* (a
  test, or another person — a second researcher in every session until removed) or *Stop*. Asking
  for a test researcher skips the question. A second one can never take the first one's name or
  file names, case and all, so a test cannot overwrite your researcher.
- **`CONTRIBUTING.md`**'s release walk makes a second researcher in the throwaway home and checks
  the first is untouched.

## [1.5.0] - 2026-10-09
The worked examples now sit by kind, like the templates, so more can join golden-flow, and `init-
example` asks which when there is more than one.

**What to do differently:** nothing; say `update` in your home, and `init-example` copies
golden-flow as before.
### Changed
- **The worked example moved** from `examples/golden-flow/` to `examples/strategy/golden-flow/`, as
  the templates sit in `templates/<kind>/`; a new example is a folder `examples/<kind>/<name>/`,
  offered with nothing to register. The strategy is still `golden-flow`, its frozen book unchanged
  (every file a pure rename, its hashes still matching).
- **`init-example`** (0.5.0): with one example it is copied as before; with several it asks which,
  through the question tool or as a numbered list in chat, each option the example's name and its
  line read from the package; `init-example <name>` copies that one without asking, and
  `init-example <kind>` chooses among that kind only. The interview (2.7.1) hands it `strategy`.
- **`scaffold.py`** (`init-strategy` 0.3.4): `examples [--kind <kind>]` lists every example,
  `<kind>/<name> — <line>`, the line from its README; `example <destination> [--name <name>]`
  copies the one chosen, and with several and none named copies nothing and lists them. The first
  version's message is built per example, unchanged for golden-flow.
- **Paths updated** in `alpha-decomposition` (0.4.2), `data-analyzer-runs` (0.2.4),
  `experiment-lifecycle` (0.14.5, with `references/structure.md` at template 0.18.3),
  `paper-trading-gate` (0.4.2), the root `AGENTS.md`, `CONTRIBUTING.md` (its checks loop over
  `examples/strategy/*/`) and the README; the strategy template (0.18.3) and the example (0.17.1)
  point their links to the new place.

## [1.4.0] - 2026-10-08
Your researcher now reaches every assistant you install it on, Codex included, and the install runs
start to finish in one conversation.

**What to do differently:** say `update` in your home. Then, on every other assistant you use your
researcher with — Codex, Gemini, Cursor, Copilot — paste the README's install line there once: it
puts that assistant on APM's list and brings your researcher back to it, without making a second
one.
### Fixed
- **A second assistant no longer loses the researcher.** APM records an assistant in
  `~/.apm/apm.yml` only when the first install creates that file; a later install or update without
  `--target` then removed every file of an assistant not on the list — Codex after Claude, or Claude
  after Codex — with no error. A new script, `init-researcher`'s `scripts/user_targets.py`, adds the
  assistant in use to that list (`add`) before every install and update, and confirms the
  researcher's files are on disk for it (`check`). `SETUP.md` step 2, `init-researcher` (0.7.0),
  `interview` (2.7.0), `next` (1.8.5) and `update` run it; `next`'s row 3 passes on `check`, never
  on `apm deps list -g` alone. Measured in a throwaway home: Claude then Codex, the reverse, each of
  the seven assistants alone, a list with no assistants, and the recovery after the old loss.
- **The install no longer stops after the package is in.** The README's line asks for the whole
  setup, start to finish in one conversation, without asking first; `SETUP.md` says done is step 6,
  never reports the install on its own, goes straight to the name, never asks for a restart or a new
  session before the end, and reads every file by a `$HOME` path. Without a question tool, Codex and
  Gemini ask every choice as a numbered list in chat. The language menu is unchanged.
### Changed
- **If you already have a researcher,** pasting the line in another assistant installs that
  researcher there instead of making a second — the way back for a Codex that lost it.
- **The researcher's skill** (0.4.3) puts its triggers first — every session, a greeting, its name,
  *what now* — so they survive an assistant shortening skill descriptions.
- **Home template 0.24.0:** `AGENTS.md` opens by saying to read `RESEARCHER.md` before the first
  answer, and keeps its rules within the first 32 KB that Codex reads; a new `GEMINI.md` loads both
  for Gemini, as `CLAUDE.md` does for Claude.
- **`SETUP.md`'s Troubleshooting** is corrected to what was measured; **the README** names Cursor
  and the Copilot CLI; **`CONTRIBUTING.md`**'s release walk installs for two assistants in both
  orders and checks both.

## [1.3.5] - 2026-10-08
The line you paste to install now tells your assistant to go ahead, so it installs straight after
you choose your language.

**What to do differently:** when you share the install, share the new line in the README's
*Install* section.
### Changed
- **The README's install line** says it in the user's own words: install the repo and everything it
  needs, no need to ask before installing. An assistant takes permission from what the user says,
  never from a file it downloads, so the rule in `SETUP.md` alone did not stop it asking.
- **`SETUP.md`** quotes the new line, and treats the older *please help me install this repo* the
  same way.

## [1.3.4] - 2026-10-08
After you choose your language, the install goes straight on: it no longer asks whether to install.

**What to do differently:** nothing; a new install runs this way.
### Changed
- **`SETUP.md`**: the line you pasted is the go. Once the language is chosen, the assistant installs
  git and uv when missing, then the package, saying in one line what each step does; your
  assistant's own prompt to allow a command is the only thing you answer.

## [1.3.3] - 2026-10-08
Your researcher is named with a warm welcome: one line on what it will be for you, then the name.

**What to do differently:** nothing; a new researcher is named this way.
### Changed
- **`init-researcher`** (0.6.4): before *What would you like to call it?*, one warm line in your
  language — your researcher will be your companion for your work and your projects, called by its
  name in any folder — and each of the three names it proposes says a few words on its feel. The
  language menu before it is unchanged.

## [1.3.2] - 2026-10-08
When a downloaded value looks wrong, your researcher tells the data provider's error from a
library's, and says where to report each.

**What to do differently:** say `update` in your home. A wrong value in your data goes to your data
provider, not to the Data Curator's issues, unless the provider's raw value is right.
### Changed
- **`data-curator-custom-calculations`** (0.4.2): *When a value looks wrong* — find the provider's
  raw value; wrong already, it is the provider's, recorded in `Universe/Data_Issues.csv` and
  reported to the provider; right, and the Curator's output wrong, it is the library's, reported on
  its issues. FMP's 2025 split volumes (ORLY, NOW, TPL) are named as a known provider fault, which
  the Data Curator's maintainers confirmed in KaxaNuk/Data-Curator#36.
- **`universe-point-in-time`** (0.3.2): a register row is the provider's data, reported to the
  provider; the split row says it is FMP's.
- **`next`** (1.8.4): its Lab reference says where a wrong value goes. **The README**'s Lab section
  says the same in one line.

## [1.3.1] - 2026-10-08
Your researcher writes its notes and documents in your language, and keeps code, file names and the
headings its skills read in English.

**What to do differently:** say `update` in your home (home template 0.23.1). Nothing else changes:
notes you already have stay as they are.
### Changed
- **One rule for language.** Notes, concept and synthesis pages, studies and a strategy's documents
  — `OBJECTIVE.md`, blueprints, journal entries — are written in the owner's language, the one
  *How it speaks* names, unless a strategy's `AGENTS.md` names one language for its team; a
  source's own terms and quotes stay as written. Code — names, docstrings, comments, commit
  messages — folder and file names, frontmatter fields and every heading a skill reads by name,
  such as a note's `## Why it is here` and `## What it changes`, stay in English, so every skill
  works in any language. In the home's `AGENTS.md`, `read`'s note format (`read` 0.12.4),
  `how-we-work` (0.5.3) and `experiment-lifecycle` (0.14.4), which asked for English documents.

## [1.3.0] - 2026-10-08
A friendlier start built around your work and your projects, and `philosophy` now writes down how
you work, in any field, not only how you invest.

**What to do differently:** say `update` in your home (home template 0.23.0, researcher's skill
0.4.2). Your rules and your `HOW-I-INVEST.md` stay as they are. To write down how you work, say
`philosophy my work`.
### Changed
- **Your researcher is a companion for your work and your projects first.** The README opens that
  way — when you want, it teaches you to invest, and if investing is why you came it has every tool
  for it — its example asks about your work, and `USE-CASES.md` puts work and personal uses first,
  then the investing ones. The README is in English only, its Spanish install section gone: the
  install asks your language first, any you choose, and its badge says so.
- **`interview`** (2.6.0) asks only who you are, how your researcher should speak — each voice with
  a short description — and *What brings you here?* (*¿Qué te trae por aquí?*), in everyday words:
  *Help with my work and my projects* first, then *Learn about investing from scratch*, *Build and
  test an investment strategy* and *Write down how I invest*, written to `RESEARCHER.md` in the
  words the other skills read. The preview shows your own picks, in plain words. The hand-over says
  who it is and where it lives, lists what you can ask it — work and projects first, then lessons,
  `philosophy` and the investing tools — with a link to more on each, step by step, then the one
  next thing and `Start?`. A work pick leads the next thing. Spanish words about you stay
  gender-neutral.
- **`philosophy`** (1.3.0) is about how you work, in any field, or how you invest: its first
  question, *About?*, suggests one from what you told the interview, and `philosophy my work` or
  `philosophy investing` skips it. A round on your work asks why you do it, what you believe about
  your field, what you have learned, how you decide and what would change your mind — about ten
  minutes, no level, no reading list about markets — and writes your words to
  `Philosophy/HOW-I-WORK.md`. Each topic keeps its own rounds.
- **Your rules are asked in `philosophy`**, on either topic, never at the first interview: keep the
  three, add one of your own, change or drop one, and, when you are here to build a strategy, the
  two for strategies — in plain words, written under *Non-negotiables* on your go. A rule about
  your holdings — from `philosophy` or *remember this* — goes to `Portfolio/RULES.md`, where the
  brief reads it. *In your own words?* follows only a hunch or a stance pick.
- **A new home ships no investing file and no rules of its own**: `philosophy` starts
  `HOW-I-WORK.md` or `HOW-I-INVEST.md` with its title and headings when a round needs it, and the
  first rule written replaces *None yet.* Placing an order or moving money joins the home's hard
  don'ts.
- **Offered to everyone.** `next` (1.8.3) and `teach` close with `philosophy` for every home, worded
  for how you work or how you invest; `next` and the interview hand it the topic. `read` (0.12.3)
  asks whether a source changes your view in your file in `Philosophy/`, and finds *None yet.* and
  *none* in any language; `query` (0.9.3) compares rounds on one topic at a time; `refine` and
  `study` name either file; `init-researcher` (0.6.3) says `philosophy` asks how you work or invest.
  The researcher's skill (0.4.2) points a holdings rule to `Portfolio/RULES.md`.
- **`update`** no longer compares `HOW-I-INVEST.md`'s headings: a home keeps its own. **`backup`**
  (0.1.4): the interview's list of uses names it in one line, never as an offer. **`challenge`**
  says why it never reads numbers from the engines' workbooks.
- **`SETUP.md`**, the READMEs and `CONTRIBUTING.md` describe the shorter interview, its hand-over
  and the open `philosophy`.

## [1.2.0] - 2026-10-08
Start a Python library of your own, laid out like the KaxaNuk Data Curator: tests, docs and a
workflow that publishes it, ready from the first day.

**What to do differently:** say `update` in your home. Then `init-python-library <name>` makes a
new Python library beside your other folders, and `next`, in it, names the one next thing.
### Added
- **`init-python-library`** (0.1.0) and **`templates/python-library/`**, the KaxaNuk Python Library
  Template 0.1.0, laid out like the KaxaNuk Data Curator, <https://github.com/KaxaNuk/Data-Curator>:
  `src/` with one example module and its error, pytest, ruff and mypy, Sphinx with MyST for Read
  the Docs, and a GitHub Actions workflow that tests Python 3.12 to 3.14 and publishes a `vX.Y.Z`
  tag to PyPI by trusted publishing, with no stored token. Its `AGENTS.md` names Bloom Code and
  carries the starting-point marker and a `## Next` table that `next` reads.
- **Naming it**: the skill shows the four names one name gives and whether PyPI has it;
  `scaffold.py` copies the template, and the skill's own `scripts/name_library.py` names the copy —
  it moves the package folder and substitutes names only, writing no text of its own. It refuses
  the template itself, anything but a fresh copy, a name another project holds on PyPI (unless the
  library stays unpublished), a reserved, built-in or Windows device name, a tool's own name, and a
  name over 40 characters.
### Changed
- **`scaffold.py`** copies a fourth starting point, `python-library`, and its texts and cache list
  say so (`init-strategy` 0.3.3).
- **`next`** (1.8.2) names `init-python-library` among the skills that make a folder.
- **The README**'s use and skills tables gain it, and *Coming next* keeps valuation, M&A and
  budgets; **`USE-CASES.md`** gains a twelfth way; **`CONTRIBUTING.md`** shows the layout, how to
  try the template and the release check at 22 skills; the root **`AGENTS.md`** gives the
  template's row, what changes together, and the starting-point rule its example;
  **`how-we-work`** (0.5.2) says a Python library keeps Keep a Changelog and its version in
  its `__init__.py`.
- **The root `.gitignore`** keeps a template's `uv.lock` out of the package.

## [1.1.0] - 2026-10-08
Eleven ways to use your researcher, a safer copy on GitHub, and a worked example made of tickers
and dates only. Two people walked the install end to end, in English on Claude and in Spanish on
Codex; what they stumbled on is fixed, and the new `USE-CASES.md` shows, step by step, a brief on
the days you choose, working toward a goal, watching your holdings beside your own rules and more.

**What to do differently:** say `update` in your home, then once more in a new conversation (home
template 0.22.1). For the new worked example, run `init-example` again, into a new folder. A clone
of this repository made before 2026-10-08 is cloned again: its history was rewritten to take
vendor data out, and every tag now points at the rewritten commit with the same files.
### Added
- **`USE-CASES.md`**: eleven ways to use your researcher, each with what you say, what it writes
  and what it never does; the README links it and `CONTRIBUTING.md` lists it.
- **The README** opens with a table of badges, as the Data Curator's does — the assistants it works
  with, the licence, the version, the APM it installs with, its two languages — and *Coming next*
  adds a template for building a Python library of your own.
- **Licence requests carry *via KaxaNuk Researcher* in their subject**, in every line that sends
  you to `lab@kaxanuk.mx` for a licence or access, so a request the researcher brings can be told.
- **Root `AGENTS.md`**, for maintainers: the worked example's seed follows its index, refreshed as
  an example release; a new worked example — an ETF strategy, or one users ask for — is a folder of
  its own under `examples/`.
### Changed
- **The Investment Lab, said the same way everywhere**: the Data Curator is open source and free;
  the Backtest Engine, Attribution Analysis and Portfolio Construction — and the Data Refinery and
  the Data Analyzer when they ship — come together, with their licences, in the KaxaNuk Investment
  Lab, which KaxaNuk sells. `references/investment-lab.md`, `backtest-engine-runs` (0.3.1),
  `attribution-analysis-runs` (0.4.1), `portfolio-construction-runs` (0.4.1), `init-example`, the
  README, the home's README and the strategy template and worked example. An access line that
  names more than one library asks which library and what it is for.
- **The worked example** (0.17.0) carries tickers and dates only: its seed is the 883 listings
  whose FMP symbol is the index's own ticker, departed names included, in four columns —
  `main_identifier`, `index_identifier`, `valid_from`, `valid_to` — with no ISIN, company name or
  match label; `Universe/seed.py` writes it so. The frozen book's seed is the same file, so it no
  longer matches `FREEZE.json`, and the daily run reports it. The example says it can run, for
  learning, on Yahoo Finance through the Data Curator's extension — with the survivorship bias of
  the 178 names that left the index, and without the unadjusted prices and VWAP its traded value,
  fills and commission need; a precise experiment uses another provider. The strategy template
  (0.18.2) changes in wording only. `universe-point-in-time` (0.3.1) and `experiment-lifecycle`
  (0.14.3) follow.
- **The `LICENSE`** of the package, the strategy template and the worked example takes the Data
  Curator's form, *Copyright since 2026 KaxaNuk SC*, with the same MIT terms.
- **Your first hello after the install asks nothing**: `interview` (2.5.1) moves the weekly version
  check a week on when `init-researcher`'s update succeeded. *Quit and reopen your assistant* is
  said only when the setup installed git or uv, and only for the next conversation.
- **Every save lands in the right folder, wherever the conversation is open**: `read` (0.12.2),
  `query` (0.9.2), `study`, `teach`, `refine`, `refresh-index`, `audit`, `objective`, `blueprint`,
  `challenge`, `philosophy` (1.2.2), `update`, `next` (1.8.1) and `backup` run every git command
  in your home or the strategy, the send included, and set a name and an e-mail there only; each
  save takes only its own files. At home, `read` saves the text clipping a note was read from.
- **A domain of two words gets one folder name**, `Knowledge/Personal_Finance/`, headed as
  `RESEARCHER.md` spells it — in the home's `AGENTS.md`, `read`'s note convention and
  `refresh-index`.
### Fixed
- **`backup`** (0.1.3): a copy made on github.com without `gh` is checked private before anything
  is sent — counted private only when GitHub refuses it to an anonymous request; any other failure
  sends nothing and says so; no sign-in prompt opens on the way; a mistyped address is forgotten
  and asked for again; the e-mail question comes once the copy exists.
- **`init-researcher`** (0.6.2): a folder that already ends in the researcher's name becomes the
  home itself, never nested. **`init-example`** (0.4.3): where a copy already is, it says so and
  offers it. **`philosophy`** (1.2.2): a round stopped early still names the study it promised.
  **`objective`**: its leads stay in `OBJECTIVE.md`, as it says. **`next`** (1.8.1): from a
  project the researcher joined, it reads and saves your home.
- **The 1.0.0 entry** says the README ran 1,397 words before the developers' link; at 1.0.0 it ran
  1,423.
### Removed
- **Vendor data, from the files and from history**: the FMP ISINs, company names and match labels
  of the worked example's seed, and the FMP security master an older example committed on
  2026-09-25 and deleted the same day. The repository's history is rewritten without them.

## [1.0.0] - 2026-10-08
Your own research companion, for every project you work on, with investment research as its home
ground. You teach it who you are and how you work; it keeps what you read and comes with you to any
folder. The first stable release: the README says in one page what it is, how to install it and how
to remove it, and your home's README teaches six habits for working well with it.

**What to do differently:** say `update` in your home, then once more in a new conversation — the
first brings this version, and the second, run by it, brings your researcher's skill as this
version writes it and, on Gemini or Windsurf, your researcher itself (home template 0.22.0).

**Since 0.34.1**, one line each:
- **0.35.0** — APM moves to 0.33.0, which installs the package cleanly on Windows.
- **0.36.0** — your researcher saves your work for you; `backup` keeps a copy on GitHub, only
  when you ask.
- **0.37.0** — the Lab skills know the Lab's newest builds; KaxaNuk's Python style applies only
  in KaxaNuk's repositories.
- **0.38.0** — a word, at most once a week, when a new version of your researcher or of a Lab
  library is out.
- **0.39.0** — three traps a live strategy fell into are caught for every strategy.
- **0.40.0** — a new strategy says what to expect on its first day; the worked example does what
  its pages promise.
- **0.41.0** — a shorter, warmer start: two questions about you, then one next thing; say
  *remember this* and your researcher keeps the rule.
### Added
- **`CONTRIBUTING.md`**: the install by hand and the APM pin, the path after the install, what the
  repository holds and owns, and *Development* — moved from the README unchanged; `AGENTS.md`
  points at it.
- **Room for the starting points to come**: the root `AGENTS.md` gives the rule a new one follows
  — a folder under `templates/` that `scaffold.py` copies, an `init-<kind>` skill, the marker line
  `<!-- kaxanuk-starting-point: <kind> -->` and a `## Next` table in its `AGENTS.md`;
  `Bibliotheca/` stays a strategy's word. `next` (1.8.0) recognises such a folder by the marker
  and reads its table for the one next thing.
### Changed
- **The README** opens with what the researcher is, for anyone — train your own research companion,
  which comes with you to every project — and a four-line exchange; then the install, which says
  each assistant needs you signed in and that, with Claude, installing adds three house rules; a use
  table with *teach it how you work* and *bring it into any project*; *Its home ground: investment
  research*, what a strategy needs from outside the package and `lab@kaxanuk.mx`; *Coming next*,
  starting points for valuation (DCF, multiples), M&A and budgets; and *Removing it*, two pinned
  `apm uninstall -g` lines — tried with APM 0.33.0 on the package installed from GitHub and a home
  named *Sofía* — and the daily brief's task to delete in the app. 1,397 words up to the developers'
  link, where 0.34.1's ran 3,632 whole; *Qué es* moves into the Spanish install.
- **The skills and commands tables** keep one short line a row; the reading-map sentence, the
  pre-0.10.0 note and the two-writes paragraph leave the README, their rules staying in the home's
  `AGENTS.md`. *What it will not do* names every journal entry the researcher appends — the
  benchmark's choice, the rule read back, `challenge`'s — each on your go.
- **`study`** says what to do today with work that needs code or data: make a folder for it, open
  your assistant there and say your researcher's name.
- **`next`** (1.8.0) is tighter, no rule dropped: the Lab's access and Analytics Factory lines are
  read from `references/investment-lab.md`; its row 3 finds the skill alone on an assistant that
  takes no agent.
- **`read`** (0.12.1): the note convention gives the true reason for its fixed frontmatter —
  `audit` checks those fields.
- **The package's description** says what it is: your own research companion, with investment
  research as its home ground.
- **The home template** (0.22.0): its README teaches *Working well with your researcher* and folds
  the advanced sections away; its `AGENTS.md` says the install mechanics once, 6,537 words where
  0.34.1's held 6,541; the Lab section names the Analytics Factory.
- **What you came for stays one click away.** `interview` (2.5.0) keeps one next thing at its
  hand-over, but `Start?` also offers, before *Later*, the start of each other thing you picked —
  the worked example, the study of a project you named, or a document — four options at most. Its
  first line says where to open your assistant: in your researcher's home, or in any project of
  yours. `init-example` (0.4.2) puts `golden-flow` beside your researcher's home, which the
  interview hands it, not beside whatever folder the install conversation was open in.
- **The researcher's skill** (template 0.4.1, in `interview`) saves and sends what it learns in its
  home from any folder, and pauses the automatic sending there too.
- **Each save takes only its own files**: `objective`, `challenge`, `audit`, `refine`,
  `refresh-index`, `study`, `teach`, `read`, `philosophy` (1.2.1), `query` (0.9.1), `interview`,
  the researcher's skill and `next` end their save with the files they wrote, so a file staged by
  hand or by an editor never rides in a *Read:* or *Challenge:* version. `update` still saves the
  moves it staged.
- **`read`** (0.12.1): at home as in a strategy, the text clipping a note was read from is saved
  with its note — never a PDF, an extract or an ignored file — so the copy `backup` keeps holds it.
- **`update`**: for a home that moved or came back on a new computer, the agent's *on this
  machine* path is set to the home on the same go, shown in the plan; `backup` (0.1.2) says so for
  a new computer.
- **The name and e-mail that sign your versions** are no longer said to stay on this computer,
  since `backup` sends them with the copy: `SETUP.md`, `interview`, `init-researcher` (0.6.1),
  `init-strategy` (0.3.2), `init-example`, `read`, `philosophy`, `query`. `init-strategy` repeats
  your one sentence on the idea at its hand-over, to give again in the new strategy.
- **`SETUP.md` and the README**: uv's folder is written `$HOME/.local/bin/`, which PowerShell and
  Git Bash expand, and `scaffold.py` is named among the commands that need git first on the path;
  the README's example rule is about how your researcher speaks, its house rules apply *only in
  KaxaNuk's own projects*, it says to quit and reopen your assistant after the install, and it
  names `audit`'s log line beside the brief.
- **The home's `AGENTS.md`**: while the researcher's skill is behind the package, every greeting
  adds one line saying so, not only once a week.
- **Strategy template 0.18.1 and worked example 0.16.1**: git is installed with one command,
  `winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements`, never
  through GitHub Desktop, whose git is not on the command line; the example's README explains
  *book*, *paper trading* and *Sharpe*, and no longer offers Portfolio Construction, which it does
  not install; `experiment-lifecycle` (0.14.2) names template 0.18.1.
### Fixed
- **Gemini and Windsurf now get your researcher.** Installing a home deploys only to the assistants
  its own `apm.yml` lists under `targets:`, with APM 0.29.0 as with 0.33.0, and the template listed
  four; a Gemini or Windsurf user had the package's skills but never the researcher's own. The
  template now lists `gemini` and `windsurf`, which take the skill alone; `update` proposes a line
  the template lists and the home lacks, whatever version the home is at, and installs the home
  again; `next` sends a home missing the assistant in use to `update`; `interview` (2.5.0),
  `SETUP.md` and the home's `AGENTS.md` say an assistant must be in both lists. OpenCode stays
  out: it rejects the agent APM writes for it, as `SETUP.md` now says.
- **`backup`'s send works on macOS** (0.1.2): it used `timeout`, which macOS does not ship, so
  every automatic send there would fail and pause; git's own stall limit,
  `-c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20`, replaces it, and an ssh address is held
  the same way, never prompting (`GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=20'`);
  tried in Git Bash and PowerShell 5.1.
- **`next`** (1.8.0) tells the worked example by `<!-- example: begin -->` alone on its line, so a
  strategy still holding the template's README, which quotes the marker, is not taken for it. A
  blueprint stamped 0.39.0 or later and saved without its read-back has a way through part E: the
  read-back is appended on your go and saved alone, and E passes with a line saying it came after.
  The weekly line quotes the headline of the version it names, not whatever tops the changelog on
  GitHub; with no installed version to compare it says nothing; the next week's date is set only
  after a check that was due. In PowerShell, `next`'s and `update`'s one-liners are preceded by
  `[Console]::OutputEncoding = [Text.Encoding]::UTF8;`, so dashes and accents come through.
- **`audit`** names three writes made without a go of their own, as the home's `AGENTS.md` does.
- **`references/investment-lab.md`** and the template's README name Portfolio Construction's
  licence in the access line.
- **The daily run's Windows schedule** (template 0.18.1, example 0.16.1) is for Command Prompt, its
  days quoted; it starts `schtasks --%` in PowerShell and `MSYS_NO_PATHCONV=1 schtasks` in Git
  Bash, and the folder's path is quoted there and in the cron line, so a path with a space works.
- **`brief`** (1.0.3, since 0.36.0) and its `portfolio-rules.md`: a brief and a holding stay on this
  computer, never in a saved version.

## [0.41.0] - 2026-10-08
Getting started is shorter and warmer: two questions about you, then one next thing. The interview
now asks what you work on — at work and on your own — and what you would like a hand with,
proposes your domains and projects from what you said instead of asking for them, and hands over
in four lines and one question. Your researcher learns from you directly: say *remember this* and
it adds the rule to its own file, on your go.

**What to do differently:** say `update` in your home, then once more in a new session — the second
brings the researcher's skill that adds what you tell it to remember (home template 0.21.0).
### Changed
- **`interview`** (2.4.0): question 1 asks what you do, what you work on at work and on your own,
  what you would like a hand with, where you are with markets — *nothing yet* is fine — and what to
  stay out of; question 2 is one call of three — the voice, your rules (*Keep the three*, *Add one
  of my own*, *Change or drop one*, *Add the two strategy rules*) and why you are here. The domains
  and a row for each project named are proposed from the answer, Finance among them when it speaks
  of investing, markets or money or names no domain at all, and taken on the preview's go. The
  hand-over is four lines — who I am and that I am in every folder, my home, the one next thing,
  *lost? say `next`* — and one `Start?` question whose options follow that next thing; `Philosophy?`
  is gone. The owner becomes the holder in the home's `LICENSE`; a researcher named like a package
  skill gets another file name. *About three minutes* is said once, by `init-researcher`.
- **The *Here for* pick** *Organise what I read* becomes *Organise what I read, and help with my
  projects*, the old wording still matching in `next` (1.7.0), `read` (0.12.0), `update` and the
  interview; a project or decision named leads to `study`, which now takes the home its caller
  names.
- **The researcher's skill** (template 0.4.0) loads when you ask for help with any project, and on
  *learn this* or *remember this* appends one line to `RESEARCHER.md` itself — under *How it speaks*
  or *Non-negotiables*, in your words, on your go — and saves it in the home.
- **`init-researcher`** (0.6.0) asks the place and the go in one question; `SETUP.md`'s steps 3 and
  4 follow it, and its step 6 describes the new hand-over.
- **`philosophy`** (1.2.0): a shorter welcome; at Starter, *your goal* is a one-line follow-up to
  *why you invest* — *And by when?*, or *What for, and by when?* — asked only when that answer named
  no goal or no date; honest times (about 10 to 15 minutes at Starter, 20 to 25 at Building, 30 to
  40 at Researching); the purpose line is yours — *I'm here so you can make better investment
  decisions, by your own yardstick* — and Q15 no longer quotes KaxaNuk's position.
- **Philosophy is offered only to an investor**: `next`'s, `teach`'s and `read`'s philosophy lines
  appear when *Domains* holds Finance or *Here for* holds *Learn the basics*, *Build and test a
  strategy* or *Write down how I invest*.
- **`teach`**: a topic with no note no longer stops there — it offers up to three works, reads the
  one picked and goes straight into the topic, so the first lesson stands on a note.
- **The reading map**: the deck's conclusions are the deck's, never KaxaNuk's; the product line and
  the bootcamp-session pointers leave.
- **`update`**: the home's `LICENSE` copyright line is the owner's, never proposed back.

## [0.40.0] - 2026-10-08
A new strategy now says what to expect on its first day, and the worked example does what its
pages promise. The template's setup tells a newcomer that nothing runs yet and that the assistant
writes each file with them; the example skips the backtest cleanly without the licensed engine,
retries a rate-limited download, and opens with three plain sentences; and the copy script never
carries a key, a lock or an assistant's folder into a new strategy.

**What to do differently:** say `update` in your home. Then, in a strategy, read the template's
0.18.0 entry; run `init-example` again for the corrected example.
### Changed
- **The strategy template** (0.18.0): `SETUP.md` says nothing runs yet — every `.py` file and
  notebook says what belongs in it, and the assistant writes each with the owner in the order of
  parts A to H, reading the example's copy — and hands over to `objective`; it reads in a few
  minutes, names the assistant and the KaxaNuk Researcher among what is needed first, gives one
  allowed check of `Config/.env` that prints names and never values (Git Bash and PowerShell) and
  one plain line on opening the file; *Paper trading, daily* moves to `Paper_Trading/BITACORA.md` as
  *Running it daily*, its cron line giving uv by its full path. Experiment 1 is *the first rule*,
  not *the benchmark*, in `RESULTS.md`, `FINDINGS_1.md` and the notebook (as 0.12.0 decided); the
  notebook names `KN_ANALYTICS_PATH` and the benchmark reconciliation; `OBJECTIVE.md` speaks to its
  owner, not to a CIO; a strategy's 1.0.0 is its own first book on paper; `pandas` is capped below
  3, since every published figure ran on pandas 2 (today the lock resolves 2.3.3 either way).
- **The worked example** (0.16.0): without the Backtest Engine, or with a licence that does not
  validate, the experiment writes every weight file, prints *step 5 skipped* and reaches its Verify,
  which checks the weight files — where it used to stop on a `KeyError` though four pages said it
  skips; the universe notebook asks FMP for a profile up to four times on a rate limit; the engine
  runs on at most as many workers as the machine has cores; its README opens with three plain
  sentences, its glossary follows *How to read it*, *Run it* starts with the environment and the
  keys, and *What a correct run shows* gives each notebook's Verify line and what a copy asks.
- **`scaffold.py`** (`init-strategy` 0.3.1): a copy, whole or with `--only`, never carries
  `.claude`, `.agents`, `.codex`, `.cursor`, `.gemini`, `.opencode`, `.windsurf`, `apm_modules`,
  `uv.lock` or `Config/.env`; its first line names the package and the version it copies from.
- **`init-example`** (0.4.1) hands over in three lines, *Read*, *Run* and *Own*; the example's
  download is *about an hour and a half* wherever a skill gives it (`next`, `interview`).
- **`experiment-lifecycle`** (0.14.1), **`objective`**, **`paper-trading-gate`** (0.4.1) and
  **`how-we-work`** (0.5.1): the same
  words — a reader, not a CIO; 1.0.0 is a strategy's own first book on paper.

## [0.39.0] - 2026-10-08
Three traps a live strategy fell into are now caught for every strategy: keys that do not join,
volume counted twice at a split, and a rule written differently from the one meant. They were
issues #13, #14 and #15, found on 2026-09-25 in a copy of the old worked example.

**What to do differently:** say `update` in your home (home template 0.20.1). Then, in a strategy,
read the template's 0.17.0 entry: make the universe notebook's Verify raise on an index listing with
no seed row and on a key used twice, read the register's blocking rows as exclusions, check traded
value at every split, and let `blueprint` read the rule back to you before you say go.
### Changed
- **Keys join, or the pipeline stops** (#13): `universe-point-in-time` (0.3.0) names
  `index_identifier`, the index's own ticker in its holdings' convention, beside `main_identifier`;
  every join to the index's files goes through the two keys; another provider's convention is a map
  to write in the seed, never a coverage caveat; a shortfall is a member the provider does not
  carry, never a listing whose key did not join; and a blocking row of the register is a label until
  a stage excludes it by name. The template's universe notebook (and the example's shared cells)
  give every register row a severity, blocking first, and its Verify raises on a weighted listing
  with no seed row, a key used twice, or one ISIN on two rows over the same dates; the experiment
  notebook reads the exclusions from the register and its Verify raises if one is ever held; both
  `AGENTS.md` carry the rule.
- **Traded value at a split** (#14): the register gains *Traded value broken at a split* — at every
  split, the median traded value of the thirty trading days after against the thirty before, near
  one when the series is right, near the split factor when the provider's volume counted the split
  twice (found on FMP files of 2026-09-23 for ORLY, NOW and TPL). `data-curator-custom-calculations`
  (0.4.1) checks any volume-based column for it, `input-columns.md` says so beside the volume
  columns, and `Data/curator.py`'s docstring too. The example says, in a marked line, that its run
  predates the check.
- **The rule is read back** (#15): `blueprint` ends its plan with the rule in one plain sentence and
  one worked date's book from the refined panel — the names held, each one's rank and signal, and
  why the last name in and the first name out fall where they do, read from the panel by one query
  never saved and never a weight or a return — asks *Is this the book you mean?*, and on yes saves
  the owner's words as a `JOURNAL_N.md` entry before the blueprint. `blueprint-critic` objects to a
  blueprint with no read-back, or to one its *Rules* would not produce, judged against the words of
  *Rules*, never by recomputing the book. The home's `AGENTS.md` (template 0.20.1) names the entry
  among those the researcher writes in a strategy. `experiment-lifecycle` (0.14.0), the template's
  `AGENTS.md`, `JOURNAL_1.md`, README part E and `references/journal-template.md` name it; `next`
  (1.6.0) checks it in part E, a blueprint stamped before 0.39.0 counting without it. The example's
  `AGENTS.md` notes, in a marked paragraph, that Golden Flow's rule was read back as a sentence
  only.

## [0.38.0] - 2026-10-08
Your researcher tells you, at most once a week, when a new version of itself — or, in a strategy,
of a Lab library — is out. Without a word, most people never update; now `next` and the greeting
add one line when a newer release is out, with its headline, and `update` brings it. *Not now*
waits a month, *stop reminding me* turns it off, and offline nothing is said.

**What to do differently:** say `update` in your home, then once more in a new session: the second
brings the researcher's skill that gives the weekly word (home template 0.20.0).
### Added
- **`next`** (1.5.0), *Step 4* item 5: when the home's git config says a check is due — a week
  after the last, read with the file tool so a week with nothing due asks no permission — it
  compares the package's version in `~/.apm/apm.lock.yaml` with the newest tag on GitHub
  (`git ls-remote`, with prompts off) and, for a newer minor or major release, says in one line
  what it is, quoting the first sentence of its changelog entry (a Python one-liner, the same in Git
  Bash and PowerShell). Whatever happens, the next check is a week on (`kaxanuk.updatenext`); *not
  now* makes it a month, *stop reminding me* sets `kaxanuk.updatereminder off`. A researcher's
  skill behind the package gets its own line on every `next`, with no network.
- **`next`, in a strategy**: the Lab libraries too, on the strategy's own date
  (`kaxanuk.labnext`), never while an experiment has a saved blueprint and no findings — the
  installed builds (`uv pip list`) against the *Latest* column and each skill's `library_version`,
  and `uv lock --upgrade-package kaxanuk-data-curator --dry-run` for the Curator, one line per
  library behind, with the upgrade to make between experiments, and a word about a frozen book.
### Changed
- **The researcher's skill** (`interview` 2.3.0 writes it at 0.3.0): the greeting adds `next`'s
  version line when there is one, and *which version are you?* is answered from the lock and the
  home's changelog — the two versions a problem report to `lab@kaxanuk.mx` names. The README's and
  `investment-lab.md`'s problem-report lines say so.
- **`update`**: from a strategy it brings the package only and reports the Lab libraries, writing
  nothing there; it reads only the changelog entries above the installed version, never the whole
  file, through a Python one-liner that works in PowerShell too (`curl` and the web fetch are
  gone); it judges the researcher's skill against `interview` on GitHub, so one run brings a newer
  skill; it says when an experiment sits between its blueprint and its findings; and it moves the
  weekly date on after the package update.
- **`init-strategy`** (0.3.0) and **`init-example`** (0.4.0): one plan line when a newer package is
  out — `update` first brings the newest template or example — never a question of its own.
- **`how-we-work`** (0.5.0) and **`AGENTS.md`**: a release's tag message is
  `X.Y.Z: <the entry's first sentence>`, the line the weekly word quotes; a *What to do
  differently* line says what the owner says, never the `apm` command `update` runs; nothing
  reaches `main` without its version, since `apm update -g` installs `main` as it stands.
- **The home template** (0.20.0): `AGENTS.md` names the third write without a go — the dates of
  the weekly check, in the home's git config, never saved or sent — and the greeting's extra line;
  `README.md`'s *Stay current* describes the reminder.
- **The strategy template** (0.16.0) and **the example** (0.15.6): `AGENTS.md` makes a new Lab
  library build a change-set between experiments, its weekly check's date in the strategy's git
  config; `SETUP.md` step 2 says how to take one; `experiment-lifecycle` (0.13.2)'s
  `references/structure.md` names template 0.16.0. The README's `next` row says the one thing it
  writes, the date of that check.
### Fixed
- **`blueprint`'s stamp and `challenge`'s comparison** read the package's entry of
  `~/.apm/apm.lock.yaml` by the rule `next` and `update` use — its `repo_url`, ignoring case, never
  a home's local entry — where *the entry named `kaxanuk-researcher`* could pick a home made before
  `interview` renamed its `apm.yml`.

## [0.37.0] - 2026-10-08
The Lab skills know the Lab's newest builds, and KaxaNuk's Python style stays in KaxaNuk's
repositories. Backtest Engine 0.67.0, Portfolio Construction 2.0.0 and Attribution Analysis 0.3.0
shipped in the last days of September; each skill now says what changed in its build, from the
library's changelog, while its traps stay marked as checked on the build a run proved. And the
Bloom Code and PEP 8 rules, installed for the whole machine, no longer reach a user's own Python
projects.

**What to do differently:** say `update` in your home (home template 0.19.1). In a strategy that
uses Portfolio Construction 2.0.0, add `KNPC_API_KEY_KAXANUK` — its licence — to the environment
or a `.kaxanuk_license` file, as `portfolio-construction-runs` says; on any licensed library's new
build, the first run needs the network. The test-writing rule leaves your machine with the update.
### Changed
- **`backtest-engine-runs`** (0.3.0), **`attribution-analysis-runs`** (0.4.0) and
  **`portfolio-construction-runs`** (0.4.0) each gain a *Changed in <build>* paragraph, from the
  library's changelog and not yet checked by a run here: the shared `kaxanuk-license-client` from
  the private index; 3 days offline instead of 7, and a rejection that is final; saved checks in a
  new folder, so the first run after upgrading needs the network; `.kaxanuk_license` read as a
  `.env` file; a keyword-only `ValidationResult`; the engine's `main()` returning a licence that
  does not validate as `success=False`; and Portfolio Construction licensed — `run_pipeline()` and
  its entry scripts check `KNPC_API_KEY_KAXANUK`, from the environment or `.kaxanuk_license`, never
  `Config/.env`, while whether `build_allocator`, the template's per-date route, checks it is
  marked unverified. Each `library_version` stays at the build its traps were checked on (0.66.0,
  0.2.0, 1.28.0).
- **`references/investment-lab.md`** (`next` 1.4.1): a *Latest* column — Data Curator 0.50.0,
  Backtest Engine 0.67.0, Portfolio Construction 2.0.0, Attribution Analysis 0.3.0 — the package's
  record of each newest build, apart from each skill's `library_version`; one definition of the
  Investment Lab, its six libraries running steps 3 to 6, in `investment-lab.md`,
  `experiment-lifecycle` (0.13.1) and the strategy template's README; Portfolio Construction on
  request and licensed since 2.0.0, there, in the README and in the home's README.
  `data-analyzer-runs` (0.2.3) says the Analyzer is one of the two Lab modules still hand-rolled,
  the only one in a notebook; `universe-point-in-time` (0.2.1) sends downloading prices to the Data
  stage, `Data/curator.py`, with `data-curator-custom-calculations`.
- **`data-curator-custom-calculations`** (0.4.0) records `library_version: 0.50.0` with the other
  library skills' rule, and gains *The library*: on PyPI, installed by `uv sync`, upgraded only
  between experiments, and a frozen paper book stopping on any other Curator. Its `template.py`
  passes the Bloom Code check (it failed ten rules), `conventions.md` follows the strategy's style,
  and the references import the package with qualified names.
- **`paper-trading-gate`** (0.4.0): a library upgrade is a change to every frozen book — a new Data
  Curator stops each with `unfrozen-input`, a new engine reprices the record — made only on the
  owner's go, and a book that must move to a new build is frozen again as a new book.
- **The house rules apply in KaxaNuk repositories only**: `python-bloom-code` (2.2.0),
  `python-pep8` (2.1.0) and `bloom-code-lint` (0.2.0) say they apply in a Lab library, a strategy,
  this package, or a repository whose `AGENTS.md`, `CLAUDE.md` or README names Bloom Code, and that
  elsewhere the project's own style holds. The README, `SETUP.md` and the home's `AGENTS.md` say so.
- **The Bloom Code checker** skips `.venv`, `venv`, `.git`, `apm_modules`, `__pycache__`,
  `.ruff_cache`, `node_modules` and `.ipynb_checkpoints` in a folder it walks, so a run on a
  strategy's root checks the strategy's own files. `alpha-decomposition`'s counterfactual snippets
  (0.4.1) are in Bloom form and build the same books.
- **The strategy template** (0.15.1) and **the example** (0.15.5): `Config/.env.template` gains
  `KNPC_API_KEY_KAXANUK`; `SETUP.md` step 3 names it, and its *Paper trading, daily* says a saved
  licence check covers 3 days offline from Backtest Engine 0.67.0 (7 before); `BITACORA.md` puts
  paper trading inside the repository, not the Lab.
- **`AGENTS.md`**: a section *When a Lab library or an Analytics Factory file changes* — read the
  changelog, record the build in *Latest* with a *Changed in* paragraph, move `library_version`
  only after a run, one release for the skill, the template, the example and every quoted figure.
### Removed
- **`python-test-writing`**: it applied only to `tests/` folders, which nothing the package ships
  has had since 0.29.0, and reached a user's other projects. APM removes it on the next install or
  update (measured with 0.29.0 and 0.33.0: *Cleaned 1 stale file*). The install deploys 3 rules.
### Fixed
- **`backup`** (0.1.1): its github.com way, which 0.36.0 left as one line past 100 columns, is
  wrapped; nothing it says changes.
- **`backtest-engine-runs`** no longer calls `KNPC_API_KEY_KAXANUK` a stale spelling of the
  engine's key: it is Portfolio Construction's licence. The engine reads only
  `KNBE_API_KEY_KAXANUK`; neither is renamed into the other.

## [0.36.0] - 2026-10-08
Your researcher saves your work for you, and keeps a copy on GitHub only when you ask. Testers
asked what *commit* means: no skill asks it any more. The go you give a plan also saves a version
of what it wrote, at home and in a strategy, and the researcher says *Saved*; a new skill,
`backup`, puts the home — or a strategy — on a private GitHub repository when you say *keep a
copy*, and brings it back on a new computer.

**What to do differently:** say `update` in your home — it shows the changes to `AGENTS.md` and
`README.md` as a diff (home template 0.19.0).
### Added
- **`backup`**, a new skill: on *keep a copy*, *back up*, *a new computer* or *what is a commit*,
  it makes a private GitHub repository of the home or of one strategy — with `gh` when it is signed
  in, else an empty private repository the owner creates on github.com, else GitHub Desktop —
  offers GitHub's private *noreply* e-mail, asks once whether to send each new version there
  (`git config kaxanuk.autosend`), and says what the copy holds and what stays on the computer by
  design (the PDFs, `Extracts/`, `Briefs/`, `Portfolio/`, any `.env`). A send never forces, pulls
  or merges; a failed one keeps the version here, says so in one line and pauses sending. An
  existing copy is checked to be private before anything is sent to it. It is never offered
  unasked, and no hand-over mentions it. The package deploys 21 skills.
### Changed
- **Every write saves a version on its own go**: `read`, `philosophy`, `query`, `interview`,
  `study`, `teach`, `refine`, `refresh-index`, `audit` (on the go of running it), `update`,
  `objective`, `blueprint` and `challenge` add the files they wrote by name, never `--all` and never
  an ignored path, commit them and say *Saved* — the `Commit?` question, *Commit it for me*, *I'll
  review it first* and the git commands shown to the owner are gone. `Save?` (*Save this version* /
  *Not now*) is asked only where no go covers a save: changes made by hand, which `next` finds, and
  an unsaved home before `update`. A missing name and e-mail are asked for in plain words and set in
  that folder only; a folder with no versions is told so, and `next` starts them on the owner's
  word. Each skill says it replaces an older home's *Commit?* question.
- **In a strategy** (`AGENTS.md` of the template and the example, `how-we-work`): a document the
  researcher writes on the owner's go — a note, `OBJECTIVE.md`, `BLUEPRINT_N.md`, a journal entry, a
  log line — is saved as its own version with no `CHANGELOG.md` entry, bump or ruff gate; the
  blueprint is saved alone, before any rule is coded (*Saved: your proof the idea came before the
  result*); the go is the owner's signature, on which the assistant removes the template's
  blockquote. `next`'s row E and `experiment-lifecycle` say the same.
- **No hand-over mentions a copy**: `init-researcher`, `init-strategy` and the strategy's
  `SETUP.md` lose their lines about pushing, a remote or publishing; the root README and the home
  README say once that `backup` exists.
- **Plain words for git's identity**: the install and every `init-*` ask for *a name and an e-mail
  to sign the versions your researcher saves*.
- **The home template** (0.19.0): `AGENTS.md`'s *Plan first, then write* says every go saves a
  version, and a new *Versions* paragraph gives the words to use and the send; `README.md`'s *Save
  a copy off this computer*, which asked the owner to type `git remote` and `git push`, becomes
  *Keep a copy off this computer*, with no command.
- **The strategy template** (0.15.0) and **the example** (0.15.4): the shared `AGENTS.md` and
  `SETUP.md` lines above; in the example only, a marked line says an untracked `uv.lock` after
  `uv sync` is expected.
### Fixed
- **`read`'s save** names only files git keeps, so an image or office file copied into `Sources/`
  no longer makes it fail.
- **`challenge`, check 10** dated the blueprint by the commit that added its file — for Experiment 1
  the template's first commit, so every cited note came out as read too late. It reads the commit
  that wrote the *Written* line instead.
### Removed
- **`teach`'s by-hand `mkdir` and `git mv`** for a topic still in `Projects/Teach/`: `update` moves
  it, on the owner's go.

## [0.35.0] - 2026-10-08
APM moves to 0.33.0, which installs the package on Windows as cleanly as 0.29.0 did. APM 0.29.1
to 0.31.0 failed the install on Windows, its staging folders pushing the worked example's longest
paths past 260 characters; 0.32.0 shortened them (microsoft/apm#2941). Eduardo Ramos (@EERamos)
found the fix, measured it and proposed the move in pull request #24; this release redoes it on
the current tree, which had moved past the pull request. The release check now runs in a
throwaway home, so a copy of the package installed for the user can no longer stand in for the
one being checked.

**What to do differently:** say `update` in your home; once it is done, install the new APM once,
`uv tool install apm-cli==0.33.0`. Every command the package gives now names `apm-cli==0.33.0`.
### Changed
- **APM is pinned at 0.33.0** in every command that runs it — the README, `SETUP.md`, `AGENTS.md`,
  `update`, `audit`, `init-researcher`, `interview`, `next`, `philosophy`, `scaffold.py`'s message,
  `experiment-lifecycle`'s `structure.md`, the home template's `AGENTS.md` and `README.md` (home
  template 0.18.2), the strategy template's `README.md`, `SETUP.md` and `AGENTS.md` (template
  0.14.1) and the example's `SETUP.md` and `AGENTS.md` (example 0.15.3). *Why APM is pinned* says
  which versions failed and why the pin moves only after the release check passes. The commands a
  strategy names for an update, once bare `apm update -g`, which a `uvx` install leaves off the
  path, name the pin too. Measured on Windows 11, each APM in its own throwaway home, against
  0.29.0: a project-scope install, a `-g` install from GitHub and a second over it, the three
  `scaffold.py` copies from the installed package, a home with an accented name installed `-g`,
  `deps list`, `outdated` and `update -g --yes`, a user folder made with 0.29.0 updated by the new
  APM, and APM 0.29.0 reading the new APM's lock: 0.32.0 and 0.33.0 both deploy exactly what
  0.29.0 deploys — 20 skills, 9 commands, 4 rules, 1 agent — and each adds only two informational
  lines about inactive experimental targets.
- **The release check** (README *Development*, `AGENTS.md`): it runs in a shell whose home is a
  short throwaway folder, because a skill installed for the user wins over a project skill of the
  same name; it installs an archive of the tree, uncommitted changes included, with LF endings and
  no ignored folders; ruff runs on the template too, and the Bloom Code check on the template and
  the example from their own roots, at their 100 columns; and two recipes compare the template and
  the example, line by line and notebook cell by cell.
- **The package's author** in `apm.yml` is KaxaNuk, as its licence says.
- **The fork rule** finds the package's name in either case, `git grep -i kaxanuk-researcher`:
  APM writes it in lower case in its lock.
### Fixed
- **`AGENTS.md`** lists the example's `README.md` among the files the example owns whole.
### Removed
- **The root `pyproject.toml`'s `[project]` table**, which nothing read and whose version had
  stopped at 0.19.0; the file keeps the ruff settings.

## [0.34.1] - 2026-10-07
The worked example's changelog lists every figure its copy carries. Its entry for the copy left
out three figures Golden Flow 0.15.1 had corrected to the record run's outputs — figures the
example's findings already carried, and its results and a note in part — and its first line said
no number moved. No file the example reads or runs changes but its version line, and no number
moves.

**What to do differently:** nothing; `uvx --from apm-cli==0.29.0 apm update -g` brings it.
### Fixed
- **`examples/golden-flow/CHANGELOG.md`** (example 0.15.2): the copy's entry lists the realistic
  commission row's 0.43 points of CAGR, not 0.42; at most 0.12% of the index unpriced in 2022, not
  under 0.1%; and the two 2023–2026 sub-periods the sell-at-t−1 rule left unchanged. Its first
  line says the copy carries them, and it says the comment opening a module's marked code, where
  there is one, was written for the copy. A new entry records the correction; the example's
  version line is its own, apart from Golden Flow's.

## [0.34.0] - 2026-10-07
Golden Flow is the worked example. `init-example` now copies `golden-flow`: the Lab's reference
strategy, taken from the first note to a book signed into paper trading on 2026-10-06 — the most
traded members of the KN US Equity Core in a 50/200 golden cross, weighted by 63-day traded value
inside a 20% cap and a 1% floor. It is a curated copy, shorter than the example it replaces, and it
shows step by step which Lab library or Analytics Factory file each step uses. The first strategy
to reach paper trading also taught the template four things: attribution pairs each weight with
the day it earns, a crash in the daily run must not read as an ordinary day, a seed's span ends
where the security did and not where its source does, and a seed taken from an index carries two
keys and one map.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home: it shows the changed line of `README.md` (template 0.18.1) as a diff and brings it across on
your go. Run `init-example` again to read the new example; `liquid-golden-cross` stays readable at
tag `v0.33.0`. In a strategy of your own, read the strategy template's 0.14.0 entry: hold both
attribution weight tables overnight and reconcile the first cut's benchmark within a point a year
before quoting any attribution figure; in a strategy with a book on paper, catch a step that
raises in `daily_update.py` and return 2, and register the scheduled task again with the redirect
`SETUP.md` gives; install with `uv sync --group notebook --inexact`.
### Added
- **`examples/golden-flow/`**, a curated copy of Golden Flow 0.15.1. Its README says how to read
  it — `OBJECTIVE.md`, then `RESULTS.md`, then Experiment 1's blueprint and findings, then the gate
  in `Paper_Trading/BITACORA.md` — and gives the rule in one table, the Lab library or Analytics
  Factory file each step uses with the skill for doing it yourself, how to run it, what a correct
  run shows and the words it uses. Its documents keep every rule and every number they quote, and
  leave out the strategy's earlier versions, which stand in its record as one row of `RESULTS.md`
  and 37 books of its trial count. FMP is this experiment's provider. The seed, the frozen book's
  `FREEZE.json` and the files it hashes ship byte for byte, but for the frozen security master,
  the provider's data; `paper_trading_1.py` carries the template's docstring and the example's
  markers. The book is a record and does not run in a copy, as `BITACORA.md` says.
- **`AGENTS.md`**: the written exceptions to the rule that the template and the example share
  every unmarked line, and that a file only the example has is its own whole; a line copied
  verbatim from a strategy's fixed or append-only record may run past 100 columns; a change to a
  Lab library's API changes the worked example too where it uses that library, with a new example
  version and a journal entry.
### Changed
- **The strategy template (0.14.0)**, in its shared lines: attribution holds both weight tables
  overnight, reconciles its benchmark with the index's own returns, maps the index's tickers to the
  book's identifiers through the seed and compares against the members it can price; a seed taken
  from an index carries `index_identifier` beside `main_identifier`, the identifier the
  experiment's provider prices under, and `Data/hand_supplied.py` maps them; refined rows stay
  inside each security's span, and a live listing's span stays open; the panel returns one
  calendar; a scheme may size by a score inside bounds its blueprint names; a book on paper is
  priced over three windows, holds the last membership an index's files wrote, and a step that
  raises exits 2, its scheduled command keeping its output; lines that read false in a filled copy
  are worded for a new strategy. Its `CHANGELOG.md` lists each file.
- **`init-example`** (0.3.0) copies `golden-flow` into a folder named `golden-flow`, and its
  hand-over gives the reading order, the measured download time and what a run needs.
  **`init-strategy`** (0.2.2): `scaffold.py`'s example is `examples/golden-flow`.
- **The example is told by its markers alone**: `audit`, `blueprint`, `challenge`, `objective` and
  `next` (1.3.1) drop the test on the old example's README title. `next`'s facts file says the
  Analytics Factory's files may be a strategy's universe, its benchmark and attribution's inputs.
- **The skills' worked cases are Golden Flow's**, every figure from its 0.15.1 files:
  `alpha-decomposition` (0.4.0) — the arm table and its lessons, and the benchmark checked whole
  and aligned; `attribution-analysis-runs` (0.3.0) — the library pairs a weight with the return of
  its own date, so both weight tables are held overnight and the benchmark reconciled, and a zero
  price in the index's holdings reads as an infinite return; `backtest-engine-runs` (0.2.0) —
  `Daily_Weights` is struck at the close, the reserve is checked run by run, commission per share
  as measured, `references/api.md`'s values, and the engine's years counted as weekday steps over
  252; `data-analyzer-runs` (0.2.2) — the orders of magnitude of an information coefficient;
  `portfolio-construction-runs` (0.3.0) — sizing by a score inside named bounds, and the sell
  before a price series stops; `paper-trading-gate` (0.3.0) — the example's gate answered yes, a
  step that raises is a failed day, what the checks do not see, the dry run before a freeze, and
  `1.0.0` waiting for a clean-clone reproduction; `universe-point-in-time` (0.2.0) — where a span
  ends, and the main identifier chosen per experiment; `data-curator-custom-calculations` (0.3.4);
  `experiment-lifecycle` (0.12.0) and its references; `read` (0.10.2).
- **Published figures that moved in skills**: the arm table of `alpha-decomposition`, the
  commission figures and `references/api.md` values of `backtest-engine-runs`, the coefficients of
  `data-analyzer-runs` and the sample figures of `audit` are Golden Flow's.
- **An in-house strategy**: examples in this package come only from `golden-flow` as the package
  ships it, never from a live strategy repository — in `AGENTS.md` and five skills.
- **`README.md`**, the home's `README.md` (template 0.18.1) and the strategy template's README,
  `AGENTS.md` and `SETUP.md` name `golden-flow`.
### Removed
- **`examples/liquid-golden-cross/`**, readable at tag `v0.33.0`. Its four experiments'
  attribution figures came from weights paired with the return of their own date and were not run
  again.
### Notes
- **Proposed, not built: check every day since the last recorded run.** `check_market_data` would
  take the newest `as_of` the record's `runs` table holds as ran — the freeze date, before a first
  run — and read each file from the row before it to the day: the bad-print and fill-price checks
  on every row of that stretch, not the newest alone; `stopped-series`, a flag, for a name whose
  file ends before the day the cash proxy and the benchmark reached while its span, if any, is
  open, and a stop when a book held it; and `internal-gap` for a day of the benchmark's calendar
  missing inside the stretch. The stretch is a day or a weekend, so the check still costs seconds.

## [0.33.0] - 2026-10-06
A way into the Lab, and less to read. The researcher is where many people first meet KaxaNuk's
Investment Lab, yet no file named an address: a licence, access or a problem had nowhere to go but
"ask KaxaNuk". Now one address, `lab@kaxanuk.mx`, takes a licence request, an access request and a
problem report, and the Lab is named as a fact at the moment a step needs it — never as advice,
never as a pitch. Testers also found the text long: what loads in every session — the home's
`AGENTS.md`, `RESEARCHER.md` and `CLAUDE.md`, and every skill's and command's description — is
9,880 words where it was 10,907, with no rule dropped and no behaviour changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home: it shows the changes to `AGENTS.md`, `README.md` and `apm.yml` (template 0.18.0) as a diff
and brings them across on your go. If you scheduled a daily brief, run `brief setup` again, so the
task's prompt takes the new contract. For a licence, access to Portfolio Construction or the
Analytics Factory's files, write to `lab@kaxanuk.mx`, saying which library and what it is for; a
problem report names the two versions `update check` shows.
### Added
- **The Lab's access facts** — `next` (1.3.0) ships `references/investment-lab.md`: each Lab
  library, its step, what it does and how to get it — the Data Curator open source, the Data
  Refinery and the Data Analyzer coming, Portfolio Construction on request, the Backtest Engine and
  Attribution Analysis licensed — the access line, KaxaNuk's Analytics Factory at
  <https://www.kaxanuk.mx/analytics>, and where a problem report goes. It is installed with the
  package and never copied into a home or a strategy. `next`'s row G gives the access line when
  the engine or the attribution library is missing, and the Analytics Factory's line when
  attribution's index or factor files are.
- **When the Lab may be named** — a hard don't in the home's `AGENTS.md`, and the facts file's
  header: as a fact, never as advice, and naming its engines as where a strategy's numbers come
  from is one; what a library does and how to get it only when a step needs a library the owner
  lacks, or when they ask; never added unasked to `RESEARCHER.md`, `Philosophy/`, a brief, a
  study, a round of `philosophy` or a *Find first* line, and never as a reason to invest.
- **The access line where access comes up** — `backtest-engine-runs` (0.1.8),
  `attribution-analysis-runs` (0.2.10) and `portfolio-construction-runs` (0.2.6) open their
  install section with it, for an owner without a licence or access; `init-example` (0.2.2) at its
  hand-over; `README.md`'s *What a strategy needs*; the strategy template's `SETUP.md` and
  `README.md`; and the home's README, in a short section on the Lab after *The path*.
- **What it is** — two lines at the top of `README.md`, in English and in Spanish: a research and
  learning tool, never investment advice; it runs on your computer, through an assistant installed
  there; KaxaNuk receives nothing from it, and a licensed Lab library checks its licence with
  KaxaNuk.
### Changed
- **Less to read, every rule kept.** The home's `AGENTS.md` (template 0.18.0) is 401 lines where
  it was 462: each rule has one owner and the rest point to it, history went to `update` and the
  changelogs, and the Claude Code setup and how to write a skill of your own went to the home's
  README, marked optional. The descriptions of `brief` (1.0.2), `read` (0.10.1), `interview`
  (2.1.1), `philosophy` (1.0.2), `init-researcher` (0.5.2), `init-example` and `query` (0.8.1)
  are 90 to 102 words each; their bodies, and `study`, `teach` and `update`, point to the home's
  `AGENTS.md` for the go words, the commit offer, the round-file rule and how an assistant without
  a question tool asks.
- **The brief's contract** (`brief` 1.0.2): its Portfolio part says a portfolio's figures come from
  the engines the project names, and no longer names the Lab.
- **"The desk" is KaxaNuk's Analytics Factory** in the strategy template (0.13.4) and the worked
  example (0.18.4) — `SETUP.md`, `Config/.env.template` and the docstrings of
  `Data/hand_supplied.py`, `Data/curator.py` and `Experiments/attribution_analysis.py` — and in
  `attribution-analysis-runs`, `paper-trading-gate` (0.2.2) and `experiment-lifecycle`'s
  `structure.md` (0.11.1). What is read, and from where, is unchanged. The template's README gives
  each Lab module a Status column, and *Two doors* the platform's page.
- **"Licenses" meaning "supports"** is *supports* or *allows* in `blueprint`, `blueprint-critic`
  and `data-analyzer-runs` (0.2.1), so no prediction reads as needing a licence. The reading map
  labels the course deck's three conclusions as KaxaNuk's view, a view to test.
- **Codex and the home install, as APM 0.29.0 does them** — `SETUP.md`, the home's `AGENTS.md`,
  `interview` and `update`: Codex receives the skills and the agent, without its tool list, and no
  commands or instructions; installing the home copies the whole folder — `.git/`, `Sources/`,
  `Extracts/`, `Briefs/` and `Portfolio/` included — into
  `~/.apm/apm_modules/_local/<folder name>/` on the same machine, and deploys only its `.apm/`; on
  Windows a long `Extracts/` path in that copy can fail the install.
- **The four house instructions' scopes**, in `README.md`, `SETUP.md` and the home's `AGENTS.md`:
  Bloom Code and PEP 8 for every Python file, test writing for Python tests, filesystem boundaries
  for every file the assistant reads, in any project.
- **`update`** opens its report with the installed package version and the home's template
  version, even when all is current: the two a problem report names.
- **Every `apm` line you are told to run names `apm-cli==0.29.0`**, `apm.yml`'s comment, `audit`'s
  fix and `structure.md` included.
- **`README.md`**: *What a strategy needs* moves up, beside *Lost at any point?*, and names the
  Analytics Factory and the address; a question or a problem to report has one line.
### Fixed
- **`scaffold.py`**: the comment on `FILE_MANAGER_FILES` says a strategy's `.gitignore` names them
  from template 0.13.4.

## [0.32.0] - 2026-10-06
The first run lands, and the next step is clear. People who installed 0.31.0 finished setup not
knowing what to do next, and found the text long: every owner in an empty home was told to drop a
PDF, whatever they came for; a greeting in the next session had no defined answer; after a first
`read`, `next` said "commit what is there" and `update` refused, a wall for anyone who has never
used a terminal; and a researcher named *Sofía* deployed as `sofa`, because APM deletes accents
from a folder name, so `next` asked for a reinstall forever. Now the researcher names one next
thing for what the owner is *Here for*, offers to commit what it writes, copies a file the owner
attaches into `Sources/`, and keeps every name installable.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home: it offers your researcher's skill again — the greeting, commands on Codex, a slug APM keeps —
as a diff, renames the agent with it when the slug changes, and reinstalls the home. Attach a file
in chat, or name one on your computer, and the researcher copies it into `Sources/` on your go.
### Added
- **The one next thing, by *Here for*** — `next` (1.2.0) and the interview's hand-over: *Learn the
  basics* → `philosophy` at Starter, which needs no reading; *Write down how I invest* →
  `philosophy`, then `brief setup`; *Build and test a strategy* → `init-example` to read, then
  `init-strategy`; *Organise what I read*, or none → a first source, then `read`. The rest is one
  line of *also*. At home the setup checklist is one line when it passes.
- **A greeting and commands on Codex** — the researcher's skill (template 0.2.0, in `interview`
  Step 4) answers *hello* or *what now* in three lines — who is speaking, the one next thing, the
  rest by name — and, on an assistant with no commands, follows a command the owner names from its
  file in the package. `update` writes it into homes already installed, on the go.
- **`Commit?` after every write at home** — `read`, `query`'s kept page, `study`, `teach`,
  `refine`, `refresh-index`, `audit`, `update` and `next` row 0 ask *Commit it for me* or *I'll
  review it first*, as `philosophy` did; never unasked, never in a strategy, where the owner
  commits.
- **A source copied in on the go** — a file the owner attaches or names is copied into
  `Sources/Papers/`, `Books/` or `Clippings/` under its own name, never over a file: the one write
  in `Sources/`. `read` (0.10.0) does it inside its own plan, one go for both.
- **`teach` checks the library first**: with no note on the topic it writes nothing and offers
  `read`, `philosophy` or a labelled general answer; `teach` alone lists the topics in `Lessons/`.
### Changed
- **The slug** — `interview` (2.1.0), `update`, `next` and `brief` (1.0.1): accents and marks
  removed, every other character a hyphen — `Sofía` → `sofia`, `Begoña Ruiz` → `begona-ruiz`; the
  name keeps its accents everywhere else. `update` moves a skill and an agent whose slug APM would
  mangle, and removes the mangled copies.
- **The interview** (2.1.0): the hand-over is five short items — who I am, where the home is, the
  first source, the one next thing, *lost? say `next`* — with the question that serves the one next
  thing asked first, *Show me the worked example* among them; the folder table lives in the home's
  README. The preview names the fixed text instead of reprinting it. `RESEARCHER.md`'s rules and
  *How it cites* are written in the owner's language; only the headings and labels the skills look
  up stay English. The owner's name is read with `git -C "<the home>"`.
- **The go words** are one list, in the home's `AGENTS.md`: *go*, *proceed*, *ok*, *yes*, *sí*,
  *dale*, *adelante*, or the same word in the owner's language; `read`, `study`, `update`,
  `philosophy` (1.0.1) and `brief` (1.0.1) use it.
- **`scaffold.py`** (`init-strategy` 0.2.1): a destination or `--package` starting with `~` starts
  in the home folder; the console prints any alphabet; a copy the system stops partway is one
  plain line, not a traceback; a folder holding only `.DS_Store`, `Thumbs.db` or `desktop.ini`
  counts as empty, and those stay out of the first commit; the missing-package message pins APM.
  `init-researcher` (0.5.1) hands the script an absolute path.
- **`init-example`** (0.2.1) and the README: reading the worked example needs nothing; running it
  takes a data key, hours of downloads, KaxaNuk's benchmark and factor files and licences.
- **`README.md`** and **`SETUP.md`**: where to paste the install line — the Code tab of the Claude
  desktop app, Claude Code, Codex, the Gemini CLI, never a web chat — how to open the home in a new
  conversation in each, a first line for an assistant to follow `SETUP.md`; `winget` accepts its
  agreements, a tool just installed is called by its full path, and the assistant is reopened
  after installing one.
- **The home template** (0.17.0): `Sources/` takes the copy, `Plan first` the go words and the
  commit offer, *Who is speaking* the greeting, `.gitignore` `desktop.ini`; the README's path reads
  the worked example before the first strategy.

## [0.31.1] - 2026-10-06
A name whose prices are about to stop is sold the day before. A strategy built on the template found
the Backtest Engine refusing its book outright: a provider's file had a 62-day gap at a corporate
event, the book held the name through it, and the engine checks every open position on every
rebalance date. The owner's rule, now the template's: when a company is delisted or a corporate
event stops its prices, the rule triggers a rebalance at t−1 and sells it at a real price.

**What to do differently:** in a strategy's eligibility, require a price on t and on t+1, so the
book re-strikes on the last priced day; apply it to every counterfactual alike, and name the day
of hindsight it takes beside the delisting exit in `AGENTS.md`.
### Changed
- **The template's `AGENTS.md`** (and the worked example's): the look-ahead row of the five ways a
  backtest lies says a name whose prices are about to stop is sold at t−1 by a re-strike the rule
  triggers, and names that exit's day of hindsight as the one stated leak.
- **`Experiments/portfolio_construction.py`**, the template's contract and the example's docstring:
  a third timing rule, *sell before a price series stops*. The example's code takes it on its next
  run; its published numbers are unchanged until then.
- **`portfolio-construction-runs`** (0.2.5): the rule in section 5, beside lagging and
  rebalancing on change. **`backtest-engine-runs`** (0.1.7): the integrity check covers every open
  position, not only the names traded, and no configuration field waives it.
- **The template** (0.13.3) and **the worked example** (0.18.3), PATCH: nothing about any result
  changes.

## [0.31.0] - 2026-10-04
The researcher is a way in for people with any background, and its setup lost the newcomers it was
for. The interview mixed two jobs, getting to know the person and asking their market beliefs, and
its step 3, *How you see markets*, put efficient prices and published edges to them in the papers'
vocabulary before anything was explained. Setup is now about the person only, about three minutes,
and the owner's investment philosophy has a skill of its own: optional, pitched at what the owner
already knows, teaching as it asks, and taken again after reading, so the owner sees how their
view moved. What it brings a beginner is a personal benchmark — what their money does if they
never choose an investment on purpose — and a process to find out whether they do better than it.
Its purpose line, the only one the package ships: *KaxaNuk built me so that more people can make
better investment decisions.* A daily brief joins it. Issue #25.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home, and accept the new `Philosophy/` row of its `AGENTS.md` before your first round of
`philosophy`: until then the home's own rules name `interview` and `refine` as its writers. Your
`RESEARCHER.md`, `Philosophy/` and agent stay as they are; `update` lists what to carry across by
hand — a *Here for* line under *Who*, `## Why I invest` in `HOW-I-INVEST.md`, and, in a home
interviewed before `interview` 2.0.0, the line *Round files in `Philosophy/Evolution/` are a record
of how the owner's answers moved: read them for dates and levels, and cite `HOW-I-INVEST.md`, never
a round file, as the owner's view.* in your agent's *How you answer*. Add the same line, by hand,
to item 2 of your researcher's skill, then run
`uvx --from apm-cli==0.29.0 apm install -g "<the home>"` again. Before `brief setup`, let `update`
bring the `Briefs/` and `Portfolio/` lines into your `.gitignore`: `brief` stops in a home that
does not ignore them.
### Added
- **`philosophy`** (skill 1.0.0): the owner's investment philosophy, by name, as often as they
  like. The opening is the same for everyone — why you invest, what you already believe, how much
  you know — and the level, *Starter*, *Building* or *Researching*, is nested: each asks what the
  one below asks, in harder words, and more; a calibration places an owner who is not sure, and the
  home suggests a level. The personal benchmark and why a process are said once, with an honest
  caveat: nothing on the reading map shows that a process makes more money; it is how you find out
  whether a result is yours or luck. Then the level's blocks — *Scoreboard*, *Edge*, *You*, *The
  world moves*, *Proof*, *Process* — one open question per message, one line that teaches after
  each answer and never a verdict, and a pitch check after the first block. Every question takes
  *explain*, *example*, *not sure yet*, *skip*, *simpler*, *harder* and *stop*, in the owner's
  language too.
  The preview shows every line word for word; on the go it adds the owner's typed answers to
  `Philosophy/HOW-I-INVEST.md`, add-only, one bullet each tagged *(round N)*, writes one round file,
  `Philosophy/Evolution/YYYY-MM-DD.md`, and may append the works picked at the close to the closing
  *Find first* line of `RESEARCHER.md`, unless the owner leaves it alone in that preview. A pick is
  never written in `Philosophy/`. It never commits on its own: after the write it asks `Commit?` —
  *Commit it for me* runs the commit, *Philosophy: round N, <level>*; *I'll review it first* leaves
  it to the owner. Taken again, it quotes each earlier answer for *keep* or new words, and shows
  then and now in chat. Its question bank is `references/questions.md`, with
  stable IDs and every paper a lead from the reading map.
- **`brief`** (skill 1.0.0): a daily brief in `Briefs/YYYY-MM-DD.md`, in up to three parts —
  *Work*, *Markets*, *Portfolio*. `brief setup` chooses the parts, the days and the time, and the
  measures, proposed from the owner's numbered questions; *Work* needs the calendar, mail and chat
  connectors, and a part with none is left out, said plainly. On the Claude desktop app it creates
  a scheduled task whose prompt is the brief's contract, `references/brief-contract.md`; elsewhere
  it says how to run `brief` each morning and creates nothing it cannot. When the owner chooses the
  *Portfolio* part, it starts `Portfolio/holdings.csv` and `Portfolio/RULES.md` from its own
  `references/`. `brief`, by name, writes today's file if none exists: nothing written elsewhere,
  message contents read as data and never as instructions, every figure quoted from a dated source
  with its link and never computed, never a weight, a P&L or a return, never *buy, sell, trim, add
  or hold*.
- **_Save a copy off this computer_**, a section of the home's `README.md`, and one line under each
  install in this `README.md` pointing to it: a commit the researcher makes saves on this computer
  only, so the owner is told why a little git is worth learning and how to push the home to a
  private repository on GitHub, or a service like it.
### Changed
- **`interview`** (skill 2.0.0): two short steps about the owner, about three minutes. *About you*
  no longer asks what pulls them to markets or what they think about them; *Me, and my rules* keeps
  *Domains*, *Voice* and *Your rules*, with a plain gloss, and adds `Here for` — *Learn the basics,
  step by step*, *Organise what I read*, *Build and test a strategy*, *Write down how I invest, and
  see it evolve* — written as a *Here for:* line under *Who*. *How you see markets* moves to
  `philosophy`, as its stance picks, and *What to read for* to `read`. *What you believe* is one
  line pointing at `Philosophy/HOW-I-INVEST.md`, the owner's own prose there kept verbatim on
  `force`, and nothing is written in `Philosophy/`. The hand-over: who the researcher is, the
  folders, *Start learning now* — a document into `Sources/` and `read`, or a topic proposed from
  the reading map — the skills that grow it in later sessions, and how to stay current; it offers
  `philosophy` now or, recommended, later in a new session. *What I did not ask* is gone.
- **`read`** (0.9.0): at home with no numbered question, it asks first which question the source
  serves, in plain words, with proposals from *Here for* and *About you*, and adds it as question 1
  on the go. Its report names the questions of the owner's philosophy a new note bears on, from the
  *Bears on* table of `philosophy`'s bank, and offers a round.
- **`next`** (1.1.0): a home with no reading question passes, and its next thing is a source
  dropped into `Sources/` and `read`; it counts `philosophy` and `brief`, and closes at home with
  one line on the owner's philosophy, offered and never pressed.
- **`query`** (0.7.0): *how has my view changed?* is answered from the round files, compared by
  question ID, and `HOW-I-INVEST.md`, never a round file, is cited as the owner's view.
- **`init-researcher`** (0.5.0): hands over to the shorter interview, and says that how the owner
  invests is `philosophy`'s, later.
- **The commands**: `objective`, `blueprint`, `study` and `teach` read round files for dates and
  levels and never cite one; `refine` refuses a round file and keeps every *(round N)* tag; `teach`
  takes the level from the newest round and offers a round at a lesson's close; `update` puts the
  `.gitignore` lines for `Briefs/` and `Portfolio/` first and lists *Here for*, *Why I invest* and
  the agent's line on round files as lines to carry across by hand.
- **The reading map**: `philosophy` among its users — its stance picks, its hunches, and the
  discussion questions, some of the seven questions and the kill switch put to the owner as
  questions about how they invest, never as a strategy's rules; a work picked at a round's close,
  or from the interview's *Suggest a topic*, goes on the closing *Find first* line.
- **The home template** (0.16.0): `Philosophy/` has two writers — `philosophy` adds the owner's
  typed answers to `HOW-I-INVEST.md`, word for word and add-only, after the owner's go, and writes
  one round file in `Philosophy/Evolution/`, never edited afterwards; `refine` edits
  `HOW-I-INVEST.md` as an editor, diff first, and never touches `Evolution/`. `AGENTS.md` gains rows
  for `Briefs/` and `Portfolio/`, both gitignored, and the *Find first* grant; `RESEARCHER.md` a
  *Here for* line, a one-line *What you believe* and no slot under *What you are reading for*;
  `HOW-I-INVEST.md` a first heading, `## Why I invest`; the README its folder table and *The path*.
- **`README.md`** and **`SETUP.md`**: the interview as a few questions about the owner,
  `philosophy` and `brief` in the tables, and the release check.
- An install deploys **20 skills and 9 commands**.
### Removed
- **`interview`'s market stances and its reading step**, and *Where it sits* in `RESEARCHER.md`:
  the stances are asked by `philosophy`, the first reading question by `read`.

## [0.30.0] - 2026-09-29
A new user installed the researcher by pasting the install line, and the path was hard to follow:
English from the first line, three sessions — install, `init-researcher`, `interview` — a parent
folder and a name asked apart, and a seven-question interview of about ten minutes. On Codex, which
takes no commands, `interview` and `next` could only run by naming a file inside `~/.apm/`, and on
assistants with no question tool the interview's options had no shape in chat.

**What to do differently:** nothing to install differently — the same line, pasted into Claude,
Codex or Gemini, now does it all in one conversation. In an existing home, run `update`.
### Changed
- **`SETUP.md`** is the agent's script, in one conversation: the language first, the two tools and
  the git identity, the package, the researcher's name and one proposed folder named after it —
  `C:\Research\<Name>` — the home copied by `scaffold.py` from the installed package, the
  interview, the hand-over. The pin, the per-assistant differences and the Windows fixes move to
  *Troubleshooting*.
- **`README.md`** opens with *Install — three steps, no coding*, the same in Spanish, and what it is
  for; the manual install, the path and the tables move under *For developers and advanced users*.
- **`interview`** (skill 1.0.0, from the command): four steps, about five minutes — about you,
  voice, domains and rules, how you see markets, what to read for and first. The language, the
  researcher's name — the home's folder — and the owner's name are taken, not asked. The testable
  sentence, the shelf life, the decision and *would change my mind* are left for the owner to add;
  *Where it sits* is still written from the map. A written chat form for assistants with no
  question tool, a shorter preview, and a hand-over with a table of the home's folders.
- **`next`** (skill 1.0.0, from the command), unchanged in what it checks.
- **`init-researcher`** (0.4.0): asks the language, the name and the place, one go, and runs the
  interview in the same conversation.
- **The home template** (0.15.0): its README, `RESEARCHER.md` and `Philosophy/HOW-I-INVEST.md`
  shorter, and `AGENTS.md` as above.
- An install deploys **18 skills and 9 commands**.

## [0.29.0] - 2026-09-29
Two checks a researcher cannot make by reading alone. `challenge` read the git log for the order
blueprint, then rule, but not for the order reading, then blueprint: a prediction citing a note read
after the blueprint's commit is look-ahead in the research itself. Nothing checked a note's figures
against the pages it cites, and a number that is not in the source is the main risk of a note an
LLM writes; `audit deep` read for contradictions, not for invented numbers. The patterns come from
the companion code of Noguer i Alonso, *Large Language Models in Finance* (Packt 2026),
`PacktPublishing/LLMs-in-Finance` at 3a61db3: an availability audit that fails closed on a missing
timestamp, and numeric agreement between an answer and its evidence. Issue #22.

**What to do differently:** open every note's `read` field with its date, as `references/note.md`
already asks, and commit a note before the blueprint that cites it. Keep the extracts of the PDFs
you read, or regenerate them with the command `audit deep` prints, so their notes can be checked.
### Added
- **`check_numbers.py`**, in the `read` skill's `scripts/` (0.8.0): each figure a note states
  beside a page citation, looked up in the extract's page markers — on the cited page, elsewhere
  in the extract, with an offset reported when most of those lines sit at one distance from the
  page cited, or not found. Notes whose extracts are not on disk are listed as unchecked, with the
  `extract.py` command that regenerates them. The slug is `extract.py`'s own `slugify`, imported.
  It reads and edits nothing; exit code 2 when a figure is not found.
- **Check 10 in `challenge`, the reading before the blueprint**: every note a prediction cites
  entered git before the commit that brought `BLUEPRINT_N.md` in, and its `read` date falls on or
  before that commit's date. A later note, or a `read` field with no date that parses, is a
  finding; a note read again since is disclosed, and read at the blueprint's commit.
### Changed
- **`audit deep`** runs `check_numbers.py` over the library's notes and reports every figure not
  found as a finding, an offset as a note and the unchecked notes as a count. It fixes nothing,
  and its one write is still the log line.
- **`AGENTS.md`** names `check_numbers.py` among the scripts every user runs.

## [0.28.0] - 2026-09-29
`BRAINSTORMING_N.md` and the `brainstorm` command are retired. A brainstorming entry had the
journal's own four fields, the thinking before a blueprint is what a dated journal entry already
holds, and each entry's open threads keep planning apart from history; a strategy worked without
the file lost nothing. The one job only the file did, choosing the benchmark before Experiment 1's
blueprint, is now an entry of `JOURNAL_1.md`. Issue #20.

**What to do differently:** write the benchmark's choice as a dated entry of `JOURNAL_1.md`, before
the blueprint, and what to try next as a journal entry's open threads. A strategy that already keeps
`BRAINSTORMING_1.md` needs nothing: `next` and `blueprint` still read the benchmark there.
### Removed
- **The `brainstorm` command**, and the lifecycle skill's `references/brainstorming-template.md`.
  An install deploys 11 commands.
- **`BRAINSTORMING_1.md` from the strategy template** (0.13.2), and the worked example's four
  (0.18.2), their five entries moved into each experiment's journal at their dates, word for word.
### Changed
- **`next`**: part E is done when `JOURNAL_1.md` has the entry choosing the benchmark, or a
  `BRAINSTORMING_1.md` a strategy still keeps has its first; part F asks for the broad reading
  alone.
- **`blueprint`** reads the benchmark from `JOURNAL_1.md`, or from that older file.
- **`challenge` and `study`** name the journal's open threads where they named `brainstorm`.
- **`experiment-lifecycle`** (0.11.0): three documents in every experiment, the benchmark's choice
  in `JOURNAL_1.md`.
- **The home template** (0.14.1): the order of work's parts E and F, and eleven commands.

## [0.27.0] - 2026-09-26
A blueprint now records the package that drafted it, and `challenge` checks it against the package
that challenges the run. `blueprint`, `blueprint-critic` and `challenge` come from one package,
updated for every strategy at once by `apm update -g`, so the checks an experiment was designed
under could change before it was challenged, and nothing said so. A strategy pins its Python
libraries in `uv.lock`; the research tooling was pinned nowhere. The version is read from
`~/.apm/apm.lock.yaml`, never from memory. Issue #18.

**What to do differently:** run `apm update -g` between experiments, not during one. A blueprint
written before 0.27.0 keeps its line as it is, and `challenge` reports that it has no stamp.
### Added
- **The stamp in `blueprint`**: after the `**Written YYYY-MM-DD, before any rule was coded.**`
  line, on the same line, `Drafted with KaxaNuk-Researcher X.Y.Z, commit abc1234.` — the `version`
  and `resolved_commit` of the `kaxanuk-researcher` entry in `~/.apm/apm.lock.yaml`, `local` for a
  package installed from a path, `version unknown` when neither the lock nor the package's
  `apm.yml` can be read. On the same line, so the tests `next` and `challenge` make for the
  *Written* line still hold.
- **The comparison in `challenge`**: the version this run uses against the blueprint's stamp. A
  different version names both, and the package's changelog entries between them that touch
  `blueprint`, `blueprint-critic` or `challenge`. A mismatch is disclosed, never a failure. The
  journal entry names both packages.

## [0.26.1] - 2026-09-26
The README's command table says what `interview` writes since 0.26.0: `RESEARCHER.md`, the agent
and the researcher's skill, installed for the owner's user and committed. The row had kept the
earlier wording, `RESEARCHER.md` and the agent only, while *The path* above it already said the
rest. Nothing the researcher writes changes.

**What to do differently:** nothing.
### Fixed
- **The `interview` row** of the README's command table.

## [0.26.0] - 2026-09-26
The researcher is in every session, in every folder, on every assistant APM deploys to — no longer
only where the owner opens the home or adds it by hand. `interview` writes a second file of the
home's own beside the agent, the researcher's skill in `.apm/skills/<slug>/`, and installs the home
for the owner's user with `apm install -g "<the home>"`, beside the package, so the agent is
callable by name from any folder and the skill's description tells every session who the researcher
is and where its home lives. The home's `AGENTS.md` says who is speaking — the researcher is the
home, the engine is how it thinks, the agent is the researcher read-only — so a session asked *who
am I talking to?* answers the same way everywhere, and says so plainly when the home cannot be read.
What the owner teaches it anywhere goes home, by the routes that already exist, instead of into one
engine's memory of one folder. Home template 0.14.0. Issue #16.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home: it writes the researcher's skill, installs the home for your user and deletes the agent an
install inside the home left there, on your go. From then on, never `apm install` inside the home;
after changing the agent or a skill of the home's own, `apm install -g "<the home>"`. Adding the
home to a session is optional: it lets the researcher read the library without asking each time.
### Added
- **The researcher's skill**, `.apm/skills/<slug>/SKILL.md` in the home, written by `interview`
  beside the agent and under its name: who is speaking, where what is learned goes — a source to
  `Sources/` then `read`, a way of working to a line for `RESEARCHER.md`, a project's fact to that
  project — and what may be written from where the session is. Its description is the one piece of
  the researcher every session carries; it copies nothing else from `RESEARCHER.md`.
- **`update`** writes the skill for a home that lacks it or has moved, installs the home for the
  user when `apm deps list -g` does not name it, and deletes the agent's copies an install inside
  the home deployed there, which shadow the user's copy at home and go stale.
### Changed
- **`interview`** installs the home with `apm install -g "<the home>"` instead of deploying the
  agent inside it, commits the skill with the rest, and hands over with the researcher present in
  every folder; the `--add-dir` it asked for becomes access to the library, not presence.
- **The home's `AGENTS.md`**: *The researcher's home* says presence comes from the install for the
  user, and keeps the `CLAUDE.md` variable and `CLAUDE.local.md` as the way to load the whole file
  from the first line; a new *Who is speaking* section; *Joining other projects* and *Where the
  skills, the commands and the agent live* follow, with a row for the researcher's skill.
- **`next`** checks the skill and the install for the user; **`audit`** looks for the home's own
  deployed under the user's folders and reports a skill that names another folder.
- **The README, `SETUP.md`, the home's README and `apm.yml`** say the same: one command,
  `apm install -g "<the home>"`, on a new machine or for a new assistant.

## [0.25.1] - 2026-09-25
The worked example stops publishing provider data: the security master `promote.py 4` froze into
`Paper_Trading_4/` — company names, ISINs, sectors and industries from FMP's profiles — left the
repository, as the master in `Universe/` never entered it. `.gitignore` keeps every book's copy
out, in the template and the example; the copy stays where the book was frozen, unchanged, its hash
in `FREEZE.json` still matching; and the example's `daily_update.py` checks every frozen file
against that hash and stops a book whose files are missing or changed. Strategy template 0.13.1,
example 0.18.1, `paper-trading-gate` 0.2.1; no frozen byte, rule or number moved. Earlier commits
still hold the file.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`. A copy of the example
made from now on has no frozen master: bring it across by hand from the machine that froze the book
before its daily run there. In a strategy of your own, add the template's `.gitignore` line, and
`git rm --cached` a frozen master already committed.
### Changed
- **`.gitignore`**, in the template and the example, keeps
  `Paper_Trading/*/Universe/Security_Master.csv` out of git.
- **The example's `daily_update.py`** checks each file `FREEZE.json` hashes before a book runs, and
  stops a book with `unfrozen-input` when one is missing or not the copy frozen; `promote.py` says
  the master stays on the machine when it freezes a book.
- **`paper-trading-gate`**, `SETUP.md` and `Paper_Trading/BITACORA.md` in the template and the
  example, and the docstrings of `promote.py` and `daily_update.py`, say the master is copied from
  disk, stays out of git and travels by hand.
### Removed
- **`examples/liquid-golden-cross/Paper_Trading/Paper_Trading_4/Universe/Security_Master.csv`**
  from the repository.

## [0.25.0] - 2026-09-25
The first two moves need nothing typed but answers and a go. `init-researcher` brings the package
to its newest version with `apm update -g` before it copies, so a home is always made from the
newest template with every command current, and hands over in two plain steps. `interview` deploys
the agent for the assistant it runs in and commits what it wrote, on the one go it already asks
for: the owner's go on its preview is their review, and the commit records it. The newcomer's path
in the README is four moves where it was five, and `SETUP.md` says the same. Home template 0.13.0;
`init-researcher` 0.3.0.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home for the new paragraph of its README. A home whose interview already ran needs nothing else.
### Changed
- **`init-researcher`** runs `uvx --from apm-cli==0.29.0 apm update -g --yes` on the go, before the
  copy, and says the version installed; when the update fails it goes on with the version
  installed, naming it. Its plan says the assistant may ask to allow two commands, and it hands
  over as two numbered steps: open the folder in a new session, type `/interview`.
- **`interview`** deploys the agent with `apm install --target <this assistant>` and commits the
  files it wrote, by name, on the same go — asking for a git identity when the commit needs one,
  never inventing it — and its hand-over opens with the new session where the agent answers by
  name.
- **The README's path** is four moves; **`SETUP.md`**'s step 2 deploys the agent by hand only on a
  new machine or for another assistant.

## [0.24.0] - 2026-09-25
A researcher's home has `Studies/`, and a command to write in it: `study`. A study is the owner's
own work from the library — an idea that is not a strategy yet, or a decision, a plan or a brief
with no repository of its own — drafted from the owner's words, with every claim from the library
linked to its note and anything from outside it marked as not checked. A synthesis page says what
the library holds; a study says what the owner will do about it. The `Projects/` that 0.18.0
removed had no rule but *anything you ask for*; a study has a contract: one way from the notes,
words only, and it moves out, staying as the record, when it needs code or data or becomes a
strategy. The README opens with what the researcher is for, with a strategy or without one, and how
it grows with its owner. Home template 0.12.0; `read` 0.7.3, `query` 0.6.1, `init-researcher`
0.2.2; no strategy template, example or Lab skill changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, then `update` in your
home: it brings `AGENTS.md`, `README.md` and the empty `Studies/` across and, on your go, moves what
a `Projects/` still holds into `Studies/`, at the same depth, so its links into `Knowledge/` still
resolve. Then by hand, if you like: `Studies/` among the places your agent never writes, `study`
among what it names, and a state on the first line of each file that moved. `study` appears in a
new session.
### Added
- **`study [subject]`**, the twelfth command: asks what you want to work out, walks the library for
  what supports it, what argues against it and the simpler rival, names the gaps as leads, and on
  your go writes one study in `Studies/`, whose first line gives its state — *idea*, *active*,
  *parked*, *closed* or *moved to `<path>`*. With no subject it lists the studies and offers the
  open ones and the reading questions that feed a decision no study works out yet. A revision
  starts from the notes written since the study's date and keeps every line you wrote. Home only.
- **`Studies/` in the home template**, empty, with its row in `AGENTS.md`'s folder table and a
  section *Studies* that is its contract.
- **What you can use it for**, at the top of the README and of the home's *Working with it*: a
  library you can ask, your studies, lessons, strategies, any other project, and a researcher that
  grows with you, each with the command that does it.
### Changed
- **`update`** moves what a home's `Projects/` holds beyond its lessons into `Studies/`, one
  `git mv` per file or folder, never onto one that exists, where it left it for the owner; and
  brings `Studies/.gitkeep` to a home without the folder.
- **`interview`**'s agent never writes in `Studies/` and names `study` for a write; its hand-over
  offers `study`.
- **`read`** never writes in `Studies/`, and its report names an open study a new note bears on,
  with the `study` that would revise it.
- **`query`** names a study that bears on a question as the owner's work, never as evidence, and
  never modifies one.
- **`audit`** reports a study's broken links, a link into `Extracts/` or to a PDF, and a first line
  with no state, and never touches `Studies/`.
- **`next`** offers `study` at home once its checklist is done; **`init-researcher`** names the
  empty `Studies/` in its plan.
- **The release check** deploys 12 commands.

## [0.23.0] - 2026-09-25
The worked example puts a book on paper for the first time: Experiment 4's, momentum held only
outside bear markets, as a candidate the owner chose to track without graduation, so that the
months after its test window become the unseen test its blueprint named. The exception is recorded
by name in the example's gate document, with the book's bands, kill switch, review dates and what
its record cannot show registered before its first day; `promote.py 4` froze it, and
`daily_update.py` runs it every day, to local files, a DuckDB database or both. Example 0.18.0; no
skill, command, rule, agent or template changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, so that `init-example`
copies the example with its paper book; in a copy, schedule `Paper_Trading/daily_update.py` as its
`SETUP.md` says.
### Added
- **The example's first paper book**, `Paper_Trading/Paper_Trading_4/`: the frozen rule, its
  control, the frozen modules and `FREEZE.json`, run daily by `daily_update.py`.
- **Its registration** in the example's `Paper_Trading/BITACORA.md`, written before its first day:
  the exception to graduation, the bands, a kill switch on behaviour, quarterly reviews, and what a
  year of paper cannot show.

## [0.22.0] - 2026-09-25
The worked example opens and reports Experiment 4, claim 5's second design: the same momentum
ranking held only outside bear markets, a negative two-year return of the index, after which Daniel
and Moskowitz find every one of momentum's fifteen worst months. It earns 11.61% a year at a Sharpe
of 0.478 over 2002-07-30 to 2026-06-01, 1.08 points a year ahead of the same pool's twenty most
traded and ahead of the ranking held in every month, but 0.0084 of Sharpe ahead where 0.03 was
required: it fails its kill switch, and nothing graduates. It was run from a wiped working copy.
Example 0.17.0; no skill, command, rule, agent or template changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, so that `init-example`
copies the example with Experiment 4. Its analyzer's new rows read the desk's index returns, as the
experiments' membership already does.
### Added
- **Experiment 4 in the example**, from brainstorming to findings, with its blueprint committed
  before any rule, reviewed cold by the blueprint critic and revised on every point; a check that
  ends a listing at its last distinct bar, so that no run was refused; and a diagnostic arm the
  rule has to beat, so that the state earns its place against its simpler baseline.
- **Daniel & Moskowitz (2013)** in the example's `Bibliotheca/`, carried from a researcher's
  library, with the warning its home note carried above the Paleologo chapter it contradicts.
- **Momentum by market state** in the example's analyzer.
### Fixed
- **Experiment 3's notebook** names its own blueprint and reserve in the comment above its costs.

## [0.21.0] - 2026-09-25
The worked example reports Experiment 3. Momentum proper on the same liquid names — of the hundred
most traded members of the index, the twenty that rose most over the twelve months before the latest
one, re-struck monthly — earns 10.81% a year at a Sharpe of 0.436 over 2002-07-30 to 2026-06-01,
against the same pool's twenty most traded at 11.03% and 0.465, and fails its kill switch; claim 5
is falsified for that design, and nothing graduates. It was run from a wiped working copy, and
Experiment 2 was reproduced from one, every figure the same. Example 0.16.0; no skill, command,
rule, agent or template changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, so that `init-example`
copies the reported example. Quote Experiment 1 from its record on the seed of 788, at `v0.18.0`:
the example's `FINDINGS_1.md` now describes what its notebook prints on the widened seed, the same
verdict with one perturbation cell fewer keeping its sign.
### Added
- **Experiment 3's findings**, in the example: the predictions, the kill switch, the book, its
  capacity, the perturbation with four cells the engine could not price, each counted against the
  rule as the blueprint fixed, the trial count of fifty-four, and an attribution that finds the
  ranking a momentum tilt with less idiosyncratic return than its control. The gate's rows, the
  results record and the objective's claim 5 follow from them.
- **Experiment 1 on the seed of 1,500, described**, in the example's `FINDINGS_1.md`, so the
  figures a copy made now prints are on record.
### Changed
- **Experiment 2's reproduction** from a wiped working copy is recorded, and its blueprint's fifth
  success criterion met.
### Fixed
- **Experiment 3's notebook** names a run the engine cannot price instead of stopping at it, and
  its verdict cell names claim 5.

## [0.20.0] - 2026-09-24
The worked example opens Experiment 3 before its rule, and the interview offers three more hints.
Experiment 3 tests momentum proper on the same liquid names — of the hundred most traded members of
the index, the twenty that rose most over the twelve months before the latest one — against the same
pool's twenty most traded, as claim 5 of the example's objective, added for it. Its blueprint is
committed, reviewed cold and revised, before any rule; the refinery gains the twelve-month return,
and the analyzer measures it. The interview offers three more hints and asks no more questions:
question 5 offers a clause naming who keeps taking the other side of the trade, and four ways an
edge's shelf life might run, the one that follows from where the owner says the edge comes from
listed first; question 3 folds *Add one of mine* and *Change or drop one* into one option and offers
a rule in the slot it frees. Home template 0.11.0. Example 0.15.0.

**What to do differently:** in a home, run `update`; then, by hand in `RESEARCHER.md`, add the rule
*Every design is challenged before it runs, and every idea tried is counted* if you want it. To be
offered the new hints, run `interview force`: every answer you keep is written back verbatim. To
study Experiment 3 before its result, run `init-example` after `uvx --from apm-cli==0.29.0 apm
update -g`.
### Added
- **Experiment 3's blueprint, brainstorming entry and first journal entry**, in the example,
  before any rule: the twenty of the hundred most traded members with the highest twelve-month
  return before the latest month, re-struck monthly, against the pool's twenty most traded with a
  momentum value, on 2002-07-30 to 2026-06-01, with a kill switch over three sub-periods, ten
  perturbation cells and a trial count of fifty-four.
- **Claim 5 in the example's objective**, momentum among the most traded, in the owner's words, with
  the note that it was chosen before the analyzer measured it and written after.
- **`r_momentum_12_1` in the example's refinery**, and its measurement in the analyzer: rows 19 to
  30 of `RESULTS.md`, on the widened panel.
- **Question 5 offers the other side of the trade**: after the testable sentence, a clause the owner
  may fill or leave — *…and ___ keeps taking the other side because ___* — the other side as the
  reading map's anatomy of an idea gives it, who sells to you and what keeps them doing it. Its
  blanks are never filled for the owner, and a clause left blank is left out.
- **Question 5 offers the shelf life as four options**, in its one message, the owner's own words
  as welcome: outlasts publication, a risk someone is paid to carry; shrinks as others learn it, a
  mistake others repeat or information; lasts while the obstacle does, others cannot take the other
  side; comes and goes. The option that follows from the `Edge from?` pick comes first. They are
  the package's own hint, not the deck's, which asks only whether an edge is paid risk or
  mispricing: no option names a work, and the reading map is unchanged.
- **A rule offered in question 3**: *Challenge my design before it runs, and count every idea I
  try*, written under *Non-negotiables* as *Every design is challenged before it runs, and every
  idea tried is counted*. The home's `RESEARCHER.md` offers it beside the fourth (home template
  0.11.0), never as a default.
### Changed
- **Question 3's rules keep four options**, the question tool's limit: *Add one of mine* and
  *Change or drop one* are one option, *Add, change or drop one*, and a rule typed under *Other* is
  its line.
- **A shelf life picked from the options** is written to `RESEARCHER.md` by its label, with any
  words the owner added; `Philosophy/HOW-I-INVEST.md` takes only their own words, as before.

## [0.19.0] - 2026-09-24
The worked example runs and reports Experiment 2, on a seed widened to every listing the index held
since 2000. Experiment 1's diagnostic arm, its design taken to 2002-07-30 to 2016-12-30 with the
names that left the market fetched from Sharadar, trails the same names without its cross by 1.64
points a year and fails its kill switch, so nothing graduates and claim 1 stays falsified, now on
two windows. The example's universe changed: Experiment 1's figures stand at `v0.18.0`, on the
788-name seed. Example 0.14.0; no skill, command, rule, agent or template changed.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g`, so that `init-example`
copies the new example. Quote Experiment 1's figures from `v0.18.0`, on the 788-name seed: a copy
made now holds the widened seed, and no recorded run gives what Experiment 1 prints on it. To fetch
Experiment 2's names, a copy needs a Sharadar key and a Data Curator with the Sharadar provider, as
the example's `SETUP.md` says.
### Added
- **Experiment 2's run and findings**: its blueprint revised once, to a 5% cash reserve, after its
  first run could not be priced; its journal's later entries, its notebook and `FINDINGS_2.md`; and
  the gate's rows in `BITACORA.md`. It has not been reproduced from a wiped working copy.
### Changed
- **The example's seed is widened** to every listing the index held since 2000: 1,500 identifiers,
  712 of them marked `sharadar` in its `provider` column.
- **The example's `RESULTS.md`, `OBJECTIVE.md`, README and `AGENTS.md`** are compiled from both
  experiments' findings, and the README names Experiment 1's rows as the 788-name seed's, at
  `v0.18.0`.

## [0.18.0] - 2026-09-24
The worked example reports Experiment 1's second design and opens Experiment 2, and a researcher's
home keeps its lessons in `Lessons/`. Experiment 1's second design is run, reported and reproduced
from a wiped working copy: it beats the index on Sharpe, earns 0.86 points a year less than the same
names without its cross, and fails its kill switch, so nothing graduates. Experiment 2, its
diagnostic arm's design on years before 2017, is committed as a blueprint before its rule. A new
home has no `Projects/`: `teach` writes to `Lessons/<topic>/`, and anything else asked for at home
is answered in chat. Home template 0.10.0, strategy template 0.13.0, example 0.13.0,
`init-researcher` 0.2.1, `read` 0.7.2, `attribution-analysis-runs` 0.2.9.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g` and open a new session.
In a home, run `update`: it brings `AGENTS.md` and `README.md` across and, on your go, moves each
`Projects/Teach/<topic>/` to `Lessons/<topic>/`. In a strategy, take the template's 0.13.0 files by
hand, as its entry lists them. Quote the example's Experiment 1 exits, entries, turnover and
capacity from its reproduction of 2026-09-24, never from its run of 2026-09-23.
### Added
- **Experiment 1's second design, reported** in `FINDINGS_1.md`, `RESULTS.md` and the gate's rows,
  and reproduced from a wiped working copy on 2026-09-24, with one manual step, every engine and
  attribution figure to the digit, on the 788-name seed.
- **Experiment 2 in the worked example, before its rule**: its brainstorming, a blueprint reviewed
  cold by `blueprint-critic`, the first entry of its journal, and its findings, not yet run. None of
  its results is in this release.
- **A second price provider**: in the example's `Data/curator.py`, `--provider sharadar`, for the
  names FMP does not carry, through the Data Curator's `issues/31` branch until a release carries
  it; in the strategy template, a line of the Curator stage's contract for names the first provider
  does not carry.
### Changed
- **A home has no `Projects/`** (home template 0.10.0). `teach` keeps each topic in
  `Lessons/<topic>/`; `update` offers, on the owner's go, to move a home's `Projects/Teach/<topic>/`
  there and to remove a `Projects/` left empty; `interview`, `init-researcher` 0.2.1 and `read`
  0.7.2 name `Lessons/` where they named `Projects/`.
- **The desk's folders**: the strategy template, the example and `attribution-analysis-runs` 0.2.9
  name the Analytics Factory's `Benchmark Portfolios/` and `Factor Models/`, read first, and the
  older `Benchmarks/` and `Factors/`, still read where those are absent.
- **The findings template's status**, in `experiment-lifecycle`'s reference and the strategy
  template, asks whether the rule beat the benchmark and its control by what its blueprint required,
  and whether it is a candidate for the gate.
- **The README's `paper-trading-gate` row** names the freeze, the daily run and its record.
### Fixed
- **The example's slot book is in date order**, which corrects Experiment 1's exits, entries,
  turnover and capacity as its run of 2026-09-23 printed them; no engine figure moved. The faults
  the paper-trading machinery's first runs found are fixed with it: a window prices only the
  listings it holds, a refused engine run stops the book with the engine's reason, a band is read
  with a billionth of tolerance, a stale lock is removed, and the record replaces a day's flags and
  holdings whole on a re-run.

## [0.17.0] - 2026-09-23
The researcher is its owner's, and grows with what they believe. The interview asks what pulls the
owner to markets and how they like to invest, puts the view that leads as one testable sentence
with a shelf life, and asks the smallest test that could kill it; its rules are offered as ones
many researchers start with, to keep, change or add to, with a fourth to keep or leave. The reading
map gains Section 02 of the bootcamp deck, *Where Alpha Comes From*, as hints that `interview`,
`objective` and `blueprint` offer as questions, never as a position to adopt. Home template 0.9.0,
`read` 0.7.1.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g` and open a new session.
In a home, run `update`: it brings the new line of `README.md` across; then, by hand in
`RESEARCHER.md`, add the fourth non-negotiable if you want it. To be asked the new questions, run
`interview force`: every answer you keep is written back verbatim. In a strategy, `objective` now
offers each claim its source of edge, other side, test and kill switch, and `blueprint` asks the
seven questions before any backtest and the kill switch; answer what you like and skip the rest.
### Added
- **Section 02 in the reading map** (`read` 0.7.1), pages 55 to 60 of the deck, as hints: the five
  sources of edge and the question each asks, the six places ideas come from and how each fools
  you, seven questions before any backtest, an idea's anatomy — the claim, the source of edge, the
  other side, the test, the kill switch — and the three discussion questions.
- **`interview` asks how the owner likes to invest**: `Your method`, a fourth question in question
  4 — rules I can write down and test; judgment, case by case; judgment designs it, rules run it;
  not sure yet. It places nothing on the map and never leads.
- **Question 5 proposes the view as one testable sentence** — if this holds, I would measure that,
  because of this source of edge — for the owner to edit or refuse, and asks how long they would
  give the edge; question 6 asks the smallest test that could kill the belief beside what they
  would see if they were wrong. What they keep is written verbatim.
- **A fourth rule, offered**: a strategy graduates only against criteria written down beforehand,
  never on a good month. `interview` writes it when picked; the home's `RESEARCHER.md` offers it.
- **`objective` offers each claim its anatomy**, and **`blueprint` asks the seven questions before
  any backtest and names the kill switch in the falsifying condition** — asked, never required.
### Changed
- **The interview's rules are the owner's**: question 3 states three rules many researchers start
  with, never "KaxaNuk's three", keeps the fact that in a KaxaNuk strategy the numbers come from
  the Lab's libraries, and is multi-select — keep the three, add the fourth, add one of mine,
  change or drop one.
- **`Edge from?` takes the deck's five sources of edge** in four options — paid for a risk others
  avoid; a mistake others repeat; others cannot take the other side; something I see or do better
  — with *not sure yet* typed under Other, which counts as *Not sure yet*.
- **Question 2 asks what about markets pulls the owner in**, the puzzle they most want to
  understand, which question 6 can take as a reading question.
- **The home** (template 0.9.0): `RESEARCHER.md`'s non-negotiables guidance offers the three as a
  start and the fourth to add; `README.md` says in one line that the researcher is yours, growing
  with what you believe, with the package's hints to make complex ideas simple.

## [0.16.0] - 2026-09-23
Paper trading gets its machinery, and Experiment 1 can graduate. A graduated book is the strategy
frozen: `promote.py` copies every file it needs, byte for byte, into `Paper_Trading_N/`, and
`daily_update.py` runs every frozen book each day — refresh, check, rule, engine — and keeps the
record in CSV files, a DuckDB database or both, set in `Config/.env`. The benchmark is now what
`BRAINSTORMING_1.md` names; Experiment 1 is the first rule tested against it, and a rewrite of it
is written down as one. The desk's index and factor files are read in place, in their own names.
The worked example's Experiment 1 is being rewritten: its second blueprint is committed here,
before any rule. Strategy template 0.12.0, example 0.12.0.

**What to do differently:** run `uvx --from apm-cli==0.29.0 apm update -g` and a new session. In a
strategy, take the template's 0.12.0 files by hand, as its entry lists them. Put the desk's folder
in `KN_ANALYTICS_PATH` rather than renaming its files into `Data/Curator/`; a drop-in copy must now
keep the desk's names and headers. Name the benchmark in `BRAINSTORMING_1.md` and hold Experiment 1
to it like any other experiment. When an experiment graduates, write its rule into
`paper_trading_N.py`, commit, run `promote.py N`, register the book in `BITACORA.md` before its
first day, and schedule `daily_update.py` as `SETUP.md` shows.
### Added
- **The daily run of a paper book**, in the template as contracts and in the example as code:
  `Paper_Trading/promote.py` freezes a graduated experiment into `Paper_Trading_N/` with
  `FREEZE.json`; `daily_update.py` refreshes the prices once, checks the newest day, runs each
  frozen book's refinery, rule and engine over the whole history and since the freeze, and exits
  0, 1 or 2; `record.py` keeps six keyed tables, upserted, with a restatement flagged and never
  overwritten, in local CSV files, a DuckDB file, or a PostgreSQL server through DuckDB. Four
  `PAPER_TRADING_*` settings and `KN_ANALYTICS_PATH` join `Config/.env.template`; `duckdb` and
  `pyarrow` join `pyproject.toml`; `.gitignore` ignores each day's output.
- **`Data/hand_supplied.py`**, the one reader of the desk's index holdings, index returns and factor
  files, in place from `KN_ANALYTICS_PATH` or from the drop zones, in the desk's own names and
  headers; the Curator's index staging, the universe notebook, the experiment and
  `attribution_analysis.py` read through it.
- **`Data/curator.py --end-date`**, with a resume by the date each file was fetched through and a
  retry on a request that hangs, so paper trading can refresh through the day.
- **`BITACORA.md` *Before a book's first day***: the section each graduated book gets, committed
  before its first run — bands, kill switch, review dates, what the record cannot show. SETUP's
  *Paper trading, daily* says how to run, configure and schedule it.
- **In the example**: the analyzer measures the cross as a 0/1 state and what a name earns after
  its cross breaks; Experiment 1's second blueprint, its brainstorming and journal entries, and the
  measurements in `RESULTS.md` it cites.
### Changed
- **The benchmark is named in `BRAINSTORMING_1.md`** — an index, an ETF or an equal-weight book of
  the universe — and Experiment 1 is the first rule tested against it, able to graduate. Its rules
  still freeze once its findings report; a rewrite the owner decides is written down as one. The
  template's `AGENTS.md`, README, blueprint, journal, notebook and `BITACORA.md`,
  `experiment-lifecycle` 0.10.0, `paper-trading-gate` 0.2.0 and `blueprint` say so.
- **`paper-trading-gate` 0.2.0** covers the freeze, the daily run and the registration before day
  one; it still never declares graduation, computes a number or re-fits.
- **`attribution-analysis-runs` 0.2.8** says the desk's files are read as shipped.
- **`Experiments/backtest_engine.py`** takes the benchmark as an argument, for a paper window past
  the index's last date.

## [0.15.0] - 2026-09-23
A blueprint now meets a critic before the go, and the bar it is held to asks for more: a control
that differs in exactly one thing, one falsification condition fixed before the rule, and the
horizon and overlap beside every ratio. Each experiment names the claim it moves, every notebook
ends in a Verify section that raises, a figure is quoted only from the file that owns it, and APM
is pinned at 0.29.0. Home template 0.8.2, strategy template 0.11.0, example 0.11.0.

**What to do differently:** run `apm --version`; on anything but 0.29.0, run
`uv tool install apm-cli==0.29.0` first, as `SETUP.md` now pins it, and never `apm self-update`.
Then `uvx --from apm-cli==0.29.0 apm update -g` and a new session, which brings the new agent,
`blueprint-critic`. In a home, run `update`: it brings `AGENTS.md` and `.gitignore` across; change
the second non-negotiable in `RESEARCHER.md` by hand, as the home's changelog shows, and
`git rm --cached` any PDF already committed outside `Sources/`. In a strategy, the next
`BLUEPRINT_N.md` names the claim it moves, a *Control* line in *Rules* and *What would falsify it*,
with the changes that may not rescue it; its `FINDINGS_N.md` and the *Claim moved* column of
`RESULTS.md` say which claim moved; a coefficient or ratio carries its horizon, its overlap and the
share of dates with the expected sign; and each notebook ends in a Verify section. A strategy made
from an earlier template takes the new sections by hand, as the template's 0.11.0 entry lists them.
### Added
- **`blueprint-critic`, the package's first agent**, in `.apm/agents/`. It reads a draft blueprint
  cold, with the strategy's bar, `OBJECTIVE.md`, the notes cited and *Before any experiment*, and
  returns objections only, each with the line and the evidence; it writes nothing and the owner
  decides. `blueprint` hands it the draft before the go, and reviews the draft itself against the
  same seven items where no subagent can be called. `SETUP.md`'s done check looks for it, and the
  README and `AGENTS.md` name it.
- **Three items at the end of a strategy's bar**, so the first eight keep their numbers: a control
  on the rule's own rebalance dates, one falsification condition and the changes that may not
  rescue it, and the horizon and overlap beside the share of dates with the expected sign. The
  blueprint gains *The claim this moves*, a *Control* line and *What would falsify it*; the
  findings and `RESULTS.md` say which claim moved (`experiment-lifecycle` 0.9.0,
  `paper-trading-gate` 0.1.1).
- **A Verify section at the end of every notebook**, which reads back what the notebook wrote and
  raises, and counts the days the engine valued against the window's trading days, never a fixed
  floor. In the example it is code, and skips where no licensed engine is installed; nothing has
  run it end to end yet. The example's analyzer writes `overlap_days` and `share_expected_sign`,
  and its README says, stage by stage, what a correct run shows, from recorded figures only.
- **`query`'s *Numbers*** (0.6.0): a performance figure is quoted only from `FINDINGS_N.md`,
  `RESULTS.md` or the analyzer section it cites, named beside it, never recomputed, rounded,
  combined or carried to another strategy. `read` (0.7.0) and its `note.md` keep a paper's figure
  the paper's.
- **Four more checks in `audit`**: a note whose `read` field does not say what was read, a claim
  status outside the template's vocabulary, a strategy's own performance figure found in neither
  its findings nor `RESULTS.md`, and, under `deep`, a part of `BIBLIOGRAPHY.md` whose sources only
  agree.
- **`library_version`** in the frontmatter of `backtest-engine-runs` 0.1.6,
  `attribution-analysis-runs` 0.2.7 and `portfolio-construction-runs` 0.2.4: the build each was
  written against, to compare with the installed one before trusting a trap. `references/api.md`
  lists the `portfolio_stats` keys the example reads, and says their risk-free rate and
  annualisation are not verified.
### Changed
- **APM is pinned at 0.29.0** in the README, `SETUP.md`, `update` and the strategy template's
  `SETUP.md`, and every command in the README, `SETUP.md` and `update` that runs APM names
  `apm-cli==0.29.0` itself, `uvx --from apm-cli==0.29.0 apm ...`, so a newer `apm` on the path
  cannot run it. Measured on Windows: 0.29.0 installs this package cleanly; from 0.29.1 on, APM
  stages a package under about 148 more characters of folders, the worked example's longest paths
  pass the 260-character limit, and the install fails with `WinError 3` or `WinError 206`. `update`
  checks the version first and installs 0.29.0 before the update.
- **A change to the package is tried by a project-scope install** of the working tree from a short
  scratch folder with the pinned APM, the `git ls-files` copy the fallback; before a release, 16
  skills, 11 commands, 4 rules and 1 agent install with no warning. `AGENTS.md` names the lines the
  100-column rule exempts, forbids a literal tab, says what a second package with a same-named
  skill or command does, and points to the home's and a strategy's own rules. The README says what
  the researcher will not do. `.gitignore` ignores what the copilot target writes in `.github/`.
- **The commands follow the template more closely.** `objective`, `audit` and `next` accept a
  note, `RESULTS.md` or the findings that measured a claim, or nothing for a claim true by
  construction; `blueprint` reads the strategy's bar and lists what the draft lacks before the go;
  `challenge` always checks the trial count the findings owe, and quotes the git log as the
  evidence the blueprint came first; `next` recognises the worked example and sends the owner to
  `init-strategy`; `interview` and `update` copy a missing home file with `scaffold.py --only`.
- **The home** (template 0.8.2): interview's one write to `Philosophy/HOW-I-INVEST.md` is named; a
  strategy with no claims reads nothing in; the hypothesis non-negotiable matches `AGENTS.md`;
  `read` proposes questions when *What you are reading for* is empty; the primitives table names
  all 16 skills, 11 commands, the agent and the house instructions; `.gitignore` ignores every PDF
  and `.env` files.
- **`data-analyzer-runs`** (0.2.0) matches the notebook: its section table ends in *7 · Verify*,
  with what that section reads back and raises on, and section 4 reports the share of dates with the
  expected sign and the overlap, *h − 1* days, beside the IR.
- **The writing commands refuse the worked example**: `objective`, `blueprint`, `brainstorm` and
  `challenge` stop in it, and `audit` reports there without appending to its log, each with the
  test `next` uses and naming `init-strategy` for a strategy of one's own.
- **A blueprint is filled when it carries its *Written* line.** `blueprint`, `challenge` and
  `next`'s part E test for the `**Written YYYY-MM-DD, before any rule was coded.**` line
  `blueprint` writes, where each had its own test; `blueprint`'s draft replaces each heading's
  guidance paragraph. `blueprint-critic` objects only to what the draft wrote, not to the
  template's guidance or, in the worked example, to anything outside the example's own lines.
- **`next` and `challenge` follow the claim the blueprint names.** `next`'s part H and `challenge`'s
  closure check read the claim under *The claim this moves* and the status `FINDINGS_N.md` says it
  reached, against `OBJECTIVE.md` and the *Claim moved* column of `RESULTS.md`; a blueprint that
  names none falls back to the statuses in `OBJECTIVE.md`. `backtest-engine-runs`' *Read the run
  before believing it* points to the experiment notebook's Verify section, and the worked example's
  99% and five-day rule.
- **`read`** documents what `extract.py` reports — the extract folder's slug, `OUTLINE.md`, a
  chapter *not written* or *thin*, exit 1 as a mistake in the command — and warns that a text
  clipping in a strategy is committed. The three `init-*` skills (0.2.0) say what to do when a git
  step fails.
### Fixed
- **`scaffold.py` refuses a copy too deep for Windows** without long paths: a plan whose longest
  path would reach 260 characters, or whose deepest folder 248, exits 1 with nothing written,
  naming the path and the longest destination that fits, where it failed partway with a traceback.
  `init-researcher`, `init-strategy` and `init-example` say so.
- **`next`** leaves an untracked source under `Sources/` to its own row, sends a home that is not a
  git repository to the commands that finish it, and names a worked example one level down as the
  example, for reading.
- **`read`** counts a section of angle-bracketed slots as empty, stops with `interview` in a home
  not yet interviewed, and never takes a `.gitkeep` for a source; `note.md` names a source with no
  author or no printed year by its organisation or project and `ND`, as the worked example does.
- **`audit`** exempts a paper's figure quoted in any of the strategy's documents through a note it
  cites, matches a figure at the precision quoted, takes a *No note yet* row for a lead, reports
  missing local copies once, *on this machine*, and audits a strategy alone when no home is in the
  session. Its one log line is named as the one write made without a go, there and in the home's
  `AGENTS.md`.
- **`update`'s `check`** reports a dirty tree as a line instead of stopping, and a home at or
  ahead of the template's version is current, with nothing proposed for removal.
- **`init-researcher`'s plan** names every file the script copies. The worked example's README
  says it is for reading and running, not copying.
- **`scaffold.py --only`** refuses an absolute path, or one that leads outside the starting point
  or the destination, and writes nothing.
- **`scaffold.py` without git** keeps the copy, exits 0 and prints the git commands left to run,
  where it ended in a traceback; git's output is decoded as UTF-8 and printed safely, and a failed
  `git init` or `git add` prints the commands that finish the job.
- **`extract.py`'s help** named the extract folder by the PDF's stem, where the script writes a
  slug, and did not say that a command argparse rejects exits 2.

### Removed
- **The worked example's `uv.lock`.** The example resolves its library versions when `uv sync`
  runs; a strategy made from the template still commits its own lock, as its `SETUP.md` says.

## [0.14.4] - 2026-09-23
The package's own `.gitattributes` leaves it.

**What to do differently:** nothing. A clone on Windows now takes its line endings from git's own
setting, so `scaffold.py` copies what the clone holds; the researcher home, the strategy template
and the example keep their `.gitattributes`, so a new home or strategy still commits LF.
### Removed
- **`.gitattributes`** at the root, and its row in the README's file map.

## [0.14.3] - 2026-09-23
The repository's own tests and tools leave it: what stays is the package users install, and the
two starting points, kept in step by hand. Strategy template 0.10.5, example 0.10.6.

**What to do differently:** before a commit, run ruff and the Bloom Code check as the README's
*Development* shows. Keep the template's copy of a shared file in step with the example's by hand,
in the same commit. Before a release that changes a skill, a command or a script, walk the
newcomer's path by hand in a scratch folder. The tests and the tools stay in the history at
`v0.14.2`.
### Removed
- **`tests/`**, 145 tests of the skills' three scripts and of the two tools.
- **`tools/check_repo.py`**, which checked versions, headings, markers, the section symbol, skill
  descriptions, generated files, path length and width before a commit.
- **`tools/sync_investment_lab_references.py`**, which generated the template's shared files and
  `experiment-lifecycle`'s references from the worked example.
- **The pytest settings and the dev dependencies** in `pyproject.toml`, and the pytest and coverage
  lines in `.gitignore`.
### Changed
- **`AGENTS.md`** says the template's shared files and `experiment-lifecycle`'s references change
  by hand, in the same commit as the example's; the skills' scripts are tried by running their
  skill in a scratch folder; ruff and the Bloom Code check pass before a commit.
- **`experiment-lifecycle` 0.8.3** says its references are kept in step with the example by hand.
- **The README's *Development*** lists the two checks that remain and what is done by hand.

## [0.14.2] - 2026-09-23
The behavioural evals leave the package: they ran once, cost about $30 a run, and needed a tool
nobody on the team had installed. A release that changes a skill is checked by walking the
newcomer's path by hand instead.

**What to do differently:** before a release that changes a skill or a command, walk the path in a
scratch folder — `init-researcher`, `interview`, `next`, `init-strategy`, and `read` on one
clipping. The evals stay in the history at `v0.14.1`, to restore the day a release needs them.
### Removed
- **`evals/`**, its 13 cases, 48 triggering requests and README; **`tools/eval_run.py`,
  `eval_fixtures.py` and `eval_history.py`**; and their 74 tests. Their one run, the pilot of
  0.12.0, found three real faults in `blueprint`, `brainstorm`, `challenge` and `query`, all fixed
  then; no run followed through 0.13.0, 0.14.0 and 0.14.1, and the cases covered none of the
  commands those releases changed.
### Changed
- **The README's *Development*** says how a release that changes a skill is checked, and its file
  map and `AGENTS.md` no longer name the evals.

## [0.14.1] - 2026-09-23
Kept clean and to the point: what nothing used is gone, every test can fail, and every eval can
run. Home template 0.8.1, strategy template 0.10.4, example 0.10.5.

**What to do differently:** `apm update -g`, then a new session. In a strategy made from an
earlier template, delete `apm.yml`: a strategy installs nothing, and nothing read it. In a home,
`update` lists the two blockquotes of `Knowledge/INDEX.md` and `Knowledge/LOG.md` to bring
across by hand.
### Removed
- **`.github/CODEOWNERS`.** It asked for a review when a pull request opened; work lands on `main`
  directly, so it had nothing to do.
- **The obsidian-vault-kit notice**, from `LICENSE`, the home's `LICENSE` and both READMEs:
  `LICENSE` is the MIT licence alone.
- **`apm.yml` from the strategy template and the worked example.** `SETUP.md` step 5 renames and
  versions `pyproject.toml` alone, and `tools/check_repo.py` reads a strategy's version there.
- **17 of the 18 eval cases that needed a shell**: the `init-example`, `init-strategy` and
  `init-researcher` copy cases, `read`'s extraction cases and their four quality cases. None had
  ever run, nine could not start for want of a history, and the team has no host whose sandbox
  runs a shell. The three `init-*` skills keep their triggering evals, and their scripts keep
  their unit tests. With them go the runner's `--no-shell` flag and the four fixtures only they
  used, and `contract/query/cites-notes`, whose graders now sit in `quality/query/claims-trace`,
  the same run.
- **`evals/findings/2026-09-22-pilot.md`**, the record of one past run; it stays in the history at
  `v0.14.0`.
- **Tests that repeated another test**, each covered by the test that stays, and the tests of the
  fixtures and the flag that went with the shell cases.
- **From the README**: the *Three commands make every folder* section, which repeated *The path*;
  the maintainers' paragraph on example markers; *Forking this package*, now one rule in
  `AGENTS.md`; the history of where the skills came from.
### Changed
- **Tests that could not fail now can.** Four Bloom Code tests passed with or without the code
  they name; each now breaks when that code does. New tests cover what a user relies on and
  nothing tested: `scaffold.py` copies byte for byte, finds a user-scope install, copies one file
  with `--only` and writes nothing before a refusal; `extract.py` writes a whole paper with its
  page markers and exits 3 for `--chapters` with no outline; the sync tool renames Experiment 1's
  documents to Experiment N. Each was checked by breaking the code in a scratch copy.
- **Every eval case runs**: `init-researcher`'s refusal when a home exists no longer needs a
  shell; the cases with a home beside the strategy check that the home is read; `clipping-at-home`
  checks the clipping is read rather than finding its name in the prompt; a regex that could not
  match a namespaced command is fixed. `evals/README.md` describes the 13 cases and 9 fixtures
  that exist, and its example commands run.
- **A file a strategy made before template 0.10.0 lacks comes back from the template**, through
  `init-strategy`'s script with `--only`, which never overwrites: in the README, `blueprint`,
  `brainstorm`, `experiment-lifecycle` 0.8.2, `data-curator-custom-calculations` 0.3.3 and
  `universe-point-in-time` 0.1.7, which sent the owner to the example and to deleting its lines by
  hand. `init-example` 0.1.4 copies a worked file into a folder of its own, to read beside yours,
  never into a strategy.
- **The home**: `Knowledge/INDEX.md` and `LOG.md` name the synthesis page `query` keeps; a
  version-history clause leaves the strategy table in `AGENTS.md`.
- **The strategy template**: `AGENTS.md` says in one paragraph where the template and the example
  live; the README's researcher paragraph names the command for each part of the order of work;
  `tools/check_repo.py`'s width check reads `templates/strategy/`.
- **Smaller**: `extract.py` says *no chapter written* where it wrote the outline; `SETUP.md` names
  the four agents that take the researcher's agent; `how-we-work` says a strategy tags the version
  its `pyproject.toml` declares; `tools/check_repo.py` reads a folder's version from `apm.yml`
  where it has one and from `pyproject.toml` otherwise; `evals/README.md` no longer documents the
  two grader types no case uses.

## [0.14.0] - 2026-09-23
The final cleaning before a newcomer meets the package: work lands on `main` without a pull
request per change, the loose ends of two closed pull requests are settled, the path from install
to first strategy is checked sentence by sentence, and the way a researcher grows beyond the
KaxaNuk Lab is written down. Home template 0.8.0, strategy template 0.10.3, example 0.10.4.

**What to do differently:** commit on `main`; open a branch and a pull request only for a change
you want reviewed. `apm update -g`, then a new session. In a home, run `update`: it brings the
home's files to template 0.8.0 and lists what is yours to edit by hand — the first
non-negotiable, the table heading *The strategies and projects it works on*, and the home's own
version in `apm.yml`. To teach your researcher a tool or a project, read *Growing your
researcher* in the home's README.
### Added
- **Growing your researcher**, a section of the home's README: a tool's or a project's
  documentation into `Sources/Clippings/`, then `read`; a skill or command of the home's own; a
  line under *What you are reading for*; a line by hand under *How it speaks* or *Non-negotiables*.
  The package README, the interview's hand-over and `next` point to it. *Joining other projects*
  in the home's `AGENTS.md` says who copies a project's files — the researcher names them and gives
  the command, the owner runs it, so `Sources/` stays the owner's — and how a clipping is named
  and a private repository cited. `read`'s `note.md` gives the convention for a tool's
  documentation as a source.
- **`next` knows more states.** A project the researcher joined through `--add-dir`, which is
  neither a home nor a strategy, is recognised and sent to *Joining other projects*, never to an
  `init-*` command; a home or strategy one folder down is named. At home it checks a clean tree
  first, skips `.gitkeep`, and lets the owner drop a *Find first* work that cannot be found; in a
  strategy, a claim carried into the blueprint as a lead counts at B, and a missing engine or
  attribution licence skips G rather than blocking it.
- **A home is committed.** The interview's hand-over, `read`'s close and `next`'s first check at
  home say to review the diff and commit; `SETUP.md` step 2 says what done looks like.
- **`update` compares in both directions** and reads `includes` and `dependencies` in `apm.yml`,
  so a home that ran it four times no longer keeps what the template dropped; the template's
  `RESEARCHER.md` and `HOW-I-INVEST.md` headings and the `INDEX.md` and `LOG.md` blockquotes come
  back as lines to edit by hand. `audit` checks a home's own skills and commands for a stale
  install.
- **The interview** proposes the home README's opening paragraph, sets the home's `apm.yml` version
  to 0.1.0, which is the owner's from then on, and says who holds `LICENSE`.
- **A strategy-side command with no home in the session** — `objective`, `blueprint`,
  `brainstorm`, `challenge` — works from the strategy alone and says so; `challenge` says it covers
  the graduation gate. `read` never offers `scaffold.py` into a strategy made from another
  template, and appends to a `LOG.md` only if it exists.
- **`tools/check_repo.py` checks width**: no line of markdown prose past 100 columns in `.apm/`,
  `templates/researcher/`, `README.md`, `SETUP.md` and `AGENTS.md`, with its tests. 236 lines in
  the Lab skills and their references were rewrapped to pass it, no word changed.
- **Three eval fixtures and three contract cases**: `blueprint` and `read` in a strategy with the
  home beside it, and `read` on a markdown clipping at home. The strategy fixtures without a home
  now test the no-home fallback on purpose.
- **`.github/CODEOWNERS`** names Alan and Arturo as the owners of every path, so a pull request,
  when one is opened, asks for their review at once. Taken over from pull request #11, which closed
  unmerged.
- **"Forking this package"** in the README: what a fork keeps, the three places that name this
  package, and one researcher package per user until two are tested side by side.
### Changed
- **Work lands on `main`.** `how-we-work` 0.3.0, this repository's `AGENTS.md` and the strategy
  template drop the issue, the branch and the pull request as a gate for every change: each
  change-set is committed on `main` with its changelog entry, and a branch is for a change someone
  wants reviewed, deleted once merged. A blueprint is committed in a commit of its own before the
  rule, which keeps the control without a branch.
- **The numbers rule names the engines the project names** — in a KaxaNuk strategy the Lab's
  libraries — in `RESEARCHER.md`, the interview, the agent it writes, the home's `AGENTS.md`,
  `query` and `objective`, so a researcher invited into a project on another stack is not told to
  distrust that project's own engine.
- **The home reads as a researcher's, not only an investor's**: *What it changes* in a note is
  measured against the owner's question; *The strategies and projects it works on*; *How it cites*
  in any other project; `HOW-I-INVEST.md` may take other headings. The README says the interview
  and the reading map cover investment research, and `read` names the map's ten papers only when
  Finance is a domain.
- **`query` 0.5.0** writes a kept synthesis page's index line and a log entry on the same go, and
  may name a work on a *Find first* line or already in `Sources/`.
- **`experiment-lifecycle` 0.8.1** describes the template as it has been since 0.10.0 — every file,
  each a description to fill in — and `references/structure.md` is at template 0.10.3.
- **Where things land**: `init-strategy` runs from the home and the strategy lands beside it, as
  `SETUP.md` and the README now say; the three `init-*` skills say how a fork passes `--package`;
  `scaffold.py` leaves cache folders behind, with tests.
- **The README** lists `evals/` and `.github/`, the eval scripts under `tools/`, and says the four
  house instructions are machine-wide for Claude Code and Copilot. `AGENTS.md` gives a route for
  trying a change that does not stage the working tree under HOME.
- **`tools/check_repo.py`** reads a folder's `uv.lock` only when git tracks it, and leaves the
  example's `CHANGELOG.md` out of the headings check: the template and the example move together
  but take their own version numbers.
### Fixed
- **`experiment-lifecycle` section 6** had a sentence cut mid-clause since 0.11.0; the paragraph is
  restored.
- **Smaller slips**: `next [strategy]` in the README; `interview` lists four agent targets, not
  `opencode`; `update`'s migration text is only for a home from before 0.7.0; the Data Curator
  skill compiles with `uv run --no-project`; the reading map sends a book to `Sources/Books/`;
  `note.md`'s Paleologo path; the home's example path is `fcf-yield-quality`, not a folder of the
  maintainer's; `evals/README.md` counts ten other commands.
### Removed
- **`docs/superpowers/`**, the eval work's design, plan and Windows notes, which 0.12.0 and 0.13.0
  shipped to every install because the package installs whole. They stay in the history at
  `v0.12.0` and `v0.13.0`. Taken over from pull request #9, which closed unmerged, with the
  addendum it added to `evals/findings/2026-09-22-pilot.md`: the blueprint surface re-run on the
  merge of 0.11.0, F-01 and F-03 holding on what `main` ships.

Left for later, as leads: a weight-matched null and a one-ingredient control in the template's
bar, a read-only `gate` command, evals for `interview`, `next` and `update`, `update` building its
URL from the installed package, and the legacy paths for homes before 0.7.0 and strategies before
0.7.15 and 0.10.0, which leave together at 1.0.0.

## [0.13.0] - 2026-09-23
The interview is `interview`, and the example researcher is no longer named after a real one.

**What to do differently:** run `interview` where you ran `researcher-init`; `apm update -g`
removes the old command and deploys the new one. In a home, `update` brings the wording across.
### Changed
- **`researcher-init` is renamed `interview`.** Two commands that were the same two words in
  either order — `init-researcher` makes the home, `researcher-init` filled it — were the first
  thing newcomers mixed up. The command is unchanged inside; every place that named it — the
  README, `SETUP.md`, `init-researcher` 0.1.2, `next`, `audit`, the reading map, the home's own
  files (home 0.7.3) and the evals — says `interview`.
- **The example researcher is `Ada`**, in the README, `SETUP.md`, `init-researcher`, the
  interview, the home's `AGENTS.md`, the eval fixtures and their tests, where it was the
  maintainer's own researcher's name. The worked example's `Bibliotheca/` keeps its provenance
  lines as they were written: they record which library its notes were carried from.

## [0.12.0] - 2026-09-23
Behavioural evals for the skills and commands, from issue #3, and the three fixes their pilot
found — merged from `issues/3` with the eval suite extended to the two skills 0.11.0 added.

**What to do differently:** `blueprint`, `brainstorm` and `challenge` take the experiment number
first: `blueprint 1`, `brainstorm 2 "an idea"`, `challenge 1 D:\Research\Golden-Flow`.
`apm update -g` brings it; in a home, `update` brings the example in `AGENTS.md` across.
### Added
- **`evals/`**: triggering requests for every skill, contract cases for `read`, `query`,
  `blueprint` and the three `init-*` skills, quality cases judged against written criteria, the
  pilot's findings, and `tools/eval_run.py`, `eval_fixtures.py` and `eval_history.py` with their
  tests, run by Claude Code's `claude plugin eval` against a real install of the working tree.
  `evals/README.md` says how; `docs/superpowers/` holds the design, the plan and the Windows notes.
  Two triggering entries are new here, for `data-analyzer-runs` and `paper-trading-gate`.
### Fixed
- **`blueprint`, `brainstorm` and `challenge` bound the experiment number to the strategy's
  path** (F-01): the optional strategy was declared first, and a harness binds arguments by
  position, so `/blueprint 1` read `1` as the path. The experiment comes first now, and
  `brainstorm` quotes a multi-word idea. Home 0.7.2.
- **`query` named works from memory** where the reading map has none (F-02): outside the map it
  now names only the kind of source. `query` 0.4.1.
- **`blueprint` deleted the template's blockquote when it wrote** (F-03), against its own text:
  the blockquote stays whole, its last line addressed to the owner.
- **The eval runner's fixture folder collided with the case's `FIXTURE` file on Windows**: the
  two names differed only by case, so every fixture case was refused as runner-written and five
  tests failed here. The folder is `fixture-files/`.

## [0.11.0] - 2026-09-22
The path is shorter to follow: a `next` command says where you stand, the order of work is
lettered so it is never mistaken for the eight steps, the interview shows its shape first, and the
two stages that had no skill — the analyzer and the paper-trading gate — have one.

**What to do differently:** run `apm update -g`, then open a new session; in a home, run `update`
to bring `AGENTS.md`'s lettered order of work across. When lost, run `next`.
### Added
- **The `next` command** — where the owner stands, at home or in a strategy, and the one thing to
  do next with the command that does it. It reads the folder against a checklist — the interview,
  the agent, the sources without a note at home; setup, then the order of work A to H in a
  strategy — and writes nothing. The README, the home's README and `researcher-init`'s hand-over
  point to it.
- **`data-analyzer-runs`**, the skill for the last block of step 3, `Data/analyzer.ipynb`, the one
  Lab module still hand-rolled and until now without a skill: the notebook's sections and what each
  measures, the information coefficient per date and on the eligible pool, the rank identity, the
  separation of return from volatility, what look-ahead costs a fitted signal, and where the
  numbers go — `RESULTS.md` first, then a blueprint's predictions by section number. Written from
  the worked example's notebook and nothing else.
- **`paper-trading-gate`**, the skill for step 7: the five criteria of `Paper_Trading/BITACORA.md`,
  how each is evidenced from `FINDINGS_N.md` and `RESULTS.md`, the usual way each fails, the
  promotion, the contract of the two scripts — a paper-trading run re-fits nothing — and what the
  assistant never decides: graduation is a person's signature.
### Changed
- **The order of work is lettered A to H**, in the template's README, the home's `AGENTS.md`,
  `experiment-lifecycle` and the commands that cite it, so *item 5* can no longer be read as
  *step 5*: the universe is C and step 2, the cycle is G and steps 4 to 6. The sentence *items are
  not steps* was the symptom. Template 0.10.2, home 0.7.1, `experiment-lifecycle` 0.8.0, `read`
  0.6.1, `universe-point-in-time` 0.1.5.
- **`researcher-init` shows the interview at a glance before question 1** — a table of the seven
  questions, what each asks, why, and where it lands — numbers every question *n of 7*, names the
  five things question 2 may cover so the owner is not left with a blank line, and hands over as a
  numbered list of what happens next, `next` last. The questions themselves and every rule around
  them are unchanged.
- **The README opens with the path**: five moves, each in a new session, in the folder the line
  names, with what each makes; and the tables list `next` and the two new skills.
### Notes
- **Two sources checked for this version, both leads, neither read into a library:** Gong (2026),
  *AI Agents in Financial Markets: Architecture, Applications, and Systemic Implications*,
  arXiv 2603.13942, whose five governance principles — bounded autonomy, traceability, diversity by
  design, embedded intervention, supervisory co-evolution — describe what this package already does
  by construction (plan-first, the go, every claim cited, nothing trades, the other side always
  named) and name what `next` adds: supervisory observability of where the work stands; and Packt's
  *Building AI Agents for Finance* (2026), whose chapter 11 evaluation harness is the shape of
  what issue #3 proposes for these skills and commands. The new primitives are in that issue's
  scope: two triggering cases each, and the contract check for `next`.

## [0.10.1] - 2026-09-22
`check_repo` names a deleted example notebook, and the template stops inheriting four of the
worked strategy's lines.
### Fixed
- **`tools/check_repo.py` crashed on an example notebook deleted from the working tree**: the
  marker check read it as an empty text and JSON refused it, so the finding that names the
  missing file never appeared. A tracked notebook that is not on disk is now skipped there, and
  the template check reports it.
- **Four lines of the worked example reached every new strategy** through the generated files
  (template 0.10.1, example 0.10.3); `experiment-lifecycle`'s reference notebook and blueprint
  template change with them.

## [0.10.0] - 2026-09-22
The strategy template ships every file its README names, generated from the worked example, from
the proposal in pull request #1.
### Added
- **`tools/sync_investment_lab_references.py` regenerates the template's files** — the drivers, the
  shared modules, the notebooks, Experiment 1's documents and the paper-trading files, eighteen in
  all, as its `TEMPLATE_FILES` lists them — from the worked example with its own lines removed, the
  way it already regenerated `experiment-lifecycle`'s references: a `.py` file comes out as its
  docstring, a notebook as its markdown cells, a document as its prose. Only the files that differ
  are written, and a missing example file stops the run with its name. **`check_repo.py` fails
  when a template file differs** from what the example says (template 0.10.0).
- **Tests for the sync tool's stripping**: the Python example block, blank lines kept around a
  removed block, adjacent blocks, the transform by suffix, the mapping against the example, and
  stale detection.
### Changed
- **A marker must stand alone at column 0, and markers inside notebook cells are checked too.**
  `check_repo.py` reads the marker strings from the sync tool and reports an indented marker, one
  with trailing whitespace, or a broken pair inside a notebook cell: the sync tool would not strip
  it, and the example's lines would reach every new strategy.
- **A removed example block no longer merges blank lines across the whole file**, so Python kept
  outside a block keeps PEP 8's two blank lines between definitions.
- **`init-example <path>` is for a strategy made before template 0.10.0**, which lacks the files. A
  strategy made now has nothing to bring across: `init-example` 0.1.2, `init-strategy` 0.1.2,
  `experiment-lifecycle` 0.7.4, `data-curator-custom-calculations` 0.3.1,
  `universe-point-in-time` 0.1.4, and the `blueprint` and `brainstorm` commands say so.

## [0.9.2] - 2026-09-22
No CI: the checks run on the maintainer's machine, as `AGENTS.md` always asked.
### Removed
- **The GitHub Actions workflow** and the README's badge. The five checks are unchanged and still
  pass before any commit, by hand, as the README's *Development* section shows; GitHub no longer
  runs them on every push, and nobody who forks or watches the repository sees a workflow run.

## [0.9.1] - 2026-09-22
Three paths in the example that failed the repository's own check.
### Fixed
- **Three chapter notes in `examples/liquid-golden-cross` had paths over 120 characters**, which
  `tools/check_repo.py` refuses because a home folder on Windows pushes them past the path limit;
  they are renamed, with every link to them rewritten and the rename logged in the example's
  `Bibliotheca/LOG.md`.

## [0.9.0] - 2026-09-22
The worked example's bibliography covers every claim, its Experiment 1 meets its last success
criterion, and its setup guide names the files it cannot download.
### Added
- **Six notes carried and two papers read in `examples/liquid-golden-cross`**, so every claim in
  its `OBJECTIVE.md` has a note behind it: Grinold and Kahn's chapters 13, 14 and 16 for the
  rebalancing band, Paleologo's chapters 6 and 8 for the sizing, the momentum review of Baltussen,
  Dom, Van Vliet and Vidojevic (2025) for the signal, and Sarkar, Du and Vafai (2019) for the
  construction. The example's own changelog, 0.10.0, has the detail.
### Changed
- **The example's `OBJECTIVE.md` is fine-tuned for claims 2 to 4** from those notes, with no
  claim's wording changed, as the order of work says a fine-tuning pass does.
- **The example's `SETUP.md` states the exact names, headers and date order of the hand-supplied
  benchmark and factor files**, and the four reserved factor names, because a file named otherwise
  is not found, or is silently counted as one more factor.
- **The example's Experiment 1 meets success criterion 1, to the data.** Its pipeline was re-run
  from a wiped working copy on a fresh download with no manual step beyond the hand-supplied
  files; every conclusion held, the filter-off control and the index came back to every
  published decimal, and the rule moved within hundredths and one rebalance. `FINDINGS_1.md`
  carries the re-run's figures beside the published ones, which stand.

## [0.8.2] - 2026-09-22
Two lines the first testers would have missed.
### Fixed
- **`SETUP.md` asks for a global git identity before anything is made.** Every folder the three
  commands make starts as a git repository with a first commit, and on a machine whose identity is
  set only per repository the commit stopped, as it did on the maintainer's own; the script's
  recovery message and the skill's instruction to ask were right, but the stop was avoidable.
- **The README's three steps name the agent deploy.** Step 2 said to run `researcher-init` in the
  home but not the `apm install --target <agent>` there that deploys the researcher as an agent
  called by name; `SETUP.md`, `init-researcher` and the home's README already said it.

## [0.8.1] - 2026-09-22
What `apm update -g` does to the retired packages, as it did on a real machine.
### Fixed
- **`update` and the 0.8.0 upgrade note say what the update really does to the eight retired
  `KaxaNuk/KaxaNuk-Agent-Skills` packages**: it removes what they deployed, and every skill and
  command of this package stays deployed, but `apm deps list -g` may keep naming them as orphaned,
  because their folders stay under `~/.apm/apm_modules/`. That is harmless; `apm prune` and
  `apm uninstall -g` do not reach them in APM 0.29.

## [0.8.0] - 2026-09-22
A package for teaching: four leftovers of the old per-repository setup are gone, the researcher's
interview places you in the history of investment research, and every Lab skill now matches the
worked example's code.

**What to do differently:** run `apm update -g`, then open a new session. The update removes the
deployed copies of the removed skills and command, and the eight orphaned
`KaxaNuk/KaxaNuk-Agent-Skills` packages an install from before 0.7.0 still carries
(`apm deps list -g` lists them). In a home, run `update`, and deploy the agent with
`apm install --target <agent>`.
### Added
- **A reading map for `read`**, `references/reading-map.md`: Section 01, *The Evolution of
  Investment Research*, of KaxaNuk's Investment Research Bootcamp, session 02, distilled. The ten
  papers of the two dated timelines; where each stance and each commonly held belief sits, who
  tested it and its other side; the pairs the deck sets against each other; the six acts with the
  arc's 21 questions and their works; *Nothing is discarded*; KaxaNuk's position; and Act VII's four
  open problems. Every work is as the deck gives it, and each one is a lead, never a citation.
- **`backtest-engine-runs` lists what the engine is called with**: the `entities.Configuration`
  fields, the three price roles and the CSV input handlers the worked example runs on engine
  0.66.0. It also records that `commission_cents=0.1` was charged about $0.083 a share.
- **A root `.gitattributes`** (`* text=auto eol=lf`), so a Windows clone checks out the bytes that
  were committed.
- **Tests for every check in `tools/check_repo.py`** and for
  `tools/sync_investment_lab_references.py`.
### Changed
- **`researcher-init` 0.7 asks seven questions**, in the owner's language from the first (Spanish
  or English): language and name; what you do; the researcher's name, domains, voice and rules in
  one call; how you see markets, three questions whose options are the reading map's stances
  and their papers; where you stand in the evolution of investment research, who tested it and who
  disagrees; what you are reading for, each question with what it feeds and what would change your
  mind; and *Find first*, the works to put in `Sources/`. There are no strategy questions. A re-run
  keeps what the owner wrote, and `Philosophy/HOW-I-INVEST.md` takes only what the owner typed. It
  also names the home: `apm.yml` gets the researcher's slug, a description and the owner as
  author, so a home no longer carries the name `kaxanuk-researcher`.
- **`read` and `query` use the map.** `read` names the *Find first* works when `Sources/` has
  nothing left to read, and after each read the map's other side of what was read; a note's
  citation never comes from the map. `query` names the missing work when it would close a gap.
- **`update` reads what is new before it installs it**: the newest `CHANGELOG.md` and
  `templates/researcher/` from GitHub `main`, and the installed version from `apm deps list -g`.
  It compares each of the home's own files — `AGENTS.md`, `CLAUDE.md`, `README.md` in substance,
  `LICENSE`, `apm.yml`'s comments only, `.gitignore` and `.gitattributes` — and runs
  `apm update -g --yes`, since the owner's go is the confirmation. It then adds a *Brought to
  template X.Y.Z* entry to the home's `CHANGELOG.md`, so the next `update` reports only newer
  versions; the rest of the home's history is left as it is.
- **`how-we-work` 0.2.3 is written for one package.** A release takes one `vX.Y.Z` tag, pushed
  after the merge, and runs `uv lock` where a `uv.lock` is committed. The root CHANGELOG keeps Keep
  a Changelog. Where a repository's `AGENTS.md` makes issue branches a recommendation, as a
  strategy's does, they are suggested, never a gate.
- **The engine skills install and run through `uv`.** `backtest-engine-runs` 0.1.4 and
  `attribution-analysis-runs` install with `uv pip install` from the repository root, so the
  licensed package lands in the strategy's `.venv`, and every CLI call runs through `uv run`;
  `init excel` is only for a project outside a Strategy Template repository.
  `backtest-engine-runs` also says the weight file sums to exactly one, with the residual in the
  cash proxy, and that `cash_reserve_percentage` cures a truncated run (the example needed 2%).
- **`data-curator-custom-calculations` calls `main()` with `data_block_providers`** (Data Curator
  0.50.0 or later), as the worked example does, instead of the deprecated per-kind providers, and
  says each data block a run reads, dividends and splits included, is mapped to a provider there,
  and that one provider can serve them all.
- **`universe-point-in-time` 0.1.3** lists the impossible-daily-move check the worked example
  writes to `Data_Issues.csv`, calls `Data/refinery.py` and `Data/analyzer.ipynb` the worked
  example's, since the template ships neither, and gives `init-example Universe/universe.ipynb` to
  a strategy that has only the seed.
- **`experiment-lifecycle` 0.7.3 and the `blueprint` and `brainstorm` commands describe a strategy
  as `init-strategy` makes it**: it installs nothing, the skills are installed once for the user,
  `Experiments/` holds `Experiment_1/` with three empty output folders, and the header-only seed is
  never deleted; `Universe/universe.ipynb` is brought by its path. The skill's references are
  called copies of the worked example's Experiment 1, not files the template ships. Notebooks are
  stripped with `uv run --group notebook jupyter nbconvert`, because a bare `uv sync` leaves
  nbconvert out, and the skill's references are regenerated with `uv run --no-project python`, as
  `AGENTS.md` says. `references/structure.md` names template 0.9.0 and the files it ships inside
  its folders.
- **`init-strategy` gives the real reason for a short path on Windows**: deep paths inside the
  folder, such as `.venv/`, break tools later with misleading errors such as `WinError 3`.
- **SETUP.md says what each `--target` receives at user scope**: Claude Code and Copilot
  everything; Cursor, Gemini, OpenCode and Windsurf the skills and commands without the
  instructions; Codex the skills only, and runs a command by naming its file in the package.
- **The README says what a strategy needs from outside the package** (a data provider's key for
  FMP, Sharadar or LSEG, the Backtest Engine and Attribution Analysis licences, access to the
  private Portfolio Construction repository) and what runs without them. Its tree lists every
  top-level file but itself.
- **The README's Development section and `AGENTS.md` run exactly what CI runs**, each through `uv`:
  the tests, ruff, ruff on the worked example, `tools/check_repo.py` and the Bloom Code check. CI
  now lints the worked example and checks its Bloom Code style too.
- **Markdown is wrapped at 100 columns** where it is written or changed; the house-style
  instructions, `bloom-code-lint`, the README, SETUP.md and `AGENTS.md` are rewrapped, their words
  unchanged but for BLOOM012's description, under Fixed.
- **The starting points move with it**: the strategy template and the worked example to 0.9.0, the
  researcher's home to 0.7.0. Their own changelogs say what changes in a strategy and in a home.
### Removed
- **`devcontainer-aware-command-execution`.** No KaxaNuk starting point has a dev container, yet
  the skill told the assistant in every folder to look for `.devcontainer/devcontainer.json` and
  run `docker ps` before its first shell command.
- **`propagate-mcp-env-vars`**, its script and its tests. No manifest here or in the starting
  points declares an MCP server; the skill assumed a per-project `.mcp.json` and a
  `.devcontainer/.env`, and its `apm install --mcp` advice was wrong for the APM in use. CI and
  `tests/conftest.py` no longer name it.
- **The `initialize-apm` command.** It set APM up per repository with `pip`, a
  `requirements-dev.txt` and one `apm install` per dependency, a layout a strategy no longer has.
  APM is installed once with `uv tool install apm-cli`, and this package with `apm install -g`.
- **`apm-usage`**, a one-link skill that framed APM as a project's dependencies. The APM commands a
  learner runs are in SETUP.md, which now links APM's own reference.
- **`metadata.version` in the commands' frontmatter.** APM keeps only `description`, `input`,
  `allowed-tools`, `model` and `argument-hint` for a command, and printed a *dropped: metadata*
  warning for each one on install. The versions live in this changelog.
- **`apm-cli` from the development group** in `pyproject.toml`: APM is a tool installed once, not a
  dependency of this repository's environment.
### Fixed
- **`teach` receives its topic.** Its body read empty backticks where `${input:topic}` belonged.
- **`init-strategy`, `init-example`, `init-researcher` and `read` run `scaffold.py` with
  `uv run --no-project python`.** SETUP.md installs no Python, and on Windows a bare `python` is
  the Microsoft Store alias. `bloom-code-lint` 0.1.1 runs its checker the same way, with the
  project's ruff line length (100 in a strategy) instead of 120. Its BLOOM013 hint and the
  `data-curator-custom-calculations` template name the error message `message`, not `msg`, as the
  strategy's `AGENTS.md` does.
- **`scaffold.py` run from a checkout copies that checkout's starting points**; it looked one
  folder too low and silently copied an installed package's. A new strategy, home or example now
  starts on branch `main` whatever `init.defaultBranch` says, and when the first commit fails the
  script prints the `git commit` that finishes it.
- **`alpha-decomposition` 0.3.4 prices a counterfactual with the worked example's functions**
  (`securities_panel.expand_to_identifiers`, then `backtest_engine.write_weight_file`,
  `build_configuration` and `run_backtest`), not `to_engine_frame` and `run_variant`, which never
  existed, and says what `eligible_matrix` is.
- **`portfolio-construction-runs` 0.2.2 describes the module the example ships**:
  `weigh(selected, history, method, maximum_weight)`, one cut in `build_weights`, and its
  `maximum_weight` and `minimum_holdings` constraints. `ConstructionSettings`,
  `build_target_weights` and `risk_lookback_days` are gone. It says which methods `weigh` builds,
  those whose configuration has no required field, and that the rest need a weigher of their own.
- **`backtest-engine-runs` 0.1.4 and `attribution-analysis-runs` 0.2.5 guard the import with
  `importlib.util.find_spec`**, as `portfolio-construction-runs` and the worked example do, not
  with a `try` around `from kaxanuk… import …`, which Bloom Code rejects (BLOOM003).
- **`attribution-analysis-runs` 0.2.5 computes returns from
  `m_close_dividend_and_split_adjusted`**, the basis the backtest marks on; a split-adjusted column
  dropped every dividend from the attribution.
- **`data-curator-custom-calculations` 0.3 knows the strategy template's layout**: `c_*` columns go
  in `Data/Curator/custom_calculations.py`, selected among the columns `Data/curator.py` requests,
  never in `Config/`; a cross-sectional or swept column is an `r_*` column in the Refinery, computed
  by the worked example's `Data/refinery.py`, which the template does not ship.
- **`backtest-engine-runs` says KaxaNuk Strategy Template** where it still said KN Research
  Process.
- **`audit`'s frontmatter rule applies to a source note or a book's `INDEX.md` only**, so concept
  and synthesis pages are not reported twice, and its note on stale installs no longer writes an
  input placeholder that APM rewrote on install.
- **`read` no longer says the template ships its Bibliotheca files "on `main`"**: the template is a
  folder inside this package.
- **The `python-test-writing` instruction's example declares `-> None`** on its test methods, as
  Bloom Code requires.
- **`tools/check_repo.py` checks a non-ASCII path** (`git ls-files -z`, decoded as UTF-8) instead
  of skipping it, measures a one-line skill description, and fails on one it cannot read.
- **`tools/sync_investment_lab_references.py` writes only the references that differ**, says so
  when none do, and stops with the file's name when a worked-example document is missing instead
  of writing an empty reference.
- **Tests**: `bloom_code_check`'s ASCII-output test no longer fails in a temporary folder with a
  non-ASCII path, and the scaffold test checks that the first commit really exists.
- **`LICENSE` names the `read` and `query` skills and the `audit`, `refine`, `refresh-index` and
  `teach` commands**, not a `compile` command that does not exist.
- **`experiment-lifecycle`'s notebook reference no longer carries the worked example's figures.**
  Section 6, *Counterfactuals*, marked the example's 45.5 of 159.5 points and its four choices as
  the template's description; they are now the example's own lines. The skill's section table
  lists 6 · Counterfactuals and 7 · Verdict, as the notebook does.
- **`experiment-lifecycle` says to retitle a copied experiment notebook**: `experiment_N.ipynb` is
  copied from Experiment 1's, so it is retitled `Experiment N`, every `_1` becomes `_N`, and the
  sentences that only apply to the benchmark go, as they already did in the blueprint.
- **`tools/sync_investment_lab_references.py` writes `experiment-notebook.ipynb` in nbformat's
  own form**, keys sorted and ending in a newline, and the worked example's notebooks carry the
  cell ids nbformat 4.5 requires, so stripping a notebook copied from the reference, or from the
  example, changes nothing.
- **`blueprint` and `brainstorm` give Experiment N > 1 its blank file**: the `experiment-lifecycle`
  skill's `references/` template, copied into `Experiment_N/`. The `init-example` command they gave
  copies `Experiment_1/`'s file, which the owner already has, so it was refused.
- **`init-strategy` restores a lost template file from the template**, not with `init-example`,
  which copies the worked example's filled-in version: `scaffold.py strategy . --only <path>`.
- **The strategy template's README, step 4 of its and the worked example's `SETUP.md`,
  `experiment-lifecycle`'s `structure.md` and `scaffold.py`'s missing-package message give the
  install command with `--target`**, as this package's SETUP.md does; they gave it bare, and a bare
  `apm install -g` on a machine with no agent folder deploys to Copilot and `.agents/`.
- **`update` compares `LICENSE` too, and records the template version it brought** as a *Brought
  to template X.Y.Z* entry at the top of the home's `CHANGELOG.md`, so the next `update` no longer
  reports the same versions again.
- **`researcher-init` keeps the tag policy and the strategy rows on a re-run under `force`**, which
  the home's 0.7.0 upgrade note now names; a plain re-run stops on a filled `RESEARCHER.md`.
- **`extract.py` stops on a password-protected PDF with its message** instead of a traceback:
  pypdf returns, rather than raises, when the empty password fails, so the check never fired.
- **`extract.py` opens the AES-encrypted PDFs publishers ship**: `read` 0.6.0 declares
  `pypdf[crypto]`, without which pypdf stopped with a `DependencyError` traceback on an AES-256 PDF
  and silently lost an AES-128 PDF's outline. A file that is not a PDF stops with a message, not a
  traceback.
- **`read` carries `--depth 2` into the extraction of a book whose depth 1 is parts.** Without it,
  `--chapters` counts the parts, and a chapter chosen from the depth-2 outline extracted a part or
  stopped with *no chapter at this depth*.
- **`read` extracts only the chapters chosen from a book with no outline.** `extract.py` refused
  `--split` with `--chapters`, so a shorter split renumbered the chapters from 1 and overwrote
  `OUTLINE.md`. `--split` now names the whole book and goes with `--chapters` or `--all`; `--split`
  alone is refused.
- **`read` says the extract's page markers are PDF pages**, not the numbers printed in the book: a
  note cites them, a book's `INDEX.md` says by how much the printed numbers differ, and `--split`
  takes PDF pages. It said the markers were the page numbers, so a book with front matter was cited
  off by its length.
- **`bloom-code-lint` 0.1.1 counts each call of a chain on the line of its method**, so a pandas
  chain split one call per line passes BLOOM012; it counted every call on the chain's first line,
  where no line break could clear it.
- **`bloom-code-lint` and the Bloom Code instruction say what BLOOM012 counts**: every call that
  starts on a line, nested or side by side, at most two (one under `--strict`). The message called
  `a(x) + b(y) + c(z)` "more than one nested call"; what the checker reports is unchanged.

## [0.7.1] - 2026-09-21
A shorter, more focused researcher interview.
### Changed
- **`researcher-init` is shorter.** The interview drops the strategy and tag-policy questions; tags
  default to loose, and the strategies table starts empty — strategies are added when the researcher
  is invited into one, not at setup. Language defaults to English. The remaining eight questions
  focus on who you are, how you invest and what you're reading for.

## [0.7.0] - 2026-09-21
Every KaxaNuk skill is in this package. One install and one `apm update -g` bring them all to every folder.
### Added
- **The Investment Lab skills**, from KaxaNuk-Agent-Skills at its commit `3b8f76c`, unchanged but for the lines that named the package they came from: `experiment-lifecycle` and `alpha-decomposition`, the process; `universe-point-in-time`, `data-curator-custom-calculations`, `portfolio-construction-runs`, `backtest-engine-runs` and `attribution-analysis-runs`, one for each library; and the house rules, `how-we-work`, `bloom-code-lint`, `apm-usage`, `devcontainer-aware-command-execution`, `propagate-mcp-env-vars`, the `initialize-apm` command and the Bloom Code, PEP 8, test-writing and filesystem-boundaries instructions. The tests of `bloom_code_check.py` and `propagate_mcp_env_vars.py` came with them.
- **`tools/sync_investment_lab_references.py`** regenerates `experiment-lifecycle`'s references from the worked example on disk instead of from GitHub, and **`check_repo.py` fails when they differ**, so the skill and the example cannot drift apart.
### Changed
- **The package depends on nothing.** `KaxaNuk/KaxaNuk-Agent-Skills/kaxanuk`, which was unpinned, is gone from `apm.yml`; a skill and the template it describes now change in one pull request. After `apm update -g`, `apm deps list -g` shows the KaxaNuk-Agent-Skills packages as orphaned; the `update` command says so.
- **CI checks Bloom Code with the repository's own `bloom-code-lint`**, over every skill's scripts, the tests and the tools, instead of fetching the checker.
- `AGENTS.md`, the README, `researcher-init`, `update`, the strategy template's README (template 0.8.1) and the home's `AGENTS.md` (home 0.6.1) name one package.

## [0.6.6] - 2026-09-21
The README says how to install once.
### Changed
- **One *Install* section** replaces the prompt in the introduction and *Install once, for your user*: the prompt to paste into Claude or Codex, the two commands by hand, then the first three commands in a new session.
### Removed
- **The root `uv.lock`**, which nothing read: CI runs with `--no-project`. It is ignored from now on. The worked example keeps its own, which pins the versions its results were run with.

## [0.6.5] - 2026-09-21
The README's install section gives both ways in.
### Changed
- ***Install once, for your user* starts with the prompt to paste into Claude or Codex**, what the assistant then does, and that `SETUP.md` is what it follows; the commands by hand come second. The prompt reads the same everywhere it appears: *Please help me install this repo: https://github.com/KaxaNuk/KaxaNuk-Researcher*.

## [0.6.4] - 2026-09-21
`extract.py`, the script `read` runs, has tests and the house style. What it writes is unchanged.
### Changed
- **`extract.py` follows Bloom Code**, like every other script here: no nested functions or reassigned names, one item per line, imports as modules, a dataclass where a tuple was returned. Its outlines, console output and extracts were compared byte for byte, before and after, on two books from a real library, with both engines and with `--split`: identical.
### Added
- **Tests for `extract.py`**: chapters from an outline and their front matter, `--chapters` and `--split` parsing and their errors, text cleaning, slugs, and a ten-page PDF built in the test for the outline and for a PDF with no text layer. CI runs them and checks the script's style.

## [0.6.3] - 2026-09-21
The repository checks itself, locally and on every push.
### Added
- **`tools/check_repo.py`**, with tests: the package and each starting point declare one version across `apm.yml`, `CHANGELOG.md`, `pyproject.toml` and `uv.lock`; every heading of a template document is in the example's copy, so the two cannot drift apart as they did on two branches; the example's markers open and close in order; no section symbol; skill descriptions within APM's limit; no path over 120 characters.
- **CI** on every push and pull request: the tests, ruff, `check_repo.py`, and the Bloom Code style of the scripts, with the checker fetched from KaxaNuk-Agent-Skills. A badge in the README.

## [0.6.2] - 2026-09-21
The install works from a deep home folder on Windows.
### Fixed
- **`apm install -g` failed with *checkout failed*** when the user's home folder was more than about 60 characters deep: one note in the worked example had a 130-character path, which took the installed copy past Windows' 260-character limit. The note is renamed `Sullivan_Timmermann_White_1999_Data_Snooping.md` (example 0.8.1); the longest path in the repository is now 116 characters. Found by installing into an empty, deliberately deep home.
### Added
- **`SETUP.md` gives the fallback,** `git config --global core.longpaths true`, for a path that is still too long.
- **`apm.yml` says why `kaxanuk` is unpinned.** APM warns about it on every install; a semver range does not resolve against KaxaNuk-Agent-Skills' tags today, and a literal tag would freeze the Lab's skills.

## [0.6.1] - 2026-09-21
A new user can install from the URL alone.
### Added
- **`SETUP.md`**, what an assistant follows when it is given only this repository's URL: the two tools, the one install for the user, then `init-researcher`, `researcher-init` and `init-strategy`, each in a new session, with the Windows short-path warning and the rule that a git identity is asked for, never invented.
### Changed
- **The README opens with the prompt to paste and the first ten minutes in four commands,** before the reference tables.
- **`researcher-init`, step 5,** says the skills are already installed for the user, and that `apm install` in the home deploys only the agent.

## [0.6.0] - 2026-09-21
The KaxaNuk Researcher is one repository and one package: its skills and commands, the three commands that make every folder, and the strategy template, its worked example and the researcher's home they copy. Versions up to 0.5.6 are in `KaxaNuk/KaxaNuk-Researcher-Template`'s `CHANGELOG.md`; the strategy template's history is in `templates/strategy/CHANGELOG.md`.
### Added
- **`init-researcher`, `init-strategy` and `init-example`**, skills the owner runs by name. Each copies a starting point into a new folder with `init-strategy`'s `scripts/scaffold.py` — byte for byte, never from memory — after a plan and the owner's go, and makes it a git repository with its first commit. `init-example <path>` copies one file or folder of the worked example into an existing strategy: a file already there with the same content is skipped, and one with other content stops the copy. The script finds the package beside itself, under `apm_modules/`, or under `~/.apm/` where `apm install -g` puts it, and has unit tests.
- **`templates/strategy/`**, the KaxaNuk Strategy Template at 0.8.0, from `KaxaNuk/KaxaNuk-Strategy-Template`'s `main`; **`examples/liquid-golden-cross/`**, its worked example at 0.8.0, from that repository's `example` branch; **`templates/researcher/`**, the researcher's home at 0.6.0, from `KaxaNuk/KaxaNuk-Researcher-Template`. All three are ordinary folders, and the template and the example no longer live on two branches kept in step by hand — 0.7.14 reached one and not the other. A strategy's `Bibliotheca/BIBLIOGRAPHY.md` and `LOG.md` ship empty in the template.
### Changed
- **The researcher is a package installed once for the user.** `read`, `query` and the ten commands were copied into every home, so each home carried code it could not safely edit and every version arrived by a git merge. Now `apm install -g KaxaNuk/KaxaNuk-Researcher` puts every KaxaNuk skill — this package's and, through its dependency on `KaxaNuk/KaxaNuk-Agent-Skills/kaxanuk`, every Investment Lab package's — in every folder the owner opens; `apm update -g` brings each new version everywhere; and a strategy installs nothing.
- **`scripts/extract.py` and `references/note.md` live in the `read` skill's folder,** and the skills name them by *this skill's directory*.
- **Files a strategy lacks come from the package.** `read` copies the empty bibliography and log from the template with `scaffold.py --only`; `blueprint` and `brainstorm` give `init-example Experiments/Experiment_1/...` instead of fetching a branch of the template's repository.
- **`update`** runs `apm update -g`, and compares the home's `AGENTS.md`, `CLAUDE.md` and `.gitignore` with `templates/researcher/`, showing what changed rather than merging. For a home from before this release it is the migration: it removes the home's copies of the skills, commands, script and reference, empties `apm.yml`'s dependencies, and installs the package for the user, keeping the agent and any skill the owner wrote.
- **`researcher-init`** checks for the skills at user scope; **`audit`** compares installed copies under `~/.claude/` with the packages under `~/.apm/apm_modules/`.
### What to do differently
- **Install once:** `uv tool install apm-cli`, then `apm install -g KaxaNuk/KaxaNuk-Researcher --target <your agent>`.
- **A home from before this release runs `update` once.** Until then it keeps working on the copies it has.
- **A new strategy is `init-strategy <name>`**, not *Use this template*; the example is `init-example`.
