---
name: rdkit-molecular-featurization
description: Use when you have molecular structure data (SMILES strings or MOL files) from an in-house chemical database and need to prepare it as input for a graph neural network that predicts liquid chromatography retention times for small molecule identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3520
  tools:
  - RDKit
  - Python
  - PyTorch
  - Preprocess.py
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- conda install -c rdkit rdkit
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

# rdkit-molecular-featurization

## Summary

Convert molecular structures from SMILES or MOL format into node-edge graph representations with atom and bond features suitable for GNN training. This preprocessing step is essential for preparing raw chemical structure data into a format consumable by PyTorch DataLoaders in the GNN-RT retention time prediction pipeline.

## When to use

You have molecular structure data (SMILES strings or MOL files) from an in-house chemical database and need to prepare it as input for a graph neural network that predicts liquid chromatography retention times for small molecule identification. Apply this skill as the mandatory first stage before training or transfer learning.

## When NOT to use

- Input is already a pre-computed molecular graph tensor or feature table — skip to model training
- You are working with spectral data (MS/MS, LC-MS) rather than chemical structures — use spectrum preprocessing instead
- Your molecular graphs are intended for non-GNN models (e.g., fingerprint-based classifiers) — use alternative featurization (e.g., Morgan fingerprints, ECFP)

## Inputs

- SMILES strings (text format)
- MOL format molecular structure files
- In-house chemical database records containing molecular identifiers

## Outputs

- Serialized molecular graphs (pickle or HDF5 format)
- Node feature matrices (atom number, degree, formal charge, hybridization per atom)
- Edge feature matrices (bond type, aromaticity per bond)
- PyTorch-compatible graph tensors ready for DataLoader consumption

## How to apply

Load molecular structure data (SMILES or MOL format) from your in-house database using RDKit's molecule parsing functions. Construct molecular graphs by converting each structure into a node-edge representation where nodes carry atom features (atomic number, degree, formal charge, hybridization) and edges carry bond features (bond type, aromaticity). Use RDKit's built-in graph construction methods to extract these features systematically. Finally, serialize the resulting molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) so they can be consumed downstream by the GNN training pipeline. The rationale is that GNNs require explicit node and edge attribute tensors; raw SMILES strings cannot be directly fed to graph neural networks.

## Related tools

- **RDKit** (Parse SMILES/MOL structures and construct molecular graphs with atom/bond features) — https://www.rdkit.org/
- **PyTorch** (Serialize and load featurized graphs via DataLoader for batched GNN training) — https://pytorch.org/
- **Preprocess.py** (Main orchestration script that executes molecular graph construction from in-house spectra files) — https://github.com/Qiong-Yang/GNN-RT

## Examples

```
python Preprocess.py
```

## Evaluation signals

- All SMILES/MOL inputs successfully parse without RDKit exceptions or warnings
- Each molecular graph contains expected node counts matching atom counts and edge counts matching bond counts
- Atom feature vectors have shape (num_atoms, 4) containing valid atomic numbers, degrees, formal charges, and hybridization states within expected ranges
- Bond feature vectors have shape (num_bonds, 2) with bond types and aromaticity flags correctly encoded
- Serialized output files load without corruption in PyTorch DataLoader (verify via iteration without errors)

## Limitations

- RDKit may fail to parse invalid or malformed SMILES strings; input data quality is critical
- The featurization is fixed to the atom/bond feature set (atomic number, degree, formal charge, hybridization, bond type, aromaticity); additional chemical properties (e.g., 3D coordinates, pharmacophoric features) are not included in this workflow
- No built-in validation that the featurized graphs are representative of the chemical diversity in the training set; chemically similar structures may lead to poor GNN generalization

## Evidence

- [other] Load molecular structure data and construct graphs with atom/bond features: "Load molecular structure data (SMILES or MOL format) from the in-house database using RDKit. 2. Construct molecular graphs by converting each structure into a node-edge representation with atom"
- [other] Serialize graphs for PyTorch consumption: "Serialize the molecular graphs into a format compatible with PyTorch's DataLoader (e.g., pickle or HDF5) for consumption by the GNN training pipeline"
- [readme] Preprocess.py is the entry point: "put your spectra files in to data directory and run [Preprocess.py]"
- [readme] GNN-RT takes molecular graph as input: "It takes molecular graph as the input, and the predicted retention time as the output"
- [other] RDKit graph construction methods: "using RDKit's graph construction methods"
