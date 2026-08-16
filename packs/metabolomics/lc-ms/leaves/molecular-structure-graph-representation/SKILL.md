---
name: molecular-structure-graph-representation
description: Use when when you have a set of chemical structures (SMILES strings or SDF files) that need to be processed for training a graph neural network model on molecular property prediction tasks, specifically when the target property (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PyG
  - RDKit
  - NumPy
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyG (PyTorch Geometric)
  - PyTorch
  - NumPy, Pandas
  - torch-scatter, torch-sparse, torch-cluster
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
evidence_spans:
- '**Python**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
- '**NumPy**'
- '**Pandas**'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-graph-representation

## Summary

Convert chemical structures into graph neural network–compatible representations using RDKit and PyG for training retention-time prediction models. This skill bridges cheminformatics and deep learning by encoding molecular topology and atom features as graph tensors suitable for PyTorch GNN architectures.

## When to use

When you have a set of chemical structures (SMILES strings or SDF files) that need to be processed for training a graph neural network model on molecular property prediction tasks, specifically when the target property (e.g., retention time) depends on molecular topology and atomic composition rather than bulk molecular descriptors alone.

## When NOT to use

- Input molecules are already pre-computed as fixed-length descriptor vectors (e.g., Morgan fingerprints or MACCS keys); graph representation is redundant.
- Task requires only 2D molecular property prediction without topological information (use simpler descriptor-based regression).
- Structure data is missing or heavily fragmented, preventing reliable graph construction.

## Inputs

- SMILES strings or SDF molecular files
- Tabular dataset linking molecule identifiers to retention-time values (e.g., .xlsx or .csv)
- Molecular structure metadata (molecular weight, formal charges, stereochemistry)

## Outputs

- PyG Data objects with node and edge feature tensors
- Batched DataLoader instances ready for GNN training
- Encoded graph representations compatible with PyTorch model forward passes

## How to apply

Load chemical structures using RDKit's SMILES/molecule parsing utilities, extracting node features (atom type, formal charge, hybridization) and edge connectivity. Convert the resulting molecular graphs into PyG Data objects with node and edge tensors. Normalize or standardize node features using NumPy/Pandas, then batch the graph tensors into DataLoader objects for training. The graph representation preserves 3D stereochemistry and ring systems, which are critical for retention-time prediction on reversed-phase chromatography datasets like SMRT. Validate that generated graphs have non-zero connectivity and that node/edge feature dimensions match the model's expected input shapes before training.

## Related tools

- **RDKit** (Parses SMILES/SDF inputs and extracts molecular graphs, node features (atom properties), and connectivity matrices)
- **PyG (PyTorch Geometric)** (Constructs Data objects from molecular graphs and batches them into DataLoader for GNN training)
- **PyTorch** (Provides the underlying tensor operations and GPU acceleration for graph construction and model training)
- **NumPy, Pandas** (Normalizes node feature tensors and manages tabular metadata linking molecules to retention-time labels)
- **torch-scatter, torch-sparse, torch-cluster** (Accelerates graph-level operations (scatter reductions, sparse matrix ops, neighborhood aggregation) during GNN forward passes)

## Examples

```
python train_SMRT.py
```

## Evaluation signals

- Graph connectivity: verify that no molecule graph has isolated nodes (degree > 0 for all non-hydrogen atoms) and edge counts match chemical valence rules.
- Node feature shape consistency: confirm all graphs in a batch have been padded or dynamically sized such that node feature tensors match the model's input layer (e.g., 14 atomic features per node).
- DataLoader batching: validate that batched PyG Data objects contain non-empty edge_index tensors and matching node/edge attribute dimensions across batch.
- Retention-time label alignment: spot-check that molecular identifiers in graph batch correspond correctly to ground-truth retention-time values in the target tensor.
- Graph statistics: compute and log the distribution of node counts, edge counts, and node feature ranges across the dataset to detect anomalies (e.g., disconnected components, feature outliers).

## Limitations

- RDKit cannot parse malformed or ambiguous SMILES strings; preprocessing and validation of input structure data is required.
- Graph representation discards 3D conformational geometry unless explicit 3D coordinates are embedded; for compounds with critical stereochemistry, 3D molecular generation may be needed.
- Memory overhead: large molecular datasets (>100k structures) may exhaust GPU VRAM during batching if graph sizes are heterogeneous; dynamic batching or graph clustering strategies are recommended.
- The skill assumes a single dominant molecular conformer; it does not account for conformational ensembles or tautomeric states.
- Node and edge feature normalization parameters must be fit on the training set and applied consistently to validation and test splits; failure to do so can degrade downstream model performance.

## Evidence

- [intro] graph neural network architecture (PyTorch + PyG): "which will instantiate the graph neural network architecture (PyTorch + PyG) and train on the SMRT data"
- [readme] torch-scatter, torch-sparse, torch-cluster for graph acceleration: "- **torch-scatter**
- **torch-sparse**
- **torch-cluster**"
- [intro] SMRT retention-time dataset domain: "The ABCoRT model is trained on the SMRT retention-time dataset"
