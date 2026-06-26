---
name: local-maxima-identification
description: Use when you have raw LC-HRMS profile-mode data and need to identify
  candidate chromatographic peaks before classification or feature extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS (TOPPView)
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

# local-maxima-identification

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Detect local maxima in LC-HRMS profile-mode chromatographic data using smoothing and gradient-descent algorithms, then extract each as a standardized two-dimensional (rt × mz) feature matrix for machine learning input. This preprocessing step converts raw mass spectrometry profiles into CNN-compatible peak candidates.

## When to use

Apply this skill when you have raw LC-HRMS profile-mode data and need to identify candidate chromatographic peaks before classification or feature extraction. Use it as a preprocessing step when training or applying a CNN model for peak validation, or when you need to generate a large number of augmented training instances from reference chromatograms with known peak locations.

## When NOT to use

- Input is already a pre-processed feature table or centroided peak list—skip to peak matching or CNN inference instead.
- You have centroid-mode LC-HRMS data rather than profile mode; local-maxima detection is designed for profile-mode continuous data.
- The goal is only to match detected peaks to a reference list without retraining the CNN model; use peak matching directly instead.

## Inputs

- LC-HRMS profile-mode chromatographic data (NetCDF or vendor format)
- Smoothing parameter (e.g., kernel size for signal filtering)
- Gradient-descent algorithm parameters (step size, convergence threshold)
- Reference chromatograms with ground-truth peak locations (for training)

## Outputs

- Standardized 2D feature matrices (rt × mz areas) as NumPy arrays or HDF5 files
- Peak coordinate list (retention time and m/z of each detected local maximum)
- Metadata: peak type, peak center, bounding box coordinates for each extracted region

## How to apply

Load LC-HRMS profile-mode data and apply smoothing to reduce noise in the chromatographic signal. Compute gradients across the smoothed signal and use a gradient-descent algorithm to identify local maxima. For each detected local maximum, extract a standardized 2D region centered on the maximum, spanning a defined retention-time (rt) and mass-to-charge (mz) window. Export each 2D area as a feature matrix (e.g., NumPy array or HDF5 format) compatible with CNN ingestion. Adapt the extraction window size and smoothing parameters based on your chromatographic resolution and CNN architecture requirements. GPU acceleration (CUDA) is recommended for large datasets to reduce generation time.

## Related tools

- **PeakBot** (Python package implementing local-maxima detection via smoothing and gradient-descent, standardized 2D area extraction, and GPU-accelerated training-instance generation) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used by PeakBot to train and run the CNN model that classifies extracted 2D areas) — https://www.tensorflow.org/
- **OpenMS (TOPPView)** (Visualization tool for featureML export of detected chromatographic peaks and their bounding boxes) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Examples

```
python quickExample_GPU.py
```

## Evaluation signals

- Visual inspection: overlay detected local maxima on the chromatogram profile to confirm alignment with visible peaks and absence of noise artifacts.
- Schema check: each exported 2D feature matrix has correct dimensions (rt × mz pixels) and contains non-zero values centered near the reported peak coordinate.
- Matching recall: percentage of ground-truth reference peaks matched by the detected local maxima (expected >90% for well-behaved reference chromatograms).
- CNN classification accuracy: downstream CNN model trained on generated 2D areas should report true peak vs. background classification accuracy consistent with published PeakBot benchmarks.
- Bounding-box consistency: estimated peak borders and centers from the gradient-descent step should align with manual peak boundaries in validation samples.

## Limitations

- GPU memory requirements scale with batch size (e.g., exportBatchSize of 2048 requires ~4 GB; smaller batches (512–1024) may be needed for limited hardware).
- Gradient-descent algorithm performance depends on smoothing parameter tuning; insufficient smoothing retains noise, while over-smoothing may merge nearby peaks or miss sharp features.
- CUDA parameters (blockdim, griddim) must be configured per GPU model; mismatched settings cause performance degradation or runtime errors (utilities like quickFindCUDAParameters.py help optimize).
- Local-maxima detection may identify artifacts (walls, background signals) as candidates; downstream CNN classification is required to filter false positives.
- Performance degrades in crowded mass spectra with overlapping peaks; reference-list matching helps but requires ground-truth peak isolation for training.

## Evidence

- [other] identifies local-maxima in LC-HRMS datasets and exports each as a standardized two-dimensional area (rt × mz region) centered on the maximum: "PeakBot identifies local-maxima in LC-HRMS datasets and exports each as a standardized two-dimensional area (rt × mz) for use as input to a machine-learning CNN model."
- [other] smoothing and gradient-descent algorithm to identify local maxima, then extract and export standardized 2D regions: "1. Load LC-HRMS profile-mode data from the input file. 2. Apply smoothing to the chromatographic signal. 3. Compute gradients and identify local maxima using gradient-descent algorithm. 4. For each"
- [readme] searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [readme] GPU (CUDA) based approach decreases the time required for training-instance generation with large datasets: "As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required"
- [readme] exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] blockdim and griddim parameters must be chosen according to GPU streaming-processor count: "Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly."
