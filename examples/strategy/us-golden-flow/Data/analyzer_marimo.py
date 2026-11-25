import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data — analyzer

    **Block 3 of 3 in the Data stage, step 3 of 8.** The other two blocks *produce* data; this notebook
    is where it is *understood*, and where a feature either earns a backtest or is dropped before
    anybody spends a week on it.

    **In plain words:** build features and test whether they carry signal, before you model anything.

    **It produces** the charts and the information-coefficient table in `Data/Analyzer/`.

    **It prevents** a book built on a feature that never predicted anything.

    > **Runs after `Data/refinery.py`, and before any experiment** — the predictions an experiment's
    > blueprint makes are supposed to come from here.

    ```
    Data/curator.py    + Data/Curator/custom_calculations.py    ->  Curator/Time_Series/   m_* + c_*
    Data/refinery.py   + Data/Refinery/custom_calculations.py   ->  Refinery/Time_Series/  + r_*
    Data/analyzer_marimo.py                                     ->  Analyzer/  charts + the IC table
    ```

    `Universe/universe_marimo.py` profiles the *catalogue* — what exists, what is missing, when each
    security becomes usable. This notebook looks at the **content**: what the data says, and whether
    the signal built on it carries anything.

    **A marimo notebook, run as a script:** `uv run python Data/analyzer_marimo.py`, or cell by cell
    with `uv run marimo edit Data/analyzer_marimo.py`. Its outputs are never saved in the file.

    **In the template this notebook holds no code:** each section below says what is expected in it.
    Write the cells.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data — analyzer

    **Block 3 of 3 in the Data stage, step 3 of 8.** The other two blocks *produce* data; this notebook
    is where it is *understood*, and where a feature either earns a backtest or is dropped before
    anybody spends a week on it.

    **In plain words:** build features and test whether they carry signal, before you model anything.

    **It produces** the charts and the information-coefficient table in `Data/Analyzer/`.

    **It prevents** a book built on a feature that never predicted anything.

    > **Experiment 1 reads the Curator alone** (the owner's decision of 2026-11-16), so this
    > notebook does too: every column it screens is a `c_*` column of
    > `Data/Curator/Time_Series/`, the files of 2026-11-16, read as they are. The Refinery, and the
    > `r_*` columns, come back with Experiment 2.

    ```
    Data/curator.py    + Data/Curator/custom_calculations.py    ->  Curator/Time_Series/   m_* + c_*
    Data/analyzer_marimo.py                                     ->  Analyzer/  the IC table and the rest
    ```

    `Universe/universe_marimo.py` profiles the *catalogue* — what exists, what is missing, when each
    security becomes usable. This notebook looks at the **content**: what the data says, and whether
    the signal built on it carries anything.

    **What this notebook screens is US-Golden-Flow's own**: the golden cross, as the 1/0 state the
    rule reads, beside the sweep's two neighbours, and the traded-value rank the book is ranked and
    sized by. Nothing here comes from another strategy's later experiments.
    """)
    return


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Setup

    Read the refined panel, and name **the columns this notebook reads, once, in this cell** — the
    eligibility column, the features it eats, the cross-sectional candidates to screen. Everything
    below re-runs unchanged when they change. Read the window the universe notebook fixed from the
    file it wrote, never retyped.

    | Column family | Built by | Scope |
    | --- | --- | --- |
    | `m_*` | the provider, via the Curator | raw market data |
    | `c_*` | `Curator/custom_calculations.py` | **per security** — one security's own history |
    | `r_*` | `Refinery/custom_calculations.py` | **cross-sectional**, or with a setting an experiment sweeps |
    | `current_*` | joined from the security master | today's classification, **not point-in-time** |

    **A new feature on the data already downloaded is an `r_*` column**, added to
    `Data/Refinery/custom_calculations.py` and read here once the refinery has run: never a widening
    of the Curator's columns and a second download.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Setup

    Read the curated panel, and name **the columns this notebook reads, once, in this cell** — the
    membership column, the features it screens, the price every return reads. Everything below
    re-runs unchanged when they change.

    | Column family | Built by | Scope |
    | --- | --- | --- |
    | `m_*` | the provider, via the Curator | raw market data |
    | `c_*` | `Curator/custom_calculations.py`, and `Data/curator.py`'s completion pass | **per security** — one security's own history, plus the Core's weight that day |
    """)
    return


@app.cell
def _():
    import itertools
    import os
    import pathlib
    import sys

    import numpy
    import pandas

    NOTEBOOK_DIRECTORY = pathlib.Path.cwd()
    REPOSITORY_ROOT = (
        NOTEBOOK_DIRECTORY
        if (NOTEBOOK_DIRECTORY / "Experiments").is_dir()
        else NOTEBOOK_DIRECTORY.parent
    )
    os.chdir(REPOSITORY_ROOT)
    sys.path.insert(0, str(REPOSITORY_ROOT / "Experiments"))

    import securities_panel  # noqa: E402 - the path above has to exist first

    # The columns this notebook reads, named once. Everything below re-runs unchanged when they change.
    SIGNAL_COLUMN = "c_golden_cross_50_200"
    FAST_SIGNAL_COLUMN = "c_golden_cross_20_100"
    SLOW_SIGNAL_COLUMN = "c_golden_cross_100_300"
    ELIGIBLE_COLUMN = "c_eligible_golden_cross_50_200"
    MEMBERSHIP_COLUMN = "c_index_weight"
    TRADED_VALUE_COLUMN = "c_traded_value_sma_63d"
    CURATOR_TRADED_VALUE_COLUMN = "c_traded_value"
    PRICE_COLUMN = "c_close_dividend_and_split_adjusted"
    # The traded-value rank is cross-sectional, so it is taken here, per date, over the members:
    # the Curator writes each security's own history and knows nothing of the others.
    LIQUIDITY_NAME = "traded-value rank, per-date percentile of c_traded_value_sma_63d"
    # The rule ranks the golden-cross members by traded value and holds a few dozen, so the pool it
    # actually chooses from is the most traded members, not the whole index.
    POOL_SIZE = 50
    HORIZONS_IN_DAYS = (21, 63, 252)
    ANALYZER_DIRECTORY = pathlib.Path("Data/Analyzer")
    # The window the universe notebook fixed, read from what it wrote, and read in the three
    # sub-periods the blueprint judges the book on: a signal that pays in one regime only is read as
    # such. ANALYSIS_END is the last date of the Core and of the factor model: nothing later exists.
    window = pandas.read_csv("Universe/Window.csv")
    WINDOW_START = pandas.Timestamp(window["window_start"].iloc[0])
    ANALYSIS_END = pandas.Timestamp(window["window_end"].iloc[0])
    PERIODS = (
        ("1999 to 2008", WINDOW_START, pandas.Timestamp("2008-12-31")),
        ("2009 to 2017", pandas.Timestamp("2009-01-01"), pandas.Timestamp("2017-12-31")),
        ("2018 to 2026", pandas.Timestamp("2018-01-01"), ANALYSIS_END),
        ("the window", WINDOW_START, ANALYSIS_END),
    )

    matrices = securities_panel.load_matrices((
        SIGNAL_COLUMN,
        FAST_SIGNAL_COLUMN,
        SLOW_SIGNAL_COLUMN,
        ELIGIBLE_COLUMN,
        MEMBERSHIP_COLUMN,
        TRADED_VALUE_COLUMN,
        CURATOR_TRADED_VALUE_COLUMN,
        PRICE_COLUMN,
    ))
    cut = {
        name: matrix.loc[:ANALYSIS_END]
        for name, matrix in matrices.items()
    }
    signal = cut[SIGNAL_COLUMN]
    fast_signal = cut[FAST_SIGNAL_COLUMN]
    slow_signal = cut[SLOW_SIGNAL_COLUMN]
    eligible = cut[ELIGIBLE_COLUMN]
    member = cut[MEMBERSHIP_COLUMN].fillna(0.0) > 0
    traded_value = cut[TRADED_VALUE_COLUMN]
    price = cut[PRICE_COLUMN]
    liquidity = traded_value.where(member).rank(axis=1, pct=True)
    print(f"panel: {price.shape[0]} dates x {price.shape[1]} securities")
    print(f"from {price.index.min().date()} to {price.index.max().date()}")
    print(f"members per date in the window: {int(member.loc[WINDOW_START:].sum(axis=1).min())} "
          f"to {int(member.loc[WINDOW_START:].sum(axis=1).max())}")
    return (
        ANALYSIS_END,
        ANALYZER_DIRECTORY,
        CURATOR_TRADED_VALUE_COLUMN,
        FAST_SIGNAL_COLUMN,
        HORIZONS_IN_DAYS,
        LIQUIDITY_NAME,
        PERIODS,
        POOL_SIZE,
        SIGNAL_COLUMN,
        SLOW_SIGNAL_COLUMN,
        WINDOW_START,
        cut,
        eligible,
        fast_signal,
        itertools,
        liquidity,
        member,
        numpy,
        pandas,
        price,
        securities_panel,
        signal,
        slow_signal,
        traded_value,
    )


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · What each stage contributed

    The refined file is the Curator file plus columns, on its rows inside the span the seed gives the
    security, or all of them where it gives none. Confirming that here is what lets every section
    below read one folder and forget the Curator exists.

    Then **coverage**, per column. A column at 60% coverage is not quietly averaged over the 60%: say
    so, and decide whether the gap is a warm-up, a late listing or a broken input.

    Where the Curator rebuilt a provider's adjustment, measure here what the provider's prices are and
    what the rebuild changed, before any experiment: how coarse the provider's rounding is, where the
    rebuild departs from the provider's own series, and what the fill price keeps of the rounding.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · What each stage contributed

    The panel is the Curator's files, each cut to its listing's dates in the seed. **Coverage**, per
    column, over the members only: a column at 60% coverage is not quietly averaged over the 60%.
    The cross's gap among members is the 200-day warm-up of a name that listed late, not a broken
    input.
    """)
    return


@app.cell
def _(cut, member, pandas, signal):
    # Coverage per column, over the members only, so nothing below is averaged over non-members.
    _member_cells = int(member.sum().sum())
    coverage = pandas.DataFrame({
        "populated": {
            name: int(matrix.where(member).notna().sum().sum())
            for name, matrix in cut.items()
        },
    })
    coverage["member_cells"] = _member_cells
    coverage["share"] = (coverage["populated"] / coverage["member_cells"]).round(3)
    print(coverage)

    signal_by_year = (
        signal.where(member).notna().sum(axis=1) / member.sum(axis=1)
    ).groupby(signal.index.year).mean().round(3)
    print("share of members with a usable cross, by year:")
    print(signal_by_year.loc[1999:].to_string())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1 · Sharadar's prices — what they are, and what the Curator rebuilt

    Three facts about the provider decide how far a backtest on it can be trusted, and each is
    measured here rather than assumed. Every figure is weighted by the KN US Equity Core's own
    weight on the day, so it says how much of the index a fault touched, not how many files.

    1. **Sharadar rounds every price to three decimals, its adjusted ones included.** Only the
       unadjusted close is exact, so the Curator rebuilds the split factor and the total-return
       close from it and Sharadar's dividends and splits, and `Data/curator.py` adds the spin-offs
       from Sharadar's actions file — into `c_close_dividend_and_split_adjusted`, which every
       signal, return and mark here reads. The table gives, by year, the share of the Core whose
       adjusted price was under a dollar, and the largest daily gap between the rebuilt return and
       Sharadar's there.
    2. **The rebuild is checked against Sharadar file by file**, wherever Sharadar's own decimals
       are fine enough: `Data/Curator/adjustment_checks.csv`.
    3. **The open keeps Sharadar's rounding**: half a rounding step over the split-adjusted open,
       weighted by the Core, bounds that error by year. It falls either way: noise, not a bias.
    """)
    return


@app.cell
def _(ANALYSIS_END, member, pandas, securities_panel):
    _matrices = securities_panel.load_matrices((
        "m_close_dividend_and_split_adjusted",
        "c_close_dividend_and_split_adjusted",
        "m_open_split_adjusted",
        "c_index_weight",
    ))
    _cut = {
        _name: _matrix.loc[:ANALYSIS_END]
        for _name, _matrix in _matrices.items()
    }
    _weight = _cut["c_index_weight"].fillna(0.0).where(member, 0.0)
    _provider = _cut["m_close_dividend_and_split_adjusted"]
    _rebuilt = _cut["c_close_dividend_and_split_adjusted"]
    _open = _cut["m_open_split_adjusted"]
    _under_a_dollar = (_provider < 1.0).astype(float)
    _return_gap = ((_rebuilt / _rebuilt.shift(1)) - (_provider / _provider.shift(1))).abs()
    _open_rounding = 0.0005 / _open.where(_open > 0)
    _total_weight = _weight.sum(axis=1)
    precision_by_year = pandas.DataFrame({
        "share of the Core under a dollar, adjusted": (
            (_under_a_dollar * _weight).sum(axis=1) / _total_weight
        ),
        "largest daily return gap, rebuilt against Sharadar": (
            _return_gap.where(_weight > 0).max(axis=1)
        ),
        "open rounding, Core-weighted, basis points": (
            (_open_rounding * _weight).sum(axis=1) / _total_weight * 10_000
        ),
    }).groupby(_total_weight.index.year).agg({
        "share of the Core under a dollar, adjusted": "mean",
        "largest daily return gap, rebuilt against Sharadar": "max",
        "open rounding, Core-weighted, basis points": "mean",
    })
    checks = pandas.read_csv("Data/Curator/adjustment_checks.csv")
    _disagreeing = checks[checks["days_disagreeing"] > 0]
    print("Sharadar's precision and the rebuild, by year:")
    print(precision_by_year.round(4).to_string())
    print(f"\nfiles checked: {len(checks)}; with a day whose rebuilt return differs from "
          f"Sharadar's by more than 0.5% where both are precise: {len(_disagreeing)} "
          f"({', '.join(_disagreeing['identifier'])})")
    print(f"split-adjusted closes still off Sharadar's: "
          f"{int((checks['split_days_disagreeing'] > 0).sum())}")
    return checks, precision_by_year


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · What diversification is actually available

    A strategy that chooses between securities is a bet that they do not all move together. Whether
    that is true is measurable, and it decides how much the strategy can possibly add: **if everything
    is one trade, choosing between them is theatre.**

    Buy-and-hold return, volatility and worst day per security; the correlation matrix; the mean
    off-diagonal correlation and the extreme pairs.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · What diversification is actually available

    A strategy that chooses between securities is a bet that they do not all move together. Whether
    that is true is measurable, and it decides how much the strategy can possibly add: **if everything
    is one trade, choosing between them is theatre.**

    Buy-and-hold return, volatility and worst day per security; the mean off-diagonal correlation.
    """)
    return


@app.cell
def _(ANALYZER_DIRECTORY, WINDOW_START, member, numpy, pandas, price):
    # Over the window, on the members. fill_method=None: a gap must stay a gap.
    daily_returns = price.loc[WINDOW_START:].pct_change(fill_method=None)
    ever_member = member.loc[WINDOW_START:].any(axis=0)
    survivors = daily_returns.columns[ever_member & (daily_returns.notna().sum() > 500)]
    sample = daily_returns[survivors]
    correlations = sample.corr()
    off_diagonal = ~numpy.eye(len(correlations), dtype=bool)
    mean_correlation = float(numpy.nanmean(correlations.to_numpy()[off_diagonal]))
    print(f"members with more than 500 daily observations in the window: {len(survivors)}")
    print(f"mean pairwise correlation: {mean_correlation:.3f}")

    per_security = pandas.DataFrame({
        "annualised_return": sample.mean() * 252,
        "annualised_volatility": sample.std() * (252 ** 0.5),
        "worst_day": sample.min(),
    })
    diversification = per_security.describe()
    diversification.loc["mean_pairwise_correlation"] = mean_correlation
    ANALYZER_DIRECTORY.mkdir(parents=True, exist_ok=True)
    diversification.to_csv(ANALYZER_DIRECTORY / "diversification.csv")
    print(diversification.round(3))
    return (mean_correlation,)


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Are the cross-sectional columns what they claim to be?

    The Refinery asserts one property that would be silent if broken: **every rank is a percentile
    taken inside a single date.** A rank computed over the pooled sample would drift as the universe's
    composition changed, and nothing would raise an error.

    Check it as an identity, not as a rule of thumb. A per-date percentile over *n* untied values has
    mean exactly `(n + 1) / (2n)` — 0.542 on twelve securities, 0.5006 on eight hundred. Testing
    against 0.5 looks like a small failure on every date of a narrow universe and passes on a wide one,
    which is the worst possible failure mode.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Are the cross-sectional columns what they claim to be?

    **The traded-value rank is a percentile taken inside a single date**, over the members. Checked as
    an identity: a per-date percentile over *n* untied values has mean exactly `(n + 1) / (2n)`.
    Testing against 0.5 looks like a small failure on every date of a narrow universe and passes on a
    wide one.

    **The rule's 63-day traded value is the 63-day average of the Curator's daily traded value**, each
    security over its own rows, and **the eligible flag is membership and the cross at the prior
    close**, on every member-date.
    """)
    return


@app.cell
def _(CURATOR_TRADED_VALUE_COLUMN, cut, eligible, liquidity, member, signal, traded_value):
    off_members = int(liquidity.where(~member).notna().sum().sum())
    observed_mean = liquidity.mean(axis=1)
    count_per_date = liquidity.notna().sum(axis=1)
    expected_mean = (count_per_date + 1) / (2 * count_per_date)
    difference = (observed_mean - expected_mean).abs()
    tested = difference[count_per_date > 0]
    largest_rank_deviation = float(tested.max())
    print(f"ranks found on non-members: {off_members}")
    print(f"dates tested: {len(tested)}")
    print(f"largest deviation from the identity: {largest_rank_deviation:.6f}")

    curator_traded_value = cut[CURATOR_TRADED_VALUE_COLUMN].rolling(63, min_periods=63).mean()
    both = traded_value.notna() & curator_traded_value.notna()
    relative_gap = (
        (traded_value - curator_traded_value).abs() / curator_traded_value.abs().clip(lower=1.0)
    ).where(both)
    largest_traded_value_gap = float(relative_gap.max().max())
    print(f"largest relative gap between the two 63-day traded values: {largest_traded_value_gap:.2e}")

    expected_eligible = (member.shift(1, fill_value=False) & (signal.shift(1) == 1)).astype(float)
    compared = member & eligible.notna()
    eligible_disagreements = int((eligible.where(compared) != expected_eligible.where(compared)).where(compared, False).sum().sum())
    print(f"member-dates compared: {int(compared.sum().sum())}; "
          f"eligible flag disagreeing with membership and the cross at the prior close: "
          f"{eligible_disagreements}")
    return (
        eligible_disagreements,
        largest_rank_deviation,
        largest_traded_value_gap,
        off_members,
    )


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Information coefficient — which features predict returns

    **The section that decides things.** For each feature and horizon, the information coefficient is
    the cross-sectional rank correlation between the feature on date *t* and the forward return from
    *t* to *t+h*, computed **per date** and then averaged. Per date is what keeps it causal: the
    correlation only ever compares securities observable at the same moment.

    - **IC** — the mean daily correlation. The sign matters as much as the size: a negative IC means
      the feature works *inverted*.
    - **IR** = IC / IC standard deviation — the consistency of the edge, which is what survives into a
      portfolio.
    - **The share of dates with the expected sign**, beside the IR, and the overlap stated. A forward
      window of *h* days, measured every day, shares *h − 1* days with the next, so the dates are not
      independent observations and an IR counted over them overstates the evidence.

    Compute it over the whole panel and, separately, over the **eligible pool** the strategy actually
    selects from. The second is the one that matters: a feature can behave differently inside an
    already-filtered group.

    > **The IC table is a screening tool, not evidence.** An information ratio scales with the square
    > root of the number of independent bets, so on a narrow universe read these as directional. **A
    > feature that fails here does not get a book built on it**; one that passes has earned a backtest,
    > not a belief.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Information coefficient — which features predict returns

    **The section that decides things.** For each feature and horizon, the information coefficient is
    the cross-sectional rank correlation between the feature on date *t* and the forward return from
    *t* to *t+h*, computed **per date** and then averaged.

    - **IC** — the mean daily correlation. A negative IC means the feature works *inverted*.
    - **IR** = IC / IC standard deviation — the consistency of the edge.
    - **The share of dates with the expected sign**, positive for every feature here, and the overlap
      stated: a forward window of *h* days, measured every day, shares *h − 1* days with the next, so
      the dates are not independent observations and an IR counted over them overstates the evidence.

    The panel is **the index's members on each date**, the pool **the fifty most traded of them** —
    the rule holds 18 to 58 names, a median of 43 — and both are read in the blueprint's three
    sub-periods and over the window. The crosses are 1/0 states, so many dates tie: a rank
    correlation over a binary feature is a scaled difference of mean ranks, read as directional.

    > **The IC table is a screening tool, not evidence.** A feature that fails here does not get a
    > book built on it; one that passes has earned a backtest, not a belief.
    """)
    return


@app.cell
def _(
    ANALYZER_DIRECTORY,
    FAST_SIGNAL_COLUMN,
    HORIZONS_IN_DAYS,
    LIQUIDITY_NAME,
    PERIODS,
    POOL_SIZE,
    SIGNAL_COLUMN,
    SLOW_SIGNAL_COLUMN,
    fast_signal,
    itertools,
    liquidity,
    member,
    pandas,
    price,
    signal,
    slow_signal,
    traded_value,
):
    traded_order = traded_value.where(member).rank(axis=1, ascending=False, method="first")
    pool = traded_order <= POOL_SIZE
    FEATURES = (
        (SIGNAL_COLUMN, signal),
        (FAST_SIGNAL_COLUMN, fast_signal),
        (SLOW_SIGNAL_COLUMN, slow_signal),
        (LIQUIDITY_NAME, liquidity),
    )
    POOLS = (
        ("members", member),
        ("fifty most traded members", pool),
    )
    _rows = []

    for _horizon in HORIZONS_IN_DAYS:
        _forward_return = price.shift(-_horizon) / price - 1

        for (_feature_name, _feature_matrix), (_pool_name, _mask) in itertools.product(FEATURES, POOLS):
            _daily_correlation = _feature_matrix.where(_mask).corrwith(
                _forward_return.where(_mask),
                axis=1,
                method="spearman",
            ).dropna()

            for _period_name, _period_start, _period_end in PERIODS:
                _in_period = _daily_correlation.loc[_period_start:_period_end]
                _coefficient = _in_period.mean()
                _rows.append({
                    "feature": _feature_name,
                    "pool": _pool_name,
                    "period": _period_name,
                    "horizon_days": _horizon,
                    "overlap_days": _horizon - 1,
                    "information_coefficient": round(_coefficient, 4),
                    "information_ratio": round(_coefficient / _in_period.std(), 3),
                    "share_expected_sign": round((_in_period > 0).mean(), 3),
                    "dates": len(_in_period),
                })

    information_table = pandas.DataFrame(_rows)
    information_table.to_csv(ANALYZER_DIRECTORY / "information_coefficient.csv", index=False)
    print(information_table.to_string(index=False))
    return FEATURES, POOLS, information_table, pool


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · The two questions any signal owes an answer to

    Sections 0 to 4 are what any strategy needs. What belongs beside them depends on your signal, and
    two are worth writing whatever it is.

    **Does the signal separate anything?** Split forward return *and* forward volatility by the
    signal's state. A signal can be worth trading on the second alone; it would not be the first.

    **If the signal is fitted, what is look-ahead worth?** Read the same model causally and smoothed
    and report the gap. It is the cheapest audit in the process and routinely the largest number in it:
    the two series agree on most days and differ exactly at the turning points, which is where the
    money is.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · The two questions any signal owes an answer to

    **Does the signal separate anything?** Forward return *and* forward volatility over 21 days, split
    by the cross's state, inside the pool, over the window. A signal can be worth trading on the second
    alone.

    **If the signal is fitted, what is look-ahead worth?** The cross is arithmetic on past prices,
    not a fitted model, so there is no smoothed reading to compare a causal one against.

    Beside them, a property of the signal and the market, never of a book: how concentrated traded
    value is among the golden-cross members — the largest member's share, and how many hold at least
    one percent of it.
    """)
    return


@app.cell
def _(ANALYZER_DIRECTORY, WINDOW_START, member, pandas, pool, price, signal, traded_value):
    _horizon = 21
    _forward_return = price.shift(-_horizon) / price - 1
    _daily = price.pct_change(fill_method=None)
    _forward_volatility = _daily.rolling(_horizon).std().shift(-_horizon) * 252 ** 0.5
    _in_window = pandas.DataFrame(
        False,
        index=pool.index,
        columns=pool.columns,
    )
    _in_window.loc[WINDOW_START:, :] = True
    _window_pool = pool & _in_window
    _uptrend = (signal == 1) & _window_pool
    _downtrend = (signal == 0) & _window_pool
    separation = pandas.DataFrame({
        "forward_return_21d": {
            "50-day above 200-day": _forward_return.where(_uptrend).stack().mean(),
            "50-day below 200-day": _forward_return.where(_downtrend).stack().mean(),
        },
        "forward_volatility_21d": {
            "50-day above 200-day": _forward_volatility.where(_uptrend).stack().mean(),
            "50-day below 200-day": _forward_volatility.where(_downtrend).stack().mean(),
        },
        "observations": {
            "50-day above 200-day": int(_uptrend.sum().sum()),
            "50-day below 200-day": int(_downtrend.sum().sum()),
        },
    })
    separation.to_csv(ANALYZER_DIRECTORY / "separation.csv")
    print(separation.round(4))

    _cross_value = traded_value.where(member & (signal == 1))
    _cross_share = _cross_value.div(_cross_value.sum(axis=1), axis=0)
    _concentration = pandas.DataFrame({
        "eligible_members": _cross_value.notna().sum(axis=1),
        "largest_share": _cross_share.max(axis=1),
        "members_at_one_percent_or_more": (_cross_share >= 0.01).sum(axis=1),
    }).loc[WINDOW_START:]
    concentration_by_year = _concentration.groupby(_concentration.index.year).median().round(3)
    concentration_by_year.to_csv(ANALYZER_DIRECTORY / "concentration.csv")
    print(concentration_by_year.to_string())
    print("signal is unfitted: causal and smoothed readings are the same series")
    return concentration_by_year, separation


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.1 · Buy and hold against the cross, stock by stock

    **The signal read the way a person first asks about it: on how many stocks would holding only
    while the cross is on have beaten simply holding?** Asked for the Investment Bootcamp, before any
    book and with no bearing on the experiment's verdict.

    For each security, on the days it was a member of the KN US Equity Core at the prior close and
    its `c_golden_cross_50_200` existed at that close, two paths over the same days:

    - **buy and hold:** the stock's total-return close, every one of those days;
    - **the cross:** the same return on the days the cross was 1 at the prior close, and nothing on
      the others: cash earning nothing, no costs, no sizing.

    A security enters a period with at least 252 such days in it. Per period and over the window:
    how many stocks, on how many the cross earned more, fell less at its worst and moved less, the
    median of each measure on each path, and the spread — the cross's annual return less buy and
    hold's — at five percentiles across stocks. **It is a teaching measurement, not a book:** cash
    earns nothing, no trade costs anything, and a stock's spans in the Core are read as one path.
    """)
    return


@app.cell
def _(ANALYZER_DIRECTORY, PERIODS, member, numpy, pandas, price, signal):
    # The days each security is counted: a member at the prior close, with its signal already there.
    _returns = price.pct_change(fill_method=None)
    _counted = member.shift(1, fill_value=False) & signal.shift(1).notna()
    _on = _counted & (signal.shift(1) == 1)
    _hold = _returns.where(_counted)
    _cross = _returns.where(_on, 0.0).where(_counted)
    _minimum_days = 252
    _rows = []
    _spread_rows = []

    for _period_name, _period_start, _period_end in PERIODS:
        _hold_period = _hold.loc[_period_start:_period_end]
        _cross_period = _cross.loc[_period_start:_period_end]
        _days = _hold_period.notna().sum()
        _kept = _days[_days >= _minimum_days].index
        _hold_kept = _hold_period[_kept]
        _cross_kept = _cross_period[_kept]
        _hold_path = (1 + _hold_kept.fillna(0.0)).cumprod()
        _cross_path = (1 + _cross_kept.fillna(0.0)).cumprod()
        _years = _days[_kept] / 252
        _hold_annual = _hold_path.iloc[-1] ** (1 / _years) - 1
        _cross_annual = _cross_path.iloc[-1] ** (1 / _years) - 1
        _hold_decline = (_hold_path / _hold_path.cummax()).min() - 1
        _cross_decline = (_cross_path / _cross_path.cummax()).min() - 1
        _hold_volatility = _hold_kept.std() * numpy.sqrt(252)
        _cross_volatility = _cross_kept.std() * numpy.sqrt(252)
        _spread = _cross_annual - _hold_annual
        _rows.append({
            "period": _period_name,
            "stocks": len(_kept),
            "stocks_cross_earned_more": int((_cross_annual > _hold_annual).sum()),
            "share_cross_earned_more": float((_cross_annual > _hold_annual).mean()),
            "share_cross_fell_less": float((_cross_decline > _hold_decline).mean()),
            "share_cross_moved_less": float((_cross_volatility < _hold_volatility).mean()),
            "median_hold_annual_return": float(_hold_annual.median()),
            "median_cross_annual_return": float(_cross_annual.median()),
            "median_hold_worst_decline": float(_hold_decline.median()),
            "median_cross_worst_decline": float(_cross_decline.median()),
            "median_hold_volatility": float(_hold_volatility.median()),
            "median_cross_volatility": float(_cross_volatility.median()),
            "median_share_of_days_on": float(
                _on.loc[_period_start:_period_end, _kept]
                .astype(float)
                .where(_hold_kept.notna())
                .mean()
                .median()
            ),
        })
        _spread_rows.append({
            "period": _period_name,
            **{
                f"spread_p{_percentile}": float(_spread.quantile(_percentile / 100))
                for _percentile in (10, 25, 50, 75, 90)
            },
        })

    hold_against_cross = pandas.DataFrame(_rows)
    hold_against_cross_spread = pandas.DataFrame(_spread_rows)
    hold_against_cross.to_csv(ANALYZER_DIRECTORY / "hold_against_cross.csv", index=False)
    hold_against_cross_spread.to_csv(ANALYZER_DIRECTORY / "hold_against_cross_spread.csv", index=False)
    print(hold_against_cross.round(4).to_string(index=False))
    print(hold_against_cross_spread.round(4).to_string(index=False))
    return hold_against_cross, hold_against_cross_spread


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Handoff

    | Output | Consumed by |
    | --- | --- |
    | `Data/Refinery/Time_Series/` | **`Experiments/` — read this one** |
    | `Data/Analyzer/` — the IC table | feature selection in every experiment |
    | `Data/Analyzer/Charts/` | `FINDINGS_N.md` |

    ## What to write in the blueprint before running an experiment

    **Write down what you expect before you run this.** A prediction made from the data and then
    confirmed by the engine is the strongest methodological result an experiment can report; a number
    found first and explained afterwards is a story.

    Put the predictions this notebook licenses in `BLUEPRINT_N.md` **before** the backtest, each with
    the section it came from and the observation that would falsify it. **Findings from this stage go
    straight into `RESULTS.md`**, under *Before any experiment* — a marimo notebook saves no output in
    its file, so a measurement living only in a cell's output does not survive the run.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Handoff

    | Output | Consumed by |
    | --- | --- |
    | `Data/Curator/Time_Series/` | **`Experiments/` — Experiment 1 reads this one** |
    | `Data/Analyzer/information_coefficient.csv` | feature selection, and a blueprint's predictions |
    | `Data/Analyzer/separation.csv`, `concentration.csv`, `diversification.csv` | `RESULTS.md`, *Before any experiment* |
    | `Data/Analyzer/hold_against_cross.csv`, `hold_against_cross_spread.csv`, section 5.1 | `RESULTS.md`, the Investment Bootcamp |

    ## What to write in the blueprint before running an experiment

    **Write down what you expect before you run this.** A prediction made from the data and then
    confirmed by the engine is the strongest methodological result an experiment can report; a number
    found first and explained afterwards is a story. **Findings from this stage go straight into
    `RESULTS.md`**, under *Before any experiment*: a marimo notebook saves no output, so a measurement
    living only in a cell's output does not survive the run.
    """)
    return


@app.cell
def _(
    ANALYZER_DIRECTORY,
    concentration_by_year,
    hold_against_cross,
    hold_against_cross_spread,
    information_table,
    separation,
):
    print(f"{ANALYZER_DIRECTORY / 'information_coefficient.csv'} -> RESULTS.md, Before any experiment")
    print(information_table.to_string(index=False))
    print(separation.round(4).to_string())
    print(concentration_by_year.to_string())
    print(hold_against_cross.to_string(index=False))
    print(hold_against_cross_spread.to_string(index=False))
    return


# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Verify

    **Assertions that raise when this stage's output is wrong**, read back from what this notebook
    wrote to `Data/Analyzer/` rather than from the variables that wrote it. A notebook that reaches its
    last cell is then one whose tables can be quoted. At the least:

    - the coefficient table has a row for every feature, pool and horizon, each with a finite
      coefficient, ratio and share of dates with the expected sign;
    - no coefficient is averaged over no dates, nor over more dates than the panel has a forward
      return for at its horizon;
    - the pool the strategy selects from never counts more dates than the whole panel at the same
      horizon, because it is a part of it.
    """)
    return


# --- example: begin ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Verify

    **Assertions that raise when this stage's output is wrong**, read back from what this notebook
    wrote to `Data/Analyzer/` rather than from the variables that wrote it. Here:

    - the panel ends on or before the window's last date, the Core's and the factor model's last;
    - the coefficient table has a row for every feature, pool, period and horizon, each with a finite
      coefficient and ratio and a share of dates with the expected sign between 0 and 1;
    - no row averages over no dates or over more dates than have a forward return at its horizon, and
      the pool never counts more dates than the members;
    - no rank sits on a non-member, every date's ranks satisfy the percentile identity, the rule's
      63-day traded value is the average of the Curator's, and the eligible flag is membership and the
      cross at the prior close on every member-date;
    - buy and hold against the cross has every period, each with stocks, its shares between 0 and 1,
      its count of stocks no larger than its stocks, and its spread's percentiles in order.
    """)
    return


@app.cell
def _(
    ANALYSIS_END,
    ANALYZER_DIRECTORY,
    FEATURES,
    HORIZONS_IN_DAYS,
    PERIODS,
    POOLS,
    eligible_disagreements,
    largest_rank_deviation,
    largest_traded_value_gap,
    numpy,
    off_members,
    pandas,
    price,
):
    # Read back the tables this notebook wrote, and raise on the first thing that is wrong.
    table_path = ANALYZER_DIRECTORY / "information_coefficient.csv"
    written_table = pandas.read_csv(table_path)
    hold_written = pandas.read_csv(ANALYZER_DIRECTORY / "hold_against_cross.csv")
    spread_written = pandas.read_csv(ANALYZER_DIRECTORY / "hold_against_cross_spread.csv")
    hold_shares = hold_written[[
        "share_cross_earned_more",
        "share_cross_fell_less",
        "share_cross_moved_less",
    ]]
    measured = written_table[[
        "information_coefficient",
        "information_ratio",
        "share_expected_sign",
    ]]
    dates_by_pool = written_table.pivot_table(
        index=["feature", "period", "horizon_days"],
        columns="pool",
        values="dates",
    )
    trading_days = len(price.index)
    most_dates = trading_days - written_table["horizon_days"]
    verifications = {
        "the panel ends no later than the window's last date": price.index.max() <= ANALYSIS_END,
        "a row for every feature, pool, period and horizon": (
            len(written_table) == len(FEATURES) * len(POOLS) * len(PERIODS) * len(HORIZONS_IN_DAYS)
        ),
        "every coefficient, ratio and sign share is finite": bool(
            numpy.isfinite(measured).all(axis=None)
        ),
        "every sign share lies between 0 and 1": bool(
            measured["share_expected_sign"].between(0, 1).all()
        ),
        "every row averages over at least one date": bool((written_table["dates"] > 0).all()),
        "no row counts more dates than have a forward return": bool(
            (written_table["dates"] <= most_dates).all()
        ),
        "the pool never counts more dates than the members": bool(
            (dates_by_pool["fifty most traded members"] <= dates_by_pool["members"]).all()
        ),
        "no rank sits on a non-member": off_members == 0,
        "every date's ranks satisfy the percentile identity": largest_rank_deviation < 1e-9,
        "the rule's traded value is the Curator's": largest_traded_value_gap < 1e-6,
        "the eligible flag is membership and the cross at the prior close": eligible_disagreements == 0,
        "the separation, concentration and diversification tables were written": (
            (ANALYZER_DIRECTORY / "separation.csv").is_file()
            and (ANALYZER_DIRECTORY / "concentration.csv").is_file()
            and (ANALYZER_DIRECTORY / "diversification.csv").is_file()
        ),
        "buy and hold against the cross has every period, each with stocks": (
            len(hold_written) == len(PERIODS) and bool((hold_written["stocks"] > 0).all())
        ),
        "its shares lie between 0 and 1": bool(hold_shares.stack().between(0, 1).all()),
        "its count of stocks is no larger than its stocks": bool(
            (hold_written["stocks_cross_earned_more"] <= hold_written["stocks"]).all()
        ),
        "its spread's percentiles are in order": bool(
            spread_written.drop(columns="period").diff(axis=1).iloc[:, 1:].ge(0).all(axis=None)
        ),
    }
    failed = [
        name
        for name, passed in verifications.items()
        if not passed
    ]

    if len(failed) > 0:
        message = f"the analyzer failed verification: {'; '.join(failed)}"

        raise AssertionError(message)

    print(f"verified: {len(verifications)} checks on {table_path}")
    return


# --- example: end ---


if __name__ == "__main__":
    app.run()
