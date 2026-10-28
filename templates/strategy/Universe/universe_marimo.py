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


if __name__ == "__main__":
    app.run()
