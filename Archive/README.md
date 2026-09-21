# Archive

Imported material: data, models, papers, platform documentation, protocols — anything that
came from outside this project. **Never edited in place**, marked `(IS_SHADOW)` on line 2
where the file is text, with a `provenance.md` beside it saying where it came from, at which
commit or version, and how to re-obtain it.

Kept separate so that "what came from outside" is answerable at a glance. Anything that
needs modifying is copied out — into a node under `analysis/`, or into
`Human-AI-collaboration/` — first; the original stays untouched, because it may later be
replaced by an updated import.

## Conventions

- **One folder per import**, with a `README.md` (what it is, what is in it) and a
  `provenance.md` (one section per file: source, commit or version, date, the command that
  fetched it, licence or governance). Append to `provenance.md`; never overwrite a section.
- **Data files carry a checksum manifest**, `sha256sums.txt`, written when they were fetched
  and re-verified by the node that reads them. The `(IS_SHADOW)` line marker cannot be
  applied to a data file — inserting a line would edit it and break its checksum — so the
  folder's `README.md` and `provenance.md` carry the statement instead.
- **Pin by commit, not by branch.** A file fetched from another repository's current state
  depends on that repository; the commit is recorded so a later reader can tell whether the
  source has moved.
- **A modelling resource** (a model library, a reference implementation) is archived the
  same way. It is adapted, if at all, by copying into a node's `scripts/`; the archived copy
  stays as fetched.
- **Where an import has a binary original and a markdown conversion**, they go in `orig/`
  and `md/` respectively; `md/` is the one to read.
- **`plan-as-delivered/`** holds the plan as it stood before the first batch ran, so that the
  live plan's drift can be measured against it.

## Currently here

Nothing yet — the project's anchors (`readme-at-start.md`) have not been fetched.
