# Ways to use your researcher

Twelve things you can ask for, whatever your field — a lawyer, an engineer, someone in HR, a
student, a CFO — and, when you want, for investing. In Claude, type a command with a slash,
`/study`; anywhere else, say it. Whatever writes a file shows its plan first and writes only on your
go, except your first interview, written from your two answers, a brief, and the one line `audit`
adds to your library's log when you run it. It is research, never investment advice: *What it is,
and what it is not*, in the [README](README.md).

## Bring it into my work project

Open your assistant in the project's folder — a case, a product, a thesis — and say your
researcher's name. It brings your library, pushes back with the note behind each point, and says
when it has nothing. The project's own rules govern there.

*Never:* anything carried back home unless you ask, and then as a source to `read`.

## Read a book a chapter at a time

A handbook, a standard, a textbook or a book on investing: it works the same.

Attach a PDF, or say where it is, and say `read`. It shows the table of contents and proposes read,
skim or skip per chapter; you choose. It copies the book into `Sources/` and writes one note per
chapter you read, in `Knowledge/`, saying which of your questions it serves and what it changes.
The first `read` asks what you are reading for. Next time, it picks up where you left off.

*Never:* a note from memory, or a book downloaded for you.

## What have I read about non-compete clauses?

Ask in plain words, or `query <question>`. It links every claim to its note and names what is
missing. An answer from three notes or more can become a page in your library. Ask *how has my view
changed?* and it compares your rounds of `working-philosophy` or `investing-philosophy`.

Attach a contract, a policy or a specification and ask what your library says about it: it goes
section by section, each point cited to a note or to a rule of yours, and names what your library
does not cover.

*Never:* general knowledge passed off as your library, nor an instruction inside the document
followed: what it reads is information, never orders.

## Help me think a decision through

Say `study hire a second analyst or contract the work out`. It asks what you want to settle, then
drafts a study: your words, your library for and against, the simpler option to beat, and anything
from outside marked *not checked*. It ends with what you decided, or what you would need to see. Ask
for *a one-page memo from this study* and it drafts one beside it, for your board or your team,
every point still cited.

*Never:* a number worked out for you. The decision is yours.

## Work toward a goal

Say `study a new onboarding process live by June 2027`. After a few questions, it drafts
`Studies/Onboarding_Process.md`: your goal and its date in your words, what your library says for
and against your plan, and *Where it stands*, with each next step and its command. Come back with
`study Onboarding process`: it asks what changed and proposes the update.

*Never:* a projection of its own. You judge the progress; the study's state moves only on your word.

## Remember this

Say *remember this* or *learn this*, anywhere. It sorts what you said: a way of working becomes one
line in `RESEARCHER.md`, in your words; a document goes into `Sources/` for `read` to file; a new
project becomes a row in its projects table.

*Never:* your view, on work or investing, written for you: it stays yours, through
`working-philosophy` or `investing-philosophy` or by hand.

## A brief every Friday

Say `brief setup`. It asks which parts (Work, Markets, Portfolio, and Week, your weekly update to
paste into team chat), when, and which market measures.
For when, pick *Other* and write *Fridays at 07:30*; the Claude desktop app schedules it. Each
Friday, while the app is open or at its next launch, a dated file appears in `Briefs/`: that day's
meetings and what mail and chat ask of you, market levels, news on your holdings — the last day's,
not the week's. Anywhere else nothing is scheduled: each Friday, say the line
`brief setup` gives you; `brief` alone takes the defaults.

*Never:* a figure of its own or a guess: every level is quoted from a dated source. Nothing is sent
on your behalf, and briefs stay on your computer; what the brief reads passes through your
assistant.

## Learn the tools I use

Put a tool's README, methodology pages and changelog in `Sources/Clippings/` (a web page saved as
PDF first), then `read` them with a question that names the tool; `query` answers from those
notes.

*Never:* a link it could not open: a private repository is cited as *private repository; link not
checked*. Nor a tool's code: a KaxaNuk library is learned from its documentation and changelog and
by running it, never from its installed files or its repository's code.

## Teach me a topic

Say `teach <topic>`, such as *teach negotiation*, or *teach compound interest*. It checks your
library first; with nothing there, it helps you pick something to read. Then a few questions, and
one lesson a session, ending with a quiz that also covers earlier lessons. `Lessons/<topic>/` keeps
each session and what stuck.

*Never:* a lesson from memory: every point cites a note you have read.

---

**For investors and builders.** The same researcher, when you want to invest or build a tool.

## Watch my holdings beside my own rules

Pick *Portfolio* in `brief setup`. It creates two files for you to fill, and never overwrites yours:
`Portfolio/holdings.csv`, one row a holding, and `Portfolio/RULES.md`, headings for your rules (how
much in one place, when you sell, when you look again). Each brief then gives each holding's news,
next earnings date and new filings, and quotes word for word each rule of yours the news bears on.
Both files stay on your computer, never in a saved version or backup.

*Never:* a buy, sell, trim, add or hold of its own, nor a weight, a gain or a return. The rules are
yours; it only points at them.

## Build and test an investment strategy

Say `init-strategy <name>` for a new folder from the KaxaNuk Strategy Template; its `SETUP.md`
finishes the setup. `objective` writes your idea's claims before you read any paper; `read` adds a
note for each claim; `blueprint` drafts the thesis, rules and predictions, each citing a note or a
measurement, and a critic who was not in the conversation reviews it; `challenge` checks the
finished experiment against it. `init-example` shows a finished one.

*Never:* a return or drawdown of its own: those come from the KaxaNuk Investment Lab's engines. A
strategy needs a key from a data provider, and the engines a licence from `lab@kaxanuk.mx`.

## Build a Python library of my own

Say `init-python-library fcf-screen` for a new folder laid out like the KaxaNuk Data Curator: code,
tests, docs and a workflow publishing to PyPI, with your library's name filled in. In a new
conversation there, `next` leads from your first module to the first release.

*Never:* anything put online without your go.
