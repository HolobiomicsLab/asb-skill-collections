---
name: classification-model-performance-evaluation
description: Use when after fitting and optimizing a MB-PLS model on training data, apply this skill to the held-out test set (typically 10% of the original sample) to obtain unbiased performance estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_2269
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - MamsiPls
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent prediction modeling for Python.'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classification-model-performance-evaluation

## Summary

Evaluate a trained multi-block PLS discriminant classifier on an independent test set by computing accuracy, recall, specificity, F1-score, and area under the receiver operating characteristic curve (AUC). This skill quantifies generalization performance and identifies which evaluation metric best represents the model's discriminative capacity for the biological or clinical endpoint.

## When to use

After fitting and optimizing a MB-PLS model on training data, apply this skill to the held-out test set (typically 10% of the original sample) to obtain unbiased performance estimates. Use it when you need to report model efficacy, compare competing models, or validate that the model generalizes to new samples not seen during training or cross-validation.

## When NOT to use

- Do not apply this skill if the test set has not been held out during model training and hyperparameter selection; performance estimates will be optimistically biased.
- Do not use this skill to evaluate model performance on the training or cross-validation set itself—use cross-validation error instead to detect overfitting.
- Do not apply this skill if the test set contains missing values or features with zero variance; preprocess and impute before evaluation.

## Inputs

- Fitted MamsiPls model object with optimal latent variable count
- Test set feature matrix (X_test): multi-assay LC-MS intensity data with assay-specific prefixes (e.g., HPOS_, LPOS_, LNEG_)
- Test set response vector (y_test): binary class labels (0/1) or continuous phenotype, same length as X_test

## Outputs

- Classification metrics table: accuracy, recall, specificity, F1-score, AUC (numeric scalars, typically 0–1 range)
- Confusion matrix (2×2 for binary classification): TP, FP, FN, TN counts
- ROC curve data (optional): false positive rates and true positive rates for plotting

## How to apply

Call MamsiPls.evaluate_class_model() on the independent test set (X_test, y_test) after the MB-PLS model has been refitted with the optimal number of latent variables determined via cross-validation. The method returns a structured set of classification metrics—accuracy (fraction of correct predictions), recall (sensitivity; true positive rate), specificity (true negative rate), F1-score (harmonic mean of precision and recall), and AUC (probability that the model ranks a random positive sample higher than a random negative sample). Record all five metrics in a results table and use AUC as the primary metric for model ranking when class imbalance is present, since it is invariant to decision threshold shifts. Report 95% confidence intervals or standard errors where possible, and ensure test set samples are completely independent from training and cross-validation subsets.

## Related tools

- **MamsiPls** (Fitted multi-block PLS classifier model object; provides evaluate_class_model() method to compute test-set performance metrics) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Optional: provides roc_auc_score, confusion_matrix, classification_report, and other standard metrics for validation)
- **pandas** (Organize and export evaluation metrics table (accuracy, recall, specificity, F1, AUC) for downstream reporting)

## Examples

```
mamsipls.evaluate_class_model([hpos_test, lpos_test, lneg_test], y_test)
```

## Evaluation signals

- All five metrics (accuracy, recall, specificity, F1-score, AUC) are computed and reported as scalar values in [0, 1] range; no NaN or inf values.
- Confusion matrix sums to total test set size (n_test); TP + FP + TN + FN = len(y_test).
- Recall and specificity are complementary: high recall with low specificity suggests the model predicts the positive class too liberally; check class imbalance in y_test.
- AUC is monotonic with model quality; AUC > 0.5 indicates better-than-random discrimination; AUC = 1.0 indicates perfect separation (rare in real data).
- Test set metrics should be reasonably consistent with cross-validation metrics from the training phase; large divergence (e.g., >10% relative difference in AUC) suggests overfitting or poor generalization.

## Limitations

- Classification metrics assume clean, well-labeled test data; mislabeled or missing outcome values will distort all metrics.
- Accuracy is insensitive to class imbalance; if test set has highly skewed phenotype distribution (e.g., 95% negative), use AUC or F1-score instead.
- Test set must be sufficiently large (typically n_test ≥ 50 for binary classification) to obtain stable, statistically reliable estimates; very small test sets yield noisy metrics.
- The framework was tested on metabolomics phenotyping data (e.g., gender, disease status); applicability to other LC-MS use cases (e.g., continuous biomarkers, regression endpoints) is untested.

## Evidence

- [methods] Evaluate final model on independent testing dataset: "### Evaluate Final Model"
- [methods] Recording accuracy, recall, specificity, F1-score, and AUC metrics.: "recording accuracy, recall, specificity, F1-score, and AUC"
- [methods] Using evaluate_class_model method to generate test-set predictions.: "evaluate on independent test set using MamsiPls.evaluate_class_model()"
- [intro] Multi-Block PLS for discriminant analysis on metabolomics data.: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets"
- [methods] Train-test split strategy maintaining sample correspondence.: "Split data into training (90%) and testing (10%) subsets using scikit-learn's train_test_split with random_state=42, maintaining sample correspondence across blocks."
