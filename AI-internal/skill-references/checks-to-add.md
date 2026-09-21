# Invariant checks a project adds

`check_invariants.py` ships with the checks every project needs: tree semantics, provenance
records, digests, plots, seeds, claims, git, hand-crossed values. Three more have proved
their worth in projects run from this starting point, and each depends on structure a fresh
copy does not have. **Add them when that structure exists, not before** — a check that
guards a file nobody has written is decoration — and add them as code in
`check_invariants.py`'s `CHECKS` table, never as a resolution to be careful.

## `combos` — the combination space is closed

**Structure it assumes.** A stability node (`/perturb`) that plans its sweep in a manifest,
`results/manifest.csv`, one row per combination with the fork it moves and the child it
takes, and nodes downstream that write each combination's outputs to `results/<combination>/`.

**What it asserts.** Every `results/<combination>/` directory anywhere in the tree is one a
manifest names (with `main`, the reported analysis, always allowed); and the manifest's
first-tier rows agree exactly with the tree's non-main alternatives children.

**What it caught.** A `results/` subdirectory nobody planned — a scratch run, a combination
renamed halfway, a typo that created a second directory beside the real one — is a set of
numbers with no row in the manifest, and therefore an analysis that is in the repository and
not in anything reported. And a fork added to the tree after the manifest was written is a
reasonable alternative the stability run does not know about: the silent absence `AGENTS.md`
§4 forbids.

**Note.** `check_provenance` already accepts `results/$COMBO/<file>` as an alias covering
every combination of one artefact. That alias is only safe when this check makes the set of
combinations closed; until it exists, review combination directories by hand.

## `freeze` — the holdout manifest was frozen before the holdout opened, and has not moved

**Structure it assumes.** A holdout manifest, `manifest_holdout.csv`, fixing what is
evaluated on the held-out data; a `holdout_freeze.json` beside it recording that file's
sha256 and the commit that added it; holdout outputs under `results/<combination>__holdout/`.

**What it asserts.** The manifest's current sha256 equals the recorded one; its row count
matches; and at the commit that added the manifest, `git ls-tree` shows no holdout result
anywhere in the tree — so the set was fixed before the year was opened, and has not been
rewritten since. Checked against git rather than believed.

**What it caught.** A freezing script that rebuilt the set on every run of `analysis/run.sh`
and returned the same bytes only because the tree had not changed. The whole holdout spread
rests on this one file being a measurement rather than a selection, and prose claiming it
was frozen is not evidence.

## `pool` — a registered ensemble membership is the membership that ran

**Structure it assumes.** An ensemble or pooled model that registers, before it runs, which
members it will have (a `premise` in a specification file), and a record of which members
were actually assembled.

**What it asserts.** No two registered members sit under one alternatives fork (two
constructions of one baseline are one member, whichever the combination takes); the
registered members equal the ones the assembler recorded for the same combination; and any
copy of the premise embedded in a downstream specification matches the child's own.

**What it caught.** A weighting child that counted contract directories while the pool
resolved each fork to one child, so the same run printed *six members at 1/6* and *four
members* three lines apart — for ten days and forty combinations. With equal weights the
count *is* the model, so a premise describing a different pool is a prediction registered
about a model that was not run.

## The general shape

Each of these has the same form: a project introduces a file that makes a promise (a plan,
a freeze, a premise), and the check compares the promise with what is on disk and in git.
When your project introduces such a file, write its check the same day.
