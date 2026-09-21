# Claims (Rule 9)

Maintain the claim collection — the bridge from results to text.

**Usage:** `/claims add <statement>` · `/claims list` · `/claims audit` ·
`/claims check-text <manuscript>` — flag draft sentences with no supporting claim

No argument: print this list and run nothing.

---

## The two-step writing process

Never write from results straight into the manuscript. Go through the collection:

**Step 1 — results to claims.** Each claim is a short statement the analysis supports, with
an explicit pointer to the stored result grounding it, at the granularity of a specific file
or value. Also record: the node it belongs to, a scope qualifier, the alternatives that
would have supported a different statement and why they were not taken, and who authored it.

```bash
.venv/bin/python AI-internal/useful-scripts/claims.py add "…" \
    --grounds analysis/02_measure/a_jaccard/results/summary.tsv \
    --node analysis/02_measure/a_jaccard --by agent-autonomous
```

**Step 2 — claims to manuscript.** Draft from the collection, in any of three modes: you
draft from it; I draft and you insert grounded findings; or I draft freely and you match
each sentence back afterwards. Sentences carry a provenance annotation in a sidecar file
keyed by paragraph — more robust than inline comments, and it survives format conversion.

## What this buys

- Provenance runs unbroken from a sentence to a claim to a result to a command.
- The set of everything the analysis supports becomes searchable, independent of what
  reached the paper.
- **It is the practical control against fabricated content.** Requiring each generated
  sentence to name the stored result it rests on constrains generation to what exists.

That control is not complete: a pointer can be attached to a result that does not support
the statement. Which is why `/claims audit` (every pointer resolves) and `check-text` (every
sentence has a claim) are both worth running, and why neither replaces reading.

## The retrospective audit

`check-text` is worth running on a fully human-written draft too. Sentences it flags are
either unsupported or point at a claim nobody recorded. Both are worth knowing. It matches
on shared content words and is deliberately crude — its job is to narrow where a human
should look, never to decide.
