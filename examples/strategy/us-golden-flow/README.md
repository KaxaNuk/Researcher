<!-- example: begin -->

# US-Golden-Flow

US-Golden-Flow buys the US stocks of an index that trade the most, but only while each one's price
trend is up, with no sector above half the book. Over 1999 to 2026 its trend filter beat the same
book without it over the whole window, but only in 1999–2008 of the three periods its blueprint
named, so the experiment is **falsified as written**; the book also lost to its index. Nothing is
on paper. Nothing needs installing to read it: *How to read it*, below, says where to start.

> **Hypothetical results.** Every return, Sharpe and drawdown in this README is simulated, never
> traded: no money was at stake, and past returns do not guarantee future returns. They come from a
> backtest on the past prices the strategy was designed on, one of 359 portfolios tested, with
> modelled costs, measured against KaxaNuk's own index. Its limits:
> [`RESULTS.md`, *Known limitations*](RESULTS.md#known-limitations).

**Own the KN US Equity Core stocks the market is trading most, while their trend is up, in
proportion to what they trade** — none above a fifth of the book, none too small to matter, and no
KN sector above half.

> **Status, as curated on 2026-11-25 from US-Golden-Flow 0.8.3: Experiment 1 is falsified as its
> blueprint words it, and nothing is on paper.** In a backtest, net of every cost the engine prices,
> 1999-12-31 to 2026-10-30: 5.58% a year at a Sharpe of 0.143, 7.14% and 0.207 at a flat 5 bp
> half-spread, against 0.124 without the golden cross and 7.93% and 0.306 for the KN US Equity
> Core. It beats its control over the window but in only 1 of 3 sub-periods; P1 and P2 fail at both
> cost rows.

**What it is, and what it is not.** A research and learning tool: a companion for your work and your
projects, and for learning to invest when you want. It is never investment advice: it never tells
you to buy, sell or hold, never trades or moves money, and every decision, and its risk, is yours.
It runs on your computer through your AI assistant; what it reads goes to the company behind that
assistant (Anthropic for Claude, OpenAI for Codex, Google for Antigravity, and for Copilot and
Cursor, GitHub or Cursor and the maker of the model you pick there), never to KaxaNuk, and a copy
goes to your own private GitHub only when you ask. This example is free under the MIT licence, as
is and without warranty; your data provider, your assistant and the Investment Lab's libraries,
which KaxaNuk sells, each have their own terms. Its figures come from a backtest on past prices,
shown to teach the method, never a promise or a recommendation. A falsified book is reported as
loudly as a promising one: that is the point of showing it.

This is the worked example `init-example` copies, built on the
[KaxaNuk Strategy Template](https://github.com/KaxaNuk/Researcher/blob/main/templates/strategy/README.md),
whose README says what each folder is for. It is for reading and running, never for building on; a
strategy of your own starts from `init-strategy`.

## How to read it

| Read | For |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the idea and its three claims |
| [`RESULTS.md`](RESULTS.md) | *The project in three sentences*, then *The uncomfortable one* |
| [`Experiments/Experiment_1/BLUEPRINT_1.md`](Experiments/Experiment_1/BLUEPRINT_1.md) | the hypothesis, fixed before the run |
| [`Experiments/Experiment_1/FINDINGS_1.md`](Experiments/Experiment_1/FINDINGS_1.md) | what the run found, and the gate read row by row |
| [`PIPELINE.md`](PIPELINE.md) | how the code runs, step by step, and how to debug it |

[`JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md) is the full story, from the owner's
decisions of 2026-11-16 through four versions of Experiment 1. In the other documents,
US-Golden-Flow's own text follows the template guidance it answers.

**A key to older text.** US-Golden-Flow rebuilt Golden-Flow, the package's earlier example, in the
KaxaNuk Investment Lab: "Golden-Flow" in these files is that strategy, and its 152 books count in
the trials. Versions such as 0.4.0 named here are US-Golden-Flow's own.

## Words used here

- **Golden cross**: a stock's 50-day average price above its 200-day one; here, the trend filter
  that makes a name eligible.
- **Book**: the portfolio a rule holds day by day — which stocks, and how much of each.
- **Sector cap**: no KN sector above half the book, the rule's risk limit.
- **Top-up**: a delisted name's cash put back into the names held, two trading days after its
  last price.
- **Sharpe**: return per unit of risk taken, excess of cash, as the Backtest Engine reports it;
  higher is better.
- **Seed**: `Universe/Investable_Universe.csv`, every listing the index held, departed ones
  included, by Sharadar's ticker and its first and last price dates.
- **Control**: the same rule with one ingredient off, here the golden cross, on the rule's dates.
- **Factor exposure**: return the factor model explains, such as the market, size and momentum.
- **Idiosyncratic**: the return left once factor exposure is taken out.
- **Brinson-Fachler**: splits the excess return into weighting (allocation) and picking (selection).
- **Soundness, S1 to S5**: the first layer of the graduation gate in `Paper_Trading/BITACORA.md` —
  no survivorship bias, no look-ahead, no overfitting, costs and capacity stated, reproducible.
- **Performance, P1 to P3**: the second layer — beats its benchmarks and its control over the whole
  window, idiosyncratic alpha in both layers of attribution, conclusions that survive perturbation.
- **Falsified**: the condition the blueprint named before the run happened.
- **In sample**: measured on the history the rule was chosen on.
- **Benchmark index**: the KN US Equity Core, which every alpha here is measured against.

## The rule, in one table

| Decision | Rule | Where it is named |
| --- | --- | --- |
| Universe | a member of the KN US Equity Core at the prior close, keyed by Sharadar's ticker, delisted names kept | the index's daily holdings, read by `Data/hand_supplied.py` through the seed `Universe/Investable_Universe.csv` |
| Prices | Sharadar, the adjustment rebuilt by the Curator from the exact close and Sharadar's actions, spin-offs added | `Data/Curator/custom_calculations.py`, `Data/curator.py` |
| Eligibility | a member with its golden cross at 1 at the prior close, and an open on the rebalance date | `c_eligible_golden_cross_50_200`, a Curator column |
| Ranking and sizing | by 63-day average traded value, in proportion to it; no weight above 20%, none below 1%, no KN sector above 50% | `c_traded_value_sma_63d`; `portfolio_construction.bounded_by_score_and_sector` |
| Rebalancing | the first trading day of each month, at the open; a held name left as it drifted when its target moved half a point or less; each book struck 99.5% invested | `portfolio_construction.banded_book` |
| Delistings | the engine sells at the last price; the cash goes into the names held on the second trading day after | `portfolio_construction.delisting_top_up_dates` |
| Cash | a 1% reserve in the engine, paid FRED's Fed funds rate less half a point | `backtest_engine` |
| Costs | commission 1 bp and the engine's spread-and-impact slippage, with a flat 5 bp re-pricing beside it | `backtest_engine.build_configuration` |
| Benchmarks | the **KN US Equity Core** first, then `SPY` | the engine's identifiers |
| Window | 1999-12-31 to 2026-10-30, 323 monthly rebalance dates | `Universe/universe_marimo.py`, `Universe/Window.csv` |

Each decision is the owner's, recorded in their words in
[`Experiments/Experiment_1/JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md) before the run that
uses it. The hypothesis — the predictions, the control that differs from the rule in the golden
cross alone, and what would falsify it — is `Experiments/Experiment_1/BLUEPRINT_1.md`.

## How US-Golden-Flow uses the Lab and the Analytics Factory

| Step | Lab library or Factory file | What US-Golden-Flow does | Skill for your own strategy |
| --- | --- | --- | --- |
| 1. Bibliotheca | — | the idea in the owner's words, three claims, and eighteen public papers that argue with them | `read`, `objective` |
| 2. Universe | the KN US Equity Core's daily holdings, from the Analytics Factory | `Universe/seed.py` writes the seed, tickers and dates only; `Universe/universe_marimo.py` profiles the download and fixes the window | `universe-point-in-time` |
| 3. Data | **Data Curator**, open source | the Curator downloads Sharadar's prices and computes every signal the rule reads as a `c_*` column; `Data/analyzer_marimo.py` screens them | `data-curator-custom-calculations`, `data-analyzer-runs` |
| 4. Portfolio | **Portfolio Construction**, licensed | the strategy's own weigher sizes the book; `compare_library_sizing.py` shows the library gives the same book | `portfolio-construction-runs` |
| 5. Backtest | **Backtest Engine**, licensed | prices the rule, its control, equal weight and the uncapped arm, and twenty random books, at two cost rows | `backtest-engine-runs` |
| 6. Attribution | **Attribution Analysis**, licensed; the KN US Equity Factor Model | Brinson-Fachler by KN sector, the factor model, Brinson-Fachler on the residual | `attribution-analysis-runs`, `alpha-decomposition` |
| 7. Paper trading | — | the gate read row by row; falsified, nothing on paper | `paper-trading-gate` |
| 8. Production | — | nothing here deploys | — |

> The Backtest Engine, Attribution Analysis and Portfolio Construction come together, with their
> licences, in the KaxaNuk Investment Lab, which KaxaNuk sells: write to `lab@kaxanuk.mx`.

**The Analytics Factory** is KaxaNuk's benchmark portfolios and factor models:
<https://www.kaxanuk.mx/analytics>; ask `analytics@kaxanuk.mx` for them. Step 3 of
[`SETUP.md`](SETUP.md) says where a strategy reads them from.

## Run it

**Before you run**, `Config/.env` holds the Sharadar key, the licence keys and
`KN_ANALYTICS_PATH`, as steps 2 and 3 of [`SETUP.md`](SETUP.md) set out. Without the licences the
experiment writes the books' weights and skips the rest.

[`PIPELINE.md`](PIPELINE.md), *The run, in order*, gives every command with what it reads, writes
and how long it takes. In short, from the repository root:

```bash
uv run python Config/install_libraries.py
uv run python Universe/seed.py
uv run python Data/curator.py
uv run python Universe/universe_marimo.py
uv run python Data/analyzer_marimo.py
uv run python Experiments/Experiment_1/experiment_1_marimo.py
uv run python Experiments/Experiment_1/attribute_base_books.py
uv run python Experiments/Experiment_1/app_workbooks.py
```

- **Every notebook is a marimo notebook**: run it as a script, or open it with
  `uv run marimo edit <file>`. Its outputs are never saved in the file. Each ends in a Verify
  section that raises.
- **`Universe/seed.py` comes first**, even though the seed is committed: it fetches Sharadar's
  catalogue, which the universe notebook reads, and writes the seed again, tickers and dates only.
- **The seed here is public**, so the universe notebook reads its name, permaticker and match
  columns as empty, and says so; no figure depends on them.
- **This copy has not been run from a wiped copy**: its figures are US-Golden-Flow's, reproduced
  there from a wiped working copy on 2026-11-20, and its code is that run's.

## What a correct run shows

The figures of US-Golden-Flow's runs of 2026-11-20 and 2026-11-24. A fresh download rebases the
adjusted columns, so a Sharpe can move in its third decimal; that is the provider's restatement,
not the example breaking.

| Stage | A correct run shows | Recorded in |
| --- | --- | --- |
| The seed | 2,203 listings, delisted ones kept | `FINDINGS_1.md`, S1 |
| `Universe/universe_marimo.py` | every member priced every day, at least 99.997% of the index's weight; `ARXS`, `CBRS`, `FDXF`, `FPS`, `H1`, `ILA.A`, `PS` and `SUNB` excluded by name, as blocking rows of `Universe/Data_Issues.csv` | `RESULTS.md`, U6; `FINDINGS_1.md` |
| `experiment_1_marimo.py` | 323 monthly rebalance dates and 36 top-ups, a median of 43 names, each book struck 99.3% to 99.6% | `FINDINGS_1.md` |
| `experiment_1_marimo.py` | Verify passing, 39 checks on the four base books; 20 engine runs read, then 40 more with the random books, 9 excluded by name | `FINDINGS_1.md` |
| `git status` | new only `uv.lock`, which `uv sync` writes, and the seed changed only where a newer catalogue moved a live listing's date | `SETUP.md` |

A fresh download can add a blocking row to `Universe/Data_Issues.csv`, and the experiment's Verify
then stops on the exclusions. That is the provider's data moving, not the example breaking: read
the new row first.

<!-- example: end -->
