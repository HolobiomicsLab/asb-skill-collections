---
name: differential-expression-empirical-bayes-moderation
description: Use when after fitting a linear model with lmFit on voom-transformed or log2-normalized RNA-seq or microarray expression matrices, apply eBayes moderation to moderate gene-wise variance estimates before extracting top differentially expressed genes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0769
  tools:
  - edgeR
  - limma
  - R
  - voom
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- calcNormFactors [TMM normalization]
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
- 'Voom: precision weights unlock linear model analysis tools for RNA-seq read counts'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_limmavoom
    doi: 10.1186/gb-2014-15-2-r29
    title: limmavoom
  dedup_kept_from: coll_limmavoom
schema_version: 0.2.0
---

# differential-expression-empirical-bayes-moderation

## Summary

Apply empirical Bayes moderation via eBayes to stabilize variance estimates across genes after fitting a linear model to normalized expression data. This shrinks per-gene variance estimates toward a common value, improving statistical power and ranking reliability especially when sample sizes are small.

## When to use

After fitting a linear model with lmFit on voom-transformed or log2-normalized RNA-seq or microarray expression matrices, apply eBayes moderation to moderate gene-wise variance estimates before extracting top differentially expressed genes. This is particularly important when the number of arrays or samples is small, as empirical Bayesian methods stabilize results in such settings.

## When NOT to use

- Input is unlogged, raw read counts without prior normalization or voom transformation; apply normalization and voom first.
- Sample size is very large (>50 arrays); empirical Bayes shrinkage provides minimal benefit and unmoderated estimates may suffice.
- You require gene-level variance estimates that reflect only the observed data without borrowing strength across genes.

## Inputs

- lmFit object (fitted linear model on normalized expression matrix)
- normalized expression matrix (voom-transformed, log2-CPM, or similar)

## Outputs

- eBayes-moderated lmFit object with stabilized variance estimates
- moderated t-statistics per gene
- log-fold-changes (from linear model coefficients)
- adjusted p-values (FDR-corrected)

## How to apply

Fit the linear model using lmFit with your design matrix on the normalized expression matrix (from voom, log2-CPM, or similar preprocessing). Pass the lmFit object directly to eBayes, which estimates a prior distribution on the variances and shrinks the observed per-gene variances toward a common variance estimate using a moderated t-statistic approach. Extract the moderated test statistics, log-fold-changes, and adjusted p-values (e.g., using topTable with FDR < 0.05 threshold) from the eBayes output. The empirical Bayes posterior variance estimates replace the unmoderated per-gene estimates, producing more stable and reliable gene rankings, particularly when sample replication is limited.

## Related tools

- **limma** (provides lmFit and eBayes functions for linear model fitting and empirical Bayes moderation of variance estimates) — https://bioconductor.org/packages/limma
- **voom** (precision-weighted normalization prior to lmFit; produces precision weights that account for mean-variance relationship in RNA-seq) — https://bioconductor.org/packages/limma
- **R** (execution environment for limma eBayes)

## Examples

```
fit <- lmFit(voom_matrix, design); fit <- eBayes(fit); topTable(fit, adjust.method='BH', p.value=0.05)
```

## Evaluation signals

- eBayes output contains moderated t-statistics and adjusted p-values; verify that t-statistics are less extreme (closer to zero) than unmoderated versions due to variance shrinkage.
- Ranked gene list from topTable shows improved stability: genes with small sample sizes or very small observed variances are deprioritized; ranking is less sensitive to outlier variance estimates.
- Compare gene rankings and log-fold-changes from eBayes pipeline vs. unmoderated lmFit results; adjusted p-values from eBayes should show fewer false positives and higher concordance with biological expectation when sample size is small.
- Inspect the prior variance estimate (stored in eBayes output as fit$s2.prior) and check that it lies within the range of observed gene-wise variances, confirming reasonable shrinkage.
- Verify FDR-adjusted p-value distribution is conservative (monotonic, no spurious clustering near zero).

## Limitations

- Empirical Bayes assumes a common prior variance distribution across genes; genes with distinctly different variance structures may be incorrectly shrunk.
- Performance depends critically on the number of samples: with very small sample counts (n < 5), the prior estimate itself may be unstable.
- eBayes assumes normality of the normalized expression scale (log2-CPM or voom-transformed); misspecification of the transformation can bias posterior estimates.
- Shrinkage reduces the magnitude of variance estimates, which may penalize highly variable genes even if the variation is genuine; trade-off is reduced false discovery rate at cost of statistical power for some truly differentially expressed genes.

## Evidence

- [other] Empirical Bayesian methods provide stable results even when the number of arrays is small: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] eBayes is applied after lmFit to moderate variance estimates for differential expression inference: "Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes."
- [other] Linear model framework applies across multiple gene expression technologies: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Empirical Bayes is used within a complete differential expression workflow: "Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix. Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes."
