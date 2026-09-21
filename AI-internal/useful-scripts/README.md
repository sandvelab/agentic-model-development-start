# useful-scripts

The repository's own machinery: the code that maintains and checks the analysis, as opposed
to the code that performs it. Every Python script here has a **dual interface** — a
programmatic API and a CLI — so it is useful both as a library and standalone. Invoke as
`.venv/bin/python AI-internal/useful-scripts/<name>.py`. Standard library only.

Note the two interpreters: these run under `.venv` (the repository's tooling), while the
analysis itself runs under the pinned analysis environment at `environment/env/`.

| Script | What it does | Skill |
|---|---|---|
| `node.py` | Create, inspect, promote and rebuild claim-tree nodes, enforcing the alternatives/sub-analyses semantics so they cannot drift by hand | `/node` |
| `check_invariants.py` | The deterministic checks: tree, provenance, hashes, plots, seeds, claims, git, and values crossing steps by hand | `/validate invariants` |
| `claims.py` | Maintain and audit the claim collection; flag draft sentences with no supporting claim | `/claims` |
| `build_hierarchical_report.py` | Generate the linked static-HTML drill-down report from the tree | `/hierarchical-report` |

`check_invariants.py` exits non-zero on any failure, so it works in a pre-commit hook or CI.
**When it fails, fix the cause — never weaken the check.**

A project adds scripts here as it needs them — a data fetcher, a release scanner, a
clean-room harness, a determinism check, a stability-manifest planner — following this
table's format and this file's convention of one row per script. Checks a project typically
adds to `check_invariants.py` once its own structure exists are described in
`../skill-references/checks-to-add.md`. `build_hierarchical_report.py` likewise gains the
within-result levels (a reported mean down to the values it averages) once the project
knows what its result files look like.
