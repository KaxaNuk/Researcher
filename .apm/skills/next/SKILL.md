---
name: next
description: >
  Say where the owner stands — in the researcher's home or in a strategy — and the one thing to do
  next, with the command or skill that does it, read from the files on disk as a checklist; at most
  once a week, one line more when a new version of the researcher, or in a strategy of a Lab
  library, is out. Nothing is written but a version the owner picks to save, in part E a late read-back entry on the
  owner's go, and the dates of that weekly check, in git config, never saved or sent anywhere. Takes an optional path to a strategy,
  when the session is not open in it. Only when the owner runs it by name, when the researcher's
  skill answers a greeting, or when the owner answers its version line — not now, stop reminding
  me, remind me about updates; never on its own otherwise.
metadata:
  version: 1.10.1
---

# Next — where you stand, and what to do next

This skill is the map of the process and of the researcher's skills and commands: it reads the
folder, says which parts are done, and names **the one thing to do next** with the command or skill
that does it. It never starts that thing itself — doing it is a different request, by the name
given — and writes only what its last paragraph lists. It is a skill, not a command, so every
assistant APM deploys to has it, Codex included.

Every path below is relative to the folder being read. That folder is a strategy's path when the
owner gives one — *next ../fcf-yield-quality* — because the session is not open in it. It is the
home, at the path the researcher's skill names, when *Step 1* reads *Step 2* from a project the
researcher joined; otherwise, the folder the session is open in. Rows 0 and E run every git
command there, the `backup` skill's send included, as `git -C "<the folder being read>"` when the
session is open elsewhere.

## Step 1: Which folder this is

| It holds | It is | What follows |
| --- | --- | --- |
| `Bibliotheca/`, `Universe/` and `Experiments/`, and the line `<!-- example: begin -->` alone at column 0 in `README.md` or `AGENTS.md`, which a strategy from the template never has: its README quotes the marker inside backticks, which does not count | the worked example, made by `init-example` | say so, and quote its status line, which says how far it went: it is for reading, never built on; a strategy of the owner's own is `init-strategy <name>`. No part of *Step 3* is offered |
| `Bibliotheca/`, `Universe/` and `Experiments/` | a strategy | *Step 3* |
| `RESEARCHER.md` | a researcher's home | *Step 2* |
| `.apm/skills/init-strategy/` and `templates/` | the KaxaNuk Researcher package itself | say so: nothing is worked on here; `AGENTS.md` has its rules |
| `AGENTS.md` with the line `<!-- kaxanuk-starting-point: <kind> -->` alone at column 0 | a project from another KaxaNuk starting point, made by `init-<kind>` | say which kind, and quote its status line where there is one; then its `AGENTS.md`'s `## Next` table, read as *Step 2*'s rows are, from the files on disk — the first *Done when* that fails gives *The next thing* — and reported as a strategy's parts are. With no such table, say its `AGENTS.md` governs, and stop |
| none of those, and a home is in the session through `--add-dir`, or readable at the path the researcher's skill names | a project the researcher joined | *Joining other projects* in the home's `AGENTS.md` governs, with the project's own rules. Name the home and its one next thing, *Step 2* read at the home's path; here, `query` answers from the library, and what the project teaches goes home as a source, then `read`. No `init-*` command is suggested for this folder |
| none of those | not a KaxaNuk folder | when a subfolder one level down holds `RESEARCHER.md` or a strategy's three folders, name it so the owner can open it, applying the first row's test, the marker alone on its line, to it: a subfolder that passes it is named as the worked example, for reading, never as a strategy to work in; otherwise say which skill makes one — `init-researcher <name>` once per person, `init-strategy <name>` once per strategy, `init-python-library <name>` for a Python library of their own, `init-example` to read the worked example — and stop |

When a home and a strategy, or a project from another starting point, are both in the session —
added to it, or named by the researcher's skill — read the strategy or the project: the home is the
library it brought along.

## Step 2: At home

Check in this order and stop at the first that fails; that is the next thing. `<slug>` is the
researcher's name in `RESEARCHER.md` made safe for a folder, as `interview` *Step 4* says: accents
removed, lowercase, anything but a to z or a digit a hyphen, hyphens collapsed and none at either
end — `Begoña Ruiz` becomes `begona-ruiz`. In rows 2 and 3 a file or a folder of another name
counts when its `name:` is the one the home's agent carries, so a home already installed is not
sent to install again.

| # | Done when | If not, the next thing is |
| --- | --- | --- |
| 0 | the folder is a git repository — it holds `.git/` — and its working tree is clean: `git status --short` prints nothing, untracked files under `Sources/` aside, which row 5 reports and which do not block | with no `.git/`, say in one line that the home keeps no versions yet, and offer to start them; on the owner's word, run what `scaffold.py` prints to finish a repository — `git init --quiet --initial-branch=main`, `git add --all`, `git commit --quiet -m "Start from the KaxaNuk Researcher template"` — and say *Saved*. Otherwise name the changes made by hand in plain words, file by file — *your note on Fama 1970*, *RESEARCHER.md* — never the commands, and ask `Save?` (`¿Guardo?`): *Save this version*, *Not now*, listed in chat without a question tool. On *Save this version*, `git add` each file by name, never `--all`, then `git commit -m "<what changed>" -- <those files>`, say *Saved* — sent too when `git config --get kaxanuk.autosend` prints `true`, as `backup` says — and go on from row 1; on *Not now*, nothing more. Wanting a name, ask in one open message, with no options, *What's your name, or what would you like me to call you?*, never invented, and no e-mail; set it in that folder only, with `user.email` as `"<>"`, an empty address, and save again |
| 1 | `RESEARCHER.md` has no angle-bracketed slot left. *What you are reading for* with no numbered question is not a slot: the template ships it so, and the first `read` asks for question 1 | `interview` — the interview |
| 2 | `.apm/agents/` holds an agent file named for the researcher, and `.apm/skills/<slug>/` the researcher's skill, its folder named in a to z, digits and hyphens only, whose description names this folder as the home | `interview` again when either is missing: it writes it from `RESEARCHER.md` without repeating the interview; `update` when the skill names another folder — the home has moved — or its folder's name holds anything but a to z, digits and hyphens, such as an accent, which APM deletes on install |
| 3 | the home is installed for the user: its `apm.yml` lists the assistant in use under `targets:`, and `uv run --no-project python "$HOME/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/init-researcher/scripts/user_targets.py" check <the assistant in use> <slug>` passes (under `KaxaNuk/KaxaNuk-Researcher/` for an install from before 1.25.0), `<slug>` the `name:` the home's agent carries — never `apm deps list -g` alone, which still counts files APM has deleted. On OpenCode, which the home's `apm.yml` leaves out, the check passes, with one line: the researcher's own skill does not reach OpenCode | `update`, when the home's `apm.yml` does not list the assistant in use under `targets:` — it proposes the line and installs again; otherwise the same script's `add <the assistant in use>`, `uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher --target <the assistant in use>`, `uvx --from apm-cli==0.33.0 apm install -g "<this folder>"`, then a new session; a copy still in this folder's `.claude/agents/`, from before the user-scope install, is `update`'s to remove |
| 4 | this place matches `settings.yml`, read with the file tool, in what it names — an empty value or list names nothing yet, which a new home's does: the file exists; an `assistants:` that lists any assistant lists the one in use; each connector under `brief: connectors` is one this session holds; on the desktop app, a `brief:` whose `parts` are not empty has this home's task in `list_scheduled_tasks`, whose prompt names this home's `Briefs/`; and the home's own git config, `git config --local`, holds a `user.email` and a `kaxanuk.autosend` wherever `versions:` names one — a global `user.email`, which a new computer's setup writes, does not count | `update`, which sets this place up from the file — every assistant it lists, the git settings, the brief through `brief setup` with only its go — and brings the file to a home that lacks it. A connector missing, alone, is not `update`'s: name it with its fix in one line, in the owner's language — in claude.ai, *Settings → Connectors*, connect it; on a company account, an administrator may have to allow it — then `brief setup`, which checks that it reads. After a new account, this is the row that says so |
| 5 | every source under `Sources/` — a PDF, a document or a clipping, not a `.gitkeep` — has a note: `uv run --no-project python "<the read skill's directory>/scripts/unread_sources.py" "<the home>"` lists none as unread. It writes nothing: it matches each file against every note's `local_copy` by its full path, so a comma, a parenthesis or an accent in a name is safe, and it filters by nothing, date included | `read <the first source it lists>`, naming the question it serves; with no numbered question yet, `read <the source>` alone, which asks the owner which question it serves and adds it as question 1. A source it lists beside a note of the same first author and year may be that note's under another path: say so, and its fix is the note's `local_copy`, on the owner's go |
| 6 | every work on a *Find first* line of `RESEARCHER.md` is in `Sources/`, or the owner took it off the line, which is theirs to edit by hand | find it by its title and authors, then attach it or say where it is saved, and the researcher copies it into `Sources/Papers/` or `Sources/Books/` on the go, then `read`; or, when it cannot be found, take it off the *Find first* line in `RESEARCHER.md` |
| 7 | `Knowledge/INDEX.md` lists every note and page on disk | `refresh-index` |

All eight done, the one next thing follows the *Here for* line under *Who* in `RESEARCHER.md`: the
first row below whose pick is on the line and whose thing is not done yet. *Step 1*'s first-row
test, the marker alone on its line, tells the worked example from a strategy of the owner's own.

| Pick | The one next thing | Done when |
| --- | --- | --- |
| *Organise what I read, and help with my projects*, or the older *Organise what I read*, or, with none of the four picks, nothing or only their own words — when *Works for* or the projects table names a project or a decision of theirs, not a strategy | `study <it>` at home, for a decision or a project with no folder of its own; for work in a folder of its own, *open me in that project's folder and say hello*, and its row takes the path when the owner says *remember this: <project> lives at <its path>* | `Studies/` holds a study, or the project's row names its path |
| The same picks, with or without a project | a source into `Sources/` — they attach it or name it, and the researcher copies it into `Sources/Papers/`, `Sources/Books/` or `Sources/Clippings/` on their go — then `read`, which asks which question it serves | `Knowledge/` holds a note |
| *Learn the basics, step by step* | `philosophy investing`, at Starter — it teaches one idea after each answer and needs no reading | a round on investing — a level, not `Field`, on its first line — exists in `Philosophy/Evolution/` |
| *Write down how I invest, and see it evolve* | `philosophy investing`; once a round on investing exists, `brief setup`, for a daily brief of the markets and holdings they follow, leads the *also* line until `Briefs/` exists | a round on investing — a level, not `Field`, on its first line — exists in `Philosophy/Evolution/` |
| *Build and test a strategy* | `init-example`, a finished strategy to read — `OBJECTIVE.md`, `RESULTS.md`, Experiment 1 — that needs nothing installed; running it takes a data key, a download of about an hour and a half, KaxaNuk's benchmark and factor files and licences, as its `SETUP.md` says. Then `init-strategy <name>` for their own | a folder beside the home holds `Bibliotheca/`, `Universe/` and `Experiments/`: the example alone → `init-strategy <name>`; a strategy of their own → done, and `next <its path>` leads the *also* line |

When every pick's thing is done, the one next thing is the second row's while `Knowledge/` holds
no note yet. Once it holds one, it is the first of these whose pick is on the line — *Learn the
basics*, `teach <topic>` on a topic the notes cover; *Write down how I invest*, a new source, and
`philosophy investing` again once a note read since its last round is a work the *Bears on* table
lists, as *Step 4* item 4 says; *Build and test a strategy*, `next <its path>`; the rest, a new
source, or `query`. Up to three more on one line as *also*: a question added under *What you are
reading for*, `study <subject>` to work out an idea from the library — `study` alone lists the
studies — `teach <topic>`, `brief setup` for a daily brief, `init-strategy <name>`, or teaching it
a tool: its documentation into `Sources/Clippings/`, then `read` — *Growing your researcher* in the
home's README. Philosophy is never a row that fails: for the other picks, *Step 4* may close with
it in one line.

## Step 3: In a strategy

Two things come before the order of work. **Setup:** `.venv/` exists, `Config/.env` exists — never
open it — and `README.md` is the strategy's own, not the template's, whose first line is
*KaxaNuk Strategy Template*. Any of those missing, the next thing is the strategy's `SETUP.md`,
from the step that failed. **The status line** at the top of `README.md` and `AGENTS.md`, which the
owner keeps current; quote it.

The commands assume the KaxaNuk Strategy Template's paths; a strategy made from another template
keeps or maps them in its own `AGENTS.md`.

Then the order of work — *Starting your own strategy* in the template's README, A to H — read from
the files. Check in order and stop at the first part not done; that is the next thing. Data and
engine outputs are gitignored, so a check on them says *on this machine*: a fresh clone shows them
empty after the work was done.

| | Part | Done when | If not, the next thing is |
| --- | --- | --- | --- |
| A | The objective | `OBJECTIVE.md` has a main idea in the owner's words and at least one claim in its table that is not the template's italic guidance | `objective` — from the owner's words, before any paper |
| B | The reading | every claim's evidence is one of three kinds — a note in `Bibliotheca/` by relative path, with a row in `BIBLIOGRAPHY.md`; `RESULTS.md` or the `FINDINGS_N.md` that measured it; or the claim is **true by construction** — or the owner has recorded the claim's evidence in `OBJECTIVE.md` as a lead carried into the blueprint, where E counts it; a claim that still names only the question that would settle it is a lead | `read <source>` for the first claim without a note, then `objective` again to rewrite its evidence from the notes |
| C | The universe | `Universe/Investable_Universe.csv` has rows under `main_identifier` | fill the seed, delisted names included — the `universe-point-in-time` skill says what belongs in it |
| D | The data | on this machine: `Data/Curator/Time_Series/` has files, `Universe/Security_Master.csv` exists, `Data/Refinery/Time_Series/` has files; and `RESULTS.md` has a measurement under *Before any experiment* with the analyzer section it came from | the first of `Data/curator.py`, `Universe/universe.ipynb`, `Data/refinery.py`, `Data/analyzer.ipynb` whose output is missing, in that order — `data-curator-custom-calculations`, `universe-point-in-time`, `data-analyzer-runs` |
| E | The blueprint | `JOURNAL_1.md` has the entry choosing the benchmark — in a strategy that still keeps `BRAINSTORMING_1.md`, its first entry counts; `JOURNAL_N.md` has the entry *the rule read back*, dated no later than the blueprint's *Written* line and saved before it — a blueprint stamped with a package before 0.39.0, or with none, counts without it, said in one line; one stamped later, saved without it, counts once the entry is appended and saved after it, as the last column says; `Experiments/Experiment_N/BLUEPRINT_N.md` carries the line `blueprint` writes under the experiment's heading, `**Written YYYY-MM-DD, before any rule was coded.**`, and every prediction names a note or an analyzer section, and it is saved as a version of its own before the rule cell of `experiment_N.ipynb` holds code | the benchmark, chosen with the owner in chat and appended to `JOURNAL_1.md` on their go, when that entry is missing; else `blueprint N`; else the read-back entry, when it is not saved yet, then the blueprint, each saved alone, before the rule — on `blueprint`'s go, or here on *Save this version*, asked and said as row 0 does: `git add` each, then `git commit -m "Experiment N: the rule read back" -- Experiments/Experiment_N/JOURNAL_N.md` and `git commit -m "Blueprint N, before the rule" -- Experiments/Experiment_N/BLUEPRINT_N.md`; a blueprint already saved without the read-back: the entry alone, drafted now from its *Rules* as `blueprint`'s *Step 5* reads a rule back, appended on the owner's go and saved by the first of those commits, and E passes with one line saying it came after the blueprint; a *no* is a new experiment, since a saved blueprint never changes |
| F | The broad reading | the leads the blueprint counted are read or recorded as leads in `BIBLIOGRAPHY.md` | `read` for the first lead |
| G | The cycle | section 2 of `experiment_N.ipynb` holds the rule; on this machine `Portfolio/`, `Backtest/` and `Attribution/` hold output; `FINDINGS_N.md` reports, every prediction of the blueprint evaluated | the first of `portfolio-construction-runs`, `backtest-engine-runs`, `attribution-analysis-runs` whose output is missing; `alpha-decomposition` to read it; then `challenge N` once `FINDINGS_N.md` reports. When the engine or the attribution library is not installed, which the notebook's guarded import reports, say the step is skipped for want of a licence and give the access line of `references/investment-lab.md`, in this skill's folder, naming that library; when attribution is installed and reports its index or factor files missing instead, that file's Analytics Factory line. Then move on to what can still be done — `FINDINGS_N.md` for the book, and the journal's open threads |
| H | The results | `RESULTS.md` has the experiment's row citing `FINDINGS_N.md`; the claim has moved — where `BLUEPRINT_N.md` names one under *The claim this moves*, `OBJECTIVE.md` gives that claim the status `FINDINGS_N.md` says it reached, and so does the row's *Claim moved* where `RESULTS.md` has that column; where the blueprint names none, the statuses in `OBJECTIVE.md` of the claims it tests have moved; and `CHANGELOG.md` has the entry | the missing one of those three |

A to H done for the newest experiment: the next thing is either the gate —
`Paper_Trading/BITACORA.md`, the `paper-trading-gate` skill — when the owner believes the findings
evidence its first criterion, or Experiment N+1, as section 6 of `experiment-lifecycle` says,
starting again at E. The objective, the universe and the data are the strategy's and stay.

## Step 4: Report

In chat, short:

1. **Which folder this is**, and the status line where there is one.
2. **The checklist**: in a strategy, a table — each part, done or not, with the file that says so;
   at home, one line when rows 0 to 7 pass, *setup: all good*, else the failing row alone.
3. **Next:** one line — the part, the command or skill by name, and what it will ask for; any
   *also*, one line after it.
4. **Your philosophy**, at home only, one closing line, offered and never pressed; left out when
   *Next* names `philosophy`. With no round file in `Philosophy/Evolution/`, when *Domains* holds
   Finance or *Here for* holds *Learn the basics*, *Build and test a strategy* or *Write down how I
   invest*: *`philosophy` writes down how you invest, in your words, at your level, and sets the
   rules I keep with you — round 1, whenever you like.* Otherwise: *`philosophy` writes down how you
   work, in your words, and sets the rules I keep with you — round 1, whenever you like.* With one
   or more: the latest round's date, of either topic, and its level or *field* — the newest file
   name, `YYYY-MM-DD-2.md` after `YYYY-MM-DD.md` — and how many notes came in since. Those are the
   notes the `read` entries of `Knowledge/LOG.md` dated on or after it — a read the same day counts
   — list as written, a book's `INDEX.md` and concept pages aside. With no notes since, end with
   *no notes since*. When notes came in, add that `philosophy` takes the round again — for a round
   on investing, only when one of them is a work the *Bears on* table of `philosophy`'s
   `references/questions.md` lists, matched as the reading map's *Match before proposing* says.
5. **A new version**, last, and only when there is one: never a line saying there is none. It
   updates nothing itself, and a failure — offline, a command failing or declined — is silent.
   Every line here is in the owner's language.
   - **Due?** The home is this folder when it is one, else the one the researcher's skill names,
     wherever `next` runs; none readable, or no `.git/` in it, means no check. Read
     `<home>/.git/config` with the file-reading tool, never a shell, so a week with nothing due asks
     no permission: under `[kaxanuk]`, `updatereminder = off` is never; an
     `updatenext = YYYY-MM-DD` after today is not yet; none, today or past is due.
   - **Installed:** in `~/.apm/apm.lock.yaml`, read the same way, the `version:` of the entry under
     `dependencies:` whose `repo_url` or `materialization_repo_url` is `KaxaNuk/Researcher`, or
     `KaxaNuk/KaxaNuk-Researcher` for an install from before 1.25.0, ignoring case, never a
     `source: local` one; with none, no line, and *Then* still sets the date.
   - **Newest:** the first tag this prints, as written in Git Bash; in PowerShell, put
     `$env:GIT_TERMINAL_PROMPT=0;` in place of `GIT_TERMINAL_PROMPT=0`:

     ```bash
     GIT_TERMINAL_PROMPT=0 git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=10 ls-remote --tags --refs --sort=-v:refname https://github.com/KaxaNuk/Researcher
     ```

     Only a newer minor or major version counts — 0.37.0 over 0.36.x, 1.0.0 over 0.x — never a
     patch alone.
   - **Headline**, when one is newer, and only if it comes: this prints the top of that version's
     changelog entry, given it without the `v`, the same in Git Bash and in PowerShell with
     `[Console]::OutputEncoding = [Text.Encoding]::UTF8;` first. Its first sentence is the headline.

     ```bash
     uv run --no-project python -X utf8 -c "import sys, urllib.request as r; L=r.urlopen('https://raw.githubusercontent.com/KaxaNuk/Researcher/main/CHANGELOG.md', timeout=10).read(65536).decode('utf-8', 'replace').splitlines(); i=[k for k, x in enumerate(L) if x.startswith('## [' + sys.argv[1] + ']')][0]; print(*L[i:i + 12], sep=chr(10))" <that version>
     ```

   - **The line:** *A new version of me is out, X (you have Y): <headline>. Say `update` when you
     like — `not now` waits a month.* With no headline, the same without it.
   - **Then**, after a due check, a line or none — so a failure costs one silent try a week — run
     `git -C "<home>" config kaxanuk.updatenext <today + 7 days>`, the date as `YYYY-MM-DD`. When
     the owner answers, then or later: *not now* sets it to today + 30 days; *stop reminding me*
     runs `git -C "<home>" config kaxanuk.updatereminder off`; *remind me about updates* runs
     `git -C "<home>" config --unset kaxanuk.updatereminder`.
   - **The researcher's skill behind the package**, on every `next` wherever the home is readable,
     never gated by the date or the network. When the home's skill, row 2's file, has a
     `metadata.version` below the `version:` of the skill template in `interview`'s *Step 4* —
     `~/.apm/apm_modules/KaxaNuk/Researcher/.apm/skills/interview/SKILL.md`, under
     `KaxaNuk/KaxaNuk-Researcher/` for an install from before 1.25.0, not that file's own — one
     line: *Your researcher's skill is behind the package — say `update` to bring it.*
   - **In a strategy, the Lab libraries too**, never in the worked example. The same rules, on the
     strategy's own date, `[kaxanuk] labnext` in `<strategy>/.git/config`, written with
     `git -C "<strategy>" config kaxanuk.labnext <date>`; the home's `updatereminder = off` stops
     it too. Not due without `.venv/`, nor while an experiment is under way — its blueprint saved,
     as part E checks, and no `FINDINGS_N.md` reporting yet, as part G does — since one experiment
     runs on one set of builds; then nothing is written. From the strategy's root, both read-only:

     ```bash
     uv pip list --format freeze
     uv lock --upgrade-package kaxanuk-data-curator --dry-run
     ```

     The first, read for the `kaxanuk-*` names and versions only, gives each installed build; the
     second names a newer Data Curator — `Update kaxanuk-data-curator v0.50.0 -> v0.51.0` —
     without writing the lock. Each Lab library installed is compared, minor and major only, with
     the *Latest* column of `references/investment-lab.md` in this skill's folder — a newer build
     is out — and with its skill's `library_version` — the skill's traps were checked on another
     build. One line per library behind:
     - The Data Curator: *Data Curator X is out (you have Y): between experiments,
       `uv lock --upgrade-package kaxanuk-data-curator`, then
       `uv sync --group notebook --inexact`.* Where `Paper_Trading/` holds a `FREEZE.json`, add:
       *a book on paper stops on any other Data Curator than its frozen one.*
     - Portfolio Construction, the Backtest Engine or Attribution Analysis: *<Library> X is out
       (you have Y): between experiments — its skill says how to install a new build.*
     - A build newer than its skill's `library_version`, with nothing newer out: *Your <Library> is
       Y; its skill was checked on Z, so its traps are unproven on Y.*

Nothing else. No log entry is appended, no number computed and no plan drafted: when the owner says
*do it*, that is the named command's or skill's own plan and go, not this one's. It writes only row
0's and row E's saves, on the owner's pick, row E's late read-back entry, on the owner's go, and
item 5's dates in git config, which are never saved or sent anywhere.
