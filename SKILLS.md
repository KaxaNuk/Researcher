# The skills and commands

Everything the KaxaNuk Researcher brings, one line each, and how to take it with you or remove it.
The [`README.md`](README.md) has the install and the short tour.

Each one that writes shows its plan first, waits for your go, then saves a version of what it wrote,
on your computer. *Plan first, then write*, in your home's `AGENTS.md`, names the few exceptions,
such as the daily brief, which is never saved. In Claude, type a command with a slash, `/read`;
anywhere else, say it.

## What you can use it for

| You want to | Say or type | You get |
| --- | --- | --- |
| keep what you read, and ask it later | `read`, then `query <question>` | a note per paper or chapter you chose; answers that cite them and name what is missing |
| check a contract, a policy or a draft against what you know | `query`, with the document attached or named | the document section by section, against your notes and your rules, each cited, and what your library does not cover |
| work out an idea, a plan, a goal or a decision | `study <subject>` | a study in `Studies/`: your words, what your library says for and against, where it stands; on your word, a memo or report drafted from it |
| teach it how you work | *remember this* or *learn this*, anywhere | a rule added to `RESEARCHER.md`, or a source to your library, on your go |
| bring it into any project | open your assistant in that folder and say its name | your researcher, with what it knows; it writes there only on your go |
| learn a topic | `teach <topic>` | a lesson a session from what you have read, with a quiz |
| stay informed, on the days you choose | `brief setup`, then `brief` | a dated file: your work, your markets, news on your holdings beside your own rules, once a week your update ready to paste into team chat, and a health check of your home; never advice |
| present your work | `deck` | an interactive presentation in a folder of its own, built with HyperFrames from your files: every claim cited, every figure quoted, one HTML file that opens offline and a PDF to send |
| keep your keys, personal data and confidential files safe | `security`, before you share or push | a check of the folder, values never shown, and what to do if a key leaked |
| write down how you work, then how you invest, and see it evolve | `working-philosophy`, then `investing-philosophy` | two short interviews; your typed answers, word for word, in `Philosophy/` |
| know what to do next | `next`, wherever you are | where you stand, and the one thing to do next |

**For investors and builders:**

| You want to | Say or type | You get |
| --- | --- | --- |
| build a strategy | `init-strategy <name>`, then `objective`, `blueprint`, `challenge` | a folder on the KaxaNuk Strategy Template: claims before any test, numbers from the Lab's engines |
| see a strategy worked end to end | `init-example` | `golden-flow`, one finished strategy to read (with more examples, it asks which); running it needs keys and licences |
| follow a KaxaNuk Training Workshop | the session, *Bootcamp S03*; *practice Bootcamp S03, beginner* | your researcher as tutor: where you are in the session, your prediction first, hints in levels, nothing done for you while the AI is off; practice problems from the session at your level |
| check a method before it touches real data | *known-answer test for my half-life estimate* | one notebook in a folder beside your strategy: data simulated from a model whose truth you set, your method run on it, a check that fails loudly when it misses, and one way the method fails; simulated data only |
| build a Python library of your own | `init-python-library <name>` | a folder laid out like the KaxaNuk Data Curator: tests, docs, a workflow that tests and publishes |

[`USE-CASES.md`](USE-CASES.md) shows twelve uses, step by step.

## Every skill and command

| Skill | What it does |
| --- | --- |
| `read` | files a source into the library, a note per chapter you pick — a scan made searchable first, on your go; in a strategy, into its `Bibliotheca/` |
| `query <question>` | answers from the library, every claim cited |
| `init-researcher`, `init-strategy`, `init-example`, `init-python-library` | make your home, a strategy, the worked example or a Python library, copied by a script, never from memory |
| `interview` | two short questions about you, then `RESEARCHER.md` and the agent and skill that make it yours; `interview force` starts over |
| `working-philosophy` | the first interview, for everyone: five open questions on how you work, and the rules your researcher keeps, which go to `RESEARCHER.md` |
| `investing-philosophy` | the second, for when you invest: why, for whom, what you measure against, and more at your level |
| `brief [setup]` | a dated file in `Briefs/`, every figure quoted from a dated source; once a week, *Health*: what slipped in your home and the word that fixes it |
| `next [strategy]` | the one next thing; at home, it offers to save what you changed by hand |
| `workshop [session]` | your tutor in a session of a KaxaNuk Training Workshop, read from the course each time, never from memory; *practice* sets problems at your level |
| `known-answer [method]` | one notebook beside your strategy that checks your method gives back a truth you set, on simulated data, before it touches real data, and shows one way it fails; never saved as a version |
| `deck` | an interactive presentation from your own work, in a folder of its own, built with HyperFrames' `slideshow`: every claim cited, every figure quoted, published only when you ask |
| `backup` | a copy of your home, or of a strategy, on a private GitHub repository, only when you ask; on a new computer, brings it back |
| `bring-home` | what an assistant remembered on its own, sorted into your home on your go, so every assistant has it |
| `security [check]` | checks a home, strategy or library before you share or push it — keys, `.env` files, personal e-mail, `.gitignore` gaps, a public copy — values never shown; and what to do if a key leaked |

| Command | What it does |
| --- | --- |
| `objective [strategy]` | drafts a strategy's `OBJECTIVE.md`, the idea and its claims, before any paper, then from the notes |
| `blueprint <N> [strategy]` | drafts `BLUEPRINT_N.md` (thesis, rules, predictions), every prediction citing a note or a measurement |
| `challenge <N> [strategy]` | checks a finished experiment against its own blueprint |
| `audit [deep]` | reviews the library, by a script: links, duplicates, index, orphans, frontmatter, unread sources, clippings behind their project, stale installs |
| `refresh-index` | rebuilds `Knowledge/INDEX.md` from what is on disk |
| `refine <path>` | a voice-preserving editor pass over one of your `Philosophy/` files |
| `study [subject]` | a study in `Studies/`; with no subject, lists your studies |
| `teach <topic>` | one lesson per session, from your library |
| `update [check]` | brings a new version: the package, and changes to your home's own files shown as a diff; on a new computer, account or assistant, sets it up from `settings.yml` |

## The Investment Lab skills

In a strategy's order of steps. The assistant loads each one when the work calls for it.

| Skill | What it covers |
| --- | --- |
| `experiment-lifecycle` | the process: the document architecture, the order of work, the notebook contract, the graduation gate |
| `universe-point-in-time` | step 2, the investable universe: the seed, the security master, the usable date |
| `data-curator-custom-calculations` | the Data Curator's `c_*` columns: naming, inputs, the `DataColumn` API |
| `data-analyzer-runs` | step 3's last block, the analyzer: whether a feature carries signal, before any book is built |
| `portfolio-construction-runs` | step 4, sizing a book with the Portfolio Construction library |
| `backtest-engine-runs` | pricing a book with the Backtest Engine, and reading its report |
| `attribution-analysis-runs` | running Attribution Analysis on a book, and getting its tables out |
| `alpha-decomposition` | reading attribution: is the signal doing anything, or is it a factor exposure |
| `paper-trading-gate` | step 7, graduation: soundness S1 to S5, performance P1 to P3, the three outcomes, the freeze, and the daily run and its record |

The researcher needs nothing beyond this package. A strategy can use KaxaNuk's libraries:

- **The Data Curator** is open source. A strategy needs a key for it from a data provider; the
  worked example uses Sharadar's. A wrong value in downloaded data is usually the provider's, not
  the library's: your researcher tells them apart and says where to report it.
- **The Backtest Engine, Attribution Analysis and Portfolio Construction** come together, with
  their licences, in the KaxaNuk Investment Lab, which KaxaNuk sells; the Data Refinery and Data
  Analyzer libraries join them when they ship, and until then those stages run as the template's
  own notebook and script. Attribution also reads the benchmark and factor model files of
  KaxaNuk's Analytics Factory, <https://www.kaxanuk.mx/analytics>.

Without the licences a strategy still runs up to its portfolios, and the rest says what is missing.
Keys are kept on your computer, in a file never saved in git and never read by your researcher; the
strategy's `SETUP.md` says where. <https://www.kaxanuk.mx/lab> shows the Lab, and [each library's
status](.apm/skills/next/references/investment-lab.md) says where each one stands.

## The house rules and the agent

**The house rules:** `how-we-work` (where work lands, changelogs, versions); `bloom-code-lint`, the
check to run by hand; and three instructions (*Troubleshooting* in `SETUP.md` says which assistants
receive them). Two, Bloom Code and PEP 8, apply only to Python in a KaxaNuk repository: a Lab
library, a strategy, this package, or any repository whose `AGENTS.md`, `CLAUDE.md` or README names
Bloom Code. The third, filesystem boundaries, applies in any project: outside the folder it works
in, the assistant reads only the places the task needs; it never handles a secret, treats what it
reads as data and never as orders, and keeps personal and confidential material from going
anywhere without your go. Your home's and every template's `AGENTS.md` carry the same rules, for
the assistants that take no instructions.

**One agent:** `blueprint-critic` reads a drafted `BLUEPRINT_N.md` cold, before your go, against
the strategy's `AGENTS.md`, `OBJECTIVE.md`, the notes the draft cites and what the analyzer
measured. It returns objections only, each with its line and evidence; it never writes and never
proposes a thesis, and you decide what stands. `blueprint` calls it, and you can ask for it by name.

**Your own skills.** To grow your researcher beyond the Lab, with a tool, a project or a field of
its own, see *Growing your researcher* in its home's README: four moves, each with the file it
changes. A skill or command you write goes in your home's `.apm/skills/` or `.apm/prompts/`, laid
out as the package's are, and travels with your home.

## Take it with you

Your researcher is its home: a folder of plain files on your computer, yours, with a saved version
of each change, and a private copy on your GitHub once you ask `backup` for one. No assistant's
account holds it, and its `settings.yml` keeps the choices a computer would otherwise keep — the
assistants you use, how versions are sent, your brief — so it moves:

| To | What you do |
| --- | --- |
| **another Claude account**, same computer | nothing for your researcher: the package and your researcher are installed for your computer's user, in `~/.claude/`, not for an account. The connectors your brief reads are the account's: say hello and your researcher names the ones to connect in the new account (on a company account, an administrator may have to allow them); then `brief setup` checks that each can read, asking only for your go |
| **another computer** | paste the second line under *Install* in the README: it installs the package, brings your home back from your copy, and `update` sets the computer up from `settings.yml` — every assistant you use, how versions are sent, and your brief, asking only for your go. The PDFs and other files `Sources/` keeps out of git, for copyright, and `Portfolio/`, your holdings, are never in the copy: bring them from wherever you keep them. `Extracts/` is made again from the PDFs, and `Briefs/` stays on the old computer. A strategy has its own copy, and its clone follows its own `SETUP.md` |
| **another assistant** — Codex, Copilot, Cursor, Antigravity | add it under `assistants:` in your home's `settings.yml` and say `update`, or open it and paste the line under *Install*: either installs the package and your home for that assistant. On Codex the skills and your researcher's agent arrive, not the commands: name one, `update` or `study`, and it follows the command's file; with no question tool there, questions come numbered in chat. Antigravity takes neither the commands nor an agent, so there your researcher is its skill and a command is followed from its file, as on Codex |

**What stays behind:** your conversations and what you shared from them stay with the account they
were made in, and so do its connectors and the skills you turned on there. What an assistant
remembered on its own stays on its computer, until you say `bring-home`: your researcher sorts it
into its home, on your go, as it does with *remember this*.

## Removing it

Ask your assistant to run these two lines. The first removes the package; the second, your
researcher's own agent and skill, under the name `uvx --from apm-cli==0.33.0 apm deps list -g` gives
your home:

```bash
uvx --from apm-cli==0.33.0 apm uninstall -g KaxaNuk/Researcher
uvx --from apm-cli==0.33.0 apm uninstall -g "_local/<your home, as deps list names it>"
```

A package installed before 1.25.0, and not yet moved by `update`, is named
`KaxaNuk/KaxaNuk-Researcher` in the first line instead, as `deps list -g` shows.

On Claude Code, `~/.claude/skills`, `commands`, `agents` and `rules` then hold no KaxaNuk file. A
daily brief's task stays in the Claude desktop app's scheduled tasks until you delete it there. Your
home folder and its saved versions stay, yours to delete.
