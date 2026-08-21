---
name: molecular-graph-construction-pytorch-geometric
description: Use when when you have parsed molecular structures (SMILES or SDF) and
  need to represent them as attributed graphs for neural network models that accept
  graph-based inputs. Specifically applicable when your architecture requires dual
  representations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3373
  tools:
  - torch_geometric
  - torch
  - Python
  - rdkit-pypi
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- torch_geometric
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Graph Construction with PyTorch Geometric

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Converts molecular structures (SMILES or SDF format) into graph representations with atom and bond features encoded as node and edge attributes using RDKit and PyTorch Geometric, enabling dual-input architectures for machine learning models like RT-Transformer that predict molecular properties such as retention time.

## When to use

When you have parsed molecular structures (SMILES or SDF) and need to represent them as attributed graphs for neural network models that accept graph-based inputs. Specifically applicable when your architecture requires dual representations (e.g., fingerprints + graph) or when graph neural networks are the downstream model choice, as in the RT-Transformer for retention time prediction.

## When NOT to use

- Input is already a processed feature table or pre-computed embedding; skip to model training.
- Your downstream model requires only molecular fingerprints without topological information; use fingerprint-only approach instead.
- Molecules contain exotic or non-standard residues not well-handled by RDKit's default atom/bond feature extraction.

## Inputs

- SMILES strings or SDF files containing molecular structures
- RDKit Chem.Mol objects representing parsed molecules
- SMRT dataset (or equivalent molecule metadata with structure field)

## Outputs

- PyTorch Geometric Data objects with node features, edge attributes, and connectivity
- Serialized graph representations (pickle or PyTorch tensor format)
- Feature tensors encoding atomic properties and bond information

## How to apply

Begin by parsing molecular structures using RDKit to obtain a Chem.Mol object for each molecule in your dataset (e.g., from SMILES strings or SDF files). Use RDKit's Chem.Descriptors and atom/bond introspection methods to extract atomic properties (atomic number, formal charge, hybridization) and bond features (bond type, aromaticity) for each atom and bond in the molecule. Encode these features as node attributes (for atoms) and edge attributes (for bonds) in a graph representation. Serialize the resulting graph objects (e.g., using PyTorch Geometric's Data objects with node_attr and edge_attr tensors) to disk in a format compatible with your training pipeline (pickle or PyTorch tensor format). The rationale is that explicit graph encoding preserves molecular topology and chemical properties simultaneously, complementing fingerprint representations in dual-input models to improve prediction accuracy for chromatographic retention time.

## Related tools

- **rdkit-pypi** (Parses molecular structures (SMILES/SDF) and extracts atomic/bond descriptors for graph node and edge features) — https://www.rdkit.org
- **torch_geometric** (Encodes atom and bond features as node and edge attributes; manages graph data structures and serialization) — https://pytorch-geometric.readthedocs.io
- **torch** (Provides tensor operations and data structures underlying PyTorch Geometric's graph representation) — https://pytorch.org

## Examples

```
# Pseudocode (no single-line invocation available in provided context)
# In practice, use: from rdkit import Chem; from torch_geometric.data import Data
# mol = Chem.MolFromSmiles(smiles_string)
# node_features = extract_atom_features(mol)  # atomic number, charge, hybridization
# edge_index, edge_attr = extract_bond_features(mol)  # bond type, aromaticity
# graph_data = Data(x=node_features, edge_index=edge_index, edge_attr=edge_attr)
# torch.save(graph_data, 'molecule_graph.pt')
```

## Evaluation signals

- Graph Data objects contain non-null node_attr and edge_index tensors with correct dimensions matching molecule atom and bond counts.
- Edge attributes (edge_attr) encode meaningful chemical features (bond type, aromaticity); node features encode atomic properties (formal charge, hybridization).
- Serialized graphs deserialize without error and preserve connectivity and feature integrity across read/write cycles.
- Graph representations integrate correctly with downstream RT-Transformer dual-input architecture; dual fingerprint + graph inputs produce expected model forward pass without shape mismatches.
- Molecular graphs reconstruct valid molecules when converted back via RDKit (sanity check on feature encoding fidelity).

## Limitations

- RDKit's default atom and bond feature extraction may not capture all chemical contexts; molecules with rare isotopes or exotic formal charges may have incomplete or default feature representations.
- Graph serialization to disk requires sufficient storage; large datasets with millions of molecules may demand optimized serialization formats (e.g., HDF5) beyond pickle.
- PyTorch Geometric's Data object design assumes fixed feature dimensionality; molecules with variable atom counts or bond types require padding or batching strategies to ensure uniform tensor shapes for batch processing.

## Evidence

- [other] Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes.: "Convert molecular structures to graph representations using RDKit's Chem.Descriptors and PyTorch Geometric to encode atom and bond features as node and edge attributes."
- [other] Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format).: "Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format)."
- [other] The RT-Transformer architecture combines fingerprint and molecular graph data as dual inputs for retention time prediction.: "The RT-Transformer architecture combines fingerprint and molecular graph data as dual inputs for retention time prediction."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
