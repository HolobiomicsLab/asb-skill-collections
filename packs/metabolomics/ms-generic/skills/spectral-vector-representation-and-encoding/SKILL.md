---
name: spectral-vector-representation-and-encoding
description: Use when when you have a set of mass spectra (query or library) that need to be searched against a large spectral reference database, and you want to use fast approximate nearest neighbor methods rather than exhaustive pairwise comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
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

# Spectral Vector Representation and Encoding

## Summary

Convert mass spectra into high-dimensional vector representations to enable fast similarity searching and indexing. This encoding step is foundational for approximate nearest neighbor indexing, allowing query spectra to be rapidly compared against large spectral libraries.

## When to use

When you have a set of mass spectra (query or library) that need to be searched against a large spectral reference database, and you want to use fast approximate nearest neighbor methods rather than exhaustive pairwise comparisons. Use this skill specifically when open modification searching requires rapid candidate selection from thousands to millions of library spectra.

## When NOT to use

- When the spectral library is small (< 1000 spectra) and exhaustive pairwise comparison is faster than index construction and lookup.
- When exact nearest neighbors are required and approximation errors are unacceptable for your downstream validation.
- When spectra have already been pre-filtered by other orthogonal methods (e.g., parent mass filtering) and the candidate pool is already tractable.

## Inputs

- mass spectra in high-dimensional vector form (m/z and intensity pairs)
- spectral library dataset with multiple spectra
- query spectrum or batch of query spectra

## Outputs

- encoded spectral vectors (high-dimensional numeric arrays)
- approximate nearest neighbor index structure
- ranked list of top-k candidate library spectra with similarity scores

## How to apply

Represent each mass spectrum as a high-dimensional vector by extracting intensity values at m/z positions or using feature-based encoding. Build or load a spatial data structure (e.g., Faiss-based approximate nearest neighbor index) on the encoded library spectra vectors. For each query spectrum, convert it to the same vector representation and execute a nearest neighbor search against the index to retrieve the top-k most similar library spectra candidates ranked by relevance. The vector representation must be consistent between library and query spectra to ensure valid distance computations in the encoded space.

## Related tools

- **ANN-SoLo** (Spectral library search engine that implements approximate nearest neighbor indexing on encoded spectra vectors for fast open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing the approximate nearest neighbor index data structures and GPU-accelerated similarity search algorithms used by ANN-SoLo) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; python -m ann_solo --library_file spectral_library.mgf --query_file query_spectra.mgf --output results.tsv
```

## Evaluation signals

- Query spectrum vectors have the same dimensionality as library spectrum vectors; dimension mismatch indicates encoding inconsistency.
- Nearest neighbor search returns results ranked by increasing distance/decreasing cosine similarity, with top candidates having scores above a relevance threshold (e.g., cosine > 0.7 for spectral matching).
- Index construction completes without memory errors and permits O(log n) or sublinear query time rather than O(n) exhaustive search.
- Cascade search strategy correctly identifies both unmodified and modified spectra by comparing query to top-k candidates while controlling false discovery rate.
- Shifted dot product score between query spectrum and candidate library spectra is computed accurately for mass shift detection.

## Limitations

- Vector encoding loses some spectral detail; rare or weak peaks may not be adequately represented, reducing sensitivity for low-abundance modified peptides.
- Approximate nearest neighbor methods trade exact correctness for speed; the top-k candidates returned may not include the true best match if the approximation threshold is too loose.
- Python 3.6–3.9 only; Python 3.10+ not yet supported. GPU-accelerated version requires NVIDIA CUDA-enabled hardware and Linux; CPU-only version supports Linux and OSX.
- Faiss installation depends on specific GPU version; installation failures are common if CUDA toolkit version does not match GPU driver and Faiss build.

## Evidence

- [other] Approximate nearest neighbor indexing operates by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "Load or construct a spectral library dataset with multiple spectra represented as high-dimensional vectors. 2. Build an approximate nearest neighbor index (e.g., using a spatial data structure or"
- [readme] Vector representation and indexing enable cascade search strategy: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] Spectral library search engine definition: "**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine for fast and accurate open modification searching."
- [readme] Installation dependencies for vector encoding infrastructure: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device,"
- [readme] Faiss dependency for vector indexing: "The **Faiss** installation depends on a specific GPU version. Please refer to the [Faiss installation instructions](https://github.com/facebookresearch/faiss/blob/master/INSTALL.md) for more"
