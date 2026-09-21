# AGENTS.md

The standing instructions for any agentic AI system working in this repository — the single source of truth for how work is done here. (`CLAUDE.md` is a pointer to this file, and carries no instructions of its own.) It refers to the agent as "you" and the human researcher as I/me.

**This repository exists to carry out one research project and produce one article from it, with full provenance.** Everything below serves that. It is not a personal knowledge base, it does not accumulate general notes, and it does not grow new subject areas over time. When the project is finished, the repository is the published record of it.

**Read `readme-at-start.md` first in every new session.** It says what *this particular* project is. `MOTIVATION.md` says why the repository is shaped the way it is; read it once, and again whenever you are tempted to work outside the structure.

---

## 0 — A fresh copy, before there is a project

This repository is distributed as a **starting point**. A copy of it has no project until `readme-at-start.md` has been filled in; while that file still carries `<placeholders>`, the project is undefined and **no analysis is done**. What is done instead, in dialogue with me:

1. **Set up** the copy per `setup-guide.md`: substitute the placeholders in `.claude/settings.json`, create `.venv`, run the invariant checker on the empty tree.
2. **Fix the anchors.** A model-development project here is anchored to three external things, each named and pinned before work starts, and each recorded in `readme-at-start.md`'s *Where the project starts from* table and in the plan's §4:
   - **an evaluation platform or harness** — what scores a model and how (the platform, its version, the metric, the backtest or split scheme, the required baselines). If the project scores with its own code instead, that code is verified against a known-correct reference before it is trusted;
   - **the modelling resources it starts from** — a model library, a reference model, a baseline implementation, a paper's method — each pinned by commit or version and archived under `Archive/` with `provenance.md`;
   - **the data** — its source, the exact version fetched, its licence, and the development/holdout split, with the holdout sealed before development starts.
   You may propose candidates for each anchor, retrieved and read rather than recalled; I decide. Ask me for anything the anchors leave open rather than inferring it.
3. **Write the first plan** with me, from `Human-input/Plans for AI generation/plan-template.md`. The test of a finished plan: a session with none of the planning conversation in context can run it end to end without asking anything.
4. **Fill in `readme-at-start.md`** from the plan — in particular the project seed, the tracking level and the compute budget for stability work, which otherwise get decided implicitly, halfway through, by whoever is impatient.
5. **Archive the plan as delivered** to `Archive/plan-as-delivered/`, so later drift is measurable, and run the first batch with `/do`. The first batch orients and sets up; it does no modelling.

From then on, everything below applies without qualification.

---

## 1 — The two rules that override everything

**Every reported result must come from a file that was executed, not from something you did in your own context.** If you compute a number by reading it out of printed output and carrying it into the next step, that number has no provenance and the chain is broken on disk even though it looks complete in the transcript. No value crosses between steps except through a file. This is the single most likely way for this repository to end up dishonest, and it fails silently.

**Never edit a file you produced. Never edit a file under `Archive/`.** Corrections go through the mechanisms below (`/manual-edit` for my hand edits, a re-run for yours). A result that was quietly patched into shape is worse than a wrong one, because nothing records that it happened.

## 2 — How the project is organised

The analysis is a **tree of claims**. A *claim* is an analytical aim — a question to be explored — written as one or two sentences of plain text. It is not an assertion. What a node's analysis *yields* is recorded as an answer, and those answers are what populate the claim collection.

Each node is a directory holding:

| Path | Contents |
|---|---|
| `claim.md` | The analytical aim; the relationship type of this node's children; for alternatives, which child is the main path; any environment override and why. Once run, the answer(s) yielded. |
| `run.sh` | **The main script.** A short list of shell lines: calls to the main scripts of this node's children, and calls to the scripts stored at this node. Nothing else. |
| `scripts/` | Every script file used by this node's own analyses. |
| `results/` | What this node's analyses produced, intermediates and plot data included. |
| `env/` | **Only** where this node needs something beyond `environment/`. |
| `provenance/` | One record per result produced at this node. |

Children are subdirectories. `analysis/` is the root node.

**Parent–child relationships come in exactly two kinds, and the kind is a property of a node's whole set of children, not of individual edges.** Where a question needs both, interpose a node.

- **Alternatives** — the children are competing paths for the same parent claim: each child claim is one possible interpretation of the parent claim, or one possible strategy for answering it. Exactly one is annotated as the main path, and **the parent's `run.sh` calls only that child's `run.sh`** — nothing else. An alternatives node is a pure switch and stores no scripts of its own.
- **Sub-analyses** — the children are supporting parts of a parallel or sequential approach to the parent claim. The parent's `run.sh` calls **every** child's `run.sh`, in the order the approach requires, alongside its own node-local scripts.

**`analysis/run.sh` reproduces the entire analysis**, following the main path at every alternatives fork. Never break that property. The paths not taken stay in the tree, complete and independently runnable; they are executed by the stability node, which calls its siblings' main scripts.

Use `/node` to create, inspect and re-annotate nodes rather than making directories by hand — it writes the scaffold in the expected shape and keeps the parent's `run.sh` consistent.

## 3 — The ten rules, and what each one demands of you

These are standing obligations, not things to be done at the end. The named skill is the invoked action; the obligation holds whether or not you invoke it.

| Rule | Obligation | Skill |
|---|---|---|
| 1. Keep track of how every result was produced | Every identifiable result gets a provenance record binding it to script, invocation, inputs, environment, seeds, commit and node. | `/track-result` |
| 2. Avoid manual data manipulation steps | You never edit your own output in place. My hand edits arrive as `<name>_edited.<ext>`; you detect the pair, treat the edited file as authoritative downstream, and record the diff as an input step. | `/manual-edit` |
| 3. Archive exact versions of external programs | Declarative spec, resolved lockfile and image; verified by building clean and re-running. | `/pin-environment` |
| 4. Version control all custom scripts | Commit before and after every analysis run, hash into the provenance record. **The instruction files are part of the method** — `AGENTS.md`, `CLAUDE.md` and `.claude/` are versioned with the same care as the code, and a change to them is a methodological change. | `/commit-run` |
| 5. Record all intermediate results | Store intermediates at every step, in the most suitable standard format, wherever space is not prohibitive by reasonable judgment. Never a language-specific pickle for anything outliving the session. | `/store-intermediates` |
| 6. Note underlying random seeds | One project-level seed, deterministically derived per component and recorded. Verified by running twice and diffing. | `/seed` |
| 7. Always store raw data behind plots | Every plot writes its plotted values, its pre-aggregation values where they differ, and its plotting script beside it. | `/plot` |
| 8. Generate hierarchical analysis output | Summaries link down to the values they aggregate, all the way to raw. Generated from the tree, as static HTML. | `/hierarchical-report` |
| 9. Connect textual statements to underlying results | Writing is two steps: results → claim collection → manuscript. Every sentence traces to a claim, to a result, to a command. | `/claims` |
| 10. Provide public access | The release is the whole tree, alternatives included, plus instructions, claims and provenance. Secrets and data-permission scan before anything is pushed. | `/release` |

Rules 1, 2, 4, 5, 6 and 7 apply continuously and without being asked. Rules 3, 8, 9 and 10 are things you do at identifiable moments, and their skills say when.

## 4 — Veridical work is part of the analysis, not a postscript

Reproducibility records what was done. It does not say whether the conclusion would survive a differently-but-equally-reasonably conducted analysis, and instability under reasonable alternative choices — not sampling noise — is the dominant way computational conclusions go wrong.

So: **record not only what was done, but the alternatives considered and rejected, on what basis, and whether the conclusion moves when they are taken instead.** Concretely —

- Every judgment call you make (a filtering threshold, a metric, a model family, a cleaning decision) is either an alternatives node in the tree or a logged decision in a provenance record. It is never silent.
- Where a judgment call has plausible alternatives, prefer making it an alternatives node so the paths not taken survive.
- The stability node runs the non-main alternatives and reports the distribution of conclusions across them, not the best one. `/perturb` plans and runs this.
- When a perturbation is not run for budget reasons, record that it was not run and why. An absence must be a visible decision.

**Agency is recorded.** Every decision carries who made it: `human-set`, `agent-on-human-assessment`, or `agent-autonomous`; and for information gathering, `agent-retrieved` or `human-pointed`. Do not flatter your own contribution or mine.

## 5 — Verification, because instructions are not guarantees

You will follow these instructions most of the time. A standing rule can be honoured for twenty steps and quietly dropped at the twenty-first, and nothing about the output looks wrong. Do not rely on remembering.

- Run `/validate invariants` at the end of every analysis and before every commit. It is deterministic code and has no attention budget.
- Run `/validate cleanroom` before any release, and on a schedule during a long project.
- Run `/validate outsider` after any substantial change to these instructions and before release. It starts a fresh agent with no context and asks it to *follow* the instructions rather than judge them; what it misunderstands is what an outsider would misunderstand.

If a check fails, fix the cause. Never adjust the check to pass.

## 6 — Trade-offs, made explicitly

- **Your processing against my effort.** Nearly everything here converts my effort into your tokens and wall-clock. That is usually a good exchange, but because each request is cheap, thoroughness expands without anyone deciding it should. The level of tracking this project warrants is stated in `readme-at-start.md`; work to that level, and raise it with me rather than drifting.
- **Reproducibility against storage.** Annotate what you store with `/annotate-criticality` — main or side result, regenerable or not, roughly what regeneration costs, how important for transparency — so pruning later is targeted. Do not delete up front.
- **Robustness against computation.** Estimate the cost of each perturbation, rank by expected informativeness, cut at the stated budget, and record where the line fell.

## 7 — Writing

- The manuscript lives in `Human-AI-collaboration/manuscript/`; the claim collection in `Human-AI-collaboration/claims/`. Nothing is written into the manuscript that does not trace to a claim.
- **Sourcing**: if a source is named, linked, or sitting in the repository, read it before writing about it. Never characterise what "the literature" says without having checked. If you write from memory because no source is reachable, say so in the chat reply — never in the document.
- **Never narrate the process.** The reader never saw our iterations. No "corrected from", "unlike the earlier version", "as we discussed". Write the document as if the final version had always been the plan. What changed belongs in the plan file or the chat reply.
- Be technically accurate; avoid hype. Trace technical choices back to their motivations. Introduce concepts conceptually before naming them technically. Question my assumptions and give honest technical feedback.
- **This repository writes articles and code. Nothing else.** No emails, no talking notes, no slide decks, no personal material.

## 8 — Working conventions

- **Plans and their execution.** A plan under `Human-input/Plans for AI generation/` is executed by `/do`, which saves the output, wires bidirectional wiki links between plan and output, and never overwrites a previous iteration. Iterations accumulate as `_v2`, `_v3`.
- **Provenance beside the file.** Any folder holding imported or generated documents carries a `provenance.md`, one section per file, with enough to re-obtain or re-generate it. Append; never overwrite an existing section.
- **`Archive/` is read-only.** Imported material is marked `(IS_SHADOW)` on line 2 and never edited. Anything needing modification is copied out first.
- **README per folder.** Every folder has a `README.md` saying what it is for and what is
  currently in it, 5–15 lines. Create it with the folder; update it when contents change
  materially. **Node directories under `analysis/` are the exception**: a node's `claim.md`
  says what it is for and what it yielded, and a README beside it would be a second place
  answering the same question. `/node` writes no README and none is owed. A README that
  restates state recorded elsewhere goes stale silently; keep each fact in one place.
- **Naming.** `YY-MM-DD_camelCaseName` for generated documents. Node directories are named
  by the relationship they stand in to their siblings: **sub-analyses children are numbered**
  `NN_shortName`, in the order the parent runs them, because that order is part of the
  approach; **alternatives children are lettered** `a_shortName`, `b_shortName`, because they
  are mutually exclusive and unordered, and only one of them ever runs on the main path. A
  number on an alternative would assert a sequence that does not exist. `/validate invariants`
  checks this.
- **Back up before editing.** Before editing any file under 1 MB, copy it to `/tmp/claude_backups/<filename>.<timestamp>.bak`.
- **Task log.** `/log-tasks` records completed work to `AI-internal/ai_task_history.md` and `ai_task_details.md`. Auto-invoke it when a substantial task ends, when I change topic, and at session end.
- **Python.** Two interpreters, and which one a script gets is decided by where the script lives, not by what it imports. **`.venv/bin/python`** runs the repository's own machinery — everything under `AI-internal/useful-scripts/`. **`environment/env/bin/python`** runs anything under `analysis/`, because a node's scripts are part of the result and the result is pinned; every `run.sh` sets `PYTHON` to it, and a node script that happens to import only the standard library is no exception. Invoke both directly, never `source …/activate && python`. Install into `.venv` with `.venv/bin/pip`; `environment/` is built from its lockfile and not installed into by hand.
- **Work that arrives outside a plan.** `/do` runs a batch of the plan. A request that does not come through the plan is still work this repository has to account for: give it a ledger row with an aim and a status, exactly as a batch added by a batch gets one, and log what it settled in the plan's §4b with its agency. Nothing is done here that the ledger does not name — a change with no row is a change with no record of why it was made.
- **Git.** Commit incrementally. Ask me for the owner/organisation and repository name before creating a remote — do not infer either. `.gitignore` covers `__pycache__/`, `*.pyc`, `.DS_Store`, `.venv/`, `.env`.

## 9 — What is deliberately not here

Do not add these, and do not propose them:

- **An insight-accumulation section in this file.** This repository presents one finished project to a public audience; it is not a personal knowledge base that grows conventions over time. If you learn something about how to work well, tell me in the chat and I will decide whether it belongs in the project's own record.
- **Generic indexes, archives and overviews of my material.** There is one project here. It needs a map of its analysis, not a map of a working life.
- **Anything personal, and any genre other than articles and code.**

---

## Available skills

Ten for the rules, five for the machinery around them, two carried over. Full definitions in `.claude/commands/`; the mechanics of the longer ones in `AI-internal/skill-references/`.

**The rules** — `/track-result` · `/manual-edit` · `/pin-environment` · `/commit-run` · `/store-intermediates` · `/seed` · `/plot` · `/hierarchical-report` · `/claims` · `/release`

**The machinery** — `/node` (the claim tree) · `/validate` (invariants, clean-room, outsider test) · `/perturb` (stability across judgment calls) · `/annotate-criticality` (the storage trade-off) · `/repro-report` (the closing report)

**Carried over** — `/do` (execute a plan) · `/log-tasks` (record completed work)
