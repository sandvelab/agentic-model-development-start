# Setting up a project from this starting point

This repository is a **starting point, not a finished project**. It carries the structure,
the instructions and the skills; the project is yours to fill in. `README.md` says what the
repository is for; this file is the mechanical part.

## 1 — Get a copy

Either clone and re-point the remote:

```bash
git clone https://github.com/sandvelab/agentic-model-development-start.git my-project
cd my-project
git remote remove origin        # this copy is a new project, not a fork of the template
```

or copy the tree out and start a fresh history:

```bash
cp -r /path/to/agentic-model-development-start/. /path/to/my-project/
cd /path/to/my-project && rm -rf .git && git init
```

The trailing dot in `cp` matters, or `.claude/` is left behind.

## 2 — Substitute the placeholders

`.claude/settings.json` contains `<PARENT_DIR>` and `<HOME>`. Replace both with real paths,
or delete the `claudeMdExcludes` entries you do not need — they exist to stop a parent
directory's `CLAUDE.md` leaking into this project's instructions, which would silently
change the method.

## 3 — Python environment for the machinery

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
```

Invoke it directly as `.venv/bin/python` — never `source .venv/bin/activate && python`.
Activation is a second shell segment, which turns a pre-approved command into a permission
prompt on every call. The machinery (`AI-internal/useful-scripts/`) uses only the standard
library, so nothing else needs installing here.

## 4 — Check it works before there is anything in it

```bash
.venv/bin/python AI-internal/useful-scripts/check_invariants.py
.venv/bin/python AI-internal/useful-scripts/node.py tree
```

An empty tree should pass every check except `git` (until you commit). If it does not, fix
that before adding analysis — a checker you have learned to ignore is worse than none.

## 5 — Fix the anchors, with the agent

Open a session. The agent reads `AGENTS.md` and finds `readme-at-start.md` still holding
placeholders, and §0 of `AGENTS.md` tells it what to do: help you fix the **evaluation
platform or harness**, the **modelling resources to start from** and the **data**, each
pinned and archived under `Archive/` with a `provenance.md`. The agent proposes, retrieves
and reads; you decide. Everything it retrieves is `agent-retrieved`; everything you point it
at is `human-pointed`; both are recorded.

## 6 — Write the plan

From `Human-input/Plans for AI generation/plan-template.md`, named `YY-MM-DD_camelCaseName.md`.
The aim, what "better" means, the non-negotiables, the decisions already made (the anchors
go here), and a batch ledger. Planning happens while you are present to answer questions, so
that execution — possibly days later, in a session with none of the planning conversation in
context — does not stall on something one sentence would have settled.

## 7 — Fill in `readme-at-start.md` and the root claim

Before doing any real work. In particular fix the **project seed**, the **tracking level**
and the **compute budget for stability work** — these are the three settings that otherwise
get decided implicitly, halfway through, by whoever is impatient. Then edit
`analysis/claim.md` with the one question this project answers; everything in the tree
hangs off it, so it is worth more than one draft.

## 8 — Pin the analysis environment

The analysis environment is **not** the `.venv` that runs the machinery. Fill in
`environment/environment.yml` with what the analysis itself needs, then `/pin-environment`
to build `environment/env/` and write `environment/lock.txt`, and `/pin-environment verify`
to confirm it rebuilds clean. This usually happens in the first or second batch, once the
first model's actual library needs are known rather than guessed.

## 9 — Git

```bash
git add . && git commit -m "Start from agentic-model-development-start"
```

For a remote, the agent will ask you for the owner/organisation and repository name rather
than inferring either. Keep it **private until release**; `/release` runs the secrets and
data-permission scan that must precede anything becoming public.

## 10 — Run the first batch

```bash
/do <plan name>
```

The first batch orients and sets up — verifies the archived anchors' checksums, stands up
the environment, writes the root claim, raises what the plan left open — and does no
modelling. Each later batch runs, reports, and stops.

## What to change, and what not to

**Change freely**: `readme-at-start.md`, `analysis/claim.md`, the environment, the plans,
anything in `Human-input/`.

**Change deliberately**: `AGENTS.md` and `.claude/commands/`. They are part of the method —
a change to them is a methodological change, and it is published as such. Commit it on its
own, with a message saying what changed about the method.

**Do not weaken**: `check_invariants.py`. When it fails, fix the cause.
