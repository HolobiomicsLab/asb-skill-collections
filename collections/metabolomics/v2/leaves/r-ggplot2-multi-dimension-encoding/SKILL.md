---
name: r-ggplot2-multi-dimension-encoding
description: Use when when you have tabular GO enrichment or gene set analysis results
  with at least 3–4 quantitative or categorical dimensions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0006
  edam_topics:
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3678
  tools:
  - R Shiny
  - ggplot2
  - plotly
  - Docker
  license_tier: open
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

# r-ggplot2-multi-dimension-encoding

## Summary

Encode multiple biological dimensions (GO terms, p-values, gene counts, enrichment metrics) into a single ggplot2 dotplot by mapping variables to position (x, y axes), size (bubble diameter), and color (gradient scale), enabling compact simultaneous visualization of enrichment patterns across all dimensions.

## When to use

When you have tabular GO enrichment or gene set analysis results with at least 3–4 quantitative or categorical dimensions (e.g., GO term names, adjusted p-values or enrichment scores, gene counts or gene ratios, and an optional grouping or color metric) and need to visualize relationships and trade-offs across all dimensions in a single plot rather than using separate univariate plots.

## When NOT to use

- Input contains fewer than 3 quantitative dimensions; use a simpler plot type (scatter, bar, or line plot).
- GO term count exceeds 50–80 terms; the y-axis becomes overcrowded; consider faceting, filtering to top-N terms, or an interactive table instead.
- Data are not pre-aggregated by GO term; you still need to perform enrichment analysis upstream before applying this skill.

## Inputs

- CSV file with GO term identifiers (character column)
- CSV file with p-value or adjusted p-value column (numeric)
- CSV file with gene count or gene ratio column (numeric)
- CSV file with enrichment score or other quantitative metric (numeric)
- Optional: grouping or categorical metadata column

## Outputs

- ggplot2 or plotly interactive dotplot object
- PNG raster image file of GO dotplot
- Optional: interactive HTML widget file

## How to apply

Load a CSV file (e.g., go_term_bubble.csv or go_bubble_example.csv) containing GO term identifiers, p-values (or adjusted p-values), gene ratios, and gene counts into R as a data frame. Parse and validate all columns. Construct a ggplot2 call that assigns GO terms to the y-axis, a quantitative measure (e.g., log p-value or enrichment score) to the x-axis, gene count or another metric to bubble size (geom_point with size aesthetic), and a color metric (e.g., log adjusted p-value or gene ratio) to the bubble fill color (scale_color_gradient or similar). Add axis labels, a legend, and a title. Render as an interactive ggplot2 or plotly object and export to PNG or HTML. The key design rationale is that by encoding 4+ dimensions into position, size, and color, you compress what would normally require multiple plots into one coherent view, making enrichment patterns and magnitudes immediately comparable.

## Related tools

- **R Shiny** (Interactive web framework that hosts and renders the multi-dimensional dotplot with real-time aesthetic parameter adjustment and user-driven data subset filtering) — github.com/databio2022/GraphBio
- **ggplot2** (R graphics package that constructs the layered dotplot by mapping data columns to position, size, and color aesthetics and applying geom_point with gradient scales)
- **plotly** (Interactive visualization library (R wrapper) that converts ggplot2 dotplot to an interactive HTML widget with hover tooltips and zoom/pan capabilities)
- **Docker** (Containerization platform used to deploy GraphBio application with all R and ggplot2 dependencies pre-installed) — databio2022/GraphBio

## Evaluation signals

- All GO terms appear on the y-axis with no label overlap or truncation.
- X-axis displays the quantitative measure (e.g., log p-value or enrichment score) with a linear or log scale and labeled tick marks.
- Bubble size is proportional to gene count or gene ratio; verify by checking that larger gene counts produce visually larger bubbles.
- Bubble color gradient is continuous and aligned to a color scale legend that maps numeric values (e.g., 0–5 for log p-values) to a perceptually distinct color ramp (e.g., blue to red).
- Interactive plotly version shows GO term ID, p-value, gene count, and other metrics in a tooltip on mouse hover; no NA or missing values are rendered as visual artifacts (e.g., grayed-out bubbles).

## Limitations

- Plotting more than 50–80 GO terms results in y-axis crowding and poor readability; the skill assumes the user pre-filters to top-N significant terms.
- Bubble overlap occurs when GO terms cluster in similar p-value and enrichment score ranges; transparency or jitter may mitigate but are not described in the article.
- Color and size encodings can lead to visual redundancy or misinterpretation if the metrics are highly correlated; the article does not discuss trade-offs or perceptual validation of the encoding.
- Export quality depends on the output format (PNG DPI, HTML rendering engine); low-resolution PNG exports may lose fine details in bubble positioning or color gradation.

## Evidence

- [other] GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2, enabling generation of GO term bubble visualizations in two distinct formats.: "GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2, enabling generation of GO term bubble visualizations in two"
- [other] For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble color scaled by the selected metric.: "For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble"
- [other] Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles.: "Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles."
- [readme] GraphBio---A modular and scalable R Shiny dashboard: "GraphBio---A modular and scalable R Shiny dashboard"
- [readme] go_term_bubble.csv for go dotplot style 1: "go_term_bubble.csv for go dotplot style 1"
