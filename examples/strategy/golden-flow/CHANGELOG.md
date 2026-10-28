# Changelog

Every notable change to this repository, newest first. The format is
`## X.Y.Z (YYYY-MM-DD)` with `### Added / Changed / Deprecated / Fixed / Removed`, and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) in its numbering.

## What a version number means here

This is a research repository, not a library, so there is no public API to version. What the team
depends on is **the results and the pipeline that produces them**, so that is what the number
tracks:

| Bump | Means | Triggered by |
| --- | --- | --- |
| **MAJOR** | **Published results are invalidated.** Anything quoted from an earlier version has to be re-derived before it can be repeated | Changing the universe, the date window, the backtest engine or its cost model, or the definition of an existing strategy. Removing a stage |
| **MINOR** | **New capability; existing results still stand** | A new experiment, signal, stage, diagnostic or document. Anything additive |
| **PATCH** | **Nothing about any result changes** | Bug fixes in tooling, documentation, repository hygiene, refactors that produce identical output |

Three conventions follow from reading it that way:

- **A result that changes is a MAJOR bump even if the code change was one line.** Severity is
  measured in what a reader has to throw away, not in the size of the diff.
- **Re-running the pipeline on refreshed data is not a version bump at all.** The strategy did not
  change; only the data did. Say so in the entry and leave the number alone.
- **While on `0.x`, a result-invalidating change bumps MINOR** — the standard pre-1.0 convention.

**1.0.0 is reserved** for this strategy's first book on **paper trading** (step 7), its results
reproduced from a clean clone. Until then the leading zero is doing real work: it says the results
are still moving.

## How to write an entry

One entry per change-set, newest at the top. Under the heading, **one sentence saying what a reader
has to do differently** — that is the part people actually read. Then the lists, each item written
for somebody who was not in the room:

- **Say what moved and why, not what file you touched.** "The regime model lives in the Refinery so
  a penalty sweep costs no download" is an entry; "updated custom_calculations.py" is a diff.
- **Name anything that invalidates a number**, and say which number.
- **A removal is a change-set too.** Deleting a stage that nobody could trace is worth an entry.

---

## 0.18.0 (2026-10-27)

**MINOR, result-invalidating** — Golden Flow is curated again from its live repository at 0.21.0,
Experiment 1 only, on the owner's decision of 2026-10-27: Sharadar prices and the KN US Equity Core
from 1998, a monthly rule from 2000 to 2026, every cost and the cash's interest inside the engine.
Read through the new two-layer gate, Experiment 1 is **sound and regime-dependent**: every
soundness criterion holds; the book beats its control in 2000–2008 and 2018–2026 and the Core only
in 2018–2026, and loses to the Core and `SPY` on Sharpe over the whole window. It is not paper
traded.

**What to do differently:** say `init-example` for a fresh copy. Running it needs a Sharadar key,
the Lab's licences and, for step 6, Attribution Analysis 0.5.0.

### Changed

- **Experiment 1**, re-curated: the blueprint of 2026-10-23, the journal to 2026-10-24 with the
  owner's decision of 2026-10-27, the findings read in two layers. Every figure is quoted from the
  live repository's findings, measured on Backtest Engine 0.67.0 and Attribution Analysis 0.5.0;
  none is computed anew.
- **Experiments 2 and 3**, their notes, claims, columns and rows stay out.
- **The seed**: 2,199 listings, tickers and dates only. `Universe/seed.py` writes them from
  Sharadar's catalogue, which it caches, and runs before the universe notebook.
- **The notebooks** are marimo; the data stage is Sharadar's, in Parquet.
- **`Bibliotheca/`**: Daniel and Moskowitz (2016), which the blueprint cites, is carried in; every
  note's implications are rewritten for the Sharadar figures.

### Removed

- **`Paper_Trading/Paper_Trading_1/`**, the FMP book of 2026-10-06, retired as the live repository
  retired it on 2026-10-24. The step-7 scripts stay, with no book in `BOOKS`.

## 0.17.8 (2026-10-21)

**PATCH** — the rules say what never leaves a strategy, and the `security` skill checks it before a
push. Nothing about any result changes.

**What to do differently:** say `security` in the strategy before you push it.

### Changed

- **`AGENTS.md`**, *Other standing rules*: a leaked key points at `security`'s *A key leaked*, and
  a new rule keeps keys, licences, holdings, licensed data and confidential material out of every
  copy, with the check run before a push.

## 0.17.7 (2026-10-18)

**PATCH** — Paleologo's index names chapter 11 as the appendix it is; prose only, no number moves.

**What to do differently:** nothing.

### Fixed

- **`Bibliotheca/Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md`**, *What this book
  does not settle*: chapters 7 and 11 were "the hedging and optimisation chapters", but the
  book's contents title chapter 11 *Appendix*. The line names chapter 7, *Manage Factor Risk*,
  and the quantitative appendix, chapter 11, both still out of reach here.

## 0.17.6 (2026-10-18)

**PATCH** — Paleologo's index gains its chapter table; prose only, nothing re-run, no number moves.

**What to do differently:** nothing.

### Fixed

- **`Bibliotheca/Books/Paleologo_2021_Advanced_Portfolio_Management/INDEX.md`** has the chapter
  table a book's index holds, which the library check found missing: chapters 3, 5, 6, 8 and 9
  *read*, the ones its sections cite, each linked to its sections; 1, 2, 4, 7, 10 and 11
  *skipped*. No copy of the book is kept here, so the table gives no pages. Its sections are
  unchanged. `Bibliotheca/LOG.md` records the fix, and `BIBLIOGRAPHY.md` says the sections sit
  under the table.

## 0.17.5 (2026-10-18)

**PATCH** — the first save asks only a name; prose only, nothing re-run, no number moves.

**What to do differently:** nothing.

### Changed

- **`SETUP.md`**, the note for the agent: when the first commit wants a git identity, it asks only
  a name, in one open message, and sets `user.email` to `"<>"`; the shared lines as the template's
  0.19.3.

## 0.17.4 (2026-10-11)

**PATCH** — the README and the status banner say the figures are hypothetical; prose only, nothing
re-run, no number moves.

**What to do differently:** nothing.

### Changed

- **`README.md`**: *Hypothetical results*, after the opening paragraph. Every return, Sharpe and
  drawdown is simulated, never traded, and past returns do not guarantee future returns. All but
  one come from a backtest on the past prices the strategy was designed on, one of 107 portfolios
  tested, with modelled costs, against KaxaNuk's own index. The one is the 24.9% drawdown the
  engine shows just after the window, before the book was frozen.
- **`README.md`**, *What it is, and what it is not*: the companies that receive what your
  researcher reads, by example: Anthropic for Claude, OpenAI for Codex, Google for Gemini.
- **`README.md`**, *What it is, and what it is not*: it no longer ends with an address; the
  researcher's list says where to write, Research Models such as this one to
  `research@kaxanuk.mx`.
- **The Analytics Factory's files**, the index's master of listings included, are asked of
  `analytics@kaxanuk.mx`: in `README.md`, `SETUP.md`, `Config/.env.template`,
  `Data/hand_supplied.py` and `Universe/seed.py`, the shared lines as the template's 0.19.2.
- **`AGENTS.md`**, above the status banner: a shorter caveat, pointing to the README's
  *Hypothetical results*.

The frozen book in `Paper_Trading/Paper_Trading_1/` is unchanged: `FREEZE.json` hashes its files.

## 0.17.3 (2026-10-10)

**PATCH** — the shared lines move as the template's 0.19.1 does, and the README says what the
example is and is not; prose only, nothing re-run, no number moves.

**What to do differently:** nothing.

### Changed

- **The shared lines** of `AGENTS.md`, `SETUP.md`, `OBJECTIVE.md`, `RESULTS.md`,
  `Bibliotheca/BIBLIOGRAPHY.md`, `Paper_Trading/BITACORA.md` and `.gitignore`, as the template's
  0.19.1.
- **`README.md`**: *What it is, and what it is not*, after the banner: the figures come from a
  backtest on past prices, shown to teach the method, never a promise or a recommendation. Yahoo
  Finance's data is for learning, under Yahoo's own terms. Each idea is said once.
- **The banners of `README.md` and `AGENTS.md`** say the headline figures come from a backtest.

The frozen book in `Paper_Trading/Paper_Trading_1/` is unchanged: `FREEZE.json` hashes its files.

## 0.17.2 (2026-10-10)

**PATCH** — the shared lines of `AGENTS.md` and `Experiments/attribution_analysis.py` move as the
template's 0.19.0 does; prose only, nothing re-run, no number moves.

**What to do differently:** nothing.

### Changed

- **`AGENTS.md`**: a Lab library's code is never read, quoted or copied, and a library trap is told
  by the call, the error and the versions, never by the library's traceback lines.
- **`Experiments/attribution_analysis.py`**, its docstring: the factor directory as the
  documentation and runs describe it.

The frozen book in `Paper_Trading/Paper_Trading_1/` is unchanged: `FREEZE.json` hashes its files.

## 0.17.1 (2026-10-09)

**PATCH** — the example now lives at `examples/strategy/golden-flow/` in the package; prose only,
nothing re-run, no number moves.

**What to do differently:** nothing.

### Changed

- **`AGENTS.md`**, the example's own lines under *How work reaches `main`*: the folder is
  `examples/strategy/golden-flow/` of the KaxaNuk Researcher, which keeps its examples by kind, as
  it keeps its templates. The strategy is still `golden-flow`.
- **`SETUP.md`**, *Step 1*: the link that reads the example on GitHub points to
  `examples/strategy/golden-flow`, and the new folder is `golden-flow` *unless you choose another
  place* — `init-example <name>` now names an example.

The template moves to 0.18.3 for the same reason; no line shared with it changes.

## 0.17.0 (2026-10-08)

**MINOR** — the example's list of stocks is tickers and dates only, 883 of the record's 896
listings, and the example can run on Yahoo Finance with no key, for learning, after the changes its
README names. The record's figures stay as they were; a run on this list lands further from them
than before, and its window may open later.

**What to do differently:** quote the record's figures as the record's; to run without an FMP key,
follow *Run it* in the README, and read that run as a lesson, not a result.

### Changed

- **`Universe/Investable_Universe.csv`**, and the frozen book's copy, the same file: four columns,
  `main_identifier`, `index_identifier`, `valid_from` and `valid_to`, and the 883 rows whose FMP
  symbol, verified or not, is the index's own (Sharadar) ticker, departed names included, in the
  same order; FMP does not carry about 80 of them, and the register names them as missing. The 13
  left out: eight with no FMP symbol, `AET`, `CBI`, `COL`, `CPN`, `CVC`, `CY`, `EVHC` and `NBL`, and
  five FMP prices under another ticker, `BF.B`, `BRK.B`, `NEBLQ`, `WLL2` and `WOLF2`. No ISIN,
  company name or match column is left in this version of the example. The frozen copy no longer
  matches its hash in `FREEZE.json`, which is never edited: `daily_update.py` reports it as
  `unfrozen-input`.
- **`Universe/seed.py`** writes those four columns, and only a listing whose FMP symbol, verified
  or not, is the index's own ticker.
- **`Universe/universe.ipynb`** reads no name, ISIN or match from the seed: the master takes the
  name and the ISIN from FMP's profile; every symbol, not only an unverified one, is checked against
  its listing's membership, and one its prices contradict leaves the seed; the register's first
  row, *not in the seed*, names every weighted listing the seed lacks. Verify accepts a weighted
  listing the register names, and checks that it names none the seed holds: still 13 checks.
- **`experiment_1.ipynb`**: the exclusions it expects are the blueprint's but `NE`, which the seed
  no longer holds.
- **`Data/hand_supplied.py`**: `read_listing_keys` says which listings the seed lacks.
- **`Data/refinery.py`**, marked: a listing the seed does not map, such as `BRK.B`, carries no
  weight in the panel and is named in the register.
- **`README.md`**: Yahoo Finance can run the example with no key, for learning, through the Data
  Curator's extension, once `Data/curator.py` is switched to it and two things that do not work as
  they stand are changed: the universe notebook's FMP profiles, and the traded value, fill and
  commission, built from a VWAP Yahoo does not send. It loses the 178 names that left the market;
  FMP, Sharadar or LSEG for a precise experiment. *Seed*, the universe's row and *What a correct
  run shows* describe this seed beside the record's, and say a run lands further from the record:
  near 91% of the index's weight priced on 2015-01-02, against the 90% floor, so the window may
  open later. The paper book's seed joins what fails `FREEZE.json`; the Lab line as the template's.
- **`SETUP.md`**, marked: Yahoo Finance in *What a run needs*, after the changes the README names,
  and 883 profiles for a copy. Shared: the access line moves as the template's 0.18.2.
- **`RESULTS.md`** and **`FINDINGS_1.md`**, marked: one line each, that their coverage figures are
  the record's.
- **`AGENTS.md`**, marked, row 1: a member FMP does not price under the index's ticker is named in
  the register rather than raised on, and the 92.97% of 2015-01-02 is the record's.
- **`Paper_Trading/BITACORA.md`**, marked: a dated line *in this copy* says the book's seed was
  rewritten and `daily_update.py` reports `unfrozen-input`.
- **`LICENSE`**: as the template's 0.18.2.

## 0.16.1 (2026-10-08)

**PATCH** — the README explains three more of its words, *book*, *paper trading* and *Sharpe*, and
the lines shared with the template move as its 0.18.1 does. No number moves.

**What to do differently:** nothing.

### Changed

- **`Paper_Trading/BITACORA.md`**, *Running it daily*: the Windows line is for Command Prompt, its
  days quoted, `"MON,TUE,WED,THU,FRI"`, which PowerShell split at the commas; it starts
  `schtasks --%` in PowerShell, and `MSYS_NO_PATHCONV=1 schtasks` in Git Bash, which turned
  `/Create` into a path. The folder's path is quoted there and in the cron line.
- **`SETUP.md`**, *What you need first*: git from `winget install --id Git.Git -e
  --accept-source-agreements --accept-package-agreements`, which does not stop to ask; GitHub
  Desktop leaves as a way to get it, since the git it brings is not on the command line.
- **`Universe/universe.ipynb`**, section 1: a line of 160 characters wrapped at 100.

- **`README.md`**: *book*, *paper trading* and *Sharpe* join *Words used here*; the access line no
  longer offers Portfolio Construction, which the example does not install.

## 0.16.0 (2026-10-08)

**MINOR** — the example does what its pages say: without the Backtest Engine, or with a licence
that does not validate, the experiment skips step 5 and reaches its Verify, where it stopped on a
`KeyError`. No number moves: the path with the engine is unchanged.

**What to do differently:** nothing.

### Changed

- **`SETUP.md`**: nothing runs yet, and why; the hand-over names `objective`; *a few minutes*;
  *What you need first* names the assistant and the KaxaNuk Researcher; one allowed check of
  `Config/.env`, names only, and a plain line on opening it; *Paper trading, daily* moves to
  `Paper_Trading/BITACORA.md` as *Running it daily*, the cron line with uv's full path and the dry
  run described as it behaves; `daily_update.py` and `.gitignore` point there.
- **`AGENTS.md`**: the `Config/.env` rule gives that one check.
- **Experiment 1 is the first rule**, not *the benchmark*, in `RESULTS.md`, `FINDINGS_1.md` and
  `experiment_1.ipynb`; the notebook's section 5 names `KN_ANALYTICS_PATH`, and its section table
  the benchmark reconciliation. `OBJECTIVE.md` speaks to its owner. The `CHANGELOG.md` head reserves
  1.0.0 for this strategy's first book on paper trading.
- **`pyproject.toml`**: `pandas>=2.3.3,<3` — every published figure ran on pandas 2; the cap lifts
  once the example runs on pandas 3, and a Data Curator that needs 3 lifts it first.

- **The example's own code**: `experiment_1.ipynb` guards every cell that reads the engine's runs
  (`ENGINE_READY`), prints *step 5 skipped* with the reason, runs attribution only after a priced
  rule, and checks the weight files when the engine is absent; `WORKERS` is at most the machine's
  cores; `universe.ipynb` retries a profile up to four times, 30 seconds apart, on HTTP 429 or a
  dropped connection, as `Universe/seed.py` does; `portfolio_construction.py`'s `bounded_book`
  docstring says the score a date is sized on is the prior close's.
- **`README.md`**: three plain sentences under the title, figures copied from `RESULTS.md`; the
  glossary after *How to read it*, with *golden cross* and *seed*, and *the first rule's book*;
  *Run it* starts with the environment and the keys; *What a correct run shows* gives 890 names on
  the committed seed (892 on the record's), each notebook's Verify line and what a fresh download
  can add; the daily run in a copy stops and exits 2. The banners lose *Replace this line*.
- **`SETUP.md`**, marked: the hand-over sends the reader to the README, and *Next* says nothing is
  written here.

## 0.15.7 (2026-10-08)

**PATCH** — the shared lines move as the template's 0.17.0 does; the example's own code is
unchanged, and marked lines say its record predates the split check and the worked-date read-back.
No number moves.

**What to do differently:** nothing.

### Changed

- **`AGENTS.md`**: *Keys join, or the pipeline stops* — every join between the index's files and
  the book goes through the seed's two keys (#13); *The rule is read back before its blueprint* —
  one plain sentence and one worked date's book, the owner's yes a `JOURNAL_N.md` entry saved before
  the blueprint, so two entries come before Experiment 1's (#15).
- **`Universe/universe.ipynb`**: every register row has a severity, blocking first, a blocking row
  excluded by name; a further check, *traded value broken at a split* (#14); a shortfall is a member
  the provider does not carry, never a listing whose key did not join; Verify, for a seed taken from
  an index, raises on a weighted listing with no seed row, a key used twice, or one ISIN on two rows
  over the same dates (#13); section 1 says an ISIN repeats only where a renamed security's rows
  follow each other in time.
- **`Experiments/Experiment_1/experiment_1.ipynb`**: section 0 reads the exclusions from the
  register's blocking rows, never typed; section 8 raises if the book, the control or any arm holds
  one (#13).
- **`Experiments/Experiment_1/JOURNAL_1.md`**, its preamble, and **`Data/curator.py`**, its
  docstring: the read-back entry (#15); traded value checked across every split (#14).

- **Marked, the example's own**: what the record's code does not do, since the checks came after it
  — its universe register lists its rows as its checks run, not blocking first, and its Verify runs
  no ISIN check (its seed holds no ISIN twice); its experiment Verify asserts the exclusions on the
  book, not on the control and each arm, which come from the same eligible set. And: the universe
  notebook says the split check was added after the record and this copy's run did not perform it;
  `AGENTS.md` says Golden Flow's rule was read back as a sentence, *bounds set the count*, without a
  worked date's book.

## 0.15.6 (2026-10-08)

**PATCH** — the shared `AGENTS.md` and `SETUP.md` lines move as the template's 0.16.0 does. No
number moves.

**What to do differently:** nothing.

### Changed

- **`AGENTS.md`**, *Other standing rules*: a new Lab library build is a change-set, between
  experiments, never during one — the researcher says when one is out, keeping the date of that
  weekly check in this repository's git config (`kaxanuk.labnext`), never saved; `uv lock
  --upgrade-package <name>`, then `uv sync --group notebook --inexact`, a re-run from a wiped copy
  and a `CHANGELOG.md` entry naming any number that moved; a book on paper runs on the Data Curator
  it was frozen with.
- **`SETUP.md`**, step 2: *A newer Lab library*, the same in three lines.

## 0.15.5 (2026-10-08)

**PATCH** — the shared `Config/.env.template` and `SETUP.md` lines move as the template's 0.15.1
does. No number moves: the record's book was sized by `Experiments/portfolio_construction.py`
itself, without the library, which it does not need.

**What to do differently:** nothing.

### Changed

- **`Config/.env.template`**: `KNPC_API_KEY_KAXANUK`, Portfolio Construction's licence since its
  2.0.0 — the library reads it from the environment or a `.kaxanuk_license` file, and a driver that
  loads this file into the environment first passes it on.
- **`SETUP.md`** step 3 names it beside the other two licences, and says the library reads it from
  the environment or `.kaxanuk_license`; *Paper trading, daily* says a saved licence check covers 3
  days offline from Backtest Engine 0.67.0 (7 before), the first run on it needing the network.
- **`Paper_Trading/BITACORA.md`**: paper trading is the last step inside this repository, not
  inside the Investment Lab, whose libraries run steps 3 to 6.

## 0.15.4 (2026-10-08)

**PATCH** — the shared lines of `AGENTS.md` and `SETUP.md` move as the template's 0.15.0 does, and
a marked line in `SETUP.md` says an untracked `uv.lock` after `uv sync` is expected here. No number
moves.

**What to do differently:** nothing.

### Changed

- **`AGENTS.md`**, *The blueprint is committed before the rule*: a document the researcher writes on
  the owner's go — a note, `OBJECTIVE.md`, `BLUEPRINT_N.md`, a `JOURNAL_N.md` entry, a line in
  `Bibliotheca/LOG.md` — is saved as its own version on that go, with no `CHANGELOG.md` entry,
  version bump or ruff gate; the blueprint is saved alone; the go is the owner's signature, on
  which the assistant removes the template's blockquote. *Before any commit to `main`* names those
  saves as the exception.
- **`SETUP.md`**: the paragraph about publishing the repository and the hand-over's line about a
  remote leave — a copy off the computer is made only when the owner asks, with `backup`; the git
  name and e-mail are asked for in plain words.

## 0.15.3 (2026-10-08)

**PATCH** — the shared lines of `SETUP.md` and `AGENTS.md` name APM 0.33.0 and the update in full,
as the template's 0.14.1 does. No number moves.

**What to do differently:** nothing.

### Changed

- **`SETUP.md`, `AGENTS.md`**: `uvx --from apm-cli==0.33.0 apm install -g` and
  `uvx --from apm-cli==0.33.0 apm update -g`.

## 0.15.2 (2026-10-07)

**PATCH** — the 0.15.1 entry, which records this copy, now lists every figure Golden Flow 0.15.1
corrected. It left out three, which `FINDINGS_1.md` already carried, and `RESULTS.md` and a note
in part; its first line said no number moved; and it said Golden Flow's own sentences, where a
module has them, open its marked code, where each such comment was written for this copy. No
other file changes but `pyproject.toml`'s version, and no number moves. This version line is the
example's own: it counts changes to this copy, which stays Golden Flow 0.15.1's.

**What to do differently:** nothing.

### Fixed

- **The 0.15.1 entry** lists the three figures under *Fixed*, says in its first line that the
  copy carries them, and says the comments opening the marked code were written for this copy.

## 0.15.1 (2026-10-07)

**PATCH** — Golden Flow, copied into the KaxaNuk Researcher as its worked example. The copy moves
no number; it carries three figures Golden Flow 0.15.1 corrected to the record run's outputs,
listed under *Fixed*.

**What to do differently:** nothing to migrate. Copy it with `init-example`; the index and factor
files come from KaxaNuk's Analytics Factory, as `SETUP.md` says.

### Changed

- **The documents are shortened for a reader.** `README.md` says how to read the example and how
  to run it, states its rule, and shows how it uses the KaxaNuk Investment Lab and the Analytics
  Factory. Elsewhere, Golden Flow's lines sit between markers, after the template's guidance they
  answer.
- **`JOURNAL_1.md` starts on 2026-10-05.** It keeps every entry from then on, whole, except the
  2026-10-06 entry that retired the brainstorming file. Private names, a local path and a branch
  name are replaced in square brackets. A dated entry at the end records this copy.
- **Eighteen notes are carried, and five are kept only as leads.** Each carried note keeps *What it
  says* word for word. Its implication is rewritten and dated, after `FINDINGS_1.md` reported.
- **The code is Golden Flow 0.15.1's, with these differences:**
  - each shared module opens with the template's docstring; where its marked code opens with a
    comment, the comment was written for this copy, from what Golden Flow's docstrings and
    records say about the module;
  - each notebook keeps the template's markdown cells, with Golden Flow's paragraphs between
    markers; every code cell is Golden Flow's, starts `# EXAMPLE-ONLY CELL`, and has no outputs;
  - `Data/hand_supplied.py` reads the Analytics Factory's own file names,
    `KN_US_Equity_Benchmark_Holdings.csv` and `KN_US_Equity_Benchmark_Returns.csv`. They are
    byte-identical to the files Golden Flow read under the KN US Equity Core's name: md5
    `eba4bf64ffa8de5d650e4e2c4b21844d` and `1668b564582f1871d7e4a6f39896e50a`;
  - the Analytics Factory is named in place of Golden Flow's older name for it, in comments,
    docstrings and one message, and a line this made longer than 100 columns is rewrapped;
  - `Universe/seed.py` takes `--index-master` as a required argument and names no machine path.
    Its shorter docstring says it overwrites the committed seed, and ships to show how the seed was
    built;
  - `.gitignore`, `Config/.env.template`, `.gitattributes`, `LICENSE`, `CLAUDE.md` and
    `pyproject.toml` are the template's; `pyproject.toml` is named `golden-flow`, at 0.15.1;
  - no `uv.lock` is committed, so the library versions resolve when `uv sync` runs. The recorded
    figures were run on Backtest Engine 0.66.0 and Attribution Analysis 0.2.0.
- **Byte for byte:** the seed, `Universe/Investable_Universe.csv`, and in
  `Paper_Trading/Paper_Trading_1/` the frozen copies and `FREEZE.json`.
- **`Paper_Trading_1` is a record here, not a running book.** Its frozen security master is not
  shipped, and `Data/Curator/custom_calculations.py` and `paper_trading_1.py` no longer match the
  hashes registered for them. `daily_update.py` stops the book, as `Paper_Trading/BITACORA.md` says.

### Fixed

Golden Flow 0.15.1's own fixes, which this copy carries:

- **`FINDINGS_1.md` keeps the promises `Paper_Trading/BITACORA.md` made before the run.** It
  publishes all twenty random books — each drawing, on the rule's dates, as many index members as
  the rule holds. Each comes with its idiosyncratic return (the part no factor explains), its
  Sharpe and its CAGR (compound yearly return).
- **The sweep is published in full.** Each of its eight perturbed settings sits beside its control,
  with both margins. The golden cross is a 50-day average above the 200-day; a control is the same
  setting without it. Beside the cap rows, how often the cap binds: 620 of 1,408 rebalance dates at
  15%, 341 of 1,381 at 20% and 141 of 1,358 at 25%.
- **The timing arm is stated.** The shifted-entry timing arm was not run, so timing is not
  separated from selection.
- **11.81 years**, in `FINDINGS_1.md` and `RESULTS.md`, is labelled the engine's count: 2,976
  weekday steps after the first day, over 252. The window spans 11.41 calendar years.
- **`OBJECTIVE.md` quotes the owner with "top 35"**, as the journal records it, and then the answer
  that retired the count. The earlier quote had dropped the number without an ellipsis.
- **Three figures, to the record run's own outputs.** The realistic commission row adds 0.43
  points of CAGR, not 0.42: the margin taken before rounding, as every other margin is. The
  members FMP does not price held at most 0.12% of the index's weight in 2022, on its first 37
  trading days, not under 0.1%. The sell-at-t−1 rule changed every first-attempt book but two,
  the rule's and the control's 2023–2026 sub-periods, which came back identical and are read
  from that attempt's cache. The trial count stands at 107.

## 0.15.0 (2026-10-06)

**MINOR** — Experiment 1, on the KN US Equity Core, the Analytics Factory's index of about 600 names
a day. The rule holds the members in a golden cross, ranked and weighted by 63-day traded value,
none above 20% and none below 1%. Measured on 2026-10-06 from a wiped working copy, it compounds at
20.33% a year at a Sharpe of 0.842 over 2015-01-02 to 2026-06-01, net of costs. Its control made
19.73% at 0.763, and the KN US Equity Core 13.05% at 0.713. Nine tenths of the excess return is
factor exposure. The book passed criteria 1 to 4 of the paper-trading gate. The owner signed the
fifth the same day, and it went to paper trading as `Paper_Trading_1`.

**What to do differently:** quote every figure as in sample; `FINDINGS_1.md` sets each beside its
comparison.

### Added

- **`OBJECTIVE.md`**, from the owner's words: the idea and its three claims, the signal, the sizing
  and the construction.
- **`Bibliotheca/`**: the notes behind the claims.
- **The seed**, `Universe/Investable_Universe.csv`: the 896 listings that were KN US Equity Core
  members on some date from 2015-01-02.
- **The data stage**, run on 2026-10-06: 892 names asked of FMP through 2026-10-05, 809
  downloaded and 83 it does not carry; `CY` and `NBL` dropped by the universe notebook, their FMP
  prices contradicting their membership.
- **The drivers, the modules and three notebooks** — universe, analyzer and experiment. Each
  notebook ends in a Verify section that raises when a check fails.
- **Experiment 1's `BLUEPRINT_1.md`**, committed before the rule was coded, with its `JOURNAL_1.md`
  and `FINDINGS_1.md`.
- **`Paper_Trading_1`**, the book frozen on 2026-10-06. What it must show on paper, and when it is
  stopped, were registered in `Paper_Trading/BITACORA.md` before its first day.

### Provenance

Golden Flow is the KaxaNuk Investment Lab's reference strategy, worked in a repository of its own.
The KaxaNuk Strategy Template was first extracted from its version 0.9.0. This copy is curated from
its version 0.15.1, and every figure is as that version recorded it. Two earlier versions of
Golden Flow tested the thirty most traded names of another index. They are not part of this
example, but the 23 and 14 books they priced count in Experiment 1's trial count of 107 books.
