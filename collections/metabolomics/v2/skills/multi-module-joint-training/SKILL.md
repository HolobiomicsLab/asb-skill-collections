---
name: multi-module-joint-training
description: Use when when you have a pretrained encoder that captures domain knowledge
  (e.g., spectral feature extraction) and need to train task-specific decoder or scoring
  modules on top of it without degrading the encoder's learned representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  - PyTorch
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multi-module joint training

## Summary

Train multiple neural network modules jointly while selectively freezing components to preserve learned representations and focus optimization on trainable submodules. In FIDDLE's rescore pipeline, this involves freezing a pretrained TCN spectrum encoder while jointly optimizing a FormulaEncoder and RescoreHead with binary cross-entropy loss.

## When to use

When you have a pretrained encoder that captures domain knowledge (e.g., spectral feature extraction) and need to train task-specific decoder or scoring modules on top of it without degrading the encoder's learned representations. Specifically applicable when you want to leverage frozen feature extraction while adapting higher-level prediction or ranking tasks to new data.

## When NOT to use

- When the pretrained encoder has not been validated on your target domain; frozen component features may not transfer well.
- When you have very limited labeled data for the trainable modules; the frozen encoder may not compensate for insufficient optimization signal.
- When all model components need to be retrained from scratch (e.g., architecture mismatch or domain shift too severe); full fine-tuning may be required instead.

## Inputs

- Pretrained TCN spectrum encoder weights (PyTorch checkpoint)
- MS/MS spectrum array with precursor m/z channel (env shape: [batch_size, num_peaks])
- Binary rescore labels (0 or 1 per spectrum)
- Training configuration (learning rate, batch size, epochs)

## Outputs

- Trained FormulaEncoder state dictionary
- Trained RescoreHead state dictionary
- Checkpoint file containing both state dicts as separate keys
- Training logs (loss values, validation metrics)

## How to apply

Load the pretrained TCN spectrum encoder and freeze all its parameters to prevent gradient updates during backpropagation. Initialize trainable FormulaEncoder and RescoreHead modules with their own learnable weights. Preprocess input spectra by zeroing the precursor m/z channel (env[:,0]) before passing to the frozen encoder to remove instrument-specific artifacts. Define a binary cross-entropy loss function and optimizer that only updates the trainable FormulaEncoder and RescoreHead parameters. Run the training loop over batches, computing BCE loss on binary rescore targets, backpropagating gradients only through trainable modules, and updating their parameters. Checkpoint both formula_encoder_state_dict and rescore_head_state_dict separately so they can be loaded or reused independently.

## Related tools

- **FIDDLE** (Deep learning framework implementing the multi-module joint training pipeline with Siamese rescore architecture, frozen TCN encoder, and trainable FormulaEncoder/RescoreHead) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package and CLI providing inference interface for FIDDLE models trained via multi-module joint training, enabling prediction on new MS/MS spectra) — https://github.com/josiehong/msfiddle
- **PyTorch** (Deep learning framework used to implement parameter freezing, optimizer instantiation, and selective gradient computation for trainable modules)

## Examples

```
python train_rescore.py --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --train_data ./data/train_spectra.mgf --epochs 50 --batch_size 32 --learning_rate 0.001 --device 0
```

## Evaluation signals

- Verify that gradients are zero for all frozen TCN encoder parameters (grad is None or all zeros) while FormulaEncoder and RescoreHead parameters accumulate non-zero gradients.
- Confirm that loss decreases over epochs and validation binary cross-entropy converges, indicating trainable modules are learning.
- Check that checkpoint files contain exactly two keys: formula_encoder_state_dict and rescore_head_state_dict, each with the correct parameter names and shapes.
- Validate that precursor m/z channel (env[:,0]) is successfully zeroed before encoder input by inspecting tensor values.
- Evaluate rescore model performance on held-out test set using metrics like ROC-AUC or F1-score to confirm joint training improved ranking accuracy.

## Limitations

- The frozen TCN encoder's quality directly bounds the trainable modules' performance; if the pretrained encoder has poor spectral representations for your data domain, joint training will not recover.
- Zeroing the precursor m/z channel assumes this peak carries instrument-specific noise rather than chemical information; this may not be appropriate for all MS/MS protocols or ionization sources.
- Binary cross-entropy loss in the rescore task requires well-balanced training labels (correct vs. incorrect formula candidates); imbalanced data may bias the RescoreHead toward the majority class.
- Joint training with a frozen encoder is only effective if the encoder was trained on related data; significant domain shift (e.g., different mass analyzer or collision energy distribution) may require partial unfreezing or full fine-tuning.

## Evidence

- [other] Load pretrained TCN spectrum encoder and freeze all its parameters: "Load pretrained TCN spectrum encoder and freeze all its parameters."
- [other] Initialize FormulaEncoder and RescoreHead modules with trainable parameters: "Initialize FormulaEncoder and RescoreHead modules with trainable parameters."
- [other] Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder: "Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder."
- [other] Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only: "Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only."
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
- [other] Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary: "Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary."
