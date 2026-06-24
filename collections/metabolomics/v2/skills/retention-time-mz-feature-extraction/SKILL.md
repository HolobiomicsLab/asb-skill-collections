---
name: retention-time-mz-feature-extraction
description: Use when you have LC-HRMS profile-mode data (e.g., netCDF or mzML format)
  and need to convert detected or reference chromatographic peaks into fixed-size
  2D arrays (rt × mz regions) to train or apply a convolutional neural network for
  peak classification and bounding-box prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
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

# retention-time-mz-feature-extraction

## Summary

Extract standardized two-dimensional (retention time × m/z) feature matrices from LC-HRMS profile-mode data by detecting local maxima and exporting them as fixed-size regions suitable for CNN model ingestion. This preprocessing step bridges raw chromatographic data and machine-learning-ready feature representations.

## When to use

You have LC-HRMS profile-mode data (e.g., netCDF or mzML format) and need to convert detected or reference chromatographic peaks into fixed-size 2D arrays (rt × mz regions) to train or apply a convolutional neural network for peak classification and bounding-box prediction. Apply this skill when you want to standardize peak representation across samples and augment training datasets with background noise and distraction peaks.

## When NOT to use

- Input is centroid-mode (not profile-mode) LC-HRMS data—this skill requires continuous m/z-intensity profiles, not discrete peak lists.
- Detected peaks have already been converted to a feature table or compound matrix—this skill is for the initial extraction step, not post-extraction processing.
- Peak boundaries are already known with high confidence from external methods; use this skill to standardize and augment, not to re-detect.

## Inputs

- LC-HRMS profile-mode data file (netCDF, mzML, or equivalent)
- Smoothing kernel parameters (e.g., window size)
- Gradient-descent algorithm configuration (step size, convergence threshold)
- Reference peak list (ground-truth isolated peaks for training augmentation)
- Standardized rt × mz window dimensions (e.g., pixels or m/z range)

## Outputs

- Standardized 2D feature matrices (rt × mz arrays) in NumPy or HDF5 format
- Peak-center coordinates (rt, mz) for each extracted feature
- Peak bounding-box annotations (rt_left, rt_right, mz_low, mz_high)
- Augmented training instances (combinations of peaks with background/distraction signals)
- Feature metadata (sample ID, peak type, isotopolog information)

## How to apply

First, load the LC-HRMS profile-mode data and apply smoothing to the chromatographic signal to reduce noise. Next, compute gradients along the retention-time axis and identify local maxima using a gradient-descent algorithm. For each detected local maximum, define a standardized rectangular region (rt × mz window) centered on the maximum—this ensures consistent input dimensions for the CNN. Extract the 2D intensity matrix from that window and export it in a CNN-compatible format (NumPy array or HDF5). When training, augment the dataset by combining matched reference peaks with background signals and distraction peaks to improve model generalization. GPU acceleration (CUDA) is recommended for large-scale feature generation.

## Related tools

- **PeakBot** (Python package that implements local-maxima detection via smoothing and gradient-descent, standardized 2D area extraction, and training-instance augmentation with GPU acceleration for CNN model training and peak prediction.) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep-learning framework used to train and deploy the CNN model that classifies extracted rt × mz features and predicts peak-center and bounding-box coordinates.) — https://www.tensorflow.org/
- **OpenMS/TOPPView** (Visualization and data-management tool for inspecting detected chromatographic peaks exported as featureML files from the extraction pipeline.) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Examples

```
from peakbot import PeakBot; pb = PeakBot.load_lchrms_data('sample.mzML'); peaks = pb.detect_local_maxima(smoothing_window=5, gradient_threshold=0.01); features = pb.extract_standardized_regions(peaks, rt_window=60, mz_window=200); pb.export_features(features, 'output_features.h5', format='hdf5')
```

## Evaluation signals

- All extracted 2D matrices conform to the expected shape (fixed rt × mz pixel dimensions) and data type (numeric intensity values).
- Peak-center coordinates fall within the bounds of the extracted window and correspond to the local maximum detected by the gradient-descent algorithm.
- Bounding-box annotations are consistent across augmented instances of the same reference peak (after accounting for transformation).
- Augmented training instances contain a documented composition: ground-truth peak + background type + count and positions of distraction peaks.
- Exported featureML files are valid XML and can be visualized in TOPPView without parse errors; tab-separated export files match the expected column schema (rt, mz, intensity, peak_id).

## Limitations

- Gradient-descent local-maxima detection may fail or produce false positives in regions with high baseline noise, wall signals, or closely-spaced co-eluting peaks; pre-smoothing can mitigate but may suppress weak peaks.
- Standardized window size (rt × mz dimensions) must be chosen to accommodate the typical peak width and m/z spread in the dataset; oversized windows waste memory, undersized windows truncate peaks.
- GPU memory requirements scale with the batch size and window dimensions (e.g., exportBatchSize=2048 requires ~4 GB); users with limited GPU memory must reduce batch size to 512–1024.
- CUDA parameter tuning (blockdim, griddim) is GPU-specific and must be optimized per hardware; suboptimal values degrade performance or cause memory errors.
- Training-instance augmentation via iterative peak combination is data-hungry; models may overfit if the reference list is small or isotopologs are not represented.

## Evidence

- [other] PeakBot identifies local-maxima in LC-HRMS datasets and exports each as a standardized two-dimensional area (rt × mz) for use as input to a machine-learning CNN model.: "PeakBot identifies local-maxima in LC-HRMS datasets and exports each as a standardized two-dimensional area (rt × mz) for use as input to a machine-learning CNN model."
- [other] Apply smoothing to the chromatographic signal; compute gradients and identify local maxima using gradient-descent; extract standardized 2D area centered on maximum; export as CNN-compatible matrix.: "Apply smoothing to the chromatographic signal. 3. Compute gradients and identify local maxima using gradient-descent algorithm. 4. For each detected local maximum, extract a standardized 2D area (rt"
- [readme] PeakBot uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [readme] Searching for chromatographic peaks using a smoothing and gradient-descend algorithm; peaks' borders and centers are also estimated in this step.: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [readme] GPU-based approach is implemented that decreases the time required for generation of training instances; exportBatchSize of 2048 requires some 4GB of GPU-memory.: "a GPU (CUDA) based approach is implemented that decreases the time required for their generation. ... If an exportBatchSize of 2048 requires some 4GB of GPU-memory."
- [readme] Generate a large number of training instances by iteratively combining matched references; each training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize.: "generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks"
