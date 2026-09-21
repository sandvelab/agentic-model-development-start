# Commit run (Rule 4)

Tie commits to results, and version the instructions as part of the method.

**Usage:** `/commit-run before <node>` · `/commit-run after <node>` ·
`/commit-run` — infer from context which of the two is meant

---

## Why the cadence differs from ordinary development

You rewrite code continuously, often several times within one response. The code state
behind a given result is far more fleeting than when a human edited a script twice a day,
so "commit at the end of the session" is no longer a meaningful granularity.

**Any result that might be reported should correspond to a commit.** Commit before an
analysis run and after it, with the run named in the message, and write the resulting hash
into the provenance record. Frequent small commits are cheap, and this history is not for
reading — it is an addressing scheme.

## The instructions are part of the method

`AGENTS.md` and `.claude/commands/` determine what code gets written, as does
`.claude/agents/` where a project defines subagents. **This project defines none**, so that
directory is empty and, git not tracking empty directories, absent from every checkout —
do not go looking for it.
Two runs of this repository under different instructions are **two different methods**, and
a mid-project change to them is a methodological change a reader must be able to see. So:

- version them with the same discipline as the analysis code;
- record in each provenance record which instruction-set commit was in force;
- when you change them, say so in the commit message in those terms.

## What does not belong in git

Large intermediates and data. Use a data store with content-addressed references from the
repository. The distinction: things whose *evolution* matters (code, instructions, claims)
are versioned; things whose *identity* matters (data, results) are addressed.

## Before pushing

Never push on your own initiative — ask. `/release` handles the secrets and data-permission
scan that must precede anything becoming public.
