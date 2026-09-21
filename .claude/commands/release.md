# Release (Rule 10)

Assemble everything for public access, after checking it is safe to publish.

**Usage:** `/release check` — the safety scan only · `/release` — scan, assemble, and report
what would be published (**never pushes without asking**)

---

## Run the safety scan first, always

1. **Secrets.** Scan the whole tree — history included — for keys, tokens, passwords and
   credential files. You will commit a key cheerfully if nobody checks.
2. **Data permission.** Confirm explicitly that every included data file may lawfully be
   published. Where it may not, replace it with an accessioned reference and say so.

If either fails, stop and tell me. Do not publish a subset and mention it afterwards.

## What goes in

- data, or accessioned references where redistribution is not permitted;
- all scripts, and `analysis/` **entire — alternatives included**;
- the environment specifications at all three layers;
- the claim collection and the manuscript's provenance sidecar;
- the provenance records;
- **the instruction files and skills** — they determine how the analysis was produced;
- the hierarchical report and the reproducibility report;
- a root script that rebuilds everything.

## Why the alternatives are the point

They are already in the tree with their scripts intact, which removes the practical reason
nobody publishes the paths they did not take: assembling them used to be work. Publishing
them changes what a reader can assess — from *does this analysis run* to *was this a
reasonable analysis among the ones that were tried*. Treat it as the most valuable thing in
the release, not an appendix.

## Before it counts as released

Run `/validate cleanroom` and `/validate outsider`, and regenerate `/hierarchical-report`
and `/repro-report`. Then deposit a **citable, versioned snapshot with a persistent
identifier** — a repository host is where the work lives, not an archive — and reference
that in the paper.
