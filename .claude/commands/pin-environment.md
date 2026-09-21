# Pin environment (Rule 3)

Pin the exact versions of everything external, and verify that the pin actually rebuilds.

**Usage:** `/pin-environment` — pin (or re-pin) the project main environment ·
`/pin-environment <node>` — pin a node-level override · `/pin-environment verify` — clean rebuild

---

## Three layers, and why each

| Layer | File | What it is for |
|---|---|---|
| Declarative | `environment/environment.yml` | Readable: what was asked for |
| Resolved | `environment/lock.txt` | What was actually installed, with versions and hashes. **This is what reproduces.** |
| Image | `environment/Dockerfile` | What survives when an upstream package repository changes or disappears |

Write the first two always. Write the third where the analysis matters enough to outlive
its dependencies.

## Node overrides

Only where a node genuinely needs something the rest of the project does not — an old tool
version, a GPU library, another language. The specification goes in that node's `env/`, and
**the reason goes in its `claim.md`.** Each override is an environment a reproducer has to
build, so keep them rare and justified. An override applies to its node and, by convention,
its subtree unless a descendant overrides again.

## Verify, don't assert

`/pin-environment verify` runs the check that was always recommended and almost never
performed: from an empty directory and a clean environment, build from the specification,
fetch the inputs, run `analysis/run.sh`, and compare outputs against the archived ones.
**Report differences rather than announcing success.** This is what catches the whole class
of failures where an analysis silently depends on something in the working directory or the
shell environment.

## Reviving unmaintained tools

Where the analysis depends on software no longer maintained, patching the source to build
against a current toolchain is usually tractable now. If you do it, the patched version is
a custom script: version-control it, archive it, and store the patch beside the original.

## Say what cannot be pinned

A vanished data source, a licence server, a specific GPU — none of this survives pinning.
Where such a dependency exists, state it plainly in `environment/README.md` rather than
leaving a reproducer to discover it.
