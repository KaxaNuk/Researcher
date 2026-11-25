# Pipeline — how the code runs, and how to debug it

> **How this strategy's code runs:** what runs, in what order, what each step reads and writes,
> where the rule lives in the code, and what to check when something looks wrong. The *why* of the
> rule is `BLUEPRINT_N.md`, the numbers are `FINDINGS_N.md`; this file is for the person who has to
> run it again, or find out why a run stopped.
>
> Write it once the pipeline has run end to end, and keep it current: a step that moves, a file
> that is renamed or a run that takes twice as long changes this file in the same commit.

---

## 1. The run, in order

*A table: the step, the one command that runs it from the repository root, what it reads, what it
writes, and how long it takes from nothing. Then any file a step does not write but needs, and
where it comes from.*

## 2. Step by step

*Each step in a few lines: what it does to its input, the bookkeeping it writes beside its output,
and what it checks before it stops.*

## 3. The columns the rule reads

*Each column the rule consumes, what it is, and the file and function that build it.*

## 4. The rule in the code

*Where eligibility, ranking, sizing, the band and the rebalance dates live: the notebook cell and
the functions of the shared modules, named, so a reader can go from the blueprint's sentence to the
line that does it.*

## 5. Debugging recipes

*Short, runnable snippets for the questions a run raises: one name end to end, one name's signals,
one date's book and why a name is in or out, a priced run read without the engine.*

## 6. Where to find what a run printed

*Which log or file each step's output lands in, and what to read first.*

## 7. Common failures

*The failures seen so far, each with its symptom, its cause and its fix.*
