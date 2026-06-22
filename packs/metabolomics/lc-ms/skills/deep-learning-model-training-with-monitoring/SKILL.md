---
name: deep-learning-model-training-with-monitoring
description: Use when you have a pre-trained deep learning encoder (e.g., TCN spectrum encoder trained on a large corpus) and want to adapt it to a new task (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-training-with-monitoring

## Summary

Train a subset of neural network components (FormulaEncoder and RescoreHead) while freezing a pre-trained encoder (TCN spectrum encoder), using validation-based checkpoint selection to capture the best model state. This technique balances transfer learning efficiency with targeted optimization of task-specific layers.

## When to use

You have a pre-trained deep learning encoder (e.g., TCN spectrum encoder trained on a large corpus) and want to adapt it to a new task (e.g., rescore ranking in molecular formula prediction) by training only new or task-specific head modules without risking catastrophic forgetting or overfitting the frozen encoder. Use this when you have annotated training data with a clear validation metric (e.g., formula_acc with H) to guide checkpoint selection.

## When NOT to use

- Your pre-trained encoder is not well-suited to your target task domain (domain shift is too large; freezing will hurt downstream performance more than fine-tuning would help).
- You lack annotated validation data or a clear, differentiable validation metric to guide checkpoint selection.
- Computational budget is extremely tight and you cannot afford multiple forward passes per epoch for validation; in such cases, training with a fixed schedule is more efficient.

## Inputs

- pre-trained TCN spectrum encoder model weights (checkpoint file, e.g., .pt)
- training dataset with annotated MS/MS spectra and ground-truth molecular formulas
- validation dataset with the same schema
- model architecture definition (FormulaEncoder, RescoreHead module specs)
- training hyperparameters (learning rate, batch size, loss function)

## Outputs

- best model checkpoint (filtered by validation metric improvement)
- formula_encoder_state_dict (serialized learned weights)
- rescore_head_state_dict (serialized learned weights)
- training log with epoch-wise validation metrics and loss values

## How to apply

Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates during backpropagation. Initialize new modules (FormulaEncoder, RescoreHead) with random weights. Prepare training dataset with annotated MS/MS spectra paired with ground-truth molecular formulas. Train only the unfrozen modules using binary cross-entropy loss, evaluating the validation metric (formula_acc with H) after each epoch. Save model checkpoint only when the validation metric improves over the previous best, discarding suboptimal intermediate states. After training completes, extract and serialize only the learned state_dicts for the trainable modules into output artifacts for downstream inference or ensemble use.

## Related tools

- **msfiddle** (CLI and Python API for running FIDDLE model training and inference, including rescore model training via train_rescore.py) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase containing train_rescore.py script and model architecture definitions for Siamese rescore training) — https://github.com/JosieHong/FIDDLE

## Examples

```
python train_rescore.py --train_data ./data/train_spectra.mgf --val_data ./data/val_spectra.mgf --tcn_checkpoint ./check_point/fiddle_tcn_orbitrap.pt --output_dir ./checkpoints/ --batch_size 32 --epochs 100
```

## Evaluation signals

- Validation metric (formula_acc with H) improves monotonically or plateaus without diverging, indicating stable training of unfrozen modules.
- Saved checkpoint corresponds exactly to the epoch with the highest validation metric; no checkpoint from a lower-performing epoch should be used.
- Frozen encoder weights remain unchanged from initialization to end of training (verify by comparing parameter snapshots before and after).
- Serialized state_dicts for FormulaEncoder and RescoreHead contain non-random values distinct from initialization, confirming learning occurred.
- Downstream inference using the best checkpoint produces formula predictions with measurable accuracy improvement over baseline (frozen-only) model on held-out test set.

## Limitations

- Freezing the encoder assumes the pre-trained representation is domain-appropriate; poor encoder quality or large domain shift between pre-training and target task will limit gains.
- Validation metric must be computed on every epoch, adding computational overhead; very large validation sets may slow training.
- Binary cross-entropy loss assumes binary classification; other tasks (multi-class, ranking, regression) may require different loss functions and validation metrics.
- The Siamese architecture redesign in v2.0.0 changes the encoder freezing behavior and component interaction; scripts written for v1.x may not be directly compatible.

## Evidence

- [other] Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates.: "Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates."
- [other] Initialize FormulaEncoder and RescoreHead modules with random weights.: "Initialize FormulaEncoder and RescoreHead modules with random weights."
- [other] Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch.: "Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch."
- [other] Save model checkpoint only when formula_acc (with H) improves over previous best validation metric.: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [other] Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact.: "Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact."
- [intro] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: "The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components"
- [readme] For training from scratch, see the train scripts (train_tcn_gpus.py, train_rescore.py): "For training from scratch, see the train scripts (train_tcn_gpus.py, train_rescore.py)"
