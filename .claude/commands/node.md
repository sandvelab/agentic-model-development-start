# Node

Create, inspect and re-annotate nodes in the analysis claim tree.

**Usage:** `/node tree` · `/node new <parent> <name> "<claim>"` · `/node show <path>` ·
`/node promote <alternatives-node> <child>` · `/node rebuild <path>`

No argument: print this list and run nothing.

---

Always go through the script rather than making directories by hand — it writes the scaffold
in the expected shape and keeps each parent's `run.sh` consistent with the semantics.

```bash
.venv/bin/python AI-internal/useful-scripts/node.py tree
.venv/bin/python AI-internal/useful-scripts/node.py new analysis 02_measure \
    --claim "By what measure should co-occurrence be quantified?" --kind alternatives
```

## What a claim is

An **analytical aim** — a question to be explored — in one or two sentences. Not an
assertion. What the node's analysis *yields* is an answer, and answers go to `/claims`.
Getting this backwards is the most common way the tree stops working: a tree of assertions
has no meaningful notion of an alternative.

## The two relationship types

The kind is a property of a node's **whole set of children**, not of individual edges.
Where a question needs both, interpose a node.

- **`alternatives`** — competing paths for the same parent claim, each child one possible
  interpretation or solution strategy. One is the main path, and the parent's `run.sh` calls
  **only** that child. So an alternatives node is a pure switch and stores no scripts of its
  own; the script enforces this.
- **`sub-analyses`** — supporting parts of a parallel or sequential approach. The parent
  calls **every** child, in directory order, then its own scripts.

Name child directories for the relationship they stand in: **sub-analyses are numbered**
`NN_name`, in the order the parent runs them; **alternatives are lettered** `a_name`,
`b_name`, because they are unordered and only one runs. `/validate invariants` checks it.

## Two properties never to break

`analysis/run.sh` reproduces the entire reported analysis, following the main path at every
fork. And the paths not taken stay in the tree, complete and runnable — they are executed
by the stability node, which calls its siblings' main scripts. `/validate invariants` checks
both.

## Promoting

When an alternative turns out to be the better path, `promote` moves the main-path marker
and rewrites the parent's one-line `run.sh`. Commit it as its own change: the history is
then the record that the switch happened and when, which is exactly the kind of decision
that otherwise disappears.
