# Backtest Engine — the public surface

Taken from the official documentation on 2026-09-06, the `main()` section from a run of **0.66.0**
on 2026-09-17, and the `Configuration` and batch sections from the worked example's code, run on
**0.67.0** on 2026-10-24 (Golden Flow 0.17.0) — never from the engine's code. Where a page could not
be reached, this file says so rather than guessing: **an invented signature is worse than a missing
one.** The URLs are at the end of `SKILL.md`.

## `main()` — the whole run, verified on 0.66.0

```python
kaxanuk.backtest_engine.main(
    *,
    configuration: Configuration,
    input_handlers: list[InputHandlerInterface],
    portfolio_handlers: list[PortfolioInputHandlerInterface],
    logger_level: int = 20,
    logger_format: str = "[%(levelname)s] %(message)s",
    logger_file: str | bytes | os.PathLike | None,
    launch_dashboard: bool,
    dashboard_port: int,
) -> BacktestResult
```

`logger_file`, `launch_dashboard` and `dashboard_port` are keyword-only with no defaults.
`kaxanuk.backtest_engine.load_config_env(env_path)` reads the licence from a `Config/.env`, which is
how a notebook keeps the key out of its own source. `BacktestResult` carries `success`, `error` and
`data`; the keys of `data`:

| Key | What it holds |
| --- | --- |
| `Register_df` | `Portfolio_Value`, `Total_Portfolio_Value`, `Returns`, indexed by the days the engine **valued** |
| `Daily_Weights` | the drifted book, one row per valued day: the holdings, the benchmark and `CASH_RESERVE` — **what step 6 reads** |
| `Shares_df`, `orders_df`, `portfolio_df` | share counts and orders per rebalance date, and the weight file as it was read |
| `Commission_df`, `Slippage_df`, `Execution_costs_df`, `Total_commissions`, `Total_slippage_costs` | what the trading cost |
| `Financing_df`, `Total_financing_costs`, `Risk_free_rate` | borrow, margin and cash interest |
| `Forced_liquidations_df` | positions the engine had to exit, with the reason |
| `benchmark`, `benchmarks`, `benchmark_stats`, `benchmarks_stats` | the comparison arm |
| `portfolio_stats` | `Start Balance`, `End Balance`, `Net Return`, `PnL`, `Annualized Return (CAGR)`, `Annualized Volatility` and the rest; the keys a strategy quotes are below |
| `start_date`, `end_date`, `years`, `initial_portfolio_value`, `final_total_portfolio_value` | **the window actually valued**, and the balances |

`start_date`, `end_date` and `years` describe what was valued, not what was configured. Compare them
with the configured window before quoting a metric: a run that stopped partway still returns
`success=True` with `error=None` (see `SKILL.md`, section 6). **On 0.67.0, from its changelog:** a
licence that does not validate comes back as `success=False` with the licence error, checked before
any data is read; 0.66.0 raised it instead.

**The keys a strategy quotes**, as the worked example's
`Experiments/Experiment_1/experiment_1_marimo.py` reads them from `portfolio_stats` for
`Backtest/summary.csv`, each with `.get`: `Annualized Return (CAGR)`, `Annualized Volatility`,
`Portfolio Sharpe Ratio`, `Portfolio Sortino Ratio`, `Max Drawdown`, `Alpha`, `Information Ratio`,
`Total Commissions`, `Total Slippage Costs` and `Total Financing Costs`, and `Risk_free_rate` from
the result itself. A single run's `benchmarks_stats` holds one entry per benchmark under the same
first five names; a batch returns none (*The batch mode* below).

**What those figures are defined as is only partly verified here.** With `financing_benchmark_rate`
set, the worked example's findings read `Risk_free_rate` as the rate file averaged over the window
— 2.04% for FRED's `DFF` over 2000–2026 — and every Sharpe ratio as excess of it, on 0.67.0. How
many periods a year each annualised figure assumes is not established by any run or page this file
was taken from. `compute_portfolio_statistics`, in *The `metrics` module* below, defaults to
`risk_free_rate=0.0` and `periods_per_year=252`, and the worked example calls it with the run's
`years` and `Risk_free_rate` to measure the benchmarks of a batch; nothing here shows that it is
what fills `portfolio_stats` or the Excel report. Do not state any other definition for a quoted
figure until one is read from the engine's documentation or checked against a run.

## `entities.Configuration` and the input handlers, as the worked example calls them

Read from the worked example's `Experiments/backtest_engine.py`, run on **0.67.0** on 2026-10-24.
These are the keyword arguments it passes, not the full signature: a field it does not set is not
listed, and nothing here says what its default is.

| Field | The example's value | What it decides |
| --- | --- | --- |
| `initial_capital` | `1_000_000`; `100_000` in the small-account row | the starting cash |
| `start_date`, `end_date` | `datetime.date` | the window asked for; compare with `data["start_date"]` and `data["end_date"]` after the run |
| `cash_reserve_percentage` | `0.01` | cash held back to pay for a rebalance; `0` truncates the run (`SKILL.md`, section 6) |
| `commission_model` | `"basis_points"` | commission as a share of the notional traded |
| `commission_basis_points` | `1.0`; `5.0` in the stress row | the commission rate, in basis points |
| `commission_cents` | `0.0` | required whatever the model — a `TypeError` without it, on 0.66.0 — and unused with basis points |
| `slippage_model` | `"spread_plus_impact"`; `"basis_points"` in the flat and stress rows | a half-spread from the day's range plus square-root impact from its volume, or a flat half-spread |
| `slippage_basis_points` | `5.0`; `10.0` in the stress row | the half-spread where a day's range is missing, or the flat half-spread |
| `spread_estimator` | `"corwin_schultz"` | the spread estimate from the day's high and low; the engine's other, Abdi–Ranaldo, also reads the close |
| `user_column_high`, `user_column_low`, `user_column_close` | `"m_high_split_adjusted"`, `"m_low_split_adjusted"`, `"m_close_split_adjusted"` | the range the spread is estimated from: a ratio, so split-adjusted prices give the tape's estimate |
| `user_column_volume` | `"c_volume_dividend_and_split_adjusted"` | the volume impact is read from, on the fill's basis |
| `financing_benchmark_rate` | `"DFF"` | the rate the cash earns: a file of that name in the market-data directory, its last observation on or before each day; also the risk-free rate of the Sharpe ratios |
| `cash_interest_spread` | `-0.005` | what the broker keeps below that rate |
| `market_data_input_format`, `portfolio_input_format` | `"csv"` | the format of each input |
| `input_market_data_directory` | `Data/Curator/Engine`, as a `str` | one `{TICKER}.csv` per security, the benchmarks' and the rate file included: a CSV copy of the columns the engine reads (`SKILL.md`, section 6) |
| `input_portfolio_directory` | `Experiments/Experiment_N/Portfolio`, as a `str` | where the weight file is |
| `portfolio_name` | `"portfolio_weights"` | the weight file's name, without `.csv` |
| `benchmark_file_name` | `"KN_US_Equity_Core,SPY"` | the benchmarks' price files in the market-data directory, without `.csv`, as one comma-separated name; every alpha and information ratio is measured against the first |
| `backtest_results_output_directory` | `Experiments/Experiment_N/Backtest`, as a `str` | where the results land |
| `user_column_date` | `"m_date"` | the date column |
| `user_column_commission_price` | `"c_open"` | the price a ticket is written in: **unadjusted** |
| `user_column_trade_execution_price` | `"c_open_dividend_and_split_adjusted"` | the fill, the next day's open, on the total-return basis |
| `user_column_mark_to_market_price` | `"c_close_dividend_and_split_adjusted"` | the daily valuation, on the total-return basis |
| `rebalance_date_handling` | `"next_trading_day"` | a rebalance date that is not a trading day moves to the next one |
| `delisted_position_handling` | `"sell_at_last_price"` | a position whose prices stop is sold at its last price, booked that day: no day of hindsight |

`commission_model` and `slippage_model` here are strings; the `PyArrowBacktester` arguments of the
same names take model objects. The input handlers each take a directory as a `str`, and `main()`
and `create_from_configuration` take each in a one-item list:

```python
import kaxanuk.backtest_engine.input_handlers

csv_input = kaxanuk.backtest_engine.input_handlers.CsvInput(
    input_dir=market_data_directory,
)
csv_portfolio_input_handler = kaxanuk.backtest_engine.input_handlers.CsvPortfolioInputHandler(
    portfolio_directory,
)
```

## The batch mode — `MultiPortfolioBacktester`

As the worked example's `price_batch` calls it, run on **0.67.0**: one load of the market data for
every book of a batch that shares all its settings but its weights.

```python
import kaxanuk.backtest_engine.backtest
import kaxanuk.backtest_engine.config_handlers
import kaxanuk.backtest_engine.input_handlers.csv_input

batch_configuration = kaxanuk.backtest_engine.config_handlers.BatchConfigParser.parse_dict({
    "global_defaults": defaults,
    "portfolios": [
        {"name": portfolio_name, "inline_weights": inline_weights},
    ],
    "output": {
        "directory": output_directory,
        "batch_name": "batch",
        "ranking_metric": "sharpe_ratio",
    },
})
market_data = kaxanuk.backtest_engine.input_handlers.csv_input.CsvInput(
    input_dir=market_data_directory,
)
backtester = kaxanuk.backtest_engine.backtest.MultiPortfolioBacktester(
    input_handlers=[market_data],
    portfolio_handlers=[],
)
results = backtester.run(batch_config=batch_configuration)
```

- **`global_defaults`** is the `Configuration`'s fields as plain values: numbers as floats — the
  configuration holds some as PyArrow decimals and the parser compares them as floats — settings as
  strings rather than enums, dates in ISO form, and `initial_capital` as an integer.
- **`inline_weights`** maps each rebalance date to its identifiers and their non-zero weights, so
  no portfolio file is read and `portfolio_handlers` is empty; a name absent on a date is held at
  zero.
- **`results["entries"]`**, one per book: `name`, `success`, `error_message` when it failed, and
  `result`, a dict with the keys of a single run's `data` — `Register_df`, `Daily_Weights`,
  `orders_df`, `Commission_df`, `Slippage_df`, `Execution_costs_df`, `Financing_df`,
  `portfolio_stats`, `Risk_free_rate`, `start_date`, `end_date`, `years` — and `benchmarks`, each
  benchmark's daily table with `date_column`, `bench_value` and `daily_return`. **There are no
  benchmark statistics**: the example computes them with
  `kaxanuk.backtest_engine.modules.metrics.compute_portfolio_statistics` over that series, on the
  book's window, `years` and `Risk_free_rate`.
- **The engine draws its report's charts into a file of one fixed name in the working folder**, so
  the example runs each batch, and each single run, from a temporary folder of its own after
  loading the licence with `load_config_env(<path to Config/.env>)`.

## `PyArrowBacktester`

Module: `kaxanuk.backtest_engine.backtest.pyarrow_backtester`. Base: `BaseBacktesterInterface`.

```python
PyArrowBacktester(
    *,
    configuration: Configuration,
    market_data_bundle: MarketDataBundlePyarrow,
    portfolio_dict: dict[Timestamp, dict[str, float]],
    benchmark: Table | None,
    portfolio_df: DataFrame | None = None,
    commission_model: CommissionModelInterface | None = None,
    slippage_model: SlippageModelInterface | None = None,
    benchmarks: dict[str, Table] | None = None,
)
```

Keyword-only. In practice it is built through one of the two class methods rather than directly:

```python
@classmethod
create_from_configuration(
    configuration: Configuration,
    input_handlers: list[InputHandlerInterface],
    portfolio_handlers: list[PortfolioInputHandlerInterface],
    commission_model: CommissionModelInterface | None = None,
    slippage_model: SlippageModelInterface | None = None,
) -> PyArrowBacktester
```

```python
@classmethod
create_from_pipeline_result(
    configuration: Configuration,
    pipeline_result: DataPipelineResult,
    commission_model: CommissionModelInterface | None = None,
    slippage_model: SlippageModelInterface | None = None,
) -> PyArrowBacktester
```

Run it:

| Method | Returns |
| --- | --- |
| `run()` | `BacktestResultDict` |
| `run_with_benchmark()` | `BacktestResultDict`, with the comparison arm |

Properties on the instance: `execution_broker` (`ExecutionBroker`), `portfolio_manager`
(`PortfolioStateManager`), `rebalance_dates` (`list[Timestamp]`), `reporting_engine`
(`ReportingEngine`), `tickers` (`list[str]`).

## The `metrics` module

Public, so a figure quoted in a document can be recomputed from the returned series instead of
copied out of a cell.

**Return and risk**

| Function | Returns |
| --- | --- |
| `annualize_rets(r, periods_per_year=252)` | `float` — `(1 + r).prod() ** (periods_per_year / n_periods) - 1` |
| `annualize_vol(r, periods_per_year=252)` | `float` — `r.std() * sqrt(periods_per_year)` |
| `calculate_annualized_return(initial_value, final_value, years)` | `float` — CAGR |
| `compound(r)` | `float` — `expm1(log1p(r).sum())` |
| `sharpe_ratio(r, riskfree_rate, periods_per_year=252)` | `float` |
| `sortino_ratio(r, riskfree_rate=0.0, target_return=None, periods_per_year=252)` | `float` |
| `sortino_ratio_simple(r, riskfree_rate=0.0, periods_per_year=252, use_log_returns=False)` | `float` |
| `downside_deviation(r, target_return=0.0, periods_per_year=252)` | `float` |
| `var_historic(r, level=5)` | `float` or `pd.Series` |
| `var_gaussian(r, level, modified)` | `float` — Cornish-Fisher when `modified` |
| `cvar_historic(r, level=5)` | `float` or `pd.Series` |
| `tracking_error(portfolio_returns, benchmark_returns, periods_per_year=252, annualized=True)` | `float` |
| `information_ratio(portfolio_returns, benchmark_returns, periods_per_year=252)` | `float` |
| `skewness(r)` / `kurtosis(r)` | `float` — population, kurtosis not excess |
| `drawdown(return_series)` | `pd.DataFrame` — Wealth, Previous Peak, Drawdown |

**Series and tables**

| Function | Returns |
| --- | --- |
| `index_price_construction(daily_portfolio_returns, base=1000)` | `pd.Series` |
| `wealth_index(returns, initial_capital)` | `pd.Series` |
| `analyze_annual_returns(df, portfolio_column, strategy_name, method='simple', min_observations=2)` | `pd.DataFrame` |
| `calculate_yearly_returns(series, strategy_name, method, min_observations, annualize=True, trading_days_per_year=252)` | `list[dict]` |
| `calculate_daily_returns(price_array)` | `pa.Array` |
| `calculate_pct_change(price_array)` | `pa.Array` |
| `calculate_returns_table(price_table, date_column_name)` | `pa.Table` |
| `decimal_cumprod_pyarrow(returns_array)` | `pa.Array` |
| `pct_change_pyarrow(column, output_column_name, table, periods=1)` | `pa.Table` |

**Composite and plots**

`compute_portfolio_statistics(initial_capital, initial_portfolio_value, final_portfolio_value,
returns, total_portfolio_series, years, risk_free_rate=0.0, var_level=5.0, periods_per_year=252,
benchmark_returns=None, additional_metrics=None)` returns `dict[str, float]` — performance, risk and
distribution metrics in one call.

`annual_returns_plot(...)` and `active_returns_plot(...)` return a `matplotlib.figure.Figure`.
**A KaxaNuk Strategy Template repository commits no charts**, so these are for looking at, not for
saving into the tree.

## CLI

```
uv run python -m kaxanuk.backtest_engine [--version] COMMAND [ARGS]...
```

| Subcommand | Arguments and options |
| --- | --- |
| `autorun` | installs missing project files on the first run, then executes the entry script |
| `init CONFIG_FORMAT` | `excel`; `--entry_script <name>` changes the generated entry script (default `__main__.py`) |
| `run [ENTRY_SCRIPT_LOCATIONS]...` | paths to entry scripts or directories |
| `update CONFIG_FORMAT` | `excel` or `entry_script` — refresh a template |

The quick start also documents `kaxanuk.backtest_engine init excel` as the first command after
installing, and `python -m kaxanuk.backtest_engine.services.cli autorun` as the run command. Treat
the module-level form above as current and the services path as the older spelling; confirm against
the installed build's `--version` before writing either into a project.

## Named in the documentation but not verified here

These appear in the API overview, but their signature pages could not be retrieved. **Read the
component pages before calling them; do not infer a signature from the name.**

- `MultiPortfolioBacktester.generate_individual_reports` — under Backtest Components, Orchestrators.
  `MultiPortfolioBacktester(...).run(batch_config=...)` is run above; its other methods are not.
- `arrow_to_pandas_for_analysis()` — the helper that turns returned PyArrow tables into pandas.
- Cost models, execution, interfaces and enums — Backtest Components lists them as Commission,
  slippage and trading-record models; portfolio state, trade broker and reporting engine; abstract
  interfaces for backtesters and cost models; and trading enums for order side, price type and
  rebalance status.
- Portfolio Data Pipeline: portfolio configuration service, transformer, helpers and date utilities.

## Inputs, in one place

| Input | Shape |
| --- | --- |
| Portfolio, horizontal | first column `Ticker`; one column per rebalancing date |
| Portfolio, vertical | first column `date`; one column per ticker |
| Market data | `{TICKER}.csv` or `{TICKER}.parquet`; a date column plus at least three price columns, roles mapped in the configuration |
| Dates | `YYYY-MM-DD` |
| Configuration | `Config/backtest_engine_parameters.xlsx`; in code an `entities.Configuration` (see above), or a dict or YAML |
| Licence | `Config/.env` — `KNBE_API_KEY_KAXANUK`, the only key the engine reads. `KNPC_API_KEY_KAXANUK` is Portfolio Construction's licence since its 2.0.0, not a spelling of this one: never rename one into the other |
