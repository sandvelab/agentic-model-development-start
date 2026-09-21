# environment

The **one main environment** for the whole analysis, used generally. A node overrides it
only where it genuinely needs something else, in that node's `env/`, with the reason
recorded in that node's `claim.md`.

| File | What it is |
|---|---|
| `environment.yml` | Declarative — the interpreter version and the libraries the analysis asks for, one line each, with a comment saying what each is for. |
| `install-env.sh` | The build. Creates `env/` **from `lock.txt`**, and re-resolves from `environment.yml` only with `RESOLVE=1`, reporting any difference between what it built and the lockfile. Uses `uv`. |
| `lock.txt` | Resolved — every package with its exact version (`uv pip freeze`). **This is what reproduces.** Written by `RESOLVE=1 bash environment/install-env.sh`, which is what `/pin-environment` runs. Absent in a fresh copy. |
| `Dockerfile` | The image layer, where the analysis matters enough to outlive its dependencies or depends on a platform-specific runner. Absent until a project decides it needs one, and the decision is recorded here either way. |
| `env/` | The built environment. Not tracked; rebuild with `install-env.sh`. |

Invoke directly, as `environment/env/bin/python` — never by activating it — matching the
convention `AGENTS.md` §8 sets for `.venv`. Note this is *not* the `.venv` at the repository
root, which runs the repository's own machinery (`node.py`, `check_invariants.py`). A node's
`run.sh` sets `PYTHON` to this interpreter; `node.py` writes that line.

## Not yet pinned

This copy has no project, so `environment.yml` lists nothing and `lock.txt` does not exist.
Pin in the first batch that knows what the first model needs — a library guessed in advance
is a library pinned for no reason — and record here what was verified: the two-pass check
(`RESOLVE=1`, then a clean rebuild from the resulting `lock.txt`, confirmed to match exactly)
and the date.

## Say what cannot be pinned

A vanished data source, a licence server, a specific GPU, an evaluation platform run as a
hosted service — none of this survives pinning. Where such a dependency exists, state it here
plainly rather than leaving a reproducer to discover it.
