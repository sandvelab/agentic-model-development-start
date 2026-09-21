# Why this repository is built this way

`README.md` says what is here. `readme-at-start.md` says what the particular project is. This file says **why the setup has the shape it has**, what each part is for, and how the whole thing is supposed to behave. Read it once before starting, and again whenever the structure feels like an obstacle — usually that means a decision recorded here is doing work you have not noticed yet.

## The problem this shape answers

Reproducibility has always been less a knowledge problem than an effort problem. What to record has been understood for a long time; recording it while the work is underway costs care and time that a researcher under deadline does not have, which is why guidance in this area has traditionally paired each requirement with a modest minimum — do at least this much.

An agentic AI system changes the economics. The tedious, meticulous recording is now nearly free, so the minimums can rise. But three new things arrive with it:

1. **A new way to lose provenance.** An agent can compute in its own context — read a number off printed output, carry it to the next step — leaving a chain that reads as complete in the transcript and is broken on disk. This is worse than a human's undocumented step, because it is fluent.
2. **Researcher degrees of freedom without the old limit.** The number of analyses a person could run used to bound how much silent tuning was possible. An agent optimising against a target can traverse a large analytic space quickly, which is precisely the setting where a proxy target and the real objective come apart.
3. **Instructions that are not guarantees.** A standing rule sits in a context attended to imperfectly and can be dropped late in a long session, silently.

Each of the three has a structural answer here, and that is what the repository is: not a folder with good intentions in an `AGENTS.md`, but a shape in which the right thing is the easy thing and the wrong thing is detectable.

## The five ideas doing the work

**1 — The analysis is a tree of questions, not a pipeline of steps.**

`analysis/` is a tree in which each node is an *analytical aim* — something to be explored — with the analysis that addresses it hanging off it. Organising by question rather than by computational step is what makes it possible to record **the analysis you decided against**. A step-organised pipeline has nowhere to put the alternative you tried and rejected; a question-organised tree puts it in the obvious place, as a sibling.

Two relationship types, and only two. *Sub-analyses* decompose a question. *Alternatives* answer the same question differently, with one annotated as the main path. The parent of a set of alternatives calls only the main child, so the tree carries every path explored while the root still reproduces exactly the reported analysis. This is the single most consequential design decision in the repository, because it makes publishing the negative space cost nothing at the end — the assembly work that has always been the practical reason nobody publishes it has already happened.

**2 — Verification instead of trust.**

`/validate` exists because the instructions in `AGENTS.md` will be followed most of the time and that is not good enough. Three checks, none of which depends on anyone remembering:

- *Invariants* — ordinary deterministic code asserting the properties the rules imply: every result has a provenance record, every plot has its data beside it, every claim resolves to a result, every stochastic script has a seed, no value crossed between steps except through a file. Runs on every commit and at the end of every analysis.
- *Clean-room* — build the environment from nothing, run `analysis/run.sh`, compare against the archived results. Catches the whole class of failures where an analysis silently depends on something in the working directory.
- *The outsider test* — start a fresh agent with no context and ask it to *follow* the instructions rather than to judge them. Documentation is always written by someone for whom everything is already obvious, and whether it is intelligible to anyone else could previously only be established by finding someone else. Now it is a cheap, repeatable check, and it is the closest thing here to an objective one.

A failing check is fixed at the cause. Adjusting a check so it passes converts the repository's one honest signal into decoration.

**3 — Text is downstream of claims, which are downstream of results.**

Writing happens in two steps. First from results to a **claim collection** in `Human-AI-collaboration/claims/`: short statements, each with an explicit pointer to the stored result that grounds it. Then from the collection to the manuscript.

This buys three things. Provenance runs unbroken from a sentence to a command. The set of everything the analysis supports becomes an object you can search and reason over, independent of what reached the paper. And it is the practical control against generated text drifting away from the analysis it describes — a sentence that cannot name the result it rests on does not get written.

The step also works backwards: a human-written draft can be matched against the collection, and the statements with no support are exactly the ones worth looking at.

**4 — Manual editing is made safe rather than forbidden.**

Telling a researcher never to hand-edit is advice that loses to reality, because natural-language instruction has an irreducible gap between what you meant and what you got, and three rounds of failing to convey a change that would take four seconds by hand is a real situation.

So hand edits are a first-class, tracked pipeline step. The agent never overwrites its own output; a hand edit goes into a copy suffixed `_edited`; the agent detects the pair, treats the edited file as authoritative for everything downstream, and records the diff as an input with the human named as its author. The artifacts involved are small, so keeping both costs nothing — and the result is a manual step that is visible and re-enactable, which is better than what a classical analysis could offer, where such edits were untracked by their nature.

**5 — The veridical question is inside the tree, not beside it.**

Recording what was done says nothing about whether the conclusion survives doing it reasonably differently, and instability under reasonable alternative choices is the dominant way computational conclusions go wrong. An agent sharpens this from both directions: it makes silent judgment calls fast, and — instrumented — it can traverse the space of those calls more completely and neutrally than a person working under publication pressure.

Here the stability node is an ordinary node in `analysis/`, and it runs the alternatives the main path skipped by calling its siblings' main scripts. Two consequences follow. The veridical work is part of the analysis rather than an exercise appended to it. And the robustness/compute trade-off becomes concrete: cut the stability node under budget and the main path still reproduces the reported result, with the unexecuted alternatives still on record — an absence that is a visible decision instead of a silence.

## What is in the repository, and why each piece is there

| Piece | Why |
|---|---|
| `analysis/` | The tree. It is the project; everything else is in service of it. |
| `environment/` | One main environment for the whole analysis, so a reproducer builds one thing. Node-level overrides exist but each is an exception that has to justify itself. |
| `Human-AI-collaboration/claims/` | The bridge between results and text (idea 3). |
| `Human-AI-collaboration/manuscript/` | The article. Downstream of claims, never upstream. |
| `Archive/` | Imported source material, never edited, marked `(IS_SHADOW)`. Kept separate so that "what came from outside" is answerable at a glance. |
| `AI-generated/` | Derived documents — the hierarchical report, the reproducibility report. Regenerable by a recorded recipe, so deletable without loss. |
| `AI-internal/` | The machinery: scripts, skill references, the task log. |
| `Human-input/Plans for AI generation/` | Plans executed by `/do`. Planning happens while the human is present; execution can happen later without stalling on a question that took one sentence to answer. |
| `AGENTS.md` | The standing instructions — the single source of truth. Named for the convention rather than for one vendor, because they govern any agentic system working here. Versioned as part of the method: two runs under different instructions are two different methods. |
| `CLAUDE.md` | A pointer to `AGENTS.md`, holding no instructions of its own. It exists because Claude Code loads a file of that name automatically. |
| `.claude/commands/` | The skills. |

## Why the skills are shaped as they are

There are seventeen, which is more than a general-purpose repository should have. The reason is that here **the command list is the method**: ten of them correspond one-to-one with the ten rules, so that the thing you invoke and the thing you are obliged to do have the same name. Five more cover the machinery the rules assume — the tree, verification, stability, the storage trade-off, and the closing report. Two, `/do` and `/log-tasks`, are ordinary working conveniences.

Each skill file is deliberately thin — usage, dispatch, and what to do — because it is loaded on every invocation. The exact commands, formats and edge cases live in `AI-internal/skill-references/`, loaded only for the subcommand actually running. A skill that needs its reference says so explicitly, because a reference that is merely available gets skipped in favour of a half-remembered version of last time's command.

The rules that apply *continuously* — provenance, no manual edits, commits, intermediates, seeds, plot data — are also standing instructions in `AGENTS.md`, not only skills. A rule you have to remember to invoke is a rule that will not be followed at step twenty-one.

## What is deliberately absent

- **No insight-accumulation section in `AGENTS.md`.** A personal vault benefits from a file that grows conventions as they are learned. This repository presents one finished project to a public audience, and an instruction file that visibly accreted over the project would be a record of the authors' learning rather than a specification of the method. Lessons go to the human, who decides what belongs in the project's record.
- **No generic indexes, archives or overviews.** There is one project here. It needs a map of its own analysis, which the tree and the hierarchical report already are.
- **No genres other than articles and code.** No emails, notes, decks, or personal material.
- **Nothing identifying.** This is a general starting point, usable by anyone.

## What has to stay true

If these stop holding, the repository has quietly become an ordinary folder of scripts:

1. `analysis/run.sh` reproduces the reported analysis from a clean environment.
2. Every reported result traces to a file that was executed.
3. Every sentence in the manuscript traces to a claim, to a result, to a command.
4. The alternatives not taken are still in the tree, runnable.
5. `/validate invariants` passes, and passes because it was satisfied rather than because it was weakened.
6. `readme-at-start.md` describes the project as it actually is.
