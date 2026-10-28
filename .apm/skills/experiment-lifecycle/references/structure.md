# Repository structure

The canonical tree of a KaxaNuk Investment Lab strategy repository, as the **KaxaNuk Strategy
Template** holds it — `templates/strategy/` in `KaxaNuk/KaxaNuk-Researcher`, copied into a new
folder by `init-strategy`. The template ships the shape and every file the process expects in it:
the six folders, the documents at the root, and inside the folders each driver, module, notebook and
document. Each is a description of what belongs there — a `.py` file as its docstring, a marimo
notebook as its markdown cells — to be filled in with the strategy's own. The same files, worked
through for one strategy, are the example beside it, `examples/strategy/golden-flow/`, with that
strategy's own lines between example markers. **The template is the source of truth for this tree;
this file is a copy of what it looked like at the version named below**, kept by hand. When they
disagree, the template wins.

Template version: **0.20.0**. The template ships `Experiments/Experiment_1/` and
`Paper_Trading/Paper_Trading_1/`; the blanks for every experiment after the first are this skill's
`references/`. `Bibliotheca/Papers/`, `Books/` and `Notes/` appear with their first note.

```
<Strategy_Name>/
├── SETUP.md                     # how to get the repository and set it up - an agent can follow it
├── OBJECTIVE.md                 # the idea and its claims, written before any paper is read
├── RESULTS.md                   # executive summary compiled from FINDINGS_N.md, citing each
├── CHANGELOG.md                 # every version, newest first; what a version number means here
├── AGENTS.md                    # how work is done: first run, workflow, restrictions, the bar, the five lies
├── CLAUDE.md                    # one line: @AGENTS.md
├── README.md                    # the strategy's own: the idea, where it stands, a link to the template
├── LICENSE                      # MIT
├── pyproject.toml               # Python >=3.12,<3.14, uv-managed; the KaxaNuk libraries installed by hand are absent
├── .gitignore                   # everything regenerable, everything APM installs, everything binary, Config/.env
├── .gitattributes               # text=auto eol=lf, so a Windows checkout commits LF
├── Config/
│   └── .env.template            # three data-provider keys, one is enough, and the three Lab licences; copy to .env
├── Bibliotheca/                 # step 1
│   ├── BIBLIOGRAPHY.md          #   the index of sources and the leads, in Parts 0-5; no notes yet
│   ├── LOG.md                   #   what was read here, and when; empty until the first read
│   ├── Papers/Author_Year_Title.md      # one note per paper, beside its PDF; frontmatter source, citation, local_copy, read
│   ├── Books/Author_Year_Title/INDEX.md # one folder per book: its chapters, one note per chapter chosen
│   ├── Notes/                   #   clippings and transcripts — the three appear with their first note
│   └── Extracts/                #   the text a researcher's script pulls out of the PDFs, gitignored
├── Universe/                    # step 2
│   ├── Investable_Universe.csv  #   THE SEED, committed: main_identifier is the only required column
│   ├── seed.py                  #   only in the worked example: how its seed was built
│   └── universe_marimo.py       #   -> Security_Master.csv, Data_Issues.csv, Provider_Cache/ (gitignored)
├── Data/                        # step 3
│   ├── curator.py               #   Data Curator driver; --end-date refreshes it for paper trading
│   ├── hand_supplied.py         #   reads the Analytics Factory's index and factor files, in place or dropped in
│   ├── Curator/
│   │   ├── custom_calculations.py   # c_* columns: one security's own history
│   │   ├── Time_Series/         #   downloaded, gitignored — universe, cash proxy, benchmarks
│   │   ├── Benchmarks/          #   dropped in by hand: index holdings and returns
│   │   └── Factors/             #   dropped in by hand: factor-model returns
│   ├── refinery.py              #   the seam the Data Refinery library replaces
│   ├── Refinery/
│   │   ├── custom_calculations.py   # r_* columns: cross-sectional, fitted, or with a setting to sweep
│   │   └── Time_Series/         #   derived, gitignored — the panel every experiment reads, + current_*
│   ├── analyzer_marimo.py       #   where a feature earns a backtest or is dropped
│   └── Analyzer/                #   charts and the signal table, gitignored
├── Experiments/                 # steps 4-6
│   ├── securities_panel.py      #   the one panel loader; names no strategy column
│   ├── portfolio_construction.py    # eligible set -> weights, one signature; the library called inside it
│   ├── backtest_engine.py       #   the one path from a weight file to a number
│   ├── attribution_analysis.py  #   the hand-supplied inputs and the book's daily weights; what is missing, first
│   └── Experiment_N/            #   Experiment_1 ships, the first rule; N > 1 from this skill's references/
│       ├── BLUEPRINT_N.md  JOURNAL_N.md  FINDINGS_N.md
│       ├── experiment_N_marimo.py
│       ├── Portfolio/           #   step 4 output, gitignored, kept by .gitkeep
│       ├── Backtest/            #   step 5 output, gitignored, kept by .gitkeep
│       └── Attribution/         #   step 6 output, gitignored, kept by .gitkeep
└── Paper_Trading/               # step 7
    ├── BITACORA.md              #   the graduation gate: soundness S1-S5, performance P1-P3
    ├── promote.py               #   freezes an experiment that graduated into Paper_Trading_N/
    ├── daily_update.py          #   runs every frozen book each day; record.py keeps the record
    ├── record.py                #   the six tables, to CSV files, a DuckDB database or both
    └── Paper_Trading_N/         #   one frozen book: paper_trading_N.py, its files, FREEZE.json
```

## What is committed, and what is not

**Only source is committed:** code, the marimo notebooks, documents and the notes, the folder
skeleton kept by `.gitkeep`, `LICENSE`, and one seed file — `Universe/Investable_Universe.csv`. A
strategy repository also commits `uv.lock`, which pins what its results came from; the template and
the example ship none. Everything under `Data/` except code, every `Portfolio/`, `Backtest/` and
`Attribution/`, the PDFs and `Bibliotheca/Extracts/`, every chart, workbook and parquet and marimo's
`__marimo__/` cache is regenerated by running a stage or supplied by hand, and is gitignored by
extension and by path. `Config/.env` is gitignored **because it is secret**; the template is
committed. Everything APM would install — `.claude/`, `.agents/`, `.codex/`, `.cursor/`,
`apm_modules/`, `apm.lock.yaml`, `.mcp.json` — is gitignored as well, though a strategy installs
nothing: the skills are installed once for the user, by
`uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/KaxaNuk-Researcher --target <agent>`.

**A marimo notebook saves no output in itself**, so there is nothing to strip before a commit. It
is a Python file: run it as a script, or open it to read and run cell by cell. `--group notebook`
adds marimo, which a bare `uv sync` leaves out; `uv run` adds it without removing a hand-installed
engine:

```bash
uv run python Experiments/Experiment_1/experiment_1_marimo.py
uv run --group notebook marimo edit Experiments/Experiment_1/experiment_1_marimo.py
```

## Starting a strategy from the template

Follow the template's own `SETUP.md`. It puts everything into **one folder**, the strategy root,
with `.venv/` beside the process folders rather than in a directory above them; `uv sync` fetches
Python itself; and the agent skills are installed once for the user, never in the strategy.
**Once a KaxaNuk library is installed by hand, a bare `uv sync`
removes it** — `backtest-engine-runs` says which commands keep it. Then follow the order of work in
`SKILL.md`, section 6: the objective first, the reading for its claims, the universe, the data, the
benchmark and `BLUEPRINT_1.md`, and only then the rule.

## Adding Experiment N to an existing strategy

From the repository root:

```bash
N=2
base="Experiments/Experiment_$N"
for d in Portfolio Backtest Attribution; do
  mkdir -p "$base/$d" && : > "$base/$d/.gitkeep"
done
```

Then copy the three templates from this skill's `references/` into `$base/`, renaming `N`, and copy
`experiment-notebook_marimo.py` to `$base/experiment_${N}_marimo.py`. The notebook is Experiment
1's: retitle it `Experiment N`, replace every `_1` in it with `_N`, and delete the sentences that
only apply to Experiment 1. Then, in the notebook, declare the experiment's columns in section 0,
import the panel loader from `Experiments/securities_panel.py` in section 1, write the rule in
section 2 and hand its sizing to `portfolio_construction.py`. **`BLUEPRINT_N.md` is written before
the rule**, and does not change afterwards.
