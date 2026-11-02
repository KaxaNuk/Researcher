---
name: working-philosophy
description: >
  The first interview after `interview`, for everyone — investors included: five short, open
  questions that tell the owner's story at work — how they got here, what changed them, what they
  believe, how they decide, what would change their mind — then the rules the researcher keeps
  with them; their typed answers added word for word, each behind its short question, to
  Philosophy/HOW-I-WORK.md, with a round file in Philosophy/Evolution/, and their rules under
  Non-negotiables in RESEARCHER.md; retaken after reading, it shows how their view moved. About ten
  minutes. Plan first, the owner's go, then write, at home only. Only when the owner runs it by
  name, or picks it where another skill offers it. It does NOT ask how they invest
  (`investing-philosophy` does, second), edit what the file holds (`refine` does), or write
  RESEARCHER.md beyond Find first and those rules, and never says buy, sell, trim, add or hold.
metadata:
  version: 2.0.1
---

# Working philosophy — how the owner works, in their own words, round by round

**When it applies.** The owner runs `working-philosophy` by name, or picks it where another skill
offers it — `interview`'s hand-over, `next`, the close of a `teach` lesson or a `study`. It is
**the first interview after `interview`, for everyone**: a lawyer, a teacher, a CFO, a portfolio
manager. How someone works comes before how they invest, and the rules the researcher keeps with
them are settled here. An owner who invests, or wants to learn, takes `investing-philosophy` after
it, as the second. It is not a test — no score, no wrong answer. It never judges an answer, never
proposes what to do, and never says buy, sell, trim, add or hold. For what the library says, use
`query`; for a lesson on an idea, `teach`.

**What it writes, and only on the owner's go.** The owner's typed answers, added word for word and
add-only to `Philosophy/HOW-I-WORK.md` — started with its title and headings when missing — and one
round file in `Philosophy/Evolution/`. This skill, `investing-philosophy` and `refine` are
`Philosophy/`'s writers, as the home's `AGENTS.md` says. Beyond `Philosophy/`, two places in
`RESEARCHER.md`: the rules settled in O4 under *Non-negotiables*, in plain words; and a work typed
in C2 on the closing *Find first* line. Nothing else, anywhere. The same go saves a version.

**Only typed words reach `Philosophy/`, each behind its question.** Every typed answer is written
as `- **<Short>** <their words> *(round N)*`: the card's *Short*, the question in at most eight
words in the owner's language, in bold, so the line makes sense a year later; then their words,
exactly as typed. The *Short* is a label, never the owner's view. Nothing the owner picks, and no
other line the researcher says, reaches `Philosophy/`, round files included. The owner's view is
cited from `HOW-I-WORK.md`, never from a round file.

**The bank.** [`references/questions.md`](references/questions.md), in this skill's folder: the
opening, the five questions in the order they are asked, each with its *Short*, *Why*, plain line,
examples and the one idea it teaches, the rules, where each answer lands and how a retake runs.
Read it whole before the first question. It is written in English and said in the owner's
language — the one *How it speaks* names — as written, in words that never mark the owner's gender,
and never improvised. IDs are stable; a retake compares by ID. No work from the reading map is
named: it is about markets, and this round is about the owner's work.

**How to ask.** Open questions are asked in chat, one per message, each opening with where the round
stands and its *Why*, and inviting a story; a *Then* is asked in a message of its own once the *Ask*
has a typed answer. An *Ask* and a *Then* are said as the bank writes them, open: never turned into
a yes-or-no, and never into a guess from earlier answers for the owner to confirm. A pick is asked
by **calling the question tool** — `AskUserQuestion` in Claude Code — at most four options, with
*Other* as the free-text escape. **Without one** — Codex — a pick is asked in chat, its options
numbered, *Other — your own words* last. Wait for each answer.

**A round at a glance.** About ten minutes, in one go, and it can stop at any point.

| # | Step | How |
| --- | --- | --- |
| 1 | pre-flight: the home, what the owner has said and read | nothing asked |
| 2 | the opening in round 1, or a retake's opening and its scope | said, then one tool question |
| 3 | the story: W1, W3, W2, W4, W5 | chat |
| 4 | your rules (O4), in round 1 or while you have none | one tool question |
| 5 | what to read next (C2) | one tool question |
| 6 | on a retake, then and now | chat, never written |
| 7 | the preview, and the go | said, then one tool question |
| 8 | write, and save a version | on the go only |
| 9 | hand over | said |

## 1. Pre-flight, asking nothing

1. **Find the home**, the folder that holds `RESEARCHER.md`; every path below is relative to it.
   Handed over by `interview` in the same conversation, it is the absolute path `interview` names.
   In a strategy or another project, find it through the researcher's skill, whose description
   names the home by path; the preview will open with *this writes to the researcher's home, not to
   this project*. If the home cannot be read from this session, say so, name the fix — add the
   home's folder to the session, or open the assistant there — and stop.
2. **Read `RESEARCHER.md` and `AGENTS.md`.**
   - A `RESEARCHER.md` with an angle-bracketed slot left under *Who* or *How it speaks* has not
     been interviewed: say so, offer `interview`, and stop.
   - An `AGENTS.md` whose `Philosophy/` row names neither `working-philosophy` nor `philosophy`
     (its name before 1.31.0) among its writers, or names no `HOW-I-WORK.md`, predates these
     interviews, and the home's own rules do not let it write: say so, offer `update`, which shows
     the new row as a diff to accept, and stop. A row that names `philosophy` only is an older
     home: the round runs, and the hand-over offers `update`.
   - An `AGENTS.md` that names no skill among the writes to `RESEARCHER.md`'s *Non-negotiables*
     predates the rules: the round runs without O4, the opening's mention of rules included, and
     the hand-over offers `update`.
   - Take the language and the voice from *How it speaks* — with none, the language of this
     conversation — and, under *Who*, the *Works for:* line, what the owner does, which titles a
     new `HOW-I-WORK.md`, and the *Here for:* line. Take the bullets under *Non-negotiables*, one
     rule each; *None yet.*, in any language, says there is none.
3. **Read what the owner has already said.** `Philosophy/HOW-I-WORK.md` whole when it is there.
   Then `Philosophy/Evolution/`: **this skill's rounds are the files whose first line ends in
   `Work`**, or in `Field`, as an earlier version wrote them; a file with a level there is
   `investing-philosophy`'s, and is left alone. With none of its rounds, this is round 1. Otherwise
   it is a retake: the latest round is the newest of them — the latest date in the file names, and
   on that date the highest suffix — and its first line gives its number *N*, so this round is
   *N* + 1. From those files, gather each ID's latest typed answer, its round and its latest status,
   and the IDs no round has a line for — O4 and C2 aside. A file whose first line is not a round
   line is no round: ignore it, and name it once.
4. **Read what the owner has read.** On a retake, the `read` entries of `Knowledge/LOG.md` dated on
   or after the last round's date, and the notes they list. For C2, `Knowledge/INDEX.md` and the
   files in `Sources/` with no note yet.

## 2. The opening

**Round 1.** Say the bank's *Before the first question*, then ask `Ready?` (`¿Comenzamos?`) —
*Start*, *Not now*. **A retake.** Say the bank's opening of *Taking it again*, then ask its scope
question, `Retake?` (`¿Repetir?`); *not now* or *stop* under *Other* is *Not now*.

On *Not now*, write nothing, and say in one line how to start later: *say `working-philosophy`
whenever you like — a new session is best.*

## 3. The story

**W1, W3, W2, W4, W5**, in that order, one per message, in chat: the round's place — *question 2 of
5 · about 8 minutes left* — its *Why*, its *Ask*, and the bank's closing line, which welcomes a
story. A *Then* follows in a message of its own once the *Ask* has a typed answer, and joins it as
one answer. After every answer — *not sure yet* and *skip* included — the question's *Teaches* line,
as written: one idea, never a verdict. W5 quotes the line the owner typed for W2; with none, it asks
about any belief on their work they would like to test. On a retake, **Presses on**: quote the
owner's own line in `HOW-I-WORK.md` that the question tests, if one clearly does; never guess one.
The escapes hold on every question — *Escapes and exits* below.

## 4. Your rules

**O4**, one tool question, `Your rules` (`Tus reglas`), as the bank gives it: in round 1, after
W5; on a retake, after W5 while *Non-negotiables* holds no rule, and otherwise only on *my rules*,
at any point. Never in a home whose `AGENTS.md` predates it, *step 1*. It shows two rules many
people start with, a plain line each, and two for testing a strategy — shown with them when *Here
for* holds *Build and test a strategy*, else offered when the owner asks. A home that already holds
some keeps its own first. A rule of the owner's own, or a change, is one line in chat after, in
their words. What it settles is written on the go under *Non-negotiables* in `RESEARCHER.md`, never
in `Philosophy/` or the round file; a rule already there stays unless the owner changes or drops it
here. A rule about holdings — how much in one place, when to sell, when to look again — is not
written there: say in one line that it belongs in `Portfolio/RULES.md`, the file `brief` quotes,
which `brief setup` starts and the owner writes. This skill never writes in `Portfolio/`.

## 5. What to read next

**C2**, `Read next` (`Aprender`), single-select, as the bank gives it: up to two files *in your
Sources/, not yet read*; `teach` on a topic the owner's notes cover, or *Learn one idea with me —
after your first reading*; *Not now*; and *Other* for a work of their own, which goes on the closing
*Find first* line, in their words, unless the preview leaves that line alone. No work from the
reading map is offered, and nothing from C2 reaches `Philosophy/`.

## 6. A retake: what moved

On a retake only, before the preview: the bank's comparison, in chat, never written to a file — a
line of counts, a table by ID and *Short* of then and now, and the notes read between the two
rounds, named once, as reading in between, never as the cause. With *Just show me what changed*,
this is the whole run, and nothing is written.

## 7. The preview, and the go

Show in chat, before anything is written:

- **From a strategy or another project**, first: *this writes to the researcher's home, not to
  this project.*
- **`Philosophy/HOW-I-WORK.md`**: a file to be started, first, `# How I work — <what *Works for*
  says they do, in their words>` and its five headings, marked *new file*. Under each heading,
  every line to be added, as it will read — `- **<Short>** <their words> *(round N)*`. On a retake,
  under each changed answer, the old line, quoted and marked *stays — I only add*.
- **A standing line a new answer clearly cuts against**, quoted once: *both will stand; edit it by
  hand, or run `refine`, if one no longer holds.*
- **The round file**, whole, under its path.
- **`RESEARCHER.md`**: the rules O4 settled, named *your rules*, never by the heading's English
  name, each line as it will read — a rule O4 changes or drops quoted and marked *changes* or
  *goes*; a rule about holdings shown apart, marked *yours to write in `Portfolio/RULES.md`*; and a
  work for *Find first*, or *left alone*.
- **Privacy**, one line: these lines are saved in your researcher's versions; leave out any you
  would rather not keep.
- **Spelling and language**, one line, when the typed lines hold typos or another language than
  *How it speaks*: they go in exactly as typed, and `refine` can clean them right after, each line
  shown as a diff first; the round file keeps them as typed.

Then ask `Go?` (`¿Escribo?`) — *Go*, described as *write it and save a version*, *Change
something*, *Stop*; in chat, any of the go words in the home's `AGENTS.md` is the go. **A round with
no typed answer** says *nothing typed, so nothing goes into `HOW-I-WORK.md`*, and asks `Keep it?`
(`¿Lo guardo?`) — *Keep this round as a record*, with its rules, *Change something*, *Write
nothing*.

**On *Change something*, ask again with options**: *Leave out a line*, a rule's included; *Reword
in my words* — they type the line again, and only their words are written; *Leave Find first
alone*; and, on a retake with a changed answer, *Leave my old line — I'll fix it with `refine`*.
Then show the revised preview and ask for the go again.

**On *Stop*, *Write nothing*, silence or a closed session, nothing is written**, and the next run
starts as this one did.

## 8. Write, on the go only

1. **`Philosophy/HOW-I-WORK.md`, add-only.**
   - **A file `Philosophy/` lacks** is created first, with `# How I work — <what they do, in their
     words>` — never their name — and the five headings of the bank's *Where each answer lands*,
     in its order, in the owner's language, and nothing else. A home keeps one `HOW-I-WORK.md`; an
     existing one keeps its title, which is the owner's to change by hand.
   - One bullet per typed answer, `- **<Short>** <their words> *(round N)*`, under the heading
     *Lands under* names, at the end of that heading's lines. An answer of several lines keeps
     them, indented under its bullet.
   - **Headings are matched by name or position**: by the English name; else by a heading in the
     owner's language that says the same; else, in a file holding the bank's five headings in that
     order, by position. A heading matched is never added again; a heading an existing file lacks
     is added at the end, in the language its other headings use.
   - A line identical to one already under its heading is not added again, and *keep* adds
     nothing. Nothing the owner wrote is edited, moved or deleted — lines an earlier round wrote
     with no *Short* in front included.
2. **`Philosophy/Evolution/YYYY-MM-DD.md`**, today's date — `-2`, `-3` for a second or third round
   the same day of either interview, the folder created when missing. Written once and never
   edited afterwards:

   ```markdown
   # Round <N> · <YYYY-MM-DD> · Work

   - W1 · <the owner's words, word for word>
   - W3 · not sure yet
   - W2 · skipped
   ```

   - **One line per question asked**, in the order asked: `- <ID> · <answer>`, the owner's typed
     words or a status — *not sure yet*, *skipped* or *explained*; an answer of several lines keeps
     them, indented under its bullet. O4 and C2 take no line. No *Short* goes here.
   - **On a retake**, a label follows the ID — *kept*, with no answer; *changed*; *new*; *still
     open*. A question answered before and skipped now takes no label, only its status.
   - **In English**: *Round*, `Work`, the IDs, the labels and the statuses, because skills parse
     them; the answers are in the owner's language.
3. **`RESEARCHER.md`**, in two places, and nothing else in that file changes:
   - **Non-negotiables**, only when O4 settled rules: one bullet per rule, `- <rule>`, in the
     owner's language — a rule from the bank translated, its meaning unchanged and the researcher's
     name for its *my*; one of their own in their words — in place of the *None yet.* paragraph
     while it is there, else after the section's last bullet. A rule held there in any words is not
     added again; one is changed or removed only as *Change or drop one* named it. Never a
     strategy's term the owner did not use, and never a rule about holdings.
   - **Find first**, only for a work typed under *Other* in C2, in the owner's words, appended to
     the closing *Find first* line in place of *none*, or as a new last line before *Out of scope
     for now*. A file already in `Sources/` never goes there.

**Then save a version**, in the home, on the go that wrote, with no second question. Every git
command runs as `git -C "<absolute path to the home>"` when the session is open elsewhere. `git add`
each file this run wrote, by name, never `--all`, and `git commit -m "Philosophy: round <N>, work"
-- <the same files>`. Say it in one plain line, *Saved*, never the commands. When `git config --get
kaxanuk.autosend` prints `true`, the version is also sent to the owner's copy on GitHub, as the
`backup` skill says. A save refused for want of a name asks in one open message, *What's your name,
or what would you like me to call you?*, never invented, and no e-mail; it sets it in the home only,
with `user.email` as `"<>"`, and saves again. A home with no `.git/` gets one line, that it keeps no
versions yet.

## 9. Hand over

Short, in the owner's language and voice, in this order:

1. **What moved.** On a retake, the comparison's line of counts; on round 1, *round 1 written*, how
   many lines went into `HOW-I-WORK.md`, and how many of *your rules* went into `RESEARCHER.md`.
2. **What next**, one line, by *Here for* and *Domains*:
   - *Learn the basics*, *Write down how I invest*, *Build and test a strategy*, or Finance among
     the domains, and no investing round yet: *`investing-philosophy`, the second interview — why
     you invest, for whom and what you measure against, at your level — in a new session.*
   - Otherwise: the first source to `read`, or the C2 pick — a `teach <topic>`, or a file in
     `Sources/` to `read`.
3. **When to come back.** *Once you have read a source or two, `working-philosophy` again, in a new
   session; what was left open waits there.*
4. **`refine Philosophy/HOW-I-WORK.md`**, when *Leave my old line* was picked, or the preview's
   *Spelling and language* line was shown — diff first.
5. **`update`**, when O4 was left out, or the home's `AGENTS.md` names only `philosophy`, *step 1*.
6. **`brief setup`**, when a rule about holdings was pointed to `Portfolio/RULES.md`.

## Escapes and exits

The bank's escape table holds on every question, at any time, in the owner's language too —
*explica*, *ejemplo*, *no sé todavía*, *salta*, *para*, *igual*, *mis reglas* — and their usual
words in any other. A message that is only an escape is that escape, and writes nothing; a message
with more is a typed answer, written as typed. When it could be either, ask once: *write that as
your answer, or mark it not sure yet?* A number, or *that one*, after an example is a pick, not
typed words: ask for their own words, or a skip.

## What this skill will not let you do

- Write a pick, an example, a *Teaches* line or a status into `HOW-I-WORK.md`, start it with more
  than its title and headings, or write anything the researcher said into a round file — the
  *Short* in front of an answer is the only line of the bank that reaches `HOW-I-WORK.md`.
- Write in `HOW-I-INVEST.md`, which is `investing-philosophy`'s, or touch a round file that is not
  this skill's.
- Edit, move or delete a line already in the file — that is `refine`'s, or the owner's by hand — or
  touch a round file once written.
- Write in `RESEARCHER.md` anything but the rules O4 settles under *Non-negotiables* and a work
  typed in C2 on *Find first*, or change or drop a rule there the owner did not name.
- Write in `Portfolio/`, or put a rule about holdings under *Non-negotiables*.
- Name a work from the reading map, or from memory.
- Cite a round file as the owner's view, or as evidence of anything.
- Write, or save a version, on a *Stop*, on silence or on a closed session, or write at home from a
  strategy or another project without saying so first in the preview.

## References

- [`references/questions.md`](references/questions.md), in this skill's folder: the bank — the
  five questions, the rules, where each answer lands and how a retake runs.
