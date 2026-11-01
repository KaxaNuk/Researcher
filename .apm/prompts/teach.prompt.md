---
description: A multi-session tutor grounded in Knowledge/ — the library checked for the topic first, and a first work read when it holds none, then an interview, then one lesson per session with a retrieval quiz; state in Lessons/<topic>/; with no topic, list the topics. Only when the owner runs it by name.
input:
  - topic: "Optional: the topic to teach; with none, the topics in Lessons/"
---

# Teach a topic

Every path below is relative to the researcher's home — the folder that holds `RESEARCHER.md`. Find
it first and read its `RESEARCHER.md` and `AGENTS.md`. This command works at home only.

Teach `${input:topic}` from what the owner has read, one lesson per session. Running this command
names `Lessons/<topic-slug>/`, at the home's root, as the only place it may write — the place, not
the go: every write still waits for a plan and an explicit go, as `AGENTS.md` requires of every
command that writes. The home ships no `Lessons/`: the first topic taught creates it, and each new
topic its own folder in it.

**No topic.** List the topics in `Lessons/`, each with its mission and its last session from
`progress.md`, and offer to continue one or start another; with none, say so in one line and ask
for a topic.

**First, the library.** Before any question on a new topic, walk `Knowledge/INDEX.md` for it, the
concept pages first. With no note bearing on it, say so in one line, then offer up to three works to
read first, and *Later*, through the question tool. The works come from the reading map in the
`read` skill's folder when Finance is among the domains and the map has the topic, matched first as
its *Match before proposing* says; otherwise, a *Find first* work that bears on it. With none, offer
*I have a document* — they attach it or say where it is saved — beside *Later*. Never download a
work: on a pick, the owner attaches it or says where it is saved, and `read` copies it into
`Sources/` and writes its note, on its one go. Then go straight on into the interview below, in the
same session, so the first lesson stands on a note; *Later* stops here. Nothing is taught from
memory.

**A new topic** (no `progress.md` yet), with notes that bear on it: interview the owner first — why
this topic, what for, what they already know, how they like to learn. Two to four questions. When
the topic is about investing and `Philosophy/Evolution/` holds a round of `investing-philosophy` — a
level, not `Work` or `Field`, on its first line — read the newest such round's level, *Starter*,
*Building* or *Researching*, instead of asking what they already know, and say so in one line for
them to correct. The newest is, among those rounds, the latest date in the file names, and on that
date the highest suffix, `YYYY-MM-DD-2.md`. Then show the plan in chat — the mission, the
preferences, the folder and the files it creates — and ask for the go through the question tool
where the harness has one: *Go*, described as *write it and save a version*; *Change something*;
*Stop*. On the go, write the mission and the preferences into `progress.md` and save it alone, as
item 5 says, with the message `Teach: <topic>, mission`. Never skip the interview; never
re-interview an existing topic unless the owner says the mission has changed.

**An existing topic**: read `progress.md` — mission, track, preferences — and pick the next lesson
just beyond what stuck last time.

**A topic still in `Projects/Teach/<topic-slug>/`** is never started afresh: `update` moves it to
`Lessons/`. With both, teach from `Lessons/`.

**Every lesson:**

1. Ground it in `Knowledge/` by the same walk as `query`: index first, then links, then notes,
   and the owner's `Philosophy/` where their own view bears on the concept, cited as theirs, never
   a round file in `Philosophy/Evolution/`, a record, as the home's `AGENTS.md` says. Cite every
   claim with a link. If the library is thin on the topic, say so and name the sources to add to
   `Sources/` — never substitute what you happen to know for what the owner has read.
2. One tightly scoped concept, tied to the mission and, where it fits, to a strategy the owner is
   building.
3. Show the lesson's plan first — the one concept, the notes it will cite, the file name — and wait
   for the go, *write it and save a version*. Then write it as `sessions/NNNN-<name>.md`, run it
   interactively in chat, and close with a short retrieval quiz that also touches earlier sessions.
4. Append one row to the track in `progress.md`: date, lesson, what stuck, what did not. That row
   is part of the same run, on the same go, the way a `LOG.md` entry is; it needs no second go.
5. **Then save a version**, in the home, on the same go, with no second question. Every git
   command, the `backup` skill's send included, runs as `git -C "<absolute path to the home>"` when
   the session is open elsewhere: `git add` the session file and `progress.md`, by name, never
   `--all`, and `git commit -m "Teach: <topic>, session <N>" -- <the same files>`; to the owner,
   *Saved*, in one plain line, never the commands. When `git config --get kaxanuk.autosend` prints
   `true`, it also goes to their copy on GitHub, as the `backup` skill says. If git wants a name,
   ask in one open message, with no options, *What's your name, or what would you like me to call
   you?*, never invented, and no e-mail; set it in the home only, with `user.email` as `"<>"`, an
   empty address, and save again; with no `.git/`, say in one line that the home keeps no versions
   yet. This replaces an older home's *Commit?* question.
6. Close the lesson with one line, offered and never pressed, a round of one of the two
   interviews, as `next` does. With no round of `working-philosophy` in `Philosophy/Evolution/` —
   `Work` or `Field` on its first line: *`working-philosophy` writes down how you work, in your
   words, and sets the rules I keep with you — about ten minutes, whenever you like.* Else, with no
   round of `investing-philosophy` and *Domains* holding Finance or *Here for* holding *Learn the
   basics*, *Build and test a strategy* or *Write down how I invest*: *`investing-philosophy`
   writes down how you invest, in your words, at your level — round 1, whenever you like.*
   Otherwise, the next round of the topic the lesson touched, naming its latest round's date and its
   level or *work*.

Never edit a past session file. Never write outside `Lessons/<topic-slug>/` — a first work's `read`,
or a round of either interview, is that skill's own run, with its own plan and go, never part of a
lesson. A lesson teaches an idea, never what to do with money: it never says buy, sell, trim, add or
hold, and never recommends a product.
