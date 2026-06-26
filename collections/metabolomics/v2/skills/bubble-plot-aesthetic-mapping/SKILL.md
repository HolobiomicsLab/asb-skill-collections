---
name: bubble-plot-aesthetic-mapping
description: Use when you have parsed GO enrichment results (GO term identifiers,
  p-values or adjusted p-values, gene ratios, gene counts) into CSV format and need
  to render them as interactive bubble plots.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0091
  tools:
  - R Shiny
  - ggplot2
  - plotly
  - GraphBio
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

# bubble-plot-aesthetic-mapping

## Summary

Map quantitative GO enrichment metrics (p-values, gene ratios, gene counts) to distinct aesthetic dimensions (position, size, color) to create comparable bubble visualizations. This skill is essential when comparing two or more bubble plot styles that encode the same biological information via different visual encodings.

## When to use

You have parsed GO enrichment results (GO term identifiers, p-values or adjusted p-values, gene ratios, gene counts) into CSV format and need to render them as interactive bubble plots. Use this skill specifically when the same enrichment dataset must be visualized in two distinct styles (e.g., style 1 vs. style 2) to explore how different aesthetic mappings (axis assignments, color gradients, bubble sizing strategies) affect interpretation or to compare alternative GraphBio rendering modes.

## When NOT to use

- Input CSV does not contain GO term identifiers, p-values, gene ratios, or gene counts; data validation must succeed first.
- Goal is to generate a single, canonical GO visualization rather than compare two distinct aesthetic styles.
- Data has already been rendered as a static image or non-interactive format; re-rendering may be unnecessary.

## Inputs

- go_term_bubble.csv (GO dotplot style 1 demo file)
- go_bubble_example.csv (GO dotplot style 2 demo file)
- CSV columns: GO term identifiers, p-values or adjusted p-values, gene ratios, gene counts

## Outputs

- Interactive ggplot2 or plotly bubble plot (style 1)
- Interactive ggplot2 or plotly bubble plot (style 2)
- PNG raster export of style 1 and style 2 visualizations
- Optional interactive HTML export of both styles

## How to apply

Load the GO enrichment CSV file (go_term_bubble.csv for style 1 or go_bubble_example.csv for style 2) as an R data frame and validate that required columns are present: GO term identifiers, p-values (or -log10(p-value) or adjusted p-values), gene ratios, and gene counts. For style 1, assign GO terms to the y-axis, log p-value or enrichment score to the x-axis, gene count to bubble size, and a selected metric (e.g., p-value or enrichment score) to bubble color using a continuous color scale. For style 2, apply alternative aesthetic mappings as specified in the demo data (e.g., different axis assignments or color gradients). Render both styles as interactive ggplot2 or plotly visualizations, ensuring that legends, axis labels, and titles are present and semantically clear. Export both figures as PNG and optionally as interactive HTML to enable side-by-side comparison.

## Related tools

- **R Shiny** (Interactive web framework for rendering and comparing bubble plot styles with reactive aesthetic mapping controls) — github.com/databio2022/GraphBio
- **ggplot2** (R package for static and layered bubble plot construction with customizable aesthetic mappings (position, size, color))
- **plotly** (R library for interactive bubble plot rendering with hover tooltips, legends, and export to HTML)
- **GraphBio** (Complete R Shiny dashboard providing GO dotplot module with pre-configured style 1 and style 2 bubble visualization modes) — github.com/databio2022/GraphBio

## Evaluation signals

- Both bubble plots render without error and display all GO terms present in the input CSV.
- Aesthetic mappings are applied correctly: style 1 has GO terms on y-axis and log p-value on x-axis with bubble size proportional to gene count; style 2 has alternative mappings as specified in demo data.
- Color gradients are continuous and correctly scaled to the selected metric (e.g., p-value or enrichment score); legend is present and labeled.
- PNG and HTML exports are generated successfully and are visually identical to on-screen renderings.
- Axis labels and plot titles are semantically clear and match GO enrichment terminology; no missing or truncated labels.

## Limitations

- CSV input files must be well-formed and contain exactly the required columns; missing or malformed columns will cause parsing errors.
- Interactive HTML exports may be large or slow to load if the GO enrichment result contains >500 terms; performance has not been quantified in the paper.
- Color gradient perception and bubble overlap may reduce readability when many GO terms are plotted; manual filtering or subsetting of GO terms may be necessary.
- The paper does not specify the exact R versions, ggplot2 versions, or plotly versions required; compatibility with older or newer R ecosystems is unknown.

## Evidence

- [other] GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2, enabling generation of GO term bubble visualizations in two distinct formats.: "GraphBio's GO dotplot component accepts two separate CSV input files: go_term_bubble.csv for style 1 and go_bubble_example.csv for style 2"
- [other] For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble color scaled by the selected metric.: "For bubble style 1: create a dotplot with GO terms on the y-axis, a quantitative measure (e.g., log p-value or enrichment score) on the x-axis, bubble size proportional to gene count, and bubble"
- [other] For bubble style 2: create a dotplot variant with alternative aesthetic mappings (e.g., different axis assignments or color gradients) as specified in the demo data.: "For bubble style 2: create a dotplot variant with alternative aesthetic mappings (e.g., different axis assignments or color gradients) as specified in the demo data"
- [other] Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles.: "Render both styles as interactive ggplot2 or plotly visualizations with legend, axis labels, and titles"
- [readme] go_bubble_example.csv for go dotplot style 2 and go_term_bubble.csv for go dotplot style 1: "go_bubble_example.csv for go dotplot style 2
8. go_term_bubble.csv for go dotplot style 1"
