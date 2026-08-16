---
name: checkpoint-selection-based-on-validation-metric
description: Use when training neural networks on MS/MS spectra (or similar scientific data) where you need to preserve model states that improve validation performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# checkpoint-selection-based-on-validation-metric

## Summary

Select and save model checkpoints during training only when a designated validation metric improves over the previous best observed value, ensuring that only the model state achieving superior generalization is retained. This skill is essential for preventing overfitting and ensuring reproducible model artifacts in deep learning workflows.

## When to use

Apply this skill when training neural networks on MS/MS spectra (or similar scientific data) where you need to preserve model states that improve validation performance. Specifically, use it when: (1) training encoder-decoder or multi-component architectures where component freezing is involved, (2) monitoring task-specific metrics such as formula_acc (with H) on a validation set, and (3) you must serialize only the best-performing model weights to disk for downstream inference or artifact reproducibility.

## When NOT to use

- When the validation metric is unavailable or undefined (e.g., unsupervised or self-supervised training without ground truth)
- When checkpoint storage is severely constrained and you require all intermediate model states for later analysis or ensemble methods
- When the validation metric is noisy or non-monotonic by design, and you need alternative criteria (e.g., patience-based early stopping rather than strict improvement) to avoid premature convergence

## Inputs

- trained model state (PyTorch state_dict or equivalent)
- validation metric value (float)
- previous best validation metric value (float)
- epoch number (int)

## Outputs

- saved checkpoint file (.pt or .pth)
- serialized state_dict(s) for frozen and trainable components
- best validation metric tracker (float)

## How to apply

During each epoch of model training, compute the designated validation metric (e.g., formula_acc with H) on a held-out validation set. Compare the current epoch's metric value against the best metric value observed so far across all previous epochs. If the current metric exceeds the previous best, update the 'best' tracker and immediately serialize the current model state (e.g., formula_encoder_state_dict and rescore_head_state_dict) to a checkpoint file on disk. If the metric does not improve, skip the checkpoint save operation and continue training. This approach ensures only improving model iterations are retained, reducing disk I/O and guaranteeing that the final artifact represents the best validation-set generalization achieved during training.

## Related tools

- **msfiddle** (PyTorch-based deep learning framework for training molecular formula prediction models on MS/MS spectra, with built-in model state management) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing train_rescore.py and other training scripts that implement checkpoint selection logic for TCN spectrum encoder freezing and FormulaEncoder/RescoreHead component training) — https://github.com/JosieHong/FIDDLE

## Examples

```
python train_rescore.py --train_data train.mgf --val_data val.mgf --metric formula_acc_with_h --save_best_only --checkpoint_dir ./check_point/ --device 0
```

## Evaluation signals

- Verify that the saved checkpoint file exists on disk and contains only the best-epoch model weights
- Confirm that the validation metric in the saved checkpoint is monotonically non-decreasing across all saved checkpoints (i.e., each saved checkpoint has a metric ≥ all previous saved checkpoints)
- Check that the number of saved checkpoints is ≤ the total number of training epochs, confirming that not every epoch was saved
- Validate that loading the checkpoint state_dict and running inference reproduces the validation metric reported at save time, confirming serialization fidelity
- Inspect training logs to confirm that metric improvements are sparse and non-trivial (not every epoch), indicating the selection criterion is working as intended

## Limitations

- The skill assumes a single, well-defined validation metric; if multiple metrics must be optimized (e.g., precision and recall), a tie-breaking rule is required
- Checkpoint selection on validation metric alone does not guarantee test-set generalization; external benchmark evaluation is still necessary to assess true model performance
- Frequent checkpoint saves (if the metric improves in many consecutive epochs) can exhaust disk space; consider implementing a rolling-window strategy to keep only the N best checkpoints
- If validation metric plateaus early in training, the skill may save a suboptimal checkpoint before late-stage improvements occur; combining with patience-based early stopping can mitigate this

## Evidence

- [other] Save model checkpoint only when formula_acc (with H) improves over previous best validation metric.: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [other] Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch.: "Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch."
- [other] Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact.: "Extract and serialize formula_encoder_state_dict and rescore_head_state_dict from the best checkpoint into output artifact."
- [intro] The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior.: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
