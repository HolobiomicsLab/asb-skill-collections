---
name: deep-learning-model-architecture-design
description: Use when you have extracted molecular features (voxel projected areas, molecular graphs, m/z values, adduct encodings) and need to build a predictive model to map these features to a continuous molecular property (CCS).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0006
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3676
  tools:
  - Python 3
  - RDKit
  - PyTorch
  - PyG
  - pandas
  - NumPy
  - conda
  - pip
  - PyG (PyTorch Geometric)
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
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
  - build: coll_massnet_cq
    doi: 10.1093/bioinformatics/btac032/6510930
    title: massNet
  - build: coll_paccs_cq
    doi: 10.1002/cem.70040
    title: PACCS
  dedup_kept_from: coll_paccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/cem.70040
  all_source_dois:
  - 10.1002/cem.70040
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-architecture-design

## Summary

Design and construct a deep-learning neural network architecture for molecular property prediction (e.g., collision cross section) by selecting appropriate PyTorch layers, optionally incorporating graph-based message passing from PyG for molecular graph representations, and configuring the model for training on structured molecular features.

## When to use

You have extracted molecular features (voxel projected areas, molecular graphs, m/z values, adduct encodings) and need to build a predictive model to map these features to a continuous molecular property (CCS). Use this skill when your input includes tabular/vectorized features and optional graph-structured representations that require a learned mapping to experimental ground-truth labels.

## When NOT to use

- Input is already a pre-trained model checkpoint; use model loading/inference instead.
- Molecular conformers have not been generated or voxel projected areas have not been computed; complete feature engineering first.
- Ground-truth CCS labels are missing or sparse; use unsupervised or semi-supervised methods instead.

## Inputs

- voxel projected area features (NumPy arrays or PyTorch tensors)
- molecular graph representations (node features, edge indices from PyG Data objects)
- one-hot encoded adduct type vectors
- m/z values (scalar or vector)
- training dataset (molecules with ground-truth CCS labels)

## Outputs

- trained PyTorch model (saved state_dict or .pt file)
- model architecture definition (Python class inheriting torch.nn.Module)
- per-molecule CCS predictions on test set

## How to apply

Construct a PyTorch neural network by defining layers that accept the concatenated feature inputs: voxel projected area features, one-hot encoded adduct types, m/z values, and optionally a molecular graph representation. If graph data is available, integrate PyG message-passing layers to learn graph-aware molecular embeddings before concatenating with tabular features. Define the model's forward pass to produce a single continuous output (CCS prediction). Configure the model with an appropriate loss function (typically L1 or L2 regression loss) and optimizer (e.g., Adam). The architecture's suitability is validated by training on the preparation dataset, monitoring validation loss across epochs, and ensuring model outputs fall within the physically plausible CCS range observed in training data.

## Related tools

- **PyTorch** (Core framework for defining, initializing, and training neural network layers and the model forward/backward passes) — https://pytorch.org/
- **PyG (PyTorch Geometric)** (Provides graph neural network layers and data structures (e.g., GCN, GraphConv) for message passing on molecular graphs) — https://pytorch-geometric.readthedocs.io/en/latest/
- **RDKit** (Preprocesses molecular structures into graph representations (node/edge features) that feed into PyG layers) — https://rdkit.org/
- **NumPy** (Handles construction and manipulation of feature arrays (voxel areas, m/z, adduct encodings) before conversion to PyTorch tensors) — https://numpy.org/

## Examples

```
from torch import nn; class PACCSModel(nn.Module):
  def __init__(self, voxel_dim, graph_dim, adduct_dim, ccs_dim=1):
    super().__init__()
    self.fc1 = nn.Linear(voxel_dim + adduct_dim + 1, 128)
    self.fc2 = nn.Linear(128, 64)
    self.output = nn.Linear(64, ccs_dim)
  def forward(self, voxel, adduct, mz): return self.output(self.fc2(nn.ReLU()(self.fc1(torch.cat([voxel, adduct, mz], dim=1)))))
model = PACCSModel(voxel_dim=1024, graph_dim=128, adduct_dim=5)
```

## Evaluation signals

- Model architecture is syntactically valid in PyTorch (no runtime errors during forward pass on a batch)
- Input tensor shapes flow correctly through all layers without dimension mismatches
- Training loss decreases monotonically (or with acceptable plateaus) over epochs on the training set
- Validation loss remains close to training loss, indicating no severe overfitting; evaluate on held-out test set
- Predicted CCS values on test molecules fall within the range observed in training data (no extreme extrapolation); residuals (predicted − ground-truth) have expected distribution and low mean absolute error

## Limitations

- Model performance depends critically on the quality and representativeness of voxel projected area feature computation; errors in feature preprocessing propagate to predictions.
- Graph neural network layers add complexity and hyperparameter tuning burden; simpler fully-connected architectures may suffice for tabular features alone.
- The model is trained on a curated dataset with specific molecular composition and adduct types; generalization to out-of-distribution molecules or novel adducts is not guaranteed.
- Conformer generation (3D structure) is stochastic; different random seeds or conformer counts may influence feature distributions and thus model performance.

## Evidence

- [other] Construct and configure a deep-learning neural network model using PyTorch, optionally incorporating graph-based message passing from PyG for molecular representations.: "Construct and configure a deep-learning neural network model using PyTorch, optionally incorporating graph-based message passing from PyG for molecular representations."
- [other] Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling.: "Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling."
- [readme] The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model: "The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model"
- [readme] PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph.: "PACCS calculates the projected area with the voxel-based approach, computes the m/z, and constructs the molecular graph."
