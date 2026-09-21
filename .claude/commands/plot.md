# Plot (Rule 7)

Produce a figure with its numbers and its script beside it.

**Usage:** `/plot <description>` — make a figure the compliant way ·
`/plot audit` — find figures missing their data or script

---

## What lands beside every figure

In the node's `results/`, sharing the figure's stem:

- **the values actually plotted**, in a tabular text format;
- **the pre-aggregation values** where the plot summarises — the observations behind a
  histogram, not only the bin heights;
- **the plotting script**, in the node's `scripts/`;
- a provenance record (`/track-result`) tying all of it to the analysis result it visualises.

A handful of kilobytes in the typical case.

## Why this matters more than it used to, not less

The case against it: you write plotting code in seconds, and can often recover values from
a rendered figure to near-pixel accuracy. The case for it is stronger. **Figure iterations
go up sharply** when a variant is one sentence away — several rounds of "try it with the
axes swapped, and with the outliers shown" are normal now — and every round that regenerates
the analysis to re-plot costs tokens, wall-clock and an opportunity for drift.

On reading values back out of an image: useful for someone else's published figure, not a
substitute for your own numbers. The recovery is approximate, it fails silently on
overlapping or clipped elements, and it cannot recover what the figure aggregated away.
