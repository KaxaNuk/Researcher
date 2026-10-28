# Input columns

Every parameter of a `c_*` function must name a column the Curator can resolve. The prefix before
the first underscore selects the data block, as the documentation's Data Tag Homogenization page
maps them; the rest of the name is the field within it.

| Prefix | Data block |
|---|---|
| `m_`   | Market data, daily: unadjusted, split-adjusted and dividend-and-split-adjusted |
| `f_`   | Fundamental data common to the statements: the filing and its fiscal period |
| `fbs_` | Balance sheet |
| `fcf_` | Cash flow |
| `fis_` | Income statement |
| `d_`   | Dividends |
| `s_`   | Splits |
| `c_`   | Calculations: the built-ins on the Features page and the project's own `c_*` functions, which may depend on each other |

Plus one non-column parameter: **`configuration`**, which receives the `Configuration`, as the
documentation's page for `c_last_twelve_months_net_income` shows with its `period`.

## Find the valid names in the documentation, do not guess them

The documentation lists them. Read the lists rather than memory, and never the installed package:

- **Input tags** — `m_*`, `f_*`, `fbs_*`, `fcf_*`, `fis_*`, `d_*`, `s_*` — on the page of the data
  provider the run uses, which lists every Data Curator tag it supports beside the provider's own
  name for it:
  <https://kaxanuk-data-curator.readthedocs.io/en/stable/data_providers/financial_modeling_prep.html>
  for FMP, <https://kaxanuk-data-curator.readthedocs.io/en/stable/data_providers/lseg_workspace.html>
  for LSEG, <https://kaxanuk-data-curator.readthedocs.io/en/stable/data_providers/sharadar.html>
  for Sharadar, since 0.51.0. The prefixes are on
  <https://kaxanuk-data-curator.readthedocs.io/en/stable/data_providers/data_tag_homogenization.html>.
  A tag missing from the provider's page is one that provider does not supply: FMP's page has no
  unadjusted `m_vwap`, and Sharadar's no VWAP in any variant.
- **Built-in calculations** — every `c_*` the library ships — on the Features page,
  <https://kaxanuk-data-curator.readthedocs.io/en/stable/api_reference/features.html>, one page per
  function with the columns it reads, what it returns and its formula. Add the project's own
  custom modules.

The `stable` pages follow the newest release, 0.51.0 when this skill was checked; on another build,
read the release notes there before trusting a list.

## Market data columns

The market data tags are `m_date` and `open`, `high`, `low`, `close`, `volume`, `vwap`, each in
three variants: unadjusted, `_split_adjusted` and `_dividend_and_split_adjusted`. So `m_close`,
`m_close_split_adjusted` and `m_close_dividend_and_split_adjusted` are three different columns. A
provider supplies only some of them: FMP's page lists no unadjusted `m_vwap` and no
`m_vwap_dividend_and_split_adjusted`, and LSEG's lists the unadjusted prices, volume and VWAP, and
split-adjusted open, high, low and close.

**Sharadar** (0.51.0) fills `m_open`, `m_high`, `m_low`, `m_close` and `m_volume` split-adjusted,
`m_close` unadjusted and `m_close_dividend_and_split_adjusted`: no VWAP in any variant and no
unadjusted open, high, low or volume, as its documentation page lists and a strategy's run on
2026-10-23 found. Every price arrives rounded to three decimals, the adjusted ones included, as
`SKILL.md`'s *Known provider faults* says, so the worked example rebuilds every adjusted price it
reads from the exact `m_close`. Its identifiers are its own tickers: a delisted name
under its final ticker (AAMRQ, LEHMQ), a recycled ticker suffixed (DD1). Its catalogue,
`/data/tickers?years=full`, comes as one zip of the whole table.

Which one to use is a modelling decision, not a detail:

- `_dividend_and_split_adjusted` for returns and anything that must be comparable through time.
- `_split_adjusted` for price levels and for anything multiplied by a share count, such as market
  cap, as the built-in `c_market_cap` does (the changelog, 0.40.2).
- unadjusted for the price actually traded on the day.

**Volume can arrive split twice.** A provider's unadjusted `m_volume` before a split may already be
post-split, and the split adjustment counts it again: check it as `universe-point-in-time` says.

`m_date` holds the trading date. Always select it: the worked example's runs did, and the
documentation does not say it is added for you.

## Dividend and split columns

These blocks report discrete events. The provider pages list their tags: `d_declaration_date`,
`d_ex_dividend_date`, `d_record_date`, `d_payment_date`, `d_dividend` and
`d_dividend_split_adjusted` for dividends; `s_split_date`, `s_numerator` and `s_denominator` for
splits. The names of the columns a run writes from them are on no documentation page: they come
from a run. The worked example's, on Sharadar and 0.51.0, joins the event's date and its amount in
one name — `d_ex_dividend_date_dividend_split_adjusted`, `s_split_date_numerator` and
`s_split_date_denominator` — and reads them so, as a `c_*` parameter or a selected column. For
another provider or another field, select it in a short run in a scratch copy, read the output's
header, and record what it was.

Dividends and splits are data blocks of their own, each mapped to a provider in
`data_block_providers` (the changelog, 0.50.0).

**Under Sharadar on 0.51.0 a shorter tag stops the run** — `s_numerator`, `d_dividend` — as
`SKILL.md`'s 0.51.0 notes say (<https://github.com/KaxaNuk/Data-Curator/issues/39>, closed as a
wrong column name); the joined names above are read. The page also says Sharadar publishes a
dividend only adjusted for later splits, so the amount as paid is a custom calculation. A spin-off
is not in its dividend column at all.

## Fundamental columns

Fundamental values are reported per filing. On the daily rows, each filing's values repeat: the
Helpers page says of `indexed_rolling_window_operation` that period data carries "the same key and
thus the same data" on every row, which is why the last-twelve-months built-ins roll over filings,
not over days. Values also depend on the configured `period` (`annual` or `quarterly`): the page for
`c_last_twelve_months_net_income` sums four quarters for quarterly and returns the period's own
value for annual.

`f_*` carries the filing metadata that makes period-aware maths possible, notably `f_fiscal_year`
and `f_fiscal_period`, which `c_last_twelve_months_net_income` takes beside `fis_net_income`, as its
page shows. FMP's page lists both; LSEG's lists neither.

## Failure modes

- A parameter that names no column stops the run with an error naming it; the changelog (0.12)
  improved the errors for a missing custom calculation and for circular dependencies.
- A column name is a documented tag — one of the prefixes above, as Data Tag Homogenization and the
  provider pages list them — or a `c_*` name in snake case. Anything else is not a column.
