<!-- example: begin -->

# Golden Flow

Golden Flow buys the stocks of a US index that trade the most, but only while each one's price
trend is up. On the history it was built on, it beat its index, mostly by taking market risk. The
trend filter's real job was cutting losses in crashes: a worst fall of −32.5%, against −46.3%
without it. Nothing needs installing to read it: *How to read it*, below, says where to start.

> **Hypothetical results.** Every return, Sharpe and drawdown in this README is simulated, never
> traded: no money was at stake, and past returns do not guarantee future returns. All but one
> come from a backtest on the past prices the strategy was designed on, one of 107 portfolios
> tested, with modelled costs, measured against KaxaNuk's own index. The one: just after the
> backtest's window, before the book was frozen, the engine has it at a 24.9% drawdown from
> 2026-06-22 to 2026-07-29, against 2.0% for `SPY`. Its limits:
> [`RESULTS.md`, *Known limitations*](RESULTS.md#known-limitations).

**Own the KN US Equity Core stocks the market is trading most, while their trend is up, in
proportion to what they trade** — none above a fifth of the book, none too small to matter.

> **Status, as copied on 2026-10-07: Experiment 1 ran in sample and passed criteria 1 to 4 of its
> gate; its book was frozen for paper trading on 2026-10-06 and is kept here as a record.**
> In a backtest, net of costs, 2015-01-02 to 2026-06-01: 20.33% a year at a Sharpe of 0.842,
> against 19.73% and 0.763 without the golden cross and 13.05% and 0.713 for the KN US Equity
> Core. Nine tenths of the excess is factor exposure, and the control won 2023 to 2026.

**What it is, and what it is not.** A research and learning tool: a companion for your work and your
projects, and for learning to invest when you want. It is never investment advice: it never tells
you to buy, sell or hold, never trades or moves money, and every decision, and its risk, is yours.
It runs on your computer through your AI assistant; what it reads goes to the company behind that
assistant (Anthropic for Claude, OpenAI for Codex, Google for Gemini), never to KaxaNuk, and a copy
goes to your own private GitHub only when you ask. It is free under the MIT licence, as is and
without warranty; your data provider, your assistant and the Investment Lab's libraries, which
KaxaNuk sells, each have their own terms. The worked example's figures come from a backtest on past
prices, shown to teach the method, never a promise or a recommendation.

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
| [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) | the gate, and the owner's sign-off |

[`JOURNAL_1.md`](Experiments/Experiment_1/JOURNAL_1.md) is the full story. Start with its entries
of 2026-10-06: the owner's decisions, the critic, and the third and fourth runs. In the other
documents, Golden Flow's own text follows the template guidance it answers.

**A key to older text.** Versions such as 0.13.0 and 0.14.0 named in these files are Golden Flow's
own earlier versions, on another index, and are not in this copy. "The desk" is KaxaNuk's Analytics
Factory. "The worked example" in text dated before 2026-10-07 is the package's earlier one.

## Words used here

- **Golden cross**: a stock's 50-day average price above its 200-day one; here, the trend filter
  that makes a name eligible.
- **Book**: the portfolio a rule holds day by day — which stocks, and how much of each.
- **Paper trading**: the frozen book run on days after the freeze, with no money in it.
- **Sharpe**: return per unit of risk taken, as the Backtest Engine reports it; higher is better.
- **Seed**: `Universe/Investable_Universe.csv`, the listings in the index at any time from
  2015-01-02 whose FMP symbol, verified or not, is the index's own ticker, delisted ones included;
  FMP does not carry about 80 of them, and the register names them as missing. Every stock the
  book holds comes from it, and its cash is `BIL`.
- **Control**: the same rule with one ingredient off, here the golden cross, on the rule's dates.
- **Factor exposure**: return the factor model explains, such as the market, size and momentum.
- **Idiosyncratic**: the return left once factor exposure is taken out.
- **Brinson-Fachler**: splits the excess return into weighting (allocation) and picking (selection).
- **Kill switch**: the result on paper days that retires the book instead of tuning it.
- **In sample**: measured on the history the rule was chosen on; only days after the freeze are not.
- **Criteria 1-5**: the graduation gate, in `BITACORA.md`; the fifth is the owner's signature.
- **Information coefficient**: the rank correlation of a feature with the returns that follow it.
- **t−1**: the trading day before day t; every signal is read at its close.
- **The first rule's book**: Experiment 1's, the first rule tested against the benchmark; every
  later experiment is measured against it too.
- **Benchmark index**: the KN US Equity Core, which every alpha here is measured against.

## The rule, in one table

| Decision | Rule | Where it is named |
| --- | --- | --- |
| Universe | a member of the KN US Equity Core at the prior close: about 600 US stocks a day, from KaxaNuk's Analytics Factory | the seed, `Universe/Investable_Universe.csv`, read by `Data/hand_supplied.py` |
| Eligibility | the golden cross at the prior close: the 50-day average of the adjusted close above the 200-day | `r_trend_50_200 > 0`, from `Data/refinery.py` |
| Ranking and sizing | by 63-day average traded value, weighted in proportion; no weight above 20%, none below 1% | `r_traded_value_sma_63d`, from `Data/refinery.py` |
| Rebalancing | only on the days the held set changes | `portfolio_construction.rebalance_dates_on_change` |
| Exits | a name whose prices are about to stop is sold the day before, at t−1 | `portfolio_construction.exit_before_price_stops` |
| Cash | when fewer than five names are eligible, what the 20% cap cannot place is held in `BIL` | `backtest_engine.CASH_IDENTIFIER` |
| Benchmarks | the KN US Equity Core first, every alpha measured against it; then `SPY` | `KN_US_Equity_Core`, the engine's identifier for the index |
| Window | from the later of 2015-01-02 and the first day from which priced members hold 90% of the index's weight on every day to the window's end, to 2026-06-01 | `Universe/universe.ipynb`, before any rule exists |

Each row is the owner's decision. Most were taken on 2026-10-05, before any stage ran, and are
quoted in `JOURNAL_1.md`. Rebalancing and cash are in the plan the owner approved that day, as
`BLUEPRINT_1.md` says. The exit came on 2026-10-06, after the cycle's first run.

## How Golden Flow uses the Lab and the Analytics Factory

| Step | Lab library or Factory file | What Golden Flow does | Skill for your own strategy |
| --- | --- | --- | --- |
| 1. Bibliotheca | — | the idea in the owner's words, three claims, and the notes that argue with them | `read`, `objective` |
| 2. Universe | the KN US Equity Core's daily holdings, from the Analytics Factory | the record's seed listed every member listing, 888 of its 896 with an FMP symbol; this copy's keeps 883 of the 896, tickers and dates only; `Universe/universe.ipynb` fixes the window's first day | `universe-point-in-time` |
| 3. Data | **Data Curator**, open source and free; **Data Refinery** and **Data Analyzer**, coming | the Curator downloads FMP prices; until the other two ship, `Data/refinery.py` builds the two features and `Data/analyzer.ipynb` screens them | `data-curator-custom-calculations`, `data-analyzer-runs` |
| 4. Portfolio | **Portfolio Construction**, licensed: not installed | the strategy's own `bounded_book` sizes the book; `weigh` shows where the library's call goes | `portfolio-construction-runs` |
| 5. Backtest | **Backtest Engine**, licensed | prices the book, its control and the other books it is compared with, net of costs, against the KN US Equity Core and `SPY` | `backtest-engine-runs` |
| 6. Attribution | **Attribution Analysis**, licensed; the Core's holdings and returns and the KN US Equity Factor Model, from the Analytics Factory | Brinson-Fachler, then the factor model, then Brinson-Fachler on what the factors leave | `attribution-analysis-runs`, `alpha-decomposition` |
| 7. Paper trading | the Data Curator, the Backtest Engine and the Factory's files, when a book runs | the book was frozen on 2026-10-06 and is kept here as a record, not run | `paper-trading-gate` |
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

**Before you run**, `Config/.env` holds the FMP key, the two licence keys and `KN_ANALYTICS_PATH`,
as steps 2 and 3 of [`SETUP.md`](SETUP.md) set out:

- **An FMP key.** FMP is this experiment's provider, and its symbols are the seed's main
  identifier. A later experiment may use Sharadar, LSEG or another provider, with the main
  identifier KaxaNuk supplies for it.
- **The Analytics Factory's KN US Equity Core holdings and returns**, without which only the
  download runs, and **its KN US Equity Factor Model**, for step 6.
- **The Backtest Engine and Attribution Analysis licences**, for steps 5 and 6. Without them the
  experiment writes the book's weights and skips the rest.

**Without an FMP key, Yahoo Finance can run it for learning, though not as it stands.** The Data
Curator's Yahoo Finance extension needs no key:
`uv pip install kaxanuk.data_curator_extensions.yahoo_finance`, then, in `Data/curator.py`,
`kaxanuk.data_curator_extensions.yahoo_finance.YahooFinance()` in place of both
`FinancialModelingPrep(...)` calls. Two things do not work as they stand, and your assistant can
change them with you:

- `Universe/universe.ipynb` asks FMP for each symbol's profile, with the FMP key.
- Yahoo sends split-adjusted prices and volume and the adjusted close, with no unadjusted price and
  no VWAP. From those the record builds the traded value the rule ranks and sizes by, the fill at
  the adjusted VWAP, and the commission, charged per share on the unadjusted VWAP. Those columns
  come back empty until they are built another way, and the trades are then not costed as the
  record costed them.

Yahoo also has no data for the 178 names in the seed that left the market, so the run carries the
survivorship bias those names are kept to prevent. It teaches the process, not the result. For a
precise experiment, use FMP, which the record used, or Sharadar or LSEG. Yahoo Finance's data is
for learning, under Yahoo's own terms.

From the repository root, each command reading what the one before it wrote:

```bash
uv sync --group notebook --inexact
uv run python Data/curator.py --end-date 2026-10-05
uv run python Data/curator.py --end-date 2026-10-05
uv run jupyter nbconvert --to notebook --execute --output-dir ../golden-flow-runs Universe/universe.ipynb
uv run python Data/refinery.py
uv run jupyter nbconvert --to notebook --execute --output-dir ../golden-flow-runs Data/analyzer.ipynb
uv run jupyter nbconvert --to notebook --execute --output-dir ../golden-flow-runs Experiments/Experiment_1/experiment_1.ipynb
```

- **The curator runs twice.** The second pass asks again for every name still without a file, so a
  name FMP refused for a rate limit or a timeout is not booked as one it does not carry.
- **The notebooks write their executed copies to `../golden-flow-runs`**, so the tracked notebooks
  stay stripped. Each ends in a Verify section that raises.
- **`Universe/seed.py` is not part of the run.** The seed is committed; the script shows how it was
  built, and needs the index's master of listings, a file the Analytics Factory can provide.
- **`Paper_Trading_1` is a record** of the book frozen on 2026-10-06, not run from this copy, for
  the reasons [`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) gives. `promote.py 1`
  refuses, and `daily_update.py --dry-run --skip-refresh` stops and exits 2: with no data, at its
  first check; with the data, on `unfrozen-input`. The frozen security master is not in the copy,
  and neither the book's seed, rewritten in this copy as tickers and dates, nor
  `Data/Curator/custom_calculations.py` matches `FREEZE.json`, which is never edited. Without
  `--skip-refresh` it first downloads every price again.

## What a correct run shows

These are the record run's figures, of 2026-10-06, from a wiped working copy. A fresh download
rebases the adjusted columns, and a run of this copy lands further from these than that alone
would. Its seed leaves out 13 of the record's listings, `BRK-B` among them. On 2015-01-02 the
members it prices hold, by estimate, near 91% of the index's weight against the record's 92.97%,
close to the 90% floor. The window may open later than 2015-01-02; then every figure after it
moves, and the experiment's Verify stops on "the window is the universe notebook's".

| Stage | A correct run shows | Recorded in |
| --- | --- | --- |
| The index's holdings | 1,399 listings, 2000-01-03 to 2026-08-14 | `JOURNAL_1.md` |
| `Data/curator.py` | 885 names asked on this copy's seed: 883 symbols, about 80 of them not carried by FMP, `BIL` and `SPY`. The record's seed asked 892: 809 downloaded, 83 that FMP does not carry | `JOURNAL_1.md`, `CHANGELOG.md` |
| `Universe/universe.ipynb` | the 13 listings the seed leaves out named in `Universe/Data_Issues.csv`, `CY` and `NBL` among them, which the record dropped for FMP prices contradicting their membership | `JOURNAL_1.md`, `CHANGELOG.md` |
| `Universe/universe.ipynb` | the record's window opening on 2015-01-02, when priced members held 92.97% of the index's weight; this copy's may open later, as above | `RESULTS.md` |
| `Universe/universe.ipynb` | `MNKKQ`, `PCP` and `RAI` excluded by name, as blocking rows of `Universe/Data_Issues.csv`; the record's fourth, `NE`, is not in this copy's seed | `JOURNAL_1.md`, `BITACORA.md` |
| `Universe/universe.ipynb` | its last line, `verified: 13 checks …` | its Verify section |
| `Data/refinery.py` | 803 securities refined | `JOURNAL_1.md`, `RESULTS.md` |
| `Data/analyzer.ipynb` | its last line, `verified: 9 checks …` | its Verify section |
| `experiment_1.ipynb` | a median of 37 names a day, re-struck on 48.1% of trading days | `RESULTS.md`, `FINDINGS_1.md` |
| `experiment_1.ipynb` | its last line, `verified: 113 checks …` | `FINDINGS_1.md` |
| `git status` | the seed unchanged; new only `uv.lock`, which `uv sync` writes | `SETUP.md` |

The universe notebook rewrites the seed only when it drops a name whose FMP prices contradict its
membership. A fresh download can add a blocking row to `Universe/Data_Issues.csv`, and the
experiment's Verify then stops on "the exclusions are the blueprint's". That is the provider's data
moving, not the example breaking: read the new row first.

<!-- example: end -->
