---
name: peak-area-intensity-normalization
description: Use when you have a targeted metabolomics peak area intensity table (samples
  in rows, compounds in columns) with assigned internal standards and you need to
  prepare data for quantification via regression models or statistical testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
  license_tier: open
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration
  of metabolomics data
- linear models with mixed effects (random and fixed), using the _lmer_ function from
  the lme4 package
- TOBIT linear models, using the _tobit_ function of the AER package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-area-intensity-normalization

## Summary

Normalize peak area intensities in targeted metabolomics data using internal standards and optional log transformation and scaling to prepare feature tables for downstream quantification and statistical analysis. This skill standardizes raw intensity measurements to account for instrumental drift, sample preparation variation, and enables comparison across samples and compounds.

## When to use

Apply this skill when you have a targeted metabolomics peak area intensity table (samples in rows, compounds in columns) with assigned internal standards and you need to prepare data for quantification via regression models or statistical testing. Use it after QC-based feature filtering but before concentration calculation or univariate/multivariate analysis.

## When NOT to use

- Input is already a feature table from non-targeted analysis (use QC-based filtering and feature elaboration instead)
- No internal standards are available and compound heterogeneity is very high (consider alternative normalization approaches or suspect screening)
- Data contains zero or negative intensity values and log transformation is planned without prior pseudocount addition

## Inputs

- peak area intensity table (samples × compounds matrix)
- sample legend with sample type classifications (blank, curve, qc, unknown)
- compound legend with assigned internal standards (matched internal standard or NA)

## Outputs

- normalized intensity matrix (samples × compounds)
- internal standard intensity matrix (optional, for CV calculation)
- normalization parameters (scaling factors, log transformation flag, scaling method)

## How to apply

First, normalize peak area intensities by dividing each compound's intensity by its assigned internal standard intensity (or by an overall scaling factor if no internal standards are available). Optionally apply log transformation to stabilize variance and reduce skew in intensity distributions. Then apply scaling (e.g., unit variance scaling or z-score normalization) if subsequent analysis requires centered or standardized features. Validate that normalized intensities preserve the rank order and relative differences across samples while reducing systematic bias from instrument sensitivity and sample handling variation.

## Related tools

- **GetFeatistics** (R package providing get_targeted_elaboration function that applies normalization via internal standards, log transformation, and scaling options to targeted metabolomics intensity tables) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Statistical computing environment (≥4.3.1) required for executing GetFeatistics normalization functions)

## Examples

```
result <- get_targeted_elaboration(df_example_targeted, df_example_targeted_legend, df_example_targeted_compounds_legend); normalized_intensities <- result$results_concentrations
```

## Evaluation signals

- Normalized intensities have zero mean and unit variance (if scaling=TRUE); log-transformed intensities exhibit reduced skewness compared to raw intensities
- Relative standard deviation (CV%) of internal standard intensities decreases post-normalization or remains within acceptable QC thresholds (<15–20% typical)
- Rank correlation between raw and normalized compound intensities remains >0.95, confirming preservation of relative differences
- Regression model R² values for curve samples increase or remain stable after normalization, indicating improved linearity
- No NA or infinite values introduced; all normalized intensities fall within biologically plausible ranges for the instrument and compound class

## Limitations

- Internal standard normalization assumes constant efficiency and recovery across samples; ion suppression or matrix effects may violate this assumption
- Log transformation undefined for zero or negative intensities; pseudocount addition (e.g., +1) is necessary but influences quantification accuracy
- Scaling (e.g., z-score) assumes approximately normal or unimodal intensity distributions; highly multimodal or sparse data may require robust scaling methods
- Normalization effectiveness depends on internal standard selection and stability; poorly chosen or unstable internal standards propagate error into normalized values

## Evidence

- [readme] Internal standard intensity-based normalization rationale: "a third table is useful especially if you work with internal standards...in the second column, the matched internal standard (or NA if there isn't an internal standard for that molecule)"
- [intro] Log transformation and scaling parameters in GetFeatistics: "If _log_transf_ is TRUE, the data will be log-transformed...If _scaling_ is TRUE, data will be scaled"
- [other] Internal standard CV as quality metric post-normalization: "cv_internal_standards (relative standard deviation of internal standard intensities)"
- [intro] Input data structure and intensity table format: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] Missing value replacement in normalization workflow: "If _missing_replace_ is TRUE, each NA in the data will be replaced"
