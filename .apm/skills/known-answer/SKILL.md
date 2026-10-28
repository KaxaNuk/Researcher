---
name: known-answer
description: >
  Load this skill when the owner asks to check a method before it touches real data — *a
  known-answer test for my half-life estimate* — or when a session of a KaxaNuk Training Workshop
  names it among its skills, even where the course still lists it as coming. It plans, and on the
  owner's go writes, one marimo notebook in a new folder of the owner's naming beside their
  strategy: data simulated from a model whose truth is set and seeded (an AR(1) and its half-life, a
  GBM's drift and volatility, a regression's beta, a factor model's loadings, a planted signal's IC,
  clusters with known members, a two-state regime, a GARCH(1,1) and its forecast, a classifier's
  coefficients, AUC and calibration), the owner's method run on it, a Verify section that raises
  when the method misses the truth by more than a stated tolerance, and one way the method fails, so
  the check is seen to bite. The owner runs it. It does NOT run the notebook, write in a strategy, a
  course's clone or the home, read the owner's real data, compute a figure about a book, screen a
  feature (`data-analyzer-runs`), validate a model out of sample, tutor a session (`workshop`),
  explain the model or its theory (`teach`, at home), or say what the library holds (`query`).
metadata:
  version: 0.2.0
---

# Known answer — a method proved on data whose truth you set

On real data nobody knows the truth, so a wrong method prints numbers that look just like a right
one's. On data simulated from a model whose parameters you set, the truth is known, and the method
gives it back or it does not. **A method that cannot recover a truth it was built for will not find
one in the market.**

A pass says the method recovers the truth when the data follow the model, at that size. It does
not say the model describes the market, nor that the method works on the owner's data: that is the
owner's own run, the analyzer's screen and the engines' numbers, later. A miss is cheap here and
dear anywhere else.

## When to Use

- The owner asks to check a method before it touches real data — *known-answer test for my
  half-life estimate*, *check my beta before I run it on my names*, *will my clustering find
  groups I planted?* — or again after they change it.
- A session of a KaxaNuk Training Workshop lists `known-answer` among its skills, in its
  course map's `researcher.skills`, which `workshop` reads, and the owner wants their own method
  checked. The session's deck says which method; this skill's recipe gives the model. A course
  written before this release lists it under `tools.researcher.coming`, or greys it on a slide as
  *coming*: it runs all the same, as `workshop`'s practice does.
- Not in a workshop block with the AI off, nor for the checkpoint: `workshop` holds those, and this
  skill waits until the owner says that part is done.
- Not to screen a feature on real data (`data-analyzer-runs`), price a book
  (`backtest-engine-runs`) or validate a model out of sample: a known answer comes before each of
  them and replaces none.
- Not to explain the model or its theory — why a short sample bends an estimate, what a GARCH
  is — which is `teach <topic>`, at home; nor to say what the owner's library holds on it, which
  is `query`. A source they want in the library is `read`'s; a source a recipe names is a lead,
  never the library's.

**Every question this skill asks** goes through the question tool where the harness has one,
Claude Code's `AskUserQuestion`, and a question with more than four options as a numbered list in
chat instead. Without one — Codex, Gemini — it is one chat message: each question numbered, its
options numbered beneath it, *Other — your own words* last, and one line on how to answer, by the
numbers or in their own words.

## The rules

1. **The owner's prediction first.** Before the plan, ask what the method should give back — the
   number, and how close — and what the failure will do to it, and why. It goes into the
   notebook's header in their words, dated, and is set against the result once their run is in.
   The recipe's own figures, in brackets in `references/recipes.md`, are never said to the owner:
   the figures read are the notebook's own output, from the owner's run.
2. **Simulated data only.** The notebook reads no data file: nothing from the strategy's `Data/`,
   `Universe/` or `Experiments/`, no download, no course data. Every figure it prints is a
   *teaching computation on simulated data*, labelled so in its header, never a figure about a book
   or the owner's data, and never quoted as one.
3. **The truth and the tolerance are set before the run**, each with its reason: the true
   parameters, the seed, the size, and how close counts as recovered. A tolerance is never widened
   after a miss to let the method pass: a new tolerance is a new plan, said to be one, and the
   header keeps both.
4. **The method is the owner's, unchanged.** It is imported from the file it lives in, or copied as
   it stands, as *Step 1* says, never rewritten to pass. A miss is the owner's to fix, in their own
   file, through that step's skill and on its own go; then the same notebook runs again.
5. **The owner runs it.** The researcher writes the notebook and lints it, and never runs it — in a
   workshop or out of one, on either track — so every figure it prints is the owner's run's, as
   `workshop`'s *No figure of the tutor's own* and the home's hard don'ts ask, and the researcher
   never states, confirms or corrects one. Beyond the lint, the researcher runs only the recipe's
   own simulation, before the plan, to measure a tolerance again for a changed size, as *Step 1*
   says: a tolerance, never a result of the owner's method.
6. **One notebook, and nothing else.** It lives in a new folder beside the strategy — never inside
   it, never inside a course's clone, never in the home — and writes no file when it runs: no CSV,
   no saved chart, no cache. It imports from the strategy without writing in it. marimo's editor
   keeps its own session beside it, in `__marimo__/`, as *Step 5* says: marimo's, not the
   notebook's.
7. **Plan first, the owner's go, then write**, as the home's `AGENTS.md` requires of every write.
   The notebook is code: in a workshop, it is written only with the AI on.

## Step 1: The method and the model

1. **The method.** Ask what it is and where it lives, unless the owner said: a function in the
   strategy — its file and name, such as `Data/Refinery/custom_calculations.py` and `half_life` —
   a cell of one of its notebooks, or a method only described. Read that file and every module of
   the strategy it imports, and nothing else of the strategy; never a Lab library's code.
   - **A function** is imported from its file, by path, as *Step 4* says, only when no code at
     module level — in that file or in a strategy module it imports — reads or writes a file or
     loads `Config/.env`, since importing runs it. Otherwise the function is copied into the
     method's section as it stands, its source named. The plan says which.
   - **A notebook cell** is copied into the method's section as it stands, its source named.
   - **A `c_*` calculation** of the Data Curator is called on the simulated series wrapped with
     `DataColumn.load()`, as `references/data-column-api.md` in `data-curator-custom-calculations`
     shows, with the Data Curator in the run's environment.
   - **A method only described** gets its function's signature and docstring in the method's
     section, for the owner to write; or, on their word, the researcher writes it from their
     description and reads it back line by line in the plan, and the header says who wrote it.
   - **A Lab library's own computation** — a sizing, the engine's pricing — is not checked here: it
     is known from its documentation and runs, and a doubt about it goes to `lab@kaxanuk.mx`. What
     the owner computes and feeds it is.
2. **The model**, from `references/recipes.md`: the recipe whose truth is what the method claims to
   estimate.

   | The method estimates | Recipe |
   | --- | --- |
   | a half-life, a speed of mean reversion, a persistence | 1 · AR(1) |
   | a drift or a volatility from prices | 2 · geometric Brownian motion |
   | a beta, a slope, a predictive coefficient and its standard error | 3 · regression |
   | factor loadings, from given factor returns or by PCA | 4 · factor model |
   | an information coefficient, from a per-date rank | 5 · planted signal |
   | groups of names that move together | 6 · clusters |
   | calm and stressed states, their volatilities, the state on a date | 7 · two-state regime |
   | a GARCH(1,1), a long-run variance, a volatility forecast | 8 · GARCH(1,1) |
   | a classifier's coefficients, its AUC, its probabilities | 9 · logistic classifier |

   A method no recipe fits: propose a model built from the method's own assumptions, with a truth,
   a seed, a tolerance and a failure in the recipes' form, and say in the plan that it is not one of
   them.
3. **The size and the failure.** The recipe's numbers stand unless the owner changes them — to the
   strategy's own number of names or dates, say. A changed size takes the tolerance's formula
   again, never the recipe's figure. The formulas are large-sample ones: a short size takes recipe
   1's *At a short length*. A tolerance the recipe measured over seeded repetitions instead of by a
   formula — 4's PCA, 6, 7, 8 and 9's AUC — either stays at the recipe's size for the pass, with
   the owner's size shown as the spread over those repetitions, or is measured again at the new
   size, over the same seeds, by the recipe's simulation and the estimator the recipe names, never
   the owner's method, before the plan. Either way the band that decides the pass stays clear of
   any bound — below 1 for a persistence — and still catches the recipe's failure; the plan says
   which route it took. The failure shown is the recipe's, or another the owner names: too few
   observations, a look-ahead and a pooled rank are the three that bite most often.
4. **The owner's prediction**, now that the model is named, as the first rule says: the number the
   method should give back and how close, then what the failure will do to it — higher or lower,
   by a little or a lot — each with why.

## Step 2: Where it goes

- **A new folder, named by the owner, beside the strategy**, in the folder that holds it. Offer
  names drawn from the method — `known-answer-half-life`, `<strategy>-known-answer` — and their own
  words. With no strategy, it goes beside the folder the session is open in, or where the owner
  says.
- **Never inside** a strategy — a folder holding `Bibliotheca/`, or any folder below one — a
  course's clone, whose `README.md` names a workshop at its root, or the researcher's home. A
  course's own notebook stays the course's: this one is the owner's, for their method.
- **Nothing is overwritten.** The folder is new or empty. A notebook this skill wrote earlier
  changes only on a new plan and go.
- **One file**, `known_answer_marimo.py`, or a name the owner gives that ends in `_marimo.py`, as
  a strategy's notebooks do.
- **No version is saved**: the folder is not a repository, as a piece `init-example` copies is not.
  The notebook is the owner's to keep, move or delete.

## Step 3: The plan

In chat, short:

- the method — its file and function, read only — and whether the notebook imports it or copies
  it, and why;
- the model, its true parameters, the seed and the size, from the recipe; at a short or changed
  size, the route *Step 1* takes;
- the tolerance and its reason; the failure to show;
- the owner's prediction, in their words;
- the folder and the one file, and that nothing is written in the strategy, a clone or the home,
  and no version saved;
- that the owner runs it, the packages it needs, and the line they run.

Then ask *Go*, *Change something* or *Stop*, and write on *Go* only. *Change something* offers the
plan's own levers: another recipe, size, failure, folder or file name, and, before any run, the
tolerance.

## Step 4: The notebook

Its narrative is in the owner's language, its code in English — names, docstrings and comments —
in the house style of the strategy beside it.

**It is a marimo notebook**, as a strategy's are from template 0.20.0: a Python file, run as a
script or opened in marimo's editor, with no output saved in it. Each section below is a markdown
cell, `mo.md(...)`, and the cells that run it. marimo runs the cells in the order their names need,
so every name is defined in one cell only, and a name a cell keeps to itself starts with `_`. The
folder it sits in is `mo.notebook_dir()`, so the strategy beside it is found wherever it runs from.

| Section | Holds |
| --- | --- |
| Header | what is checked, against which model; *Teaching computation on simulated data: no figure here is about a book or your data*; the owner's prediction, in their words, dated; any source the recipe names, as this skill's — *a lead from the known-answer skill, not in your library* — never as evidence, the theory left to `teach` and `query`; the line the owner runs |
| 0 · Setup | the seed, the true parameters, the size and the tolerance with its reason, each named once, in capitals; one generator for the main draw, `numpy.random.default_rng(SEED)`, and one per repetition seed, each made once and passed to every draw it serves; the strategy's path and the method's import |
| 1 · Simulate | the data drawn from the model, from that generator; no file read, none written |
| 2 · The method | the owner's method, as imported or copied, its source named, and nothing else |
| 3 · Recover | the method run on the simulated data; the estimate beside the truth and the tolerance, in one small table |
| 4 · The check bites | the recipe's failure: the same method on the broken case, the recipe's own comparison, the miss shown — over seeded repetitions wherever one draw could be luck |
| 5 · Verify | an explicit `raise`, never a bare `assert`, each with a message naming what missed and by how much: when the estimate falls outside the tolerance; when the failure does not miss as its recipe states — outside the tolerance, or past the recipe's own failure threshold — since a check that cannot catch it catches nothing; when the same seed does not draw the same first values |
| What this does not show | that the model describes the market, or that the method works on the owner's data |

States, signs and labels are matched to the truth before any comparison: a component's sign, a
cluster's number and a regime's order are arbitrary, as the recipes say. A chart, where one helps,
is shown inline and never saved.

**Importing from the strategy writes nothing in it**, once *Step 1* found nothing at module level
that reads or writes a file or loads `.env`. Section 0 turns bytecode off first,
`sys.dont_write_bytecode = True`, so no `__pycache__` lands there; puts the strategy's root first on
`sys.path`, never `os.chdir` into it; and loads the file by its path with
`importlib.util.spec_from_file_location`. The strategy's folder was unchanged after such a run,
checked again, with marimo, by running it on 2026-10-27.

## Step 5: Check, hand over and read

1. **Lint**, before the hand-over, with the strategy's own settings and no cache written; with no
   strategy, `--line-length 100` in place of `--config`; then marimo's own check. A strategy made
   before template 0.20.0 has no ignores for a marimo notebook in its settings, and the notebook,
   written as above, needs none. Checked with ruff 0.17.3 and marimo 0.25.2 on 2026-10-27:

   ```bash
   uvx ruff check --no-cache --config "<strategy>/pyproject.toml" "<folder>/known_answer_marimo.py"
   uvx --from marimo marimo check --strict "<folder>/known_answer_marimo.py"
   ```

2. **The owner runs it**, on either track: cell by cell in marimo's editor, where every figure
   shows, or as a script by the second line below, pasted into a terminal, each with a `--with`
   for each package the method imports. The script shows only whether Verify passed or which raise
   fired; the figures are read in the editor. It saves nothing — the notebook stays as written —
   and a raise prints its message and exits 1, checked by running it on 2026-10-27 with marimo
   0.25.2 and NumPy 2.5.4: it passed, and with the method's intercept dropped it raised and exited
   1, both folders unchanged.

   ```bash
   uv run --no-project --with marimo --with numpy marimo edit "<folder>/known_answer_marimo.py"
   uv run --no-project --with marimo --with numpy python "<folder>/known_answer_marimo.py"
   ```

   The editor keeps its session beside the notebook, in `__marimo__/`, with the figures it showed:
   the simulation's, never the owner's data. It is marimo's, and deleting it loses nothing.

3. **Read** it with the owner, from their run: Verify passed, or which raise fired, with its
   message; then their prediction against what came back, their reading first, on the no-code
   track section by section. The figures are the notebook's, pointed to by cell, and the
   researcher never states, confirms or corrects one; none goes into the strategy's documents as
   evidence about the market.
4. **A miss** is the method's until shown otherwise: the size and the tolerance were set first. Name
   what the recipe's failure suggests to look at; the fix is the owner's, in their own file.
5. **A record**, when the owner wants one in the strategy — a dated line in `JOURNAL_N.md` — is
   written as `experiment-lifecycle` says, on its own plan and go, never by this skill.

## What it never does

- **Run the notebook**, or state, confirm or correct a figure it prints: the owner runs it and
  reads it.
- **Write anything but the one notebook**, or write in a strategy, a course's clone or the home.
- **Read real data, or compute a figure about a book**: an IC, a return, a Sharpe or an attribution
  of the owner's comes from their own run and the engines.
- **Rewrite the owner's method to pass, or widen a tolerance after a miss.**
- **Copy code** from a book, a course or a library into the notebook: the simulation and the check
  are written fresh from the recipe's formulas.
- **Cite a source as evidence**: a source a recipe names is a lead, and the theory is `teach`'s and
  `query`'s.
- **Run in a block with the AI off**, or give investment advice.

## References

- `references/recipes.md` — nine recipes, one per model: the model, its true parameters, a seed,
  the estimator to check, the tolerance and why, and the failure to show, in prose and formulas.
