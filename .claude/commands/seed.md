# Seed (Rule 6)

Seed every source of randomness, and prove it by re-running.

**Usage:** `/seed <node>` — seed a node's scripts and verify · `/seed audit` — whole tree

---

## One project seed, derived downward

A single project-level seed, recorded in `readme-at-start.md`, deterministically derived
into per-component seeds. This is more robust than seeding each site independently, because
it cannot drift out of sync and there is one number to report.

## The coverage checklist

These are what get missed:

- the language-level global generator, and *each library's own* generator;
- per-worker seeds under multiprocessing, and the seeding of workers a data loader spawns;
- subprocess invocations that reseed from system entropy;
- hash randomisation, which changes iteration order over sets and dictionaries;
- nondeterministic reduction order on GPUs;
- the environment itself — thread counts changing floating-point summation order.

## Verify, don't assert

Seeding is only credible when checked. **Run the analysis twice, compare outputs bit for
bit, and treat any difference as a defect to locate** rather than a tolerance to accept.
Where exact equality is genuinely unattainable — some GPU kernels, some parallel reductions
— record that fact and the achievable tolerance, so a later reproducer knows what to expect.

## Your own nondeterminism is a different thing

You are stochastic, and your output is not reproducible from a seed: asked the same question
twice you will write two different scripts. Do not try to suppress this by fixing a sampling
temperature — it does not do what it appears to, and it is not what reproducibility requires.

What must be reproducible is the **artifact** — script, environment, seeds, results — not the
process that produced it. The transcript is not a specification; the archived artifacts are.

There is a use for this, though: running the same analytical brief through several
independent sessions and comparing the conclusions perturbs exactly the judgment-call space
`/perturb` is concerned with.
