---
name: ggplot2-geom-treemap-rendering
description: Use when after running qc_summary() on a filtered mpactr object and aggregating ion counts by filter status category (passed/failed).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - ggplot2
  - treemapify
  - mpactr
  - data.table
  - scale_fill_brewer()
  techniques:
  - LC-MS
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`
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

# ggplot2-geom-treemap-rendering

## Summary

Render hierarchical ion filtering results as a treemap visualization using ggplot2's geom_treemap() and geom_treemap_text() layers, scaled by ion counts and annotated with filter status labels and percentages. This skill transforms aggregated qc_summary() data into a publication-ready treemap that communicates the distribution and relative abundance of ions across filter outcome categories.

## When to use

After running qc_summary() on a filtered mpactr object and aggregating ion counts by filter status category (passed/failed). Use this skill when you need to communicate the proportional breakdown of ions retained vs. removed by filtering, and when a compact, area-encoded visualization is preferred over bar charts for showing multiple hierarchical dimensions (status, count, percentage) simultaneously.

## When NOT to use

- Input contains only a single filter status category (treemap loses hierarchical meaning with one rectangle).
- Ion count data is not pre-aggregated by status; raw feature-level data will produce an uninterpretable treemap with too many small tiles.
- Audience requires precise numerical comparison across many status categories; bar charts or tables are more readable than area encoding when exact values matter more than proportional intuition.

## Inputs

- mpactr object (filtered)
- data.table from qc_summary() output containing ion status (passed/failed filters)
- aggregated ion counts by filter status category

## Outputs

- ggplot2 treemap object
- PNG file of rendered treemap visualization

## How to apply

Extract the qc_summary() data.table, aggregate ion counts by filter status using data.table syntax, and calculate the percentage of total ions per status. Initialize a ggplot() call mapping status to fill aesthetic and ion count to the area parameter. Layer geom_treemap() to render rectangles sized by ion count, then geom_treemap_text() to overlay status labels and percentage annotations. Customize with scale_fill_brewer() (e.g., Greens palette) to distinguish status categories, suppress the legend, and apply ggplot2 theme() functions for publication formatting. Save the rendered plot to PNG.

## Related tools

- **ggplot2** (Core graphics framework for treemap layer specification and customization)
- **treemapify** (Provides geom_treemap() and geom_treemap_text() layers for rectangular treemap rendering)
- **mpactr** (Generates qc_summary() data.table containing ion filter status used as input) — https://github.com/mums2/mpactr
- **data.table** (Efficient aggregation and percentage calculation from qc_summary() output)
- **scale_fill_brewer()** (Applies categorical color palette (e.g., Greens) to distinguish filter status)

## Examples

```
qc_dt <- qc_summary(filtered_mpactr_obj)[, .(ion_count = .N, pct = 100*.N/nrow(qc_summary(filtered_mpactr_obj))), by=status]; ggplot(qc_dt, aes(area=ion_count, fill=status, label=paste0(status, '\n', ion_count, ' (', round(pct,1), '%)'))) + geom_treemap() + geom_treemap_text(place='centre') + scale_fill_brewer(palette='Greens') + theme(legend.position='none') + ggsave('ion_filter_treemap.png')
```

## Evaluation signals

- Treemap renders with exactly one rectangle per filter status category, sized proportional to ion count.
- geom_treemap_text() labels are legible and correctly display status name, ion count, and percentage (sum to 100%).
- Color palette is applied consistently and legend is suppressed when specified.
- PNG file is written to disk with expected dimensions and no rendering artifacts.
- Ion counts in treemap match aggregated values from qc_summary() data.table (no data loss or duplication).

## Limitations

- Treemap readability degrades with more than ~6–8 status categories; extremely granular status hierarchies may require faceting or hierarchical treemaps.
- Text labels may overlap or become unreadable if rectangles are too small; aggregate data or increase figure dimensions as needed.
- Treemapify's geom_treemap() does not natively support interactive tooltips; use plotly::ggplotly() for interactivity or plotly treemaps for hover annotations.
- Color blindness accessibility depends on palette choice; scale_fill_brewer() Greens is red–green colorblind-safe, but confirm with CVD simulators for other palettes.

## Evidence

- [other] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text() to display status labels, ion counts, and percentages: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text() to display status labels,"
- [other] Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette, no legend, sized by ion count and labeled with status and percentage.: "Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette, no legend, sized by ion count and labeled with status and percentage"
- [other] The visualization can be customized with ggplot2 scale_fill_brewer() and theme() functions.: "The visualization can be customized with ggplot2 scale_fill_brewer() and theme() functions"
