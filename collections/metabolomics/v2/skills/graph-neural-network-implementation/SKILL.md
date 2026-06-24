---
name: graph-neural-network-implementation
description: Use when when your input includes molecular structures (SMILES, conformers)
  and you need to predict a continuous property (e.g., CCS, binding affinity, solubility)
  that depends on molecular connectivity and spatial relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3318
  tools:
  - Python 3
  - RDKit
  - PyTorch
  - PyG
  - pandas
  - NumPy
  - conda
  - pip
  - PyTorch Geometric (PyG)
  - NumPy and pandas
  - DGL
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
- doi: 10.1021/acs.analchem.3c03177
  title: ''
evidence_spans:
- '[python3](https://www.python.org/)'
- '[RDKit](https://rdkit.org/)'
- '[PyTorch](https://pytorch.org/)'
- '[PyG](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '[pandas](https://pandas.pydata.org/)'
- '[NumPy](https://numpy.org/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paccs_cq
    doi: 10.1002/cem.70040
    title: PACCS
  - build: coll_retention_time_gnn_cq
    doi: 10.1021/acs.analchem.3c03177
    title: retention_time_gnn
  dedup_kept_from: coll_paccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/cem.70040
  all_source_dois:
  - 10.1002/cem.70040
  - 10.1021/acs.analchem.3c03177
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-neural-network-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Implement a graph neural network (GNN) using PyTorch Geometric to encode molecular structure and predict molecular properties (collision cross section) from graph-based representations of conformers. This skill is essential when molecular topology and connectivity must inform property prediction beyond simple numerical features.

## When to use

When your input includes molecular structures (SMILES, conformers) and you need to predict a continuous property (e.g., CCS, binding affinity, solubility) that depends on molecular connectivity and spatial relationships. GNN is particularly appropriate when voxel-based or numerical features alone are insufficient; use it when graph-based message passing can capture bonding patterns and atomic environments that improve prediction accuracy over non-graph baselines.

## When NOT to use

- Input is a simple tabular dataset without molecular structures or connectivity information; conventional ML (e.g., random forest, linear regression) is more efficient.
- Molecules are very small (e.g., single atoms, ions) or have trivial graph structure where graph convolution adds minimal signal.
- Computational budget is severely constrained; GNNs are more expensive than traditional feature engineering and may not justify the overhead for small datasets (<1000 molecules).

## Inputs

- 3D molecular conformers (RDKit Mol objects or equivalent)
- Molecular graph representations (nodes=atoms, edges=bonds)
- Node and edge features (atomic number, bond type, hybridization)
- Supplementary numeric features (voxel projected area, m/z, adduct type)
- Ground-truth labels (CCS values or other continuous properties)

## Outputs

- Trained PyTorch Geometric GNN model (serialized state_dict)
- Per-molecule predicted property values (float arrays)
- Per-molecule learned graph embeddings (dense vectors)
- Model performance metrics (MAE, RMSE, R² on test set)

## How to apply

Construct a molecular graph representation from each 3D conformer, where atoms are nodes and bonds are edges, optionally with node features such as atomic number, hybridization, and formal charge. Initialize a PyTorch Geometric GNN model with message-passing layers (e.g., GraphConv or similar) to aggregate neighbor information iteratively. Concatenate learned graph embeddings with non-graph features (voxel projected area, m/z, one-hot encoded adduct type) before passing through dense layers for final property regression. Train using a supervised loss function (e.g., MSE) with PyTorch optimizers and learning rate scheduling. Validate that learned representations correlate with known molecular property variations, and confirm that the GNN component improves test-set performance compared to non-graph baselines.

## Related tools

- **PyTorch Geometric (PyG)** (Defines graph-based message-passing layers (GraphConv, etc.) and provides batched graph data structures for mini-batch training of GNN models on molecular graphs.) — https://pytorch-geometric.readthedocs.io/en/latest/
- **PyTorch** (Core deep-learning framework used to build, train, and optimize the GNN model with gradient descent and learning rate scheduling.) — https://pytorch.org/
- **RDKit** (Constructs molecular graphs from SMILES or conformer objects and computes node/edge features (atomic properties, bond types) for the GNN input.) — https://rdkit.org/
- **NumPy and pandas** (Prepare and organize training/validation/test splits, handle tabular metadata (m/z, adduct types, ground-truth labels), and compute evaluation metrics.)

## Examples

```
from PACCS.MolecularRepresentations import construct_graph; from torch_geometric.data import DataLoader; model = GNNModel(); optimizer = torch.optim.Adam(model.parameters(), lr=0.001); for epoch in range(epochs):
    for batch in DataLoader(graph_dataset, batch_size=32):
        out = model(batch); loss = criterion(out, batch.y); loss.backward(); optimizer.step()
```

## Evaluation signals

- Test-set prediction error (MAE, RMSE) is lower when the GNN is trained end-to-end compared to a baseline model using only voxel projected area and m/z features.
- Learned node embeddings cluster by chemical environment (e.g., aromatic vs. aliphatic atoms) when visualized with dimensionality reduction (t-SNE, UMAP).
- Per-molecule predictions are consistent across multiple random seeds and hyperparameter settings, indicating stable learning.
- Ablation study: removing graph features or freezing the GNN encoder degrades test performance, confirming that graph structure contributes predictive signal.
- Prediction residuals (predicted − observed CCS) show no systematic bias across charge states, m/z ranges, or molecular size bins.

## Limitations

- GNN performance depends on correct molecular graph construction; errors in bond topology or missing hydrogens will propagate to embeddings.
- The method assumes 3D conformers are available and correctly optimized; poor conformer geometry can degrade predictions even with a well-trained GNN.
- Message-passing depth (number of convolutional layers) must be tuned; too few layers limit receptive field, too many lead to over-smoothing and information loss.
- Training is more computationally expensive than traditional feature-based methods, especially on large datasets or with deep/wide architectures.
- No explicit handling of multiple conformers per molecule in the published code; only one conformer is used per SMILES.

## Evidence

- [other] optionally incorporating graph-based message passing from PyG for molecular representations: "optionally incorporating graph-based message passing from PyG for molecular representations"
- [readme] PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph. The related method is shown in VoxelProjectedArea.py, MZ.py, and MolecularRepresentations.py.: "PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph"
- [readme] The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model: "feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model"
- [other] PyTorch and PyG (PyTorch Geometric) as core deep-learning frameworks: "PyTorch and PyG (PyTorch Geometric) as core deep-learning frameworks"
- [other] Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling.: "Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling"
