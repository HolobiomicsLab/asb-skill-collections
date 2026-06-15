---
name: microarray-expression-normalization-log-quantile
description: Use when when you have raw or minimally processed microarray expression data (e.g., from GEO) with intensity values that exhibit sample-to-sample distributional differences and variance heterogeneity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3170
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
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

# microarray-expression-normalization-log-quantile

## Summary

Apply log2 transformation followed by quantile normalization to microarray expression matrices to remove technical artifacts and improve comparability across samples. This two-step normalization stabilizes variance and aligns intensity distributions, a prerequisite for downstream pathway enrichment and dimensionality reduction analyses.

## When to use

When you have raw or minimally processed microarray expression data (e.g., from GEO) with intensity values that exhibit sample-to-sample distributional differences and variance heterogeneity. Apply this skill before filtering, PCA, or gene set enrichment analysis to ensure that downstream statistical comparisons reflect biological signal rather than technical batch effects.

## When NOT to use

- Input is RNA-seq count data; use alternative normalizations (e.g., TMM, DESeq2 VST, SCTransform) designed for discrete count distributions.
- Data is already log-normalized or pre-normalized by the array manufacturer with documented normalization pipeline; check data source and documentation before re-normalizing.
- Expression matrix has already undergone quantile normalization; applying a second round may remove biological signal.

## Inputs

- raw microarray expression matrix (numeric, genes × samples)
- expression object with intensity values (e.g., ExpressionSet from Bioconductor)

## Outputs

- log2-transformed, quantile-normalized expression matrix (numeric, genes × samples)
- normalized ExpressionSet object (if input was an ExpressionSet)

## How to apply

First, apply log2 transformation to the raw or background-corrected intensity matrix to stabilize variance across the intensity range and linearize fold-changes. Then apply quantile normalization using limma::normalizeBetweenArrays() with method='quantile' to force all samples to share an identical empirical intensity distribution. This ensures that each quantile (percentile) of the intensity values across genes is the same in every sample, removing systematic biases while preserving gene-level rank order and relative expression differences. Use the normalized log2-scale matrix for all subsequent analyses (filtering, normalization checks, dimensionality reduction).

## Related tools

- **limma** (Provides normalizeBetweenArrays() function for quantile normalization of microarray expression matrices) — https://bioconductor.org/packages/release/bioc/html/limma.html
- **R** (Language and runtime for executing normalization workflow)

## Examples

```
exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")
```

## Evaluation signals

- Verify log2 transformation: all intensity values should be non-negative and on logarithmic scale (original intensities ~1–65536 map to log2 values ~0–16).
- Check quantile normalization: compute summary statistics (min, median, max) for each sample across genes — all samples should have identical quantiles after normalization.
- Visual inspection: MA-plots or box-plots of log-intensities should show aligned median and similar spread across all samples post-normalization.
- Correlation structure: pairwise Pearson correlation of log2-normalized values between biological replicates should be ≥0.95, indicating successful normalization without loss of biological signal.
- Downstream stability: pathway enrichment p-values (e.g., from fgsea/geseca) computed on the normalized matrix should be reproducible across subsets of top genes (e.g., Pearson correlation of log10 p-values ≥0.95 when comparing full vs. filtered gene sets).

## Limitations

- Quantile normalization assumes that global intensity distributions should be identical; it may obscure real biological differences in overall expression levels between conditions if such differences are expected a priori.
- Log transformation of zero or near-zero intensities can produce undefined or extreme values; preprocessing should include background correction or pseudocount addition before log2 transformation.
- Quantile normalization is sensitive to the presence of extreme outlier samples; outlier detection and removal or robust normalization variants may be needed if array quality is variable.
- The choice of log base (log2 vs. natural log) affects interpretation of fold-changes; log2 is conventional in genomics to report fold-changes in powers of 2, but choice should be consistent with downstream analysis tools.

## Evidence

- [methods] Apply log2 and quantile normalization using limma::normalizeBetweenArrays: "apply log2 and quantile normalization using limma::normalizeBetweenArrays"
- [methods] Quantile normalization details in article workflow: "exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")"
- [other] Purpose of normalization in preprocessing pipeline: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
