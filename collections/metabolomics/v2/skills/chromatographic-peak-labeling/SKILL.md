---
name: chromatographic-peak-labeling
description: Use when you have a user-defined reference list of isolated, high-confidence chromatographic peaks (ground-truth) matched across multiple LC-HRMS samples, and you need to produce a labelled training dataset large enough to train a CNN model that discriminates true peaks from background noise and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - CUDA
  - OpenMS/TOPPView
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

# chromatographic-peak-labeling

## Summary

Generate large-scale labelled training datasets for CNN peak detection by iteratively combining matched reference features from LC-HRMS chromatograms. This skill augments ground-truth peak properties (borders, centers, isomeric variants) with synthetic distraction peaks and background variations to train robust peak-type classifiers.

## When to use

Apply this skill when you have a user-defined reference list of isolated, high-confidence chromatographic peaks (ground-truth) matched across multiple LC-HRMS samples, and you need to produce a labelled training dataset large enough to train a CNN model that discriminates true peaks from background noise and false positives. The workflow assumes reference peaks have already been detected, matched to a reference list, and their properties (borders, centers) updated to fit the training chromatograms.

## When NOT to use

- Reference peaks have not been matched to a user-defined reference list or have not been validated as ground-truth isolated peaks.
- Input chromatograms are in centroid mode rather than profile mode (PeakBot is designed for profile mode LC-HRMS data).
- The goal is to detect peaks in a new sample, not to generate training data; use the trained CNN model directly instead.

## Inputs

- Matched reference peak features (peaks with estimated borders, centers, and assigned identities from reference chromatograms)
- Reference list (ground-truth: isolated single chromatographic peaks)
- LC-HRMS training chromatogram data (profile mode, exported as standardized 2D areas: retention time × m/z)
- Peak property metadata (isomeric variant annotations, background type labels)

## Outputs

- Labelled training instances (synthetic 2D areas: retention time × m/z)
- Labelled dataset with peak-type annotations (chromatographic peak with isomeric variants or background signal)
- Bounding-box and peak-center coordinates for each training instance
- Augmented training dataset (large number of labelled instances for CNN training)
- Exported training set in standardized format (compatible with TensorFlow CNN model input)

## How to apply

Load the matched reference features (peaks with estimated borders, centers, and assigned identities) extracted from training chromatograms. Iteratively combine these reference peaks in various proportions and spatial arrangements (retention time × m/z) to create synthetic training instances that represent both chromatographic peaks and background signal variations. For each instance, assign labels indicating peak type (true peak with left/right isomeric variants, or background), bounding box coordinates, and peak center position. Use GPU-accelerated batch generation (with tuned CUDA blockdim and griddim parameters) to produce a large augmented dataset. Export the labelled training set as standardized two-dimensional areas (retention time × m/z) with metadata describing peak type, bounding box, and peak center, suitable for direct CNN model input. Include multiple background types (walls, baseline noise) to generalize the model's discrimination capability.

## Related tools

- **PeakBot** (Python package executing the iterative combination, labelling, and GPU-accelerated batch generation of training instances from matched references) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework in which the CNN model is implemented and trained on the generated labelled instances) — https://www.tensorflow.org/
- **CUDA** (GPU computation toolkit enabling accelerated generation of large training datasets) — https://developer.nvidia.com/cuda-downloads
- **OpenMS/TOPPView** (Visualization tool for exported featureML files to verify detected and labelled chromatographic features) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- Generated training instances are all valid 2D areas (retention time × m/z) with dimensions matching the original chromatogram resolution and no NaN or out-of-range values.
- Each training instance has complete metadata: peak-type label (peak or background), bounding-box coordinates (top, bottom, left, right), and peak-center (x, y); no missing annotations.
- Bounding-box coordinates are consistent (left < right, top < bottom) and peak-center lies within the bounding-box for all peak-type instances.
- The augmented dataset size is substantially larger than the matched reference set (due to iterative combination and proportion variation), indicating successful augmentation.
- Background type labels are present and varied across instances (e.g., walls, baseline noise), confirming that distraction peaks and background variations were included during combination.

## Limitations

- GPU memory constraints: an exportBatchSize of 2048 requires ~4 GB GPU memory; must be reduced to 1024 or 512 on GPUs with less memory.
- CUDA parameters (blockdim, griddim) must be tuned for the specific GPU hardware; suboptimal parameters can cause timeouts (Windows TDR issues) or reduced performance.
- The quality of labelled instances depends critically on the accuracy of the input reference features (borders, centers, identities); errors in reference peak detection or matching will propagate to the training dataset.
- Augmentation by iterative combination and spatial arrangement may not capture all realistic peak distributions and noise patterns encountered in novel samples, limiting generalization.
- The skill requires a CUDA-enabled NVIDIA GPU for practical performance; CPU-only operation is feasible but substantially slower for large-scale dataset generation.

## Evidence

- [other] Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model.: "Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model."
- [other] Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances.: "Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances."
- [other] Assign labels to each generated instance indicating peak type (chromatographic peak with isomeric variants or background signal), bounding box, and peak center.: "Assign labels to each generated instance indicating peak type (chromatographic peak with isomeric variants or background signal), bounding box, and peak center."
- [readme] The matched references are then used to generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset). Moreover, also different background types are supported by PeakBot so that it differentiates between true chromatographic peaks and irrelevant background information (e.g., walls, which are signals present throughout the entire or large parts of the chromatograms).: "The matched references are then used to generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background"
- [readme] As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required for their generation.: "As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required"
- [other] Export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input.: "Export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input."
- [readme] Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU.: "Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU."
