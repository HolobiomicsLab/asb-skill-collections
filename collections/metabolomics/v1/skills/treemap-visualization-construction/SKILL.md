---
name: treemap-visualization-construction
description: Use when after applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to an mpactr object, use this skill when you need to communicate the count and percentage breakdown of ions retained vs. rejected across filter status categories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - R
  - ggplot
  - ggplot2
  - treemapify
  - data.table
  - mpactr
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
---

# treemap-visualization-construction

## Summary

Construct a treemap visualization to display the distribution and proportions of ions across filter status categories (passed/failed) from qc_summary() output. This skill enables rapid visual assessment of filtering efficiency and ion loss across multiple quality control filters in metabolomics workflows.

## When to use

After applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to an mpactr object, use this skill when you need to communicate the count and percentage breakdown of ions retained vs. rejected across filter status categories. Particularly useful when presenting filtering results to stakeholders or deciding whether filter thresholds should be adjusted based on ion loss.

## When NOT to use

- Ion counts are not aggregated by a categorical status variable—use bar or box plots instead.
- The goal is to show hierarchical relationships across >2 categorical levels; use nested treemaps or sunburst plots.
- Real-time filtering decisions are needed; static PNG output is insufficient—use interactive plotly rendering.

## Inputs

- mpactr object (filtered, post-filter_* operations)
- qc_summary() output (data.table with ion status column)

## Outputs

- ggplot2 treemap object (geom_treemap + geom_treemap_text)
- PNG file (rendered treemap visualization)

## How to apply

Extract qc_summary() data.table from the filtered mpactr object, which reports ion status (passed/failed filters). Aggregate ion counts by status category using data.table syntax and compute the percentage of total ions per status. Construct a treemap using ggplot2 geom_treemap() and geom_treemap_text() layers, mapping ion count to the area aesthetic and status category to the fill aesthetic. Customize the palette (e.g., scale_fill_brewer with Greens) and remove the legend to maximize plot area. Label each tile with the status category, ion count, and percentage. The treemap's area-to-count encoding makes relative filtering impact immediately apparent.

## Related tools

- **ggplot2** (Foundation for treemap geometry (geom_treemap, geom_treemap_text) and scale customization (scale_fill_brewer, theme))
- **treemapify** (Provides geom_treemap and geom_treemap_text geometries for rendering hierarchical area-encoded visualizations)
- **data.table** (Efficient aggregation of ion counts and percentage computation from qc_summary() output)
- **mpactr** (Supplies filtered object and qc_summary() method reporting ion status by filter result) — https://github.com/mums2/mpactr

## Examples

```
qc_dt <- filtered_mpactr_obj$qc_summary(); status_counts <- qc_dt[, .(ion_count = .N), by = status][, pct := 100 * ion_count / sum(ion_count)]; ggplot(status_counts, aes(area = ion_count, fill = status, label = paste(status, ion_count, sprintf('%.1f%%', pct)))) + geom_treemap() + geom_treemap_text(colour = 'black', place = 'centre') + scale_fill_brewer(palette = 'Greens') + theme(legend.position = 'none')
```

## Evaluation signals

- Treemap tiles sum to 100% across all status categories; no ion count discrepancies.
- Area of each tile is proportional to ion count; visual scaling is accurate (spot-check 2–3 tiles).
- Text labels (status, count, percentage) are readable and do not overlap within tiles.
- Color palette (e.g., Greens) differentiates status categories clearly; no ambiguity between fill values.
- PNG output renders without clipping or layer misalignment; compare rendered size to expected dimensions.

## Limitations

- Treemaps are less effective when comparing very small ion counts (<<1% of total); consider adding a numeric table for precise values.
- Only two categorical levels (status × count) are shown; more complex hierarchies (e.g., status × filter_type × count) require faceting or nested treemaps.
- Static PNG output loses interactivity; hover tooltips and dynamic filtering are not available without switching to plotly.
- Requires qc_summary() output structure; custom status columns or missing data will require preprocessing before aggregation.

## Evidence

- [other] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text() to display status labels, ion counts, and percentages: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text() to display status labels,"
- [other] Aggregate ion counts by status category and calculate percentage of total ions per status.: "Aggregate ion counts by status category and calculate percentage of total ions per status."
- [other] Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette, no legend, sized by ion count and labeled with status and percentage.: "Create a treemap using ggplot2 geom_treemap() and geom_treemap_text() with Greens palette, no legend, sized by ion count and labeled with status and percentage."
- [methods] creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`: "creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`"
