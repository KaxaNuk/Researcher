---
name: investing-philosophy
description: >
  The second interview, for an owner who invests or wants to learn: why they invest and for whom,
  their best and worst money decision, what they measure against and how they react to a fall,
  then — at their level — where their edge is, how they split money and how they would prove it,
  one plain idea taught after each answer; their typed answers added word for word, each behind
  its short question, to Philosophy/HOW-I-INVEST.md, with a round file in Philosophy/Evolution/;
  retaken after reading, it shows how their view moved. Plan first, the owner's go, then write, at
  home only. Only when the owner runs it by name, or picks it where another skill offers it. It
  does NOT ask how they work or their general rules (`working-philosophy` does, first), edit what
  the file holds (`refine` does), or write RESEARCHER.md beyond Find first and the two rules for
  strategies, and never says buy, sell, trim, add or hold.
metadata:
  version: 2.0.1
---

# Investing philosophy — how the owner invests, in their own words, round by round

**When it applies.** The owner runs `investing-philosophy` by name, or picks it where another
skill offers it — `interview`'s hand-over for *Learn the basics* or *Write down how I invest*,
`next`, `read`'s report, the close of a `teach` lesson. It is **the second interview**: the first,
for everyone, is `working-philosophy`, how the owner works, which also settles the rules the
researcher keeps. An owner who comes here first is welcome — *Learn the basics* starts here — and
the hand-over names `working-philosophy` for later. It asks about the owner and their own money,
never a strategy: a yardstick, a fall or a split asks about the owner's own habit, never a
strategy's rule, which `objective` and `blueprint` ask later, in a strategy. It is not a test — no
score, no quiz, no wrong answer. It never tells the owner to buy, sell, trim, add or hold, never
names a product or a ticker, never proposes an allocation or a benchmark, and never computes a
return. For what the library says, use `query`; for a lesson on an idea, `teach`.

**What it writes, and only on the owner's go.** The owner's typed answers, added word for word and
add-only to `Philosophy/HOW-I-INVEST.md` — started with its title and headings when missing — and
one round file in `Philosophy/Evolution/`. This skill, `working-philosophy` and `refine` are
`Philosophy/`'s writers, as the home's `AGENTS.md` says. Beyond `Philosophy/`, two places in
`RESEARCHER.md`: the works picked in C2 on its closing *Find first* line, unless the preview leaves
that line alone; and, only when O4 is asked, the two rules for strategies under *Non-negotiables*.
Nothing else, anywhere. The same go saves a version of what it wrote.

**Only typed words reach `Philosophy/`, each behind its question.** Every typed answer is written
as `- **<Short>** <their words> *(round N)*`: the card's *Short*, the question in at most eight
words in the owner's language, in bold, so the line makes sense a year later; then their words,
exactly as typed. The *Short* is a label, never the owner's view. Nothing the owner picks — a level,
an example, a work, a rule — and no other line the researcher says reaches `Philosophy/`, round
files included. A round file is a record, read for dates and levels; the owner's view is cited from
`HOW-I-INVEST.md`, never from a round file.

**The bank.** [`references/questions.md`](references/questions.md), in this skill's folder: the
opening and the explainer, every question by level with its *Short*, *Why*, plain line, examples
and the one idea it teaches, where each answer lands, how a retake runs and which works bear on
which question. Read it whole before the first question. It is written in English and said in the
owner's language — the one *How it speaks* names — as written, in words that never mark the owner's
gender, and never improvised. IDs are stable; a retake compares by ID.

**The reading map.** Every work named comes from `references/reading-map.md` in the `read` skill's
folder, or from the owner's own `Sources/` and `Knowledge/`, with its year, authors and title as the
map gives them — never from memory. A work is a lead, never a source.

**How to ask.** Open questions are asked in chat, one per message, each opening with where the round
stands and its *Why*; a *Then* is asked in a message of its own once the *Ask* has a typed answer.
An *Ask* and a *Then* are said as the bank writes them, open: never turned into a yes-or-no, and
never into a guess from earlier answers for the owner to confirm. A pick is asked by **calling the
question tool** — `AskUserQuestion` in Claude Code — at most four options, with *Other* as the
free-text escape. **Without one** — Codex — a pick is asked in chat, its options numbered, *Other —
your own words* last. Wait for each answer.

**A round at a glance.** About 10, 15 or 20 minutes by level — 6, 8 or 10 typed questions — and it
can stop at any point.

| # | Step | How |
| --- | --- | --- |
| 1 | pre-flight: the home, what the owner has said and read, the level to suggest | nothing asked |
| 2 | the opening in round 1, or a retake's opening and its scope | said, then one tool question |
| 3 | your story: O1, Q18, Q15 | chat |
| 4 | the level (O3), then the idea the rest builds on | one tool question; said |
| 5 | the level's blocks: your yardstick, your edge, your proof | chat; one checkpoint |
| 6 | the closing: C1, then O4 when it applies, then C2 | chat; tool questions |
| 7 | on a retake, then and now | chat, never written |
| 8 | the preview, and the go | said, then one tool question |
| 9 | write, and save a version | on the go only |
| 10 | hand over | said |

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
   - An `AGENTS.md` whose `Philosophy/` row names none of `investing-philosophy`, `philosophy` (its
     name before 1.31.0) among its writers predates these interviews, and the home's own rules do
     not let it write: say so, offer `update`, which shows the new row as a diff to accept, and
     stop. A row that names `philosophy` only is an older home: the round runs, and the hand-over
     offers `update`.
   - Take the language and the voice from *How it speaks* — with none, the language of this
     conversation — and, under *Who*, the *Works for:*, *Domains:* and *Here for:* lines, whose
     picks `interview` writes in English. Take the bullets under *Non-negotiables*, one rule each;
     *None yet.*, in any language, says there is none.
3. **Read what the owner has already said.** `Philosophy/HOW-I-INVEST.md` whole when it is there,
   and `Philosophy/HOW-I-WORK.md`, for its *Why I do this work* line only, which the opening may
   quote. Then `Philosophy/Evolution/`: **this skill's rounds are the files whose first line names
   a level** — *Starter*, *Building* or *Researching*; a file with `Work` or `Field` there is
   `working-philosophy`'s, and is left alone. With none of its rounds, this is round 1. Otherwise
   it is a retake: the latest round is the newest of them — the latest date in the file names, and
   on that date the highest suffix — and its first line gives its number *N*, so this round is
   *N* + 1. From those files, gather each ID's latest typed answer, its round and its latest status,
   and the questions the last round's level asks that no round has a line for — O3, O4 and C2
   aside. A file whose first line is not a round line is no round: ignore it, and name it once.
4. **Read what the owner has read.** `Knowledge/INDEX.md` end to end; on a retake, also the `read`
   entries of `Knowledge/LOG.md` dated on or after the last round's date, and the notes they list.
5. **Find the reading map**, `references/reading-map.md` in the `read` skill's folder: under
   `~/.claude/skills/read/` or the user's folder for the agent in use, or in the package under
   `~/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/read/`, under `KaxaNuk/KaxaNuk-Researcher/`
   for an install from before 1.25.0. Match its works against `Sources/` and `Knowledge/INDEX.md`,
   as its *Match before proposing* says: a work with a note is *read*, named by a link to the note;
   a file with no note is *in your Sources/, not yet read*. **Without the map**, the bank's *Without
   the reading map* holds: say why in one line — the map comes with the `read` skill, which is not
   installed here — and give the fix, `uvx --from apm-cli==0.33.0 apm install -g
   KaxaNuk/Researcher --target <agent>`, then a new session. Never write the map, or a work from
   it, from memory.
6. **Work out, for later**: the level to suggest (*step 4*); on a retake, the last round's level,
   its reading list — the *Behind it* works of the questions it asked, derived from its IDs, never
   stored — and the notes read since.

## 2. The opening

**Round 1.** Say the bank's *Before the first question*, then ask `Ready?` (`¿Comenzamos?`) —
*Start*, *Not now*. When `HOW-I-WORK.md` holds no round yet, one line first: *there's also a first,
shorter interview on how you work, `working-philosophy`, which sets the rules I keep with you;
this one stands on its own.*

**A retake.** Say the bank's opening of *Taking it again*, then ask its scope question, `Retake?`
(`¿Repetir?`); *not now* or *stop* under *Other* is *Not now*. The scope is applied after O3,
against the questions of the level chosen there.

On *Not now*, write nothing, and say in one line how to start later: *say `investing-philosophy`
whenever you like — a new session is best.*

## 3. Your story

The same at every level, in plain words, in chat: **O1**, **Q18**, **Q15**, one per message, each
with its *Why* and its closing line; Q18's *Then* waits for the level, and is asked after O3 at
Building and Researching. After each answer, its *Teaches* line, in its Starter form: no work
named yet.

## 4. The level, and the idea the rest builds on

**O3**, one tool question, `Experience` (`Experiencia`), as the bank gives it. One option is marked
*(suggested)* — never picked for the owner — by the first rule that applies:

- **A retake.** The last round's level is marked *(current)*. The level above it is *(suggested)*
  when two works from the last round's reading list now have notes — never more than one level up.
- **Round 1.** *Here for* holds *Learn the basics*, or *How it speaks* names *Explain as you go*:
  *Just starting*. Otherwise what O1, Q18 and Q15 described — a career in markets, papers read,
  strategies tested — suggests *I research*; funds or shares bought, *Some experience*. Otherwise
  none is marked.

**An answer typed in place of a pick** is mapped to the level it describes, said back, and the
owner may change it. Then say how many questions are left and the minutes, from the bank's table.

Then the bank's explainer at the level — the **personal benchmark** and the **process** — said once,
never asked, worded so that it settles nothing the owner answers later. Its purpose line is the
bank's and the only one: *I'm here so you can make better investment decisions, by your own
yardstick.* Its caveat stays beside it. On a retake, it is said again only when the level changed,
or when the owner asks.

## 5. The level's blocks

The bank's table says which questions each level asks — *Your yardstick* at every level, *Your
edge* from Building, *Your proof* at Researching. Open each block with its name and where it stands
— *block 2 of 3 · Your edge · 2 questions*.

- **An open question** is the round's place and its *Why*, then its *Ask* at the level, ending
  with the bank's closing line; its *Then*, where the level has one, follows in a message of its
  own once the *Ask* has a typed answer, and joins it as one answer.
- **After every answer** — *not sure yet* and *skip* included — the question's *Teaches* line, as
  written: one idea, never a verdict. Starter names no work; Building at most one, as a lead;
  Researching the lead and its other side.
- **Presses on**, at Researching and on every retake: quote the owner's own line in
  `HOW-I-INVEST.md` that the question tests, if one clearly does; never guess one.
- **Behind it** is shown at Researching, or on *show me the paper*: the map's leads, a note linked
  in place of a work it holds, a gap said out loud.
- **The checkpoint**, after *Your yardstick* at Building and Researching, is the bank's `Continue?`.
  *Simpler* and *harder* switch the questions left; *Save and stop here* goes to the preview.
- **The escapes** hold on every question — *Escapes and exits* below.

## 6. The closing

**C1**, quoting the line the owner typed for Q4 — or, with none, for O1; with neither, ask about
any view they would like to test, or skip.

**O4, the two rules for strategies**, only as its card says: *Here for* holds *Build and test a
strategy* and *Non-negotiables* lacks them in any words, or the owner says *my rules* — never in
a home whose `AGENTS.md` names no skill among the writers of *Non-negotiables*. One tool
question, `Your rules` (`Tus reglas`). What it settles is written on the go under *Non-negotiables*
in `RESEARCHER.md`, never in `Philosophy/` or the round file. The owner's other rules are
`working-philosophy`'s: on *my rules*, name it for them in one line, and add here only the two. A
rule about holdings is not written there: say in one line that it belongs in `Portfolio/RULES.md`,
which `brief setup` starts and the owner writes. This skill never writes in `Portfolio/`.

**C2**, `Read next` (`Aprender`), as the bank gives it at the level: no work already *read* is
offered; a work *in your Sources/, not yet read* only needs `read`; the others are found by their
title and authors, and nothing is downloaded. `teach` is offered only when `Knowledge/` holds a
note on the idea. The works picked go on the closing *Find first* line of `RESEARCHER.md` on the go,
unless the owner leaves that line alone in the preview. Nothing from C2 reaches `Philosophy/`.

## 7. A retake: what moved

On a retake only, before the preview: the bank's comparison, in chat, never written to a file — a
line of counts, a table by ID and *Short* of then and now, and under each changed answer the notes
read between the two rounds whose work is its *Behind it*, named as reading in between, never as
the cause. Answers an earlier round gave under an ID this bank no longer asks are listed once as
*no longer asked*. With *Just show me what changed*, this is the whole run, and nothing is written.

## 8. The preview, and the go

Show in chat, before anything is written:

- **From a strategy or another project**, first: *this writes to the researcher's home, not to
  this project.*
- **`Philosophy/HOW-I-INVEST.md`**: a file to be started, first, its title and five headings,
  marked *new file*. Under each heading, every line to be added, as it will read —
  `- **<Short>** <their words> *(round N)*` — and a heading to be added at the end of an existing
  file. On a retake, under each changed answer, the old line, quoted and marked *stays — I only
  add*.
- **A standing line a new answer clearly cuts against**, quoted once: *both will stand; edit it by
  hand, or run `refine`, if one no longer holds.*
- **The round file**, whole, under its path.
- **`RESEARCHER.md`**: the works to add to the closing *Find first* line, or *left alone*; and,
  when O4 was asked, the rules it settled, named *your rules*, each line as it will read.
- **Privacy**, one line: these lines are saved in your researcher's versions; leave out any you
  would rather not keep — a name, an account, a broker typed in an answer is marked here.
- **Spelling and language**, one line, when the typed lines hold typos or another language than
  *How it speaks*: they go in exactly as typed, and `refine` can clean them right after, each line
  shown as a diff first; the round file keeps them as typed.

Then ask `Go?` (`¿Escribo?`) — *Go*, described as *write it and save a version*, *Change
something*, *Stop*; in chat, any of the go words in the home's `AGENTS.md` is the go. **A round with
no typed answer** says *nothing typed, so nothing goes into `HOW-I-INVEST.md`*, and asks instead
`Keep it?` (`¿Lo guardo?`) — *Keep this round as a record*, *Change something*, *Write nothing*.

**On *Change something*, ask again with options**: *Leave out a line*; *Reword in my words* — they
type the line again, and only their words are written; *Leave Find first alone*; and, on a retake
with a changed answer, *Leave my old line — I'll fix it with `refine`*. Then show the revised
preview and ask for the go again.

**On *Stop*, *Write nothing*, silence or a closed session, nothing is written**, and the next run
starts as this one did.

## 9. Write, on the go only

1. **`Philosophy/HOW-I-INVEST.md`, add-only.**
   - **A file `Philosophy/` lacks** is created first, with `# How I invest` and the five headings of
     the bank's *Where each answer lands*, in its order, in the owner's language, and nothing else.
   - One bullet per typed answer, `- **<Short>** <their words> *(round N)*`, under the heading
     *Lands under* names, at the end of that heading's lines. An answer of several lines keeps
     them, indented under its bullet.
   - **Headings are matched by name or position**: by the English name; else by a heading in the
     owner's language that says the same; else, in a file holding the bank's five headings, or an
     older template's four without *Why I invest*, in that order, by position. A heading matched is
     never added again.
   - Under a heading that still holds an older template's angle-bracketed prompt, the prompt stays
     and the line goes below it: the prompt is the owner's to delete by hand.
   - A heading an existing file lacks is added at the end of the file, in the language its other
     headings use, English when it has none. Nothing above it is moved.
   - A line identical to one already under its heading is not added again, and *keep* adds
     nothing. Nothing the owner wrote is edited, moved or deleted — lines an earlier round wrote
     with no *Short* in front, and any note at the top, included.
2. **`Philosophy/Evolution/YYYY-MM-DD.md`**, today's date — `-2`, `-3` for a second or third round
   the same day of either interview, the folder created when missing. Written once and never
   edited afterwards:

   ```markdown
   # Round <N> · <YYYY-MM-DD> · <level>

   - O1 · <the owner's words, word for word>
   - Q18 · not sure yet
   - Q15 · skipped
   - Q6 · explained
   ```

   - **The first line** is the round, the date and the level the round ended at — *Starter*,
     *Building* or *Researching*.
   - **One line per question asked**, in the order asked: `- <ID> · <answer>`, the owner's typed
     words or a status; an answer of several lines keeps them, indented under its bullet. O3 is the
     level on the first line; O4 and C2 take no line. No *Short* goes here: the ID is the label.
   - **On a retake**, a label follows the ID — `- <ID> · <label> · <answer>`: *kept*, with no
     answer; *changed*; *new*; *still open*. A question answered before and skipped now takes no
     label, only its status.
   - **In English**: *Round*, the level, the IDs, the labels and the statuses, because skills parse
     them; the answers are in the owner's language.
3. **`RESEARCHER.md`**, in two places, and nothing else in that file changes:
   - **Find first**, only when C2 picked a work and the owner did not leave it alone: each work
     appended to the closing *Find first* line — year, authors and title as the map gives them,
     separated by semicolons, in place of *none*, in any language — skipping one already there or
     already read. A section with no such line takes one as its last line, before *Out of scope for
     now*: `**Find first:** <the works>`.
   - **Non-negotiables**, only when O4 settled rules: one bullet per rule, `- <rule>`, in the
     owner's language, its meaning unchanged, in place of the *None yet.* paragraph while it is
     there, else after the section's last bullet. A rule held there in any words is not added again.

**Then save a version**, in the home, on the go that wrote, with no second question. Every git
command runs as `git -C "<absolute path to the home>"` when the session is open elsewhere. `git add`
each file this run wrote, by name, never `--all`, and `git commit -m "Philosophy: round <N>,
<level>" -- <the same files>`. Say it in one plain line, *Saved*, never the commands. When `git
config --get kaxanuk.autosend` prints `true`, the version is also sent to the owner's copy on
GitHub, as the `backup` skill says. A save refused for want of a name asks in one open message,
*What's your name, or what would you like me to call you?*, never invented, and no e-mail; it sets
it in the home only, with `user.email` as `"<>"`, and saves again. A home with no `.git/` gets one
line, that it keeps no versions yet.

## 10. Hand over

Short, in the owner's language and voice, in this order:

1. **What moved.** On a retake, the comparison's line of counts; on round 1, *round 1 written*, and
   how many lines went into `HOW-I-INVEST.md`; and the rules, when O4 wrote any.
2. **The first thing to `read`, or to learn.** A `teach <topic>` picked in C2 first; then the first
   work picked — in `Sources/` already, `read` it; otherwise find it by its title and authors,
   attach it or say where it is saved, and I copy it into `Sources/` on your go and read it.
3. **When to come back.** Two or three works from this round's reading list — the ones picked in C2
   first, then the list's *Start here* works in the map's order; at Starter, in the plain words of
   C2's *Three classic studies*. Then: once two of them have notes, `investing-philosophy` again, in
   a new session; what was left open waits for them there. Without the map, no work is named.
4. **`working-philosophy`**, when no working round exists: the first interview, on how you work,
   about ten minutes, and the rules I keep with you.
5. **`refine Philosophy/HOW-I-INVEST.md`**, when *Leave my old line* was picked, or the preview's
   *Spelling and language* line was shown — diff first.
6. **`update`**, when the home's `AGENTS.md` names only `philosophy`, *step 1*.
7. **`brief setup`**, when a rule about holdings was pointed to `Portfolio/RULES.md`.

## Escapes and exits

The bank's escape table holds on every question, at any time, in the owner's language too —
*explica*, *ejemplo*, *no sé todavía*, *salta*, *más simple*, *más difícil*, *para*, *igual*,
*muéstrame el estudio* — and their usual words in any other. A message that is only an escape is
that escape, and writes nothing; a message with more is a typed answer, written as typed. When it
could be either, ask once: *write that as your answer, or mark it not sure yet?* A number, or *that
one*, after an example is a pick, not typed words: ask for their own words, or a skip.

## What this skill will not let you do

- Write a pick, an example, a *Teaches* line or a status into `HOW-I-INVEST.md`, start it with more
  than its title and headings, or write anything the researcher said into a round file — the
  *Short* in front of an answer is the only line of the bank that reaches `HOW-I-INVEST.md`.
- Write in `HOW-I-WORK.md`, which is `working-philosophy`'s, or touch a round file that is not this
  skill's.
- Edit, move or delete a line already in the file — that is `refine`'s, or the owner's by hand — or
  touch a round file once written.
- Write in `RESEARCHER.md` anything but works on the closing *Find first* line and the two rules
  for strategies under *Non-negotiables*, or change or drop a rule there but one O4's *Change
  one* names.
- Write in `Portfolio/`, or put a rule about holdings under *Non-negotiables*.
- Name a work from memory, or state a paper's finding as a settled fact.
- Cite a round file as the owner's view, or as evidence of anything.
- Propose a product, a ticker, an allocation or a benchmark; compute a return; say buy, sell,
  trim, add or hold.
- Write, or save a version, on a *Stop*, on silence or on a closed session, or write at home from a
  strategy or another project without saying so first in the preview.

## References

- [`references/questions.md`](references/questions.md), in this skill's folder: the bank, what
  holds without the reading map, and the *Bears on* table that `read`'s report reads to offer the
  next round.
- `references/reading-map.md`, in the `read` skill's folder: the one list a work may be proposed
  from besides the owner's library. A work in it is a lead, never a citation.
