---
name: graph-tensor-serialization
description: Use when after constructing feature tensors encoding atom adjacency matrices, bond types, and chemical properties from canonical SMILES—and before feeding graphs into a GNN training loop—to enable reproducible, portable, and memory-efficient storage of graph objects that will be loaded in batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0176
  tools:
  - manual expert review
  - RDKit
  - PyTorch
  - Python pickle module
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00899-w
  all_source_dois:
  - 10.1186/s13321-024-00899-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-tensor-serialization

## Summary

Converts preprocessed molecular graph representations (atom and bond feature tensors) into standardized serialized formats (PyTorch .pt or pickle .pkl) for efficient storage, loading, and batching in deep learning pipelines. This skill ensures graph objects retain structural and chemical information while remaining compatible with GNN training frameworks.

## When to use

After constructing feature tensors encoding atom adjacency matrices, bond types, and chemical properties from canonical SMILES—and before feeding graphs into a GNN training loop—to enable reproducible, portable, and memory-efficient storage of graph objects that will be loaded in batches across multiple training epochs.

## When NOT to use

- Graph objects have not yet been constructed from canonical SMILES or already exist in a memory-mapped or database format (e.g., HDF5, LMDB) designed for streaming—use those formats instead.
- Atom and bond features are incomplete or have not been validated against the molecular structure—serialize only after feature extraction is fully validated.
- The downstream model is a traditional (non-GNN) architecture that expects flattened feature vectors rather than graph tensors.

## Inputs

- Graph objects with atom feature tensors (atomic number, formal charge, hybridization, aromaticity per node)
- Edge feature tensors (bond type, aromaticity, stereochemistry per edge)
- Adjacency matrices (sparse or dense tensor encoding connectivity)
- Metadata dictionary (SMILES string, CCS value, adduct, 3D coordinates if present)

## Outputs

- PyTorch serialized graph files (.pt format)
- Pickle serialized graph files (.pkl format)
- Index or manifest file mapping graph identifiers to serialized file paths

## How to apply

After constructing atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry) as tensors, serialize the complete graph object—including adjacency matrices, node features, edge features, and associated metadata (SMILES, CCS labels, adduct type)—using PyTorch's `torch.save()` for .pt format or Python's `pickle` module for .pkl format. Store the serialized files with a consistent naming or index scheme so they can be loaded in deterministic order during dataset construction. Verify serialization by deserializing a sample graph and confirming that tensor shapes, chemical features, and metadata match the original graph specification.

## Related tools

- **RDKit** (Canonicalizes SMILES and constructs the initial molecular graph representation before feature extraction and serialization) — https://www.rdkit.org/
- **PyTorch** (Provides `torch.save()` and `torch.load()` for serializing and deserializing graph tensors in .pt format; enables downstream batch loading in DataLoader) — https://pytorch.org/
- **Python pickle module** (Serializes graph objects and metadata dictionaries into .pkl files as an alternative to PyTorch format)

## Evaluation signals

- Deserialized graph tensors have identical shapes, data types, and values as the original graph before serialization (bitwise comparison or torch.allclose with appropriate tolerance).
- Metadata (SMILES, CCS value, adduct) is correctly preserved and retrievable after deserialization.
- File size and I/O performance metrics (load time per graph, throughput in graphs/sec) meet expectations for batch training (typically <100 ms per batch of 32–64 graphs on modern hardware).
- Serialized files can be loaded in a reproducible order by a PyTorch DataLoader or custom data pipeline without errors or data corruption.
- A sample of deserialized graphs, when re-fed through the GNN, produces predictions statistically identical to those obtained when the graphs were not serialized (ruling out precision loss or structural corruption).

## Limitations

- PyTorch .pt format is tied to specific PyTorch versions; compatibility issues may arise when reloading on a different PyTorch release. Pickle files are Python-version-dependent.
- Serialized files are not human-readable; debugging feature or metadata errors requires deserialization and inspection of tensor values.
- No built-in versioning or schema validation in .pt or .pkl formats; if the graph construction logic changes (e.g., new atom features added), old serialized files will not automatically reflect the new schema.
- Large-scale datasets with millions of graphs may incur significant disk space overhead; consider memory-mapped or columnar storage (e.g., HDF5, Parquet) for very large collections.

## Evidence

- [other] Construct feature tensors encoding atom and bond adjacency matrices. Serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format.: "Construct feature tensors encoding atom and bond adjacency matrices. 6. Serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format."
- [other] The repository contains code for preprocessing raw SMILES strings from the CCS dataset into atom and bond feature tensors (graph objects) that serve as input to the graph neural network.: "The repository contains code for preprocessing raw SMILES strings from the CCS dataset into atom and bond feature tensors (graph objects) that serve as input to the graph neural network."
- [other] Extract atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry).: "Extract atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry)."
