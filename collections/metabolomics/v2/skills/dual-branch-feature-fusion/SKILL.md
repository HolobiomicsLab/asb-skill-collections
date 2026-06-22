---
name: dual-branch-feature-fusion
description: Use when when you have molecular input data available in two or more distinct formats (e.g., RDKit-extracted fingerprints AND torch_geometric Graph objects representing molecular topology) and your prediction target (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3895
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - torch_geometric
  - rdkit-pypi
  - torch-scatter, torch-sparse, torch-cluster
  - RT-Transformer
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
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

# dual-branch-feature-fusion

## Summary

Fuse complementary molecular representations (fingerprint and graph-structured data) through parallel processing branches that independently embed each modality before combining them in a learned fusion layer. This dual-branch strategy exploits both the compactness of fixed-length fingerprints and the topological richness of molecular graphs to improve retention time prediction accuracy.

## When to use

When you have molecular input data available in two or more distinct formats (e.g., RDKit-extracted fingerprints AND torch_geometric Graph objects representing molecular topology) and your prediction target (e.g., retention time, property value) may benefit from both fixed-feature and graph-structured context. Apply this skill when single-modality baseline models underperform and you suspect that structural information alone or feature vectors alone are insufficient.

## When NOT to use

- Input is already a single unified feature table (e.g., pre-concatenated fingerprint + manually engineered descriptors). Use simple MLPs or linear regressors instead.
- Molecular graph data is incomplete or unavailable; fingerprints alone suffice. Single-branch models are simpler and faster.
- Training set is very small (< 100 examples). Multi-branch architectures risk overfitting; consider transfer learning or simpler baselines first.

## Inputs

- Molecular fingerprint tensor: shape [batch_size, fingerprint_dim], dtype float32 (e.g., 1024-bit or 2048-bit RDKit fingerprints)
- Molecular graph batch object: torch_geometric Data object containing node features, edge indices, and batch assignment for multiple graphs
- Retention time labels (optional, for training): shape [batch_size], dtype float32

## Outputs

- Retention time predictions: tensor of shape [batch_size, 1], dtype float32, containing scalar retention time values in the units of the training target
- Fused molecular embedding: tensor of shape [batch_size, embedding_dim], the learned joint representation before the regression head (useful for downstream analysis or transfer learning)

## How to apply

Instantiate two independent processing branches: (1) a fingerprint branch that accepts RDKit-computed molecular fingerprints as dense tensors and projects them through fully connected layers; (2) a graph neural network branch that accepts torch_geometric Graph objects and applies graph convolution layers (e.g., GCN, GIN) to learn node-level and graph-level embeddings. After independent processing, concatenate or apply learned attention-based fusion on the two branch outputs to produce a joint embedding. Feed the fused representation into a regression head (fully connected layers + output neuron) to predict the scalar target. Verify correct forward-pass execution by running a sample batch through the complete model, confirming output shape matches [batch_size, 1] and contains numeric predictions without NaN or Inf values.

## Related tools

- **torch** (Core deep learning framework for defining and training the dual-branch neural network modules)
- **torch_geometric** (Graph neural network library providing graph convolution layers and batch-wise graph handling for the graph branch)
- **rdkit-pypi** (Computes molecular fingerprints (input to the fingerprint branch) and generates initial node/edge features for graph construction)
- **torch-scatter, torch-sparse, torch-cluster** (Low-level PyTorch extensions required by torch_geometric for efficient sparse tensor operations and graph sampling)
- **RT-Transformer** (Reference implementation combining fingerprint and molecular graph inputs for retention time prediction) — https://github.com/01dadada/RT-Transformer

## Examples

```
import torch; from rt_transformer import RTTransformer; model = RTTransformer(fingerprint_dim=1024, graph_hidden_dim=64, fusion_dim=128); fp_batch = torch.randn(8, 1024); graph_batch = create_graph_batch_from_smiles(smiles_list); preds = model(fp_batch, graph_batch); print(preds.shape)  # torch.Size([8, 1])
```

## Evaluation signals

- Forward pass executes without RuntimeError or NaN values; output shape is exactly [batch_size, 1].
- Gradients flow through both branches and the fusion layer during backward pass (check torch.autograd.grad or .backward() without errors).
- Fused embedding dimensionality and composition reflect both fingerprint and graph branch contributions (inspect intermediate tensor shapes and concatenation).
- Model achieves lower mean absolute error or root mean squared error on hold-out test set compared to single-branch (fingerprint-only or graph-only) baselines.
- Ablation study: zeroing one branch's gradients or removing it should degrade performance, confirming both branches contribute predictive signal.

## Limitations

- Architecture assumes fingerprints and graph representations are available for all input molecules; missing or malformed inputs require preprocessing or filtering.
- Different chromatographic conditions may produce different retention times for the same metabolite, limiting the model's cross-method transferability unless transfer learning is applied.
- Fusion layer design (concatenation vs. attention vs. bilinear pooling) is not automatically optimal; hyperparameter tuning and architecture search may be needed.
- Computational cost scales with graph size and batch size; very large molecular graphs or extremely large batches may cause memory overflow.

## Evidence

- [other] The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch, with both inputs processed to produce a retention time prediction as output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [other] Load molecular fingerprints from RDKit feature extraction and construct molecular graph representations using torch_geometric Graph objects.: "Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects."
- [other] Initialize fingerprint processing branch and graph neural network branch with torch_geometric convolution layers.: "instantiate the fingerprint processing branch and the graph neural network branch (using torch_geometric convolution layers)"
- [other] Define a fusion layer that combines fingerprint and graph embeddings, then implement a regression head that outputs scalar retention time predictions.: "Define the fusion layer that combines fingerprint and graph embeddings. 4. Implement the regression head that outputs scalar retention time predictions."
- [other] Verify model runs forward pass without errors and produces output tensor of shape [batch_size, 1] with numeric predictions.: "confirm model runs forward pass without errors and produces output tensor of shape [batch_size, 1] with numeric predictions"
- [readme] Liquid chromatography retention times prediction can assist in metabolite identification in non-targeted metabolomics.: "Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics."
- [readme] Different chromatographic conditions may result in different retention times for the same metabolite, limiting cross-method transferability.: "different chromatographic conditions may result in different retention times for the same metabolite"
