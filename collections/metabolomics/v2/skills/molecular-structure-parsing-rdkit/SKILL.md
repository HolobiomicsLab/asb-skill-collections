---
name: molecular-structure-parsing-rdkit
description: Use when you have raw molecular structures in SMILES or SDF format from a chemical database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3407
  tools:
  - rdkit-pypi
  - torch
  - Python
  - torch_geometric
  - RT-Transformer
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- rdkit-pypi
- '- rdkit-pypi'
- torch
- Python 3.9
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular structure parsing with RDKit

## Summary

Parse molecular structure files (SMILES or SDF format) using RDKit to extract chemical features and generate standardized molecular representations (fingerprints and graph encodings). This is essential preprocessing for machine learning models that require dual molecular inputs for retention time prediction and metabolite annotation.

## When to use

You have raw molecular structures in SMILES or SDF format from a chemical database (e.g., METLIN, PubChem) or experimental dataset and need to convert them into learnable representations (Morgan fingerprints and graph-encoded atom/bond features) for input to neural network models that predict molecular properties like retention time.

## When NOT to use

- Input is already a pre-computed feature matrix or embedding—no need to re-parse.
- Molecular structures are incomplete, contain invalid valences, or fail RDKit sanitization; preprocessing or curation is required first.
- Model architecture expects only one representation type (fingerprint OR graph), not both; clarify input requirements before parsing.

## Inputs

- SMILES strings or SDF molecular structure files
- Molecular structure dataset (e.g., SMRT dataset from METLIN with InChI/SMILES identifiers and metadata)

## Outputs

- Morgan fingerprint vectors (bit-encoded molecular descriptors)
- Molecular graph representations (node features, edge lists, edge attributes in PyTorch Geometric format)
- Serialized dual-input tensor pairs (pickle or .pt files) ready for model training

## How to apply

Load molecular structures from SMILES or SDF files using RDKit's mol parsers. Generate Morgan fingerprints for each molecule to capture molecular topology as fixed-length bit vectors. Simultaneously convert each molecule to a graph representation using RDKit's atom/bond extraction (Chem.Descriptors) and encode atom types, formal charges, and bond orders as PyTorch Geometric node and edge features. Serialize both representations (fingerprints and graphs) to disk in pickle or PyTorch tensor format for compatibility with downstream model training pipelines. Validate that fingerprint bit-lengths and graph feature dimensions match the model's expected input specifications.

## Related tools

- **rdkit-pypi** (Core library for parsing molecular structures (SMILES/SDF), generating Morgan fingerprints, and extracting atom/bond topological features for graph encoding.)
- **torch_geometric** (Framework for encoding RDKit molecular topologies as graph representations (nodes, edges, features) compatible with graph neural networks.)
- **torch** (Tensor serialization and GPU-compatible storage of fingerprints and graph tensors for efficient model training.)
- **RT-Transformer** (Downstream model that consumes the parsed fingerprint and graph representations as dual inputs for retention time prediction.) — github.com/01dadada/RT-Transformer

## Evaluation signals

- All molecular structures parse successfully without RDKit sanitization errors; invalid molecules are logged and excluded.
- Morgan fingerprints have consistent bit-length (e.g., 2048 bits) and non-zero information content across the dataset (not all zeros or all ones).
- Graph representations preserve atom and bond counts from the original structure; node feature dimensions and edge attribute dimensions match model input specs.
- Serialized fingerprint and graph files are non-empty, loadable, and match row counts in the input molecular dataset (no data loss during encoding).
- Downstream model training accepts the dual-input tensor pairs without shape mismatch errors; loss curves show learning progress.

## Limitations

- RDKit sanitization may fail or require manual curation for molecules with unusual bonding, radicals, or non-standard valences; quality-control preprocessing is recommended.
- Morgan fingerprint fixed-length encoding may lose information for very large molecules; alternative or complementary descriptors may be needed.
- Graph representations incur higher memory overhead and compute cost than fingerprints alone; trade-offs between expressiveness and scalability depend on dataset size and model architecture.
- The skill assumes SMILES/SDF input format; other formats (InChI, PDB, MOL2) require separate parsers or pre-conversion steps.

## Evidence

- [other] Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule.: "Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule."
- [other] Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes.: "Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes."
- [other] Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format).: "Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format)."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [readme] The SMRT dataset is collect from this paper (doi: 10.1038/s41467-019-13680-7): "The SMRT dataset is collect from [this paper](https://doi.org/10.1038/s41467-019-13680-7)"
