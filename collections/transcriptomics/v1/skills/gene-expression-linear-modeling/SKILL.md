---
name: gene-expression-linear-modeling
description: Use when you have normalized or voom-transformed gene expression counts/intensities indexed by gene and sample, along with an experimental design matrix specifying condition, batch, or covariate assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
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

# gene-expression-linear-modeling

## Summary

Fit linear models to gene expression data (microarray, RNA-seq, or qPCR) to identify and quantify differential expression across experimental conditions. This skill applies least-squares regression with empirical Bayes moderation to stabilize variance estimates, enabling robust statistical inference even with small sample sizes.

## When to use

You have normalized or voom-transformed gene expression counts/intensities indexed by gene and sample, along with an experimental design matrix specifying condition, batch, or covariate assignments. Use this skill when you need to test for differential expression between groups, account for confounders, or quantify fold-changes with adjusted p-values.

## When NOT to use

- Expression data are not yet normalized or variance-stabilized (apply normalization or voom transformation first).
- Sample size is extremely small (n < 3 per group) and biological replication is absent; empirical Bayes cannot robustly estimate variance trends.
- You are analyzing single-cell RNA-seq where cell-level sparsity and zero-inflation dominate; consider zero-inflated or mixed-effects alternatives.

## Inputs

- Expression matrix (genes × samples): log2-normalized intensities (microarray) or voom-transformed counts (RNA-seq)
- Design matrix (samples × covariates): numeric or factor columns encoding condition, batch, or other variables
- Gene annotations (optional): gene names, symbols, or IDs for reporting

## Outputs

- Linear model fit object: per-gene coefficients, standard errors, and residuals
- Moderated t-statistics and adjusted p-values (FDR) for each contrast of interest
- Ranked table of differentially expressed genes: gene ID, log-fold-change, t-statistic, p-value, adjusted p-value

## How to apply

Construct a design matrix encoding the experimental variables (e.g., condition, batch) as numeric or factor columns. Fit a linear model via lmFit to the expression matrix using this design matrix, producing per-gene coefficient estimates and residuals. Apply empirical Bayes moderation (eBayes) to shrink per-gene variance estimates toward a global trend, which stabilizes t-statistics and p-values especially when sample size is small. Extract ranked lists of differentially expressed genes using topTable, filtering by adjusted p-value threshold (e.g., FDR < 0.05) and optionally log-fold-change magnitude. Compare results across nested or alternative model formulae to validate robustness.

## Related tools

- **limma** (Core package for linear model fitting, empirical Bayes moderation (eBayes), and differential expression testing via lmFit and topTable) — https://github.com/bioc/limma
- **voom** (Variance-stabilization transformation for RNA-seq read counts; computes precision weights accounting for mean-variance relationship prior to lmFit) — https://github.com/bioc/limma
- **edgeR** (Companion package providing calcNormFactors for normalization (TMM, RLE, etc.) and DGEList object creation; normalization factors are passed to voom)
- **R** (Programming environment for model fitting and statistical computation)

## Examples

```
library(limma); fit <- lmFit(expr_matrix, design); fit <- eBayes(fit); top_genes <- topTable(fit, adjust.method='BH', p.value=0.05, number=Inf)
```

## Evaluation signals

- Model diagnostics: residuals are approximately normal and homoscedastic; no systematic patterns in residual vs. fitted plots.
- Empirical Bayes moderation has shrunk variance estimates downward relative to unmoderated estimates; prior degrees of freedom (df.prior) > 0.
- Ranked gene list is reproducible and robust: top differentially expressed genes remain stable across subsamples or alternative model formulae.
- Adjusted p-value distribution is well-calibrated: histogram of p-values is approximately uniform under null, with peak near 0 for true signals.
- Log-fold-change estimates are consistent in magnitude and direction when comparing alternative normalization or design specifications.

## Limitations

- Empirical Bayes variance moderation assumes a shared variance trend across genes; genes with extreme or bimodal variance distributions may be misjudged.
- Linear model assumes additive effects and homogeneous error variance; violations (e.g., gene-by-batch interactions, outliers) can bias inference.
- Requires specification of design matrix a priori; post-hoc model selection (e.g., stepwise variable inclusion) inflates false-discovery rate.
- Not designed for single-cell RNA-seq data in their raw form; sparsity and zero-inflation violate homoscedasticity assumption.

## Evidence

- [other] Empirical Bayesian methods are used to provide stable results even when the number of arrays is small.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] Linear models apply across microarrays, qPCR, RNA-seq, and proteomics technologies.: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Limma provides linear model analysis for differential expression.: "the use of linear models for analysing designed experiments and the assessment of differential expression"
- [other] voom transformation computes precision weights for RNA-seq data.: "Extract the TMM-normalized library sizes and pass them to voom along with the design matrix to compute precision weights accounting for mean-variance relationship."
- [other] Empirical Bayes moderation stabilizes variance across genes.: "Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes."
