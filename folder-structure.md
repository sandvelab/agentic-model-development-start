# Folder structure

What each directory is for, and the one rule that governs it. Create every folder with a
`README.md` at the same time.

```
<repo>/
├── readme-at-start.md      what THIS project is           read first, every session
├── README.md               what this repository is, for humans
├── MOTIVATION.md           why the repository is shaped this way
├── AGENTS.md               the standing instructions       part of the method
├── CLAUDE.md               pointer to AGENTS.md
├── setup-guide.md          how to start a project from this copy
├── folder-structure.md     this file
├── LICENSE                 CC BY 4.0 — the documents, data and provenance records
├── LICENSE-CODE            MIT — the scripts, every run.sh, .claude/ and environment/
├── .claude/
│   ├── settings.json
│   └── commands/           the 17 skills
├── analysis/               THE CLAIM TREE — the project itself
│   ├── claim.md            the top-level analytical aim
│   ├── run.sh              reproduces the entire reported analysis
│   ├── scripts/  results/  provenance/
│   ├── NN_name/            sub-analyses children — numbered, every one of them runs
│   └── a_name/             alternatives children — lettered, only the main path runs
│                           (a project that runs stability sweeps writes each node's
│                            outputs to results/<combination>/, `main` by default)
├── environment/            the one main environment (spec · build · lockfile · image)
├── Archive/                imported material, never edited
│   ├── <dataset>/          data pinned by commit, with sha256sums.txt and provenance.md
│   ├── <model-resource>/   a model library or reference implementation, pinned, (IS_SHADOW)
│   ├── <source-material>/  papers, protocols, platform documentation, (IS_SHADOW)
│   └── plan-as-delivered/  the plan before any of it had been run
├── AI-generated/           derived documents — regenerable, therefore deletable
│   ├── batch-reports/      one per executed batch — the exception: not regenerable
│   ├── validation/         what /validate cleanroom and /validate outsider found
│   ├── determinism-checks/ Rule 6: the models run twice and diffed
│   ├── hierarchical-report/
│   └── reproducibility-report/
├── AI-internal/
│   ├── useful-scripts/     node.py · check_invariants.py · claims.py ·
│   │                       build_hierarchical_report.py, plus what the project adds
│   ├── reconnaissance/     facts about external systems the project does not control
│   ├── data-acquisition/   scripts that bring external data and models into Archive/
│   ├── skill-references/   the detail the thin skills defer to
│   ├── ai_task_history.md
│   └── ai_task_details.md
├── Human-input/
│   └── Plans for AI generation/   plans executed by /do, and plan-template.md
└── Human-AI-collaboration/
    ├── claims/             claims.md — every statement bound to its result
    └── manuscript/         the article, written from the claims
```

Folders shown in `<angle brackets>` or under `AI-generated/` and `AI-internal/` beyond the
first row are what a project typically adds; they do not exist in a fresh copy.

## The rule for each

| Folder | Rule |
|---|---|
| `analysis/` | `run.sh` at the root reproduces everything. Alternatives stay in the tree. Never create nodes by hand — use `/node`. |
| `environment/` | One environment for the whole analysis. A node-level override must justify itself in that node's `claim.md`. |
| `Archive/` | Read-only and write-once. Text documents are marked `(IS_SHADOW)` on line 2; data files cannot be, because inserting a line would edit them and break their checksums, so their folder's `README.md` and `provenance.md` carry the statement instead. Anything needing change is copied out first. |
| `AI-generated/` | Everything here is rebuilt by a recorded recipe. Never hand-edit; if it is wrong, its source is wrong. |
| `AI-internal/` | The machinery. Scripts have a dual API/CLI interface. |
| `Human-input/` | Mine. You execute plans from here; you do not rewrite them except to add output links and to fill in the ledger. |
| `Human-AI-collaboration/claims/` | The only route from results to text. |
| `Human-AI-collaboration/manuscript/` | Downstream of claims, never upstream. |

## Node directories

Sub-analyses are named `NN_shortName`, numbered in the order the parent runs them;
alternatives are named `a_shortName`, `b_shortName`, because they are unordered and only one
runs on the main path. Each holds `claim.md`, `run.sh`, `scripts/`, `results/`,
`provenance/`, and `env/` only where it overrides the main environment.
