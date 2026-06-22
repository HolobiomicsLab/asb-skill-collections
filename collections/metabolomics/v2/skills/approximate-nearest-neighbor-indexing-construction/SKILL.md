---
name: approximate-nearest-neighbor-indexing-construction
description: Use when when you have a large spectral library (hundreds of thousands to millions of spectra) and need to perform open modification searching on query spectra where exhaustive comparison against all library entries is computationally prohibitive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Approximate Nearest Neighbor Indexing Construction

## Summary

Build a spatial index structure on high-dimensional spectral library vectors to enable fast retrieval of the top-k most similar candidate spectra for a query spectrum, thereby accelerating open modification spectral library searching while maintaining sensitivity. This skill reduces computational overhead by pre-indexing library spectra so only relevant candidates are compared during cascade search.

## When to use

When you have a large spectral library (hundreds of thousands to millions of spectra) and need to perform open modification searching on query spectra where exhaustive comparison against all library entries is computationally prohibitive. Use this skill when query-to-library search latency is a bottleneck and you can tolerate approximate neighbor retrieval in exchange for speed.

## When NOT to use

- When your spectral library is small (< 10,000 spectra) and brute-force comparison is already fast enough; indexing overhead will outweigh benefits.
- When exact nearest neighbor results are required and approximate retrieval errors cannot be tolerated (e.g., regulatory or validation contexts where all candidates must be exhaustively ranked).
- When query spectra are already low-dimensional or pre-filtered to a small subset of library candidates; the indexing step would be redundant.

## Inputs

- Spectral library dataset with multiple spectra
- High-dimensional vector representations of library spectra (e.g., peak intensities, normalized intensity vectors)
- Query spectrum as a vector

## Outputs

- Approximate nearest neighbor index structure (spatial or LSH-based)
- Top-k ranked candidate library spectra for each query spectrum
- Relevance scores (similarity metrics) for retrieved candidates

## How to apply

Load the spectral library dataset and represent each spectrum as a high-dimensional vector (e.g., normalized peak intensity vectors). Construct an approximate nearest neighbor index using a spatial data structure or locality-sensitive hashing (LSH) method—the ANN-SoLo implementation uses Faiss, which supports GPU acceleration. For each query spectrum, execute a nearest neighbor search against the index to retrieve the top-k most similar library spectrum candidates ranked by vector similarity. The selected candidates are then passed to a cascade search strategy that performs detailed scoring (e.g., shifted dot product) to maximize identifications while controlling false discovery rate. The index construction is a one-time preprocessing step; the retrieval is executed per query.

## Related tools

- **ANN-SoLo** (Spectral library search engine that implements approximate nearest neighbor indexing using Faiss to retrieve top-k candidate spectra for cascade search and open modification identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying vector search library that builds and manages the approximate nearest neighbor index structure; supports both CPU and GPU-accelerated retrieval) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; python -c "from ann_solo import spectral_library; lib = spectral_library.SpectralLibrary('library.mgf'); lib.build_index(); matches = lib.query(query_spectrum, k=10)"
```

## Evaluation signals

- Index construction completes without errors and the index size is reasonable relative to library size (typically proportional to the number of spectra and vector dimensionality).
- For a set of test query spectra, verify that the top-k retrieved candidates show high vector similarity (cosine similarity, dot product, or Faiss distance metric) to the query; spot-check that known matches appear in the top-k set.
- End-to-end cascade search on indexed library produces the same or higher number of identified spectra (modified and unmodified) compared to exhaustive search, with false discovery rate controlled below a specified threshold (e.g., 1%).
- Query retrieval latency is substantially lower than brute-force search (e.g., 10–100× speedup on large libraries); measure wall-clock time for a batch of queries.
- The shifted dot product scores of cascade-matched spectra align with expected distributions; visual inspection of top-k matches confirms they represent plausible biological or instrumental variants.

## Limitations

- Approximate nearest neighbor retrieval may miss some true neighbors at the boundary of the top-k set, potentially reducing sensitivity for spectra with weaker similarity to the library.
- Index memory footprint scales with library size and vector dimensionality; GPU versions require NVIDIA CUDA-capable hardware and are restricted to Linux; CPU-only versions support Linux and macOS.
- The choice of k (number of candidates) is a hyperparameter that affects both speed and sensitivity; too small a k may miss relevant candidates, while too large a k reduces speedup.
- Index construction requires all library spectra to be vectorized consistently; heterogeneous or missing peak data must be preprocessed before indexing.
- ANN-SoLo currently requires Python 3.6–3.9; Python 3.10 and newer are not yet supported.

## Evidence

- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [other] Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval.: "Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval"
- [intro] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score.: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [readme] The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support.: "The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support."
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet).: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)."
