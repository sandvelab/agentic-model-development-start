# Hierarchical report (Rule 8)

Generate the linked drill-down report over the claim tree.

**Usage:** `/hierarchical-report` — regenerate · `/hierarchical-report --open` — and open it

---

## What it does

```bash
.venv/bin/python AI-internal/useful-scripts/build_hierarchical_report.py --open
```

Walks `analysis/`, writing static HTML to `AI-generated/hierarchical-report/` in which each
node's claim, answers, results, scripts, provenance and `run.sh` are one click from its
parent, down to the raw files. Alternatives are marked main-path or not-taken.

**Never hand-edit the output.** It is generated from the tree, so its structure follows the
analysis rather than being maintained separately; an edit is lost on the next run and is a
lie in the meantime. If the report is wrong, the tree is wrong.

Regenerate after any structural change to the tree, and before every release.

## Why static HTML

It costs nothing to keep, needs no server, and will still open in twenty years. This is a
case where the old technology is the right one.

## Who reads it

**You do.** When debugging, or when a later session needs detail from an earlier one, the
stored detail is free where regenerating it is not, and it is what the analysis actually
produced rather than what a reconstruction produces. It also removes the debug-output
anti-pattern — adding print statements, running, reading, removing them — which modifies
working code, sometimes leaves residue, and throws the output away.

**I do.** I can ask you to investigate, but a conversation is a narrow channel. Scanning a
structure visually for the thing that looks wrong is something I do far faster than I can
describe what I am looking for, which is what asking would require.
