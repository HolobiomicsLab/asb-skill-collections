---
name: enrichment-metric-scaling-and-normalization
description: Use when you have parsed GO enrichment results (CSV with GO term identifiers,
  p-values or adjusted p-values, gene ratios, and gene counts) and need to prepare
  these metrics for dotplot visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0091
  tools:
  - R Shiny
  - ggplot2
  - plotly
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

# enrichment-metric-scaling-and-normalization

## Summary

Transform raw GO enrichment metrics (p-values, gene counts, gene ratios) into scaled visual representations suitable for bubble plot aesthetics in omics visualization. This skill normalizes heterogeneous enrichment statistics into bounded, interpretable dimensions (bubble size, color intensity, axis position) for comparative display.

## When to use

You have parsed GO enrichment results (CSV with GO term identifiers, p-values or adjusted p-values, gene ratios, and gene counts) and need to prepare these metrics for dotplot visualization. Use this skill when raw metric ranges are too large or asymmetric to map directly to visual encodings, or when you need to highlight statistical significance and biological magnitude simultaneously across multiple GO terms.

## When NOT to use

- Input data lacks p-values or gene counts; scaling requires at least one quantitative enrichment metric.
- GO term identifiers or enrichment metrics are already pre-scaled or binned in the input CSV; re-scaling may introduce artifacts or loss of resolution.
- You need to preserve raw, unscaled p-values for statistical reporting or publication supplementary tables (use raw values separately).

## Inputs

- go_term_bubble.csv (CSV with columns: GO term ID, p-value or adjusted p-value, gene ratio, gene count)
- go_bubble_example.csv (CSV with alternative metric structure for style 2 visualization)
- data frame parsed from CSV in R with validated numeric and character columns

## Outputs

- Scaled numeric vectors (log-transformed p-values, normalized gene counts, color-mapped enrichment scores)
- ggplot2 or plotly object with scaled aesthetic mappings (x-axis, y-axis, bubble size, bubble color)
- PNG raster image of GO dotplot with legend and axis labels
- Interactive HTML visualization (optional plotly export)

## How to apply

Parse the two input CSV files (go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2) and extract columns for GO term IDs, p-values (or adjusted p-values), gene ratios, and gene counts. For style 1, apply log-transformation (e.g., −log10(p-value)) to compress the p-value distribution onto the x-axis and scale gene counts to bubble radius using a nonlinear mapping (e.g., sqrt or linear binning) to reduce visual dominance of outliers. For style 2, apply alternative aesthetic mappings as specified in the demo data (e.g., color gradients by enrichment score or different axis assignments). Validate that scaled values fall within expected ranges (e.g., bubble radii proportional to gene count, color intensity monotonic with significance or effect size). Render using ggplot2 or plotly with explicit scale definitions and legends clarifying the metric-to-visual encoding.

## Related tools

- **R Shiny** (Interactive web dashboard framework for rendering scaled GO dotplot visualizations and handling metric transformation workflows) — https://github.com/databio2022/GraphBio
- **ggplot2** (R graphics package for mapping scaled enrichment metrics to aesthetic layers (position, size, color) in dotplot construction)
- **plotly** (Interactive visualization library for rendering scaled GO dotplots with hover tooltips and dynamic legend controls)
- **Docker** (Container platform for deploying GraphBio with pre-configured metric scaling and GO dotplot modules) — https://hub.docker.com/r/databio2022/graphbio

## Evaluation signals

- Log-transformed p-values span a continuous range (e.g., 0–20 on −log10 scale) with no negative or undefined values; axis labels and scale bar are mathematically correct.
- Bubble sizes are monotonically increasing with gene count and proportional to visual area; no bubble exceeds plot boundaries or overlaps excessively.
- Color gradient is monotonic with the selected metric (e.g., lighter to darker with increasing p-value significance or enrichment score); legend is legible and maps all values in the data range.
- GO terms are correctly positioned on y-axis; x-axis label specifies transformation applied (e.g., '−log10(p-value)' or 'enrichment score').
- Both style 1 and style 2 dotplots render without errors; exported PNG and HTML files are readable and interactive features (hover, zoom, legend toggle) function in HTML format.

## Limitations

- Log-transformation of p-values assumes p-values follow uniform or beta distribution; extreme p-values (< 1e-300) may cause numerical underflow or overflow.
- Gene count scaling via bubble size can mask biological significance if gene counts are highly skewed; consider using robust percentile-based binning or square-root transformation for skewed distributions.
- Color scale choice (continuous vs. binned gradient) affects interpretation; the article does not specify which color palette or binning strategy is optimal, leaving this a design choice.
- CSV input must have correctly formatted column names and data types; missing or malformed entries (e.g., 'NA', empty cells, non-numeric p-values) will cause parsing or scaling to fail silently or produce misleading visualizations.

## Evidence

- [other] GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2: "GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2"
- [other] Parse and validate GO term identifiers, p-values (or adjusted p-values), gene ratios, and gene count columns: "Parse and validate GO term identifiers, p-values (or adjusted p-values), gene ratios, and gene count columns."
- [other] For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble color scaled by the selected metric: "For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble"
- [other] Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles: "Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles."
- [readme] go_term_bubble.csv for go dotplot style 1: "go_term_bubble.csv for go dotplot style 1"
