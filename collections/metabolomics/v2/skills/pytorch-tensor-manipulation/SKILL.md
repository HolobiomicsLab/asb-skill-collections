---
name: pytorch-tensor-manipulation
description: Use when when you have parsed molecular graph representations (atom nodes, bond edges, feature vectors) from SMILES or molecular structure files and need to prepare them for forward passes through a pre-trained GNN encoder in PyTorch.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - DGL
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.3c03177
  title: retention_time_gnn
evidence_spans:
- Pytorch implementation of the model described in the paper
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_retention_time_gnn_cq
    doi: 10.1021/acs.analchem.3c03177
    title: retention_time_gnn
  dedup_kept_from: coll_retention_time_gnn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03177
  all_source_dois:
  - 10.1021/acs.analchem.3c03177
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pytorch-tensor-manipulation

## Summary

Conversion and structuring of molecular graph data (nodes, edges, atom features) into PyTorch tensor format for input to graph neural network models. This skill enables efficient batch processing and GPU acceleration of molecular representations for retention time prediction tasks.

## When to use

When you have parsed molecular graph representations (atom nodes, bond edges, feature vectors) from SMILES or molecular structure files and need to prepare them for forward passes through a pre-trained GNN encoder in PyTorch. Use this skill before feeding molecular data into the GNN layers for embedding generation or retention time inference.

## When NOT to use

- Input is already a pre-computed molecular embedding or feature vector from another model.
- Molecular structure information is unavailable or cannot be parsed into graph format.
- Working with pre-extracted fixed-length feature tables rather than graph-structured data.

## Inputs

- Parsed molecular graph data with node features (atom properties)
- Edge lists (bond connectivity information)
- Atom feature vectors (numeric representations from RDKit or similar)
- Raw molecular structures (SMILES or structure files)

## Outputs

- PyTorch tensor representation of molecular graphs
- Batched graph tensors compatible with GNN input layers
- Device-mapped tensors (GPU or CPU)

## How to apply

Extract molecular graph components (node features representing atoms, edge indices representing bonds, and associated atom feature vectors) from the molecular representation. Convert these components into PyTorch tensors using torch.tensor() or torch.from_numpy() with appropriate dtype (typically float32 for features, long for indices). Organize tensors into a batch structure compatible with DGL (Deep Graph Library) graph objects or PyTorch Geometric formats, depending on the GNN architecture. Validate tensor shapes match the model's input specifications (e.g., node feature dimension, edge list format). Transfer tensors to the appropriate device (CPU or GPU) using .to(device) before passing to the GNN encoder. This structured tensor format enables the GNN to efficiently compute molecular embeddings through learned convolution operations.

## Related tools

- **PyTorch** (Core tensor computation framework for creating and manipulating multi-dimensional arrays representing molecular graphs)
- **DGL** (Graph neural network library providing optimized graph tensor structures and batch operations for GNN input)
- **RDKit** (Cheminformatics library for parsing molecular structures and extracting node/edge features from SMILES or structure files)

## Evaluation signals

- Tensor shapes match GNN model input specifications (node feature dimension, batch size, edge list format).
- Tensors are on the correct device (GPU or CPU) as verified by tensor.device property.
- Edge indices are within valid range [0, num_nodes) and edge tensor dtype is torch.long.
- Node feature tensors have dtype float32 and no NaN or Inf values after conversion.
- Forward pass through GNN encoder completes without dimension mismatch or shape errors.

## Limitations

- Tensor conversion assumes input molecular graphs are valid and complete; malformed structures or missing features will propagate errors downstream.
- Memory constraints on GPU may limit batch size for large molecular graphs or datasets.
- Different GNN architectures (graph convolution vs. message passing) may require different tensor organization schemes; verification against specific model architecture is required.
- RDKit feature extraction and tensor mapping must preserve chemical semantic information; incorrect atom feature encoding will degrade downstream prediction quality.

## Evidence

- [other] Prepare input molecular graph data (nodes, edges, atom features) into PyTorch tensor format.: "Prepare input molecular graph data (nodes, edges, atom features) into PyTorch tensor format."
- [other] Forward pass through the GNN encoder layers to generate molecular embeddings.: "Forward pass through the GNN encoder layers to generate molecular embeddings."
- [readme] Dependencies: Python, Pytorch, DGL, RDKit: "Dependencies
- **Python**
- **Pytorch**
- **DGL**
- **RDKit**"
- [readme] Pytorch implementation of the model described in the paper: "Pytorch implementation of the model described in the paper [Retention Time Prediction by Learning from Small Training Dataset with Pre-Trained Graph Neural Network"
