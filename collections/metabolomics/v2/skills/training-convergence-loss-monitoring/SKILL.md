---
name: training-convergence-loss-monitoring
description: Use when executing a multi-stage deep learning pipeline (pretraining → fine-tuning → alignment) where each stage loads a checkpoint from the previous stage and you need to confirm that loss is decreasing monotonically within each stage, that checkpoints are being saved, and that no training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Hugging Face Transformers
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- github.com/OpenDFM/MS-BART
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_bart_cq
    doi: 10.48550/arxiv.2510.20615
    title: MS-BART
  dedup_kept_from: coll_ms_bart_cq
schema_version: 0.2.0
---

# training-convergence-loss-monitoring

## Summary

Monitor and validate training convergence across pretraining, fine-tuning, and alignment stages by logging loss metrics at each stage and verifying model checkpoint files are saved correctly. This skill ensures that multi-stage training pipelines (like MS-BART's three-stage process) are progressing as expected and that intermediate trained states are properly persisted.

## When to use

Apply this skill when executing a multi-stage deep learning pipeline (pretraining → fine-tuning → alignment) where each stage loads a checkpoint from the previous stage and you need to confirm that loss is decreasing monotonically within each stage, that checkpoints are being saved, and that no training divergence or collapse has occurred before proceeding to the next stage.

## When NOT to use

- Training a single-stage model without checkpointing requirements — simpler logging suffices.
- Performing inference or evaluation on a fixed pretrained model — no loss logging is needed.
- Running hyperparameter sweep where you need full reproducibility and determinism across runs; this skill monitors but does not control for seed/device variation.

## Inputs

- Training dataset (tokenized spectra-molecule pairs for pretraining, or supervised task-specific examples for fine-tuning/alignment)
- Validation dataset (same modalities, held-out split)
- Pretrained checkpoint file (for fine-tuning and alignment stages)
- Training hyperparameters (learning rate, batch size, number of epochs, loss function definition)

## Outputs

- Loss trajectory logs (per-batch or per-epoch loss values across all stages)
- Model checkpoint files saved at stage-specific paths
- Convergence validation report (qualitative assessment: 'loss decreased' / 'checkpoint saved successfully')
- Training curves (plot of loss vs. epoch/batch for each stage)

## How to apply

At each of the three training stages (pretraining, fine-tuning, and alignment), enable loss logging by configuring the training loop to record the loss value at regular intervals (e.g., per batch or per epoch). Plot or tabulate the loss trajectory to visually inspect for monotonic decrease and absence of sudden spikes or plateaus that would indicate divergence or poor convergence. In parallel, verify that model checkpoints are being written to disk at the expected paths after each stage completes (e.g., 'data/CANOPUS/pretrained-model/', 'data/CANOPUS/model-weights/'). Use validation loss on a held-out validation split to detect overfitting. Only proceed to the next stage if loss has demonstrably decreased over the training period and the checkpoint file exists and is readable.

## Related tools

- **PyTorch** (Provides training loop, loss computation, and backward pass; enables custom loss logging hooks and checkpoint saving via torch.save().)
- **Hugging Face Transformers** (Supplies Trainer class and TrainingArguments for managing multi-stage training, logging, and checkpoint management; handles loss aggregation and validation loop.)

## Examples

```
bash scripts/pretrain.sh && bash scripts/msg/finetune.sh && bash scripts/msg/align.sh
```

## Evaluation signals

- Loss values show consistent downward trend (or stable plateau) within each training stage, with no sudden divergence spikes.
- Training loss on the training set is lower than validation loss, indicating the model is not severely overfitting.
- Model checkpoint files exist at the expected paths after each stage completes and can be loaded without corruption.
- Checkpoint size and file modification timestamps confirm that checkpoints are being written and not skipped.
- No NaN or Inf values appear in the logged loss trajectory.

## Limitations

- Loss logging alone does not guarantee model quality — a low training loss may mask poor generalization; validate on held-out test data after all stages.
- Checkpoint validation only confirms file existence and readability; it does not verify that the checkpoint contains a valid trained model state until a checkpoint is actually loaded and used.
- This skill does not account for distributed training artifacts (e.g., loss synchronization across GPUs); implementation details depend on the training framework's distributed backend.
- Multi-stage checkpointing assumes each stage is independent; if stages interact or share parameters in non-obvious ways, loss patterns may not reflect true convergence of the joint model.

## Evidence

- [other] Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly.: "Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly."
- [other] Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences.: "Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences."
- [other] Load the pretrained checkpoint and execute fine-tuning stage on task-specific mass spectra structure elucidation examples with supervised loss.: "Load the pretrained checkpoint and execute fine-tuning stage on task-specific mass spectra structure elucidation examples with supervised loss."
- [readme] The folder tree are: data ├─ CANOPUS │ ├─ ... │ ├─ pretrained-model # pretrain on clean 4M pretrain dataset: "pretrained-model # pretrain on clean 4M pretrain dataset"
- [readme] The final MS-BART model on CANOPUS dataset and MassSpecGym dataset are stored in model-weights folders.: "model-weights # The final MS-BART model on CANOPUS dataset"
