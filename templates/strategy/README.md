# KaxaNuk Strategy Template

**A template for researching an investment strategy with the KaxaNuk Investment Lab:** eight steps
as folders, and the conventions that let two people share a tool without explaining it first. The
universe is one CSV whose only required column is `main_identifier`, so **equities, ETFs, FX,
crypto, commodities or futures run the same process.** Building the data needs a data-provider key;
the backtest and attribution also need the licensed Backtest Engine and Attribution Analysis. It is
research, never investment advice: *What it is, and what it is not*, in the
[KaxaNuk Researcher's README](https://github.com/KaxaNuk/Researcher#readme).

**To start a strategy**, install the KaxaNuk skills once for your user, as step 4 of
[`SETUP.md`](SETUP.md) shows, then ask Claude or Codex to run `init-strategy <strategy-name>`. It
copies this template into a new folder, a git repository of its own, and its `SETUP.md` takes over.
A strategy ships with no licence: every right in it is its owner's.

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
| [`PIPELINE.md`](PIPELINE.md) | how the code runs, step by step, and how to debug it — written once the pipeline has run |

Every `Experiments/Experiment_N/` holds three more, and the split is the point: `BLUEPRINT` is
frozen so a result cannot reshape its question, `JOURNAL` is append-only so the path is
recoverable, and `FINDINGS` is rewritten so there is one current answer.

---

## What is in here

The eight steps, and the folder each one owns. Each stage reads only from the one above it. Every
file is already here as a description of what belongs in it — a `.py` file as its docstring, a
notebook as its markdown cells — to be filled in with the strategy's own.

| # | Step | Folder | What belongs in it | It prevents |
| --- | --- | --- | --- | --- |
| 1 | **Bibliotheca** | `Bibliotheca/` | `BIBLIOGRAPHY.md`, the sources and leads; one note per paper in `Papers/`, one per chapter in `Books/`; `LOG.md`, what was read and when | backtesting a hunch you cannot defend |
| 2 | **Universe** | `Universe/` | `Investable_Universe.csv`, **the seed**, one row per security, delisted names kept; `universe_marimo.py`, which writes `Security_Master.csv` and `Data_Issues.csv` | survivorship bias |
| 3 | **Data** | `Data/` | the drivers `curator.py`, `refinery.py`, `analyzer_marimo.py`; `hand_supplied.py` for the index and factor files; `c_*` columns in `Curator/custom_calculations.py`, `r_*` in `Refinery/custom_calculations.py` | results that came from broken inputs |
| 4–6 | **Portfolio, Backtest, Attribution** | `Experiments/` | the four shared modules; one `Experiment_N/` per idea, with its three documents, its notebook and its `Portfolio/`, `Backtest/` and `Attribution/` outputs; beside the notebook, the scripts that check its sizing against the library, attribute its books apart and write the KaxaNuk app's workbooks | a book nobody could hold, paper returns, factor beta sold as alpha |
| 7 | **Paper trading** | `Paper_Trading/` | `BITACORA.md`, the gate; `promote.py`, `daily_update.py`, `record.py`; one frozen book per `Paper_Trading_N/` | plumbing problems on day one of funding |
| 8 | Production | **elsewhere** | real capital, real monitoring, a real drawdown policy | research that stays research forever |
| — | | `Config/` | `.env.template`, copied to `.env` with the keys and licences | |

**Committed:** the code, the notebooks (which save no output), the documents and the notes.
**Ignored:** every data file, every output and the PDFs, all regenerable — and `.env`, which is
never committed and cannot be regenerated.

---

## Starting your own strategy

Once setup is done, in this order; ask your assistant `next` at any moment and it says which comes
next. The letters are not the steps above.

- **A. The objective.** `OBJECTIVE.md`: the idea in one sentence and its claims, **before any paper
  is read**. Each claim's evidence starts as the question that would settle it.
- **B. The reading.** One note per paper or chapter in `Bibliotheca/`, the sources that argue
  against each claim included; then rewrite each claim's evidence from the notes.
- **C. The universe.** The seed, delisted names included: a list of today's names has deleted
  everything that failed.
- **D. The data.** Your `c_*` and `r_*` columns, then curator, `universe_marimo.py`, refinery and
  `analyzer_marimo.py`, in that order. The analyzer's measurements go straight into `RESULTS.md`.
- **E. The blueprint.** Choose the benchmark in `JOURNAL_1.md`, read the rule back on one worked
  date, then write `BLUEPRINT_1.md` before the rule: every prediction cited, its control and what
  would falsify it named.
- **F. The broad reading.** Papers on what the blueprint left open, as the journal's open threads.
- **G. The cycle.** Portfolio, backtest, attribution, until the notebook's Verify passes,
  `FINDINGS_1.md` rewritten as results change.
- **H. The results.** Every finished cycle to `RESULTS.md`, kept or rejected, with the claim it
  moved.

Then the gate in `Paper_Trading/BITACORA.md` — soundness S1 to S5, then performance P1 to P3 — or
Experiment 2, from E again.

---

## The libraries

| Module | Step | What it does | Status |
| --- | --- | --- | --- |
| **Data Curator** | 3 | pulls market and fundamental data from any provider onto one calendar | open source, on [PyPI](https://pypi.org/project/kaxanuk.data-curator/) |
| **Data Refinery** | 3 | cleans and reshapes the curated data into analysis-ready series | coming; `Data/refinery.py` until then |
| **Data Analyzer** | 3 | tests whether a feature carries signal before anything is modelled | coming; `Data/analyzer_marimo.py` until then |
| **Portfolio Construction** | 4 | turns a signal into weights, limits and a rebalancing rule | licensed |
| **Backtest Engine** | 5 | runs the rules over history with costs and no look-ahead | licensed |
| **Attribution Analysis** | 6 | splits the return into factor exposure and the part that is yours | licensed |

The licensed three come with the KaxaNuk Investment Lab (`lab@kaxanuk.mx`), are installed by hand
as their skills describe, and stay out of `pyproject.toml`, so no key enters version control. A
notebook **guards their imports**: without them it builds the books and says what waits. KaxaNuk's
skills teach your assistant every library and this process; they are one package,
[`KaxaNuk/Researcher`](https://github.com/KaxaNuk/Researcher), installed once for your user, so a
strategy installs nothing; a researcher made once with its `init-researcher` writes the objective,
the notes and the blueprint with you. Beside it: git for versions, an editor (PyCharm or VS Code).
KaxaNuk's platform, <https://www.kaxanuk.mx/lab>, drives the same pipeline from a workspace.

---

## Conventions

**The prefix says which stage owns a column, and so which file to open.**

| Prefix | Built by | Scope |
| --- | --- | --- |
| `m_*` | the provider, via the Curator | raw market data — never changed |
| `c_*` | `Data/Curator/custom_calculations.py` | **one security's own history** |
| `r_*` | `Data/Refinery/custom_calculations.py` | **securities against each other, per date**, and any column with a setting to sweep |
| `current_*` | `Data/refinery.py`, from the security master | **today's classification, not point-in-time** — never selected on |

- A `c_*` column that needs other securities belongs in the Refinery.
- **A sweep never costs a download:** a window or a fitted model is an `r_*` column, its arithmetic
  inputs `c_*`.
- A strategy column is named only in a notebook's setup cell and its rule, never in a shared module.

**The four shared modules in `Experiments/`** are shared so experiments stay comparable:
`securities_panel.py` reads the refined files into `dates x securities`;
`portfolio_construction.py` turns an eligible set into weights, one date at a time;
`backtest_engine.py` writes the weight file, runs the engine and reads results back;
`attribution_analysis.py` shapes the book and the index files for the attribution library.

---

## The example

[`us-golden-flow`](https://github.com/KaxaNuk/Researcher/tree/main/examples/strategy/us-golden-flow)
is these files worked through for one strategy, its own lines between the example markers. Copy it
whole to read or run it with `init-example`; never build on it.

**Next:** [`SETUP.md`](SETUP.md) to set up, then [`AGENTS.md`](AGENTS.md): the workflow, the bar
any new signal has to clear, and the five ways a backtest lies.
