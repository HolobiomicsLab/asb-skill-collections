---
name: volcano-plot-generation
description: Use when you have CSV files containing fold-change estimates and statistical
  p-values from a differential expression analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - R Shiny
  - Docker
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

# volcano-plot-generation

## Summary

Generate an interactive volcano plot from differential expression data (fold change and p-values) to simultaneously visualize statistical significance and effect size, with customizable threshold lines for identifying differentially expressed genes or features.

## When to use

You have CSV files containing fold-change estimates and statistical p-values from a differential expression analysis (e.g., RNA-seq, proteomics, or metabolomics comparisons) and need to identify and visualize features that are both statistically significant and biologically meaningful by effect size. Volcano plots are appropriate when you want to display the joint distribution of two contrasting dimensions: magnitude of change (x-axis) and statistical confidence (y-axis).

## When NOT to use

- Input data lacks valid p-values or fold-change estimates (e.g., only raw counts or already-filtered lists of significant genes).
- The analysis goal is exploratory clustering or sample-level quality control rather than feature-level ranking by effect and significance.
- Data are already aggregated into binary significant/non-significant calls without access to the underlying continuous fold-change and p-value distributions.

## Inputs

- CSV file with columns for fold change and p-value (e.g., volcano_example.csv)
- Optional: metadata or grouping information for filtering or stratification

## Outputs

- Interactive or static volcano plot (web display, PNG, or PDF)
- Plotted data with significance and fold-change threshold annotations

## How to apply

Load a CSV file with columns for fold change and p-value. Compute −log₁₀(p-value) to transform p-values into a linear scale suitable for the y-axis. Set significance thresholds: typically p=0.05 (corresponding to −log₁₀(p)≈1.30) on the y-axis and symmetric fold-change cutoffs (e.g., |log₂FC| > 1 or > 2) on the x-axis. Render the plot as an interactive R Shiny visualization with threshold reference lines overlaid to delineate the region of interest (e.g., high fold change AND low p-value). Export the result as a PNG or PDF for publication or further sharing.

## Related tools

- **R Shiny** (Interactive web application framework for rendering and displaying the volcano plot with interactive threshold controls and export options) — https://github.com/databio2022/GraphBio
- **Docker** (Containerization tool for deploying the GraphBio Shiny application to a web server for remote access) — https://github.com/databio2022/GraphBio

## Evaluation signals

- The volcano plot correctly displays fold change on the x-axis (linear or log scale) and −log₁₀(p-value) on the y-axis.
- Horizontal and vertical threshold lines (e.g., p=0.05, fold-change cutoffs) are rendered and align with user-specified or default parameters.
- Points representing features with both high absolute fold change AND low p-value cluster in the upper-left and upper-right regions of the plot.
- Export formats (PNG, PDF) render without distortion and preserve labels, legend, and threshold annotations.
- Plot is interactive (if using Shiny): users can hover to identify features, adjust thresholds dynamically, and observe the change in point counts and coloring.

## Limitations

- Volcano plots assume a two-group comparison; multi-group or time-series data require additional stratification or separate plots per contrast.
- The choice of p-value threshold and fold-change cutoff is arbitrary and should be justified by biological domain knowledge, not statistical convention alone.
- Extreme p-values (p < 1e-300) may cause numerical overflow in −log₁₀ transformation; pseudocounts or capping strategies may be needed.
- Missing or invalid p-values or fold-change values in the input CSV will cause plotting errors or data loss.

## Evidence

- [other] GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical significance versus fold change relationships.: "volcano_example.csv and volcano_example1.csv for volcano plot"
- [other] Compute −log10(p-value) transformation for the y-axis and generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis).: "Compute −log10(p-value) transformation for the y-axis. 3. Generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on"
- [readme] GraphBio is a modular and scalable R Shiny dashboard for omics data visualization.: "GraphBio---A modular and scalable R Shiny dashboard"
- [other] Render plot as an interactive or static figure suitable for web display and export as PNG or PDF.: "Render plot as an interactive or static figure suitable for web display and export as PNG or PDF"
