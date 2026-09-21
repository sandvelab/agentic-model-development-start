# claims

`claims.md` holds everything the analysis supports: short statements, each bound to the
result grounding it, with its scope, the alternatives that would have supported something
different, and who authored it.

Maintained through `/claims`, which wraps `AI-internal/useful-scripts/claims.py`:

```bash
.venv/bin/python AI-internal/useful-scripts/claims.py audit
.venv/bin/python AI-internal/useful-scripts/claims.py check-text \
    Human-AI-collaboration/manuscript/<draft>.md
```

## What a claim may say

**A claim may state what follows trivially from the figures it cites — a ratio between two of
them, a ranking, a difference — and may not state anything that needed a step nobody ran.**
The line is between arithmetic a reader could do from the cited figures and a computation
that would have been an analysis step: the first is legible and checkable from the claim
itself, the second is a number with no provenance dressed as one that has some, which is what
`AGENTS.md` §1 forbids. A paired difference and its standard error may both be cited and the
ratio between them stated; a new aggregate may not.

Two things this file is for beyond writing the paper. It is the searchable record of what
the analysis established, independent of what reached the manuscript — including the
findings that did not. And it is the practical control against generated text drifting away
from the analysis: a sentence that cannot name the result it rests on does not get written.
