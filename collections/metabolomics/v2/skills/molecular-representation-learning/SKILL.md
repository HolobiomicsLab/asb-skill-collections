---
name: molecular-representation-learning
description: Use when when you have a collection of molecules with known property labels (e.g., retention times on a chromatographic column) and need to predict those properties on new compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3336
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0081
  tools:
  - Python
  - PyG
  - RDKit
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyTorch
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
- doi: 10.1021/acs.analchem.0c04071
  title: ''
evidence_spans:
- '**Python**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
- '**Pandas**'
- '**torch-scatter**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_abcort_cq
    doi: 10.1021/acs.jcim.4c02179
    title: ABCoRT
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-representation-learning

## Summary

Train and fine-tune graph neural network models to learn molecular representations (embeddings) for predicting compound properties such as retention time. This skill uses PyTorch and PyG to encode molecular structures as graphs and transfer knowledge across chromatography datasets.

## When to use

When you have a collection of molecules with known property labels (e.g., retention times on a chromatographic column) and need to predict those properties on new compounds. Apply this skill if you want to leverage pre-trained molecular representations or fine-tune them on domain-specific datasets like Eawag_XBridgeC18_364.xlsx to improve prediction accuracy.

## When NOT to use

- Input molecules lack chemical structure information (no SMILES or 3D coordinates available).
- Target property is not amenable to molecular graph representation (e.g., discrete categorical labels without ordinal meaning).
- Dataset is very small (< 50 samples) — transfer learning may overfit without sufficient regularization.

## Inputs

- SMILES strings (molecular identifiers)
- Property labels (e.g., retention times in minutes)
- Excel file (e.g., Eawag_XBridgeC18_364.xlsx) with molecule–property pairs
- Pre-trained model checkpoint (for transfer learning)

## Outputs

- Fine-tuned graph neural network model checkpoint
- Molecular embedding vectors (learned representations)
- Training logs and performance metrics (TorchMetrics output)
- Property predictions on held-out test molecules

## How to apply

Begin by preparing molecular SMILES strings and property labels in Excel format (e.g., Eawag_XBridgeC18_364.xlsx). Convert SMILES to molecular graphs using RDKit, then train a graph neural network via train_SMRT.py using PyTorch and PyG for model training. Monitor training metrics with TorchMetrics. For domain adaptation, execute transfer learning via train_transfer_FE.py by passing the target dataset name with the --DataSet flag. The script loads the pre-trained model checkpoint, fine-tunes on the new dataset, and saves the updated model and training logs. Use torch-scatter, torch-sparse, and torch-cluster for efficient graph operations during both training and inference.

## Related tools

- **PyTorch** (Deep learning framework for training and evaluating graph neural networks)
- **PyG (PyTorch Geometric)** (Graph neural network library for molecular graph construction and message passing)
- **RDKit** (Molecular toolkit for converting SMILES to molecular graphs and property calculation)
- **TorchMetrics** (Monitoring and logging training metrics during model optimization)
- **Pandas** (Loading and preprocessing tabular datasets from Excel files)
- **torch-scatter, torch-sparse, torch-cluster** (Efficient graph operations for aggregation and neighbor sampling in GNN layers)

## Examples

```
python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx
```

## Evaluation signals

- Training loss decreases monotonically or shows expected convergence pattern reported by TorchMetrics.
- Model checkpoint file is created and can be loaded without errors in subsequent transfer learning runs.
- Predicted retention times on test molecules fall within the observed range of training data (sanity check for regression bounds).
- Transfer learning on target dataset (e.g., Eawag_XBridgeC18_364.xlsx) reduces prediction error compared to zero-shot pre-trained model.
- Molecular embeddings cluster similarly structured compounds (visual inspection via dimensionality reduction or similarity metrics).

## Limitations

- Transfer learning performance depends on similarity between pre-training and target datasets; large domain shifts may require more extensive fine-tuning.
- SMILES representation can be ambiguous for some molecules; stereochemistry or tautomers may not be fully captured.
- No changelog is available in the repository, making it difficult to track updates or breaking changes.
- Requires explicit passing of dataset name via --DataSet flag; batch processing multiple datasets requires separate script invocations.

## Evidence

- [other] Transfer learning on the Eawag_XBridgeC18_364 dataset is executed by running the train_transfer_FE.py script with the dataset name passed as a command-line argument via the --DataSet flag.: "Transfer learning on the Eawag_XBridgeC18_364 dataset is executed by running the train_transfer_FE.py script with the dataset name passed as a command-line argument via the --DataSet flag."
- [other] Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. Execute train_transfer_FE.py with the --DataSet parameter set to Eawag_XBridgeC18_364.xlsx using PyTorch and PyG for graph neural network operations.: "Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. Execute train_transfer_FE.py with the --DataSet parameter set to"
- [other] Monitor training metrics via TorchMetrics during fine-tuning. Save the fine-tuned model checkpoint and training logs.: "Monitor training metrics via TorchMetrics during fine-tuning. Save the fine-tuned model checkpoint and training logs."
- [readme] If you want to train the Model. Please command python train_SMRT.py: "If you want to train the Model. Please command python train_SMRT.py"
- [readme] If you want to run the transfer learning on thirteen transfer learning data sets, use: python train_transfer_FE.py --DataSet  Eawag_XBridgeC18_364.xlsx: "If you want to run the transfer learning on thirteen transfer learning data sets, use: python train_transfer_FE.py --DataSet  Eawag_XBridgeC18_364.xlsx"
