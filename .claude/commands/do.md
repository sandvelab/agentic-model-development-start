# Do

Execute a plan from `Human-input/Plans for AI generation/`.

**Usage:** `/do <plan name or path>` · `/do <plan> iteration N`

---

## Steps

1. **Read the plan in full**, plus any resource it references. Identify which iteration to
   run: iteration 1 if there are no prior outputs, otherwise the next one, inferred from the
   wiki links already under *Generated outputs*.
2. **Carry it out.** Follow `AGENTS.md` — in particular §7 on writing, and §1 on results
   coming from files that were executed.
3. **Save the output** to the folder the plan names, or `Human-AI-collaboration/manuscript/`
   for manuscript work, as `YY-MM-DD_camelCaseName.md`. Iterations beyond the first take a
   `_v2`, `_v3` suffix. **Never overwrite a previous iteration.**
4. **Wiki-link both ways.** `Generated from [[<plan>]] — iteration N` near the top of the
   output; `- [[<output>]]` under the plan's iteration heading. The plan accumulates a link
   per iteration.
5. **Back up the plan** to `/tmp/claude_backups/` before editing it.
6. **Open the output** in Obsidian and report what was produced.

## Never narrate the process

The reader never saw our iterations. No "corrected from", "unlike the earlier version", "as
we discussed". Write the document as if the final version had always been the plan. What
changed belongs in the plan file or the chat reply — never in the output.

## Marking iterations

From iteration 2, bold the passages changed in *this* iteration and un-bold the previous
iteration's marks, so exactly one iteration's changes are marked at a time. Bold the
substance of what changed, not whole sections wholesale — if a section was rewritten
entirely, say so in the chat instead, because marking two thousand words carries no
information.
