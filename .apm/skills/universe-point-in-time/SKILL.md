---
name: universe-point-in-time
description: >
  Load this skill whenever you build, extend, run or debug the Universe stage of a KaxaNuk Strategy
  Template repository — `Universe/Investable_Universe.csv` and `Universe/universe_marimo.py`,
  step 2. Use it when the user asks what belongs in the seed, how to add or change the securities
  a strategy trades, why delisted names are kept, how to build or refresh `Security_Master.csv`,
  how to reconcile a provider against the seed, what a recycled identifier is, why classifications
  are prefixed `current_`, what belongs in `Data_Issues.csv`, or from which date a universe is
  usable. It covers the seed's contract, the two-layer master, the checks and the usable date. It
  does NOT cover downloading prices (the Data stage, `Data/curator.py`, with
  `data-curator-custom-calculations`), the refinery's cross-sectional panel (see the example's
  `Data/refinery.py`), screening a feature (use `data-analyzer-runs`), sizing a book (use
  `portfolio-construction-runs`), or the research process around the stage (use
  `experiment-lifecycle`).
metadata:
  version: 0.4.0
---

# The Universe — the eligible list, rebuilt for each date rather than for today

**In plain words:** which securities are investable, point-in-time. **It produces**
`Universe/Security_Master.csv` and `Universe/Data_Issues.csv`. **It prevents** survivorship bias —
testing on the winners that happened to survive.

**Eligibility is decided here and nowhere else.** Everything downstream reads the security master
and does not second-guess it.

The stage comes **after the objective**: the claims in `OBJECTIVE.md` decide what the universe has
to contain, so the seed is chosen once they exist. And it sits **between** the two Data commands,
where the order is not cosmetic either: the curator downloads from the seed, this notebook profiles
what the curator wrote, and the refinery joins the master this notebook produces.

```
Universe/Investable_Universe.csv   the seed, committed  ->  edit this to change the universe
        |
        +--> Data/curator.py       downloads one file per identifier in it
        |
        +--> universe_marimo.py    Security_Master.csv, Data_Issues.csv, the usable date
                    |
                    +--> Data/refinery.py    joins the master onto the panel as current_*
```

**The template ships the seed, header-only, and the notebook as its markdown cells**, each section
a description of what its code must do. The notebook is a marimo notebook, run as a script —
`uv run python Universe/universe_marimo.py`, or cell by cell with
`uv run marimo edit Universe/universe_marimo.py` — which saves no output in its file; its session
cache, `__marimo__/`, is ignored. In a strategy made from a template before 0.10.0 the notebook is
missing, and before 0.20.0 it is a Jupyter notebook, `Universe/universe.ipynb`. The marimo one
comes back from the template through `init-strategy`'s script, run from the strategy's root,
`scaffold.py strategy . --only Universe/universe_marimo.py` — by its own path, because
`--only Universe` stops over the seed, which is already the strategy's own — and an old notebook's
cells are moved into it by hand, then the old file deleted. Never write the notebook from memory.

## 1. The seed is the whole decision

`Universe/Investable_Universe.csv` is the only file in the repository that decides what the
strategy is about. It is **committed** — the one data file that is — because the entire pipeline
grows from it, and because a universe nobody can reconstruct makes every number downstream
unverifiable.

- **One column is required: `main_identifier`**, the name the Data Curator asks the provider for.
  It is chosen per experiment, the identifier that experiment's provider prices under, and mapped
  from an index's own ticker by the strategy's seed builder, or by the Analytics Factory when it
  supplies the map. Replace the rows with equities, ETFs, FX crosses, crypto pairs or futures and
  every stage below still runs: nothing downstream names an asset class.
- **It holds identifiers and dates, and nothing a provider sells.** A name, a permanent
  identifier, an ISIN, a sector: each is the provider's data, read from the provider's catalogue
  cached in `Universe/Provider_Cache/`, which git ignores, and joined into the security master. The
  seed is committed, so a vendor field in it is the vendor's data published with the strategy. The
  worked example's seed is `main_identifier,index_identifier,valid_from,valid_to`, and nothing
  else.
- **A seed taken from an index carries a second key, `index_identifier`**: the index's own
  ticker, in its holdings' own convention — `BRK.B`, a digit-suffixed reused ticker — beside
  `main_identifier`. Every join to the index's files — membership, the benchmark's weights, the
  factor exposures — goes through the seed's two keys, and `Data/hand_supplied.py` is the one
  place that maps them. A provider whose tickers follow another convention is **a map to write in
  the seed, never a coverage caveat**, since a key that does not join raises nothing and makes a
  member that can never be held.
- **It is point-in-time, and it retains delisted, acquired and renamed names.** A universe built
  from *today's* members has silently deleted everything that failed, and the backtest then
  discovers that markets go up. If a seed shows 0% delisted, it is not a universe, it is a survivor
  list.
- **It is also the membership list.** The Curator's folder holds the cash proxy and the benchmarks
  as well, because the engine prices everything from one directory. The refinery and the panel
  loader both take membership from the seed, so those extras can never leak into a cross-section
  and there is no second list to forget to update.

**Changing the seed changes every published number.** Adding or removing a security changes the
cross-section, so every rank, every breadth reading and every book struck from them moves. Treat it
as a change-set of its own: its own commit, its own changelog entry, and the pipeline re-run before
any figure from it is quoted beside an older one.

### What else the universe is worth carrying

Nothing beyond the identifier is required in the seed, and two things earn their place in most
strategies' security masters, both from the provider's cached catalogue, never typed into the seed:

- **A stable identity — a provider's permanent identifier, an ISIN, a FIGI.** A point-in-time
  universe *contains* renamed securities: two identifiers sharing one identity, each carrying part
  of the history. Without a column that says which two rows are one company, the panel holds both
  legs and doubles the bet at the changeover. **The stitching downstream is only as good as this
  column**, and where there is none the loader keys by the identifier itself and stitches nothing
  — which is correct, because nothing has told it more. The worked example checks that no
  `permaticker` of Sharadar's catalogue falls on two of its rows.
- **A readable name**, so a book can be read by a person rather than decoded.

A seed taken from an index's own list often carries **a span**, the first and last dates
an identifier speaks for one company, so the panel reads no price of the company that later reused
the symbol. **A span ends where the security did, never where its source does.** A listing still
trading on the last date of the file the span was taken from — an index's master, a provider's
listing table — has no last date: that date is when the file was written, not a delisting. Closed
there, every live name stops on that day. No backtest cut earlier notices, because inside it a
span ending then reads the same as an open one; a paper book is the first reader of the days after,
and finds nothing to price.

Add whatever else the strategy groups or reports by. A column the provider can fill is filled by
section 2, from its cache; a column only you know — a hand-assigned bucket, an internal
classification — belongs in the seed, because nothing else will supply it.

## 2. The security master, in two layers

The seed gives identity. Everything else comes from the provider: the official name, what kind of
instrument it is, where it trades, in what currency, and when it started.

**Cache the provider's raw payload, then shape the master from the cache.** Two layers, and the
split pays three times: re-running costs nothing, changing the column mapping never triggers a
refetch, and the untouched payload stays available for fields the notebook does not yet use.
Adding a provider is then one fetch function and one normaliser, registered in an adapter table,
and no other cell changes.

Three properties the fetch layer needs, for the same reason the Curator's does: **cached**,
**resumable** — only identifiers missing from the cache are ever requested — and a switch that
makes the whole section offline, so a run can report what the cache holds and touch no network.

**The adapter declares what it can supply.** The columns a provider does not carry are a permanent
gap for that provider, not a fetch failure, and saying which is which is the difference between a
known limitation and a mystery.

### The seed wins on identity

A provider value never overwrites an identity column. It is **compared**, and a disagreement is
reported:

> **A provider that now points an identifier at a different security is a recycled symbol.** The
> ticker of a company that delisted gets reissued, and joining on it across the whole history
> silently mixes two companies. The seed's identity is authoritative; the provider's is evidence
> that the identifier has been reused, and the register records it.

### Classification is what a security is **today**

The provider keeps no history. On a universe whose members get reclassified — an equity moving
between GICS sectors, a fund changing category — **every period before the move is attributed
wrongly, and nothing raises an error.**

That is why the refinery prefixes every joined column `current_`, and why anything bucketed on one
is read as indicative. **Group or report by a `current_*` column; never select on it.** If the
strategy needs true point-in-time classification, it has to arrive as a per-date column out of the
Data stage, and until it does, the gap belongs in the register and in the caveats of every findings
file.

## 3. The data-issues register

The seed says what *should* exist. This section reads what *does* — the Curator's own output — and
writes `Universe/Data_Issues.csv`, one row per issue with the identifiers attached, so the next
stage has a work list rather than a chart to interpret.

| Check | The failure it catches |
| --- | --- |
| **Not in the catalogue** | a member of the index the provider does not list at all: still a row of the seed, with no span, and its weight is survivorship cost, named |
| **Missing file** | an identifier the provider does not carry, which becomes a silent hole in the panel — counted apart from one it refused today (a rate limit, a timeout), because only the second is worth asking again |
| **Spliced** | a file that runs outside its security's span: another company's history under a reused symbol, read only inside the span |
| **Schema drift** | a folder holding two column sets, which makes every downstream read conditional |
| **Late start** | a series that begins after the panel does, so the cross-section is smaller before that date |
| **Early end** | a series that stops early — delisted or halted, and a held position must be exited on its last priced day |
| **Internal gaps** | sessions missing inside a name's own range. Measure against a **real trading calendar**, not a business-day range: a business-day range counts every market holiday as a gap and makes almost every name look broken. An index ETF's own dates *are* the calendar |
| **Identity conflict** | the provider's identity differs from the seed's — a recycled identifier |
| **Status disagreement** | the price history and the provider's listing status disagree: a series ending early on a name the provider calls active is a data gap, not a delisting, and the reverse is a reused symbol |
| **Unusable values** | zero or negative prices, which break every return calculation downstream |
| **Impossible daily move** | an adjusted price that multiplies several times over in one day — an unadjusted corporate action or a bad print, not a return. Set the threshold above real squeezes, so a flag means the series is wrong rather than merely wild |
| **Traded value broken at a split** | a provider whose unadjusted volume before a split is already in post-split shares: the split adjustment counts it twice, so traded value — and every rank or weight taken on it — is too large by the split factor over the security's whole history before the split. At every split, compare the median traded value of the thirty trading days after with the thirty before, and the shares the tape printed the same way: traded value landing on the split's own factor while the shares stay flat is this fault, and a jump without the flat shares is the market. Fill prices are not affected. Found on FMP files of 2026-09-23 for ORLY (15:1, 2025-06-10), NOW (5:1, 2025-12-18) and TPL (3:1, 2025-12-23) — FMP's data, its maintainers confirmed, <https://github.com/KaxaNuk/Data-Curator/issues/36> — and on Sharadar, measured by the worked example on 2026-10-23, at 82 splits in 77 listings. Where the Curator corrects the volume in its own `c_*` traded value, as the example's does, this check reads the same signature and names any split the correction missed |
| **No usable signal** | a history shorter than the strategy's longest warm-up, so the name can never be selected |

Give each row a severity, and **sort blocking first**. A register nobody can triage is a chart with
extra steps. **A blocking row is a label until a stage reads it:** each experiment excludes the
names the blocking rows list, by name, read from the register and never typed, and its Verify raises
if one is ever held. **A row here is the provider's data**, reported to the provider — the security,
the date, the field, the value — never as an issue on a library, as
`data-curator-custom-calculations` says under *When a value looks wrong*.

## 4. When the universe is actually usable

A file that starts in 2010 gives no signal in 2010. Every feature has a warm-up, and a five-year
one moves the honest start of a backtest by five years.

**The date that matters is the first day on which the universe can be both priced and
signalled** — every security in it, or the share of it the strategy declares, with the shortfall
published beside every result. For a strategy that selects a fixed number of names, it is the first
day on which the eligible pool is also at least as deep as the book. Before it the strategy is
choosing from a smaller menu than it appears to be, and a backtest that starts earlier is quietly
comparing books drawn from different universes. **A shortfall is a member the provider does not
carry, never a listing whose key did not join**: that one is a map still to write in the seed,
section 1.

Nothing else in the pipeline says so, which is why it is answered here, and why it is declared in
`BLUEPRINT_N.md` before the rule rather than discovered afterwards. The worked example declares 90%
of its index's weight, priced and with 200 days of history behind it, on every date to the window's
end; on 2000-01-03, its owner's floor, the members Sharadar prices and signals held 98.1% of the KN
US Equity Core, and never less than 96.5% after, so the window opens on the floor. It writes the
coverage per date to `Universe/Coverage.csv` and the window to `Universe/Window.csv`, which the
analyzer and the experiment read rather than retype.

## 5. What the stage hands on

| Output | Consumed by |
| --- | --- |
| `Universe/Security_Master.csv` | `Data/refinery.py`, which joins its columns onto the panel as `current_*` |
| `Universe/Data_Issues.csv` | the caveats table of every `FINDINGS_N.md`, the Data stage's work list, and each experiment's exclusions: the names its blocking rows list |
| The usable date — the example's `Universe/Window.csv` | the analyzer and the experiment, which read it from the file, and `BLUEPRINT_N.md`, as the declared window |
| The coverage per date — the example's `Universe/Coverage.csv` | the survivorship row of `RESULTS.md` and every `FINDINGS_N.md` |

Every table the notebook writes and the provider cache are **regenerable and therefore
gitignored**; `Investable_Universe.csv` is the only committed input. Composition, listing status and
listing age belong here too — a universe whose members mostly listed after the backtest starts is a
different universe from the one the row count suggests.

## What this skill will not let you do

- **Build a universe from today's index members.** It deletes every failure and the backtest
  discovers that markets go up.
- **Let a provider overwrite the seed's identity.** Compare, report the disagreement, and keep the
  seed.
- **Join on a key the index does not use.** Every listing the index weights from the window's
  floor is a row of the seed under `index_identifier`, and the universe notebook's Verify raises
  when one is not.
- **Close a span on its source's last date.** A listing still trading then has no last date.
- **Select on a `current_*` column**, or present a classification-bucketed number without saying it
  is a today-snapshot.
- **Drop a bad identifier silently.** It goes in the register, by name, with the check that caught
  it.
- **Change the seed without a change-set.** Its own commit, changelog entry, and the pipeline re-run
  before a figure from the new universe stands beside one from the old.
- **Use a live KaxaNuk strategy as a worked example.** Examples in this package come only from
  `golden-flow` as the package ships it, never from a live strategy repository.
