# Reproducibility report

The closing step of the project: a report on what can be tracked, and how.

**Usage:** `/repro-report` — generate from the current state of the repository

---

## When

After the analysis is finished and there is a final text — which need not be a full
manuscript; a short write-up is enough. Regenerate before release.

## Inputs

The final text · the claim collection · the claim tree · the provenance records · the
environment specifications.

## What it contains

1. **What was produced** — the results, at every level of the tree.
2. **What is tracked, and how** — the provenance chain from each statement in the text down
   to a claim, a result, a script, a commit and an environment. A provenance graph over the
   claim tree is the natural backbone.
3. **The veridical section** — which alternatives were explored, on what basis each choice
   was made, how stable the conclusions were across the perturbation set, and what was left
   unexplored and why.
4. **The agency record** — which decisions were mine and which yours, from the `agency`
   fields, summarised honestly. Do not flatter either party's contribution.
5. **What does not hold** — every place the chain is broken, incomplete, or verified only
   partially.

Section 5 is not optional and is the section a critical reader will value most. A
reproducibility report that reports only success is an advertisement.

## Degrade gracefully

Run against a project that followed none of these rules, this should still produce an honest
account of what little can be established. That is itself a useful diagnostic, and it is why
the report is written from the artifacts rather than from a checklist of what should exist.
