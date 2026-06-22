---
name: reference-feature-combination-strategy
description: Use when when you have isolated, high-confidence reference chromatographic peaks (ground-truth) from reference LC-HRMS chromatograms that have been matched across multiple samples, and you need to train a CNN model to detect peaks in new chromatograms but lack sufficient labelled instances.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - CUDA/cuDNN
  - OpenMS
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
---

# reference-feature-combination-strategy

## Summary

Iteratively combine matched reference features (peaks with estimated borders, centers, and assigned identities from reference chromatograms) in various proportions and spatial arrangements to generate a large, labelled synthetic training dataset for CNN model training on LC-HRMS data. This augmentation strategy increases training instance diversity while maintaining ground-truth annotation.

## When to use

When you have isolated, high-confidence reference chromatographic peaks (ground-truth) from reference LC-HRMS chromatograms that have been matched across multiple samples, and you need to train a CNN model to detect peaks in new chromatograms but lack sufficient labelled instances. Use this skill to synthetically expand the training set by mixing reference features at different proportions and spatial arrangements, simulating real chromatographic variability.

## When NOT to use

- Input already consists of a sufficiently large, manually annotated training dataset with good coverage of peak types and background variability.
- Reference features have not been reliably matched across samples or lack ground-truth validation.
- Computational resources (GPU with CUDA support) are unavailable and dataset size is prohibitive for CPU-based generation.

## Inputs

- Matched reference features with estimated peak borders and centers
- User-defined reference list of isolated single chromatographic peaks
- Peak identity assignments from reference chromatograms
- LC-HRMS profile mode data (retention time × m/z arrays)

## Outputs

- Labelled synthetic training instances (standardized 2D areas: rt × mz)
- Training metadata: peak type, bounding box, peak center coordinates
- Augmented training dataset for CNN model input
- Labelled training set as tab-separated-values or featureML files

## How to apply

Load matched reference features (peaks with estimated borders, centers, and assigned identities from the reference chromatograms). Iteratively combine these matched references by mixing them in various proportions and spatial arrangements to create synthetic training instances. Each synthetic instance may consist of a chromatographic peak or background signal along with several distraction peaks to promote generalization. Assign labels to each generated instance indicating peak type (chromatographic peak with left/right isomeric variants or background signal), bounding box, and peak center. Use GPU acceleration (CUDA) to accelerate the generation of the large training dataset. Export the labelled training set as standardized two-dimensional areas (retention time × m/z) with associated metadata for CNN model input.

## Related tools

- **PeakBot** (End-to-end framework for peak detection in LC-HRMS data; manages reference feature extraction, matching, combination, CNN training, and peak detection) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework for implementing and training the CNN model on synthetic training instances) — https://www.tensorflow.org/
- **CUDA/cuDNN** (GPU acceleration libraries enabling fast generation of large synthetic training datasets) — https://developer.nvidia.com/cuda-downloads
- **OpenMS** (Visualization and analysis of detected chromatographic peaks exported as featureML files) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- Generated training instances conform to the standardized 2D area schema (retention time × m/z with numeric bounds).
- Each labelled instance has valid metadata: peak type ∈ {chromatographic peak with isomers, background signal}, bounding box with min/max rt and m/z, and peak center coordinates within bounds.
- Labelled instances exhibit diversity in peak proportions, spatial arrangements, and background types, not simple replicates of reference features.
- CNN model trained on the augmented dataset achieves higher generalization performance (e.g., precision, recall, F1 on held-out validation set) compared to a model trained on raw reference instances alone.
- Synthetic instances do not introduce artifacts (e.g., overlapping peaks with physically impossible positions) that violate chromatographic physics.

## Limitations

- Quality and diversity of synthetic instances depend critically on the breadth and reliability of the input matched reference features; sparse or biased reference sets will produce limited augmentation.
- GPU memory constraints may require adjustment of exportBatchSize (e.g., from 2048 down to 512–1024) depending on available VRAM, impacting generation throughput.
- Iterative combination strategy may not capture all real-world chromatographic peak morphologies or edge cases (e.g., highly co-eluting peaks, unusual background types) unless explicitly represented in the reference set.
- CUDA parameters (blockdim, griddim) must be tuned per GPU architecture; suboptimal parameters reduce generation speed or cause runtime errors.

## Evidence

- [other] Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model.: "Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model."
- [other] Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances.: "Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances."
- [readme] Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset).: "Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset)."
- [readme] As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required for their generation.: "As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required"
- [other] export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input.: "export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input."
