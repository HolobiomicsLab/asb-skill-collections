---
name: linear-regression-design-matrix-construction
description: Use when after log-transformation and missing-value imputation of featuredata
  (via LogTransform and MissingValues functions), when you have normalized metabolomics
  intensity data and need to identify metabolites associated with specific biological
  or experimental factors encoded as covariates in a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - LinearModelFit
  - LogTransform
  - MissingValues
  - NormQcmets
  license_tier: open
  provenance_tier: literature
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

# linear-regression-design-matrix-construction

## Summary

Construction of a design matrix (factormat) that encodes biological factors of interest (e.g., gender, age, BMI) for use in linear regression analysis of normalized metabolomics feature data. This skill is essential for enabling downstream biomarker identification and statistical comparison of metabolite abundance across experimental groups.

## When to use

After log-transformation and missing-value imputation of featuredata (via LogTransform and MissingValues functions), when you have normalized metabolomics intensity data and need to identify metabolites associated with specific biological or experimental factors encoded as covariates in a design matrix for input to LinearModelFit.

## When NOT to use

- featuredata has not yet been log-transformed or imputed for missing values — apply LogTransform and MissingValues first
- factors of interest are already encoded as columns in the featuredata itself rather than in separate metadata — ensure factormat is a separate, aligned matrix
- sample identifiers in featuredata row names do not match those in the factor metadata — factormat construction requires exact row-name correspondence

## Inputs

- normalized featuredata matrix (samples × metabolites, log-transformed, missing values handled)
- sample metadata or factor table with factor-of-interest columns (e.g., gender, age, BMI, batch)

## Outputs

- design matrix (factormat): samples × factors numeric matrix with aligned row names
- LinearModelFit model object containing coefficient matrix, p-value matrix, and residuals (one column per factor)

## How to apply

Construct a design matrix (factormat) with one row per sample (matching the row names and order of the normalized featuredata matrix) and one column per factor of interest (e.g., gender, age, BMI, batch, treatment group). Encode categorical factors as numeric indicators (e.g., 0/1 for binary factors or contrast-coded levels) and continuous factors as numeric values. Ensure sample names align exactly between featuredata and factormat row names to prevent indexing mismatches. Pass the featuredata matrix and factormat together to LinearModelFit() along with optional parameters (ruv2=FALSE for unadjusted analysis or ruv2=TRUE with k and qcmets for RUV2-adjusted analysis). The design matrix structure directly determines which coefficients and p-values are extracted in the model output.

## Related tools

- **LinearModelFit** (receives factormat as input to fit linear model and generate coefficient/p-value tables for biomarker identification) — github.com/metabolomicstats/NormalizeMets
- **LogTransform** (log-transforms featuredata prior to design-matrix construction and model fitting) — github.com/metabolomicstats/NormalizeMets
- **MissingValues** (handles missing-value imputation in featuredata before design-matrix-based analysis) — github.com/metabolomicstats/NormalizeMets
- **NormQcmets** (normalizes featuredata using optional RUV2 method; qcmets metadata may inform design matrix construction if quality-control factors are modeled) — github.com/metabolomicstats/NormalizeMets
- **R** (environment for constructing factormat data frames and passing to LinearModelFit)

## Examples

```
# In R: construct factormat from sample metadata and pass to LinearModelFit
factormat <- data.frame(gender=c(0,1,0,1), age=c(25,32,28,45), BMI=c(22.5,24.1,23.8,26.2), row.names=rownames(featuredata))
lmfit_result <- LinearModelFit(featuredata, factormat, ruv2=FALSE)
```

## Evaluation signals

- factormat row names exactly match featuredata row names in identical order (no reordering or misalignment)
- all factor columns in factormat are numeric (continuous or contrast-coded categorical); non-numeric entries cause LinearModelFit to fail
- factormat has no missing values (NA); missing factor values must be handled before LinearModelFit input
- coefficient matrix output has one column per factor column in factormat, and p-value matrix dimensions match (samples × factors)
- extracted coefficients and p-values enable downstream volcano plots, RLA plots, and p-value histograms without index or dimension mismatches

## Limitations

- factormat construction assumes factors are correctly labeled and measured in the source metadata; measurement error or mislabeling propagates directly into model results
- categorical factors must be pre-coded numerically (e.g., via contrast coding or 0/1 encoding); LinearModelFit does not auto-convert character or factor columns
- linear model assumes linear relationships between factors and log-transformed metabolite abundance; non-linear associations may be missed
- confounding variables must be explicitly included as columns in factormat; omitted confounders can bias coefficient and p-value estimates

## Evidence

- [other] load the imputed featuredata matrix (log-transformed, missing values handled via knn or replacement) and a design matrix (factormat) encoding factors of interest (e.g., gender, age, BMI): "Load the imputed featuredata matrix (log-transformed, missing values handled via knn or replacement) and a design matrix (factormat) encoding factors of interest (e.g., gender, age, BMI) using R."
- [other] Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method): "Call LinearModelFit() with featuredata, factormat, and optional parameters (ruv2=FALSE for unadjusted analysis, or ruv2=TRUE with k and qcmets for RUV2 method)."
- [other] Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object: "Extract coefficient matrix (one column per factor), p-value matrix (one column per factor), and residuals from the model object."
- [readme] The input data format consists of three parts: (i) 'featuredata' which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names: "The input data format consists of three parts: (i) "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be"
- [readme] the statistical analysis of metabolomic data and can be used assess, select and implement statistical methods for normalizing metabolomics data: "The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data"
