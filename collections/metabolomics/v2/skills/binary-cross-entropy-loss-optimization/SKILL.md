---
name: binary-cross-entropy-loss-optimization
description: Use when when you have a pretrained spectrum encoder (TCN) and need to train a formula rescoring module that ranks candidate molecular formulas against MS/MS spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  - PyTorch
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
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
---

# binary-cross-entropy-loss-optimization

## Summary

Train a Siamese rescore model by freezing a pretrained TCN spectrum encoder and optimizing FormulaEncoder and RescoreHead components using binary cross-entropy loss. This two-stage approach leverages spectrum feature extraction while learning formula-spectrum affinity scoring.

## When to use

When you have a pretrained spectrum encoder (TCN) and need to train a formula rescoring module that ranks candidate molecular formulas against MS/MS spectra. The trigger is having binary classification labels (correct vs. incorrect formula candidates) and wanting to transfer learned spectrum representations without retraining the encoder.

## When NOT to use

- Input spectra lack binary formula labels or ground truth; the model requires contrastive pairs (correct vs. incorrect formulas).
- The spectrum encoder checkpoint is missing or corrupted; frozen transfer learning cannot proceed without a pretrained baseline.
- Formula candidates are already ranked by an orthogonal method (e.g., isotope pattern matching or rule-based scoring); rescoring may introduce conflicting signals unless integrated carefully.

## Inputs

- Pretrained TCN spectrum encoder checkpoint (.pt file)
- MS/MS spectrum arrays (m/z and intensity pairs, with precursor m/z in env[:,0])
- Binary labels (1 = correct formula, 0 = incorrect/decoy candidate)
- Candidate formula embeddings or encoded representations

## Outputs

- Trained FormulaEncoder state dictionary
- Trained RescoreHead state dictionary
- Checkpoint file with both state dicts and optimizer state
- Rescoring confidence scores (probabilities in [0, 1]) for formula candidates

## How to apply

Load the pretrained TCN spectrum encoder checkpoint and freeze all its parameters to preserve learned spectrum feature extraction. Initialize trainable FormulaEncoder and RescoreHead modules. Zero the precursor m/z channel (env[:,0]) from input spectrum arrays before encoding to remove the precursor signal and force the model to learn from fragment patterns only. Define a binary cross-entropy (BCE) loss function and configure an optimizer (e.g., Adam) with learning rate and weight decay to update only the FormulaEncoder and RescoreHead parameters. Train over batches by computing BCE loss on predictions, backpropagating, and updating trainable weights only. After convergence, save the formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary for later inference or ensemble use.

## Related tools

- **FIDDLE** (Deep learning framework for MS/MS formula prediction; the rescore model is a Siamese architecture component trained with BCE loss after TCN encoder freezing.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package providing CLI and Python API for inference with pretrained FIDDLE checkpoints (TCN + rescore); encapsulates the trained BCE-optimized rescore module.) — https://github.com/josiehong/msfiddle
- **PyTorch** (Deep learning framework used to define and optimize the FormulaEncoder, RescoreHead modules and compute BCE loss during training.)

## Examples

```
# Python snippet to train rescore model with frozen TCN encoder
import torch
from msfiddle import MsFiddlePredictor
# Load frozen TCN checkpoint, initialize trainable modules, and train with BCE loss
# (See train_rescore.py in FIDDLE repo for full implementation)
```

## Evaluation signals

- Frozen TCN parameters remain unchanged after training (verify by checkpoint diff or parameter inspection); only FormulaEncoder and RescoreHead weights update.
- BCE loss decreases monotonically over training epochs on the training set and does not increase sharply on a held-out validation set (no divergence).
- Rescoring confidence scores fall in [0, 1] and rank correct formulas higher than decoys on a test set (rank-based precision/recall or AUC-ROC > 0.7).
- Checkpoint file contains exactly two keys (formula_encoder_state_dict, rescore_head_state_dict) with matching architecture and no frozen TCN weights.
- Precursor m/z channel zeroing is verified: env[:,0] is all zeros before encoder input; model recovers ranking ability, confirming it learns from fragments only.

## Limitations

- Freezing the TCN encoder assumes it has been pretrained on a sufficiently large and representative spectrum corpus; poor pretraining degrades rescoring accuracy.
- Zeroing the precursor m/z channel (env[:,0]) removes explicit mass information, which may hurt rescoring on spectra with weak fragment signals or high noise.
- Binary classification framing (correct vs. incorrect formula) requires explicit negative candidate generation; the model does not rank multiple plausible formulas if not trained on ranked pairs.
- The rescore model is instrument-specific (Orbitrap vs. Q-TOF); separate checkpoints and retraining are needed for different mass analyzer types.
- Training stability depends on class balance (correct vs. incorrect label proportions); imbalanced datasets may require loss weighting or sampling strategies not detailed in the workflow.

## Evidence

- [other] The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and persisting formula_encoder_state_dict and rescore_head_state_dict to the checkpoint.: "The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder, and"
- [other] 1. Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder. 4. Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only. 5. Run training loop over batches, computing BCE loss on predictions, backpropagating, and updating trainable parameters. 6. Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary.: "1. Load pretrained TCN spectrum encoder and freeze all its parameters. 2. Initialize FormulaEncoder and RescoreHead modules with trainable parameters. 3. Zero the precursor m/z channel (env[:,0])"
- [readme] The rescore model has been redesigned with a Siamese architecture in v2.0.0: "The rescore model has been redesigned (Siamese architecture)"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
