---
name: probability-threshold-calibration
description: Use when after training or loading a NeatMS neural network model, apply this skill when you have a labelled validation dataset and need to determine the optimal probability threshold that maximizes classification performance (true positives minus false positives).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# probability-threshold-calibration

## Summary

Calibrate the classification probability threshold of a trained neural network model on a labelled validation dataset to maximize the difference between true positives and false positives. This ensures the model's decision boundary is optimized for the specific task of filtering false positive MS1 peaks in untargeted LCMS workflows.

## When to use

After training or loading a NeatMS neural network model, apply this skill when you have a labelled validation dataset and need to determine the optimal probability threshold that maximizes classification performance (true positives minus false positives). Use it before deploying the model to filter peaks in new LCMS datasets.

## When NOT to use

- Input dataset is unlabelled or has no ground-truth class assignments
- Model has not yet been trained or loaded into memory
- Peak probability scores are not available or have already been hard-classified

## Inputs

- trained NeatMS neural network model (Keras/TensorFlow model object)
- labelled peak validation dataset with binary class labels (High_quality / Low_quality)
- peak probability scores from model prediction on validation set

## Outputs

- optimal classification probability threshold (scalar float, e.g. 0.22)
- true positive vs. false positive rate dataframe across threshold values

## How to apply

Load a trained NeatMS neural network model and a labelled peak validation dataset using NN_handler.create_model(). Call nn_handler.get_threshold(), which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true positive and false positive rates across a range of probability thresholds. The method identifies the threshold that maximizes (True positives minus False positives) and returns the optimal scalar threshold value. For the default NeatMS model applied to validation data labelled 'High_quality', the expected optimal threshold is approximately 0.22. Verify the returned threshold is within the expected range and document it for downstream peak filtering.

## Related tools

- **NeatMS** (provides NN_handler.get_threshold() and get_true_vs_false_positive_df() methods for threshold calibration; hosts the default pre-trained neural network model) — https://github.com/bihealth/NeatMS
- **scikit-learn** (used internally (via auc import) for computing ROC and performance metrics)
- **pandas** (represents and manipulates true vs. false positive rate dataframes)
- **NumPy** (numerical operations on threshold values and metric arrays)
- **Keras/TensorFlow** (backend for trained neural network model and probability prediction)

## Examples

```
nn_handler = NeatMS.NN_handler(model_path='path/to/default_model.h5'); optimal_threshold = nn_handler.get_threshold(validation_peaks_batch)
```

## Evaluation signals

- Returned threshold is a scalar float value in the range [0, 1]
- Returned threshold matches the expected reference value (0.22 ± tolerance) for the default model on validation data
- True positive vs. false positive dataframe contains monotonically ordered threshold values and corresponding TP/FP rates
- The threshold that maximizes (TP − FP) can be independently verified by inspecting the returned dataframe
- Applying the returned threshold to peak probability scores produces a binary classification consistent with expected class balance on the validation set

## Limitations

- Threshold calibration is specific to the labelled validation dataset used; threshold may not generalise to datasets with different peak characteristics or LCMS processing pipelines
- Optimal threshold selection criterion (TP − FP) assumes equal cost of false positives and false negatives; domain-specific costs may require manual threshold adjustment
- Requires sufficient labelled data to compute stable TP/FP rates across thresholds; small validation sets may produce noisy or unreliable estimates
- NeatMS does not currently provide automatic callbacks to stop training, which may affect model convergence and thus downstream threshold calibration

## Evidence

- [other] Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [other] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [other] Verify the returned threshold matches the expected reference value (0.22 for the default model).: "Verify the returned threshold matches the expected reference value (0.22 for the default model)."
- [readme] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
- [readme] NeatMS relies on neural network based classification.: "NeatMS relies on neural network based classification."
