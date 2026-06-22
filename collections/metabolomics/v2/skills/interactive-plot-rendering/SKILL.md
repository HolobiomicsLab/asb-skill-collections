---
name: interactive-plot-rendering
description: Use when you have validated omics data loaded into R (expression matrices, fold-change and p-value pairs, gene ontology enrichment statistics, survival or distribution data) and need to generate publication-quality figures that must be explored interactively via a web browser, support pan/zoom, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3316
  - http://edamontology.org/topic_0219
  tools:
  - R Shiny
  - ggplot2
  - plotly
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# interactive-plot-rendering

## Summary

Render statistical plots (volcano plots, heatmaps, GO dotplots, cumulative distribution curves, MA plots, ROC curves) as interactive web-based visualizations within an R Shiny application, enabling real-time exploration and export to static formats. This skill transforms parsed omics data into publication-ready, zoomable, and interactive figures suitable for web deployment.

## When to use

You have validated omics data loaded into R (expression matrices, fold-change and p-value pairs, gene ontology enrichment statistics, survival or distribution data) and need to generate publication-quality figures that must be explored interactively via a web browser, support pan/zoom, and be exported as PNG, PDF, or interactive HTML. Use this skill when the audience requires dynamic exploration rather than static images alone.

## When NOT to use

- Input data is not yet parsed or validated — first apply data loading and schema validation before rendering.
- Visualization requirement is a static publication figure only without interactive exploration needs — use base R or ggplot2 export directly without Shiny overhead.
- Data contains missing values or outliers that have not been addressed — render will fail or produce misleading aesthetics; handle missing data and outlier filtering before this step.

## Inputs

- Parsed R data frame with volcano plot columns: fold_change (numeric), p_value (numeric)
- Parsed R data frame with expression matrix: rows=genes, columns=samples, values=expression counts
- Parsed R data frame with group annotations: sample_id, group_label
- Parsed R data frame with GO enrichment results: GO_term (character), p_value or adjusted_p_value (numeric), gene_ratio (numeric), gene_count (integer)
- Parsed R data frame with cumulative distribution data: value (numeric), optionally group (character for multi-group)
- Parsed R data frame with MA plot data: log2_fold_change (numeric), log2_average_expression (numeric)
- Parsed R data frame with ROC curve data: predicted_score (numeric), true_class (binary)

## Outputs

- Interactive web widget rendered in R Shiny UI (plot object via renderPlot() or renderPlotly())
- PNG static image exported via png() device driver
- PDF static image exported via pdf() device driver
- Interactive HTML file (plotly or Shiny app) suitable for standalone viewing or deployment

## How to apply

Load the parsed and validated data frame into R Shiny's reactive context. Select the appropriate visualization type (volcano plot, heatmap, GO dotplot, CDC, MA plot, ROC curve, etc.) based on the data structure and research question. Map data columns to aesthetic parameters: for volcano plots, fold-change to x-axis and −log10(p-value) to y-axis with significance threshold lines overlaid; for heatmaps, apply row and column clustering and color scaling to expression values with group annotations as sidebars; for GO dotplots, place GO terms on y-axis and quantitative metrics (e.g., −log10(p-value)) on x-axis with bubble size proportional to gene count and color scaled by enrichment metric. Use ggplot2 or plotly to construct the base plot, then wrap with renderPlot() or renderPlotly() to expose interactivity (hover tooltips, click events, zoom). Configure export buttons to save to PNG (via png() device) and optionally to interactive HTML (via plotly). Verify all axis labels, legends, and titles are populated and legible at intended display size.

## Related tools

- **R Shiny** (Application framework for rendering interactive plots and managing UI reactivity; wraps base R and ggplot2 plots with renderPlot() or renderPlotly() to expose zoom, pan, hover, and export capabilities) — https://github.com/rstudio/shiny
- **ggplot2** (Grammar of graphics layer for constructing static plot objects that are then wrapped by Shiny for interactivity; handles aesthetic mapping, scaling, and layering) — https://github.com/tidyverse/ggplot2
- **plotly** (R plotting library that generates interactive plots with built-in hover tooltips, zoom, pan, and one-click export to PNG; used as alternative to ggplot2 + renderPlot for enhanced interactivity) — https://github.com/plotly/plotly.r
- **GraphBio** (Reference R Shiny dashboard application that implements this skill across 15+ visualization types (volcano, heatmap, GO dotplot, CDC, MA, ROC, etc.); serves as example implementation) — https://github.com/databio2022/GraphBio

## Examples

```
renderPlotly({ggplot(volcano_data, aes(x=log2_fold_change, y=-log10(p_value))) + geom_point() + geom_hline(yintercept=-log10(0.05), linetype='dashed') + geom_vline(xintercept=c(-1, 1), linetype='dashed')})
```

## Evaluation signals

- Plot renders without error in Shiny UI; no console warnings about missing aesthetics, NaN values, or infinite scales.
- Axes are correctly labeled with data column names and units (e.g., 'log2(fold change)', '−log10(p-value)', 'GO term').
- Hover tooltip (plotly) or interactive elements (ggplot2 + Shiny) display expected data values when user interacts with plot elements.
- Exported PNG/PDF file exists on disk, opens without corruption, and displays all plot elements (legend, title, axis labels) legibly.
- For volcano plots: significance threshold lines (p=0.05 or adjusted p cutoff, fold-change cutoffs) are overlaid and correctly positioned on log-scales.
- For heatmaps: row and column clustering dendrograms are computed and rendered; group annotation sidebar colors match group_info.csv labels.
- For GO dotplots: bubble size reflects gene count values; bubble color gradient matches enrichment metric range; GO terms are readable and non-overlapping.

## Limitations

- Large datasets (>10,000 genes or >5,000 samples) may cause slow rendering or browser lag in interactive mode; consider subsampling or server-side filtering.
- Export to PNG via png() device may produce low resolution (default 72 dpi); users should increase width and height parameters or use pdf() for vector output.
- Interactive tooltips and zoom behavior depend on plotly; ggplot2 + renderPlot() offers limited interactivity compared to native plotly objects.
- Color palette and theme choices are not data-driven and may not be colorblind-friendly by default; user must specify palette manually (e.g., viridis, RColorBrewer).
- Reactivity in Shiny may update plots on every data change, causing flicker or performance issues if tied to real-time input controls; debounce or cache intermediate results.

## Evidence

- [readme] GraphBio---A modular and scalable R Shiny dashboard: "GraphBio---A modular and scalable R Shiny dashboard"
- [other] Render the interactive heatmap within the R Shiny application interface.: "Render the interactive heatmap within the R Shiny application interface."
- [other] Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles.: "Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles."
- [other] Render plot as an interactive or static figure suitable for web display and export as PNG or PDF.: "Render plot as an interactive or static figure suitable for web display and export as PNG or PDF."
- [readme] GraphBio: a shiny web app to easily perform popular visualization analysis for omics data: "GraphBio: a shiny web app to easily perform popular visualization analysis for omics data"
