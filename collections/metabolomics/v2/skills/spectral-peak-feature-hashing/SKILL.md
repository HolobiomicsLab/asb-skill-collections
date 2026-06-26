---
name: spectral-peak-feature-hashing
description: Use when when you have a large collection of query high-resolution mass
  spectra that must be rapidly matched against a spectral library containing modified
  and unmodified peptides, and you need to reduce computational overhead before approximate
  nearest neighbor indexing or GPU-accelerated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  - NumPy
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is
  a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary)
  is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
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

# spectral-peak-feature-hashing

## Summary

Feature hashing converts high-resolution mass spectra peaks into fixed-size, deterministic vector representations suitable for fast approximate nearest neighbor indexing and GPU acceleration. This enables rapid open modification spectral library searching by reducing dimensionality while preserving spectral similarity.

## When to use

When you have a large collection of query high-resolution mass spectra that must be rapidly matched against a spectral library containing modified and unmodified peptides, and you need to reduce computational overhead before approximate nearest neighbor indexing or GPU-accelerated similarity search. Apply this skill specifically when open modification searching (searching without pre-specifying which modifications are allowed) requires sub-second query latency.

## When NOT to use

- Input spectra are already low-resolution or have very few peaks (feature hashing requires sufficient peak density for effective dimensionality reduction).
- The CPU-only version is required and you are using Python 3.10 or newer (ANN-SoLo currently supports only Python 3.6–3.9).
- You are searching against a small spectral library where cascade filtering provides negligible speedup over full dot product scoring.

## Inputs

- high-resolution mass spectra (m/z and intensity peak pairs)
- spectral library (reference spectra with known peptide assignments)
- query mass spectra (unidentified spectra to search)
- GPU device (NVIDIA CUDA-enabled for GPU version)

## Outputs

- fixed-size feature hash vectors per spectrum
- approximate nearest neighbor index (GPU-resident)
- ranked candidate spectra with shifted dot product scores
- filtered identifications with false discovery rate control

## How to apply

Compute a deterministic hashing function that maps individual spectrum peaks (m/z and intensity pairs) into fixed-size feature vectors. Load query spectra and spectral library data into memory-aligned structures suitable for GPU processing. Transfer the feature-hashed vectors to GPU memory and build approximate nearest neighbor indexes using locality-sensitive hashing or similar GPU-accelerated indexing methods (via Faiss). Execute a cascade search strategy: retrieve top-k candidate spectra from the ANN index, then compute full-precision shifted dot product scores for rescoring, and filter results by false discovery rate threshold. Measure query latency (milliseconds per spectrum) and identification accuracy (sensitivity/specificity) to validate speedup against CPU baseline.

## Related tools

- **ANN-SoLo** (spectral library search engine that implements cascade search combining feature hashing, approximate nearest neighbor indexing, and shifted dot product scoring with FDR control) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (GPU-accelerated approximate nearest neighbor indexing backend (locality-sensitive hashing and other ANN methods)) — https://github.com/facebookresearch/faiss
- **NumPy** (required dependency for numerical operations on feature vectors)

## Examples

```
pip install ann_solo; python -c "from ann_solo import ann_solo; ann_solo.main(['spectrum_query.mgf', '--library', 'reference_library.mgf', '--gpu'])" # GPU-accelerated feature-hashed search with cascade scoring and FDR control
```

## Evaluation signals

- Feature vectors are fixed-size and deterministic: identical spectra always produce identical hash vectors.
- Query latency per spectrum is measured in milliseconds and shows documented speedup factor compared to CPU baseline.
- Identification sensitivity and specificity are maintained at or above levels achieved by full dot product scoring (cascade search does not sacrifice accuracy).
- GPU memory utilization and throughput (spectra per second) meet or exceed documented performance benchmarks in the 2019 follow-up work.
- False discovery rate is strictly controlled at specified threshold across all identified unmodified and modified spectra.

## Limitations

- Feature hashing with fixed-size vectors can cause collisions, potentially reducing spectral discrimination quality; cascade search with full-precision dot product rescoring mitigates but does not eliminate this loss.
- GPU version requires NVIDIA CUDA-enabled GPU on Linux; CPU-only version supports Linux and OSX but has lower throughput.
- Python version support is limited to 3.6–3.9; Python 3.10 and newer are not yet supported.
- Memory alignment and transfer overhead for GPU processing may not justify speedup for very small query sets (<1000 spectra).
- Performance gains depend on spectral library size; benefit is maximal when library contains thousands to millions of reference spectra where ANN filtering provides largest relative speedup.

## Evidence

- [other] feature hashing representation combined with GPU-based computation enable extremely fast and accurate open modification spectral library searching: "feature hashing representation combined with GPU-based computation enable extremely fast and accurate open modification spectral library searching of high-resolution mass spectra"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] cascade search strategy combined with approximate nearest neighbor indexing to maximize identified unmodified and modified spectra while strictly controlling false discovery rate and shifted dot product score: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [other] Compute feature hash representations of all spectra using deterministic hashing function to map peaks into fixed-size feature vectors: "Compute feature hash representations of all spectra using a deterministic hashing function to map peaks into fixed-size feature vectors"
- [other] Transfer feature-hashed vectors to GPU memory and build approximate nearest neighbor indexes using locality-sensitive hashing or similar GPU-accelerated indexing: "Transfer feature-hashed vectors to GPU memory and build approximate nearest neighbor (ANN) indexes using locality-sensitive hashing or similar GPU-accelerated indexing"
- [readme] The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device"
- [readme] ANN-SoLo requires Python 3.6 to 3.9; Python 3.10 and newer are currently not supported yet: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)"
