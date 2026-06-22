---
name: mass-spectrometry-peak-intensity-encoding
description: Use when working with imaging mass spectrometry (IMS) datasets where you need to (1) automatically identify marker ions without manual annotation, (2) reduce peak intensity dimensionality while preserving spatial relationships between measurement points, or (3) apply iterative peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - scanpy
  - STAGATE
  - pandas
  - h5py
  techniques:
  - direct-infusion-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-intensity-encoding

## Summary

Encodes imaging mass spectrometry peak intensities into low-dimensional latent representations using a graph-attention autoencoder that preserves spatial adjacency structure. This enables automatic peak picking and marker ion identification in spatial metabolomics workflows.

## When to use

Use this skill when working with imaging mass spectrometry (IMS) datasets where you need to (1) automatically identify marker ions without manual annotation, (2) reduce peak intensity dimensionality while preserving spatial relationships between measurement points, or (3) apply iterative peak picking strategies that require stable latent feature representations across multiple rounds of selection.

## When NOT to use

- Input peak intensities are already in a stable, manually curated low-dimensional feature space (e.g., from prior marker selection)—encoding would introduce unnecessary reconstruction loss.
- Spatial structure is unknown or irrelevant to the analysis goal; a standard PCA or VAE would be more efficient.
- IMS data lacks clear spatial coherence or the measurement grid is severely sparse or irregular; graph-attention benefits diminish when spatial adjacency is uninformative.

## Inputs

- imaging mass spectrometry (IMS) peak intensity matrix (e.g., n_pixels × n_peaks, typically stored in .h5 format)
- spatial adjacency graph structure defining neighborhood relationships between IMS measurement points
- node feature matrix (peak intensities at each spatial location)

## Outputs

- latent peak feature representation (low-dimensional embedding per spatial location)
- reconstructed peak intensity matrix (autoencoder decoder output)
- graph-attention weights (optionally, for interpretability of spatial influence)

## How to apply

Construct a graph-attention autoencoder by: (1) defining an encoder with one or more graph-attention layers that process node features (peak intensities from each spatial location) and edge information (spatial adjacency between neighboring measurement points in the IMS grid); (2) progressively reducing dimensionality through the encoder layers to a target latent dimension; (3) implementing a symmetric decoder using transposed graph-attention or fully-connected layers to reconstruct peak intensities from latent vectors; (4) training the autoencoder end-to-end on the full IMS peak matrix so that forward passes accept spatial graph tensors and output both reconstructed intensities and latent representations. The spatial graph structure is critical—it ensures the latent features encode not just intensity patterns but also their spatial context, which supports iterative marker ion discovery.

## Related tools

- **scanpy** (Preprocessing and handling spatial transcriptomics/metabolomics data structures; preparing peak intensity matrices and spatial coordinate annotations for graph construction.)
- **STAGATE** (Provides spatial graph-attention framework and reference implementations for encoding spatial features with attention mechanisms; used as a foundation for the IMS-specific autoencoder variant.)
- **pandas** (Data manipulation and metadata handling for peak annotations, spatial coordinates, and results aggregation.)
- **h5py** (Reading and writing IMS peak intensity data stored in HDF5 format (.h5 files).)

## Evaluation signals

- Latent representation dimensionality is significantly reduced (e.g., from thousands of peaks to 10–100 latent dims) with low reconstruction error (mean squared error between input and autoencoder output stays below ~5–10% of input variance).
- Graph-attention encoder weights show high activation along spatial adjacency edges, indicating the model is learning spatial structure; random adjacency graphs should show lower attention weights.
- Iterative peak picking applied downstream produces consistent marker ion selections across successive rounds, and the latent features remain stable between training runs.
- Reconstructed peak intensities preserve rank-order relationships with input intensities within each spatial neighborhood; local spatial coherence is maintained.
- Marker ions identified via latent feature clustering are interpretable and consistent with biological/chemical expectations (e.g., known metabolite signatures in the tissue type being imaged).

## Limitations

- Graph-attention autoencoder performance depends critically on the quality and correctness of the spatial adjacency graph; misspecified or noisy spatial relationships will degrade latent quality.
- Reconstruction loss alone is not sufficient to validate the latent representation; downstream tasks (peak picking, marker identification) must be evaluated to confirm utility.
- Computational cost scales with both the number of peaks and the spatial resolution of the IMS dataset; very large datasets may require distributed training or data sampling strategies.
- The method assumes peak intensities follow patterns that are spatially coherent; IMS data from highly heterogeneous tissue or with strong noise may not benefit from spatial encoding.
- No published changelog or versioning documented; reproducibility across SmartGate repository forks may vary.

## Evidence

- [intro] Graph-attention autoencoder in SmartGate transforms imaging mass spectrometry peak intensities into low-dimensional latent representations: "SmartGate employs a graph-attention autoencoder architecture that generates latent low-dimensional peak features from imaging mass spectrometry datasets to enable automatic peak picking and marker"
- [other] Graph-attention encoder processes node features (peak intensities) and edge information (spatial adjacency): "Define the graph-attention autoencoder architecture with graph-attention encoder layers that process node features (peak intensities) and edge information (spatial adjacency) from IMS data."
- [other] Encoder reduces dimensionality progressively to target latent dimension; decoder reconstructs from latent vectors: "Implement the encoder to map input peak intensity features through one or more graph-attention layers, reducing dimensionality progressively to the target latent dimension."
- [other] Forward pass accepts spatial graph tensors and outputs reconstructed intensities and latent representations: "Assemble the complete autoencoder module by chaining encoder and decoder components and validate that forward pass accepts spatial graph tensors and outputs both reconstructed peak intensities and"
- [readme] Graph-attention autoencoder achieves automatic peak picking iteratively to find marker ions: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions."
- [readme] Iterative graph attention auto-encoder method for spatial metabolomics: "spatial metabolomics by introducing an iterative graph attention auto-encoder method SmartGate"
