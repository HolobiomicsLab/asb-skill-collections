---
name: latent-space-dimensionality-reduction
description: Use when you have imaging mass spectrometry (IMS) datasets where peak
  intensities are high-dimensional and sparse, and you need to extract compressed
  latent features that preserve spatial adjacency relationships and enable iterative
  automatic peak picking to identify marker ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - scanpy
  - STAGATE
  - pandas
  - h5py
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: restricted
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

# latent-space-dimensionality-reduction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use a graph-attention autoencoder to compress imaging mass spectrometry peak intensity data into low-dimensional latent representations that capture spatial and spectral structure. This enables downstream automatic peak picking and marker ion identification in spatial metabolomics.

## When to use

You have imaging mass spectrometry (IMS) datasets where peak intensities are high-dimensional and sparse, and you need to extract compressed latent features that preserve spatial adjacency relationships and enable iterative automatic peak picking to identify marker ions.

## When NOT to use

- Input data is already in a manually-curated low-dimensional feature space or peak list
- Spatial adjacency information is unavailable or meaningless for your IMS dataset
- Your primary goal is direct peak annotation rather than unsupervised feature discovery

## Inputs

- Imaging mass spectrometry (IMS) peak intensity matrix (nodes × peaks)
- Spatial adjacency graph structure (edge list or adjacency matrix)
- Target latent dimensionality (integer, typically << input peak count)

## Outputs

- Latent low-dimensional peak feature matrix (nodes × latent_dim)
- Reconstructed peak intensity matrix (nodes × peaks)
- Encoder weights for downstream peak-picking inference

## How to apply

Define a graph-attention autoencoder architecture where the encoder processes node features (peak intensities) and edge information (spatial adjacency) from IMS data through one or more graph-attention layers, progressively reducing dimensionality to your target latent dimension. Implement the decoder using transposed graph-attention or fully-connected layers mirroring the encoder to reconstruct peak intensities from latent vectors. Train the autoencoder end-to-end on your IMS spatial graph tensor, then extract the latent representations from the encoder output. These compressed latent features are then fed into iterative peak-picking routines to identify marker ions without manual thresholding.

## Related tools

- **scanpy** (Single-cell / spatial data manipulation and analysis for preprocessing IMS tensors)
- **STAGATE** (Spatial transcriptomics graph-attention framework that provides the base graph-attention architecture)
- **pandas** (Tabular data I/O and metadata management for peak intensity tables)
- **h5py** (HDF5 I/O for large-scale IMS datasets)

## Evaluation signals

- Latent feature dimensionality is significantly lower than input peak count while retaining reconstruction fidelity (e.g., mean squared error of reconstructed peaks < user tolerance)
- Latent representations cluster spatially-adjacent pixels in 2D/3D latent space, indicating learned spatial structure
- Iterative peak picking applied to latent features identifies consistent marker ions across multiple runs
- Encoder forward pass accepts spatial graph tensors and outputs both reconstructed peak intensities and latent vectors without shape mismatches
- Ablation: removing graph-attention layers degrades marker ion identification rate compared to graph-attention baseline

## Limitations

- No changelog or version history available in the provided documentation
- Latent dimensionality is a hyperparameter requiring manual tuning or cross-validation; no principled selection method is specified
- Performance depends on quality of spatial adjacency graph; irregular or noisy spatial coordinates may degrade learned representations
- Computational cost scales with number of peaks and spatial graph density; very large IMS datasets may require memory-efficient sparse implementations

## Evidence

- [other] How does the graph-attention autoencoder in SmartGate transform imaging mass spectrometry peak intensities into low-dimensional latent representations?: "How does the graph-attention autoencoder in SmartGate transform imaging mass spectrometry peak intensities into low-dimensional latent representations?"
- [other] SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets: "SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker"
- [other] Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension.: "Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension."
- [other] Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data.: "Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data."
- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions."
