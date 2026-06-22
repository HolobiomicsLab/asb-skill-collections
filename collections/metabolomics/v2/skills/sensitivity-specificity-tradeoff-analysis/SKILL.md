---
name: sensitivity-specificity-tradeoff-analysis
description: Use when you have a trained neural network model and a labelled validation dataset (with high-quality and low-quality peak annotations), and you need to determine the optimal probability threshold that maximizes the difference between true positive rate and false positive rate for classifying MS1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - NeatMS
  - Python
  - pandas
  - scikit-learn
  - NumPy
  - Keras/TensorFlow
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- import pandas as pd
- from sklearn.metrics import auc
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sensitivity-specificity-tradeoff-analysis

## Summary

Compute optimal classification thresholds for neural network-based peak filtering by analyzing the tradeoff between true positive and false positive rates across a range of probability thresholds. This skill is essential when deploying trained classifiers to LCMS peak datasets where the cost of false positives must be balanced against detection sensitivity.

## When to use

You have a trained neural network model and a labelled validation dataset (with high-quality and low-quality peak annotations), and you need to determine the optimal probability threshold that maximizes the difference between true positive rate and false positive rate for classifying MS1 peaks. Use this skill when you want to empirically derive a threshold value rather than relying on default cutoffs.

## When NOT to use

- Your dataset has no labelled peaks or no ground-truth High_quality/Low_quality annotations — the method requires labelled validation data to compute true and false positive rates.
- You are working with a different classifier type (non-neural-network or external model) — this skill is specific to NeatMS neural network handlers.
- You only have a training set without a separate validation set — using the training set to select thresholds risks overfitting; a held-out validation cohort is required.

## Inputs

- trained NeatMS neural network model (Keras/TensorFlow)
- labelled peak validation dataset with High_quality and Low_quality annotations
- NN_handler object initialized with the model

## Outputs

- optimal scalar probability threshold value (e.g., 0.22)
- true vs. false positive rate dataframe (from get_true_vs_false_positive_df)
- per-threshold evaluation metrics

## How to apply

Load the trained NeatMS neural network model and prepare labelled peak batches from your validation dataset using NN_handler methods. Call get_threshold() with label='High_quality' to internally compute true vs. false positive rates across all probability thresholds. The method evaluates the objective function (True positives minus False positives) at each threshold and selects the scalar threshold value that maximizes this difference. Compare the returned threshold against reference values (e.g., 0.22 for the default model) to validate consistency. The rationale is that maximizing (TP − FP) identifies the threshold where the net benefit of correct identifications outweighs false alarms, accounting for the specific dataset characteristics.

## Related tools

- **NeatMS** (neural network model loader and threshold optimization via get_threshold() method) — https://github.com/bihealth/NeatMS
- **scikit-learn** (metrics computation (e.g., auc, roc-like evaluation))
- **pandas** (dataframe handling for true/false positive rate tables)
- **NumPy** (numerical array operations for threshold sweeps)
- **Keras/TensorFlow** (underlying neural network framework for model inference)

## Examples

```
from neatms import NN_handler; nn_handler = NN_handler.create_model(model_path='path/to/model'); optimal_threshold = nn_handler.get_threshold(validation_data, label='High_quality')
```

## Evaluation signals

- The returned threshold value matches or is close to the reference threshold for the model (e.g., 0.22 for default NeatMS model), indicating consistent threshold selection logic.
- The true vs. false positive rate dataframe returned by get_true_vs_false_positive_df covers a reasonable range of thresholds (e.g., 0.0 to 1.0) with smooth monotonic behavior: TP rate decreases and FP rate increases as threshold increases.
- The selected threshold corresponds to the peak of the (TP − FP) curve, verified by manually inspecting the dataframe to confirm no higher TP − FP value exists at other thresholds.
- When applied to the validation dataset, peaks classified as high-quality above the returned threshold have higher empirical precision and recall compared to using a naive threshold (e.g., 0.5).
- The threshold value is scalar, numeric, and within the valid probability range [0, 1].

## Limitations

- The method requires a labelled validation dataset with sufficient high-quality and low-quality examples; severely imbalanced datasets may produce unstable threshold estimates.
- The objective function (TP − FP) does not account for class imbalance or asymmetric costs; if false positives are much more costly than false negatives (or vice versa), a weighted optimization criterion may be preferable.
- The threshold is optimized for the specific validation cohort and may not generalize to new datasets with different peak characteristics or instrument parameters.
- NeatMS does not provide automated callbacks to halt training; the user must manually manage training state before threshold optimization, and resuming training after threshold selection may invalidate the threshold.

## Evidence

- [other] Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [other] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [readme] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
- [other] Verify the returned threshold matches the expected reference value (0.22 for the default model).: "Verify the returned threshold matches the expected reference value (0.22 for the default model)."
- [other] Load a trained NeatMS neural network model and its associated validation dataset using NN_handler.create_model() and prepare labelled peak batches.: "Load a trained NeatMS neural network model and its associated validation dataset using NN_handler.create_model() and prepare labelled peak batches."
