---
name: heatmap-clustering-and-visualization
description: Use when you have a gene expression matrix (samples × genes, with numeric values) and corresponding sample group/phenotype labels, and you need to identify co-expression patterns, sample clustering, or condition-specific expression trends.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0203
  tools:
  - R Shiny
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

# heatmap-clustering-and-visualization

## Summary

Generate an interactive heatmap visualization from omics expression matrices with hierarchical clustering and group annotations. This skill transforms raw gene expression data into a color-scaled, clustered heatmap suitable for exploratory analysis of expression patterns across samples and conditions.

## When to use

You have a gene expression matrix (samples × genes, with numeric values) and corresponding sample group/phenotype labels, and you need to identify co-expression patterns, sample clustering, or condition-specific expression trends. Use this skill when the goal is visual exploration and comparison of expression profiles across multiple samples or experimental groups.

## When NOT to use

- Input matrix is not numeric or contains missing values without imputation strategy.
- Sample count is very large (>1000 samples); heatmap becomes unreadable and interaction computationally expensive.
- Expression values are already log-transformed and z-scored with no biological interpretation needed — use simpler correlation heatmaps instead.

## Inputs

- Expression matrix CSV (genes × samples, numeric expression values)
- Group annotation CSV (sample identifiers and group/phenotype labels)

## Outputs

- Interactive clustered heatmap visualization (HTML/Shiny widget)
- Row dendrogram (gene clustering tree)
- Column dendrogram (sample clustering tree)
- Colored annotation sidebars (group metadata)

## How to apply

Load the expression matrix (CSV format with genes as rows, samples as columns) and group annotation file (CSV with sample IDs and group labels) into R. Validate that matrix dimensions match the group annotation sample count. Apply hierarchical clustering to both rows (genes) and columns (samples) using a distance metric (typically Euclidean) and linkage method. Scale expression values (typically z-score normalization per gene) to enable color intensity to represent deviation from mean. Render the clustered heatmap with row/column dendrogram, apply color gradient (e.g., blue–white–red for down–neutral–up), and overlay group annotations as colored sidebars or labels to contextualize clusters.

## Related tools

- **R Shiny** (Interactive web framework for rendering clustered heatmap with mouse-over tooltips, zoom, and group annotation display) — https://github.com/databio2022/GraphBio
- **GraphBio** (Omics visualization dashboard providing the heatmap module with pre-configured clustering, scaling, and annotation integration) — https://github.com/databio2022/GraphBio

## Evaluation signals

- Heatmap renders without errors; row and column dendrograms are present and reflect expected hierarchical relationships.
- Expression matrix dimensions match group annotation sample count (no unmatched samples).
- Clustered samples within the same group show visual co-localization in the dendrogram; inter-group samples show separation.
- Color scale is continuous and symmetric around the median (neutral color); no color bar truncation or saturation artifacts.
- Group annotation sidebars are correctly aligned with heatmap columns and display expected group labels and colors.

## Limitations

- Hierarchical clustering assumes Euclidean distance and complete/average linkage; alternative distance metrics (Manhattan, Pearson) or linkage methods may yield different sample/gene orderings.
- Z-score normalization per gene can mask global expression level differences; alternative scaling (CPM, TMM) may be more appropriate for RNA-seq count data.
- Large heatmaps (>10,000 genes) may be computationally slow and visually crowded; row filtering (e.g., top-variance genes) is often necessary for interpretability.
- Missing or low-quality samples can distort clustering topology; no built-in quality control or outlier detection is mentioned in the module documentation.

## Evidence

- [other] The heatmap component consumes two CSV files: heatmap_test.csv (expression matrix) and group_info.csv (group annotations) to produce the heatmap visualization.: "heatmap_test.csv (expression matrix) and group_info.csv (group annotations) to produce the heatmap visualization"
- [other] Generate a heatmap visualization using R Shiny's rendering capabilities, applying row and column clustering and color scaling to represent expression values.: "Generate a heatmap visualization using R Shiny's rendering capabilities, applying row and column clustering and color scaling"
- [other] Integrate group annotation metadata as heatmap annotations (e.g., colored sidebars or labels).: "Integrate group annotation metadata as heatmap annotations (e.g., colored sidebars or labels)"
- [readme] GraphBio: a shiny web app to easily perform popular visualization analysis for omics data: "GraphBio: a shiny web app to easily perform popular visualization analysis for omics data"
- [readme] heatmap_test.csv and group_info.csv for heatmap.: "heatmap_test.csv and group_info.csv for heatmap"
