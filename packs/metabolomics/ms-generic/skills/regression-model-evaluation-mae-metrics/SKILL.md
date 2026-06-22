---
name: regression-model-evaluation-mae-metrics
description: Use when when you have trained a regression model on experimental retention times or similar continuous molecular property predictions and need to quantify its generalization performance on held-out test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - alvaDesc
  - cmmrt
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-model-evaluation-mae-metrics

## Summary

Evaluate regression models for continuous-valued prediction tasks (e.g., retention time) by computing mean absolute error (MAE) and median absolute error (MdAE) on held-out test sets, with reported uncertainty bounds. This skill is essential for assessing predictive performance when absolute deviations from ground truth are the primary concern.

## When to use

When you have trained a regression model on experimental retention times or similar continuous molecular property predictions and need to quantify its generalization performance on held-out test data. Use this skill when MAE and MdAE are the primary evaluation metrics of interest, particularly for retention time prediction on chromatographic or mass spectrometry datasets where symmetric error penalties are preferred over squared-error metrics.

## When NOT to use

- When the model has not been trained on the same dataset or feature engineering pipeline; evaluation must use consistent preprocessing.
- When test set is not truly held-out (e.g., it overlaps with training data due to improper cross-validation setup).
- When squared-error metrics (MSE, RMSE) or classification metrics (accuracy, AUC) are the required evaluation standard instead of absolute error.

## Inputs

- trained regression model (fitted on molecular descriptors and/or fingerprints)
- held-out test set with molecular structures/features and experimental retention times
- predictions from the trained model on test set compounds

## Outputs

- mean absolute error (MAE) with uncertainty bounds (e.g., 39.2±1.2 s)
- median absolute error (MdAE) with uncertainty bounds (e.g., 17.2±0.9 s)
- absolute error distribution per test sample

## How to apply

After training a regression model (e.g., a heavily regularized DNN with cosine annealing warm restarts and stochastic weight averaging), evaluate it on a held-out test set by computing the absolute difference between predicted and observed retention times for each molecule. Calculate mean absolute error as the arithmetic mean of all absolute differences, and median absolute error as the middle value of the sorted absolute differences. Report both metrics with their uncertainty bounds (typically ±1 standard deviation estimated via bootstrap or cross-validation). The rationale is that MAE is robust to outliers and interpretable in the original units (seconds for retention time), while MdAE provides a resistant measure of central tendency unaffected by extreme predictions.

## Related tools

- **alvaDesc** (generates molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) used as input features for the regression model being evaluated) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Python package implementing retention time prediction pipeline including model training and evaluation with MAE/MdAE metrics) — https://github.com/constantino-garcia/cmmrt

## Evaluation signals

- MAE and MdAE values are strictly non-negative and expressed in the same units as the target (seconds for retention time).
- MdAE ≤ MAE (median absolute error should be less than or equal to mean absolute error due to robustness to outliers).
- Reported uncertainty bounds (e.g., ±1.2 s) are consistent with bootstrap or k-fold cross-validation estimates and typically represent ~1 standard deviation.
- Absolute error distribution has no systematic bias (mean of signed residuals ≈ 0) and no obvious outliers introduced by data leakage.
- Test set performance metrics are computed only on samples not used during model training, hyperparameter tuning, or learning rate scheduling.

## Limitations

- MAE and MdAE assume that all prediction errors are equally important; they do not penalize large errors more heavily than small errors (unlike MSE/RMSE). Use with caution if very large deviations are more costly.
- Uncertainty bounds depend on the stability of the model and the representativeness of the test set; small or biased test sets may yield unreliable confidence intervals.
- For retention time prediction specifically, model performance may degrade on out-of-distribution molecules or chromatographic conditions not represented in training data (METLIN SMRT).
- The reported uncertainties (±1.2 s, ±0.9 s) are tied to the specific DNN architecture and hyperparameters; different regularization or training procedures will produce different confidence ranges.

## Evidence

- [intro] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s and median absolute error of 17.2 ± 0.9 s on retention time prediction.: "A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s and median absolute error of 17.2 ± 0.9 s"
- [other] Evaluate trained model on held-out test set and compute mean absolute error (MAE) and median absolute error (MdAE) with reported uncertainties (±1.2 s and ±0.9 s respectively).: "Evaluate trained model on held-out test set and compute mean absolute error (MAE) and median absolute error (MdAE) with reported uncertainties (±1.2 s and ±0.9 s respectively)"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
