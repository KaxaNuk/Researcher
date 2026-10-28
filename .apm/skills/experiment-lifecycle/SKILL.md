---
name: experiment-lifecycle
description: >
  Load this skill whenever you start, structure, run or document a KaxaNuk Investment Lab strategy
  repository or one of its experiments. Use it when the user asks to start a strategy from the
  KaxaNuk Strategy Template, scaffold an Experiments/Experiment_N/ folder, write a blueprint,
  journal or findings file, update RESULTS.md, or move a strategy
  through the order of work and the eight steps. It defines the document architecture, each file's
  contract, the notebook section contract and where each kind of logic goes, and points to the
  restrictions, the bar a new signal must clear and the graduation gate. It does NOT cover what
  another tool owns: step 1 (the KaxaNuk Researcher), `universe-point-in-time`,
  `data-curator-custom-calculations`, `data-analyzer-runs`, `portfolio-construction-runs`,
  `backtest-engine-runs`, `attribution-analysis-runs`, `alpha-decomposition`,
  `paper-trading-gate`, or branches and changelogs (`how-we-work`).
metadata:
  version: 0.15.0
---

# The research process — how a strategy repository is worked in

Every KaxaNuk Investment Lab strategy lives in its own repository, copied from the **KaxaNuk
Strategy Template**, which ships in `KaxaNuk/Researcher` as `templates/strategy/`. The
template is the shape and every file the process expects in it: six folders, the documents at the
root, and inside the folders each driver, module, notebook and document. Each is a description of
what belongs there — a `.py` file as its docstring, a notebook as its markdown cells — to be filled
in with the strategy's own. The worked example beside it, `examples/strategy/golden-flow/`, works
one strategy, `golden-flow`, through the same files, with the strategy's own lines between example
markers. The fixed shape buys comparability and legibility: any experiment looks like any other,
every experiment is measured against the same named benchmark, and a reader takes in the whole state
of a project from two files, `OBJECTIVE.md` and `RESULTS.md`.

Code in English — function names, docstrings and comments — and so are file names and the
headings the skills read; the notebook narrative and the documents in the owner's language, unless
the strategy's `AGENTS.md` names one language for its team.

**To start a new strategy, copy the template; never scaffold one by hand.** The owner runs
`init-strategy <name>`, from the KaxaNuk Researcher, which copies it into a new folder by script and
makes it a repository; the new folder's own `SETUP.md` owns the rest of the procedure. To work
inside a strategy repository, follow this skill. **Do not name Obsidian or a deck in a repository
document, nor any KaxaNuk in-house strategy other than the package's worked example,
`golden-flow`.**

## 1. The eight steps

Steps 1 to 7 are the strategy repository's, and steps 3 to 6 run on the Investment Lab's
libraries. Step 8 is not: a strategy leaves the repository when it is funded. Each stage owns its
outputs and reads only from the stage above it.

| # | Step | In plain words | It produces | It prevents | Where |
| --- | --- | --- | --- | --- | --- |
| 1 | **Bibliotheca** | the idea and its claims first, then the literature that argues with them | a referenced hypothesis, dated | backtesting a hunch you cannot defend | `OBJECTIVE.md`, `Bibliotheca/` |
| 2 | **Universe** | the eligible list, rebuilt for each date rather than for today | a point-in-time membership table | survivorship bias | `Universe/` |
| 3 | **Data** | curation, then refinery, then analysis | a reproducible dataset, and evidence a feature carries signal | beautiful results from broken inputs | `Data/` |
| 4 | **Portfolio** | how much of what, and how often you change your mind | weights with position and turnover limits | a good signal in a book nobody could hold | `Experiments/Experiment_N/` |
| 5 | **Backtest** | the simulation, run by the Backtest Engine | a cost-aware track record | paper returns real trading would erase | `Experiments/Experiment_N/Backtest/` |
| 6 | **Attribution** | which part of the return did you actually earn? | factor and idiosyncratic breakdown | selling factor beta as alpha | `Experiments/Experiment_N/Attribution/` |
| 7 | **Paper trading** | a dress rehearsal on data nobody has seen | out-of-sample evidence | plumbing problems on day one of funding | `Paper_Trading/` |
| 8 | Production | real capital, real monitoring, a drawdown policy | a funded strategy with an owner | research that stays research | outside the repository |

**A stage that recomputes something an earlier stage produced has broken the process**, even when
the number matches: the next experiment computes it slightly differently and the two stop being
comparable. A step is finished when its output is reproducible from the step above by re-running
one command or one notebook.

The Investment Lab is KaxaNuk's six libraries that run steps 3 to 6, with a web front end. Each
maps onto one module of the strategy: Data Curator (`Data/curator.py`), Data Refinery
(`Data/refinery.py`), Data Analyzer (`Data/analyzer_marimo.py`), Portfolio Construction
(`Experiments/portfolio_construction.py`), Backtest Engine (`Experiments/backtest_engine.py`),
Attribution Analysis (`Experiments/attribution_analysis.py`). Four have shipped — the Data
Curator, Portfolio Construction, the Backtest Engine and Attribution Analysis — and two, the
Refinery and the Analyzer, are coming, hand-rolled in the strategy until they land. A hand-rolled
stage says so in its docstring and names the interface its library will replace. A skill says how
each library is called: `data-curator-custom-calculations`, `portfolio-construction-runs`,
`backtest-engine-runs` and `attribution-analysis-runs`, with `universe-point-in-time` for step 2,
`data-analyzer-runs` for the hand-rolled Analyzer, and `paper-trading-gate` for step 7. **Step 1 is
the KaxaNuk Researcher's**, `KaxaNuk/Researcher`, whose home `init-researcher` makes: its
`objective` drafts the claims, its `read` writes the notes in `Bibliotheca/`, and its `blueprint`
drafts `BLUEPRINT_N.md` with every prediction citing a note.

## 2. The control documents

Four files at the root carry the whole state. Everything else is code, or a note feeding one of
them.

| Document | Holds | Changes when |
| --- | --- | --- |
| `OBJECTIVE.md` | the main idea, the objective, the claims inside it with their status | the idea and the claims' wording almost never — a change there is a different strategy; each claim's evidence and status move as notes arrive (B) and as findings report (H), each `FINDINGS_N.md` naming the claim it moved |
| `RESULTS.md` | the executive summary of every experiment, **compiled from the `FINDINGS_N.md` files and citing each**, each experiment's row naming the claim it moved | a `FINDINGS_N.md` changes |
| `CHANGELOG.md` | every version, newest first, in the form `how-we-work` section 3 gives: `## X.Y.Z (YYYY-MM-DD)` and its five headings | any change-set lands |
| `AGENTS.md` | how work is done: workflow, who writes each document, restrictions, the bar, the five ways a backtest lies | the process changes |

`CLAUDE.md` is one line, `@AGENTS.md`. `README.md` says what the repository is and where each kind
of logic goes. `Paper_Trading/BITACORA.md` is the graduation gate — a contract, deliberately not
named `JOURNAL`, because a journal here is an append-only dated log.

**When a number changes, change it in `FINDINGS_N.md` first, then `RESULTS.md`.** One exception:
findings from step 3 go straight into `RESULTS.md`, because a marimo notebook saves no output and
a measurement seen only on the screen of a run does not survive it.

## 3. The three files in every experiment

Each `Experiments/Experiment_N/` is one idea: three markdown files, a notebook, and three gitignored
output folders (`Portfolio/`, `Backtest/`, `Attribution/`, each kept by a `.gitkeep`).

| File | Holds | Who writes it | Changes when | Template |
| --- | --- | --- | --- | --- |
| `BLUEPRINT_N.md` | **the hypothesis** — thesis, the claim it moves, rules with the control, predictions, success criteria, the one condition that would falsify it and the changes that may not rescue it, risks | a person, or with the AI | **never, once written** | `references/blueprint-template.md` |
| `JOURNAL_N.md` | **the running log**, dated, oldest first, the thinking before a blueprint included | the AI, as work proceeds | append only; a correction is a new entry | `references/journal-template.md` |
| `FINDINGS_N.md` | **the latest results worth keeping**, and the claim they moved | the AI, from the journal | rewritten when a result changes; feeds `RESULTS.md` | `references/findings-template.md` |

`BLUEPRINT` is fixed so a result cannot reshape the question it was meant to answer. `JOURNAL` is
append-only so the path is recoverable, and each entry's open threads look forward, so planning is
never mistaken for history. `FINDINGS` is rewritten so there is one current answer. **Every
prediction in a blueprint cites where it comes from** — a note in `Bibliotheca/` or a section of
the analyzer — and a prediction with no source is a lead to read first, not a prediction.

Repository-level history — the benchmark and the choice of it, the data step, the architecture —
belongs in `JOURNAL_1.md`, Experiment 1 being the first rule tested against that benchmark and the
yardstick for every later one. Later journals point there. Two of its entries come before
`BLUEPRINT_1.md`. One chooses the benchmark — the blueprint states what "beat" means, so the
benchmark cannot wait for it. The other is *the rule read back*, the owner's yes that the rule
written is the rule meant, given to one plain sentence and one worked date's book; every later
blueprint has its own, in `JOURNAL_N.md`. A strategy made from a template before 0.13.2 may keep
the benchmark's choice in `BRAINSTORMING_1.md`, which the Researcher's commands still read.
Experiment 1 can graduate like any other; its rules freeze once its findings report, and a rewrite
the owner decides is written down as one, as the strategy's `AGENTS.md` says. A rule with a band
reads the band back beside the rule, on two consecutive dates: the held names left as they drifted,
the orders let through and the cash left over.

## 4. The notebook — one section contract, one cell that is the strategy

`experiment_N_marimo.py` follows the same sections every time. **Every notebook is a marimo
notebook**: a Python file of cells that runs as a script, `uv run python <file>`, opens with
`uv run marimo edit <file>`, and saves no output in itself, so there is nothing to strip before a
commit; marimo's cache, `__marimo__/`, is ignored. There is no Jupyter notebook in the template or
the example. `references/experiment-notebook_marimo.py` is the worked example's Experiment 1
notebook with its own lines stripped — one markdown cell per section saying what that section
computes, and the cells every strategy runs — and is the file to copy. The example's own lines sit
between `# --- example: begin ---` and `# --- example: end ---`, each alone at column 0.

| Section | Contains |
| --- | --- |
| Header · Position in the pipeline · What this notebook does not do | the claim, the standing warnings, the four shared modules |
| 0 · Setup | the repository and the shared modules, then **the strategy's window, columns, bounds and costs** — the only strategy names in the notebook outside the rule |
| 1 · The panel | the refined files loaded and reshaped to `dates x securities` matrices, and the rebalance calendar |
| 2 · The rule | selection, sizing, timing and the control — **the one cell you write**; it produces `REBALANCE_DATES`, `target_weights` with rows summing to **at most** 1.0, the rest cash the engine pays interest on, and, under a no-trade band, `struck_weights` |
| 2.1 · Invariants | what every rule must pass, whatever it is: printed here, raised on in section 8 |
| 3 · Construction | the book's shape — invested share, orders and turnover, holdings and concentration, group drift — capacity against traded value, and every weight file written before any is priced |
| 4 · Backtest | the KaxaNuk Backtest Engine, the only backtest anywhere, guarded; every cost and the cash priced inside it; every run read whole or excluded by name |
| 5 · Attribution | where the return came from, by the library's own pipeline, guarded the same way |
| 6 · Counterfactuals | the sweep, and the arms that price who earned the idiosyncratic share: the same book with one choice removed, priced by the same engine |
| 7 · Verdict | what it concluded, **in words**: the gate read row by row, soundness then performance, the handoff and the open items |
| 8 · Verify | assertions that raise when the output is wrong: the invariants, the weight file read back, each engine run's valued days against its window's trading days, no blocking name held by any book, and the first cut's benchmark within a point a year of the index's own returns file — each skipped where its library is absent. A truncated run is excluded by name with its reason; Verify fails a run that is neither read whole nor excluded, and refuses to exclude the rule, its control or the equal-weight arm |
| 9 · Dashboards | optional: the engine's and the attribution library's own, to look at a run, never to quote |

**Every notebook of the pipeline ends in a Verify section** — `Universe/universe_marimo.py`,
`Data/analyzer_marimo.py` and each experiment's — that reads back what the notebook wrote and raises
when it is wrong. It is where a strategy's tests live; `AGENTS.md` says why it counts against the
window rather than a fixed floor.

**The look-aheads are stated plainly, in section 2 and nowhere else:** everything the rule reads on
a rebalance date *d* is read at the close of the trading day before it, and the fill is at *d*'s
price (the lag); a condition read on *d* itself is named as the one same-day condition. There is no
delisting exit: the engine sells a position whose prices stop at its last price, so the rule takes
no day of hindsight for it, and a gap inside a series, which the engine cannot price, is a blocking
row of the register, its name excluded by name.

**Four modules beside the notebook are shared by every experiment**, one per Lab library.
`securities_panel.py` is the one panel loader. `portfolio_construction.py` takes the eligible set
to weights, with one signature every scheme shares. Where it is installed, the Portfolio
Construction library is called inside it one rebalance date at a time. The bounds the blueprint
names are the design, and every other constraint is switched off — a lever a later experiment
earns. `backtest_engine.py` is the one path from a weight file to a number.
`attribution_analysis.py` shapes the hand-supplied inputs and the book's **daily** weights from the
backtest — the attribution library rejects a rebalance-only file. It holds both weight tables
overnight, reconciles the benchmark with the index's own returns before any figure is read, and
says what is missing first. **A strategy column is named in exactly two kinds of place — a
notebook's setup cell and the rule — never in a shared module**, so a signal cannot become every
later experiment's default without anyone deciding it. Experiment 1 loads the panel through
`securities_panel.py` like every later experiment, so the comparison is on the rule and nothing
else.

## 5. Where each kind of logic goes

**The prefix tells you which stage owns a column, and therefore which file to open.**

| Prefix | Built by | Scope |
| --- | --- | --- |
| `m_*` | the provider, via the Curator | raw market data — never edited |
| `c_*` | `Data/Curator/custom_calculations.py` | **one security's own history** |
| `r_*` | `Data/Refinery/custom_calculations.py` | **securities against each other, per date**, or anything fitted |
| `current_*` | `Data/refinery.py`, joined from the security master | today's classification — **not point-in-time**; group or report by it, never select on it |

A `c_*` column that needs other securities is misplaced. Widening the Curator's schema refetches
every identifier, so nothing tunable lives there: **a fitted column lives in the Refinery even when
it is per-security, because a sweep must never cost a download.** Its inputs — arithmetic with
nothing to tune — stay in the Curator. **A new experiment's signal on the data already downloaded is
an `r_*` calculation of the Refinery**, never a wider Curator schema and a second download.

## 6. Scaffolding

**A new strategy.** Follow the template's `SETUP.md` — the repository, `uv sync`, the credential
file; the skills are installed once for the user, not here — then work in this order. **It is an
index of *Starting your own strategy* in the template's README**, which is the source and says why
each part comes where it does. The parts are lettered A to H so they are never mistaken for the
eight steps. What this skill adds is the last column — which tool each part loads. The KaxaNuk
Researcher's `next` skill reads a strategy against this list and names the part that comes next.

| | Part | Lands in | Load |
| --- | --- | --- | --- |
| A | The objective, **before any paper is read** | `OBJECTIVE.md` | the KaxaNuk Researcher, `objective` |
| B | The reading, for each claim; then the objective fine-tuned from the notes | `Bibliotheca/`, then `OBJECTIVE.md` | the Researcher, `read`, then `objective` |
| C | The investable universe, delisted names included | `Universe/Investable_Universe.csv` | `universe-point-in-time` |
| D | The data — curator, universe notebook, refinery, analyzer, in that order | `Data/`, and `RESULTS.md` for the analyzer's measurements | `data-curator-custom-calculations`, `universe-point-in-time`, `data-analyzer-runs` |
| E | The benchmark, chosen in `JOURNAL_1.md`, then the rule read back there and `BLUEPRINT_1.md` **before the rule** | `Experiments/Experiment_1/` | this skill; the Researcher, `blueprint`, which reads the rule back |
| F | The broad reading, for what the blueprint left open | `Bibliotheca/` | the Researcher, `read` |
| G | The cycle — portfolio, backtest, attribution | the notebook, `FINDINGS_1.md` | `portfolio-construction-runs`, `backtest-engine-runs`, `attribution-analysis-runs`, `alpha-decomposition`; the Researcher, `challenge` |
| H | Every finished cycle, with the gate's outcome — graduates, sound and regime-dependent, or not sound | `RESULTS.md` | this skill |

Then the gate — `Paper_Trading/BITACORA.md`, `paper-trading-gate` — or the next experiment. **The
gate has two layers, read in order.** Soundness, S1 to S5: no survivorship bias, no look-ahead, no
overfitting, costs and capacity stated, reproducible from a working copy whose data folders were
emptied first. Then performance, P1 to P3: beats the benchmarks and its control over the whole
window, idiosyncratic alpha in both layers, conclusions that survive perturbation. Three outcomes:
it graduates, and is frozen and paper traded once a person signs; it is sound and
regime-dependent, its periods named, and is not paper traded alone; or it is not sound, and no
conclusion is drawn. A person reads the gate; the assistant never decides it.

Every file those parts name is in the template, and so in a strategy made from it: each a
description of what belongs in it, to be filled in — the worked example's drivers, modules,
notebooks and experiment files with its own lines removed. A strategy made from a template
before 0.10.0 lacks the files inside the folders; each comes back from the template, never from the
example, whose copy is filled in: `init-strategy`'s script, run from the strategy's root,
`scaffold.py strategy . --only <path>`. It never overwrites, so bring `Universe/universe_marimo.py`
by its path: `--only Universe` stops over the seed, which is already the strategy's own.

**A new experiment `N` inside an existing strategy:**

1. Create `Experiments/Experiment_N/` with `Portfolio/`, `Backtest/`, `Attribution/`, each holding a
   `.gitkeep`. The template's `.gitignore` already covers them.
2. Copy the three templates from `references/`, replacing `N`. **Write `BLUEPRINT_N.md` before any
   code**, with the Researcher's `blueprint N`, which reads the rule back to the owner — one plain
   sentence and one worked date's book, their yes a `JOURNAL_N.md` entry saved before the
   blueprint — and puts the draft to its critic. The blueprint states the economic mechanism, the
   claim it moves, its control and the one condition that would falsify it, and cites every
   prediction's source; on the owner's go it is saved alone, before the rule. The blueprint
   template is the first experiment's; delete the sentences that only apply to Experiment 1.
3. Copy `references/experiment-notebook_marimo.py` to `experiment_N_marimo.py`. It too is
   Experiment 1's: retitle it `Experiment N`, replace every `_1` in it with `_N`, and delete the
   sentences that only apply to Experiment 1. Then declare the experiment's columns in section 0;
   import the panel loader in section 1; write the rule in section 2.
4. Add a row to `RESULTS.md` when `FINDINGS_N.md` first reports, citing it. A new experiment is a
   MINOR bump in `CHANGELOG.md`, and the entry is part of the change-set.

## 7. Where the rules live

Every strategy repository carries its rules in `AGENTS.md`, committed on `main`, so they are there
whether or not the skills are installed. **This skill does not restate them**: a rule written twice
is two rules, and the copies drift. Read them where they are.

| Rule | Where |
| --- | --- |
| One experiment at a time, and its exceptions | `AGENTS.md`, *One experiment at a time* |
| The bar any new signal must clear | `AGENTS.md`, *The bar any new signal must clear* |
| Committed results, bad runs, binaries, Production, `Config/.env`, example markers | `AGENTS.md`, *Other standing rules* |
| The five ways a backtest lies, what look-ahead costs a fitted signal, and the Verify section every notebook ends in | `AGENTS.md`, *Research integrity — the five ways a backtest lies* |
| What attribution must report | `AGENTS.md`, *What attribution must report*; reading it is `alpha-decomposition` |
| The graduation gate: soundness S1 to S5, performance P1 to P3, three outcomes | `Paper_Trading/BITACORA.md`, in the template; reading it is `paper-trading-gate` |
| What a version number means | `CHANGELOG.md`, *What a version number means here* |

## References

- `references/structure.md` — the template's tree, what is committed, and the steps to fill it in.
- `references/blueprint-template.md`, `journal-template.md`, `findings-template.md` — the three
  documents of an experiment, the blanks for Experiment N > 1;
  the template ships Experiment 1's, the same files under `Experiments/Experiment_1/`.
- `references/experiment-notebook_marimo.py` — Experiment 1's marimo notebook, the example's lines
  stripped, the blank for `experiment_N_marimo.py`.

The three documents and the notebook are copies of Experiment 1's files in the worked example,
`examples/strategy/golden-flow/` in the package, with the example's own lines stripped. They
change by hand with the example's, in the same commit, and so does `references/structure.md`.
