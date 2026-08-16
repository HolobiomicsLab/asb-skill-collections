---
name: standardized-region-export-for-deep-learning
description: Use when you have LC-HRMS profile-mode data with detected local maxima (from gradient-descent peak finding) and need to prepare them as input for a convolutional neural network trained to classify peaks vs. background signal or to estimate peak boundaries and centers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS (TOPPView)
  techniques:
  - mass-spectrometry
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

# standardized-region-export-for-deep-learning

## Summary

Export detected local maxima from LC-HRMS profile-mode data as standardized two-dimensional (rt × mz) regions suitable for CNN model ingestion. This skill transforms raw chromatographic peaks into uniform feature matrices that enable consistent deep-learning-based peak classification.

## When to use

You have LC-HRMS profile-mode data with detected local maxima (from gradient-descent peak finding) and need to prepare them as input for a convolutional neural network trained to classify peaks vs. background signal or to estimate peak boundaries and centers. Use this skill when your downstream task is neural-network-based peak validation or bounding-box prediction.

## When NOT to use

- Input is already a pre-aligned feature table or spectrum library (no local-maxima detection needed).
- Your analysis goal is traditional peak integration or quantification, not peak classification or deep-learning inference.
- LC-HRMS data is in centroid mode rather than profile mode (centroid data lacks the fine rt × mz resolution needed for CNN training).

## Inputs

- LC-HRMS profile-mode data (raw or smoothed chromatographic signal)
- Detected local-maxima coordinates (rt, mz pairs from gradient-descent algorithm)
- Peak border and center estimates (from pre-detection phase)

## Outputs

- Standardized two-dimensional feature matrices (rt × mz regions as NumPy arrays)
- Exported regions in CNN-compatible format (HDF5 or NumPy array files)
- Feature matrix collection indexed by local-maximum ID

## How to apply

After identifying local maxima using smoothing and gradient-descent peak detection, extract a fixed-size two-dimensional region (retention-time × m/z) centered on each maximum. Standardize the region size and intensity scaling so all extracted areas have uniform dimensions and value ranges compatible with CNN input tensors. Export each standardized area as a separate NumPy array or HDF5 matrix. The standardization ensures the CNN receives consistent feature geometry across all training and inference samples, enabling the model to learn peak morphology invariant to absolute chromatogram dimensions.

## Related tools

- **PeakBot** (Python package that implements local-maxima detection, standardized region extraction, and CNN-based peak classification for LC-HRMS profile-mode data) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep-learning framework used to implement the CNN model that ingests standardized rt × mz regions and outputs peak type, center, and bounding box) — https://www.tensorflow.org/
- **OpenMS (TOPPView)** (Visualization and analysis platform for chromatographic feature detection; PeakBot exports standardized peaks as featureML files for visualization in TOPPView) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- All exported regions have identical dimensions (rt × mz pixel count) and consistent value ranges (e.g., 0–1 after normalization).
- Each region is centered on the reported local-maximum coordinate with reproducible offset.
- Exported arrays conform to CNN input schema (e.g., shape matches model's expected input layer, dtype is float32).
- Region size is sufficient to capture peak boundaries and surrounding context without excessive padding or truncation.
- Exported feature matrices can be successfully ingested by the trained CNN model without shape/type errors; model predictions (peak type, center, bounding box) are semantically valid.

## Limitations

- Standardized region size must be chosen to balance peak morphology capture with computational cost; too small regions may truncate peak edges, too large regions introduce noise and slow CNN inference.
- Requires accurate prior local-maxima detection; regions centered on false positives or mislocalized peaks will introduce label noise into training or misclassified peaks in inference.
- GPU memory and time requirements scale with exportBatchSize parameter; the README notes that exportBatchSize=2048 requires ~4 GB GPU memory; smaller batch sizes (512–1024) are needed for GPUs with less memory.
- Different GPU architectures require tuning of CUDA blockdim and griddim parameters; suboptimal values significantly degrade extraction performance.

## Evidence

- [other] For each detected local maximum, extract a standardized 2D area (rt × mz region) centered on the maximum.: "For each detected local maximum, extract a standardized 2D area (rt × mz region) centered on the maximum."
- [other] Export each standardized area as a separate feature matrix in a format compatible with CNN ingestion (e.g., NumPy array or HDF5).: "Export each standardized area as a separate feature matrix in a format compatible with CNN ingestion (e.g., NumPy array or HDF5)."
- [readme] uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly.: "Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly."
