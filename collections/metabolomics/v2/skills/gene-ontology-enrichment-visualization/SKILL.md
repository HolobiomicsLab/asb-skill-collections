---
name: gene-ontology-enrichment-visualization
description: Use when you have completed a GO enrichment analysis (e.g., via hypergeometric test or similar) and need to visualize the results as a dotplot. Input is a CSV table with columns for GO term identifiers, p-values or adjusted p-values, gene ratios (or counts), and gene count;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0092
  tools:
  - R Shiny
  - ggplot2
  - plotly
  - GraphBio Docker image
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
---

# gene-ontology-enrichment-visualization

## Summary

Generate interactive bubble dotplots for Gene Ontology (GO) enrichment results, mapping GO terms to quantitative enrichment metrics (p-values, gene ratios, counts) across two distinct visualization styles. This skill transforms tabular GO term statistics into publication-ready, explorable graphics for communicating functional annotation findings.

## When to use

You have completed a GO enrichment analysis (e.g., via hypergeometric test or similar) and need to visualize the results as a dotplot. Input is a CSV table with columns for GO term identifiers, p-values or adjusted p-values, gene ratios (or counts), and gene count; you want to communicate both the statistical significance and the magnitude of enrichment in a single, scalable visualization.

## When NOT to use

- Input lacks GO term identifiers or p-value columns; pre-process with a GO enrichment tool first.
- You need to perform the GO enrichment analysis itself; this skill assumes enrichment is already complete.
- Input is a raw gene list without functional annotation; use a GO enrichment engine (e.g., clusterProfiler, topGO) first.

## Inputs

- go_term_bubble.csv (CSV table with GO term IDs, p-values, gene ratios, gene counts for style 1)
- go_bubble_example.csv (CSV table with GO term IDs and enrichment metrics for style 2)
- R data frame with validated GO enrichment statistics

## Outputs

- Interactive ggplot2 or plotly GO dotplot visualization (style 1)
- Interactive ggplot2 or plotly GO dotplot visualization (style 2)
- PNG-exported GO dotplot figure(s)
- Interactive HTML GO dotplot (optional)

## How to apply

Load the GO enrichment CSV (either go_term_bubble.csv for style 1 or go_bubble_example.csv for style 2) into R as a data frame. Validate the presence and format of required columns: GO term IDs, p-values or adjusted p-values, gene ratios, and gene counts. For style 1, map GO terms to the y-axis, a quantitative measure (e.g., −log10(p-value) or enrichment score) to the x-axis, bubble size proportional to gene count, and bubble color scaled by the selected metric (e.g., p-value or gene count gradient). For style 2, apply alternative aesthetic mappings as specified in the demo data structure. Render both styles as interactive ggplot2 or plotly visualizations with labeled axes, legend, and title. Export as PNG for publication or interactive HTML for exploration.

## Related tools

- **R Shiny** (Web framework for hosting and rendering interactive GO dotplot visualizations with real-time parameter adjustment) — github.com/databio2022/GraphBio
- **ggplot2** (R graphics package for constructing layered aesthetic mappings (GO terms, p-values, bubble size/color) in dotplot)
- **plotly** (R package for converting static ggplot2 dotplots into interactive HTML visualizations with hover tooltips and zoom)
- **GraphBio Docker image** (Pre-configured containerized deployment of the full GraphBio application including GO dotplot module) — databio2022/graphbio

## Evaluation signals

- GO term identifiers are correctly parsed and appear on the y-axis without truncation or encoding errors.
- Quantitative metrics (−log10(p-value), enrichment score, or gene count) scale appropriately on the x-axis with no negative or infinite values displayed.
- Bubble sizes increase monotonically with gene count; bubble colors follow a consistent gradient matching the legend and metric range.
- Legend, axis labels, and title are present and human-readable; interactive version allows hover inspection of GO term name, p-value, gene count.
- Exported PNG has resolution ≥300 dpi and dimensions suitable for publication; interactive HTML loads without rendering errors in a web browser.

## Limitations

- GraphBio accepts exactly two predefined CSV formats (go_term_bubble.csv and go_bubble_example.csv); custom column names or additional metrics require manual data reshaping.
- Bubble dotplots become difficult to interpret when >100 GO terms are present; consider filtering by p-value threshold or selecting top N terms.
- Color gradients and aesthetic defaults are fixed within the application; deep customization of aesthetics (e.g., specific color palettes, axis scales) may require direct R/ggplot2 scripting outside GraphBio.
- Export formats are limited to PNG and optional HTML; other publication formats (PDF, SVG) are not mentioned as supported.

## Evidence

- [other] GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2, enabling generation of GO term bubble visualizations in two distinct formats.: "GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2"
- [other] For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble color scaled by the selected metric.: "For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble"
- [other] Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles. Export the GO dotplot figures as PNG and optionally as interactive HTML.: "Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles. Export the GO dotplot figures as PNG and optionally as interactive HTML"
- [readme] GraphBio: a shiny web app to easily perform popular visualization analysis for omics data: "GraphBio: a shiny web app to easily perform popular visualization analysis for omics data"
- [readme] go_bubble_example.csv for go dotplot style 2; go_term_bubble.csv for go dotplot style 1: "go_bubble_example.csv for go dotplot style 2; go_term_bubble.csv for go dotplot style 1"
