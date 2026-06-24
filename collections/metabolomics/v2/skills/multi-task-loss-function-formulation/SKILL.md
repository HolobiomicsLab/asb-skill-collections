---
name: multi-task-loss-function-formulation
description: Use when when training an object detection network that must predict
  both discrete labels (e.g., true peak vs. false peak) and continuous coordinates
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PyTorch
  - QuanFormer
  techniques:
  - LC-MS
  license_tier: open
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

# multi-task-loss-function-formulation

## Summary

Design and combine separate loss functions for peak classification and boundary localization in a CNN-Transformer object detection network, optimizing both tasks jointly during end-to-end training. This skill is essential when a single model must simultaneously solve two related but distinct regression or classification problems (e.g., true/false peak prediction + peak coordinate localization).

## When to use

When training an object detection network that must predict both discrete labels (e.g., true peak vs. false peak) and continuous coordinates (e.g., peak start/end positions in LC-MS ROIs), and you need a single loss function that balances both objectives without one task dominating the other during backpropagation.

## When NOT to use

- Input data is already a feature table or quantified peak area matrix; this skill is for raw ROI detection and localization, not post-detection analysis.
- Only one task is needed (e.g., binary classification without boundary regression); use single-task loss functions instead.
- Training data lacks ground-truth boundary coordinates; the regression head cannot be supervised without localization labels.

## Inputs

- Annotated ROI snippets (tensor windows from LC-MS data)
- Ground-truth peak/non-peak binary labels per ROI
- Ground-truth peak boundary coordinates (start, end positions)
- Untrained or pre-trained CNN-Transformer encoder architecture

## Outputs

- Trained model checkpoint with learned weights
- Architecture definition file (model parameters and loss formulation)
- Training logs with classification and localization loss curves

## How to apply

Define separate loss heads for each task: a binary classification head outputting logits for true/false peak labels (use cross-entropy loss) and a boundary regression head outputting start/end position coordinates (use smooth L1 or focal loss). Combine these losses by weighted summation or learnable weighting to create a unified multi-task objective. Load annotated training data with ground-truth peak/non-peak labels and boundary coordinates for each ROI snippet. Train the model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly by computing gradients through the combined loss. The rationale is that joint optimization forces the shared CNN-Transformer encoder to learn spectral features and long-range mass chromatogram dependencies that serve both tasks, preventing overfitting to one objective at the expense of the other.

## Related tools

- **PyTorch** (Deep learning framework used to implement the CNN-Transformer encoder, define multi-task loss function, and run backpropagation training)
- **QuanFormer** (Complete implementation of peak detection combining CNN-Transformer with multi-task loss for peak classification and boundary localization in LC-MS data) — https://github.com/LinShuhaiLAB/QuanFormer

## Evaluation signals

- Loss curves for classification and localization tasks both decrease monotonically over epochs, indicating joint optimization is working.
- Classification head produces binary logits in expected range (e.g., 0–1 after softmax) and localization head outputs boundary coordinates within ROI pixel bounds.
- Validation performance on held-out annotated ROI snippets shows both tasks converge (e.g., peak classification F1 score > 0.85, boundary coordinate MAE within acceptable tolerance).
- Gradient flow is non-zero through both task heads during backpropagation; no task head is starved of updates.
- Saved model checkpoint size is consistent with architecture (>300 MB expected for full CNN-Transformer) and can be loaded without shape mismatches.

## Limitations

- Requires high-quality annotated training data with both peak/non-peak labels and precise boundary coordinates; missing or mislabeled boundary coordinates degrade localization performance.
- Relative weighting between classification and localization losses must be tuned or learned; poor weight balance causes one task to dominate, reducing the other task's performance.
- Method is developed and validated on high-resolution LC-MS metabolomics data; applicability to other mass spectrometry formats (centroided vs. profile data) or instruments requires re-training and validation.
- Joint optimization may result in suboptimal solutions for each individual task compared to task-specific single-task models, depending on task correlation and data overlap.

## Evidence

- [other] Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates.: "Define the peak classification head to output binary logits (true/false peak) and the boundary localization head to output peak start/end position coordinates."
- [other] Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks.: "Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks."
- [other] Load training data comprising annotated ROI snippets with ground-truth peak/non-peak labels and boundary coordinates.: "Load training data comprising annotated ROI snippets with ground-truth peak/non-peak labels and boundary coordinates."
- [other] Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly.: "Train the combined model end-to-end using backpropagation, optimizing both the classification and localization objectives jointly."
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
