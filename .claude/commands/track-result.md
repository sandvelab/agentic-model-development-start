# Track result (Rule 1)

Bind a result to how it was produced, so the pairing is an artifact rather than an inference.

**Usage:** `/track-result <result path>` — write the provenance record for one result ·
`/track-result --all <node>` — do it for every unrecorded result at a node

---

## When this runs

Whenever an identifiable result appears — a figure, a table, a number you will report, a
statement, a manuscript section. Do not batch it to the end of a session: the details you
need are in your context now and will not be later.

## What a record contains

Write one file per result to the node's `provenance/`, named after the result:

```
result: results/summary.tsv
script: scripts/summarise.py
        sha256:5b1d9c…
invocation: ../.venv/bin/python scripts/summarise.py --window 500 --min-count 3
inputs: ../01_prepare/results/regions_filtered.tsv  sha256:9f2c…
environment: environment/ (project main)
seeds: project seed 20260820, component seed 20260820-summarise
commit: a3f91c2
node: analysis/02_measure/a_jaccard
produced: 2026-08-20
alternatives-considered: median instead of mean; rejected because the distribution is
  bounded below and the mean is what the downstream test assumes
agency: agent-autonomous
```

**The `sha256:` under `script:` is not optional either, and it is the one field that goes
stale on its own.** A record is a running account: when a script changes, append a section
saying what changed and what has run on it since, rather than editing the digest above.
Earlier sections keep the version they name, because each describes a run that happened under
it. `/validate invariants`' `hashes` check fails when a record does not name the file's
current digest. The check exists because the failure is common and invisible: a record
describing a version of a script that no longer exists looks exactly like one that is right.

`alternatives-considered` and `agency` are not optional. A record that says only what was
done, with no account of what else was possible and who decided, is reproducible but not
veridical — see `AGENTS.md` §4. `agency` is one of `human-set`, `agent-on-human-assessment`,
`agent-autonomous`; for information gathering, `agent-retrieved` or `human-pointed`.

## The failure this exists to prevent

A result that never touched disk. If you computed a number by reading it out of printed
output and carrying it into the next step, there is nothing to write a record about, and
the record you write will be fiction. Go back and make the step write a file.

`/validate invariants` checks that every result has a record, that each record names an
existing script, commit and environment, and that the digest it gives for a file is that
file's current one. It cannot check that the record is *true* — that the script it names is
the one that ran, or that a digest belongs to the run it sits beside. That part is on you.
