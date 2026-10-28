# Setup

Everything needed to go from nothing to a repository you can work in, from `init-example` to an
environment the worked strategy runs in. An agent — Claude, Codex, Cursor — can follow it end to
end, and a person can read it in a few minutes.

<!-- example: begin -->

> **On the example.** This folder is for reading. To run it, `init-example` copies it into a folder
> of its own — step 1 — and step 5 is skipped: this README is already the strategy's.
>
> **What a run needs.**
>
> - **An FMP key**, `KNDC_API_KEY_FMP`. FMP is this experiment's provider, and its symbols are the
>   seed's main identifier. A later experiment may use another provider, with the main identifier
>   KaxaNuk supplies for it. **Without one, Yahoo Finance can run it for learning**, with no key,
>   through the Data Curator's Yahoo Finance extension, after the changes the README's *Run it*
>   names — but it has no data for the 178 names in the seed that left the market, and no
>   unadjusted price or VWAP, from which the record builds the traded value, the fill and the
>   commission. For a precise experiment use FMP, which the record used, or Sharadar or LSEG.
> - **Three products of KaxaNuk's Analytics Factory**, below. No provider sells them.
>   `Data/hand_supplied.py` reads them under the Factory's own names, from where step 3 says.
> - **The Backtest Engine and Attribution Analysis licences.** Every performance and attribution
>   figure here came from Backtest Engine 0.66.0 and Attribution Analysis 0.2.0. Without them the
>   notebooks still write the portfolios, then report what is missing and skip.
> - **Portfolio Construction is not needed.** It is not installed:
>   `Experiments/portfolio_construction.py` sizes the book itself.
>
> | Product | File | What it holds |
> | --- | --- | --- |
> | KN US Equity Core, holdings | `KN_US_Equity_Benchmark_Holdings.csv`, 46,388,746 bytes, md5 `eba4bf64ffa8de5d650e4e2c4b21844d` | the index's daily weights: `m_date` first, in ISO dates, then one column per listing keyed by the index's own ticker; about 600 members a day, 1,399 listings, 2000-01-03 to 2026-08-14 |
> | KN US Equity Core, returns | `KN_US_Equity_Benchmark_Returns.csv`, md5 `1668b564582f1871d7e4a6f39896e50a` | `m_date` written day first, then the index's daily return under the Factory's own header, `kn600` |
> | KN US Equity Factor Model | twenty files, about 1 GB | `Beta`, `Momentum`, `Residual_Volatility`, `Size`, `Value`, the eleven GICS sectors, `Market`, `Total_Factor_Returns`, `Total_Excess_Returns` and `Idyo_Returns`; the sector files hold no values, so sector attribution reads zero |
>
> Golden Flow's own run read these two index files, byte for byte, as
> `KN_US_Equity_Core_Holdings.csv` and `KN_US_Equity_Core_Returns.csv`; its journal uses those
> names. An older, smaller holdings file of the same name is the KN US Equity 600, another index:
> replace it. **Without the holdings, only the download runs**: every later stage reads membership
> from them.
>
> **The seed is committed.** `Universe/seed.py` rebuilds it only from the index's master of
> listings, a file of the Analytics Factory not in its published folders (ask
> `analytics@kaxanuk.mx`). Running it overwrites the committed seed.
>
> **Times recorded on 2026-10-06.** The curator took 1 hour 37 minutes for 892 names, and 2 minutes
> for its second pass. The universe notebook took 17 seconds, once `seed.py` had filled the profile
> cache; a copy skips `seed.py`, so it first asks FMP for the profiles of the seed's 883 symbols.
> The refinery took 3 minutes. The analyzer's and the experiment's times were not recorded; the
> experiment prices 47 weight files in ten engine processes.

<!-- example: end -->

## What you need first

The two tools below, and an assistant — Claude or Codex — with the KaxaNuk Researcher installed
once for your user, as step 4 says. You do **not** need Python: `uv` fetches the right version in
step 2.

| Tool | Windows | macOS and Linux |
| --- | --- | --- |
| [git](https://git-scm.com) | `winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements` | `xcode-select --install` on macOS; your package manager on Linux |
| [uv](https://docs.astral.sh/uv/) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Open a **new** terminal after installing either, so it is on the path. If `git --version` and
`uv --version` both answer, you are ready.

> **For the agent, before anything else.** Look at the folder you are in, and say what you found:
>
> - it holds `Bibliotheca/`, `Universe/` and `Experiments/` → the repository exists, go to step 2;
> - otherwise the repository does not exist yet → step 1. It needs **where to put it**, which
>   defaults to `golden-flow` beside the folder you are in; ask if the user has not said.
>
> Every command from step 2 on runs **in the root**, the folder step 1 made. Never a level above it.

---

## The rule: one folder is the whole project

One folder is the repository: open that folder and run every command in it, with nothing installed
a level above it and nothing nested a level below. What setup writes there, `.venv/` and
`Config/.env`, is ignored, as is anything an assistant or APM writes per machine (`.claude/`,
`.agents/`, `.codex/`, `apm_modules/`, `apm.lock.yaml`). `uv.lock`, which `uv sync` writes, is
committed.

---

## Step 1 — Get the repository

**`init-example` makes it.** It is a skill of the
[KaxaNuk Researcher](https://github.com/KaxaNuk/Researcher), installed for your user as
step 4 says. A script copies the worked example inside the researcher package, byte for byte, into
a new folder, `golden-flow` unless you choose another place. It then makes that folder a git
repository and commits it once. That folder is the root. You can read the example
[on GitHub](https://github.com/KaxaNuk/Researcher/tree/main/examples/strategy/golden-flow)
without making anything.

**On Windows, keep the path short.** `D:\Research\...` is fine; a deep synced path such as
`C:\Users\<you>\OneDrive\Documents\Projects\...` is not. Tools that write deep inside the folder,
such as `uv sync` building `.venv/`, can pass Windows' 260-character path limit and fail with a
message that does not say so, such as `WinError 3: The system cannot find the path specified`.

A strategy of your own is not made from here: `init-strategy <strategy-name>` makes it from the
template, which holds every file this example works through, describing what belongs in it. Never
build on the example.

> **For the agent.** If the first commit fails for want of a git identity, ask the user in one open
> message, with no options, *What's your name, or what would you like me to call you?*; never invent
> it, and ask no e-mail. Set it for this folder only: `git config user.name "<name>"` then
> `git config user.email "<>"`, an empty address.
> Then commit again: `git commit -m "Start from the KaxaNuk example strategy, golden-flow"`.

---

## Step 2 — Build the environment

From the root:

```bash
uv sync --group notebook --inexact
```

That creates `.venv/` and installs the pipeline with the `notebook` group: JupyterLab, and
`nbconvert` to run a notebook or strip its outputs from the command line. **If neither Python 3.12
nor 3.13 is on the machine, `uv` downloads 3.13**; there is nothing to install by hand.

**Why 3.13 and not the newest.** Every performance figure comes from the Backtest Engine, which is
documented for Python 3.12 or 3.13. The Data Curator allows 3.12 to 3.14, so 3.13 satisfies both.

**Once the Backtest Engine, Attribution Analysis or Portfolio Construction is installed by hand,
never run a bare `uv sync` here again.** It is exact: it removes every package `uv.lock` does not
name, and those three are deliberately not named. Use the command above, `--inexact` included, and
`uv run` for everything else; both keep them. The `backtest-engine-runs`,
`attribution-analysis-runs` and `portfolio-construction-runs` skills say how to install each.

**Upgrade a Lab library between experiments**, never during one; your researcher says when a new
one is out. For the Data Curator, run `uv lock --upgrade-package kaxanuk-data-curator`, then the
command above; for a licensed library, follow its skill. A book on paper stops on any Data Curator
but the one it was frozen with.

---

## Step 3 — Put your keys in place

```bash
cp Config/.env.template Config/.env
```

Then open `Config/.env` with Notepad or TextEdit (in the macOS Finder, Cmd+Shift+. shows files
that start with a dot), paste each key after its `=`, and save.

Fill in the key for your data provider; the template has a line for FMP, Sharadar and LSEG.
`KNBE_API_KEY_KAXANUK` and `KNAA_API_KEY_KAXANUK` are the Backtest Engine and Attribution Analysis
licences. Without them the process runs up to portfolio construction, and the backtest and
attribution report what is missing and skip. `KNPC_API_KEY_KAXANUK` is the Portfolio Construction
licence; the library reads it from the environment or a `.kaxanuk_license` file, not from this
file, as `portfolio-construction-runs` says. An equal-weight book needs neither the key nor the
library. The three come together, with their licences, in the KaxaNuk Investment Lab, which
KaxaNuk sells: write to `lab@kaxanuk.mx`, saying which library and what it is for, with
*via KaxaNuk Researcher* in the subject — <https://www.kaxanuk.mx/lab> shows the Lab.

`KN_ANALYTICS_PATH` is not a key. It is the folder where KaxaNuk's Analytics Factory ships its
benchmark portfolios and factor models, which a strategy may read as its universe, its benchmark
and attribution's inputs (<https://www.kaxanuk.mx/analytics>; ask `analytics@kaxanuk.mx` for them). It
holds `Benchmark Portfolios/` and `Factor Models/`, read in place under the Factory's own names and
headers; older `Benchmarks/` and `Factors/` folders are read where the new ones are absent. Or
leave it empty and drop the same files, unchanged, into `Data/Curator/Benchmarks/` and
`Data/Curator/Factors/`.

The four `PAPER_TRADING_*` lines configure step 7. Once a book is on paper,
`Paper_Trading/BITACORA.md` says how its daily run is scheduled.

<!-- example: begin -->

**In this example, `Paper_Trading_1` is Experiment 1's book**, frozen on 2026-10-06 and kept as a
record. It does not run from this copy, for the reasons
[`Paper_Trading/BITACORA.md`](Paper_Trading/BITACORA.md) gives.

<!-- example: end -->

> **For the agent.** Never open, read back, print or echo `Config/.env`, and never put a value from
> it in a command that gets recorded. You may say **which keys are still empty, by name only**,
> with the one check allowed, which prints names and never values — Git Bash, then PowerShell:
>
> ```
> grep -E '^[A-Z_]+=$' Config/.env | cut -d= -f1
> Select-String -Pattern '^[A-Z_]+=$' Config/.env | ForEach-Object { $_.Line.TrimEnd('=') }
> ```
>
> You cannot fill them: that is the one thing in this file only the user can do.

---

## Step 4 — The agent skills are installed once, for your user

**Nothing to install here.** KaxaNuk's agent skills (how each Lab library is called, how an
experiment is structured, how attribution is read, the house rules) and the
[KaxaNuk Researcher](https://github.com/KaxaNuk/Researcher)'s own are installed once for
your user, not per repository, by the same command that gave you step 1:

```bash
uvx --from apm-cli==0.33.0 apm install -g KaxaNuk/Researcher --target claude
```

For another assistant, put `codex`, `cursor` or its name in place of `claude`; the researcher
package's [`SETUP.md`](https://github.com/KaxaNuk/Researcher/blob/main/SETUP.md) says what
each receives.

The skills then work in every folder, this one included, and
`uvx --from apm-cli==0.33.0 apm update -g` keeps every strategy current at once. Nothing in the
pipeline imports a skill: the repository, the notebooks and the results are the same with or
without them.

Your researcher's home, made once with `init-researcher`, can be invited into this folder for its
library: `claude --add-dir <the researcher's folder>`, `/add-dir` once inside, or the desktop app's
add-folder button. For its identity to load with it, follow *In a strategy or another project* in
the researcher's own README.

> **For the agent.** Do not install skills into this repository. If they are missing, give the user
> the command above with the assistant you are as the target; it installs for their user, not here.
> Say that they appear in a **new** conversation.

---

## Step 5 — Make the README the strategy's

The `README.md` that `init-strategy` copied describes the KaxaNuk Strategy Template, not your
strategy. A strategy's README describes **the strategy**: what it is, what it claims, where it
stands. Replace the whole file with this, filled in, and leave the process to the link:

```markdown
# <strategy-name>

<one sentence on the idea — or: The objective is not written yet; see OBJECTIVE.md.>

> **Status: set up, nothing measured.** Replace this line as the strategy moves, and the banner at
> the top of `AGENTS.md` with it.

Built on the [KaxaNuk Strategy Template](https://github.com/KaxaNuk/Researcher/blob/main/templates/strategy/README.md):
eight steps as a folder structure. Its README says what each folder is for, where each
kind of logic goes and, under *Starting your own strategy*, the order to work in; this one does not
repeat it. **Next:** [`OBJECTIVE.md`](OBJECTIVE.md), the idea and its claims, before any paper is
read.

| Read | For |
| --- | --- |
| [`OBJECTIVE.md`](OBJECTIVE.md) | the idea, and the status of each claim inside it |
| [`RESULTS.md`](RESULTS.md) | every number this repository has measured, and what it cost |
| [`AGENTS.md`](AGENTS.md) | how work is done here, and the bar a result has to clear |
| [`SETUP.md`](SETUP.md) | how this repository is set up on a new machine |

Research, never investment advice: *What it is, and what it is not*, in the
[KaxaNuk Researcher's README](https://github.com/KaxaNuk/Researcher#readme).
```

Put the same status line in place of the banner at the top of `AGENTS.md`. In `pyproject.toml`,
rename `name` to the strategy's and set `version` to `0.1.0`. `LICENSE` names KaxaNuk as the
holder: put yourself there, or choose another licence. In `CHANGELOG.md`, keep everything above the
first `---` line and replace the template's entries below it with the strategy's first, naming the
template version `pyproject.toml` declared before you reset it:

```markdown
## 0.1.0 (YYYY-MM-DD)

**MINOR** — started from the KaxaNuk Strategy Template <template-version>. Nothing measured yet.
```

Then run `uv lock`, so `uv.lock` records the new name and version, and commit it with the rest:

```bash
git add README.md AGENTS.md pyproject.toml LICENSE CHANGELOG.md uv.lock
git commit -m "README: <strategy-name>"
```

> **For the agent.** Use the name you asked for at the start, and the user's sentence on the idea
> if they gave one; **never invent a thesis**, use the placeholder. The holder in `LICENSE` is the
> user's name: ask if you do not have it, never invent it. Everything else in the block is fixed.
> Do not keep the template's README under another name: the process lives upstream, and a copy
> here drifts.

---

## What "done" looks like

From the root:

```bash
git status
```

**It should be clean.** Step 5 committed everything setup changed, `uv.lock` included: it pins the
versions this strategy's results will come from, which is why the template ships without one and
your repository keeps one. Everything else setup produced is ignored, as *The rule* above says.
**Anything showing up means something was written in the wrong place.**

<!-- example: begin -->

**In this example, `uv.lock` shows up untracked,** and nothing is wrong: the example commits none,
so its library versions resolve when `uv sync` runs.

<!-- example: end -->

Then open **this folder**, not a parent of it, in your editor (PyCharm or VS Code) and in your
assistant (Claude or Codex).

**In a new strategy nothing runs yet, on purpose:** every `.py` file and notebook says what belongs
in it. Your assistant writes each one with you, in the order of parts A to H of the template's
README, and can read the worked example's copy of the same file beside yours (`init-example`, into
a folder of its own). The first code that runs is `Data/curator.py`, once `OBJECTIVE.md` and the
seed exist.

> **For the agent — the hand-over.** Say the absolute path of the root, that it is the whole project
> and the folder to open, that the README is now the strategy's, which `.env` keys are still empty
> by name, that the skills are installed once for the user and nothing is installed here, and that
> the next step is `objective`, which drafts `OBJECTIVE.md` with them; `next` says what comes after.
> Then stop: starting research work is a different request.

<!-- example: begin -->

**In this example, the hand-over says the folder is the worked example, for reading;** the next
thing is its README's *How to read it*, or *Run it* once the keys and files are in place; a
strategy of your own is `init-strategy <name>`.

<!-- example: end -->

---

## Next

The first thing to write is `OBJECTIVE.md`: the idea and its claims, before any paper is read. The
order after it is *Starting your own strategy* in the
[template's README](https://github.com/KaxaNuk/Researcher/blob/main/templates/strategy/README.md);
[`AGENTS.md`](AGENTS.md) says how work is done here.

<!-- example: begin -->

**In this example nothing is written:** read `OBJECTIVE.md`, then `RESULTS.md`.

<!-- example: end -->
