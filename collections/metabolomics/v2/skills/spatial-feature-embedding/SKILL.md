---
name: spatial-feature-embedding
description: Use when when analyzing imaging mass spectrometry datasets where you need to reduce high-dimensional peak intensity features while preserving spatial structure, and when automatic peak picking and marker ion identification are required.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - scanpy
  - STAGATE
  - pandas
  - h5py
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
---

# Reconstruct the graph-attention autoencoder for latent peak-feature embedding on IMS data

## Summary

A graph-attention autoencoder architecture that transforms imaging mass spectrometry (IMS) peak intensities into low-dimensional latent representations by encoding spatial adjacency and node features, enabling automatic peak picking and marker ion identification in spatial metabolomics.

## When to use

When analyzing imaging mass spectrometry datasets where you need to reduce high-dimensional peak intensity features while preserving spatial structure, and when automatic peak picking and marker ion identification are required. Apply this skill when your IMS data is represented as a spatial graph (nodes = pixels/spectra, edges = spatial adjacency) and you aim to discover interpretable latent features for downstream analysis.

## When NOT to use

- Input IMS data lacks explicit spatial structure or adjacency information (use standard autoencoders instead)
- Peak intensity data is already dimensionality-reduced or converted to a pre-computed feature table
- Analysis goal is simple denoising without latent feature extraction (use conventional filtering)

## Inputs

- Imaging mass spectrometry (IMS) spatial graph with node features (peak intensity vectors per pixel/spectrum)
- Edge adjacency matrix or list encoding spatial relationships between pixels
- Peak intensity feature matrix (samples × m/z values or spectral features)

## Outputs

- Latent low-dimensional peak feature embeddings (samples × latent_dimension)
- Reconstructed peak intensity features (same shape as input)
- Autoencoder model weights and architecture
- Identified marker ions from iterative peak picking on latent features

## How to apply

Define a graph-attention autoencoder with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency relationships) from the IMS spatial graph. The encoder progressively reduces peak intensity dimensionality through one or more graph-attention layers to a target latent dimension. Implement a corresponding decoder using transposed graph-attention or fully-connected layers that mirrors the encoder structure to reconstruct peak intensities from latent vectors. Assemble the complete autoencoder by chaining encoder and decoder components, then validate the forward pass accepts spatial graph tensors (node features and adjacency) and outputs both reconstructed peak intensities and latent representations. The latent features are then used iteratively to identify marker ions through automatic peak picking.

## Related tools

- **scanpy** (Single-cell analysis framework used for processing and manipulation of spatial omics data structures)
- **STAGATE** (Spatial transcriptomics analysis method providing graph-attention mechanisms for spatial data)
- **pandas** (Data manipulation and tabular representation of peak intensities and metadata)
- **h5py** (HDF5 file I/O for storing and retrieving large imaging mass spectrometry datasets)

## Evaluation signals

- Forward pass on spatial graph tensor completes without shape mismatches; encoder output latent dimension matches specified target; decoder output shape matches input peak intensity shape
- Reconstruction error (e.g., MSE between input and reconstructed peak intensities) decreases monotonically during training
- Latent representations capture meaningful variance: dimensionality reduction from high-dimensional peak space to low-dimensional embedding is verified (e.g., variance explained, reconstruction fidelity)
- Marker ions identified through iterative peak picking on latent features show biological or chemical consistency (co-localization with known metabolite distributions in spatial context)
- Graph-attention weights reflect expected spatial locality: higher attention scores between adjacent pixels/spectra, lower scores for distant nodes

## Limitations

- Requires explicit spatial adjacency definition; performance depends on correct graph construction and edge weighting
- Computational cost scales with graph size; may be prohibitive for very large IMS datasets or dense adjacency matrices
- No changelog found; version stability and API compatibility across releases are not documented
- Latent feature interpretability depends on architecture choices (number of layers, hidden dimensions); no guidance provided for hyperparameter selection

## Evidence

- [other] SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker ion identification.: "SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker"
- [other] Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data.: "Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data"
- [other] Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension.: "Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension"
- [readme] For imageing mass specturm(IMS) datasets, SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions.: "For imageing mass specturm(IMS) datasets, SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the"
- [other] Assemble the complete autoencoder module by chaining encoder and decoder components and validate that forward pass accepts spatial graph tensors and outputs both reconstructed peak intensities and latent representations.: "Assemble the complete autoencoder module by chaining encoder and decoder components and validate that forward pass accepts spatial graph tensors and outputs both reconstructed peak intensities and"
