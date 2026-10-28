<!-- example: begin -->

# Golden Flow

Golden Flow buys the stocks of a US index that trade the most, but only while each one's price
trend is up. Over 2000 to 2026 its trend filter earned its keep against the same book without it,
and the book still lost to its index: all of the shortfall came in 2000–2008, and since 2018 it has
beaten the index. Its gate reads it as **sound and regime-dependent**, so it is not paper traded.
Nothing needs installing to read it: *How to read it*, below, says where to start.

> **Hypothetical results.** Every return, Sharpe and drawdown in this README is simulated, never
> traded: no money was at stake, and past returns do not guarantee future returns. They come from a
> backtest on the past prices the strategy was designed on, one of 152 portfolios tested, with
> modelled costs, measured against KaxaNuk's own index. Its limits:
> [`RESULTS.md`, *Known limitations*](RESULTS.md#known-limitations).

**Own the KN US Equity Core stocks the market is trading most, while their trend is up, in
proportion to what they trade** — none above a fifth of the book, none too small to matter.

> **Status, as curated on 2026-10-27: Experiment 1 ran in sample on Sharadar and reads as sound and
> regime-dependent; it does not graduate, and no book is on paper.** In a backtest, net of every
> cost the engine prices, 2000-01-03 to 2026-08-14: 6.21% a year at a Sharpe of 0.162, 7.72% and
> 0.221 at a flat 5 bp half-spread, against 0.097 without the golden cross and 8.12% and 0.315 for
> the KN US Equity Core. The whole shortfall is 2000–2008; since 2018 it beats the Core.

**What it is, and what it is not.** A research and learning tool: a companion for your work and your
projects, and for learning to invest when you want. It is never investment advice: it never tells
you to buy, sell or hold, never trades or moves money, and every decision, and its risk, is yours.
It runs on your computer through your AI assistant; what it reads goes to the company behind that
assistant (Anthropic for Claude, OpenAI for Codex, Google for Gemini), never to KaxaNuk, and a copy
goes to your own private GitHub only when you ask. It is free under the MIT licence, as is and
without warranty; your data provider, your assistant and the Investment Lab's libraries, which
KaxaNuk sells, each have their own terms. The worked example's figures come from a backtest on past
prices, shown to teach the method, never a promise or a recommendation. A sound, regime-dependent
book is not a recommendation either: whether to use one, paired with another signal or at a
portfolio manager's discretion, is a person's decision, and its risk is theirs.

This is the worked example `init-example` copies, built on the
[KaxaNuk Strategy Template](https://github.com/KaxaNuk/Researcher/blob/main/templates/strategy/README.md):
eight steps as a folder structure, whose README says what each folder is for. It is for reading and
running, never for building on; a strategy of your own starts from `init-strategy`.

## How to read it

| Read | For |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the idea and its three claims |
| [`RESULTS.md`](RESULTS.md) | *The project in three sentences*, then *The uncomfortable one* |
| [`Experiments/Experiment_1/BLUEPRINT_1.md`](Experiments/Experiment_1/BLUEPRINT_1.md) | the hypothesis, fixed before the run |
| [`Experiments/Experiment_1/FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) | what the run found |
| [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) | the gate, both layers, read row by row |

[`JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md) is the full story. Start with its entries
of 2026-10-23 and 2026-10-24: the owner's decisions, the rule read back, the critic, and the three
runs. In the other documents, Golden Flow's own text follows the template guidance it answers.

**A key to older text.** Versions such as 0.15.0 and 0.16.0 named in these files are Golden Flow's
own; the earlier ones, on FMP from 2015 and on another index, are rows of `RESULTS.md` and are not
in this copy. "The desk" is KaxaNuk's Analytics Factory. "The worked example" in text dated before
2026-10-07 is the package's earlier one.

## Words used here

- **Golden cross**: a stock's 50-day average price above its 200-day one; here, the trend filter
  that makes a name eligible.
- **Book**: the portfolio a rule holds day by day — which stocks, and how much of each.
- **Paper trading**: a frozen book run on days after the freeze, with no money in it. Only a book
  that graduates is paper traded; this one is not.
- **Sharpe**: return per unit of risk taken, excess of cash, as the Backtest Engine reports it;
  higher is better.
- **Seed**: `Universe/Investable_Universe.csv`, every listing in the index at any time from
  1998-12-31, departed ones included, by Sharadar's ticker and its first and last price dates.
  Every stock the book holds comes from it; what the bounds cannot place is US dollar cash.
- **Control**: the same rule with one ingredient off, here the golden cross, on the rule's dates.
- **Factor exposure**: return the factor model explains, such as the market, size and momentum.
- **Idiosyncratic**: the return left once factor exposure is taken out.
- **Brinson-Fachler**: splits the excess return into weighting (allocation) and picking (selection).
- **Soundness, S1 to S5**: the first layer of the graduation gate in `BITACORA.md` — no
  survivorship bias, no look-ahead, no overfitting, costs and capacity stated, reproducible.
- **Performance, P1 to P3**: the second layer — beats its benchmarks and its control over the whole
  window, idiosyncratic alpha in both layers of attribution, conclusions that survive perturbation.
- **Sound and regime-dependent**: every soundness criterion holds, and performance holds only in
  named periods. Not paper traded alone.
- **In sample**: measured on the history the rule was chosen on.
- **Information coefficient**: the rank correlation of a feature with the returns that follow it.
- **The first rule's book**: Experiment 1's, the first rule tested against the benchmark; every
  later experiment is measured against it too.
- **Benchmark index**: the KN US Equity Core, which every alpha here is measured against.

## The rule, in one table

| Decision | Rule | Where it is named |
| --- | --- | --- |
| Universe | a member of the KN US Equity Core at the prior close, keyed by Sharadar's ticker, delisted names kept | the index's daily holdings from 1998-12-31, read by `Data/hand_supplied.py` through the seed `Universe/Investable_Universe.csv` |
| Prices | Sharadar, with the adjustment rebuilt by the Curator from the exact unadjusted close and Sharadar's dividends and splits, spin-offs added from its actions file | `Data/Curator/custom_calculations.py`, `Data/curator.py` |
| Eligibility | the golden cross holds at the month's last close: the 50-day average of the adjusted close above the 200-day, read as a state, not a crossing; an open on the rebalance date | `r_trend_50_200 > 0`, the Refinery |
| Ranking and sizing | by 63-day average traded value, the close times the volume, weighted in proportion to it; no weight above 20% and none below 1%, so names are added in rank order while the smallest weight stays at 1% or more | `r_traded_value_sma_63d`, the Refinery |
| Rebalancing | the first trading day of each month, at the open; a held name is left as it drifted when its target moved by half a point or less | `portfolio_construction.first_trading_days_of_month`, `banded_book` |
| Cash | what the bounds cannot place is US dollar cash, paid by the engine at FRED's Fed funds rate less half a point, as Interactive Brokers pays | `backtest_engine.CASH_RATE_IDENTIFIER`, `CASH_INTEREST_SPREAD` |
| Costs | commission 1 bp of the notional and the engine's spread-and-impact slippage, with a flat 5 bp re-pricing beside it, all inside the engine | `backtest_engine.build_configuration` |
| Benchmarks | the **KN US Equity Core** first, every alpha measured against it, then `SPY` | `KN_US_Equity_Core`, the engine's identifier for the index |
| Window | 2000-01-03 to 2026-08-14, the floor confirmed by the coverage rule (members priced and signalled hold at least 90% of the index's weight) | `Universe/universe_marimo.py` fixes the first date before any rule exists |

Each of those is the owner's decision of 2026-10-23, recorded in his words in
[`Experiments/Experiment_1/JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md) before any stage
ran. The hypothesis — the predictions, the control that differs from the rule in the golden cross
alone, and what would falsify it — is in `Experiments/Experiment_1/BLUEPRINT_1.md`, committed on
its own before the rule cell held code; the record is `FINDINGS_1.md`.

## How Golden Flow uses the Lab and the Analytics Factory

| Step | Lab library or Factory file | What Golden Flow does | Skill for your own strategy |
| --- | --- | --- | --- |
| 1. Bibliotheca | — | the idea in the owner's words, three claims, and the notes that argue with them | `read`, `objective` |
| 2. Universe | the KN US Equity Core's daily holdings, from the Analytics Factory | `Universe/seed.py` writes the seed, tickers and dates only, from the holdings and Sharadar's catalogue; `Universe/universe_marimo.py` profiles the download and fixes the window's first day | `universe-point-in-time` |
| 3. Data | **Data Curator**, open source; **Data Refinery** and **Data Analyzer**, coming | the Curator downloads Sharadar's prices and rebuilds the adjustment; until the other two ship, `Data/refinery.py` builds the two features and `Data/analyzer_marimo.py` screens them | `data-curator-custom-calculations`, `data-analyzer-runs` |
| 4. Portfolio | **Portfolio Construction**, licensed: not installed | the strategy's own weigher sizes the book inside the bounds, and the band leaves small moves alone | `portfolio-construction-runs` |
| 5. Backtest | **Backtest Engine**, licensed | prices the book, its control and the other books it is compared with, with commission, slippage and the cash's interest inside it, against the KN US Equity Core and `SPY` | `backtest-engine-runs` |
| 6. Attribution | **Attribution Analysis**, licensed; the Core's holdings and returns and the KN US Equity Factor Model, from the Analytics Factory | Brinson-Fachler by KN sector, then the factor model, then Brinson-Fachler on what the factors leave | `attribution-analysis-runs`, `alpha-decomposition` |
| 7. Paper trading | the Data Curator, the Backtest Engine and the Factory's files, when a book runs | the gate read row by row: sound and regime-dependent, so no book is frozen; the step-7 scripts are here, working, with none to run | `paper-trading-gate` |
| 8. Production | — | nothing here deploys | — |

`experiment-lifecycle` holds the documents around the steps: the blueprint, the journal and the
findings. When a library ships, the example moves to it in a new version.

> The Backtest Engine, Attribution Analysis and Portfolio Construction come together, with their
> licences, in the KaxaNuk Investment Lab, which KaxaNuk sells: write to `lab@kaxanuk.mx`.

**The Analytics Factory** is KaxaNuk's benchmark portfolios and factor models, which a strategy may
read as its universe, its benchmark and attribution's inputs: <https://www.kaxanuk.mx/analytics>;
ask `analytics@kaxanuk.mx` for them. Step 3 of [`SETUP.md`](SETUP.md) says where a strategy
reads them from.

## Run it

**Before you run**, `Config/.env` holds the Sharadar key, the two licence keys and
`KN_ANALYTICS_PATH`, as steps 2 and 3 of [`SETUP.md`](SETUP.md) set out:

- **A Sharadar key**, `KNDC_API_KEY_SHARADAR`. Sharadar is this experiment's only provider, and its
  tickers are the seed's main identifier; it keeps the securities that left the market, which is
  what lets the universe carry its dead.
- **The Analytics Factory's KN US Equity Core holdings and returns**, without which only the
  download runs, and **its KN US Equity Factor Model**, for step 6.
- **The Backtest Engine and Attribution Analysis licences**, for steps 5 and 6. Without them the
  experiment writes the book's weights and skips the rest.

From the repository root, each command reading what the one before it wrote:

```bash
uv sync --group notebook --inexact
uv run python Universe/seed.py
uv run python Data/curator.py
uv run python Universe/universe_marimo.py
uv run python Data/refinery.py
uv run python Data/analyzer_marimo.py
uv run python Experiments/Experiment_1/experiment_1_marimo.py
```

- **Every notebook is a marimo notebook**: run it as a script, as above, or open it with
  `uv run marimo edit <file>` to read and run it cell by cell. Its outputs are never saved in the
  file, so nothing has to be stripped. Each ends in a Verify section that raises.
- **The curator is one fetch, from 1998-01-02 to 2026-08-14, fixed**; the backtest window is cut
  from it. It is resumable: run it again and it asks only for the names that have no file yet.
- **The universe notebook sits between the two Data commands**, because it profiles what the
  curator downloaded and writes the security master the refinery joins.
- **`Universe/seed.py` comes first**, even though the seed is committed. It fetches Sharadar's
  tickers catalogue into `Universe/Provider_Cache/`, which the universe notebook reads for each
  listing's name and permanent identifier, and writes the seed again from the index's holdings,
  tickers and dates only. A newer catalogue can move a live listing's last date: `git diff` shows
  it.
- **Step 7 has no book to run.** `Paper_Trading/promote.py` freezes only an experiment that
  graduates, and `BOOKS` in `Paper_Trading/daily_update.py` is empty, for the reasons
  [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) gives.

## What a correct run shows

These are the record run's figures, of 2026-10-23 and 2026-10-24, from a working copy whose data
folders were emptied first. A fresh download rebases the adjusted columns, so a Sharpe can move in
its third decimal; that is the provider's restatement, not the example breaking.

| Stage | A correct run shows | Recorded in |
| --- | --- | --- |
| The index's holdings | 2,199 listings from 1998-12-31 | `JOURNAL_1.md`, 2026-10-23 |
| `Data/curator.py` | every file checked against Sharadar's own adjusted close where its decimals allow; volume adjusted twice at 82 splits in 77 listings, corrected | `JOURNAL_1.md`, `RESULTS.md` row 16 |
| `Universe/universe_marimo.py` | 2,198 listings priced, `UB` not in Sharadar; the window opening on 2000-01-03, 98.1% of the Core priced and signalled, never below 96.5% | `JOURNAL_1.md`, `RESULTS.md` rows 14 and 15 |
| `Universe/universe_marimo.py` | `FPS`, `H1`, `ILA.A`, `MDLN`, `Q`, `SUNB` and `TXCCQ` excluded by name, as blocking rows of `Universe/Data_Issues.csv` | `JOURNAL_1.md` |
| `Data/analyzer_marimo.py` | `RESULTS.md`, *Before any experiment*, rows 1 to 17 | `RESULTS.md` |
| `experiment_1_marimo.py` | 320 rebalance dates, a median of 43 names; 102 engine runs, 81 read and 21 excluded by name | `FINDINGS_1.md`, `JOURNAL_1.md` |
| `experiment_1_marimo.py` | its Verify section passing, 71 checks | `FINDINGS_1.md` |
| `git status` | new only `uv.lock`, which `uv sync` writes, and the seed changed only where a newer catalogue moved a live listing's date | `SETUP.md` |

A fresh download can add a blocking row to `Universe/Data_Issues.csv`, and the experiment's Verify
then stops on the exclusions. That is the provider's data moving, not the example breaking: read
the new row first.

<!-- example: end -->
