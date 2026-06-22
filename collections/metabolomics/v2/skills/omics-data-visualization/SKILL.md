---
name: omics-data-visualization
description: Use when you have tabular omics data (expression matrices, p-values, fold changes, functional annotations, or clinical outcomes) in CSV format and need to generate publication-ready visualizations that reveal distributional patterns, statistical significance thresholds, group comparisons, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3517
  tools:
  - R Shiny
  - Docker
  - GraphBio
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# omics-data-visualization

## Summary

GraphBio is an R Shiny web application that generates interactive and static visualizations for omics data, including volcano plots, heatmaps, cumulative distribution curves, chord plots, network plots, GO dotplots, MA plots, ROC curves, and survival curves from CSV input files. This skill enables rapid exploratory and publication-quality visualization of differential expression, statistical relationships, and functional enrichment patterns in genomic datasets.

## When to use

Apply this skill when you have tabular omics data (expression matrices, p-values, fold changes, functional annotations, or clinical outcomes) in CSV format and need to generate publication-ready visualizations that reveal distributional patterns, statistical significance thresholds, group comparisons, or functional relationships. Use it specifically when your analysis goal involves assessing fold-change versus p-value trade-offs (volcano plots), comparing distributions across groups (CDCs), exploring gene co-expression networks (network plots), or visualizing enrichment results (GO dotplots).

## When NOT to use

- When your data is not in tabular CSV format (e.g., raw sequencing reads, BAM files, or HDF5 matrices) — GraphBio expects pre-processed, aggregated omics data with explicit columns.
- When your analysis requires advanced statistical modeling beyond visualization (e.g., mixed-effects models, Bayesian inference, time-series forecasting) — GraphBio is a visualization dashboard, not a statistical inference platform.
- When you need highly customized aesthetics or publication layouts beyond Shiny UI parameters — custom R/ggplot2 scripting will be more flexible than the constrained Shiny interface.

## Inputs

- CSV file containing fold-change and p-value columns (volcano plots)
- CSV file with distribution values, optionally stratified by group (CDCs)
- Expression matrix CSV (heatmap_test.csv) and optional group annotation file (group_info.csv)
- CSV with correlation or network edge data (network plots, correlation scatter plots)
- CSV with functional annotation or GO term data (GO dotplots)
- CSV with survival time and event status columns (survival curves)
- CSV with binary outcome and predictor columns (ROC curves)

## Outputs

- Interactive or static volcano plot (PNG/PDF) depicting fold-change vs. −log₁₀(p-value)
- Cumulative distribution curve figure(s) for single-group or multi-group datasets (PNG/PDF)
- Heatmap with hierarchical clustering and group annotation (PNG/PDF)
- Chord diagram showing categorical relationships (PNG/PDF)
- Network graph showing co-expression or correlation structure (PNG/PDF)
- GO dotplot or bubble plot with enrichment metrics (PNG/PDF)
- MA plot or ROC curve (PNG/PDF)
- Survival curve with confidence intervals (PNG/PDF)

## How to apply

Load your structured omics CSV file(s) into the GraphBio R Shiny application, where each visualization module expects a specific column structure (e.g., fold-change and p-value columns for volcano plots; distribution values stratified by group for CDCs). For volcano plots, the application computes −log₁₀(p-value) transformation and overlays threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis) to highlight significant features. For multi-group analyses (e.g., CDCs with cdc-multiple-group.csv), the workflow parses group-stratified data and renders overlaid or faceted curves. Select the appropriate demo data template (e.g., volcano_example.csv, cdc_example.csv, heatmap_test.csv + group_info.csv) that matches your data structure, configure aesthetic parameters in the Shiny UI (thresholds, group colors, axis labels), and export the rendered figure as PNG or PDF. The modular design allows independent execution of each visualization module without requiring external R scripting.

## Related tools

- **R Shiny** (Web framework for interactive omics visualization dashboard and parameter configuration UI) — https://shiny.rstudio.com
- **Docker** (Containerization and deployment tool for reproducible GraphBio environment) — https://docs.docker.com
- **GraphBio** (Complete R Shiny application implementing modular visualization modules for omics data) — https://github.com/databio2022/GraphBio

## Examples

```
docker run --rm -d -p 80:3838 -v /root/log/:/home/shiny/graphbio-log/ databio2022/graphbio:v2.2.7-manual /init
```

## Evaluation signals

- Volcano plot correctly renders fold-change on x-axis and −log₁₀(p-value) on y-axis with threshold lines at p=0.05 and expected fold-change cutoffs visibly distinguishing significant features above/outside thresholds.
- Cumulative distribution curves from multi-group CSV (cdc-multiple-group.csv) display separate overlaid or faceted curves per group with monotonic cumulative behavior (0 to 1 range).
- Heatmap displays correct hierarchical clustering, with rows (genes/features) and columns (samples) matching input matrix dimensions, and group_info.csv annotations rendered as side color bars.
- Exported PNG/PDF files are readable, contain complete axis labels and legends, and preserve plot interactivity (if using interactive format) without rendering errors or truncated elements.
- Network plots and chord diagrams correctly parse edge or categorical relationships from input CSV without duplicate or missing nodes, and visual layout is stable across re-renders.

## Limitations

- GraphBio expects pre-processed, aggregated CSV input; it does not perform upstream data normalization, batch correction, or quality control — users must prepare clean, quantile-normalized, or log-transformed data beforehand.
- The volcano plot module assumes a simple two-group comparison structure; complex multi-level factorial designs require external data reshaping before CSV input.
- Interactive visualization performance may degrade with very large datasets (e.g., >100,000 features or >10,000 samples) due to Shiny rendering overhead and browser memory constraints.
- Export formats are limited to PNG and PDF; no native support for SVG or interactive HTML export for embedding in other web platforms.
- The application provides no built-in statistical testing or p-value calculation; users must pre-compute statistics (p-values, fold-changes, enrichment scores) in external tools before visualization.

## Evidence

- [other] GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical significance versus fold change relationships.: "GraphBio provides volcano plot visualization functionality that accepts demo data files (volcano_example.csv and volcano_example1.csv) as inputs to generate volcano plots depicting statistical"
- [other] Compute −log10(p-value) transformation for the y-axis.: "Compute −log10(p-value) transformation for the y-axis."
- [other] Generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis).: "Generate interactive volcano plot using R Shiny with significance threshold lines (typically p=0.05 on y-axis and fold-change cutoffs on x-axis)."
- [other] GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis.: "GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis."
- [readme] GraphBio---A modular and scalable R Shiny dashboard: "GraphBio---A modular and scalable R Shiny dashboard"
- [readme] a shiny web app to easily perform popular visualization analysis for omics data: "a shiny web app to easily perform popular visualization analysis for omics data"
- [readme] heatmap_test.csv and group_info.csv for heatmap. 2. volcano_example.csv and volcano_example1.csv for volcano plot. 3. cdc_example.csv and cdc-mutiple-group.csv for Cumulative Distribution Curves 4. chord_example.csv for chord plot 5. corr_net.csv for network plot 6. corr_scatter.csv for correlation scatter plot 7. go_bubble_example.csv for go dotplot style 2: "heatmap_test.csv and group_info.csv for heatmap. 2. volcano_example.csv and volcano_example1.csv for volcano plot. 3. cdc_example.csv and cdc-mutiple-group.csv for Cumulative Distribution Curves"
- [readme] docker pull databio2022/graphbio:v2.2.7-manual: "docker pull databio2022/graphbio:v2.2.7-manual"
