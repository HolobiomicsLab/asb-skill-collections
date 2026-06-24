---
name: color-palette-application-greens
description: Use when when rendering a treemap of qc_summary() output showing ion
  counts and percentages by filter status (passed/failed), and you need a perceptually
  uniform, colorblind-friendly palette that clearly distinguishes filter categories
  while using sequential intensity to reinforce the magnitude of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0573
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - ggplot2
  - treemapify
  - RColorBrewer
  - mpactr
  - data.table
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- creating an interactive plot of input features and the filters they failed, if any,
  using `ggplot` and `plotly`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00997-24
  all_source_dois:
  - 10.1128/mra.00997-24
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Apply Greens color palette to treemap visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply the RColorBrewer Greens sequential palette to a treemap visualization of QC filtering results, enabling intuitive perception of ion count magnitudes across filter status categories. This palette choice leverages sequential color progression to emphasize both categorical distinctions and quantitative differences in ion abundances.

## When to use

When rendering a treemap of qc_summary() output showing ion counts and percentages by filter status (passed/failed), and you need a perceptually uniform, colorblind-friendly palette that clearly distinguishes filter categories while using sequential intensity to reinforce the magnitude of ion counts within each status group.

## When NOT to use

- When your audience contains individuals with deuteranopia (green–red colorblindness); consider alternative palettes such as Viridis or Greys in such cases.
- When filter status categories exceed ~7 distinct values; Greens palette works best for 3–5 ordinal categories due to limited sequential range.
- When the treemap background or surrounding plot area is already predominantly green; color contrast may be compromised.

## Inputs

- qc_summary() output as data.table (columns: ion identifiers, filter status category)
- aggregated ion count and percentage summaries by status
- ggplot2 aesthetic mapping (aes) linking status categories to color fill

## Outputs

- ggplot2 treemap object with Greens palette applied
- PNG/PDF rendered treemap file showing ion counts and percentages colored by filter status

## How to apply

After aggregating ion counts by filter status from qc_summary() output using data.table, construct a ggplot2 treemap geometry with geom_treemap() and geom_treemap_text() to display status labels and ion counts. Apply the Greens palette via scale_fill_brewer(palette = 'Greens') to map filter status categories to shades of green, where lighter shades represent lower status ranks and darker shades represent higher ranks or more severe filtering outcomes. The sequential nature of Greens makes it suitable for ordinal status levels (e.g., passed → flagged → failed). Customize treemap appearance with theme() to remove legend if status labels are already visible in geom_treemap_text(), and adjust text size and color for readability against the green background. This approach aligns with ggplot2 best practices for discrete categorical fills while maintaining visual hierarchy.

## Related tools

- **ggplot2** (Foundation for treemap geometry layers (geom_treemap, geom_treemap_text) and scale_fill_brewer(palette='Greens') color mapping)
- **treemapify** (Provides geom_treemap() and geom_treemap_text() geometries for rendering hierarchical rectangles with text labels)
- **RColorBrewer** (Supplies the 'Greens' sequential palette (9-color ramp) used via scale_fill_brewer())
- **mpactr** (Provides qc_summary() method that generates data.table output of ion filter status for treemap input) — https://github.com/mums2/mpactr
- **data.table** (Enables efficient aggregation of ion counts and percentage calculations from qc_summary() output using by= and .N/.SD syntax)

## Examples

```
ggplot(status_summary, aes(area = ion_count, fill = status, label = paste(status, '\n', ion_count, '\n', percentage, '%'))) + geom_treemap() + geom_treemap_text(colour = 'white', place = 'centre') + scale_fill_brewer(palette = 'Greens') + theme_minimal()
```

## Evaluation signals

- Treemap visual inspection: all filter status categories are rendered as rectangles with distinct green shades; no categories are missing or overlapping.
- Color fidelity: scale_fill_brewer(palette='Greens') call is present in ggplot() specification; verify via ggplot_build(plot)$data[[scale_index]]$fill contains valid green hex codes (e.g., #E5F5E0, #31A354).
- Text legibility: geom_treemap_text() labels (status, count, percentage) are readable against green background; font color (default black or white) does not merge with fill.
- Palette coverage: number of distinct green shades used equals number of unique filter status levels; verify nlevels(factor(data$status)) ≤ length(brewer.pal(9,'Greens')).
- Output file properties: exported PNG/PDF contains correct dimensions and DPI; verify via file metadata or manual inspection of rendered treemap matches on-screen appearance.

## Limitations

- RColorBrewer Greens palette is optimized for 3–9 categories; application to >9 distinct filter statuses requires manual color interpolation or alternative palette.
- Greens palette may have reduced contrast on light backgrounds or screens with low brightness; test rendering on target display hardware.
- Sequential Greens palette assumes ordinal relationship between status categories (e.g., passed < flagged < failed); if statuses are unordered nominal categories, a different palette family (Set1, Paired) may be more appropriate.
- The article does not specify whether treemap should use alpha transparency or pattern fills for accessibility; Greens palette alone may not fully satisfy WCAG AAA color contrast requirements for all audiences.

## Evidence

- [methods] Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette: "Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette, no legend, sized by ion count and labeled with status and percentage."
- [methods] Ion counts and percentages rendered as treemap from qc_summary() output: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text()"
- [methods] Customization via ggplot2 scale_fill_brewer() and theme() functions: "the visualization can be customized with ggplot2 scale_fill_brewer() and theme() functions."
- [other] Research question on visualizing filtering results by filter status: "How can filtering results from qc_summary() be visualized as a treemap showing the count and percentage of ions in each filter status category?"
