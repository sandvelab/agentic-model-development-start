# Perturb

Plan, run and report the stability of conclusions across reasonable analytic choices.

**Usage:** `/perturb plan` — enumerate judgment calls and cost them · `/perturb run` —
execute the planned set · `/perturb report` — the distribution of conclusions

No argument: print this list and run nothing.

---

## Why this is part of the analysis, not an appendix

Reproducibility records what was done. It says nothing about whether the conclusion would
survive a differently-but-equally-reasonably conducted analysis — and instability under
reasonable alternative choices, not sampling noise, is the dominant way computational
conclusions go wrong. A perfectly reproducible pipeline reproduces a fragile conclusion
perfectly.

Here the **stability node** is an ordinary node in `analysis/`, and it runs the alternatives
the main path skipped by calling its siblings' main scripts. So the veridical work lives
inside the tree.

## plan

Enumerate every judgment call: filtering thresholds, cleaning decisions, feature
definitions, metric choice, model family, null model. For each, list the reasonable
alternatives, estimate the compute cost of taking it, and rank by expected informativeness.
Prefer making a judgment call an **alternatives node** so the path not taken survives.

## run

Execute down the ranked list until the stated budget is reached. **Record where the line
fell and what was below it.** An absence must be a visible decision: a stability analysis
that stopped for budget reasons and says so is far more useful than one that silently
explored whatever happened to be quick.

## report

Report the **distribution of conclusions** across the perturbation set — not the best one,
and not a single headline with a robustness footnote. Say which choices the conclusion is
insensitive to and which it is not; the latter is the finding. Each conclusion goes to
`/claims` as its own claim, including the stability claim itself.

## The reason this cuts both ways

You can traverse the judgment-call space more completely and neutrally than a person working
under publication pressure. You can also, optimising freely against a target, tune to the
available data or to a chosen metric faster than anyone could check. Which one happens is
decided by whether this skill is run, not by anything about the technology.
