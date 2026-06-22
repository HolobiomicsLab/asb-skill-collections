---
name: roc-curve-auc-metric-evaluation
description: Use when after training a NeatMS CNN model on labeled MS1 peaks and generating predictions on a held-out test set, compute ROC-AUC to assess whether the model achieves the target discrimination threshold (AUC ≥ 0.9) without evidence of overfitting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - NeatMS
  - Python
  - TensorFlow
  - Keras
  - scikit-learn
  - pandas
  - NumPy
  - Jupyter Notebook
  - TensorFlow/Keras
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- calling the training method (1000 by default). NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training
- from keras.optimizers import SGD, Adam
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

# roc-curve-auc-metric-evaluation

## Summary

Compute ROC curve and AUC score from classifier predictions to quantify the model's ability to discriminate true positive from false positive MS1 peaks across all classification thresholds. This is essential for evaluating NeatMS CNN model performance on untargeted LCMS data without bias toward any particular operating point.

## When to use

After training a NeatMS CNN model on labeled MS1 peaks and generating predictions on a held-out test set, compute ROC-AUC to assess whether the model achieves the target discrimination threshold (AUC ≥ 0.9) without evidence of overfitting. Use this when you need to verify that validation accuracy reflects genuine generalization rather than memorization, or when comparing model variants trained under different hyperparameters or class balance settings.

## When NOT to use

- Input is already a published, pre-trained NeatMS model—use transfer learning or direct application instead of retraining and re-evaluating.
- Dataset has fewer than ~500 peaks per class; use transfer learning with a smaller labeled subset to avoid unstable AUC estimates.
- Labels are unlabeled or only partially annotated; ROC-AUC requires ground-truth class assignments.

## Inputs

- NeatMS experiment object with trained CNN model
- Test set predictions (true labels and predicted probabilities) from get_true_vs_false_positive_df()
- TensorFlow/Keras training and validation accuracy logs

## Outputs

- ROC curve (False Positive Rate vs. True Positive Rate plot)
- AUC score (scalar, 0–1 range)
- Classification of overfitting status (present/absent based on training–validation divergence)

## How to apply

Extract true positive and false positive labels along with predicted probabilities from the NeatMS model using get_true_vs_false_positive_df(), which returns a DataFrame keyed by class membership and prediction confidence. Compute False Positive Rate (1 − specificity) and True Positive Rate (sensitivity) across all decision thresholds, then calculate the area under the ROC curve using scikit-learn's auc() function. Inspect the ROC curve shape: a curve that hugs the top-left corner indicates strong discrimination; a diagonal line indicates random guessing. Simultaneously monitor training vs. validation accuracy curves from TensorFlow/Keras logs—if training accuracy approaches ~100% while validation accuracy stagnates significantly below, halt training to prevent overfitting, as high AUC on a validation set proves genuine discrimination rather than memorization.

## Related tools

- **NeatMS** (Provides get_true_vs_false_positive_df() method to extract predictions and ground-truth labels for ROC-AUC calculation) — https://github.com/bihealth/NeatMS
- **scikit-learn** (Computes AUC from FPR and TPR arrays via sklearn.metrics.auc())
- **TensorFlow/Keras** (Returns training and validation accuracy logs during model.fit() to detect overfitting by comparing final metrics)
- **Python** (Environment for orchestrating data extraction, ROC computation, and curve visualization)
- **Jupyter Notebook** (Interactive environment for visualizing ROC curves and inspecting accuracy divergence plots)

## Examples

```
from sklearn.metrics import auc
import numpy as np
df = experiment.neural_network_handler.get_true_vs_false_positive_df()
fpr = np.linspace(0, 1, 100)
tpr = np.interp(fpr, df['false_positive_rate'], df['true_positive_rate'])
roc_auc = auc(fpr, tpr)
print(f'AUC ROC Score: {roc_auc:.3f}')
```

## Evaluation signals

- AUC score ≥ 0.9 on held-out test set, indicating strong discrimination between true and false positive MS1 peaks.
- Training accuracy and validation accuracy converge or diverge by < 5 percentage points at final epoch; large divergence signals overfitting and invalidates AUC as a generalization metric.
- ROC curve visually hugs the top-left corner rather than following a diagonal, confirming the classifier outperforms random chance across all thresholds.
- AUC computed from get_true_vs_false_positive_df() is consistent across multiple random seeds or cross-validation folds if repeated evaluation is performed.
- Threshold-independent nature of AUC is verified by comparing to a single-point metric (e.g., accuracy at default threshold); AUC should remain valid even if the default threshold is suboptimal.

## Limitations

- NeatMS does not provide built-in callback functions for automatic early stopping; practitioners must manually inspect TensorFlow logs and call train_model() again or halt to avoid overfitting.
- AUC can be misleading on severely class-imbalanced datasets; the normalise_class parameter in create_batches() can balance training but may not reflect real-world class proportions in the test set.
- Publication for NeatMS is currently pending, limiting access to peer-reviewed validation on diverse LCMS platforms and peak detection pipelines.
- Minimum recommended dataset size of ~500 peaks per class for full model training; smaller datasets may yield unstable AUC estimates with wide confidence intervals.

## Evidence

- [other] Compute ROC curve and AUC using get_true_vs_false_positive_df() data with scikit-learn's auc() function on False Positive Rate vs. True Positive Rate.: "Compute ROC curve and AUC using get_true_vs_false_positive_df() data with scikit-learn's auc() function on False Positive Rate vs. True Positive Rate."
- [other] Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training.: "Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training."
- [readme] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
- [methods] We recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "We recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
- [methods] NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training.: "NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training."
