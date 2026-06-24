---
name: machine-learning-model-evaluation
description: Use when you have a trained NeatMS neural network model and a labelled
  validation dataset of MS1 peaks (annotated as 'High_quality' or 'Low_quality'),
  and you need to identify the scalar probability threshold that separates true positive
  from false positive peak classifications in your specific.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3316
  tools:
  - NeatMS
  - Python
  - pandas
  - scikit-learn
  - NumPy
  - Keras
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
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

# machine-learning-model-evaluation

## Summary

Determine the optimal classification threshold for a trained neural network model by computing true and false positive rates across probability thresholds and selecting the threshold that maximizes the difference between true positives and false positives. This skill is essential for validating model performance on labelled peak datasets and ensuring the model generalizes beyond training data.

## When to use

You have a trained NeatMS neural network model and a labelled validation dataset of MS1 peaks (annotated as 'High_quality' or 'Low_quality'), and you need to identify the scalar probability threshold that best separates true positive from false positive peak classifications in your specific LCMS dataset.

## When NOT to use

- Input peak dataset is unlabelled or lacks quality annotations; threshold optimization requires ground truth labels.
- You are working with raw LCMS data files that have not yet been processed by peak detection pipelines; NeatMS operates on detected peaks, not raw spectra.
- Your validation dataset is too small (<~50 peaks per class); sparse data may yield unstable or non-representative threshold estimates.

## Inputs

- Trained NeatMS neural network model (Keras/TensorFlow format)
- Labelled peak validation dataset with binary class labels ('High_quality', 'Low_quality')
- Peak batches prepared via NeatMS batch creation workflow

## Outputs

- Optimal classification threshold scalar value (float)
- True vs. false positive rates table (pandas DataFrame) across probability thresholds

## How to apply

Load a trained NeatMS neural network model and prepare labelled peak batches using NN_handler.create_model(). Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true positive and false positive rates across a range of probability thresholds. The method applies the optimization criterion (True Positives minus False Positives) to identify the threshold that maximizes this difference. Verify the returned scalar threshold value against expected reference values (0.22 is the documented default for the standard NeatMS model). The rationale is that this data-driven approach, rather than arbitrary thresholds, directly optimizes for the trade-off between sensitivity and specificity on your validation set.

## Related tools

- **NeatMS** (Provides NN_handler class with get_threshold() method and neural network training/validation infrastructure for MS1 peak classification) — https://github.com/bihealth/NeatMS
- **Python** (Language for scripting the workflow and calling NeatMS API)
- **pandas** (Data manipulation library for loading, filtering, and analyzing the true vs. false positive rates DataFrame)
- **scikit-learn** (Provides metrics (e.g., AUC computation) for threshold evaluation and ROC analysis)
- **NumPy** (Numerical array operations for threshold comparison and optimization)
- **Keras** (Neural network framework underlying the trained NeatMS classification model)

## Examples

```
from neatms import NN_handler
nn_handler = NN_handler.create_model(model_path='model.h5')
optimal_threshold = nn_handler.get_threshold(validation_batches, label='High_quality')
print(f'Optimal threshold: {optimal_threshold}')
```

## Evaluation signals

- Returned threshold scalar is a float in the plausible range [0, 1] that matches or is close to documented reference values (e.g., 0.22 for the default model).
- The true vs. false positive rates table shows monotonic or near-monotonic increase in true positives and decrease in false positives as threshold decreases, consistent with ROC curve behavior.
- When the threshold is applied to the validation dataset, the resulting peak classifications (High_quality vs. Low_quality) achieve balanced or documented sensitivity/specificity trade-offs.
- The method succeeds without errors, indicating the labelled dataset is compatible with the trained model's input shape and label encoding.
- Applying the returned threshold to an independent test dataset (not used in threshold optimization) yields stable classification performance metrics (precision, recall, F1) within expected ranges for the application domain.

## Limitations

- Threshold optimization is dataset-specific; a threshold optimal for one LCMS dataset or sample type may not generalize to different instruments, ionization modes, or peak detection pipelines.
- The optimization criterion (TP − FP) does not account for class imbalance or different cost weightings for false positives vs. false negatives; datasets with highly imbalanced High_quality/Low_quality ratios may require threshold adjustment.
- NeatMS does not provide automated callbacks to halt training early; resuming training on an already-trained model may lead to overfitting, which can inflate threshold estimates derived from the same validation data.
- The method requires manually labelled peaks; if the labelling is noisy or inconsistent (acknowledged by the article as inevitable, e.g., 'High quality' can become 'Low quality'), the estimated threshold may be suboptimal.

## Evidence

- [other] Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [other] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [intro] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
- [other] Verify the returned threshold matches the expected reference value (0.22 for the default model).: "Verify the returned threshold matches the expected reference value (0.22 for the default model)."
- [methods] A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen.: "A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen."
