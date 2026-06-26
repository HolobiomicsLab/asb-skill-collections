---
name: plot-customization-and-styling
description: Use when after generating a numerical visualization (e.g., confusion
  matrix, heatmap, or similarity array) using matplotlib, when you need to add axis
  labels, class names, colormaps, normalization annotations, colorbars, titles, and
  export the figure in a publication-ready format (PNG or PDF).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2269
  tools:
  - ms2deepscore
  - GitHub
  - matplotlib
  - scikit-learn
  - numpy
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular
  structural similarities'
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

# plot-customization-and-styling

## Summary

Apply visual styling, annotations, and formatting to matplotlib figures to enhance interpretability and publication readiness. This skill configures heatmaps, colorbars, axis labels, titles, legends, and save formats to transform raw numerical outputs into polished visualizations.

## When to use

After generating a numerical visualization (e.g., confusion matrix, heatmap, or similarity array) using matplotlib, when you need to add axis labels, class names, colormaps, normalization annotations, colorbars, titles, and export the figure in a publication-ready format (PNG or PDF).

## When NOT to use

- Input is a pre-rendered image or bitmap; styling applies only to vector graphics and numerical data arrays.
- Interactive visualization is the end goal; matplotlib static exports do not support user interactivity (consider plotly or bokeh instead).
- High-dimensional data (>2D) that requires dimensionality reduction before heatmap representation (e.g., 3D confusion tensor).

## Inputs

- numpy array (prediction scores or confusion matrix)
- numpy array or list (ground-truth labels)
- optional: list of class names (strings)
- optional: normalization mode string ('row', 'col', 'all', or None)
- optional: colormap name (string, e.g. 'viridis', 'RdYlGn')

## Outputs

- matplotlib Figure object
- PNG or PDF file on disk
- styled heatmap with annotated cells, axis labels, colorbar, and title

## How to apply

Render the matrix or array data as a heatmap using matplotlib's imshow or heatmap functions. Annotate cell values with numeric text overlays to show raw or normalized values. Configure the colormap (e.g., 'viridis', 'RdYlGn') to match the data domain and normalize the colorbar scale if needed (e.g., by row, column, or all elements). Set axis tick labels to class names or spectrum identifiers and add a descriptive title. Attach a colorbar legend indicating the metric scale (e.g., similarity score, confusion count). Apply styling choices (font size, tick rotation, aspect ratio) for readability, then save to disk in PNG or PDF format using savefig with appropriate dpi and bbox_inches parameters.

## Related tools

- **matplotlib** (Core library for figure rendering, heatmap creation, and annotation of cell values, axis labels, colorbars, and titles) — https://matplotlib.org
- **scikit-learn** (Computes confusion_matrix from predictions and labels prior to visualization styling) — https://scikit-learn.org
- **numpy** (Provides array normalization operations (row-wise, column-wise, or global) applied before heatmap rendering) — https://numpy.org
- **ms2deepscore** (Example domain context: generates similarity matrices between mass spectrometry spectra that are then styled and visualized as heatmaps) — https://github.com/matchms/ms2deepscore

## Examples

```
from matplotlib import pyplot as plt; import numpy as np; cm = np.array([[90, 5], [10, 85]]); ax = plt.imshow(cm, cmap='viridis', origin='upper'); plt.colorbar(ax); plt.xticks([0, 1], ['Neg', 'Pos']); plt.yticks([0, 1], ['Neg', 'Pos']); plt.title('Confusion Matrix'); plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
```

## Evaluation signals

- Heatmap contains annotated cell values matching input array dimensions.
- Axis labels correctly display class names or spectrum identifiers with no truncation or misalignment.
- Colorbar is present and scaled to the data range (e.g., 0–1 for normalized similarities, 0–N for counts).
- Title and legend text are legible at saved resolution (dpi ≥ 100 for PNG, ≥ 300 for print-quality PDF).
- Output file exists at specified path in declared format (PNG or PDF) with file size >0 bytes and no rendering errors.

## Limitations

- Large matrices (>1000×1000 cells) may produce unreadable heatmaps due to cell size and label crowding; consider downsampling or tiling.
- Colormap choice can obscure or amplify patterns depending on perceptual uniformity; diverging maps ('RdYlGn', 'coolwarm') suit bipolar data, sequential maps ('viridis', 'plasma') suit unipolar data.
- Normalization by row or column can hide global patterns; choice of normalization mode must be justified by analysis goal.
- Raster export (PNG) loses vector quality at high zoom; PDF is preferred for publication but requires vector-compatible backends.

## Evidence

- [other] Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels.: "Render the matrix as a heatmap using matplotlib, with annotated cell values and axis labels"
- [other] Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format.: "Apply styling (colorbar, title, legend) and save the figure to disk in PNG or PDF format"
- [other] Optionally normalize the matrix (by row, column, or all elements) based on parameter.: "Optionally normalize the matrix (by row, column, or all elements) based on parameter"
- [other] Define the `create_confusion_matrix_plot` function signature accepting prediction array, ground-truth label array, and optional parameters (class names, normalization mode, colormap).: "optional parameters (class names, normalization mode, colormap)"
