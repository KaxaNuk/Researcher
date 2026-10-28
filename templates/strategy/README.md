# KaxaNuk Strategy Template

**A template for researching an investment strategy with the KaxaNuk Investment Lab.** Its eight
steps as a folder structure, with the conventions that let two people share a tool without
explaining it first. Building the data needs a data-provider key; the backtest and attribution,
steps 5 and 6, also need the licensed Backtest Engine and Attribution Analysis. It is research,
never investment advice: *What it is, and what it is not*, in the
[KaxaNuk Researcher's README](https://github.com/KaxaNuk/Researcher#readme).

The universe is one CSV whose only required column is `main_identifier`, and every stage reads it
without knowing what is in it: **equities, ETFs, FX, crypto, commodities or futures all run the
same process.**

**To start a strategy, install the KaxaNuk skills once, for your user**, as step 4 of
[`SETUP.md`](SETUP.md) shows, **then ask Claude or Codex to run `init-strategy <strategy-name>`.**
It copies this template into a new folder named after the strategy and makes it a git repository,
and its copy of `SETUP.md` takes over from there. Issues and pull requests are welcome: the process
improves in public.

This template is the shape and every file the process expects in it, each a description of what
belongs there; *What is in here* says what each file is for. The
[example](https://github.com/KaxaNuk/Researcher/tree/main/examples/strategy/golden-flow)
is the same files worked through for one strategy, `golden-flow`.

---

## Eight steps, one repo

Each stage owns its outputs and reads only from the stage above it. **Steps 1 to 7 are this
repository, and steps 3 to 6 run on the KaxaNuk Investment Lab's libraries.** Step 8 is the one
that leaves it.

| # | Step | In plain words | It produces | It prevents | Where |
| --- | --- | --- | --- | --- | --- |
| 1 | **Bibliotheca** | the idea and its claims first, then the literature that argues with them | a referenced hypothesis, in the repo, dated | backtesting a hunch you cannot defend afterwards | `OBJECTIVE.md`, `Bibliotheca/` |
| 2 | **Universe** | the eligible list, rebuilt for each date rather than for today | a point-in-time membership table | survivorship bias — testing on the winners that survived | `Universe/` |
| 3 | **Data** | curation, then refinery, then analysis — in that order | a reproducible dataset, and the evidence a feature carries signal | beautiful results that came from broken inputs | `Data/` |
| 4 | **Portfolio** | how much of what, and how often you change your mind | a weighting scheme with position and turnover limits | a good signal in a portfolio nobody could hold | `Experiments/Experiment_N/` |
| 5 | **Backtest** | the simulation, run by the Backtest Engine | a performance curve and a cost-aware track record | paper returns that real trading would have erased | `Experiments/Experiment_N/Backtest/` |
| 6 | **Attribution** | which part of the return did you actually earn? | a factor and idiosyncratic breakdown of performance | selling factor beta as if it were alpha | `Experiments/Experiment_N/Attribution/` |
| 7 | **Paper trading** | a dress rehearsal on data nobody has seen yet | out-of-sample evidence and an operations checklist | finding the plumbing problems on day one of funding | `Paper_Trading/` |
| 8 | Production | real capital, real monitoring, a real drawdown policy | a funded, monitored strategy with an owner | research that stays research forever | **elsewhere** |

---

## The tools

Three jobs, one tool for each. Install once, use for every strategy.

| Job | What it is for | Use |
| --- | --- | --- |
| **Versions** | where your work lives, and how you get it back after you break it | the [git](https://git-scm.com) command line, which setup and every save need; [GitHub Desktop](https://desktop.github.com) can sit on top, not in its place |
| **Code and debug** | your pair for the parts you have not written before | [Claude](https://claude.ai/download), or [Codex](https://openai.com/codex) |
| **Read and run** | where you write and run Python; the free editions are enough | [PyCharm](https://www.jetbrains.com/pycharm/), or [VS Code](https://code.visualstudio.com) |

**KaxaNuk's agent skills teach whichever assistant you pick** the Lab modules and this process:
what each does, how it is called, and what it must never be asked to do. They are one package,
[`KaxaNuk/Researcher`](https://github.com/KaxaNuk/Researcher), installed once for
your user and there in every strategy, so **a strategy installs nothing**. Nothing here needs them
to be read; a filled-in repository is faster with them.

### A researcher beside the process

A researcher is a separate project, one per person rather than per strategy, made once with
`init-researcher`, a skill of the [KaxaNuk Researcher](https://github.com/KaxaNuk/Researcher):
a companion you name and teach, with its own library of what you have read. Its commands serve the
parts below: `objective` drafts the claims in `OBJECTIVE.md` and rewrites their evidence from the
notes (A, B); `read` writes the notes in `Bibliotheca/` (B, F); `blueprint` drafts each
`BLUEPRINT_N.md`, every prediction citing a note (E); and `challenge` checks a finished cycle
against its blueprint (G). [`SETUP.md`](SETUP.md) step 4 says how to invite it.

---

## Setup

**[`SETUP.md`](SETUP.md) is the whole of it**: getting the repository, the one folder it has to
live in, the environment, the keys and where the agent skills come from, each with the command an
agent runs and the mistake it must not make.

---

## Starting your own strategy

Once setup is done, work in this order. **These eight parts are lettered so they are never mistaken
for the eight steps above:** the universe, C, is step 2; the cycle, G, is steps 4 to 6. Every file
they name is already in your repository, waiting to be filled in; the seed,
`Universe/Investable_Universe.csv`, holds only its `main_identifier` header. Ask your assistant to
run `next` at any moment: it reads the folder and says which part comes next.

- **A. The objective.** Write `OBJECTIVE.md`, the idea in one sentence and the claims inside it,
  **before any paper is read** and before anything is measured. Reading with no claim to read for
  has no stopping condition, and a claim written after the reading is an observation wearing a
  hypothesis's clothes. Each claim's evidence starts as the question that would settle it.
- **B. The reading.** Fine-tune the objective: read for each claim's question, the sources that
  argue against it included, one note per paper and one per chapter of a book, in `Bibliotheca/`.
  Then rewrite each claim's evidence from the notes.
- **C. The universe.** Put your securities in `Universe/Investable_Universe.csv`, one row each,
  **delisted names included**: a list of today's names has already deleted everything that
  failed. `main_identifier` is the only required column; add whatever else your strategy groups
  by. The universe comes after the claims because they decide what it has to contain.
- **D. The data.** Write your `c_*` and `r_*` columns into the two `custom_calculations.py`, fill in
  the Curator and Refinery drivers that call the libraries, and run the Universe and Data steps in
  this order: curator, then `universe_marimo.py`, then refinery, then `analyzer_marimo.py`. The
  universe notebook sits *between* the two Data commands because it profiles what the curator
  downloaded and writes the master the refinery joins. The analyzer's measurements go straight into
  `RESULTS.md`. Every notebook is a marimo notebook: a Python file that runs as a script and saves
  no output in itself.
- **E. The blueprint.** Name the benchmark, then write `BLUEPRINT_1.md` before the rule. The
  benchmark is what "beat" means: an index, an ETF or an equal-weight book of the universe.
  Choosing it, with the candidates set aside, is an entry of `JOURNAL_1.md` before the blueprint;
  Experiment 1 is the first rule tested against it, a real strategy with a real return. Every
  prediction in the blueprint cites a `Bibliotheca/` note from B or an analyzer measurement from
  D, and the blueprint names the claim it moves, its control and what would falsify it: a
  hypothesis edited after its test is not a hypothesis. Before the blueprint is saved, its rule is
  read back in one plain sentence and one worked date's book: the names it holds that day, and why
  the names at the edge are in or out. The owner's yes is the `JOURNAL_1.md` entry *the rule read
  back*, because code can follow a blueprint faithfully and still not be the book its owner meant.
- **F. The broad reading.** Search for papers on what the blueprint left open. What to try next
  goes in the journal, as each entry's open threads.
- **G. The cycle.** Portfolio construction, backtest, attribution, until it is finished and the
  notebook's last section, Verify, passes, rewriting `FINDINGS_1.md` as its results change.
- **H. The results.** Send every finished cycle to `RESULTS.md`, kept or rejected, with the claim
  it moved. Report the rejected result as loudly as the promising one: *What is closed* is what
  stops the next person repeating it.

Then the gate in `Paper_Trading/BITACORA.md` — soundness first, S1 to S5, then performance, P1 to
P3 — or Experiment 2, from E again. An experiment that is sound and earns only in named periods is
read as such, and may go to paper on probation on the owner's sign-off, never to production from
paper alone.

---

## The documents

**Two files answer "is this worth anything?"** — [`OBJECTIVE.md`](OBJECTIVE.md) says what we are
trying to do, [`RESULTS.md`](RESULTS.md) says how far we got and what it cost.

| Document | What it holds |
| --- | --- |
| [`SETUP.md`](SETUP.md) | how to get this repository, where it must live, and the commands |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the main idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | the executive summary of every experiment, compiled from the `FINDINGS_N.md` files |
| [`CHANGELOG.md`](CHANGELOG.md) | every version, newest first, and what a version number means here |
| [`AGENTS.md`](AGENTS.md) | **how work is done** — the workflow, the restrictions, and the bar a result has to clear |

Every `Experiments/Experiment_N/` holds three documents, and the split between them is the point:
`BLUEPRINT` is frozen so a result cannot quietly reshape the question it was meant to answer,
`JOURNAL` is append-only so the path is recoverable, and `FINDINGS` is rewritten so there is one
current answer. The journal also keeps the thinking before a blueprint, and each entry's open
threads look forward, so planning is never mistaken for history.

---

## What is in here

What the template ships, besides the documents above:

```
pyproject.toml        the version, and the environment: Python 3.13, the open-source libraries,
                      uv-managed

Bibliotheca/          step 1
Universe/             step 2
Data/                 step 3
Experiments/          steps 4-6
Paper_Trading/        step 7
Config/               .env.template - copy to .env and fill in your keys
```

What goes in each folder, written down only here, so keep this table current:

| Folder | Step | What belongs in it | Committed |
| --- | --- | --- | --- |
| `Bibliotheca/` | 1 | `BIBLIOGRAPHY.md`, the index of sources and the leads. `Papers/`, one note per paper, and `Books/`, one folder per book — its `INDEX.md` of chapters and one note per chapter somebody chose to read — each beside the PDF it came from. `LOG.md`, what was read here and when. `Notes/` for clippings and transcripts | the notes and the indexes — they are the reasoning. The PDFs and `Extracts/` are ignored: licensed material, and the extracts regenerate |
| `Universe/` | 2 | `Investable_Universe.csv`, **the seed**: one row per security. `universe_marimo.py`, which profiles what the curator downloaded and writes `Security_Master.csv` and `Data_Issues.csv` | the seed and the notebook; the two outputs and `Provider_Cache/` are regenerated, so ignored |
| `Data/` | 3 | `curator.py`, `refinery.py`, `analyzer_marimo.py` — the three drivers — and `hand_supplied.py`, the one reader of the index and factor files KaxaNuk's Analytics Factory ships, in place from `KN_ANALYTICS_PATH` or from the drop zones. `Curator/custom_calculations.py` for `c_*` columns and `Refinery/custom_calculations.py` for `r_*`. `Curator/Time_Series/`, `Benchmarks/`, `Factors/` and `Refinery/Time_Series/` for what is downloaded or dropped in by hand; `Analyzer/` for charts and the signal table | code only. **Every data file is ignored** — downloaded, derived or dropped in, all of it regenerable |
| `Experiments/` | 4–6 | The four shared modules — `securities_panel.py`, `portfolio_construction.py`, `backtest_engine.py`, `attribution_analysis.py`. One `Experiment_N/` per idea: `BLUEPRINT_N.md`, `JOURNAL_N.md`, `FINDINGS_N.md`, the notebook, and its `Portfolio/`, `Backtest/` and `Attribution/` output folders | the documents, the notebook, which saves no output, and the modules. The output folders are rebuilt by the notebook, so ignored, as is marimo's `__marimo__/` |
| `Paper_Trading/` | 7 | `BITACORA.md`, what graduation means and the gate. `promote.py`, which freezes a graduated experiment into `Paper_Trading_N/`; `daily_update.py`, which runs every frozen book each day; `record.py`, which keeps the record in files, a DuckDB database or both. `Paper_Trading_N/`, one frozen book: its `paper_trading_N.py`, the files it needs in the strategy's own layout, and `FREEZE.json` | the scripts, `BITACORA.md` and every frozen book. Each day's raw files, logs and record are ignored, and the record cannot be fetched again: keep it in the database or back it up |
| `Config/` | — | `.env.template`, copied to `.env` and filled in with a data-provider key, the Lab's licences, the Analytics Factory's folder and the paper-trading settings | the template. **`.env` never** — and it cannot be regenerated, so discarding all changes loses it |

**Every one of those files is in this template**, except `Bibliotheca/Papers/`, `Books/` and
`Notes/`, which appear with their first note. Each is a description of what is expected in it, to
be filled in with the strategy's own: a `.py` file as its docstring, a notebook as its markdown
cells, a document as its prose.

The [example](https://github.com/KaxaNuk/Researcher/tree/main/examples/strategy/golden-flow)
works the same files through, its own lines beside that description between the example markers:
`<!-- example: begin -->` and `<!-- example: end -->` in Markdown, `# --- example: begin ---` and
`# --- example: end ---` in Python, a marimo notebook included. To read the example, or run it,
copy it whole into a folder of its own:

```text
init-example
```

Never build on it. The seed in `Universe/`, everything between the markers and every file only the
example has (its notes and `Universe/seed.py`) are that strategy's.

---

## The six Lab modules

Six modules across steps 3 to 6, each reading the previous one's output, so you can enter the
pipeline wherever your work already is.

| Module | Step | What it does | Status |
| --- | --- | --- | --- |
| **Data Curator** | 3 | pulls raw market and fundamental data from any provider and aligns it on one calendar | open source and free, on [PyPI](https://pypi.org/project/kaxanuk.data-curator/) |
| **Data Refinery** | 3 | cleans, adjusts and reshapes the curated data into analysis-ready series | coming; hand-rolled in `Data/refinery.py` until then |
| **Data Analyzer** | 3 | builds features and tests whether they carry signal, before you model anything | coming; hand-rolled in `Data/analyzer_marimo.py` until then |
| **Portfolio Construction** | 4 | turns a signal into weights, position limits and a rebalancing rule | licensed |
| **Backtest Engine** | 5 | runs the rules over history with costs and no look-ahead, and returns the track record | licensed |
| **Attribution Analysis** | 6 | splits the return into known factor exposure and the part that is actually yours | licensed |

**Two doors.** KaxaNuk's platform, <https://www.kaxanuk.mx/lab>, drives the same pipeline from a
workspace instead of a terminal. The other door is `pip install`: the open-source libraries are
public on [PyPI](https://pypi.org/project/kaxanuk.data-curator/) and
[GitHub](https://github.com/KaxaNuk), with no account or platform login, and `uv sync` installs
the Data Curator.

The **licensed** engines, the Backtest Engine and Attribution Analysis, are deliberately absent
from `pyproject.toml`, so their index URLs and keys never enter version control. **Portfolio
Construction** is absent too: it is KaxaNuk's own library, licensed and not distributed publicly
yet. The three, and the Data Refinery and the Data Analyzer when they ship, come together with
their licences in the KaxaNuk Investment Lab, which KaxaNuk sells: write to `lab@kaxanuk.mx`.
Install each by hand, as the `portfolio-construction-runs`, `backtest-engine-runs` and
`attribution-analysis-runs` skills describe, and **guard their imports**: a notebook that uses one
reports what is missing and skips. Without Portfolio Construction, an equal-weight book still
needs nothing but the eligible set; without the engines, the pipeline still builds its portfolios,
and the backtest and attribution results wait until they are installed.

---

## The conventions worth keeping

Everybody will have their own ideas, and that is the point of a template rather than a framework.
But when we want to share a tool, some names have to mean the same thing in both repositories.

### Where each kind of logic goes

**The prefix tells you which stage owns a column, and therefore which file to open.**

| Prefix | Built by | Scope | Change it when |
| --- | --- | --- | --- |
| `m_*` | the provider, via the Curator | raw market data | never — it is what arrived |
| `c_*` | `Data/Curator/custom_calculations.py` | **one security's own history** | you need a new per-security quantity |
| `r_*` | `Data/Refinery/custom_calculations.py` | **securities against each other, per date** | you need a rank, a breadth reading, or a column with a setting an experiment will sweep — a fitted model, or a window |
| `current_*` | `Data/refinery.py`, joined from the security master | **today's classification — not point-in-time** | you group or report by something new. Never select on it |

Three rules follow, and one exception worth knowing:

- **A `c_*` column that needs to see other securities is misplaced** and belongs in the Refinery.
- **Widening the Curator's schema forces a refetch of every identifier.** That is deliberate, since
  it stops a folder holding a mix of schemas, but it makes the Curator the wrong home for anything
  you intend to tune.
- **A new experiment's signal on the data already downloaded is an `r_*` column**, computed by the
  Refinery, never a wider Curator schema and a second download.
- **The exception: a column with a setting to sweep, fitted or a window such as a twelve-month
  return's, lives in the Refinery even when it is per-security.** Its settings are exactly what an
  experiment sweeps, and **a sweep must never cost a download.** Its *inputs*, arithmetic with
  nothing to tune, stay in the Curator.

### The names

| Name | What it is |
| --- | --- |
| `Universe/Investable_Universe.csv` | the seed. One row per security; **`main_identifier` is the only required column**, and every other column is yours |
| `Universe/Security_Master.csv` | the seed plus what the provider knows, written by step 2 |
| `Universe/Data_Issues.csv` | what is wrong with the downloaded files, written by step 2 |
| `Data/Curator/Time_Series/` | one file per identifier: `m_*` and `c_*` |
| `Data/Refinery/Time_Series/` | each security's rows inside its span, plus `r_*` and `current_*` — **the panel every experiment reads** |
| `Experiments/Experiment_N/` | one folder per idea: `BLUEPRINT_N.md`, `JOURNAL_N.md`, `FINDINGS_N.md`, and the notebook |
| `Portfolio/portfolio_weights.csv` | the book, in the shape the Backtest Engine reads |

### The four shared modules

Everything specific to a strategy lives in its notebook, where a reader can see it. Four Python
modules in `Experiments/` are shared between experiments for one reason: **if they differed between
experiments, comparing experiments would be meaningless.**

| Module | Owns |
| --- | --- |
| `securities_panel.py` | reading the refined files, stitching renamed securities into one position, pivoting to `dates x securities` |
| `portfolio_construction.py` | turning an eligible set into weights through one signature, one rebalance date at a time on a history cut before it — the Portfolio Construction library called inside it where it is installed |
| `backtest_engine.py` | writing the weight file, running the engine, reading results back — the book's daily weights among them — and aligning variants onto one window |
| `attribution_analysis.py` | shaping the hand-supplied index and factor files, and the book's daily weights from the backtest, into what the attribution library reads — it rejects a file with only the rebalance dates — widening the book to every benchmark constituent at zero weight so the benchmark is compared whole, holding both weight tables overnight so the close of t−1 earns day t, reconciling the first cut's benchmark with the index's own returns, and saying what is missing before it tries |

**A strategy column is named in exactly two kinds of place: a notebook's setup cell, and the rule.**
Never in a shared module, so a signal cannot become every later experiment's default without anyone
deciding it.

**[`AGENTS.md`](AGENTS.md) is next**: the workflow, the bar any new signal has to clear, and the
five ways a backtest lies.
