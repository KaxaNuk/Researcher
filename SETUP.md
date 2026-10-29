# Setup

From nothing to a researcher you can talk to, in one conversation. This file is written for the
assistant — Claude, Codex, Gemini, Cursor, Copilot — that was told *please install this repo for
me and set up my researcher, start to finish in this conversation — install everything it needs
without asking first:* `https://github.com/KaxaNuk/Researcher`, or its former address,
`https://github.com/KaxaNuk/KaxaNuk-Researcher`, or, from an older README, *please install this
repo for me, with everything it needs* or *please help me install this repo*: all three ask for the
same, a researcher set up from start to finish. Told instead *please install
this repo for me and bring back my researcher from my private copy on GitHub*, it asks for the same
install and a researcher brought back, not made: step 3 says how.

> **For the agent, read this first.**
>
> - **Done is step 6, not step 2.** Installing the package is a means; what the user asked for is
>   a researcher they can talk to. Never end your turn between steps 0 and 6 except with a question
>   the user must answer — never with a report that something is installed: a line on what a step
>   does is a progress note, sent while you keep working. With a plan tool, list steps 0 to 6 in it
>   first.
> - **Ask the language before anything else**, in Spanish and English together — *¿En qué idioma
>   prefieres que hablemos? / Which language would you like to use?* — *Español*, *English*, or
>   another. From then on every message, question and explanation is in that language.
> - **Never ask whether to install.** The user already asked: the line they pasted says to install
>   the repo and everything it needs, with no need to ask first, and the older *please help me
>   install this repo* asks for the same. Once the language is chosen, install what is missing and
>   the package, and go straight on.
> - **The user may never have used a terminal.** Plain words, one question at a time, and you run
>   every command yourself; never ask them to type one. Without a question tool — Codex, Gemini —
>   each pick is one chat message, its options a numbered list, *Other — your own words* last; the
>   user answers with the number. Say in one sentence what each step does, and that their
>   assistant may ask them to allow a command — allowing it is all they do.
> - **One conversation, start to finish.** Never ask the user to restart their assistant, open a
>   new session or a new terminal before step 6, even when a tool's output says to: a tool just
>   installed is called by its full path, as step 1 says, and steps 3 to 6 follow the package's
>   files by their installed path, as the table below gives.
> - **Nothing is cloned.** This repository is a package: it is installed once for the user, and
>   its files then make every folder they need.

**The files you follow**, once step 2 has installed the package. `$HOME` is the user's home folder
— `C:\Users\<user>` on Windows — and expands in PowerShell, bash and zsh alike, also in a path
handed to a program, where `~` does not; a file-reading tool expands neither, so give it the path
with the home folder spelled out. The paths are the same on every assistant. A package installed
before 1.25.0, under the repository's former name, sits at
`$HOME/.apm/apm_modules/KaxaNuk/KaxaNuk-Researcher/` instead, and one installed from an archive or
a folder at `$HOME/.apm/apm_modules/_local/KaxaNuk-Researcher/`:

| For | Follow or run |
| --- | --- |
| step 2 and the done check, the assistants APM keeps | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py` |
| steps 3 and 4, the researcher's home | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/SKILL.md` |
| the copy it makes | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-strategy/scripts/scaffold.py` |
| step 5, the interview | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/interview/SKILL.md` |
| step 6, `read`, only if the user brings a document now | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/read/SKILL.md` |
| step 6, `philosophy`, only if the user takes it now | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/philosophy/SKILL.md` |
| step 6, `init-example`, only if the user asks for the worked example now | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-example/SKILL.md` |
| step 6, `study`, only if the user starts the study now | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/prompts/study.prompt.md` |
| step 3, a researcher brought back from GitHub | `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/backup/SKILL.md`, its *Step 10*, then `$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/prompts/update.prompt.md` |

---

## Step 0 — The language

Ask it, as the box above says. That is the whole step.

## Step 1 — Two tools, and a name for git

Two tools. Python is **not** one of them — `uv` fetches what it needs itself. Check both with
`git --version` and `uv --version`, and install whichever is missing, without asking:

| Tool | Windows | macOS and Linux |
| --- | --- | --- |
| [git](https://git-scm.com) | `winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements` | `xcode-select --install` on macOS; the package manager on Linux |
| [uv](https://docs.astral.sh/uv/) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

On macOS, `xcode-select --install` opens a dialog: ask the user to click *Install* and to say when
it has finished; `xcode-select -p` printing a folder confirms it. When they say it has finished, go
straight on to the next step. A tool just installed is not on this shell's path yet, so call it by
its full path for the rest of the conversation: `uv` and `uvx` in `$HOME/.local/bin/` — in
PowerShell, `& "$HOME/.local/bin/uv"` — and git at `C:\Program Files\Git\cmd\git.exe` on Windows. A
command that runs git itself, APM and `scaffold.py` among them, finds it when
`C:\Program Files\Git\cmd` is put first on the path in that same command.

Every folder the researcher makes keeps dated versions of its files, each signed with a name. If
`git config --global user.name` prints nothing, ask for it in one open chat message, with no box
and no options — *What's your name, or what would you like me to call you?* (*¿Cómo te llamas, o
cómo quieres que te llame?*) — **never invent it**, and set it. No email is asked: when
`git config --global user.email` prints nothing too, set it to `<>`, an empty address that every
shell passes as it is, so versions are signed with the name alone:

```bash
git config --global user.name "<their answer>"
git config --global user.email "<>"
```

## Step 2 — Install the package

```bash
uv tool install apm-cli==0.33.0
uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher --target <the assistant you are>
uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py" add <the assistant you are>
uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py" clashes <the assistant you are>
```

The target is the assistant you are: `claude`, `codex`, `gemini`, `cursor`, `copilot`, `opencode` or
`windsurf`. Run all four without asking. `-g` installs for the user, whatever folder you are in,
and `add` keeps your assistant in APM's list, `~/.apm/apm.yml`, so that a later install or update
does not remove what it put there. uv may warn that its tool folder is not on the PATH; leave it.
**If `add` cannot find the script**, an older package was already installed, and an install keeps
the version it had: run `uvx --from apm-cli==0.33.0 apm update -g --yes`, then the install above
again, then `add`. If `add` exits 1, say why in one line at the opening of step 3's question, and go
on.

**If `clashes` exits 1**, the user already has a skill, command or agent of their own under one of
the package's names: the install kept theirs, left the package's out, and the researcher would run
without it. Before step 3, ask one question, header `Same name` (`Mismo nombre`), the names it
printed in place of `<names>`: *You already have your own `<names>`. I kept yours, so mine weren't
installed. Rename yours to `<name>-mine` so both work?* (*Ya tienes tus propios `<names>`. Dejé los
tuyos, así que los míos no se instalaron. ¿Renombro los tuyos a `<name>-mine` para que funcionen
ambos?*) — *Rename mine (recommended)*, described as *yours keep working under the new name;
nothing is deleted*, and *Keep mine as they are*, described as *the researcher works without those
parts*. On *Rename*, run the same script's `keep-mine <the assistant you are>`, the install above
again and `clashes` once more, without asking. When `clashes` exits 0, nothing is said about it.

Every command that runs APM names `apm-cli==0.33.0` itself; *Troubleshooting* below says why,
and what to do if the install fails. **The package is not the researcher yet:** never report the
install on its own. Go on to step 3 in the same turn — after the `Same name` question, when there
is one — and let your next message to the user be step 3's first question, opening with one line:
*The package is installed; now your researcher.*

## Step 3 — The researcher's name, and where it lives

**A researcher brought back.** When the user asked to bring one back — the README's second line, or
in their own words, *I have one on GitHub*, *it's a new computer* — nothing is made: follow the
`backup` skill's *Step 10* from its clone, in this conversation. It asks for the copy's address,
clones it into a short folder and runs `update` there, which sets this computer up from the home's
`settings.yml`; then hand over as *Use <Name>* below does. Steps 4 and 5 are skipped: the home and
its interview came back with it.

First look in `$HOME/.apm/apm_modules/_local/` for a home already made — a folder with a filled
`RESEARCHER.md` — and at a researcher's skill loaded in this session, which names its home. With
one, follow *One researcher per person*, below: it asks whether to use it, unless the user already
asked for another. Otherwise read `init-researcher` now, in the same turn, and follow it from its
step 2, with the language already chosen; its file is
`$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/SKILL.md`, and its
own questions take the name, then the place and the go in one. If the file is not there, list
`$HOME/.apm/apm_modules` to find it; if it still cannot be found, say so in one line and offer to
install again.

## Step 4 — Make the home

`init-researcher` goes on, on that go, in the same turn: it skips its update, copies the
researcher's home with `scaffold.py`, its first version saved, and goes straight into step 5. Never
end the turn after the copy: what the user reads next is the interview's question 1, one open chat
message with no options. A folder the script refuses is `Where?` again, with the reason, never a
stop.

## Step 5 — The interview

Read the whole `interview` skill from its installed path and follow it in the same turn as step 4,
from its *Step 1*, with the new folder as the home, by its absolute path, whatever folder the
session is open in. It asks two questions about the user — what they do and the projects and topics
they will work on, then the researcher's voice — in the user's language; what they are here for,
the domains and the projects are proposed from what they say. Nothing about how they invest is
asked here. It writes `RESEARCHER.md`, the agent that makes the researcher callable by name and the
skill that puts it in every session, installs them for the user and saves a first version — the
user answers the two questions, and nothing more is asked before the hand-over.

## Step 6 — Hand over

The interview's own hand-over ends the conversation: who the researcher is and that it is in every
folder, where its home is, then one question, `First step`, which recommends a first document — put
in the home's `Sources` folder, or attached. On *I have a document*, follow `read` from its
installed path, in this conversation. Only at the end, once that is done or put off: what the user
can ask it for — one short line a use, and a link to `USE-CASES.md` — the one next thing for what
they came for, and *not sure what's next? say `next`*.

**What "done" looks like:** the home holds `RESEARCHER.md` with no angle-bracketed slot left,
`.apm/agents/<slug>.agent.md` and `.apm/skills/<slug>/SKILL.md`, and everything is saved:
`git status` is clean. The researcher reaches the assistant in use when this exits 0; it prints one
line for each file missing:

```bash
uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py" check <the assistant you are> <slug>
```

On Claude Code, `$HOME/.claude/skills/` also holds `init-strategy`, `read`, `query`, `interview`,
`philosophy`, `brief` and `backup`, and `$HOME/.claude/agents/` holds `blueprint-critic.md`.

---

## Later

**The user's philosophy, and a daily brief.** In a new session in the home: `philosophy`, a second
interview on how they work or how they invest — investing at their level — and `brief setup`, which
schedules the brief on the Claude desktop app and says how to run it elsewhere.

**A strategy.** In a new session in the home: `init-strategy fcf-yield-quality`. It makes the
strategy's folder beside the home, from the KaxaNuk Strategy Template; open that folder in a new
session, and its own `SETUP.md` builds the environment and the keys. `init-example` copies a
finished strategy to read first.

**Updating.** `update`, in the home, brings every new version: the package, with
`uvx --from apm-cli==0.33.0 apm update -g`, to every folder at once, then what changed in the
home's own files. Always with `-g`: a bare `apm update` outside an APM project updates APM itself.

**Another assistant.** Step 2 with the new target, which adds it to APM's list; then install the
home, once, the assistant added under `targets:` in the home's `apm.yml` first, OpenCode aside:
`uvx --from apm-cli==0.33.0 apm install -g "<the home>"`; then the done check's `check`, with that
target. `update`, in the home, does this for every assistant its `settings.yml` lists.

**A new machine.** Steps 1 and 2, then the researcher brought back, as step 3's first paragraph
says: nothing is made again.

---

## Troubleshooting

**What each assistant receives.** Claude Code receives everything: the skills, the commands, the
agents and the three instructions, which land in `~/.claude/rules/` — Bloom Code and PEP 8 for
Python in a KaxaNuk repository, and nowhere else, and filesystem boundaries, in any project, for
every file the assistant reads: outside the folder it works in, only the places the task needs.
Copilot receives the same, its instructions as files in `~/.copilot/instructions/`. Cursor, Gemini,
OpenCode and Windsurf get the skills and the commands but not the instructions, and Gemini and
Windsurf take no agent: there the researcher is its skill. OpenCode takes the package but not the
researcher's own agent and skill: it rejects the agent APM writes for it, so the home's `apm.yml`
leaves it out of `targets:`; APM's hint to run `apm compile` is printed for OpenCode alone.
**Codex gets the skills and the agents, and no commands.** The skills land in `~/.agents/skills/`
and each agent in `~/.codex/agents/<name>.toml`, without its tool list: APM warns that it drops
it, so on Codex an agent has no tool boundary. No instruction lands either. So the steps a newcomer
needs — `init-researcher`, `interview`, `next`, `read`, `query`, `philosophy`, `brief` — are all
skills. A command, such as `objective` or `blueprint`, is run there by naming its file — *follow
`$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/prompts/objective.prompt.md`* — and once
the interview has run, the researcher's own skill does this for the user: they name the command,
and it follows the file.

**Why APM is pinned at 0.33.0.** APM 0.33.0 installs this package cleanly, on Windows too. APM
0.29.1 to 0.31.0 staged every package under long folders, and on Windows the worked example's
longest paths passed the 260-character limit: the install failed with `WinError 3` or
`WinError 206`. APM 0.32.0 shortened them (microsoft/apm#2941). A version is adopted only once the
package's release check passes with it on Windows, so the pin is written into every command that
runs APM. `uv tool upgrade` keeps it.
**Never run `apm self-update`**, nor a bare `apm update` outside an APM project, which forwards to
it: both bring the newest APM back. A machine on any other APM runs the same
`uv tool install apm-cli==0.33.0` over it. If `apm` typed by hand is *command not found*,
`uv tool update-shell` and a new terminal fix it, after the setup: every command here runs through
`uvx` and does not need it.

**On Windows, if the install fails with *checkout failed*,** git itself went past the
260-character limit. Let git use long paths, once, then install again:

```bash
git config --global core.longpaths true
```

**What installing the home copies.** `uvx --from apm-cli==0.33.0 apm install -g "<the home>"`,
which the interview runs, copies the whole home — `.git/`, `Sources/`, `Extracts/`, `Briefs/` and
`Portfolio/` included — into `~/.apm/apm_modules/_local/<the home's folder name>/`, on the same
machine, and deploys only its `.apm/`: the researcher's agent and skill. Nothing leaves the
machine, and each install refreshes the copy. On Windows a deep path in that copy, such as a long
slug under `Extracts/`, can pass the 260-character limit and fail the install. The fix is a
shorter path for the home, or fewer deep extracts: `Extracts/` is a cache, which `read`'s script
makes again from the source.

**On Windows, `git diff` prints a CRLF warning** for the files the researcher wrote; it is expected
and harmless — `.gitattributes` normalises them on commit.

**One researcher per person.** A home already made — a folder with a filled `RESEARCHER.md`, copied
into `$HOME/.apm/apm_modules/_local/` when it was installed, or the home a researcher's skill loaded
in this session names — is used, not made again: one library, grown in one place. Say where it is in
one line — read its path from the description of the researcher's skill in that copy,
`.apm/skills/<slug>/SKILL.md`, and ask the user only when it is missing; <Name> below is the *Name*
in its `RESEARCHER.md`. Unless the user already asked for another — *a test researcher*, *a second
one*, *another one*, in any words — ask once, through the question tool, `Another?` (`¿Otro?`):

- *Use <Name> (recommended)* — run step 2 for this assistant, if this conversation has not run it,
  install the home and run `check` as *Another assistant* says, and hand over:
  who and where, as the interview's hand-over says it, and *say `next`*;
- *Make a second one* — a test, or another person on this computer: a second library, and a second
  researcher in every session until it is removed — then `init-researcher` from its step 2, as step
  3 says, the interview included, under a name other than <Name>;
- *Stop*.

When the user already asked for another, ask nothing: `init-researcher` runs from its step 2, under
a name other than <Name>, and its `Where?` says once, in *Go*'s description, that the new home will
sit beside <Name>, a second researcher in every session until it is removed. *Use <Name>* is how a
researcher an assistant lost comes back: paste the README's line in that assistant again.

APM's own reference, for any error it prints: <https://microsoft.github.io/apm/llms.txt>.
