# Store intermediates (Rule 5)

Keep the intermediate results, in formats that will still open.

**Usage:** `/store-intermediates <node>` — review what a node stores and fill the gaps ·
`/store-intermediates audit` — across the whole tree

---

## The standing instruction

Store intermediate results at every step, in the most suitable standard format, wherever
space is not prohibitive by reasonable judgment. This is continuous, not something to do
when asked.

## Format

Standard, self-describing and language-agnostic where such a format exists for the data
type; a documented plain-text form where it does not. **Never a language-specific pickle
for anything that must outlive the session** — it is a time bomb attached to a library
version.

## Why the old trade-off no longer binds

The original reason to hedge was human effort: writing serialisation code at each step,
choosing formats, judging where storage becomes prohibitive, and then writing more code to
summarise the intermediates or re-enter the pipeline mid-way. All of that is now close to
free, so the balance tips decisively toward storing.

Two benefits are also larger than they used to be. Partial re-execution is cheap to arrange
on demand — a sub-pipeline entering at any stored intermediate is minutes of throwaway
code. And **perturbation happens at intermediates**: asking how much a conclusion moves when
an upstream threshold changes requires the upstream output to exist in a form that can be
varied and fed back downstream. Without them, `/perturb` has nothing to work with.

## When to say no

The exception is still real — per-iteration outputs of a long sampling procedure, full
intermediate tensors, anything on the order of the raw data times the number of steps.
There, store a summary at that step instead, **annotate what was skipped and why**, and
record roughly what regenerating it would cost. Then run `/annotate-criticality`, which is
what makes the decision revisitable rather than final.
