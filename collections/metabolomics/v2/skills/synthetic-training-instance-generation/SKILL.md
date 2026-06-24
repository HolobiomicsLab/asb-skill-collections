---
name: synthetic-training-instance-generation
description: Use when when you have a small set of matched reference features (isolated,
  high-quality chromatographic peaks from reference chromatograms that have been aligned
  to a ground-truth reference list) and need to train a CNN model for peak detection
  in LC-HRMS profile mode data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - CUDA
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

# Synthetic training instance generation

## Summary

Generate large labelled datasets for CNN model training by iteratively combining matched reference features (peaks with borders, centers, and identities) in various proportions and spatial arrangements. This augmentation strategy creates diverse training instances that include chromatographic peaks with isomeric variants and background signals, enabling the model to generalize across different LC-HRMS chromatographic conditions.

## When to use

When you have a small set of matched reference features (isolated, high-quality chromatographic peaks from reference chromatograms that have been aligned to a ground-truth reference list) and need to train a CNN model for peak detection in LC-HRMS profile mode data. Use this skill when the number of real training instances is insufficient to achieve high CNN model performance, or when you need to simulate diverse peak morphologies, backgrounds, and spatial arrangements without acquiring additional experimental data.

## When NOT to use

- Input dataset already contains sufficient real, experimentally-measured training instances with high coverage of peak morphologies and background types.
- Reference features have not been validated or matched to a ground-truth reference list, making labels unreliable.
- CNN model will be applied only to LC-HRMS data with identical instrumental and chromatographic conditions to the training set, where augmentation may not improve generalization.

## Inputs

- Matched reference features (peaks with estimated borders, centers, and assigned identities from reference chromatograms)
- Reference chromatograms (LC-HRMS profile mode data in standardized format)
- Ground-truth reference list (isolated single chromatographic peaks with known identities)

## Outputs

- Labelled training dataset (large collection of two-dimensional areas in retention time × m/z space)
- Training instances with metadata (peak type, bounding box, peak center annotations)
- CNN model input-ready standardized two-dimensional areas

## How to apply

Starting with matched reference features that include peak borders, centers, and assigned chemical identities, iteratively combine multiple matched references by mixing them in various proportions and spatial arrangements to create synthetic training instances. Each instance is labelled with peak type (chromatographic peak with left/right isomeric compounds or background signal), bounding box, and peak center. Include multiple background types (e.g., walls—signals present throughout entire or large chromatogram regions) and distraction peaks to generalize the training set. Export each instance as a standardized two-dimensional area in retention time × m/z space with associated metadata. Use GPU (CUDA) acceleration to reduce generation time for the large number of instances required for effective CNN training.

## Related tools

- **PeakBot** (Python package that implements synthetic training instance generation via iterative combination of matched reference features for CNN model training in LC-HRMS peak detection) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Framework used to implement the CNN model that consumes the generated synthetic training instances) — https://www.tensorflow.org/
- **CUDA** (GPU-accelerated computation framework used to decrease time required for generation of large numbers of synthetic training instances)

## Evaluation signals

- Total number of generated training instances meets or exceeds the minimum required for effective CNN convergence and high model performance, as determined by validation curves.
- Distribution of instance labels (peak type, isomeric variants, background types) matches the expected diversity from iterative combinations of matched references without class imbalance.
- Each instance exports as a valid standardized two-dimensional area (retention time × m/z) with complete metadata (bounding box, peak center, peak type) in the required format for CNN input.
- Synthetic instances exhibit morphological variation across peak borders, centers, and spatial arrangements consistent with real chromatographic variability across samples.
- CNN model trained on synthetic instances achieves target detection accuracy and false-positive rate on held-out experimental data, validating that augmentation improved generalization.

## Limitations

- Generation of large training datasets is computationally intensive and requires GPU (CUDA) support; CPU-only execution is significantly slower.
- GPU-specific parameters (blockdim, griddim) must be tuned to hardware; suboptimal values can cause crashes or inefficient execution. The quickFindCUDAParameters.py script from PeakBot examples is required to identify suitable values for a given GPU.
- Synthetic instances generated by combining only matched references may not capture all real-world peak morphologies or background artifacts present in unseen LC-HRMS chromatograms, limiting generalization to novel instrumental or chromatographic conditions.
- exportBatchSize of 2048 requires approximately 4 GB of GPU memory; systems with less memory must reduce this parameter to 1024 or 512, increasing generation time.
- Generation quality depends entirely on the quality and diversity of the input matched reference features; poor reference selection or incomplete matching will result in low-quality training instances.

## Evidence

- [other] Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model.: "Matched references are used to generate a large number of training instances by iteratively combining them, which serve as the labelled dataset for training the CNN model."
- [other] Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances.: "Iteratively combine matched reference features by mixing them in various proportions and spatial arrangements to create synthetic training instances."
- [readme] Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset). Moreover, also different background types are supported by PeakBot so that it differentiates between true chromatographic peaks and irrelevant background information (e.g., walls, which are signals present throughout the entire or large parts of the chromatograms).: "Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize (augmentation of the training dataset). Moreover, also"
- [readme] As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required for their generation.: "As a large number of training instances is required to train the CNN model and to achieve a high performance of the model, a GPU (CUDA) based approach is implemented that decreases the time required"
- [other] Export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input.: "Export the labelled training set as a standardized collection of two-dimensional areas (retention time × m/z) with associated metadata for CNN model input."
- [readme] Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU.: "Note: Different GPUs have a different number of streaming-processors. Thus, the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU."
