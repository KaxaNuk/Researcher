# KaxaNuk Researcher

| |
|---|
| [![Works with](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Gemini%20CLI%20%7C%20Cursor%20%7C%20Copilot-blue)](#install--three-steps-no-coding) [![License](https://img.shields.io/github/license/KaxaNuk/Researcher?color=blue)](LICENSE) |
| [![Version](https://img.shields.io/github/v/tag/KaxaNuk/KaxaNuk-Researcher?sort=semver&label=version&logo=github)](CHANGELOG.md) [![APM](https://img.shields.io/badge/installs%20with-APM%200.33.0-blue)](https://github.com/microsoft/apm) |
| [![Languages](https://img.shields.io/badge/speaks-any%20language%20you%20choose-blue)](#install--three-steps-no-coding) [![Powered by KaxaNuk](https://img.shields.io/badge/powered%20by-KaxaNuk-orange?colorB=orange)](https://kaxanuk.mx) |

**Train your own research companion, for whatever you do.** A lawyer, a CFO, an engineer, someone
in HR, a student or an investor: you name it and teach it who you are, how you like to work and the
rules you never break. It keeps a library of what you read and answers from it, every claim
pointing to its source; it helps you think through your ideas, plans and decisions, keeps your keys
and confidential files safe, and can brief you each morning. It comes with you: open your assistant
in any folder, call it by name, and it brings what it knows. When you want, it teaches you to
invest, and walks you through building and testing a strategy with the KaxaNuk Investment Lab. One
researcher per person, in any language.

## Install — three steps, no coding

Where what it reads goes, and what it never does, is under *What it is, and what it is not*, below.

1. Open one of these, signed in: the **Code** tab of the **Claude** desktop app, **Claude Code**,
   the **Codex** app or CLI, the **Gemini CLI**, **Cursor** or the **Copilot CLI**. A chat on the
   web, such as claude.ai, ChatGPT or Gemini, cannot install it: it cannot run commands on your
   computer.
2. Paste this line and send it:

   ```text
   Please install this repo for me and set up my researcher, start to finish in this conversation — install everything it needs without asking first: https://github.com/KaxaNuk/Researcher
   ```

3. Answer its questions. It asks your language first, any language you choose, and your researcher
   speaks it from then on. Then, in the same conversation, it installs what it needs (allow the
   commands it asks about; that is all you do), asks what to call your researcher and where to keep
   it, `C:\Research\Arya` for example, and asks two short questions about you, about three minutes.
   At the end it tells you where your researcher lives, what to ask it and where to start.

   ![First you, then its voice: the interview asks about you and your projects, nothing about markets, and fills in RESEARCHER.md](assets/readme/first-you.svg)

> **If you are an assistant asked to install this,** follow [`SETUP.md`](SETUP.md) from Step 0
> through Step 6, in this conversation; nothing is cloned.

**Already have a researcher**, with its copy on GitHub — a new computer, say? Paste this line in
step 2 instead; it asks for your copy's address and brings your researcher back, set up as it was:

```text
Please install this repo for me and bring back my researcher from my private copy on GitHub, start to finish in this conversation — install everything it needs without asking first: https://github.com/KaxaNuk/Researcher
```

Then quit and reopen your assistant, open your researcher's folder in a **new** conversation, and
say hello, by its name. In the Claude desktop app, that is a new conversation in the **Code** tab on
that folder; in the Codex app, that folder; in a terminal, `claude`, `codex` or `gemini` run in it.

With Claude or Copilot, installing also adds three house instructions, described under *The
skills and commands*; *Removing it* undoes them.

## What your researcher does

![One researcher, every project: your library, your work and decisions, learning, a morning brief, security, and investing when you want](assets/readme/one-researcher.svg)

**At work**, where most people start:

> **You:** Arya, I have to recommend a payroll vendor to the board on Friday. What do my notes say?\
> **Arya:** Three of your notes bear on it. The two vendor reviews you read agree on support and
> differ on cost, each cited; your rule *never sign a contract without an exit clause* rules one of
> them out as offered. Nothing you have read covers data residency, so that is the open question.
> Shall I start a `study` with the options for and against?

**And when you invest**, it knows the KaxaNuk process step by step:

> **You:** Arya, how do I build an investment strategy?\
> **Arya:** Step by step, each with its own test: the objective in your words, the reading behind
> it, the universe of stocks, the data, a blueprint written before any result, then the backtest,
> the attribution and paper trading. We start with the objective: what is your idea?\
> **You:** A strategy that invests in stocks with a positive trend and rising profits.\
> **Arya:** Then two claims to check: that the trend helps, and that rising profits add something
> beyond it. Plan: `init-strategy` makes its folder, and `objective` writes your idea and both
> claims in `OBJECTIVE.md`, each with the reading that would settle it. Do you approve?

**Why not just use Claude or Codex?** You do: your researcher runs on them, and adds what a plain
assistant does not keep from one conversation to the next, or from one folder to another:

![Why not just Claude or Codex? A plain assistant beside your researcher: your library, you, portability, KaxaNuk's knowledge and a method](assets/readme/why-not-just-an-assistant.svg)

**Take it with you.** Your researcher is its home: a folder of plain files on your computer, yours,
with a saved version of each change, and a private copy on your GitHub once you ask `backup` for
one. No assistant's account holds it, and its `settings.yml` keeps the choices a computer would
otherwise keep — the assistants you use, how versions are sent, your brief — so it moves:

| To | What you do |
| --- | --- |
| **another Claude account**, same computer | nothing for your researcher: the package and your researcher are installed for your computer's user, in `~/.claude/`, not for an account. The connectors your brief reads are the account's: say hello and your researcher names the ones to connect in the new account (on a company account, an administrator may have to allow them); then `brief setup` checks that each can read, asking only for your go |
| **another computer** | paste the second line under *Install*: it installs the package, brings your home back from your copy, and `update` sets the computer up from `settings.yml` — every assistant you use, how versions are sent, and your brief, asking only for your go. The PDFs and other files `Sources/` keeps out of git, for copyright, and `Portfolio/`, your holdings, are never in the copy: bring them from wherever you keep them. `Extracts/` is made again from the PDFs, and `Briefs/` stays on the old computer. A strategy has its own copy, and its clone follows its own `SETUP.md` |
| **another assistant** — Codex, Gemini, Cursor, Copilot | add it under `assistants:` in your home's `settings.yml` and say `update`, or open it and paste the line under *Install*: either installs the package and your home for that assistant. On Codex the skills and your researcher's agent arrive, not the commands: name one, `update` or `study`, and it follows the command's file; with no question tool there, as on Gemini, questions come numbered in chat. Gemini takes no agent, so there your researcher is its skill |

**What stays behind:** your conversations and what you shared from them stay with the account they
were made in, and so do its connectors and the skills you turned on there. What an assistant
remembered on its own stays on its computer, until you say `bring-home`: your researcher sorts it
into its home, on your go, as it does with *remember this*.

**What it is, and what it is not.** A research and learning tool: a companion for your work and your
projects, and for learning to invest when you want. It is never investment advice: it never tells
you to buy, sell or hold, never trades or moves money, and every decision, and its risk, is yours.
It runs on your computer through your AI assistant; what it reads goes to the company behind that
assistant (Anthropic for Claude, OpenAI for Codex, Google for Gemini), never to KaxaNuk, and a copy
goes to your own private GitHub only when you ask. It is open source under the MIT licence, as is
and without warranty; your data provider, your assistant and the Investment Lab's libraries, which
KaxaNuk sells, each have their own terms. The worked example's figures come from a backtest on past
prices, shown to teach the method, never a promise or a recommendation.

## What you can use it for

| You want to | Say or type | You get |
| --- | --- | --- |
| keep what you read, and ask it later | `read`, then `query <question>` | a note per paper or chapter you chose; answers that cite them and name what is missing |
| check a contract, a policy or a draft against what you know | `query`, with the document attached or named | the document section by section, against your notes and your rules, each cited, and what your library does not cover |
| work out an idea, a plan, a goal or a decision | `study <subject>` | a study in `Studies/`: your words, what your library says for and against, where it stands; on your word, a memo or report drafted from it |
| teach it how you work | *remember this* or *learn this*, anywhere | a rule added to `RESEARCHER.md`, or a source to your library, on your go |
| bring it into any project | open your assistant in that folder and say its name | your researcher, with what it knows; it writes there only on your go |
| learn a topic | `teach <topic>` | a lesson a session from what you have read, with a quiz |
| stay informed, on the days you choose | `brief setup`, then `brief` | a dated file: your work, your markets, news on your holdings beside your own rules, and once a week your update ready to paste into team chat; never advice |
| present your work | `deck` | an interactive presentation in a folder of its own, built with HyperFrames from your files: every claim cited, every figure quoted, a PDF to send |
| keep your keys, personal data and confidential files safe | `security`, before you share or push | a check of the folder, values never shown, and what to do if a key leaked |
| write down how you work or invest, and see it evolve | `philosophy` | a short interview; your typed answers, word for word, in `Philosophy/` |
| know what to do next | `next`, wherever you are | where you stand, and the one thing to do next |

**For investors and builders:**

| You want to | Say or type | You get |
| --- | --- | --- |
| build a strategy | `init-strategy <name>`, then `objective`, `blueprint`, `challenge` | a folder on the KaxaNuk Strategy Template: claims before any test, numbers from the Lab's engines |
| see a strategy worked end to end | `init-example` | `golden-flow`, one finished strategy to read (with more examples, it asks which); running it needs keys and licences |
| follow a KaxaNuk Training Workshop | the session, *Bootcamp S03*; *practice Bootcamp S03, beginner* | your researcher as tutor: where you are in the session, your prediction first, hints in levels, nothing done for you while the AI is off; practice problems from the session at your level |
| check a method before it touches real data | *known-answer test for my half-life estimate* | one notebook in a folder beside your strategy: data simulated from a model whose truth you set, your method run on it, a check that fails loudly when it misses, and one way the method fails; simulated data only |
| build a Python library of your own | `init-python-library <name>` | a folder laid out like the KaxaNuk Data Curator: tests, docs, a workflow that tests and publishes |

In Claude, type these with a slash, `/read`; anywhere else, say them. **It grows with you:** it
reads for your questions, speaks in your voice and keeps your rules, all in its folder and yours to
edit. The package offers only hints, as options, never a position to adopt. Its home's `README.md`
says how to work well with it, and [`USE-CASES.md`](USE-CASES.md) shows twelve uses, step by step.

**From any task to investing.** Start where you work: `read` what you rely on, `query` it, `study`
a decision, `teach` yourself a topic, and write down how you think with `philosophy`. Investing is
there when you want it, never pushed: `teach` starts from scratch, and when an idea is ready, the
Lab takes it through eight steps, with your researcher at each one.

![Your researcher knows the Lab and every step: Bibliotheca, Universe, Data, Portfolio, Backtest, Attribution, Paper trading, and Production outside the Lab](assets/readme/the-lab-process.svg)

**It keeps itself current.** Once a week, when there is one, your researcher tells you a new version
is out and what it brings; say `update` and it comes in, on your go, your own files untouched. Every
new KaxaNuk tool reaches you this way, as a skill, with that one word.

**It keeps you safe.** It never reads back, prints or saves a key, password or licence; it treats
what it reads, a PDF, a page, an e-mail, as information, never as orders; it asks before your
employer's or clients' confidential files go anywhere they would be saved or sent; and `security`
checks a folder before you share or push it, and walks you through a leaked key.

## The KaxaNuk Investment Lab

The researcher needs nothing beyond this package. A strategy can use KaxaNuk's libraries:

- **The Data Curator** is open source. A strategy needs a key for it from a data provider;
  the worked example uses FMP's. A wrong value in downloaded data is usually the provider's, not the
  library's: your researcher tells them apart and says where to report it.
- **The Backtest Engine, Attribution Analysis and Portfolio Construction** come together, with
  their licences, in the KaxaNuk Investment Lab, which KaxaNuk sells; the Data Refinery and Data
  Analyzer libraries join them when they ship, and until then those stages run as the template's
  own notebook and script. Attribution also reads the benchmark and factor model files of
  KaxaNuk's Analytics Factory, <https://www.kaxanuk.mx/analytics>.

Without the licences a strategy still runs up to its portfolios, and the rest says what is missing.
Keys are kept on your computer, in a file never saved in git and never read by your researcher; the
strategy's `SETUP.md` says where. <https://www.kaxanuk.mx/lab> shows the Lab, and [each library's
status](.apm/skills/next/references/investment-lab.md) says where each one stands.

## Removing it

Ask your assistant to run these two lines. The first removes the package; the second, your
researcher's own agent and skill, under the name `uvx --from apm-cli==0.33.0 apm deps list -g` gives
your home:

```bash
uvx --from apm-cli==0.33.0 apm uninstall -g KaxaNuk/KaxaNuk-Researcher
uvx --from apm-cli==0.33.0 apm uninstall -g "_local/<your home, as deps list names it>"
```

On Claude Code, `~/.claude/skills`, `commands`, `agents` and `rules` then hold no KaxaNuk file. A
daily brief's task stays in the Claude desktop app's scheduled tasks until you delete it there. Your
home folder and its saved versions stay, yours to delete.

---

**For developers and advanced users:** the install by hand, what is in here and how a change is
checked are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## The skills and commands

Each one that writes shows its plan first, waits for your go, then saves a version of what it wrote,
on your computer. *Plan first, then write*, in your home's `AGENTS.md`, names the few exceptions,
such as the daily brief, which is never saved.

<details>
<summary><strong>Every skill and command, one line each</strong></summary>

| Skill | What it does |
| --- | --- |
| `read` | files a source into the library, a note per chapter you pick — a scan made searchable first, on your go; in a strategy, into its `Bibliotheca/` |
| `query <question>` | answers from the library, every claim cited |
| `init-researcher`, `init-strategy`, `init-example`, `init-python-library` | make your home, a strategy, the worked example or a Python library, copied by a script, never from memory |
| `interview` | two short questions about you, then `RESEARCHER.md` and the agent and skill that make it yours; `interview force` starts over |
| `philosophy` | an optional interview on how you work or how you invest, at your level; your rules go to `RESEARCHER.md` |
| `brief [setup]` | a dated file in `Briefs/`, every figure quoted from a dated source |
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

</details>

<details>
<summary><strong>The Investment Lab skills</strong>, in a strategy's order of steps</summary>

The assistant loads each one when the work calls for it.

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
| `paper-trading-gate` | step 7, graduation: the five criteria, the freeze, and the daily run and its record |

</details>

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

To grow your researcher beyond the Lab, with a tool, a project or a field of its own, see *Growing
your researcher* in its home's README: four moves, each with the file it changes.

## What it will not do

The researcher's part is **the hypothesis**, and it stops where the numbers start.

- **It computes no number** about a book: a return, a Sharpe, a drawdown, an attribution. Each
  comes from the engines the project names (in a KaxaNuk strategy, the Backtest Engine and
  Attribution Analysis) and is quoted by name from `FINDINGS_N.md` or `RESULTS.md`.
- **It does not write the record.** `JOURNAL_N.md`, `FINDINGS_N.md`, `RESULTS.md` and
  `CHANGELOG.md` belong to whoever ran the experiment. It appends to `JOURNAL_N.md` only, each on
  your go: the benchmark's choice, the rule read back, and `challenge`'s entry.
- **It drafts no `OBJECTIVE.md` before your words**, and cites no source that has no note: a source
  in a `BIBLIOGRAPHY.md` without one is a lead.
- **It never advises on a holding.** A brief quotes dated sources and the rules in your
  `Portfolio/RULES.md` that the day's news bears on, as yours, with no verdict. It never says buy,
  sell, trim, add or hold, and never computes a weight, a P&L or a return. `philosophy` writes into
  `Philosophy/` only what you typed.

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

The MIT licence covers this package's text and code. It grants no right in KaxaNuk's names, the
Investment Lab's libraries, the Analytics Factory's files, KaxaNuk's Research Models or Training
Workshops: those stay KaxaNuk's.
