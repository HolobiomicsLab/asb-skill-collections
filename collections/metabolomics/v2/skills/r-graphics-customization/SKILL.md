---
name: r-graphics-customization
description: Use when when you have completed a comprehensive ranking of preprocessing workflows (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - norvisualization
  - R graphics functions
  - ggord
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- Run norvisualization on the overall ranking CSV
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# r-graphics-customization

## Summary

Configure and render circular barplots in R to visualize ranked metabolomic preprocessing workflows with performance metrics. This skill applies R graphics functions to transform ranking CSV data into publication-ready circular layouts that emphasize relative workflow performance.

## When to use

When you have completed a comprehensive ranking of preprocessing workflows (e.g., from NOREVA's normulticlassqcall or nortimecoursenoall) and need to display the top-N workflows (typically top-100) in a circular barplot format to identify and communicate the best-performing preprocessing strategies for a specific metabolomic dataset.

## When NOT to use

- Ranking CSV file is absent or in a non-standard format not recognized by norvisualization.
- Fewer than 10 workflows in the ranking file (circular layout becomes illegible).
- Performance scores contain negative values or do not follow a consistent scale suitable for radial representation.

## Inputs

- overall ranking CSV file (containing workflow IDs, performance scores, and metadata from NOREVA assessment)
- cutoff parameter (integer, typically 100)

## Outputs

- circular barplot visualization (PNG or PDF format)
- ranked workflow figure with performance metrics displayed radially

## How to apply

Load the overall ranking CSV file produced by NOREVA's workflow assessment functions into R. Call the norvisualization function with the ranking file and set the cutoff parameter to the desired number of top workflows (e.g., cutoff='100' for top-100 rankings). The function extracts and orders workflows by performance score, then uses R graphics functions to render a circular barplot where radius represents performance and angular position reflects workflow rank. Save the output figure in PNG or PDF format with a descriptive filename (e.g., NOREVA-Ranking-Top.100.workflows.png).

## Related tools

- **norvisualization** (Extracts top-N ranked workflows from CSV and configures circular barplot rendering with performance scores and workflow metadata.) — https://github.com/idrblab/NOREVA
- **R graphics functions** (Render circular layout, map performance scores to radius, apply color scales, and export final figure to PNG/PDF.) — https://www.r-project.org/
- **ggord** (Optional enhancement for ordination-based circular visualizations in NOREVA workflows.) — https://github.com/fawda123/ggord

## Examples

```
library(NOREVA); norvisualization(fileName='overall_ranking.csv', cutoff='100'); # outputs NOREVA-Ranking-Top.100.workflows.png/pdf
```

## Evaluation signals

- Output file exists at expected path with correct naming convention (e.g., NOREVA-Ranking-Top.100.workflows.png).
- Circular barplot displays exactly N workflows (or up to N if fewer exist) ordered by performance score from highest (longest radius) to lowest.
- Workflows are evenly distributed around the circle with no overlapping labels or bars; radial scale is linear and matches the performance score range from the input CSV.
- Visual encoding is consistent: color, bar height (radius), and angular position all reflect workflow rank and performance metrics without distortion.
- Figure is exportable in both PNG and PDF formats with legible resolution (≥300 DPI recommended for publication).

## Limitations

- Circular barplot clarity degrades when visualizing >150–200 workflows; cutoff parameter should be tuned to dataset size and figure resolution.
- Performance scores must be comparable across all workflows (normalized or on a consistent scale); mixed units or incompatible metrics will produce misleading visualizations.
- The norvisualization function depends on the exact schema of the NOREVA ranking CSV file; custom ranking files from other sources may not parse correctly.
- No built-in interactive features (hover tooltips, drill-down); static export limits exploratory analysis of individual workflows.

## Evidence

- [other] The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to "100" to produce a circular barplot illustration of the top-100 processing workflows ranked by performance.: "The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to "100" to produce a circular barplot illustration of the top-100 processing workflows ranked by"
- [other] Generate a circular barplot visualization using R graphics functions, with workflows ranked by performance score and displayed in circular layout.: "Generate a circular barplot visualization using R graphics functions, with workflows ranked by performance score and displayed in circular layout."
- [readme] NOREVA enables pre-processing and assessment of multi-class/time-series metabolomic data and realize a high-throughput discovery of the well-performing pre-processing: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [other] Save the resulting figure as NOREVA-Ranking-Top.100.workflows in PNG or PDF format.: "Save the resulting figure as NOREVA-Ranking-Top.100.workflows in PNG or PDF format."
