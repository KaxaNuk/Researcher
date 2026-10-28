---
name: init-example
description: >
  Copy a KaxaNuk worked example — today one, the strategy golden-flow — into a new folder to study
  or run it, or one of its worked files, such as Data/analyzer_marimo.py, into a folder of its own to
  read beside a strategy's own, from the copy inside the researcher package, by a script; with
  several examples, it asks which. Only when the owner runs it by name. It does NOT start a
  strategy of the owner's own (use `init-strategy`), does NOT bring back a template file a strategy
  lacks (`init-strategy`'s script with `--only` does), and never builds on the example.
metadata:
  version: 0.5.4
---

# Init example — a worked example, whole or one piece at a time

The examples sit in the package by kind, as the templates do: `examples/<kind>/<name>/`, the kind
being what the example is an example of — `strategy`, worked through the KaxaNuk Strategy Template.
Today there is one, `examples/strategy/golden-flow/`: one strategy worked through every folder of
the template — the objective and its claims, the notes, the universe, the data, the experiment and
its documents, the findings, the results and the paper-trading gate. An example's own lines sit
between example markers — `<!-- example: begin -->` and `<!-- example: end -->` in Markdown,
`# --- example: begin ---` and `# --- example: end ---` in Python, a marimo notebook included —
beside the template's description of what belongs in each file. Every example is also readable
without installing anything, in `examples/<kind>/<name>/` of `KaxaNuk/Researcher`.

**The list is the package's, never yours.** Which examples there are, and the line on what each
shows, come from the script, which reads them from the package's folders and READMEs: never name
or describe an example from memory.

## When to Use

- **A whole example, in a new folder** — *init-example*, *init-example golden-flow*, *give me the
  example to look at*. To read it, run its notebooks, or see what a finished experiment looks like.
- **The examples of one kind** — *init-example strategy*: the same, chosen among that kind only.
- **One worked file, to read beside your own** — *init-example Data/analyzer_marimo.py*, *show me
  the example's blueprint*. A strategy's copy of a file says what belongs in it; the example's shows
  it filled. The piece goes into a folder of its own, never into the strategy, and nothing is built
  on it.
- Not to bring back a file a strategy lacks — lost, or never there because the strategy was made
  before template 0.10.0 shipped the drivers, notebooks and documents. That file comes back from
  the template, never from the example, whose copy is filled in: `init-strategy`'s script, run from
  the strategy's root, `scaffold.py strategy . --only <path>`, which never overwrites.
- Not on its own initiative. A skill that points to the example names this skill and the path, and
  the owner runs it.

## Steps

1. **Which example.** The script lists them, one line each, `<kind>/<name> — <what it shows>`,
   after a first line naming the package:

   ```bash
   uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" examples
   ```

   A word the owner gave that the list holds as a name, or as `<kind>/<name>`, is that example,
   taken without asking; one it holds as a kind leaves that kind's examples only. When one example
   is left — today `golden-flow`, with no word at all — it is the one, and nothing is asked. When
   several are left, ask which through the question tool, one option per example: its name, and its
   line from the list, which gives its kind and its subject. The tool takes four options, so with
   more, ask the kind first, and with more than four of one kind, ask as a numbered list in chat
   instead. Without a question tool — Codex, Gemini — ask in one chat message, the examples numbered
   beneath it, each with its line, *Other — your own words* last. Any other word —
   `Data/analyzer_marimo.py`, `Experiments/Experiment_1`, `Universe` — is a path of the example, one
   piece of the example chosen the same way.

2. **Whole or one piece, and where.** A path means that one piece; no path means the whole
   example. Either lands in a folder outside any strategy: ask where through the question tool.
   The default is a folder named after the example — `golden-flow` — in the folder a caller hands
   it, else beside the researcher's home — the folder holding `RESEARCHER.md` here, or the one the
   researcher's skill names — else beside the folder the session is open in. Never into a
   strategy: its file of the same name is the template's description, for the owner to fill. When
   the whole example is asked for where it already is — `<!-- example: begin -->` alone at column 0
   in its `README.md` or `AGENTS.md` — say so, and offer to open it, with *step 6*'s hand-over, or
   another folder: the script would refuse it.

3. **The plan.** In chat: which example, what will be copied and where. For one piece, also that the
   folder is made if it is not there, that the piece keeps its path inside it, that nothing already
   there is overwritten — the script refuses rather than overwrite — and that the worked example's
   own lines come with it. When a newer package is out, checked and dated as item 5 of *Step 4* in
   the `next` skill beside this one says — never with `updatereminder` off or an `updatenext` still
   ahead — one more line: *a newer version of the package is out, X.Y.Z: `update` first brings the
   newest example*. Never a question of its own, and the copy never waits on it. Ask for the go —
   *Go*, *Change something*, *Stop* — and run on *Go* only.

4. **Copy.** The script is in the `init-strategy` skill's folder, beside this one; `--name` takes
   the example's name as the list gives it, or `<kind>/<name>` where two kinds share a name:

   ```bash
   uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" example "<new folder>" --name <name>
   uv run --no-project python "<the init-strategy skill's directory>/scripts/scaffold.py" example "<its folder>" --name <name> --only <path>
   ```

   With several examples and none named, the script copies nothing and lists them; go back to
   step 1. The whole example becomes a git repository with its first commit; one piece is only
   copied, into a folder that must exist — make it, empty, when it does not. On Windows without
   long paths, the script refuses a destination so deep that a copied path would pass 259
   characters, names that path and the longest destination that fits, and writes nothing; choose a
   shorter place. A fork of the package, or a clone in a folder of another name, is not found on its
   own: pass `--package <its install folder>`. A git step that fails leaves the copy in place — the
   script still exits 0 — and prints every command that finishes the repository from that step on.
   If git is missing, install it on the owner's go, then run the printed commands in the new
   folder. If the first commit fails for want of a git identity, ask in one open message, with no
   options, *What's your name, or what would you like me to call you?*, never invented, and no
   email; set them in that folder only, `git config user.name "<their answer>"` and
   `git config user.email "<>"`, an empty address, then run the printed commands there.

5. **For one piece, say what it shows.** Everything between the markers in what was copied is the
   example's own work, and so, whole, is every file only the example has — for `golden-flow`, its
   seed, its notes and `Universe/seed.py`; an example with a book on paper adds that book's
   `FREEZE.json` and the files it hashes.
   Around the markers is the template's description, which the strategy's copy already holds. Name
   the path it landed at, to read beside the strategy's file; never copy its lines into the
   strategy.

6. **Hand over**, for the whole example, in three short lines — for `golden-flow`:
   - *Read*, with nothing installed: `OBJECTIVE.md`, `RESULTS.md`, then `BLUEPRINT_1.md` and
     `FINDINGS_1.md` in `Experiments/Experiment_1/`, then `Paper_Trading/BITACORA.md`.
   - *Run*: its README's *Run it*, in a **new** session opened in the folder — a Sharadar key of
     their own, the Analytics Factory's KN US Equity Core and factor model files, and the Backtest
     Engine and Attribution Analysis, which come with their licences in the KaxaNuk Investment Lab,
     sold by KaxaNuk. For the files, write to `analytics@kaxanuk.mx`; for the licences, to
     `lab@kaxanuk.mx`, saying which library and what it is for, with *via KaxaNuk Researcher* in the
     subject — <https://www.kaxanuk.mx/lab> shows the Lab.
   - *Own*: a strategy of your own is `init-strategy <name>`; nothing is built on the example. Its
     Experiment 1 reads as sound and regime-dependent, so it has no book on paper.

   For another example, the same three lines from its own README: what to read first, how it runs,
   and the `init-<kind>` that starts one of the owner's own.

## References

- `scripts/scaffold.py`, in the `init-strategy` skill's folder — lists the examples, every folder
  `examples/<kind>/<name>/` of the KaxaNuk Researcher package, with `examples`, and copies one with
  `example`, whole or `--only` one path.
