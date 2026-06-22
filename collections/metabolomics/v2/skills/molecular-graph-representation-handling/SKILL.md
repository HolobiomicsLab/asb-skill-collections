---
name: molecular-graph-representation-handling
description: Use when when you have molecular structure data (SMILES or molecular IDs) from chemistry databases (e.g., PubChem, HMDB) and need to feed it into a neural network architecture like TransG-Net that expects multimodal inputs combining graph-structured molecular topology with learned embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3373
  tools:
  - RDKit 2020.03.4
  - torch
  - numpy
  - RDKit
  - scikit-learn
  - CUDA
  - cuDNN
  - PyTorch (torch >= 1.4.0)
  - data_prep.py
  - TransGNet.py
derived_from:
- doi: 10.1007/s10489-022-04351-0
  title: Mass Spectrum Transformer
evidence_spans:
- RDKit == 2020.03.4
- torch >= 1.4.0
- numpy == 1.19.1
- scikit-learn == 0.23.2
- cuda >= 9.0
- cudnn >= 7.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass_spectrum_transformer_cq
    doi: 10.1007/s10489-022-04351-0
    title: Mass Spectrum Transformer
  dedup_kept_from: coll_mass_spectrum_transformer_cq
schema_version: 0.2.0
---

# molecular-graph-representation-handling

## Summary

Extract, construct, and validate molecular graph representations (vertices, edges, atomic features) as inputs to neural network models that process multimodal molecular data. This skill bridges molecular chemistry (RDKit) and deep learning (PyTorch) by converting chemical structure files into tensor-compatible graph formats.

## When to use

When you have molecular structure data (SMILES or molecular IDs) from chemistry databases (e.g., PubChem, HMDB) and need to feed it into a neural network architecture like TransG-Net that expects multimodal inputs combining graph-structured molecular topology with learned embeddings.

## When NOT to use

- Input is already a pre-computed feature matrix or embedding table — skip to direct model ingestion.
- Molecular data is in a format incompatible with RDKit (e.g., abstract structural descriptors without explicit atoms/bonds).
- You need only SMILES string representation without explicit graph topology — use SMILES embedding pipeline alone.

## Inputs

- molecule ID list or SMILES strings (from data.csv or equivalent)
- RDKit molecule objects
- raw molecular structure data from PubChem or HMDB

## Outputs

- graph feature tensors (node and edge attributes)
- molecular graph adjacency/connectivity matrices
- PyTorch tensors compatible with TransG-Net input specification
- model-ready batched multimodal input (graphs + embeddings)

## How to apply

Load molecule structures from the data source (data.csv with PubChem/HMDB IDs or SMILES strings) using RDKit 2020.03.4. Convert each molecule into a graph representation extracting atom nodes and bond edges with their chemical properties (atomic number, degree, formal charge, hybridization). Generate consistent graph feature tensors matching the multimodal input specification (graph features + SMILES embeddings) documented in data_prep.py. Verify that all graph tensors have consistent shape and dtype before batching. Pass sample graph tensors through the TransG-Net model forward pass to confirm input compatibility and output tensor dimensions.

## Related tools

- **RDKit** (Parse SMILES/molecular files and extract graph structure (atoms, bonds, properties) into networkx-compatible or tensor form)
- **PyTorch (torch >= 1.4.0)** (Convert graph features to dense/sparse tensors and batch multimodal inputs for neural network ingestion)
- **data_prep.py** (Implements the full multimodal dataset production workflow including graph representation generation) — github.com/chensaian/TransG-Net
- **TransGNet.py** (Defines the neural network model that accepts the constructed multimodal graph+SMILES inputs) — github.com/chensaian/TransG-Net

## Examples

```
import torch; from rdkit import Chem; mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O'); graph_features = torch.tensor([[atom.GetAtomicNum() for atom in mol.GetAtoms()]], dtype=torch.float32); model_input = (graph_features, smiles_embedding)
```

## Evaluation signals

- Graph feature tensors have consistent shape across all molecules in the batch (e.g., [batch_size, num_atoms, feature_dim]).
- Forward pass through TransG-Net completes without shape mismatch or dtype errors on sample graph inputs.
- Node features (atomic number, degree, formal charge, hybridization) are within expected chemical ranges (e.g., atomic number 1–118, valence 0–8).
- Adjacency/connectivity matrices are symmetric (undirected bonds) and sparse (not fully connected).
- Model architecture summary and parameter count match the paper specification after instantiation with graph inputs.

## Limitations

- Requires RDKit 2020.03.4 specifically (version compatibility critical for molecular parsing).
- Graph representation is deterministic from SMILES/molecule ID but sensitive to preprocessing choices (stereochemistry handling, explicit vs. implicit hydrogens, charge states).
- Large molecular databases (PubChem, HMDB) require efficient batch generation; memory usage scales with molecule size and batch count.
- No changelog provided in repository; version compatibility with newer RDKit/PyTorch may not be guaranteed.

## Evidence

- [readme] the process of multimodal dataset production is in data_prep.py: "the process of multimodal dataset production is in data_prep.py"
- [other] TransG-Net is implemented in TransGNet.py and processes multimodal datasets produced by data_prep.py: "TransG-Net is implemented in TransGNet.py and processes multimodal datasets produced by data_prep.py"
- [other] graph features and SMILES embeddings multimodal input specification: "multimodal input specification (graph features and SMILES embeddings)"
- [readme] the data is from pubchem and HMDB: "the data is from pubchem and HMDB"
- [readme] torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time): "torch >= 1.4.0 (please upgrade your torch version in order to reduce the training time)"
