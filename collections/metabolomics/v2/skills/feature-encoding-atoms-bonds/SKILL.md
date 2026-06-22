---
name: feature-encoding-atoms-bonds
description: Use when you have parsed SMILES or SDF molecular structures from a chemical dataset (e.g., SMRT dataset) and need to convert them into graph representations for input to a graph neural network or RT-Transformer model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - torch
  - Python
  - rdkit-pypi
  - torch_geometric
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
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
---

# feature-encoding-atoms-bonds

## Summary

Encode atom and bond features from molecular structures into node and edge attributes suitable for graph neural network input. This skill converts chemical structures into machine-readable graph representations where atoms become labeled nodes and bonds become labeled edges, enabling dual-input molecular featurization for retention time prediction.

## When to use

You have parsed SMILES or SDF molecular structures from a chemical dataset (e.g., SMRT dataset) and need to convert them into graph representations for input to a graph neural network or RT-Transformer model. Use this skill when fingerprints alone are insufficient and you require explicit atom-level and bond-level chemical features as node and edge attributes.

## When NOT to use

- Input molecules are already featurized as fixed-size fingerprints or descriptor vectors and do not require graph structure.
- The retention time prediction model uses only fingerprint-based dual inputs without graph neural network components.
- Molecules contain rare or unhandled atom types or bond configurations that RDKit cannot parse or represent.

## Inputs

- Molecular structures in SMILES or SDF format
- Parsed RDKit molecule objects (rdkit.Chem.Mol)
- Chemical metadata (optional: molecular ID, chromatographic conditions)

## Outputs

- PyTorch Geometric graph objects (torch_geometric.data.Data) with node features, edge indices, and edge features
- Serialized graph representations (pickle or PyTorch tensor format)
- Node feature tensor (num_atoms × num_atom_features)
- Edge index tensor (2 × num_bonds) and edge feature tensor (num_bonds × num_bond_features)

## How to apply

Parse molecular structures using RDKit to extract atom types, formal charges, hybridization states, aromaticity, and bond types. Use RDKit's Chem.Descriptors module to compute atom-level descriptors and enumerate bonds, storing atom features as node attributes and bond features as edge attributes. Convert these feature dictionaries into PyTorch Geometric graph objects (torch_geometric.data.Data) with a node feature tensor and an edge index tensor paired with edge features. Validate that all atoms are assigned at least atomic number, hybridization, and aromaticity; all bonds are assigned bond type and aromaticity. Serialize the resulting graph objects to disk (pickle or PyTorch format) for downstream model training, ensuring compatibility with DataLoader batching in PyTorch Geometric.

## Related tools

- **rdkit-pypi** (Parse molecular structures, compute atom descriptors, and enumerate bond connectivity and features) — https://github.com/rdkit/rdkit
- **torch_geometric** (Convert atom and bond features into PyTorch Geometric graph objects (Data) and enable batch processing for model training) — https://github.com/pyg-team/pytorch_geometric
- **torch** (Serialize and manage feature tensors and graph objects for GPU-accelerated model training) — https://github.com/pytorch/pytorch

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; import torch_geometric; mol = Chem.MolFromSmiles('CCO'); AllChem.Compute2DCoords(mol); data = torch_geometric.data.Data(x=atom_features, edge_index=edge_indices, edge_attr=edge_features); torch.save(data, 'molecule_graph.pt')
```

## Evaluation signals

- Node feature tensor has shape (num_atoms, num_atom_features) with no NaN or infinite values; atomic number ≥ 1 and ≤ 118.
- Edge index tensor has shape (2, num_bonds) with valid node indices in range [0, num_atoms); each edge is unique and undirected edges appear exactly once.
- Edge feature tensor has shape (num_bonds, num_edge_features); bond types are valid (single, double, triple, aromatic) and numeric; no rows are identical unless chemically identical bonds exist.
- PyTorch Geometric Data object successfully batches into a mini-batch without shape mismatches; graph connectivity is consistent with molecular valency rules.
- Serialized graph objects can be loaded and reconstructed identically; model forward pass accepts batched graphs without tensor dimension errors.

## Limitations

- RDKit may fail to parse non-standard or highly reactive molecules; bond aromaticity perception requires valid Kekule structures.
- Rare atom types (e.g., lanthanides, synthetic elements) may not be assigned standard descriptors; user must define custom atom features.
- Edge features depend on bond perception; molecules with unspecified or ambiguous stereochemistry may produce inconsistent features across runs.
- Graph size (num_atoms, num_bonds) varies widely; very large molecules or very small fragments may require padding or filtering strategies not covered by this skill.

## Evidence

- [other] Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes.: "Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [other] Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule.: "Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule."
- [other] Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format).: "Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format)."
