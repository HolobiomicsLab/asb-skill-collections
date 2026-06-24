---
name: regression-metric-computation-rmse-mae-r2
description: 'Use when you have model predictions and ground-truth labels for a test
  set and need to assess how well the trained model generalizes to unseen data. Typical
  triggers: after executing inference on a held-out test partition, after cross-dataset
  evaluation (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - scikit-learn metrics module
  - PyTorch Geometric
  - enveda/ccs-prediction
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00899-w
  all_source_dois:
  - 10.1186/s13321-024-00899-w
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-metric-computation-rmse-mae-r2

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute root-mean-square error (RMSE), mean absolute error (MAE), and coefficient of determination (R²) to quantify the generalizability and predictive accuracy of regression models on held-out test data. This skill is essential for validating graph neural network models trained for molecular property prediction across independent datasets.

## When to use

Apply this skill when you have model predictions and ground-truth labels for a test set and need to assess how well the trained model generalizes to unseen data. Typical triggers: after executing inference on a held-out test partition, after cross-dataset evaluation (e.g., training on METLIN-CCS and testing on CCSBase), or when comparing baseline models against new approaches.

## When NOT to use

- Input is classification labels (discrete/categorical) rather than continuous numeric predictions — use classification metrics (accuracy, precision, recall, F1, AUC) instead.
- Predictions or labels contain missing values (NaN/inf) — impute, filter, or handle missing data before metric computation.
- Test set is extremely small (n < 10) or highly imbalanced with outliers — RMSE and MAE may be dominated by a few extreme errors; consider robust alternatives (median absolute error, quantile loss) or log-transform the target.

## Inputs

- predicted values (numeric array or column from model inference)
- ground-truth test labels (numeric array or column, same shape as predictions)
- baseline metric values (for reproducibility comparison)

## Outputs

- RMSE (scalar numeric value, same units as target variable)
- MAE (scalar numeric value, same units as target variable)
- R² (scalar numeric value, typically 0–1 range, 1 is perfect prediction)
- aggregated results table with metrics alongside reported baselines

## How to apply

After loading predictions and ground-truth test labels, compute RMSE as the square root of mean squared differences, MAE as the mean of absolute differences, and R² as the proportion of variance explained by the model. These metrics should be computed on the full test set without filtering or subsetting. The workflow: (1) align predicted and ground-truth values by index; (2) compute element-wise differences; (3) apply the metric formulas (RMSE = sqrt(mean((y_pred - y_true)²)), MAE = mean(|y_pred - y_true|), R² = 1 - SS_res / SS_tot); (4) report each metric as a scalar value; (5) compare results against baseline values reported in the paper to verify reproducibility. These metrics are model-agnostic and work for any continuous-valued prediction task.

## Related tools

- **scikit-learn metrics module** (Provides mean_squared_error, mean_absolute_error, r2_score functions for direct metric computation)
- **PyTorch Geometric** (Graph neural network framework used to train the CCS prediction model whose outputs are evaluated by these metrics)
- **enveda/ccs-prediction** (Repository containing pre-trained GNN checkpoints, test data, and scripts to generate predictions on which metrics are computed) — https://github.com/enveda/ccs-prediction

## Examples

```
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score; rmse = sqrt(mean_squared_error(y_true, y_pred)); mae = mean_absolute_error(y_true, y_pred); r2 = r2_score(y_true, y_pred); print(f'RMSE: {rmse}, MAE: {mae}, R²: {r2}')
```

## Evaluation signals

- RMSE value is strictly non-negative (≥ 0) and has the same physical units as the target (e.g., collision cross section in Ų).
- MAE value is strictly non-negative (≥ 0), ≤ RMSE (MAE ≤ RMSE by Cauchy–Schwarz inequality), and expressed in target units.
- R² value lies in [−∞, 1]; R² = 1 indicates perfect predictions; R² = 0 indicates the model explains no more variance than predicting the mean; R² < 0 indicates the model performs worse than a constant baseline.
- Reported metrics match (or closely reproduce, within numerical precision) the baseline values listed in the paper for the same train–test split combination.
- Metric values are computed only on the designated test set partition (not train or validation) to avoid overfitting bias.

## Limitations

- RMSE is sensitive to outliers; a single large prediction error disproportionately increases RMSE. If the test set contains extreme outliers, report MAE alongside RMSE or use robust loss metrics.
- R² is undefined or misleading when SS_tot = 0 (all ground-truth labels are identical); always verify that test labels have non-zero variance before interpreting R².
- These metrics assume predictions are on the same scale as ground-truth labels; if predictions were made on log-transformed or scaled data, back-transform before metric computation to ensure interpretability.
- Cross-dataset evaluation (e.g., training on METLIN-CCS and testing on CCSBase) may show large metric gaps due to domain shift or instrumental differences, not model failure; metrics alone do not diagnose the root cause.

## Evidence

- [other] Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels.: "Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels."
- [other] Execute model inference on the test set using the trained GNN to generate collision cross section predictions.: "Execute model inference on the test set using the trained GNN to generate collision cross section predictions."
- [other] Aggregate results and tabulate metric values alongside reported baseline values for reproducibility verification.: "Aggregate results and tabulate metric values alongside reported baseline values for reproducibility verification."
- [readme] Run the notebooks located in the `notebooks` corresponding to each analysis.: "Run the notebooks located in the `notebooks` corresponding to each analysis."
