---
name: high-dimensional-similarity-search-optimization
description: Use when when you have a large spectral library (thousands to millions of spectra) represented as high-dimensional vectors and need to match unknown query spectra against it, but exhaustive pairwise comparison is computationally prohibitive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
---

# High-Dimensional Similarity Search Optimization

## Summary

Optimize search speed in high-dimensional spectral spaces by building approximate nearest neighbor indexes that retrieve only the most relevant library spectra candidates, enabling fast open modification searching without exhaustive comparisons. This approach trades theoretical exhaustiveness for practical speed while maintaining sensitivity and specificity through cascade search validation.

## When to use

When you have a large spectral library (thousands to millions of spectra) represented as high-dimensional vectors and need to match unknown query spectra against it, but exhaustive pairwise comparison is computationally prohibitive. Particularly valuable for open modification searching where the search space is large and false discovery rate control is required.

## When NOT to use

- When the spectral library is small enough (<1000 spectra) that exhaustive search is already fast enough
- When you need guaranteed optimal (exact nearest neighbor) results rather than approximate results, and accuracy loss is unacceptable
- When query spectra are already pre-filtered to a manageable candidate set through orthogonal methods

## Inputs

- Spectral library dataset with multiple spectra represented as high-dimensional vectors
- Query spectrum (unknown spectrum to be identified)
- Spectral library in standard format (e.g., MGF, mzML, or library-specific index)

## Outputs

- Ranked list of top-k candidate library spectra most similar to query spectrum
- Approximate nearest neighbor index structure enabling fast retrieval
- Validated matches with false discovery rate controlled scores

## How to apply

Build an approximate nearest neighbor index (e.g., using spatial data structures or locality-sensitive hashing) on the spectral library vectors to enable fast neighbor retrieval in sublinear time. For each query spectrum, execute a nearest neighbor search against the index to retrieve the top-k most similar library spectra candidates ranked by relevance. Combine this candidate selection with a cascade search strategy that validates candidates using shifted dot product scoring to maximize identifications while controlling false discovery rate. The rationale is that most relevant matches are concentrated in the k-nearest neighbors, so filtering to this subset before expensive scoring operations yields orders-of-magnitude speedup with minimal sensitivity loss.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing approximate nearest neighbor indexing with cascade search and false discovery rate control for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing approximate nearest neighbor indexing implementation (spatial data structures and similarity search)) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo
```

## Evaluation signals

- Verify index was successfully built and can retrieve candidates in sublinear time (significantly faster than brute-force search)
- Confirm that top-k candidates include true matches ranked by similarity score (audit a sample of query-candidate pairs)
- Validate that cascade search validation produces false discovery rate ≤ target threshold (typically 1% or 5% as specified)
- Check that sensitivity (fraction of true modifications identified) is maintained near exhaustive search levels despite the filtering
- Confirm shifted dot product scores correctly rank unmodified and modified spectrum matches for same peptide

## Limitations

- Approximate nearest neighbor methods trade exhaustiveness for speed — a true match might not be in the top-k candidates if it does not rank among the most similar in high-dimensional space
- Performance depends on the choice of k (number of candidates) and index parameters; setting k too low reduces sensitivity, too high reduces speedup
- GPU-powered version requires NVIDIA CUDA-enabled device on Linux; CPU-only version supports Linux and OSX but is slower
- Python version support is limited to 3.6–3.9; Python 3.10+ not yet supported
- Effectiveness depends on spectral representation quality; poor vector representations or mismatched preprocessing between library and query spectra degrade matching

## Evidence

- [other] Approximate nearest neighbor indexing operates by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum, thereby speeding up open modification searching.: "Approximate nearest neighbor indexing operates by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum, thereby speeding up open modification"
- [other] Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval.: "Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval."
- [other] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device"
- [readme] The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information.: "The Faiss installation depends on a specific GPU version."
