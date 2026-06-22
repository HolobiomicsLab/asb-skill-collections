---
name: python-function-implementation
description: Use when when you have classification predictions and ground-truth labels and need to generate a confusion matrix visualization with flexible normalization (by row, column, or all elements) and styling options for publication or diagnostic review.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3474
  tools:
  - ms2deepscore
  - Python
  - GitHub
  - scikit-learn
  - matplotlib
  - numpy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
- make sure the existing tests still work by running ``python setup.py test``
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the create_confusion_matrix_plot plotting function

## Summary

Implement a Python function that accepts prediction arrays, ground-truth labels, and optional parameters to compute, normalize, and visualize confusion matrices as annotated heatmaps. This skill enables modular construction of diagnostic plotting utilities for multi-class classification tasks.

## When to use

When you have classification predictions and ground-truth labels and need to generate a confusion matrix visualization with flexible normalization (by row, column, or all elements) and styling options for publication or diagnostic review.

## When NOT to use

- Input arrays are not 1-D or do not have equal length — function requires aligned prediction and label arrays.
- Classification problem is multi-label (samples belong to multiple classes simultaneously) rather than multi-class — confusion matrix assumes mutually exclusive classes.
- You need real-time interactive visualization rather than static file output — consider using matplotlib's interactive backends instead.

## Inputs

- prediction array (1-D numpy array of predicted class labels)
- ground-truth label array (1-D numpy array of true class labels)
- class names (optional list of strings)
- normalization mode (optional string: 'none', 'true', 'pred', 'all')
- colormap name (optional string, e.g., 'viridis', 'Blues')

## Outputs

- confusion matrix (2-D numpy array or normalized equivalent)
- figure saved to disk (PNG or PDF file)
- matplotlib Figure object (if returned by implementation)

## How to apply

Define the function signature to accept a prediction array, a ground-truth label array, and optional parameters for class names, normalization mode, and colormap selection. Compute the confusion matrix using scikit-learn's confusion_matrix utility. Apply optional row, column, or global normalization to the matrix depending on the parameter. Render the normalized matrix as a matplotlib heatmap with annotated cell values, axis labels derived from class names, and styling (colorbar, title) appropriate for the normalization mode. Save the resulting figure to disk in PNG or PDF format using matplotlib's savefig method.

## Related tools

- **scikit-learn** (Provides confusion_matrix function to compute the confusion matrix from predictions and labels)
- **matplotlib** (Provides heatmap rendering (imshow/seaborn), axis labels, colorbars, and file I/O (savefig))
- **numpy** (Supports array normalization operations (division, masking) and element-wise calculations)
- **ms2deepscore** (Provides context for multi-class spectrum classification and embedding evaluation workflows) — https://github.com/matchms/ms2deepscore

## Examples

```
from sklearn.metrics import confusion_matrix; import matplotlib.pyplot as plt; cm = confusion_matrix(y_true, y_pred); cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]; plt.imshow(cm_norm, cmap='Blues'); plt.colorbar(); plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- Confusion matrix dimensions match number of classes (N × N for N classes).
- Row sums equal 1.0 when normalization mode is 'true'; column sums equal 1.0 when 'pred'; all elements sum to 1.0 when 'all'.
- Output file (PNG/PDF) exists and is readable; figure contains annotated heatmap with axis labels and colorbar.
- Cell values in the heatmap are within expected range (0–1 for normalized; ≥0 for unnormalized counts).
- Diagonal elements (true positives) are visually distinct; off-diagonal elements show misclassification patterns clearly.

## Limitations

- Function assumes multi-class (not multi-label) classification; confusion matrices are undefined for overlapping class memberships.
- Normalization modes ('true', 'pred', 'all') alter interpretation of cell values; user must select appropriate mode for their diagnostic goal.
- Large number of classes (>20) may produce unreadable heatmaps; consider subsetting or aggregating classes.
- No built-in support for hierarchical or imbalanced class weighting; raw counts may mask minority-class errors in imbalanced datasets.

## Evidence

- [other] Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap).: "Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap)."
- [other] Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix.: "Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix."
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter.: "Optionally normalize the matrix (by row, column, or all elements) based on parameter."
- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels.: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels."
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format.: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format."
