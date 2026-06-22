---
name: spectral-peak-embedding-encoding
description: Use when when you have variable-length MS/MS peak lists (m/z and intensity arrays) that must be fed into a transformer-based model for spectra analysis, and you need deterministic, normalized embeddings that preserve peak frequency information across multiple scales.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - CLERMS
  - PyTorch
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c00260
  title: CLERMS
evidence_spans: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-embedding-encoding

## Summary

Encodes MS/MS peak m/z and intensity information into fixed-length tensor representations using sinusoidal basis functions for transformer input. This skill transforms raw peak metadata into learnable embeddings compatible with contrastive learning architectures for spectra representation.

## When to use

When you have variable-length MS/MS peak lists (m/z and intensity arrays) that must be fed into a transformer-based model for spectra analysis, and you need deterministic, normalized embeddings that preserve peak frequency information across multiple scales.

## When NOT to use

- Input spectra have already been embedded or vectorized by another method (e.g., already in feature table form).
- Peak lists are extremely short (< 3 peaks) or extremely long (> 10,000 peaks) without adaptive windowing strategy.
- MS/MS data is in formats that do not preserve m/z and intensity information (e.g., spectral similarity scores only).

## Inputs

- m/z array (mass-to-charge ratio values, typically numpy array or torch tensor)
- intensity array (peak intensity values, corresponding 1D array)
- peak metadata (optional: retention time, charge state, or other spectral properties)

## Outputs

- fixed-length embedding tensor (torch.Tensor, shape typically [embedding_dim] or [batch_size, embedding_dim])
- normalized peak representation compatible with transformer input

## How to apply

Define a sinusoidal embedding function that encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales, similar to positional encoding in transformers. Implement the embedder as a callable module that accepts peak metadata arrays (m/z array, intensity array) and outputs fixed-length tensor representations. Normalize input peaks (typically m/z values to a fixed range and intensity values to [0, 1]) before encoding. Apply the sinusoidal basis functions to map normalized peak positions and intensities into a higher-dimensional embedding space. Validate that output tensors have consistent shape regardless of input peak count, maintain numerical stability within expected ranges, and produce deterministic outputs for identical inputs.

## Related tools

- **CLERMS** (Reference implementation of sinusoidal embedder within contrastive learning framework for MS/MS spectra) — https://github.com/HaldamirS/CLERMS
- **PyTorch** (Tensor operations and transformer module implementation)
- **matchms** (MS/MS peak processing and spectra manipulation library)

## Evaluation signals

- Embedding output tensor shape is deterministic and consistent for variable-length input peak lists (e.g., always [embedding_dim] regardless of peak count).
- Sinusoidal encoding maintains orthogonality properties: embeddings for different peak positions produce uncorrelated basis functions across frequency scales.
- Numerical range of embeddings is within expected bounds (typically [-1, 1] for sine/cosine basis) with no NaN or Inf values.
- Unit tests confirm embedder handles edge cases: variable-length peak lists (1 to 10,000+ peaks), normalized vs. unnormalized inputs, and produces identical outputs for identical inputs (determinism).
- Embeddings are compatible with transformer attention mechanisms: batch processing produces correct shape alignment and gradient flow during backpropagation.

## Limitations

- Sinusoidal embeddings assume peak m/z values are normalized to a fixed range; denormalization logic must be preserved for downstream interpretation.
- Fixed-length embedding dimension may lose information for spectra with very high peak density or unusual m/z distributions not seen during design.
- Orthogonality of sinusoidal basis functions degrades if frequency scales are poorly chosen or if m/z normalization range does not span [0, 1) appropriately.
- Some peak records in raw data may contain inaccurate or missing information; preprocessing and filtering (e.g., via dataset_preprocessing.ipynb) must be applied beforehand.

## Evidence

- [other] Define the sinusoidal embedding function that encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales.: "Define the sinusoidal embedding function that encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales."
- [other] Implement the embedder module as a callable component that accepts peak metadata (m/z array, intensity array) and outputs fixed-length tensor representations compatible with Transformer input.: "Implement the embedder module as a callable component that accepts peak metadata (m/z array, intensity array) and outputs fixed-length tensor representations compatible with Transformer input."
- [other] Validate embedding output shape, numerical range, and orthogonality properties of the sinusoidal encoding.: "Validate embedding output shape, numerical range, and orthogonality properties of the sinusoidal encoding."
- [other] Create unit tests confirming embedder handles variable-length peak lists, normalizes inputs correctly, and produces deterministic outputs.: "Create unit tests confirming embedder handles variable-length peak lists, normalizes inputs correctly, and produces deterministic outputs."
- [readme] The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak information and the metadata.: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak"
- [readme] Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for the model input.: "Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for"
