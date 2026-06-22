---
name: log-transformation-application
description: Use when apply log-transformation immediately after loading a raw metabolomics featuredata matrix (metabolite peak intensities as rows=samples, columns=metabolites) and before normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - R
  - NormalizeMets
  - RStudio
  - MissingValues
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment (IDE)
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

# log-transformation-application

## Summary

Log-transformation of metabolomics feature intensity matrices to stabilize variance and handle zeros before normalization. This pre-processing step converts raw peak intensities to a log scale, making downstream normalization methods more effective by reducing the impact of extreme values and improving homogeneity of variance.

## When to use

Apply log-transformation immediately after loading a raw metabolomics featuredata matrix (metabolite peak intensities as rows=samples, columns=metabolites) and before normalization. Essential when the data exhibits skewed distributions with right-tail outliers (typical of untransformed mass spectrometry intensities) or contains zero values that would violate assumptions of downstream normalization methods such as 'is', 'nomis', 'ccmn', 'ruv2', or 'ruvrand'.

## When NOT to use

- Data is already log-transformed or normalized (check for mean~0, SD~1, or verify prior transformation steps)
- featuredata contains only positive, non-zero values with symmetric, approximately normal distribution already
- Missing data is not compatible with your downstream analysis (LogTransform with zerotona=TRUE creates NAs that require imputation)

## Inputs

- featuredata matrix (numeric; rows=samples, columns=metabolites; raw peak intensities or concentrations)
- base parameter (numeric; default=exp(1) for natural logarithm)
- zerotona parameter (logical; TRUE to replace zeros with NA)

## Outputs

- log-transformed featuredata matrix (numeric; same dimensions as input; zeros converted to NA)
- LogTransform output object (R object containing transformed matrix and metadata)

## How to apply

Call the LogTransform function with the featuredata matrix as input, setting base=exp(1) (natural logarithm) and zerotona=TRUE to convert zero values to NA before transformation. The zerotona parameter is critical: it replaces zeros with missing values, which are then handled in the next step via MissingValues with feature.cutoff=0.8, sample.cutoff=0.8, and method='knn' or 'replace'. The natural log scale is chosen because it approximates the multiplicative error structure typical of analytical instruments. After log-transformation and missing-value imputation, extract the transformed featuredata matrix and proceed to identify internal standards (QC metabolites) from metabolitedata before calling NormQcmets.

## Related tools

- **NormalizeMets** (R package providing LogTransform function and downstream normalization workflow) — github.com/metabolomicstats/NormalizeMets
- **R** (Execution environment for LogTransform and featuredata matrix operations)
- **RStudio** (Recommended IDE for interactive LogTransform execution and result inspection)
- **MissingValues** (Companion function (applied after LogTransform) to impute NA values created by zerotona=TRUE) — github.com/metabolomicstats/NormalizeMets

## Examples

```
LogTransform(featuredata = mixdata$featuredata, base = exp(1), zerotona = TRUE)
```

## Evaluation signals

- Transformed featuredata has no zero values; all zeros are converted to NA (verify via sum(featuredata==0, na.rm=TRUE)==0)
- Distribution of transformed values is approximately symmetric and unimodal (inspect via histogram or density plot)
- Mean of log-transformed intensities is near zero; standard deviation is stable across metabolites (run colMeans and colSds on result)
- Outliers in original space are reduced in magnitude after transformation (compare boxplot before/after)
- Missing-value imputation (via MissingValues) succeeds on the transformed matrix with no samples or metabolites removed beyond feature.cutoff=0.8 or sample.cutoff=0.8 thresholds

## Limitations

- zerotona=TRUE converts zeros to NA; subsequent imputation (MissingValues) may fail or remove features if too many zeros are present per metabolite or sample
- Natural logarithm is undefined for negative values; ensure featuredata contains only non-negative intensities before transformation
- Log-transformation assumes multiplicative error structure; if errors are additive or data are already heavily pre-processed, transformation may not improve normalization
- Base=exp(1) (natural log) is the recommended choice; other bases are supported but changing base may affect downstream interpretation of effect sizes in linear models

## Evidence

- [other] Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros.: "Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros."
- [other] A metabolomics data matrix in the featuredata format can be transformed using the LogTransform function.: "A metabolomics data matrix in the _featuredata_ format can be transformed using the following function. LogTransform <- function(featuredata, base=exp(1), saveoutput=FALSE,"
- [other] The following MissingValues() function can be used to replace missing values after log-transformation.: "The following `MissingValues()` function can be used to replace missing values, depending on the nature of missing data."
- [readme] Metabolomics data are subject to unwanted variation due to batch effects and matrix effects.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
