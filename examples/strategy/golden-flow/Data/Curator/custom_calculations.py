"""
The `c_*` columns -- step 3 of 8, computed by the Data Curator while it downloads.

`c_*` means one security's own history and nothing else.  The Curator works one identifier at a
time, so anything that compares securities against each other belongs one stage later, in
`Data/Refinery/custom_calculations.py`, as an `r_*` column.

What is expected here is one function per column, named exactly as the column:

- Each function's parameters are named after the columns it reads -- a provider column, a dividend
  or split column, or another `c_*` column.  The Curator resolves the dependency order from the
  signatures, so the order of definition here does not matter.
- Each returns a column of the same length.  Prices arrive as fixed-point decimals; anything
  statistical casts to float once, at the boundary, and a value that is not finite is returned as
  a null.
- A column is registered by listing it among the output columns `Data/curator.py` requests.
  Nothing else registers it.
- Never give a column the name of one the library ships: which of two functions of one name a run
  uses is not documented, so a column of your own carries a name of its own.

The minimum a backtest needs -- and the first two are never removed:

- the cumulative split ratio and the dividend-and-split ratio, the factors between the day's quoted
  price and the split-adjusted and total-return series;
- the total-return close every signal, return and mark reads, and its one-day return, because
  nearly every feature is built on it;
- the price a book is filled at, unadjusted for the order ticket and on the total-return basis for
  the fill;
- the day's traded value, because capacity is a question every strategy has to answer, checked
  and corrected across every split: volume can arrive adjusted twice.

**Where the provider rounds its adjusted prices**, the ratios and the total-return close are
rebuilt here from the exact unadjusted close and the provider's own dividends and splits, read
through the joined column names the Curator writes for them.  A split after the requested window
is already in the provider's split-adjusted prices and dividends but not in the window's split
columns: take the constant between the two bases from the provider's own split-adjusted close, so
the rebuilt price, the provider's volume and its dividends stay on one basis.

Widening the schema changes every file's header, so the next run refetches every identifier.  That
is intended, because it is what stops the folder holding a mix of schemas, and it makes this the
wrong home for anything you intend to tune.  Put a model's frozen arithmetic inputs here and the
model itself in the Refinery: a sweep must never cost a download, and a new experiment's signal on
the data already downloaded is an `r_*` column, never a new `c_*` one.

It produces the `c_*` columns in every file under `Data/Curator/Time_Series/`.

It prevents a feature computed on a price basis it should not use -- a plausible number and no
error.
"""

# --- example: begin ---

# **Sharadar rounds every price to three decimals, its adjusted ones included,** and only its
# unadjusted close is exact: on 1998-01-02 its AAPL rows read a close of 16.25, a split-adjusted
# close of 0.145 and an adjusted close of 0.121, a series that can only move in steps of 0.8%.  So
# the adjustment is rebuilt here from the exact close and the provider's own dividends and splits,
# read through their joined column names -- `d_ex_dividend_date_dividend_split_adjusted` (cash a
# share, in today's split-adjusted shares, on its ex-date) and `s_split_date_numerator` /
# `s_split_date_denominator` (new shares to old, on the split's date).
#
# **A split after the requested window is in Sharadar's split-adjusted prices and dividends, but not
# in the window's split columns** (NFE's 1-for-50 of 2026-09-14), and one security's split-adjusted
# prices carry a factor no split records at all (NVTP).  Both are a constant between Sharadar's
# basis and the window's splits, taken from Sharadar's own split-adjusted close over the exact
# close, so the rebuilt price, Sharadar's volume and its dividends stay on one basis.
# `Data/curator.py` checks every file against Sharadar's adjusted close where its decimals allow.
#
# **Sharadar's volume is adjusted twice at some splits**: traded value steps by the split's own
# factor while the shares the tape printed do not move.  `c_traded_value` divides the earlier volume
# by that factor where both hold.
#
# The columns, and why each exists:
#
# - `c_split_ratio` and `c_dividend_and_split_ratio`, the factors between the day's quoted price and
#   the split-adjusted and total-return series;
# - `c_close_dividend_and_split_adjusted`, the total-return close every signal, return and mark
#   reads, and `c_log_returns_total`, its one-day log return;
# - `c_open` and `c_open_dividend_and_split_adjusted`, the next day's open a book is filled at,
#   unadjusted for the order ticket and on the total-return basis for the fill;
# - `c_traded_value`, the day's dollars traded, and `c_volume_dividend_and_split_adjusted`, the
#   volume in the shares of the fill's basis, which the engine's market impact divides by.
#
# The library ships `c_daily_traded_value` and `c_log_returns_dividend_and_split_adjusted` of its
# own, read from columns Sharadar leaves empty or rounds, and which of two functions of one name a
# run uses is not documented; so these carry names of their own.

import numpy
import pandas

import kaxanuk.data_curator

__all__ = [
    "c_close_dividend_and_split_adjusted",
    "c_dividend_and_split_ratio",
    "c_log_returns_total",
    "c_open",
    "c_open_dividend_and_split_adjusted",
    "c_split_ratio",
    "c_traded_value",
    "c_volume_dividend_and_split_adjusted",
]

# Where Sharadar's three decimals are fine enough to read its split basis from: a split-adjusted
# close of ten dollars or more, a rounding of five parts in a hundred thousand.
BASIS_PRICE_FLOOR = 10.0
# A basis more than this far from the window's own splits is a factor the window does not record.
BASIS_TOLERANCE = 0.02
# Volume adjusted twice for a split: traded value steps by the split's own factor, within this in
# logs, while the shares traded move by less than the next, over this many days on each side; and
# only a split of five shares for four or more is read.
SPLIT_SHARES_TOLERANCE = 0.15
SPLIT_SIGNATURE_TOLERANCE = 0.10
SPLIT_SMALLEST_LOG_FACTOR = 0.2
SPLIT_WINDOW_DAYS = 30


def c_close_dividend_and_split_adjusted(
    m_close: "kaxanuk.data_curator.DataColumn",
    c_split_ratio: "kaxanuk.data_curator.DataColumn",
    d_ex_dividend_date_dividend_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The total-return close, compounded back from the last day, where it equals the exact close.

    The split-adjusted close is the exact close times the split ratio.  A dividend, or the cash
    value of a spin-off, is paid in today's split-adjusted shares on its ex-date, so a day's total
    return is the split-adjusted close plus what was paid, over the day before's.
    """
    split_adjusted_close = _floats(m_close) * _floats(c_split_ratio)
    paid = _floats(d_ex_dividend_date_dividend_split_adjusted).fillna(0.0)
    gross_return = (split_adjusted_close + paid) / split_adjusted_close.shift(1)
    clean_return = gross_return.where(
        numpy.isfinite(gross_return) & (gross_return > 0),
        1.0,
    )
    log_return = numpy.log(clean_return.to_numpy())
    log_after = numpy.append(
        numpy.cumsum(log_return[::-1])[::-1][1:],
        0.0,
    )
    total_return_close = split_adjusted_close.iloc[-1] * numpy.exp(-log_after)

    return _column(pandas.Series(total_return_close))


def c_dividend_and_split_ratio(
    c_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
    m_close: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The factor between the day's quoted close and the total-return series.
    """
    ratio = _floats(c_close_dividend_and_split_adjusted) / _floats(m_close)

    return _column(ratio)


def c_log_returns_total(
    c_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The one-day log total return, null on the first day.
    """
    close = _floats(c_close_dividend_and_split_adjusted)
    log_return = numpy.log(close / close.shift(1))

    return _column(log_return)


def c_open(
    m_open_split_adjusted: "kaxanuk.data_curator.DataColumn",
    c_split_ratio: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The unadjusted open, which Sharadar publishes only split-adjusted, at three decimals.

    Dividing by the split ratio puts it back in the day's own share terms; the three decimals stay.
    """
    unadjusted_open = _floats(m_open_split_adjusted) / _floats(c_split_ratio)

    return _column(unadjusted_open)


def c_open_dividend_and_split_adjusted(
    c_open: "kaxanuk.data_curator.DataColumn",
    c_dividend_and_split_ratio: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The open on the total-return basis, the price a fill is booked at.

    No dividend goes ex between a day's open and its close, so the two share the day's factor.
    """
    adjusted_open = _floats(c_open) * _floats(c_dividend_and_split_ratio)

    return _column(adjusted_open)


def c_split_ratio(
    m_close: "kaxanuk.data_curator.DataColumn",
    m_close_split_adjusted: "kaxanuk.data_curator.DataColumn",
    s_split_date_numerator: "kaxanuk.data_curator.DataColumn",
    s_split_date_denominator: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The split-adjusted close over the exact close, from the splits themselves, never the rounding.

    The factor on a day is one over the product of every later split's ratio; Sharadar's basis --
    its split-adjusted close over the exact close, on the days its decimals are precise -- supplies
    the constant the window's own splits do not record.
    """
    numerator = _floats(s_split_date_numerator)
    denominator = _floats(s_split_date_denominator)
    ratio_on_row = (numerator / denominator).where(
        numerator.notna() & denominator.notna() & (denominator > 0),
        1.0,
    )
    ratios = ratio_on_row.to_numpy()
    splits_from_here = numpy.cumprod(ratios[::-1])[::-1]
    splits_from_window = numpy.append(
        splits_from_here[1:],
        1.0,
    )
    close = _floats(m_close).to_numpy()
    provider_split_close = _floats(m_close_split_adjusted).to_numpy()
    provider_factor = close / provider_split_close
    precise_rows = provider_split_close >= BASIS_PRICE_FLOOR
    compared_rows = precise_rows if precise_rows.any() else numpy.isfinite(provider_factor)
    factor_ratio = provider_factor[compared_rows] / splits_from_window[compared_rows]
    median_ratio = numpy.nanmedian(factor_ratio) if compared_rows.any() else 1.0
    basis_gap = float(median_ratio)
    basis_correction = basis_gap if abs(basis_gap - 1.0) > BASIS_TOLERANCE else 1.0
    splits_after = splits_from_window * basis_correction

    return _column(pandas.Series(1.0 / splits_after))


def c_traded_value(
    m_close: "kaxanuk.data_curator.DataColumn",
    c_split_ratio: "kaxanuk.data_curator.DataColumn",
    m_volume_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The dollars traded that day, with the volume Sharadar adjusted twice at a split corrected.

    The split-adjusted close times the split-adjusted volume is the day's dollars, whatever splits
    came later.  Where a split's 30 days after carry traded value stepped by the split's own factor
    while the shares the tape printed stay flat, the volume before it was already in the new shares
    and adjusted again, and every earlier day's is divided by the factor.
    """
    split_ratio = _floats(c_split_ratio)
    split_adjusted_close = _floats(m_close) * split_ratio
    volume = _floats(m_volume_split_adjusted)
    traded_value = (split_adjusted_close * volume).to_numpy()
    shares = (volume * split_ratio).to_numpy()
    factors = split_ratio.to_numpy()
    fix = numpy.ones(len(traded_value))
    factor_change = factors[1:] / factors[:-1]
    split_rows = numpy.flatnonzero(numpy.abs(factor_change - 1.0) > 0.01) + 1

    for row in split_rows:
        if row < SPLIT_WINDOW_DAYS or row + SPLIT_WINDOW_DAYS > len(traded_value):
            continue

        split_factor = float(factors[row - 1] / factors[row])

        if split_factor <= 0 or abs(numpy.log(split_factor)) < SPLIT_SMALLEST_LOG_FACTOR:
            continue

        value_before = numpy.nanmedian(traded_value[row - SPLIT_WINDOW_DAYS:row] * fix[row - 1])
        value_after = numpy.nanmedian(traded_value[row:row + SPLIT_WINDOW_DAYS])
        shares_before = numpy.nanmedian(shares[row - SPLIT_WINDOW_DAYS:row] * fix[row - 1])
        shares_after = numpy.nanmedian(shares[row:row + SPLIT_WINDOW_DAYS])
        measured = value_before > 0 and value_after > 0 and shares_before > 0 and shares_after > 0

        if not measured:
            continue

        lands_on_factor = abs(numpy.log(value_after / value_before / split_factor))
        shares_flat = abs(numpy.log(shares_after / shares_before))

        if lands_on_factor < SPLIT_SIGNATURE_TOLERANCE and shares_flat < SPLIT_SHARES_TOLERANCE:
            fix[:row] = fix[:row] * split_factor

    return _column(pandas.Series(traded_value * fix))


def c_volume_dividend_and_split_adjusted(
    c_traded_value: "kaxanuk.data_curator.DataColumn",
    c_close_dividend_and_split_adjusted: "kaxanuk.data_curator.DataColumn",
) -> "kaxanuk.data_curator.DataColumn":
    """
    The day's volume in the shares of the total-return series, which the book is traded in.

    The engine measures an order's market impact as its shares over the day's volume; on a
    dividend-adjusted fill those are more shares than the tape printed, so the volume is put on the
    same basis: the day's dollars over the adjusted close.
    """
    volume = _floats(c_traded_value) / _floats(c_close_dividend_and_split_adjusted)

    return _column(volume)


def _column(
    values: "pandas.Series",
) -> "kaxanuk.data_curator.DataColumn":
    """
    A column for the Curator, every non-finite value a null rather than a NaN or an infinity.
    """
    finite = values.replace([numpy.inf, -numpy.inf], numpy.nan)
    nullable = finite.astype("Float64")

    return kaxanuk.data_curator.DataColumn.load(nullable)


def _floats(
    column: "kaxanuk.data_curator.DataColumn",
) -> "pandas.Series":
    """
    A column as plain floats, a null as NaN, for the arithmetic numpy does.
    """
    # Through a plain list: a sparse column -- a dividend on its ex-date, null elsewhere -- reaches
    # pandas whole that way, where the Arrow-backed conversion handed back its values alone.
    values = column.to_pyarrow().to_pylist()
    numbers = pandas.Series(
        values,
        dtype="object",
    )

    return pandas.to_numeric(
        numbers,
        errors="coerce",
    ).astype(float)

# --- example: end ---
