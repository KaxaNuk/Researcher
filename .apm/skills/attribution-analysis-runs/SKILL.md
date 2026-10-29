---
name: attribution-analysis-runs
description: >
  Load this skill whenever a run of the KaxaNuk Attribution Analysis library is being set up,
  executed, debugged or read. Use it when the user asks to install `kaxanuk-attribution_analysis`,
  initialise its project files, shape the four inputs it reads (market data, daily portfolio and
  benchmark weights, benchmark returns, per-factor returns), turn a backtested book into the daily
  weights it requires, fill in `attribution_analysis_parameters.xlsx`, call the CLI or
  `performance_attribution.main`, drive `BrinstonFachlerArrowAttribution` or
  `KNFMArrowAttribution` directly, or get the allocation / selection / interaction and
  per-factor tables back out. It covers the exact input layouts, the traps that produce a
  clean-looking but wrong run, and how step 6 is called from a KaxaNuk Strategy Template repository. It
  does NOT cover what the numbers mean for a strategy (use `alpha-decomposition`) or running the
  backtest that produced the book (use `backtest-engine-runs`).
metadata:
  version: 0.7.0
  library_version: 0.2.0
---

# Running the KaxaNuk Attribution Analysis

Step 6 of the KaxaNuk Investment Lab: a book that beat its benchmark is taken apart into the pieces
that explain it. The library is **licensed** — not on public PyPI, and deliberately absent from the
KaxaNuk Strategy Template's `pyproject.toml` so its index URL and key never enter version control.
Its documentation is public, at
`https://kaxanuk-attribution-analysis.readthedocs-hosted.com/en/latest/`, and this skill is written
against the **0.2.0** build of it. Go there for anything this file does not cover; this file keeps
what the documentation does not say, and what a KaxaNuk repository adds. Build 0.2.0 is the
frontmatter's `library_version`: compare it with the installed build `uv pip list` shows, and on a
newer minor or major version treat every trap here as unproven until it is checked again.

**What this skill knows comes from the documentation, the changelog and runs — never from the
library's code.** The library is licensed: never open, search, print or inspect its installed
files, and never read the source pages its documentation site links to. What neither the
documentation nor a run says is not known; a run settles it, and a difference from this file goes
to `lab@kaxanuk.mx`. An error is reported by the call, its type and its message, never by the
library's own traceback lines.

**Changed in 0.3.0, from its changelog — not yet checked by a run here.** The licence is checked
through `kaxanuk-license-client`, a new dependency from KaxaNuk's private index — the one the
welcome email's install command names, which serves it to any valid licence. The check runs on the
unified licence server, for the product `attribution-analysis`: a licence without it is refused,
naming the products it holds. Offline, a saved check stands in for **3 days** from the last
successful one (7 on 0.2.0); a rejection is final and deletes it. Saved checks live in
`%LOCALAPPDATA%\KaxaNuk\licence-cache\attribution-analysis` on Windows,
`$XDG_CACHE_HOME/kaxanuk/licence-cache/attribution-analysis` elsewhere (`KAXANUK_LICENSE_CACHE_DIR`
moves them); `~/.kaxanuk_attribution_cache` is no longer read, so **the first run after upgrading
needs the network**. `.kaxanuk_license` is read as a `.env` file: `KNAA_API_KEY_KAXANUK=<key>`, or
one unnamed key for every product. `KNAA_LICENSE_SERVER_URL`, then `KAXANUK_LICENSE_SERVER_URL`,
names another server; `LicenseConfigurationError` refuses one that is not an http or https URL; the
licence errors are also `kaxanuk.license_client.LicenseError`. `validate_license()` returns a
keyword-only `ValidationResult` (`ok`, `message`, `expires_at`): code that built the old one by
position names its fields. The log file is UTF-8, and a console that cannot encode the offline
warning still shows it.

**Changed in 0.4.0 to 0.6.0, from its changelog — not yet checked by a run here.** Until a run
checks them, read every section below as written for 0.2.0, and these first:

- **The numbers change by default (0.4.0).** Brinson-Fachler is the textbook formula of 1985 by
  segment, `brinson_fachler_formula = textbook`, and each date's effects must reconcile to
  `R_p - R_b` or the run stops; the former asset-level numbers are `legacy`, deprecated. Cumulative
  effects are linked, `linking_method = carino` (or `grap`, or `none` for the former running sums),
  so they add up to the compounded return. The first price date, which has no return, is left out.
  Net weights under 1 are topped up with `cash_ticker` (`CASH`), which earns 0. In the factor model
  `f_market` is an ordinary factor, the aggregate files `f_total_factor_returns`,
  `f_total_excess_returns` and `f_idyo_returns` are no longer loaded, and `f_carry.csv` and
  `f_dividends.csv` are components of their own, not factors.
- **The classes this file names were renamed (0.4.0), and the old names fail since 0.5.0:**
  `BrinstonFachlerArrowAttribution` is `BrinsonFachlerArrowAttribution`, `.brinston_fach_indexes`
  is `.brinson_fachler_indexes`, `cummulative_pct_decomp()` is `cumulative_pct_decomp()`, and
  `returns_investible_assets` is `returns_investable_assets`. The code in section 6 below runs only
  on 0.2.0 to 0.4.x as written.
- **Results come back as data (0.4.0).** `run_attribution(configuration)` returns an
  `AttributionResult` and writes nothing; `main()` returns it too. `run_attribution_from_backtest()`
  attributes a finished Backtest Engine 0.67.0 run in memory, with an `implementation` table that
  splits the engine's return into holdings return and costs. New settings: `factor_return_type`
  (`log` restates log factor files as simple returns), `risk_free_rate` for the Sharpe ratio, and
  `active_factor_model`, the factor model on the benchmark's weights too. Weights files must be
  daily. The dashboard binds to `127.0.0.1`, debug mode off.
- **`main()` writes an Excel report (0.5.0)**, `<portfolio>_<UTC time>_attribution_results.xlsx`, to
  `output_directory` (`Output` by default), and raises `OSError` if it cannot;
  `output_handlers=()` writes nothing. `AttributionResult.diagnostics` keeps every warning a run
  logged, each with a stable `code`. 0.6.0 adds `benchmark_stats`, `relative_stats` (tracking error
  and information ratio, defined as the Backtest Engine's) and results `by_year`, and lays the
  report out as professional attribution reports are.

**This skill gets the numbers out. It does not read them.** What allocation, selection and the
idiosyncratic residual mean for a strategy — and the counterfactual books that turn the residual
into selection, sizing and timing — is `alpha-decomposition`.

## 1. Install it without leaking the key

**Without a licence:** Attribution Analysis comes, with its licence, in the KaxaNuk Investment Lab,
which KaxaNuk sells. For a licence, write to `lab@kaxanuk.mx`, saying what it is for, with *via
KaxaNuk Researcher* in the subject — <https://www.kaxanuk.mx/lab> shows the Lab. (The Lab's access
facts: `references/investment-lab.md` in the `next` skill's folder.)

The documentation's quick start has the command; the ready-to-run version, key included, arrives in
the licence welcome email. Run it from the repository root and through `uv`, so it lands in the
repository's `.venv` rather than wherever the first `pip` on the path points:

```bash
uv pip install kaxanuk-attribution_analysis --extra-index-url https://license:{YOUR_LICENSE_KEY}@{SERVER}/simple/
```

Inside a KaxaNuk Strategy Template repository that is all: in the worked example
`Experiments/attribution_analysis.py` shapes the inputs and builds the attribution objects in code
(sections 6 and 8), so there is no workbook and nothing at the root. Outside one, lay down the
project files once:

```bash
uv run kaxanuk.attribution_analysis init excel
```

Three rules, and the first is not negotiable:

- **Never print, echo or commit the key or the index URL** — not into a notebook output, a log line,
  a shell history or a dependency file. The command carries a credential: run it, do not paste it
  back. An exposed key is rotated, not edited out.
- **Never add the library to a repository's dependency file.** It is installed by hand, per machine,
  by whoever holds the licence.
- **Python 3.12 or 3.13** — the Backtest Engine's ceiling too, and part of why a KaxaNuk Strategy
  Template repository pins `requires-python = ">=3.12,<3.14"`.

The licence key lives in `Config/.env` as **`KNAA_API_KEY_KAXANUK`** — a different variable from the
engine's `KNBE_API_KEY_KAXANUK`, and both sit in the same file; `~/.kaxanuk_license` or the exported
variable work too. **Never print the value of any of them.** The licence is checked against
KaxaNuk's server on every run, with a 24-hour local cache and an offline grace period of 7 days on
0.2.0, 3 on 0.3.0. A run that worked last week can fail today on a plane, and that is the licence,
not the data.

**Keep it installed.** `uv sync` is *exact* by default and removes every package the lockfile does
not name, and this one is deliberately not in the lockfile. Once it is installed, after a relock use
`uv sync --inexact` with the repository's groups, run everything else through `uv run`, and check
`uv pip list | grep -i kaxanuk` before step 6. If the library has vanished, that is why, and the
install command is the fix.

## 2. Guard the import, always

A clone without a licence must still run everything else. Any module or cell that imports the
library reports what is missing and skips, rather than raising:

```python
import importlib.util

LIBRARY_INSTALLED = importlib.util.find_spec("kaxanuk.attribution_analysis") is not None
```

Check `LIBRARY_INSTALLED` before the call, and import
`kaxanuk.attribution_analysis.performance_attribution` only inside that branch, as the worked
example does (`report_missing_inputs` in `Experiments/attribution_analysis.py`, then the import
inside its `attribute_book`, called only when nothing is missing). Where it is `False`, say plainly
that step 6 was skipped for want of the licensed library. A `try` around `from kaxanuk… import …`
does the same job but fails Bloom Code (BLOOM003). **A pipeline that dies at an optional import is
a pipeline nobody can read.**

## 3. The four inputs

The layouts are on the documentation's *Data Formats* page; `init excel` lays down `Input/Data/`,
`Input/Portfolios/`, `Input/Benchmark_Portfolios/` and `Input/Factor_Models/`. What decides whether
a run is right:

**The first header decides everything, and it is not what the documentation says.** A weight file is
read as horizontal when its first header is `Ticker` and as vertical when it is **`date_column`**,
in any case — checked on 0.2.0 by running it. Anything else raises
`MissingPortfolioError: First column must be 'Ticker' or 'date_column'` before a number is read.
*Data Formats* asks for a date header, and `date` is rejected. The same rule governs the portfolio
weights, the benchmark weights and the benchmark returns file.

**The weights are daily.** Portfolio and benchmark weights alike, no nulls. **Once a weight table
spans a year or more, the library requires 240 to 260 rows a year** in its first and last year and
raises `DataIntegrityError` otherwise, precisely to catch a rebalance-only file passed by mistake.
So the weight file a Backtest Engine priced — one column per rebalance date — **cannot be passed
in**, whatever the *Data Formats* example suggests. The attribution reads the book as it was
actually held each trading day, drift included (section 8).

**A weight earns the next day's return, and the library will not lag it for you.** Both cuts pair
a weight with the return of its own date — the *Brinson-Fachler* methodology page's per-date
formulas, and the measurement below: a weight dated `t` multiplies the return dated `t`. The
Backtest Engine's `Daily_Weights` are struck at each day's close — shares at the day's mark over
the day's value, on engine 0.66.0 — and so are the Analytics Factory's index holdings, whose file
starts the day before its returns file does. Passed as they arrive, a weight that already holds a
day's move multiplies that move again, and every book, the benchmark's included, is credited with
the cross-section's daily variance. Nothing raises, and every figure reads larger. **Move both
tables one day on** — `weights.shift(1)`, first row dropped, so the close of `t−1` earns day `t` —
after the asset returns are computed on the unmoved dates, as the worked example's `held_overnight`
does. On the worked example's earlier Experiment 1, 2015 to 2026 on 0.2.0, the first cut's
benchmark read **21.23** points a year against the index's own 14.30 paired on the same day, and
**14.85** against 14.31 held overnight: a gap of 6.94 points a year, then of 0.54. Its current
Experiment 1, 2000 to 2026 on 0.5.0, held overnight, reconciles to 0.22 points a year.

**Market data — one file per security**, `{TICKER}.csv` or `{TICKER}.parquet`, with the date and
price columns named in the configuration (`user_column_date`, `user_column_price`); returns are
computed from the prices, and the Data Curator's `m_date` and `m_close_dividend_and_split_adjusted`
drop straight in. **Use the price basis the backtest marked on**: in a KaxaNuk Strategy Template
repository that is the dividend-and-split-adjusted close, and a split-adjusted column would drop
every dividend from the attribution. Dates are `YYYY-MM-DD`, as *Data Formats* asks, and **no file
carries a blank price**: trim its rows before its first price and after its last.

**Benchmark returns** go through the same portfolio loader, so they take the same two shapes: one
row of dates-as-columns, or a vertical file whose first header is `date_column` and whose single
other column is the index's daily return. Checked on 0.2.0: the vertical form loads and is reported
as one ticker.

**Per-factor returns — one CSV per factor**: the first column is the date, then one column per asset
holding that factor's return *for that asset*. **The first header may be empty**: a file whose
header row starts with a bare comma loads (checked on 0.2.0). Four things about that directory:

- **The file name is the factor name**, as *Data Formats* shows with `f_momentum.csv`: give every
  factor a plain file name ending in `.csv`.
- **Keep nothing but factor files in it.** The API reference says the loaders take each factor's
  name from its file and skip only `.gitkeep`.
- **Read the coverage.** *Data Formats* asks that factor files reference only the portfolio's
  tickers, and the API reference allows partial coverage: a held name missing from a factor file
  lowers that factor's coverage without raising. The run logs
  `Average total factor coverage throughout the portfolio`, as a percentage, and
  `Factor '<name>': reading k/n asset columns` per file. **Read both.** Low coverage means the
  factor attribution describes part of the book.
- **Four names belong to the model's own series**: `f_market`, `f_total_factor_returns`,
  `f_total_excess_returns` and `f_idyo_returns`, the names `Data/hand_supplied.py` gives the
  Analytics Factory's `Market`, `Total_Factor_Returns`, `Total_Excess_Returns` and `Idyo_Returns`.
  A run on 0.2.0 left the last three out of `cummulative_pct_decomp()` and kept a file named
  `f_Market` as an ordinary factor: the names are matched exactly, in lower case. Never give a
  factor of your own one of them.

**Widen the book to the benchmark, or the first cut compares it with a fraction of the index.**
On 0.2.0 the first cut prices only the securities named in the *portfolio* weight file and computes
the benchmark's return from those prices alone; the benchmark returns file, which *Data Formats*
says is used for date-range alignment, never enters it. Benchmark weight on a name the book does
not list has no return and silently drops out. **List every benchmark constituent in the portfolio
file, at zero weight where it is not held, each with a price series.** Proved on 0.2.0 with a book
of 8 names inside a 788-name index, the other 780 priced to earn exactly the index's daily return:

| First cut | Book only | Widened |
| --- | --- | --- |
| benchmark return, as a share of the index's own | 6.0% | 98.9% |
| alpha | +0.8845 | +0.1735 |
| interaction | +0.7415 | +0.0399 |
| portfolio return | +0.9305 | +0.9305 |

Unwidened, the benchmark was the 7.3% of the index the book happened to own, alpha came out about
five times too large, and nearly all of the excess was filed under **interaction** — the effect
least likely to be questioned. The book's own return did not move, which is what zero weights should
do. The last 1.1% was the 8 held names earning their own returns rather than the index's.

## 4. Configure it

`Config/attribution_analysis_parameters.xlsx`, one **General** sheet: the parameter name in A (**do
not touch**), your value in B, the description in C. The documentation's *Configuration Reference*
has every row; `references/configuration.md` has them with the traps below. The ones that decide the
run are the two methods (`brinson_fachler_method`, `factor_model_method`, independent), the two
columns read from your market data, the formats (lowercase), and the window (`YYYY-MM-DD` or
`auto`).

Two things to know:

- **Three directories are subfolders of `input_directory`** — the portfolio weights, the benchmark
  weights and the benchmark returns — while the *Configuration Reference*'s examples give
  `investable_assets_directory` and `factor_returns_by_factor_directory` with `Input/` in front.
  Set each the way the reference shows it, and check the paths when `input_directory` moves.
- **A notebook or a sweep builds `Configuration` directly**, which the API reference says raises
  `ConfigurationError` on an invalid value, at construction — and **a sweep that edits a workbook
  between runs is a sweep nobody will reproduce.**

## 5. Run it

The CLI, from the project root and through `uv run`, is on the documentation's *CLI* page; a
KaxaNuk Strategy Template repository calls the library in code instead (sections 6 and 8). Two
details it is easy to misread: `autorun` on a fresh folder **installs the project files and exits**
— it runs only on the next call — and `run` executes each entry script as its own subprocess.

In code, the documented sequence — *Running from Python* — is four calls, and the first two are not
optional in a notebook:

```python
load_config_env()
configure_logger(
    logger_name="kaxanuk.attribution_analysis",
    logger_level=logging.INFO,
    logger_format="[%(levelname)s] %(message)s",
    logger_file=None,
)
parameters_path = pathlib.Path("Config") / "attribution_analysis_parameters.xlsx"
configurator = ExcelConfigurator(parameters_path)
performance_attribution.main(
    configurator.get_configuration(),
    launch_dashboard=False,
    dashboard_port=configurator.get_dashboard_port(),
)
```

`load_config_env()` is what reads `Config/.env`, and without `configure_logger` at `INFO` the
coverage and date-range lines this skill tells you to read never print. The imports are
`services.env_loader`, `services.configuration_logger`, `config_handlers.excel_configurator` and
`performance_attribution`, under `kaxanuk.attribution_analysis`.

- **`dashboard_port` is keyword-only and has no default** — required even with the dashboard off,
  whatever the `main()` examples in the documentation show.
- **`main()` shows plots itself.** With `launch_dashboard=False` it draws static matplotlib
  figures, as the API reference says, and a run on 0.2.0 called `plt.show()` for each methodology.
  In a script, a notebook batch or CI, call `matplotlib.use("Agg")` before `main()`, or the run
  waits on a window nobody will close.

## 6. Read what comes back

**`main()` writes no files.** It returns `None`: log lines, figures, and perhaps a dashboard. The
quick start, the Excel workflow and the CLI page all say results are written to `Output/`; nothing
is. **To get numbers back, build the two attribution objects yourself** and read their attributes:

```python
brinson = BrinstonFachlerArrowAttribution(
    returns_investable_assets=asset_returns,
    complete_portfolio_weights=portfolio_weights,
    complete_benchmark_weights=benchmark_weights,
    date_column="date",
)
brinson.time_series_calculation()          # sets .df and .output_dict
brinson.attribution_plots()                # sets .brinston_fach_indexes, and draws its figure
```

| Attribute | What it holds |
| --- | --- |
| `.df` | the daily totals: `date`, `portfolio_returns`, `benchmark_returns`, `alpha`, `allocation`, `selection`, `interaction` |
| `.output_dict` | date to per-asset detail: `asset`, both weights, `returns_data`, both returns, `alpha` and the three effects |
| `.brinston_fach_indexes` | the cumulative sums — the series to quote. Set only by `attribution_plots()` |

**Read the effects the way the library defines them.** Its *Brinson-Fachler* methodology page
computes them **per asset and per date**: with `r` the asset's return, `r_b = w_b · r`, and
`alpha = w_p · r − r_b`, allocation is `(w_p − w_b) · r_b`, selection is `alpha · w_p`, and
interaction the remainder. That is not the textbook group-level split, so an *allocation* number is
not a sector bet unless the inputs were built as groups. Say which you mean when you quote one.

```python
factor_returns = load_by_factor_returns_arrow(
    path=factor_directory,
    available_factors=factor_file_names,
    portfolio_weights=portfolio_weights_entity,
)
factor_tables = {
    factor_name: factor.table
    for factor_name, factor in factor_returns.items()
}
factor_model = KNFMArrowAttribution(
    daily_portfolio_weights=portfolio_weights,
    by_factor_factor_returns=factor_tables,
    asset_returns=asset_returns,
    benchmark_returns=benchmark_returns,
    date_column="date",
)
factor_model.run()                         # sets .portfolio_attribution_ts and .simulated_rets
factor_model.calc_pct_area()               # sets .pct_df_returns
decomposition = factor_model.cummulative_pct_decomp()
```

`load_by_factor_returns_arrow` returns `FactorReturns` entities; the class wants their tables.
`.portfolio_attribution_ts` is the daily contribution per factor, `.simulated_rets` its cumulative
sum, `.pct_df_returns` the daily percentage split, and `cummulative_pct_decomp()` a dict: each
factor's share of total excess return at the last date. Tables are `pa.Table`; `.to_pandas()` at the
analysis boundary.

Note the names, none of which is a typo you may fix. The first cut is
**`Brinston`**`FachlerArrowAttribution` with `.brinston_fach_indexes`, while its method is
`brinson_fachler_model`; its constructor takes `returns_investable_assets` where the documented
interface spells it `returns_investible_assets`. **The factor model class is
`KNFMArrowAttribution`** — the documentation calls it `FactorModelArrowAttribution` throughout,
importing that name from `interfaces.factor_model_arrow_attribution` raises `ImportError` on 0.2.0,
and the worked example runs `KNFMArrowAttribution` from the same module.

Four things to know before quoting any of it:

- **The idiosyncratic residual has three spellings.** `f_idio_returns` is the column
  `calc_pct_area()` creates and `idio_returns` the key `cummulative_pct_decomp()` returns, as the
  API reference says; `f_idyo_returns` is the Analytics Factory's series, which the decomposition
  leaves out (section 3). Say which one a quoted number came from.
- **The percentage decomposition divides by the day's total return**, and the API reference says
  non-finite values are forward-filled. On days near zero the ratio explodes: read
  `.pct_df_returns` as a shape and quote `cummulative_pct_decomp()` for a number.
- **Everything is aligned to the intersection of every input's date range**, and the run logs it as
  `Aligned all tables to common date range`. One short factor file shortens the whole analysis;
  state the common range beside the backtest window. Ranges that do not overlap leave no data.
- `summary_stats(returns)`, in `modules.performance_functions`, gives the one-row frame the
  dashboard shows; the whole module is public, so a figure in a document can be recomputed from the
  series. `summary_stats` assumes 252 periods a year unless told otherwise; the annualising
  functions take `periods_per_year` and infer nothing.

## 7. The dashboard

With `factor_model_method` on and `launch_dashboard=True`, a Dash app is served on `dashboard_port`
(1–9999, typically 8050). **It needs the factor model**: with only Brinson-Fachler, static
matplotlib plots are what you get. `run_server` starts Dash's development server, which runs until
stopped, with `debug=True` by default.
Never launch it from an automated run, a scheduled job or a notebook you expect to finish: pass
`launch_dashboard=False` and read the tables.

## 8. Inside a KaxaNuk Strategy Template repository

Step 6 reads what step 5 produced, and `Experiments/attribution_analysis.py` shapes it:

- **The book's daily weights, not `Portfolio/portfolio_weights.csv`.** That file is the book on its
  rebalance dates, which the library rejects. Take the weights the engine actually held each trading
  day — `Daily_Weights` in its results, verified on engine 0.66.0 — and reshape them to one row per
  trading day with `date_column` first. Keep the cash position, drop the engine's benchmark column
  (it comes back at zero), and **widen them to every benchmark constituent at zero weight** (section
  3). The engine names only what was held, so the widening is a step of its own, and every added
  name needs a price series in the market-data directory. Then **hold the book and the index's
  holdings overnight** (section 3): both are struck at the close.
- **Reconcile the benchmark before any figure is read.** The first cut's `benchmark_returns`, mean
  daily times 252, against the index's own returns file over the same days. That file never enters
  the first cut, which is what makes it the check: weights paired with the day they already hold,
  members with no price and a book not widened each leave a clean-looking run and a gap here.
  **A zero price in the index's holdings reads as an infinite return**: in the worked example
  `RAI`, excluded from every book, was still in the index, so its `load_prices` reads a price of
  zero or below as none. Its notebook prints the gap beside the first cut; above a point a year,
  the blueprint's tolerance, its Verify raises and the gate's performance criterion P2 reads "not
  evidenced".
- **The benchmark's daily weights and its daily returns** belong to the experiment, not to the
  library's defaults, with the same density rule. A benchmark chosen after seeing the result is not
  a benchmark.
- **The Analytics Factory's files are read as it ships them** — KaxaNuk's Analytics Factory,
  which ships the benchmark and the factor model files attribution reads
  (<https://www.kaxanuk.mx/analytics>); ask `analytics@kaxanuk.mx` for them. `Data/hand_supplied.py`
  reads the index's holdings and returns under `Benchmark Portfolios/`, the factor model under
  `Factor Models/`, or under the older `Benchmarks/` and `Factors/`, in place from the folder
  `KN_ANALYTICS_PATH` names, or from the drop zones `Benchmarks/` and `Factors/` under
  `Data/Curator/`. It parses the Factory's `m_date` headers — ISO in the holdings, day first in
  the returns — and gives the model's own series their reserved names, `Market.csv` as `f_market`
  and so on. Never rename or re-head a Factory file by hand: a renamed copy drifts from the one the
  Factory refreshes.
- `Experiments/Experiment_N/Attribution/` is where output lands, and **nothing in it is committed**:
  no workbooks, no charts, no dashboards. The numbers reach `FINDINGS_N.md`, and `RESULTS.md` is
  compiled from those.
- **Record the factor set** — how many files, and their names — and the coverage line. Attribution
  numbers are only comparable across runs when the factor set is identical, and the file names *are*
  the factor set.

Then hand off. `alpha-decomposition` takes it from the tables: two layers and a third pass, and the
counterfactual books that say what the residual is made of.

## What this skill will not let you do

- **Pass a rebalance-only weight file** and work around the error it raises. The library is right;
  derive the daily book.
- **Pair a weight struck at a day's close with that day's return.** Hold it overnight; paired on
  the same day, it earns the day's move twice.
- **Quote an attribution whose benchmark does not reconcile** with the index's own returns file.
- **Quote a number this library did not produce.** The agent never computes an attribution figure
  itself; it shapes inputs, calls the library and reads tables back.
- **Report a factor split without its coverage.** The coverage line and the count of factor files
  travel with every attribution number.
- **Treat an empty `Output/` as a failed run.** It is what `main()` does; read the attributes
  instead.
- **Silently accept a shortened window.** The common date range is an output, and it is stated.
- **Use a live KaxaNuk strategy as a worked example.** Examples in this package come only from
  `golden-flow` as the package ships it, never from a live strategy repository.

## Where the documentation is

Base: `https://kaxanuk-attribution-analysis.readthedocs-hosted.com/en/latest/`, build **0.2.0**. Prefer
it whenever it and this file disagree — except where `references/api.md` names a place the
documentation and a run disagree. Read its pages, never the source pages they link to.

| Page | Path under the base |
| --- | --- |
| Quick start — install, licence key, project tree | `user_guide/quick_start.html` |
| Data formats — the four inputs, the pre-run checklist | `user_guide/end_user_manual/data_formats.html` |
| Configuration reference — every workbook row | `user_guide/end_user_manual/configuration.html` |
| Excel workflow | `user_guide/end_user_manual/excel_workflow.html` |
| Running from Python | `user_guide/end_user_manual/running_from_python.html` |
| Brinson-Fachler methodology — the per-asset formulas | `methodology/brinson_fachler.html` |
| Factor model methodology | `methodology/factor_model.html` |
| `main()` and `Configuration` in code | `api_reference/performance_attribution.html` |
| `BrinstonFachlerArrowAttribution` | `api_reference/attribution_methodologies/brinson_fachler.html` |
| The factor model class — `KNFMArrowAttribution` in a run — and the factor loader | `api_reference/attribution_methodologies/factor_model.html` |
| Weight entities — the daily-density rule | `api_reference/portfolio_data_pipeline/entities.html` |
| `ExcelConfigurator`, `Configuration` | `api_reference/portfolio_data_pipeline/configuration.html` |
| Metrics | `api_reference/metrics.html` |
| CLI | `api_reference/cli.html` |
| Dashboard | `api_reference/dashboard/core.html` |
| Release notes | `release_notes/v0/index.html` |
