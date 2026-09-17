---
name: neural-network-architecture-training
description: Use when you have a pretrained TCN spectrum encoder from formula prediction
  and need to train a rescoring model that ranks formula candidates by confidence.
  The input is a set of spectra with ground-truth formula labels and multiple candidate
  formulas per spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0121
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

# neural-network-architecture-training

## Summary

Train a Siamese neural network architecture for MS/MS formula rescoring by freezing a pretrained TCN spectrum encoder while optimizing formula and rescore head modules with binary cross-entropy loss. This approach leverages transfer learning to improve formula prediction confidence without retraining the spectrum feature extractor.

## When to use

You have a pretrained TCN spectrum encoder from formula prediction and need to train a rescoring model that ranks formula candidates by confidence. The input is a set of spectra with ground-truth formula labels and multiple candidate formulas per spectrum. Apply this skill when you want to freeze learned spectrum representations and focus optimization on learning formula-specific scoring without degrading the encoder's generalization.

## When NOT to use

- The TCN spectrum encoder has not been pretrained or validated on your instrument type (e.g., you only have Orbitrap models but need Q-TOF spectra) — retrain or adapt the encoder first.
- Your formula candidate set is incomplete or biased (e.g., missing correct formulas) — BCE loss will optimize ranking among a truncated set and may not generalize.
- You need to jointly optimize the spectrum encoder with the rescore head (e.g., because the encoder was trained on a different MS/MS protocol) — use a warmer initialization or unfreeze encoder layers selectively.

## Inputs

- Pretrained TCN spectrum encoder checkpoint (PyTorch .pt file)
- Batch of MS/MS spectra with m/z and intensity arrays (shape: [batch_size, num_peaks, 2])
- Ground-truth formula labels and candidate formula sets per spectrum
- Configuration file specifying model architecture and training hyperparameters

## Outputs

- Trained FormulaEncoder state dictionary
- Trained RescoreHead state dictionary
- Checkpoint file containing both state dicts and optimizer state
- Binary cross-entropy loss values logged per training step

## How to apply

Load the pretrained TCN spectrum encoder checkpoint and freeze all its parameters to prevent gradient updates. Initialize trainable FormulaEncoder and RescoreHead modules. Before passing spectra to the frozen encoder, zero the precursor m/z channel (env[:,0]) to remove the redundant mass information. Define a binary cross-entropy (BCE) loss function and optimizer that updates only the FormulaEncoder and RescoreHead parameters. Run the training loop over batches, compute BCE loss on binary correctness predictions (correct vs. incorrect formula), backpropagate gradients only through trainable modules, and update their weights. After training completes, persist the formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary for later inference.

## Related tools

- **FIDDLE** (Complete deep learning pipeline for molecular formula prediction from MS/MS spectra; provides the pretrained TCN encoder and rescore model architecture) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package wrapping FIDDLE for command-line and Python API inference; used to load and run pretrained checkpoints) — https://github.com/josiehong/msfiddle
- **PyTorch** (Deep learning framework for defining neural network modules, managing checkpoints, computing gradients, and optimizing trainable parameters)

## Examples

```
python train_rescore.py --train_data ./data/training_spectra.mgf --config_path ./config/rescore_config.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --result_path ./check_point/fiddle_rescore_orbitrap.pt --device 0
```

## Evaluation signals

- The frozen TCN encoder parameters remain unchanged after training (verify by comparing encoder checkpoint before and after training).
- FormulaEncoder and RescoreHead parameters show non-zero gradient updates during backpropagation steps.
- Binary cross-entropy loss converges or decreases monotonically over training epochs, indicating the rescore head is learning to rank formulas correctly.
- Validation set rescoring accuracy (fraction of top-ranked candidates matching ground truth) improves after training relative to randomly initialized head.
- Checkpoint file contains exactly two state dict keys (formula_encoder_state_dict and rescore_head_state_dict) with matching parameter names and shapes to the training modules.

## Limitations

- The rescore model's performance is bounded by the pretrained TCN encoder's spectrum representation quality; if the encoder is poorly trained or instrument-mismatch exists (e.g., encoder from Orbitrap but spectra are Q-TOF), rescoring will not compensate.
- Freezing the encoder assumes that m/z-intensity spectrum features transfer well to the rescoring task; if the formula distribution at inference time differs significantly from training, the frozen representation may be suboptimal.
- Zeroing the precursor m/z channel (env[:,0]) is specific to the FIDDLE architecture and assumes the encoder was trained with this preprocessing; changing this step may require retraining the encoder itself.

## Evidence

- [other] The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and persisting formula_encoder_state_dict and rescore_head_state_dict to the checkpoint.: "The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and"
- [other] Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder. 4. Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only. 5. Run training loop over batches, computing BCE loss on predictions, backpropagating, and updating trainable parameters. 6. Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary.: "Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0]) from"
- [intro] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] For the full experimental codebase, see https://github.com/JosieHong/FIDDLE.: "CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle) for the full experimental codebase"
