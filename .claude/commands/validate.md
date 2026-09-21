# Validate

Check that the rules were actually followed — with code, not with memory.

**Usage:** `/validate invariants` · `/validate cleanroom` · `/validate outsider` · `/validate all`

No argument: print this list and run nothing.

---

## Why this skill exists

You will follow the instructions in `AGENTS.md` most of the time. A standing rule can be
honoured for twenty steps and quietly dropped at the twenty-first, and nothing about the
output looks wrong. The party being reminded is not the party who cares about the result,
so the remedy cannot be another reminder.

**If a check fails, fix the cause. Never adjust the check so it passes.** That converts the
one honest signal here into decoration.

## invariants — every commit, every analysis end

```bash
.venv/bin/python AI-internal/useful-scripts/check_invariants.py
```

Deterministic code asserting what the rules imply: tree semantics hold; every result has a
provenance record; **every digest a record gives is the file's current one**; every plot has
its data and script; every stochastic script has a seed; every claim resolves; the working tree is clean
and every commit a record names is an ancestor of HEAD; and no value looks transcribed
between steps by hand. Ordinary code, no attention budget.

A project adds checks as its own discipline acquires structure — that every stability
combination on disk is one the manifest planned, that a holdout manifest frozen before the
holdout opened has not moved since. `AI-internal/skill-references/checks-to-add.md` describes
these patterns; add them when the structure they check exists, not before.

## cleanroom — before release, and on a schedule during a long project

Build the environment from nothing, run `analysis/run.sh`, compare against the archived
results, and report differences rather than announcing success. Run it on a schedule, not
only at submission: it is how you find out an upstream dependency changed while you were
still writing.

## outsider — after any substantial change to the instructions, and before release

Start a **fresh agent with no context** — a subagent is enough — give it only what a reader
would have (the repository and its instructions, no conversation history), and ask it to
**follow** the instructions, not to judge them. A system asked whether instructions are
clear will say yes; a system asked to follow them fails visibly at the ambiguous step.

Record what it got wrong, fix the documentation, repeat. What it misunderstands is what an
outsider would misunderstand — and the failures are almost always assumptions nobody knew
they were making. This is the closest thing here to an objective check, and it replaces a
judgment that was never reliable.

## What validation cannot do

These checks confirm the record is structurally **complete**, not that it is **true**. A
provenance record can name the wrong script; a claim can point at a result that does not
support it. Structural checking narrows where a human must look. It does not remove the
need to look.

Put sharply: **these checks verify shape and never content.** One thing sits across that
line — a record's digest is checked against the file rather than merely being present — and
the rest of the line is where it was. A number can be right and its noun wrong, and nothing
here looks at nouns. The outsider test is the check that finds statements true as prose and
false as behaviour, and it finds them only when it is run.
