---
name: watch
description: >
  Load this skill whenever the owner gives a video's link — a YouTube talk, a lecture, an
  interview, a podcast — or a video's transcript, and asks to watch it, read it, take its main
  ideas or add it to the library. A script fetches the video's details and captions (never the
  video) into a Markdown transcript; the owner picks which chapters serve which question; on their
  go the transcript is copied into Sources/Videos/ and read into a note in Knowledge/, timestamps
  in place of pages, the concept pages it touches updated, as the `read` skill does. When YouTube
  refuses, it stops and asks the owner for the transcript. It does NOT write in Philosophy/ (the
  owner's view is theirs, through `working-philosophy`), read a PDF (use `read`), or answer from
  the library (use `query`).
metadata:
  version: 0.2.0
---

# Watch — a video into the library, a chapter at a time

The owner gives a video's link, or a transcript they copied, and asks to watch it, take its main
ideas or add it to the library; or asks for a video's chapters before deciding what to read. What
they said carries the arguments: the link, the question it should serve by number, and *outline
only* to stop after the chapters.

This is the `read` skill for a video. Find the researcher's home — the folder that holds
`RESEARCHER.md` — and read its `RESEARCHER.md` and `AGENTS.md`, then the `read` skill's
`SKILL.md` and its `references/note.md`: everything they say holds here, with the differences
below. At home only for now; in a strategy, say that `watch` does not write there yet, and stop.
**A plan in chat, and the owner's explicit go, before any file is written.**

Three jobs, kept apart, as in `read`. **Fetching** the transcript is deterministic and belongs to
`scripts/transcript.py` in this skill's folder. **Choosing** what to read is the owner's, with the
chapters in front of them. **Reading** the chosen text and writing the note is the researcher's.

## 1. Know what happened recently

As `read`'s *step 1*: the last five entries of `Knowledge/LOG.md`, the index, and in
`RESEARCHER.md` the domains, *Here for*, *Works for*, the tag policy and the questions under *What
you are reading for*. A video already in `Sources/Videos/` with a note naming it is not read again
unless the owner says so; a partly read one continues from its note's `read` line.

## 2. Fetch the transcript

From the home, run:

```bash
uv run "<this skill's directory>/scripts/transcript.py" "<link>"
```

It asks yt-dlp for the video's details and its caption track — human-made captions first, else
YouTube's auto-generated ones in the video's own language, never a machine translation — and
writes `<video id>.md` in the system's temporary folder, `watch/`: the details, the description,
and the transcript under the video's chapters, or ten-minute parts when it has none, a `[m:ss]`
marker about every thirty seconds. It prints the details, a name hint and the outline, each
chapter with its times and word count. `--lang es` asks for another language. It never writes
inside `Sources/`: the copy is *step 6*, on the go.

- **Exit 3, YouTube refused** — a sign-in or bot check, a 403, a 429, a private or removed video.
  Nothing is retried: no cookies, no other client, no proxy, no mirror, no browser tool. Ask the
  owner to open the video, click *… → Show transcript*, copy it into a text file and say where it
  is saved, with the video's title as YouTube shows it. Then run, with `--channel` and
  `--uploaded YYYY-MM-DD` when the owner gives them:

  ```bash
  uv run "<this skill's directory>/scripts/transcript.py" "<link>" --paste "<file>" --title "<title>"
  ```
- **Exit 4, no captions** in that language: the script names the tracks there are. Offer `--lang`
  for one of them, or the owner's own transcript as above; never a summary from elsewhere.
- **Exit 2** is a mistake in the command: fix it and run again. **Exit 1** is a link yt-dlp cannot
  read — not a video, or a site it does not know: say so, and ask for the video's YouTube link.
- **A transcript the owner attaches** with timestamps is run through `--paste` the same way; one
  without timestamps is copied in as a clipping and read with `read`, which cites no time.

## 3. Show the chapters, and ask

One message: the video's title, speaker, channel, date, length and which captions were used, then
the chapters as the script numbered them, with their times, and beside each a proposal — **read**,
**skim** or **skip** — and the question it would serve, by its number, judged from the titles and
the owner's questions. An intro, a host's announcements and credits are proposed *skip*. Then ask
through the question tool as `read`'s *step 3* does: *Take the proposal as it stands*; *Change
some chapters*; *Read everything*; *Outline only*. The three open answers of `read` — a new
question, *the other side of question N*, *background reading* — stay open, and a question with no
number yet is asked first, exactly as there. A fourth is open here: *background for my philosophy*,
for a talk on how to work or invest — `## Why it is here` then names `Philosophy/HOW-I-WORK.md` or
`HOW-I-INVEST.md` as what the reading is for, with any question it also serves by number, and the
report's questions for the owner (*step 7*) are its point.

## 4. Read what was chosen, and decide

Read each chosen chapter of the transcript in full, from the file in the temporary folder. A
skimmed chapter is read for one line. Then decide, as `read`'s *step 4* does, where the note goes,
its citation, what it links to, the concept pages it touches, what it contradicts and which file in
`Philosophy/` speaks to the same subject — with these differences:

- **One note per video**, named `Speaker_Year_Title.md`: the speaker as the video names them —
  its title, its description or the host's introduction in the transcript — never from memory;
  two speakers for a conversation; the channel when nobody is named. The year is the upload year
  the script printed, or the talk's own date when the video states it. A long video is still one
  note: its chapters are the claims' sections, and the provenance line names what was skipped.
- **Timestamps take the place of pages**: `(12:34)`, the transcript's markers, on every claim.
  A video's chapters are the uploader's and often cut through an answer: cite each claim by the
  marker where the speaker actually says it, and a section by the marker where its answer begins,
  never by the chapter's start.
- **Captions mishear.** Auto-generated captions drop punctuation, run speakers together and
  misspell names, firms and figures — *Draper Fisher derson* for *Draper Fisher Jurvetson*. A
  name is written in its usual spelling when the video shows it — its title, its description, the
  speaker spelling it out — or when the captions give it recognisably and the context leaves no
  doubt which one is meant: *GeForce*, *Sequoia*. Only a name the captions garble beyond that,
  where it could be more than one thing, is quoted as captioned and marked *(as captioned)*. A
  figure the captions give is the speaker's, said aloud, and the note says so.
- **Questions from the audience** are claims of the speaker's answer, the question in one line.

What you remember of a well-known talk or speaker is not the talk: nothing is written from memory,
and nothing from a summary.

## 5. Present the plan

As `read`'s *step 5*: the copy of the transcript to `Sources/Videos/<the note's name>.md`, never
over an existing file; the note's path and the question it serves; the concept pages created and
updated, one line each; links; the `Philosophy/` file to cite; contradictions; questions to add to
`RESEARCHER.md`, in the owner's words; and the log line. The transcript is text, so it is saved
with its note, as a clipping is; the plan says so. Then *Go* — *write it and save a version* —,
*Change something*, *Stop*; on *Change something*, options, never an open question.

## 6. Write, on approval only

- The transcript copied from the temporary folder to `Sources/Videos/` under the note's name,
  never over a file. `Sources/Videos/` is made if it is missing. That copy is the only write into
  `Sources/`.
- The note, in `references/note.md`'s paper shape, with this frontmatter:

  ```yaml
  ---
  source: https://www.youtube.com/watch?v=<id>
  citation: Speaker, A. (Year). Title [Video]. Channel, YouTube. Link checked YYYY-MM-DD.
  local_copy: Sources/Videos/Speaker_Year_Title.md
  read: YYYY-MM-DD, chapters 2-12 of 20 (intro and audience questions 15-17 skipped)
  tags: [...]
  ---
  ```

  and a provenance line that names the captions: *Chapters 2-12, 3:44-31:12, from YouTube's
  auto-generated English captions.*
- The concept pages, the index and the log entry, as `read`'s *step 6* says, its scripts used the
  same way. A concept page cites notes only and never links to `Philosophy/`: where the owner's
  file speaks to the talk, the link is in the note. The log entry's kind is `watch`, and its
  `read:` line names the chapters read, skimmed and skipped.
- The version saved, as *step 7* says: every file written, the transcript with its note, by name,
  in one save named `Watch: <Speaker Year, short title>`.

## 7. Report, and save

As `read`'s *step 7*: what was written and flagged, the gaps, the strategy or study a note could
serve, and whether the talk bears on a belief in `Philosophy/HOW-I-WORK.md` or `HOW-I-INVEST.md` —
as a question for the owner to answer there in their own words, by hand or in a round of
`working-philosophy` or `investing-philosophy`. The researcher writes nothing in `Philosophy/`, not
even the talk's ideas the owner agreed with. Then save a version as `read` does, the transcript
with its note, the commit named `Watch: <Speaker Year, short title>`, said in one line: *Saved*.

## What this skill will not let you do

- Download a video, or get past a refusal, a sign-in or a bot check. The owner fetches what
  YouTube will not give a script.
- Write the transcript into `Sources/` before the go, over an existing file, or anywhere but
  `Sources/Videos/`; or move, rename or edit a transcript once it is there.
- Write in `Philosophy/`, `Studies/` or `Lessons/`, or in a strategy.
- Fill a chapter, a name or a figure from memory, from a summary or from another site.
- Write a note for a chapter the owner did not choose, or a question or reason they did not give.
- Write a plan or a report as a file. The chat and the log entry are the record.

## References

- `scripts/transcript.py`, in this skill's folder: the video's details and captions as Markdown,
  outside the library, and the outline. `--help` has every option; its docstring, the exit codes.
- The `read` skill's `SKILL.md` and `references/note.md`: the steps and the note's shape this skill
  follows, and the scripts it uses for concept pages and checks.
