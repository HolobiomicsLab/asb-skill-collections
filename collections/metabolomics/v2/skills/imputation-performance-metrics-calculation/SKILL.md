---
name: imputation-performance-metrics-calculation
description: Use when when you have imputed a metabolomics dataset using multiple MNAR (missing not at random) imputation methods and possess the ground-truth values (from simulation or manual retrieval).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3957
  tools:
  - R
  - GSimp_evaluation.R
  - imputeLCMD (QRILC wrapper)
  - Trunc_KNN (kNN-TN implementation)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imputation-performance-metrics-calculation

## Summary

Calculate quantitative performance metrics (RMSE, bias, and other quality measures) to compare multiple left-censored missing value imputation methods (GSimp, QRILC, kNN-TN) against known true values in metabolomics data. This skill enables objective evaluation of which imputation strategy best recovers artificially censored metabolite abundances.

## When to use

When you have imputed a metabolomics dataset using multiple MNAR (missing not at random) imputation methods and possess the ground-truth values (from simulation or manual retrieval). Use this skill to quantify how well each method recovered the censored values and to rank methods by reconstruction accuracy.

## When NOT to use

- Input lacks ground-truth values or cannot be simulated (e.g., real data with only MCAR/MAR and no retrieval); evaluation requires known true values to compute reconstruction error.
- Imputed matrices have not been back-transformed to the original scale (log-transformed or scaled data will produce misleading RMSE and bias estimates).
- You are evaluating imputation for right-censored or mixed-censored data; GSimp_evaluation.R is specifically designed for left-censored MNAR metabolomics data.

## Inputs

- imputed data matrix from GSimp (log-transformed, scaled, and recovery-transformed)
- imputed data matrix from QRILC (quantile regression imputation)
- imputed data matrix from kNN-TN (truncation k-nearest neighbors)
- ground-truth values (known true abundances at originally missing positions)
- NA_pos matrix (row-column indices of originally missing values)

## Outputs

- performance metrics table (RMSE, bias, or other quality measures per method)
- method comparison CSV or TSV file documenting method-wise performance
- ranked imputation methods by reconstruction accuracy

## How to apply

Load each imputed matrix (output from GSimp, QRILC, and kNN-TN applied to MNAR-corrupted data) into R and source the GSimp_evaluation.R script containing the evaluation functions. Execute the evaluation functions on each imputed matrix, computing performance metrics such as root mean squared error (RMSE) and bias by comparing imputed values to the known true values at the originally missing positions. Aggregate results across all three methods into a structured comparison table. The evaluation compares imputed values only at positions that were originally missing (NA_pos), not across the entire matrix, ensuring fair assessment of recovery quality.

## Related tools

- **GSimp_evaluation.R** (contains MNAR generation and evaluation functions for computing performance metrics (RMSE, bias) against known true values) — https://github.com/WandeRum/GSimp
- **imputeLCMD (QRILC wrapper)** (computes QRILC-imputed matrix for comparison)
- **Trunc_KNN (kNN-TN implementation)** (computes kNN-TN-imputed matrix for comparison) — https://github.com/WandeRum/GSimp
- **R** (execution environment for sourcing evaluation functions and computing metrics)

## Examples

```
source('GSimp_evaluation.R'); NA_pos <- which(is.na(untargeted_data), arr.ind=T); metrics_GSimp <- evaluate_imputation(after_GS_imp, true_values, NA_pos); metrics_QRILC <- evaluate_imputation(after_QRILC_imp, true_values, NA_pos); comparison <- rbind(metrics_GSimp, metrics_QRILC); write.csv(comparison, 'imputation_comparison.csv')
```

## Evaluation signals

- Comparison table contains one row per imputation method (GSimp, QRILC, kNN-TN, optionally HM) with consistent metric columns (RMSE, bias, etc.) populated for each.
- RMSE values are computed only at NA_pos indices; values should be non-negative and expressed in the original (back-transformed, unscaled) data scale.
- Bias values (mean imputed value − mean true value) should be close to zero for accurate methods and symmetric around zero across methods.
- Performance metrics allow rank-ordering of methods; the method with lowest RMSE and bias closest to zero is the best performer for the evaluated dataset.
- Output file (CSV/TSV) is parseable and machine-readable, with clear method labels and metric names enabling downstream comparison or visualization.

## Limitations

- Evaluation accuracy depends critically on ground-truth values being truly known; simulated MNAR data may not fully capture real-world censoring mechanisms.
- Results are specific to the dataset, sample size, and missing proportion used; performance ranking may differ for untargeted vs. targeted metabolomics or for datasets with different missingness patterns.
- Metric choice (RMSE vs. bias vs. other measures) affects interpretation; article emphasizes RMSE and bias but does not specify optimal thresholds for metabolomics data.
- GSimp_evaluation.R is not publicly versioned in the repository README; reproducibility may be affected by undocumented changes or parameter defaults not clearly documented.

## Evidence

- [other] Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values.: "Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values."
- [readme] GSimp_evaluation.R contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline.: "**GSimp_evaluation.R** contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline."
- [other] Aggregate results across all three methods into a structured comparison table. Export the comparison table as a CSV or TSV file documenting method-wise performance.: "Aggregate results across all three methods into a structured comparison table. Export the comparison table as a CSV or TSV file documenting method-wise performance."
- [readme] We compared GSimp with other left-censored missing imputation/substitution methods: QRILC (Quantile Regression Imputation of Left-Censored data) imputes missing elements randomly drawing from a truncated distribution estimated by a quantile regression.: "We compared GSimp with other left-censored missing imputation/substitution methods: QRILC (Quantile Regression Imputation of Left-Censored data)"
- [other] Load the imputed matrices (output from GSimp, QRILC, and kNN-TN applied to MNAR-corrupted data) into R. Source the GSimp_evaluation.R script containing the evaluation functions.: "Load the imputed matrices (output from GSimp, QRILC, and kNN-TN applied to MNAR-corrupted data) into R. Source the GSimp_evaluation.R script containing the evaluation functions."
