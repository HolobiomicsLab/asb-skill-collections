---
name: molecular-graph-construction-from-smiles
description: Use when you have raw SMILES strings from a chemical database (e.g.,
  CCSBase, METLIN, or custom sources) and need to feed them into a graph neural network
  model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0159
  tools:
  - manual expert review
  - RDKit
  - PyTorch
  - scripts/train-test.py
  techniques:
  - ion-mobility-MS
  license_tier: restricted
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

# molecular-graph-construction-from-smiles

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert SMILES strings into graph tensor representations suitable for graph neural network input by canonicalizing structures and extracting atom and bond features. This is essential for preparing molecular datasets for GNN-based property prediction tasks like collision cross section estimation.

## When to use

You have raw SMILES strings from a chemical database (e.g., CCSBase, METLIN, or custom sources) and need to feed them into a graph neural network model. Apply this skill when you are building training or test sets for molecular property prediction and require consistent, structured graph representations with atom-level and bond-level features.

## When NOT to use

- Input is already a feature table or pre-computed graph representation — skip canonicalization and feature extraction.
- SMILES strings are malformed or uninterpretable by RDKit — the canonicalization step will fail; validate SMILES syntax first.
- Molecules contain unusual stereochemistry or exotic functional groups not well-supported by RDKit — manual curation may be required.

## Inputs

- raw SMILES strings (from CSV/parquet/Excel)
- CCS dataset with smiles column (e.g., METLIN-CCS, CCSBase)
- Optional: 3D coordinates for enhanced molecular representation

## Outputs

- canonical SMILES strings
- atom feature tensors (atomic number, formal charge, hybridization, aromaticity)
- bond feature tensors (bond type, aromaticity, stereochemistry)
- adjacency matrices (atom and bond)
- PyTorch (.pt) or pickle (.pkl) serialized graph objects
- graph metadata file

## How to apply

Load raw SMILES strings from your dataset and canonicalize them using RDKit to ensure structural consistency across the dataset. Convert each canonical SMILES to a molecular graph representation by extracting atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry). Construct feature tensors encoding atom and bond adjacency matrices, then serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format for downstream GNN input. The canonicalization step is critical to avoid duplicate or conflicting representations of the same molecule.

## Related tools

- **RDKit** (SMILES canonicalization, molecular graph construction, atom and bond feature extraction) — https://github.com/rdkit/rdkit
- **PyTorch** (tensor serialization and storage of graph objects in .pt format) — https://github.com/pytorch/pytorch
- **scripts/train-test.py** (downstream GNN training script that consumes preprocessed graph tensors from parquet files with smiles-column-name parameter) — https://github.com/enveda/ccs-prediction

## Examples

```
# After loading data with SMILES column, canonicalize and extract features using RDKit:
from rdkit import Chem
mols = [Chem.MolToSmiles(Chem.MolFromSmiles(smi)) for smi in df['smiles']]
atom_feats = [[atom.GetAtomicNum(), atom.GetFormalCharge(), atom.GetHybridization()] for mol in [Chem.MolFromSmiles(s) for s in mols] for atom in mol.GetAtoms()]
# Then serialize to PyTorch format and pass to train-test.py with --smiles-column-name 'smiles'
```

## Evaluation signals

- All SMILES strings canonicalize without error and map to valid RDKit molecule objects.
- Atom feature tensors contain expected dimensions matching the number of atoms; bond feature tensors match the number of bonds.
- Adjacency matrices are symmetric and sparse, with diagonal zeros (no self-loops) and binary or weighted bond types.
- Serialized .pt or .pkl files load without corruption and reconstruct identical graph objects on reload.
- Downstream GNN training script accepts the serialized graphs without shape mismatches or missing feature errors.

## Limitations

- RDKit may fail to canonicalize malformed or exotic SMILES strings; preprocessing must include SMILES validation and filtering.
- Large molecular datasets (>>100k molecules) may require memory-efficient streaming or batched serialization to avoid RAM exhaustion.
- 3D coordinate information (if present) is not automatically extracted during graph construction; separate handling required for coordinate-aware models.
- Bond stereochemistry and aromaticity perception depends on RDKit's aromatization model; output may differ if custom aromatization rules are needed.

## Evidence

- [other] Load raw SMILES strings from the CCS dataset: "Load raw SMILES strings from the CCS dataset repository (enveda/ccs-prediction)."
- [other] Canonicalize SMILES using RDKit: "Canonicalize SMILES using RDKit to ensure structural consistency."
- [other] Extract atom and bond features: "Extract atom-level features (atomic number, formal charge, hybridization, aromaticity) and bond-level features (bond type, aromaticity, stereochemistry)."
- [other] Construct and serialize graph tensors: "Construct feature tensors encoding atom and bond adjacency matrices. Serialize all graph objects and metadata to a standard PyTorch (.pt) or pickle (.pkl) format."
- [readme] Train with SMILES input via train-test.py: "--train-input-file is the training set (see notebooks/data_processing/2_data_splits.ipynb for details on the format)/ --smiles-column-name column name of the smiles"
