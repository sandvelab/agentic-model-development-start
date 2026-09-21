# Read this first

The first thing to read in a new session, human or agent. It says what *this particular*
project is. When it stops matching reality it is worse than nothing.

Then read `AGENTS.md` — the standing instructions, and the single source of truth for how
work is done here.

---

> **This copy has not been given a project yet.** Every `<…>` below is a placeholder. Until
> they are filled in — by the human, in dialogue with the agent, before any analysis — the
> only work to do here is the set-up in `setup-guide.md` and the writing of the first plan
> from `Human-input/Plans for AI generation/plan-template.md`. `AGENTS.md` §0 says exactly
> what an agent does in this state. Delete this box when the project is defined.

## The project

**<One or two sentences: develop or improve which model, for which target, on which data,
and establish what about it — typically whether it earns its place against the named
baselines and reference.>** Full aim, success criteria and non-negotiables:
`Human-input/Plans for AI generation/<YY-MM-DD_planName>.md`.

## Where the project starts from

The three anchors every project here is bound to. Each is pinned, archived under `Archive/`
with a `provenance.md`, and named here so that no session has to rediscover it.

| Anchor | This project |
|---|---|
| Evaluation platform or harness | `<platform and version, or "own scoring code, verified against <reference> in node <path>">` |
| Metric | `<primary metric; secondary metrics>` |
| Backtest or split scheme | `<scheme, and where it is recorded as a file>` |
| Required baselines | `<baselines every model is compared against, scored through the same pipeline>` |
| Reference model | `<external reference, pinned by version — or "none", and why>` |
| Modelling resources to start from | `<model library / reference implementation / method, pinned by commit or version, at Archive/<dir>>` |
| Data | `<source, exact version fetched, licence, at Archive/<dir> with sha256sums.txt>` |
| Target | `<what is predicted, at what resolution>` |
| Development data | `<the only slice development ever sees>` |
| Held-out data | `<sealed until the final validation; opened once>` |

## The article

- **Target venue**: `<not yet decided | venue>`.
- **Status**: `<which batches are done, what they established, what is open — kept current>`.
- **Manuscript**: `Human-AI-collaboration/manuscript/` (empty).
- **The plan being executed**: `Human-input/Plans for AI generation/<YY-MM-DD_planName>.md`.
  It carries the batch ledger (§6); `/do` runs the next open batch and stops.

## Settings this project has fixed

| Setting | Value |
|---|---|
| Project random seed | `<integer>`. Every component seed derives from it (`AI-internal/skill-references/provenance-record.md`). |
| Main environment | `<pinned in batch N: interpreter and the libraries the analysis needs>`. Installed from `environment/lock.txt` by `environment/install-env.sh`. Invoked as `environment/env/bin/python`. `<Docker image: yes/no, and why>` |
| Repository machinery interpreter | `.venv`, per `setup-guide.md` §3. |
| Tracking level | `<full | standard | light>` (`AGENTS.md` §6). Raise it with the human rather than drifting. |
| Compute budget for stability work | `<not yet set — set once the per-run cost is known | budget>` |
| Storage budget | `<not a constraint by default | budget>` |
| Data governance | `<public and redistributable | restricted: what may and may not be published>` |
| Git remote | `<owner/repository, public or private>`. Nothing is pushed without the human's instruction; `/release` runs the secrets and data-permission scan before anything becomes public. |

## What must not happen

These override everything else here; the plan's §3 states them in full for this project.

1. **The holdout is sealed before any work begins and opened once**, at the final validation,
   across a perturbation manifest frozen beforehand. Nothing is added, dropped, re-tuned or
   re-run on the holdout after a number from it has been seen.
2. **No number reaches a claim except through a file.** Whatever computes a score writes it
   to a file; every reported figure is read from that file by a script.
3. **Every judgment call is a node or a logged decision, never silent** — model family,
   specification, inputs, preprocessing, training window, the combination rule, the metric.
4. **Agency is recorded on every decision.**
5. **Failures are kept**: a model that does not fit, a specification that does not converge,
   an ablation showing no benefit — all stay in the record.
