---
name: read
description: >
  Load this skill whenever the owner asks to read, file, compile or add a source to the library — a
  PDF, a paper, a clipping — at home from Sources/ into Knowledge/, a file they attach copied in
  first; in a strategy, once OBJECTIVE.md has claims, into a note beside the PDF in Bibliotheca/.
  It extracts a PDF by chapter with a script — a scan made searchable first, on the owner's go —
  asks which chapters serve which question or claim, and writes a note for each chapter read,
  after a plan and the owner's go. It does NOT answer questions from the library (use `query`) or
  rebuild the index (`refresh-index` does).
metadata:
  version: 0.13.0
---

# Read — a source into the library, a chapter at a time

The owner attaches a PDF or a clipping, names one on their computer or drops one into the sources,
and asks to read it, file it, compile it or add it to the library; names a source and the question
or claim it should serve; or asks for a book's table of contents before deciding what to read. What
they said carries the arguments: the strategy's path when the session is not open in it, a path
under the sources or on their computer to read only that, the question or claim by number, and
*outline only* to stop after the table of contents.

Every path below is relative to the researcher's home — the folder that holds `RESEARCHER.md`. Find
it first and read its `RESEARCHER.md` and `AGENTS.md`. In a strategy — the session is open in a
repository with a `Bibliotheca/`, or the owner named one by path — *Working in a strategy* in
`AGENTS.md` says where each of these paths lands.

Turn sources into notes — a paper into one note, a book into one note per chapter that serves one
of the owner's questions, and nothing for a chapter they did not choose — and, at home, into the
wiki: the concept pages those chapters touch, one small page per idea, created and updated as the
sources come in. One convention serves both repositories, so a note has the same shape at home and
in a strategy; it and the concept page are in [`references/note.md`](references/note.md), in this
skill's own folder. **A plan in chat, and the owner's explicit go, before any file is written.**

Three jobs, kept apart. **Extracting** text from a PDF is deterministic and belongs to
`scripts/extract.py` in this skill's folder, never to reading the PDF page by page.
**Choosing** what to read is the owner's, with the table of contents in front of them.
**Reading** the chosen text and writing the note is the researcher's.

## 1. Know what happened recently

Read the last five entries of the library's log, its index end to end, and in `RESEARCHER.md` the
domains, the *Here for* line and *Works for* under *Who*, the tag policy and the owner's open
questions under *What you are reading for*, with the works each one names to *Find first*. In a
strategy the index is `BIBLIOGRAPHY.md` — a row without a note is a lead, not a source — and the
questions are the claims in `OBJECTIVE.md`, by number.

**A home whose `RESEARCHER.md` still holds an angle-bracketed slot** has not been interviewed: with
*Domains* a slot there is no folder for a note, and with the tag policy a slot no tag can be
checked. A section holding only such slots counts as empty. Say so, offer `interview`, and stop.
*What you are reading for* with no numbered question is not a slot: the template ships it so, and
*step 3* asks for question 1.

**A strategy whose `OBJECTIVE.md` has no claims yet** cannot take a note. The objective comes
before any paper — *The order of work* in `AGENTS.md` — because a note is read for a claim, and a
claim written after the reading is shaped by it. Say so, offer `objective`, whose first pass drafts
the claims from the owner's words, and stop. The reading that follows comes in two waves: narrow,
per claim, to fine-tune the objective before the blueprint; broad, after the blueprint.

**A strategy with no `Bibliotheca/BIBLIOGRAPHY.md`** cannot take a note either: there is no row
to add and no convention to follow. Say so, and give the commands that copy it and
`Bibliotheca/LOG.md` from the template inside the KaxaNuk Researcher package, run in the
strategy's root — the script is in the `init-strategy` skill's folder:

```bash
uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" strategy . --only Bibliotheca/BIBLIOGRAPHY.md
uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" strategy . --only Bibliotheca/LOG.md
```

Then stop; the owner runs it, and the read continues from there. Never scaffold `BIBLIOGRAPHY.md` by
hand: it is the template's file, with its parts and its prose.

A strategy whose `README.md` or `AGENTS.md` names another template is never offered `scaffold.py`
to copy KaxaNuk files in: follow that template's own record of what was read, wherever its
`AGENTS.md` says it lives.

A source already read is not read again unless the owner says so. A book begun in an earlier run is
found by its path in the log and by its `INDEX.md` — the status column says which chapters are
read, skimmed, skipped or to come — and this run continues from there.

## 2. List the sources, and extract

List what is in the sources that has no note yet — at home, every subfolder of `Sources/`, where a
`.gitkeep` is never a source; in a strategy, every PDF under `Bibliotheca/Papers/` and `Books/`
with no note beside it, and every clipping under `Notes/` with no note in `Papers/` — or only what
the owner named. The owner may also point at a file under `Sources/` at home for a strategy: it is
read for the strategy, and its note and its extract are written there, nothing at home.
`uv run --no-project python "<this skill's directory>/scripts/unread_sources.py"`, run from the
folder whose library this is, lists the sources with no note: every one no note's `local_copy`
names, by its full path, whatever its name or its date.

**A file the owner attaches or names on their computer is copied in, at home** — a paper into
`Sources/Papers/`, a book into `Sources/Books/`, an article, notes or a page saved as PDF into
`Sources/Clippings/` — under its own file name, never over an existing file. When an attachment has
no path you can read, ask where it is saved — Downloads, usually — and copy it from there. The copy
is part of this read's plan, and one go covers the copy and the read; until then the script runs on
the file where it lies. That copy, and a scan's searchable copy beside it, below, are the only
writes into `Sources/`: a source there is never moved, renamed, edited or deleted.

**At home, with nothing in `Sources/` left to read,** say so, and name the works under *Find first*
in `RESEARCHER.md` that have no file yet — year, authors and title as written there, and the
question each serves — for the owner to find by title and authors, and attach or put in
`Sources/Papers/`, or `Sources/Books/` for a book. With no *Find first* either, and Finance among
the domains in `RESEARCHER.md`, name the ten papers of the two timelines in
`references/reading-map.md`, in this skill's folder, one line each, as leads, matched against
`Sources/` and the index as the map's *Match before proposing* says. With Finance not among the
domains, ask the owner for the works to find, and say that the reading map covers investment
research. Never download one, and write nothing; stop there.

For every PDF among them, run the script — `scripts/extract.py` in this skill's folder, wherever
the harness installed it — from the folder whose library this is, home or the strategy, and read
what it prints:

```bash
uv run "<this skill's directory>/scripts/extract.py" "<pdf>" --outline
```

In a strategy, every run of the script carries `--out Bibliotheca/Extracts`.

Without `uv`: `pip install "pypdf[crypto]"`, then `python` in place of `uv run`; the extra reads
the AES-encrypted PDFs publishers ship. Extracts land in `Extracts/<slug>/` at home and
`Bibliotheca/Extracts/<slug>/` in a strategy — `--out` names the root, the slug is the PDF's name
without `.pdf`, its ASCII words joined by underscores, and the script's *extracts in* line names
the folder — one markdown file per chapter, a marker before every page, with `OUTLINE.md` beside
them listing every chapter the run knows of, written or not. They are a cache: regenerable, kept on
this computer only, never cited. If the strategy's `.gitignore` does not keep out
`Bibliotheca/Extracts/`, say so in the plan, which adds that one line to it on the same go.

- **A PDF with no outline.** The script says so and gives the page count. Read the pages that carry
  the table of contents — the first ten to fifteen, through the assistant's PDF reader, or, where
  it cannot show them, as it cannot on Windows without Poppler's `pdftoppm`, as images:
  `uv run "<this skill's directory>/scripts/render_pages.py" "<pdf>" 1-15 --dpi 100` — and
  propose a split of the whole book by page ranges, every chapter in order, for the owner to
  confirm when the table of contents is shown. `--split` takes PDF pages and a table of contents
  gives printed ones: add the offset, checked against one printed page. Every run after that
  passes that same whole `--split`, with `--chapters` for what the owner chose, so each chapter
  keeps its number; the book's `INDEX.md` keeps the pages. A paper is one chapter: `--all`.
- **A PDF whose depth 1 is parts.** The script says so; run `--outline --depth 2`, and carry
  `--depth 2` into the run that extracts the chapters: without it, `--chapters` counts parts.
- **A PDF with no text layer** — a scan. The script writes no chapter and says why. Offer a
  searchable copy, through the question tool, header `Scan` (`Escaneo`): *Make a searchable copy*
  (*its text read off each page by OCR, on this computer — a few seconds a page*), *Leave it
  unread*; in chat where there is no such tool. On the go, run, in the background for a book,
  `uv run "<this skill's directory>/scripts/ocr_pdf.py" "<pdf>"`: it writes `<its name> (OCR).pdf`
  beside the scan, never over a file, and leaves the scan as it was — in a strategy, beside it in
  `Bibliotheca/`. The copy is then extracted and read like any PDF, and the note's `local_copy`
  names it. OCR runs words together and misreads a digit or a sign: read the copy's extract for
  that before a note is planned on it, and take a figure, a name or a formula from it only as the
  page's image shows it — *Page images*, in *step 4*. Without the go, report the source as
  unreadable, leave it out of the plan, and do not fill it in from memory. A chapter reported *not
  written* while others were written is scanned pages the same way: the offer is a copy with
  `--pages` for those pages, from which every chapter is then extracted, and the plan says so. One
  reported *thin* was written with few characters a page — a preface, plates, a page of figures —
  and is checked for prose before a note is planned on it.
- **A source that is not a PDF** — a markdown clipping, a transcript — is read directly, whole.

**Exit 1 is a mistake in the command, not in the source** — a chapter number the outline does not
have, a `--split` item the script cannot read or with pages outside the PDF, `--split` with
`--outline`, a path that is not a file or not a PDF, `--engine pdftotext` with no `pdftotext` on the
PATH. Fix the command and run it again; never report the source unreadable for it.

## 3. Show the table of contents, and ask

One message per book: the chapters as the script numbered them, with their pages, and beside each
a proposal — **read**, **skim** or **skip** — and the question it would serve, by its number under
*What you are reading for* — in a strategy, the claim's number in `OBJECTIVE.md` — judged from the
titles and the owner's questions. A paper is one line: read whole, and which question. Then ask
through the question tool: *Take the proposal as it stands*; *Change some chapters*, and they say
which in chat — *read 3, 4 and 7 for Q2, skim 5, skip the rest*; *Read everything*; *Outline only*.
Where there is no such tool, ask for the one line in chat. Do not ask about a source whose question
came with the command or was given earlier in the session. Three answers are always open: a
question the list does not have yet, which the plan offers to add to `RESEARCHER.md` in the
owner's words; *the other side of question N*; and *background reading, no question in mind*,
recorded as such.

**At home with no numbered question yet, ask which question this source serves, first,** in plain
words: *what do you want this reading to help you answer?* Ask it through the question tool, header
`Reading for` (`Leer para`), single-select: three proposals, then *Background reading, no question
in mind*, with *Other* for their own words. One proposal comes from the source itself, its title and
table of contents; the others from the *Here for* line and *Works for* under *Who* in
`RESEARCHER.md`, or *Works for* alone where there is no *Here for*. With *Here for* *Learn the
basics, step by step*, or the voice *Explain as you go*, every proposal is in everyday words — *can
anyone do better than the market, year after year?*, *why do people make the same money mistakes?* —
and never *edge*, *factor* or *alpha*; with *Build and test a strategy*, one may come from the
reading map's *Questions to read for, from the evidence*; with *Write down how I invest, and see it
evolve*, one asks about the owner's own way of investing; with *Organise what I read, and help with
my projects* — or the older *Organise what I read* — they follow the source's own subject and the
projects *Works for* names. A proposal drawn from an investing pick is offered only when the source
is about money or markets; for any other source, the proposals follow the source and *Works for*, in
everyday words when *Learn the basics* is picked or the voice is *Explain as you go*. The question
the owner picks or types is theirs: the plan offers to add it as question 1 under *What you are
reading for*, in their words — with the copy of *step 2*, the only write this skill makes outside
the library and the extracts, at home only, said in the plan. Then the table of contents is shown
against it, as above. In a strategy, a question the claims do not cover is a claim to add with
`objective` before the reading, and *background reading* is a home answer: in a strategy every note
serves a claim.

Never write a question or a reason the owner did not pick or confirm. Proposing candidates for
them to choose is how the reading keeps moving; writing one they did not choose is not. If the
owner would rather not say, the note simply has no `## Why it is here`. Stop here if the owner
asked for the outline only.

With the owner's choice in hand, extract what they chose — `--chapters 3,4,5,7`, skims included,
at the `--depth` the outline was shown at, after the whole `--split` for a PDF with no outline, and
`--out Bibliotheca/Extracts` in a strategy — and nothing more.

## 4. Read what was chosen, and decide

Read each chosen extract in full — the extract, not the PDF. Where the assistant can delegate, give
each chapter to one delegate with the extract, the question and `references/note.md`, and collect
the drafts, staged outside the library, in the system's temporary folder, never in it: each draft
is checked before the plan — `uv run "<this skill's directory>/scripts/check_numbers.py"` on it,
with the library's extracts, and its claims read against the extract wherever the extract is thin,
garbled or from an OCR copy — and one that fails is read again from the extract. Otherwise read one
chapter at a time. A skimmed chapter is read for one line: what it holds, and why it was passed
over.

**Page images.** A table, an equation or a figure the extract dropped or garbled, and any figure,
name or formula from an OCR copy, is read from its page's image:
`uv run "<this skill's directory>/scripts/render_pages.py" "<pdf>" <page> --dpi 200`, `--region`
for a part of it, writes the image outside the library and prints its path, for the assistant's
image reader. The note cites the page as any other, and its provenance line says which pages came
from an image, as `references/note.md` gives. Nothing on an image the assistant cannot make out is
guessed: it is quoted as unclear, with its page.

For each note, decide:

- **Where it goes.** At home, the domain folder; in a strategy, `Papers/` or `Books/`. For a
  chapter, the book's folder.
- **What the citation is.** `source` and `citation` come from the source itself — its title page,
  its header, its DOI — or from its row in `BIBLIOGRAPHY.md`; never from memory, and never from
  `references/reading-map.md`, whose years and titles are there to find a work, not to cite it. A
  URL nobody has checked is not written.
- **Whether the home library has read it already.** In a strategy, when `Knowledge/` at home holds
  a note on the source, the source's part travels — the claim headings and their bullets, in the
  source's terms — and only what is the strategy's is written anew: `## Why it is here` against the
  claim, every implication blockquote, `## What it changes`. Say so in the plan. Nothing links back
  home, and the PDF is not read twice.
- **What it links to.** The existing notes it relates to, by relative path, in the same repository.
- **Which concept pages it touches.** At home only: the ideas the chapter argues in the service of
  one of the owner's questions, or that a page already covers — an existing page to update, a new
  one to create, never a page for a passing mention. Three to eight per chapter is usual. Each
  claim a page takes from the chapter cites the chapter note and its page; a claim that contradicts
  what a page holds is kept beside the old one under a `> [!WARNING]` callout naming both notes.
- **What it contradicts or supersedes.** Any claim in an existing note that the chapter conflicts
  with, quoted.
- **What the owner believes about it.** Any file in `Philosophy/` on the same subject — at home,
  to be cited from the note; in a strategy, named in prose — never compiled into it, and never a
  round file in `Philosophy/Evolution/`, a record, as the home's `AGENTS.md` says.

What you remember of a well-known book is not the book: nothing is written from memory, and nothing
from a summary.

## 5. Present the plan

In chat: for each source, its copy into `Sources/` when it came from outside, the notes it becomes
— target paths, each with the question or claim it serves, by number — and, for a book, what its
`INDEX.md` will record for the chapters skimmed and skipped; in a strategy, the row each note adds
to `BIBLIOGRAPHY.md` or the lead it replaces, under the part it bears on; at home, the concept pages
it creates and the ones it updates, one line each; links; `Philosophy/` files to cite, never a
round file in `Philosophy/Evolution/`; contradictions found; new domain folders at home, if any;
questions to add to `RESEARCHER.md` at home, if any, in the owner's words; and the log line. A
clipping in markdown or plain text is saved with its note, as a PDF or an extract never is, so the
plan says so, beside the note it becomes. Then ask for the go through the question tool — *Go*,
described as *write it and save a version* (*escribirlo y guardar una versión*), *Change something*,
*Stop* — or in chat where there is none; any of the go words in the home's `AGENTS.md` is the go.
**On *Change something*, ask again with options, never with an open question**: the changes this
plan admits, as concrete alternatives — fewer notes or pages, different names, only the notes this
run, a different domain — and ask for the go again on the revised plan.
**Never write on silence or on a rejection.**

## 6. Write, on approval only

- At home, the copy into `Sources/` first, when the plan has one, as *step 2* says.
- The notes, in the shape `references/note.md` gives and under its names: its frontmatter, `tags`
  where the owner's policy asks; the provenance line; `## Why it is here` with the question or
  claim by number and the owner's reason in their words; the claims as headings, a blockquote under
  each; `## What it changes` last. For a book, its `INDEX.md` with every chapter's status.
- At home, the concept pages, in the shape `references/note.md` gives and as *step 4* decided,
  their `## For the owner's questions` and `## Open` brought up to date: a new page written whole,
  an existing one through `scripts/update_concept_pages.py` in this skill's folder — a spec of
  what each page gains, on standard input, run without `--write` to check its diff against the
  plan, then with it. `--help` gives the spec. In a strategy, none:
  `OBJECTIVE.md` is its synthesis.
- For every contradiction the owner confirmed: keep the original claim in the older note and place
  a `> [!WARNING]` callout above it naming the newer note by link. Never delete the claim.
- At home, when the plan added questions: write them under *What you are reading for* in
  `RESEARCHER.md`, in the owner's words, numbered after the ones already there — the first one in a
  section with none is question 1, in place of the template's *None yet.* paragraph, in whatever
  language it is written — each followed by *feeds: nothing yet* and *Would change my mind: not yet
  known*, the labels a question carries there, for the owner to fill by hand. Nothing else in that
  file changes.
- The index. At home, `Knowledge/INDEX.md`, under the domain, as *What the indexes show* in
  `references/note.md` gives it: *Concepts* first, then *Sources*.
  In a strategy, `BIBLIOGRAPHY.md`: the note's row under the part it bears on — replacing the
  *No note yet* of a lead, or added where the source was not listed — and nothing else in that
  file: its parts and its prose are the owner's.
- One entry appended to the library's log — `Knowledge/LOG.md` at home, `Bibliotheca/LOG.md` in a
  strategy, and only if the file exists — in the format `AGENTS.md` gives: `read`, the notes and
  concept pages written and updated, the flags, and for a book a `read:` line naming the chapters
  read, skimmed, skipped and to come.

## 7. Report

In chat: what was written, updated and flagged; any gap the source exposed — a concept the library
leans on with no source behind it — as a suggestion for the sources, naming the work the reading map
gives as this one's other side when it names one, as a lead; whether the source changes a belief in
the owner's file in `Philosophy/` — `HOW-I-WORK.md` or `HOW-I-INVEST.md` — as a question for the
owner to answer there in their words, by hand or in a round of `working-philosophy` or
`investing-philosophy`; and, at home, the strategy a note could serve, with the `read <strategy>
<source>` that would carry it there, and a study in `Studies/`, still *idea* or *active*, that the
note bears on, with the `study <its name>` that would revise it.

At home, where *Domains* holds Finance or *Here for* holds *Learn the basics*, *Build and test a
strategy* or *Write down how I invest*, one more line: **the investing questions of the owner's
philosophy the new note bears on.** Match the note's work, by its authors' surnames as the reading
map's *Match before proposing* says, against the *Bears on* table of `references/questions.md` in
the `investing-philosophy` skill's folder, and name each question it lists by its ID and its
*Short*. With a round of it in `Philosophy/Evolution/` — a level, not `Work` or `Field`, on its
first line — the line gives the last such round's date and offers the next round with
`investing-philosophy`; with none, it offers round 1. A work the table does not list, or a table
that cannot be read because the skill is not installed, gets no line.

**Then save a version**, on the plan's go, with no second question, in the folder whose library
this is — every git command, the `backup` skill's send included, as `git -C "<that folder>"` when
the session is open elsewhere: `git add` each file this run wrote — with the text clipping a note
was read from — by name, never `--all`, never an extract or a PDF, leaving out any path the folder's
`.gitignore` keeps out, and `git commit -m "Read: <Author Year, short title>" -- <the same files>`.
Say it in one plain line, *Saved*, never the commands. When `git config --get kaxanuk.autosend`
prints `true`, the version is also sent to the owner's copy on GitHub, as the `backup` skill says.
This replaces the *Commit?* question, and in a strategy the owner's own commit, that an older home's
`AGENTS.md` describes. A save refused for want of a name asks in one open message, with no options,
*What's your name, or what would you like me to call you?*, never invented, and no e-mail; it sets
it in that folder only, with `user.email` as `"<>"`, an empty address, and saves again; a folder
with no `.git/` gets one line, that it keeps no versions yet. In a strategy the version takes no
`CHANGELOG.md` entry, version bump or ruff gate: the next change-set's entry names it.

## What this skill will not let you do

- Read a PDF page by page when the script can extract it. The exceptions are the table-of-contents
  pages of a PDF with no outline, and the image of a page whose table, equation or figure the
  extract dropped, or whose OCR text may be wrong — *Page images*, in *step 4*.
- Write to the sources beyond the copy and the searchable copy *step 2* makes, or to
  `Philosophy/`, `Studies/` or `Lessons/`. Only the script writes the extracts.
- Write at home while reading in a strategy — no note, no index line, no log entry, no question in
  `RESEARCHER.md`, no extract. A strategy's source enters the home library only when it is copied
  into `Sources/` at home, on the owner's go, and read there.
- Write into a strategy's `Bibliotheca/Knowledge/`. Its notes live beside its sources, and
  `BIBLIOGRAPHY.md` is its index.
- Rewrite `BIBLIOGRAPHY.md` beyond the row a note adds or replaces.
- Carry a home note's blockquotes into a strategy. The source's words travel; the implications are
  written for the strategy's claims.
- Write a note for a chapter the owner did not choose, or a question or a reason they did not give.
- Cite an extract. Notes cite the source and its pages; extracts are regenerated.
- Cite a PDF or an extract from a concept page, or build one from memory. A concept page cites
  notes and their pages; notes cite sources.
- Create a concept page for a passing mention, or one in a strategy — `OBJECTIVE.md` is the
  strategy's synthesis.
- Read a source you could not open, or fill one in from memory or from a summary.
- Enter a paper's figure into a note as though it were the strategy's. A number in a source is the
  source's, and the note says whose it is; a figure about the strategy is quoted only from the file
  that owns it, as *Numbers* in the `query` skill says.
- Write a plan or a report as a file. The chat and the log entry are the record.
- Rewrite an existing note in a different voice. Match what is there.

## References

- `scripts/extract.py`, in this skill's folder: the PDF's table of contents, and its chapters as
  text, one file per chapter. `--help` has every option.
- `scripts/check_numbers.py`, in this skill's folder: each figure a note states beside a page
  citation, looked up in the extract on the cited page, elsewhere, or nowhere; `audit deep` runs it,
  and it edits nothing. `--help` has every option.
- `scripts/ocr_pdf.py`: a scan's searchable copy, `<its name> (OCR).pdf`, beside it, its text read
  by an OCR engine on this computer and laid over each page as invisible text. *Step 2*.
- `scripts/render_pages.py`: a PDF's pages, or a part of one, as images outside the library, for
  the contents pages a reader cannot show and for *Page images* in *step 4*.
- `scripts/unread_sources.py`: every source no note's `local_copy` names, by its full path. *Step
  2*, and `next`.
- `scripts/update_concept_pages.py`: existing concept pages brought up to date from a spec, its
  diff shown before `--write`. *Step 6*.
- `scripts/check_library.py`: the checks `audit` makes on every run; it and the two before it share
  `scripts/library.py`. Every script here needs only `uv`; `--help` has each one's options.
- `references/note.md`, in this skill's folder: the shape of every note, book index, index line,
  concept page and synthesis page, and how a home note travels into a strategy.
- `references/reading-map.md`, in this skill's folder: the evolution of investment research and
  where alpha comes from — the ten papers of the two timelines, where each belief sits and its
  other side, the arc's 21 questions and their works, and hints. The one list a work to read may be
  proposed from besides the owner's library; a work in it is a lead, never a citation.
- `references/questions.md`, in the **`investing-philosophy` skill's** folder, not this one: its
  *Bears on* table, which works touch which of the owner's philosophy questions, read on demand for
  the one line in *step 7*. It is that skill's file; this skill reads it and never copies it.
