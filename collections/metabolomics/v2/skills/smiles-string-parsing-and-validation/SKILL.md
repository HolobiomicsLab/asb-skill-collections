---
name: smiles-string-parsing-and-validation
description: Use when when you have SMILES strings as input to a molecular machine learning pipeline (e.g., retention time prediction, spectral prediction) and need to convert them into structured molecular representations before calculating descriptors or constructing molecular graphs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - mordred
  - NumPy
  - pandas
  - RDKit
  - mspcompiler
  - R
  - MS-DIAL
  - Python
  - TensorFlow Serving
  - Docker & docker-compose
  - NP Classifier (mwang87/NP-Classifier)
  - MongoDB
  - Pickaxe
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
- doi: 10.1021/acs.analchem.2c05389
  title: ''
- doi: 10.1021/acs.jnatprod.1c00399
  title: ''
- doi: 10.1186/s12859-023-05149-8
  title: ''
evidence_spans:
- import mordred from mordred import Calculator, descriptors
- import numpy as np
- import pandas as pd
- library(mspcompiler)
- Read the msp file into R.
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  - build: coll_mspcompiler_cq
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  - build: coll_npclassifier_cq
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
---

# SMILES String Parsing and Validation

## Summary

Convert SMILES (Simplified Molecular Input Line Entry System) strings into RDKit molecule objects for downstream descriptor calculation and molecular property prediction. This foundational step validates chemical notation syntax and prepares molecules for featurization in graph transformer and descriptor-based workflows.

## When to use

When you have SMILES strings as input to a molecular machine learning pipeline (e.g., retention time prediction, spectral prediction) and need to convert them into structured molecular representations before calculating descriptors or constructing molecular graphs. Required before any RDKit or mordred descriptor calculation.

## When NOT to use

- Input is already a feature matrix or descriptor table — skip directly to model training.
- Molecules are already in 3D structure format (SDF, MOL, XYZ files) — use RDKit's AllChem.MolFromMolFile() or equivalent 3D loaders instead.
- SMILES strings contain non-standard notation or require specialized parsing (e.g., polymers, Markush structures) — standard RDKit parsing may fail.

## Inputs

- SMILES strings (one per molecule, typically from a pandas DataFrame or text file)
- Input data table with SMILES column (e.g., CSV, pickle, or structured database)

## Outputs

- RDKit molecule objects (rdkit.Chem.Mol instances, one per valid SMILES)
- List or array of valid molecules ready for descriptor or graph featurization
- Optional: validation report listing invalid SMILES indices and failure reasons

## How to apply

Parse each SMILES string using RDKit's Chem.MolFromSmiles() function, which returns a molecule object or None if parsing fails. Validate that the returned object is not None; discard or flag invalid SMILES. The resulting RDKit molecule objects serve as the canonical input for both RDKit descriptor calculation and mordred Calculator initialization. No additional normalization or sanitization steps are mentioned in the article beyond standard RDKit parsing; however, ensure input SMILES are in standard format (e.g., canonical SMILES from chemical databases). The parsed molecules are then passed directly to the descriptor calculation routines (RDKit's descriptor module and mordred's Calculator) or to graph construction pipelines (e.g., Graphormer's graph featurization).

## Related tools

- **RDKit** (Parses SMILES strings into molecule objects via Chem.MolFromSmiles(); serves as foundation for all downstream descriptor and graph featurization steps.) — https://github.com/rdkit/rdkit
- **pandas** (Loads and organizes input SMILES data (e.g., from CSV); manages molecule object lists for batch processing.) — https://github.com/pandas-dev/pandas

## Examples

```
from rdkit import Chem; mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]; valid_mols = [m for m in mols if m is not None]
```

## Evaluation signals

- All returned RDKit molecule objects are non-None and have valid atomic and bond properties (validate via mol.GetNumAtoms() > 0).
- Parsing succeeds on ≥95% of input SMILES (or expected success rate from domain prior).
- Molecules can be serialized back to canonical SMILES (Chem.MolToSmiles()) and re-parsed without loss of structure.
- Descriptors can be successfully calculated from parsed molecules using RDKit and mordred without errors.
- Graph representation (used in Graphormer) can be constructed from parsed molecules without failures.

## Limitations

- RDKit's standard SMILES parser does not support all non-standard notations (e.g., polymers, isotope-specific heavy atoms may require additional sanitization).
- Invalid or malformed SMILES strings silently return None; downstream steps must include explicit None checks to avoid errors.
- SMILES parsing does not validate 3D stereochemistry or chirality beyond connectivity; 2D stereochemistry is preserved but 3D coordinates are not inferred.
- Large-scale parsing can be memory-intensive for molecules with many heavy atoms; batch processing and garbage collection may be needed for datasets > 100k molecules.

## Evidence

- [full_text] Parse input SMILES strings and convert to RDKit molecule objects.: "Parse input SMILES strings and convert to RDKit molecule objects"
- [full_text] Calculate RDKit descriptors using RDKit's descriptor module.: "Calculate RDKit descriptors using RDKit's descriptor module"
- [results] from rdkit import Chem: "from rdkit import Chem"
- [full_text] The resulting descriptor matrix in compressed NumPy format (.npz) follows molecule object parsing and RDKit descriptor calculation.: "Save the resulting descriptor matrix in compressed NumPy format (.npz)"
