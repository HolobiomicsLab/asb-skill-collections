---
name: gene-level-volcano-and-ma-plot-generation
description: Use when after completing differential expression analysis (edgeR, DESeq2,
  or RankProduct) on count matrices to visualize fold-changes versus p-values and
  to assess the relationship between average expression levels and log2 fold-changes
  for gene-level omics data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3673
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger,
  limma, sva, ggplot2, ComplexHeatmap'
- 'R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gene-level-volcano-and-ma-plot-generation

## Summary

Generate diagnostic visualization plots (volcano and MA plots) from differential expression analysis results to assess the magnitude and statistical significance of gene expression changes across experimental conditions. These plots enable rapid visual identification of significantly differentially expressed genes and quality assessment of the differential expression analysis.

## When to use

After completing differential expression analysis (edgeR, DESeq2, or RankProduct) on count matrices to visualize fold-changes versus p-values and to assess the relationship between average expression levels and log2 fold-changes for gene-level omics data.

## When NOT to use

- When differential expression analysis has not yet been performed or results table is incomplete
- When input is raw count matrices rather than processed differential expression results
- When working with non-gene omics features (e.g., raw spectra, unprocessed lipid signals) without prior statistical testing

## Inputs

- Differential expression results table (TSV/CSV) containing: feature identifiers, fold-changes, test statistics, raw p-values, adjusted p-values
- Sample metadata with experimental group assignments

## Outputs

- Volcano plot (PDF/PNG) with -log10(adjusted p-value) vs. log2(fold-change)
- MA plot (PDF/PNG) with average log2 expression (A-value) vs. log2(fold-change) (M-value)
- P-value distribution histogram (PDF/PNG)
- Organized output directory structure by omics type

## How to apply

Extract feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values from the differential expression results table. Use ggplot2 to construct volcano plots mapping -log10(adjusted p-value) on the y-axis against log2(fold-change) on the x-axis, highlighting genes exceeding user-defined significance thresholds (typically adjusted p < 0.05). Generate MA plots showing the relationship between average log2 expression (A-value, x-axis) and log2 fold-change (M-value, y-axis) using ggplot2. Optionally create p-value distribution histograms to assess the behavior of raw p-values across the feature set. Organize outputs hierarchically by omics type (e.g., /output_directory/genes/) and export plots in publication-ready formats.

## Related tools

- **ggplot2** (R package for constructing volcano and MA plot visualizations)
- **ComplexHeatmap** (R package for generating diagnostic heatmap and plot annotations)
- **DESeq2** (R package generating differential expression results (fold-changes, p-values) used as input)
- **edgeR** (R package generating differential expression results (fold-changes, p-values) used as input)
- **RankProd** (R package generating differential expression results (fold-changes, p-values) used as input)

## Evaluation signals

- Volcano plot displays non-random distribution of points with visible separation between significant (upper regions) and non-significant features
- MA plot shows expected MA-plot characteristics: symmetric M-value distribution around zero, no systematic bias relative to A-value
- P-value histogram exhibits expected distribution shape; uniform distribution under null hypothesis, enrichment near zero under alternative
- Output files exist in correct directory structure (/output_directory/genes/) with expected file naming conventions
- Plot axes are correctly labeled with appropriate transformations (-log10 for p-values, log2 for fold-changes) and significance threshold lines are visible

## Limitations

- Plot quality and interpretability depend on differential expression analysis quality; garbage input (poor sample grouping, batch effects) yields uninformative plots
- Visualization assumes adequate statistical power; very small sample sizes may produce sparse, difficult-to-interpret volcano plots regardless of method
- Threshold selection for 'significant' features (adjusted p-value cutoff, fold-change minimum) is user-dependent; no universal recommendation provided in multiOmicsIntegrator documentation

## Evidence

- [methods] Generate diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap.: "Generate diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap."
- [methods] Execute the selected algorithm (edgeR, DESeq2, or RankProduct via their R package implementations) using sample group assignments from the required samplesheet column. Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values.: "Execute the selected algorithm (edgeR, DESeq2, or RankProduct via their R package implementations) using sample group assignments from the required samplesheet column. Generate a results table"
- [methods] Write results to output directory organized hierarchically by omics type (e.g., /output_directory/genes/).: "Write results to output directory organized hierarchically by omics type (e.g., /output_directory/genes/)."
- [methods] The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'), with each algorithm (edgeR, DESeq2, RankProduct) requiring specific samplesheet column conventions: "The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'), with each algorithm"
