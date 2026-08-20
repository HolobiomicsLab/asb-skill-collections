---
name: cnn-transformer-hybrid-architecture-design
description: Use when when you need to detect and classify peaks in LC-MS regions
  of interest (ROIs) and simultaneously localize their boundaries for area integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - QuanFormer
  - PyTorch
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c04531
  title: QuanFormer
evidence_spans:
- written in Python (v3.8.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quanformer_cq
    doi: 10.1021/acs.analchem.4c04531
    title: QuanFormer
  dedup_kept_from: coll_quanformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04531
  all_source_dois:
  - 10.1021/acs.analchem.4c04531
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cnn-transformer-hybrid-architecture-design

## Summary

Design and implement a hybrid CNN-Transformer encoder architecture that combines convolutional layers for local spectral feature extraction with transformer layers for long-range dependency modeling in LC-MS peak detection. This architecture enables joint optimization of peak classification (true/false) and boundary localization tasks.

## When to use

When you need to detect and classify peaks in LC-MS regions of interest (ROIs) and simultaneously localize their boundaries for area integration. Use this skill when your input is annotated ROI snippets from high-resolution LC-MS data and you require binary peak classification plus coordinate regression in a single end-to-end model.

## When NOT to use

- Input data is already a feature table or pre-quantified peak list; this skill is for raw ROI detection and localization.
- Peak detection in centroided or processed LC-MS data where ROI extraction has not been performed; the architecture assumes structured 2D ROI windows as input.
- Tasks requiring only classification without boundary localization; simpler architectures may be more efficient.

## Inputs

- ROI snippets (image-like 2D arrays of m/z × retention time intensity values)
- Ground-truth binary peak labels (true peak vs. false peak) per ROI
- Ground-truth peak boundary coordinates (start and end positions in ROI windows)
- Hyperparameter configuration (learning rate, batch size, loss weights)

## Outputs

- Trained model checkpoint (.pth file)
- Peak classification logits (confidence scores for true/false peak classification)
- Peak boundary localization coordinates (start and end positions)
- Joint loss curve and per-task loss metrics over training epochs

## How to apply

Construct a hybrid encoder by stacking convolutional layers to extract local spectral features from ROI windows, followed by transformer layers to capture long-range dependencies in the mass chromatogram signal. Define two task-specific heads: a peak classification head outputting binary logits (true/false peak) and a boundary localization head outputting peak start/end position coordinates. Combine classification loss (e.g., cross-entropy) and boundary regression loss (e.g., smooth L1 or focal loss) into a joint objective function. Load annotated training data with ground-truth peak/non-peak labels and boundary coordinates, then train the combined model end-to-end using backpropagation to jointly optimize both objectives. Save the trained checkpoint and architecture definition for inference on new ROI data.

## Related tools

- **QuanFormer** (Reference implementation of the CNN-Transformer hybrid architecture for LC-MS peak detection and quantification) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Deep learning framework for implementing and training the hybrid CNN-Transformer model)

## Evaluation signals

- Classification accuracy and F1-score on held-out test ROIs comparing predicted binary labels to ground truth
- Intersection-over-Union (IoU) or mean absolute error between predicted and ground-truth peak boundary coordinates
- Joint loss convergence: both classification loss and localization loss should decrease monotonically during training without divergence
- Inference speed: trained checkpoint should process ROI batches with latency compatible with the intended deployment setting
- Visualization check: overlay predicted boundaries and classification confidence on raw ROI images to detect systematic mislocalizations or false positives

## Limitations

- Architecture is optimized for high-resolution LC-MS metabolomics data; generalization to other mass spectrometry modalities (e.g., low-resolution, ion mobility) not explicitly validated.
- Requires substantial annotated training data with accurate peak and boundary labels; performance degrades significantly with label noise or class imbalance.
- Inference depends on pre-extracted ROIs; quality of ROI extraction (m/z tolerance, retention time window) directly affects downstream detection accuracy.
- Model checkpoint size exceeds 300 MB, requiring careful resource management in resource-constrained environments.
- Joint loss function requires careful tuning of loss weights between classification and localization tasks; suboptimal weighting can cause one task to dominate training.

## Evidence

- [other] Design and construct a hybrid CNN-Transformer encoder architecture where convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal.: "Design and construct a hybrid CNN-Transformer encoder architecture where convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies"
- [other] Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates.: "Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates."
- [other] Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks.: "Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks."
- [other] Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly.: "Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly."
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
