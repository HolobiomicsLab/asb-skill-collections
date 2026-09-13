---
name: peak-background-binary-classification
description: Use when you have LC-HRMS profile-mode chromatograms with extracted local
  maxima exported as standardized 2D rt×mz areas, and you need to disambiguate true
  chromatographic peaks from background signals (including wall artifacts and noise)
  at scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - TOPPView (OpenMS)
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

# peak-background-binary-classification

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Train and apply a convolutional neural network to classify local maxima in LC-HRMS data as chromatographic peaks (with optional isomeric annotation) or background noise, while simultaneously predicting peak bounding-box coordinates and center location. This skill is essential for automated, high-throughput peak detection in untargeted metabolomics workflows.

## When to use

You have LC-HRMS profile-mode chromatograms with extracted local maxima exported as standardized 2D rt×mz areas, and you need to disambiguate true chromatographic peaks from background signals (including wall artifacts and noise) at scale. Use this skill when manual peak picking is infeasible, when you require consistent peak boundary and center estimates across many samples, or when you want to handle isomeric variants (left/right peaks) systematically.

## When NOT to use

- Input is already a feature table or pre-processed peak list — skip directly to quantification or statistical testing.
- Your LC-HRMS data is acquired in centroided (not profile) mode, as the standardized 2D rt×mz area representation depends on profile-mode resolution.
- You have very few reference chromatograms or ground-truth peaks; insufficient training data will not support robust CNN generalization across sample diversity.

## Inputs

- Standardized 2D rt×mz area images extracted from LC-HRMS local maxima
- User-defined ground-truth reference list (isolated single chromatographic peaks)
- Training chromatograms (raw or profile-mode LC-HRMS data)
- Optional: isotopolog definitions for reference extension

## Outputs

- Trained CNN model (TensorFlow format)
- Peak classification labels (peak vs. background; isomer type if applicable)
- Peak bounding-box coordinates (retention time and m/z bounds)
- Peak-center coordinates (rt and mz location)
- Exported detection images (user verification)
- featureML and tab-separated-values files for downstream tools (e.g., TOPPView)

## How to apply

First, prepare training data by extracting reference features from representative chromatograms using a smoothing and gradient-descent algorithm to estimate peak borders and centers. Match detected peaks with a user-defined ground-truth reference list and extend it with isotopologs as needed. Generate large training datasets by iteratively combining matched references with distraction peaks and multiple background types (e.g., walls, baseline noise) to improve generalization. Construct a CNN with convolutional and pooling layers that outputs three predictions: (1) peak-type classification (peak vs. background, with isomer annotation), (2) peak-center coordinates, and (3) bounding-box coordinates. Train on GPU using TensorFlow with CUDA acceleration, tuning blockdim and griddim parameters to your GPU's streaming-processor count. Validate on a held-out test set, evaluating classification accuracy, bounding-box coordinate prediction error, and peak-center localization precision.

## Related tools

- **PeakBot** (Python package implementing the complete workflow: reference feature extraction via smoothing and gradient descent, peak-reference matching, training instance generation with GPU acceleration, CNN model training and inference, and export to featureML/TSV formats.) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used to implement and train the CNN model with convolutional and pooling layers for peak classification and coordinate regression.) — https://www.tensorflow.org/
- **TOPPView (OpenMS)** (Visualization tool for inspecting detected features exported in featureML format from the CNN predictions.) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Examples

```
python quickExample_GPU.py
```

## Evaluation signals

- Classification accuracy on held-out test set: proportion of correctly classified peaks vs. background signals.
- Bounding-box prediction error: mean absolute or root-mean-square error of predicted rt and m/z bounds relative to ground truth.
- Peak-center localization error: distance (in rt and m/z units) between predicted and ground-truth peak centers.
- Generalization across sample types: consistent performance metrics when applied to samples outside the training distribution (e.g., different matrix, LC method, or instrument tuning).
- Isomer disambiguation rate: when applicable, proportion of correctly annotated left/right isomeric peaks in multi-peak regions.

## Limitations

- GPU requirement (CUDA-enabled Nvidia card) for practical throughput; blockdim and griddim parameters must be tuned per GPU model to avoid memory errors or timeouts.
- Memory constraints: exportBatchSize of 2048 requires ~4 GB GPU memory; must be reduced to 1024 or 512 for GPUs with less VRAM.
- Training data quality is critical: insufficient or biased ground-truth references (e.g., missing isotopologs or background types) will limit model robustness to new samples.
- Profile-mode LC-HRMS data only; centroided data cannot be meaningfully converted to standardized 2D rt×mz areas.
- Background signal types must be explicitly represented in training (e.g., walls, chemical noise, baseline artifacts); novel background types unseen during training may not be reliably classified.

## Evidence

- [readme] uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [readme] reports whether the local-maxima is a chromatographic peak with left/right isomeric compounds or a signal of the background. Moreover, for chromatographic peaks it suggests a bounding-box and a peak-center: "reports whether the local-maxima is a chromatographic peak with left/right isomeric compounds or a signal of the background. Moreover, for chromatographic peaks it suggests a bounding-box and a"
- [readme] searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [readme] matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [readme] generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize: "generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks"
- [readme] a GPU (CUDA) based approach is implemented that decreases the time required for their generation. The CNN model is implemented in the TensorFlow package: "a GPU (CUDA) based approach is implemented that decreases the time required for their generation. The CNN model is implemented in the TensorFlow package"
- [readme] It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box.: "It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box."
- [readme] the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU.: "the blockdim and griddim need to be chosen accordingly. Please adapt these values to your GPU."
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [other] The CNN model accepts standardized two-dimensional rt×mz areas as input and outputs: (1) classification of whether each local-maximum is a chromatographic peak with left/right isomeric compounds or background signal, and (2) for peaks, a suggested bounding-box and peak-center.: "The CNN model accepts standardized two-dimensional rt×mz areas as input and outputs: (1) classification of whether each local-maximum is a chromatographic peak with left/right isomeric compounds or"
