---
name: multiple-testing-correction-and-p-value-adjustment
description: Use when when you have generated raw p-values from differential expression analysis on preprocessed count matrices (mRNA, miRNA, isoforms, lipids, or proteins) using edgeR, DESeq2, or RankProduct and need to identify statistically significant features while controlling familywise error rate or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - RankProduct
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-testing-correction-and-p-value-adjustment

## Summary

Adjust raw p-values from differential expression analysis to control for multiple testing across thousands of genomic features, producing adjusted p-values that balance false discovery rate control with statistical power. This skill is essential when interpreting results from edgeR, DESeq2, or RankProduct to identify truly significant features amid multiple hypothesis tests.

## When to use

When you have generated raw p-values from differential expression analysis on preprocessed count matrices (mRNA, miRNA, isoforms, lipids, or proteins) using edgeR, DESeq2, or RankProduct and need to identify statistically significant features while controlling familywise error rate or false discovery rate across all tested features.

## When NOT to use

- The input is already a filtered feature list with pre-selected significant features and no raw p-value column is available for re-correction.
- Single-feature hypothesis testing (no multiple testing problem exists); raw p-values are already interpretable.
- The DE analysis was conducted outside the multiOmicsIntegrator pipeline and correction methodology is incompatible with downstream integration steps.

## Inputs

- Results table from differential expression analysis (edgeR, DESeq2, or RankProduct)
- Raw p-values column from DE results
- Test statistics (t-statistic or log-likelihood ratio)
- Feature identifiers (gene/miRNA/protein IDs)

## Outputs

- Adjusted p-values column added to DE results table
- Volcano plot (log2 fold-change vs. -log10 adjusted p-value)
- P-value distribution plots (histogram of raw and adjusted p-values)
- Filtered feature list meeting adjusted p-value threshold (typically p_adj < 0.05)
- Hierarchically organized output directory by omics type (e.g., /output_directory/genes/)

## How to apply

After executing the selected differential expression algorithm (edgeR, DESeq2, or RankProduct) and obtaining a results table with raw p-values for each feature, apply multiple-testing correction within the R environment using standard methods (e.g., Benjamini-Hochberg for FDR control or Bonferroni for FWER control). The corrected p-values are included in the final differential expression results table alongside fold-changes, test statistics, and raw p-values. The choice of correction method depends on the analysis goal: use Benjamini-Hochberg (FDR) for discovery-oriented studies where some false positives are acceptable, or Bonferroni for confirmatory analyses requiring stricter control. Generate diagnostic plots (volcano plots, p-value distributions) that visualize the distribution of adjusted p-values and highlight features crossing the significance threshold (typically adjusted p < 0.05).

## Related tools

- **edgeR** (Generates raw p-values for differential expression that require adjustment)
- **DESeq2** (Generates raw p-values for differential expression that require adjustment)
- **RankProduct** (Generates raw p-values for differential expression that require adjustment)
- **ggplot2** (Creates volcano plots and p-value distribution plots to visualize adjusted p-value results)
- **ComplexHeatmap** (Generates diagnostic heatmap visualizations of significant features post-correction)

## Evaluation signals

- Adjusted p-values are monotonically non-decreasing relative to raw p-values (no adjusted p-value is smaller than its corresponding raw p-value).
- All adjusted p-values fall within the valid range [0, 1] with no missing or infinite values.
- Volcano plot shows clear separation between significant (adjusted p < 0.05) and non-significant features, with clustering visible at the significance threshold.
- P-value distribution histogram demonstrates expected behavior: uniform distribution for raw p-values under null, concentrated at 1.0 for adjusted p-values of true negatives.
- Number of significant features (adjusted p < 0.05) is substantially lower than the count passing raw p-value threshold, confirming correction is applied.

## Limitations

- Multiple-testing correction reduces statistical power; fewer features are declared significant compared to unadjusted analysis, which may mask real weak signals.
- Method choice (FDR vs. FWER vs. other) is not explicitly specified in the multiOmicsIntegrator task description; default implementation details are not provided, requiring verification against the underlying R package documentation.
- Correction assumes independence of tests, which may be violated in genomic datasets where features share regulatory mechanisms or are in linkage disequilibrium.
- Extremely stringent correction (e.g., Bonferroni with thousands of features) may result in zero significant features even when true effects exist, particularly with modest sample sizes or effect sizes.

## Evidence

- [methods] Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values.: "Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values."
- [methods] Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap.: "Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap."
- [other] Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
- [other] Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap: "Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
