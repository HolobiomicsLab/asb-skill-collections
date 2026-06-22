---
name: neural-network-encoder-freezing
description: Use when when you have a pre-trained encoder (e.g., TCN spectrum encoder in FIDDLE) that has learned useful representations on a source task (e.g., MS/MS spectrum encoding), and you want to train lightweight task-specific modules (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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

# neural-network-encoder-freezing

## Summary

Freeze pre-trained encoder weights in a neural network to prevent gradient updates while training task-specific decoder or head modules. This skill is used when leveraging transfer learning to adapt a pre-trained feature extractor to a new downstream task without catastrophic forgetting.

## When to use

When you have a pre-trained encoder (e.g., TCN spectrum encoder in FIDDLE) that has learned useful representations on a source task (e.g., MS/MS spectrum encoding), and you want to train lightweight task-specific modules (e.g., FormulaEncoder, RescoreHead) on a new annotated dataset without degrading the encoder's learned features through gradient descent.

## When NOT to use

- The encoder has not been pre-trained or validated on a relevant source task — freezing an untrained encoder provides no transfer learning benefit.
- Your downstream task is substantially different in modality or structure from the encoder's training task; encoder representations may not be useful and fine-tuning (unfrozen training) may be necessary.
- You have very limited training data and need to adapt all model layers — freezing reduces the model's capacity to learn task-specific representations from sparse data.

## Inputs

- Pre-trained encoder checkpoint file (.pt)
- Training dataset with annotated MS/MS spectra and ground-truth molecular formulas
- Configuration file specifying model architecture (YAML)

## Outputs

- Trained state dictionary for FormulaEncoder module
- Trained state dictionary for RescoreHead module
- Best model checkpoint selected by validation metric improvement

## How to apply

Load the pre-trained encoder weights from a checkpoint file and explicitly freeze all parameters by setting `requires_grad=False` on the encoder module, preventing any gradient flow during backpropagation. Initialize the downstream modules (e.g., FormulaEncoder, RescoreHead) with random weights so they can be trained. Prepare your training dataset with paired inputs (MS/MS spectra) and ground-truth annotations (molecular formulas). During training, compute loss only over the task-specific modules and monitor validation metrics (e.g., formula_acc with H) after each epoch. Save model checkpoints only when the validation metric improves, and serialize only the learned state dictionaries of the unfrozen modules into the output artifact, leaving the frozen encoder weights untouched.

## Related tools

- **msfiddle** (CLI and Python API for running FIDDLE inference and training pipelines with frozen/unfrozen encoder control) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase implementing the Siamese rescore model architecture with TCN spectrum encoder freezing and training of FormulaEncoder and RescoreHead modules) — https://github.com/JosieHong/FIDDLE

## Examples

```
python train_rescore.py --train_data ./data/train_spectra.mgf --val_data ./data/val_spectra.mgf --resume_path ./check_point/fiddle_tcn_orbitrap.pt --config_path ./config/fiddle_rescore_orbitrap.yml --output_dir ./trained_models --device 0
```

## Evaluation signals

- Verify that the pre-trained encoder weights remain unchanged after training by comparing checkpoint parameter values before and after the training run.
- Confirm that gradient is zero for all encoder parameters during backpropagation by inspecting `.grad` attributes or using `torch.no_grad()` context verification.
- Monitor that validation metric (formula_acc with H) improves monotonically or plateaus, indicating the downstream modules are learning without encoder degradation.
- Verify the output artifact contains only FormulaEncoder and RescoreHead state dictionaries, not the frozen encoder weights.
- Check that unfrozen module weights show non-zero changes from initialization after training, confirming they were actually updated during optimization.

## Limitations

- Freezing the encoder assumes its pre-trained representations are directly useful for the downstream task; if the source and target tasks are very different, frozen features may be suboptimal.
- The rescore model architecture was redesigned with Siamese layout in version 2.0.0, which may affect how encoder components are organized and frozen compared to earlier versions.
- No discussion section explicitly addresses reproducibility constraints or methodological limitations beyond the changelog release notes in the FIDDLE repository.

## Evidence

- [other] Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates.: "Load pre-trained TCN spectrum encoder weights and freeze all parameters to prevent gradient updates."
- [other] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: "The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior."
- [other] Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch.: "Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch."
- [other] Save model checkpoint only when formula_acc (with H) improves over previous best validation metric.: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [other] Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact.: "Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra."
