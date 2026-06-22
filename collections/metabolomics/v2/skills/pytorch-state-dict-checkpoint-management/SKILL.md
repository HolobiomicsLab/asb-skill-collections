---
name: pytorch-state-dict-checkpoint-management
description: Use when when training a multi-component deep learning model where some components (e.g., a pretrained TCN spectrum encoder) should remain frozen while others (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - FIDDLE
  - PyTorch
  - msfiddle
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PyTorch State Dict Checkpoint Management

## Summary

Manage selective freezing and persistence of PyTorch model components by saving individual module state dictionaries (e.g., formula_encoder_state_dict, rescore_head_state_dict) to checkpoint files while keeping other components (e.g., TCN encoder) frozen during training. This enables modular training workflows where different components are updated at different stages.

## When to use

When training a multi-component deep learning model where some components (e.g., a pretrained TCN spectrum encoder) should remain frozen while others (e.g., FormulaEncoder and RescoreHead) are trainable, and you need to persist only the trainable component weights separately for later inference or transfer learning.

## When NOT to use

- When all model components should be trainable (use standard full-model checkpoint save instead).
- When inference requires the frozen encoder to have updated parameters (the frozen encoder must remain static across training and deployment).
- When the frozen and trainable components are tightly coupled with shared gradients (this workflow assumes clean separation).

## Inputs

- Pretrained PyTorch model checkpoint (e.g., fiddle_tcn_orbitrap.pt with frozen TCN spectrum encoder)
- Training dataset with spectra and target labels (e.g., binary classification targets for rescoring)
- PyTorch Module definitions for trainable components (FormulaEncoder, RescoreHead)
- Hyperparameters: learning rate, optimizer type, loss function, batch size

## Outputs

- Checkpoint dictionary containing only trainable module state dicts (formula_encoder_state_dict, rescore_head_state_dict)
- Trained model weights for FormulaEncoder and RescoreHead components
- Training log with loss values per epoch

## How to apply

Load a pretrained PyTorch model and freeze all its parameters using model.eval() and torch.no_grad() or by setting requires_grad=False on all parameters. Initialize new trainable modules (FormulaEncoder, RescoreHead) with requires_grad=True. Configure an optimizer that targets only the trainable parameters. During the training loop, compute loss (e.g., binary cross-entropy) on the trainable module outputs, backpropagate, and update only trainable weights. After training, extract and save only the trainable modules' state dictionaries—not the frozen encoder—using torch.save({"formula_encoder_state_dict": formula_encoder.state_dict(), "rescore_head_state_dict": rescore_head.state_dict()}, checkpoint_path). At inference, load the frozen encoder and trainable modules separately, ensuring the frozen encoder's parameters remain unchanged.

## Related tools

- **FIDDLE** (Deep learning pipeline for molecular formula prediction from MS/MS spectra; uses this checkpoint strategy to train FormulaEncoder and RescoreHead while keeping TCN spectrum encoder frozen) — https://github.com/JosieHong/FIDDLE
- **PyTorch** (Deep learning framework providing state_dict() and load_state_dict() for managing module weights and checkpoint persistence)
- **msfiddle** (CLI and Python API for FIDDLE inference; loads pretrained checkpoints containing frozen encoder and trainable component state dicts) — https://github.com/josiehong/msfiddle

## Examples

```
import torch
from fiddle_models import FormulaEncoder, RescoreHead

# Load frozen encoder
tcn_encoder = torch.load('fiddle_tcn_orbitrap.pt')
for param in tcn_encoder.parameters():
    param.requires_grad = False

# Initialize trainable modules
formula_encoder = FormulaEncoder()
rescore_head = RescoreHead()

# Train with optimizer on trainable params only
optimizer = torch.optim.Adam(
    list(formula_encoder.parameters()) + list(rescore_head.parameters()),
    lr=1e-3
)

# Save checkpoint
torch.save({
    'formula_encoder_state_dict': formula_encoder.state_dict(),
    'rescore_head_state_dict': rescore_head.state_dict()
}, 'checkpoint.pt')
```

## Evaluation signals

- Frozen encoder parameters remain unchanged after training (compare initial and final checkpoint values; they should be identical).
- Training loss decreases over epochs for trainable components only, while frozen encoder contributes static feature representations.
- Saved checkpoint dictionary contains exactly the expected keys (formula_encoder_state_dict, rescore_head_state_dict) with no encoder weights.
- Model successfully loads and performs inference using the frozen encoder + trained components without shape or type mismatches.
- Optimizer step count matches the number of trainable parameters (not the total model size), confirming only trainable modules were updated.

## Limitations

- Requires careful initialization: if trainable modules have incompatible input/output shapes with the frozen encoder, training will fail silently or produce NaN losses.
- No built-in gradient checkpointing for memory efficiency; freezing reduces memory overhead but may not be sufficient for very large models.
- Separating state dicts complicates deployment: inference code must load frozen encoder and trainable components separately, increasing error surface.
- The frozen encoder's pretraining quality is a bottleneck; poor pretraining cannot be recovered by downstream trainable modules.

## Evidence

- [other] Load pretrained TCN spectrum encoder and freeze all its parameters: "Load pretrained TCN spectrum encoder and freeze all its parameters."
- [other] Initialize FormulaEncoder and RescoreHead modules with trainable parameters: "Initialize FormulaEncoder and RescoreHead modules with trainable parameters."
- [other] Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only: "Define binary cross-entropy (BCE) loss function and optimizer for FormulaEncoder and RescoreHead parameters only."
- [other] Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary: "Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary."
- [other] The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss: "The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder"
