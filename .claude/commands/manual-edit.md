# Manual edit (Rule 2)

Register a hand edit as a tracked pipeline input, instead of letting it break the chain.

**Usage:** `/manual-edit` — scan for `_edited` pairs and register any that are new ·
`/manual-edit <file>` — register one specific pair

---

## The convention

You never overwrite your own output. When I want to change something you produced, I copy
it and edit the copy, keeping the name with `_edited` before the extension:

```
results/parameters.json          <- yours, untouched
results/parameters_edited.json   <- mine
```

## What you do when you find a pair

1. **Treat the edited file as authoritative for everything downstream.** Every script that
   consumed the original now consumes the edited version. Change the calls; do not copy the
   edited content back over the original.
2. **Generate a diff** and store it in the node's `provenance/` as `<name>_edit.diff`.
3. **Write a provenance record** for the edit as an input step, with `agency: human-set` and
   the human named as its author, summarising in one or two sentences what the edit changed.
4. **Re-run everything downstream** so results reflect the edited input.
5. **Tell me what you found**, especially if the edit changes a conclusion.

## Why this rather than forbidding hand edits

Telling a researcher never to hand-edit loses to reality: natural-language instruction has
an irreducible gap between what was meant and what was got, and three failed rounds of
re-specifying a change that takes four seconds by hand is a real situation. The artifacts
here are small, so keeping both versions costs nothing — and a manual step that is visible,
diffed and re-enactable is *better* than what a classical analysis offered, where such
edits were untracked by their nature.

## What is not covered

The convention assumes small, text-like artifacts. For a large binary intermediate it
degrades into two copies and a useless diff: there, ask me to re-specify instead, or record
the edit as a scripted transformation.
