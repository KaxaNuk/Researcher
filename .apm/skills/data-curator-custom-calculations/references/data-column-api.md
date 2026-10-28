# DataColumn API

`DataColumn` wraps a `pyarrow.Array`, as the documentation's DataColumn page says. It is what every
calculation parameter receives, and the preferred return type. Its API reference is on that page:
<https://kaxanuk-data-curator.readthedocs.io/en/stable/api_reference/data_column.html>.

```python
import kaxanuk.data_curator.modules.data_column
```

The documentation names the class `kaxanuk.data_curator.modules.data_column.DataColumn`. KaxaNuk
code imports the module and writes the name qualified, as the patterns below do; the reference
lines shorten it to `DataColumn`.

## Null semantics

Any operation involving a null yields null, as the Custom Calculations page says: **any row where an
operand is null comes out null**. That is the main reason to stay in `DataColumn` arithmetic rather
than dropping to raw arrays — you get the correct missing-data behaviour for free. The
documentation does not say what a zero denominator gives, so guard it or clean the result, and when
you drop down to `pyarrow.compute`, `pandas` or `numpy`, you own that cleanup.

## Operators

`+`, `-`, `*`, `/`, `//`, `%` and the comparisons `==`, `!=`, `<`, `<=`, `>`, `>=` all work
element-wise between two `DataColumn`s or between a `DataColumn` and a number, in either order
(`3 + column` works too), each returning a new `DataColumn`, a boolean one for a comparison. Unary
minus came in the changelog's 0.26; unary plus did not, as that release left it unimplemented.

```python
return m_close_split_adjusted * fis_weighted_average_diluted_shares_outstanding   # market cap
return m_close_split_adjusted - m_open_split_adjusted                             # daily range
return c_last_twelve_months_net_income / c_market_cap                             # earnings to price
```

The first and the last are built-ins already, `c_market_cap` and `c_earnings_to_price` on the
Features page: they show the arithmetic, and in practice are reused.

A division involving decimal columns returns float64 (the changelog, 0.38), and one between integer
columns returns float (0.43.0). The worked example's prices arrive as fixed-point decimals.

**A sparse column reaches pandas whole through a plain list.** In the worked example's runs on
0.51.0, a dividend column — a value on its ex-date, null elsewhere — converted through its
Arrow-backed pandas Series handed back its values alone; `column.to_pyarrow().to_pylist()`, then
`pandas.to_numeric`, kept every row. Its `c_*` calculations read every input that way, as floats,
and hand each result back through `DataColumn.load()` with any non-finite value made null.

## Conversions and inspection

```python
column.to_pyarrow()             # -> pyarrow.Array, for pyarrow.compute
column.to_pandas()              # -> pandas.Series backed by Arrow, for rolling/ewm/shift
column.type                     # -> pyarrow.DataType
column.is_null()                # -> True if the underlying array is a NullArray, wholly null
DataColumn.load(data, dtype=None)       # wrap a pyarrow.Array, a pandas.Series or another iterable
DataColumn.concatenate(*columns, separator='', null_replacement='')   # string-join columns element-wise
DataColumn.equal(column1, column2, approximate_floats=False, equal_nulls=False)
DataColumn.boolean_and(*columns)        # combine boolean columns; boolean_or likewise
```

`DataColumn.load()` is the canonical way to build the return value.
`DataColumn.concatenate()` is how composite keys are built, for example joining `f_fiscal_year` and
`f_fiscal_period` into one period key.

## Pattern A — shift and pad with pyarrow

Lag through `to_pyarrow()` and pyarrow's own slicing, then restore the length by prepending as many
`None`s as rows the shift consumed. The worked example casts its decimal prices to float once, at
the boundary, before anything statistical:

```python
import pyarrow
import pyarrow.compute

import kaxanuk.data_curator.features.helpers
import kaxanuk.data_curator.modules.data_column

prices = m_close_dividend_and_split_adjusted.to_pyarrow()
float_prices = prices.cast(pyarrow.float64())
# P_t, from the 22nd row on, and P_{t-21}, both N - 21 rows long.
current = float_prices.slice(21)
earlier = float_prices.slice(
    0,
    len(float_prices) - 21,
)
ratio = pyarrow.compute.divide(
    current,
    earlier,
)
momentum = pyarrow.compute.subtract(
    ratio,
    1,
)
padding = pyarrow.array(
    [None] * 21,
    type=momentum.type,
)
output = pyarrow.concat_arrays([
    padding,
    momentum,
])
output_column = kaxanuk.data_curator.modules.data_column.DataColumn.load(output)

return kaxanuk.data_curator.features.helpers.replace_infinite_with_none(output_column)
```

## Pattern B — pandas

`pandas` pads the leading rows itself, so lengths take care of themselves:

```python
series = m_close_dividend_and_split_adjusted.to_pandas()
result = series.rolling(21).mean()

return kaxanuk.data_curator.modules.data_column.DataColumn.load(result)
```

Make sure those leading rows reach the output as nulls, not `NaN`: the documentation does not say
how `load()` converts them.

## Pattern C — clean up non-finite results

Whenever a formula leaves `pyarrow`'s or `pandas`' own null handling, funnel the result through the
helper. In practice this very formula is the built-in `c_log_difference_high_to_low`, on the
Features page, to reuse; it is shown here for the helper:

```python
import kaxanuk.data_curator.features.helpers

rebased = m_high / m_low
result = pyarrow.compute.ln(
    rebased.to_pyarrow()
)
result_column = kaxanuk.data_curator.modules.data_column.DataColumn.load(result)

return kaxanuk.data_curator.features.helpers.replace_infinite_with_none(result_column)
```

## Helpers worth reusing

From `kaxanuk.data_curator.features.helpers`, as the Helpers page lists them, one page each, all
keyword-only unless noted. Each raises `CalculationHelperError` when given something other than a
`DataColumn`, or a window that is not a positive integer, as its page says.

| Helper | Purpose |
|---|---|
| `annualized_volatility(*, column, days)` | rolling standard deviation, annualized; the `c_annualized_volatility_*` pages give σ × √252 |
| `exponential_moving_average(*, column, days)` | EMA with a `2 / (days + 1)` smoothing factor, reset on missing data |
| `simple_moving_average(column, days)` | rolling mean, `None` until the window fills |
| `log_returns(column)` | `ln(P_t / P_{t-1})`, first row `None` |
| `relative_strength_index(*, column, days)` | RSI |
| `chaikin_money_flow(*, high, low, close, volume, days)` | CMF |
| `indexed_rolling_window_operation(*, key_column, value_column, operation_function, window_length)` | rolling window over the *unique* keys, repeating the result on duplicate keys — the way to do last-twelve-months maths on filing data repeated across days. Each key must occupy one contiguous block of rows, or it raises (the changelog, 0.50.0) |
| `replace_infinite_with_none(column)` | turn `inf` / `-inf` into null |
