# Log tasks

Record completed work to the project's task log.

**Usage:** `/log-tasks` — log what was just completed · `/log-tasks <description>`

**Auto-invoke without being asked** when a substantial task ends, when I change topic, and
at session end. Do not log minor edits, single-file fixes or quick lookups.

---

## Steps

1. **Check whether this extends an existing entry** before creating a new one — read the
   last few entries of `AI-internal/ai_task_history.md`. A second iteration of the same
   piece of work extends its entry; it does not get a new number.
2. **Append one line** to `AI-internal/ai_task_history.md`:
   `- T<N> (<YYYY-MM-DD>): <what was done — outputs, capabilities, decisions>`
   The date is required.
3. **Append a block** to `AI-internal/ai_task_details.md`: two to five sentences on what was
   produced, the design decisions, the files affected, and anything a future session would
   need. Include follow-ups.
4. **Update what the work changed** — the affected folder's `README.md`, `provenance.md`
   beside any new document, and `readme-at-start.md` if the project's shape moved. Only
   where genuinely changed; not as a formality.

## Why this log is different here

This repository will be published. The task log is part of the record of how the work came
about, not a private working note — so write entries that a reader who was not present can
follow, and keep them honest about what did not work.
