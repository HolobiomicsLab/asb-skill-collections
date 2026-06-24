---
name: molecular-embedding-generation
description: Use when when you have molecular structures (SMILES or explicit graph
  representations) and need fixed-size vector representations to feed into a prediction
  head or transfer learning task.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3336
  tools:
  - PyTorch
  - DGL
  - RDKit
  - retention_time_gnn
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c03177
  title: retention_time_gnn
evidence_spans: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-embedding-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate dense vector embeddings of molecular structures by forward-passing molecular graphs through pre-trained graph neural network encoder layers. This skill enables compact, learnable representations of molecules for downstream retention time prediction and other property forecasting tasks on small datasets.

## When to use

When you have molecular structures (SMILES or explicit graph representations) and need fixed-size vector representations to feed into a prediction head or transfer learning task. Specifically apply this skill when working with small training datasets where pre-trained molecular features can improve generalization, such as in chromatographic retention time prediction across different analytical platforms.

## When NOT to use

- Input is already a hand-crafted molecular fingerprint or descriptor table (e.g., Morgan fingerprints, Mordred descriptors) — embedding generation is redundant.
- Molecules are too large or contain rare atom types not present in pre-training data; the model may produce uninformative embeddings.
- Target task is entirely orthogonal to the pre-training objective (e.g., if pre-training was on retention time but target is 3D protein–ligand docking pose prediction), transfer learning may not help.

## Inputs

- Molecular structures (SMILES strings or RDKit molecule objects)
- Pre-trained GNN model checkpoint (PyTorch .pt file)
- Molecular graph tensors (node features, adjacency lists, edge attributes in PyTorch tensor format)

## Outputs

- Molecular embedding vectors (dense 1D PyTorch tensors, typically 64–256 dimensions)
- Per-molecule fixed-size representations suitable for downstream prediction layers

## How to apply

Load the pre-trained GNN model weights from the retention_time_gnn repository using PyTorch. Convert input molecular structures into graph tensor format (nodes representing atoms with chemical features, edges representing bonds). Pass the graph through the GNN encoder layers to compute node embeddings, then aggregate across the molecular graph (typically via global pooling) to produce a single fixed-size molecular embedding vector. The embedding dimensionality and aggregation strategy are determined by the pre-trained architecture. These embeddings can then be directly passed to a prediction head (e.g., fully connected layers) for fine-tuning on target datasets. The pre-training on the METLIN-SMRT dataset provides initialization that captures generalizable molecular structure–property relationships before adaptation to new retention time targets.

## Related tools

- **PyTorch** (Core framework for loading pre-trained GNN model weights, defining the computational graph for forward passes, and managing GPU/CPU tensor operations during embedding generation.)
- **DGL** (Graph deep learning library used to construct and manipulate molecular graph data structures (nodes, edges, features) for input to the GNN encoder.)
- **RDKit** (Chemistry toolkit for converting SMILES strings and molecular structures into graph representations (atoms as nodes, bonds as edges) with chemical feature annotations.)
- **retention_time_gnn** (Reference implementation containing pre-trained GNN model, encoder architecture definitions, and dataset utilities for molecular embedding generation and transfer learning.) — https://github.com/seokhokang/retention_time_gnn

## Examples

```
python run_transfer.py -t FEM_long
```

## Evaluation signals

- Embedding vector shape matches expected dimensionality (e.g., batch_size × 64 or batch_size × 128); shape mismatch indicates incorrect forward pass or pooling.
- Embedding values are finite (no NaN or inf); presence of NaNs suggests numerical instability, missing node features, or disconnected graph components.
- Downstream prediction head (MLPs, classifiers) achieves reasonable loss on validation set when initialized with embeddings; poor downstream performance may indicate embeddings are not discriminative for the target task.
- Embeddings from similar molecules (high Tanimoto similarity in fingerprint space) exhibit low cosine distance in embedding space; this validates that the GNN has learned meaningful molecular structure–property relationships.
- Transfer learning fine-tuning converges faster and to lower error than training from random initialization on the target retention time dataset; this confirms pre-trained embeddings capture transferable molecular features.

## Limitations

- Pre-trained model is initialized on the METLIN-SMRT dataset; molecules or chemical classes far outside this training distribution may receive poorly calibrated embeddings.
- Model performance depends on the quality of the input graph representation (RDKit's ability to correctly parse SMILES and assign atom/bond types). Invalid or ambiguous SMILES will produce incorrect or incomplete graphs.
- Embedding generation is a form of dimensionality reduction; information loss is inherent and may be problematic if fine-grained structural details (e.g., stereochemistry, unusual valence states) are critical for downstream tasks.
- The skill assumes pre-trained weights are available; if training from scratch on a new domain, initialization benefits are lost and larger labeled datasets are required.

## Evidence

- [other] forward pass through the GNN encoder layers to generate molecular embeddings: "Forward pass through the GNN encoder layers to generate molecular embeddings."
- [other] pre-trained GNN components: "The implementation is a PyTorch-based graph neural network model designed to predict retention time by learning from small training datasets through pre-trained GNN components."
- [other] prepare input molecular graph data into PyTorch tensor format: "Prepare input molecular graph data (nodes, edges, atom features) into PyTorch tensor format."
- [readme] GNN architecture: "gnn/*.py - GNN architecture"
- [readme] learning from small training datasets with pre-trained model: "Retention Time Prediction by Learning from Small Training Dataset with Pre-Trained Graph Neural Network"
