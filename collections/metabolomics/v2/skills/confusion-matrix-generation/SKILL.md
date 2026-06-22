---
name: confusion-matrix-generation
description: Use when after training or evaluating a classification model (e.g., MS2DeepScore or other neural networks) when you have paired arrays of predicted class labels and ground-truth labels and need to assess per-class prediction accuracy, false positive/negative rates, or class imbalance effects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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

# confusion-matrix-generation

## Summary

Generate a confusion matrix visualization from model predictions and ground-truth labels, with optional normalization and heatmap rendering. This skill is essential for evaluating classification performance in mass spectrometry similarity prediction and other multi-class scenarios.

## When to use

After training or evaluating a classification model (e.g., MS2DeepScore or other neural networks) when you have paired arrays of predicted class labels and ground-truth labels and need to assess per-class prediction accuracy, false positive/negative rates, or class imbalance effects.

## When NOT to use

- Input predictions are already aggregated or averaged (e.g., if you only have overall accuracy, not per-sample predictions)
- Ground-truth labels and predictions have mismatched lengths or cannot be paired element-wise
- Your task is regression (continuous targets) rather than multi-class or binary classification

## Inputs

- prediction array (1D numpy array or list of predicted class labels)
- ground-truth label array (1D numpy array or list of true class labels)
- optional: class names (list of strings for axis labels)
- optional: normalization mode (string: 'row', 'col', 'all', or None)

## Outputs

- confusion matrix (2D numpy array)
- confusion matrix heatmap figure (matplotlib Figure object)
- saved visualization file (PNG or PDF)

## How to apply

Compute the confusion matrix from prediction and ground-truth label arrays using scikit-learn's confusion_matrix function. Optionally normalize the matrix by row (recall per class), column (precision per class), or all elements (proportional view). Render the normalized or raw matrix as a matplotlib heatmap with annotated cell values, axis labels showing class names, and a colorbar. Apply styling (title, legend) and save the figure to PNG or PDF format. Use this workflow to identify which classes are most frequently confused and whether misclassifications are systematic or random.

## Related tools

- **scikit-learn** (Compute confusion_matrix from predictions and ground-truth labels)
- **matplotlib** (Render confusion matrix as annotated heatmap with colorbar and styling)
- **ms2deepscore** (Example context: neural network producing class predictions for mass spectrometry spectra that require confusion matrix evaluation) — https://github.com/matchms/ms2deepscore

## Examples

```
from sklearn.metrics import confusion_matrix; import matplotlib.pyplot as plt; cm = confusion_matrix(y_true, y_pred); plt.imshow(cm, cmap='viridis'); plt.colorbar(); plt.savefig('confusion_matrix.png')
```

## Evaluation signals

- Confusion matrix shape matches (n_classes, n_classes) and sums to total number of samples
- Diagonal values (true positives per class) are non-zero for well-predicted classes; off-diagonal values reveal class confusion patterns
- If normalized by row, each row sums to 1.0 (or close, accounting for floating-point precision); if by column, each column sums to 1.0
- Heatmap renders without errors, all class names appear on axes, cell values are readable and range as expected (0–1 if normalized; 0–total_samples if raw)
- Output file exists at specified path with correct format (PNG/PDF) and is non-empty

## Limitations

- Confusion matrix assumes multi-class or binary classification; not suitable for regression or ranking tasks
- Very large number of classes (>20–30) makes the heatmap difficult to read; consider aggregating or filtering classes
- Class imbalance is not directly addressed by the matrix itself; normalization modes (row, column) can help highlight recall vs. precision trade-offs but do not correct underlying imbalance
- Confusion matrix alone does not capture decision-threshold effects or probability calibration; consider pairing with ROC curves or calibration plots for probabilistic models

## Evidence

- [other] Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix: "Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix."
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter: "Optionally normalize the matrix (by row, column, or all elements) based on parameter."
- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels."
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format."
- [intro] intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra."
