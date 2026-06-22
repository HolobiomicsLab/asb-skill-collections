---
name: feature-matrix-preprocessing
description: Use when you have raw metabolomics data in CSV format (samples as rows, features as columns, batch identifier in the first column) that contains missing values (zeros or NAs) and requires standardization before batch effect correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - dbnorm
  - R
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-preprocessing

## Summary

Reconstruct and apply dbnorm's 11 distinct preprocessing and missing-value estimation functions to prepare raw metabolomics data matrices (samples × features) for batch effect correction. This initial stage standardizes feature distributions, estimates and imputes missing values (zeros and NAs), and removes technical artifacts before downstream normalization.

## When to use

Apply this skill when you have raw metabolomics data in CSV format (samples as rows, features as columns, batch identifier in the first column) that contains missing values (zeros or NAs) and requires standardization before batch effect correction. The data must already be normalized and log2-scaled to account for high-abundance features.

## When NOT to use

- Data is already imputed or contains no missing values (zeros or NAs)
- Input is already a batch-corrected feature table or normalized output from another pipeline
- Features have not been log2-scaled or data structure lacks batch annotation in first column

## Inputs

- Raw metabolomics data matrix (CSV format): samples × features, log2-scaled, with batch identifier in first column
- Feature abundance matrix (numeric values, may contain 0 or NA)

## Outputs

- Imputed metabolomics data matrix (CSV file in R temporary directory or working directory)
- Feature matrix with missing values replaced by estimated minima

## How to apply

Load the raw metabolomics data matrix into R in CSV format with batch levels in the first column and features in subsequent columns. Select one of two missing-value estimation strategies: emvd() to impute missing values using the lowest detected value across the entire experiment, or emvf() to impute feature-wise using the lowest value detected for each individual feature. Apply the chosen function to the data matrix (excluding the batch column). The rationale is that feature-wise imputation (emvf) preserves per-feature abundance distributions, while global imputation (emvd) uses overall experiment-level thresholds. Export the resulting imputed matrix as a CSV file for input to downstream batch effect correction functions (dbnormBer, dbnormPcom, dbnormNPcom, or dbnormBagging).

## Related tools

- **dbnorm** (Provides emvd() and emvf() functions for missing-value estimation and imputation in metabolomics preprocessing pipeline) — https://github.com/NBDZ/dbnorm
- **R** (Execution environment for dbnorm preprocessing functions)

## Examples

```
data <- read.csv('path/to/mydata.csv', sep = ',', header = T, row.names = 1); library(dbnorm); df <- data[-1]; f <- emvf(df); write.csv(f, 'imputed_data.csv')
```

## Evaluation signals

- Imputed matrix has no remaining 0 or NA values in the feature columns
- Output CSV dimensions match input (same number of samples and features)
- Imputed values are positive and fall within the detected range for each feature (or across the entire experiment, depending on function choice)
- Batch column is preserved unchanged in the output
- Downstream batch-effect correction functions (Visodbnorm, dbnormBer, etc.) execute without missing-value errors on the output

## Limitations

- emvd and emvf use only the minimum detected value; no probabilistic or distribution-aware imputation is applied
- Input data must be already log2-scaled; the functions do not verify or enforce this assumption
- No built-in validation or QC plots for the imputation step; users should inspect pre/post distributions manually
- Missing completely at random (MCAR) assumption is not explicitly tested; method may bias inference if missingness depends on unobserved abundance

## Evidence

- [intro] dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values: "dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values"
- [other] Load raw metabolomics data matrix and apply dbnorm preprocessing functions to estimate and impute missing values: "Load raw metabolomics data matrix (samples × features) in R using appropriate I/O functions. 2. Apply dbnorm preprocessing functions to estimate and impute missing values across the feature matrix."
- [readme] emvd estimates missing values by the lowest detected value in the entire experiment: "This function allows you to estimate missing values (Zero or/and NA values) by the lowest detected value in the entire experiment."
- [readme] emvf estimates missing values for each feature by the lowest value detected for that feature: "This function allows you to estimate missing values (Zero or/and NA values) for each feature (variable) by the lowest value detected for the corresponding feature (variable), applied on the column."
- [readme] Data must be normalized and scaled on log2 with batch levels in the first column: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked. The input data must be in"
