---
name: transformer-input-representation-construction
description: Use when you have variable-length MS/MS peak lists (m/z arrays and intensity arrays) that must be fed into a transformer architecture for tasks like compound identification or spectral clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - transformer
  - CLERMS
  - PyTorch
  - matchms
derived_from:
- doi: 10.1021/acs.analchem.3c00260
  title: CLERMS
evidence_spans:
- based on transformer architecture
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clerms_cq
    doi: 10.1021/acs.analchem.3c00260
    title: CLERMS
  dedup_kept_from: coll_clerms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00260
  all_source_dois:
  - 10.1021/acs.analchem.3c00260
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-input-representation-construction

## Summary

Construct sinusoidal token embeddings from MS/MS peak m/z and intensity data to generate fixed-length tensor representations compatible with transformer input. This skill bridges raw mass spectrometry peak information into the continuous vector space required by transformer-based models for spectral analysis.

## When to use

Apply this skill when you have variable-length MS/MS peak lists (m/z arrays and intensity arrays) that must be fed into a transformer architecture for tasks like compound identification or spectral clustering. The skill is necessary whenever raw peak data needs to be converted into fixed-length, position-aware embeddings that preserve both magnitude (intensity) and frequency (m/z) information.

## When NOT to use

- Input is already a pre-computed embedding or feature table from another representation learning method.
- Peak data has already been encoded by a different embedder (e.g., spectral library fingerprints or molecular descriptors); re-embedding introduces redundant transformations.
- You require interpretable peak-level outputs; sinusoidal embeddings obscure individual peak contributions in high-dimensional space.

## Inputs

- m/z array (mass-to-charge ratio values)
- intensity array (peak intensity values)
- peak metadata dictionary
- variable-length peak lists

## Outputs

- fixed-length tensor representations
- transformer-compatible token embeddings
- normalized embedding tensors with shape [num_peaks, embedding_dim]

## How to apply

Define sinusoidal embedding functions that encode peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales. Implement an embedder module that accepts peak metadata (m/z array, intensity array) and outputs fixed-length tensor representations. Normalize input peaks to a standard range before encoding to ensure consistent scaling across variable-intensity spectra. The embedder must handle variable-length peak lists by either padding or truncating to a fixed maximum number of peaks, then validate that output tensors have consistent shape, numerical range within expected bounds, and that the sinusoidal basis functions exhibit orthogonality properties. Produce deterministic outputs to ensure reproducibility across training runs.

## Related tools

- **CLERMS** (Contrastive learning framework that consumes sinusoidal embeddings as input to its transformer backbone for MS/MS spectral representation learning) — https://github.com/HaldamirS/CLERMS
- **PyTorch** (Tensor computation and autograd framework used to implement sinusoidal embedder module and transformer components)
- **matchms** (Mass spectrometry data loading and preprocessing library for handling raw peak data and metadata)

## Evaluation signals

- Embedding output tensor shape is [num_peaks, embedding_dim] where num_peaks is consistent (e.g., padded to max_peaks=500) and embedding_dim is the configured sinusoidal feature dimension.
- Numerical range of embeddings falls within expected bounds (typically ±1 for normalized sine/cosine functions); check min/max values and histogram of embedding values.
- Sinusoidal basis functions exhibit orthogonality: dot product between distinct frequency components across a batch approaches zero (e.g., correlation < 0.1).
- Variable-length input peak lists (10 peaks, 100 peaks, 500 peaks) all produce valid outputs without shape mismatches or NaN values.
- Repeated calls on identical input (m/z, intensity) produce bitwise-identical embeddings; verify determinism with seed-setting and checksums.

## Limitations

- Sinusoidal embeddings lose direct interpretability; individual peaks become entangled in high-dimensional space, complicating ablation studies.
- Padding or truncation of variable-length peak lists to a fixed size may discard rare high-intensity peaks or introduce artificial sparsity.
- Normalized input assumptions: if input m/z or intensity distributions differ significantly across datasets (e.g., different MS instruments or ion sources), re-normalization may be required; the README notes that 'peak information needs to be normalized for the model input'.
- No explicit handling of missing or zero-intensity peaks; the embedder must gracefully handle edge cases like spectra with very few peaks or all-zero intensities.

## Evidence

- [other] CLERMS employs a sinusoidal embedder component that processes peak information and metadata to generate embeddings consumed by a transformer-based architecture.: "CLERMS employs a sinusoidal embedder component that processes peak information and metadata to generate embeddings consumed by a transformer-based architecture."
- [other] The sinusoidal embedder encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales.: "Define the sinusoidal embedding function that encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales."
- [other] The embedder accepts peak metadata and outputs fixed-length tensor representations compatible with Transformer input.: "Implement the embedder module as a callable component that accepts peak metadata (m/z array, intensity array) and outputs fixed-length tensor representations compatible with Transformer input."
- [other] Validation includes embedding output shape, numerical range, and orthogonality properties of the sinusoidal encoding.: "Validate embedding output shape, numerical range, and orthogonality properties of the sinusoidal encoding."
- [intro] The model architecture is equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss.: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss"
- [readme] Peak information needs to be normalized for the model input during preprocessing.: "the peak information needs to be normalized for the model input"
- [other] Unit tests must confirm embedder handles variable-length peak lists and produces deterministic outputs.: "Create unit tests confirming embedder handles variable-length peak lists, normalizes inputs correctly, and produces deterministic outputs."
