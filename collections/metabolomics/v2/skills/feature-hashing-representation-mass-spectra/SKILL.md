---
name: feature-hashing-representation-mass-spectra
description: Use when when you have high-resolution mass spectra that must be rapidly searched against large spectral libraries with open modifications, and you need to reduce the dimensionality of spectral data without losing the ability to retrieve spectrally similar peptides.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-hashing-representation-mass-spectra

## Summary

Feature hashing converts high-resolution mass spectra into fixed-size hash vector representations that preserve spectral similarity while reducing dimensionality, enabling efficient approximate nearest neighbor indexing for rapid open modification spectral library searching.

## When to use

When you have high-resolution mass spectra that must be rapidly searched against large spectral libraries with open modifications, and you need to reduce the dimensionality of spectral data without losing the ability to retrieve spectrally similar peptides. Feature hashing is particularly valuable when the spectral library is too large for exhaustive comparison and you want to index candidates efficiently on GPU hardware.

## When NOT to use

- If you require exact mass accuracy or peak resolution beyond what discretization into hash bins allows; feature hashing inherently trades peak fidelity for speed.
- If your spectral library is small enough for exhaustive comparison; feature hashing adds overhead without benefit when brute-force search is feasible.
- If you need to preserve the full spectral profile for post-hoc interpretation or visualization; hashed representations lose the original spectrum structure.

## Inputs

- High-resolution mass spectra in mzML or similar format
- Query spectrum collection (unknown spectra to be identified)
- Spectral library (reference spectra with known annotations)

## Outputs

- Feature hash vectors (fixed-size binary or numeric vectors per spectrum)
- Indexed approximate nearest neighbor candidate sets for each query
- Ranked peptide identifications with open modification assignments
- False discovery rate–controlled match scores

## How to apply

Convert each query mass spectrum and library spectrum into a feature hash vector using a fixed-size hash table representation. This process discretizes the m/z and intensity dimensions into hash bins, reducing the spectral data to a compact vector while preserving the spectral similarity structure needed for nearest neighbor matching. The hashed vectors are then indexed using approximate nearest neighbor (ANN) indexing (e.g., via Faiss), allowing rapid retrieval of the most relevant library spectra without exhaustive comparison. The cascade search strategy is then applied: first match against unmodified peptides using the hashed candidates, then perform open modification searches on a filtered subset, with strict false discovery rate control applied throughout.

## Related tools

- **ANN-SoLo** (Spectral library search engine that implements feature hashing and GPU-accelerated approximate nearest neighbor indexing for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Provides approximate nearest neighbor indexing and GPU-accelerated similarity search backend for hashed spectral vectors) — https://github.com/facebookresearch/faiss

## Evaluation signals

- Hash vectors are fixed-size and uniform across all spectra; no vector contains null or variable-length fields.
- Nearest neighbor recall: spectra known to be highly similar (high cosine similarity in original space) should consistently rank in top-k ANN candidates.
- False discovery rate at fixed thresholds (e.g., 1%, 5%) matches expected rates from cascade search with unmodified and modified peptides.
- Search speed scales linearly or sublinearly with library size, not quadratically as would occur with exhaustive comparison.
- Ranked identification scores and open modification mass offsets are reproducible across multiple runs with the same query and library.

## Limitations

- Feature hashing requires tuning of hash table size; oversized tables waste memory and computation, while undersized tables increase hash collisions and degrade sensitivity.
- GPU-accelerated feature hashing is currently supported only on Linux systems with NVIDIA CUDA-enabled GPUs; CPU-only versions run on Linux and OSX but are substantially slower.
- ANN-SoLo supports only Python 3.6 to 3.9; Python 3.10 and newer are not currently supported, limiting integration with newer proteomics pipelines.
- The cascade search strategy depends on strict false discovery rate control, which may reject valid identifications if prior unmodified peptide matching is overly stringent.

## Evidence

- [other] Convert spectra to feature hash vectors using a fixed-size hash table representation to reduce dimensionality while preserving similarity structure.: "Convert spectra to feature hash vectors using a fixed-size hash table representation to reduce dimensionality while preserving similarity structure."
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [readme] The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms.: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms."
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet).: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)."
