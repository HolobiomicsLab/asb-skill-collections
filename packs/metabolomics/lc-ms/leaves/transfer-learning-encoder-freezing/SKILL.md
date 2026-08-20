---
name: transfer-learning-encoder-freezing
description: Use when you have a pretrained spectrum encoder (e.g., TCN on mass spectrometry data) that has learned useful representations, and you need to train new components (e.g., a rescoring module) for a related but distinct task (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0089
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - LC-MS
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

# Transfer-Learning Encoder Freezing

## Summary

Freeze a pretrained encoder's parameters while training downstream task-specific modules (e.g., FormulaEncoder and RescoreHead) on a new objective function. This skill enables efficient transfer of learned spectrum representations without catastrophic forgetting or computational overhead of full model retraining.

## When to use

You have a pretrained spectrum encoder (e.g., TCN on mass spectrometry data) that has learned useful representations, and you need to train new components (e.g., a rescoring module) for a related but distinct task (e.g., binary classification of formula candidates) without modifying the encoder's learned features.

## When NOT to use

- The pretrained encoder was trained on a very different data domain (e.g., different mass spectrometry instrument, chemical space, or collision energy regime) with no validation on your target instrument type.
- You need to adapt the encoder to a completely new input representation (e.g., different m/z binning, intensity normalization, or spectrum preprocessing) — frozen parameters cannot learn these transformations.
- Computational resources permit full model fine-tuning and you have sufficient labeled data to avoid overfitting; encoder freezing trades flexibility for data efficiency.

## Inputs

- Pretrained encoder checkpoint (PyTorch .pt file with frozen TCN spectrum encoder weights)
- MGF-formatted MS/MS spectra with precursor m/z, collision energy, and peak lists
- Training labels (e.g., binary target for rescoring: correct vs incorrect formula candidate)
- Configuration file specifying encoder architecture and training hyperparameters

## Outputs

- State dictionaries for trainable modules (formula_encoder_state_dict, rescore_head_state_dict)
- Training loss history per epoch
- Validation/test metrics (e.g., binary cross-entropy loss, accuracy, AUROC on rescoring task)

## How to apply

Load the pretrained encoder checkpoint and explicitly freeze all its parameters using PyTorch parameter registration (e.g., `param.requires_grad = False`). Initialize new trainable modules (FormulaEncoder, RescoreHead) with their own parameter sets. Preprocess the input (e.g., zero the precursor m/z channel before passing spectra to the frozen encoder) to ensure consistency with the original training protocol. Define a task-specific loss function (e.g., binary cross-entropy for rescoring) and an optimizer that updates only the trainable modules' parameters. Run the training loop: forward pass through frozen encoder, then through trainable modules; compute loss; backpropagate (gradients flow only to trainable parameters); update trainable weights. After convergence, save state dictionaries for both the trainable modules separately from the frozen encoder checkpoint.

## Related tools

- **FIDDLE** (Deep learning method providing pretrained TCN spectrum encoder and rescoring architecture) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (Python API and CLI for loading pretrained checkpoints and running inference on frozen encoder with trainable rescoring head) — https://github.com/josiehong/msfiddle

## Examples

```
from torch import nn; encoder = load_checkpoint('fiddle_tcn_orbitrap.pt'); [p.requires_grad_(False) for p in encoder.parameters()]; formula_encoder = FormulaEncoder(...); rescore_head = RescoreHead(...); optimizer = torch.optim.Adam(list(formula_encoder.parameters()) + list(rescore_head.parameters())); loss_fn = nn.BCEWithLogitsLoss(); for epoch in range(num_epochs):
    for batch_env, batch_labels in dataloader:
        env_zero = batch_env.clone(); env_zero[:,0] = 0
        encoded = encoder(env_zero); pred = rescore_head(formula_encoder(encoded)); loss = loss_fn(pred, batch_labels); optimizer.zero_grad(); loss.backward(); optimizer.step()
```

## Evaluation signals

- Frozen encoder parameter gradients remain zero throughout training; verify via `print(model.encoder.weight.grad)` — should be None or zero tensor after first backward pass.
- Training loss on the rescoring task converges monotonically or reaches a validation plateau; overfitting to training set indicates successful parameter updates in trainable modules.
- Saved state_dict keys for trainable modules (formula_encoder_state_dict, rescore_head_state_dict) are distinct from frozen encoder keys and load without shape mismatches.
- Rescoring metrics (binary cross-entropy, AUROC on test set) improve relative to random baseline; frozen encoder should capture sufficient spectrum information for the downstream task.
- Gradient flow verification: confirm that gradients from loss backpropagation reach trainable module parameters but do not propagate into frozen encoder (use `hook` or print `requires_grad` flag).

## Limitations

- Performance is bounded by the pretrained encoder's learned representations; if the encoder was not trained on spectra representative of your target domain (instrument, collision energy, adduct type), transfer may be poor.
- The precursor m/z channel must be explicitly zeroed before the encoder (as in FIDDLE workflow step 3) to match the original training protocol; failure to do so introduces distribution shift and reduces rescoring accuracy.
- Freezing the encoder prevents adaptation to label noise or data drift in the training set; if the downstream task involves spectra significantly different from the encoder's training distribution, consider partial fine-tuning (unfreezing late encoder layers) or retraining.
- Binary cross-entropy loss assumes balanced or properly weighted classes; imbalanced rescoring labels (e.g., far more 'correct' than 'incorrect' candidates) will bias the model toward the majority class despite frozen encoder quality.

## Evidence

- [other] The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and persisting formula_encoder_state_dict and rescore_head_state_dict to the checkpoint.: "freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and persisting formula_encoder_state_dict"
- [other] 1. Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder. 4. Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only. 5. Run training loop over batches, computing BCE loss on predictions, backpropagating, and updating trainable parameters. 6. Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary.: "Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0]) from"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
