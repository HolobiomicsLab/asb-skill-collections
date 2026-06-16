---
name: binary-cross-entropy-loss-optimization
description: Use when you have a pre-trained TCN spectrum encoder, annotated MS/MS spectra paired with ground-truth molecular formulas, and you want to train only the formula ranking and rescoring components without retraining the spectrum feature extractor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - msfiddle
  - FIDDLE
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
---

# binary-cross-entropy-loss-optimization

## Summary

Train a Siamese rescore model by optimizing binary cross-entropy loss on a FormulaEncoder and RescoreHead while keeping a pre-trained TCN spectrum encoder frozen. This skill is used to refine molecular formula predictions by learning to rank candidate formulas against ground-truth annotations.

## When to use

You have a pre-trained TCN spectrum encoder, annotated MS/MS spectra paired with ground-truth molecular formulas, and you want to train only the formula ranking and rescoring components without retraining the spectrum feature extractor. The rescore model must distinguish between correct and incorrect formula candidates using a binary classification objective.

## When NOT to use

- The TCN spectrum encoder has not been pre-trained or validated on your instrument type (e.g., you need an Orbitrap model but only have Q-TOF weights).
- You lack annotated ground-truth molecular formula labels for your spectra.
- Your goal is to improve spectrum feature extraction rather than formula ranking; in that case, retrain the TCN encoder instead of freezing it.

## Inputs

- Pre-trained TCN spectrum encoder checkpoint (.pt file)
- Training dataset with annotated MS/MS spectra (mgf format with TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY fields)
- Ground-truth molecular formula annotations paired with spectra
- Validation dataset with annotated spectra and formulas

## Outputs

- Trained FormulaEncoder state dictionary (serialized)
- Trained RescoreHead state dictionary (serialized)
- Model checkpoint containing best validation formula_acc (with H)
- Training log with per-epoch validation metrics

## How to apply

Load the pre-trained TCN spectrum encoder weights and freeze all its parameters to prevent gradient updates during training. Initialize FormulaEncoder and RescoreHead modules with random weights. Prepare a training dataset with annotated MS/MS spectra and their corresponding ground-truth molecular formulas. Optimize using binary cross-entropy loss, updating only FormulaEncoder and RescoreHead parameters. Monitor the validation metric formula_acc (with H) after each epoch, and save model checkpoints only when this metric improves over the previous best value. Extract and serialize the formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint.

## Related tools

- **msfiddle** (CLI and Python API for running pre-trained FIDDLE inference and downloading checkpoints; used to validate trained rescore model on test data) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase containing train_rescore.py script, model definitions (TCN encoder, FormulaEncoder, RescoreHead), and configuration files for rescore model training) — https://github.com/JosieHong/FIDDLE

## Examples

```
python train_rescore.py --train_data ./data/train_spectra.mgf --val_data ./data/val_spectra.mgf --resume_path ./check_point/fiddle_tcn_orbitrap.pt --output_path ./check_point/fiddle_rescore_orbitrap.pt --device 0
```

## Evaluation signals

- formula_acc (with H) metric on validation set improves monotonically or plateaus before overfitting, indicating the binary classification objective is optimizing the intended ranking behavior.
- Checkpoint is saved only when validation formula_acc (with H) exceeds the previous best value, confirming the improvement tracking logic works.
- Extracted state dictionaries contain only FormulaEncoder and RescoreHead parameters; TCN encoder parameters are absent or unchanged from the pre-trained checkpoint.
- Serialized checkpoint files are loadable and contain matching tensor shapes for formula_encoder_state_dict and rescore_head_state_dict as defined in the model architecture.
- Inference on held-out test spectra using the trained rescore model produces ranked formula candidates with confidence scores consistent with binary cross-entropy logits.

## Limitations

- The rescore model redesign to Siamese architecture in v2.0.0 introduces a structural change that may affect compatibility with older checkpoint formats or training scripts.
- No explicit discussion section in CHANGELOG or README documents limitations such as failure modes on chimeric spectra, low-intensity peaks, or instrument-specific noise characteristics.
- The skill assumes the pre-trained TCN encoder is adequate for the target instrument type (Orbitrap vs. Q-TOF); cross-instrument transfer is not validated in the provided materials.

## Evidence

- [other] Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates. Initialize FormulaEncoder and RescoreHead modules with random weights.: "Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates. Initialize FormulaEncoder and RescoreHead modules with random weights."
- [other] Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch.: "Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch."
- [other] Save model checkpoint only when formula_acc (with H) improves over previous best validation metric.: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [intro] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: "The rescore model has been redesigned with a Siamese architecture in version 2.0.0"
- [readme] For training from scratch, see the train scripts (train_tcn_gpus.py,: "For training from scratch, see the train scripts (train_tcn_gpus.py,"
