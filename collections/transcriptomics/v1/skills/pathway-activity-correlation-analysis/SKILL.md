---
name: pathway-activity-correlation-analysis
description: Use when when you have run gene set enrichment analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3295
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - geseca
  - base::prcomp
  - limma::normalizeBetweenArrays
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- library(GEOquery)
- exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fgsea
    doi: 10.1101/060012
    title: fgsea
  dedup_kept_from: coll_fgsea
schema_version: 0.2.0
---

# pathway-activity-correlation-analysis

## Summary

Compare pathway enrichment results (scores and p-values) across different input dimensionalities or analytical approaches to assess the robustness and reproducibility of pathway activity inference. This skill validates whether dimensionality reduction or methodological variations preserve the biological signal captured by gene set enrichment methods.

## When to use

When you have run gene set enrichment analysis (e.g., geseca or fgsea) on the same biological samples under two different conditions—such as full-dimensional versus PCA-reduced expression matrices, or different normalization schemes—and need to quantify whether the pathway rankings and significance estimates remain consistent. Use this skill to verify that dimensionality reduction (e.g., to 10 PCs) does not introduce spurious pathway rankings or lose critical biological signal.

## When NOT to use

- Input is a single enrichment result without a paired comparison matrix—this skill requires at least two independent pathway enrichment runs to compute correlation.
- Gene sets have not been filtered to a consistent size range (minSize, maxSize) across both runs—inconsistent filtering invalidates the p-value comparison.
- The enrichment method does not report p-values or uses non-comparable statistical frameworks across the two conditions (e.g., one method reports adjusted p-values only).

## Inputs

- full-dimensional expression matrix (log2-normalized, quantile-normalized)
- PCA-reduced expression matrix (10 principal components extracted via prcomp)
- gene set collection (minSize=15, maxSize=500)
- geseca or fgsea result tables with pathway names, scores, and p-values

## Outputs

- scatter plot of log10(pval) full vs. reduced (ggplot2 object)
- Pearson correlation coefficient of log10-transformed p-values
- validation report confirming correlation ≥0.95 or documenting discrepancies

## How to apply

Run geseca() or fgsea() independently on both input matrices (e.g., full-dimensional and PCA-reduced expression data) with identical parameters (minSize=15, maxSize=500, center=FALSE). Extract pathway p-values from both results, log10-transform them to handle the wide range of magnitudes, and compute the Pearson correlation coefficient between the two p-value distributions. Plot log10(pval) from the full matrix on the x-axis versus log10(pval) from the reduced matrix on the y-axis using ggplot2, and inspect for linearity and scatter. A Pearson correlation of ≥0.95 indicates negligible information loss and validates that the dimensionality reduction preserves pathway enrichment rankings. This approach leverages the adaptive multi-level split Monte-Carlo scheme in fgsea to ensure accurate p-value estimation at both dimensionalities.

## Related tools

- **fgsea** (Fast preranked GSEA for pathway enrichment; computes p-values via adaptive multi-level split Monte-Carlo scheme to enable accurate comparison across dimensionalities) — https://github.com/ctlab/fgsea
- **geseca** (Gene Set Expression Class Analysis; alternative enrichment method that can be run on both full and reduced expression matrices with identical parameters) — https://github.com/ctlab/fgsea
- **ggplot2** (Visualization of log10(pval) scatter plots to assess correlation between enrichment results visually)
- **base::prcomp** (Standard PCA implementation (center=FALSE) to generate dimensionality-reduced expression matrix for comparison)
- **limma::normalizeBetweenArrays** (Quantile normalization applied to log2-transformed expression matrix prior to PCA)
- **data.table** (Efficient manipulation and comparison of pathway result tables)

## Examples

```
fgseaRes_full <- fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500); fgseaRes_reduced <- fgsea(pathways = examplePathways, stats = exampleRanks_pca10, minSize = 15, maxSize = 500); cor_test <- cor.test(log10(fgseaRes_full$pval), log10(fgseaRes_reduced$pval), method = 'pearson')
```

## Evaluation signals

- Pearson correlation of log10(pval) between full and reduced matrices ≥0.95, indicating negligible information loss
- Scatter plot of log10(pval) from full vs. reduced shows linear trend with R² ≥0.90, confirming consistent pathway rankings
- Top-ranked pathways (e.g., top 10 by p-value) remain in the same rank order or with minimal rank shift (<5 positions) between full and reduced results
- No pathway changes sign in effect size (ES) or normalized enrichment score (NES) between the two conditions, indicating no reversal of biological direction
- Comparison statistics (correlation, R², residual distribution) are computed and reported explicitly in methods/results

## Limitations

- Correlation-based validation assumes that p-value rank preservation is sufficient; it does not guarantee that absolute effect sizes or biological interpretation remain valid under aggressive dimensionality reduction.
- The ≥0.95 correlation threshold is arbitrary and may require adjustment depending on the biological system, sample size, or gene set collection; no adaptive threshold selection is provided in the article.
- PCA assumes linear relationships; nonlinear dimensionality reduction methods (e.g., t-SNE, UMAP) may show different correlation patterns and are not addressed in the task or article.
- The skill requires that both geseca/fgsea runs use identical parameters (minSize, maxSize, center, etc.); parameter drift between runs will confound the comparison.
- fgsea's default lower bound for p-value estimation (eps=1e-10) may limit the precision of extremely low p-values; setting eps=0 increases computation time but improves granularity for comparison.

## Evidence

- [other] Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?: "Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250"
- [other] fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities.: "fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities."
- [other] Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2.: "Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2."
- [other] confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction.: "confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction."
- [readme] This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
- [readme] gesecaRes <- geseca(exampleExpressionMatrix, examplePathways, minSize = 15, maxSize = 500): "gesecaRes <- geseca(exampleExpressionMatrix, examplePathways, minSize = 15, maxSize = 500)"
