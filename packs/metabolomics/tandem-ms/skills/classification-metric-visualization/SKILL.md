---
name: classification-metric-visualization
description: Use when after training or evaluating a classification model (e.g., a Siamese neural network for spectrum similarity prediction) and obtaining a prediction array and corresponding ground-truth label array.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3473
  tools:
  - ms2deepscore
  - GitHub
  - scikit-learn
  - matplotlib
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classification-metric-visualization

## Summary

Construct and render a confusion matrix heatmap from predicted and ground-truth class labels to visualize classifier performance across all class pairs. This skill enables rapid diagnosis of per-class precision, recall, and misclassification patterns by normalizing the matrix (by row, column, or all elements) and overlaying annotated cell counts or proportions on a color-scaled grid.

## When to use

After training or evaluating a classification model (e.g., a Siamese neural network for spectrum similarity prediction) and obtaining a prediction array and corresponding ground-truth label array. Use this skill to qualitatively inspect whether the classifier confuses particular class pairs, whether class imbalance drives high error in minority classes, or whether performance is uniform across classes.

## When NOT to use

- Input predictions or labels are not discrete class indices or strings (e.g., continuous regression outputs); use a regression residual plot instead.
- Number of classes is very large (>50–100); consider aggregating classes or using alternative summaries (e.g., per-class ROC curves) to avoid visual clutter.
- Input data contains NaN or None values without prior imputation or filtering; clean data first.

## Inputs

- prediction array (1D numpy array or list of predicted class labels)
- ground-truth label array (1D numpy array or list of true class labels)
- optional class names (list of strings for axis labels)
- optional normalization mode (string: 'row', 'column', 'all', or None)

## Outputs

- confusion matrix heatmap (matplotlib Figure object)
- rendered image file (PNG or PDF on disk)

## How to apply

Compute the confusion matrix from the prediction array and ground-truth labels using scikit-learn's confusion_matrix function. Optionally normalize the matrix—by row (to show per-class recall), by column (to show per-class precision), or by all elements (to show overall error proportions)—depending on whether you want to emphasize false negatives, false positives, or absolute frequency. Render the normalized or raw matrix as a heatmap using matplotlib, with cell values annotated numerically, row and column axes labeled with class names, and a colorbar to indicate magnitude. Apply styling (title, legend if needed) and save the figure to disk in PNG or PDF format for inclusion in reports or publications.

## Related tools

- **scikit-learn** (compute confusion_matrix from predictions and ground-truth labels)
- **matplotlib** (render heatmap visualization with annotations and styling)
- **ms2deepscore** (source domain: Siamese model generating predictions for spectrum pairs) — https://github.com/matchms/ms2deepscore

## Evaluation signals

- Confusion matrix dimensions are (num_classes, num_classes) and contain only non-negative integers or floats (if normalized).
- Sum of each row equals the total ground-truth count for that class (before normalization); normalized rows sum to 1.0 (within floating-point tolerance).
- Diagonal elements (true positives) are visually prominent (high color intensity) for well-performing classes; off-diagonal elements indicate class confusion patterns consistent with the prediction errors.
- Annotated cell values match the underlying data and are readable at the selected figure resolution; axis labels match the provided class names.
- Output file is created at the specified path and opens without corruption in standard image viewers.

## Limitations

- Confusion matrix does not scale well to >50–100 classes; visual inspection becomes difficult and heatmap cells become too small.
- Normalization by row ('recall') can obscure class imbalance; normalization by column ('precision') can obscure differences in support. Choose normalization mode intentionally based on the analysis goal.
- Raw (unnormalized) matrix dominated by the most frequent class(es) may hide minority-class errors; always consider normalized versions.
- Assumes prediction and label arrays are 1D and aligned (same length, same order); misaligned or ragged inputs produce meaningless matrices.

## Evidence

- [other] Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix: "Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix."
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter: "Optionally normalize the matrix (by row, column, or all elements) based on parameter."
- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels."
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format."
- [other] Define the function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap): "Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap)."
