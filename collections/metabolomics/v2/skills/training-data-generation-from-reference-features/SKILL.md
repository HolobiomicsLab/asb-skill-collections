---
name: training-data-generation-from-reference-features
description: Use when you have isolated, manually curated reference chromatographic peaks (ground-truth features) matched to local maxima detected in LC-HRMS profile-mode data, and you need to train a CNN classifier to distinguish peaks from background signals across diverse sample compositions.
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
  - CUDA Toolkit and cuDNN
  - OpenMS/TOPPView
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

# training-data-generation-from-reference-features

## Summary

Generate a large augmented training dataset for CNN peak classification by iteratively combining matched reference chromatographic peaks with various background types and distraction peaks. This skill is essential for training a CNN model to distinguish true LC-HRMS chromatographic peaks from background noise while learning to predict peak bounding-boxes and centers.

## When to use

You have isolated, manually curated reference chromatographic peaks (ground-truth features) matched to local maxima detected in LC-HRMS profile-mode data, and you need to train a CNN classifier to distinguish peaks from background signals across diverse sample compositions. Use this skill when a single set of reference peaks is insufficient and you must augment training data to improve generalization across different background types (e.g., walls, chemical noise) and peak co-elution scenarios.

## When NOT to use

- You already have a pre-trained CNN model or a sufficiently large labeled dataset of rt×mz images; data generation is unnecessary.
- Reference features are not reliably matched to ground-truth peaks; unvalidated references will produce poor training labels.
- Your GPU does not support CUDA or GPU memory is severely limited (< 512 MB); training-data generation will be prohibitively slow or impossible.

## Inputs

- User-defined reference list of isolated ground-truth chromatographic peaks (peak images, borders, centers)
- Training LC-HRMS profile-mode data (raw or standardized rt×mz two-dimensional areas)
- Pre-detected local maxima from training chromatograms
- GPU configuration parameters (blockdim, griddim, exportBatchSize)

## Outputs

- Augmented training dataset: large number of synthetic standardized two-dimensional rt×mz area images
- Associated training labels: peak-type (peak vs. background), peak-center coordinates, bounding-box coordinates
- Training instances incorporating multiple background types and distraction peaks for generalization

## How to apply

First, extract reference features from training chromatograms using a smoothing and gradient-descent peak-detection algorithm, estimating peak borders and centers. Match these detected peaks to a user-defined reference list (ground-truth isolated peaks), then update the reference feature properties to best fit the detected peaks. Generate training instances by iteratively combining matched references with various background types and distraction peaks to create synthetic chromatographic scenarios. Use GPU acceleration (CUDA) to accelerate the generation of large numbers of training instances, with parameters like exportBatchSize tuned to available GPU memory (e.g., 2048 for 4GB, reduced to 1024 or 512 if memory-constrained). The augmented dataset should include both true chromatographic peaks and irrelevant background information (e.g., baseline walls) so the model learns to differentiate them.

## Related tools

- **PeakBot** (Python package implementing the complete workflow: reference extraction, peak matching, training-data generation, and CNN training for LC-HRMS peak classification) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used to implement and train the CNN model on generated training instances) — https://www.tensorflow.org/
- **CUDA Toolkit and cuDNN** (GPU acceleration libraries required for fast training-data generation and CNN training on Nvidia GPUs) — https://developer.nvidia.com/cuda-downloads
- **OpenMS/TOPPView** (Optional downstream tool for visualization and validation of detected features exported as featureML files) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Evaluation signals

- The generated training dataset contains a large, balanced number of peak and background instances (expected to be orders of magnitude larger than the initial reference set due to iterative combination and augmentation).
- Each training instance is a standardized rt×mz two-dimensional image with consistent dimensions and normalized intensities, readable as input to the CNN.
- Associated labels (peak-type, peak-center, bounding-box) are numerically valid: peak-type is binary (0/1), coordinates are within image bounds, and bounding-boxes are non-degenerate rectangles.
- The training dataset includes multiple background types (e.g., baseline walls, chemical noise) to simulate real sample diversity and verify that distraction peaks and background clutter are correctly labeled as non-peaks.
- GPU memory usage and generation time scale appropriately with exportBatchSize and GPU parameters (blockdim/griddim); generated data is reproducible when using the same random seed and reference set.

## Limitations

- GPU memory constraints limit exportBatchSize; users must manually tune blockdim/griddim for their specific GPU model; training-data generation is infeasible on CPU-only systems.
- Reference feature quality directly determines training-data quality; poor initial peak detection or mismatched references will propagate errors to all generated instances.
- Augmentation via iterative combination may not capture all real-world peak coelution patterns or unusual background artifacts present in novel samples, potentially limiting CNN generalization.
- Training instances are synthetic; the model may underperform on real chromatograms if the augmentation strategy does not adequately simulate sample complexity or if reference peaks do not represent the full diversity of target analytes.

## Evidence

- [intro] generate a large number of training instances by iteratively combining them: "generate a large number of training instances by iteratively combining them"
- [readme] Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize: "Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize"
- [intro] matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [intro] the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms: "the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms"
- [readme] A GPU (CUDA) based approach is implemented that decreases the time required for their generation: "A GPU (CUDA) based approach is implemented that decreases the time required for their generation"
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] also different background types are supported by PeakBot so that it differentiates between true chromatographic peaks and irrelevant background information (e.g., walls, which are signals present throughout the entire or large parts of the chromatograms): "also different background types are supported by PeakBot so that it differentiates between true chromatographic peaks and irrelevant background information (e.g., walls, which are signals present"
