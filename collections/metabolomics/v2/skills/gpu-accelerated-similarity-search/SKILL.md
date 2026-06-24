---
name: gpu-accelerated-similarity-search
description: Use when you have a large spectral library and many query spectra to
  search against it, and you need to identify both unmodified and open-modification
  peptides with strict false discovery rate control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary)
  is a spectral library search engine'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GPU-Accelerated Similarity Search

## Summary

Accelerate approximate nearest neighbor (ANN) indexing and spectral library candidate retrieval using GPU computation to enable fast and accurate open modification searching on high-resolution mass spectra. This skill combines feature dimensionality reduction with GPU-powered similarity matching to speed up identification workflows while maintaining sensitivity.

## When to use

You have a large spectral library and many query spectra to search against it, and you need to identify both unmodified and open-modification peptides with strict false discovery rate control. GPU acceleration is particularly valuable when searching high-resolution mass spectra where cascade search strategies (unmodified first, then open modifications) require repeated candidate ranking and scoring.

## When NOT to use

- Input spectra are already pre-indexed or pre-filtered; GPU acceleration adds no benefit over existing indices
- Low-resolution mass spectra or small spectral libraries where CPU-only ANN indexing is already sufficiently fast
- Computing environment lacks NVIDIA CUDA-enabled GPU device or is not Linux-based (CPU-only mode available for Linux/OSX but without GPU speedup)

## Inputs

- Query mass spectra (high-resolution format)
- Spectral library (high-resolution format)
- Feature hash configuration (fixed-size hash table representation)

## Outputs

- Ranked candidate spectral matches
- Identification scores per query spectrum
- False discovery rate-controlled identifications (unmodified and modified)

## How to apply

Load query spectra and spectral library in high-resolution format. Convert spectra to fixed-size feature hash vectors to reduce dimensionality while preserving similarity structure. Index the hashed library spectra using approximate nearest neighbor (ANN) indexing to enable rapid candidate retrieval. Accelerate the indexing and candidate retrieval steps using GPU computation (NVIDIA CUDA-enabled devices on Linux). Execute a cascade search strategy starting with unmodified peptides, then open modification searches, applying strict false discovery rate control. GPU acceleration primarily speeds up the ANN indexing construction and the high-dimensional similarity distance computations needed to rank candidates.

## Related tools

- **ANN-SoLo** (GPU-accelerated spectral library search engine implementing approximate nearest neighbor indexing with cascade search strategy and shifted dot product scoring) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library for approximate nearest neighbor indexing with GPU support; required dependency for ANN-SoLo GPU-powered version) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --spectrum_file query_spectra.mgf --library_file library.mgf --output results.tsv
```

## Evaluation signals

- GPU memory utilization and computation time should be significantly lower than CPU-only equivalent; benchmark wall-clock time for candidate retrieval and ranking steps
- Cascade search strategy should correctly identify unmodified matches first, then apply open modification search to remaining unmatched spectra without increasing false discovery rate
- Cascade search FDR should be strictly controlled (verify reported FDR values against expected thresholds set in the analysis parameters)
- Ranked candidates should have higher shifted dot product scores for true matches; verify score distributions are unimodal and separated from decoy distribution
- GPU version should produce identical match rankings and scores as CPU version (bitwise or statistical equivalence on a validation set)

## Limitations

- GPU-powered version requires Linux operating system with NVIDIA CUDA-enabled GPU device; CPU-only mode available for Linux and OSX but without acceleration benefits
- Python version support limited to 3.6–3.9; Python 3.10 and newer not yet supported
- Approximate nearest neighbor indexing trades exhaustive search accuracy for speed; candidate set size is tunable but incomplete coverage of library may miss low-scoring true matches
- Open modification search assumes unmodified counterpart exists in the library; shifted dot product scoring depends on close spectral similarity between modified and unmodified forms

## Evidence

- [other] Convert spectra to feature hash vectors using a fixed-size hash table representation to reduce dimensionality while preserving similarity structure: "Convert spectra to feature hash vectors using a fixed-size hash table representation to reduce dimensionality while preserving similarity structure."
- [other] Accelerate the indexing and candidate retrieval using GPU computation: "Accelerate the indexing and candidate retrieval using GPU computation."
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra"
- [intro] Cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [readme] The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device"
- [other] Execute cascade search strategy starting with unmodified peptides, then open modification searches, applying strict false discovery rate control: "Execute cascade search strategy starting with unmodified peptides, then open modification searches, applying strict false discovery rate control."
