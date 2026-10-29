---
name: init-researcher
description: >
  Create a KaxaNuk researcher's home, once per person — ask the language, the researcher's name and
  where to put it, bring the package to its newest version with apm update -g, copy the home
  template inside it by a script, its first version saved — then run the interview in the same
  conversation. With a home already made, it offers that one first, and makes a second — a test,
  or another person — only on the owner's word. Only when the owner runs it by name, or as the step
  of the install SETUP.md walks through; never per strategy. It does NOT create a strategy (use
  `init-strategy`), nor ask how the owner works or invests (`philosophy` does, later).
metadata:
  version: 0.9.0
---

# Init researcher — a home for the library, once

A researcher is one per person, not per strategy: its library — `Sources/`, `Knowledge/`,
`Philosophy/` — grows across every strategy and project, and a second home would split it. So this
runs once a person, and a second home — a test, or another person on this computer — is made only
when the owner asks for one. The home is named after the researcher — `Arya`, not `my-researcher`.

**Plain words throughout.** The owner may never have used a terminal. Ask one thing at a time, never
ask them to type a command — you run every one — and say what happens in a sentence, as a progress
note sent with the command it announces: from step 1 to the interview's hand-over, a turn ends only
on a question. **Done is the interview's first question, never the copy.** After the owner's *Go* on
`Where?`, steps 4 to 7 run in the same turn, and what the owner reads next is the interview's
question 1 — one open chat message, with no options — never a message that only reports the home
is made, never an offer to start the interview. The only questions between are step 6's own —
`Where?` again for a folder the script refuses, git, or a name to sign with — and question 1
follows straight after the answer. Without a question tool — Codex, Gemini —
each question marked *through the question tool* is one chat message, its options numbered beneath
and *Other — your own words* last.

**The package**, where a step reads or runs one of its files — `<the package>` in a command below —
is `$HOME/.apm/apm_modules/KaxaNuk/Researcher/`;
`$HOME/.apm/apm_modules/KaxaNuk/KaxaNuk-Researcher/` when it was installed before 1.25.0, under
the repository's former name; or `$HOME/.apm/apm_modules/_local/KaxaNuk-Researcher/` when it was
installed from an archive or a folder. A path not found there: list `$HOME/.apm/apm_modules` and
use the package it shows; never end the turn on it. `$HOME` expands in a command, but a
file-reading tool does not expand it: give that tool the full path, the home folder spelled out —
`C:\Users\<user>\.apm\...` on Windows.

## When to Use

- The owner runs `init-researcher` by name — *init-researcher Arya*, *set up my researcher*, *make a
  test researcher* — or `SETUP.md` reaches its step 3, in the conversation that installed the
  package.
- A home made before the researcher was a package is brought forward by `update`, not replaced.

## Steps

**Before step 1, a home already made.** Look in `$HOME/.apm/apm_modules/_local/` for a folder whose
`RESEARCHER.md` is filled — no angle-bracketed slot left — and at the researcher's skill loaded in
this session, whose description names its home. With none, go on to step 1. With one, <Existing> is
the *Name* in its `RESEARCHER.md`, and where it lives is the path the description of its skill
gives, `.apm/skills/<slug>/SKILL.md` in that copy, asked of the owner only when it is missing:

- **When the owner did not ask for another** — *a test researcher*, *a second one*, *another one*,
  in any words — say where it is in one line, install nothing yet, and ask once, in the language the
  owner writes in, through the question tool, `Another?` (`¿Otro?`):
  - *Use <Existing> (recommended)* — install it for this assistant as `SETUP.md`'s *One researcher
    per person* says — the package with `--target`, `user_targets.py add`, this assistant added
    under `targets:` in the home's `apm.yml` when it is missing there (OpenCode aside) and saved in
    the home, the home, `check` — and hand over in the interview's *Step 6* words: who and where,
    and *say `next`*;
  - *Make a second one* — a test, or another person on this computer: a second library, and a
    second researcher in every session until it is removed — then every step below as written, the
    interview included, under a name other than <Existing>;
  - *Stop*, and nothing is installed or made.
- **When the owner asked for another**, ask nothing: run every step below as written, under a name
  other than <Existing>.

With several homes, a *Use* option for each, the one whose skill is loaded in this session first;
past four options, *Stop* is left out and the other homes are named in the line before the question.

1. **The language.** If the owner has not chosen one in this conversation, ask it first, alone, in
   Spanish and English together, through the question tool: `Idioma/Lang` — *Español*,
   *English*; *Other* for another. Everything after is in that language, the interview included.

2. **The name, with a welcome.** One warm line first, in their language — *Your researcher will be
   your companion for your work and your projects, and you'll call it by its name in any folder.*
   (*Tu investigador será tu compañero para tu trabajo y tus proyectos, y lo llamarás por su nombre
   en cualquier carpeta.*) — and one line on what it is, as written: *It's for research and
   learning, never investment advice: it can be wrong, every decision is yours, and what you share
   with it goes to the company behind your assistant.* (*Es para investigar y aprender, nunca
   asesoría de inversiones: puede equivocarse, cada decisión es tuya y lo que compartes con él llega
   a la empresa detrás de tu asistente.*) — then *What would you like to call it?* (*¿Cómo te
   gustaría llamarlo?*), through the question tool: three short names proposed, each with a few
   words on its feel, and *Other* for theirs. A name given with the command is used without asking,
   after the two lines. Never pick one for them. With a home already made, no name proposed is
   <Existing>, and a name that matches <Existing>, or a folder in `$HOME/.apm/apm_modules/_local/`,
   letter for letter but for case — `arya` beside `Arya` — is asked for again, in one line: its home
   would be copied over that folder. Accents count, so `Sofia` beside `Sofía` is a new name.

3. **The place and the go, in one question.** Before asking, look at the path proposed: when it
   exists and is not empty, the question opens with that, in one line, and *Go* proposes `<Name>`
   under another parent. Then `Where?` (`¿Dónde?`), through the question tool:
   - *Go — make it at <path>*, described as *creates your researcher's home there, then two quick
     questions about you, and sets it up — about three minutes*, *after bringing the package up to
     date* added when step 5 will run, and *beside <Existing>, which stays as it is — a second
     researcher in every session until this one is removed* when the owner asked for another home
     and `Another?` was not asked;
   - *Another folder*, which asks for the parent folder only, in chat, puts `<Name>` inside it — a
     path already ending in `<Name>` is used as is, never nested — looks at that path too, and asks
     `Where?` again with it;
   - *Stop*, and nothing is made.

   The path proposed is built from the name, short and outside any synced folder:
   `C:\Research\<Name>` on Windows — `D:\Research\<Name>` when a `D:` drive exists —
   `/Users/<you>/Research/<Name>` on macOS and `/home/<you>/Research/<Name>` on Linux, handed to
   the script absolute, the home folder spelled out, never `~`. Never a deep path such as
   `C:\Users\<you>\OneDrive\...`: on Windows a copied path may pass the path limit.
   *About three minutes* is said here and nowhere else on the way in. Run on *Go* only.

4. **On *Go*, one line**, a progress note sent with the first command step 5 or 6 runs, never alone
   — on Codex a message with no command ends the turn — then the next step at once, in the same
   turn: *Your assistant may ask you to allow a few commands; allowing them is all you need to do.*

5. **Bring the package up to date**, on the same go, before anything is copied.
   **Skip this step when the package was installed in this same conversation**: it is
   already the newest, and `SETUP.md`'s step 2 listed the assistant. Otherwise, first put the
   assistant in use — `claude`, `codex`, `copilot`, `cursor`, `gemini`, `opencode` or `windsurf` —
   on APM's list in `$HOME/.apm/apm.yml`, so the update keeps its files. The script is in this
   skill's folder; where the skill is not loaded, run it from the package. Run one of these, never
   both:

   ```bash
   uv run --no-project python "<this skill's directory>/scripts/user_targets.py" add <assistant>
   uv run --no-project python "<the package>/.apm/skills/init-researcher/scripts/user_targets.py" add <assistant>
   ```

   Then update, in the foreground, and wait for it, up to ten minutes — a timeout of 600000 ms where
   the command tool takes one: it copies every home installed for the user again, which can take
   minutes. Never leave it running in the background and end the turn:

   ```bash
   uvx --from apm-cli==0.33.0 apm update -g --yes
   ```

   The go is the confirmation, so `--yes` answers APM's own prompt, which an agent's shell cannot.
   If `add` exits 1, skip the update too — it could delete this assistant's files — and never fix
   `apm.yml` here. When `add` or the update fails — no network, GitHub out of reach — say why in one
   plain line, as a progress note sent with step 6's command, and go on to step 6 in the same turn:
   the home is made from the version installed, and `update` brings it forward later. Old
   `KaxaNuk-Agent-Skills` packages the update may list as orphaned are harmless; leave them
   unmentioned.

   After an update that ran, look for the owner's own skills, commands and agents under the
   package's names, which an install keeps and leaves the package's out for, by the package's
   script, without asking:

   ```bash
   uv run --no-project python "<the package>/.apm/skills/init-researcher/scripts/user_targets.py" clashes <assistant>
   ```

   When it exits 1, ask the `Same name` question of `SETUP.md`'s step 2, in its words, before step
   6; on *Rename mine*, run the same script's `keep-mine <assistant>`, then
   `uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher` and `clashes` once more. When it
   exits 0, nothing is said about it.

6. **Copy.** The script is in the `init-strategy` skill's folder, beside this one; in the
   conversation that installed the package, where the skill is not loaded yet, run it from the
   package itself. Run one of these, never both:

   ```bash
   uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" researcher "<full path>"
   uv run --no-project python "<the package>/.apm/skills/init-strategy/scripts/scaffold.py" researcher "<full path>"
   ```

   In the conversation that installed git or uv, put `C:\Program Files\Git\cmd` first on the path in
   the same command, and call `uv` by its full path, as `SETUP.md`'s step 1 says.

   It creates the parent folder when it is missing, and refuses a folder that exists and is not
   empty. On Windows without long paths, it also refuses a destination so deep that a copied path
   would pass 259 characters, names that path and the longest destination that fits, and writes
   nothing. **A folder refused** is answered by asking `Where?` again at once, its first line the
   reason in plain words, a shorter or an empty place proposed; never end the turn on the refusal,
   and on its *Go* run step 6 again, never steps 4 and 5. A copy stopped partway —
   `The copy stopped at …` — is run once more with the assistant's permission to write there;
   stopped again, it is answered as a folder refused. But when it says `<full path>` is not empty
   and this conversation copied into it — its oldest commit reads
   `Start from the KaxaNuk Researcher template` — that copy is the home: go on to step 7, never
   asking for another folder.

   A fork of the package, or a clone in a folder of another name, is not found on its own: pass
   `--package <its install folder>`. A git step that fails leaves the copy in place — the script
   still exits 0 — and prints every command that finishes the repository from that step on. **When
   it says git was not found** and this conversation installed git, run the printed commands in the
   new folder with git first on the path, as above — never install it again, never ask. Only when
   git is truly missing, install it on the owner's go, then run the printed commands there. If the
   first commit fails for want of a git identity, ask in one open message, with no options, *What's
   your name, or what would you like me to call you?*, never invented, and no email; set them in
   that folder only, `git config user.name "<their answer>"` and `git config user.email "<>"`, an
   empty address, then run the printed commands there. Then step 7 at once, in the same turn.

7. **Run the interview now**, in this same turn. Read the whole `interview`
   skill, not only its steps — as a skill when this session lists it, or else its file: `SKILL.md`
   in the `interview` folder beside this skill's own folder, or
   `<the package>/.apm/skills/interview/SKILL.md`; a file not found is looked for as *The package*
   says, never a stop. Then follow it from its *Step 1*, with `<full path>` as the home — read and
   written by that absolute path, whatever folder the session is open in, even one holding another
   `RESEARCHER.md` — and the name step 2 took as the researcher's, never judged or asked again. What
   it must still ask — the owner's name, another short name for the files — goes into question 1, as
   the interview's *Step 1* says, never a message of its own. Question 1 is what the owner reads
   next, opened by *Your researcher's home is ready at `<full path>`. Now two quick questions about
   you, so it is yours.* — the first line of question 1's message, in the same turn. The interview
   says the rest; its own hand-over ends the run, or goes on into what the owner picks there.

   Only when the owner asks to stop — in chat, at question 1 or before it — one line: *When you're
   ready, open `<full path>` in a new session and say `interview`.* Never offer stopping on your
   own, nor in question 1.

## References

- `apm update -g`, with the APM the package is pinned to, 0.33.0 — the update its `SETUP.md` and
  the `update` command run.
- `scripts/user_targets.py`, in this skill's folder — puts an assistant on APM's list in
  `~/.apm/apm.yml`, which an install or update without `--target` keeps, and checks the
  researcher's files for it; `SETUP.md`, `interview`, `next` and `update` run it too.
- `scripts/scaffold.py`, in the `init-strategy` skill's folder — copies `templates/researcher/`
  from the KaxaNuk Researcher package.
- The `interview` skill, beside this one.
