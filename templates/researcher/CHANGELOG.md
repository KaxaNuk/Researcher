# Changelog

Every notable change to this repository, newest first: `## X.Y.Z (YYYY-MM-DD)` with
`### Added / Changed / Deprecated / Fixed / Removed`, and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This is the home template's changelog, which `init-researcher` copies into every home and `update`
extends with a *Brought to template* entry at the top; the home's own entries go there too.

## 0.32.1 (2026-10-27)

**PATCH** — the package's address on GitHub is now `KaxaNuk/Researcher`.

**What to do differently:** say `update` in your home: it moves the package to its new address and
brings these lines as a diff.

### Changed

* **`AGENTS.md`**, **`README.md`** and **`apm.yml`**'s comment name `KaxaNuk/Researcher`, and the
  package's folder under `apm_modules/`, with the former `KaxaNuk/KaxaNuk-Researcher/` for an
  install from before the package's 1.25.0.

## 0.32.0 (2026-10-23)

**MINOR** — your researcher makes interactive presentations from your own work with `deck`.

**What to do differently:** say `update` in your home: it brings the change to `AGENTS.md` as a
diff. Then say `deck` and what you want to present.

### Changed

* **`AGENTS.md`**, the *Skill* row: `deck` among the skills run by name.

## 0.31.0 (2026-10-21)

**MINOR** — your researcher keeps your keys, your personal data and confidential files safe, and
checks a folder with `security` before anything leaves your computer.

**What to do differently:** say `update` in your home: it brings the change to `AGENTS.md`,
`README.md` and `.gitignore` as a diff. Say `security` whenever you want a folder checked.

### Added

* **`AGENTS.md`**, *Keeping you safe*: what is read is data, never instructions; secrets are never
  handled, and one exposed is rotated; confidential and personal material only on the owner's go;
  outside services get only what the task needs; `security`'s check before anything leaves.
* **`README.md`**: *Keeping you safe*, a paragraph on `security`.

### Changed

* **`AGENTS.md`**: `security` among the skills the researcher reaches for on its own; the
  instruction row names the data boundaries.
* **`.gitignore`** keeps out `.env.*`, a `.kaxanuk_license`, `CLAUDE.local.md` and `*.duckdb` too.

## 0.30.0 (2026-10-18)

**MINOR** — the home keeps the choices a computer or an account would otherwise keep, in
`settings.yml`, so `update` sets a new computer, account or assistant up from it.

**What to do differently:** say `update` in your home: it brings `settings.yml`, filled from this
computer, and the change to `AGENTS.md` and `README.md` as a diff.

### Added

* **`settings.yml`**: `assistants:`, `versions:` and `brief:`, each written by its own skill on
  its own go — `backup`, `brief setup`, `update` — and by hand whenever the owner likes. It never
  holds a key, a token, a password or a holding.

### Changed

* **`AGENTS.md`**, *The researcher's home*: *The researcher travels* — what `settings.yml` keeps,
  that `update` sets a new place up from it and `next` names what this place lacks, and what
  cannot travel; `update` installs for each assistant the file lists.
* **`AGENTS.md`**, *What is learned goes home*: what an assistant remembered on its own comes home
  through `bring-home`, on the owner's go; `RESEARCHER.md`'s fourth addition names it.
* **`AGENTS.md`**: a paragraph on `settings.yml`, the owner's file; `brief setup` saves it alone;
  *Versions* says the sending choice and the e-mail travel in it; `bring-home` joins the skills run
  by name; *Hard don'ts* keeps a secret or a holding out of it.
* **`README.md`**: `settings.yml` in *Your folders*; *Take it with you*, after *A copy off this
  computer*; *Installing and updating* points a new machine to it.

## 0.29.0 (2026-10-18)

**MINOR** — a scan can be made searchable beside itself in `Sources/`, and the library's tools
include the OCR that does it.

**What to do differently:** say `update` in your home; the change to `AGENTS.md` comes as a diff.

### Changed

* **`AGENTS.md`**, the row for `Sources/`: a scan's searchable copy, `<its name> (OCR).pdf`, made
  beside it by the `read` skill's `scripts/ocr_pdf.py` on the owner's go, is the second write
  there; *Hard don'ts* says the two copies.
* **`AGENTS.md`**, *Knowledge conventions*: the library's tools include `ocr_pdf.py`, and
  `render_pages.py` also shows the page images `read` reads for what an extract dropped or OCR
  may have misread.

## 0.28.0 (2026-10-18)

**MINOR** — the library's tools are named where every skill reads them, a delegate's draft is
checked before it reaches `Knowledge/`, and a download that refuses goes to the owner.

**What to do differently:** say `update` in your home; the change to `AGENTS.md` comes as a diff.

### Added

* **`AGENTS.md`**, *Knowledge conventions*: the library's tools in the `read` skill's `scripts/` —
  `unread_sources.py`, `check_library.py`, `check_numbers.py`, `render_pages.py` and
  `update_concept_pages.py` — what each is for, and that an existing concept page is updated
  through `update_concept_pages.py`, its diff shown first.
* **`AGENTS.md`**, *Knowledge conventions*: a delegate's draft is staged outside the home and
  checked against its extract before the plan; only checked drafts are written.
* **`AGENTS.md`**, *Hard don'ts*: a download behind a login, a refusal, a busy server or a bot check
  is the owner's to fetch in their browser, never got past.

### Fixed

* **`AGENTS.md`**, *Where the skills, the commands and the agent live*: the researcher's skills
  include `workshop` and `known-answer`, which it reaches for on its own.

## 0.27.0 (2026-10-12)

**MINOR** — a brief may hold the owner's weekly update, and today's brief may be changed the same
day on the owner's word.

**What to do differently:** say `update` in your home; the change to `AGENTS.md` comes as a diff.

### Changed

* **`AGENTS.md`**, the row for `Briefs/`: up to four parts, *Week* the fourth, written one day a
  week; a brief is changed only the same day on the owner's word, never by the schedule and never
  afterwards.

## 0.26.1 (2026-10-11)

**PATCH** — the rules name every place advice is never given, and the README says what the MIT
licence does not cover.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff.

### Changed

* **`AGENTS.md`**, *Hard don'ts*: a brief, a round, a study, a lesson or an answer never says buy,
  sell, trim, add or hold.
* **`README.md`**, *What it is, and what it is not*: the companies that receive what your
  researcher reads, by example: Anthropic for Claude, OpenAI for Codex, Google for Gemini.
* **`README.md`**: *Contact*, one address for each kind of question, in place of the addresses in
  *The KaxaNuk Investment Lab* and the disclaimer's *Questions* line.
* **`README.md`**, *Licence*: the KaxaNuk Researcher package's MIT licence grants no right in
  KaxaNuk's names, the Investment Lab's libraries, the Analytics Factory's files, KaxaNuk's
  Research Models or Training Workshops.

## 0.26.0 (2026-10-10)

**MINOR** — your home's guide and rules read more simply, and its README says what your researcher
is for and what it is not.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md`, `README.md` and
`apm.yml` come as a diff.

### Added

* **`README.md`**, after the opening: *What it is, and what it is not* — a research and learning
  tool, never investment advice; it runs through your assistant, and what it reads goes to the
  company behind it, never to KaxaNuk; MIT, as is.

### Changed

* **`AGENTS.md`**: each rule said once, in its own section, and the others point to it. 6,576
  words, from 6,648.
* **`README.md`**: each folder and idea described once. What stays on this computer is said once,
  under the folder table, and *Directionality* is one sentence; the Lab paragraph points to the
  package's README for how to ask for a licence.
* **`apm.yml`**: shorter comments; the install commands are in `README.md`'s *Installing and
  updating*.

## 0.25.2 (2026-10-10)

**PATCH** — the interview's first question is shorter.

**What to do differently:** say `update` in your home; the change to `README.md` comes as a diff.

### Changed

* **`README.md`**, *The path*: the interview's two questions are what you do and what you're
  working on, and the researcher's voice.

## 0.25.1 (2026-10-10)

**PATCH** — the interview no longer asks what you are here for: it proposes it from what you say.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff.

### Changed

* **`README.md`**, *The path*: the interview's two questions are what you do and work on, what
  you'd like a hand with, and the researcher's voice; what you are here for is proposed from what
  you say.
* **`AGENTS.md`**: what the interview proposes, and you change on a word, includes what you are
  here for. 6,648 words, from 6,643.

## 0.25.0 (2026-10-10)

**MINOR** — your researcher learns KaxaNuk's tools from their documentation and from running them,
never from their code.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff, and your researcher's skill is brought to 0.5.0.

### Changed

* **`AGENTS.md`**, *Hard don'ts*: don't read, quote or copy a tool's code. KaxaNuk's tools — the
  Lab's libraries, the Analytics Factory — are known from their skills, documentation, changelogs
  and runs, never from a library's installed files, a clone, a wheel or a source page; their code,
  the Factory's files and KaxaNuk's research go into no note, clipping, strategy, study, issue or
  message; an error is told by the call, its type and its message; in a Lab library's own
  repository its rules govern its code. *Joining other projects*: from a Lab library, never its
  code. 6,643 words, up from 6,539, for the new rule.
* **`README.md`**, *Growing your researcher*: for a KaxaNuk library, its documentation and
  changelog only, never its code. The example home is `D:/Research/Arya`.

## 0.24.1 (2026-10-09)

**PATCH** — the first interview writes on your two answers, and you change what it wrote on a
word.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff.

### Changed

* **`AGENTS.md`**: the first `interview` alone writes with no plan, on the owner's two answers, and
  its hand-over names what it wrote; a change the owner asks for to it is written, its diff shown.
  *Working lean* is shorter, its defaults kept. Still at most 6,541 words.
* **`README.md`**: the interview writes the paragraph about your researcher, yours to change.

## 0.24.0 (2026-10-08)

**MINOR** — your home is read by every assistant, Gemini included, and keeps the assistants you
use on APM's list.

**What to do differently:** say `update` in your home; the changes to `AGENTS.md`, `README.md`,
`apm.yml` and `.gitignore` come as a diff, and `GEMINI.md` is brought across. Then paste the
README's install line once in each other assistant you use.

### Added

* **`GEMINI.md`**: `@./AGENTS.md` and `@./RESEARCHER.md`, so Gemini loads the rules and who your
  researcher is, as `CLAUDE.md` does for Claude; `.gitignore` no longer hides it.

### Changed

* **`AGENTS.md`**: it opens by saying to read it and `RESEARCHER.md` before the first answer, a
  greeting included — Codex, Cursor and Copilot load `AGENTS.md`, not `CLAUDE.md`. *Working in a
  strategy*, *The order of work* and *Joining other projects* move after *Hard don'ts*, so the rules
  fall within the first 32 KB Codex reads. Adding an assistant names its order: the package with
  `--target`, `user_targets.py add`, then the home. What `apm compile` writes is corrected. No rule
  dropped; still at most 6,541 words.
* **`README.md`** and **`apm.yml`**: installing for an assistant is three commands — the package
  with `--target`, `user_targets.py add`, the home — and says why the list matters.

## 0.23.1 (2026-10-08)

**PATCH** — notes are written in your language, and the names the skills read stay in English.

**What to do differently:** run `update` in your home; the change to `AGENTS.md` comes as a diff.

### Changed

* **`AGENTS.md`**: notes, pages and studies are written in the language *How it speaks* names, a
  source's terms and quotes as written; folder and file names, frontmatter fields and the headings
  the skills read stay in English. A few repeated phrases trimmed. Still at most 6,541 words.

## 0.23.0 (2026-10-08)

**MINOR** — a new home ships no investing file and no rules of its own: `philosophy` writes down
how you work or how you invest, and asks your rules.

**What to do differently:** run `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff, and *What you believe* in `RESEARCHER.md` as a line to change by hand, if you like.
Your `HOW-I-INVEST.md` and the rules you hold stay yours.

### Changed

* **`Philosophy/`** ships empty: `philosophy` starts `HOW-I-WORK.md`, how you work, or
  `HOW-I-INVEST.md`, how you invest, with its title and headings, when a round needs it; or you
  write your own by hand.
* **`RESEARCHER.md`**: *What you believe* names both files in `Philosophy/`; *Here for* lists your
  work and projects first; *Non-negotiables* starts as *None yet.* — say *remember this* to add a
  rule of your own, and `philosophy` asks for your rules; the first one written takes its place.
* **`AGENTS.md`**: `Philosophy/` holds how you work and how you invest, each your view;
  `philosophy` writes the rules you approve under *Non-negotiables*, on your go; a rule about your
  holdings goes to `Portfolio/RULES.md`, yours to write; the hard don'ts add placing an order and
  moving money. Still at most 6,541 words.
* **`README.md`**: two short questions at the start; `philosophy` writes down how you work or how
  you invest.

### Removed

* **`Philosophy/HOW-I-INVEST.md`** from the template: a home that has it keeps it.

## 0.22.1 (2026-10-08)

**PATCH** — a domain of two words gets one folder name, and the Lab is said as one offer.

**What to do differently:** run `update` in your home; the changes to `AGENTS.md` and `README.md`
come as a diff.

### Changed

* **`AGENTS.md`**: a domain folder joins the words of its name with underscores,
  `Knowledge/Personal_Finance/`, headed in `INDEX.md` as `RESEARCHER.md` spells it, and a folder
  already there keeps its name; how to get a Lab licence is read from the access line in `next`'s
  `references/investment-lab.md`, not restated. Still at most 6,541 words.
* **`README.md`**: the Lab section says the Data Curator is open source and free, and that the
  other libraries come together, with their licences, in the KaxaNuk Investment Lab; a request to
  `lab@kaxanuk.mx` names the library and what it is for, with *via KaxaNuk Researcher* in the
  subject.

## 0.22.0 (2026-10-08)

**MINOR** — the README teaches six habits for working well with your researcher, and your
researcher now reaches Gemini and Windsurf.

**What to do differently:** run `update` in your home, then once more in a new conversation — the
second proposes `gemini` and `windsurf` under `targets:` in `apm.yml` and installs the home again.
The changes to `AGENTS.md` and `README.md` come as a diff.

### Added

* **`README.md`**: *Working well with your researcher* — one task per conversation, the file rather
  than a summary, *remember this*, ask for the other side, click the links, a new conversation
  after an install or an update.

### Changed

* **`README.md`**: *The rules, loaded from the first line*, *Writing a skill or a command of your
  own* and *Installing and updating* fold away, their text kept; what installing the home copies is
  said once, in the package's `SETUP.md`. *Keep a copy off this computer* is three lines naming
  `backup` and what never goes in the copy. The Lab section names the Analytics Factory.
* **`AGENTS.md`**: *Where the skills, the commands and the agent live* says in three lines that the
  package and the home's own `.apm/` are installed for the user, never inside the home; the
  `Philosophy/` row leaves a round file's format to the `philosophy` skill; links between notes are
  standard Markdown so GitHub renders them. 6,537 words, from 6,793; no rule dropped.
* **`AGENTS.md`**: while the researcher's skill is behind the package, every greeting adds one line
  saying so, not only once a week.
* **`apm.yml`**: the description follows the package's — your own research companion, which comes
  with you to every project.

### Fixed

* **`apm.yml`**: `targets:` adds `gemini` and `windsurf`, which take the researcher's skill alone —
  installing a home reaches only the assistants listed both here and in `~/.apm/apm.yml`, so a
  Gemini or Windsurf user never had the researcher. OpenCode stays out: it rejects the agent APM
  writes for it. `AGENTS.md` and `README.md` say an assistant must be in both lists.

## 0.21.0 (2026-10-08)

**MINOR** — your researcher learns from you directly: say *remember this* and it adds the rule to
`RESEARCHER.md` itself, on your go. The interview proposes your domains and projects from what you
said.

**What to do differently:** run `update` in your home — it shows the changes to `RESEARCHER.md`'s
headings, `AGENTS.md` and `README.md` as a diff; the `RESEARCHER.md` lines are yours to carry across
by hand.

### Changed

* **`RESEARCHER.md`**: *Works for* asks what you do and what you work on, at work and on your own;
  *Here for* names *organise what I read, and help with my projects*; *Domains* are proposed by the
  interview, yours to change; *Non-negotiables* offers the two strategy rules; a projects row may
  come from the interview.
* **`AGENTS.md`**: on *learn this*, the researcher appends one line in your words under *How it
  speaks* or *Non-negotiables*, on your go, and saves it in the home; a fact about your work becomes
  a projects row or a *Works for* change shown as a diff.
* **`README.md`**: *remember this* in *Growing your researcher*; the interview's questions as they
  now are.

## 0.20.1 (2026-10-08)

**PATCH** — in a strategy, `blueprint` now reads the rule back before its go and saves your yes as a
journal entry; the home's `AGENTS.md` names that entry among those the researcher writes there.

**What to do differently:** run `update` in your home — it shows the three changed lines as a diff.

### Changed

* **`AGENTS.md`**, *Working in a strategy* and *The order of work*, part E: `blueprint`'s *the rule
  read back*, on one worked date before the go, beside the benchmark's entry and `challenge`'s.

## 0.20.0 (2026-10-08)

**MINOR** — your researcher tells you, at most once a week, when a new version of itself is out,
in one line after its greeting; `update` brings it.

**What to do differently:** run `update` in your home, then once more in a new session — the second
brings the researcher's skill that gives the weekly word.

### Changed

* **`AGENTS.md`**, *Who is speaking*: at most once a week, a fourth line follows the greeting when a
  new version is out — *not now* waits a month, *stop reminding me* turns it off. *Plan first, then
  write*: three writes are made without a go of their own, the third the dates of the weekly
  version check, in this home's git config, from any folder, never saved or sent; *Hard don'ts*
  makes room for them.
* **`README.md`**, *Stay current*: the weekly word, and `update`; a problem report names the
  versions your researcher gives when you ask *which version are you?*

## 0.19.1 (2026-10-08)

**PATCH** — the house rules described as the package now ships them: three, Bloom Code and PEP 8
for Python in KaxaNuk repositories only; and Portfolio Construction is licensed since its 2.0.0.

**What to do differently:** run `update` in your home — it shows the two changed lines as a diff.

### Changed

* **`AGENTS.md`**, the *Instruction* row: three house instructions, Bloom Code and PEP 8 for Python
  in a KaxaNuk repository and nowhere else, and filesystem boundaries.
* **`README.md`**, *The KaxaNuk Investment Lab*: Portfolio Construction is on request, and licensed
  since its 2.0.0.

## 0.19.0 (2026-10-08)

**MINOR** — your researcher saves your work for you: every go also saves a version of what it
wrote, said in one word, *Saved*, and no skill asks *Commit?* any more. A copy off this computer is
made only when you ask — *keep a copy* — with the package's new `backup` skill.

**What to do differently:** run `update` in your home — it shows the changes to `AGENTS.md` and
`README.md` as a diff, and brings them across on your go.

### Changed

* **`AGENTS.md`**, *Plan first, then write*: every go also saves a version — files by name, never
  `--all` — said in one line; `Save?` (*Save this version* / *Not now*) only where no go covers a
  save — changes made by hand, which `next` finds, and an unsaved home before `update`. A new
  paragraph, **Versions**: to you a saved version is never a *commit*; `backup` makes a private
  GitHub copy only when asked; with `kaxanuk.autosend` at `true` each saved version is sent there,
  never forced, and a failed send pauses sending until you say *back up*.
* **`AGENTS.md`**, *Working in a strategy*: the go on the plan is your review and signature and
  saves the version; the blueprint is saved alone, before the rule. *Studies* and *Joining other
  projects*: what holds a private project's material keeps any copy of the home private. `backup`
  joins the skills you run by name.
* **`README.md`**: *Save a copy off this computer* becomes *Keep a copy off this computer*, in plain
  words with no command, saying what the copy holds and what stays on this computer; the folder
  table says *kept on this computer only* where it said *committed*; the Windows line-ending note,
  which was for the assistant, leaves (the package's `SETUP.md` keeps it).

## 0.18.2 (2026-10-08)

**PATCH** — the commands this home names run APM 0.33.0, which installs the package on Windows as
cleanly as 0.29.0 did.

**What to do differently:** run `update` in your home — it shows the changed lines of `AGENTS.md`
and `README.md` as a diff — then install the new APM once, `uv tool install apm-cli==0.33.0`.

### Changed

* **`AGENTS.md`** and **`README.md`**: every `apm` command names `apm-cli==0.33.0`.

## 0.18.1 (2026-10-07)

**PATCH** — the worked example `init-example` copies is `golden-flow`: one strategy taken from the
first note to a book signed into paper trading, where `liquid-golden-cross` stopped at the gate.

**What to do differently:** run `update` in your home — it shows the changed line of `README.md` as
a diff, and brings it across on your go.

### Changed

* **`README.md`**, step 6 of *The path*: `init-example` copies `golden-flow`; reading it needs
  nothing, and running it needs the Analytics Factory's files and the Lab's two licences.

## 0.18.0 (2026-10-06)

**MINOR** — a way into the KaxaNuk Investment Lab, and less to read. `README.md` says in a short
section which Lab libraries a strategy can use — open source, licensed, on request or coming — and
gives one address, `lab@kaxanuk.mx`, for a licence, access or a problem with your researcher.
`AGENTS.md`, which loads in every session, is 401 lines where it was 462: no rule dropped and none
changed, and a new hard don't names the Lab as a fact, never as advice. Installing the home is
described as it happens — APM copies the whole folder on this machine and deploys only `.apm/` —
and every `apm` line you are told to run names `apm-cli==0.29.0`.

**What to do differently:** run `update` in your home — it shows the changes to `AGENTS.md`,
`README.md` and `apm.yml` as a diff, and brings them across on your go.

### Added

* **`README.md`, *The KaxaNuk Investment Lab***, after *The path*: what a strategy built from here
  can use — the Data Curator open source, the Backtest Engine and Attribution Analysis licensed,
  Portfolio Construction on request, the Data Refinery and the Data Analyzer coming — with
  <https://www.kaxanuk.mx/lab>, and `lab@kaxanuk.mx` for a licence, access or a problem report,
  with the version `update check` shows.
* **`AGENTS.md`, a hard don't**: the Lab is named as a fact, never as advice, and naming its
  engines as where a strategy's numbers come from is one. What a library does and how to get it is
  said only when a step needs a library you lack, or when you ask; never added unasked to
  `RESEARCHER.md`, `Philosophy/`, a brief, a study, a round of `philosophy` or a *Find first*
  line, and never as a reason to invest in anything.

### Changed

* **`AGENTS.md` is shorter, every rule kept.** What moved: the
  `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` setting and the `CLAUDE.local.md` fallback, to *The
  rules, loaded from the first line* under `README.md`'s *In a strategy or another project*, marked
  optional and for Claude Code only; how a skill or a command of the home's own is written —
  frontmatter, body, inputs, and why nothing goes in `.apm/instructions/` — to *Writing a skill or a
  command of your own (advanced)* under *Growing your researcher*, which says nothing there is
  needed to use the researcher; the history of `targets:`, to `apm.yml`'s comment; the home's
  version rule, to `README.md`'s *Installing and updating*, which states it once. The `Philosophy/`
  row holds the two writers and the whole round-file rule — read for dates and levels, quoted only
  as the record of a round, never cited as your view — and the paragraph after the folder table,
  *Plan first, then write* and the hard don'ts point to it. The skills' row and *Working lean* are
  shorter. The note on a strategy made from a template before 0.13.2, which keeps the benchmark in
  `BRAINSTORMING_1.md`, is gone: `blueprint` and `next` still read it there. "Save" meaning "except"
  now says "except", and a study is "a decision, a plan or a memo" where it said "a brief", the
  daily brief's name.
* **`AGENTS.md`, *Where the skills, the commands and the agent live***: installing the home copies
  the whole folder — `.git/`, `Sources/`, `Extracts/`, `Briefs/` and `Portfolio/` included — into
  `~/.apm/apm_modules/_local/<folder name>/` on this machine, refreshed by each install, and
  deploys only its `.apm/`; nothing leaves the machine, and on Windows a long `Extracts/` path in
  that copy can fail the install. On Codex the skills and the agent arrive, the agent without its
  tool list, and the commands and the instructions do not; with no question tool, each question
  is asked in chat with its options numbered, *Other — your own words* last, and one line on how
  to answer. The Instruction row gives the four house instructions' real scopes — Bloom Code and
  PEP 8 for every Python file, test writing for Python tests, filesystem boundaries for every file
  the assistant reads, in any project — where it said every Python project on the machine.
* **`apm.yml`**: its comment says what deploys and what the install copies, where it said that
  only `.apm/` publishes, and holds the history of `targets:`.
* **`README.md`, *Installing and updating***: the same fact about the install, in one sentence
  that names the folders it copies.
* **Every `apm` line you are told to run names `apm-cli==0.29.0`**, in `AGENTS.md` and
  `README.md`.

### Fixed

* **`CHANGELOG.md`**: a 101-column line in the 0.5.3 entry, rewrapped.

## 0.17.0 (2026-10-06)

**MINOR** — the first run lands, and the next step is clear. Attach a file in chat or name one on
your computer and the researcher copies it into `Sources/` on your go — the one write there. Every
skill that writes at home then asks `Commit?` — *Commit it for me* or *I'll review it first* — and
never commits unasked. A go is *go*, *proceed*, *ok*, *yes*, *sí*, *dale*, *adelante*, or the same
word in your language. `next`, and your researcher when you greet it, name the one next thing for
what you are *Here for*; the interview's hand-over is shorter.

**What to do differently:** run `update` in your home — it offers the new researcher skill, with
the greeting, commands on Codex and a safe slug, as a diff, and on your go writes it, renames the
agent with it when the slug changes, and reinstalls the home. The changes to `AGENTS.md`,
`README.md` and `.gitignore` come with it, as a diff too.

### Changed

* **`AGENTS.md`**: the `Sources/` row allows one write — a source you attach or name, copied in on
  your go under its own file name, never over an existing file; nothing there is moved, renamed,
  edited or deleted. *What is learned goes home*, *Working in a strategy*, *Joining other projects*
  and the first hard don't say the same. *Plan first, then write* lists the go words, and has a
  skill that wrote at home offer the commit, your pick its go. *Who is speaking* answers a greeting
  with the one next thing, and on Codex a command you name is followed from its file in the
  package.
* **`.gitignore`**: `desktop.ini`, which Explorer leaves in a folder, beside `.DS_Store` and
  `Thumbs.db`.
* **`README.md`**: the `Sources/` row and step 2 of *The path* — attach or name a file, copied in
  on your go; step 6 reads the worked example, `init-example`, before `init-strategy`; *Save a copy
  off this computer* says every skill that writes here offers to commit; *Lost?* says `next` names
  the one next thing for what you came for.

## 0.16.0 (2026-10-04)

**MINOR** — setup is about you, and your investment philosophy has a skill of its own. `interview`
asks a few questions about you, about three minutes, and writes nothing in `Philosophy/`;
`philosophy`, a second interview in the package, optional and pitched at what you already know,
adds what you typed to `Philosophy/HOW-I-INVEST.md`, word for word, and keeps each round in
`Philosophy/Evolution/`, so you can see how your view moves. `Philosophy/` has two writers,
`philosophy` and `refine`. `RESEARCHER.md` gains a *Here for* line and ships *What you are reading
for* with no slot, for the first `read` to fill; and the home makes room for a daily brief,
`Briefs/`, and the holdings it reads, `Portfolio/`, both kept out of git.

**What to do differently:** run `update`; accept the new `Philosophy/` row before your first round.
The paragraph after the folder table comes with it, and `.gitignore` gains `Briefs/` and
`Portfolio/`. Your `RESEARCHER.md` and `Philosophy/` stay as they are: add a *Here for* line under
*Who*, or `## Why I invest` at the top of `HOW-I-INVEST.md`, by hand if you want them. An agent
and a researcher's skill written before this release lack one line: add *Round files in
`Philosophy/Evolution/` are a record of how the owner's answers moved: read them for dates and
levels, and cite `HOW-I-INVEST.md`, never a round file, as the owner's view.* to the agent's *How
you answer* and to item 2 of your researcher's skill, by hand, then `apm install -g "<the home>"`
again.

### Added

* **`Philosophy/Evolution/`**, in `AGENTS.md`'s `Philosophy/` row: one round file per `philosophy`
  round — the round's number, date and level on its first line, then the question IDs with your
  typed answers word for word, or their status, and *kept*, *changed*, *new* or *still open* on a
  retake — never edited afterwards, and never cited as your view. The template ships none: your
  first round creates it.
* **`Briefs/` and `Portfolio/`**: a row each in `AGENTS.md`'s folder table and in `README.md`'s,
  and two lines in `.gitignore`. The template ships neither: the first brief creates `Briefs/`, and
  `brief setup` starts `Portfolio/holdings.csv` and `Portfolio/RULES.md` when you choose its
  portfolio part.
* **`## Why I invest`**, the first heading of `Philosophy/HOW-I-INVEST.md`.
* **`Here for:`** under *Who* in `RESEARCHER.md`, from the interview's new question.
* **_Save a copy off this computer_** in `README.md`: a commit saves on this computer only; how to
  keep a copy on a private GitHub repository as well.

### Changed

* **`AGENTS.md`**: the `Philosophy/` row and the first hard don't name its two writers —
  `philosophy` adds your typed answers to `HOW-I-INVEST.md`, word for word and add-only, after your
  go, and writes one round file in `Philosophy/Evolution/`, never edited afterwards; `refine` edits
  `HOW-I-INVEST.md` as an editor, diff first, and never touches `Evolution/`. A pick is never
  written in `Philosophy/`. The paragraph after the folder table lets `philosophy` append the works
  you pick at a round's close to the closing *Find first* line of `RESEARCHER.md`, unless you leave
  it alone in that round's preview, and says round files are a record, never cited as your view.
  *Plan first, then write* keeps the round file and the day's brief as records by design, and the
  go on `brief setup` covers every brief its schedule writes. The skills' row and the Codex line
  name `philosophy` and `brief`; two hard don'ts on briefs, round files and advice.
* **`RESEARCHER.md`**: *What you believe* is one line, pointing at `Philosophy/HOW-I-INVEST.md`,
  written by hand or with `philosophy`. *What you are reading for* ships with no slot — your first
  `read` asks which question a source serves and adds it as question 1 — and its closing *Find
  first* line reads *none*.
* **`Philosophy/HOW-I-INVEST.md`**: its note names its two writers, and says nothing else writes
  there.
* **`README.md`**: the folder table gains `Philosophy/Evolution/`, `Briefs/` and `Portfolio/`;
  *The path* takes the place of *First things to do* — set up, start learning, `philosophy`,
  `brief`, then the rest — and says how to stay current; the privacy note covers `Philosophy/`.

### Removed

* **`RESEARCHER.md`**: *Where it sits*, the *Add later* line under *What you believe*, and the
  slots under *What you are reading for*.

## 0.15.0 (2026-09-29)

**MINOR** — quick to start: the install asks your language first and, in one conversation, makes
your researcher's home under the name you give it and runs a four-step interview, about five
minutes. `README.md` opens with a table of your folders — what each holds and what you do with it
— and `RESEARCHER.md` and `Philosophy/HOW-I-INVEST.md` carry shorter prompts, with an *Add later*
line for what the interview no longer asks. `interview` and `next` are skills now, so Codex and
Gemini have them too.

**What to do differently:** run `update` in your home. It brings the new `README.md` and the
changed rows of `AGENTS.md` across, on your go. Your `RESEARCHER.md` and `Philosophy/` stay as they
are; add the *Add later* lines by hand if you want them.

### Changed

* **`README.md`**: *Your folders* and *First things to do* first; *In a strategy or another
  project*, *Growing your researcher* and *Installing and updating* after them, shorter.
* **`RESEARCHER.md`** and **`Philosophy/HOW-I-INVEST.md`**: shorter prompts; *Add later* lines
  under *What you believe* and *What you are reading for*.
* **`AGENTS.md`**: `interview` and `next` in the skills' row, nine commands in the commands' row,
  and how an assistant with no question tool asks.

## 0.14.1 (2026-09-29)

**PATCH** — the order of work chooses the benchmark in an entry of `JOURNAL_1.md`, and the
`brainstorm` command is gone from the package: part E names the journal, part F is the broad reading
alone, and the commands' row counts eleven. A strategy that keeps `BRAINSTORMING_1.md` still works.

**What to do differently:** run `update` in your home. It brings the changed rows of `AGENTS.md`
across, on your go.

### Changed

* **`AGENTS.md`**: *Where things are, in a strategy*, *The order of work* and the commands' row, as
  above.

## 0.14.0 (2026-09-26)

**MINOR** — your researcher is in every folder: `interview`, in the package, writes the researcher's
skill beside the agent and installs the home for your user, so every session, on every assistant
APM deploys to, knows who it is talking to and where the library lives. `AGENTS.md` says who is
speaking and where what the researcher learns goes, and the READMEs say that adding the home to a
session is for reading the library, not for bringing the researcher.

**What to do differently:** run `update` in your home. It brings the new sections of `AGENTS.md`,
`README.md` and `apm.yml` across, writes `.apm/skills/<slug>/SKILL.md` and installs the home with
`apm install -g "<the home>"`, on your go. Never `apm install` inside the home from now on.

### Added

* **`AGENTS.md`, *Who is speaking***: the researcher is the home, the engine is how it thinks, the
  agent is the researcher read-only; and what is learned anywhere goes home.

### Changed

* **`AGENTS.md`, *The researcher's home***: the install for the user makes the researcher present;
  `--add-dir` gives access to the library; the `CLAUDE.md` variable and `CLAUDE.local.md` load the
  whole file from the first line. *Joining other projects* and *Where the skills, the commands and
  the agent live* follow, with a row for the researcher's skill.
* **`README.md`** and **`apm.yml`**: `apm install -g "<this folder>"` in place of an install inside
  the home.

## 0.13.0 (2026-09-25)

**MINOR** — nothing to type but your answers: `interview`, in the package, now deploys the agent
for the assistant you are using and commits what it wrote, on the one go it asks for, and
`init-researcher` brings the package up to date before it makes a home. `README.md` says so under
*First, once*, and keeps the one command for a new machine or another assistant.

**What to do differently:** run `update` in your home, which brings the new paragraph of
`README.md` across. Nothing else: your interview has run, and your agent is deployed wherever you
ran `apm install --target <agent>`.

### Changed

* **`README.md`'s *First, once***: the interview deploys the agent and commits what it wrote; the
  command that deploys it by hand stays, for a new machine or another assistant.

## 0.12.0 (2026-09-25)

**MINOR** — the home has `Studies/`: your own work from the library — an idea that is not a
strategy yet, or a decision, a plan or a brief with no repository of its own — written by `study`,
a new command in the package, after its plan and your go. A synthesis page says what the library
holds; a study says what you will do about it. Every claim from the library links its note;
anything from outside it — a chat, a page, a figure — says where it came from and that it was not
checked; and a study that needs code or data, or an idea ready to be a strategy, moves out and
stays behind as the record. The directionality is `Sources/ → Extracts/ → Knowledge/ → Studies/,
Lessons/`: no note is ever written from a study. `README.md` opens with what you can use the
researcher for, with a strategy or without one.

**What to do differently:** run `update` in your home. It brings `AGENTS.md`, `README.md` and the
empty `Studies/` across and, on your go, moves what a `Projects/` still holds into `Studies/`, at
the same place below it, so its links into `Knowledge/` still resolve — a lesson under
`Projects/Teach/` into `Lessons/`, as before. Then by hand, if you like: in your agent in
`.apm/agents/`, `Studies/` among the places it never writes and `study` among what it names for a
write; and a state on the first line of each file that moved — *idea*, *active*, *parked*,
*closed* or *moved to `<path>`* — or run `study <its name>`, which proposes one.

### Added

* **`Studies/`**, empty, with its `.gitkeep`, and its row in `AGENTS.md`'s folder table: written
  through `study` only, after its plan and your go.
* **A section *Studies* in `AGENTS.md`**: what a study is and what it is not, its first line and
  its state, the library linked and the rest marked, one way from the notes, words only, and
  committed with the home.
* **`README.md` opens with what you can use it for** — a library you can ask, your studies,
  lessons, strategies, any other project and a researcher that fits you — each with the command
  that does it.

### Changed

* **`AGENTS.md`**: the paragraph under the folder table says anything else asked for at home is
  answered in chat unless you keep it as a study; the directionality, the paths the skills resolve
  and the in-strategy table name `Studies/`, and `study` works at home only, as `teach` does; the
  primitives table names twelve commands; a command's plan or report is never written as a file;
  a hard don't: no note is written from a study, and none cites one as a source.
* **`README.md`**: the opening names your studies; the file tree and the directionality name
  `Studies/`; *Growing your researcher* names `study` beside `teach`.

## 0.11.0 (2026-09-24)

**MINOR** — `RESEARCHER.md` offers a second rule beside the fourth, to add or leave: *every design
is challenged before it runs, and every idea tried is counted.* The three you start with are
unchanged, and neither offered rule is a default. The interview that fills the file — `interview`,
in the package — offers it in its rules question, where *Add one of mine* and *Change or drop one*
are now one option, and in question 5 offers two more hints, each yours to take, edit or leave: a
clause naming who keeps taking the other side of your trade, and four ways your edge's shelf life
might run, the one that follows from where you said the edge comes from listed first. The interview
is still seven questions.

**What to do differently:** run `update` in your home, which brings the new `interview` with the
package; none of the home's own files changed, so nothing else comes across. Then by hand, in
`RESEARCHER.md`, which is yours: the rule, if you want it, as a line under *Non-negotiables* —
*Every design is challenged before it runs, and every idea tried is counted.* To be offered the new
hints, run `interview force`: every answer you keep is written back verbatim.

### Added

* **A second rule is offered** in the guidance under *Non-negotiables* in `RESEARCHER.md`, after
  the fourth, to add or leave: every design is challenged before it runs, and every idea tried is
  counted. `interview` writes it only when you pick *Challenge my design before it runs, and count
  every idea I try* in its rules question.

## 0.10.0 (2026-09-24)

**MINOR** — the home has no `Projects/`. The researcher is invited into the projects it works on,
outside its home, so a new home is made without the folder: `teach` keeps each topic's lessons in
`Lessons/<topic>/`, created the first time it teaches that topic; anything else you ask for at home
is answered in chat, or as a page you can share, never written as a file; strategy work stays in
the strategy. The directionality is `Sources/ → Extracts/ → Knowledge/ → Lessons/`, with
`Philosophy/` cited, never compiled.

**What to do differently:** run `update` in your home. It brings `AGENTS.md` and `README.md`
across and, on your go, moves each `Projects/Teach/<topic>/` to `Lessons/<topic>/`, removes a
`Projects/` left holding only its `.gitkeep`, and lists anything else there for you to keep, move
or delete by hand. If your agent in `.apm/agents/` names `Projects/` among the places it never
writes, change it to `Lessons/` by hand, or leave it: the folder is gone.

### Changed

* **`AGENTS.md`'s folder table** has a `Lessons/` row, written through `teach` only, after its plan
  and your go, where the `Projects/` row allowed any write you asked for. A paragraph under the
  table says anything else asked for at home is answered in chat, never written as a file, and that
  work on a strategy or another project lives there. The paths the skills resolve, the
  directionality and the in-strategy table say `Lessons/`.
* **`README.md`'s file tree and directionality** say the same.
* **`teach` keeps its lessons in `Lessons/<topic>/`**, in the package, where it kept them in
  `Projects/Teach/<topic>/`, and writes nowhere else; a topic still in `Projects/Teach/` points at
  `update` rather than starting again. **`update`** offers to move it whenever a home still has a
  `Projects/`, at any template version, so a move declined once is offered again.

### Removed

* **`Projects/`**, and its `.gitkeep`: `init-researcher` no longer creates it.

## 0.9.0 (2026-09-23)

**MINOR** — the researcher is yours, and grows with what you believe. `RESEARCHER.md` offers its
three starting non-negotiables as rules many researchers start with, to keep, change or add to, and
offers a fourth; `README.md` says in one line what the researcher is. The interview that fills them
— `interview`, in the package — now also asks what pulls you to markets, how you like to invest,
your view as one testable sentence and how long you would give its edge, and the smallest test that
could kill it.

**What to do differently:** run `update` in your home, which brings the new line of `README.md`
across. Then by hand, in `RESEARCHER.md`, which is yours: the fourth non-negotiable, if you want it,
as a line under *Non-negotiables* — *A strategy graduates only against criteria written down
beforehand, never on a good month.* To be asked the new questions, run `interview force`: every
answer you keep is written back verbatim.

### Added

* **`README.md` says what the researcher is**, at the top of *Working with it*: yours, growing with
  what you believe, the package bringing only hints, offered as options, that make a complex idea
  simple — never a position to adopt.
* **A fourth non-negotiable is offered** in the guidance under *Non-negotiables* in `RESEARCHER.md`,
  to keep or leave: a strategy graduates only against criteria written down beforehand, never on a
  good month. `interview` writes it when you pick it.

### Changed

* **The guidance under *Non-negotiables*** calls the three the rules many researchers start with,
  to keep, change or add to, where it called them KaxaNuk's defaults. The three are unchanged: the
  first still says that in a KaxaNuk strategy the numbers come from the Lab's libraries.

## 0.8.2 (2026-09-23)

**PATCH** — a new home's rules agree with each other and with the skills: `AGENTS.md` names the one
write `interview` makes to `Philosophy/`, says nothing is read into a strategy before its objective
has claims, and names every primitive the package carries; `RESEARCHER.md` states the citation rule
as `AGENTS.md` does; the `.gitignore` keeps every PDF and every `.env` file out of git.

**What to do differently:** run `update` in your home, which brings `AGENTS.md` and `.gitignore`
across. Then by hand, in `RESEARCHER.md`, which is yours: the second non-negotiable in the new
wording, if you kept KaxaNuk's. A PDF you had committed outside `Sources/` stays tracked until you
`git rm --cached` it.

### Added

* **`.gitignore` ignores `.env` and `*.env`**, under a comment saying why: a key kept in a `.env`
  file never reaches a push. `AGENTS.md` already said a value from one is never printed.
* **`AGENTS.md`'s primitives table names everything the package carries**: every skill — the
  researcher's, the process's and each Lab library's, the house rules' — every command by name, the
  package's one agent, `blueprint-critic`, a read-only reviewer `blueprint` calls on its draft
  before the go, and an *Instruction* row for the four house instructions, which the home adds
  none of. An owner naming a skill, a command or an agent of the home's own can now see every name
  the package uses.
* **`AGENTS.md` says a command's required input comes first**, the optional ones after it, because
  an assistant binds the arguments by position.

### Changed

* **`.gitignore` ignores `*.pdf` anywhere in the home**, not only under `Sources/`, as the
  strategy template already does, so a PDF filed in `Knowledge/` or `Projects/` by mistake is never
  pushed. Its comment says so.

### Fixed

* **`interview`'s write to `Philosophy/HOW-I-INVEST.md`** — the owner's typed answers, verbatim,
  on their go — is named in `AGENTS.md`'s folder table and its hard don'ts, which allowed writes to
  `Philosophy/` only through `refine`.
* **The in-strategy row for *What you are reading for*** said the researcher reads for whatever
  the owner says while `OBJECTIVE.md` has no claims; it now says nothing may be read into the
  strategy and `objective` comes first, as the out-of-order rule and the `read` skill say.
* **`RESEARCHER.md`'s second non-negotiable** said a prediction cites a source; it now cites a note
  or an analyzer measurement, one with neither is a lead, and a source without a note cannot be
  cited, as `AGENTS.md` says.
* **The *What you are reading for* prompt** said `read` asks for the questions when the section is
  empty; it proposes candidate questions from what is already in `Sources/` and asks you to pick,
  as the skill does.
* **`AGENTS.md`'s *Plan first, then write*** said every write waits for a go, while `audit` appends
  its line to `LOG.md` without one; it now names that line as the one write made without a go.

## 0.8.1 (2026-09-23)

**PATCH** — a new home's own files agree with its rules: the blockquotes of `Knowledge/INDEX.md`
and `Knowledge/LOG.md` name the synthesis page `query` keeps, as `AGENTS.md` has since 0.8.0.
`LICENSE` is the MIT licence alone.

**What to do differently:** run `update` in your home, which brings `README.md` and `AGENTS.md`
across and lists the two blockquotes as *by hand* lines; carry the `INDEX.md` and `LOG.md`
blockquotes across by hand, since those files are yours. `LICENSE` names KaxaNuk as the holder, as
the template ships it: put yourself there, as `interview` says.

### Changed

* **`Knowledge/INDEX.md`** is rebuilt by `read` and `refresh-index` and given one line by `query`
  when you keep a synthesis page; **`Knowledge/LOG.md`** records every synthesis page `query`
  keeps, beside every `read`, `audit` and `refresh-index`.

### Removed

* **The obsidian-vault-kit notice**, from the end of `LICENSE` and from the *Licence* section of
  `README.md`: `LICENSE` is the MIT licence alone.
* **`AGENTS.md`'s version history of a strategy's `Bibliotheca/`**: the *Where things are, in a
  strategy* table says the template ships `BIBLIOGRAPHY.md` and `LOG.md`, and no longer what a
  strategy older than 0.7.15 has; the `read` skill still says it.

### Fixed

* **The 0.8.0 entry** called `fcf-yield-quality` the example strategy and the worked example's
  name; it is the placeholder name `init-strategy` uses, and the worked example is
  `liquid-golden-cross`. Corrected in place.

## 0.8.0 (2026-09-23)

**MINOR** — the home's rules change: the numbers rule names the engines the project names, not only
the Lab's, `query` may write a kept page's index line and log entry, *Joining other projects* says
who copies and how a project's files are named and cited, and the README says how a researcher
grows. The example path in `AGENTS.md` is `fcf-yield-quality`.

**What to do differently:** run `apm update -g`, open a new session, and run `update` in your home,
which brings `README.md`, `AGENTS.md`, `apm.yml` and `.gitignore` across. Then by hand: the first
non-negotiable in `RESEARCHER.md` in the new wording, its table heading to *The strategies and
projects it works on*, and the version field in `apm.yml`, which is yours and which `update` never
touches.

### Added

* **`README.md` has *Growing your researcher***: the four moves — a tool's or a project's
  documentation into `Sources/Clippings/` then `read`; a skill or command of the home's own in
  `.apm/skills/` or `.apm/prompts/`, then `apm install --target <agent>`; a line under *What you
  are reading for*; a line by hand under *How it speaks* or *Non-negotiables* — each with the
  `AGENTS.md` section that governs it, and one line on who teaches whom: `teach` tutors you from
  the library, you teach the researcher by these four moves.
* **`AGENTS.md` says who copies a project's files**: the researcher names them and gives the copy
  command, the owner runs it, then `read`; `Sources/` stays the owner's. A paragraph under *Joining
  other projects* names the clipping `Org_Year_Project_File.md`, cites a private repository as
  "private repository; link not checked", ties the read to a numbered question, says a project's
  own skills are installed or read there, never imitated, and that a home holding a private
  project's material stays a private repository. `README.md` says the last of these too.
* **`AGENTS.md` and `README.md` say the home's version is the owner's**: `interview` sets it to
  0.1.0, the owner bumps it with each changelog entry, and `update` reads the *Brought to template*
  line, never the field.
* **`README.md` lists `.apm/skills/` and `.apm/prompts/`** in its file map, for a home's own skills
  and commands, and says `git diff` prints a CRLF warning on Windows for files the researcher
  wrote, which `.gitattributes` settles on commit.
* **`.gitignore` ignores `.ruff_cache/` and `.pytest_cache/`.**

### Changed

* **The numbers rule names the engines the project names.** `RESEARCHER.md`'s first non-negotiable
  and the hard don't in `AGENTS.md` say every number about a book comes from the engines the
  project names — in a KaxaNuk strategy the Lab's libraries — never from the researcher.
* **`RESEARCHER.md` is a researcher's, not only an investor's**: the table is *The strategies and
  projects it works on* with a *Strategy or project* column, the *What you believe* prompt asks
  how you work and what you think is true in your field, and *How it cites* says that in any other
  project the note is named in prose. `Philosophy/HOW-I-INVEST.md` tells an owner whose research is
  not investing to edit the headings and keep the file name, which `interview` and the skills find
  it by.
* **`query` reaches the index and the log** in `AGENTS.md`: `INDEX.md` takes one line from it when
  the owner keeps a synthesis page, and `LOG.md` an entry.
* **`AGENTS.md` names every file the commands write in a strategy**: a line in `Bibliotheca/LOG.md`
  from `read` and `audit`, and one dated entry appended to `JOURNAL_N.md` by `challenge`, which the
  mapping table lists. The template ships `BIBLIOGRAPHY.md` with no notes, only the seeded leads,
  and `LOG.md` empty. The commands assume the KaxaNuk Strategy Template's paths; a strategy made
  from another template keeps or maps them in its own `AGENTS.md`.
* **The order of work's row E** names `brainstorm 1` for the benchmark entry, then `blueprint`, as
  `next` does, and row G says every number comes from the engines the project names.
* **A blueprint is committed in a commit of its own, before the rule**, in *Working in a
  strategy*, where it was "the branch's first commit": a strategy's work lands on `main`, and a
  branch is for a change the owner wants reviewed.
* **`AGENTS.md` reaches a strategy from home as `blueprint 1 D:\Research\fcf-yield-quality`**, the
  placeholder name `init-strategy` uses, not a folder of the maintainer's.
* **A note's *What it changes* is measured against the owner's question**, not their investing;
  the `RESEARCHER.md` paragraph says a line by hand under *How it speaks* or *Non-negotiables* is
  how the owner teaches the researcher to behave; and a skill of the home's own is written as the
  package's are — a body that says when it applies, then numbered steps, as `read` does.
* **`apm.yml` lists the four targets that take an agent** — `claude`, `copilot`, `cursor`,
  `codex` — and its comment says `apm install --target <agent>` here deploys the agent and any
  skill or command of this home's own.
* **`.gitignore` ignores only what APM writes under `.github/`**, the five lines the strategy
  template uses, so a home backed up on GitHub can carry a workflow.
* **`README.md`'s *In a strategy* is *In a strategy or another project***, and says that what comes
  back comes as a source in `Sources/` that `read` files; its first paragraph says `interview`
  proposes its replacement.

### Fixed

* **`CHANGELOG.md` lists its five headings**, says it is the home template's changelog, which
  `init-researcher` copies and `update` extends, and the 0.7.3 entry promises only `README.md` and
  `AGENTS.md` through `update`, the rest by hand. Two lines named a real home; they say "a home"
  and "Ada".

## 0.7.3 (2026-09-23)

**PATCH** — the interview is the `interview` command. `init-researcher <name>` makes the home,
`interview` makes the researcher yours; the two are no longer the same two words in either order.
The example home in `AGENTS.md` is `D:\Research\Ada`.

**What to do differently:** run `interview` where you ran `researcher-init`, and `interview force`
to start over. `apm update -g` brings it; `update` brings the wording in `README.md` and
`AGENTS.md` across; `RESEARCHER.md`'s blockquote and `Philosophy/HOW-I-INVEST.md` are by hand.

## 0.7.2 (2026-09-23)

**PATCH** — `blueprint`, `brainstorm` and `challenge` take the experiment number first.

**What to do differently:** run `blueprint 1`, and `blueprint 1 D:\Research\Golden-Flow` from
home; `brainstorm 2 "an idea"` quotes an idea of more than one word. `apm update -g` brings it.

### Changed

* **`AGENTS.md`** reaches a strategy from home as `blueprint 1 D:\Research\Golden-Flow`: the
  strategy's path is optional, so it comes last.

## 0.7.1 (2026-09-22)

**PATCH** — *The order of work* in `AGENTS.md` letters its eight parts A to H, as the template's
README now does, so a part is never mistaken for one of the eight steps; the commands cite the
parts by letter. The primitives table counts eleven commands, `next` among them, and `README.md`
says to run `next` when lost.

**What to do differently:** run `update` in your home to bring the lettered table across; nothing
you wrote changes.

## 0.7.0 (2026-09-22)

**MINOR** — `RESEARCHER.md` says where your view sits in the evolution of investment research and
which works to find first, from the reading map in the `read` skill.

**What to do differently:** run `apm update -g`, open a new session, and run `update` in your home;
re-run `researcher-init force` to fill the new lines, which keeps what you wrote. Deploy the agent
with `apm install --target <your agent>` (for example `--target claude`), never a bare
`apm install`, which deploys to all seven targets in `apm.yml`.

### Added

* **`RESEARCHER.md` has a *Where it sits* line** under *What you believe*: the act, the work that
  holds your view, who tested it and its other side, from the reading map — a lead, never a
  citation.
* **`RESEARCHER.md` has *Find first***: a line under each reading question with the works to find
  for it, and a closing line for a work that serves no question. A question may say its
  mind-changer is *not yet known*.
* **`AGENTS.md`**: a work to read may be proposed from the reading map, and the primitives table
  lists `reading-map.md`.

### Changed

* **`AGENTS.md` names one package throughout**, says `read` gives the `scaffold.py` command that
  copies `BIBLIOGRAPHY.md` and `LOG.md` from the template inside the package, gives
  `apm install --target <agent>` for the agent, notes that OpenCode rejects the agent's tool list,
  and says a command carries no `metadata`.
* **`RESEARCHER.md`'s strategies table ships a *none listed* row** and the note that the researcher
  joins a strategy when invited, as the interview leaves it, not a slot row it no longer fills.
* **`apm.yml`'s comment** says the package carries every Investment Lab skill itself.

### Fixed

* **`README.md` deploys the agent with `apm install --target claude`**, your assistant in place of
  `claude`, not a bare `apm install`.
* **`LICENSE` names the `read` and `query` skills and the `audit`, `refine`, `refresh-index` and
  `teach` commands**, not a `compile` command that does not exist.
* **`README.md` says `update` adds a *Brought to template* entry to `CHANGELOG.md`**, so the file
  names the template version the home is at, not only the one it was made from.
* **`AGENTS.md` names the worked example's `BRAINSTORMING_1.md`** where it said the template's;
  the strategy template ships none.

## 0.6.1 (2026-09-21)

**PATCH** — the researcher's package carries every Investment Lab skill itself.

**What to do differently:** nothing; `apm update -g` brings it.

### Changed

* **`AGENTS.md` names one package**, `KaxaNuk/KaxaNuk-Researcher`, for the skills and the commands.

## 0.6.0 (2026-09-21)

**MINOR** — the researcher is a package, `KaxaNuk/KaxaNuk-Researcher`, installed once for the user;
this template is its home, which `init-researcher` makes.

**What to do differently:** install once, `apm install -g KaxaNuk/KaxaNuk-Researcher`, which brings
every Investment Lab package from KaxaNuk-Agent-Skills with it; update with `apm update -g`. A home
from 0.5.6 or before runs `update` once.

### Changed

* **The skills and commands are a package.** `read`, `query` and the ten commands were copied into
  every home, so each carried code it could not safely edit and every version arrived by a merge.
  They now live in `KaxaNuk/KaxaNuk-Researcher`, with `extract.py` and `note.md` in the `read`
  skill's folder, and every folder the owner opens has them — the home and every strategy, which
  installs nothing.
* **`apm.yml` names no dependency.** `apm install` here deploys only the home's own agent.
* **`AGENTS.md`**: *Where the skills, the commands and the agent live* says the package is at user
  scope, lists `init-researcher`, `init-strategy` and `init-example`, and names the package's path
  under `~/.apm/` for Codex. A strategy's empty `BIBLIOGRAPHY.md` and `LOG.md` come with the
  template now, and an invited researcher brings the library, not the skills.
* **`README.md`** is a home's README: first run, working at home and in a strategy, what is in
  here. What the researcher is, and how to install it, is the package's README.

### Removed

* **`.apm/skills/`, `.apm/prompts/`, `scripts/`, `references/` and `SETUP.md`.** The package carries
  the first four, and `init-researcher` replaces `SETUP.md`.
* **The repository `KaxaNuk/KaxaNuk-Researcher-Template`** is no longer where the home comes from;
  it is `templates/researcher/` in KaxaNuk-Researcher.

## 0.5.6 (2026-09-21)

**PATCH** — the template every strategy is copied from is called the KaxaNuk Strategy Template
everywhere, and a few leftovers are gone. Nothing to do differently.

### Changed

* **One name for the strategy template.** `AGENTS.md`, `README.md`, `apm.yml`,
  `references/note.md`, `read`, `researcher-init` and `update` said *KN Research Process* where
  they meant the template at `KaxaNuk/KaxaNuk-Strategy-Template`, so there were two names for one
  repository. They now say *KaxaNuk Strategy Template*. Older entries below keep the name they
  were written with.

### Removed

* **A leftover line in `researcher-init`** about a dependency that `apm.yml` no longer declares.
* **`.gitignore` entries for things this repository never produces**: `requirements-dev.txt`,
  which was removed long ago, plus `.grok/`, `.kiro/`, `build/` and `.claude-plugin/`.

## 0.5.5 (2026-09-21)

**PATCH** — the repository is `KaxaNuk/KaxaNuk-Researcher-Template`. GitHub redirects the old
name, so every clone keeps fetching, and the package keeps its name.

**What to do differently:** in a clone whose template remote still names `KaxaNuk-Researcher`,
run the `git remote set-url` line that `update` now gives. Nothing else.

### Changed

* **The repository is KaxaNuk-Researcher-Template**, and `README.md`, `SETUP.md` and the commands
  that name it say so. Both repositories a person starts from are templates, and now both names
  say it: `KaxaNuk-Researcher` read as the researcher itself, when what it holds is the skeleton
  every researcher is cloned from. The package stays `kaxanuk-researcher`, because what
  `apm install` puts in a project is a researcher, not a template.

### Fixed

* **`update` recognises a remote at the old name.** It had one rule — no remote at the template,
  so add `upstream` and stop — and a clone whose `upstream` still named `KaxaNuk-Researcher` would
  have been told to add a remote it already has, which `git remote add` refuses. It now uses that
  remote, which still works, and gives the `git remote set-url` line that renames it.

## 0.5.4 (2026-09-21)

**PATCH** — three template lines fit the 100-column width again. Nothing to do differently.

### Fixed

* **The template's own prose keeps the width every other line here keeps.** The renames of 0.5.2
  and the index of 0.5.3 pushed three lines past 100 columns — one in `researcher-init` reached
  106 — so every home taking the update inherited them, and a home had once committed a rewrap for
  exactly this. The same words, rewrapped; no command reads differently.

## 0.5.3 (2026-09-21)

**PATCH** — *The order of work* says what it is: an index of the template's list, not a second
copy of it. Nothing to do differently; every command behaves as before.

### Changed

* **The tie-breaker is gone.** *Working in a strategy* said "where the skill and the template's
  README disagree, the README holds" — a clause that only exists because two documents both claimed
  the order. It now says there is one source, *Starting your own strategy* in the template's README,
  and that this repository's table and the `experiment-lifecycle` skill both index it.
* **The table's *Item* column is names, not restatements.** The reasons behind the order — why the
  objective comes before any paper, why the universe comes after the claims — stay in the template's
  README. *Where it lands*, *the researcher's part* and the rule for a command asked for out of
  order are unchanged word for word, and so are the item numbers `blueprint` and `challenge` cite.
* The paragraph on items and steps is three lines instead of six; its examples named lines in a
  strategy's files that change as the strategy does.

## 0.5.2 (2026-09-20)

**PATCH** — the two repositories the researcher points at were renamed. Nothing to do differently.

### Changed

* **`blueprint`, `brainstorm` and `read` fetch from `KaxaNuk/KaxaNuk-Strategy-Template`**, and
  `researcher-init` names `KaxaNuk/KaxaNuk-Agent-Skills` as where the process knowledge lives. The
  template was `KaxaNuk-Research-Process`, which named an abstraction where the artifact is a
  repository you copy — and collided with this repository's own name, the confusion a new reader
  arrives with. The skills package was `KaxaNuk-APM`, which reads as Application Performance
  Monitoring and named the delivery mechanism rather than what the packages hold. GitHub redirects
  both old paths, so a `git fetch` written from an older copy still reaches the right place.
* **The *How it fits with the rest of KaxaNuk* table** uses both new names. The **KN Research
  Process** keeps its name throughout: the process is not the repository.

## 0.5.1 (2026-09-20)

**PATCH** — `update` knows the case it will meet most often. Nothing to do differently.

### Changed

* **`update` handles a clone that renamed the template's prose** (0.2). A home that rewrote the
  text it was given — its researcher's name and its owner's, a narrower target list, its own
  README — conflicts on nearly every template file, and nearly every conflict resolves the same
  way. The command now says so before the merge, resolves by side rather than hunk by hunk, renames
  the taken files in one pass and then reads the result for the pronouns a rename leaves behind,
  sets `apm.yml`'s version by hand because that line was kept, and names the prose the owner had
  deleted that comes back with the template's text.

## 0.5.0 (2026-09-20)

**MINOR** — two commands at the ends of the work that had none: `update`, which takes a new version
of the template into a clone without losing what makes it its owner's, and `challenge`, which
checks a finished experiment against its own blueprint. With them, everything the researcher says
about a strategy checked against a real one, and the rules it breaks in its own files fixed.

**What to do differently:** pull, run `apm install --target <your agent>`, open a new session, and
from then on run `update` instead of merging by hand. A clone whose remote is not named `upstream`
is fine: `update` finds the remote that points at the template. In a strategy, read *The order of
work* again: its rows are the template README's **items**, not the process's eight **steps**, and a
strategy's own files mean the second thing when they say *step 7*.

### Added

* **`update`** (0.1), home only. It checks the working tree is clean and that nothing is hidden by
  `skip-worktree`, finds the template's remote and fetches it, reads the `CHANGELOG` from this
  clone's version to the newest and reports every *What to do differently* in full, names the files
  that are the owner's — `RESEARCHER.md`, `Philosophy/HOW-I-INVEST.md`, `Knowledge/INDEX.md`,
  `LOG.md`, the agent, and the library itself — and what the template wanted to change in them,
  then merges after a plan and a go: template conflicts resolved, the owner's conflicts kept as
  theirs, never `researcher-init force` to pick up a new section. It reinstalls, reports, and
  appends nothing to `Knowledge/LOG.md`, which records reads, audits and refreshes. `update check`
  reports what is new and stops.
* **`challenge`** (0.1), items 7 and 8 of the order of work — the first command that runs *after*
  the work, and the only one whose default output is no file. It checks each verdict against its
  own falsifier, the tally against the rows, a verdict that answers a question the prediction did
  not ask, the run against the frozen window and costs, each success criterion before any claim of
  adoption, the notes behind the predictions, whether every falsification reached *What is closed*,
  and whether a published difference reconciles with the numbers beside it. It reads the engines'
  outputs never, quotes numbers only from `FINDINGS_N.md` and `RESULTS.md`, refuses to touch
  `BLUEPRINT_N.md`, `FINDINGS_N.md`, `RESULTS.md` or `OBJECTIVE.md`, and writes at most one
  appended `JOURNAL_N.md` entry, on the owner's go.
* **`blueprint` and `brainstorm` bootstrap from the `example` branch** (0.3 and 0.2), the way `read`
  already does: a strategy created from the template's `main` has `Experiments/.gitkeep` and no
  `BLUEPRINT_N.md` or `BRAINSTORMING_N.md`, so they give the fetch command, say what between the
  example markers is the worked strategy's, and stop rather than writing the template's headings
  from memory.

### Changed

* **The order of work counts *items*, not steps** (`AGENTS.md`, and the wording in `blueprint`,
  `objective` and `read`). The template's README says its eight are "the order of work, not the
  eight steps above: item 3, the universe, is step 2", and a strategy's own files use *step* in
  that second sense — *step 7* is the paper-trading gate, *step 8* is Production and is not in the
  repository. The table now says so instead of claiming one shared numbering.
* **A prediction may cite an analyzer measurement** (`AGENTS.md`), as `blueprint` has always said
  and the real blueprints do; only a prediction citing neither a note nor a section number is a
  lead. `audit` stops reporting those predictions as defects, and stops asking `BIBLIOGRAPHY.md`
  for a row per book chapter when the convention gives a book one row linking its `INDEX.md`.
* **`objective` takes a claim's status from the template's vocabulary** (0.3) instead of writing
  **untested** over every row — the shipped `OBJECTIVE.md` ships a claim that is *true by
  construction*, and the real first pass kept it.
* **`teach` plans before it writes** (0.2). Running it names `Projects/Teach/<topic-slug>/` as the
  only place it may write — the place, not the go: the new topic's files and each lesson wait for
  a plan and an explicit go, as `AGENTS.md` requires of every command that writes.
* **`query` stays out of the index and the log** (0.3). A kept synthesis page is written under its
  domain and nothing else; `refresh-index` is what puts it under *Concepts* and records the run.
  Its own refusal list no longer forbids the one write it makes.
* **`audit` and `refresh-index` say "only when the owner runs it by name"** in their descriptions,
  as the other eight do and `AGENTS.md` requires (0.2.2 and 0.2.1).
* **Ten commands**, in `README.md`, `AGENTS.md`, `SETUP.md` and the README's file tree.

### Fixed

* **The `example`-branch strip instruction left a dangling link.** The markers bound only Part 1 of
  `BIBLIOGRAPHY.md`; a Part 5 row links a note that does not come across, so a bootstrapped
  strategy shipped a broken relative path and a lead that read as a source already read. `read` and
  `AGENTS.md` now say to put a `[note](...)` link outside the markers back to *No note yet.* rather
  than delete the row, which is the template's.
* **`read`'s extract command wrote to the wrong folder in a strategy.** The script's `--out`
  defaults to `Extracts/` under the folder it runs in, so every run in a strategy now carries
  `--out Bibliotheca/Extracts` (0.4.1).
* **`brainstorm`'s closing reminder contradicted the file it appends to.** An idea leaves the file
  for a new experiment once the blueprint is written; before that — the benchmark choice in
  `BRAINSTORMING_1.md` — an entry feeds the blueprint that does not exist yet.
* **`researcher-init` checks for `scripts/extract.py` and `references/note.md`** (0.3). Installing
  the package into an existing project carries `.apm/` only, so `read` had no extractor and no note
  shape and nothing said so. The README says it too, for that route and for `apm pack`.
* **`SETUP.md` pointed at `git pull upstream main`** as how updates arrive; it names `update`.
* **The README** said "Eight are commands" in the one section that explains them, hard-coded
  `--target claude` in the step that had just told Codex readers what to do, and carried a
  102-character line.
* **`CHANGELOG.md`** stated its own format as *Added / Changed / Removed* while five entries use
  *Fixed*, and 0.2.0's instruction read "The run `apm install`" for "Then run".

## 0.4.2 (2026-09-19)

**PATCH** — the researcher installs the way the KN Research Process template does: paste one line
into Claude or Codex. Nothing to do differently in a researcher that is already installed.

### Added

* **`SETUP.md`**, written for an agent that was given only the URL and readable by a person in two
  minutes: the two tools, git and `uv`; the researcher's name, which is the folder's; one folder as
  the whole researcher, and the wrapper folder to avoid; a short path on Windows; the template kept
  as `upstream` so its updates can still be pulled; APM through `uv tool install apm-cli`, and the
  skills installed without asking, for the assistant doing the install; a check that a PDF can be
  read; the invitation variable, asked for rather than set; and the hand-over to
  `researcher-init` in a new session.
* **`Philosophy/HOW-I-INVEST.md`**, the page where the owner writes how they invest: four headings
  — what I believe about markets, what I have learned, how I decide, what would change my mind —
  each with a one-line prompt, and a blockquote saying the file is theirs and in their own words.
  It replaces `Philosophy/.gitkeep`. `researcher-init` fills it verbatim, heading by heading, where
  it used to create `how-i-invest.md`; `RESEARCHER.md` links it by name; and `AGENTS.md` says a
  prompt still in place is never cited as the owner's view.

### Changed

* **The README opens with the prompt to paste**, and its *Start* no longer carries the clone and
  install commands — `SETUP.md` does, and the README does not repeat it. `researcher-init` can be
  typed or asked for, and on Codex is run by naming its file.

## 0.4.1 (2026-09-17)

**PATCH** — three sentences that were true when written stop contradicting the KN Research Process
template and KaxaNuk-APM. Nothing to do differently.

### Fixed

* **The README's KaxaNuk-APM row** said no KaxaNuk package was installed and that the packages would
  come once they taught research. `investment-lab` carries the process, the Lab libraries each have
  their own package, and a strategy installs them through its own `apm.yml` — as 0.4.0's Fixed entry
  already said.
* **`Bibliotheca/Extracts/` is ignored by the template's `.gitignore`**, and has been since the
  template's 0.7.1; `AGENTS.md` still said it would be once the template carried the line. `read`
  keeps saying so in its plan for a strategy whose `.gitignore` lacks it.
* **`AGENTS.md` no longer names a version of `experiment-lifecycle`** that lists the universe before
  the objective. KaxaNuk-APM's `investment-lab` 0.7.0 follows the template's order of work; the rule
  that stays is general: where the skill and the template's README disagree, the README holds.

## 0.4.0 (2026-09-17)

**MINOR** — the researcher knows the order a strategy is built in, and arrives in a strategy whole:
the objective before any paper, and its own `CLAUDE.md`, `AGENTS.md` and `RESEARCHER.md` loaded
beside its skills when it is invited. Carried back from a researcher in use.

**What to do differently:** set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` once on each
machine — `setx CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD 1` on Windows — quit and reopen your
assistant, run `apm install --target <your agent>`, and open a new session. In a strategy, run
`objective` before the first `read`: a strategy whose `OBJECTIVE.md` has no claims no longer takes a
note.

### Added

* **The order of work, in `AGENTS.md`.** Eight steps, the template's numbering, each with where it
  lands and the researcher's part: the objective, before any paper; the objective fine-tuned by
  reading for each claim; the investable universe, delisted names included; the data; the
  benchmark, then the blueprint, before the rule; the broad reading and the brainstorming; the
  cycle — portfolio construction, backtest, attribution — until it is finished; and every finished
  cycle into `RESULTS.md`, kept or rejected. Reading comes in two waves: narrow and per claim before
  the blueprint, so its predictions have notes to cite, and broad after it. A command asked for out
  of order names the step that comes first, and stops.
* **Checking an invitation.** `AGENTS.md` and step 5 of the README say what loads from an added
  folder: the skills, the commands and the agent on their own, and `CLAUDE.md` — with its imports,
  `AGENTS.md` and `RESEARCHER.md` — only when the variable is in the environment before launch,
  because an `env` entry in `settings.json` is applied too late for it. They say how to check it
  with `/context`, and give the fallback when the assistant does not honour the variable: a
  gitignored `CLAUDE.local.md` at the strategy's root that imports the researcher's `CLAUDE.md` by
  absolute path.
* **Joining other projects, in `AGENTS.md`.** Outside a strategy the researcher challenges on
  evidence, follows the project's own rules, writes there only after a plan and the go, and brings
  nothing home unless the owner asks — and then as a source in `Sources/` that `read` files.
* **Working lean, in `AGENTS.md`**, a default the owner may change. One short planning round,
  small changes batched into one install, one task per session, search before reading, short
  replies.
* **`.obsidian/` is gitignored**, for owners who open their library as a vault.

### Changed

* **`objective` works before the reading** (0.2). The first pass drafts the claims from the owner's
  words, each claim's evidence the question that would settle it, marked as a lead; fine-tuning
  passes rewrite the evidence from the notes, and a claim the reading sharpened is proposed, never
  changed silently.
* **`read` refuses a strategy with no claims** (0.4.0). The objective comes first; in a strategy a
  question the claims do not cover is a claim to add with `objective`, and every note serves a
  claim.
* **`blueprint` refuses without claims or without an investable universe** (0.2), naming the step
  that comes first, and closes by pointing at the broad reading, `brainstorm` and the cycle. When
  `RESULTS.md` has no analyzer measurement yet, it says so in the plan and writes the predictions
  that needed one as leads, rather than treating the empty section as normal for Experiment 1.
* **Where the `experiment-lifecycle` skill and the template's README disagree on the order, the
  README holds.** Since the KN Research Process 0.7.4 a strategy's own `README.md` links to
  *Starting your own strategy* rather than carrying it; the published skill still lists the
  universe before the objective, and `AGENTS.md` says so.

### Fixed

* **`read` no longer fetches a whole `Bibliotheca/` from the template's `example` branch.** That
  branch is a worked strategy, so the command brought another strategy's notes into a new one. It
  fetches `BIBLIOGRAPHY.md` and `LOG.md` only, says what in them is the example's to delete, and
  checks for the claims before it checks for the folder. The *Working in a strategy* table says the
  same. The fetch is two commands, because `&&` does not parse in Windows PowerShell 5.1.
* **KaxaNuk's `investment-lab` and `data-curator` packages exist**, and `investment-lab` carries
  `experiment-lifecycle`, the process as a skill. `apm.yml` and `researcher-init` said they did not
  exist or were not packaged — 0.2.0's Fixed entry recorded that; it was true when written and is
  not now. A strategy installs them through its own `apm.yml`; a home starts with none, and
  its owner adds whatever stack their own work needs.

## 0.3.0 (2026-09-11)

**MINOR** — the researcher reads a book a chapter at a time, in one note convention shared with the
KN Research Process template, keeps a wiki of concept pages, and lives in `.apm/` as two skills,
eight commands and an agent, in KaxaNuk's own format.

**What to do differently:** pull, run `apm install --target <your agent>` and open a new session,
as 0.2.0 already asks; then run `read` where you ran `compile` or `note`. Reading a PDF needs
[`uv`](https://docs.astral.sh/uv/) on the machine, or `pip install pypdf`. If your `RESEARCHER.md`
is already filled, add the section *What you are reading for* by hand — the shape is in the
template — or leave it out and `read` asks for it the next time a source arrives. A strategy needs
the matching KN Research Process template — the branch `researcher-unified-note` until it is
released — which drops `Bibliotheca/Knowledge/`, adds `Bibliotheca/LOG.md` and ignores
`Bibliotheca/Extracts/`. In an existing clone, rename `Sources/Notes/` to `Sources/Clippings/`.

### Changed

* **Every step offers options, and the go is one of them.** Where the assistant has a question
  tool, the interview's questions with options, the choice of chapters in `read` and every plan
  are asked through it — *Go*, *Change something*, *Stop* closes a plan — and when the owner has
  nothing to answer the researcher proposes, from what is already in the folder: the questions
  they might be reading for, drawn from the sources and their tables of contents; a way of
  investing to start the beliefs from. A proposal the owner picks is theirs; one they did not pick
  is never written. `researcher-init` and `read` are at 0.2 for it.
* **`.apm/` stays the only copy, and `read` is a skill in it.** Two skills in `.apm/skills/` —
  `read` and `query` — and the eight commands in `.apm/prompts/`, as 0.2.0 laid them out; `compile`
  and `note` are gone. Both are written the way KaxaNuk-APM writes its own: a skill with a folded
  description, `metadata.version`, *When to Use* and *Steps*, its folder holding `SKILL.md` and
  nothing else — what `read` runs and reads, `scripts/extract.py` and `references/note.md`, lives
  at the root of the home, so `.apm/` carries prose only; a command with an `input` list that APM
  turns into each harness's arguments, in place of `argument-hint` and `$ARGUMENTS`. The agent that
  `researcher-init` writes names `read` where it named `compile` and `note`, and `audit` checks
  the agent file as well as the installed copies.
* **One note, one convention, both repositories.** A note has the same shape at home and in a
  strategy: the KN Research Process note's frontmatter — `source`, `citation`, `local_copy`, `read`
  — plus `tags` for the owner's tag policy; the name `Author_Year_Title`; the source's claims as
  headings, in its authors' terms, and what each implies for the owner's question — or the
  strategy's claim, by number — as a blockquote; `## Why it is here` first and `## What it changes`
  last. In a strategy `read` writes the note beside the PDF in `Bibliotheca/Papers/` or `Books/`,
  its row in `BIBLIOGRAPHY.md`, and a line in `Bibliotheca/LOG.md`; `Bibliotheca/Knowledge/` is no
  longer written. A note the home library already holds travels into a strategy without re-reading
  the PDF: the source's part is carried, and the implications are written anew for the strategy's
  claims. The `writer` field is gone — git records who wrote — and the word *article* with it: every
  skill says *note*. `refresh-index` is home only, because a strategy's `BIBLIOGRAPHY.md` is
  curated by hand; `read` writes each note's row and `audit` reports the gaps.
* `compile` is `read`, rebuilt around the owner's choice. A script pulls a PDF's table of contents
  and its chapters into text; the researcher shows the table of contents, proposes *read*, *skim* or
  *skip* for each chapter against the owner's questions, reads only what they choose, and writes
  one note per chapter read. A book is a folder, with an `INDEX.md` that records what became of
  every chapter; a paper is one file. "One article per idea" gives way to one note per unit read —
  an idea that spans sources is a synthesis, written on request, linking the notes it rests on.
  The chapter and pages read go in a provenance line under the title.
* `Sources/Notes/` is `Sources/Clippings/` — articles, transcripts and threads the owner collected.
  Now that *note* names what the researcher writes, a folder of raw material could not keep the
  word. The strategy template still says `Bibliotheca/Notes/`; the table in `AGENTS.md` maps one to
  the other.
* Every skill opens with the same lines — find the home, read `RESEARCHER.md` and `AGENTS.md`, and
  in a strategy take the paths from *Working in a strategy* — and that table in `AGENTS.md` is now
  the one place that says where a path lands there, the owner's questions included. The *Which
  library* paragraph that `read`, `query` and `audit` each carried is gone.
* `refine` says what it edits — a file in `Philosophy/`, the owner's own writing — and `audit`
  says what it does: reports, appends one line to the log, never fixes on its own. Neither was
  described that way before.

### Added

* **The wiki: concept pages.** Beside the source notes, `Knowledge/` now holds one small page per
  idea the library knows about, created and updated by `read` as chapters come in — every claim on
  it citing the chapter note and its page, contradictions kept under a callout, an `## Open` list
  of what the library does not yet hold. `query` lands on those pages first and follows them to
  the notes, and offers to keep an answer that spans several notes as a synthesis page, on your
  go. `audit` lints them: a claim with no note behind it, a page that cites a PDF, a chapter whose
  ideas reached no page. `INDEX.md` lists *Concepts* before *Sources* under each domain. A strategy
  has no pages — `OBJECTIVE.md` is its synthesis. This is the LLM-wiki pattern the library was
  built on, kept: the chapter is the unit of choice and provenance, the idea is the unit of
  knowledge. `read` is at 0.3; `query`, `audit` and `refresh-index` at 0.2.
* `RESEARCHER.md` gains *What you are reading for*: the owner's open questions, numbered, each with
  what it feeds and what would change their mind, and what is out of scope for now. It is the one
  section meant to change often, and the owner edits it by hand. `researcher-init` asks for it as
  its last question. `read` reads it before every source and asks which question each one serves,
  by number, instead of a free reason — that is what `## Why it is here` now records and what
  `## What it changes` is measured against. When the section is empty at home, `read` asks for the
  questions first and offers to write them, on the owner's go; in a strategy the numbered claims in
  `OBJECTIVE.md` play that role, and nothing is written at home.
* `scripts/extract.py`, the first code in this repository, because extraction
  is deterministic and the researcher was doing it by hand, twenty pages at a time. It reads the
  PDF's outline, prints the chapters with their pages, and writes one markdown file per chapter
  asked for, a marker before every page — `pdftotext` when it is on the machine, `pypdf` otherwise,
  and it says which. It refuses a PDF with no text layer instead of guessing, takes page ranges by
  hand when a PDF has no outline, and runs with `uv run`, its one dependency declared inline, so it
  needs no install step. Its output lives in `Extracts/` at home and `Bibliotheca/Extracts/` in a
  strategy: a cache, gitignored, regenerable, never cited.
* `references/note.md`, the shape of every note the researcher writes, at home
  and in a strategy — paths and names, frontmatter, the chapter note, the paper note, the book's
  `INDEX.md` and its status vocabulary, what the indexes show, how a home note travels.

### Fixed

* **`read` on a strategy whose `Bibliotheca/` is still a `.gitkeep`.** The KN Research Process
  template released 0.7.0 with `main` as the shape alone, every file below the six folders on its
  public `example` branch, so a new strategy has no `BIBLIOGRAPHY.md` to add a row to. `read` says
  so and hands over the one `git fetch` that brings step 1 across, then stops; it never scaffolds
  that file by hand.
* **`audit` called every command a stale install.** APM translates a command's `${input:name}` into
  each harness's own placeholder on install, so comparing a deployed copy byte for byte against
  `.apm/` always differed. It compares what APM does not rewrite. Found by running `audit deep`.
* **`Knowledge/INDEX.md` ships describing the index it now builds** — Concepts before Sources.

### Removed

* `note`, merged into `read`: the strategy note is what `read` writes there.
* The `writer` frontmatter field.
* The per-skill whitelist in `.gitignore`. Deployed copies under `.claude/`, `.agents/` and the
  other agents' folders are not versioned at all; `.apm/` is. `Extracts/`, `__pycache__/` and
  `.venv/` are ignored too.

## 0.2.0 (2026-09-09)

**MINOR** — the folders are renamed, and the researcher is no longer tied to one assistant.

**What to do differently:** if you already have a clone, rename three folders — `Library/` to
`Knowledge/`, `Notes/` to `Philosophy/`, `Output/` to `Projects/` — and nothing else moves. Then
run `apm install --target <your agent>` in the folder after you pull: `/compile`, `/query` and the
rest keep their names, and they are discoverable only in a **new** session.

### Changed

* `Library/` is now `Knowledge/`, `Notes/` is now `Philosophy/`, and `Output/` is now `Projects/`.
  The directionality is unchanged: `Sources/ → Knowledge/ → Projects/`, with `Philosophy/` cited
  and never compiled from.
* The eleven commands are APM primitives in `.apm/`, the only copy of each: three **skills** in
  `.apm/skills/` — `query`, `compile`, `note`, capabilities the researcher reaches for on its own
  when the work calls for them — and eight **commands** in `.apm/prompts/`, tasks you start by
  name. `apm install --target <agent>` copies them into the folders that agent reads, which git
  ignores, so nothing is committed twice and every assistant runs the same researcher. Codex has
  no command primitive, so there a command is run by naming its prompt file. `/audit` reports an
  installed copy that has gone stale.
* `/query` and the `library-query` skill were the same procedure reached two ways, and are merged
  into one `query` skill that still answers a direct question and still fires on its own.
* `apm.yml` no longer builds anything. It declares what publishes — `.apm/` and nothing else — so
  the researcher can be installed into a project you already have, and so a person's `Sources/`
  and `Philosophy/` are structurally incapable of being packed.
* `Sources/` now has `Books/`, `Papers/` and `Notes/`, and the taxonomy is yours to extend.
  `Sources/Notes/` is raw material you collected; your own writing stays in `Philosophy/`.
* Every skill now works from wherever the session is open. Each begins by finding the researcher's
  home — the folder that holds `RESEARCHER.md` — and reading `RESEARCHER.md` and `AGENTS.md`
  there, so the researcher is itself when invited into a strategy and not only at home.
* Strategy work lives in the strategy. Invited into a repository built from the KN Research
  Process template, the researcher's library is that repository's `Bibliotheca/` — `Papers/`,
  `Books/` and `Notes/` are the sources, `Bibliotheca/Knowledge/` the articles with their own
  index and log — and `/note`, `/objective`, `/blueprint` and `/brainstorm` write into the
  strategy's own files, after the plan and your go, for you to commit. `Projects/` keeps lessons
  and what you ask for in chat at home. **Nothing flows back:** while it works on a strategy the
  researcher writes nothing at home unless you ask for that write by name, so one experiment
  cannot leak into the researcher every strategy shares.
* `/compile` asks, before it reads, why each source is there. The answer opens the article as
  `## Why it is here`, in your words — the reason you added a source decides where it files, what
  it links to, which part of a book matters and what `## What it changes` is measured against —
  and a source read for a strategy ends with the `/note` that would carry it there. It walks every
  subfolder of `Sources/`, compiles a book a part at a time, naming in the log the parts done and
  the parts to come, and reports a source it cannot open rather than filling it in from memory.
  `/brainstorm` and `/teach` now read `Philosophy/`, so how you invest weighs on what to try next
  and on what you are taught.

### Added

* The researcher can be invited into a strategy: open your assistant in the strategy's folder, add
  the researcher's folder to the session, and the skills come along.
* **The researcher is an agent, not only a way of configuring a session.** `/researcher-init` now
  writes `.apm/agents/<your researcher>.agent.md` as well, so the harness can call it by name —
  *ask Ada what we have read about momentum crashes* — with its own tool boundary: read, search
  and the skills, and nothing that writes. Its prompt points at `RESEARCHER.md` and `AGENTS.md`
  instead of copying them, so there is still one source of truth. **It never writes**, structurally
  rather than by preference: every skill that writes waits for your go, and an agent reporting back
  cannot ask for one, so it names the skill for you to run instead. Claude Code, Copilot and Cursor
  enforce the tool list; Codex drops it, which is why the rule is in the prompt too; Gemini and
  Windsurf have no agent primitive. An existing researcher gets one by running `/researcher-init`
  again — it skips the interview when `RESEARCHER.md` is already filled in and only writes the
  agent.
* Two more ways to install: `apm install KaxaNuk/KaxaNuk-Researcher --target claude` adds the
  researcher to a project you already have, and `apm pack` builds a plain plugin bundle for agents
  that do not use APM.
* `.gitattributes`, so prose checks out with the bytes it was committed with on every platform.

### Removed

* `Philosophy/Private/`, and the rule that it was read only when named. `Philosophy/` is one
  folder, read and cited in full; anything you would not want read does not go in the repository.
* The `KaxaNuk/KaxaNuk-APM/common` dependency. It installed Python style rules — pep8,
  test-writing, bloom-code — into every assistant's context, and there is almost no code in this
  repository. It returns when there is a KaxaNuk package that teaches research rather than linting.
* `requirements-dev.txt`. It pinned `apm-cli` for `pip`; the README now says where the APM CLI
  comes from, and `apm install --target <agent>` is the one step a clone needs.

### Fixed

* `apm.yml` declared `KaxaNuk/KaxaNuk-APM/data-curator` and `.../investment-lab`, which do not
  exist in that repository, so every `apm install` failed before it did anything.

## 0.1.0 (2026-09-05)

**MINOR** — the first researcher skeleton.

**What to do differently:** clone it under the name you give your researcher, open the folder in
Claude Code, run `/researcher-init`.

### Added

* The library architecture — `Sources/` read-only, `Library/` compiled with one `INDEX.md` and an
  append-only `LOG.md`, `Notes/` cited never compiled, `Notes/Private/` never read unasked,
  `Output/` written only when asked — adapted from the MIT-licensed obsidian-vault-kit, with
  standard markdown links instead of wikilinks and no dependency on any viewer.
* `RESEARCHER.md`, the personality file the `/researcher-init` interview writes: name, owner,
  domains, voice, beliefs, non-negotiables, tag policy, the strategies it works on.
* `AGENTS.md`, the operating rules, and `CLAUDE.md` pointing at both.
* Eleven commands: `researcher-init`, `compile`, `query`, `teach`, `audit`, `refine`,
  `refresh-index`, and the four that connect the researcher to a strategy built from the KN
  Research Process template — `note`, `objective`, `blueprint`, `brainstorm`.
* The `library-query` skill, which answers questions about what the library says from the index
  and the links, citing every claim.
* `apm.yml` declaring KaxaNuk's core knowledge — the `common`, `data-curator` and `investment-lab`
  packages from `KaxaNuk/KaxaNuk-APM` — so `apm install` teaches the researcher the process and the
  Lab modules.
