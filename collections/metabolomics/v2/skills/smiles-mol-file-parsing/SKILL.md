---
name: smiles-mol-file-parsing
description: Use when when you have molecular structures encoded as SMILES strings or MOL files from an in-house database or spectroscopy repository, and need to convert them into node-edge graph representations with explicit atom features (atomic number, degree, formal charge, hybridization) and bond features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - Python
  - RDKit
  - PyTorch
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
---

# SMILES and MOL file parsing for molecular graph construction

## Summary

Parse molecular structure data from SMILES strings or MOL files using RDKit to extract atom and bond features, enabling conversion into node-edge graph representations suitable for GNN input. This skill is essential for preparing chemical structure data from spectroscopy databases into machine-learning-ready formats.

## When to use

When you have molecular structures encoded as SMILES strings or MOL files from an in-house database or spectroscopy repository, and need to convert them into node-edge graph representations with explicit atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type, aromaticity) for training graph neural networks like GNN-RT.

## When NOT to use

- Input is already in node-edge graph format or precomputed feature tensors — skip directly to GNN training.
- Molecular structures are incomplete, contain unspecified stereochemistry critical to your analysis, or lack proper atom valence validation.
- Input files are malformed SMILES (e.g., unbalanced parentheses) or corrupted MOL files that RDKit cannot parse without manual curation.

## Inputs

- SMILES strings from in-house molecular database
- MOL format files from spectroscopy data repositories
- Spectra files containing encoded molecular structures

## Outputs

- Molecular graphs with node-edge representation
- Atom feature arrays (atomic number, degree, formal charge, hybridization)
- Bond feature arrays (bond type, aromaticity)
- Serialized graph objects (pickle or HDF5 format) compatible with PyTorch DataLoader

## How to apply

Load molecular structure files (SMILES or MOL format) from the database using RDKit's molecular parsing functions. For each structure, construct a molecular graph by converting it into a node-edge representation with atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type, aromaticity) using RDKit's graph construction methods. Validate that all features are correctly extracted and non-null. Serialize the resulting graph objects into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) for downstream consumption by the GNN training pipeline. The rationale is that RDKit's native graph representation captures the full chemical topology needed for end-to-end GNN learning to predict molecular properties like LC retention time.

## Related tools

- **RDKit** (Parse SMILES and MOL files; construct molecular graphs with atom/bond feature extraction and graph serialization) — https://www.rdkit.org/
- **PyTorch** (Serialize and load molecular graphs via DataLoader for GNN training pipeline compatibility)
- **Python** (Scripting environment (Anaconda 3.6+) for orchestrating RDKit and PyTorch operations)

## Examples

```
python Preprocess.py
```

## Evaluation signals

- All SMILES/MOL inputs parse without errors; RDKit returns valid molecule objects for ≥95% of input records.
- Atom feature arrays contain no NaN or None values; atomic numbers, degrees, formal charges, and hybridization states are in chemically valid ranges.
- Bond feature arrays correctly reflect bond types (single, double, triple, aromatic) and aromaticity labels matching chemical structure.
- Serialized graph objects can be successfully deserialized by PyTorch DataLoader without shape/type mismatches during GNN training.
- Graph feature counts match downstream GNN input layer expectations (e.g., node feature dimension matches concatenated atom features; edge features match bond feature dimension).

## Limitations

- RDKit parsing may fail on non-standard or malformed SMILES strings; validation and error handling are required.
- MOL file format variation (MOL vs. MOL2 vs. SDF) may require format-specific parsers; the skill assumes standard V2000/V3000 MOL format.
- Stereochemistry, isotopes, and formal charges must be explicitly encoded in SMILES or MOL files; implicit hydrogens and 2D coordinates in MOL files may cause feature extraction discrepancies.
- No explicit changelog or version pinning guidance provided in the repository, so RDKit API stability across versions is not guaranteed.

## Evidence

- [other] Load molecular structure data (SMILES or MOL format) from the in-house database using RDKit. Construct molecular graphs by converting each structure into a node-edge representation with atom features (atomic number, degree, formal charge, hybridization) and bond features (bond type, aromaticity) using RDKit's graph construction methods.: "Load molecular structure data (SMILES or MOL format) from the in-house database using RDKit. Construct molecular graphs by converting each structure into a node-edge representation with atom features"
- [other] Serialize the molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) for consumption by the GNN training pipeline.: "Serialize the molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) for consumption by the GNN training pipeline."
- [readme] put your spectra files in to data directory and run [Preprocess.py]: "put your spectra files in to data directory and run [Preprocess.py]"
- [readme] It takes molecular graph as the input, and the predicted retention time as the output.: "It takes molecular graph as the input, and the predicted retention time as the output."
