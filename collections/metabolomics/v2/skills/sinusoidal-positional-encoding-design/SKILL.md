---
name: sinusoidal-positional-encoding-design
description: Use when you have variable-length lists of MS/MS peaks (m/z and intensity pairs) that need to be encoded into a fixed-dimensional representation compatible with transformer architecture.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3444
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - PyTorch
  - matchms
  - CLERMS
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
---

# sinusoidal-positional-encoding-design

## Summary

Design and implement a sinusoidal embedder that encodes MS/MS peak m/z and intensity metadata into fixed-length tensor representations for transformer input. This skill is essential when building transformer-based models for mass spectrometry data where peak positions and magnitudes must be converted into learnable token embeddings.

## When to use

You have variable-length lists of MS/MS peaks (m/z and intensity pairs) that need to be encoded into a fixed-dimensional representation compatible with transformer architecture. Use this skill when your downstream model requires position-aware and magnitude-aware embeddings of mass spectrometry spectral data, and when contrastive learning or attention mechanisms depend on structured peak metadata.

## When NOT to use

- Peak data is already pre-embedded or represents a feature table incompatible with sinusoidal encoding.
- Your model does not use transformer architecture or does not require position-aware embeddings.
- MS/MS data has been heavily binned or discretized into fixed-size histogram bins (use existing bin indices instead).

## Inputs

- m/z array (mass-to-charge ratio values, typically numpy array or tensor)
- intensity array (peak intensity values, aligned with m/z array)
- peak metadata (optional: retention time, adduct type, or other spectral properties)
- variable-length peak lists (ragged or padded)

## Outputs

- fixed-length tensor embeddings compatible with transformer input
- embedding tensor of shape (batch_size, max_peaks, embedding_dim)
- normalized embeddings with documented numerical range

## How to apply

Define sinusoidal basis functions at multiple frequency scales to encode peak m/z and intensity values independently, following the standard transformer positional encoding pattern. Normalize input peak m/z and intensity arrays to consistent ranges (typically [0, 1] or standardized). Implement the embedder as a callable module that accepts raw peak metadata and outputs fixed-length tensors. Validate that embeddings have the correct shape, numerical range within expected bounds, and exhibit orthogonality properties across frequency dimensions. Handle variable-length peak lists through padding or masking, and confirm deterministic output for identical inputs.

## Related tools

- **PyTorch** (Tensor computation and neural module implementation for the sinusoidal embedder)
- **matchms** (MS/MS spectrum object handling and peak metadata extraction)
- **CLERMS** (Reference implementation of sinusoidal embedder integrated with contrastive learning and transformer backbone) — github.com/HaldamirS/CLERMS

## Examples

```
python model.ipynb  # After running dataset_preprocessing.ipynb and cal_tanimoto_score.ipynb to normalize peaks; embedder processes m/z and intensity arrays into fixed-length tensors for CLERMS transformer training.
```

## Evaluation signals

- Embedding tensor shape matches (batch_size, num_peaks, embedding_dim) with no ragged dimensions.
- Numerical values lie within expected range (e.g., ±1.0 for standard sinusoidal encoding) and do not contain NaN or Inf.
- Orthogonality check: dot product between embedding vectors from different frequency scales is near zero.
- Determinism: identical peak lists produce identical embeddings across repeated runs.
- Variable-length handling: padded or masked embeddings produce valid transformer attention weights without spurious alignments.
- Downstream task performance: embeddings achieve non-trivial accuracy on compound identification or spectra clustering benchmarks (e.g., GNPS dataset).

## Limitations

- Requires normalized peak m/z and intensity inputs; raw, unnormalized spectra will produce out-of-range embeddings. Preprocessing via cal_tanimoto_score.ipynb or dataset_preprocessing.ipynb is necessary.
- Performance depends on choice of frequency scales and embedding dimensionality; no guidance is provided in the article for tuning these hyperparameters beyond transformer defaults.
- Does not account for complex peak features such as isotope patterns or neutral loss metadata unless explicitly augmented into the metadata array.
- Sinusoidal encoding assumes relative peak positions are meaningful; spectra that have been heavily filtered or deisotoped may lose information.

## Evidence

- [intro] peak_encoding: "Define the sinusoidal embedding function that encodes peak m/z and intensity values using sine and cosine basis functions at multiple frequency scales."
- [intro] embedder_module: "Implement the embedder module as a callable component that accepts peak metadata (m/z array, intensity array) and outputs fixed-length tensor representations compatible with Transformer input."
- [intro] validation_criteria: "Validate embedding output shape, numerical range, and orthogonality properties of the sinusoidal encoding."
- [intro] unit_tests: "Create unit tests confirming embedder handles variable-length peak lists, normalizes inputs correctly, and produces deterministic outputs."
- [readme] clerms_architecture: "The model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak"
- [readme] preprocessing_requirement: "Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for"
