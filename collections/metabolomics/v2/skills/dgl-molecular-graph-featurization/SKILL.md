---
name: dgl-molecular-graph-featurization
description: Use when you have a set of SMILES or molecular structures and need to represent them as graph tensors for a Graphormer or other graph neural network model that predicts molecular properties (e.g., retention time, spectroscopic features).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0082
  tools:
  - Graphormer
  - DGL
  - RDKit
  - PyTorch
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github
- import dgl
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# DGL Molecular Graph Featurization

## Summary

Encode small molecules as heterogeneous directed graphs with node and edge attributes (atom types, bond orders, chirality) using DGL, suitable for input to Graph Transformer backbones in retention-time prediction and other molecular property tasks.

## When to use

You have a set of SMILES or molecular structures and need to represent them as graph tensors for a Graphormer or other graph neural network model that predicts molecular properties (e.g., retention time, spectroscopic features). Use this skill when your downstream task requires differentiable molecular graph representations compatible with PyTorch and DGL data loaders.

## When NOT to use

- Input molecules are already pre-computed as fixed-size feature vectors (e.g., Morgan fingerprints or Mordred descriptors); use graph featurization only if graph structure and atom/bond types are informative for your model.
- Your downstream model is not a graph neural network or Graphormer (e.g., you are using a traditional random forest on molecular descriptors).
- Molecules contain atoms or bond types outside your pre-defined vocabulary and you have no fallback strategy for handling unknown features.

## Inputs

- List of SMILES strings or RDKit molecule objects
- Atom type vocabulary (e.g., atomic numbers or element symbols)
- Bond type vocabulary (e.g., SINGLE, DOUBLE, AROMATIC, TRIPLE)

## Outputs

- DGL graph objects with node features (atom attributes) and edge features (bond attributes)
- Batched DGL graph tensors compatible with PyTorch DataLoader
- Node embeddings (intermediate representation) for downstream Graphormer layers

## How to apply

Convert each molecule (SMILES or MOL object) to an RDKit molecule object, then extract atom types, bond orders, and chirality as discrete node and edge features. Use DGL's heterogeneous graph constructor (or homogeneous graph with feature tensors) to encode atoms as nodes and bonds as edges. Normalize or one-hot encode categorical features (atom types, bond types) as float32 tensors. Validate that node/edge feature tensors propagate through a sample Graphormer forward pass with correct shapes before training. Store graphs in batched DGL graph format (via collate_fn in PyTorch DataLoader) to enable efficient mini-batch training.

## Related tools

- **DGL** (Heterogeneous graph construction and batching; provides DGL graph data structures and collate_fn utilities for PyTorch DataLoader integration) — https://github.com/dmlc/dgl
- **RDKit** (Molecule parsing (SMILES to MOL), atom/bond type extraction, chirality detection, and feature enumeration) — https://github.com/rdkit/rdkit
- **PyTorch** (Tensor operations, DataLoader, and gradient-based training of featurized graphs) — https://github.com/pytorch/pytorch
- **Graphormer** (Graph Transformer backbone that consumes DGL graph embeddings and node/edge features to predict molecular properties) — https://github.com/microsoft/Graphormer

## Examples

```
import dgl; from rdkit import Chem; mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(O)=O'); g = dgl.from_networkx(nx.DiGraph([(i, j) for i in range(mol.GetNumAtoms()) for j in range(mol.GetNumAtoms()) if mol.GetBondBetweenAtoms(i,j)])); # Extract atom/bond features and featurize with one-hot encodings for Graphormer input
```

## Evaluation signals

- Node feature tensors have shape (num_atoms, feature_dim) and contain only valid atom type indices or one-hot encodings (no NaN or out-of-vocabulary values).
- Edge feature tensors have shape (num_edges, feature_dim) and encode valid bond types (SINGLE, DOUBLE, AROMATIC, TRIPLE) with no missing or invalid entries.
- DGL graph object passes heterogeneous graph validation: graph.num_nodes('atom') > 0, graph.num_edges('bond') >= 0, and node/edge data keys are consistent across all graphs in a batch.
- Forward pass through Graphormer backbone produces output tensor with expected shape (batch_size, output_dim) without shape mismatch or runtime errors.
- Gradient flow during backpropagation is unbroken (no NaN gradients), indicating all node/edge features are differentiable float32 tensors.

## Limitations

- Graph featurization is lossy with respect to 3D conformational information; chirality is encoded as a discrete feature but not 3D coordinates. For tasks requiring stereochemical discrimination, consider augmenting with conformer-based features.
- Molecules with unusual or rare atom types (e.g., exotic lanthanides) or bond types not in your pre-defined vocabulary will encounter out-of-vocabulary errors; fallback strategies (e.g., masking, remapping to generic atom type) must be manually implemented.
- DGL heterogeneous graphs require consistent node and edge type definitions across all graphs; inconsistent graph structures (e.g., some graphs with aromatic bonds, others without) may cause collation errors in batched training.

## Evidence

- [methods] Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality).: "Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality)."
- [readme] Supports interface and datasets of PyG, DGL, OGB, and OCP.: "Supports interface and datasets of PyG, DGL, OGB, and OCP."
- [results] from rdkit import Chem: "from rdkit import Chem"
- [methods] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to final dense output layer for continuous retention-time prediction.: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
