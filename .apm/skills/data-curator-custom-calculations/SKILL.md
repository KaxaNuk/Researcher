---
name: data-curator-custom-calculations
description: >
  Load this skill whenever you need to author, modify, review or debug a KaxaNuk Data Curator custom
  calculation, meaning any `c_*` feature function that becomes an output column. Use it when the
  user asks to install or upgrade the Data Curator, or run `Data/curator.py`; to add a custom
  calculation, computed column, custom indicator, feature or financial metric; when they mention
  `custom_calculations.py`, `custom_calculation_modules`, `Output_Columns`, `DataColumn`, or column
  tags like `m_*`, `f_*`, `fbs_*`, `fcf_*`, `fis_*`, `d_*`, `s_*`, `c_*`; or when they want to
  compute a ratio, moving average, momentum, volatility, returns or signal from curated market or
  fundamental data; or when a downloaded value looks wrong, before it is reported as a bug. It
  covers the library and its upgrade, naming, valid input columns, the DataColumn API,
  composition, wiring the column into the output, for configuration files and runs of `main()`,
  and whether a wrong value is the provider's or the library's.
metadata:
  version: 0.7.0
  library_version: 0.51.0
---

# Data Curator Custom Calculations

A custom calculation is a plain Python function whose name starts with `c_`. The Data Curator
turns each such function into one output column with the exact same name as the function, and
injects each of the function's parameters with the data of the column named after that parameter.

This skill was checked against Data Curator **0.51.0**, the frontmatter's `library_version`:
checked on 0.51.0 by Golden Flow's run of 2026-10-24, from emptied data folders — the worked
example's pipeline, from the download to the experiment's Verify, on Sharadar. Compare it with the
build `uv pip list` shows, and on a newer minor or major version treat every trap here as unproven
until it is checked again. FMP's lines below stay as checked on 0.50.0, by the example's earlier
runs.

**0.51.0** is the first release with the Sharadar provider, released 2026-10-23. `main()` requires
`data_block_providers`, and `ExcelConfigurator` needs `data_blocks`; a parameter workbook from an
earlier build is brought up to date with `kaxanuk.data_curator update excel`. It asks for pyarrow
26 or later. Each column's prefix is checked against the data blocks of the run, so a `d_*` or `s_*`
column with no dividends or splits block mapped stops the run before anything is fetched.

**Sharadar on 0.51.0**, as the worked example's runs of 2026-10-23 and 2026-10-24 found it:

- **Dividends and splits are read through their joined names**, once the dividends and splits
  blocks are mapped to Sharadar in `data_block_providers`:
  `d_ex_dividend_date_dividend_split_adjusted`, the cash a share in today's split-adjusted shares
  on its ex-date, and `s_split_date_numerator` and `s_split_date_denominator`, new shares to old on
  the split's date. A shorter tag — `s_numerator`, `s_denominator`, `d_dividend` — stops the run,
  `[CRITICAL] Column not available under prefix 's': s_denominator`: what
  <https://github.com/KaxaNuk/Data-Curator/issues/39> reported, closed as a wrong column name.
- **The built-in `c_daily_traded_value` is empty on every row**: Sharadar sends no VWAP.
  Reported, <https://github.com/KaxaNuk/Data-Curator/issues/40>. Build the traded value in a `c_*`
  of your own, under a name of its own: the example's `c_traded_value`, the split-adjusted close
  times `m_volume_split_adjusted`, with the volume adjusted twice at a split corrected.
- **A spin-off is not in the dividend column** — GE's GE HealthCare and GE Vernova among them. The
  example adds it after the download from Sharadar's `actions` table, whose `spinoffdividend` rows
  carry its cash value a share in today's split-adjusted shares; asked of the Curator,
  <https://github.com/KaxaNuk/Data-Curator/issues/43>.
- **A refused request is logged, not raised**: `main()` logs a rate limit or a refused batch and
  returns normally, so the example reads what the `kaxanuk` logger recorded at error level to tell
  a name Sharadar has nothing for from a batch refused today, and asks the second again after a
  pause. It also sets `socket.setdefaulttimeout` before the call, so a connection that hangs raises
  instead of hanging the run.
- **`ParquetOutput` writes each file's prices as decimals of that file's own precision, and its
  volume as integers**, so two files do not stack as they come. The example rewrites every file it
  downloads into one schema — the date as `date32`, every other column as `float64` — through its
  `Data/time_series.py`, before anything reads it.
- **The key and its server.** Sharadar's startup subscription, <https://sharadar.com/startup>, is
  served by Sharadar's own API, `https://api.sharadar.com/v1.0`, with the key as the `api_key`
  parameter or the `x-api-key` header. Nasdaq Data Link, `data.nasdaq.com`, answers that key with
  HTTP 429, *exceeded the API speed limit and your account has temporarily been disabled*: it is
  the wrong server, not a rate limit. A key on the free tier answers 403, *Exceeds free tier*, and
  returns about five years of a few sample tickers.

**What this skill knows comes from the documentation, the changelog and runs — never from the
library's code.** The Curator is open source, but the rule is the same for every KaxaNuk tool:
never open, search, print or inspect its installed files, nor a source page its documentation
links to. What neither the documentation nor a run says is not known; a run settles it. An error
is reported by the call, its type and its message, never by the library's own traceback lines.

## The library

Open source, on PyPI as `kaxanuk-data-curator`, with no Lab licence: a KaxaNuk strategy's `uv sync`
installs it, and `Data/curator.py`, written from its docstring, is the strategy's one caller of
`main()`, run as `uv run python Data/curator.py`, with `--end-date` for the paper-trading refresh.
Its documentation is <https://kaxanuk-data-curator.readthedocs.io/en/stable/>, whose `stable` pages
follow the newest release, with the changelog among its release notes.

**Upgrade it between experiments, never during one**: a new build can change what is downloaded.
`uv lock --upgrade-package kaxanuk-data-curator`, then `uv sync --group notebook --inexact`, which
keeps a hand-installed engine; a line in `JOURNAL_1.md` naming both builds; `uv.lock` committed
with a `CHANGELOG.md` entry. A book on paper stops with `unfrozen-input` on any Curator but the one
it was frozen with: where a book is frozen, say so and wait for the owner's go before upgrading.

## 1. Detect the loading and selection surface

Two things vary by project, and nothing else in this skill does: **where the calculation functions
come from**, and **where the output columns are selected**. Both are just arguments to
`kaxanuk.data_curator.main()` — `custom_calculation_modules` and `configuration.columns` — so
identify how the project supplies them before writing anything. Look for an entry script (usually
`__main__.py` at the project root, which `kaxanuk.data_curator init excel` writes, as the README
says), a notebook, or any other caller of `main()`, and match it to one of these surfaces:

**(a) Configuration file + modules on disk.** `kaxanuk.data_curator init excel` writes the entry
script, `Config/data_curator_parameters.xlsx` and `Config/custom_calculations.py`; the entry script
reads the workbook and loads that module, as the README's *Customization* and the documentation's
Custom Calculator Workflow page say. Add new functions to that module. Some projects replace it
with their own multi-file layout, for example a package of category subfolders scanned into a list
of modules. If so, **follow the layout that is already there** — read that project's loader to
see which files it picks up and which it skips, and read a sibling module to copy its shape.

**(b) Programmatic `main()` with modules on disk.** The caller builds the `Configuration` in Python
and imports its calculation modules normally, as the documentation's Component Integrator Workflow
page describes. Files as in (a), selection as in (c).

**(c) Programmatic `main()` with in-memory modules — not checked by a run.** A self-contained
experiment notebook could define its `c_*` functions in a cell, attach them to a module object
built at run time, and construct the `Configuration` inline: no files, no workbook. Neither the
documentation nor a recorded run shows it working, so run it once in a scratch copy before an
experiment relies on it. See `references/programmatic-run.md`.

The documentation and the worked example's run show this much: a `c_` function in a module passed
in `custom_calculation_modules` becomes the column of its name. A module loaded from its file by
path, under a name of the caller's own, works too, as the worked example's `Data/curator.py`
loads its own.

**In a KaxaNuk Strategy Template repository the surface is (b), and the files are fixed.** The
functions go in `Data/Curator/custom_calculations.py`. `Data/curator.py`, the step-3 driver, loads
that file and passes the output columns to `main()` as `Configuration.columns`; in the worked
example's driver they are the `OUTPUT_COLUMNS` tuple. The identifiers are the seed's
`main_identifier`, chosen per experiment with its provider; Sharadar in the worked example is that
experiment's choice. Never create `Config/custom_calculations.py` there. The template ships both
as descriptions — a docstring each — to be filled in. In a strategy made from a template before
0.10.0 they are missing: they come back from the template, never from the example, through
`init-strategy`'s script run from the strategy's root —
`scaffold.py strategy . --only Data/curator.py` and `--only Data/Curator/custom_calculations.py`,
which never overwrite. Since template 0.20.0 every per-security file is Parquet, written and read
through `Data/time_series.py`; a strategy made earlier gets that description the same way,
`--only Data/time_series.py`. Two kinds of column are not `c_*` columns, even when asked for as a
"signal". One compares securities on a date (a rank, a breadth reading); the other has a setting
an experiment will sweep (a fitted model, or a window such as the 50- and 200-day averages the
example builds as `r_trend_50_200`). Both are `r_*` columns in
`Data/Refinery/custom_calculations.py`, which the worked example's `Data/refinery.py` computes
and this skill does not cover. Only their frozen arithmetic inputs are `c_*` columns. **When a new
experiment can use the data already downloaded, its signals are `r_*` columns too**, computed from
the `c_*` columns the Curator wrote — the daily total-return log returns, the traded value —
never by widening the Curator's columns and downloading again.

Anywhere else, if a project has no surface yet, default to (a): create
`Config/custom_calculations.py` and confirm the entry script imports it.

## 2. Reuse before writing

Never duplicate an existing column.

- List the built-ins on the documentation's Features page,
  <https://kaxanuk-data-curator.readthedocs.io/en/stable/api_reference/features.html>: one page per
  built-in, with the columns it reads, what it returns and its formula. The helpers to reuse are on
  the Helpers page, <https://kaxanuk-data-curator.readthedocs.io/en/stable/api_reference/helpers.html>.
- List the project's existing custom `c_*` functions in the layout found in step 1.
- Show the user the relevant matches. If one already computes what they want, stop and point them to
  it. If one computes part of it, depend on it by parameter name instead of recomputing it.

Never name a custom function after one on the Features page: which of the two a run would use is
not documented.

## 3. Interrogate before generating

Ask **one question at a time**, and prefer concrete multiple-choice questions.
Do not write code until the inputs and the output name are settled. Resolve at least:

- The financial concept, in plain words, and its formula.
- Price adjustment: raw (`m_close`), split-adjusted (`m_close_split_adjusted`), or
  dividend-and-split-adjusted (`m_close_dividend_and_split_adjusted`). This changes the result;
  never pick it silently. A provider fills only some of them: under Sharadar, `m_close` is the one
  unadjusted price, as `references/input-columns.md` says, and the one exact price, so the worked
  example rebuilds its adjusted ones from it, as *Known provider faults* below says.
- Window and horizon (`5d` / `21d` / `63d` / `252d`, rolling vs exponential) if the concept has one.
- For fundamentals: whether the configured `period` is `annual` or `quarterly`, since the same
  function yields different values for each, and last-twelve-months logic only makes sense for
  `quarterly`.
- Edge handling: what the leading rows should be before the window fills (`None`), and what a zero
  denominator or a missing input should produce (`None`).

## 4. Write the function

- Read `references/conventions.md` for the naming rules and the full contract of a calculation
  function.
- Read `references/input-columns.md` to resolve every parameter name to a real column, and to find
  the valid names on the documentation's lists rather than guessing them.
- Read `references/data-column-api.md` for the `DataColumn` operations, and the shift-and-pad
  pattern.
- Start from `references/template.py`.
- Follow the project's Python style. `template.py` is in a KaxaNuk strategy's, Bloom Code at 100
  columns, which `bloom-code-lint` checks; elsewhere, match the surrounding module or cell.
- Write in English — names, parameters, docstrings and comments — as the Data Curator's
  documentation is.

## 5. Select the column in the output

Defining the function is not enough: the column has to be selected, or it is never computed. The
output table contains exactly the selected columns, in the order they were given, as the worked
example's runs wrote them. Columns used only as intermediate steps are resolved as dependencies and
need not be selected.

- Surface (a): add the exact function name, `c_` prefix included, to the `Output_Columns` sheet of
  `Config/data_curator_parameters.xlsx`. The documentation's Custom Calculations page says the entry
  includes the prefix; its Features page says the opposite, and the worked example's run, through
  `Configuration.columns`, used the prefix. If you cannot edit the workbook, tell the user the exact
  string to add.
- Surfaces (b) and (c): add the name to the `columns` tuple of the `Configuration` passed to
  `main()`.
- A KaxaNuk Strategy Template repository: add the name to the output columns `Data/curator.py`
  requests (`OUTPUT_COLUMNS` in the example). Widening them changes every file's header, so the
  next run of the driver refetches every identifier. Say so before adding the column.
- Projects with their own configuration surface (a column picker, a settings service, an API):
  follow theirs.

Always select `m_date`: the worked example's runs did, and the documentation does not say it is
added for you.

## 6. Validate

Run every check, and fix until all pass:

- [ ] The function name starts with `c_` and is a valid Python identifier in `snake_case`.
- [ ] The function is reachable: for surfaces (a) and (b), the file is in a location the project's
      loader actually picks up (mind loaders that skip files whose name starts with `_`). For
      surface (c), the function is attached to one of the modules in `custom_calculation_modules`.
- [ ] The column name is in `Configuration.columns`, or is a dependency of a column that is.
- [ ] Every parameter name is an existing column: a documented tag with its prefix, a built-in
      `c_*` from the Features page, another custom `c_*`, or the special `configuration`
      parameter. A wrong name stops the run with an error naming the column.
- [ ] No dependency cycle among the `c_*` functions: a cycle stops the run with an error.
- [ ] The return value is an iterable of the **same length** as the inputs; shifted results are
      padded with `None` on the leading positions.
- [ ] No `inf` or `NaN` leaks into the output; they must be `None`.
- [ ] A column built on volume or traded value — the built-in `c_daily_traded_value` and anything
      averaged or ranked on it — is checked for continuity at every split before anything reads
      it, as `universe-point-in-time`'s register says. A provider's unadjusted volume can already
      be in post-split shares before the split date, and the split adjustment then counts it twice.
      Under Sharadar, `c_daily_traded_value` is empty: build it as the 0.51.0 notes above say, and
      correct it where the volume is adjusted twice, as *Known provider faults* below says.
- [ ] The code parses: `uv run --no-project python -m py_compile <file>` for a file, or a clean run
      of the cell for a notebook, and the linter the project uses passes.
- [ ] If the calculation depends, directly or transitively, on any `f_*`, `fbs_*`, `fcf_*`, `fis_*`,
      `d_*` or `s_*` column, the run needs a provider for the fundamentals, dividends or splits
      block in `data_block_providers`. For the fundamental blocks the result also depends on the
      configured `period`. Under Sharadar on 0.51.0, a `d_*` or `s_*` dependency reads the joined
      names the 0.51.0 notes above give; a shorter tag stops the run.

## 7. Report

Tell the user: the new column name, its direct and transitive dependencies, whether it requires a
fundamental data provider and which `period` it assumes, how many leading rows come out `None`, and
the exact step they must take to select the column on their surface.

## When a value looks wrong — the provider's or the library's?

The Data Curator downloads what the data provider sends, adjusts it and computes from it. Most
wrong values a strategy meets are the provider's, and they go to the provider, never to the Data
Curator's issues. Before anyone reports a bug, tell them apart:

1. **Find the provider's raw value** — the unadjusted column the Curator wrote, `m_close`,
   `m_volume` or a fundamental field as delivered — for the security and the date in question.
2. **The raw value is already wrong** — a price, a volume or a field that cannot be true on that
   date, or that breaks with the security's own history, as the data-issues register's checks
   find it: it is the provider's data. Record it in `Universe/Data_Issues.csv` with its severity,
   as `universe-point-in-time` says, and handle it there — exclude the name, or correct the value
   with its source named. Report it to the provider: the security, the date, the field, the
   value, and why it cannot be right. The library's maintainers cannot fix it.
3. **The raw value is right and the Curator's output is wrong** — a correct input adjusted or
   computed wrongly: it is the library's. Report it on
   <https://github.com/KaxaNuk/Data-Curator/issues>, with the Curator's version, the provider,
   the input and the output.

**Known provider faults** are register checks, so a run finds them on its own. FMP's unadjusted
volume before some 2025 splits is already in post-split shares — ORLY 15:1 on 2025-06-10, NOW
5:1 on 2025-12-18, TPL 3:1 on 2025-12-23 — so `m_volume_split_adjusted` and
`c_daily_traded_value` adjust it twice. The Data Curator's maintainers confirmed it is FMP's
data, <https://github.com/KaxaNuk/Data-Curator/issues/36>: it is reported to FMP. The
documentation's FMP page maps `m_volume_split_adjusted` straight to FMP's own split-adjusted
volume, so the second count is FMP's adjustment, not the Curator's.

**Sharadar rounds every price to three decimals**, the adjusted ones included, as its raw API
sends them — AAPL on 1998-01-02: close 16.25 unadjusted, 0.145 split-adjusted, 0.121
dividend-and-split-adjusted. An early adjusted series of a name split many times moves in steps of
about 0.8% or more, which is noise in a daily return, not the market. The Curator maps
`m_close_split_adjusted` and `m_close_dividend_and_split_adjusted` straight to Sharadar's `close`
and `closeadj`, as the documentation's Sharadar page says, so the rounding is Sharadar's; an open
fill on `m_open_split_adjusted` keeps it too. What the worked example does, checked by its run of
2026-10-24: rebuild the split factor and the total-return close as `c_*` calculations, from the
exact unadjusted `m_close` and the joined dividend and split columns of the 0.51.0 notes above. A
split after the window — NFE's 1-for-50 of 2026-09-14 — is in every earlier Sharadar price and
dividend but not in the window's split columns, and one listing's split-adjusted prices carry a
factor no split records (NVTP): both are a constant between Sharadar's basis and the window's
splits, taken from Sharadar's own split-adjusted close where its decimals are fine. Spin-offs are
added from the `actions` table, downloaded whole with `/data/actions?years=full`. Then every file
is read back and compared with Sharadar's own adjusted close wherever both of its prices are $10 or
more: of 2,199 files, three had a day whose rebuilt return differs from Sharadar's by more than
0.5% — BILL and IOT on 2025-06-03, a one-day glitch in Sharadar's adjusted close the rebuild does
not share, and CXW in 1998, dividends Sharadar books on other dates than its `actions` table — and
none a split-adjusted close off Sharadar's. Asked of the Curator as a feature,
<https://github.com/KaxaNuk/Data-Curator/issues/41>.

**Sharadar's volume is adjusted twice at some splits too**, FMP's fault on another provider: at 82
splits in 77 listings — BBWI on 2000-05-31, FAST on 2002-05-13, GILD on 2002-03-08 among them —
traded value steps by the split's own factor while the shares the tape printed stay flat. The
worked example's `c_traded_value` divides the volume before such a split by its factor, where
traded value lands within 10% of the factor in logs and the shares move by less than 15%, over 30
trading days on each side, for splits of five shares for four or more; the universe notebook's
register reads the same signature and finds none left. Filed with Sharadar's other faults the
example found, <https://github.com/KaxaNuk/Data-Curator/issues/42>.

## References

- `references/conventions.md` — naming rules and the calculation function contract.
- `references/input-columns.md` — the column tags, and the documentation's lists of valid ones.
- `references/data-column-api.md` — the `DataColumn` API and the common patterns.
- `references/programmatic-run.md` — running `main()` without configuration files, as the worked
  example does, and the in-memory modules no run has checked yet.
- `references/template.py` — skeleton to copy, with worked examples.
