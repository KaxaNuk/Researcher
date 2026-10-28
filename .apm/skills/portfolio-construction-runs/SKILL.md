---
name: portfolio-construction-runs
description: >
  Load this skill whenever a book is sized in a KaxaNuk Strategy Template repository — step 4, the rule
  cell and `Experiments/portfolio_construction.py` — or the KaxaNuk Portfolio Construction library is
  installed, configured, called or debugged. Use it when the user asks to pick or compare a sizing
  method (equal weight, inverse volatility, risk parity, HRP, mean-variance, the KN Index), call
  `build_allocator` or `run_pipeline`, build point-in-time eligibility, lag a signal, choose
  rebalance dates, add a no-trade band, a weight cap or a minimum holding count, leave cash to the
  engine, or write the weight file the Backtest Engine reads. It covers installing the library and its licence, the
  per-date weigher and its one causal cut, the traps that make a plausible book wrong, and the
  invariants every rule must pass. It does NOT cover pricing the book (use `backtest-engine-runs`),
  reading what sizing earned (use `alpha-decomposition`), or the documents around the experiment
  (use `experiment-lifecycle`).
metadata:
  version: 0.6.0
  library_version: 1.28.0
---

# Portfolio construction — the library inside one signature, and one cut

**In plain words:** how much of what, and how often you change your mind. **It produces** the
`REBALANCE_DATES x securities` target weights a rule hands to the diagnostics and the weight file.
**It prevents** a good signal in a portfolio nobody could hold — and a weighting difference that
reads as a signal difference because each notebook invented its own sizing.

Written against **KaxaNuk Portfolio Construction 1.28.0**. That build is the frontmatter's
`library_version`: compare it with the installed build `uv pip list` shows, and on a newer minor or
major version treat every trap here as unproven until it is checked again. The library keeps three
questions apart — *who plays* (selection), *how much* (sizing), *when* (timing) — and deliberately
leaves a fourth to its caller: *what was known on the day*. That fourth question is most of this
skill.

**What this skill knows comes from the library's README, its changelog and runs — never from its
code.** The library is licensed: never open, search, print or inspect its installed files, and of
the clone it is installed from read only `README.md`, `CHANGELOG.md` and `examples/`. What none of
them says is not known; a run settles it, and a difference from this file goes to `lab@kaxanuk.mx`.
An error is reported by the call, its type and its message, never by the library's own traceback
lines.

**Changed in 2.0.0, from its changelog — not yet checked by a run here.** The library needs a
licence: `run_pipeline()` checks it first, once per process, for the product
`portfolio-construction`, and without one raises `LicenseNotFoundError`, never wrapped in a
`PipelineError`. The entry script `init excel` installs, `run` / `autorun`, `__main__.py` and the
Docker image all go through it. The changelog and the README name no other call: **whether
`build_allocator`, which section 4's per-date weigher calls, checks the licence is unverified.** The
key is `KNPC_API_KEY_KAXANUK`, in the environment or in a `.kaxanuk_license` file in the home or the
working folder; the entry script does not read `Config/.env`, whatever the missing-key message,
shared with the other two libraries, suggests. `KNPC_LICENSE_SERVER_URL` names another server.
`LicenseError`, `LicenseNotFoundError`, `LicenseValidationError`, `LicenseServerError` and
`LicenseConfigurationError` sit under `PortfolioConstructionError`. A saved check spares the server
for 24 hours and stands in offline for 3 days; a rejection is final; **the first run needs the
network.**

**Changed in 2.0.1, from its changelog — not yet checked by a run here.** Nothing a caller does
changes: the release adds a documentation site and corrects docstrings, with no change to the code,
so the 2.0.0 paragraph above is still what a run has to check. The README links the site —
<https://kaxanuk-portfolio-construction.readthedocs-hosted.com/en/latest/>, a User Guide, a
Methodology and an API Reference — which on 2026-10-18 answered *not found*. Until it answers, the
repository's `README.md`, `CHANGELOG.md` and `examples/` stay the documentation; once it does, read
its pages, never a source page one links to. The User Guide states three behaviours the README did
not: **a rebalance date absent from the data gives a snapshot of nulls, so every ticker is filtered
out**; the KN Index applies `min_weight` only when `max_constituents` is empty; and
`min_constituents` is validated but not enforced. Where a docstring or a registry card says
otherwise, the Methodology follows the code: HRP bisects its leaf order by position, and HERC does
not cut its tree. And the README now agrees with the changelog on three points `references/api.md`
records apart at 1.28.0: `calendars` installs QuantLib, input files are CSV or Parquet, and the
examples live in `examples/`.

## 1. Install it, and keep it installed

The library is **proprietary**: not on public PyPI, its repository `KaxaNuk/Portfolio-Construction`
private. Up to 1.28.0 it had no licence key or environment variable of its own; since 2.0.0 it
needs one, as above. **Without access:** the library comes, with its licence and access to its
repository, in the KaxaNuk Investment Lab, which KaxaNuk sells. For a licence and access, write to
`lab@kaxanuk.mx`, saying what it is for, with *via KaxaNuk Researcher* in the subject —
<https://www.kaxanuk.mx/lab> shows the Lab. (The Lab's access facts: `references/investment-lab.md`
in the `next` skill's folder.) Whoever has access installs it by hand, per machine, from a clone
kept **beside** the strategy — never inside it — and, from 2.0.0, with the index URL of the licence
welcome email, which serves its new dependency, `kaxanuk-license-client`:

```bash
uv pip install -e "<path to the Portfolio-Construction clone>[solver,clustering]" --extra-index-url https://license:{YOUR_LICENSE_KEY}@{SERVER}/simple/
```

- **Never print, echo or commit the key or the index URL**: the command carries a credential — run
  it, do not paste it back. An exposed key is rotated, not edited out.
- **Import `kaxanuk.portfolio_construction`; Python 3.12 or later, as its README says** — a KaxaNuk
  Strategy Template repository's 3.12 or 3.13 suits it, so it needs nothing new.
- **The extras decide which methods exist.** `solver` (cvxpy) for constrained mean-variance, CVaR
  and CDaR; `clustering` (scipy) for HRP, HERC and NCO; `plots` (matplotlib) for figures and the PDF
  report; `calendars` for the exchange-calendar rebalancers — QuantLib, by the changelog, where the
  README names `exchange-calendars`. A missing extra fails at different moments, as the changelog
  records: HRP when it is built, HERC and NCO only when they allocate, and a QuantLib-backed
  rebalancer only when one is used.
- **A research notebook needs no workbook**: configure in code, as the README's quick start, *The
  sixty-second tour*, does.
- **Never add it to a strategy's `pyproject.toml`.** A clone without access must still resolve. And
  as with the engine and attribution, `uv sync` is exact and removes a hand-installed package: after
  a relock use `uv sync --inexact`, and run everything else through `uv run`.

## 2. Guard the import — step 4 still runs without it

```python
import importlib.util

LIBRARY_INSTALLED = importlib.util.find_spec("kaxanuk.portfolio_construction") is not None
```

A clone without the library still builds a book: equal weight needs nothing but the eligible set.
**A method that needs the library, asked for without it, stops the run with a `ModuleNotFoundError`
that names it — never quietly replaced by equal weight**, because a book sized another way is
another experiment.

## 3. The three stages, and the registry

| Stage | Question | The pieces |
| --- | --- | --- |
| Selection | who plays | a `Signal` per date — True, False or null per security — and a `BinaryMatrix` across dates; `LiquidityFilter`, `BinaryFilter`, `ColumnMembershipFilter`, `CompositeUniverseFilter`, `UniverseCreator` |
| Sizing | how much | fourteen methods behind one factory, `build_allocator`, each built by its registry name |
| Timing | when | `CalendarRebalancer`, `FixedDateRebalancer`, `TimeSignalRebalancer`, and the QuantLib-backed rebalancers |

**Null is not zero.** Selection is tri-state, and missing data becomes True or False only through
`MissingDataPolicy`. For a returns history `EXCLUDE` means listwise deletion: a date with a gap in
any eligible security is dropped for all of them. **The library dies loud**: one pinned solver,
`optimal_inaccurate` is an error, an infeasible mandate names the constraint that cannot be met.
Read an error before working around it.

**Ask the registry before choosing a method.** `describe("hrp")` renders what a method needs,
honours and assumes, as the README shows for `cvar`; `requirements_for("hrp")` looks up its registry
entry, and a typo lists every valid name.

| What the method needs | Methods |
| --- | --- |
| nothing but the eligible set | `equal_weight` |
| a column in the snapshot | `feature_weighting` (one number per security), `kn_index` (market cap and rolling traded-value windows) |
| a returns history | `inverse_volatility`, `risk_parity`, `max_diversification`, `mean_variance`, `black_litterman` (plus market cap); `hrp`, `herc`, `nco` with `clustering`; `constrained_mean_variance`, `cvar`, `cdar` with `solver` |

What the README and the changelog say of each method's configuration, bounds and short selling is
in `references/api.md`.

## 4. The contract: one signature, one cut

In a KaxaNuk Strategy Template repository the library is called from **inside** the step-4 shared
module, `Experiments/portfolio_construction.py`, never around it. Every method goes through one
**weigher**, `weigh` in the worked example's module:

```python
weigh(
    selected: tuple[str, ...],              # what may be held on this rebalance date
    history: pandas.DataFrame,              # daily returns, ending STRICTLY BEFORE that date
    method: str,                            # "equal_weight", "proportional_to_score", or a registry name
    maximum_weight: float | None,           # the cap; None switches it off
    score: pandas.Series | None = None,     # where the scheme sizes by one: as it stood BEFORE that date
) -> pandas.Series                          # weights, non-negative, summing to at most 1.0
```

Equal weight, proportional to a score, or a library method built by its registry name is one
`method` string. Swapping one for another is one line in the rule cell, and nothing else in the
notebook moves — which is what makes two experiments comparable rather than merely adjacent.
`weigh` builds a method from its name and the history alone, as the README's
`build_allocator(name="risk_parity", returns=returns)` does. A method that needs a configuration,
or one that reads its columns from the snapshot, such as `feature_weighting` or `kn_index`, needs a
weigher of its own, of the same shape.

**The cut is the module's, made once.** `build_weights` hands `weigh` the rows dated strictly
before the rebalance date, and a score's last row before it; `.loc[:date]` would include the date
itself. A weigher never sees a date, so it has no future to reach for.

**Never let the library make that cut, because it does not.** A returns-based method estimates over
whatever table it was built with, and `run_pipeline` calls one allocator on every date with the same
table, so over a multi-date run the early books are sized on returns that had not happened yet. The
library's own changelog records it — *Known and open after 1.28.0*, 24% future observations in its
integration test — and says to slice the history yourself. So **build one allocator per rebalance
date, on the history already cut**, inside the weigher, as the worked example's `weigh` does:

```python
dated_history = history.rename_axis("date")
history_table = pyarrow.Table.from_pandas(
    dated_history.reset_index(),
    preserve_index=False,
)
allocator = kaxanuk.portfolio_construction.sizing.build_allocator(
    name="risk_parity",
    returns=history_table,
)
eligible_table = pyarrow.table(
    {
        "ticker": list(selected),
    }
)
snapshot = kaxanuk.portfolio_construction.entities.UniverseSnapshot(
    table=eligible_table,
)
allocated = allocator.allocate(
    snapshot=snapshot,
)
allocated_weights = kaxanuk.portfolio_construction.entities.Weights.from_allocated(
    allocated=allocated,
)
weights = pandas.Series(
    allocated_weights.as_mapping(),
)
```

- **The history is wide** — a `date` column, then one column of returns per security — and must
  carry **every** eligible security: a security the history lacks raises, by the changelog, rather
  than being silently dropped. Two complete dates are the only floor the changelog records, and its
  own example, four securities over two dates, gives an HRP book of pure noise.
- **The factory checks the pairing.** A snapshot-only method refuses a `returns` argument and a
  returns-based one refuses to be built without it, so pass the history only when the method's
  registry entry, `requirements_for(name)`, has `history_input="returns"`. Snapshot methods read
  their columns from the snapshot table: put the feature there, as it stood before the date.
- **Weights sum to at most one, not to exactly one.** A method's book sums to its target exposure,
  1.0; the module scales it down when a lever asks for cash, and what the weights leave is cash,
  which the Backtest Engine holds and pays interest on (`backtest-engine-runs`). Nothing eligible is
  an empty book — 100% cash, kept as an all-zero row, because "went to cash" is an instruction the
  engine has to receive.

## 5. Eligibility and timing, point in time

The library lags nothing — its README leaves look-ahead to the analyst — so the order is the
module's, and it is fixed:

- **Lag the eligibility** so the set used on rebalance date *t* is the one observed at *t-1*, filled
  with False so the warm-up holds nothing rather than everything. A security has to have been
  authorised yesterday and be sellable today, and those are two different days on purpose.
- **No day of hindsight for a delisting.** A name is tradable on a rebalance date if it has a price
  to fill at that day. A position whose prices stop is the engine's to sell at its last price
  (`delisted_position_handling = "sell_at_last_price"`), so the rule takes no exit for it. **A gap
  inside a series** is different: the Backtest Engine refuses a rebalance date on which any open
  position has no price, so a book that holds a name through a gap is refused outright, not
  mispriced. The worked example lists such a name as a blocking row of `Universe/Data_Issues.csv`
  and excludes it by name from every book, its weight published, so no book trades off its own
  dates. The older cure — selling at *t−1*, the last priced day, one day of hindsight — is
  `exit_before_price_stops` in its module, no longer called.
- **Rebalance on change** when the rule is event-driven: the days the lagged set changed. A
  `BinaryMatrix` of the lagged signal counts entries and exits per date with `turnover()`. A
  calendar rule takes
  `CalendarRebalancer(trading_dates=..., frequency=RebalanceFrequency.MONTH_END)` on the panel's own
  dates; the worked example's `first_trading_days_of_month` gives the first trading day of each
  month, each decided on the close before it.
- **A no-trade band**, where the blueprint names one: a held name whose target differs from the
  weight it drifted to by no more than the band keeps its drifted weight; entries, exits and larger
  moves trade to target, and what the kept names hold over their targets comes out of the traded
  names in proportion, so the book never exceeds one. It is decided at the close and written at the
  next open, so a kept name's weight can sit outside the bounds by the band plus the overnight move:
  count those excursions. The worked example's `banded_book` does this at half a point, and it is
  read back on two consecutive dates beside the rule's read-back, before the blueprint.

In a KaxaNuk Strategy Template repository the eligible set comes from the refined panel — the rule
builds it from the `r_*` columns — and the library sizes it. If you do use its loaders and
`run_pipeline`, two things are silent until they are not:

- **Warm-up nulls reach the matrix.** A 252-day column is null for its first year, and the README
  keeps a warm-up row null all the way to the matrix, where `EXCLUDE` reads it as *does not play*.
  A date on which nothing plays has nothing to size: by the changelog a `UniverseSnapshot` cannot
  be filtered to an empty universe, and a stage that fails stops the run with a `PipelineError`
  naming the date and the stage. Start after the warm-up.
- **Membership is read per date.** A dated `Classification` queried without `as_of` raises.
  Point-in-time membership comes from a per-date flag column (`BinaryFilter`) or
  `UniverseCreator.build_membership`, which threads each snapshot's date into the classification,
  read per date with `BinaryMatrix.active_on(target_date=..., missing=MissingDataPolicy.EXCLUDE)`.

## 6. Constraints are levers, switched off until the blueprint names them

`build_weights(eligibility, returns, rebalance_dates, method, maximum_weight, minimum_holdings)`
takes the constraints as arguments beside the method, so two methods can be compared without also
changing the constraints; a scheme that sizes by a score takes it as `scores` too:

| Argument | Off | What switching it on means |
| --- | --- | --- |
| `maximum_weight` | `None` | a cap, applied by `weigh`. **What it frees becomes cash**, unless the blueprint sends it to the other names, as the worked example's `bounded_by_score` does. The library's `Weights.cap` redistributes the excess to keep the book fully invested — use it only when the blueprint names that lever |
| `minimum_holdings` | 1 | below it the date holds nothing: the book is cash. The honest response to too few things to hold is to hold less |

Start with every constraint the blueprint does not name **off**, because such a constraint is a
lever a later experiment has to earn against the simpler baseline. Bounds the blueprint names — a
cap and a floor on each weight — are the design, not levers to earn, and the control holds them
too. The library's richer machinery — a `Mandate` with group limits, a tracking-error budget,
Black-Litterman views — is a lever of the same kind: one at a time, each beating the book without
it. The worked example sizes by traded value inside a 20% cap and a 1% floor, by the owner's
design, and in its in-sample backtest the equal-weight arm lost: at the flat 5 bp row, 5.67% a year
at a Sharpe of 0.157, against 7.72% at 0.221.

## 7. The weight file

In a KaxaNuk Strategy Template repository `Experiments/backtest_engine.py` writes
`Portfolio/portfolio_weights.csv`: wide, `Ticker` first, one ISO date per column, every column
summing to at most 1.0, each weight written to six places and rounded down; what a column leaves is
cash, held by the engine. Outside one, the library's output
handlers write the same layout — `Ticker`, then one column per date, the layout the engine detects.
The changelog says the portfolio entity stores tickers normalised: check they still match the
market-data file names.

The attribution library does not read this file: it needs the book's **daily** weights, as the
engine marked them. That hand-off is `attribution-analysis-runs`.

## 8. The invariants every rule must pass

Cheap to check in section 2.1 of the notebook, expensive to discover inside a P&L. Whatever the
method:

- no book is more than fully invested, and none is negatively invested;
- no negative weights, if the strategy is long-only; gross and net within the limits the engine will
  be given, if it is not;
- **every security paid for today had its signal on the prior close** — check the signal itself, not
  the composed eligibility, because the signal is what had to exist in advance;
- every security bought has a price to fill at on the day it is bought;
- no name a blocking row of `Universe/Data_Issues.csv` lists is ever held;
- under a band, every struck weight is its target or a held name's drift within the band, and the
  struck weights the band leaves outside the bounds are counted;
- the control trades only on the rule's dates.

The notebook's section 8, Verify, raises on every one of them.

Run them over **every** book an experiment builds, not only the benchmark's. A variant that holds a
name the benchmark could not is a bug wearing a Sharpe.

## What this skill will not let you do

- **Give a weigher a date**, or a history that reaches the rebalance date.
- **Build one returns-based allocator for many dates**, or run one through `run_pipeline` over a
  multi-date window.
- **Redistribute what a cap frees** unless the blueprint names that lever.
- **Choose a sizing method on the Sharpe it produces** over the window it will be judged on. Choose
  it on a property of the book — concentration, turnover, capacity — and publish the comparison.
- **Swap in equal weight because the library is missing.** Let the error stop the run.
- **Quote a number the engine did not produce.** This module builds weights; `backtest-engine-runs`
  prices them.
- **Use a live KaxaNuk strategy as a worked example.** Examples in this package come only from
  `golden-flow` as the package ships it, never from a live strategy repository.

## Where the documentation is

The library has no public documentation site yet. Its repository carries it: `README.md` for the
principles and the table of its fourteen methods, each one's card a `describe` call away,
`CHANGELOG.md` — read *Known and open* before trusting a feature — and `examples/`.
`references/api.md` is the surface this skill keeps, with the places where the README and the
changelog disagree. Read those, never the package's code.
