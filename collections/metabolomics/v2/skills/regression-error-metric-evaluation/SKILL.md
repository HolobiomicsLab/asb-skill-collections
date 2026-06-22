---
name: regression-error-metric-evaluation
description: 'Use when when you have trained multiple regression models (e.g., using different feature sets: descriptors-only, fingerprints-only, or combined) on the same training data and need to objectively rank their generalization performance on unseen test data.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_3318
  - http://edamontology.org/topic_0602
  tools:
  - alvaDesc
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Regression Error Metric Evaluation

## Summary

Quantitative assessment of machine learning regression model performance using mean absolute error (MAE) and median absolute error (MdAE) computed on held-out test sets. This skill is essential for comparing model architectures, feature representations, and hyperparameter choices in predictive tasks where absolute prediction accuracy matters.

## When to use

When you have trained multiple regression models (e.g., using different feature sets: descriptors-only, fingerprints-only, or combined) on the same training data and need to objectively rank their generalization performance on unseen test data. Apply this skill whenever comparing competing model architectures or feature engineering choices to determine which reduces prediction error most effectively.

## When NOT to use

- Model has not yet been applied to a held-out test set; use cross-validation or internal validation metrics first.
- Test set contains fewer than ~20 samples; error estimates become unreliable and confidence intervals are wide.
- Input data is categorical or classification task; use classification metrics (accuracy, F1, ROC-AUC) instead.

## Inputs

- Test set retention times (reference/experimental values)
- Model predictions on test set (point estimates)
- Training/validation histories (for optional confidence interval computation)

## Outputs

- Mean absolute error (MAE) with uncertainty estimate (e.g., ±1.2 s)
- Median absolute error (MdAE) with uncertainty estimate (e.g., ±0.9 s)
- Ranked comparison table of models by error metrics
- Per-sample absolute error distribution

## How to apply

After training a regression model on the training partition, apply it to generate predictions on the held-out test set. Compute the absolute error for each test sample as |predicted_value − reference_value|. Calculate mean absolute error (MAE) as the arithmetic mean of all absolute errors, and median absolute error (MdAE) as the 50th percentile of the absolute error distribution. Report both metrics with confidence intervals (e.g., ±1.2 s) derived from cross-validation or bootstrap resampling. Use MAE to assess average prediction quality and MdAE to assess robustness to outliers. Compare metrics across conditions (e.g., descriptors-only vs. fingerprints-only vs. combined); the model with lower MAE and MdAE is preferred. If models are nested (e.g., one uses a subset of the other's features), verify that performance differences are statistically significant before claiming one is superior.

## Related tools

- **alvaDesc** (Feature generation (descriptors and fingerprints) for input to regression models whose error is subsequently evaluated) — https://www.alvascience.com/alvadesc/

## Examples

```
# After training DNN on SMRT fingerprints, evaluate on test set
from sklearn.metrics import mean_absolute_error; import numpy as np
y_true = test_rts; y_pred = model.predict(test_fingerprints)
mae = mean_absolute_error(y_true, y_pred); mde = np.median(np.abs(y_true - y_pred))
print(f'MAE: {mae:.1f}±1.2 s, MdAE: {mde:.1f}±0.9 s')
```

## Evaluation signals

- MAE and MdAE values are in the same units as the target variable (seconds for retention time) and are positive.
- MdAE ≤ MAE (median error should not exceed mean error).
- Uncertainty estimates (confidence intervals) are non-zero and consistent with the spread of cross-validation or bootstrap runs.
- Error distributions are examined for outliers; extreme predictions are flagged and can be traced back to molecules with unusual structural properties.
- Model with lower MAE/MdAE on test set also shows lower error on independent validation folds during cross-validation (no sign of overfitting to test set).

## Limitations

- MAE and MdAE assume symmetric error distributions; highly skewed prediction errors (e.g., systematic bias for retained vs. unretained molecules) may not be fully captured by these summary statistics.
- Error metrics do not indicate which chemical structures or property ranges are poorly predicted; post-hoc error analysis (e.g., binning by molecular weight) is needed to diagnose failure modes.
- Confidence intervals depend on the number of test samples and the variability of the underlying model; small test sets yield wide intervals that limit decision-making power.
- Comparing MAE across datasets with different retention time scales (e.g., different chromatographic methods) requires normalization; raw MAE alone is not portable.

## Evidence

- [other] Fingerprints tend to perform better than descriptors alone across the three feature conditions tested (descriptors only, fingerprints only, and both types combined).: "Results suggest that fingerprints tend to perform better"
- [other] The best results were achieved by a heavily regularized DNN with specific training strategies, yielding quantified error metrics.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [other] The three feature sets (descriptors only, fingerprints only, combined) are evaluated and ranked by error metrics.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously"
- [other] Test set performance is the criterion for model selection in retention time prediction.: "record mean absolute error (MAE) and median absolute error (MdAE)"
