# How to use this repository

A practical walkthrough for a human: what is here, what to ask the agent for, how work moves
through the repository, and where to find the results, the article and the logs afterwards.

This file is the *order of operations*. It does not restate the canonical documents, it
points at them — [README.md](README.md) (what the repository is for),
[setup-guide.md](setup-guide.md) (the mechanical set-up),
[folder-structure.md](folder-structure.md) (what each folder is),
[AGENTS.md](AGENTS.md) (the rules the agent works under),
[MOTIVATION.md](MOTIVATION.md) (why it is shaped this way). Where this file and one of those
disagree, they are right.

---

## 1 — What this is, in one minute

A **starting point for developing one machine-learning model with an agentic AI system, in a
way you can defend afterwards.** You anchor it to an evaluation harness, a set of modelling
resources and a dataset; you write a plan; the agent executes it one batch at a time inside
a structure where every number is traceable and the shortcuts are detectable.

Two things are produced at once, and neither is subordinate to the other:

1. **A model with a defensible score** — evidence on whether it improves on the named
   baselines and reference, by how much, and how reliably.
2. **The complete record of how that conclusion came about**, alternatives included.

It is deliberately narrow: one project, one model, one article. Not a sandbox, not a
notebook collection, not a knowledge base.

---

## 2 — The two principles behind everything here

Every rule in this repository comes from one of two ideas. Knowing which one a rule serves
is usually enough to know why it will not bend.

### Reproducibility — can someone re-run what you did and get your numbers?

Reproducibility has always been **less a knowledge problem than an effort problem**. What to
record has been understood for decades; recording it *while the work is underway* costs care
and time, which is why guidance in this area has traditionally paired each requirement with a
modest minimum — do at least this much. An agentic system changes that economics: the
tedious, meticulous recording is now nearly free, so the minimums can rise. That is what the
[ten rules](AGENTS.md) are — the classical reproducibility requirements, raised to what is
now affordable.

But an agent also brings **three new ways to lose reproducibility**, each with a structural
answer here:

| New failure mode | The answer in this repository |
|---|---|
| The agent computes in its own context — reads a number off printed output and carries it to the next step. The chain reads as complete in the transcript and is **broken on disk**. Worse than a human's undocumented step, because it is fluent | Every reported number must come from a file that was executed. `/validate invariants` checks for values that crossed between steps by hand |
| **Researcher degrees of freedom without the old limit** — an agent can traverse a large analytic space fast, which is exactly where a proxy target and the real objective come apart | The sealed holdout (§4.2), and every judgment call recorded as an alternative rather than made silently |
| **Instructions are not guarantees** — a standing rule can be honoured for twenty steps and dropped at the twenty-first, with nothing looking wrong | `/validate` — deterministic code, which has no attention budget |

### Veridical data science — would the conclusion survive doing the analysis differently?

Reproducibility records what was done. It says nothing about whether the conclusion holds up
if the analysis had been conducted **differently but equally reasonably** — and *instability
under reasonable alternative choices*, not sampling noise, is the dominant way computational
conclusions go wrong.

The framework is **Yu & Kumbier's veridical data science** and its three principles —
**predictability, computability, stability (PCS)** — applied to model development. Stability
is the one that shapes this repository most:

- The analysis is a **tree of questions, not a pipeline of steps**, so the alternative you
  tried and rejected has an obvious place to live: as a sibling node, still runnable.
- **Every judgment call is either an alternatives node or a logged decision — never silent.**
  A filtering threshold, a metric, a model family, a training window, a cleaning rule.
- The **stability node is an ordinary node inside `analysis/`**, not an appendix. It runs the
  alternatives the main path skipped and reports the **distribution** of conclusions across
  them, rather than the best one.

This is why publishing the negative space costs nothing at the end here: the assembly work
that is the practical reason nobody publishes it has already happened, batch by batch.

---

## 3 — How you work with this repository

**You do not normally run any of the commands in this file.** You open a session, tell the
agent what you want in ordinary words, and it carries out the steps — because
[CLAUDE.md](CLAUDE.md) sends it to [AGENTS.md](AGENTS.md), which is the single source of
truth for how work is done here, and the skills in [`.claude/commands/`](.claude/commands)
encode the mechanics.

So each step below is given as:

> **Say:** what you tell the agent
>
> **It does:** what happens behind the scenes — with the actual commands, so you can run
> them yourself if you want to, and so you can check that what happened is what should have.

Your real work is the four things the agent cannot do for you: **deciding the anchors,
writing the plan, settling the questions each batch raises, and saying what may be
published.**

### The shape of it

| Where | What it is | Who writes it |
|---|---|---|
| [`Human-input/Plans for AI generation/`](Human-input/Plans%20for%20AI%20generation) | The plans the agent executes, one batch per `/do` | **You** |
| [`analysis/`](analysis) | The claim tree — the project itself. [`analysis/run.sh`](analysis/run.sh) reproduces everything | The agent, via `/node` |
| [`AI-generated/`](AI-generated) | Batch reports, the drill-down report, validation findings | The agent — **never hand-edit** |
| [`Human-AI-collaboration/`](Human-AI-collaboration) | [`claims/claims.md`](Human-AI-collaboration/claims/claims.md), then [`manuscript/`](Human-AI-collaboration/manuscript) written from it | Both |
| [`AI-internal/`](AI-internal) | The machinery and the task log | The agent |
| [`Archive/`](Archive) | Imported data and models — read-only, checksummed, never edited | The agent |

---

## 4 — Getting started

### 4.1 Set up your copy

> **Say:** *"Set this copy up per `setup-guide.md` — it's a new project, not a fork."*
>
> **It does:** four things, in order. Full detail in [setup-guide.md](setup-guide.md) §1–4.
>
> **1. Gives your copy its own git history.** Your project must not be a fork of the
> template; you want a history that starts at your project.
>
> ```bash
> git clone https://github.com/sandvelab/agentic-model-development-start.git my-project
> cd my-project && git remote remove origin
> ```
>
> or, copying a local tree — **the trailing dot matters**, or `.claude/` is left behind:
>
> ```bash
> cp -r /path/to/agentic-model-development-start/. /path/to/my-project/
> cd /path/to/my-project && rm -rf .git && git init
> ```
>
> **2. Substitutes the placeholders** in [`.claude/settings.json`](.claude/settings.json):
> `<PARENT_DIR>` and `<HOME>` become real paths. They exist to stop a parent directory's
> `CLAUDE.md` leaking in — that would **silently change the method**, which is the one thing
> that must never happen quietly.
>
> **3. Builds the machinery environment:**
>
> ```bash
> python3 -m venv .venv
> .venv/bin/pip install --upgrade pip
> ```
>
> **4. Checks the empty tree passes:**
>
> ```bash
> .venv/bin/python AI-internal/useful-scripts/check_invariants.py
> .venv/bin/python AI-internal/useful-scripts/node.py tree
> ```
>
> Everything should pass except `git` (until you commit). **Any other failure gets fixed
> before analysis starts** — a checker you have learned to ignore is worse than no checker.

Two things worth knowing even though you will not type them:

**There are two Python interpreters, and which one a script gets depends on where it lives,
not on what it imports** — `.venv/bin/python` runs the repository's own machinery
([`AI-internal/useful-scripts/`](AI-internal/useful-scripts)), and
`environment/env/bin/python` runs anything under [`analysis/`](analysis), because a node's
scripts are part of the result and the result is pinned. Both are invoked directly, never
via `source … /activate`, which turns a pre-approved command into a permission prompt every
time.

**The repository stays private until release.** For a remote, the agent will ask you for the
owner and repository name rather than inferring either, and `/release` runs the secrets and
data-permission scan that must precede anything becoming public.

### 4.2 Fix the three anchors

While [readme-at-start.md](readme-at-start.md) still contains `<placeholders>`, the project
is undefined and **the agent will do no analysis** — [AGENTS.md](AGENTS.md) §0 holds it to
set-up and planning only.

> **Say:** *"Let's fix the anchors. Here is the platform / data / model library I have in
> mind — check what's actually available and propose options."*
>
> **It does:** retrieves and reads candidates (never recalls them), proposes, and — once you
> decide — pins each by version, archives it under [`Archive/`](Archive) with a
> `provenance.md` and a checksum manifest, and records it in
> [readme-at-start.md](readme-at-start.md) and the plan's §4.

**You decide; the agent proposes.** Three anchors:

| Anchor | What gets pinned |
|---|---|
| **Evaluation platform or harness** | What scores a model: platform + version, the metric, the backtest/split scheme, the required baselines, any reference model. If you score with your own code instead, it must be verified against a known-correct reference before it is trusted |
| **Modelling resources** | The model library, reference implementation or published method you develop from — by commit or version |
| **Data** | Source, exact version fetched, licence, and the development/holdout split |

#### The sealed holdout — decided now, because it cannot be decided later

This is the point in the set-up where you buy the credibility of the final number, so it is
worth being explicit about why.

**The holdout is split off and sealed before any development begins, and opened exactly
once**, at the final validation, against a perturbation manifest **frozen beforehand**. It is
not characterised beyond row counts and completeness while sealed. Nothing is added, dropped,
re-tuned or re-run after a number from it has been seen.

The reason is the second failure mode in §2: an agent can try a great many things quickly,
and every look at held-out data during development converts it, a little, into data you
tuned against. A holdout that is peeked at is not a holdout — it is a slow leak that nothing
in the record would show. Sealing it up front and freezing the manifest before it opens is
what makes the last number mean what it says. §9 is the mechanics of the opening itself.

### 4.3 Write the plan, with the agent, while you are in the room

> **Say:** *"Let's write the plan from the template."*
>
> **It does:** works through
> [plan-template.md](Human-input/Plans%20for%20AI%20generation/plan-template.md) with you —
> the aim, what "better" means (§2), the non-negotiables (§3), the decisions already made
> (§4, where the anchors land), and the batch ledger (§6) — saving it as
> `YY-MM-DD_camelCaseName.md`, then archives it as delivered to `Archive/plan-as-delivered/`
> so later drift is measurable.

**The test of a finished plan:** a session with none of your planning conversation in context
can run it end to end without asking you anything. Planning is when you are present to
answer; execution may be days later, in a fresh session, and should not stall on something
one sentence would have settled.

### 4.4 Fill in the project description and the root claim

> **Say:** *"Fill in `readme-at-start.md` from the plan, and draft the root claim."*
>
> **It does:** completes [readme-at-start.md](readme-at-start.md) and drafts
> [analysis/claim.md](analysis/claim.md) — the one question the project answers, written as
> an *aim* to be explored, never as an assertion.

Fix three settings **explicitly** here, because they otherwise get decided implicitly halfway
through by whoever is impatient: the **project seed**, the **tracking level**
(full / standard / light) and the **compute budget for stability work**. And give the root
claim more than one draft — everything in the tree hangs off it.

---

## 5 — Running the work: the batch loop

This is the whole day-to-day rhythm.

> **Say:** *`/do <plan name>`* — or just *"run the next batch of the plan"*.
>
> **It does:** runs **one batch and stops**. Within it: commits before and after every run,
> writes a provenance record for every result, stores intermediates, seeds every stochastic
> script from the project seed, writes plot data beside every figure, leaves a report under
> `AI-generated/batch-reports/`, and wiki-links that report back to the plan.

Then:

1. **Read the batch report.**
2. **Settle whatever the batch left open** — the agent raises decisions rather than inventing
   them. What you settle lands in the plan's **§4b**, append-only, with its basis and its
   agency.
3. **Run the next batch.**

The first batch (Phase A) orients and sets up only — verifies the archived anchors'
checksums, stands up the environment, writes the root claim, raises open questions. **No
modelling.**

**Work that arrives outside the plan still gets a ledger row** with an aim and a status.
Nothing happens here that the ledger does not name — a change with no row is a change with no
record of why it was made.

### The three habits this loop asks of you

**1. Never accept a number that did not come from a file.** If you cannot follow a figure in
the text back to a claim, to a result file, to the command that produced it, the chain is
broken — however complete the conversation looked. This is the failure mode of §2, and it is
the one thing most worth spot-checking.

**2. Hand-edit outputs only through the `_edited` convention.** Hand editing is not
forbidden here — it is made *safe*, because telling a researcher never to hand-edit is advice
that loses to reality. Three rounds of failing to convey in words a change that would take
four seconds by hand is a real situation.

So: the agent never overwrites its own output. When you want to change something it
produced, **copy the file and edit the copy, keeping the name with `_edited` before the
extension** — `summary.tsv` → `summary_edited.tsv`. The agent then detects the pair, treats
the edited file as **authoritative for everything downstream**, and records the diff as a
tracked input step with you named as its author. The result is a manual step that is visible
and re-enactable, which is better than a classical analysis could offer.

> `/manual-edit` registers any new `_edited` pair; the agent also scans for them without
> being asked.

**3. Let failures stay in the record.** A model that does not fit, a specification that does
not converge, an ablation showing no benefit — all stay, with what happened. An honest "it
does not reliably help" is a conclusion, not a failure.

---

## 6 — How the analysis is organised

The analysis is a **tree of claims**, not a pipeline of steps — the single most consequential
design decision in the repository, and the reason the alternatives can be published at all.
A claim is an *aim*, a question in one or two sentences, never an assertion. What a node
yields is recorded separately, as answers.

Each node directory holds `claim.md`, `run.sh` (the main script — only calls to children and
to this node's own scripts), `scripts/`, `results/`, `provenance/`, and `env/` only where it
overrides the pinned environment.

**Children come in exactly two kinds, and the kind belongs to the whole set of children:**

- **Alternatives** (`a_name`, `b_name` — lettered, because they are unordered): competing
  ways to answer the same parent claim. Exactly one is the main path, and the parent's
  `run.sh` calls **only** that one. The rest stay in the tree, complete and runnable — and
  they are what the stability node later executes.
- **Sub-analyses** (`01_name`, `02_name` — numbered, because the order is part of the
  approach): supporting parts of one approach. The parent's `run.sh` calls **every** child.

Two invariants worth knowing as the human reviewing this:

- [`analysis/run.sh`](analysis/run.sh) reproduces the **entire** reported analysis, following
  the main path at every fork. This property is never broken.
- Nodes are **never created by hand**. `/node new`, `/node promote`, `/node rebuild` write
  the scaffold and keep each parent's `run.sh` consistent with the semantics.

> **Say:** *"Show me the tree"* → `.venv/bin/python AI-internal/useful-scripts/node.py tree`

---

## 7 — Which skill to use, and when

Seventeen skills, linked to their definitions. You rarely need to invoke the continuous ones
— the agent is held to them whether or not you ask — but invoking one is how you force the
check now. Ten correspond one-to-one with the ten rules, so **the thing you invoke and the
thing the agent is obliged to do have the same name**.

**The ones you will actually type:**

| Skill | Use it when |
|---|---|
| [`/do <plan>`](.claude/commands/do.md) | Run the next batch of a plan. The main loop |
| [`/validate invariants`](.claude/commands/validate.md) | Before trusting anything. Deterministic, no attention budget |
| [`/hierarchical-report --open`](.claude/commands/hierarchical-report.md) | You want to *look* at what the analysis produced |
| [`/claims list`](.claude/commands/claims.md) · `/claims audit` | See what the project can currently support in writing |

**Continuous obligations** (running without being asked; invoke to force or audit them):

| Skill | Rule |
|---|---|
| [`/track-result`](.claude/commands/track-result.md) | 1 — every result bound to script, inputs, environment, seed, commit, node |
| [`/manual-edit`](.claude/commands/manual-edit.md) | 2 — registers your hand edits via the `_edited` convention (§5) |
| [`/commit-run`](.claude/commands/commit-run.md) | 4 — commit before and after every run, hash into the provenance record |
| [`/store-intermediates`](.claude/commands/store-intermediates.md) | 5 — intermediates at every step, standard formats, never pickles |
| [`/seed`](.claude/commands/seed.md) | 6 — one project seed derived downward; verified by running twice and diffing |
| [`/plot`](.claude/commands/plot.md) | 7 — every figure ships its plotted values and its plotting script beside it |

**At identifiable moments:**

| Skill | When |
|---|---|
| [`/pin-environment`](.claude/commands/pin-environment.md) | Once the first model's real library needs are known (usually batch 1–2), from [environment/environment.yml](environment/environment.yml). Then `/pin-environment verify` for a clean rebuild |
| [`/node`](.claude/commands/node.md) | Any change to the tree's structure |
| [`/perturb`](.claude/commands/perturb.md) `plan` → `run` → `report` | Phase D — stability across the judgment calls |
| [`/annotate-criticality`](.claude/commands/annotate-criticality.md) | Before pruning storage, so pruning is targeted rather than panicked |
| [`/hierarchical-report`](.claude/commands/hierarchical-report.md) | After any structural change, and before release |
| [`/claims`](.claude/commands/claims.md) `add` · `check-text` | Writing: results → claims → manuscript, never results → manuscript |
| [`/validate`](.claude/commands/validate.md) `cleanroom` · `outsider` | Before release; on a schedule in a long project; after any change to the instructions |
| [`/repro-report`](.claude/commands/repro-report.md) | The closing report, once there is a final text |
| [`/release`](.claude/commands/release.md) `check` → `/release` | Publication. Never pushes without asking |
| [`/log-tasks`](.claude/commands/log-tasks.md) | Auto-invoked at the end of substantial work; type it to force an entry |

---

## 8 — Where to find the article, and the results

### The article is in `Human-AI-collaboration/manuscript/`

**This is where the one main write-up lives** — [that folder](Human-AI-collaboration/manuscript),
as `YY-MM-DD_camelCaseName.md`, with iterations accumulating as `_v2`, `_v3` and earlier ones
never overwritten. Beside each draft:

- **`provenance.md`** — what generated it, from which plan, on what date;
- **a provenance sidecar** keyed by paragraph or sentence, mapping each statement to the
  claim it rests on. A sidecar rather than inline comments, so it survives format conversion
  and can be published as supporting material.

The manuscript is written **only** from
[`claims/claims.md`](Human-AI-collaboration/claims/claims.md), never directly from results.
Before submission, `/claims check-text` is run over the draft; the sentences it flags are
either unsupported or point at a claim nobody recorded. Both are worth knowing, and the
exercise is meant to be slightly uncomfortable.

The other document a reader receives is the **reproducibility report**, generated by
`/repro-report` into `AI-generated/reproducibility-report/` at the end of the project.

### The results are beside the analysis that made them

There is no central results folder. Four ways in, from most specific to most readable:

1. **The node itself** — `analysis/<path>/results/` for the files,
   `analysis/<path>/provenance/` for one record per result (script, invocation, inputs,
   environment, seeds, commit, node), and `analysis/<path>/claim.md` for what it yielded.
2. **The drill-down report** — `/hierarchical-report --open` builds static HTML in
   `AI-generated/hierarchical-report/` where each node's claim, answers, results, scripts,
   provenance and `run.sh` are one click from its parent, all the way down to raw values.
   Alternatives are marked main-path or not-taken. **This is the one to open when you do not
   yet know what you are looking for** — scanning a structure visually for the thing that
   looks wrong is far faster than describing what to look for, which is what asking would
   require.
3. **The claim collection** — [`Human-AI-collaboration/claims/claims.md`](Human-AI-collaboration/claims/claims.md).
   One block per claim: the statement, `grounds:` (the result file), `node:`, `scope:`,
   `alternatives:` and `by:` (the agency). This is the searchable record of what the analysis
   established **independent of what reached the paper** — including the findings that did
   not.
4. **The batch reports** — `AI-generated/batch-reports/`, one per `/do`: the narrative of
   what a batch did and what it left open.

**Never hand-edit anything under [`AI-generated/`](AI-generated).** It is rebuilt by a
recorded recipe; an edit is lost on the next run and is wrong in the meantime. If a derived
document is wrong, its source is wrong. (The `_edited` convention of §5 is for the agent's
*results*, not for generated documents.)

---

## 9 — Logging: what is recorded where

Six distinct records, answering different questions. This table is the fastest way to the
right one.

| You want to know… | Look at |
|---|---|
| What work has been done, in what order | [`AI-internal/ai_task_history.md`](AI-internal/ai_task_history.md) — one line per task (`T1`, `T2`, …) |
| The detail of one of those tasks | [`AI-internal/ai_task_details.md`](AI-internal/ai_task_details.md) — outputs, design decisions, files affected, follow-ups |
| What a given batch did, and what it left open | `AI-generated/batch-reports/YY-MM-DD_bNN_name.md` |
| How a specific result file was produced | The `provenance/` record next to it in its node |
| Why a decision was made, and by whom | The plan's **§4b**, append-only, each entry with its basis and agency |
| What state the code was in for a result | Git — commits before and after every run, hashed into the provenance record |
| What the checks found | `AI-generated/validation/`, `AI-generated/determinism-checks/` |

Two things to know about the logs:

- **The task log is part of the published record**, not a private working note. Entries are
  written so a reader who was not present can follow them, and are honest about what did not
  work.
- **Agency is recorded on every decision**: `human-set`, `agent-on-human-assessment` or
  `agent-autonomous`; and for information gathering, `agent-retrieved` (the agent found it)
  or `human-pointed` (you pointed at it). Neither party's contribution is flattered.

---

## 10 — What you may change, and the trade-offs you own

| | |
|---|---|
| **Freely** | [readme-at-start.md](readme-at-start.md), [analysis/claim.md](analysis/claim.md), the environment, the plans, anything in [`Human-input/`](Human-input) |
| **Deliberately** | [AGENTS.md](AGENTS.md) and [`.claude/commands/`](.claude/commands) — these *are* the method. Two runs under different instructions are two different methods. A change here is a methodological change: commit it on its own, with a message saying what changed about the method, and run `/validate outsider` afterwards |
| **Never weaken** | [`check_invariants.py`](AI-internal/useful-scripts/check_invariants.py). When a check fails, fix the cause. Adjusting a check so it passes converts the repository's one honest signal into decoration |

**Decide the trade-offs explicitly rather than letting them drift.** Because each request to
the agent is cheap, thoroughness expands without anyone deciding it should:

- **Tracking level** is stated in [readme-at-start.md](readme-at-start.md); the agent works
  to it and raises a change with you rather than drifting.
- **Storage** — nothing is deleted up front. `/annotate-criticality` marks what each artifact
  is worth (main or side result, regenerable or not, roughly what regeneration costs) so that
  pruning later is targeted.
- **Compute for stability work** — perturbations are costed, ranked by expected
  informativeness, and cut at the stated budget. When one is not run, *that it was not run
  and why* is recorded, so **an absence is a visible decision instead of a silence**.

---

## 11 — Finishing a project

The last phases, in order.

**1. Stability (Phase D).** `/perturb plan` enumerates the judgment calls made so far and
costs them; you cut at the budget; `/perturb run` executes the set; `/perturb report` gives
the **distribution of conclusions across reasonable alternatives**, not the best one. This is
the veridical question of §2 being answered — and note that the main path still reproduces the
reported result even if the stability node is cut under budget.

**Freeze the holdout manifest before the holdout opens.**

**2. Final validation (Phase E) — the single opening of the holdout.** This is the moment
§4.2 was set up for. The holdout is opened **once**; **exactly** the frozen manifest is run
against it, nothing more; the held-out distribution is reported beside the development one.
Nothing is added, dropped, re-tuned or re-run afterwards. If a second opening ever happens,
it is recorded as such.

**3. Claims and report (Phase F).** Build the claim collection from the tree; regenerate the
hierarchical report; write the manuscript from the claims only.

**4. Validate.** `/validate cleanroom` — build the environment from nothing, run
`analysis/run.sh`, compare against the archived results; it catches the whole class of
failures where an analysis silently depends on something in the working directory.
`/validate outsider` — start a fresh agent with no context and ask it to *follow* the
instructions rather than judge them; **what it misunderstands is what an outsider would
misunderstand**. Documentation is always written by someone for whom everything is already
obvious, and this is the closest thing here to an objective check on that. Fix what they
find.

**5. Release.** `/repro-report`, then `/release check` for the secrets and data-permission
scan, then `/release`, which never pushes without asking. The release is the **whole tree**,
alternatives included, plus the instructions, claims and provenance.

### What has to still be true at the end

If these stop holding, the repository has quietly become an ordinary folder of scripts
([MOTIVATION.md](MOTIVATION.md)):

1. `analysis/run.sh` reproduces the reported analysis from a clean environment.
2. Every reported result traces to a file that was executed.
3. Every sentence in the manuscript traces to a claim, to a result, to a command.
4. The alternatives not taken are still in the tree, runnable.
5. `/validate invariants` passes — **because it was satisfied, not because it was weakened**.
6. `readme-at-start.md` describes the project as it actually is.
