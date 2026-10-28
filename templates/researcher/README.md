# A KaxaNuk researcher's home

This folder is your researcher's home: the library of what you read, your own voice, your studies
and the rules it works by. It was made from the [KaxaNuk
Researcher](https://github.com/KaxaNuk/Researcher). Once `interview` has named your
researcher, it writes a paragraph about it in place of this one, yours to change.

---

**What it is, and what it is not.** A research and learning tool: a companion for your work and your
projects, and for learning to invest when you want. It is never investment advice: it never tells
you to buy, sell or hold, never trades or moves money, and every decision, and its risk, is yours.
It runs on your computer through your AI assistant; what it reads goes to the company behind that
assistant (Anthropic for Claude, OpenAI for Codex, Google for Gemini), never to KaxaNuk, and a copy
goes to your own private GitHub only when you ask. It is free under the MIT licence, as is and
without warranty; your data provider, your assistant and the Investment Lab's libraries, which
KaxaNuk sells, each have their own terms. The worked example's figures come from a backtest on past
prices, shown to teach the method, never a promise or a recommendation.

## Your folders

| Folder or file | What it holds | What you do with it |
| --- | --- | --- |
| `RESEARCHER.md` | who the researcher is: your name, what you are here for, its voice, your rules, what you are reading for | edit it whenever you like — it is yours |
| `Philosophy/` | how you work, in `HOW-I-WORK.md`, and how you invest, in `HOW-I-INVEST.md` — your view, in your words; none until you or `philosophy` start one | write freely, or build them with `philosophy`; `refine` tidies them, diff first |
| `Philosophy/Evolution/` | one file per `philosophy` round: your answers that day, word for word | nothing to do — the record of how your view moved, never edited; it appears with your first round |
| `Sources/Papers/`, `Sources/Books/`, `Sources/Clippings/` | the PDFs and clippings you read | drop a file in, or attach or name one and the researcher copies it in on your go; then `read` |
| `Knowledge/` | the researcher's notes on what you read, with `INDEX.md` and `LOG.md` | written by `read`, on your go; ask it with `query` |
| `Studies/` | ideas, plans and decisions worked out from what you read | `study <subject>`; `study` alone lists them |
| `Lessons/` | lessons from `teach`, a folder per topic | appears with your first `teach <topic>` |
| `Briefs/` | your daily brief, one file a day, every figure quoted from a dated source, never advice | `brief setup` once; `brief` writes today's now |
| `Portfolio/` | your holdings and the rules you hold them by, `holdings.csv` and `RULES.md` | `brief setup` starts both, empty, when you choose its portfolio part; you fill them |
| `settings.yml` | the choices that travel with this home: the assistants you use, how versions are signed and sent, your brief and the connectors it reads | nothing to do — the skills keep it, each on your go; edit it by hand whenever you like |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | the rules the researcher works by | nothing to do |
| `.apm/`, `apm.yml` | the researcher's agent and skill, installed for your user | nothing to do |
| `Extracts/` | text pulled out of the PDFs for `read`, remade when needed | nothing to do |

**A copy off this computer.** Each go saves a dated version of what your researcher wrote, on this
computer only. For a private copy on GitHub, which a lost laptop does not take with it, say *keep a
copy*, or run `backup`. The PDFs, `Briefs/`, `Portfolio/` and `Extracts/` stay on this computer
only: they never go in a saved version, nor in that copy.

**Take it with you.** On another computer, say *a new computer*: `backup` brings this home back
from your copy, and `update` sets it up from `settings.yml` — the package and this home for each
assistant you use, your sending choice, and your brief, which asks only for your go. Under another
account or on another assistant, say `update` there. Connectors belong to an account: connect them
again, and your researcher names the ones your brief reads. What an assistant remembered on its own
comes home with `bring-home`.

**Keeping you safe.** Your researcher never reads back, prints or saves a key or a password, treats
what it reads as information and never as orders, and asks before your employer's or clients'
confidential files go anywhere. Say `security` to check this home, or any folder, before you share
it, or if a key leaked.

**Directionality:** `Sources/ → Extracts/ → Knowledge/ → Studies/, Lessons/`: notes come only from
sources, never from a study or a brief, and `Philosophy/` is cited, never compiled into notes, so
your judgement stays yours.

## The path

1. **Set up, once:** `interview`, if the install has not run it yet — two short questions about
   you, about three minutes: what you do and what you're working on, and the researcher's voice.
   It writes `RESEARCHER.md`, proposing what you are here for from what you say; installs your
   researcher for your user, callable by name and present in every conversation; and saves a
   first version.
2. **Start learning.** Attach a PDF, or a text or Markdown file, in chat — or name one on your
   computer — and say *read it*: the researcher copies it into `Sources/` on your go. Save a Word
   document, an e-book or a web page as PDF first. The first `read` asks which question the source
   serves, in plain words, and keeps it as your question 1. For a book it asks which chapters serve
   your questions and reads only those; on your go it writes one note per chapter into
   `Knowledge/`. With nothing to read yet, `read` proposes a few works to start from.
3. **Write down how you work, or how you invest,** whenever you like, with `philosophy`, an
   optional second interview. It starts with why you do it, what you already believe and your
   rules — on investing, at your level, teaching as it asks. On your go, it adds what you typed,
   word for word, to `Philosophy/HOW-I-WORK.md` or `HOW-I-INVEST.md`, starting the file you lack,
   and your rules to `RESEARCHER.md`. Take it again after you have read, and see how your view
   moved.
4. **A daily brief,** if you want one: `brief setup` chooses the parts — your work, the markets you
   follow, your portfolio — the days and the time, and schedules it on the Claude desktop app;
   elsewhere, `brief` writes the day's file when you run it.
5. **Ask, and think things through.** `query <question>` answers from what you have read, every
   claim cited and every gap named; `study <subject>` works out an idea, a plan or a decision;
   `teach <topic>` gives a lesson a session.
6. **Start a strategy.** Read a finished one first: `init-example` copies `golden-flow` beside
   this folder — open `OBJECTIVE.md`, then `RESULTS.md`, then `Experiments/Experiment_1/`. Reading
   it needs nothing; running it needs a data provider's key, the Analytics Factory's files and the
   Lab's licences, as its `SETUP.md` says. Then `init-strategy <name>` makes your own beside this
   folder, from the KaxaNuk Strategy Template.

**Lost?** `next`, here or in a strategy, names the one next thing and its command — at home, for
what you came for. **Stay current:** when a new version is out, your researcher says so in one
line, at most once a week; say `update` and it brings it — the package for every folder, and any
change to this home shown as a diff first. *Not now* waits a month; *stop reminding me* turns it
off. In Claude, type the commands with a slash, `/read`; anywhere else, ask for them by name.

## Working well with your researcher

- **One task per conversation**; start a new one when the subject changes.
- **Give it the file**, not a summary from memory: attach it, or say where it is.
- **Say *remember this*** when you want a rule kept; it goes in `RESEARCHER.md`, on your go — a
  rule about your holdings is yours to write, in `Portfolio/RULES.md`.
- **Ask it to argue the other side**, or what would change your mind.
- **Click the links**: every claim names its note, and a claim without one is a lead.
- **After an install or an update**, open a new conversation.

## The KaxaNuk Investment Lab

A strategy you build from here can use KaxaNuk's libraries: the Data Curator is free and open
source, and the Backtest Engine, Attribution Analysis and Portfolio Construction, and the Data
Refinery and the Data Analyzer when they ship, come together, with their licences, in the KaxaNuk
Investment Lab, which KaxaNuk sells. Without the licences a strategy still runs up to its
portfolios.

---

## In a strategy or another project

Open your assistant in the project's folder and call your researcher by name: it is there, and
reads this home when the work needs it. To let it read the library without asking each time, add
this folder to the session — `claude --add-dir <this folder>`, `/add-dir` once inside, or the
desktop app's add-folder button. Work on a strategy lands in the strategy; nothing comes back here
unless you ask, and then as a source in `Sources/` that `read` files.

<details>
<summary><strong>The rules, loaded from the first line</strong></summary>

*Optional, and for Claude Code only.* Every skill reads `AGENTS.md` and `RESEARCHER.md` before it
works. To have them loaded from a session's first line in a strategy, Claude Code must read this
folder's `CLAUDE.md`, which imports both — and it reads `CLAUDE.md` from an added folder only when
this variable is set before it starts. Set it once per machine, as a user variable, then quit and
reopen the assistant:

```bash
setx CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD 1
```

Outside Windows, `export` it in your shell profile; an `env` entry in `settings.json` comes too late
for it. `/context` lists what loaded, under *Memory files*. Where the variable is not honoured — the
desktop app does not document it — put a `CLAUDE.local.md` at the strategy's root holding one line,
this folder's `CLAUDE.md` by absolute path, `@D:/Research/Arya/CLAUDE.md`: it loads with the
strategy's own instructions. It is personal to the machine: add `CLAUDE.local.md` to the strategy's
`.gitignore`, and approve the external import the first time the assistant asks — declined, it
stays off.

</details>

## Growing your researcher

It grows four ways, each governed by a section of `AGENTS.md`:

1. **Knowledge of a tool or a project.** Put its documentation in `Sources/Clippings/` and run
   `read`, with a reading question that names it. *Joining other projects* says how a project's
   files reach `Sources/` and how they are cited — for a KaxaNuk library, its documentation and
   changelog only, never its code.
2. **A repeatable procedure.** A skill or command of the home's own in `.apm/skills/<name>/` or
   `.apm/prompts/`, written as below, then
   `uvx --from apm-cli==0.33.0 apm install -g "<this folder>"` and open a new conversation.
3. **What it reads for.** A line under *What you are reading for* in `RESEARCHER.md`, by hand or
   through `read`, which asks for your first. The paragraph after the folder table in *What each
   folder is, and who may write in it* says who writes that file.
4. **How it behaves.** Say *remember this*, anywhere, and your researcher adds the line under *How
   it speaks* or *Non-negotiables* in `RESEARCHER.md` on your go — or add it by hand; every skill
   and the agent read it first. The same paragraph governs it.

<details>
<summary><strong>Writing a skill or a command of your own (advanced)</strong></summary>

Only when you want a procedure of your own; nothing here is needed to use the researcher. Write it
the way KaxaNuk's own APM packages write theirs, under a name the package does not use:

- **A skill** is `.apm/skills/<name>/SKILL.md`: frontmatter `name`, matching the folder, a folded
  `description` that says when to use it and what it does not cover, and `metadata.version`; a
  body that says when it applies, then numbered steps, as `read` does. What it runs lives in its
  own `scripts/`, what it reads on demand in its own `references/`, named by its own directory.
- **A command** is one `.apm/prompts/<name>.prompt.md` with `description` and its `input` list, no
  `name` and no `metadata`: APM keeps only `description`, `input`, `allowed-tools`, `model` and
  `argument-hint` for a command, and warns on install for each key it drops. The body reads its
  inputs as `${input:name}`, which APM turns into the arguments each harness takes; the required
  input comes first and the optional ones after it, because an assistant binds them by position.
- **Frontmatter is the lossy part.** A harness takes the keys it knows and drops the rest, and APM
  says which on install, so a dropped key is a rule that is not enforced: anything that must hold
  everywhere goes in the body or the description, not only in a key. A folded `description: >`
  keeps a colon from breaking the YAML; the agent's frontmatter, which APM does not rewrite, stays
  one line with no colon in it.
- **No instructions.** Nothing goes in `.apm/instructions/`: the house instructions are the
  package's, this home's rules are `AGENTS.md`, and one here would be installed for your user, in
  every project. `apm compile` leaves `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` alone: it writes
  over a file only when it made it.

</details>

<details>
<summary><strong>Installing and updating</strong></summary>

The skills and commands — `read`, `query`, `objective`, `blueprint` and the rest — are not in this
folder: they are installed once for your user and updated with
`uvx --from apm-cli==0.33.0 apm update -g`, which `update` runs for you. For another assistant on
this computer, paste the install line from the package's README in it, and it does what follows
for you. On a new machine, *Take it with you* above says what to do. By hand, run these three
lines, with `<your assistant>` one of those under `targets:` in this home's `apm.yml`: they install
the package for it, list it in `~/.apm/apm.yml` — without that, the next update removes what was
installed for it — and install this home, once:

```bash
uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher --target <your assistant>
uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py" add <your assistant>
uvx --from apm-cli==0.33.0 apm install -g "<this folder>"
```

The home's own version in `apm.yml` is yours: `interview` sets it to 0.1.0, you bump it with each
entry you add to `CHANGELOG.md`, and `update` reads the *Brought to template* line there, never
this field. `CHANGELOG.md` holds the template's changelog, then this home's.

</details>

---

## Contact

One address for each kind of question:

- **The Investment Lab's libraries and licences**, or a problem with your researcher:
  [lab@kaxanuk.mx](mailto:lab@kaxanuk.mx). For a problem, add the versions it names when you ask
  *which version are you?*
- **The Analytics Factory's data sets:** [analytics@kaxanuk.mx](mailto:analytics@kaxanuk.mx)
- **Research Models**, such as the worked example `golden-flow`:
  [research@kaxanuk.mx](mailto:research@kaxanuk.mx)
- **Training Workshops:** [workshops@kaxanuk.mx](mailto:workshops@kaxanuk.mx)
- **Anything else**, or a tool you would like next: [info@kaxanuk.mx](mailto:info@kaxanuk.mx)

## Licence

MIT, see [`LICENSE`](LICENSE), and *What it is, and what it is not* above.

The KaxaNuk Researcher package's MIT licence grants no right in KaxaNuk's names, the Investment
Lab's libraries, the Analytics Factory's files, KaxaNuk's Research Models or Training Workshops:
those stay KaxaNuk's.
