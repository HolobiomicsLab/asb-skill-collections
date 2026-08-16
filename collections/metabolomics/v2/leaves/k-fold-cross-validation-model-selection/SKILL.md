---
name: k-fold-cross-validation-model-selection
description: Use when when fitting a multi-block PLS discriminant model on multi-assay
  LC-MS metabolomics data and you need to determine the number of latent variables
  to retain without overfitting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - MamsiPls
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent
  prediction modeling for Python.'
- import pandas as pd
- import numpy as np
- from sklearn.model_selection import train_test_split
- from matplotlib import pyplot as plt
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# k-fold-cross-validation-model-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use k-fold cross-validation to estimate the optimal number of latent variables in a multi-block PLS model by iteratively training on k−1 folds and evaluating on the held-out fold, selecting the latent variable count where model performance plateaus. This prevents overfitting and provides a data-driven criterion for model complexity in multi-assay metabolomics integration.

## When to use

When fitting a multi-block PLS discriminant model on multi-assay LC-MS metabolomics data and you need to determine the number of latent variables to retain without overfitting. Apply this skill after train-test splitting but before final model evaluation, to estimate the latent variable count that maximizes generalization performance (e.g., AUC) across the training cohort.

## When NOT to use

- Latent variable count is already known or predetermined by prior domain knowledge or literature.
- Input is a small or sparse dataset where k-fold splitting leaves insufficient samples per fold for stable estimation.
- Response variable is continuous (use regression cross-validation metrics like RMSE instead) and linear model performance does not plateau meaningfully.

## Inputs

- Multi-assay LC-MS intensity matrices (e.g., HPOS, LPOS, LNEG blocks) with assay-specific column name prefixes
- Binary or multiclass response vector (y) corresponding to samples in the intensity matrices
- Training subset of data (typically 80–90% of total samples)

## Outputs

- Optimal number of latent variables (integer)
- Cross-validated performance scores (e.g., AUC) as a function of latent variable count
- Performance plateau identification (vector of metric values per LV)

## How to apply

Split the training data into k folds (typically k=5). For each candidate number of latent variables, fit the MB-PLS model on k−1 training folds, evaluate on the held-out fold using a performance metric (AUC is recommended for classification), and record the metric. Aggregate scores across folds and identify the latent variable count where performance plateaus or ceases to improve meaningfully—use a plateau threshold (e.g., 0.01 improvement) to avoid retaining unnecessary latent variables that add no predictive gain. This cross-validated estimate guards against overfitting caused by tuning on the full training set. Refit the final model using the optimal latent variable count on all training data, then evaluate once on the independent test set.

## Related tools

- **mbpls** (Implements the MB-PLS model fitting and the estimate_lv() method for k-fold cross-validation of latent variable count) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Provides train_test_split for initial data partitioning and can support k-fold cross-validation utilities)
- **MamsiPls** (High-level wrapper that exposes the estimate_lv() method for automated k-fold cross-validation with AUC metric) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
mamsipls.estimate_lv([hpos_train, lpos_train, lneg_train], y_train, metric='auc')
```

## Evaluation signals

- Cross-validated performance metric (AUC) reaches a plateau: successive increases in latent variables produce improvement < plateau_threshold (e.g., < 0.01 change in AUC).
- Selected latent variable count is lower than the maximum tested (indicating the model did not simply retain all candidates), preventing unnecessary complexity.
- Final model evaluated on independent test set shows performance (accuracy, recall, specificity, F1-score, AUC) consistent with cross-validation estimates, confirming no overfitting during latent variable selection.
- Cross-validation folds are balanced in size and sample composition; each fold contains representative samples from all outcome classes.
- Plateau threshold and number of folds are justified and reported explicitly in methods, ensuring reproducibility.

## Limitations

- K-fold cross-validation is computationally expensive for very large datasets; larger k values (e.g., k=10) increase runtime proportionally.
- The choice of plateau_threshold is somewhat arbitrary; suboptimal thresholds may select too few or too many latent variables depending on the signal-to-noise ratio in the data.
- Small sample size relative to the number of features (common in LC-MS metabolomics) can lead to unstable cross-validation estimates; consider stratified k-fold to maintain outcome class balance.
- Performance metric choice (AUC, accuracy, etc.) influences the optimal latent variable count; different metrics may suggest different optima, requiring justification of metric selection.

## Evidence

- [other] Estimate optimal number of latent variables using k-fold cross-validation (n_splits=5) with AUC metric via MamsiPls.estimate_lv(), identifying the model plateau threshold (plateau_threshold=0.01).: "Estimate optimal number of latent variables using k-fold cross-validation (n_splits=5) with AUC metric via MamsiPls.estimate_lv(), identifying the model plateau threshold (plateau_threshold=0.01)."
- [methods] For each candidate number of latent variables, fit the MB-PLS model on k−1 training folds, evaluate on the held-out fold using a performance metric (AUC is recommended for classification), and record the metric.: "estimate_lv([hpos_train, lpos_train, lneg_train], y_train, metric='auc')"
- [intro] The framework was tested on metabolomics phenotyping data with multi-assay LC-MS datasets: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data"
- [other] Refit MB-PLS with optimal latent variable count and evaluate on independent test set: "Refit MB-PLS with optimal latent variable count and evaluate on independent test set using MamsiPls.evaluate_class_model()"
- [readme] K-fold cross-validation prevents overfitting by providing independent evaluation folds: "You can install MAMSI from PyPI using pip: `pip install mamsi`"
