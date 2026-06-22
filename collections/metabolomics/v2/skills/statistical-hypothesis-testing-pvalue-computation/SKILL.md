---
name: statistical-hypothesis-testing-pvalue-computation
description: Use when after log-transformation and missing-value imputation of a metabolomics featuredata matrix, when you have a design matrix encoding one or more factors of interest and need to test the statistical significance of each metabolite's association with those factors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - R
  - NormalizeMets
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-hypothesis-testing-pvalue-computation

## Summary

Compute p-values and regression coefficients by fitting linear models to normalized metabolomics feature data matrices in order to identify biomarkers associated with factors of interest (e.g., exposure, disease status, or demographic variables). This skill enables downstream statistical comparison and filtering of metabolites.

## When to use

Apply this skill after log-transformation and missing-value imputation of a metabolomics featuredata matrix, when you have a design matrix encoding one or more factors of interest and need to test the statistical significance of each metabolite's association with those factors. Use when the goal is biomarker discovery and you require both coefficient estimates and per-metabolite p-values for volcano plot or threshold-based filtering.

## When NOT to use

- Input featuredata contains untransformed or unadjusted raw peak intensities; log-transform and normalize first.
- Missing values in featuredata have not been imputed; apply MissingValues() function before LinearModelFit.
- Design matrix (factormat) is not aligned to featuredata row order or does not encode all factors of biological interest.

## Inputs

- featuredata: log-transformed metabolomics matrix (samples × metabolites) with missing values imputed
- factormat: design matrix encoding factors of interest (samples × factors), with factor levels or numeric codes
- optional: qcmets vector identifying quality-control metabolites for RUV2 normalization

## Outputs

- coefficient matrix: one column per factor, rows are metabolites
- p-value matrix: one column per factor, rows are metabolites, values in [0, 1]
- residuals matrix: model residuals (samples × metabolites) for downstream diagnostics
- fitted model object: full model output enabling extraction of diagnostics and comparisons

## How to apply

Load the log-transformed, imputed featuredata matrix (samples as rows, metabolites as columns) and a design matrix encoding factors of interest (factormat). Call LinearModelFit() with both matrices and specify whether to use unadjusted analysis (ruv2=FALSE) or the RUV2 batch-correction method (ruv2=TRUE with k and qcmets parameters). Extract the resulting coefficient matrix (one column per factor), p-value matrix (matching structure), and residuals. The linear model fits the normalized intensity for each metabolite as a function of the factors, producing one p-value per metabolite per factor; these enable identification of significantly associated biomarkers (e.g., p < 0.05 after multiple-testing correction) and construction of diagnostic plots (volcano, RLA, p-value histogram).

## Related tools

- **NormalizeMets** (R package providing LinearModelFit() function and supporting functions (LogTransform, MissingValues, NormQcmets) for preparing and analyzing normalized metabolomics data) — https://github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment for executing LinearModelFit() and downstream statistical tests and visualizations)

## Examples

```
LinearModelFit(featuredata, factormat, ruv2=FALSE)
```

## Evaluation signals

- Coefficient and p-value matrices have dimensions matching featuredata columns (metabolites) and factormat columns (factors).
- P-value matrix contains values in the range [0, 1] with no NaN or Inf unless a metabolite has zero variance.
- Residuals matrix has same dimensions as input featuredata; residual mean per factor should be close to zero, indicating proper model fit.
- Number of significant metabolites (e.g., p < 0.05) is reasonable given the data; volcano plot shows expected distribution of effect sizes vs. −log10(p).
- RLA plots or residual diagnostics confirm that normalization is adequate and no systematic bias remains after model fit.

## Limitations

- LinearModelFit assumes linear associations; nonlinear or interaction effects require custom model specification.
- Multiple-testing correction (e.g., FDR, Bonferroni) is not automatic; multiple p-value matrices across factors require manual correction or post-hoc filtering.
- RUV2 method requires specification of k (number of unwanted variation components) and qcmets (quality-control metabolites); incorrect choice can bias results or inflate false positives.
- Model assumes homogeneity of variance across groups; heteroscedasticity or outliers may inflate or deflate p-values; diagnostic plots (RLA, residual plots) should be inspected.
- Missing values imputed via knn or replacement may introduce bias if missing data are not missing-at-random; sensitivity analysis is recommended.

## Evidence

- [other] Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method).: "Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method)."
- [other] Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object.: "Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object."
- [other] The LinearModelFit mechanism fits a linear model to normalized data to identify biomarkers associated with factors of interest, producing results that enable downstream comparison.: "The LinearModelFit mechanism fits a linear model to normalized data to identify biomarkers associated with factors of interest, producing results that enable downstream comparison."
- [other] Identifying biomarkers that are associated with an exposure, adjusting for confounding variables: "Identifying biomarkers that are associated with an exposure, adjusting for confounding variables"
- [readme] The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data: "The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data"
