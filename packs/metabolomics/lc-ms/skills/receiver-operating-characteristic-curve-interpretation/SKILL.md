---
name: receiver-operating-characteristic-curve-interpretation
description: Use when you have a trained NeatMS neural network model and labelled peak validation data, and need to select an operational classification threshold or understand how TPR and FPR vary across probability thresholds (e.g., 0.00–0.99).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NeatMS
  - Python
  - pandas
  - scikit-learn
  - NumPy
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

# receiver-operating-characteristic-curve-interpretation

## Summary

Interpret ROC curves and extract threshold-dependent classification metrics (TPR, FPR, precision) from a trained neural network classifier to understand the trade-off between true and false positive rates across probability thresholds. This skill is essential for selecting optimal decision thresholds and evaluating classifier performance on imbalanced MS1 peak datasets.

## When to use

You have a trained NeatMS neural network model and labelled peak validation data, and need to select an operational classification threshold or understand how TPR and FPR vary across probability thresholds (e.g., 0.00–0.99). Use this skill when optimizing peak filtering to balance retention of true positives (High_quality peaks) against rejection of false positives (Low_quality and Noise peaks).

## When NOT to use

- Input is a raw MS1 feature table without neural network probability scores or labels — use peak annotation/labelling skill first.
- You have only unlabelled data and no validation set — ROC interpretation requires ground-truth labels.
- Your goal is model training rather than threshold selection or performance evaluation — use model training workflow instead.

## Inputs

- Trained NeatMS neural network model (.h5 file)
- Labelled peak dataset with High_quality / Low_quality / Noise annotations
- Probability threshold value(s) for query (scalar or range 0.00–0.99)

## Outputs

- True vs. False Positive rate DataFrame (threshold-indexed)
- Optimal classification threshold scalar (from get_threshold())
- TPR, FPR, False_low, False_noise metrics at specified thresholds
- ROC-equivalent threshold-metric table for visualization

## How to apply

Load a trained NeatMS model (.h5 format) via nn_handler.create_model() and call nn_handler.get_true_vs_false_positive_df(label='High_quality') to generate a threshold-dependent recall table. This method computes True Positive Rate (TPR), False Positive Rate (FPR), and breakdowns of false positives (Low_quality vs. Noise) across probability thresholds from 0.00 to 0.99. Extract rows at your target threshold(s) and inspect the True, False, False_low, and False_noise columns. For threshold optimization, call nn_handler.get_threshold(), which internally uses the same recall table and selects the threshold maximizing (TP − FP). Interpret the resulting metrics in the context of your analytical goal: high TPR with low FPR indicates good separation; inspect False_low and False_noise ratios to understand false positive composition. Compare retrieved values against reference thresholds (e.g., 0.22 for the default model, 1.0 TPR and 0.440 FPR at threshold 0.01) to validate model consistency.

## Related tools

- **NeatMS** (Provides nn_handler.get_true_vs_false_positive_df() and get_threshold() methods to compute and interpret threshold-dependent TPR/FPR metrics.) — https://github.com/bihealth/NeatMS
- **scikit-learn** (Underpins ROC curve computation and AUC calculation; used internally by NeatMS for threshold analysis.)
- **pandas** (Structures and manipulates the threshold-indexed recall table returned by get_true_vs_false_positive_df().)
- **NumPy** (Supports numerical operations on threshold metrics and probability scores.)

## Examples

```
from neatms import NN_handler
nn_handler = NN_handler.create_model(model='path_to_model.h5')
roc_df = nn_handler.get_true_vs_false_positive_df(label='High_quality')
threshold_01 = roc_df[roc_df['Probability_threshold'] == 0.01]
print(threshold_01[['True', 'False', 'False_low', 'False_noise']])
optimal_threshold = nn_handler.get_threshold()
```

## Evaluation signals

- Returned TPR and FPR values at reference thresholds match expected benchmarks (e.g., TPR ≈ 1.0, FPR ≈ 0.440 at threshold 0.01 for default model).
- Optimal threshold from get_threshold() matches the reference value (0.22 for default model) — threshold maximizes (TP − FP).
- DataFrame row count matches expected number of probability thresholds scanned (typically 0.00–0.99 in 0.01 increments = ~100 rows).
- False_low + False_noise column sums to approximately 1.0 (or total False count) — validates decomposition of false positives.
- TPR decreases monotonically and FPR decreases monotonically as threshold increases — ensures inverse relationship is preserved.

## Limitations

- ROC interpretation assumes a representative labelled validation set; severely imbalanced or non-representative labels bias threshold selection.
- The default model's optimal threshold (0.22) is specific to the training/validation data used; thresholds may need retuning for new datasets or instrument configurations.
- NeatMS does not provide automated confidence intervals or hypothesis tests for threshold differences — threshold selection is deterministic but point estimates lack uncertainty quantification.
- False positive decomposition (Low_quality vs. Noise) depends on correct peak labelling; annotation errors propagate to false positive rate estimates.

## Evidence

- [methods] Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [methods] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [methods] Extract the row corresponding to Probability_threshold=0.01 and read the True, False, False_low, and False_noise column values.: "Extract the row corresponding to Probability_threshold=0.01 and read the True, False, False_low, and False_noise column values."
- [intro] NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data.: "NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data."
- [intro] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
