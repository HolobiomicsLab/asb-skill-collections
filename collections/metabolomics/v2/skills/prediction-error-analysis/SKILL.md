---
name: prediction-error-analysis
description: Use when when you have trained multiple machine learning regressors on the same prediction task (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - RDKit
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

# prediction-error-analysis

## Summary

Comparative evaluation of machine learning model predictions by computing prediction errors (mean absolute error, median absolute error) across different feature sets or model configurations on a held-out test set. This skill enables quantitative assessment of whether different molecular representations (descriptors, fingerprints, or combinations) produce meaningfully different retention time prediction accuracy.

## When to use

When you have trained multiple machine learning regressors on the same prediction task (e.g., retention time prediction) using different feature configurations or molecular representations, and you need to determine which configuration produces the lowest prediction errors and whether the differences are meaningful. Specifically applicable when comparing descriptor-only, fingerprint-only, or combined feature sets for metabolite annotation or retention time forecasting.

## When NOT to use

- Training data and test data overlap or are not independently sampled — error estimates will be unreliably optimistic
- Only one model or feature set has been trained; no meaningful comparison is possible
- Input is already a feature table or preprocessed descriptor/fingerprint matrix rather than raw molecular structures — error analysis requires end-to-end trained models

## Inputs

- trained machine learning regressors (one per feature set or configuration)
- held-out test set with molecular structures and experimental retention times
- model predictions on test set (continuous values)

## Outputs

- mean absolute error (MAE) per model configuration with ± standard deviation
- median absolute error (MedAE) per model configuration with ± standard deviation
- ranked comparison table of feature sets or model architectures
- error distribution visualization (e.g., histogram or box plot across configurations)

## How to apply

Train independent machine learning regressors on each feature set or model configuration using the same training data and hyperparameters. Apply each trained model to a held-out test set containing ground-truth labels (e.g., experimental retention times). For each model, compute mean absolute error (MAE) and median absolute error (MedAE) by comparing predictions to observed values. Compare error distributions across all configurations and rank them by both central tendency and dispersion (±standard deviation). Use these metrics to identify the feature set or model that achieves lowest error and most stable predictions. The rationale is that fingerprints often encode structural patterns more effectively than raw descriptors for chromatographic properties, but empirical error comparison on your specific dataset and test split is the only valid criterion.

## Related tools

- **alvaDesc** (Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) that serve as input feature sets for training regressors prior to error analysis) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative fingerprint generation tool for training machine learning models whose predictions are then compared via error metrics)

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models; python cmmrt/rt/test_model.py --model_dir saved_models --test_data SMRT_test.csv --output_errors rt_errors.csv
```

## Evaluation signals

- Error metrics (MAE, MedAE) computed on a held-out test set independent of training and hyperparameter tuning splits
- Standard deviation reported alongside mean and median errors; variability should be small relative to central value (e.g., ±1–3 s for retention time in seconds)
- Ranking of configurations is consistent across both MAE and MedAE; if fingerprints outperform descriptors, both metrics should show the same trend
- Error distributions should show fingerprint-only and combined models producing lower error quantiles (25th, 50th, 75th percentiles) than descriptor-only models
- Comparison is performed on the same test set and same models; no retraining or data leakage between configurations

## Limitations

- Error comparison is sensitive to train/test split; nested cross-validation is recommended for robust estimates, but single held-out test results may be unstable with small test sets
- The superiority of fingerprints over descriptors observed in this study (METLIN SMRT, 80,038 molecules, MACCS/ECFP/PFP) may not generalize to other datasets, chromatographic methods, or molecular domains with different structural diversity
- Requires that all competing models are trained with the same hyperparameters and stopping criteria; unfair hyperparameter tuning per configuration will bias error comparisons
- Mean and median absolute error do not capture prediction uncertainty; complementary methods (e.g., quantile regression, Bayesian predictive intervals) are needed to assess whether prediction confidence varies across feature sets

## Evidence

- [intro] fingerprints tend to perform better than descriptors alone or combined: "Results suggest that fingerprints tend to perform better."
- [intro] MAE and MedAE as error metrics: "Compute prediction errors (mean absolute error and median absolute error) for each of the three trained models on a held-out test set."
- [intro] three feature configurations compared independently: "Train machine learning regressors independently on three feature sets: (a) descriptors only, (b) fingerprints only, (c) both descriptors and fingerprints combined."
- [intro] benchmark results on METLIN SMRT: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] fingerprint types used for comparison: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software. The models were trained using only"
