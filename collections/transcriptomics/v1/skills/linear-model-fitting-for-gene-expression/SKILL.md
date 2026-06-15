---
name: linear-model-fitting-for-gene-expression
description: Use when you have a normalized gene expression matrix (genes × samples) and an experimental design with known treatment groups or conditions, and you need to estimate the effect of those conditions on expression levels while accounting for sample-to-sample variability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0099
  tools:
  - limma
  - R
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
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

# linear-model-fitting-for-gene-expression

## Summary

Fit linear models to gene expression matrices using a design matrix encoding experimental groups or conditions, obtaining coefficient estimates and residual standard errors for downstream differential expression analysis. This skill applies to microarray, RNA-seq, qPCR, and proteomics data.

## When to use

You have a normalized gene expression matrix (genes × samples) and an experimental design with known treatment groups or conditions, and you need to estimate the effect of those conditions on expression levels while accounting for sample-to-sample variability. Apply this skill before computing moderated t-statistics or contrasts.

## When NOT to use

- Expression data are not yet normalized; apply normalization and background correction before lmFit.
- Design is unbalanced or confounded in ways that violate linear model assumptions; consider model diagnostics first.
- You have already computed per-gene statistics (e.g., from a separate pipeline); lmFit is redundant.

## Inputs

- gene expression matrix (genes × samples; numeric)
- design matrix (samples × covariates; numeric, typically with intercept)
- phenotype metadata or experimental group assignments

## Outputs

- MArrayLM object containing fitted coefficients, standard errors, residual degrees of freedom, and design matrix
- coefficient estimates (log-fold-change or effect sizes) for each gene and design column

## How to apply

Construct a design matrix that encodes the experimental groups or conditions of interest as columns (typically with an intercept column). Pass the expression matrix and design matrix to limma's lmFit function, which fits ordinary least squares regression for each gene independently. The function returns an MArrayLM object containing coefficient estimates, standard errors, and residual degrees of freedom for each gene. Verify that all contrast coefficients and standard errors have been computed by inspecting the returned object's structure before proceeding to empirical Bayes moderation (eBayes) or contrast-based analysis.

## Related tools

- **limma** (Core R package providing lmFit function for linear model fitting to gene expression matrices; also provides downstream empirical Bayes moderation (eBayes) and contrast analysis) — https://github.com/bioc/limma
- **R** (Programming environment in which limma and design matrix construction are executed)

## Examples

```
design <- model.matrix(~0 + factor(c('ctrl', 'ctrl', 'treat', 'treat'))); fit <- lmFit(expr_matrix, design)
```

## Evaluation signals

- MArrayLM object is returned with non-empty coefficients slot matching the number of design columns
- Residual standard error estimates are positive and finite for all genes
- Residual degrees of freedom equal (number of samples) − (number of design columns)
- Coefficients and standard errors show expected magnitude and sign relative to experimental design (e.g., treated samples have non-zero coefficients for treatment column)
- No NaN or Inf values in coefficients, standard errors, or degrees of freedom (indicates no rank-deficient or singular design)

## Limitations

- Linear model assumes that residuals are normally distributed and homoscedastic across samples; violations may inflate or deflate standard errors.
- When the number of arrays is small, empirical Bayes moderation (eBayes) is required to stabilize variance estimates; raw lmFit output alone is unstable.
- Design matrix must have full column rank; perfect collinearity or confounding of factors will produce singular matrices and NA coefficients.
- lmFit applies ordinary least squares; for small sample sizes or very sparse data, penalized or robust methods may be preferable.

## Evidence

- [other] lmFit produces MArrayLM object with coefficient estimates and residual standard errors: "Apply limma's lmFit function to fit a linear model to the expression matrix using the design matrix, obtaining coefficient estimates and residual standard errors."
- [other] limma applies to microarray, RNA-seq, qPCR, and proteomics: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Linear models are used for analyzing designed experiments and assessing differential expression: "Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments"
- [other] Empirical Bayes methods stabilize results when sample size is small: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
