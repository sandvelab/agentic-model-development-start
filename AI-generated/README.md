# AI-generated

Derived documents. Most of what will be here is produced by a recorded recipe and can be
rebuilt, so it can also be deleted without loss — and should be, when its source goes away.
`batch-reports/` is the exception: it is an account of what happened during one batch, and
no re-run produces the same report twice, so it is never pruned.

**Never hand-edit anything here.** An edit is lost on the next run and is wrong in the
meantime. If a derived document is wrong, its source is wrong.

## What a project puts here

- `batch-reports/` — one report per executed batch, written by `/do`, named
  `YY-MM-DD_bNN_shortName.md`. Not regenerable; never pruned.
- `hierarchical-report/` — the drill-down over the tree, from `/hierarchical-report`.
  Gitignored except its `provenance.md`.
- `validation/` — what `/validate cleanroom` and `/validate outsider` found, per run.
- `determinism-checks/` — Rule 6: each model run twice and diffed.
- `reproducibility-report/` — the closing report, from `/repro-report`.
- Reconnaissance of external systems (what the evaluation platform does, what the model
  library holds), where a project needs to establish such facts before relying on them.

## Currently here

Nothing yet.
