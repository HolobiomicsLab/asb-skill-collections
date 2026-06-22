---
name: local-statistics-median-mean-computation
description: Use when you have raw LA-ICP-MS image data containing potential spike outliers (e.g., instrumental noise, ablation irregularities) and need to establish a local reference statistic for each pixel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0625
  tools:
  - pewpew
  - pewlib
  - Python
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
- python library [pewlib]
- python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# local-statistics-median-mean-computation

## Summary

Compute local median or mean statistics within a rolling window around each pixel in LA-ICP-MS image data to establish baseline and deviation thresholds for spike detection and removal. This is a foundational preprocessing step that prepares local reference statistics needed by downstream outlier-detection filters.

## When to use

Apply this skill when you have raw LA-ICP-MS image data containing potential spike outliers (e.g., instrumental noise, ablation irregularities) and need to establish a local reference statistic for each pixel. Use it as the first step before applying Rolling Median or Rolling Mean spike-removal filters, or whenever you need to detect pixels that deviate significantly from their local neighborhood.

## When NOT to use

- Input data is already spike-free or has been pre-filtered by the instrument software (skip to quantification/calibration).
- Window size is larger than the lateral spatial resolution of the ablation pattern; local statistics become uninformative when the neighborhood is too coarse.
- Data contains sharp, intentional chemical gradients smaller than the window size; rolling statistics will blur legitimate compositional boundaries.

## Inputs

- raw LA-ICP-MS image data (2D or 3D pixel intensity array)
- window size parameter (3, 5, 7, or user-defined)
- filter type selection (Rolling Median or Rolling Mean)

## Outputs

- local median statistic layer (one value per pixel, or NaN for edge pixels)
- local mean statistic layer (one value per pixel, or NaN for edge pixels)
- intermediate deviation array (absolute difference between each pixel and its local statistic)

## How to apply

For each pixel in the LA-ICP-MS image, define a rolling window (typical sizes: 3, 5, or 7 pixels, symmetric around the target pixel) and compute either the local median or local mean of intensities within that window, excluding the pixel itself from the calculation. Store these local statistics as a separate layer or intermediate array. The choice between median and mean determines the downstream threshold parameter: use median for Rolling Median filtering (threshold M = distance in medians from local median) or mean for Rolling Mean filtering (threshold σ = distance in standard deviations from local mean). Window size and threshold parameters should be tuned based on the spike frequency and intensity distribution observed in pilot data.

## Related tools

- **pewlib** (Python library that implements median/mean computation and provides data structures for LA-ICP-MS image arrays; core backend for local-statistics calculations) — https://github.com/djdt/pewlib
- **pewpew** (GUI front-end for pewlib that exposes Rolling Median and Rolling Mean filter dialogs with configurable window size and threshold parameters; used for interactive application and visualization of local-statistics-based filters) — https://github.com/djdt/pewpew

## Evaluation signals

- Edge pixel handling: confirm that pixels within window_size/2 of image boundaries are either marked NaN or excluded from downstream filtering to avoid boundary artifacts.
- Window size consistency: verify that all pixels use the same symmetric window geometry (e.g., 3×3 means ±1 pixel in x and y); asymmetry indicates a bug.
- Local statistic monotonicity check: compare local statistics to global image statistics; local medians should cluster tightly around the global median if the data is homogeneous, and scatter widely if there are regional gradients.
- Deviation distribution: plot histogram of absolute deviations (pixel value − local statistic); spike-free regions should show low deviations, while spike-containing regions should show a long tail (validate against expected noise floor).
- Reproducibility: re-running the same filter on the same image with the same parameters should produce byte-identical results (or numerically identical within floating-point tolerance).

## Limitations

- Rolling-window statistics are undefined or unreliable at image edges; typical implementation marks these as NaN or requires padding (zero-padding biases edge estimates downward).
- Window size choice is user-dependent and dataset-specific; no universal optimal size exists. Too-small windows (e.g., 3×3) may fail to distinguish true spikes from real fine structure; too-large windows (e.g., 7×7 or larger) smooth legitimate compositional variations.
- Median computation is more robust to extreme outliers than mean but is slower (O(k log k) per pixel for window size k); mean is faster but sensitive to the very spikes being detected.
- Local statistics assume spatial stationarity (uniform noise level and intensity gradients); methods fail or require adaptive windowing in regions of very sharp ablation boundaries or instrumental drift.
- No changelog available for pewlib/pewpew; implementation details of local-statistics algorithms (e.g., how ties are broken in median, handling of NaN propagation) may vary between versions without documentation.

## Evidence

- [other] Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels.: "Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels."
- [other] Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter.: "Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter."
- [other] Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic.: "Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic."
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library [pewlib]: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library"
