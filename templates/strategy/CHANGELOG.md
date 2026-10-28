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

## 0.20.0 (2026-10-27)

**MINOR** — the template takes what Golden Flow 0.16.0 to 0.21.0 learned, the proposals of issue
KaxaNuk/Researcher#41: marimo notebooks in place of Jupyter, Sharadar in the curator, the adjustment
rebuilt from the exact close, every cost and the cash inside the engine, a Verify that excludes a
truncated run by name, the band read back beside the rule, and a graduation gate in two layers.

**What to do differently:** nothing for a strategy already made, whose files are its own; a new one,
made with `init-strategy`, starts from this. Its experiments read the gate in two layers: soundness,
then performance.

### Changed

- **The notebooks** are marimo, run as scripts, nothing saved in them to strip:
  `Universe/universe_marimo.py`, `Data/analyzer_marimo.py` and
  `Experiments/Experiment_1/experiment_1_marimo.py` replace the three Jupyter notebooks.
  `pyproject.toml`'s notebook group is marimo, without jupyterlab or ipykernel, its ruff ignores a
  marimo notebook's generated cell signatures, and `.gitignore` ignores `__marimo__/`.
- **Universe**: the seed holds identifiers and dates only, and the name and the permanent identifier
  come from the provider's cached catalogue; the register reads spliced files and traded value
  across a split by the signature the Curator corrects.
- **Data**: `Data/curator.py` downloads Sharadar in batches, rebuilds the adjustment from the exact
  close as `c_*` calculations, carries spin-offs, checks every file against the provider and
  corrects volume adjusted twice; every per-security file is Parquet, through the new
  `Data/time_series.py`; a cash-rate series rides beside the benchmarks; and
  `Data/Refinery/custom_calculations.py` says a new experiment's signal on data already downloaded
  is an `r_*` column. The Data Curator floor is 0.51.0.
- **Experiments**: `backtest_engine.py` prices every cost and the cash inside the engine —
  basis-point commission, spread-and-impact slippage with a flat half-spread re-pricing beside it,
  cash at a rate file less a broker's spread — in batches, a truncated run excluded by name;
  `portfolio_construction.py` adds the monthly calendar and the no-trade band, with blocking rows
  in place of a sale the day before a series stops; `attribution_analysis.py` names its
  methodology, the book's cash a segment of its own.
- **The experiment's documents**: the blueprint asks for costs and cash in the engine, the band
  read back and the evidence for each soundness row; the findings read the gate in two layers,
  soundness S1 to S5 and performance P1 to P3, with three outcomes — graduates, sound and
  regime-dependent, not sound; the journal reads the band back beside the rule.
- **Paper trading**: `BITACORA.md` and `promote.py` freeze an experiment that graduates, or one
  signed off as sound and regime-dependent on probation: its regime prediction, at least 12 months
  and its review registered before day one, and paper alone never sending it to production.
- **`AGENTS.md`, `README.md`, `SETUP.md`, `RESULTS.md`**: marimo throughout, the two-layer gate,
  the band, the costs and the cash in the engine, and the `r_*` rule.

## 0.19.5 (2026-10-27)

**PATCH** — the KaxaNuk Researcher's address on GitHub is now `KaxaNuk/Researcher`. Nothing about
any result changes.

**What to do differently:** nothing.

### Changed

- **`SETUP.md`**, **`AGENTS.md`**, **`README.md`** and **`Bibliotheca/BIBLIOGRAPHY.md`**: every link
  to the package and its install line name `KaxaNuk/Researcher`.

## 0.19.4 (2026-10-21)

**PATCH** — the rules say what never leaves a strategy, and the `security` skill checks it before a
push. Nothing about any result changes.

**What to do differently:** say `security` in the strategy before you push it.

### Changed

- **`AGENTS.md`**, *Other standing rules*: a leaked key points at `security`'s *A key leaked*, and
  a new rule keeps keys, licences, holdings, licensed data and confidential material out of every
  copy, with the check run before a push.

## 0.19.3 (2026-10-18)

**PATCH** — a strategy's first save asks only a name, as every save of the researcher's does.
Nothing about any result changes.

**What to do differently:** nothing.

### Changed

- **`SETUP.md`**, *Step 1*, the note for the agent: when the first commit wants a git identity, it
  asks *What's your name, or what would you like me to call you?* in one open message, and no
  e-mail; `user.email` is set to `"<>"`, an empty address.

## 0.19.2 (2026-10-11)

**PATCH** — the Analytics Factory's files are asked of `analytics@kaxanuk.mx`. Nothing about any
result changes.

**What to do differently:** nothing in a new strategy. In one made from an earlier template, ask
`analytics@kaxanuk.mx` for the Analytics Factory's files; licences and questions about the Lab's
libraries stay with `lab@kaxanuk.mx`.

### Changed

- **`SETUP.md`**, *Step 3*, **`Config/.env.template`** and **`Data/hand_supplied.py`**: the
  Analytics Factory's files come from `analytics@kaxanuk.mx`.

## 0.19.1 (2026-10-10)

**PATCH** — the guides read more simply, each idea said once, and `.gitignore` keeps a licence file
out of git. Nothing about any result changes.

**What to do differently:** nothing in a new strategy. In one made from an earlier template, add
`.kaxanuk_license` to `.gitignore` if you keep a licence file in the repository.

### Changed

- **`AGENTS.md`, `README.md`, `SETUP.md`, `OBJECTIVE.md`, `RESULTS.md`,
  `Bibliotheca/BIBLIOGRAPHY.md` and `Paper_Trading/BITACORA.md`**: each idea said once, where it
  belongs, and the others point to it; long sentences split. Every rule, command, check and
  heading is kept.
- **`README.md`**, and the README block in `SETUP.md`'s step 5: a link to *What it is, and what it
  is not* in the KaxaNuk Researcher's README.
- **`.gitignore`**: `.kaxanuk_license`, the licence file the Lab's libraries can read, is never
  committed.

## 0.19.0 (2026-10-10)

**MINOR** — a Lab library's code is never read, quoted or copied here: a library is known from its
skill, its documentation, its changelog and runs. Nothing about any result changes.

**What to do differently:** nothing in a new strategy. In one made from an earlier template, bring
the two new passages of `AGENTS.md` across by hand; the researcher already follows them.

### Changed

- **`AGENTS.md`**, *Other standing rules*: a Lab library's code is never read, quoted or copied —
  never its installed files, a clone, a wheel or a source page its documentation links to — and no
  part of it, no copy of the Analytics Factory's files and nothing of KaxaNuk's research goes into a
  file here, an issue or a message. Where a skill and a library disagree, a run settles it.
- **`AGENTS.md`**, *How work reaches `main`*: a trap found in a Lab library is told by what was
  called, the error's type and message and the versions, as an issue in the package or a word to
  `lab@kaxanuk.mx`, never by the library's traceback lines or its code.
- **`Experiments/attribution_analysis.py`**, its docstring: the factor directory holds nothing but
  factor files, each named by its file name, and the model's four series are matched exactly — said
  from the documentation and runs, no longer from how the library reads the directory. Two earlier
  entries of this changelog lose the same detail.

## 0.18.4 (2026-10-09)

**PATCH** — the note for the agent in `SETUP.md` hands step 1 to `init-strategy`, which now asks
what the idea is and suggests names when the strategy has none. Nothing about any result changes.

**What to do differently:** nothing. `init-strategy` asks for what it needs.

### Changed

- **`SETUP.md`**, the note *For the agent, before anything else*: step 1 is `init-strategy`, which
  takes the user's name for the strategy, put in the folder's form, or asks what the idea is and
  suggests a few, and puts the folder beside the one you are in unless they say another; pass on
  what the user has said.

## 0.18.3 (2026-10-09)

**PATCH** — the worked example now lives at `examples/strategy/golden-flow/` in the package, and
the README's two links to it point there. Nothing about any result changes.

**What to do differently:** nothing. `init-example` copies the example as before.

### Changed

- **`README.md`**, the opening and *What is in here*: the two links to the worked example point to
  `examples/strategy/golden-flow` in the KaxaNuk Researcher, which keeps its examples by kind, as
  it keeps its templates. The strategy is still `golden-flow`.

## 0.18.2 (2026-10-08)

**PATCH** — the README and the setup say plainly how the Lab's libraries are had: the Data Curator
is open source and free, and the others come together, with their licences, in the KaxaNuk
Investment Lab, which KaxaNuk sells. Nothing about any result changes.

**What to do differently:** nothing in a strategy already set up; to ask for the Lab, write to
`lab@kaxanuk.mx` with *via KaxaNuk Researcher* in the subject, as `SETUP.md` says.

### Changed

- **`README.md`**, *The six Lab modules*: the Data Curator is *open source and free*, and Portfolio
  Construction *licensed since its 2.0.0*, no longer *on request*. The access line says the three,
  and the Data Refinery and the Data Analyzer when they ship, come together in the KaxaNuk
  Investment Lab.
- **`SETUP.md`**, *Step 3*: the access line says the same in its own words. Both end as one: write
  to `lab@kaxanuk.mx`, saying which library and what it is for, with *via KaxaNuk Researcher* in
  the subject.
- **`LICENSE`**: KaxaNuk SC holds the copyright, since 2026; the terms are MIT's, unchanged.

## 0.18.1 (2026-10-08)

**PATCH** — the line that schedules the daily run on Windows works in every shell and from a folder
whose path has a space, and git is installed with one command, not with GitHub Desktop. Nothing
about any result changes.

**What to do differently:** nothing in a strategy already set up; to schedule a book on Windows,
take the line from this version's `Paper_Trading/BITACORA.md`.

### Changed

- **`Paper_Trading/BITACORA.md`**, *Running it daily*: the Windows line is for Command Prompt, its
  days quoted, `"MON,TUE,WED,THU,FRI"`, which PowerShell split at the commas; it starts
  `schtasks --%` in PowerShell, and `MSYS_NO_PATHCONV=1 schtasks` in Git Bash, which turned
  `/Create` into a path. The folder's path is quoted there and in the cron line.
- **`SETUP.md`**, *What you need first*: git from `winget install --id Git.Git -e
  --accept-source-agreements --accept-package-agreements`, which does not stop to ask; GitHub
  Desktop leaves as a way to get it, since the git it brings is not on the command line.
- **`Universe/universe.ipynb`**, section 1: a line of 160 characters wrapped at 100.
- **`README.md`**, *The tools*: versions are the git command line; GitHub Desktop can sit on top,
  not in its place. Its access line names Portfolio Construction's licence beside the two engines'.

## 0.18.0 (2026-10-08)

**MINOR** — a new strategy says what to expect: nothing runs yet, and the assistant writes each file
with you. Its setup is shorter, its words plainer, and pandas is capped below 3. Nothing about any
result changes.

**What to do differently:** nothing to do in a strategy already set up; read the new `SETUP.md`
and `Paper_Trading/BITACORA.md` when a book goes on paper.

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

- **`README.md`**: the note for strategies made before 0.10.0 leaves; *a few minutes*.

## 0.17.0 (2026-10-08)

**MINOR** — three checks a live strategy needed: keys that join, traded value continuous at a split,
and the rule read back before its blueprint. They add to what Verify raises on; no published result
changes by itself, but a strategy whose universe dropped index members by key, or ranked on traded
value broken at a split, should re-run before quoting a figure.

**What to do differently:** make your universe notebook's Verify raise on an index listing with no
seed row and on a key used twice; read the register's blocking rows as exclusions in the experiment
and raise if one is held; check traded value at every split; and before a blueprint is saved, have
its rule read back to you on one worked date.

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

- **`README.md`**, part E: the read-back entry before the blueprint.

## 0.16.0 (2026-10-08)

**MINOR** — the researcher says, at most once a week, when a newer build of a Lab library this
strategy runs on is out, and a new build is taken between experiments as a change-set of its own.
Nothing about any result changes.

**What to do differently:** take a new library build between experiments, as `AGENTS.md` says.

### Changed

- **`AGENTS.md`**, *Other standing rules*: a new Lab library build is a change-set, between
  experiments, never during one — the researcher says when one is out, keeping the date of that
  weekly check in this repository's git config (`kaxanuk.labnext`), never saved; `uv lock
  --upgrade-package <name>`, then `uv sync --group notebook --inexact`, a re-run from a wiped copy
  and a `CHANGELOG.md` entry naming any number that moved; a book on paper runs on the Data Curator
  it was frozen with.
- **`SETUP.md`**, step 2: *A newer Lab library*, the same in three lines.

## 0.15.1 (2026-10-08)

**PATCH** — Portfolio Construction needs a licence since its 2.0.0, and the template says where its
key goes; the README says steps 1 to 7 are this repository, and steps 3 to 6 run on the Lab's
libraries. Nothing about any result changes.

**What to do differently:** with Portfolio Construction 2.0.0, put `KNPC_API_KEY_KAXANUK` in the
environment or a `.kaxanuk_license` file.

### Changed

- **`Config/.env.template`**: `KNPC_API_KEY_KAXANUK`, Portfolio Construction's licence since its
  2.0.0 — the library reads it from the environment or a `.kaxanuk_license` file, and a driver that
  loads this file into the environment first passes it on.
- **`SETUP.md`** step 3 names it beside the other two licences, and says the library reads it from
  the environment or `.kaxanuk_license`; *Paper trading, daily* says a saved licence check covers 3
  days offline from Backtest Engine 0.67.0 (7 before), the first run on it needing the network.
- **`Paper_Trading/BITACORA.md`**: paper trading is the last step inside this repository, not
  inside the Investment Lab, whose libraries run steps 3 to 6.

- **`README.md`**: steps 1 to 7 are this repository, and steps 3 to 6 run on the Investment Lab's
  libraries; Portfolio Construction is licensed since its 2.0.0.

## 0.15.0 (2026-10-08)

**MINOR** — the researcher saves the documents it writes on your go, each as its own version, and
the blueprint alone before the rule: nobody has to commit by hand for the order the process rests
on to hold. Nothing about any result changes.

**What to do differently:** nothing; the researcher saves what it writes. Code and data
change-sets keep their `CHANGELOG.md` entry, as before.

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

## 0.14.1 (2026-10-08)

**PATCH** — the commands that install and update the KaxaNuk skills run APM 0.33.0, and the update
is named in full: a bare `apm update -g` is not on the path after a `uvx` install. Nothing about
any result changes.

**What to do differently:** nothing in a strategy; the skills are updated from your researcher's
home.

### Changed

- **`README.md`, `SETUP.md`, `AGENTS.md`**: `uvx --from apm-cli==0.33.0 apm install -g` and
  `uvx --from apm-cli==0.33.0 apm update -g`.

## 0.14.0 (2026-10-07)

**MINOR** — the contract learns what the first strategy to reach paper trading found, and the
worked example becomes `golden-flow`. Attribution holds every weight overnight and reconciles its
benchmark before any figure is read; a seed taken from an index carries two keys and one map; the
refined rows stay inside each security's span; a book on paper is priced over three windows and a
crash in its daily run exits 2; and a scheme may size by a score inside bounds its blueprint names.
The template computes no figure, so none moves here; a strategy's attribution computed the old way
does.

**What to do differently:** in `Experiments/attribution_analysis.py`, move both weight tables one
day on before any pass, compare against the members the strategy can price, and make section 8
raise unless the first cut's benchmark comes within a point a year of the index's own returns file
— run an attribution computed without them again before quoting it. In a strategy with a book on
paper, catch a step that raises in `daily_update.py` and return 2, and register the scheduled task
again with the redirect `SETUP.md` gives. Install with `uv sync --group notebook --inexact`. Point
the two links to the worked example at `examples/golden-flow`, or at tag `v0.33.0` for
`liquid-golden-cross`.

### Changed

- **`Experiments/attribution_analysis.py`**: both weight tables are held overnight, so the close of
  t−1 earns day t, and the first cut's benchmark is reconciled with the index's own returns before
  any figure is read; the index's tickers are mapped to the book's identifiers through the seed's
  two keys; the index is compared on the members the strategy can price, the rest renormalised and
  the dropped share reported per year; the factor files are named by their file names, the model's
  own series matched exactly, nothing renamed on disk; the library's numbers are kept as tables, and
  the notebook says whether its figures are kept.
- **`Experiments/portfolio_construction.py`**: a scheme may size by a score, cut once before each
  date, inside bounds the blueprint names — the design, held by the control too — and the blueprint
  says where a capped name's excess goes; a constraint it does not name is off, a lever to earn.
  **`BLUEPRINT_1.md`**'s *Sizing* line says the same.
- **`Experiments/securities_panel.py`**: every matrix comes back on one calendar and one set of
  positions.
- **`Data/hand_supplied.py`**: *Two keys, one map* — a seed taken from an index carries the index's
  ticker beside the provider's identifier, and this module is the one place that maps them, the map
  coming from the strategy's seed builder or from the Analytics Factory; a frozen book carries its
  own copy.
- **`Data/curator.py`**: the library is called once per identifier, and the provider's answer is
  kept per name, so a name it does not carry is told from one it refused today; `main_identifier`
  is the identifier the experiment's provider prices under; leaving the dead names out and
  publishing the survivorship cost is a choice beside a second provider.
- **`Data/refinery.py`** and **`Data/analyzer.ipynb`**: each security's rows stay inside the span
  the seed gives it, in place of "the same rows".
- **`Universe/universe.ipynb`**: a live listing's span stays open — the seed's last date is when the
  source was written, not a delisting; `main_identifier` is the provider's identifier and an index's
  ticker its second key; the register states no fixed count of checks, and the old example's own
  sentence is gone; the usable date counts the share of the universe the strategy declares.
- **`Paper_Trading/daily_update.py`**, **`record.py`**, **`Paper_Trading_1/paper_trading_1.py`** and
  **`BITACORA.md`**: a book is priced over the whole history, the days after the experiment's window
  and since the freeze; a step that raises exits 2, with its traceback in the day's log; the index's
  and factor files are linked into a book's folder; a book holds the last membership an index's
  files wrote; the daily checks say what they miss.
- **`SETUP.md`**: `uv sync --group notebook --inexact`, so `nbconvert` is installed; the scheduled
  command keeps its output in `Paper_Trading/Logs/scheduled.log`; the Analytics Factory's files
  are what a strategy may read as its universe, its benchmark and attribution's inputs.
- **`.gitignore`**: `Universe/*.csv` but the seed, `Data/Curator/*.json`, and the index's and factor
  files linked into a book's folder.
- **Lines that read false in a filled copy** are worded for a new strategy: the notebooks' *empty by
  design*, the blueprint's and the objective's *delete this blockquote*, the findings' *Not yet
  run*, the results' *empty by design* and limitation 1, and the gate's *Nothing has graduated*.
- **`AGENTS.md`**: what attribution must report is said without the passage on savvy investors and
  allocators.
- **`README.md`**, **`AGENTS.md`** and **`SETUP.md`**: the worked example is `golden-flow`, and the
  files only it has are its own whole.

## 0.13.4 (2026-10-06)

**PATCH** — the way to a licence, to access and to the index and factor files is written where a
strategy meets them. The Backtest Engine and Attribution Analysis licences, and access to Portfolio
Construction, are KaxaNuk's to give, and nothing here said whom to ask; "the desk" that ships the
index and the factor model had no name. Nothing about any result changes.

**What to do differently:** for a licence, access to Portfolio Construction or the Analytics
Factory's files, write to `lab@kaxanuk.mx`, saying which library and what it is for. Run APM as
`uvx --from apm-cli==0.29.0 apm`, as every command here now shows.

### Added

- **`.gitignore`**: `.DS_Store`, `Thumbs.db` and `desktop.ini`, which Finder or Explorer leaves in
  a folder it shows. `init-strategy` already left them out of the first commit; this keeps them out
  after it.

### Changed

- **`SETUP.md`**: step 3 says how a licence or access is asked for, and names KaxaNuk's Analytics
  Factory, with its page, as what ships the files `KN_ANALYTICS_PATH` points at; the folders it
  reads are unchanged. Step 4's install command names `apm-cli==0.29.0` itself, so the agent's note
  on putting `uvx` in front is gone.
- **`README.md`**: *The six Lab modules* has a Status column — the Data Curator open source, the
  Data Refinery and the Data Analyzer coming and hand-rolled in `Data/` until then, Portfolio
  Construction on request, the Backtest Engine and Attribution Analysis licensed — and *Two doors*
  gives the platform's page, <https://www.kaxanuk.mx/lab>, without the list of what it does. The
  licensed paragraph says how a licence or access is asked for; the install command names
  `apm-cli==0.29.0`; the folder table names the Analytics Factory where it said the desk.
- **`Config/.env.template`**, **`Data/hand_supplied.py`**, **`Data/curator.py`** and
  **`Experiments/attribution_analysis.py`**: the Analytics Factory where they said the desk, in a
  comment and the docstrings; no code changes.

## 0.13.3 (2026-10-06)

**PATCH** — a name whose prices are about to stop is sold the day before. A strategy built on the
template found the Backtest Engine refusing its book outright: a provider's file had a 62-day gap
at a corporate event, the book held the name through it, and the engine checks every open
position on every rebalance date. Nothing about any result changes: the rule is written into the
contract, and a strategy takes it when its own rule does.

**What to do differently:** in a strategy's eligibility, require a price on t and on t+1, so the
book re-strikes on the last priced day; apply it to every counterfactual alike, and name the day
of hindsight it takes beside the delisting exit in `AGENTS.md`.

### Changed

- **`AGENTS.md`**: the look-ahead row of the five ways a backtest lies says a name whose prices
  are about to stop is sold at t−1 by a re-strike the rule triggers, and names that exit's day of
  hindsight as the one stated leak.
- **`Experiments/portfolio_construction.py`**: a third timing rule in its contract, *sell before a
  price series stops*.

## 0.13.2 (2026-09-29)

**PATCH** — `Experiments/Experiment_1/BRAINSTORMING_1.md` is gone. Its entries had the journal's
own four fields, and the thinking before a blueprint is a dated journal entry like any other, each
entry's open threads keeping planning apart from history. The benchmark's choice, the one entry that
had to come before the blueprint, is now an entry of `JOURNAL_1.md`, and `BLUEPRINT_1.md`, the
notebook, `AGENTS.md` and the README read it there. Nothing about any result changes.

**What to do differently:** choose the benchmark in a dated entry of `JOURNAL_1.md`, before the
blueprint. A strategy made from an earlier template can keep its `BRAINSTORMING_1.md`: the
Researcher's commands still read the benchmark there.

### Removed

- **`Experiments/Experiment_1/BRAINSTORMING_1.md`.**

### Changed

- **`Experiments/Experiment_1/JOURNAL_1.md`** says the entry before the blueprint chooses the
  benchmark; **`BLUEPRINT_1.md`**, **`experiment_1.ipynb`**, **`AGENTS.md`** and **`README.md`**
  name the benchmark `JOURNAL_1.md` chose, and three documents in every experiment.

## 0.13.1 (2026-09-25)

**PATCH** — a frozen book's security master stays out of git. `.gitignore` keeps
`Paper_Trading/*/Universe/Security_Master.csv` out, as it keeps the one in `Universe/`: it is the
provider's data. The docstrings of `promote.py` and `daily_update.py`, `SETUP.md` and
`Paper_Trading/BITACORA.md` say that the master is copied from disk, stays on the machine that froze
the book and is brought across by hand, and that the daily run checks every frozen file against its
hash in `FREEZE.json`. Nothing about any result changes.

**What to do differently:** in a strategy made from 0.13.0, add the `.gitignore` line; if a book's
frozen master is already committed, `git rm --cached` it — the file stays on disk — and back it up
with the record.

### Changed

- **`.gitignore`, `SETUP.md`, `Paper_Trading/BITACORA.md`, and the docstrings of
  `Paper_Trading/promote.py` and `Paper_Trading/daily_update.py`**, as above.

## 0.13.0 (2026-09-24)

**MINOR** — the template describes a second price provider and the desk's new folders, and
Experiment 1's findings ask the question Experiment 1 now answers. Nothing about any result changes.

**What to do differently:** in a strategy made from 0.12.0, bring across by hand the docstrings of
`Data/curator.py`, `Data/hand_supplied.py` and `Paper_Trading/daily_update.py`, `SETUP.md`'s
paragraph on `KN_ANALYTICS_PATH` and its comment in `Config/.env.template`, and the status guidance
of `FINDINGS_1.md`. If your desk reader reads only `Benchmarks/` and `Factors/`, teach it the
Analytics Factory's `Benchmark Portfolios/` and `Factor Models/` as well.

### Added

- **A second price provider, in `Data/curator.py`'s contract.** A provider's history can stop where
  its coverage does, so a name that left the market is fetched from a second provider that carries
  it, into the same files and columns, and the strategy's documents say which names came from where
  and how any column the second provider lacks was filled.

### Changed

- **The desk's folders.** `Data/hand_supplied.py`, `SETUP.md` and `Config/.env.template` name the
  Analytics Factory's `Benchmark Portfolios/` and `Factor Models/`, read first, and the older
  `Benchmarks/` and `Factors/`, still read where those are absent. The files keep their names and
  headers, and the drop-in folders under `Data/Curator/` keep the older names.
- **`FINDINGS_1.md`'s status** asks whether the rule beat the benchmark and its control by what the
  blueprint required, and whether it is a candidate for the gate, where it asked whether the
  benchmark was adopted: Experiment 1 is the first rule tested against the benchmark, not the
  benchmark itself.
- **`Paper_Trading/daily_update.py`'s contract** says a lock a killed run left for twelve hours is
  removed, and the log says so.

## 0.12.0 (2026-09-23)

**MINOR** — step 7 gets its machinery: a graduated book is the strategy frozen, and one daily run
refreshes, checks, rules and prices every frozen book into a record kept in files, a database or
both. The benchmark is named in `BRAINSTORMING_1.md` and Experiment 1 can graduate. The desk's files
are read in place. Nothing about any result changes.

**What to do differently:** in a strategy made from 0.11.0, bring across by hand the new files —
`Data/hand_supplied.py`, `Paper_Trading/promote.py` and `record.py` — and the changed ones:
`Data/curator.py`'s docstring, `Paper_Trading/daily_update.py` and `paper_trading_1.py`,
`BITACORA.md`'s *What a paper-trading run is* and *Before a book's first day*, `SETUP.md`'s keys and
*Paper trading, daily*, `Config/.env.template`, `.gitignore`, `pyproject.toml`, and the benchmark's
wording in `AGENTS.md`, this README, `BLUEPRINT_1.md`, `JOURNAL_1.md` and the experiment notebook.

### Added

- **`Paper_Trading/promote.py` and `record.py`**, beside `daily_update.py`, each a contract in its
  docstring: freeze a graduated experiment into `Paper_Trading_N/` with `FREEZE.json`; run every
  frozen book each day; keep six keyed tables in CSV files, a DuckDB database or both, a
  restatement flagged and never overwritten.
- **`Data/hand_supplied.py`**, the reader of the desk's index and factor files, in place from
  `KN_ANALYTICS_PATH` or from the drop zones, in the desk's own names and headers.
- **`KN_ANALYTICS_PATH` and four `PAPER_TRADING_*` settings** in `Config/.env.template`; `duckdb`
  and `pyarrow` in `pyproject.toml`; `.gitignore` lines for each day's paper-trading output.
- **`BITACORA.md` *Before a book's first day*** and **`SETUP.md` *Paper trading, daily***.

### Changed

- **The benchmark is what `BRAINSTORMING_1.md` names**, and Experiment 1 is the first rule tested
  against it, able to graduate like any other; its rules freeze once `FINDINGS_1.md` reports, and a
  rewrite the owner decides is written down as one. `AGENTS.md`, this README's order of work,
  `BLUEPRINT_1.md` — its thesis, success criteria and falsifying condition — `JOURNAL_1.md`, the
  experiment notebook and `BITACORA.md` say so.
- **`Data/curator.py`** says a paper-trading refresh takes `--end-date` and refetches each file
  whole; `daily_update.py` and `paper_trading_1.py` state the freeze and the daily run.

## 0.11.0 (2026-09-23)

**MINOR** — the bar asks for a control on the rule's own rebalance dates, one falsification
condition fixed before the rule, and the horizon and overlap beside every ratio; each experiment
names the claim it moves; and every notebook ends in a Verify section that raises. Nothing about
any result changes.

**What to do differently:** in `BLUEPRINT_N.md`, name the claim the experiment moves, its control
in *Rules*, and the one condition that would falsify it with the changes that may not rescue it. In
`FINDINGS_N.md` and `RESULTS.md`, say which claim moved. Beside any coefficient, t statistic or
ratio, state the horizon and the overlap and report the share of dates with the expected sign. End
each notebook in a Verify section that reads back what it wrote and raises. A trap found in a Lab
library goes to that library's skill in the KaxaNuk Researcher, as an issue there.

### Added

- **Three items at the end of the bar in `AGENTS.md`**, so the first eight keep their numbers: 9, a
  control that differs in exactly one thing, named in the blueprint's *Rules* and trading on the
  rule's own rebalance dates; 10, one falsification condition for the whole experiment, and the
  changes that may not rescue it, each a new experiment and a trial; 11, the horizon and the overlap
  stated, and the share of dates with the expected sign beside any t statistic or ratio.
- **A Verify section at the end of `Universe/universe.ipynb`, `Data/analyzer.ipynb` and
  `experiment_1.ipynb`**, saying what each reads back and raises on, and a row for it in the
  experiment's section contract. `AGENTS.md` says every notebook ends in one, that it is where a
  strategy's tests live, and that the days the engine valued are counted against the window's
  trading days, never a fixed floor, which a run that stopped years early can clear.
- **Three sections of `BLUEPRINT_1.md`**: *The claim this moves*, a *Control* line in *Rules*, and
  *What would falsify it*.
- **A table under *Before any experiment* in `RESULTS.md`**, with a column for the share of dates
  with the expected sign and the overlap stated above it; and a *Claim moved* column in the
  experiments table.

### Changed

- **`FINDINGS_1.md`'s status** ends with the claim the experiment moved and the status it reached,
  and *The book, priced by the engine* sets the book against the control its blueprint names.
- **Criterion 1 of `Paper_Trading/BITACORA.md`** says which control: the one the blueprint names,
  trading on the rule's own rebalance dates.
- **`AGENTS.md`** sends a trap found in a Lab library to that library's skill in the package, as an
  issue there; commits a result once every notebook has reached the end of its Verify section; and
  row 5 of the five ways a backtest lies says the experiment's Verify section catches a truncated
  run.
- **Limitation 2 of `RESULTS.md`** says what a control differing in exactly one thing is, and is
  written as a condition that holds in any strategy: an experiment that claims a margin without one
  has inferred which lever earned it, not measured it.
- **Section 4 of `Data/analyzer.ipynb`** asks for the share of dates with the expected sign beside
  the IR, and says why: consecutive windows overlap.
- **The README's parts E, G and H** name the claim, the control and the falsification condition in
  the blueprint, the Verify section in the cycle, and the claim moved in the results.
- **`SETUP.md`'s note for the agent and the README's install line** pin
  `uvx --from apm-cli==0.29.0`, the APM the KaxaNuk Researcher's own `SETUP.md` installs.

## 0.10.5 (2026-09-23)

**PATCH** — the README no longer says the template's files are generated from the example: the
KaxaNuk Researcher keeps the two in step by hand. Nothing about any result changes.

**What to do differently:** nothing.

### Changed

- **The README's *What is in here*** says the shared files are the example's with its own lines
  removed, and no longer that a tool generates them.

## 0.10.4 (2026-09-23)

**PATCH** — `AGENTS.md` and the README stop explaining how the researcher package keeps the template
and the example in step, the README's researcher paragraph maps each command to the part it serves,
a strategy made before 0.10.0 is sent to `init-strategy`'s script rather than to the example,
`apm.yml` is gone, and this template's markdown is wrapped at 100 columns. Nothing about any result
changes.

**What to do differently:** in a strategy made from a template before 0.10.0, bring a missing file
back from the template with `init-strategy`'s script, `scaffold.py strategy . --only <path>`, never
from the example. In a strategy made from an earlier template, delete `apm.yml`: its version lives
in `pyproject.toml` alone.

### Changed

- **`AGENTS.md`'s two paragraphs on where the template and the example live are one**: both live in
  the KaxaNuk Researcher package, the example is for reading and nothing in a strategy is brought
  across from it, issues and pull requests about the process land there, and what the template ships
  is *What is in here* in its README. How the template's files are generated from the example is the
  package's business, not a strategy's.
- **The README's *A researcher beside the process* is one paragraph**: what a researcher is, and
  which command serves which part — `objective` (A, B), `read` (B, F), `blueprint` (E), `brainstorm`
  (E, F), `challenge` (G) and `next`. How `read` works is in `Bibliotheca/BIBLIOGRAPHY.md`, and how
  to invite a researcher is in `SETUP.md` step 4.
- **The README's sentence for a strategy made before 0.10.0** sends a missing file to
  `init-strategy`'s script, which copies it from the template and never overwrites, rather than to
  `init-example` and a hand-deletion of the example's lines.
- **The README says the skills teach the Lab modules**, not the six of them: no skill covers the
  Data Refinery.
- **`Bibliotheca/BIBLIOGRAPHY.md`** says `Papers/`, `Books/` and `Notes/` are directories created on
  the day there is something to put in them; the template ships none of the three, and it named only
  two.
- **Eight lines of the README, `SETUP.md` and `Bibliotheca/BIBLIOGRAPHY.md` are rewrapped at 100
  columns**, and the researcher package's check now reads this template's markdown for width.

### Removed

- **`apm.yml`.** A strategy installs nothing — the skills come with the researcher, installed once
  for the user — and nothing read it. `SETUP.md` step 5 renames and versions `pyproject.toml` alone,
  the first `CHANGELOG.md` entry names the template version `pyproject.toml` declared, and the agent
  asks for the user's name as the holder in `LICENSE`. `.gitignore`'s header, the README's
  *What is in here* and `SETUP.md`'s *What "done" looks like* no longer name it.
- **The README's *Where the template and the example live***, the fourth description of the example
  after the intro, *What is in here* and `SETUP.md` step 1. Its closing pointer to `AGENTS.md` stays
  as the README's last line.

## 0.10.3 (2026-09-23)

**PATCH** — work lands on `main` without an issue, a branch or a pull request per change, the
documents say who appends `Bibliotheca/LOG.md` and what moves in `OBJECTIVE.md`, the README names
the researcher's other commands, `SETUP.md` covers the licence holder and the
researcher's identity, and `.gitattributes` normalises line endings. Nothing about any result
changes.

**What to do differently:** commit on `main`; open a branch only for a change you want reviewed.
In a strategy made from an earlier template, add `.gitattributes` with `* text=auto eol=lf`, and
put yourself as the holder in `LICENSE` if you have not.

### Added

- **`.gitattributes`**, `* text=auto eol=lf`, as the researcher package and a home already carry,
  so a clone on Windows, macOS or Linux sees exactly what was committed.
- **A row for `Bibliotheca/LOG.md` in `AGENTS.md`'s who-writes table**: whoever reads a source or
  audits the folder appends it, the researcher's `read` and `audit` do so themselves, and a past
  entry is never edited. The log's own header says the same.

### Changed

- **Work lands on `main`.** *How work reaches `main`* no longer asks for an issue and an
  `issues/<number>` branch before every change, nor a pull request after it: work is committed on
  `main` with its changelog entry, and a branch and a pull request are for a change you want
  reviewed, deleted once merged. The blueprint rule keeps its point without a branch: under *The
  blueprint is committed before the rule*, `BLUEPRINT_N.md` is committed in a commit of its own
  before the rule cell holds code. *Before any pull request* is *Before any commit to `main`*, a
  result is committed once the pipeline has re-run from a wiped working copy, and a moved number
  is named in the commit message. The paragraph on what `init-strategy` copies says
  `BIBLIOGRAPHY.md` ships with only its seeded leads.
- **`OBJECTIVE.md`'s "Changes when" cell** separates the idea and the claims' wording, which almost
  never change, from each claim's evidence and status, which move as notes arrive (B) and as
  findings report (H).
- **The README** says `Bibliotheca/Papers/`, `Books/` and `Notes/` appear with their first note,
  names what `brainstorm` (E, F), `challenge` (G) and `next` do beside `objective`, `read` and
  `blueprint`, and points to *In a strategy or another project* in the researcher's own README for
  its identity to load with it. `SETUP.md` step 4 gives the same pointer.
- **`SETUP.md` step 5** says `LICENSE` names KaxaNuk as the holder — put yourself there, or choose
  another licence — commits it with the rest, and says it is the first `---` line of
  `CHANGELOG.md` that everything is kept above.
- **`Experiments/Experiment_1/BLUEPRINT_1.md`** says each prediction cites a `Bibliotheca/` note or
  a section of `Data/analyzer.ipynb`, as *Starting your own strategy* already did.
- **`Bibliotheca/BIBLIOGRAPHY.md` and `LOG.md` are generated from the example**, with the rest of
  the files inside the folders, so the two cannot drift. Part 5's row on Sullivan, Timmermann &
  White says its note, once read for a claim, is linked from its Part 1 row.

### Removed

- **The rule on marking the example's content**, which a strategy has no example to apply to, no
  longer reaches a new strategy; it stays in the example's `AGENTS.md`.

## 0.10.2 (2026-09-22)

**PATCH** — *Starting your own strategy* in the README letters its eight parts A to H, so a part of
the order of work is never mistaken for one of the eight steps; each part is named, the analyzer's
measurements are said to go straight into `RESULTS.md` under D, and the list ends with what comes
after H: the gate, or Experiment 2 from E again. It also says that `next`, a command of the KaxaNuk
Researcher, reads the folder and names the part that comes next. Nothing inside the folders
changes.

## 0.10.1 (2026-09-22)

**PATCH** — three generated files no longer carry the worked example's own state. No
result changes.

**What to do differently:** nothing.

### Fixed

- **`Experiments/Experiment_1/experiment_1.ipynb`**: section 6 no longer says "each
  counterfactual below", pointing at cells this template does not have, and the first open item
  states its condition — no result without the licensed engines — rather than the example's
  "the book is real".
- **`Experiments/Experiment_1/BLUEPRINT_1.md`**: the open questions get a placeholder table to
  fill in, as the predictions already had.
- **`Paper_Trading/BITACORA.md`**: one line is re-wrapped at 100 columns.

## 0.10.0 (2026-09-22)

**MINOR** — the template ships every file its README's *What is in here* table names, each as a
description of what belongs in it. No result changes.

**What to do differently:** a new strategy brings nothing across from the example. Fill in the
files that are already here — a `.py` file is its docstring, a notebook its markdown cells, a
document its prose. A strategy made from an earlier template can take a file it lacks with
`init-example <path>`, and delete what is between the example markers.

### Added

- **Eighteen files inside the folders**: `Universe/universe.ipynb`; `Data/curator.py`,
  `refinery.py`, `analyzer.ipynb` and the two `custom_calculations.py`; the four shared modules in
  `Experiments/`; `Experiment_1/`'s four documents and notebook; `Paper_Trading/BITACORA.md`,
  `daily_update.py` and `Paper_Trading_1/paper_trading_1.py`. Each is generated from the worked
  example with the worked strategy's own lines removed, by
  `tools/sync_investment_lab_references.py` in the KaxaNuk Researcher, and `tools/check_repo.py`
  there fails when one differs.

### Changed

- **`README.md`, `AGENTS.md` and `SETUP.md` no longer send a new strategy to
  `init-example <path>`** for a file: it is already here. `init-example` copies the example whole,
  to read or run. `AGENTS.md` says the example markers are what the sync tool strips.

### Removed

- **The `.gitkeep` files in `Universe/`, `Data/`, `Experiments/` and `Paper_Trading/`**, which held
  the folders open while they had no file.

## 0.9.0 (2026-09-22)

**MINOR** — a new strategy takes its own name and version at setup, `SETUP.md` no longer describes
an install a strategy never runs, and the Data Curator floor is 0.50.0. No result changes.

**What to do differently:** in a strategy you made from this template, give `pyproject.toml` its
own name and version as step 5 of `SETUP.md` now says, and once a licensed engine is installed by
hand, use `uv sync --inexact` and `uv run`, never a bare `uv sync`.

### Added

- **Step 2 of `SETUP.md` warns that `uv sync` is exact.** It removes every package `uv.lock` does
  not name, so a bare `uv sync` uninstalls the Backtest Engine, Attribution Analysis or Portfolio
  Construction once any of them is installed by hand; `uv sync --inexact` and `uv run` keep them.

### Changed

- **Step 5 of `SETUP.md` gives a new strategy its own identity**: `pyproject.toml`'s name, both
  versions set to `0.1.0`, the template's changelog entries replaced by the strategy's first, and
  `uv lock` run before the commit.
- **`SETUP.md`'s Windows short-path advice gives the real reason**: deep paths inside the folder,
  such as `.venv/`, can pass Windows' path limit and fail with misleading errors. The old reason
  was an APM install a strategy no longer runs.
- **The code-style summary in `AGENTS.md` matches the Bloom Code instruction**: one item per line
  from three items, or from two on a line over the length limit, and the error message goes in
  `message`, not `msg`. It names `bloom-code-lint`, with `--max-line-length 100`, as the check.
- **`apm.yml`'s comment names one package** for every KaxaNuk skill, installed once for the user
  with `apm install -g KaxaNuk/KaxaNuk-Researcher --target <agent>`.
- **`SETUP.md` step 4 gives the install command with `--target claude`**, your assistant in place
  of `claude`, as `apm.yml` and the researcher package's `SETUP.md` do; it gave it bare, and so
  did the README.
- **`pyproject.toml` asks for `kaxanuk-data-curator>=0.50.0`**, the first version whose `main()`
  takes `data_block_providers`, which the `data-curator-custom-calculations` skill now uses.

### Fixed

- **`AGENTS.md` and the README no longer say to delete the seed after `init-example`.** The
  template ships it header-only, so `init-example Universe` and `init-example Bibliotheca` are
  refused; bring `Universe/universe.ipynb` by its path. The `main` row of the branch table is now
  simply the strategy's finished work.
- **Template only: the `AGENTS.md` status banner says what the template ships**:
  `Config/.env.template`, the header-only seed, and the `Bibliotheca/` index and log. It said every
  folder but `Config/` held only a `.gitkeep`.
- **Template only: the README no longer says the example has no `Bibliotheca/Books/`.** The
  example ships Paleologo (2021)'s `INDEX.md` and its chapter note; only `Bibliotheca/Notes/`
  appears with its first note.

### Removed

- **`SETUP.md`'s wrapper-folder check and its paragraph**, since a strategy installs nothing. It
  lists only `.venv/`, `Config/.env` and per-machine assistant files as ignored, and `AGENTS.md` no
  longer points at the removed text.

## 0.8.1 (2026-09-21)

**PATCH** — the KaxaNuk skills are one package. No result changes.

**What to do differently:** nothing; `apm update -g` brings them.

### Changed

- **`README.md` names one package for the skills**, `KaxaNuk/KaxaNuk-Researcher`, which now carries
  every Investment Lab skill itself instead of bringing them from `KaxaNuk/KaxaNuk-Agent-Skills`.

## 0.8.0 (2026-09-21)

**MINOR** — the template and the worked example now ship inside the KaxaNuk Researcher,
`KaxaNuk/KaxaNuk-Researcher`, and a strategy is made with `init-strategy`. No result changes.

**What to do differently:** install the KaxaNuk skills once for your user —
`apm install -g KaxaNuk/KaxaNuk-Researcher` —
then start a strategy with `init-strategy <name>`, and bring a file of the example across with
`init-example <path>`, never with `git fetch`.

### Changed

- **The template and the example moved into the researcher package.**
  `KaxaNuk/KaxaNuk-Strategy-Template`, with its `main` and `example` branches, and
  `KaxaNuk/KaxaNuk-Researcher-Template` are retired. What `main` held is now
  `templates/strategy/` in `KaxaNuk/KaxaNuk-Researcher`, what `example` held is
  `examples/liquid-golden-cross/`, and the researcher's home is
  `templates/researcher/`. One repository now versions the process, the worked strategy
  and the skills that read them, so the three cannot drift apart between releases.
- **A strategy is made by `init-strategy`, not by *Use this template* or a clone.** The skill copies
  the template by a script, byte for byte, makes the folder a git repository and commits it once;
  publishing it to GitHub is the owner's, one repository per strategy. Step 1 of `SETUP.md` now says
  only that, and keeps the short-path warning for Windows and the git-identity fallback; the button,
  `gh repo create --template` and the plain clone with a fresh history are gone, with the two
  failure notes they needed.
- **A file of the example comes with `init-example <path>`**, which copies one path of the example
  into the strategy and never overwrites a file already there; the marked lines are deleted
  afterwards, as before. It replaces the README's `git fetch ... example` and `FETCH_HEAD` block.
  `init-example` with no path copies the whole example into a folder of its own. The README's branch
  table becomes a description of the two folders, and `AGENTS.md` says where they live instead of
  naming the two branches.
- **The skills are installed once for the user**, with `apm install -g`, and `apm update -g` keeps
  every strategy current; a strategy installs nothing, and step 4 of `SETUP.md` no longer keeps an
  in-repository install for a user with no researcher. A researcher is made once with
  `init-researcher`. Every link to the retired repositories — in the README, `SETUP.md`, `AGENTS.md`
  and `Bibliotheca/BIBLIOGRAPHY.md` — now points at the package on GitHub.

## 0.7.15 (2026-09-21)

**PATCH** — `main` carries an empty bibliography and log, and installs no agent skills. No result
changes.

**What to do differently:** in a new strategy, do not install skills — invite your researcher, and
they come with it. Step 1 needs nothing from `example`: `Bibliotheca/BIBLIOGRAPHY.md` and `LOG.md`
are already here.

### Added

- **`Bibliotheca/BIBLIOGRAPHY.md` and `Bibliotheca/LOG.md`, empty, on `main`.** A strategy made
  from `main` had to fetch both from `example` and then delete what was the worked strategy's — the
  rows between the example markers, each `[note](...)` link left outside them, every log entry
  below the rule. Every strategy did that by hand, the first time it read a paper. The two files are
  now `example`'s with exactly that removed: Parts 0 to 5 and their leads, *No note yet.* on every
  row, and the log's header and rule.

### Changed

- **The agent skills come with the researcher, and this repository installs none.** `apm.yml` no
  longer names the `kaxanuk` package, `apm-cli` leaves the `dev` dependency group, and step 4 of
  `SETUP.md` says where the skills come from instead of installing them. A researcher made from
  `KaxaNuk/KaxaNuk-Researcher-Template` installs every KaxaNuk package once, in its own home, and
  brings them into any strategy it is invited to — so a new version reaches every strategy with one
  `apm update` in that home, and a strategy never goes stale. `AGENTS.md` and the README say the
  same. For a user with no researcher, step 4 keeps the one command that installs them here.
- **The KaxaNuk Strategy Template, on `main` too.** 0.7.14 renamed the process on `example`
  only; `SETUP.md`'s first commit, the README it has a strategy write, and `apm.yml` still said *KN
  Research Process* here.

### Removed

- **`Bibliotheca/.gitkeep`**, now that the folder has files.

## 0.7.13 (2026-09-21)

**PATCH** — the researcher's repository is `KaxaNuk/KaxaNuk-Researcher-Template`. No result
changes.

**What to do differently:** nothing. GitHub redirects the old name.

### Changed

- **The researcher's repository was renamed `KaxaNuk/KaxaNuk-Researcher-Template`**, and the README
  and `AGENTS.md` link it by that name. Like this repository, it is a template: what reads the notes
  and drafts the claims is a researcher made from it, which is how both files now put it.

## 0.7.12 (2026-09-21)

**PATCH** — on `example`, the blueprint and the findings keep the template's headings outside the
example markers again. Nothing on `main` changes but the version. No result changes.

**What to do differently:** nothing.

### Fixed

- **Ten of the template's headings sat inside the worked strategy's example markers** on `example`:
  *Thesis*, *Rules* and *What this experiment should show* in `BLUEPRINT_1.md`, and seven sections of
  `FINDINGS_1.md`, whose *Status* had also lost its guidance. Regenerating the references in
  `experiment-lifecycle` stripped them as strategy content, 82 lines in all, so two references could
  not be regenerated. Each heading is back outside the markers with the template's guidance beneath
  it, and the strategy's own text follows in its own block, as *Key risks* always had it. The change
  only adds lines; not one line of the strategy's text changed, and stripping the fixed files
  reproduces the current references exactly.

## 0.7.11 (2026-09-21)

**PATCH** — the Python project is named `kn-strategy-template`, like the repository and its `apm.yml`.
No result changes.

**What to do differently:** nothing. The project is virtual — `uv` never installs it as a package —
so the rename moves no file in `.venv`.

### Fixed

- **`pyproject.toml` still named the project `kn-research-process`** after the repository became
  `KaxaNuk-Strategy-Template` and `apm.yml` became `kn-strategy-template`. It now matches both.
  Found by `tools/check_release.py` in KaxaNuk-Agent-Skills, which treats the old name as retired
  everywhere but the changelog and the journals.


## 0.7.10 (2026-09-20)

**PATCH** — the two version fields agree again, and the notebooks on `example` name a kernel that
exists. No result changes.

**What to do differently:** nothing. If you copied a notebook across from `example` and were asked
to pick a kernel, bring it across again.

### Fixed

- **`pyproject.toml` kept version 0.7.8 while `apm.yml` moved to 0.7.9.** The two have always moved
  together and 0.7.9 bumped only one of them. Both read 0.7.10 here.
- **The notebooks on `example` declared a kernel named `kn-research-process`.** Nothing in this
  template registers that name and `SETUP.md` never mentions it, so a new clone could not execute
  them — the name resolved to whatever that machine happened to have, or to nothing. They now name
  `python3`, which the `.venv` this repository builds registers, and record Python 3.13.15 rather
  than 3.14.5, a version `pyproject.toml` forbids under `>=3.12,<3.14`.

### Changed

- **`example`'s pipeline was re-run end to end on the supported interpreter** and every published
  number reproduced: the universe files byte-identical, the refinery's 787 files over the same
  4,252,848 rows, all nine analyzer measurements, all eleven weight files, and every engine figure.
  Nothing in its `RESULTS.md` moved.

## 0.7.9 (2026-09-20)

**PATCH** — the repository is now `KaxaNuk/KaxaNuk-Strategy-Template` and the skills come from
`KaxaNuk/KaxaNuk-Agent-Skills`. No result changes.

**What to do differently:** nothing, if you already cloned. GitHub redirects both old paths, so an
existing repository keeps installing and `git pull` keeps working; run
`git remote set-url origin https://github.com/KaxaNuk/KaxaNuk-Strategy-Template.git` when you want
the remote to say what it is. New pins should use the new paths.

### Changed

- **`apm.yml` fetches from `KaxaNuk/KaxaNuk-Agent-Skills/kaxanuk`.** "APM" read as Application
  Performance Monitoring and named the delivery mechanism rather than what the packages hold. The
  package names stay `kaxanuk-apm-*` — they are APM packages, and every published tag embeds that
  name. The project's own name here is `kn-strategy-template`.
- **The README, `AGENTS.md` and `SETUP.md` name both new repositories**, in prose, in the install
  instruction and in the `git fetch` that copies a file across from `example`. The old name said
  *process* where the artifact is a repository you copy, and collided with `KaxaNuk-Researcher`.
  The **KN Research Process** keeps its name: the process is not the repository.
- **The example strategy is `liquid-golden-cross`.** `example` was restarted under that name and
  three documents still said `liquid-momentum`, sending a reader to a strategy no longer there.

## 0.7.8 (2026-09-17)

**PATCH** — step 6 compares the book with the whole benchmark, not the part of it the book holds. No
result changes.

**What to do differently:** before handing the book to the attribution library, add every benchmark
constituent it does not hold at zero weight, each with a price series. The engine's daily weights
name only what was held.

### Changed

* **`Experiments/attribution_analysis.py`, on [`example`](../../tree/example), widens the book to the
  benchmark.** The library prices only the securities named in the book's weight file, and the first
  cut computes the benchmark's return from those prices alone; the index's own return series never
  enters it. A book of 8 names inside a 788-name index was compared with the 7% of the index it
  overlapped: the benchmark return came out at 6% of the index's, and alpha about five times too
  large, most of the excess filed under interaction. With the other 780 names added at zero weight the
  benchmark return reached 98.9% of the index's, the rest being the held names' own returns. The run is
  recorded in `JOURNAL_1.md` on that branch.
* **The same module drops the engine's benchmark column** from the daily weights, which the engine
  returns at zero, and keeps the cash position.
* **The README's four shared modules** say that `attribution_analysis.py` widens the book to every
  benchmark constituent.

## 0.7.7 (2026-09-17)

**PATCH** — step 6's module says what the attribution library's loader actually accepts, checked by
running it against a strategy's own files. No result changes.

**What to do differently:** give every weight file a first header of `Ticker` or `date_column` —
nothing else loads, whatever the library's documentation says — and check that the four reserved
factor names are in lower case before an attribution run.

### Changed

* **`Experiments/attribution_analysis.py`, on [`example`](../../tree/example), names the one cell that
  decides whether a file loads**: the first header. `Ticker` means securities down and dates across,
  `date_column` means dates down and securities across, and any other name — `date`, `m_date`,
  whatever a provider used — raises before a number is read. The module said the hand-supplied files
  were both horizontal, and that a wrong orientation produced a transposed number rather than an
  error. Both were wrong.
* **The same module says what the factor directory has to look like**: nothing but factor files,
  each factor named by its file name, the date column first, its header possibly empty, and the four
  names of the model's own series — `f_market`, `f_total_factor_returns`,
  `f_total_excess_returns`, `f_idyo_returns` — are matched exactly and in lower case, so a file
  capitalised differently is attributed as an ordinary factor.
* **`JOURNAL_1.md` on that branch records the run** that settled all of it: both engines installed, a
  synthetic book priced, and the attribution run over a strategy's real benchmark and factor files. It
  also records a backtest that reported success while valuing 522 of 1305 days, because a book summing
  to one with no cash reserve cannot pay commission at a rebalance.

## 0.7.6 (2026-09-17)

**PATCH** — the tools are three jobs with a choice for each, not a fixed list. No result changes.

**What to do differently:** nothing, if you use GitHub Desktop, PyCharm and Claude. Otherwise pick
one tool per job — the git command line for GitHub Desktop, VS Code for PyCharm, Codex for Claude —
and follow the same steps.

### Changed

* **`README.md`'s *The tools* is three jobs, one tool for each, either option doing the job**:
  versions, in GitHub Desktop or the git command line; code and debug, in Claude or Codex; read and
  run, in PyCharm or VS Code, whose free editions are enough. It named GitHub Desktop and PyCharm as
  though there were no alternative. The APM packages leave the table for the paragraph below it:
  they come on top of whichever assistant is picked, not as a pick of their own.
* **`SETUP.md` offers the same choice wherever it names a tool**: step 1 clones with GitHub Desktop or
  `git clone`; *What "done" looks like* publishes a plain clone from GitHub Desktop or from the git
  command line, and opens the folder in PyCharm or VS Code and in Claude or Codex.

## 0.7.5 (2026-09-17)

**PATCH** — steps 4 and 6 describe the libraries as they now are: Portfolio Construction exists and is
called inside step 4's one signature, and Attribution Analysis, whose documentation is now public,
reads a daily book. No result changes.

**What to do differently:** in step 6, hand the attribution library the book's daily weights from the
backtest, never `Portfolio/portfolio_weights.csv`. In step 4, build a Portfolio Construction method one
rebalance date at a time, on a history cut before that date. If you trimmed `apm.yml` to some
packages, `universe` and `portfolio-construction` can now be named.

### Changed

* **`portfolio_construction.py` calls the Portfolio Construction library inside its one signature**
  where the library is installed, instead of being the seam a future library would replace. The
  library is KaxaNuk's own and not distributed publicly yet, so it stays out of `pyproject.toml` like
  the engines, installed by hand and imported behind a guard. Its methods that estimate from a returns
  history use whatever history they are built with, so the module builds one per rebalance date on
  the history before it.
* **The attribution reads the book's daily weights.** Attribution Analysis 0.2.0 rejects a weight file
  that is not a daily series once it spans a year, so `backtest_engine.py` reads the book's daily
  weights back from the engine and `attribution_analysis.py` shapes them. The README's four shared
  modules say so; on [`example`](../../tree/example) the module descriptions and the notebook's
  handoff table do too.
* **`SETUP.md` step 4 and `apm.yml` list the published packages** — `common`, `universe`,
  `data-curator`, `portfolio-construction`, `backtest-engine`, `attribution-analysis` and
  `investment-lab` — in the order of the steps they serve.

## 0.7.4 (2026-09-17)

**PATCH** — the template reads in the order a newcomer needs it, and a repository made from it says
what comes after setup and stays true about itself. No result changes.

**What to do differently:** after setup, start at `OBJECTIVE.md`; the order after it is *Starting
your own strategy* in the template's README, which now follows *Setup* directly. In step 5, put the
README's status line in `AGENTS.md`'s banner and rename `name` and `author` in `apm.yml`, and commit
all four files together.

### Changed

* **`README.md` puts the newcomer's path first**: what the template is for and what it needs, the
  install line, the eight steps, *The tools*, *Setup*, *Starting your own strategy* and *The
  documents*; *What is in here*, *The six Lab modules* and *The conventions worth keeping* follow as
  reference for when the work reaches the universe and the data. The paragraph on `main` and
  `example` moves below the install line, and the first lines say that building the data needs a
  provider key and that steps 5 and 6 need the licensed engines.
* **The order of work says what it is before it starts.** Its eight items are named as the order of
  work, not the eight steps; the files it names are said to be on `example` before the list, not
  after; item 3 requires delisted names in the seed; item 5 is headed by the benchmark choice it
  asks for first.
* **`AGENTS.md` holds inside a strategy repository.** It pointed at a local `README.md` that step 5
  replaces, said `main` holds no strategy, and put issues on KaxaNuk's project. It now points at the
  template's README, says what `main` and `example` are on the template and in a strategy
  repository, states that `main` is never merged into `example`, and marks example content only on
  `example`. Its banner no longer says every file is a description on a branch whose folders hold
  `.gitkeep`.
* **Setup step 5 hands over a next step.** The strategy README it writes links to the order of work
  and names `OBJECTIVE.md` as next, and so does the agent's hand-over; step 5 also carries the
  status line into `AGENTS.md` and the owner's name into `apm.yml`, whose comment asking for that
  is gone.
* **`SETUP.md` is shorter before its first command**: the folder rule is two paragraphs, the skills
  step says what APM and a skill are, the keys step names each key, and the paragraph for somebody
  who needs no research process is one sentence.
* **`OBJECTIVE.md` marks all its guidance in italics** and has the fifth part its closing table
  lists, *Where each half is named*, which is where the `c_*` and `r_*` columns are now asked for.
* **`RESULTS.md`'s comparison rule says what to compare**: a winner's Sharpe with its own
  experiment's control, and `vs control` across experiments.
* **The six Lab modules are numbered by the step they belong to**, 3 to 6, not 1 to 6 beside a step
  table where step 1 is the Bibliotheca, and the licensed engines point at the skills that install
  them.

### Fixed

* **The two-command lines in `SETUP.md` step 5 and `README.md`'s fetch are split in two**: `&&` is a
  parse error in Windows PowerShell 5.1, which step 1 names as the shell the Claude app and Codex
  drive on Windows.
* **`SETUP.md` says `uv` uses Python 3.12 if it finds it**, and downloads 3.13 only if neither is
  there; `pyproject.toml` allows both.
* **`AGENTS.md` puts the benchmark in `JOURNAL_1.md` once `BRAINSTORMING_1.md` has chosen it**, and
  lets that entry come before `BLUEPRINT_1.md`, which is otherwise still the first commit on an
  experiment's branch; it named the journal as where the benchmark is chosen.
* **`RESULTS.md` says *Known limitations* is not empty**, and `.gitignore` and `AGENTS.md` point at
  files a strategy repository still has.

## 0.7.3 (2026-09-16)

**PATCH** — the public `example` is the worked strategy, and the documents stop contradicting each
other about it and about the order of work. No result changes.

**What to do differently:** read `example` as `liquid-momentum` worked through the process, its own
lines between example markers; copy the shape from it and delete what is the strategy's — the
fenced content, the seed, the notes under `Bibliotheca/Papers/` and the entries in
`Bibliotheca/LOG.md`. Set nothing up twice: a repository with `.venv/` is set up, with or without
`apm_modules/`.

### Changed

* **`example` holds `liquid-momentum`.** 0.7.0 said it held no strategy; it now carries one, worked
  through the process step by step, public beside `main`, so the shape can be read rather than
  imagined. `README.md`, `SETUP.md` and `AGENTS.md` describe the branch that way, name the example
  markers, and say what to strip when a file is brought across.
* **`OBJECTIVE.md`'s header says before any paper is read**, where it said before the backtest —
  the later deadline let the reading come before the claims — and its guidance names what a claim's
  evidence is at each step: the question that would settle it, then the notes, then `RESULTS.md`.
* **The researcher paragraph in `README.md` follows the order of work**: the claims are drafted from
  the owner's words before any paper, and their evidence rewritten from the notes afterwards. It
  said the claims were drafted from the notes.
* **The eight steps say which numbering they use.** Item 4 runs *process* steps 2 and 3 — Universe
  and Data — and item 5 cites a note from the reading in item 2, so the two numberings no longer
  read as one. Item 5 names the one entry that comes early: `BRAINSTORMING_1.md`'s benchmark
  choice, before `BLUEPRINT_1.md`, because Experiment 1 is the benchmark.
* **`experiment-lifecycle` is named with the package that carries it**, `investment-lab`, in
  `README.md` and `SETUP.md`; a reader who trims `kaxanuk` to a subset can now keep it. `apm.yml`,
  `README.md` and `SETUP.md` promise one skill package per Lab library *as each is written* — three
  of the six libraries have one today.
* **A column with a setting an experiment will sweep lives in the Refinery**, whether it is fitted
  or a window. `README.md`'s prefix table and its rule admitted only a rank, a breadth reading or a
  fitted model to `r_*`, and sent every other per-security quantity to the Curator — where a sweep
  costs a download.
* **Graduation criterion 3 demands what the process produces**: the trial count published beside
  the winner, and the sign-off saying whether the deflated figure was also computed. It demanded a
  deflated count no stage computes, and `FINDINGS_N.md` gains the section `RESULTS.md` compiles the
  count from. The step descriptions on `example` stop contradicting the README: the universe
  notebook talks to the provider too, a window to sweep lives in the Refinery, the null VWAP is one
  provider's habit rather than every provider's, `Universe/Charts/` is gone, and step 8 is funding,
  wherever the desk is.
* [`example`](../../tree/example) takes the same text, and its notes, notebooks and journal stop
  saying the branch is private or that a filled-in copy is elsewhere.

### Fixed

* **The first-run test in `AGENTS.md` is `.venv/` alone.** It also named `apm_modules/`, so a
  repository whose owner answered *no* to the skills — which `SETUP.md` calls a working repository —
  was reported as not set up in every session. The same block says *the commands in it*, not *four
  commands*: the count depends on whether the clone and the README step are included.
* **`.gitignore` names `CLAUDE.local.md`** — the per-machine fallback KaxaNuk-Researcher's
  invitation describes, which holds an absolute path to one machine — and the folders the other
  APM targets write: `.gemini/`, `.opencode/`, `.windsurf/`. `SETUP.md` invites those targets and
  then says anything else in `git status` is a mistake.
* **`SETUP.md`'s example for a project that is not built from this template** no longer prefixes
  `apm` with `uv run`, which only works inside this repository's `.venv/`.
* **`SETUP.md`'s last paragraph points at the template's README** for the order of work, since
  step 5 replaces the strategy's README with one that links there.
* **`apm.yml` and `pyproject.toml` carry the changelog's number.** 0.7.1 and 0.7.2 left them at
  0.7.0.

---

## 0.7.2 (2026-09-16)

**PATCH** — the order a strategy is built in starts with the objective, before any paper. No result
changes.

**What to do differently:** start a strategy with `OBJECTIVE.md` — the idea and its claims — and
read for those claims before choosing the investable universe, which is now step 3 of the order
rather than the first thing done.

### Changed

* **`README.md`'s *Starting your own strategy* is the order of work, in eight steps.** The objective
  before any paper; the objective fine-tuned by reading for each claim, the sources that argue
  against it included; the investable universe; the data, in the order the Data stage already gave;
  `BLUEPRINT_1.md` before the rule, every prediction citing a note or an analyzer measurement; the
  broad reading and brainstorming; the cycle of portfolio construction, backtest and attribution
  until it is finished; and every finished cycle into `RESULTS.md`, kept or rejected. It listed the
  universe first, but the claims decide what the universe has to contain, and reading with no claim
  to read for has no stopping condition.
* **Step 1 of the eight is the idea and its claims first, then the literature that argues with
  them**, where it read *a literature review with a thesis at the end of it* — the order this change
  reverses. Its row names `OBJECTIVE.md` beside `Bibliotheca/`.
* **`SETUP.md`'s last paragraph** names the objective as the first thing to do, where it named the
  universe.
* [`example`](../../tree/example) takes the same text, and its `BIBLIOGRAPHY.md` plain-words line
  to match.

---

## 0.7.1 (2026-09-11)

**PATCH** — what a `Bibliotheca/` holds, now that a researcher writes its notes a chapter at a
time. No result changes.

**What to do differently:** keep the PDFs beside their notes and let git ignore them, along with
`Bibliotheca/Extracts/`, where the researcher's script leaves a book's chapters as text. A book is
a folder — `Books/Author_Year_Title/INDEX.md` for the chapter table, one file per chapter read —
and `Bibliotheca/Knowledge/` is gone: the notes beside the sources are the library, `BIBLIOGRAPHY.md`
is its index and `Bibliotheca/LOG.md` its record. The files themselves are on
[`example`](../../tree/example).

### Added

* **`AGENTS.md` says who writes a note:** a person, or a researcher with `read`, after a plan and a
  go; whoever writes a note adds its row to `BIBLIOGRAPHY.md`. It was the one step-1 document the
  table did not name.
* **`.gitignore` keeps the PDFs and the extracts out**, as step 1's own section. Licensed material
  is not redistributed by a clone, and the extracts regenerate with one command.

### Changed

* **`README.md`'s `Bibliotheca/` row describes the folder as it is now** — notes beside their PDFs,
  a book as a folder of chapters, `LOG.md` — and its researcher section says what the companion
  actually does here rather than that it is being built. `KaxaNuk/KaxaNuk-Researcher` 0.3.0 is the
  version that writes these notes.

---

## 0.7.0 (2026-09-10)

**MINOR** — `main` is the shape and nothing else: six folders and the documents at the root. Every
file the process expects inside those folders moved to the public `example` branch, unchanged.

**What to do differently:** `main` no longer ships `Experiment_1`, the drivers, the notebooks or the
shared modules. Bring a file across from `example` when you need it — `README.md` gives the one
command — or let the `experiment-lifecycle` skill scaffold an experiment.

### Removed

* **Everything below the six folders**, moved to `example` as it was: `Bibliotheca/`'s index,
  `Knowledge/`, `Notes/`, `Papers/` and `Books/`; `Universe/`'s seed and notebook; `Data/`'s three
  drivers, the two `custom_calculations.py` and the data directories; `Experiments/`' four shared
  modules and `Experiment_1/`; `Paper_Trading/`'s gate and scripts. `Config/.env.template` stays,
  because setup needs it. A reader opening `main` now sees the shape in one screen, and a reader
  who wants the files finds all of them on one branch rather than half here and half there.

### Changed

* **`README.md`'s *What is in here* is the one place the folder contents are written down** — a
  table per folder saying which step owns it, what belongs in it and what is committed. The old
  tree listed files that are no longer on `main`.
* **`README.md`'s Setup section is a pointer to `SETUP.md`**, with no commands of its own. Two
  copies of the same commands had already started to differ.
* **`example` is public, in this repository, beside `main`.** `README.md`, `SETUP.md` and
  `AGENTS.md` said it was private; it holds no strategy, so there was nothing to keep private. A
  strategy worked end to end still stays in KaxaNuk's own repositories.

---

## 0.6.0 (2026-09-06)

**MINOR** — one prompt sets a strategy up from nothing. *Please help install
`https://github.com/KaxaNuk/KaxaNuk-Research-Process`* is now enough for an agent with no other
context, and the manifest names one package so the template cannot go stale.

**What to do differently:** the skills command is `uv run apm install --target claude` (or `codex`),
not a bare `apm install`, and there is nothing to install by hand before `uv sync` — not even Python.

### Changed

* **`SETUP.md` was run as an agent would run it, and rewritten where it broke.** Handed only the
  URL, an agent does not know the strategy's name — it now asks, and decides the root from what the
  current folder holds. `apm` lives inside `.venv/` and is not on a fresh terminal's path, so every
  skills command is `uv run apm …`. The fresh-history sequence is given in PowerShell as well as
  bash, because that is what the Claude app and Codex drive on Windows. A first commit on a machine
  that has never committed fails for want of a git identity; the agent asks for one and sets it for
  the repository only. Prerequisites shrink to git and uv, each with its one-line installer — `uv`
  downloads Python 3.13 itself. A hand-over paragraph says what the agent reports and where it stops.
* **`apm.yml` names one package, `kaxanuk`.** It is every KaxaNuk package under one name, and it
  resolves transitively — verified. The template listed four packages by hand and was already stale:
  `attribution-analysis` had shipped and a fresh install missed it. Replace the line with the packages
  you want if you want fewer.
* **The skills question has an answer when the request already gave one.** *Install it and the
  skills* is consent and the agent runs it; a bare *set this up* still gets asked. `AGENTS.md` and
  `SETUP.md` say the same rule.
* **A plain clone ends with no remote, and `SETUP.md` now says so** — GitHub Desktop, *Add existing
  repository*, *Publish*. The user's to do, not the agent's.

---

## 0.5.1 (2026-09-06)

**PATCH** — documentation. `SETUP.md` says what a finished setup actually leaves behind.

**What to do differently:** commit `uv.lock`. `uv sync` writes it, the template ships without one on
purpose, and your repository keeps it — it pins the versions a result came from.

### Fixed

* **The "what done looks like" check said `git status` would be clean; a real run leaves `uv.lock`
  untracked.** Running the file end to end from a fresh clone is what caught it, which is the reason
  the check is in `SETUP.md` at all.

---

## 0.5.0 (2026-09-06)

**MINOR** — the repository now carries its own setup instructions and declares which agent skills it
wants. No result changes; nothing in the pipeline moved.

**What to do differently:** set a strategy up from [`SETUP.md`](SETUP.md) rather than from a prompt
held in another repository. `apm install` needs no arguments, and it is a question you get asked
rather than a step you have to run.

### Added

* **`SETUP.md` — the whole of setup in one file**, written so an agent can follow it end to end:
  getting the repository (the template button, `gh repo create`, or a plain clone with a fresh
  history), the one-folder rule, `uv sync`, the credential copy, and — last, and as a question — the
  agent skills. It replaces the `start-a-strategy` prompt that lived in `KaxaNuk/KaxaNuk-APM`, on the
  rule that **the instruction to install a thing belongs with that thing**. A bootstrap you can only
  reach after installing the tool it bootstraps is a bootstrap that gets pasted from a URL.
* **`apm.yml`, committed.** It names the KaxaNuk packages this repository wants, so `apm install`
  takes no arguments and nobody types a package name. It carries no `targets` key on purpose: the
  template serves Claude Code, the Claude app, Codex and Cursor alike, so the target is set on the
  machine or passed per command.

### Changed

* **`.gitignore` stops ignoring `apm.yml`**, and says why: the manifest is a declaration, like
  `pyproject.toml`, while everything APM downloads and writes — `apm_modules/`, `.claude/`,
  `apm.lock.yaml` — is build output, ignored the way `.venv/` is. **A clean `git status` after a full
  setup is the test** that the split is right.
* **`AGENTS.md` opens with a *First run* block**, before anything about branches. An agent that finds
  no `.venv/` or `apm_modules/` offers `SETUP.md` instead of starting work in a repository that has
  not been set up, and the two rules it must not get wrong are restated there: never print a value
  from `Config/.env`, and ask before installing the skills.
* **`README.md`'s Setup section is three commands and a link.** One source, so the two cannot drift.
* **Python is `>=3.12,<3.14`, and 3.13 is the one to install.** The ceiling is the Backtest
  Engine's: it is documented for 3.12 or 3.13, and every performance figure here comes from that
  engine, so a version it cannot be installed beside is a version that cannot finish the pipeline.
  The Data Curator allows 3.12 to 3.14, which leaves 3.13 as the version that satisfies both. Ruff
  targets `py313` to match. Widen it when the engine supports 3.14.
* **`SETUP.md` says to clone somewhere short on Windows.** APM stages downloads several directories
  below the root, so a deep synced path fails part-way through with `WinError 3: The system cannot
  find the path specified`. The same install from a short path succeeds, which is why the message is
  worth naming: it reads like a missing file, not like a path-length limit.

---

## 0.4.1 (2026-09-05)

**PATCH** — documentation. `README.md` now states the setup order and the layout it has to produce.
No result and no file in the pipeline changed.

**What to do differently:** set a strategy up in **one** folder. The clone is the root; `uv sync`,
`apm init` and `apm install` all run in it, and the agent tooling lands beside the process folders
rather than in a directory above them.

### Changed

* **`README.md` gains an ordered Setup** — the repository named after the strategy, cloned, then
  `uv sync`, `apm init -y --target claude`, `apm install KaxaNuk/KaxaNuk-APM/common`, then the
  credential file. The order is a dependency: `apm-cli` arrives with the `dev` group, so the
  environment has to exist before APM can be initialised.
* **The setup section shows the root it should produce**, and names the failure it is there to
  prevent: a wrapper folder holding the clone. Initialising APM in an empty wrapper writes a second
  `apm.yml`, a second `.claude/` and a `requirements-dev.txt` that only exists because the wrapper
  has no `pyproject.toml` — and Claude opened at the wrapper reads that empty setup and never sees
  the research tree.
* **"The tools" moved above "Setup"**, so the README reads install-once, then set-one-strategy-up,
  then start it. The APM paragraph says where the packages land rather than only how the CLI
  arrives.

---

## 0.4.0 (2026-09-04)

**MINOR** — `main` becomes a description-only template. **There is no code on it any more:** every
file is a short statement of what is expected in it.

**What to do differently:** nothing on `main` runs. Read it to learn the shape, fill it in with your
own idea, or read the `example` branch KaxaNuk keeps beside `main` for one strategy worked end to
end.

### Added

* **`LICENSE` — MIT**, the Data Curator's licence, so the template can be public, forked and
  contributed to without friction. `main` lives at `KaxaNuk/KaxaNuk-Research-Process`.
* **The tools, and a researcher beside the process.** `README.md` names the four tools — GitHub
  Desktop, PyCharm, Claude, and the APM packages through which Claude learns the six modules — and
  points at `KaxaNuk/KaxaNuk-Researcher`, a companion that reads a strategy's `Bibliotheca/` and
  drafts the hypothesis in each blueprint from it.
* **Attribution in two layers and a third pass.** `AGENTS.md` now says what each layer answers:
  Brinson-Fachler names the lever that moved, the factor model separates compensated tilts from
  idiosyncratic alpha, and Brinson-Fachler on the residual says whether the Sharpe survives once
  the factor turns. The notebook, the module and the gate say the same.

### Removed

* **All executable code.** The Curator and Refinery drivers, the four shared experiment modules,
  the two calculation modules and every notebook code cell are now docstrings and markdown. A template whose example code has to be
  deleted before you can start is a template that gets started by deleting things.
* **The nine Bibliotheca notes and the lockfile** — they belong to a filled-in repository, and they
  are on `example`.
* **The dev container** and its Docker build context. Setting the environment up is two commands,
  and a container that has to be rebuilt whenever the process changes is a second thing to maintain.

### Changed

* **Every remaining file describes what is expected in it**, in the same shape: what the stage is in
  plain words, what it produces, what it prevents, and the sections it owes. Learn the shape once.
* **`README.md` rewritten around the eight steps**, each with its plain-words sentence, its output
  and the failure it prevents, plus the six Lab modules mapped one per stage and the conventions
  worth keeping when two people share a tool.
* **`AGENTS.md` cut roughly in half.** The five ways a backtest lies are one table — the lie, what
  the process does, what it still does not do. Everything the README covers was removed rather than
  restated.
* **The source-note convention moved to `Bibliotheca/BIBLIOGRAPHY.md`**, next to the notes it
  governs. Its Part 0 keeps the lineage the process descends from, as provenance rather than notes.
* **`Universe/Investable_Universe.csv` requires only `main_identifier`** — the name the Data Curator
  asks a provider for. Every other column is yours, so an equity, ETF, FX, crypto or futures seed
  runs the same process.
* **`Config/.env.template` carries the Data Curator's provider keys**, not one.
* **Joined classification columns are prefixed `current_`**, not suffixed `_current`, so every column
  family is a prefix, and the prefix alone says which stage owns a column and whether it is
  point-in-time.
* **Bibliotheca notes carry their four fields as frontmatter**, so a tool can index what cites
  what, and **blueprint predictions cite a note or a measurement** — never nothing.

## 0.3.0 (2026-09-04)

**MINOR** — the template stops being US-equity-shaped, gains a fourth shared module, and splits into
two branches: `main` is the process with nothing in it, `example` is one strategy worked end to end.

**What to do differently:** the universe is now a CSV whose only required columns are `ticker` and
`name`, so the repository is multi-asset by default. Name your signal in two places —
`ELIGIBILITY_COLUMN` in `Data/analyzer.ipynb` and `SIGNAL_COLUMN` in the experiment notebook — and
the benchmark rule runs without being written.

### Added

* **`Experiments/portfolio_construction.py`** — step 4, behind one swappable signature: given the
  securities eligible today and a returns history already cut off before today, return weights
  summing to **at most** one. `equal_weight` and `inverse_volatility` ship; a minimum-variance
  optimiser, hierarchical risk parity, or a call into the KaxaNuk Portfolio Construction library are
  the same shape, so swapping one is one line in the rule cell.
* **`Experiments/attribution_analysis.py`** — step 6, split out of the engine so the two KaxaNuk
  libraries live in one module each. It owns the shaping of hand-supplied index data into the tables
  the library auto-detects, and reports which of its four inputs are missing before it tries. Getting
  that layout wrong makes the loader read the attribution transposed rather than fail, which is why
  the shaping is not left in a notebook.
* **A benchmark rule that works out of the box.** Section 2 of the experiment notebook holds
  everything the signal calls eligible, equally weighted, cash for the rest — event-driven, one day
  of lag. It runs as soon as `SIGNAL_COLUMN` is set, because a benchmark you have to write before you
  can measure anything is a benchmark that never gets written.
* **A run order that is stated in seven places.** `README.md` numbers the six commands, and every
  file in the pipeline says where it sits in that order in its first paragraph, so wherever you land
  you know what must have run before it.
* **The branching model, written down.** `main` (the template), `example` (one strategy, for reading)
  and `issues/<number>` cut from `main` and merged back into it — one per issue on the GitHub
  Project, opened before the branch because the issue is where the reasoning lives.
* **Example markers.** `# --- example: begin ---`, `<!-- example: begin -->` and
  `# EXAMPLE-ONLY CELL` mark any line that belongs to a worked example rather than to the process, so
  the two branches can be told apart by reading rather than by diffing.
* **A step-3 findings section in `RESULTS.md`.** Notebook outputs are stripped before committing, so
  a measurement that lived only in a cell output did not survive the commit. Findings from the Data
  stage now have a durable home.

### Changed

* **`Universe/Investable_Universe.csv` requires only `ticker` and `name`.** Every stage reads it
  without knowing what is in it, so a crypto, FX or futures seed runs the same pipeline. The 787-row
  US-equity seed is gone.
* **`Data/curator.py` rewritten** — 851 lines to 652, and the reduction is the smaller half of it.
  Work is handed out one identifier at a time through a plain thread pool with thread-local
  providers, replacing a chunked worker scheme, a shared mutable tally object and a lock-guarded
  progress counter; `download_identifier` now returns an outcome string instead of mutating shared
  state. An empty universe file is reported as a sentence rather than a traceback.
* **`Data/refinery.py` deletes refined files for securities no longer in the universe.** Leaving
  them was the worst kind of bug this stage can have: every cross-sectional column is computed over
  the securities present, so a stale file carries ranks taken against a universe that no longer
  exists, and anything reading the directory silently averages two incompatible cross-sections. It
  produced a plausible number and no error.
* **The daily return moved from the Refinery to the Curator**, as `c_return_1d`. It is a function of
  one security's own history, so it was in the wrong stage.
* **`Data/refinery.py` joins whatever the security master classifies by**, reporting and skipping a
  column the master does not carry instead of joining it in as nulls. The `sector`/`industry`
  hard-coding is gone; the `_current` suffix rule that made it safe stays.
* **The shared modules are renamed for what they hold**: `panel.py` is now `securities_panel.py` and
  `engine.py` is now `backtest_engine.py`, joined by the two new modules — so `Experiments/` reads as
  panel in, weights, engine out, attribution.
* **`securities_panel.py` names no classification column in `BASE_PANEL_COLUMNS`.** Classification is
  optional and discovered from the files, and a missing column raises a readable error naming it
  rather than failing inside `read_csv`.
* **`Universe/universe.ipynb` rewritten**, from 49 cells to 20, and no longer equity-shaped. It now
  answers the question everybody forgets: **when does each security become usable?** A five-year
  warm-up moves the honest start of a backtest by five years, and nothing else in the pipeline says
  so.
* **`Data/analyzer.ipynb` rewritten** around the information-coefficient table, with the two
  questions any signal owes an answer to written into its header: does it separate anything, and if
  it is fitted, what is look-ahead worth?
* **`AGENTS.md` cut from 624 lines to about 380.** Everything the README covers — the eight steps,
  the column convention, setup, credentials, the shared modules — was removed rather than restated.
  Versioning moved here, to the file that already explained it.
* **`README.md` rewritten as the entry point**: six numbered steps that run the pipeline, a
  walkthrough of the eight process steps in the order to do them, and one table saying where each
  kind of logic goes. **The run order is stated as a dependency**, because the universe notebook sits
  between two Data commands and running the refinery early does not fail — it silently drops columns.
* **The invariant that weights sum to 1.0 is now "at most 1.0".** A strategy that can go to cash
  cannot satisfy the stricter form, and the engine already parks the residual in a real, priced
  instrument.
* **The bar in `AGENTS.md` gains a clause:** never choose a parameter on the metric it will be judged
  by. Choose it on a property of the signal — persistence, coverage, turnover — and publish the
  sweep.

### Removed

* `stage_supplied_price_series` and its engine-column fallbacks from the Curator. It staged a
  hand-supplied index price series into the market-data directory; machinery kept for a file that
  does not exist teaches the reader to keep machinery for files that do not exist. The drop-zone
  directories and the *what is missing* report stay.
* The `sector_sample` download mode, and the 787-row US-equity universe with it.

## 0.2.0 (2026-09-03)

**MINOR** — additive. The Bibliotheca gains the two books whose method the process runs, and the
lineage the process descends from.

### Added

* **Part 0 of `Bibliotheca/BIBLIOGRAPHY.md` — where the process comes from.** Fifteen questions the
  field asked in order, who answered each, what it settled, and which step or rule of this process
  descends from it. Provenance, not notes.
* **Two book notes**: Paleologo (2021) — total PnL as an idiosyncratic series plus a factor series,
  selection, sizing and timing by counterfactual books, and why a factor model built on relative
  factors is blind to an absolute rule; and Grinold & Kahn (2000) — the information coefficient, the
  fundamental law, and the information horizon behind the analyzer's decay chart.
* Part 5 states the one control with no paper behind it — look-ahead — rather than citing a weak fit.

---

## 0.1.0 (2026-09-03)

**MINOR** — the template instantiated. No strategy, no data, no result: the KN Research Process with
nothing in it yet.

### Added

* The eight-step **KN Research Process** as a folder structure, steps 1-7 inside the repository and
  step 8 outside it. Each stage owns its outputs and reads only from the stages above it.
* **Four control documents at the root** — `OBJECTIVE.md`, `RESULTS.md`, `CHANGELOG.md`, `AGENTS.md`
  — with stated contracts, plus `README.md` and a one-line `CLAUDE.md`.
* **`Experiments/Experiment_1/`**, the benchmark slot, with its four per-experiment files and a
  notebook whose section contract leaves exactly one cell — the rule — to the strategy.
* The two shared modules, `Experiments/securities_panel.py` and `Experiments/backtest_engine.py`, and the Data stage's
  three blocks.
* `Universe/universe.ipynb` and the 787-row `Universe/Investable_Universe.csv` seed.
* `Bibliotheca/` with the note convention and **seven research-integrity notes**, one per control
  `AGENTS.md` claims.
* `Paper_Trading/BITACORA.md` with the five-criterion graduation gate, and two skeleton scripts
  carrying their contracts as docstrings.
* Dev container, `Config/.env.template`, Ruff configuration and `.gitignore`.

### Provenance

Extracted from **Golden-Flow 0.9.0** (commit `10a0d6b`), the KaxaNuk Investment Lab's reference
implementation, on 2026-09-03. Everything specific to that strategy was removed; everything the
process itself needs was kept.
