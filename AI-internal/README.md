# AI-internal

The machinery: the scripts the skills call, the reference material the thin skills defer to,
and the log of what has been done.

| Path | Holds |
|---|---|
| `useful-scripts/` | The repository's own machinery — the scripts the skills call, and the checks on them. **What is in it is listed in its own `README.md`**, with one row per script; a second list here would go stale the first time a batch adds one |
| `skill-references/` | The exact commands, formats and edge cases the skills defer to |
| `ai_task_history.md` | One line per completed task, `T1`, `T2`, … |
| `ai_task_details.md` | The expanded entry for each |

A project may add `reconnaissance/`, `data-acquisition/` or similar folders here as it needs
them — scripts that establish facts about external systems, or bring external data into
`Archive/` — following the pattern the useful-scripts convention sets. None exist yet.

The task log is **part of the published record** of how the work came about, not a private
working note. Write entries a reader who was not present can follow, and keep them honest
about what did not work.
