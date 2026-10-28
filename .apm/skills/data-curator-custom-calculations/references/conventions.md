# Custom calculation conventions

The contract every `c_*` function must satisfy, and how to name it.

## 1. Function equals column

- A function `def c_foo(...)` defines an output column named `c_foo`. The column name **is** the
  function name.
- Only functions whose name starts with `c_` become columns: "Any function name not prefixed with
  `c_` will be ignored", says the documentation's Custom Calculator Workflow page. Anything else in
  the module is a private helper, so factor shared logic into normal functions freely.
- A `c_` function in a module passed in `custom_calculation_modules` becomes the column of its
  name, as the Custom Calculations page and the worked example's run show. The example's module is
  loaded from its file by path, under a name of the driver's own, and that works. A module built in
  memory, as a notebook might, is not checked by a run: see `programmatic-run.md`.
- Never name a custom function after one on the Features page: which of the two a run would use is
  not documented.

## 2. Parameters are injected by column name

Each parameter name must be the name of a column the curator can resolve, and it is filled with that
column's data as a `DataColumn`, as the Custom Calculations page says. See `input-columns.md` for
the tags and the documentation's lists of the valid names.

- Type hints follow the project's style. The documentation's own signatures carry none, and the
  worked example's quoted hints ran, so `def c_x(m_close)` works hinted or not, and a parameter is
  never renamed for readability: its name is the column. In a KaxaNuk strategy every parameter and
  the return are hinted, quoted, as in `template.py`.
- Dependencies resolve recursively: a `c_*` parameter is computed first, whether it is a built-in or
  another custom function. The Features page's `c_earnings_to_price` takes two `c_*` columns, and
  the worked example's `c_open_dividend_and_split_adjusted` takes its own `c_open` and
  `c_dividend_and_split_ratio`. A cycle stops the run with an error.
- The parameter named exactly `configuration` is special: it receives the `Configuration` instead
  of a column, as the page for `c_last_twelve_months_net_income` shows with `configuration.period`,
  and with it the other fields a caller sets: `.start_date`, `.end_date`, `.identifiers` and
  `.columns`. Use it when the maths depends on annual vs quarterly reporting.

## 3. Return value

- Return an iterable of the **same length as the inputs**, "preferably a `DataColumn`,
  `pyarrow.Array`", as the Custom Calculations page says; `DataColumn.load()` also takes a
  `pandas.Series`. The result is wrapped into a `DataColumn` automatically (the changelog, 0.8), so
  it can feed other calculations.
- Any operation that drops rows (a shift, a diff, a ratio against a lagged slice) must pad the
  missing leading positions with `None` to restore the length. See the shift-and-pad pattern in
  `data-column-api.md`.
- Undefined results must be `None`, never `inf` or `NaN`. `DataColumn` arithmetic returns null for
  any row where an operand is null — "any operation involving a null yields null", says the Custom
  Calculations page. The documentation says nothing of a zero denominator, though: guard it, or
  clean the result with `kaxanuk.data_curator.features.helpers.replace_infinite_with_none()`, which
  turns `inf` and `-inf` into null. When computing through `pyarrow.compute`, `numpy` or `pandas`
  directly, you own the cleanup, a `NaN` turned into `None` included.
- A rolling window of `n` rows leaves the first `n - 1` rows null — the Helpers page's
  `simple_moving_average` returns "None for initial elements until window is reached" — and `n`
  when the input's own first row is null, as log returns' is. Say so in the docstring.

## 4. Naming

Names must be a single `snake_case` identifier, prefixed with `c_`, descriptive enough to be
unambiguous in an alphabetically sorted list. The rules are the documentation's Feature Tag
Homogenization page's, in the order they are applied:

1. **Most relevant term first**, so sorted lists surface the concept:
   `c_exponential_moving_average_21d_close`, not `c_close_21d_exponential_moving_average`.
2. **Spell out elementary concepts** even when an acronym exists: `c_simple_moving_average_5d`, not
   `c_sma_5d`.
3. **Use standard acronyms for complex indicators** that are universally known that way:
   `c_rsi_14d`, `c_macd_26d_12d`.
4. **Encode the time parameter** as `<number><letter>` with `d` days, `w` weeks, `m` months, `y`
   years, placed after the descriptive phrase. Prefer days when feasible: `c_returns_20d` over
   `c_returns_4w`.
5. **State the price type** (`open`, `high`, `low`, `close`) when it distinguishes the feature,
   except for returns and for indicators that are almost always computed on the close (RSI, MACD),
   where `close` is implied and omitted.
6. **Append the adjustment** when the feature depends on adjusted prices: `_split_adjusted` or
   `_dividend_and_split_adjusted`, at the very end.

Examples from the built-in catalogue on the Features page:
`c_log_returns_dividend_and_split_adjusted`, `c_simple_moving_average_21d_close_split_adjusted`,
`c_annualized_volatility_63d_log_returns_dividend_and_split_adjusted`, `c_market_cap`,
`c_book_to_price`, `c_last_twelve_months_revenue_per_share`.

## 5. Documentation

Docstrings follow the project's style. In a KaxaNuk strategy they are prose without sections, as
its `AGENTS.md` says, and never repeat what the hints say: a one-line summary, the formula on a line
of its own, and why — the price basis, how many leading rows come out null. A project with no style
of its own can match the built-ins instead: the documentation's Docstrings, Tests, and Continuous
Integration page asks for NumPy-style docstrings, and each built-in's page shows `Parameters`,
`Returns` and a `Notes` section holding the formula. A docstring holding LaTeX or backslashes is a
raw string (`r"""`), so Python keeps the backslashes.

## 6. Fundamentals and the period

- Any dependency on `f_*`, `fbs_*`, `fcf_*`, `fis_*`, `d_*` or `s_*` means the run needs a provider
  for the fundamentals, dividends or splits block it comes from, in `data_block_providers` (the
  changelog, 0.50.0).
- Fundamental values are reported per filing, and on the daily rows each filing's values repeat:
  the Helpers page says period data carries "the same key and thus the same data" on every row.
  Design for that.
- The configured `period` (`annual` or `quarterly`) changes the values. When a formula only makes
  sense for one of them, branch on `configuration.period`, as the page for
  `c_last_twelve_months_net_income` describes its own: the rolling sum of four quarters for
  quarterly, the period's own value for annual. Raise an error of your own for any other value.

## 7. Composition

Prefer composing over recomputing: take `c_log_returns_dividend_and_split_adjusted` as a parameter
rather than recomputing log returns, and reuse the helpers of
`kaxanuk.data_curator.features.helpers` that the Helpers page lists for the heavy lifting
(`annualized_volatility`,
`exponential_moving_average`, `simple_moving_average`, `log_returns`, `relative_strength_index`,
`chaikin_money_flow`, `indexed_rolling_window_operation`, `replace_infinite_with_none`). Chaining is
explicitly encouraged: "Chain your functions to make them modular and testable", says the Custom
Calculations page.
