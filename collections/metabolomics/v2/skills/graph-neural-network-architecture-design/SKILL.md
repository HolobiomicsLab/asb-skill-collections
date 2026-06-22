---
name: graph-neural-network-architecture-design
description: Use when you have molecular structures that need to be represented as both fingerprint vectors (fixed-length chemical descriptors) and graph-structured data, and you need a model that can learn from both representations simultaneously to predict a continuous molecular property (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3934
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - torch_geometric
  - PyTorch (torch)
  - RDKit (rdkit-pypi)
  - torch-scatter, torch-sparse, torch-cluster
  - scanpy
  - STAGATE
  - pandas
  - h5py
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
- doi: 10.1021/acs.analchem.4c06210
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
- scanpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  - build: coll_smartgate_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
---

# Graph Neural Network Architecture Design

## Summary

Design and instantiate a dual-branch graph neural network architecture that processes molecular graph representations (constructed as torch_geometric Graph objects) alongside molecular fingerprints to produce molecular property predictions. This skill integrates graph convolution layers with fingerprint embeddings via a fusion layer for joint feature learning.

## When to use

You have molecular structures that need to be represented as both fingerprint vectors (fixed-length chemical descriptors) and graph-structured data, and you need a model that can learn from both representations simultaneously to predict a continuous molecular property (e.g., retention time). Typical scenario: predicting retention time for metabolite identification when different chromatographic conditions produce variable retention times for the same compound.

## When NOT to use

- Input molecules are only available as SMILES strings or InChI without pre-computed fingerprints or graph representations — use preprocessing steps first.
- You need to predict discrete classes (e.g., metabolite categories) rather than continuous properties — use classification heads instead.
- Graph representations are unavailable or computationally prohibitive for your dataset size — fall back to fingerprint-only or fingerprint + traditional descriptor methods.

## Inputs

- RDKit molecular fingerprints (dense tensor of shape [batch_size, fingerprint_dim])
- torch_geometric Graph objects with node features, edge indices, and optional edge attributes
- torch_geometric DataLoader batch object combining graphs from multiple molecules

## Outputs

- Trained RT-Transformer model instance (PyTorch nn.Module)
- Scalar retention time predictions (tensor of shape [batch_size, 1])
- Joint embeddings from fingerprint and graph branches (intermediate representations)

## How to apply

First, prepare dual molecular representations: extract fingerprints using RDKit feature extraction and construct molecular graph representations using torch_geometric Graph objects with node and edge features. Second, define a dual-branch PyTorch architecture: instantiate one branch with fully connected layers for fingerprint processing and another branch using torch_geometric convolution layers (e.g., GraphConv, GATConv) for graph-structured data. Third, implement a fusion layer that concatenates or otherwise combines embeddings from both branches. Fourth, attach a regression head (typically fully connected layers) that outputs scalar predictions (e.g., shape [batch_size, 1]). Finally, verify the complete forward pass on a sample batch containing both fingerprint tensors and graph batch objects (from torch_geometric.data.DataLoader), confirming output shape and numeric predictions without errors.

## Related tools

- **torch_geometric** (Graph neural network library providing Graph objects, convolution layers (GraphConv, GATConv), and batch utilities for processing molecular graph data)
- **PyTorch (torch)** (Core deep learning framework for building and training the dual-branch neural network architecture)
- **RDKit (rdkit-pypi)** (Molecular cheminformatics library for extracting fingerprints from molecular structures)
- **torch-scatter, torch-sparse, torch-cluster** (Supporting libraries for efficient graph operations and scatter operations required by torch_geometric)

## Examples

```
from torch_geometric.data import DataLoader; from rdkit import Chem; from rdkit.Chem import AllChem; import torch; fingerprints = torch.tensor([AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromInChI(inchi), 2, nBits=2048) for inchi in inchis], dtype=torch.float32); graph_batch = DataLoader(graphs, batch_size=32).__iter__().__next__(); model(fingerprints, graph_batch)
```

## Evaluation signals

- Forward pass executes without errors on a sample batch containing both fingerprint tensors and torch_geometric graph batch objects
- Output tensor has expected shape [batch_size, 1] with numeric (float) dtype
- Model gradients flow correctly through both fingerprint and graph branches during backpropagation (no NaN or Inf values)
- Loss decreases monotonically over training epochs when fitted on labeled data (e.g., SMRT dataset with InChI and RT columns)
- Predictions on held-out test set show correlation with ground-truth retention times (e.g., Pearson R² or mean absolute error within acceptable range for the chromatographic method)

## Limitations

- Different chromatographic conditions may result in different retention times for the same metabolite, requiring transfer learning or condition-specific fine-tuning rather than universal predictions
- Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another without retraining
- Graph construction requires valid molecular structure representations (InChI, SMILES); invalid or ambiguous structures will fail preprocessing
- Fingerprint dimensionality and graph feature engineering choices significantly impact model performance but require domain tuning

## Evidence

- [other] The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [methods] Molecular graphs are constructed using torch_geometric Graph objects with convolution layers: "construct molecular graph representations using torch_geometric Graph objects. 2. Initialize the RT-Transformer dual-branch architecture in PyTorch: instantiate the fingerprint processing branch and"
- [methods] The model outputs scalar retention time predictions with shape [batch_size, 1]: "Validation: confirm model runs forward pass without errors and produces output tensor of shape [batch_size, 1] with numeric predictions."
- [methods] Fingerprints are extracted from RDKit feature extraction: "Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects."
- [readme] Different chromatographic conditions and method transferability are key challenges: "different chromatographic conditions may result in different retention times for the same metabolite. Current retention time prediction methods lack sufficient scalability to transfer from one"
- [readme] Datasets use InChI and RT columns for training: "Prepare your dataset as a csv file which has "InChI" and "RT" columns."
