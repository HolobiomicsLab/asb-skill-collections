---
name: autoencoder-encoder-decoder-design
description: Use when when working with imaging mass spectrometry (IMS) datasets where you need to extract latent low-dimensional peak features from high-dimensional peak intensity data while preserving spatial adjacency information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scanpy
  - STAGATE
  - pandas
  - h5py
  techniques:
  - MS-imaging
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- scanpy
- STAGATE
- pandas
- h5py
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartgate_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smartgate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# autoencoder-encoder-decoder-design

## Summary

Design and implement a graph-attention autoencoder architecture that maps imaging mass spectrometry peak intensities into low-dimensional latent representations and reconstructs them. This skill enables automatic feature extraction from spatial metabolomics data for downstream peak picking and marker ion identification.

## When to use

When working with imaging mass spectrometry (IMS) datasets where you need to extract latent low-dimensional peak features from high-dimensional peak intensity data while preserving spatial adjacency information. Use this skill when your goal is to enable iterative automatic peak picking or marker ion identification in spatial metabolomics studies.

## When NOT to use

- Input data lacks spatial structure or adjacency information; use a standard autoencoder instead
- Peak intensities are already in a processed low-dimensional latent space
- Computational resources are severely constrained; graph-attention layers have higher complexity than fully-connected autoencoders

## Inputs

- Imaging mass spectrometry (IMS) dataset as HDF5 or scanpy-compatible format
- Peak intensity matrix with spatial adjacency graph structure
- Node features (peak intensities) and edge information (spatial neighbors)

## Outputs

- Latent low-dimensional peak feature representations
- Reconstructed peak intensity features
- Trained graph-attention autoencoder model

## How to apply

First, define a graph-attention autoencoder architecture by implementing graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from your IMS data. Implement the encoder to progressively reduce dimensionality through one or more graph-attention layers down to your target latent dimension. Then implement a symmetric decoder using transposed graph-attention or fully-connected layers to reconstruct peak intensities from latent vectors. Assemble the complete autoencoder by chaining encoder and decoder components, ensuring the forward pass accepts spatial graph tensors as input and outputs both reconstructed peak intensities and latent representations. Validate that latent features capture peak identity and spatial structure by inspecting their utility in downstream peak picking tasks.

## Related tools

- **scanpy** (Manage and process imaging mass spectrometry data structures)
- **STAGATE** (Provide graph-attention layer implementations and spatial graph construction)
- **pandas** (Handle tabular peak intensity and metadata formats)
- **h5py** (Read and write HDF5-formatted IMS datasets)

## Evaluation signals

- Forward pass accepts spatial graph tensors (nodes, edges) and outputs latent vectors with expected dimensionality matching the target latent dimension
- Reconstruction loss (MSE or similar) on held-out peak intensity data decreases monotonically during training
- Latent representations enable accurate marker ion identification and automatic peak picking in downstream tasks compared to baseline methods
- Decoder successfully reconstructs peak intensity distributions with fidelity comparable to input data statistics
- Latent features from the encoder show meaningful clustering or separation of chemically distinct peaks when visualized in 2D/3D space

## Limitations

- Requires well-defined spatial adjacency graph; missing or noisy spatial information may degrade latent feature quality
- Graph-attention layers scale computationally with graph size; very large IMS datasets may require subsampling or tiling strategies
- Hyperparameter tuning (latent dimension, number of attention heads, encoder depth) is data-dependent and may require cross-validation
- No changelog or version history provided in the SmartGate repository, limiting reproducibility across releases

## Evidence

- [other] SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker ion identification.: "SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker"
- [other] Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data.: "Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data"
- [other] Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension.: "Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension"
- [other] Implement the decoder to reconstruct peak intensity features from latent vectors using transposed graph-attention or fully-connected layers, mirroring the encoder structure.: "Implement the decoder to reconstruct peak intensity features from latent vectors using transposed graph-attention or fully-connected layers, mirroring the encoder structure"
- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions"
