# Blueprint — Experiment 1

> **The hypothesis, fixed once written.** Thesis, the claim it moves, rules, predictions, success
> criteria, what would falsify it and key risks, recorded *before* any code runs.
>
> **This file does not change when results arrive.** A hypothesis edited after its test is no longer
> a hypothesis — that is the whole reason it is kept apart from the result. What the experiment
> actually produced is in [`FINDINGS_1.md`](FINDINGS_1.md); the running log, the thinking
> before this blueprint included, in [`JOURNAL_1.md`](JOURNAL_1.md).
>
> In a new strategy, record the date it was written and delete this blockquote.

---

## Experiment 1 — the first rule against the benchmark

### Thesis

One paragraph: what book this rule produces, why it should beat the benchmark
`JOURNAL_1.md` chose, and why it is also a fair yardstick — sensible, liquid, low-complexity
— for judging whether any later idea adds value. **Be modest on purpose.** A first rule does not
assert its signal is the best of its kind, only that it is simple enough to be understood, liquid
enough to be traded, and stable enough to measure other things against.

### The claim this moves

Which claim of `OBJECTIVE.md`, by number, this experiment exists to move, the status it reaches if
the predictions below hold, and the one it reaches if they fail. **One claim.** An experiment that
could beat every benchmark and settle nothing is a measurement, not a test.

### Rules

- **Selection:** the eligibility condition, naming the column it reads.
- **Sizing:** the weighting scheme, and any bounds it sizes inside — a cap and a floor on each
  weight, and whether a capped name's excess goes to cash or to the other names. Named bounds are
  the design, and the control holds them too; every other constraint is switched off, a lever a
  later experiment has to earn.
- **Cash:** what the weights leave uninvested is cash, which the engine holds and pays interest
  on: name the rate file, the spread a broker keeps below it, and the cash reserve. The same rate
  is the risk-free rate of every Sharpe ratio the engine reports.
- **Costs, inside the engine:** commission in basis points of the notional; the slippage model and
  the half-spread it falls back on; and, registered now so it is never a forking path later, the
  flat half-spread every book is priced again at beside the model, a stress row and a small
  account. Then **what the cost model does not do**, by name.
- **Delistings and gaps:** a position whose prices stop is sold by the engine at its last price; a
  gap inside a series, which the engine cannot price, is a blocking row of the register, excluded
  by name from every book.
- **Timing:** calendar, or event-driven on a stated trigger. Say what happens between triggers,
  and name any no-trade band: how far a held name's target may move before it is traded, read
  back beside the rule in `JOURNAL_1.md` before this file is written.
- **Lag:** how many days between the signal and the fill, and what the engine adds on top.
- **Control:** the same rule with exactly one ingredient removed — name which — trading on this
  rule's own rebalance dates, so that the ingredient is the only difference. A control left to find
  its own dates differs in when it trades as well.
- **Screens deliberately absent**, and why each is redundant under the rules above.

### What this experiment should show

**Predictions, fixed before the run.** Each cites a `Bibliotheca/` note or a section of
`Data/analyzer_marimo.py`, which measures the signal but builds no book. Getting these right is
worth more than a good Sharpe; getting them wrong is worth more than a bad one.

| # | Prediction | Where it comes from | What would falsify it |
| --- | --- | --- | --- |
| 1 | what the book should do | a `Bibliotheca/` note, or the analyzer section and its number | the observation that would refute it |

Note anything you are watching but cannot predict, because nothing licenses a prediction about it.
Costs usually belong here.

### Success criteria

What the experiment has to show to count as a success, fixed now. At the least:

1. It beats the benchmark `JOURNAL_1.md` chose **and its own control** on risk-adjusted
   return, net, over the same window — performance criterion P1 of the gate in
   `Paper_Trading/BITACORA.md`.
2. Reproducible from a working copy whose data folders were emptied first, through the pipeline,
   with no manual step, every Verify passing — soundness criterion S5.
3. A tradeable trigger frequency — not a rule that fires every day.
4. Every prediction above evaluated explicitly in `FINDINGS_1.md`, **including the ones that turn
   out wrong.**

**Success is necessary for graduation, not sufficient.** The gate in `Paper_Trading/BITACORA.md`
decides it, in two layers — soundness, S1 to S5, then performance, P1 to P3 — and a person signs
it. Name here what will evidence each soundness row: the trial count and the sweep, the control
and the random books, the cost rows, the run from emptied data folders. A row without its evidence
does not hold, and a book whose soundness fails yields no conclusion at all.

### What would falsify it

**One condition for the whole experiment, fixed now.** Each prediction above has its own falsifier;
this is the result under which the experiment as a whole has failed — usually a margin against its
control, or a result that holds in one sub-period and not in the others. Then **the
changes that may not rescue it**: every setting that could be moved once the result is in — a
holding count, a trigger, a window, a threshold — by name. Moving one after the result is a new
experiment, and one more trial in the count.

### Key risks

- **Survivorship and point-in-time integrity.** The universe must include delisted names; step 2
  quantifies how many.
- **The signal's known weakness** — slow exits, whipsaw, regime dependence — named here, and either
  handled by the rules above or accepted on simplicity grounds and left to a later experiment.
- **Concentration.** How the weighting concentrates, and which diagnostics measure it.
- **The signal may not be what earns the return.** If the book beats its benchmarks because of a
  factor exposure rather than the signal, the honest product is a cheaper factor fund. That is what
  step 6 exists to answer.

### Open questions this experiment deliberately does not answer

Each is a later experiment, and each has to beat this one.

| # | Question | Why it is not answered here |
| --- | --- | --- |
| 1 | the question | why this experiment leaves it open |
