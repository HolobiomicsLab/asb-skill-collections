---
name: fold-change-significance-interpretation
description: Use when when you have differential expression results with both fold-change
  and p-value columns from a CSV file (e.g., volcano_example.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3674
  tools:
  - R Shiny
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fold-change-significance-interpretation

## Summary

Interpret the relationship between fold change (effect size) and statistical significance (p-value) in differential expression data by visualizing them jointly on a volcano plot, allowing rapid identification of biologically and statistically meaningful expression changes.

## When to use

When you have differential expression results with both fold-change and p-value columns from a CSV file (e.g., volcano_example.csv format), and need to simultaneously assess both magnitude of change and statistical confidence to prioritize genes or features for downstream validation or functional analysis.

## When NOT to use

- Input CSV lacks both fold-change and p-value columns (required for scatter interpretation).
- Data is already filtered to only highly significant genes; the joint fold-change–significance trade-off is the core insight, so pre-filtered datasets lose interpretive value.
- P-values are not valid statistical tests (e.g., rank correlations or arbitrary thresholds); volcano plots assume well-calibrated p-values.

## Inputs

- CSV file with fold-change column (typically log2-transformed) and p-value column (e.g., volcano_example.csv or volcano_example1.csv)
- Optionally: threshold parameters for fold-change cutoffs and significance level (default p=0.05)

## Outputs

- Interactive or static volcano plot visualization showing fold change vs. −log10(p-value) relationship
- PNG or PDF export of volcano plot suitable for publication or presentation

## How to apply

Load the CSV file containing fold-change and p-value columns into R. Transform p-values using −log10(p-value) to compress the scale and emphasize small p-values on the y-axis. Plot fold change (typically log2-transformed) on the x-axis against −log10(p-value) on the y-axis. Add vertical threshold lines at typical fold-change cutoffs (e.g., ±1 or ±2 log2-fold change) and a horizontal line at −log10(0.05) to demarcate the significance boundary (p=0.05). Features in the upper-left and upper-right regions (high −log10(p-value) AND large fold change magnitude) represent the most reliable differentially expressed candidates. Render the plot interactively in R Shiny for web display, with option to export as PNG or PDF.

## Related tools

- **R Shiny** (Interactive visualization framework for rendering volcano plots as a modular web dashboard component, with built-in support for threshold adjustment and plot export.) — https://github.com/databio2022/GraphBio

## Examples

```
# In R Shiny: load CSV, extract fold-change and p-value, compute -log10(p-value), plot with threshold lines at FC=±1 and p=0.05, export PNG
```

## Evaluation signals

- Plot displays clear quadrants with upper-left and upper-right regions enriched for significant, large-magnitude changes; lower regions show non-significant results.
- Threshold lines (vertical fold-change and horizontal p-value) are visibly labeled and accurately positioned at specified cutoffs (e.g., ±log2-fold change, p=0.05).
- Interactive features (hover tooltips, zoom, export) function without errors; PNG/PDF exports retain axis labels, legend, and all threshold annotations.
- Axis scales are appropriate: x-axis spans the fold-change range (typically −4 to +4 or wider), y-axis spans −log10(p-value) from 0 to 1–3+ depending on data distribution.
- No data points are plotted outside the axis bounds; missing or infinite −log10(p-value) values are handled gracefully (e.g., excluded or capped).

## Limitations

- Volcano plots do not account for multiple-testing correction at the visualization stage; the p-value threshold displayed is typically unadjusted; practitioners should filter input data to adjusted p-values if multiple-testing correction has been applied.
- Fold-change and p-value are not independent; very small sample sizes or high noise can yield high p-values even for large fold changes, or vice versa; visual interpretation must consider the experimental design and data quality.
- No automatic detection of optimal fold-change or p-value thresholds; thresholds are user-specified or convention-based (e.g., p=0.05, log2-FC=1) and should be justified by the study's biological or statistical context.

## Evidence

- [other] Workflow step: Load volcano demo CSV file(s), extract columns for fold change and p-value; compute −log10(p-value) transformation; generate interactive volcano plot with significance threshold lines; render for web display and export.: "Load volcano demo CSV file(s) (volcano_example.csv and/or volcano_example1.csv) into R, extracting columns for fold change and p-value. Compute −log10(p-value) transformation for the y-axis. Generate"
- [readme] Demo data specification: volcano_example.csv and volcano_example1.csv are used for volcano plot visualization.: "volcano_example.csv and volcano_example1.csv for volcano plot"
- [other] Tool application: GraphBio provides volcano plot visualization functionality that accepts demo data files as inputs.: "GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical"
