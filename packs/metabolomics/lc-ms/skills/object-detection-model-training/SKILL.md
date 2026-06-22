---
name: object-detection-model-training
description: Use when you have annotated LC-MS ROI snippets with ground-truth peak/non-peak labels and boundary coordinates (peak start/end positions), and you need to build a model that can discriminate true peaks from false peaks while precisely localizing peak boundaries for area integration in future LC-MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - QuanFormer
  techniques:
  - LC-MS
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

# object-detection-model-training

## Summary

Train a hybrid CNN-Transformer object detection network to classify peaks in LC-MS regions of interest (ROIs) as true or false peaks and localize their boundaries. This skill combines convolutional feature extraction with transformer-based long-range dependency modeling to jointly optimize peak classification and boundary regression.

## When to use

You have annotated LC-MS ROI snippets with ground-truth peak/non-peak labels and boundary coordinates (peak start/end positions), and you need to build a model that can discriminate true peaks from false peaks while precisely localizing peak boundaries for area integration in future LC-MS analyses.

## When NOT to use

- Input is already a feature table or peak list with quantified areas—skip directly to quantification/statistical analysis.
- You have only centroided LC-MS data without the ability to extract ROI snippets from profile data—the model is trained on spectral intensity patterns within ROIs.
- Ground-truth annotations are incomplete or labels are ambiguous (true vs. false peak judgments must be consistent and reliable for supervised training).

## Inputs

- Annotated LC-MS ROI snippets (image-like spectral windows extracted from high-resolution mass chromatograms)
- Ground-truth peak/non-peak binary labels per ROI
- Ground-truth peak boundary coordinates (start and end positions) per ROI
- mzML format raw LC-MS data (for ROI extraction and training data construction)

## Outputs

- Trained object detection model checkpoint (.pth file)
- Model architecture definition
- Binary peak classification predictions (true/false for each ROI)
- Peak boundary localization predictions (start/end coordinates)

## How to apply

Design a hybrid encoder architecture where convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal. Define a dual-head architecture: one head outputs binary logits (true/false peak classification) and the other outputs peak start/end position coordinates (boundary localization). Combine both objectives with a multi-task loss function—use cross-entropy for classification and smooth L1 or focal loss for boundary regression. Load training data as annotated ROI snippets with ground-truth labels and coordinates, then train the combined model end-to-end using backpropagation to jointly optimize both the classification and localization objectives. Use a confidence threshold (e.g., 0.99) during inference to filter low-confidence predictions, and save the trained model checkpoint and architecture definition for deployment.

## Related tools

- **PyTorch** (Deep learning framework for implementing and training the hybrid CNN-Transformer architecture) — https://pytorch.org
- **QuanFormer** (Reference implementation of the CNN-Transformer object detection pipeline for peak detection in LC-MS ROIs) — https://github.com/LinShuhaiLAB/QuanFormer
- **Python** (Programming language for model training and checkpoint management)

## Examples

```
# After preparing annotated training ROI data and ground-truth labels, train with: python -c "import torch; model = train_object_detection_network(train_rois, train_labels, train_boundaries, epochs=100, lr=0.001); torch.save(model.state_dict(), 'checkpoint0029.pth')"
```

## Evaluation signals

- Validation loss (classification + localization combined) shows monotonic decrease or plateaus at a reasonable value after training epochs.
- Binary classification metrics (precision, recall, F1-score) on held-out validation ROIs exceed domain-appropriate thresholds (e.g., F1 > 0.85 for peak discrimination).
- Boundary localization error (e.g., mean absolute error between predicted and ground-truth start/end positions) is within acceptable tolerances for peak area integration (typically ≤ 2–5 sample points).
- Model checkpoint file size is ≥ 300 MB (as noted in QuanFormer README), indicating full parameter storage.
- Inference on test ROIs produces predictions that can be filtered by confidence threshold (≥ 0.99) and yield meaningful peak area values when integrated.

## Limitations

- Model is trained on high-resolution LC-MS data for metabolomics; generalization to other peak detection domains (e.g., proteins, lipids) requires retraining on domain-specific annotated ROIs.
- Training data quality and annotation consistency directly determine model performance; ambiguous or mislabeled ground truth will degrade both classification and localization accuracy.
- The method requires profile LC-MS data (not centroided) for ROI extraction and training; centroided data loses the spectral fine structure needed for transformer-based long-range dependency learning.
- Computational cost during training scales with ROI window size and dataset size; GPU (NVIDIA CUDA 11.7 recommended) is strongly recommended for feasible training times.

## Evidence

- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [other] convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal: "convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal"
- [other] Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates: "Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates"
- [other] Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks: "Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks"
- [other] Load training data comprising annotated ROI snippets with ground-truth peak/non-peak labels and boundary coordinates: "Load training data comprising annotated ROI snippets with ground-truth peak/non-peak labels and boundary coordinates"
- [other] Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly: "Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly"
- [readme] Keep only predictions with 0.99 confidence: "Keep only predictions with 0.99 confidence"
