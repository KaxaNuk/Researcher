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
    # Universe — step 2 of 8

    **In plain words:** the eligible list, rebuilt for each date rather than for today.

    **It produces** `Universe/Security_Master.csv` and `Universe/Data_Issues.csv`, and the date from
    which the universe is usable.

    **It prevents** survivorship bias — testing on the winners that happened to survive — and a
    window that opens before the universe can honestly be priced.

    > **Runs after `Data/curator.py`**, because it profiles the files that were downloaded, and
    > **before `Data/refinery.py`**, because that stage joins the security master this one writes.

    **The universe is decided in `Universe/` and nowhere else** — the seed says which securities, this
    notebook what each one is and from when. Nothing downstream second-guesses either.

    ```
    Universe/Investable_Universe.csv   the seed, committed  ->  edit this to change the universe
            |
            +--> Data/curator.py       downloads one file per identifier in it
            |
            +--> this notebook         Security_Master.csv, Data_Issues.csv, the usable date
    ```

    **A marimo notebook, run as a script:** `uv run python Universe/universe_marimo.py`, or cell by
    cell with `uv run marimo edit Universe/universe_marimo.py`. Its outputs are never saved in the
    file, so there is nothing to strip before a commit; marimo's session cache, `__marimo__/`, is
    ignored.

    **In the template this notebook holds no code:** each section below says what is expected in it.
    Write the cells.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The universe is decided in `Universe/` and nowhere else** — the index's membership says which
    listings, `Universe/seed.py` the span Sharadar prices each over, and this notebook what each
    one is, from when, and how much of the index this repository can price on each date.

    ```
    Data/Curator/Benchmarks/index_daily_holdings_1998.csv   the index's daily membership, by hand
            |
            +--> Universe/seed.py      Investable_Universe.csv: each member listing and its span
            |
            +--> Data/curator.py       downloads one Sharadar file per listing in it
            |
            +--> this notebook         Security_Master.csv, Data_Issues.csv, Coverage.csv, the window
    ```

    **Since 0.16.0 the index and the prices speak one language.** The KN US Equity Core is built on
    Sharadar and keys every listing by Sharadar's ticker, so the price file of a listing is filed
    under the index's own key. What 0.15 had to prove listing by listing — that an FMP symbol was the
    index's security — is true by construction here, and Sharadar keeps delisted securities, so the
    survivorship cost this notebook publishes is the share of the index Sharadar does not price.
    """)
    return
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 0 · Setup

    Paths, and the strategy's rules for the window. Resolve the repository root whichever folder the
    notebook started in, and put `Data/` on the import path before importing from it: the files are
    read through `Data/time_series.py`, and an index's through `Data/hand_supplied.py`. Nothing here
    touches the network, and no value from `Config/.env` is ever printed.

    ## The seed

    `Universe/Investable_Universe.csv` is the only thing that decides what this repository is about.
    Replace its rows with equities, ETFs, FX crosses, crypto pairs or futures and every stage below
    still runs — nothing downstream names an asset class.

    **One column is required: `main_identifier`**, the identifier the experiment's provider prices
    each security under, which the Data Curator asks it for. A seed taken from an index also carries
    the index's own ticker, `index_identifier`, which can differ; the map between the two comes from
    the strategy's seed builder, or from the Analytics Factory when it supplies one.

    **The seed holds identifiers and dates, and nothing a provider sells.** A name, a permanent
    identifier, an ISIN, a classification: each is the provider's data, so it is read from the
    provider's catalogue cached in `Universe/Provider_Cache/`, never committed. A column only you
    know — a hand-assigned bucket, an internal classification — belongs in the seed, because nothing
    else will supply it.

    **A span ends where the security did, never where its source does.** A seed that carries the
    dates each identifier speaks for — `valid_from` and `valid_to`, so a recycled symbol never joins
    two companies — leaves the last empty for a listing still trading on its source's last date: that
    is the day the source was written, not a delisting. Closed there, every live name stops on that
    day; no backtest cut earlier can notice, and a paper book finds nothing to price the day after.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Paths, and the owner's rules for the window. No network call is made here: the catalogue the
    security master is shaped from was cached by `Universe/seed.py`, and `Config/.env` is not read.
    """)
    return


@app.cell
def _():
    import csv
    import datetime
    import json
    import os
    import pathlib
    import sys

    import numpy
    import pandas

    # Every path below is relative to the repository root, whichever folder the notebook started in.
    NOTEBOOK_DIRECTORY = pathlib.Path.cwd()
    REPOSITORY_ROOT = next(
        folder
        for folder in (NOTEBOOK_DIRECTORY, *NOTEBOOK_DIRECTORY.parents)
        if (folder / "Universe").is_dir() and (folder / "Data").is_dir()
    )
    os.chdir(REPOSITORY_ROOT)
    # The index's files are the desk's, read in place by one module, never renamed or re-headed.
    sys.path.insert(0, str(REPOSITORY_ROOT / "Data"))

    import time_series  # noqa: E402

    import hand_supplied  # noqa: E402 - the path above has to exist first

    SEED_PATH = pathlib.Path("Universe/Investable_Universe.csv")
    CATALOGUE_DIRECTORY = pathlib.Path("Universe/Provider_Cache")
    CURATOR_DIRECTORY = pathlib.Path("Data/Curator/Time_Series")
    BENCHMARK_DIRECTORY = pathlib.Path("Data/Curator/Benchmarks")
    FETCH_OUTCOMES_PATH = pathlib.Path("Data/Curator/fetch_outcomes.json")
    SECURITY_MASTER_PATH = pathlib.Path("Universe/Security_Master.csv")
    DATA_ISSUES_PATH = pathlib.Path("Universe/Data_Issues.csv")
    COVERAGE_PATH = pathlib.Path("Universe/Coverage.csv")
    WINDOW_PATH = pathlib.Path("Universe/Window.csv")
    PRICE_COLUMN = "c_close_dividend_and_split_adjusted"
    TRADED_VALUE_COLUMN = "c_traded_value"
    SPLIT_RATIO_COLUMN = "c_split_ratio"

    # The owner's floor and the panel's last day, decided on 2026-10-23: the window opens no
    # earlier than the first date the factor model covers, and closes on the last date the Core and
    # the factor model both reach.
    WINDOW_FLOOR = pandas.Timestamp("2000-01-03")
    PANEL_END = pandas.Timestamp("2026-08-14")
    # The owner's rule of 2026-10-05, kept: the window opens on the first date from which the
    # members Sharadar prices, with a signal, hold at least this share of the index's weight on
    # every date to the window's end.
    COVERAGE_REQUIRED = 0.90
    # The golden cross needs 200 trading days of prices before it can say anything.
    WARM_UP_DAYS = 200
    # The data checks look at what the rule can read: the window and the warm-up before it.
    CHECK_FROM = WINDOW_FLOOR - pandas.Timedelta(450, unit="D")
    # A price file that starts or ends this far outside the security's own span carries another
    # company's history under the same symbol, and only the span is read.
    SPAN_TOLERANCE_DAYS = 30
    IMPOSSIBLE_DAILY_MOVE = 5.0
    # Traded value moves with the market, never by the split ratio itself: a step by the split's own
    # factor, within a tenth in logs, while the shares traded stay within this, over this many days
    # on each side, is volume adjusted twice.
    SPLIT_JUMP_TOLERANCE = 0.10
    SPLIT_SHARES_TOLERANCE = 0.15
    SPLIT_WINDOW_DAYS = 30
    VOLUME_COLUMN = "m_volume_split_adjusted"

    seed_rows = pandas.read_csv(SEED_PATH, dtype=str, keep_default_na=False)
    priced_rows = seed_rows[seed_rows["main_identifier"] != ""]
    identifiers = list(priced_rows["main_identifier"])
    holdings = hand_supplied.read_benchmark_holdings()
    print(f"seed: {len(seed_rows)} index listings, {len(priced_rows)} with a price key")
    # The seed holds tickers and dates only: what each listing is -- its permanent identifier,
    # its name -- is read from the newest catalogue `Universe/seed.py` cached.
    catalogue_path = sorted(CATALOGUE_DIRECTORY.glob("sharadar_tickers_*.csv"))[-1]
    _catalogue = pandas.read_csv(catalogue_path, dtype=str, keep_default_na=False)
    _equities = _catalogue[_catalogue["table"] == "SEP"] if "table" in _catalogue else _catalogue
    catalogue_by_ticker = _equities.drop_duplicates("ticker").set_index("ticker")
    in_catalogue = seed_rows["main_identifier"].isin(catalogue_by_ticker.index)
    print(f"in the catalogue {catalogue_path.name}: {int(in_catalogue.sum())}, "
          f"not in it: {int((~in_catalogue).sum())}")
    return (
        BENCHMARK_DIRECTORY,
        CATALOGUE_DIRECTORY,
        CHECK_FROM,
        COVERAGE_PATH,
        COVERAGE_REQUIRED,
        CURATOR_DIRECTORY,
        DATA_ISSUES_PATH,
        FETCH_OUTCOMES_PATH,
        IMPOSSIBLE_DAILY_MOVE,
        PANEL_END,
        PRICE_COLUMN,
        SECURITY_MASTER_PATH,
        SEED_PATH,
        SPAN_TOLERANCE_DAYS,
        SPLIT_JUMP_TOLERANCE,
        SPLIT_RATIO_COLUMN,
        SPLIT_SHARES_TOLERANCE,
        SPLIT_WINDOW_DAYS,
        TRADED_VALUE_COLUMN,
        VOLUME_COLUMN,
        WARM_UP_DAYS,
        WINDOW_FLOOR,
        WINDOW_PATH,
        catalogue_by_ticker,
        catalogue_path,
        csv,
        datetime,
        hand_supplied,
        holdings,
        identifiers,
        in_catalogue,
        json,
        numpy,
        pandas,
        priced_rows,
        seed_rows,
        time_series,
    )
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · The seed, checked

    Two things to establish before anything downstream trusts this file.

    1. **Every identifier is unique**, and so is every identity the provider's catalogue gives a row —
       a permanent identifier, an ISIN — but where a renamed security's rows follow each other in
       time. A repeated identity under two rows is usually a renamed security, and the two legs have
       to be stitched into one position or the book holds it twice. A point-in-time universe is
       supposed to contain these; what it must not do is hide them.
    2. **Nothing the strategy needs is missing.** For a seed taken from an index, every listing the
       index weights from the window's floor is a row; and whatever column the strategy compares
       things by, a missing value in it is a security that silently drops out of every group-level
       view.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before anything downstream trusts this file:

    1. **Every key is unique**, the price key, the index's key and Sharadar's permanent identifier.
       A repeated identity under two rows is usually a renamed security, and the two legs have to be
       stitched into one position or the book holds it twice.
    2. **Every listing the index ever weighted from the floor on is a row**, so no member drops out
       of the cross-section because nobody wrote it down.
    3. **The desk's two companion files agree with the holdings**: the 0/1 mask marks exactly the
       weighted cells, and the ticker list names exactly the holdings' columns.
    """)
    return


@app.cell
def _(
    BENCHMARK_DIRECTORY,
    WINDOW_FLOOR,
    catalogue_by_ticker,
    holdings,
    pandas,
    priced_rows,
    seed_rows,
):
    duplicate_symbols = priced_rows["main_identifier"][priced_rows["main_identifier"].duplicated()]
    duplicate_listings = seed_rows["index_identifier"][seed_rows["index_identifier"].duplicated()]
    # The permanent identifier is the catalogue's, never the seed's.
    _permanent = seed_rows["main_identifier"].map(catalogue_by_ticker["permaticker"])
    _permanent = _permanent[_permanent.notna() & (_permanent != "")]
    duplicate_permatickers = _permanent[_permanent.duplicated()]
    _since_floor = holdings.loc[holdings.index >= WINDOW_FLOOR - pandas.Timedelta(450, unit="D")]
    weighted_listings = set(_since_floor.columns[(_since_floor > 0).any(axis=0)])
    listings_without_row = sorted(weighted_listings - set(seed_rows["index_identifier"]))
    _mask = pandas.read_csv(
        BENCHMARK_DIRECTORY / "backtest_components_mask.csv",
        index_col=0,
        parse_dates=True,
    )
    _tickers = pandas.read_csv(BENCHMARK_DIRECTORY / "tickers.csv")["ticker"]
    _aligned_mask = _mask.reindex(index=holdings.index, columns=holdings.columns)
    mask_disagreements = int(((holdings > 0) != (_aligned_mask == 1)).sum().sum())
    tickers_agree = set(_tickers) == set(holdings.columns)
    print(f"duplicate price keys: {len(duplicate_symbols)}, index keys: {len(duplicate_listings)}, "
          f"permatickers: {len(duplicate_permatickers)}")
    print(f"listings weighted from the warm-up on with no seed row: {listings_without_row}")
    print(f"mask cells disagreeing with the weights: {mask_disagreements}; "
          f"ticker list equals the holdings' columns: {tickers_agree}")
    return (
        duplicate_listings,
        duplicate_permatickers,
        duplicate_symbols,
        listings_without_row,
        mask_disagreements,
        tickers_agree,
        weighted_listings,
    )
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · The security master

    The seed gives identity. Everything else comes from the provider: the official name, what kind of
    instrument it is, where it trades, in what currency, and when it started.

    **Cache the provider's raw payload, then shape the master from the cache.** Re-running then costs
    nothing, changing the column mapping never triggers a refetch, and the untouched payload stays
    available for fields this notebook does not yet use. Adding a provider is one fetch function and
    one normaliser.

    **The seed wins.** Its identity columns define the universe, so a provider value never overwrites
    one — it is compared instead, and a disagreement is reported. A provider that now points a symbol
    at a different security is a recycled identifier, and joining on it across the whole history would
    silently mix two companies.

    > **What the master carries is what a security is *today*.** The provider keeps no history, so on
    > a universe whose members get reclassified, every period before the move is attributed wrongly and
    > nothing raises an error. That is why the refinery prefixes every joined column `current_`.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The seed gives identity. Everything else comes from the provider's catalogue, cached by
    `Universe/seed.py` under the date it was fetched: the name, what kind of instrument it is, where
    it trades, in what currency, and its sector and industry.

    **The seed wins.** Its identity columns define the universe, so a catalogue value never
    overwrites one.
    """)
    return


@app.cell
def _(SECURITY_MASTER_PATH, catalogue_by_ticker, catalogue_path, pandas, priced_rows):
    _by_ticker = catalogue_by_ticker
    _master_rows = []

    for _row in priced_rows.itertuples(index=False):
        _entry = _by_ticker.loc[_row.main_identifier] if _row.main_identifier in _by_ticker.index else {}
        _master_rows.append({
            "main_identifier": _row.main_identifier,
            "index_identifier": _row.index_identifier,
            "permaticker": _entry.get("permaticker") or None,
            "name": _entry.get("name") or None,
            "category": _entry.get("category"),
            "exchange": _entry.get("exchange"),
            "currency": _entry.get("currency"),
            "is_delisted": _entry.get("isdelisted"),
            # Today's classification, never point-in-time: the refinery joins these as `current_*`.
            "sector": _entry.get("sector"),
            "industry": _entry.get("industry"),
            "valid_from": _row.valid_from or None,
            "valid_to": _row.valid_to or None,
            "match": (
                "sharadar ticker"
                if _row.main_identifier in _by_ticker.index
                else "not in catalogue"
            ),
        })

    security_master = pandas.DataFrame(_master_rows)
    security_master.to_csv(SECURITY_MASTER_PATH, index=False)
    print(f"catalogue {catalogue_path.name}; wrote {SECURITY_MASTER_PATH}: {len(security_master)} rows")
    print(security_master["category"].value_counts(dropna=False).head(8).to_string())
    return (security_master,)
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Composition, and how long each member has existed

    Two facts decide what a backtest can honestly claim. **What the universe is made of** sets what
    diversification is even available; **when each member started trading** sets the window, because a
    universe is only complete from the inception of its youngest member. **How much of it stopped
    trading before the panel ends** says whether this is a universe or a survivor list.

    ## 4 · The data-issues register

    The seed says what *should* exist. This section reads what *does*, and writes
    `Universe/Data_Issues.csv`. Every check below has cost somebody real time somewhere:

    | Check | The failure it catches |
    | --- | --- |
    | **Missing file** | an identifier the provider does not carry, which becomes a silent hole in the panel — counted apart from one it refused today, because only the second is worth asking again |
    | **Schema drift** | a folder holding two column sets, which makes every downstream read conditional |
    | **No usable signal** | a history shorter than the strategy's longest warm-up, so the name can never be selected |
    | **Unusable values** | zero or negative prices, which break every return calculation downstream |
    | **Spliced** | a file running outside its security's own span: another company's history under the same symbol, read only inside the span |
    | **Impossible daily move** | an adjusted price that multiplies by more than six in a day: an unadjusted corporate action or a bad print, not a return |
    | **Traded value across a split** | volume adjusted twice: traded value steps by the split's own factor while the shares traded stay flat, so liquidity is ranked on a number off by that factor |
    | **Late start** | a series that begins after the panel does, so the cross-section is smaller before that date |
    | **Status disagreement** | a series that ends early on a name the provider still calls active: a data gap, not a delisting |
    | **Early end** | a series that stops early — delisted or halted, and a held position must be exited on its last priced day |

    **Each row has a severity, blocking first.** A blocking row lists names no book may hold: every
    experiment reads them from this file and excludes them by name, so the row is never just a label.

    The split check is for any strategy that ranks, weights or screens on traded value: at every
    split, the median traded value of the thirty trading days after, against the thirty before, stays
    near one on a correct series, and lands near the split factor where the provider's volume counted
    the split twice. Where `Data/curator.py` corrects that signature, this check reads the same one,
    so a name the correction missed is named here. The `universe-point-in-time` skill lists two more:
    **internal gaps** and **identity conflict**.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The seed says what *should* exist. This section reads what *does*, and writes
    `Universe/Data_Issues.csv`, one row per check, each with a severity: a **blocking** row is an
    exclusion every experiment applies by name, **survivorship** rows are the cost published beside
    every result, **masked** rows are read only inside their span, and **expected** rows are facts
    of a point-in-time universe.

    | Check | The failure it catches |
    | --- | --- |
    | **Not in the catalogue** | an index member Sharadar does not list: survivorship cost, by name |
    | **Missing file** | a listing Sharadar does not price, or refused tonight — counted apart, because only the second is worth asking again |
    | **Schema drift** | a folder holding two column sets |
    | **No usable signal** | a history shorter than the longest warm-up, so the name can never be selected |
    | **Unusable values** | zero or negative prices, which break every return downstream |
    | **Spliced** | a file running outside its security's own span: masked to the span |
    | **Impossible daily move** | an adjusted price that multiplies by more than six in a day |
    | **Traded value across a split** | volume adjusted twice, or not at all: liquidity ranked on a number off by the split's factor |
    | **Late start** | a series that begins after the floor |
    | **Status disagreement** | a series that ends early on a name the catalogue still calls listed: a gap, not a delisting |
    | **Early end** | a series that stops before the panel ends — delisted, acquired or halted |
    | **Keys used twice** | a price key, index key or permaticker on two rows |
    | **Listing with no seed row** | a weighted member nobody wrote down |
    """)
    return


@app.cell
def _(PANEL_END, pandas, security_master):
    _valid_to = pandas.to_datetime(security_master["valid_to"], errors="coerce")
    ended = int((_valid_to < PANEL_END).sum())
    print(f"prices end before {PANEL_END.date()}: {ended} of {len(security_master)} "
          f"({ended / len(security_master):.0%} of the universe is dead today)")
    print(security_master["sector"].value_counts(dropna=False).head(12).to_string())
    return


@app.cell
def _(
    CHECK_FROM,
    CURATOR_DIRECTORY,
    FETCH_OUTCOMES_PATH,
    IMPOSSIBLE_DAILY_MOVE,
    PANEL_END,
    PRICE_COLUMN,
    SPAN_TOLERANCE_DAYS,
    SPLIT_JUMP_TOLERANCE,
    SPLIT_RATIO_COLUMN,
    SPLIT_SHARES_TOLERANCE,
    SPLIT_WINDOW_DAYS,
    TRADED_VALUE_COLUMN,
    VOLUME_COLUMN,
    WARM_UP_DAYS,
    WINDOW_FLOOR,
    datetime,
    identifiers,
    json,
    numpy,
    pandas,
    priced_rows,
    security_master,
    time_series,
):
    # The checks run against what the curator wrote, inside each security's span, over the window
    # and its warm-up. Each row names the identifiers, so the next stage gets a work list.
    fetch_outcomes = (
        json.loads(FETCH_OUTCOMES_PATH.read_text(encoding="utf-8"))
        if FETCH_OUTCOMES_PATH.is_file()
        else {}
    )
    _spans = {
        _row.main_identifier: (
            pandas.Timestamp(_row.valid_from) if _row.valid_from else None,
            pandas.Timestamp(_row.valid_to) if _row.valid_to else None,
        )
        for _row in priced_rows.itertuples(index=False)
    }
    price_frames = {}
    short_history = []
    non_positive_prices = []
    impossible_moves = []
    split_traded_value = []
    spliced = []
    schema_drift = []
    _expected_header = None

    for _identifier in identifiers:
        _path = time_series.path_for(CURATOR_DIRECTORY, _identifier)

        if not _path.is_file():
            continue

        _header = time_series.read_column_names(_path)

        if _expected_header is None:
            _expected_header = _header
        elif _header != _expected_header:
            schema_drift.append(_identifier)

        _whole = time_series.read_frame(
            _path,
            (
                "m_date",
                PRICE_COLUMN,
                TRADED_VALUE_COLUMN,
                SPLIT_RATIO_COLUMN,
                VOLUME_COLUMN,
            ),
        )
        _span_start, _span_end = _spans[_identifier]
        _tolerance = pandas.Timedelta(SPAN_TOLERANCE_DAYS, unit="D")
        _starts_early = _span_start is not None and _whole["m_date"].min() < _span_start - _tolerance
        _ends_late = _span_end is not None and _whole["m_date"].max() > _span_end + _tolerance

        if _starts_early or _ends_late:
            spliced.append(_identifier)

        _inside = pandas.Series(True, index=_whole.index)

        if _span_start is not None:
            _inside &= _whole["m_date"] >= _span_start

        if _span_end is not None:
            _inside &= _whole["m_date"] <= _span_end

        _frame = _whole.loc[_inside].reset_index(drop=True)
        price_frames[_identifier] = _frame

        if len(_frame) < WARM_UP_DAYS:
            short_history.append(_identifier)

        _checked = _frame[(_frame["m_date"] >= CHECK_FROM) & (_frame["m_date"] <= PANEL_END)]

        if (_checked[PRICE_COLUMN] <= 0).any():
            non_positive_prices.append(_identifier)

        # A price that multiplies by six in one day is an unadjusted corporate action or a bad
        # print, not a return; real squeezes reach three or four times.
        _daily_move = _checked[PRICE_COLUMN].pct_change(fill_method=None)

        if (_daily_move.abs() > IMPOSSIBLE_DAILY_MOVE).any():
            impossible_moves.append(_identifier)

        # Across a split, the 30 days after against the 30 before: traded value that lands on the
        # split's own factor while the shares the tape printed do not move is volume the provider
        # adjusted twice -- the signature `Data/curator.py` corrects, so a name here is one it
        # missed.  A jump without the flat shares is the market, and is not flagged.
        _ratio = _checked[SPLIT_RATIO_COLUMN].astype(float)
        _split_rows = numpy.flatnonzero(
            (_ratio / _ratio.shift(1) - 1).abs().fillna(0).to_numpy() > 0.01
        )
        _value = _checked[TRADED_VALUE_COLUMN].astype(float).to_numpy()
        _shares = (_checked[VOLUME_COLUMN] * _checked[SPLIT_RATIO_COLUMN]).astype(float).to_numpy()

        for _position in _split_rows:
            if _position < SPLIT_WINDOW_DAYS or _position + SPLIT_WINDOW_DAYS > len(_value):
                continue

            _factor = float(_ratio.iloc[_position - 1] / _ratio.iloc[_position])
            _value_jump = numpy.nanmedian(_value[_position:_position + SPLIT_WINDOW_DAYS]) / numpy.nanmedian(_value[_position - SPLIT_WINDOW_DAYS:_position])
            _shares_jump = numpy.nanmedian(_shares[_position:_position + SPLIT_WINDOW_DAYS]) / numpy.nanmedian(_shares[_position - SPLIT_WINDOW_DAYS:_position])

            # A stock dividend of a few percent cannot show the signature: only a real split is read.
            if _factor > 0 and abs(numpy.log(_factor)) >= 0.2 and _value_jump > 0 and _shares_jump > 0:
                _lands_on_factor = abs(numpy.log(_value_jump / _factor)) < SPLIT_JUMP_TOLERANCE
                _shares_flat = abs(numpy.log(_shares_jump)) < SPLIT_SHARES_TOLERANCE

                if _lands_on_factor and _shares_flat:
                    split_traded_value.append(_identifier)

    split_traded_value = sorted(set(split_traded_value))
    missing_files = [
        _identifier
        for _identifier in identifiers
        if _identifier not in price_frames
    ]
    not_carried = [
        _identifier
        for _identifier in missing_files
        if fetch_outcomes.get(_identifier) == "not carried"
    ]
    refused = [
        _identifier
        for _identifier in missing_files
        if _identifier not in not_carried
    ]
    late_start = [
        _identifier
        for _identifier, _frame in price_frames.items()
        if len(_frame) > 0 and _frame["m_date"].min() > WINDOW_FLOOR
    ]
    early_end = [
        _identifier
        for _identifier, _frame in price_frames.items()
        if len(_frame) > 0 and _frame["m_date"].max() < PANEL_END - datetime.timedelta(days=7)
    ]
    # A series that stops while the catalogue still calls the security listed is a data gap, not a
    # delisting -- and the two need different answers, so they are counted apart.
    _listed = set(security_master.loc[security_master["is_delisted"] == "N", "main_identifier"])
    status_disagreement = [
        _identifier
        for _identifier in early_end
        if _identifier in _listed
    ]
    print(f"files read: {len(price_frames)}, missing: {len(missing_files)} "
          f"({len(not_carried)} not carried, {len(refused)} refused or never asked)")
    return (
        early_end,
        impossible_moves,
        late_start,
        missing_files,
        non_positive_prices,
        not_carried,
        price_frames,
        refused,
        schema_drift,
        short_history,
        spliced,
        split_traded_value,
        status_disagreement,
    )


@app.cell
def _(
    DATA_ISSUES_PATH,
    duplicate_listings,
    duplicate_permatickers,
    duplicate_symbols,
    early_end,
    impossible_moves,
    in_catalogue,
    late_start,
    listings_without_row,
    non_positive_prices,
    not_carried,
    pandas,
    refused,
    schema_drift,
    seed_rows,
    short_history,
    spliced,
    split_traded_value,
    status_disagreement,
):
    _not_catalogued = seed_rows.loc[~in_catalogue, "index_identifier"].tolist()
    _duplicates = sorted(
        set(duplicate_symbols) | set(duplicate_listings) | set(duplicate_permatickers)
    )
    _checks = (
        ("not in the catalogue (index listing Sharadar does not list)", "survivorship", _not_catalogued),
        ("missing file (Sharadar does not carry the listing)", "survivorship", not_carried),
        ("missing file (refused by the provider, or never asked)", "blocking", refused),
        ("schema drift", "blocking", schema_drift),
        ("no usable signal (history shorter than the warm-up)", "blocking", short_history),
        ("unusable values (zero or negative prices)", "blocking", non_positive_prices),
        ("impossible daily move (the adjusted price multiplies by more than six)", "blocking", impossible_moves),
        ("traded value across a split (volume adjusted twice, missed by the curator)", "blocking", split_traded_value),
        ("spliced (the file runs outside the security's own span; only the span is read)", "masked", spliced),
        ("late start (no prices when the floor opens in 2000)", "expected", late_start),
        ("status disagreement (series ends early, catalogue still calls it listed)", "blocking", status_disagreement),
        ("early end (last price before the panel ends: delisted, acquired or halted)", "expected", early_end),
        ("keys used twice (a price key, index key or permaticker on two rows)", "blocking", _duplicates),
        ("listing with no seed row (weighted by the index, absent from the seed)", "blocking", listings_without_row),
    )
    issues = pandas.DataFrame([
        {
            "check": _name,
            "severity": _severity,
            "count": len(_identifiers),
            "identifiers": " ".join(_identifiers),
        }
        for _name, _severity, _identifiers in _checks
    ])
    issues.to_csv(DATA_ISSUES_PATH, index=False)
    print(f"wrote {DATA_ISSUES_PATH}")
    issues[["check", "severity", "count"]]
    return
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · When the universe is actually usable

    A file that starts in 2010 gives no signal in 2010. Every feature has a warm-up, and a five-year
    one moves the honest start of a backtest by five years.

    **The date that matters is the first day on which the universe can be both priced and
    signalled** — every security in it, or the share of it the strategy declares, with the shortfall
    published beside every result. A shortfall is a member the provider does not carry, never a listing
    whose key did not join. Before that date the strategy is choosing from a smaller menu than it
    appears to be, and a backtest that starts earlier is quietly comparing books drawn from different
    universes. Nothing else in the pipeline says so, which is why it is answered here.

    Write the coverage per date, and the date itself, to files of their own beside the master, so the
    analyzer and every experiment read the same first date rather than retype it.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A file that starts in 1999 gives no golden cross until its 200th day, and a member Sharadar does
    not price gives none at all. **The date that matters is the first day from which this repository
    can price, and signal, the index it says it trades**: the owner's rule of 2026-10-05, kept on
    2026-10-23 — the window opens on the later of the floor, 2000-01-03, and the first date from
    which the members with a price and 200 days of history behind it on that date hold at least 90%
    of the index's weight on every date to the window's end.

    The coverage is written per date to `Universe/Coverage.csv`, and the share the index loses is
    **the survivorship cost**, quoted beside every result.
    """)
    return


@app.cell
def _(
    COVERAGE_PATH,
    COVERAGE_REQUIRED,
    PANEL_END,
    PRICE_COLUMN,
    WARM_UP_DAYS,
    WINDOW_FLOOR,
    WINDOW_PATH,
    hand_supplied,
    holdings,
    pandas,
    price_frames,
):
    _keys = hand_supplied.read_listing_keys()
    _window_dates = holdings.index[(holdings.index >= WINDOW_FLOOR) & (holdings.index <= PANEL_END)]
    _on_window = holdings.loc[_window_dates]
    _signalled = pandas.DataFrame(False, index=_window_dates, columns=holdings.columns)
    _priced = pandas.DataFrame(False, index=_window_dates, columns=holdings.columns)

    for _listing in holdings.columns:
        _symbol = _keys.get(_listing)

        if _symbol is None or _symbol not in price_frames:
            continue

        _series = price_frames[_symbol].set_index("m_date")[PRICE_COLUMN]
        _history = _series.notna().cumsum()
        _priced[_listing] = _series.reindex(_window_dates).notna().to_numpy()
        _signalled[_listing] = (
            _history.reindex(_window_dates, method="ffill").fillna(0) >= WARM_UP_DAYS
        ).to_numpy() & _priced[_listing].to_numpy()

    _members = _on_window > 0
    _index_weight = _on_window.sum(axis=1)
    _priced_weight = _on_window.where(_priced, 0.0).sum(axis=1)
    _signalled_weight = _on_window.where(_signalled, 0.0).sum(axis=1)
    coverage_share = _signalled_weight / _index_weight
    coverage = pandas.DataFrame({
        "members": _members.sum(axis=1),
        "members_priced": (_members & _priced).sum(axis=1),
        "members_signalled": (_members & _signalled).sum(axis=1),
        "index_weight": _index_weight.round(6),
        "priced_weight": _priced_weight.round(6),
        "signalled_weight": _signalled_weight.round(6),
        "coverage": coverage_share.round(6),
        "survivorship_cost": (1 - _priced_weight / _index_weight).round(6),
    })
    coverage.index.name = "m_date"
    coverage.to_csv(COVERAGE_PATH)
    _short = coverage_share[coverage_share < COVERAGE_REQUIRED]
    window_start = (
        _window_dates[_window_dates > _short.index.max()].min()
        if len(_short) > 0
        else _window_dates.min()
    )
    print(f"coverage on the floor, {WINDOW_FLOOR.date()}: {coverage_share.iloc[0]:.2%}")
    print(f"dates below {COVERAGE_REQUIRED:.0%}: {len(_short)}")
    print(f"THE WINDOW OPENS ON {window_start.date()} and closes on {PANEL_END.date()}")
    pandas.DataFrame([{
        "window_start": window_start.date().isoformat(),
        "window_end": PANEL_END.date().isoformat(),
        "coverage_required": COVERAGE_REQUIRED,
        "coverage_on_floor": round(float(coverage_share.iloc[0]), 6),
    }]).to_csv(WINDOW_PATH, index=False)
    by_year = coverage.groupby(coverage.index.year).agg(
        members=("members", "mean"),
        members_priced=("members_priced", "mean"),
        coverage_mean=("coverage", "mean"),
        coverage_min=("coverage", "min"),
        survivorship_cost_max=("survivorship_cost", "max"),
    )
    print(by_year.round(4).to_string())
    return (window_start,)
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · Handoff

    | Output | Consumed by |
    | --- | --- |
    | `Universe/Security_Master.csv` | `Data/refinery.py`, which joins its columns onto the panel as `current_*` |
    | `Universe/Data_Issues.csv` | the caveats section of every `FINDINGS_N.md`; its blocking rows are each experiment's exclusions |
    | the usable date | the analyzer and the experiment, and `BLUEPRINT_N.md` before any rule exists |

    ## Open items to carry forward

    | # | Item | Why it matters |
    | --- | --- | --- |
    | 1 | **Classification is a snapshot, not a history.** | A security reclassified mid-window is misattributed before its move. The `current_*` prefix marks exactly this. |
    | 2 | **The last day of a delisted name is unaudited.** Nothing here checks whether a truncated series ends on a real final price or on a provider gap. | On a universe that retains delisted names, the missing returns are disproportionately the bad ones. |
    | 3 | **Inception dates come from the provider, not from the price file.** | The price file is what the backtest actually trades; the master is what a reader believes. Where they disagree, say so. |
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Output | Consumed by |
    | --- | --- |
    | `Universe/Security_Master.csv` | `Data/refinery.py`, which joins its columns onto the panel as `current_*` |
    | `Universe/Data_Issues.csv` | the caveats of every `FINDINGS_N.md`; its blocking rows are the experiment's exclusions |
    | `Universe/Coverage.csv` | the survivorship row of `RESULTS.md` and `FINDINGS_1.md` |
    | `Universe/Window.csv` | the analyzer, which screens over the same window, and the experiment |
    | the window's first date | `JOURNAL_1.md`, then `BLUEPRINT_1.md`, before any rule exists |

    ## Open items to carry forward

    | # | Item | Why it matters |
    | --- | --- | --- |
    | 1 | **Classification is a snapshot, not a history.** | A security reclassified mid-window is misattributed before its move. The `current_*` prefix marks exactly this. |
    | 2 | **The last day of a delisted name is Sharadar's last trade**, often over the counter after the exchange dropped it. | The engine sells a held name at that price; a delisting return after it (a cash-out, a write-off) is not in any file. |
    | 3 | **The catalogue is the one of 2026-09-24**, cached by `Universe/seed.py`. | A listing added to Sharadar later is "not in the catalogue" until the seed is rebuilt with `--refresh`. |
    """)
    return
# --- example: end ---


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7 · Verify

    **Assertions that raise when this stage's output is wrong**, read back from the files this notebook
    wrote rather than from the variables that wrote them. A check that prints is one somebody has to
    read; one that raises stops the run, so a notebook that reaches its last cell is one whose outputs
    hold. At the least:

    - `Universe/Security_Master.csv` has one row per identifier in the seed, each once, and no
      identifier the seed lacks;
    - `Universe/Data_Issues.csv` has a row for every check section 4 runs, each with a count;
    - the downloaded files and the register's missing ones account for the whole seed;
    - section 5 found a date from which the universe is usable;
    - for a seed taken from an index: every listing the index weights from the window's floor, the
      earliest date it may open, is a row of the seed under `index_identifier`; every row with no
      `main_identifier` is named in the register; no `main_identifier` or `index_identifier` appears
      twice; and no two rows hold one identity over the same dates — a renamed security's two rows
      follow each other.
    """)
    return


# --- example: begin ---
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - the security master has one row per price key in the seed, each once, and no key the seed
      lacks;
    - the register has a row for every check section 4 runs, each with a count, and its
      structural rows — keys twice, listings with no row — are empty;
    - the downloaded files and the missing ones account for every key in the seed;
    - the desk's mask and ticker list agree with the holdings;
    - section 5 found a window, and from its first date to its last the members Sharadar prices and
      signals hold at least 90% of the index's weight.
    """)
    return


@app.cell
def _(
    COVERAGE_PATH,
    COVERAGE_REQUIRED,
    DATA_ISSUES_PATH,
    PANEL_END,
    SECURITY_MASTER_PATH,
    SEED_PATH,
    WINDOW_FLOOR,
    WINDOW_PATH,
    identifiers,
    mask_disagreements,
    missing_files,
    pandas,
    price_frames,
    tickers_agree,
    weighted_listings,
    window_start,
):
    _seed = pandas.read_csv(SEED_PATH, dtype=str, keep_default_na=False)
    _priced = _seed[_seed["main_identifier"] != ""]
    _master = pandas.read_csv(SECURITY_MASTER_PATH)
    _issues = pandas.read_csv(DATA_ISSUES_PATH).set_index("check")
    _coverage = pandas.read_csv(COVERAGE_PATH, parse_dates=["m_date"]).set_index("m_date")
    _in_window = _coverage.loc[window_start:PANEL_END, "coverage"]
    _structural = _issues[
        _issues.index.str.startswith("keys used twice") | _issues.index.str.startswith("listing with no")
    ]
    _verifications = {
        "the master has one row per price key in the seed": len(_master) == len(_priced),
        "the master holds exactly the seed's keys": (
            set(_master["main_identifier"]) == set(_priced["main_identifier"])
        ),
        "the register holds all fourteen checks": len(_issues) == 14,
        "every check has a count": bool(_issues["count"].notna().all()),
        "no key is used twice and every weighted listing has a row": int(_structural["count"].sum()) == 0,
        "files and missing files account for every key": (
            len(price_frames) + len(missing_files) == len(identifiers)
        ),
        "every weighted listing is a row of the seed": (
            weighted_listings <= set(_seed["index_identifier"])
        ),
        "the desk's mask agrees with its weights": mask_disagreements == 0,
        "the desk's ticker list names the holdings' columns": tickers_agree,
        "the window has a first date": pandas.notna(window_start),
        "the window opens no earlier than the floor": window_start >= WINDOW_FLOOR,
        "the window file says the same": (
            pandas.read_csv(WINDOW_PATH)["window_start"].iloc[0] == window_start.date().isoformat()
        ),
        "coverage holds the owner's share on every window date": bool(
            (_in_window >= COVERAGE_REQUIRED).all()
        ),
    }
    _failed = [
        _name
        for _name, _passed in _verifications.items()
        if not _passed
    ]

    if len(_failed) > 0:
        _message = f"the universe failed verification: {'; '.join(_failed)}"

        raise AssertionError(_message)

    print(f"verified: {len(_verifications)} checks on the master, the register and the coverage")
    return
# --- example: end ---


if __name__ == "__main__":
    app.run()
