---
name: matplotlib-heatmap-rendering
description: Use when when you have a confusion matrix (predicted vs. ground-truth labels) or similarity matrix (pairwise scores between spectra) and need to communicate classification accuracy or chemical similarity patterns through a visual heatmap.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - ms2deepscore
  - GitHub
  - matplotlib
  - scikit-learn
  - numpy
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# matplotlib-heatmap-rendering

## Summary

Render a normalized confusion matrix or similarity matrix as an annotated heatmap using matplotlib, with optional normalization (by row, column, or all elements), colorbar, and styled axis labels. This skill is essential for visualizing classification performance or spectral similarity patterns in mass spectrometry workflows.

## When to use

When you have a confusion matrix (predicted vs. ground-truth labels) or similarity matrix (pairwise scores between spectra) and need to communicate classification accuracy or chemical similarity patterns through a visual heatmap. Typical trigger: post-model-evaluation or after computing MS2DeepScore similarities between spectrum pairs.

## When NOT to use

- Input is a 1D array or non-square matrix unsuitable for heatmap visualization.
- Matrix dimensions exceed ~100×100 without hierarchical clustering or downsampling; cell annotations will be illegible.
- You need interactive exploration of spectrum similarities; use UMAP or t-SNE embeddings instead.

## Inputs

- 2D numpy array (confusion matrix or similarity matrix)
- array of predicted class labels or spectrum identifiers
- array of ground-truth class labels or reference spectrum identifiers
- optional: list of class names (string)
- optional: normalization mode ('row', 'column', 'all', or None)

## Outputs

- matplotlib Figure object
- PNG or PDF file saved to disk containing the annotated heatmap

## How to apply

Compute or load a 2D confusion or similarity matrix (e.g., from scikit-learn's confusion_matrix or MS2DeepScore's similarity predictions). Optionally normalize the matrix by row (to show per-class recall), by column (per-class precision), or globally (to a 0–1 range). Render the matrix as a heatmap using matplotlib.imshow(), annotate each cell with its numeric value, label axes with class names or spectrum identifiers, add a colorbar to indicate the value scale, apply a perceptually uniform colormap (e.g., 'viridis'), and save to disk in PNG or PDF format. The normalization choice depends on the analytical question: row normalization highlights per-class performance; global normalization emphasizes the absolute magnitude of similarities.

## Related tools

- **matplotlib** (Rendering heatmap graphics with imshow(), colorbar, and annotations)
- **scikit-learn** (Computing confusion_matrix from predictions and ground-truth labels)
- **ms2deepscore** (Source of similarity matrices from MS2DeepScore model predictions) — https://github.com/matchms/ms2deepscore
- **numpy** (Matrix normalization (division, row-wise/column-wise operations))

## Examples

```
import matplotlib.pyplot as plt; from sklearn.metrics import confusion_matrix; import numpy as np; cm = confusion_matrix(y_true, y_pred); cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]; fig, ax = plt.subplots(); im = ax.imshow(cm_norm, cmap='viridis'); ax.set_xticks(range(len(class_names))); ax.set_xticklabels(class_names); ax.set_yticks(range(len(class_names))); ax.set_yticklabels(class_names); for i in range(cm.shape[0]): for j in range(cm.shape[1]): ax.text(j, i, f'{cm_norm[i, j]:.2f}', ha='center', va='center', color='white'); plt.colorbar(im, ax=ax); plt.savefig('confusion_matrix.png')
```

## Evaluation signals

- Heatmap cell values match the input matrix exactly (before normalization) or satisfy the chosen normalization invariant (e.g., row sums = 1 for row-normalized matrices).
- All cells are annotated with their numeric values at readable font size.
- Axis labels are present and correspond to class names or spectrum identifiers provided in input.
- Colorbar scale matches the range of plotted values (e.g., 0–1 for normalized matrices, or 0–max(matrix) for unnormalized).
- Output file exists at the specified path, is valid PNG/PDF, and renders without artifacts.

## Limitations

- Matrix values must be numeric (int or float); categorical or string data will fail.
- Heatmaps with >100 rows or columns become visually dense and difficult to interpret without aggressive downsampling or clustering.
- Cell annotations are not automatically adjusted for font size; very large or very small matrices may require manual figure resizing.
- Normalization assumes the matrix represents non-negative quantities; negative values may produce unexpected colormap behavior.
- The skill does not perform hierarchical clustering or reordering of rows/columns; the matrix is rendered as-is.

## Evidence

- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels.: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels."
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter.: "Optionally normalize the matrix (by row, column, or all elements) based on parameter."
- [other] Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix.: "Compute the confusion matrix from predictions and labels using scikit-learn's confusion_matrix."
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format.: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format."
- [readme] The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra.: "The library provides intuitive classes to prepare data, train a Siamese model, and compute similarities between pairs of spectra."
