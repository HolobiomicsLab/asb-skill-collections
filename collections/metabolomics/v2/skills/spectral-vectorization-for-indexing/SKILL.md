---
name: spectral-vectorization-for-indexing
description: Use when when you have a collection of MS/MS reference spectra and unknown
  query spectra that must be rapidly matched against a large spectral library, and
  you need to enable approximate nearest neighbor indexing to reduce computational
  cost from exhaustive pairwise comparison to K-nearest neighbor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - LC-MS
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

# spectral-vectorization-for-indexing

## Summary

Convert mass spectrometry spectra into numerical vector representations suitable for approximate nearest neighbor indexing and rapid similarity search. This vectorization step bridges raw spectral data and efficient ANN-based library candidate selection in open modification searching.

## When to use

When you have a collection of MS/MS reference spectra and unknown query spectra that must be rapidly matched against a large spectral library, and you need to enable approximate nearest neighbor indexing to reduce computational cost from exhaustive pairwise comparison to K-nearest neighbor retrieval.

## When NOT to use

- Input spectra are already vectorized and indexed in a Faiss or Annoy data structure — skip directly to querying.
- Library size is small (<1000 spectra) such that exhaustive pairwise scoring is already fast enough; ANN indexing adds unnecessary overhead.
- Spectral data lacks intensity or peak position information required for meaningful vector representation.

## Inputs

- MS/MS reference spectral library (collection of preprocessed peak lists with m/z and intensity values)
- Unknown query spectrum (peak list with m/z and intensity values)

## Outputs

- Vectorized spectral library suitable for ANN indexing
- Ranked set of K most similar library spectrum candidates for the query

## How to apply

Load the spectral library and query spectrum into memory and preprocess each spectrum into a numerical representation (e.g., intensity vectors or spectral features) suitable for distance-based indexing. The vectorization must preserve intensity information and peak positions in a form that Faiss or similar ANN libraries can index efficiently. Build an approximate nearest neighbor index over the preprocessed library spectra using space-partitioning or hashing-based algorithms. Query the index with the vectorized unknown spectrum to retrieve a limited candidate set of K most similar library spectra ranked by index distance. Return the ranked candidate spectra for downstream cascade search scoring. The rationale is that precomputed ANN indexing avoids full O(n) library comparison while preserving sensitivity to modified peptide spectra through the shifted dot product score applied in cascade search.

## Related tools

- **ANN-SoLo** (Spectral library search engine that performs vectorization and ANN indexing for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing approximate nearest neighbor indexing algorithms and GPU acceleration) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --library reference_spectra.mgf --query unknown_spectrum.mgf --candidates 50 --output candidates.tsv
```

## Evaluation signals

- Vectorized spectra are in a dense numerical format (numpy arrays or Faiss-compatible tensors) with dimensionality and range suitable for distance metrics (e.g., cosine similarity, L2 distance).
- ANN index successfully queries and returns K candidates in sublinear time (log or constant-factor speedup relative to library size).
- Retrieved candidate spectra include true matches (unmodified or modified versions of query) in the top-K results, verified by cascade search scoring.
- Vectorization preserves peptide modification information: shifted dot product scores in cascade search discriminate between modified and unmodified library spectra.
- False discovery rate and unmodified/modified spectrum identification counts remain within expected ranges when cascade search is applied post-retrieval.

## Limitations

- ANN indexing trades exact nearest neighbors for approximate ones; some true matches may fall outside top-K if K is set too low relative to library diversity.
- Vectorization quality depends on preprocessing choices (e.g., peak normalization, m/z binning); poor preprocessing can degrade ranking.
- GPU-accelerated Faiss requires NVIDIA CUDA-enabled hardware and specific GPU driver versions; CPU-only mode is slower.
- Python version support is limited to 3.6–3.9; Python 3.10+ not currently supported as of the README.
- Vector dimensionality and memory footprint scale with spectral resolution and preprocessing choices; very large libraries may require careful tuning of index parameters (e.g., number of Voronoi cells, number of probe dimensions).

## Evidence

- [other] Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features).: "Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features)."
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [other] Build an approximate nearest neighbor index over the library spectra using a space-partitioning or hashing-based algorithm.: "Build an approximate nearest neighbor index over the library spectra using a space-partitioning or hashing-based algorithm."
- [readme] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
