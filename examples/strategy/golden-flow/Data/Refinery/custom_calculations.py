"""
The `r_*` columns -- step 3 of 8, computed by the Data Refinery over the whole cross-section.

Two kinds of column live here, and only here:

1.  Anything that compares securities against each other on a date -- a rank, a breadth reading, a
    share of the cross-section.  No per-security calculation can express it.
2.  Anything with a setting an experiment will sweep, even when it is per-security -- a fitted
    model, or a window such as a twelve-month return's.  Widening the Curator's schema costs a
    refetch of every identifier, and a sweep must never cost a download, so the frozen inputs stay
    in the Curator and the column with the setting lives here.

**A new experiment's signal on the data already downloaded is an `r_*` column here**, computed from
the `c_*` columns the Curator wrote -- the daily total-return log returns, the traded value --
never a widening of the Curator's columns and a second download.

What is expected here is one function per column, named exactly as the column, resolved by
parameter name the same way the Curator resolves its own.  Every parameter is a column of the
panel -- the date, `main_identifier`, any `c_*` or `r_*` column, any `current_*` column -- and a
function may group by any of them.  The column is registered by listing it in this module's output
tuple; nothing else registers it.

One requirement this module exists to enforce: causality.  Every cross-sectional column on date t
uses only the cross-section as of t, and every rolling window looks strictly backward.  A rank
taken over the pooled sample, or a mean over the whole history, would leak the future distribution
into every row and would not raise a single error doing it.

Rank convention: every `*_rank` column is a per-date percentile, ascending, so 1.0 is the highest
raw value in that day's cross-section.  A percentile over n values averages to (n + 1) / 2n, not to
0.5 -- 0.542 on 12 securities, 0.5006 on 800.  A check written against 0.5 fails on every date of
a narrow universe and passes on a wide one, which is the worst possible failure mode; check against
the identity.

The minimum that ships in a filled-in repository: a per-date liquidity rank, the universe size on
each date (the denominator behind every rank), and one worked example of per-date normalisation.
A column that reads a `current_*` column is marked as such, so the refinery can skip it before the
security master exists.

It produces the `r_*` columns in every file under `Data/Refinery/Time_Series/`.

It prevents a signal that knew the future distribution, and a rank that was silently pooled.
"""

# --- example: begin ---

import pandas

__all__ = [
    "CLASSIFICATION_DEPENDENT_COLUMNS",
    "REFINERY_COLUMNS",
    "r_liquidity_rank",
    "r_traded_value_sma_126d",
    "r_traded_value_sma_21d",
    "r_traded_value_sma_63d",
    "r_trend_100_300",
    "r_trend_20_100",
    "r_trend_50_200",
    "r_universe_size",
]

# The columns this module produces, in the order the driver builds them.  A column may read any
# column built before it, and `r_index_weight`, which the driver attaches from the index's
# holdings before any of them.
REFINERY_COLUMNS = (
    "r_universe_size",
    "r_traded_value_sma_21d",
    "r_traded_value_sma_63d",
    "r_traded_value_sma_126d",
    "r_liquidity_rank",
    "r_trend_20_100",
    "r_trend_50_200",
    "r_trend_100_300",
)
# The subset that needs `Universe/Security_Master.csv`, so the refinery still runs before the
# universe notebook has written one.  This strategy groups by nothing, so the subset is empty.
CLASSIFICATION_DEPENDENT_COLUMNS = ()


def r_liquidity_rank(
    m_date: "pandas.Series",
    r_index_weight: "pandas.Series",
    r_traded_value_sma_63d: "pandas.Series",
) -> "pandas.Series":
    """
    Rank each member's quarter-long average traded value against that day's members.

    The rank is what "most traded" means once it has to be measured: a percentile inside the day,
    so a dollar figure that grows with the market over twenty years stays comparable with itself.
    Ranking within the date is also what keeps it causal -- a rank taken over the pooled sample
    would know the whole history's distribution and would not raise a single error doing it.  Only
    the index's members on the date are ranked, so a name that left the index, or has not joined
    it, never moves another name's percentile; a non-member's rank is null.
    """
    member = r_index_weight > 0
    member_traded_value = r_traded_value_sma_63d.where(member)
    traded_value_by_date = member_traded_value.groupby(m_date)

    return traded_value_by_date.rank(
        pct=True,
        ascending=True,
    )


def r_traded_value_sma_126d(
    main_identifier: "pandas.Series",
    c_traded_value: "pandas.Series",
) -> "pandas.Series":
    """
    The 126-day simple average of daily traded value, one of the sweep's two neighbours of 63.
    """
    return _rolling_mean(
        main_identifier,
        c_traded_value,
        126,
    )


def r_traded_value_sma_21d(
    main_identifier: "pandas.Series",
    c_traded_value: "pandas.Series",
) -> "pandas.Series":
    """
    The 21-day simple average of daily traded value, one of the sweep's two neighbours of 63.
    """
    return _rolling_mean(
        main_identifier,
        c_traded_value,
        21,
    )


def r_traded_value_sma_63d(
    main_identifier: "pandas.Series",
    c_traded_value: "pandas.Series",
) -> "pandas.Series":
    """
    The 63-day simple average of daily traded value: the rule's rank and weight.

    It is built here, beside its 21- and 126-day neighbours, so the rule and its sweep read one
    definition; the analyzer checks it equals the 63-day average
    of the Curator's own daily column.
    """
    return _rolling_mean(
        main_identifier,
        c_traded_value,
        63,
    )


def r_trend_100_300(
    main_identifier: "pandas.Series",
    c_close_dividend_and_split_adjusted: "pandas.Series",
) -> "pandas.Series":
    """
    The 100-day average over the 300-day one, minus one: the slower neighbour of the golden cross.
    """
    return _trend(
        main_identifier,
        c_close_dividend_and_split_adjusted,
        100,
        300,
    )


def r_trend_20_100(
    main_identifier: "pandas.Series",
    c_close_dividend_and_split_adjusted: "pandas.Series",
) -> "pandas.Series":
    """
    The 20-day average over the 100-day one, minus one: the faster neighbour of the golden cross.
    """
    return _trend(
        main_identifier,
        c_close_dividend_and_split_adjusted,
        20,
        100,
    )


def r_trend_50_200(
    main_identifier: "pandas.Series",
    c_close_dividend_and_split_adjusted: "pandas.Series",
) -> "pandas.Series":
    """
    Measure how far the 50-day average sits above the 200-day one, as a fraction.

    Positive means the golden cross is on for that security on that date; the rule reads only the
    sign, but the distance is kept because it costs nothing and a later experiment can rank on it.
    The first 199 rows of every security are null, which is the warm-up rather than a downtrend,
    and keeping them null is what stops a young listing being read as one.
    """
    return _trend(
        main_identifier,
        c_close_dividend_and_split_adjusted,
        50,
        200,
    )


def r_universe_size(
    m_date: "pandas.Series",
    r_index_weight: "pandas.Series",
) -> "pandas.Series":
    """
    Count the index's members on each date, which is the denominator behind every rank.

    A percentile over a narrow cross-section means something different from one over a wide one, so
    the count travels beside the rank instead of being reconstructed later by whoever reads it.
    """
    member = (r_index_weight > 0).astype(int)
    members_by_date = member.groupby(m_date)

    return members_by_date.transform("sum")


def _rolling_mean(
    main_identifier: "pandas.Series",
    values: "pandas.Series",
    window: int,
) -> "pandas.Series":
    """
    A strictly backward simple average per security, null until the window is full.
    """
    panel = pandas.DataFrame({
        "identifier": main_identifier,
        "value": values,
    })
    values_by_security = panel.groupby("identifier")["value"]
    rolling = values_by_security.rolling(window).mean()

    return rolling.reset_index(
        level=0,
        drop=True,
    )


def _trend(
    main_identifier: "pandas.Series",
    prices: "pandas.Series",
    short_window: int,
    long_window: int,
) -> "pandas.Series":
    """
    The short average over the long one, minus one, per security, null through the long warm-up.

    Both windows are arguments because the rule's pair and its two sweep neighbours share one
    definition, and a sweep that changed the definition with the window would test two things.
    """
    short_average = _rolling_mean(
        main_identifier,
        prices,
        short_window,
    )
    long_average = _rolling_mean(
        main_identifier,
        prices,
        long_window,
    )

    return short_average / long_average - 1

# --- example: end ---
