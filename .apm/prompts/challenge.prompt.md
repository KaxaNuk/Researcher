---
description: Challenge a finished experiment against its own blueprint — which predictions held, which falsifiers fired, what the findings do not say — reported in chat and, on the owner's go, as one appended JOURNAL_N.md entry. Never edits the blueprint, the findings or the results, and never computes a number. Only when the owner runs it by name, on a strategy they name or are working in.
input:
  - experiment: "The experiment number N"
  - strategy: "Optional: path to the strategy repository, if not the one the session is in"
---

# Challenge a finished cycle

Every path below is relative to the researcher's home — the folder that holds `RESEARCHER.md`. Find
it first and read its `RESEARCHER.md` and `AGENTS.md`. In a strategy — the session is open in a
repository with a `Bibliotheca/`, or the owner named one by path — *Working in a strategy* in
`AGENTS.md` says where each of these paths lands. With no home in the session, work from the
strategy alone, with no library contrast, and say so.

This is G and H of *The order of work*: the cycle has run, and the researcher's part is to
challenge it. A blueprint is a set of predictions somebody was willing to be wrong about; this
command asks whether the run treated them that way. `${input:experiment}` is the experiment number
`N`; `${input:strategy}` is the strategy's path, given when the session is not already open in it.

**It is the last command that runs, and the only one whose default output is no file at all.**

## Step 1: Refuse if there is nothing to challenge

- **The folder is the worked example** — its `README.md` or `AGENTS.md` holds a line reading
  `<!-- example: begin -->`, the test `next` uses. The example is for reading and running, never
  built on; a strategy of the owner's own is `init-strategy <name>`.
- **No `Experiments/Experiment_N/BLUEPRINT_N.md`, or it is not filled** — it lacks the line
  `blueprint` writes under the experiment's heading, `**Written YYYY-MM-DD, before any rule was
  coded.**` — there is no hypothesis to check the run against: `blueprint`, E.
- **No `FINDINGS_N.md`, or it reports nothing yet** — the cycle is still running. Say so and stop;
  challenging a run in progress invites the findings to be written to match.
- **Home** — there is no experiment here. Say so and stop.

## Step 2: Read, in this order

1. `Experiments/Experiment_N/BLUEPRINT_N.md` — every prediction with its falsifier, the declared
   window, universe, rules, costs and success criteria, and the claim it names under *The claim this
   moves* where it has that section, and the package it was drafted with, after the *Written*
   line: `Drafted with KaxaNuk-Researcher X.Y.Z`. A blueprint written before 0.27.0 has none.
   This is the fixed side of the comparison.
2. `FINDINGS_N.md` — the verdicts, the tally, the trial count, the caveats, and the claim it says
   the experiment moved.
3. `JOURNAL_N.md` — what happened during the run, and what was already disclosed.
4. `RESULTS.md`, including *Before any experiment* — where the analyzer's measurements survive once
   notebook outputs are stripped, and where the published numbers live.
5. `OBJECTIVE.md` — the claims this experiment tests, and their statuses.
6. `BIBLIOGRAPHY.md` and every note a prediction cites, in the strategy's `Bibliotheca/`.
7. `AGENTS.md` in that repository — the bar a result has to clear, and who writes each document.
8. `Paper_Trading/BITACORA.md` only when graduation is being claimed.

**Not the engine's workbooks.** `Backtest/` and `Attribution/` are gitignored outputs: a fresh
clone has none, and they can differ from what the findings published. Every number in the report
is quoted from `FINDINGS_N.md` or `RESULTS.md`, with its source named.

## Step 3: The checks

1. **Verdict against falsifier.** Take each prediction's falsifier as written. A falsifier with two
   limbs fires when either limb fires — a verdict of *split* or *mixed* where a limb fired is a
   falsification recorded in a softer word, and that is the single most useful thing to catch.
2. **The tally against the rows.** Count the rows yourself and compare with the sentence that sums
   them up. A row counted twice, or a verdict dropped, is a bookkeeping error, not a finding about
   the strategy.
3. **A verdict that answers a question the prediction did not ask.** *Falsified against the index,
   confirmed against the control* where the prediction named only the index is a falsification plus
   a new observation; say that the second half belongs in a new line, not in the verdict.
4. **The run against the frozen blueprint.** Window, universe, rules, costs and any parameter the
   run added. A deviation with a good reason is fine — an undisclosed one is not: check that it is
   in the caveats or the journal, and name it when it is nowhere.
5. **Success criteria, one by one.** Each is met, unmet or unevaluated, before any claim of
   adoption or graduation. A criterion that passes is worth a line too. When the owner claims
   graduation, the gate is covered here: `Paper_Trading/BITACORA.md`'s five criteria are read
   against `FINDINGS_N.md` and `RESULTS.md`, each evidenced or not met, and nothing is written
   there.
6. **The notes behind the predictions** — the part no backtest reviewer will do. Open each cited
   note: does it say what the prediction says it says, does the relative path resolve inside the
   strategy, and is any source cited that has no note? Where the findings claim a source's failure
   mode reproduced, check that against the note rather than against memory.
7. **The trial count.** `FINDINGS_N.md` owes it, under *The trial count*: how many variants were
   ranked to reach the book, and every run excluded by name with its reason. `RESULTS.md` compiles
   it. A count missing from the findings is a finding whether or not graduation is claimed, and one
   present in `RESULTS.md` but not in `FINDINGS_N.md` is a summary leading its source.
8. **Closure.** Every falsified prediction and every falsified claim reaches `RESULTS.md` under
   *What is closed* or *Known limitations*, and the claim's status in `OBJECTIVE.md` moves. Where
   the blueprint names a claim under *The claim this moves*, that is the claim to follow:
   `FINDINGS_N.md` names the status it reached, and `OBJECTIVE.md` — and the experiment's *Claim
   moved* in `RESULTS.md`, where that column exists — carry the same one. A findings file that names
   a different claim, or two files that give it different statuses, is a finding. Where the
   blueprint names none, read the statuses in `OBJECTIVE.md` of the claims it tests. What stops the
   next person repeating an experiment is written down, or it does not exist.
9. **Arithmetic between published numbers.** A difference published alongside the two numbers it
   comes from either reconciles or it does not. Report a disagreement and ask for a re-run; never
   supply the corrected value.
10. **The reading before the blueprint.** A note read after the blueprint cannot have informed its
    predictions, and a prediction that cites one is look-ahead in the research itself. Read the
    commit that wrote the blueprint's *Written* line — `BLUEPRINT_1.md` itself came in blank with
    the template — and the one that brought in each note a prediction cites, with its date. Every
    git command of this check runs in the strategy's folder, as `git -C "<that folder>"` from a
    session open elsewhere:

    ```bash
    git log -S'before any rule was coded' --reverse --format='%h %cs' -- Experiments/Experiment_N/BLUEPRINT_N.md
    git log --diff-filter=A --format='%h %cs' -- <note>
    ```

    The blueprint's commit is the first line the first command prints. The note must have entered
    git before it, and the first `YYYY-MM-DD` in its frontmatter's `read` field must fall on or
    before that commit's date. A note that entered with the blueprint or after it, or whose `read`
    field holds no date that parses, is a finding: it cannot be shown to have informed the
    prediction. A note that entered before but whose `read` date is later was read again since: say
    so, and read for check 6 the version the prediction rests on, the one at the blueprint's
    commit, `git show <commit>:<note>`. That is not a finding by itself. The log is read, never
    changed.

Two things cannot be checked from the working tree, and the report says so when they matter. The
falsifiers are prose, so pairing *a beta at or above one* with *beta is 1.028* is a judgement made
in words. The ordering the whole process rests on — the blueprint saved before the rule, the
counterfactuals before the engine — lives in the git log, not in the files. So read the log, as
check 10 does: run `git log --oneline -- Experiments/Experiment_N` in the strategy's folder. Quote
in the report, in plain words, what it shows — the version that wrote the blueprint, as check 10
finds it, and whether it was saved before the one that put the rule into `experiment_N.ipynb`. A
blueprint saved with its rule, or after it, cannot be told from one written afterwards; say so.

The process can move under an experiment too: `blueprint`, `blueprint-critic` and this command come
from one package, updated for every strategy at once. Read the version this run uses as `blueprint`
does, in `~/.apm/apm.lock.yaml`: the entry under `dependencies:` whose `repo_url` or
`materialization_repo_url` is `kaxanuk/researcher`, or `kaxanuk/kaxanuk-researcher` for an install
from before 1.25.0, ignoring case, as `next` reads it. A
`source: local` entry is read only when its `local_path` holds `templates/researcher/`, the
package's own checkout, never a home. Compare that version with the blueprint's stamp. The same
version is one line of the report. A different one names both, and the entries of the package's
`CHANGELOG.md`, beside that `apm.yml`, between them that touch `blueprint`, `blueprint-critic` or
`challenge` — so the owner sees what changed in the checks, not only that something did.
No stamp: say the blueprint predates it, and that the question cannot be answered from the files.
A mismatch is disclosed, never a failure: the verdicts stand or fall on the blueprint as written.

## Step 4: Report, and offer the one line it may write

**In chat:** what held, what failed and by which falsifier, what the findings do not say, the
bookkeeping, and every cited note read after the blueprint or read again since. Then the leads —
what to read for what the run left open, and what the next experiment should consider, which the
journal entry below carries as open threads. Name every file and every note by path.

**Then offer one appended entry in `JOURNAL_N.md`**, dated, in the template's format, and write it
only on the owner's go, *write it and save a version*. It is the one file this command may touch,
because the journal is appended and never edited, and a look-across is already recorded there. Its
*What we tried / considered* names both packages: *`challenge` with KaxaNuk-Researcher X.Y.Z,
against a blueprint drafted with W.W.W*, or *with no stamp*.

**Then save it as a version of its own**, in the strategy's folder, on the same go, with no second
question and no `CHANGELOG.md` entry, version bump or ruff gate — the next change-set's entry names
it. Every git command, the `backup` skill's send included, runs as `git -C "<that folder>"` when
the session is open elsewhere: `git add Experiments/Experiment_N/JOURNAL_N.md` and
`git commit -m "Challenge: Experiment N" -- Experiments/Experiment_N/JOURNAL_N.md`; to the owner,
*Saved*, in one plain line, never the commands. When `git config --get kaxanuk.autosend` prints
`true`, it also goes to the owner's copy on GitHub, as the `backup` skill says. If git wants a name,
ask in one open message, with no options, *What's your name, or what would you like me to call
you?*, never invented, and no e-mail; set it in that folder only, with `user.email` as `"<>"`, an
empty address, and save again; with no `.git/`, say in one line that the strategy keeps no versions
yet. This replaces the owner's own commit an older home's `AGENTS.md` asks for.

**What it never does, whatever the argument:**

- **`BLUEPRINT_N.md` — never, once written.** A prediction worded better after its test is not a
  prediction. A wording problem becomes a lead for the next blueprint.
- **`FINDINGS_N.md` and `RESULTS.md`** belong to the experiment's own writer, and a challenger that
  rewrites what it challenges is both hands at once. Report the discrepancy and stop.
- **`OBJECTIVE.md`** — a claim's status is `objective`'s to change, and its wording is the owner's.
- **Compute or restate a performance number**, including a corrected one. The engines produce
  numbers; this command compares the ones already written down.
- **Declare graduation.** The gate's last criterion is a person's signature.
- **Open another experiment's files** unless the request and the reason are already in
  `JOURNAL_N.md`, and **write anything at home.**
