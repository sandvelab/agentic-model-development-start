# Annotate criticality

Record what each stored artifact is worth, so pruning later is targeted rather than a panic.

**Usage:** `/annotate-criticality <node>` · `/annotate-criticality audit` — whole tree ·
`/annotate-criticality prune --budget <size>` — propose (never perform) a pruning list

---

## The trade-off this serves

More stored intermediates, versions and environments make reproduction easier and more
complete. Occasionally the volume becomes genuinely prohibitive. The old response was to
decide up front what not to keep, which destroys exactly what cannot be recovered.

The better option is to **defer the decision** — keep everything while it is affordable, and
annotate it well enough that pruning later is a targeted operation.

## What to record

Beside each stored artifact, four rough judgments:

| Field | Values |
|---|---|
| `role` | main result · side result · intermediate |
| `regenerable` | yes, at roughly `<cost>` · no |
| `transparency` | how much a critical reader would want it |
| `cost` | approximate compute and wall-clock to regenerate |

They only need to be roughly right. Producing them at scale is cheap for you and impossible
for me, which is the whole reason this works.

## Pruning

`prune` produces a **proposal**, ordered by lowest transparency value per byte, with what
each entry costs to regenerate. It never deletes. Deleting from the record of a project is
mine to authorise, item by item — the asymmetry is deliberate: a stale kept file costs
storage, an unwanted deletion can cost something irreplaceable.

The one exception, as everywhere in this repository: an output fully regenerable by a
recorded recipe, being rebuilt in the same step, is safe to replace without asking.
