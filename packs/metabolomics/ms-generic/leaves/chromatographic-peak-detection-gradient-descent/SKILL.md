---
name: chromatographic-peak-detection-gradient-descent
description: Use when you have LC-HRMS profile-mode data (retention time × m/z matrix
  format) and need to automatically identify chromatographic peak locations and boundaries
  prior to feature extraction, reference matching, or training a peak-classification
  CNN model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS/TOPPView
  techniques:
  - mass-spectrometry
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: christophuv/PeakBot
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac344
  title: PeakBot
evidence_spans:
- PeakBot is a python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakbot_cq
    doi: 10.1093/bioinformatics/btac344
    title: PeakBot
  dedup_kept_from: coll_peakbot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac344
  all_source_dois:
  - 10.1093/bioinformatics/btac344
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-detection-gradient-descent

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Detects chromatographic peaks in LC-HRMS profile-mode data by applying smoothing followed by gradient-descent algorithms to identify local maxima, estimate peak borders and centers. This preprocesses data for reference matching or CNN model training in untargeted metabolomics workflows.

## When to use

You have LC-HRMS profile-mode data (retention time × m/z matrix format) and need to automatically identify chromatographic peak locations and boundaries prior to feature extraction, reference matching, or training a peak-classification CNN model. This is appropriate when peaks are not pre-aligned and you require standardized peak center and bounding-box estimates.

## When NOT to use

- Input data is already centroided (not profile-mode LC-HRMS); use centroid-based peak picking instead.
- Peaks have already been detected and aligned; skip to reference matching or feature extraction.
- Signal-to-noise ratio is extremely low (<2:1); preprocessing or data filtering may be necessary first.

## Inputs

- LC-HRMS profile-mode data (retention time × m/z matrix)
- Chromatographic signal as 2D numpy array or HDF5 file
- Smoothing kernel parameters (e.g., window size, filter type)

## Outputs

- Detected peak center coordinates (retention time, m/z)
- Peak bounding boxes (rt_min, rt_max, mz_min, mz_max)
- Peak border estimates and center positions
- List of local maxima with associated intensity values

## How to apply

Load the LC-HRMS chromatogram as a retention time × m/z matrix in profile mode. Apply a smoothing filter to the chromatographic signal to reduce noise while preserving peak shape information. Execute a gradient-descent algorithm to locate local maxima in the smoothed signal and estimate each peak's center coordinates (rt, mz) and borders. For each detected maximum, extract or record the bounding box and center position. The gradient-based approach identifies inflection points where the signal transitions from increasing to decreasing intensity, making it robust to moderate noise. Estimated peaks are then available for downstream matching against reference lists or synthetic training-set generation.

## Related tools

- **PeakBot** (Python package implementing smoothing, gradient-descent peak search, and subsequent CNN-based peak classification for LC-HRMS data) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Neural network framework used to train the CNN model that classifies detected peaks as true chromatographic peaks or background signal) — https://www.tensorflow.org/
- **OpenMS/TOPPView** (Visualization tool for featureML export of detected chromatographic peaks) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Examples

```
curl https://raw.githubusercontent.com/christophuv/PeakBot_Example/main/quickExample_GPU.py > quickExample_GPU.py && python quickExample_GPU.py
```

## Evaluation signals

- Detected peaks should correspond visually to intensity maxima in the smoothed 2D chromatogram.
- Peak center coordinates (rt, mz) should fall within the estimated bounding boxes.
- Peak borders (rt_min, rt_max, mz_min, mz_max) should tightly enclose the signal above a defined threshold (e.g., half-max intensity).
- Comparison of detected peaks against reference ground-truth peaks (isolated single chromatographic peaks) should show agreement in retention time and m/z within instrument tolerance (e.g., ±5 ppm for m/z).
- Number and distribution of detected peaks should be consistent across replicate chromatograms from the same sample or reference material.

## Limitations

- Performance depends on smoothing filter choice; over-smoothing may merge adjacent peaks or eliminate small peaks, while under-smoothing may detect noise as false peaks.
- Gradient-descent algorithm may struggle with overlapping or co-eluting peaks, particularly in complex background regions or high-noise regions (walls, edges).
- Peak borders estimated by gradient-descent may be inaccurate for highly asymmetric or multi-modal peaks.
- CUDA GPU support is required for fast processing of large training datasets; CPU-only operation is slower and may require parameter tuning (blockdim, griddim) per GPU model.
- User must manually define reference list and set retention time and m/z alignment criteria; mismatches in these parameters will degrade the quality of reference feature updates.

## Evidence

- [intro] Apply smoothing to the chromatographic signal and identify local maxima using gradient-descent algorithm: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [intro] Standardized 2D area extraction for CNN input: "each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [intro] Peak matching with reference list using retention time and m/z alignment: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [readme] Input format and preprocessing workflow: "Load training chromatogram data (retention time × m/z matrix format). 2. Apply smoothing filter to the chromatographic signal to reduce noise. 3. Execute gradient-descent algorithm to locate"
- [readme] GPU acceleration and parameter tuning guidance: "the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU. To find good values for your particular GPU, the script quickFindCUDAParameters.py from the PeakBot"
