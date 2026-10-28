---
name: backtest-engine-runs
description: >
  Load this skill whenever a run of the KaxaNuk Backtest Engine is being set up, executed, debugged
  or read. Use it when the user asks to install `kaxanuk-backtest-engine`, initialise its project
  files, shape a portfolio weight file or market-data files for it, fill in
  `backtest_engine_parameters.xlsx`, call `PyArrowBacktester`, the batch mode
  (`MultiPortfolioBacktester`) or the `kaxanuk.backtest_engine` CLI, price commission, slippage and
  the cash's interest inside the engine, add a benchmark, or read the returned tables and the Excel
  report (CAGR, Sharpe, Sortino, VaR, CVaR, drawdown, annual returns). It covers the two inputs the
  engine reads and the layouts it detects, the licence and its environment variable, and how the
  engine is called from a KaxaNuk Strategy Template repository. It does NOT cover the research process or
  the notebook contract (use `experiment-lifecycle`), running the attribution library (use
  `attribution-analysis-runs`), reading attribution output (use `alpha-decomposition`), or authoring
  Data Curator `c_*` columns (use `data-curator-custom-calculations`).
metadata:
  version: 0.5.0
  library_version: 0.67.0
---

# Running the KaxaNuk Backtest Engine

Step 5 of the KaxaNuk Investment Lab: the rules are run over history, with costs and no look-ahead,
and a track record comes back. The engine is **licensed** and closed-source — it is not on public
PyPI, and it is deliberately absent from the KaxaNuk Strategy Template's `pyproject.toml` so its
index URL and key never enter version control. This skill was verified on build **0.67.0** of the
engine, the frontmatter's `library_version`, by the worked example's run on it (Golden Flow 0.17.0,
2026-10-24, every book priced in the batch mode); a line that names 0.66.0 was measured on that
build and not repeated. Compare it with the installed build `uv pip list` shows, and on a newer
minor or major version treat every trap here as unproven until it is checked again.

**What this skill knows comes from the documentation, the changelog and runs — never from the
engine's code.** Never open, search, print or inspect its installed files, and never read a source
page its documentation site links to. What neither the documentation nor a run says is not known;
a run settles it, and a difference from this file goes to `lab@kaxanuk.mx`. An error is reported by
the call, its type and its message, never by the engine's own traceback lines.

**Since 0.67.0, from its changelog; the worked example's licence validated on 0.67.0 for every book
it priced.** The licence is checked
through `kaxanuk-license-client`, a new dependency from KaxaNuk's private index — the one the
install command below names, which serves it to any valid licence — for the product
`backtest-engine`: a licence without it is refused, naming the products it holds. Offline, a saved
check stands in for **3 days** from the last successful one (7 on 0.66.0); a rejection is final and
deletes it. Saved checks live in `%LOCALAPPDATA%\KaxaNuk\licence-cache\backtest-engine` on Windows,
`$XDG_CACHE_HOME/kaxanuk/licence-cache/backtest-engine` elsewhere (`KAXANUK_LICENSE_CACHE_DIR`
moves them); `~/.kaxanuk_cache` is no longer read, so **the first run after upgrading needs the
network**. `.kaxanuk_license` is read as a `.env` file: `KNBE_API_KEY_KAXANUK=<key>`, or one
unnamed key for every product. `KNBE_LICENSE_SERVER_URL`, then `KAXANUK_LICENSE_SERVER_URL`, names
another server; `LicenseConfigurationError` refuses one that is not an http or https URL; the
licence errors are also `kaxanuk.license_client.LicenseError`. `validate_license()` returns a
keyword-only `ValidationResult` (`ok`, `message`, `expires_at`). **`main()` returns a licence that
does not validate as `success=False`** in its `BacktestResult` instead of raising: read `success`
before `data`, as the worked example does. The log file is UTF-8.

**Every performance figure in a KaxaNuk strategy comes from this engine.** There is deliberately no
second, lighter simulator: one that disagreed would only let a reader pick the number they
preferred.

## 1. Install it without leaking the key

**Without a licence:** the Backtest Engine comes, with its licence, in the KaxaNuk Investment Lab,
which KaxaNuk sells. For a licence, write to `lab@kaxanuk.mx`, saying what it is for, with *via
KaxaNuk Researcher* in the subject — <https://www.kaxanuk.mx/lab> shows the Lab. (The Lab's access
facts: `references/investment-lab.md` in the `next` skill's folder.)

Install from the index URL in the licence welcome email, from the repository root and through `uv`,
so it lands in the repository's `.venv` rather than wherever the first `pip` on the path points:

```bash
uv pip install kaxanuk-backtest-engine --extra-index-url https://license:{YOUR_LICENSE_KEY}@{SERVER}/simple/
```

Inside a KaxaNuk Strategy Template repository that is all: the configuration is built in code, in
`Experiments/backtest_engine.py` (section 7; the worked example's `build_configuration` shows how),
and nothing is initialised at the root. Outside one, lay down the project files once:

```bash
uv run python -m kaxanuk.backtest_engine init excel
```

Three rules, and the first is not negotiable:

- **Never print, echo or commit the key or the index URL** — not into a notebook output, a log line,
  a shell history or a dependency file. The command above carries a credential: run it, do not paste
  it back. An exposed key is rotated, not edited out.
- **Never add the engine to a repository's dependency file.** It is installed by hand, per machine,
  by whoever holds the licence.
- **Python 3.12 or 3.13**, per the documentation. That ceiling is the engine's, and it is why a
  KaxaNuk Strategy Template repository pins `requires-python = ">=3.12,<3.14"` and installs 3.13:
  the Data Curator allows up to 3.14 and the engine does not, so 3.13 is the version that satisfies
  both. A project pinned above the range needs a separate interpreter for the engine — report the
  mismatch rather than quietly pinning around it.

The licence key lives in `Config/.env` as **`KNBE_API_KEY_KAXANUK`**. That is the name KaxaNuk uses,
and it is what a repository created from the KaxaNuk Strategy Template ships in
`Config/.env.template`. It is the only key the engine reads: **`KNPC_API_KEY_KAXANUK` is Portfolio
Construction's licence**, since its 2.0.0, and a page that shows it for the engine is wrong. Never
rename one into the other, and **never print the value of either.**

**Keep it installed.** The licensed package is deliberately absent from `pyproject.toml` and the
lockfile, and `uv sync` is *exact* by default: it removes every package the lockfile does not name.
Probed on 2026-09-09 in a strategy repository — a plain `uv run …` keeps a hand-installed package,
`uv sync --inexact` keeps it, a bare `uv sync` removes it. So, once the engine is installed, never
run a bare `uv sync` in that repository again. After a relock use `uv sync --inexact` (with the
repository's groups), run everything else through `uv run`, and check `uv pip list | grep -i
kaxanuk` before any engine run. If the engine has vanished, this is why, and the install command
above is the fix.

## 2. Guard the import, always

A clone without a licence must still run everything else. Any module or cell that imports the engine
reports what is missing and skips, rather than raising:

```python
import importlib.util

ENGINE_INSTALLED = importlib.util.find_spec("kaxanuk.backtest_engine") is not None
```

Check `ENGINE_INSTALLED` before the call, and import `kaxanuk.backtest_engine` only inside that
branch, as the worked example's `Experiments/backtest_engine.py` does; where it is `False`, say
plainly that step 5 was skipped for want of the licensed engine. A `try` around `from kaxanuk…
import …` does the same job but fails Bloom Code (BLOOM003). **A pipeline that dies at an optional
import is a pipeline nobody can read.**

## 3. The two inputs

**The portfolio file — what to hold, and when.** Two layouts, detected automatically:

| Layout | First column | The rest |
| --- | --- | --- |
| Horizontal | `Ticker` | one column per rebalancing date |
| Vertical | `date` | one column per ticker |

**The market-data files — one per security**, named `{TICKER}.csv` or `{TICKER}.parquet`. Each needs
a date column and at least three price columns. Which column plays which role is declared in the
configuration rather than inferred from its name, so a provider's naming does not have to be bent to
suit the engine.

Two consequences, and both are ways a backtest lies:

- **Commission is charged on the unadjusted price**, so the file the engine costs against has to
  carry the price actually paid, not a back-adjusted series.
- **A security missing from the market data on a rebalance date cannot be filled.** Reconcile the
  portfolio file's tickers against the market-data directory *before* running, and report the
  difference by name. A run that quietly holds fewer names than the weights say still summarises
  cleanly, and that is the failure nobody catches.

## 4. Configure it

`Config/backtest_engine_parameters.xlsx` holds the simulation parameters and the column-role
mapping. The same configuration can be supplied programmatically as a dict or YAML, which is what a
sweep should use — **a sweep that edits a workbook between runs is a sweep nobody will reproduce.**

In code, `main()` and `PyArrowBacktester` take a `kaxanuk.backtest_engine.entities.Configuration`.
The fields the worked example sets, the three price roles among them, and the two CSV input
handlers it passes are listed in `references/api.md`.

**Every cost and the cash are the engine's settings, never a calculation beside it** — the worked
example's, run on 0.67.0:

- **Commission in basis points of the notional:** `commission_model = "basis_points"` and
  `commission_basis_points`. `Configuration` still requires `commission_cents` whatever the model —
  without it, a `TypeError` (on 0.66.0) — so the example passes `0.0`, unused.
- **Slippage from the day's range and volume:** `slippage_model = "spread_plus_impact"`, a
  half-spread estimated from the day's high and low (`spread_estimator = "corwin_schultz"`; the
  engine's other estimator, Abdi–Ranaldo, also reads the close) plus square-root impact from the
  volume, with `slippage_basis_points` the half-spread where a range is missing. Those columns are
  roles, like the prices: `user_column_high`, `user_column_low`, `user_column_close` and
  `user_column_volume`. `slippage_model = "basis_points"` is a flat half-spread instead.
- **The cash's interest:** `financing_benchmark_rate` names a rate file in the market-data folder,
  read at its last observation on or before each day, and `cash_interest_spread` is what the broker
  keeps below it — `"DFF"` and `-0.005` in the example, FRED's effective federal funds rate less
  half a point, as Interactive Brokers pays on a dollar balance. **The same rate is the risk-free
  rate of every Sharpe ratio the engine reports**, so those Sharpe ratios are excess of cash.
- **A delisted position**, whose prices stop: `delisted_position_handling = "sell_at_last_price"`
  sells it at its last price, booked that day, with no day of hindsight.

**A range-based spread overstates the most traded names.** In the worked example the engine's
Corwin–Schultz estimate charged the rule $362,502 of slippage against $15,573 of commission at 1 bp
— about 23 bp a trade, 40 to 55 bp on some dates, on AAPL, MSFT and NVDA — and Abdi–Ranaldo was no
better, 7 to 40 bp, median by year (measured on 0.66.0; no engine figure of a book moved on 0.67.0).
Its stress row, 5 bp commission and 10 bp flat, came out cheaper than the base. So **price every
book again at a flat half-spread beside the model**, and register that row in the blueprint before
the run, so it is never a forking path afterwards.

## 5. Run it

The CLI, from the project root, outside a KaxaNuk Strategy Template repository — inside one the
engine is called in code (section 7):

| Command | What it does |
| --- | --- |
| `uv run python -m kaxanuk.backtest_engine autorun` | installs missing project files on the first run, then executes the entry script |
| `uv run python -m kaxanuk.backtest_engine init excel` | lays down the configuration format and an entry script |
| `uv run python -m kaxanuk.backtest_engine run [PATHS]` | executes the given entry scripts or directories |
| `uv run python -m kaxanuk.backtest_engine update excel` | refreshes a template after an engine upgrade (also `update entry_script`) |

Or in code — `PyArrowBacktester`, built one of two ways and run one of two ways:

```python
backtester = PyArrowBacktester.create_from_configuration(
    configuration=configuration,
    input_handlers=[csv_input],
    portfolio_handlers=[csv_portfolio_input_handler],
    commission_model=commission_model,
)
results = backtester.run_with_benchmark()
```

`create_from_pipeline_result` is the same construction when the data pipeline has already run;
`run()` is `run_with_benchmark()` without the comparison arm. Full signatures, the properties an
instance exposes, and where each came from are in `references/api.md`.

**Many books at once: the batch mode, run on 0.67.0.** A single run loads the market data for its
one book; an experiment of a hundred books spent most of its time loading the same files — 445 of
452 engine minutes in the worked example. `MultiPortfolioBacktester` prices a batch of books that
share every setting but their weights against one load. The worked example parses a batch with
`config_handlers.BatchConfigParser.parse_dict` — `global_defaults`, the configuration's fields as
plain numbers, strings and ISO dates, the capital an integer; `portfolios`, each a `name` and its
`inline_weights`, rebalance date to identifier to weight; and an `output` folder — and runs
`MultiPortfolioBacktester(input_handlers=[...], portfolio_handlers=[]).run(batch_config=...)`. Each
of `results["entries"]` carries `name`, `success`, `error_message` and `result`, the same tables as
a single run's `data`, but **no benchmark statistics**: it returns each benchmark's daily value and
return, and the example measures them with the engine's own `compute_portfolio_statistics`, on the
book's window, years and risk-free rate. Read that way, the KN US Equity Core's Sharpe is 0.315,
where the figure reported beside a single run was 0.308 — one no series of the index reproduces.
`references/api.md` has the shapes.

**Attach the real cost model.** On a high-turnover book the difference between a flat cost
assumption and real per-share commission can be a third of the edge, so results are accepted **net,
or not at all**. `commission_model` and `slippage_model` are constructor arguments precisely so this
is a decision somebody makes rather than a default nobody read.

## 6. Read what comes back

`run()` returns a `BacktestResultDict`, and the `main()` entry point wraps it in a `BacktestResult`
with `success`, `error` and `data`. Tables arrive as PyArrow or pandas; the Excel report carries
CAGR, Sharpe, Sortino, alpha, VaR, CVaR, maximum drawdown, annual returns, drawdown analysis and
portfolio weights. `references/api.md` lists the keys of `data`, verified on 0.66.0 and read on
0.67.0 by the worked example's batch.

**`Daily_Weights` is the book as the engine actually held it**, one row per trading day, its columns
the holdings plus the benchmark and `CASH_RESERVE`. That is the drifted daily series **step 6
reads** — the attribution library rejects a file that only carries the rebalance dates — so it is
written out beside the other results rather than recomputed later from the weight file. **Each row
is struck at that day's close**: shares at the day's mark over the day's value, on 0.66.0, so it
already holds the day's return — and on 0.67.0 the worked example's first cut, both weight tables
moved one day on, reconciles to the index within 0.22 points a year. It earns the next day's;
`attribution-analysis-runs` says how step 6 moves it one day on.

The `metrics` module is public, so a figure quoted in a document can be recomputed from the returned
series rather than copied out of a cell: `sharpe_ratio`, `sortino_ratio`, `annualize_rets`,
`annualize_vol`, `var_historic`, `var_gaussian`, `cvar_historic`, `drawdown`, `tracking_error`,
`information_ratio` and `compute_portfolio_statistics` among them — all listed in
`references/api.md`.

**The engine's years are weekday steps over 252**, measured on 0.66.0: a window of 2015-01-02 to
2026-06-01 was 11.81 years as the engine counts them — 2,976 weekday steps after the first day —
against a calendar span of 11.41 years, so a CAGR sits a little below one taken over calendar
years. The worked example's window, 2000-01-03 to 2026-08-14, is 27.56 years as the engine counts
them. Label a quoted CAGR as the engine's.

**Read the run before believing it.** A truncated run — one that stopped valuing the book partway —
still produces a clean-looking summary over the stub. Check the last valued date against the window
that was asked for, and when they differ the variant is excluded **by name, with its reason**, never
quietly dropped. In a KaxaNuk Strategy Template repository the experiment notebook's section 4
counts the days each engine run valued against the trading days of the window it was asked for,
never against a fixed floor, which a run that stopped years early can clear, and **excludes a short
run by name, with its reason**, in `Backtest/excluded_runs.csv`; no cell after it reads that run,
and a gate criterion that needs it reads "not evidenced". Section 8, Verify, raises if a run is
neither read whole nor excluded, or if a book the verdict stands on — the rule, its control, the
arms the blueprint names — is among the excluded. The worked example holds each run to at least 99%
of those days valued and no more than five unvalued at the end — a rule of its own, not a sourced
figure.

**What a truncated run looks like, reproduced on 0.66.0.** A book whose weights sum to exactly 1.0
run with `cash_reserve_percentage = 0` cannot pay commission at a rebalance. The engine prints one
line — `Cash error on <date> with $-340.92` — stops valuing there, and returns:

| | Truncated | Complete |
| --- | --- | --- |
| `success` / `error` | `True` / `None` | `True` / `None` |
| days in `Register_df` | 522 | 1305 |
| CAGR | 23.6% | 14.2% |
| a key naming the stub | none | — |

Both runs wrote an Excel report, and the shorter one annualised over its stub, so its CAGR is the
higher of the two. **The check that catches it:** `data["end_date"]` and `data["years"]` describe
the window the engine *valued*, not the one the configuration asked for — compare them with the
configured dates before reading a single metric. **The cure is `cash_reserve_percentage`**, a
fraction, the cash held back to pay for a rebalance. No reserve is safe for every book and window,
so check every run's valued days: the worked example holds 1%, and twenty-one of its runs still
stopped at a rebalance whose costs outran the reserve, random books most of them; each is excluded
by name, as its `FINDINGS_1.md` lists them. A reserve raised after the result is a change to the
experiment, not a fix.

Configuration guards worth knowing before a first run, measured on 0.66.0: `commission_cents` is
rejected outside `[0.00, 0.10]`, and the engine checks on every rebalancing date that each position
it touches has a price and that no position outlives its price series. **"Touches" includes every
open position, not only the names traded.** A book that still holds a name across a gap in its
prices — a corporate event, a provider's missing days — is refused on the first rebalance date
inside the gap, with a data-integrity error naming the ticker and the date. No configuration field
waives it. A name whose prices simply stop is `delisted_position_handling`'s to sell; a gap inside
a series is the register's: the worked example lists the name as a blocking row of
`Universe/Data_Issues.csv`, excludes it by name from every book and prices the run again, so no
book trades off its own dates (`portfolio-construction-runs`).

**`commission_cents` is not cents per share, measured on 0.66.0** and not repeated on 0.67.0, since
the worked example now charges basis points. On one stock bought once, a setting of `0.05` charged
$0.041 a share on SPY and $0.035 on KO, and `0.006` charged $0.0049 and $0.0042: neither a flat
amount per share nor a share of the price. Before a per-share figure is frozen in a blueprint, run
it once and compare `Total_commissions` with the shares traded in `orders_df`.

**Two traps of the inputs, met by the worked example.** The engine reads weights as fixed-scale
decimals and refuses a value it cannot hold exactly, so a third written as 0.3333333333333333 fails
before the first fill: the example writes six places, each rounded down, so no column sums above
one. And on 0.66.0 its Parquet reader refused the example's curated Parquet files, so the example
stages a CSV copy of the columns the engine reads, `Data/Curator/Engine/`, and points it there.

## 7. Inside a KaxaNuk Strategy Template repository

The engine is not called from a notebook directly. `Experiments/backtest_engine.py` is the seam, and
it owns five things: writing the weight file the engine reads, setting every cost and the cash in
the engine's configuration, pricing books — many at once, in the batch mode, each answer cached
under the hash of its weight file and its settings — reading the results back, and aligning
variants onto one window so they can be compared. Everything specific to a strategy stays in that
strategy's notebook, `Experiments/Experiment_N/experiment_N_marimo.py`, a marimo notebook run as a
script.

- `Experiments/Experiment_N/Portfolio/portfolio_weights.csv` — the book, in the shape section 3
  describes.
- `Experiments/Experiment_N/Backtest/` — where results land, and **nothing in it is committed**: no
  workbooks, no charts. The numbers reach `FINDINGS_N.md`, and `RESULTS.md` is compiled from those.
- Target weights, what the rule returns, sum to **at most** one, and so does every column of the
  weight file. There is no cash fund and no cash row: what the weights leave stays as cash in the
  engine, which pays it the rate file's rate less the broker's spread (section 4).
- `Backtest/excluded_runs.csv` — every run excluded by name, with its reason (section 6).

## Where the documentation is

This skill was written from these pages. Go to them for anything it does not answer, and prefer them
whenever the two disagree.

| Page | URL |
| --- | --- |
| Quick start | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/user_guide/quick_start.html` |
| End user manual | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/user_guide/end_user_manual/index.html` |
| Base backtest | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/base_backtest_rebalance_pyarrow.html` |
| Backtest components — cost models, execution, interfaces, enums, orchestrators | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/backtest_components.html` |
| Metrics | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/metrics.html` |
| Portfolio data pipeline | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/portfolio_data_pipeline.html` |
| Market data pipeline | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/market_data_pipeline_orchestrator.html` |
| Data pipeline executor | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/data_pipeline_executor.html` |
| CLI | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/api_reference/cli.html` |
| Methodology | `https://kaxanuk-backtest-engine.readthedocs-hosted.com/en/latest/methodology/index.html` |
