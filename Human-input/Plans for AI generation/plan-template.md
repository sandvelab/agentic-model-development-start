# <Develop or improve MODEL for TARGET on DATA>, veridically

<The plan this repository exists to execute. It is written to be run by an agent that has
none of the conversation behind it in context: everything needed to start is either here or
in `Archive/`. Replace every `<…>`; delete this paragraph.>

---

## 1. The aim

**<One sentence: develop, as autonomously as the setup allows, MODEL for TARGET, and
establish whether it earns its place.>** What is fixed and what is open:

1. <The part of the architecture or approach that is fixed by this plan.>
2. <The parts that are judgment calls — model family, specification, inputs, preprocessing,
   training window, combination rule — each to be explored as an alternatives node, not
   decided here.>

Two things are produced at once, and neither is subordinate to the other (`AGENTS.md` §1):

1. **A model, with a defensible score** — evidence on whether it improves on <the baselines
   and reference>, by how much, and how reliably across reasonable alternative ways of
   building it.
2. **The complete veridical record of how it came about.**

**The central comparison this project is built to answer**: <what is compared against what,
on the same data, same splits, same everything else — e.g. the new model vs. the reference
model; the full model vs. the ablated one>. A project that reports only an absolute score
without this comparison has not answered its own question.

## 2. What "earns its place" means

- **Primary**: <metric> of <the model> vs. <the comparator>, across <units and splits>, on
  the development backtest. <Direction; whether a margin threshold applies; what the real
  content of the answer is — the margin, its spread, and its stability.>
- **Secondary**: <the required baselines, scored through the identical pipeline; calibration
  or other properties a model must not lose while winning on the primary metric>.

**The aim is to conclude, and the conclusion may be an uncertain call.** An honest "it does
not reliably help" is a conclusion, not a failure. If the model does not help on the main
configuration, that is reported plainly, together with which alternatives were tried and what
they cost.

## 3. Non-negotiables

These override anything else in this plan.

- **The holdout stays sealed until the final validation.** Development, tuning and selection
  happen only on <the development slice>; the holdout is opened once, at the end, in a single
  batch, and the perturbation set evaluated on it is frozen beforehand. The holdout is not
  characterised beyond row counts and completeness before it opens; a second opening, if it
  happens, is recorded; the frozen manifest binds and nothing else does.
- **No number reaches a claim except through a file** (`AGENTS.md` §1). Whatever computes
  the metric writes its output to a file, and every reported figure is read from that file by
  a script, not carried by hand from terminal output.
- **Every judgment call is a node or a logged decision, never silent.** <List the calls this
  project foresees.> Each is either an alternatives node with its rejected siblings intact,
  or an explicitly logged decision with its basis.
- **Agency is recorded on every decision**: `human-set`, `agent-on-human-assessment`, or
  `agent-autonomous`; for information gathering, `agent-retrieved` or `human-pointed`. The
  default is `agent-autonomous`, so the entries that matter are the exceptions.
- **Failures are kept.** A model that does not fit, a specification that does not converge,
  an ablation that shows no benefit: all stay in the record with what happened.
- **If an anchor turns out to be wrong** — a defect in the archived data, a reference model
  that does not run as documented, a platform whose scoring differs from its documentation —
  **stop and report it** rather than silently patching around it.

## 4. Decisions already made

Settled here so that execution does not reopen them. The first block is the project's
anchors (`readme-at-start.md`, *Where the project starts from*).

| | Decision |
|---|---|
| **Evaluation platform or harness** | <Platform and pinned version, how it is invoked, and what of its behaviour has been verified; or: own scoring code, to be verified against <reference implementation> before it is trusted on real data. Agency.> |
| **Metric** | <Primary; secondary. Who computes it and where the file lands.> |
| **Backtest or split scheme** | <Scheme; where it is recorded as a file; whether a batch may deviate with a recorded reason.> |
| **Required baselines** | <The baselines every model is compared against, scored through the same pipeline.> |
| **Reference model** | <External reference pinned by version and how it is run; or "none", and why.> |
| **Modelling resources to start from** | <Library, reference implementation or method; commit or version; where archived; how it may be used (run as-is through the platform, adapted into a node's scripts, used as a design only).> |
| **Data** | <Source repository or API, commit or version, licence, what the fetch script is, where archived with its checksum manifest.> |
| **Target** | <What is predicted, at what resolution.> |
| **Development data** | <The only slice development ever sees.> |
| **Held-out data** | <Sealed until the final validation (§3).> |
| **Project seed** | `<integer>`. Every component seed derives from it by the construction in `AI-internal/skill-references/provenance-record.md`. |
| **Environment** | <One main environment, pinned per Rule 3 once the first model's needs are known; Docker image yes/no and why.> |
| **Tracking level** | <Full / standard / light (`AGENTS.md` §6), and why.> |
| **Compute budget for stability work** | <Set now, or: set in phase D once per-run cost is known.> |
| **Storage budget** | <Not a constraint by default; raised with the human if outputs are unusually large.> |
| **Data governance** | <Public and redistributable; or what may not be published and how the release will handle it.> |
| **Scope of the tree** | The whole analysis is in `analysis/`. Nothing important happens outside it. |
| **Git remote** | <owner/repository, public or private; when it may be pushed.> |

## 4b. Decisions settled during execution

Append-only, oldest first; each entry with its basis and its agency.

### <YYYY-MM-DD> — <what was being settled>

| Decision | Basis | Agency |
|---|---|---|
| <the decision> | <why, and what question it answered> | <human-set / agent-on-human-assessment / agent-autonomous; information: agent-retrieved / human-pointed> |

## 5. How this plan is used

This plan is edited as it runs: §6 is the live batch ledger, and sketched phases become
concrete batches as they are reached. The plan as it stands before the first batch is
archived to `Archive/plan-as-delivered/` so later drift is measurable. A request that
arrives outside the plan still gets a ledger row and a §4b entry (`AGENTS.md` §8).

## 6. Batch ledger

One row per `/do` invocation. Status: `open`, `done`, or `blocked` with why. A batch's number
is an identifier assigned when it starts, not a position fixed in advance; rows are inserted
and later rows renumbered as the work demands, but the phase structure is meant to hold.

| Batch | Phase | Aim | Status |
|---|---|---|---|
| 1 | A — Orient & set up | Read `readme-at-start.md`, `AGENTS.md`, `MOTIVATION.md`; verify the archived anchors (checksums, pinned versions) and re-read their `provenance.md`; stand up `.venv`; write the root `analysis/claim.md`; raise any open questions this plan leaves the human. No modelling. | open |
| 2 | B — Data, metric & first model | Partition development from holdout and seal the holdout; characterise the development data; verify the metric implementation (or the platform's scoring) against a known-correct reference; get one model — the reference, or the simplest defensible version of the new one — running end to end and producing a file-grounded score. | open |
| 3 | B (cont.) | The required baselines through the same pipeline; the first honest number for how much the backtest can resolve at all. | open |
| 4–N | C — Candidates | The new model and its alternatives, one candidate per batch as alternatives nodes; each scored through the unchanged pipeline with calibration or other secondary properties beside the primary metric; a main-path decision on development evidence, with rejected candidates kept runnable. | open |
| | D — Stability | Enumerate the judgment calls made so far as a perturbation manifest; cost it; freeze the development manifest; run it; report the distribution rather than the single number. Freeze the holdout manifest before the holdout opens. | open |
| | E — Final validation | Open the holdout once; run exactly the frozen manifest; report the held-out distribution beside the development one. | open |
| | F — Claims & report | Build the claim collection from the tree; generate the hierarchical report. | open |
| | F (cont.) | `/validate cleanroom` and `/validate outsider`; fix what they find. | open |
| | F — Release | Write the manuscript section(s) this project supports; run the release scan; push. | open |

## Batch ledger — reports

*(One link per completed batch, added by `/do`. Never overwritten.)*
