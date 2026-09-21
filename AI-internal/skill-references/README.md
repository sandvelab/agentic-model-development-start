# skill-references

The skill files in `.claude/commands/` are loaded on **every** invocation, so they stay thin
— usage, dispatch, and what to do. Anything longer lives here and is read only when the
subcommand that needs it actually runs.

A skill that has a reference says so explicitly, in words like *"read this before acting;
don't improvise from memory of a previous run."* Without that instruction the reference gets
skipped in favour of a half-remembered version of last time's command, which is the exact
failure the split exists to prevent.

## Currently here

- `provenance-record.md` — the full field list for a provenance record, with a worked
  example; what to do when a script changes, which is to append a section rather than edit
  the digest above it; and what `/validate invariants` can and cannot verify about a record.
- `checks-to-add.md` — invariant checks a project adds once the structure they check exists:
  the closed combination space of a stability sweep, the frozen holdout manifest, and the
  consistency of a registered ensemble membership. Patterns, with what each caught before.

Add a reference when a skill starts wanting more than about seventy lines.
