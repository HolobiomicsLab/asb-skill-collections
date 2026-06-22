---
name: pytorch-distributed-training-execution
description: Use when when you have a pre-trained GNN model checkpoint and need to apply transfer learning to a new chromatography or molecular property prediction dataset (e.g., Eawag_XBridgeC18_364.xlsx) by fine-tuning the model weights on domain-specific examples without retraining from scratch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3336
  tools:
  - Python
  - PyTorch
  - PyG
  - RDKit
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
evidence_spans:
- '**Python**'
- '**Pytorch**'
- '- **Pytorch**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_abcort_cq
    doi: 10.1021/acs.jcim.4c02179
    title: ABCoRT
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
---

# PyTorch Distributed Training Execution

## Summary

Execute transfer learning workflows on graph neural network models using PyTorch and PyG with command-line parameter passing to enable fine-tuning on domain-specific molecular datasets. This skill bridges pre-trained model checkpoints and transfer learning datasets through scripted execution with structured dataset arguments.

## When to use

When you have a pre-trained GNN model checkpoint and need to apply transfer learning to a new chromatography or molecular property prediction dataset (e.g., Eawag_XBridgeC18_364.xlsx) by fine-tuning the model weights on domain-specific examples without retraining from scratch.

## When NOT to use

- Input dataset is already a learned feature embedding or pre-computed molecular fingerprint table (use direct model inference instead)
- No pre-trained model checkpoint is available (train from scratch using train_SMRT.py rather than transfer learning)
- Dataset is in a format other than .xlsx and conversion is not feasible

## Inputs

- Pre-trained model checkpoint (PyTorch .pt or .pth file)
- Transfer learning dataset in Excel format (.xlsx)
- train_transfer_FE.py script
- Command-line arguments (--DataSet flag with dataset filename)

## Outputs

- Fine-tuned model checkpoint
- Training logs with metrics (loss, validation scores)
- Model weights optimized for transfer learning dataset

## How to apply

Load the pre-trained model checkpoint using PyTorch's model serialization and the transfer learning dataset (in .xlsx format) via Pandas. Execute the designated transfer learning script (train_transfer_FE.py) with the target dataset name passed as a command-line argument via the --DataSet flag. Use PyTorch optimizers and PyG's graph operations to perform forward/backward passes on molecular graph representations. Monitor training metrics (loss, validation performance) via TorchMetrics during fine-tuning epochs. Upon convergence or completion, save the fine-tuned model checkpoint and training logs for downstream evaluation.

## Related tools

- **PyTorch** (Deep learning framework for model training, checkpoint loading, and gradient-based optimization)
- **PyG (PyTorch Geometric)** (Graph neural network operations for molecular graph representation and message passing)
- **Pandas** (Loading and parsing transfer learning datasets from Excel (.xlsx) files)
- **TorchMetrics** (Monitoring and logging training metrics during fine-tuning)
- **torch-scatter, torch-sparse, torch-cluster** (Graph operations and sparse tensor handling for PyG computations)
- **RDKit** (Molecular structure parsing and feature extraction for input preprocessing)

## Examples

```
python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx
```

## Evaluation signals

- Training loss decreases monotonically or shows expected convergence pattern across epochs, indicating model is learning dataset-specific features
- Validation metrics (e.g., RMSE, correlation) on held-out examples improve relative to the pre-trained baseline
- Fine-tuned model checkpoint is successfully saved and can be loaded without serialization errors
- Training logs from TorchMetrics contain expected fields (epoch, loss, validation score) with numeric values in plausible ranges
- Model inference on the transfer learning dataset produces predictions (e.g., retention time, solubility) compatible with input molecular properties

## Limitations

- Transfer learning script assumes pre-trained model architecture matches the target dataset's molecular graph structure; mismatch will cause shape errors
- Dataset must be in .xlsx format; other formats (CSV, parquet) require conversion step not automated by this workflow
- No built-in hyperparameter tuning (learning rate, batch size, epochs) — these must be set manually in the train_transfer_FE.py script
- Training is executed sequentially on a single device; distributed multi-GPU execution is not documented in provided README

## Evidence

- [intro] Transfer learning is executed by running train_transfer_FE.py with --DataSet flag: "python train_transfer_FE.py --DataSet  Eawag_XBridgeC18_364.xlsx"
- [other] Pre-trained model and dataset are loaded, then script is executed with PyTorch and PyG for graph operations: "Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. Execute train_transfer_FE.py with the --DataSet parameter set to"
- [other] Training metrics are monitored via TorchMetrics and results are saved: "Monitor training metrics via TorchMetrics during fine-tuning. Save the fine-tuned model checkpoint and training logs."
- [intro] Transfer learning is performed on thirteen datasets: "run the transfer learning on thirteen transfer learning data sets"
- [readme] Required dependencies include PyTorch, PyG, and graph-specific tensor libraries: "Pytorch, PyG, torch-scatter, torch-sparse, torch-cluster, torch_geometric"
