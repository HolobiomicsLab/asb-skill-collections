---
name: checkpoint-serialization-and-model-persistence
description: Use when after completing a full training loop on preprocessed molecular graph data and validating model performance on a held-out validation set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - PyTorch
  - Train.py
  - Transferlearning.py
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04071
  all_source_dois:
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# checkpoint-serialization-and-model-persistence

## Summary

Serialize and persist trained GNN models to PyTorch checkpoint format after convergence, enabling reproducibility, transfer learning, and downstream inference without retraining. This skill ensures trained molecular graph representations learned during end-to-end GNN training are captured and reusable.

## When to use

After completing a full training loop on preprocessed molecular graph data and validating model performance on a held-out validation set. Apply this skill when you have a converged GNN model and need to preserve its learned parameters, architecture, and optimizer state for later transfer learning (e.g., via Transferlearning.py) or for inference on new retention-time prediction tasks.

## When NOT to use

- Model is still actively training and has not yet converged on the validation set; defer checkpoint save until validation performance stabilizes.
- Output directory lacks write permissions or disk space is exhausted; checkpoint serialization will fail silently or incompletely.
- Input model object is None or corrupted; verify model initialization and training completion before attempting serialization.

## Inputs

- Trained GNN model object (PyTorch nn.Module instance)
- Training metadata (final epoch number, converged loss value, validation metrics)
- Optimizer state dictionary (for resuming training if needed)

## Outputs

- PyTorch checkpoint file (.pt or .pth format)
- Serialized model state dictionary
- Persisted architecture and learned molecular graph representations

## How to apply

At the end of the Train.py training loop, after validation metrics stabilize or reach target performance, serialize the trained GNN model state using PyTorch's checkpoint mechanism. Save the model weights, architecture definition, and training metadata (epoch, loss history) to disk in PyTorch format (.pt or .pth). Verify the checkpoint file size matches expected model parameters and that metadata fields are readable before proceeding. Store the checkpoint in a persistent location accessible to downstream transfer-learning or inference pipelines to avoid loss of learned molecular representations.

## Related tools

- **PyTorch** (Provides torch.save() and model.state_dict() APIs for serializing trained GNN model checkpoints and optimizer state in native PyTorch format)
- **Train.py** (Produces the trained GNN model object that is serialized at convergence; executed before checkpoint save step) — https://github.com/Qiong-Yang/GNN-RT
- **Transferlearning.py** (Downstream consumer of persisted checkpoint; loads saved model state for fine-tuning on new retention-time datasets) — https://github.com/Qiong-Yang/GNN-RT

## Examples

```
torch.save(model.state_dict(), 'checkpoint.pt')
```

## Evaluation signals

- Checkpoint file exists on disk with size > 100 KB (confirms non-trivial model weights were serialized)
- PyTorch can successfully load the checkpoint via torch.load() without corruption errors
- Loaded model produces identical predictions on validation set when compared to in-memory trained model (determinism check)
- Checkpoint metadata (epoch, loss, validation metrics) are correctly stored and retrievable
- Transferlearning.py successfully initializes its GNN using the loaded checkpoint without architecture mismatch errors

## Limitations

- Checkpoint format is specific to PyTorch and cannot be directly loaded by other deep-learning frameworks without conversion (e.g., TensorFlow, ONNX)
- No changelog mechanism in the GNN-RT repository; checkpoint provenance (which training run, which hyperparameters, which dataset version) must be manually tracked outside the checkpoint file
- Checkpoint only preserves model weights and optimizer state; preprocessing parameters, molecular graph featurization settings, and data normalization statistics are not included and must be versioned separately
- Large model checkpoints may consume significant disk space; no automatic compression or pruning is mentioned in the repository documentation

## Evidence

- [other] Save the trained model checkpoint in PyTorch format for downstream transfer learning or inference: "Save the trained model checkpoint in PyTorch format for downstream transfer learning or inference."
- [other] Train the GNN model on the molecular graph dataset, iterating over training batches until convergence. Validate model performance on held-out validation set at each epoch.: "Train the GNN model on the molecular graph dataset, iterating over training batches until convergence. Validate model performance on held-out validation set at each epoch."
- [readme] run [Preprocess.py], [Train.py] and [Transferlearning.py]: "run [Preprocess.py], [Train.py] and [Transferlearning.py]"
- [readme] The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations.: "The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations."
