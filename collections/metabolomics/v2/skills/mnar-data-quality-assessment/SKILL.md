---
name: mnar-data-quality-assessment
description: Use when when you have applied multiple left-censored missing value imputation methods to metabolomics data and need to compare their performance quantitatively.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GSimp.R
  - GSimp_evaluation.R
  - imputeLCMD R package (QRILC)
  - Trunc_KNN (kNN-TN)
  - R (with magrittr, reshape2, ggplot2)
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
evidence_spans:
- '**GSimp.R** contains the core functions for GSimp'
- GSimp.R contains the core functions for GSimp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gsimp_cq
    doi: 10.1371/journal.pcbi.1005973
    title: GSimp
  dedup_kept_from: coll_gsimp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1005973
  all_source_dois:
  - 10.1371/journal.pcbi.1005973
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MNAR Data Quality Assessment

## Summary

Evaluate the quality and recovery accuracy of left-censored missing value imputation methods (GSimp, QRILC, kNN-TN) in metabolomics data by comparing imputed values against known true values using standardized performance metrics.

## When to use

When you have applied multiple left-censored missing value imputation methods to metabolomics data and need to compare their performance quantitatively. Apply this skill when you have generated MNAR-corrupted test data with known true values (via simulation or controlled introduction of missingness), imputed those missing values using different methods, and now need to benchmark which method recovers the underlying values most accurately.

## When NOT to use

- Input data contains real (not artificially introduced) missingness and no ground truth is available — evaluation requires known true values to compute error metrics.
- Single imputation method has been applied — the skill is designed for comparative evaluation across multiple methods.
- Missing data mechanism is confirmed to be MCAR or MAR rather than MNAR — the evaluation pipeline is specifically tuned for left-censored missingness and may not be appropriate for other mechanisms.

## Inputs

- imputed data matrices (one per method: GSimp, QRILC, kNN-TN) in data frame or matrix format
- ground truth / original uncorrupted data matrix (before artificial MNAR introduction)
- positions of missing values (row–column indices where MNAR was artificially introduced)
- GSimp_evaluation.R evaluation function source script

## Outputs

- structured comparison table (data frame) with performance metrics (RMSE, bias, etc.) indexed by imputation method and variable
- CSV or TSV file documenting method-wise performance metrics
- summary statistics (e.g., mean RMSE, bias per method across all variables)

## How to apply

Load the imputed matrices produced by each imputation method (GSimp, QRILC, kNN-TN) alongside the ground truth values into R. Source the GSimp_evaluation.R script containing the evaluation functions that compute performance metrics such as root mean squared error (RMSE), bias, and other quality measures. Execute the evaluation functions on each imputed matrix by comparing imputed values against known true values at the positions where missingness was artificially introduced. Aggregate results across all three methods into a structured comparison table, organizing metrics by method and variable. Export the comparison as a CSV or TSF file for downstream visualization and interpretation. The rationale is that MNAR missingness requires controlled simulation to establish ground truth; comparing multiple methods simultaneously reveals which approach best recovers metabolite abundances under the specific censoring mechanism (left-censoring with upper bound = minimum observed value).

## Related tools

- **GSimp.R** (Core imputation method for left-censored missing values; outputs imputed matrix to be evaluated) — https://github.com/WandeRum/GSimp
- **GSimp_evaluation.R** (Provides evaluation functions (MNAR generation and performance metric computation) that compare imputed matrices against ground truth) — https://github.com/WandeRum/GSimp
- **imputeLCMD R package (QRILC)** (Quantile Regression Imputation of Left-Censored data method; one of the three imputation methods compared in evaluation)
- **Trunc_KNN (kNN-TN)** (Truncation k-nearest neighbors imputation method; one of the three imputation methods compared in evaluation) — https://github.com/WandeRum/GSimp
- **R (with magrittr, reshape2, ggplot2)** (Statistical computing environment for loading data, executing evaluation functions, and aggregating results)

## Examples

```
source('GSimp_evaluation.R'); source('Impute_wrapper.R'); after_GS_imp <- pre_processing_GS_wrapper(untargeted_data); after_QRILC_imp <- sim_QRILC_wrapper(log(untargeted_data)) %>% exp(); after_trKNN_imp <- sim_trKNN_wrapper(log(untargeted_data)) %>% exp(); eval_results <- compare_methods(list(GSimp=after_GS_imp, QRILC=after_QRILC_imp, kNN_TN=after_trKNN_imp), ground_truth=untargeted_data, NA_pos=NA_pos); write.csv(eval_results, 'imputation_comparison.csv')
```

## Evaluation signals

- Performance metrics (RMSE, bias) are computed for all three methods and comparison table contains no NA or NaN values for any populated cell.
- Comparison table structure matches expected schema: rows indexed by variable or method, columns contain metric names and method identifiers, all numeric metric values fall within plausible ranges (e.g., RMSE ≥ 0).
- Results table is exported successfully as CSV/TSV with consistent delimiter and no truncation of numeric precision.
- Method ranking by RMSE is consistent with expected performance patterns from the literature or pilot analyses (e.g., GSimp typically outperforms simpler methods like half-minimum substitution).
- Comparison includes per-variable and per-method summary statistics (mean, SD) allowing identification of variables where one method substantially outperforms others.

## Limitations

- Evaluation requires artificially introduced MNAR missingness with known ground truth; real-world data with uncontrolled missingness cannot be evaluated using this pipeline.
- Performance metrics are sensitive to the bounds used for left-censoring (e.g., upper bound = minimum value may be too strict); evaluation results may not generalize to datasets with different censoring thresholds.
- Comparison is limited to three specific imputation methods (GSimp, QRILC, kNN-TN); other left-censored imputation approaches must be wrapped into compatible functions before inclusion.
- Evaluation does not assess whether imputation preserves correlation structure or multivariate relationships — only per-variable recovery accuracy is quantified.
- Metabolomics data should be log-transformed before imputation and evaluation to meet normality assumptions of the Gibbs sampler and quantile regression methods.

## Evidence

- [readme] GSimp_evaluation.R contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline.: "GSimp_evaluation.R contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline."
- [other] Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values.: "Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values."
- [other] Aggregate results across all three methods into a structured comparison table.: "Aggregate results across all three methods into a structured comparison table."
- [readme] wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods: "wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods"
- [readme] Log transformation, Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction): "Log-transformation (for non-normal data); Initialization for missing values (e.g., QRILC); Centralization and scaling"
