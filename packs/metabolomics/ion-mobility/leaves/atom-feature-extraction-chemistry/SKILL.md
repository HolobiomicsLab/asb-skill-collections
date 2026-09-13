---
name: atom-feature-extraction-chemistry
description: Use when you have canonicalized SMILES strings from a chemical database
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3372
  tools:
  - manual expert review
  - RDKit
  - train-test.py
  - PyTorch
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# atom-feature-extraction-chemistry

## Summary

Extract atomic-level chemical features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry) from canonicalized SMILES strings to construct molecular graph representations for GNN input. This skill bridges chemical structure notation and learnable tensor representations required by graph neural networks.

## When to use

You have canonicalized SMILES strings from a chemical database (e.g., METLIN-CCS, CCSBase, or the CCS dataset) and need to convert them into graph tensor representations suitable for training or inference with a graph neural network for molecular property prediction tasks such as collision cross section (CCS) estimation.

## When NOT to use

- Input is already a pre-computed feature matrix or embedding; re-extracting from SMILES is redundant and may introduce inconsistency.
- SMILES strings are non-canonical or malformed; canonicalization must precede feature extraction.
- You need 3D spatial coordinates (e.g., for distance-based features); this skill extracts connectivity and atom/bond properties only—use a separate 3D coordinate generation step if the model requires geometric input.

## Inputs

- canonical SMILES strings (format: text, from databases such as METLIN-CCS, CCSBase, or CCS dataset)
- molecular structure database records (parquet or CSV with smiles column)
- RDKit-compatible SMILES notation

## Outputs

- atom feature tensors (shape: [num_atoms, num_atom_features])
- bond feature tensors (shape: [num_bonds, num_bond_features])
- adjacency matrices or edge index tensors (graph connectivity)
- serialized graph objects (PyTorch .pt or pickle .pkl format)
- graph metadata (e.g., molecule ID, adduct type, CCS label if available)

## How to apply

Load each canonical SMILES string using RDKit and construct a molecular graph object. Extract atom-level features—atomic number, formal charge, hybridization state, and aromaticity flag—for each atom in the molecule. Simultaneously extract bond-level features—bond type (single, double, triple, aromatic), aromaticity, and stereochemistry—for each bonded pair. Encode these features as numerical tensors (e.g., one-hot or continuous vectors) alongside adjacency matrices representing the graph topology. Serialize the resulting graph objects (atom features, bond features, adjacency matrices, and metadata) to PyTorch (.pt) or pickle (.pkl) format for downstream GNN input. The rationale is that GNNs require explicit feature vectors and connectivity patterns; raw SMILES strings lack the structured graph representation needed for message-passing algorithms.

## Related tools

- **RDKit** (Parse SMILES strings, construct molecular graph objects, and extract atom/bond features (atomic number, hybridization, aromaticity, bond types, stereochemistry)) — https://www.rdkit.org/
- **train-test.py** (Training script that accepts preprocessed graph tensors and metadata (coordinates, adduct, CCS labels) via parquet input files; demonstrates downstream consumption of extracted features) — enveda/ccs-prediction
- **PyTorch** (Serialize and load graph objects (.pt format) for batching and GPU-accelerated training in GNN models)

## Evaluation signals

- All SMILES strings parse successfully with RDKit without errors or warnings; check that num_atoms and num_bonds > 0 for every molecule.
- Feature tensors have consistent shape within a batch (atom features: [num_atoms, feature_dim]; bond features: [num_bonds, feature_dim]) and contain expected value ranges (e.g., atomic number 1–118, hybridization 0–3, aromaticity {0,1}).
- Adjacency/edge index tensors correctly represent the molecular graph: every bond appears exactly once (or twice if undirected), and no self-loops exist unless explicitly added.
- Serialized graph objects load without corruption and feature values remain unchanged after deserialization (verify via checksum or element-wise comparison).
- Feature extraction preserves chemical semantics: canonical SMILES with identical atom/bond configurations should produce identical feature vectors; isomers with different stereochemistry should have different features.

## Limitations

- RDKit may fail to parse non-standard or malformed SMILES notation; input validation and canonicalization are prerequisite steps.
- Feature extraction captures local atom and bond properties but does not encode global molecular fingerprints, 3D geometry, or conformational state; multi-modal models may require supplementary features (e.g., 3D coordinates as mentioned in the README).
- Feature dimensionality depends on RDKit's feature set and encoding scheme; different atom/bond feature definitions may require custom feature extraction code and could affect GNN generalization across datasets.
- The skill produces graph-level tensors without context on dataset-specific preprocessing (e.g., normalization, imbalance handling, or adduct-specific feature augmentation) mentioned in the training script; downstream model performance depends on appropriate data splits and preprocessing.

## Evidence

- [other] Extract atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry).: "Extract atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry)."
- [other] Construct feature tensors encoding atom and bond adjacency matrices.: "Construct feature tensors encoding atom and bond adjacency matrices."
- [other] Convert each canonical SMILES to a molecular graph representation with atom and bond features.: "Convert each canonical SMILES to a molecular graph representation with atom and bond features."
- [other] Serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format.: "Serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format."
- [other] The repository contains code for preprocessing raw SMILES strings from the CCS dataset into atom and bond feature tensors (graph objects) that serve as input to the graph neural network.: "The repository contains code for preprocessing raw SMILES strings from the CCS dataset into atom and bond feature tensors (graph objects) that serve as input to the graph neural network."
