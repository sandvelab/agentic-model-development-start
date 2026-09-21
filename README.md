# agentic-model-development-start

A starting point for developing machine-learning models with an agentic AI system,
**reproducibly and veridically**: every reported number traces to a file that was executed,
every judgment call is recorded with its alternatives, and the paths not taken stay in the
repository, runnable. Copy it, anchor it to an evaluation platform, a set of modelling
resources and a dataset, and the agent develops or improves a model inside a structure
where the right thing is the easy thing and the wrong thing is detectable.

This file is the introduction for **humans**. The agent's standing instructions are
`AGENTS.md`; `MOTIVATION.md` explains, for both readers, why the repository is shaped the way
it is.

## What it is for

One project at a time: **develop, or improve on, one model** — a forecaster, a classifier,
a two-stage ensemble, a fine-tuned baseline — and **establish whether it earns its place**
against the baselines and reference models the project names, together with the complete
record of how that conclusion came about. The output is a model with a defensible score
*and* the record; neither is subordinate to the other. When the project is finished, the
repository is its published record: analysis, alternatives, claims, manuscript and the
instructions the agent worked under.

It is not a general-purpose ML sandbox, a notebook collection or a personal knowledge base.
Its structure is deliberately narrow so that it can be trusted.

## Why it exists

Reproducibility guidance has long been an effort problem more than a knowledge problem, and
an agent makes the meticulous recording nearly free. But agents also add three new ways to
go wrong: computing in their own context so a number never touches disk; traversing a large
analytic space quickly enough to tune silently to a target; and dropping a standing rule at
step twenty-one of a long session without anything looking wrong. Each of these has a
structural answer here — a tree of questions rather than a pipeline of steps, verification
by code rather than by reminder, text written only from grounded claims — and `MOTIVATION.md`
sets them out. The principles are those of **veridical data science** (Yu & Kumbier's
predictability, computability and stability) applied to model development: it is not enough
that the pipeline reproduces; the conclusion has to survive the reasonable alternative ways
the analysis could have been done.

## How a project starts here

1. **Copy the repository** and follow `setup-guide.md`. Ten minutes: a placeholder in
   `.claude/settings.json`, a `.venv`, an invariant check on the empty tree.
2. **Fix the three anchors**, with the agent proposing and you deciding. They go into
   `readme-at-start.md` and the plan.

   | Anchor | What is pinned |
   |---|---|
   | **Evaluation platform or harness** | What scores a model and how: the platform and its version (or the project's own scoring code, verified against a reference before it is trusted), the metric, the backtest or split scheme, the required baselines and any reference model. Examples of the kind of thing this names: a domain platform such as [Chap](https://github.com/dhis2/chap-core) for climate-health forecasting, a benchmark suite, a competition harness. |
   | **Modelling resources to start from** | The model library, reference implementation, or published method the project develops from or improves on — pinned by commit or version, archived under `Archive/` with `provenance.md`. Examples: a community model repository, a baseline the platform ships, a paper's released code. |
   | **Data** | Source, exact version fetched, licence, and the development/holdout split — with the holdout sealed before development starts and opened once, at the end. |

3. **Write the plan** with the agent, from `Human-input/Plans for AI generation/plan-template.md`:
   the aim, what "better" means, the non-negotiables, the decisions already made, and a batch
   ledger. The test of a finished plan is that a session with no memory of the planning
   conversation can run it end to end without asking anything.
4. **Run it one batch at a time** with `/do`. Each batch leaves a report, commits before and
   after every run, writes a provenance record for every result, and stops. You read the
   report, settle what the batch left open, and start the next.
5. **Finish**: stability across the judgment calls, one opening of the holdout against a
   manifest frozen beforehand, claims, manuscript, clean-room and outsider validation,
   release.

## What the agent is held to

Ten rules, each with a skill of the same name, and a stance that veridical work is part of
the analysis rather than a postscript. In one breath: every result comes from an executed
file; no output is ever edited in place; environments are pinned and rebuilt clean; every
run is committed before and after; intermediates are stored; seeds derive from one project
seed; every plot ships its data; the report is hierarchical down to the raw values; every
sentence traces to a claim to a result to a command; the release is the whole tree,
alternatives included. `/validate` checks the rules with code, because instructions are not
guarantees. `AGENTS.md` has the full statement.

## Structure

| Path | Holds |
|---|---|
| `readme-at-start.md` | What *this particular* project is. A template until a project is defined. |
| `AGENTS.md` | The agent's standing instructions — the single source of truth for how work is done. |
| `MOTIVATION.md` | Why the repository is shaped this way. |
| `setup-guide.md` · `folder-structure.md` | How to start a project from this copy; what each folder is for. |
| `analysis/` | The claim tree. `analysis/run.sh` reproduces the whole reported analysis. |
| `environment/` | The one pinned analysis environment; nodes override only where they must. |
| `Archive/` | Imported data, models and documents — pinned, checksummed, never edited. |
| `Human-input/Plans for AI generation/` | Plans the agent executes, one batch per `/do`, and the plan template. |
| `Human-AI-collaboration/claims/` · `manuscript/` | The claim collection, and the article written from it. |
| `AI-generated/` | Derived documents: batch reports, the hierarchical report, validation findings. |
| `AI-internal/` | The machinery: `node.py`, `check_invariants.py`, `claims.py`, `build_hierarchical_report.py`, skill references, the task log. |
| `.claude/commands/` | The seventeen skills. `CLAUDE.md` is a pointer to `AGENTS.md`. |

## Two readers

**If you are a person**: read this file, then `setup-guide.md`, then `MOTIVATION.md`. You
write plans, settle the decisions the agent brings you, hand-edit outputs only through the
`_edited` convention, and decide what is pruned and what is pushed.

**If you are an agent**: `CLAUDE.md` sends you to `AGENTS.md`. Read it in full, then
`readme-at-start.md`. If that file still carries placeholders, §0 of `AGENTS.md` says what
to do and what not to do.

## Licence

Two licences, because this repository is both a record and a program. `LICENSE` (CC BY 4.0)
covers the documents, data, records and prose; `LICENSE-CODE` (MIT) covers the scripts,
every `run.sh`, `.claude/`, `environment/` and `AI-internal/useful-scripts/`. Material under
`Archive/` also carries the terms it came with, stated per directory in each `provenance.md`.
