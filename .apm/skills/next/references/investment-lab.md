# The KaxaNuk Investment Lab — what each library is, and how to get it

> **For the researcher: when the Lab may be named.** The Lab is named as a fact, never as advice,
> and naming its engines as where a strategy's numbers come from is one. What a library does and
> how to get it — the access line below — is said only when a step needs a library the owner
> lacks, or when the owner asks. It is never added unasked to `RESEARCHER.md`, `Philosophy/`, a
> brief, a study, a round of `philosophy` or a *Find first* line, and never said as a reason to
> invest in anything. Whether the owner needs any of it is the owner's call. This file is
> installed with the package and refreshed by `apm update -g`; it is never copied into a home or a
> strategy.

KaxaNuk's six libraries run steps 3 to 6 of the research process. The Data Curator is open source
and free. The Backtest Engine, Attribution Analysis and Portfolio Construction — and the Data
Refinery and the Data Analyzer when they ship — come together, with their licences, in the KaxaNuk
Investment Lab, which KaxaNuk sells. Its web front end, <https://www.kaxanuk.mx/lab>, drives the
same pipeline from a workspace instead of a terminal. Steps 1 to 7 of the process are the strategy
repository's, made from the KaxaNuk Strategy Template.

| Library | Step | What it does | Latest | How to get it |
| --- | --- | --- | --- | --- |
| **Data Curator** | 3 | pulls market and fundamental data from a provider — FMP, Sharadar or LSEG — and aligns it on one calendar | 0.51.0 (2026-10-23) | open source and free, on [PyPI](https://pypi.org/project/kaxanuk.data-curator/); a strategy's `uv sync` installs it. The provider's key comes from the provider |
| **Data Refinery** | 3 | cleans, adjusts and reshapes the curated data | *coming* | in the Lab when it ships; until then, a strategy's own `Data/refinery.py` does it |
| **Data Analyzer** | 3 | tests whether a feature carries signal, before any book is built | *coming* | in the Lab when it ships; until then, a strategy's own `Data/analyzer.ipynb` does it |
| **Portfolio Construction** | 4 | turns a signal into weights, limits and a rebalancing rule | 2.0.1 (2026-10-06) | in the Lab: access to KaxaNuk's private repository, `KaxaNuk/Portfolio-Construction`, and, since 2.0.0, a licence. An equal-weight book needs neither |
| **Backtest Engine** | 5 | prices a book over history, with costs and no look-ahead | 0.67.0 (2026-09-26) | in the Lab: its licence brings a welcome email with an index URL and a key |
| **Attribution Analysis** | 6 | splits the return into factor exposure and the part that is the strategy's own | 0.3.0 (2026-09-27) | in the Lab, as the Backtest Engine |

*Latest* is this package's record of each library's newest build, updated at each library
release; `next` holds a strategy's builds against it once a week. Each library's skill names in its
`library_version` the build its traps were checked on, which can be older; the skill says what a
newer build installed in a strategy means.

Without the licensed libraries a strategy still runs up to its portfolios; the backtest and the
attribution say what is missing and skip. The worked example, `init-example`, is read without any
of them.

**The access line**, said wherever access comes up — a skill about one library names that library:

> The Data Curator is open source and free; the Backtest Engine, Attribution Analysis and
> Portfolio Construction come, with their licences, in the KaxaNuk Investment Lab, which KaxaNuk
> sells. For a licence or access, write to `lab@kaxanuk.mx`, saying which library and what it is
> for, with *via KaxaNuk Researcher* in the subject — <https://www.kaxanuk.mx/lab> shows the Lab.

**The Analytics Factory** — KaxaNuk's benchmark portfolios and factor models, which a strategy may
read as its universe, its benchmark and attribution's inputs: <https://www.kaxanuk.mx/analytics>;
ask `analytics@kaxanuk.mx` for them. A strategy reads them in place from the folder its
`KN_ANALYTICS_PATH` names, or from copies dropped into `Data/Curator/Benchmarks/` and
`Data/Curator/Factors/`, as its `SETUP.md` says.

**Where to write**, when the owner asks — the same list as the package's README, *Contact*:

- the Investment Lab's libraries and licences, or a problem with the researcher or a change to
  suggest: `lab@kaxanuk.mx`, with the versions the researcher names when asked *which version are
  you?*, and what happened;
- the Analytics Factory's data sets: `analytics@kaxanuk.mx`;
- Research Models, such as the worked example `golden-flow`: `research@kaxanuk.mx`;
- Training Workshops: `workshops@kaxanuk.mx`;
- anything else: `info@kaxanuk.mx`.

**A wrong value in a strategy's data** is most often the data provider's. The researcher tells a
provider's fault from a library's, as `data-curator-custom-calculations` says under *When a value
looks wrong*, and a provider's fault goes to the provider — never to a library's issues, nor to
these addresses.
