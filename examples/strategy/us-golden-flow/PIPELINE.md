# Pipeline — how the code runs, and how to debug it

> **How this strategy's code runs:** what runs, in what order, what each step reads and writes,
> where the rule lives in the code, and what to check when something looks wrong. The *why* of the
> rule is `BLUEPRINT_N.md`, the numbers are `FINDINGS_N.md`; this file is for the person who has to
> run it again, or find out why a run stopped.
>
> Write it once the pipeline has run end to end, and keep it current: a step that moves, a file
> that is renamed or a run that takes twice as long changes this file in the same commit.

---

<!-- example: begin -->

How US-Golden-Flow's Experiment 1 turns Sharadar's prices into books, backtests and attribution:
what runs, in what order, what each step reads and writes, where the rule lives in the code, and
what to check when something looks wrong. The *why* of the rule is
[`Experiments/Experiment_1/BLUEPRINT_1.md`](Experiments/Experiment_1/BLUEPRINT_1.md); the numbers
are [`FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md). **Experiment 1 reads the Curator
alone** (owner's decision, 2026-11-16); the Refinery comes back with Experiment 2.

---

<!-- example: end -->

## 1. The run, in order

*A table: the step, the one command that runs it from the repository root, what it reads, what it
writes, and how long it takes from nothing. Then any file a step does not write but needs, and
where it comes from.*

<!-- example: begin -->

`Universe/KN_US_Equity_Core.csv`, the universe as the KaxaNuk app reads it, is written by
`Universe/seed.py` with the seed, not by any step below: a run that clears outputs keeps it.

Every command runs from the repository root. Each step stops with an error when its input is
missing; none of them guesses.

| # | Command | Reads | Writes | Time |
| --- | --- | --- | --- | --- |
| 0 | `uv run python Config/install_libraries.py` | `Config/.env` (keys and index hosts, by name) | the environment | minutes, once |
| 1 | `uv run python Data/curator.py` | `Universe/Investable_Universe.csv` (the seed), Sharadar, the Core's holdings | `Data/Curator/Time_Series/<TICKER>.csv`, one per listing, plus `DFF.csv`, `KN_US_Equity_Core.csv`, `SPY.csv` | ~1 h 45 min from nothing (2026-11-20) |
| 2 | `uv run python Universe/universe_marimo.py` | the seed, the curated files | `Universe/Security_Master.csv`, `Data_Issues.csv`, `Coverage.csv`, `Window.csv` | minutes |
| 2b | `uv run python Data/analyzer_marimo.py` | the curated files, `Universe/Window.csv` | `Data/Analyzer/`: the IC table, separation, concentration, diversification, buy and hold against the cross | ~5 min |
| 3 | `uv run python Experiments/Experiment_1/compare_library_sizing.py` | the curated files | `library_sizing_check.csv` | minutes |
| 4 | `uv run python Experiments/Experiment_1/experiment_1_marimo.py` | everything above, the factor model | `Portfolio/`, `Backtest/`, `Attribution/` | ~1 h 40 min, the twenty random books priced at both cost rows |
| 4b | `uv run python Experiments/Experiment_1/attribute_base_books.py` | the engine's cached runs in `Backtest/cache/`, the Core's holdings and returns, the factor model | `Attribution/`: the three passes for the rule, its control, equal weight and the uncapped arm, at both cost rows, and for the rule and the uncapped arm by sub-period; the factor model on the random books, over the window and by sub-period | ~25 min |
| 5 | `uv run python Experiments/Experiment_1/app_workbooks.py` | the four headline weight files | four engine workbooks in `Backtest/`, the flat 5 bp row | ~30 min |

To look at a notebook instead of running it: `uv run marimo edit
Experiments/Experiment_1/experiment_1_marimo.py`.

**After step 5, in the KaxaNuk app:** *Backtest → Parameters → Import results* lists the workbooks
in `backtest/`; import each one, and it appears in *History*. A workbook dropped in the folder is
not listed in History until it is imported.

---

<!-- example: end -->

## 2. Step by step

*Each step in a few lines: what it does to its input, the bookkeeping it writes beside its output,
and what it checks before it stops.*

<!-- example: begin -->

### Step 1 — `Data/curator.py`: the data

Downloads every listing in the seed from Sharadar through the KaxaNuk Data Curator, in batches of
25, every column the Curator serves (prices, dividends, splits, quarterly fundamentals) plus the
`c_*` columns of `Data/Curator/custom_calculations.py`. Then three passes over the files:

1. **Spin-offs** (`apply_spin_offs`) — Sharadar's `actions` table adds the value of a spin-off to
   the total-return close, which its dividend column leaves out.
2. **Completion** (`complete_files` → `_complete_file`) — for every seed listing:
   - cuts the file to its dates in the seed (`valid_from`, `valid_to`), so a ticker another company
     reused never mixes in;
   - computes again the window columns on what is left (`golden_cross_of_closes`,
     `traded_value_average`);
   - adds `c_index_weight` (the Core's weight that day) and `c_eligible_golden_cross_50_200` (see
     the columns below).
3. **Checks** (`check_adjustments`) — every file's rebuilt adjustment against Sharadar's own,
   written to `Data/Curator/adjustment_checks.csv`.

**Bookkeeping it writes beside the files:** `fetched_through.json` (the date each file was fetched
through: a file already current is skipped on the next run) and `fetch_outcomes.json` (Sharadar's
last word on each name: `downloaded`, `not carried`, `recycled ticker`, `refused`).

### Step 2 — `Universe/universe_marimo.py`: the universe

Checks the seed, builds the security master, writes the data-issues register (a **blocking** row
excludes a name from every book), and the window: it opens on 1999-12-31 if the members with a
price and 200 days of history hold at least 90% of the Core's weight on every date.

### Step 4 — `Experiments/Experiment_1/experiment_1_marimo.py`: the experiment

| Section | What it does | Look here when |
| --- | --- | --- |
| 0 · Setup | every constant: window, bounds, costs, sweep, `SECTORS` | a number in the rule is wrong |
| 1 · The panel | `securities_panel.load_matrices` — one `dates x securities` matrix per column; the rebalance dates | a name or a date is missing |
| 2 · The rule | `eligibility`, `target_book`, `strike`: the rule, its control, the no-cap arm | the book holds the wrong names |
| 2.1 · Invariants | caps, floor, sector cap, lag, `c_eligible_golden_cross_50_200` agreement — printed PASS/FAIL | any FAIL |
| 3 · Construction | holdings, orders, turnover, capacity, sector weights | the book looks untradeable |
| (books cell) | every book written: four in `Portfolio/`, the rest in `Portfolio/variants/` | a book is missing in the app |
| 4 · Backtest | every book priced in the engine's batch mode; truncated runs excluded by name | a run is excluded |
| 5 · Attribution | Brinson-Fachler by KN sector, the factor model, Brinson-Fachler on the residual | an attribution figure is odd |
| 6 · Counterfactuals | the sweep, the band, the random books | P3 or P2 |
| 7 · Verdict | the predictions and the gate, `gate.csv` | the gate's reading |
| 8 · Verify | reads back what it wrote and **raises** if wrong | the run stopped here |

---

<!-- example: end -->

## 3. The columns the rule reads

*Each column the rule consumes, what it is, and the file and function that build it.*

<!-- example: begin -->

All in each `Data/Curator/Time_Series/<TICKER>.csv`, so the app charts them.

| Column | Meaning | Written by |
| --- | --- | --- |
| `c_close_dividend_and_split_adjusted` | the total-return close every signal, return and mark reads | `custom_calculations.py`, rebuilt from the exact close |
| `c_open_dividend_and_split_adjusted` | the fill price, the open on the same basis | `custom_calculations.py` |
| `c_golden_cross_50_200` | **1** while the 50-day average is above the 200-day, **0** otherwise, empty for the first 199 days | `custom_calculations.py`, again in `complete_files` |
| `c_golden_cross_20_100`, `c_golden_cross_100_300` | the same for the sweep's two neighbours | same |
| `c_traded_value` | the day's close times its volume, split-adjusted, double-adjusted splits corrected | `custom_calculations.py` |
| `c_traded_value_sma_63d` | its 63-day average: **the rule's rank and weight** | `custom_calculations.py`, again in `complete_files` |
| `c_traded_value_sma_21d`, `c_traded_value_sma_126d` | the sweep's neighbours | same |
| `c_index_weight` | the KN US Equity Core's weight that day; 0 when not a member | `complete_files` |
| `c_eligible_golden_cross_50_200` | **1** when the name was a member with `c_golden_cross_50_200` at 1 **at the prior close** | `complete_files` |
| `c_market_cap` | the Curator's own, close times diluted shares; not read by the rule | the Curator |

---

<!-- example: end -->

## 4. The rule in the code

*Where eligibility, ranking, sizing, the band and the rebalance dates live: the notebook cell and
the functions of the shared modules, named, so a reader can go from the blueprint's sentence to the
line that does it.*

<!-- example: begin -->

On each rebalance date d (the first trading day of the month):

```
eligible on d   = c_eligible_golden_cross_50_200 on d                      (member and crossed at the prior close)
                  and a traded value at the prior close
                  and an open price on d
                  and not a blocking row of Data_Issues.csv
target          = bounded_book(eligible, score, cap 20%, floor 1%, weigher)
struck          = banded_book(target, ..., band 0.5 points)
```

**Where each piece lives:**

- `eligibility()` and `target_book()` — the rule cell, section 2 of the notebook.
- `portfolio_construction.bounded_book` — cuts the score to the prior close (`.shift(1)`) and
  sizes each date with the weigher.
- `portfolio_construction.bounded_by_score_and_sector` — **the sizing**: names in order of traded
  value; each is added if no weight falls below 1%, otherwise skipped and the next tried.
- `portfolio_construction._capped_by_name_and_sector` — **the filling**: weights proportional to the
  score; a name above 20% held at 20%; a sector above 50% scaled down to 50%; what that frees spread
  over the names still free; what nobody can take is cash.
- `portfolio_construction.banded_book` — a held name whose target moved half a point or less keeps
  its drifted weight.
- The control: `target_book(use_cross=False)`. The cap's control:
  `target_book(sector_maximum=None)`.

---

<!-- example: end -->

## 5. Debugging recipes

*Short, runnable snippets for the questions a run raises: one name end to end, one name's signals,
one date's book and why a name is in or out, a priced run read without the engine.*

<!-- example: begin -->

### Run one name, end to end

```bash
uv run python Data/curator.py --identifiers AAPL
```

It downloads AAPL only, runs the three passes, and stages the cash rate and the index. A file
already current is skipped: delete `Data/Curator/Time_Series/AAPL.csv` to fetch it again.

### Look at one name's signals

```python
import pandas
frame = pandas.read_csv("Data/Curator/Time_Series/AAPL.csv", index_col="m_date")
columns = ["c_index_weight", "c_golden_cross_50_200", "c_eligible_golden_cross_50_200", "c_traded_value_sma_63d"]
print(frame.loc["2026-09-25":"2026-10-02", columns])
```

`c_eligible_golden_cross_50_200` on a day equals `c_index_weight > 0` and `c_golden_cross_50_200 ==
1` **on the row before**. If it does not, the completion pass did not run on that file.

### See one date's book, and why a name is in or out

```python
import sys
import pandas
sys.path.insert(0, "Experiments")
import attribution_analysis
import portfolio_construction

sectors = attribution_analysis.kn_sectors(attribution_analysis.load_factor_returns())
score = pandas.Series({"MU": 31.6e9, "NVDA": 26.4e9, "AMZN": 10.0e9, "BE": 3.7e9})
book = portfolio_construction.bounded_by_score_and_sector(score, 0.20, 0.01, sectors, 0.50)
print(book, book.groupby(book.index.map(lambda name: sectors.get(name, "unclassified"))).sum())
```

With these four names each takes the 20% cap and 20% stays in cash: four names cannot place every
dollar under a 20% cap. Hand it the scores at the prior close of the date you care about
(`c_traded_value_sma_63d`, the row before the date) for the names `c_eligible_golden_cross_50_200`
lets in. The journal's read-back (`JOURNAL_1.md`, *the rule read back*) shows 2026-09-01 and
2026-10-01 done this way.

### Check the sizing against the library

`compare_library_sizing.py` sizes every date both ways and writes
`Experiments/Experiment_1/library_sizing_check.csv`: names in one book only, and the largest weight
difference. A row with a difference above 1e-5 is a date to look at.

### Read a priced run without the engine

Every engine answer is cached in `Experiments/Experiment_1/Backtest/cache/` under the hash of its
weight file and settings; a re-run reads it instead of pricing again.

```python
import glob
import pandas
for path in glob.glob("Experiments/Experiment_1/Backtest/cache/*.pkl"):
    run = pandas.read_pickle(path)
    if run.get("name") == "portfolio_weights":
        print(run["start_date"], run["end_date"], run["window"])
        print(run["register"]["Total_Portfolio_Value"].tail())
```

Changing one digit of a weight file prices it again: its hash changed.

### Why a run was excluded

`Backtest/excluded_runs.csv` gives each excluded run and its reason. **Truncated** means the engine
stopped valuing before the window's end — usually a cash error, a rebalance whose costs outran the
1% reserve. Verify refuses to exclude the rule, its control, equal weight or the no-cap arm: if one
of those is truncated, the run stops at section 8.

### The app shows no backtest

History lists only what was imported. *Backtest → Parameters → Import results*, pick the workbook.
The app's log is `%LOCALAPPDATA%\KaxaNuk\logs\connector.log`: an import shows there as
`received dispatch: job <n> (backtest ...)` and `... completed`.

---

<!-- example: end -->

## 6. Where to find what a run printed

*Which log or file each step's output lands in, and what to read first.*

<!-- example: begin -->

The notebooks print as they go; run from a terminal, redirect to keep it:

```bash
uv run python Experiments/Experiment_1/experiment_1_marimo.py > experiment_1.log 2>&1
```

What each step leaves on disk to read afterwards:

| File | What it says |
| --- | --- |
| `Data/Curator/fetch_outcomes.json` | each name's download outcome |
| `Data/Curator/adjustment_checks.csv` | each file's rebuilt adjustment against Sharadar's |
| `Universe/Data_Issues.csv` | every data issue; `blocking` rows are excluded |
| `Universe/Window.csv`, `Coverage.csv` | the window, and the Core's share priced each day |
| `Experiments/Experiment_1/Backtest/summary.csv` | every book's engine statistics |
| `Backtest/excluded_runs.csv`, `gate.csv`, `sub_periods.csv`, `sweep_*.csv` | the exclusions, the gate, the sub-periods, the sweep |
| `Attribution/brinson_fachler.csv`, `factor_model.csv`, `brinson_fachler_residual.csv` | the three attribution passes |

---

<!-- example: end -->

## 7. Common failures

*The failures seen so far, each with its symptom, its cause and its fix.*

<!-- example: begin -->

| Message or symptom | Cause | What to do |
| --- | --- | --- |
| `KNDC_API_KEY_SHARADAR is empty` | the key is not in `Config/.env` | fill it; check by name: `grep -E '^[A-Z_]+=$' Config/.env \| cut -d= -f1` |
| `Column not available under prefix 's'` | a short dividend or split name | use the joined names: `s_split_date_numerator`, `d_ex_dividend_date_dividend_split_adjusted` |
| `LicenseNotFoundError` from Portfolio Construction | the licence not loaded | `portfolio_construction._load_licence` reads `Config/.env`; run from the root |
| `no panel files in Data/Curator/Time_Series` | step 1 not run | run `Data/curator.py` |
| a FAIL in 2.1 · Invariants | the rule broke a bound | the line names which; check one date with the recipe above |
| `r_golden_cross_50_200 differs from the Curator's` | Refinery only (Experiment 2) | the Refinery's cross and the Curator's disagree on more rows than a tie can flip |
| the app lists ~100 portfolios | weight files at the top of `Portfolio/` | only the four headline books belong there; the rest go to `Portfolio/variants/` |

<!-- example: end -->
