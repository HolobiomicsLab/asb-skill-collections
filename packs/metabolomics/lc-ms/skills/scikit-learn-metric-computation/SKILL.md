---
name: scikit-learn-metric-computation
description: Use when you have prediction arrays (model outputs) and ground-truth label arrays from a classification task and need to compute confusion matrices, accuracy scores, or other performance metrics for visualization or quantitative evaluation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ms2deepscore
  - GitHub
  - scikit-learn
  - matplotlib
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
- use the search functionality [here](https://github.com/matchms/ms2deepscore/issues)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_2_0_cq
    doi: 10.1101/2024.03.25.586580v5
    title: MS2DeepScore 2.0
  dedup_kept_from: coll_ms2deepscore_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.03.25.586580v5
  all_source_dois:
  - 10.1101/2024.03.25.586580v5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# scikit-learn-metric-computation

## Summary

Use scikit-learn's confusion_matrix and related metric functions to compute classification performance matrices from predicted and ground-truth label arrays. This enables rapid evaluation of model predictions against reference labels in mass spectrometry and other classification workflows.

## When to use

You have prediction arrays (model outputs) and ground-truth label arrays from a classification task and need to compute confusion matrices, accuracy scores, or other performance metrics for visualization or quantitative evaluation. Typical triggers: post-training model evaluation, cross-validation score aggregation, or comparison of competing classifiers on the same spectrum or compound dataset.

## When NOT to use

- Inputs are already in a pre-computed confusion matrix or aggregated metric form — skip directly to visualization or interpretation.
- You need probabilities or decision thresholds rather than hard class labels — use probability calibration or ROC/AUC metrics instead.
- The classification problem is multi-label (samples belong to multiple classes simultaneously) — use multilabel_confusion_matrix or hamming loss instead.

## Inputs

- prediction array (numpy array or list of predicted class labels)
- ground-truth label array (numpy array or list of true class labels)
- optional class names (list of strings for axis labels)
- optional normalization mode (string: 'true', 'pred', or None)

## Outputs

- confusion matrix (2D numpy array or pandas DataFrame)
- confusion matrix heatmap visualization (matplotlib figure)
- saved figure file (PNG or PDF)

## How to apply

Import scikit-learn's confusion_matrix function and pass both the ground-truth labels and predicted labels to compute the confusion matrix. Optionally normalize the resulting matrix by row (per-class recall), column (per-class precision), or across all elements (stochastic normalization) depending on the evaluation context. The normalization mode is a key parameter: use 'true' for row-normalized (recalls per true class), 'pred' for column-normalized (precisions per predicted class), or None for raw counts. Once computed, render the matrix as a heatmap using matplotlib with annotated cell values, axis labels showing class names, a colorbar, and a title; save the figure in PNG or PDF format. Use this metric when you need both a visual confusion summary and quantitative misclassification patterns.

## Related tools

- **scikit-learn** (Provides confusion_matrix function to compute classification performance matrix from predicted and ground-truth labels)
- **matplotlib** (Renders confusion matrix as heatmap with annotations, colorbar, and styling)
- **ms2deepscore** (Example application: evaluating Siamese neural network predictions against ground-truth molecular similarity or compound class labels) — https://github.com/matchms/ms2deepscore

## Examples

```
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

y_true = np.array([0, 1, 2, 0, 1, 2])
y_pred = np.array([0, 1, 1, 0, 2, 2])
cm = confusion_matrix(y_true, y_pred, normalize='true')
plt.imshow(cm, cmap='Blues', interpolation='nearest')
plt.colorbar()
plt.savefig('confusion_matrix.png')
```

## Evaluation signals

- Confusion matrix shape matches (n_classes, n_classes) where n_classes = number of unique labels in ground-truth array.
- Matrix row sums or column sums equal total sample count (before normalization) or sum to 1.0 (after normalization), indicating no dropped or duplicated samples.
- Diagonal elements (correct predictions) are visually prominent in the heatmap; off-diagonal elements reveal systematic confusions between specific class pairs.
- Normalization is correctly applied: row-normalized values represent per-class recall (each row sums to 1.0), column-normalized values represent precision (each column sums to 1.0).
- Saved figure is readable and includes clear axis labels, class names, colorbar with scale range, and title.

## Limitations

- Confusion matrix assumes single-label classification; multi-label or hierarchical classification requires alternative metrics (multilabel_confusion_matrix, Hamming loss).
- Matrix values are computed from hard class labels only; probabilistic or soft predictions must be thresholded or converted to labels beforehand.
- Imbalanced datasets can produce misleading visual patterns in unnormalized matrices; normalization by row (recall) or column (precision) is strongly recommended for exploration.
- Large numbers of classes (>20) make heatmap difficult to read; consider aggregating minority classes or using alternative visualizations (hierarchical clustering, class-specific precision/recall plots).

## Evidence

- [other] Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix.: "Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix."
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter.: "Optionally normalize the matrix (by row, column, or all elements) based on parameter."
- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels.: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels."
- [other] Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap).: "Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap)."
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format.: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format."
