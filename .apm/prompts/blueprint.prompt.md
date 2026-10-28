---
description: Draft BLUEPRINT_N.md in place for a strategy, once its objective has claims and its investable universe exists — thesis, rules, predictions — with every prediction citing a Bibliotheca note or an analyzer measurement, the draft put to a critic and its rule read back to the owner on one worked date; plan first, the owner's go, then write, before the rule. Only when the owner runs it by name, on a strategy they name or are working in.
input:
  - experiment: "The experiment number N"
  - strategy: "Optional: path to the strategy repository, if not the one the session is in"
---

# Draft a blueprint

Every path below is relative to the researcher's home — the folder that holds `RESEARCHER.md`. Find
it first and read its `RESEARCHER.md` and `AGENTS.md`. In a strategy — the session is open in a
repository with a `Bibliotheca/`, or the owner named one by path — *Working in a strategy* in
`AGENTS.md` says where each of these paths lands. With no home in the session, work from the
strategy alone, with no library contrast, and say so.

The blueprint is the hypothesis, fixed once written, recorded before the notebook's rule cell
exists. This command drafts it so that every prediction can be traced to something read or
measured, and writes it where the template keeps it. `${input:experiment}` is the experiment number
`N`; `${input:strategy}` is the strategy's path, given when the session is not already open in it.

## Step 1: Refuse if the order is wrong

The blueprint is E in *The order of work* in `AGENTS.md`. Stop, and name the part that comes
first, when:

- **The folder is the worked example** — its `README.md` or `AGENTS.md` holds a line reading
  `<!-- example: begin -->`, the test `next` uses. The example is for reading and running, never
  built on; a strategy of the owner's own is `init-strategy <name>`.
- **`OBJECTIVE.md` has no claims** — the objective comes first, and its claims fine-tuned by reading
  for them: `objective`, then `read`.
- **`Universe/Investable_Universe.csv` has no identifier under its header** — the investable
  universe comes before the hypothesis about it.
- **`Experiments/Experiment_N/experiment_N_marimo.py` already holds a rule in its section 2** — a
  hypothesis written after its test is not a hypothesis.
- **`BLUEPRINT_N.md` is already filled** — it carries the line this command writes under the
  experiment's heading, `**Written YYYY-MM-DD, before any rule was coded.**` It does not change once
  written; a new idea is Experiment N+1.

**For Experiment 1 the blueprint is already there to fill.** The template ships
`Experiments/Experiment_1/BLUEPRINT_1.md` as the headings and what belongs under each. Never write
the headings from memory — they are the template's. A strategy made from a template before 0.10.0
lacks the file: say so, give the command that brings the template's blank back, run from the
strategy's root, and stop. It never overwrites:

```bash
uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" strategy . --only Experiments/Experiment_1/BLUEPRINT_1.md
```

The owner runs it, and the draft continues from there.

**For N > 1 there is no file yet.** The blank is the `experiment-lifecycle` skill's
`references/blueprint-template.md` — the example's file with its own lines stripped — copied to
`Experiments/Experiment_N/BLUEPRINT_N.md` with `N` replaced, as that skill's section 6 says, and
`references/journal-template.md` the same way when `JOURNAL_N.md` is missing, for the read-back's
entry. Offer the copy as the plan, make it on the owner's go — it is saved with the blueprint, in
*Step 5* — and the draft continues from there.

## Step 2: Read, in this order

1. `OBJECTIVE.md` — the claims this experiment tests, by number.
2. `AGENTS.md` in the strategy — *The bar any new signal must clear*. Read it, not a memory of it:
   a strategy may have changed it, and the predictions and the rules answer to it.
3. The strategy's `Bibliotheca/` notes, through `BIBLIOGRAPHY.md`, and which sources are still
   leads.
4. `RESULTS.md`, section *Before any experiment*, and anything in `Data/Analyzer/` — the
   measurements the analyzer has already made about the signal. The data comes before the blueprint
   in the order of work, so if that section is still the template's prose, say so in the plan and
   write every prediction that needed a measurement as a lead — *run analyzer section Y before
   predicting this*. Probe `RESULTS.md` first, not the folder: `Data/Analyzer/` is ignored by git,
   so a fresh clone has it empty even after D, the data, was done.
5. `Experiments/Experiment_N/BLUEPRINT_N.md` as shipped — the headings to fill — and for N > 1,
   `FINDINGS_1.md` (Experiment 1 is shared context) but **no other experiment's files** unless the
   owner has written the request and reason into `JOURNAL_N.md` first. Say so if they have not.
6. The home library, for the domains the thesis touches, and the owner's `Philosophy/` — as
   contrast and warning, never as a citation. Round files in `Philosophy/Evolution/` are a record
   of how the owner's answers moved: read them for dates and levels, and cite `HOW-I-INVEST.md`,
   never a round file, as the owner's view.
7. The reading map, `references/reading-map.md` in the `read` skill's folder — *Seven questions
   before any backtest* and *An idea's anatomy* — as questions to put to the owner, never as a bar
   the draft is held to.

## Step 3: Draft, in the file's own shape

Under each heading, the draft replaces the template's guidance paragraph: what belongs there gives
way to what does. The example's blueprint keeps the guidance only because its own lines are marked
as the example's.

- **Thesis** — one paragraph, modest on purpose, naming the economic mechanism. Before drafting it,
  put the map's seven questions before any backtest to the owner, once, in chat, as questions they
  may answer or skip: why the edge exists; who is on the other side, and why they keep losing; risk
  premium or mispricing, and which they mean to own; how many independent bets a year; whether it
  survives costs, and how much capital it takes; when it fails, and whether they would hold it
  through that; how many ideas came before this one. The thesis draws on what they answer — the
  map's test is that the seven answers fit in one paragraph — and a question they skip is left
  out, never answered for them, and named again in *Step 5*. The bar in `AGENTS.md`, not these
  seven, is what the draft must meet.
- **The claim this moves** — one claim of `OBJECTIVE.md`, by number, and the status it reaches if
  the predictions hold and if they fail.
- **Rules** — selection, sizing, cash, timing, lag, the control, screens deliberately absent — each
  naming the column it reads and the shared module that implements it. The control differs from the
  book in exactly one ingredient and trades on the rule's own rebalance dates.
- **Predictions** — the table the template gives. **Every row's *where it comes from* is a note in
  `Bibliotheca/` or an analyzer section with its number.** A prediction with neither is written as a
  lead — *read X, or run analyzer section Y, before predicting this* — and counted separately.
  Each row says what would falsify it.
- **Success criteria**, **what would falsify it** — one condition for the whole experiment, and the
  changes that may not rescue it — **key risks** and **open questions this experiment does not
  answer**, in the template's terms. For Experiment 1, what it has to beat is the benchmark
  `JOURNAL_1.md` chose — or, in a strategy that still keeps `BRAINSTORMING_1.md`, the one its first
  entry names.
  For the falsifying condition, ask the owner for the kill switch — the result that would make them
  drop the idea rather than tune it, the map's *An idea's anatomy* — or propose the one the claim
  already carries in `OBJECTIVE.md`; the condition names it, in their words. With none given, the
  drafted condition stands, labelled as the kill switch for them to confirm, change or refuse.
- Add one line under the experiment's heading, with today's date, as the example's blueprint does:
  `**Written YYYY-MM-DD, before any rule was coded.**` — and after it, on the same line, the
  package the draft was made with: `Drafted with KaxaNuk-Researcher X.Y.Z, commit abc1234.` Read
  both from the entry under `dependencies:` in `~/.apm/apm.lock.yaml` whose `repo_url` or
  `materialization_repo_url` is `kaxanuk/kaxanuk-researcher`, ignoring case, as `next` reads it:
  its `version`, and the first seven characters of its `resolved_commit`. A `source: local` entry
  counts only when its `local_path` holds `templates/researcher/`, the package's own checkout,
  never a home. Installed from a local path, the entry has no commit: write `local` in its place.
  With no such entry, read `version:` in `~/.apm/apm_modules/KaxaNuk/KaxaNuk-Researcher/apm.yml`
  and write no commit; with neither, write `version unknown` and say so in *Step 5*. Never a
  version from memory: the stamp is how `challenge` tells whether the process changed between the
  blueprint and its run. The template's blockquote stays, whole, until the go.

## Step 4: Put the draft to its critic

The blueprint does not change once written, so its weak spots are found now, not at `challenge`.
Where the assistant can call a subagent and the `blueprint-critic` agent is installed, hand it the
draft, the experiment number, the strategy's path and the read-back *Step 5* will show, prepared
now, and bring its objections back to show beside the draft. The critic reads and objects; it
writes nothing, and the owner's go stays the only go. Where the assistant cannot call a subagent,
or the agent is not there, review the draft yourself against the same checklist, and say in
*Step 5* that you did: a second reader would have been better than the hand that drafted it.

The checklist. The agent's objections cover the same ground, grouped their own way, and add two: a
rule that reads data it could not have had on the date, and a tuned parameter with no reason written
beside it. The agent reads only the strategy, so item 6's source against the idea in the home
library is yours to check:

1. **Every prediction's source.** Each row names a note in `Bibliotheca/` that says what the row
   says, or an analyzer section by its number in `RESULTS.md`; a row with neither is written and
   counted as a lead.
2. **Every prediction's falsifier.** Each row says what would falsify it, in terms `FINDINGS_N.md`
   can report; a falsifier with two limbs fires on either.
3. **A prediction worth being wrong about.** A table of things that will obviously happen is not a
   hypothesis.
4. **No performance number without a measurement behind it.** No return, Sharpe or drawdown is
   predicted unless an analyzer measurement supports it.
5. **The bar in the strategy's `AGENTS.md`**, item by item: the economic reason stated in the
   thesis; a *Control* line in *Rules* that differs from the book in exactly one thing and trades on
   the rule's own rebalance dates (item 9); a trial count, if variants will be ranked (item 3);
   results net of the costs the rules declare; each parameter chosen on a property of the signal,
   never on the metric it will be judged by; one condition under *What would falsify it* and the
   changes that may not rescue it (item 10); for any coefficient or ratio a prediction leans on, its
   horizon and overlap, and the share of dates with the expected sign beside it (item 11).
6. **The source against the idea.** The thesis or the key risks name what argues against it, when
   the strategy's `Bibliotheca/` or the home library holds it.
7. **The claim this moves.** One claim of `OBJECTIVE.md`, by number, and the status it reaches
   either way.
8. **The rule read back.** The sentence and the worked date's book of *Step 5* follow from *Rules*
   as drafted: every name held, its rank and signal, and the edge, explained by the rules and
   nothing else; with no refined panel yet, the sentence alone, the worked date named as owed.

## Step 5: Show, wait, then write

Show the draft in chat, the critic's objections beside it — each with what the draft does about it,
changed or kept and why — or the line saying the command reviewed it itself. Then list: the leads
(notes to write first), the predictions the owner should be willing to be wrong about, the analyzer
sections still to run, the seven questions they left open and whether the kill switch is theirs or
still the draft's, and **anything the bar in `AGENTS.md` asks for that the draft does not have**
— a control differing in exactly one thing on the rule's own dates, a trial count if variants will
be ranked, the one falsification condition — so the owner meets now what graduation will ask, not at
the gate.

**Read the rule back**, because code can follow a blueprint faithfully and still not be the book its
owner meant. The rule in one plain sentence, in the owner's words where they gave them, then one
worked date's book, for a date inside the window, from the refined panel the data step already
wrote, `Data/Refinery/Time_Series/`. Show the names the rule would hold that day, each one's rank
and signal value, and why the last name in and the first name out fall where they do. Reading the
panel is allowed; writing rule code is not, in the notebook or in any file. The worked date is
read, not built: one query run in the shell and never saved, which takes that date's rows of the
panel, filters and sorts them as *Rules* say, and quotes each name's signal value and its rank in
that column from the files. No weight, return or other figure about the book is stated: where the
count depends on the sizing, the edge is explained in words — which bound stops the book — and the
weights are left to the rule cell. **Where *Rules* name a no-trade band, read the band back beside
the rule**, on the worked date and the rebalance before it: the names held on both, and which of
them the band leaves as they drifted and which it trades — named, not weighed, read from the panel
the same way and never coded into the notebook. Ask *Is this the book you mean?* A no is a new
draft of *Rules*, back through *Step 4*. On yes, the plan adds a `JOURNAL_N.md` entry, *the rule
read back* — the sentence, the worked date's book, the band where there is one, and the owner's yes
in their words — saved before the blueprint.
With no refined panel yet, read back the sentence alone, and say, in chat and in the entry, that
the worked date is owed before the rule cell.

Wait for the go, described as *sign it, write it and save a version*: it is the owner's
signature. On it, append the read-back entry to `JOURNAL_N.md`, dated today, then write the draft
into `Experiments/Experiment_N/BLUEPRINT_N.md` in the strategy, under the template's headings, and
remove the template's blockquote.

**Then save the entry, then the blueprint, each alone**, in the strategy's folder, on the same go,
**before any rule is coded** — no rule cell, no code, no second question, and no `CHANGELOG.md`
entry, version bump or ruff gate: the next change-set's entry names them. Every git command, the
`backup` skill's send included, runs as `git -C "<that folder>"` when the session is open elsewhere:
`git add` each, then
`git commit -m "Experiment N: the rule read back" -- Experiments/Experiment_N/JOURNAL_N.md` and
`git commit -m "Blueprint N, before the rule" -- Experiments/Experiment_N/BLUEPRINT_N.md`, so
nothing else staged goes with either. To the owner, one plain line, never the commands: *Saved: your
proof the idea came before the result.* When `git config --get kaxanuk.autosend` prints `true`, it
also goes to the owner's copy on GitHub, as the `backup` skill says. If git wants a name, ask in
one open message, with no options, *What's your name, or what would you like me to call you?*,
never invented, and no e-mail; set it in that folder only, with `user.email` as `"<>"`, an empty
address, and save again; with no `.git/`, say in one line that the strategy keeps no versions yet.
This replaces the owner's own commit an older home's `AGENTS.md` asks for.

Then say what comes next in the order of work: the broad reading, for what the blueprint left as
leads; and the cycle — portfolio construction, backtest, attribution — until it is finished.

Never write into the researcher's home from here. Never state a performance number as a prediction
unless an analyzer measurement supports it; the engine has not run, and the blueprint must not
pretend it has.
