---
name: missing-value-imputation-strategy
description: Use when your feature intensity table (samples × compounds) contains
  NA values and you intend to apply log transformation or scaling-based normalization.
  Specifically, apply this skill when the transf_data function is invoked with missing_replace=TRUE,
  before any log transformation or scaling step.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3409
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0749
  tools:
  - R
  - GetFeatistics
  - R (≥ 4.3.1)
  license_tier: open
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
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

# missing-value-imputation-strategy

## Summary

Replace missing values (NAs) in metabolomics feature intensity tables prior to log transformation and scaling. This skill is essential because log transformation cannot be applied to missing data, and imputation must occur before normalization to prevent bias in downstream statistical comparisons.

## When to use

Your feature intensity table (samples × compounds) contains NA values and you intend to apply log transformation or scaling-based normalization. Specifically, apply this skill when the transf_data function is invoked with missing_replace=TRUE, before any log transformation or scaling step. Imputation is a prerequisite for compounds where detection is sporadic or below instrument sensitivity thresholds across the sample cohort.

## When NOT to use

- Input data has no missing values (NA count = 0); imputation is unnecessary and adds no information.
- You intend to use non-imputation methods (e.g., complete-case analysis or paired comparisons) that explicitly require NA preservation.
- The missing-data mechanism is not missing-at-random (MAR) or missing-completely-at-random (MCAR); systematic missingness linked to low abundance or instrument failure may require domain-specific imputation (e.g., half-LOD replacement) instead of mean-centering.

## Inputs

- Feature intensity table (numeric matrix or data frame; samples in rows, compounds in columns, with NA entries)
- Boolean parameter missing_replace (TRUE to enable imputation)
- Optional vect_names_transf parameter (character string prefix for naming intermediate vectors)

## Outputs

- Feature intensity table with all NAs replaced by compound-wise means (suffix _mr appended to column names)
- Vector of post-imputation column names saved in global environment (if vect_names_transf is specified)

## How to apply

The transf_data function replaces all NA values in the feature intensity matrix using mean-centering imputation: each missing value for a given compound is replaced with the mean intensity of that compound calculated across all samples where it was detected. This produces intermediate columns with the _mr (mean replacement) suffix. The imputation occurs prior to log transformation because the log function is undefined for zero or negative values; by imputing with compound means (strictly positive for detected metabolites), all imputed entries become log-transformable. After imputation, check that no NAs remain before proceeding to log transformation (_ln suffix) and scaling (e.g., paretosc for Pareto scaling). The vect_names_transf argument automatically saves the vector of post-imputation column names in the global environment, allowing you to track which compounds were altered and verify imputation coverage.

## Related tools

- **GetFeatistics** (R package that implements the transf_data function for sequential missing-value imputation, log transformation, and scaling in metabolomics feature tables.) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R (≥ 4.3.1)** (Runtime environment in which GetFeatistics and transf_data are executed.)

## Examples

```
data_imputed <- transf_data(data = feature_matrix, missing_replace = TRUE, log_transf = FALSE, scaling = FALSE, vect_names_transf = 'names_mr')
```

## Evaluation signals

- All NA entries in the input feature table are replaced with numeric values; verify with any(is.na(output_data)) == FALSE.
- Each imputed value equals the arithmetic mean of detected intensities for that compound across the sample cohort; spot-check by comparing imputed entries to colMeans(input_data, na.rm=TRUE).
- Output column names include _mr suffix and match the pre-imputation count of compounds; length(grep('_mr$', colnames(output))) == ncol(input).
- Intermediate column-name vector is saved in the global environment under the name specified by vect_names_transf parameter; verify with exists() and inspect with print().
- Downstream log transformation and scaling steps execute without error (no NaN or Inf values introduced by log(0) or division by undefined standard deviations).

## Limitations

- Mean-centering imputation may bias variance and covariance estimates, particularly when missingness is high (>20%) or non-random, because compound means are less reliable when estimated from few samples.
- If a compound is detected in only one or two samples, the imputed mean may not represent the true biological value in missing samples, potentially confounding concentration-response relationships or group comparisons.
- The skill does not test the missing-data mechanism; if missingness is correlated with sample type (e.g., blanks systematically lack compound detection), imputation may artificially homogenize group profiles.
- No sensitivity analysis or alternative imputation method (e.g., k-NN, half-LOD) is provided within transf_data; practitioners requiring robust imputation must implement custom preprocessing or use external tools before invoking this function.

## Evidence

- [other] The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale, auto_scale, pareto_scale, or range_scale.: "The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling"
- [intro] If _missing_replace_ is TRUE, each NA in the data will be replaced with the mean of that feature across all samples.: "If _missing_replace_ is TRUE, each NA in the data will be replaced with the mean of that feature across all samples"
- [intro] If _log_transf_ is TRUE, the data will be log-transformed, and missing values must be replaced first because log transformation is undefined for zero or negative values.: "If _log_transf_ is TRUE, the data will be log-transformed"
- [other] Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors.: "Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors"
