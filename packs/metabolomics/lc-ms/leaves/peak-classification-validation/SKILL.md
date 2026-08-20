---
name: peak-classification-validation
description: Use when after training or loading a NeatMS neural network model, before applying it to filter false positive MS1 peaks in a new dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-classification-validation

## Summary

Validate a trained neural network classifier's optimal decision threshold on a labelled peak dataset by computing true vs. false positive rates across probability thresholds and selecting the threshold that maximizes (TP − FP). This skill ensures the classifier is correctly tuned before deployment on unlabelled LCMS data.

## When to use

After training or loading a NeatMS neural network model, before applying it to filter false positive MS1 peaks in a new dataset. Specifically when you have a labelled validation dataset with 'High_quality' and other class annotations, and need to determine the optimal classification threshold that balances true positives against false positives for your experimental context.

## When NOT to use

- Input validation dataset is unlabelled or lacks 'High_quality' annotations—get_threshold() requires labelled data to compute true/false positive rates.
- You are tuning hyperparameters during model training—threshold optimization should occur after model convergence, not during iterative training.
- The peak detection pipeline has already been manually filtered or curated with domain knowledge—get_threshold() assumes ground truth labels reflect the classification task, not downstream filtering decisions.

## Inputs

- Trained NeatMS neural network model (Keras/TensorFlow)
- Labelled peak dataset with binary annotations (e.g., 'High_quality' vs. other classes)
- NN_handler object initialized with model and validation data

## Outputs

- Optimal classification threshold scalar value (float, e.g., 0.22)
- True vs. false positive rate table (DataFrame with thresholds and corresponding TP/FP counts)

## How to apply

Load a trained NeatMS neural network model and its associated labelled validation dataset using NN_handler.create_model(). Prepare labelled peak batches and call nn_handler.get_threshold(), which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute TP and FP rates across a range of probability thresholds. The method selects the threshold that maximizes the (TP − FP) criterion and returns this optimal scalar value. Verify the returned threshold value matches expected reference values (e.g., 0.22 for the default NeatMS model) as a sanity check before applying this threshold to new data.

## Related tools

- **NeatMS** (Provides NN_handler class and get_threshold() method to compute and select optimal classification threshold from labelled peak batches.) — https://github.com/bihealth/NeatMS
- **scikit-learn** (Used internally by NeatMS for computing receiver operating characteristic (ROC) metrics and area under curve (AUC) calculations.)
- **pandas** (Used to construct and manipulate the true vs. false positive rate DataFrame returned by get_true_vs_false_positive_df().)
- **NumPy** (Underlying numerical computation library for threshold and rate calculations.)

## Examples

```
nn_handler = NeatMS.NN_handler.create_model(model_path='path/to/model'); batches = nn_handler.create_batches(labelled_peaks_df); optimal_threshold = nn_handler.get_threshold(batches, label='High_quality'); print(f'Optimal threshold: {optimal_threshold}')
```

## Evaluation signals

- Returned threshold value is a scalar float within the valid probability range [0.0, 1.0].
- Returned threshold matches reference value from literature or original model publication (e.g., 0.22 for the default NeatMS model).
- True vs. false positive DataFrame shows monotonic decrease in TP count and monotonic increase in FP count as threshold increases across probability values.
- The selected threshold corresponds to the row in the TP/FP table with maximum (TP − FP) value.
- Applying the returned threshold to the same validation dataset produces peak classifications with expected sensitivity and specificity ranges for high-quality MS1 peak detection.

## Limitations

- The optimal threshold is dataset-specific: the (TP − FP) criterion may not suit all applications; clinical or high-precision use cases may require receiver operating characteristic (ROC) curve inspection and manual threshold selection.
- Threshold optimization is sensitive to class imbalance in the labelled dataset; if 'High_quality' peaks are rare, the optimizer may select a threshold that favours false negatives.
- The method assumes that labels in the validation dataset accurately reflect the ground truth classification task; systematic annotation errors or reviewer drift (noted in the article's 'Review mode' section) will bias the returned threshold.
- No automated stopping or validation-set hold-out is mentioned; if the same labelled dataset is used for both training and threshold selection, threshold values may be optimistic (overfit to the training cohort).

## Evidence

- [other] Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [other] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [other] Verify the returned threshold matches the expected reference value (0.22 for the default model).: "Verify the returned threshold matches the expected reference value (0.22 for the default model)."
- [intro] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
- [methods] A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen.: "A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen."
