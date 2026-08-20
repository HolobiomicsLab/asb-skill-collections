---
name: metabolomics-missing-value-imputation
description: Use when raw metabolomics data matrices contain zero values or NA entries
  representing undetected metabolic features. Imputation is required before batch
  effect correction models (ComBat, ber) can be reliably applied, as these models
  assume complete feature matrices.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3216
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - impute
  license_tier: restricted
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical
  heterogeneity'
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

# metabolomics-missing-value-imputation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Estimate and impute missing values (zeros and NAs) in metabolomics feature matrices prior to batch effect correction, using either global minimum or feature-wise minimum strategies. This is a foundational preprocessing step that standardizes sparse metabolomics datasets and prevents loss of samples during downstream normalization.

## When to use

Raw metabolomics data matrices contain zero values or NA entries representing undetected metabolic features. Imputation is required before batch effect correction models (ComBat, ber) can be reliably applied, as these models assume complete feature matrices. Apply this skill when you load a metabolomics dataset in samples × features format and observe missing data density > 0%.

## When NOT to use

- Data has already been imputed or contains no missing values.
- Missingness is not random but systematic (e.g., entire features below detection limit in specific batches)—requires batch-aware imputation instead.
- Goal is to preserve missingness patterns for missing data analysis rather than cleaning for downstream modeling.

## Inputs

- Raw metabolomics data matrix (CSV format; samples × features; log2-scaled; batch identifier in first column)
- Feature matrix with zero or NA values representing undetected metabolites

## Outputs

- Imputed metabolomics feature matrix (complete; CSV format; same dimensions as input)
- Preprocessed data matrix ready for batch effect correction

## How to apply

Load the metabolomics data matrix (samples in rows, features in columns, batch identifier in first column) in CSV format, normalized and log2-scaled to account for high-abundance features. Remove the batch column to isolate the feature matrix. Choose imputation strategy: emvd() imputes missing values to the lowest detected value across the entire experiment (global strategy), while emvf() imputes feature-wise to the lowest detected value within each feature column. Apply your chosen function and save the imputed matrix. The choice depends on data sparsity pattern—use emvf() if missingness is concentrated in specific metabolites, emvd() for uniformly distributed missingness. Verify completeness (no zeros or NAs remain) before proceeding to batch correction.

## Related tools

- **dbnorm** (Provides emvd() and emvf() functions to estimate and impute missing values in metabolomics matrices as first stage of preprocessing pipeline) — https://github.com/NBDZ/dbnorm
- **R** (Runtime environment for executing dbnorm functions and managing data I/O (read.csv, library calls))
- **impute** (Bioconductor dependency of dbnorm; provides supporting imputation algorithms)

## Examples

```
df <- read.csv("path/to/metabolomics.csv", sep=",", header=TRUE, row.names=1); library(dbnorm); df_clean <- data[-1]; f_imputed <- emvf(df_clean); write.csv(f_imputed, "imputed_data.csv")
```

## Evaluation signals

- Imputed matrix contains zero NAs and zero undetected (zero) values in feature columns.
- All imputed values are ≤ the actual observed minimum within their scope (global or feature-wise).
- Imputed matrix has identical dimensions (samples × features) as input matrix.
- Distribution of imputed values does not introduce artificial peaks or bimodality inconsistent with observed metabolite distributions.
- Downstream batch effect correction models (ComBat, ber) run without missing-value-related errors.

## Limitations

- Both emvd() and emvf() replace missing values with observed minima, not statistical estimates (e.g., mean, median, or model-based predictions). This may underestimate true metabolite abundances and inflate batch effect signals if missingness is batch-dependent.
- The method assumes that missing values are MCAR (missing completely at random) or MAR (missing at random); if missingness is MNAR (missing not at random) and correlated with batch, these strategies may mask or exacerbate batch effects.
- Input data must be pre-normalized to log2 scale; the imputation functions do not perform log transformation themselves and will fail or produce invalid results on untransformed count data.
- The README does not document the computational complexity; performance on matrices with >2000 features may be slow (see Visodbnorm() guidance limiting visualization to <2000 features for comparable operations).

## Evidence

- [intro] dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values: "dbnorm includes 11 distinct functions for pre-processing of data and estimation of missing values"
- [readme] emvd estimates missing values using lowest detected value in entire experiment: "This function allows you to estimate missing values (Zero or/and NA values) by the lowest detected value in the entire experiment."
- [readme] emvf estimates missing values feature-wise: "This function allows you to estimate missing values (Zero or/and NA values) for each feature (variable) by the lowest value detected for the corresponding feature (variable), applied on the column."
- [readme] Input data must be normalized and scaled on log2: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables)"
- [other] Imputation precedes batch correction workflow: "1. Load raw metabolomics data matrix (samples × features) in R using appropriate I/O functions. 2. Apply dbnorm preprocessing functions to estimate and impute missing values across the feature matrix."
