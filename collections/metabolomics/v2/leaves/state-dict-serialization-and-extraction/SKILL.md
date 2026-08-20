---
name: state-dict-serialization-and-extraction
description: Use when after training a multi-component neural network architecture
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - msfiddle
  - PyTorch
  - FIDDLE
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# state-dict-serialization-and-extraction

## Summary

Extract and serialize PyTorch model component state dictionaries (weights and parameters) from a trained checkpoint into separate output artifacts for modular storage and reuse. This skill ensures trained neural network modules can be independently saved, versioned, and loaded downstream.

## When to use

After training a multi-component neural network architecture (e.g., FormulaEncoder and RescoreHead in a Siamese rescore model) where you need to persist individual module weights separately from a combined checkpoint, or when preparing model artifacts for deployment where different components may be loaded or frozen independently.

## When NOT to use

- The model architecture is monolithic (single module) with no subcomponents to extract separately.
- You need the full model for inference and do not require modular component reuse or transfer learning.
- The checkpoint is from an earlier version with a different architecture (e.g., v1.x) that is not compatible with the current module structure.

## Inputs

- PyTorch model checkpoint (.pt file) containing a multi-component architecture
- Model architecture definition with named submodules (e.g., formula_encoder, rescore_head)
- Validation metric or training log indicating the best checkpoint epoch

## Outputs

- Serialized state dict files (.pt format) for each model component
- Metadata or naming scheme documenting component names and checkpoint provenance

## How to apply

Load the best-performing model checkpoint identified during validation (e.g., by monitoring formula_acc with H on the validation set). Using PyTorch's `.state_dict()` method, extract the weights and parameters for each trainable module independently (e.g., `formula_encoder_state_dict = model.formula_encoder.state_dict()` and `rescore_head_state_dict = model.rescore_head.state_dict()`). Serialize each component state dict to disk using `torch.save()`, writing to files in a designated output artifact directory with descriptive filenames that indicate the component name and optionally the checkpoint metadata (e.g., epoch number, validation metric value). This enables downstream scripts to load individual modules without requiring the full combined model architecture, facilitating transfer learning and modular inference pipelines.

## Related tools

- **PyTorch** (Provides torch.save() and .state_dict() APIs for serialization and extraction of model parameters)
- **msfiddle** (Python package and CLI that uses pre-trained FIDDLE model checkpoints; internally manages state dict loading for inference) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing training scripts (train_rescore.py) that save and serialize component state dicts after training) — https://github.com/JosieHong/FIDDLE

## Examples

```
torch.save(model.formula_encoder.state_dict(), './check_point/formula_encoder_state_dict.pt'); torch.save(model.rescore_head.state_dict(), './check_point/rescore_head_state_dict.pt')
```

## Evaluation signals

- Verify that extracted state dict files are valid PyTorch tensors by loading them with torch.load() and inspecting shape and dtype consistency with the original module.
- Confirm that the extracted component state dicts contain all expected parameter keys (e.g., 'weight', 'bias' for linear layers) by comparing against model.formula_encoder.state_dict().keys().
- Test that extracted state dicts can be successfully re-loaded into fresh module instances using module.load_state_dict(extracted_dict) without shape mismatch errors.
- Verify that file sizes and metadata (creation time, file count) match expectations based on the number of components and layer counts in the architecture.
- Cross-check that reloaded modules produce identical predictions on a held-out test sample compared to inference through the original combined checkpoint.

## Limitations

- State dict extraction assumes the module architecture is statically defined and named consistently; dynamic or conditional submodule creation may cause missing or unexpected keys.
- Version compatibility: the Siamese architecture introduced in v2.0.0 is not compatible with v1.x checkpoint formats; extraction must target the correct architecture version.
- Only parameter tensors are extracted; non-learned attributes (e.g., running statistics from batch normalization, custom metadata) may require separate handling depending on the module design.
- Extracted state dicts are inert snapshots and do not preserve training state (optimizer momentum, learning rate schedules) needed for fine-tuning; full checkpoint with optimizer state is required for resuming training.

## Evidence

- [other] Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact.: "Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact."
- [other] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: "The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior."
- [other] Save model checkpoint only when formula_acc (with H) improves over previous best validation metric.: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [readme] For the full experimental codebase, see https://github.com/JosieHong/FIDDLE.: "For the full experimental codebase, see https://github.com/JosieHong/FIDDLE."
