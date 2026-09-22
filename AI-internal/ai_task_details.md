# Task details

The expanded entry for each task in `ai_task_history.md`: what was produced, the design
decisions, the files affected, and what a future session would need to know. Include
follow-ups, and say plainly where something did not work.

## T1 (2026-09-22) — `How-to-use-vault.md`

A human-facing walkthrough of how the repository is meant to be used, written at the root as
`How-to-use-vault.md`. It covers, in the order the work actually happens: what the repository
is for; the two principles behind it; set-up and git; fixing the three anchors and sealing the
holdout; writing the plan; the `/do` batch loop; the claim tree; all seventeen skills and when
each applies; where the manuscript and the results are found; what each of the six logs
records; what may and may not be changed; and the closing phases through release.

**The design decision worth knowing** is what this file deliberately does *not* do. `README.md`,
`setup-guide.md` and `folder-structure.md` already state much of this content, and `AGENTS.md`
§8 warns that a fact kept in two places goes stale silently. So the file is written as an
*order of operations* that links to those documents as canonical rather than restating them,
and says so in its own opening. That constraint was raised with the human before writing and
again after; it was accepted rather than resolved, so **the overlap is real and this file will
need checking whenever `README.md` or `setup-guide.md` changes.**

**Revised once on feedback**, which changed six things: the set-up and git steps were reframed
from shell commands the human types into a *Say: / It does:* form — what to ask the agent, and
what it runs behind the scenes — because the agent normally performs them; reproducibility and
veridical data science (Yu & Kumbier's predictability, computability, stability) were added as
an explicit §2 stating the motivation for every rule that follows; the `_edited` hand-edit
convention and the sealed holdout were each moved to the point in the workflow where they first
matter, rather than appearing only at the end; the manuscript's location was made a headed
subsection of its own, since it had been hard to find; and paths that already exist were turned
into working relative links (forty-three of them, all verified to resolve, with `%20` for the
spaces in `Human-input/Plans for AI generation/`).

**Files affected**: `How-to-use-vault.md` (new); `folder-structure.md` (one row added to the
root-level listing, which would otherwise have been incomplete).

**Follow-ups**: `/validate invariants` reports only the expected `git` failure while the tree is
dirty. A copy of this repository that is made into a real project should re-read this file for
statements that its own set-up has made untrue.
