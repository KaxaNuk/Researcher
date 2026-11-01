---
description: A voice-preserving editor pass over a file in Philosophy/ — the owner's own writing — typos and slips fixed, and on the owner's word grammar cleaned or lines put in the home's language, ambiguities flagged, diff shown before anything is written; never a round file in Philosophy/Evolution/. Only when the owner runs it by name, on a path they give.
input:
  - path: "The file under Philosophy/ to edit"
---

# Refine a Philosophy file

Every path below is relative to the researcher's home — the folder that holds `RESEARCHER.md`. Find
it first and read its `RESEARCHER.md` and `AGENTS.md`. This command works at home only.

`Philosophy/` is the owner's voice, and it has exactly three writers. `working-philosophy` adds the
owner's typed answers to `HOW-I-WORK.md`, and `investing-philosophy` to `HOW-I-INVEST.md`, word for
word and add-only, each behind its short question in bold, after the owner's go, and each writes one
round file in `Philosophy/Evolution/`, never edited afterwards. `refine` edits either file as an
editor, diff first, and never touches `Evolution/`. A file the owner keeps beside them in
`Philosophy/`, outside `Evolution/`, is theirs in the same way and takes the same pass.
`${input:path}` is one file under `Philosophy/`.

1. Confirm the path is under `Philosophy/` and not under `Philosophy/Evolution/`. A round file is a
   record of how the owner's answers moved, never edited afterwards: refuse it, say so in one line,
   and stop — whatever the owner wants changed there is a line in the file of that round's topic,
   or the next round of `working-philosophy` or `investing-philosophy`.
2. Read the file. Find **only** typos, doubled words, broken links and obvious slips. Preserve the
   voice, the headings, the order, the analogies, the emphasis and the bullet structure, every
   *(round N)* tag a round put on a line, and every short question in bold a round put in front of
   an answer, exactly as they stand: a retake finds the owner's earlier answers by them, and the
   question is a label, never the owner's words. **On the owner's explicit word** — *clean the
   grammar*, *put it in English*, in any words — the pass also fixes grammar and accents, or puts
   lines into the language *How it speaks* names, line by line: the meaning, the order, the bullet
   structure, every *(round N)* tag and every question in bold kept, a name, a number and a term of
   art left as written, nothing added or dropped. A line whose meaning is unclear is flagged, as
   below, never guessed. The round file keeps the words as typed.
3. Where a passage is unclear or ambiguous, do not rewrite it: name it in chat, with the question a
   careful reader would ask; the owner answers it by hand, or types a line that goes in as typed.
4. **A line a later round changed** — the owner names it, or a round of either interview sent them
   here for it: offer, as options, to leave it; to add a line the owner types beneath it; or, on the
   owner's explicit word, to take it out. Never reword it for them: their new words are already in
   the file, under their own tag.
5. Show the diff in chat and wait for an explicit go, *write it and save a version*.
6. Apply exactly the approved diff. Report what changed.
7. **Then save a version**, in the home, on the same go, with no second question. Every git
   command, the `backup` skill's send included, runs as `git -C "<absolute path to the home>"` when
   the session is open elsewhere: `git add` the file, by name, never `--all`, and
   `git commit -m "Refine: <file>" -- <file>`; to the owner, *Saved*, in one plain line, never the
   commands. When `git config --get kaxanuk.autosend` prints `true`, it also goes to their copy on
   GitHub, as the `backup` skill says. If git wants a name, ask in one open message, with no
   options, *What's your name, or what would you like me to call you?*, never invented, and no
   e-mail; set it in the home only, with `user.email` as `"<>"`, an empty address, and save again;
   with no `.git/`, say in one line that the home keeps no versions yet. This replaces an older
   home's *Commit?* question.

Never restructure, reorder or paraphrase. Never move a `Philosophy/` file's content into
`Knowledge/` as a side effect. Never invent content to resolve an ambiguity — flag it.
