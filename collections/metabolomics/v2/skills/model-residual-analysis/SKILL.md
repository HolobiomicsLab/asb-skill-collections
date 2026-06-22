---
name: model-residual-analysis
description: Use when after fitting a linear model to normalized metabolomics featuredata using LinearModelFit(), to validate model assumptions (homogeneity of variance, normality), detect influential observations, and confirm that the model's coefficient and p-value estimates are reliable for downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - LinearModelFit
  - RlaPlots
  - PcaPlots
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-residual-analysis

## Summary

Extract and analyze residuals from a fitted linear model to assess model assumptions, identify outliers, and evaluate the quality of biomarker identification in metabolomics data. Residual analysis validates whether the linear model adequately captures the relationship between metabolites and factors of interest after normalization.

## When to use

After fitting a linear model to normalized metabolomics featuredata using LinearModelFit(), to validate model assumptions (homogeneity of variance, normality), detect influential observations, and confirm that the model's coefficient and p-value estimates are reliable for downstream biomarker identification and visualization (volcano plots, RLA plots).

## When NOT to use

- LinearModelFit has not yet been called or the model object is unavailable—extract residuals first before analysis.
- Featuredata contains untransformed intensities or unhandled missing values—apply LogTransform and MissingValues functions before model fitting.
- The goal is only to identify biomarkers without validating model assumptions—residual analysis is optional if coefficient p-values alone are acceptable for your downstream use case.

## Inputs

- LinearModelFit model object (containing coefficients, p-values, residuals, and fitted values)
- Normalized featuredata matrix (log-transformed, missing values handled)
- Design matrix (factormat) encoding factors of interest

## Outputs

- Residuals matrix (one column per factor or global residuals)
- Residual diagnostics (histograms, Q–Q plots, residuals vs. fitted plots)
- Outlier flagging and influence metrics
- Model validation report (assumption checks, variance homogeneity assessment)

## How to apply

Extract the residuals matrix from the LinearModelFit model object. Examine residual distributions for normality using histograms or Q–Q plots; assess homogeneity of variance by plotting residuals against fitted values; identify outliers exceeding predetermined thresholds (e.g., standardized residuals > ±3). Compare residual patterns across factors and normalization methods to confirm the chosen method (e.g., ruv2=TRUE with appropriate k and qcmets) has adequately removed unwanted variation. Residual analysis informs whether coefficient and p-value tables are suitable for biomarker annotation and downstream classification or clustering tasks.

## Related tools

- **LinearModelFit** (Fits linear model to normalized featuredata and produces the residuals, coefficients, and p-values to be analyzed)
- **NormalizeMets** (Provides integrated workflow for normalizing metabolomics featuredata prior to linear model fitting; residual analysis validates effectiveness of chosen normalization method) — github.com/metabolomicstats/NormalizeMets
- **RlaPlots** (Generates relative log abundance plots that visualize residual variability across groups and samples)
- **PcaPlots** (Principal component analysis on residuals or normalized data to assess clustering and outliers in multivariate space)
- **R** (Environment for executing LinearModelFit, extracting residuals, and producing diagnostic plots)

## Examples

```
# Extract residuals from fitted model and create diagnostic plot
residuals <- fitted_model$residuals
plot(fitted_model$fitted.values, residuals, main='Residuals vs Fitted'); abline(h=0)
```

## Evaluation signals

- Residuals are approximately normally distributed (histogram/Q–Q plot symmetry around zero, no heavy tails).
- Variance is homogeneous across fitted values (residuals vs. fitted plot shows no cone or funnel pattern).
- Outliers are sparse and identifiable (standardized residuals > ±3 flagged, count consistent with expected significance level).
- Residual patterns are consistent across factors in the design matrix (no systematic bias by treatment group).
- Residuals from the chosen normalization method (e.g., ruv2=TRUE) show smaller magnitude and better assumptions than unadjusted analysis (ruv2=FALSE), validating method choice.

## Limitations

- Residual analysis assumes the linear model is the correct functional form; non-linear relationships or interaction terms not included will produce structured residuals unrelated to model adequacy.
- Presence of batch effects or confounding variables not captured in factormat will produce correlated residuals; assess with RLA or PCA plots before concluding model validity.
- Small sample sizes or highly unbalanced design matrices may produce residual patterns that do not clearly indicate assumption violations.
- Metabolites with very high or very low abundance relative to others may have heterogeneous variance despite normalization; consider scaling or per-metabolite variance assessment.

## Evidence

- [other] Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object.: "Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object."
- [other] Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method).: "Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method)."
- [other] The LinearModelFit mechanism fits a linear model to normalized data to identify biomarkers associated with factors of interest, producing results that enable downstream comparison.: "The LinearModelFit mechanism fits a linear model to normalized data to identify biomarkers associated with factors of interest, producing results that enable downstream comparison."
- [other] Save or return the fitted model object containing coefficients, p-values, and residuals for downstream volcano plot, RLA plot, and p-value histogram comparisons.: "Save or return the fitted model object containing coefficients, p-values, and residuals for downstream volcano plot, RLA plot, and p-value histogram comparisons."
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
