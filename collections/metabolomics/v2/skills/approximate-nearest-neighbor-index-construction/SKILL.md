---
name: approximate-nearest-neighbor-index-construction
description: Use when when you have a large collection of reference MS/MS spectra (spectral library) and need to search unknown query spectra against it rapidly, particularly for open modification searching where the modification mass is unknown and candidate space is large.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  - NumPy
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

# approximate-nearest-neighbor-index-construction

## Summary

Build a space-partitioning or hashing-based approximate nearest neighbor (ANN) index over preprocessed MS/MS spectral library data to enable fast retrieval of the K most similar candidate spectra for an unknown query spectrum. This skill accelerates open modification spectral library searching by avoiding exhaustive comparisons against all library spectra.

## When to use

When you have a large collection of reference MS/MS spectra (spectral library) and need to search unknown query spectra against it rapidly, particularly for open modification searching where the modification mass is unknown and candidate space is large. Use this skill when exhaustive pairwise scoring of all library spectra becomes a computational bottleneck and you can tolerate approximate rather than exact nearest neighbors.

## When NOT to use

- Library size is small (<1000 spectra) or computational budget is not a constraint—exhaustive search may be simpler and yield exact results.
- Query spectra have not been preprocessed to the same numerical representation as library spectra—vectorization must be uniform and deterministic.
- Exact nearest neighbor ranking is required and approximate candidates are unacceptable (e.g., regulatory contexts requiring complete auditability).

## Inputs

- Spectral library (collection of preprocessed MS/MS spectra in vectorized numerical form)
- Query spectrum (unknown MS/MS spectrum, preprocessed and vectorized identically to library)

## Outputs

- Ranked list of K candidate library spectra (indices or metadata) most similar to the query
- Similarity scores or distances from the ANN index

## How to apply

First, preprocess and vectorize all library spectra into a uniform numerical representation suitable for indexing—typically intensity vectors or spectral feature descriptors. Next, build an approximate nearest neighbor index over these vectorized library spectra using a space-partitioning algorithm (e.g., learned indices, locality-sensitive hashing) or Facebook's Faiss library. When a query spectrum arrives, preprocess it identically to the library spectra, then query the ANN index to retrieve the K most similar candidate library spectra ranked by index distance. The retrieved candidates are then passed to downstream scoring functions (e.g., shifted dot product for modified spectra) and cascade search to balance sensitivity and false discovery rate control. Key parameter: K (number of candidates retrieved) trades off recall against computational cost.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing ANN indexing and cascade search strategy for open modification searching; primary tool demonstrating this skill) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Facebook's library for efficient similarity search and clustering of dense vectors; underlying dependency for ANN index construction in ANN-SoLo) — https://github.com/facebookresearch/faiss
- **NumPy** (Required for spectral vectorization and numerical preprocessing prior to ANN index construction)

## Examples

```
pip install ann_solo; python -m ann_solo.main --library spectra.mgf --query query.mgf --ann_candidates 100
```

## Evaluation signals

- The constructed index successfully retrieves K candidate spectra for every query spectrum without runtime errors or out-of-memory failures.
- Retrieved candidates include the true matching spectrum (if one exists in the library) within the top K with high recall (e.g., >95% for K=100).
- Total search time (query + candidate retrieval) is substantially faster than exhaustive pairwise comparison against all library spectra (e.g., >10× speedup).
- Downstream cascade search on the candidate set achieves comparable sensitivity and false discovery rate control to exhaustive search, indicating K is sufficiently large.
- Index memory footprint and construction time are acceptable for the library size and available hardware (verify no crash or timeout during index build).

## Limitations

- ANN indexing trades exact nearest neighbor ranking for speed; some relevant spectra may be missed if K is too small or the index is poorly tuned.
- Index quality depends heavily on spectral vectorization; poor feature representation leads to poor candidate retrieval regardless of index algorithm.
- Python 3.6–3.9 required; Python 3.10+ not supported yet (as of README). GPU-powered indexing requires NVIDIA CUDA-enabled GPU and Linux.
- Vectorization and index construction must be deterministic and reproducible; any randomness in preprocessing can lead to inconsistent results across runs.
- Index cannot be easily updated; adding or removing library spectra typically requires full reconstruction rather than incremental updates.

## Evidence

- [other] Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features). Build an approximate nearest neighbor index over the library spectra using a space-partitioning or hashing-based algorithm. Query the ANN index with the unknown spectrum to retrieve a limited candidate set of the K most similar library spectra.: "Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features). 3. Build an approximate nearest neighbor index over the"
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [readme] The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support.: "The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support."
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet).: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)"
