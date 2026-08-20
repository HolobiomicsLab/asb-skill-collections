---
name: regression-model-evaluation-absolute-error
description: Use when after training a regression model on labeled continuous data
  (e.g., retention times, physicochemical properties) and generating predictions on
  held-out test data, compute MAE and MedAE to assess model generalization and compare
  against published reference performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - alvaDesc
  - cmmrt
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
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

# regression-model-evaluation-absolute-error

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate regression model performance on continuous-valued predictions (e.g., retention time) by computing mean absolute error (MAE) and median absolute error (MedAE) with confidence intervals. This skill enables quantitative assessment of prediction accuracy and reproducibility of model performance against reference benchmarks.

## When to use

After training a regression model on labeled continuous data (e.g., retention times, physicochemical properties) and generating predictions on held-out test data, compute MAE and MedAE to assess model generalization and compare against published reference performance. Use this skill when you need to report point estimates and confidence intervals for absolute deviations rather than squared errors, particularly when median robustness to outliers is important alongside mean performance.

## When NOT to use

- Input predictions are classification probabilities or class labels rather than continuous values.
- Regression target is binary or ordinal (use classification metrics instead).
- Test set is imbalanced or heavily weighted; MAE/MedAE alone do not account for sample weighting—report weighted variants or stratified performance.

## Inputs

- Predicted continuous values (vector)
- Ground-truth continuous labels (vector)
- Held-out test dataset or cross-validation fold predictions

## Outputs

- Mean absolute error (MAE) with confidence interval (scalar ± uncertainty)
- Median absolute error (MedAE) with confidence interval (scalar ± uncertainty)
- Error distribution (vector of absolute deviations)

## How to apply

On held-out test predictions and ground-truth labels, compute mean absolute error (MAE) as the average of |y_pred - y_true| across all samples, and median absolute error (MedAE) as the median of the same absolute deviations. Generate confidence intervals (e.g., ±1.2 s in the reference study) by bootstrap resampling or cross-validation fold statistics. Report both metrics with their uncertainty bounds and compare against the reference benchmark (MAE 39.2±1.2 s, MedAE 17.2±0.9 s for METLIN SMRT retention time prediction). Verify that the model generalizes by ensuring test-set errors align with or improve upon training/validation errors and match the reference performance within stated confidence intervals.

## Related tools

- **alvaDesc** (Generates molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) used as input features for the retention time regression model whose performance is evaluated by this skill) — https://www.alvascience.com/alvadesc/
- **cmmrt** (Reference implementation of retention time predictors and evaluation workflows including MAE/MedAE computation on METLIN SMRT dataset) — https://github.com/constantino-garcia/cmmrt

## Examples

```
from sklearn.metrics import mean_absolute_error; mae = mean_absolute_error(y_test, y_pred); med_ae = np.median(np.abs(y_pred - y_test)); print(f'MAE: {mae:.1f}±{bootstrap_ci[1]-mae:.1f} s, MedAE: {med_ae:.1f}±{bootstrap_ci_med[1]-med_ae:.1f} s')
```

## Evaluation signals

- MAE and MedAE values match the reference benchmark (39.2±1.2 s and 17.2±0.9 s respectively) within stated confidence intervals for the METLIN SMRT dataset.
- Confidence intervals are symmetric or justified (e.g., from bootstrap or k-fold cross-validation with n ≥ 10 folds) and properly account for test-set variability.
- MedAE is substantially smaller than MAE (as in the reference: 17.2 vs 39.2 s), indicating the error distribution is right-skewed and median provides robustness to outliers.
- Test-set MAE/MedAE do not exceed training/validation estimates by >10%, confirming the model generalizes and is not severely overfitting.
- Error distribution is inspected visually or via quantile plots to confirm absence of bimodal or pathological distributions that would invalidate simple summary statistics.

## Limitations

- MAE and MedAE are insensitive to systematic bias; report mean prediction error separately to detect whether model tends to over- or under-predict.
- Confidence intervals depend on sample size and resampling scheme; small test sets (<50 samples) yield wide intervals and unreliable estimates.
- Outlier predictions dominate MAE but not MedAE; report both metrics but do not rely on MAE alone if high-stakes predictions require robustness.
- No significance test is provided by MAE/MedAE alone; use permutation testing or cross-validation to assess whether improvements are statistically meaningful.
- Reference benchmark (39.2±1.2 s, 17.2±0.9 s) is specific to METLIN SMRT with heavily regularized DNN + cosine annealing warm restarts + stochastic weight averaging; other datasets, models, or training procedures will yield different error ranges.

## Evidence

- [intro] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2±0.9 s on retention time prediction.: "A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2±0.9 s"
- [intro] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [other] Evaluate the trained model on held-out test data, computing mean absolute error and median absolute error.: "Evaluate the trained model on held-out test data, computing mean absolute error and median absolute error."
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively."
