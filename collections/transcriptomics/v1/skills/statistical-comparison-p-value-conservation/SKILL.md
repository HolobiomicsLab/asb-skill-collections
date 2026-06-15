---
name: statistical-comparison-p-value-conservation
description: Use when you have run the same pathway enrichment analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3518
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - data.table
  - prcomp (base R)
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

# statistical-comparison-p-value-conservation

## Summary

Validate that dimensionality reduction or alternative analytical pipelines preserve the statistical significance (p-values) of pathway enrichment results by computing correlation of log10-transformed p-values between two analytical approaches. This skill is critical for assessing whether faster or lower-dimensional methods sacrifice statistical fidelity.

## When to use

Apply this skill when you have run the same pathway enrichment analysis (e.g., geseca or fgsea) on two different input matrices—such as a full-dimensional expression matrix and a PCA-reduced matrix, or two different normalization pipelines—and need to verify that dimensionality reduction or computational optimization does not degrade the significance of pathway discovery. Use it to justify methodological shortcuts before deploying them in downstream analyses.

## When NOT to use

- The two input matrices were created using fundamentally different experimental protocols or sample cohorts—comparison is only valid for the same biological samples analyzed under different computational transformations.
- The two analyses used different gene set collections, parameter thresholds (minSize, maxSize), or enrichment algorithms—the p-value comparison becomes confounded by these methodological differences.
- You are comparing p-values from different statistical tests (e.g., fgsea vs. hypergeometric test) rather than the same enrichment method applied to different inputs.

## Inputs

- full-dimensional gene expression matrix (normalized and filtered)
- reduced-dimensional matrix (e.g., PCA-projected or SCT-normalized)
- gene set collection (e.g., from msigdbr or loaded pathways)
- identical geseca or fgsea parameter set (minSize, maxSize, center)

## Outputs

- pathway enrichment results from full-dimensional matrix (pathway scores, p-values)
- pathway enrichment results from reduced-dimensional matrix (pathway scores, p-values)
- log10-transformed p-value pairs
- Pearson correlation coefficient of log10 p-values
- scatter plot comparing log10(pval_full) vs log10(pval_reduced)
- boolean validation flag (correlation ≥ threshold)

## How to apply

Run pathway enrichment analysis (geseca or fgsea) on both the reference (full-dimensional) and candidate (reduced or alternative) input matrices using identical parameters (e.g., minSize=15, maxSize=500). Extract pathway p-values from both results. Log10-transform both p-value sets to linearize the relationship across the wide dynamic range typical of GSEA outputs. Compute Pearson correlation of the log10-transformed p-values and visualize the agreement using a scatter plot (log10(pval_full) vs. log10(pval_reduced)). Set a minimum correlation threshold (typically ≥0.95) as the criterion for acceptable conservation; correlations above this threshold indicate negligible information loss, while lower correlations suggest the reduction may alter pathway rankings or significance.

## Related tools

- **fgsea** (Fast preranked gene set enrichment analysis to compute pathway p-values and scores for comparison) — https://github.com/ctlab/fgsea
- **ggplot2** (Visualization of log10 p-value scatter plots to assess correlation visually)
- **data.table** (Efficient handling and merging of enrichment result tables for paired p-value extraction)
- **limma** (Normalization of expression matrices prior to dimensionality reduction)
- **prcomp (base R)** (Principal component analysis to generate reduced-dimensional matrix for comparison)

## Examples

```
fgseaRes_full <- fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500); fgseaRes_reduced <- fgsea(pathways = examplePathways, stats = exampleRanks_pca, minSize = 15, maxSize = 500); cor(log10(fgseaRes_full$pval), log10(fgseaRes_reduced$pval), use='complete.obs')
```

## Evaluation signals

- Pearson correlation of log10-transformed p-values between full and reduced matrices is ≥0.95, indicating negligible information loss from dimensionality reduction.
- Scatter plot of log10(pval_full) vs. log10(pval_reduced) shows tight linear agreement with minimal vertical scatter around the diagonal.
- Rank order of top pathway hits (by p-value) remains largely concordant between the two approaches; pathways significant in the full matrix remain significant in the reduced matrix.
- The slope and intercept of the linear regression through log10 p-value pairs are close to 1 and 0 respectively, indicating no systematic bias in p-value magnitude between approaches.
- No pathways exhibit a flip in direction of enrichment (e.g., positive NES in full matrix becoming negative in reduced matrix) that would indicate loss of biological signal.

## Limitations

- The comparison assumes both runs use identical enrichment parameters and the same gene set collection; differences in parameters or databases will confound the p-value correlation.
- P-value conservation does not guarantee biological interpretation is unchanged; correlation of high p-values (non-significant pathways) may be spurious due to floor effects in very low p-value estimation.
- Extremely small sample sizes or very sparse gene sets may violate the assumptions of GSEA, rendering the p-value comparison unreliable regardless of correlation.
- The adaptive multi-level split Monte-Carlo scheme used by fgsea introduces stochasticity; repeated runs may yield slightly different p-values, especially at very low thresholds (eps=0), so reproducibility requires fixing random seeds.

## Evidence

- [other] fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities.: "fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities."
- [other] Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?: "Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250"
- [other] Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2.: "Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2."
- [other] confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction.: "confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction."
- [readme] This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
