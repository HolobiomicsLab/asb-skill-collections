---
name: biomarker-coefficient-extraction
description: Use when after normalizing a log-transformed metabolomics featuredata
  matrix (with missing values imputed via knn or replacement) and encoding experimental
  factors into a design matrix (factormat), use this skill to fit a linear model and
  extract per-metabolite coefficients and p-values for each.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - NormalizeMets
  license_tier: open
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
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

# biomarker-coefficient-extraction

## Summary

Extract coefficient and p-value matrices from a fitted linear model applied to normalized, log-transformed metabolomics feature data to identify biomarkers associated with factors of interest (e.g., gender, age, BMI). This skill produces quantitative association metrics and statistical significance estimates required for downstream biomarker validation and visualization.

## When to use

After normalizing a log-transformed metabolomics featuredata matrix (with missing values imputed via knn or replacement) and encoding experimental factors into a design matrix (factormat), use this skill to fit a linear model and extract per-metabolite coefficients and p-values for each factor. Apply this when your goal is to identify which metabolites show significant association with one or more study factors, optionally adjusted for unwanted variation via RUV2.

## When NOT to use

- Input featuredata is not log-transformed or has not undergone normalization (apply LogTransform and NormQcmets first).
- Missing values in featuredata have not been addressed (apply MissingValues first).
- Design matrix factormat is not provided or does not encode the factors of interest; LinearModelFit requires explicit factor encoding, not raw sample labels.

## Inputs

- featuredata matrix (log-transformed, samples × metabolites, missing values imputed)
- design matrix / factormat (samples × factors encoding exposure/covariate levels)
- optional: qcmets indices (integer vector identifying quality control metabolites for RUV2)
- optional: k integer (number of unwanted variation components for RUV2)

## Outputs

- coefficient matrix (metabolites × factors)
- p-value matrix (metabolites × factors)
- residuals from fitted linear model
- fitted model object containing all three

## How to apply

Load the imputed, log-transformed featuredata matrix (samples as rows, metabolites as columns) and a design matrix factormat encoding factors of interest into R. Call LinearModelFit() with parameters: featuredata, factormat, and optional ruv2=TRUE/FALSE (set ruv2=TRUE to invoke RUV2 correction with k and qcmets parameters; set FALSE for unadjusted analysis). Extract the coefficient matrix (one column per factor, rows = metabolites) and p-value matrix (same structure) from the returned model object. The coefficients quantify the per-unit change in (log) metabolite intensity per unit increase in each factor; p-values assess statistical significance. Verify that dimensions match featuredata (number of metabolites) and factormat (number of factors).

## Related tools

- **NormalizeMets** (R package providing LinearModelFit function and companion normalization/preprocessing functions (LogTransform, MissingValues, NormQcmets) required to prepare featuredata and factormat inputs) — github.com/metabolomicstats/NormalizeMets
- **R** (Computing environment in which LinearModelFit is invoked and coefficient/p-value matrices are extracted and manipulated)

## Examples

```
model_fit <- LinearModelFit(featuredata, factormat, ruv2=TRUE, k=2, qcmets=qc_indices); coef_matrix <- model_fit$coefficients; pval_matrix <- model_fit$pvalues
```

## Evaluation signals

- Coefficient matrix has exactly nrow(featuredata) rows (one per metabolite) and ncol(factormat) columns (one per factor).
- P-value matrix has identical dimensions and all values are in [0, 1].
- Residuals from the model sum to approximately zero (within numerical precision) when aggregated across samples.
- Coefficients with smallest p-values (e.g., p < 0.05) show expected biological direction and magnitude relative to study design (e.g., positive coefficients for metabolites elevated in a case group).
- When ruv2=FALSE and ruv2=TRUE are compared on the same data, p-values and coefficients for unwanted-variation-confounded metabolites should show larger adjustment in the RUV2 version.

## Limitations

- LinearModelFit assumes linear relationship between log-intensity and factors; non-linear or interaction effects require manual model specification outside this skill.
- RUV2 correction requires pre-specification of quality control metabolites (qcmets); misidentified or absent QC metabolites may lead to over- or under-correction.
- Multiple testing correction (e.g., Benjamini–Hochberg FDR) is not applied within LinearModelFit; practitioners must apply it separately to p-value matrices downstream.
- Model assumes residuals are approximately normally distributed; heavy-tailed or bimodal residual distributions may inflate type I error rates.

## Evidence

- [other] Task 004 finding: "The LinearModelFit mechanism fits a linear model to normalized data to identify biomarkers associated with factors of interest, producing results that enable downstream comparison."
- [other] Task 004 workflow step 1: "Load the imputed featuredata matrix (log-transformed, missing values handled via knn or replacement) and a design matrix (factormat) encoding factors of interest (e.g., gender, age, BMI) using R."
- [other] Task 004 workflow step 2: "Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method)."
- [other] Task 004 workflow step 3: "Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object."
- [readme] NormalizeMets README workflow: "Identifying biomarkers that are associated with an exposure, adjusting for confounding variables"
