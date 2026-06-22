---
name: nearest-neighbor-candidate-retrieval
description: Use when when you have a large spectral library (thousands to millions of spectra represented as high-dimensional vectors) and need to search unknown query spectra against it, particularly under open modification search scenarios where all possible mass shifts must be considered.
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

# nearest-neighbor-candidate-retrieval

## Summary

Use approximate nearest neighbor (ANN) indexing to rapidly select a limited subset of the most relevant library spectra from a large spectral database for comparison against a query spectrum. This reduces computational cost in open modification spectral matching while preserving sensitivity through cascade search strategies.

## When to use

When you have a large spectral library (thousands to millions of spectra represented as high-dimensional vectors) and need to search unknown query spectra against it, particularly under open modification search scenarios where all possible mass shifts must be considered. Use this skill when brute-force comparison of all library spectra is computationally prohibitive.

## When NOT to use

- Input library is very small (< 1000 spectra): brute-force search is already fast; ANN indexing overhead may not justify the added complexity.
- Query spectra have no vector representation or are highly sparse: ANN methods assume dense, high-dimensional vectors; sparse or poorly characterized queries may yield unreliable neighbors.
- Exhaustive or all-hits search is required: if every possible match (no matter how low-similarity) must be inspected, ANN candidate filtering is inappropriate.

## Inputs

- spectral library dataset (collection of mass spectra as high-dimensional vectors, typically m/z and intensity pairs)
- query spectrum (unknown mass spectrum to search, represented as a high-dimensional vector)
- top-k parameter (number of candidate spectra to retrieve per query)

## Outputs

- ranked list of top-k library spectrum candidates (spectra most similar to the query by ANN distance metric)
- relevance scores (distances or similarity metrics from the index)
- candidate spectra metadata (spectrum identifiers, precursor m/z, peptide sequences if available)

## How to apply

Load or construct a spectral library dataset where each spectrum is represented as a high-dimensional vector. Build an approximate nearest neighbor index (e.g., using Faiss with an LSH-based or learned quantization method) on these library vectors to enable fast neighbor retrieval without examining all spectra. For each query spectrum, execute a nearest neighbor search against the index to retrieve the top-k most similar library spectra candidates ranked by relevance. Pass these ranked candidates to downstream cascade search steps that apply stringent scoring (e.g., shifted dot product) and false discovery rate control. The rationale is that true matching spectra tend to cluster near the query in the vector space, so limiting comparison to top-k candidates dramatically accelerates search while a cascade strategy recovers sensitivity by filtering hits with FDR-aware thresholds.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing approximate nearest neighbor indexing for open modification searching; orchestrates ANN candidate retrieval followed by cascade search with FDR and shifted dot product scoring) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing approximate nearest neighbor index construction and fast neighbor search (CPU and GPU implementations)) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; python -m ann_solo search --library library.mgf --query query.mgf --candidates 100 --output results.tsv
```

## Evaluation signals

- Verify that top-k candidates include the correct matching spectrum (if ground truth is available) with a high rank position (e.g., rank ≤ 100 for typical library sizes).
- Confirm that the returned candidate list is sorted by relevance (distance or similarity scores in monotonic order).
- Check that the number of candidates returned equals the requested top-k value (or fewer only at library boundaries).
- Validate that cascade search applied to ANN candidates recovers true-positive identifications at the same or comparable sensitivity as exhaustive search, while false discovery rate remains ≤ specified threshold (typically 1%).
- Measure speedup: wall-clock time for ANN-based search should be orders of magnitude faster than exhaustive comparison for large libraries (e.g., >10× on millions of spectra).

## Limitations

- ANN methods are approximate: neighbors are not guaranteed to be exact; low-similarity spectra near the boundary of the top-k cutoff may occasionally be missed. This is mitigated by cascade search and FDR control applied downstream.
- Index construction and memory overhead: building and storing the ANN index requires upfront computation and disk/RAM space proportional to library size; for very large libraries (>100M spectra) this can be substantial.
- Performance depends on vector quality: if spectra are represented as poorly normalized or uninformative vectors, ANN will retrieve irrelevant candidates. Vector representation choices (e.g., peak binning, intensity scaling, window-based encoding) directly affect retrieval quality.
- Hyperparameter sensitivity: the choice of top-k, ANN index type (LSH, product quantization, etc.), and index parameters (e.g., number of hash functions, codebook size) influences both speed and accuracy; tuning is often necessary for new datasets.
- GPU-accelerated version requires NVIDIA CUDA-capable hardware on Linux; CPU-only version supports Linux and OSX but is slower (Faiss dependency).

## Evidence

- [other] Approximate nearest neighbor indexing operates by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum, thereby speeding up open modification searching.: "Approximate nearest neighbor indexing operates by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum, thereby speeding up open modification"
- [other] Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval.: "Build an approximate nearest neighbor index (e.g., using a spatial data structure or LSH-based method) on the library spectra vectors to enable fast neighbor retrieval."
- [other] For each query spectrum, execute a nearest neighbor search against the index to retrieve the top-k most similar library spectra candidates.: "For each query spectrum, execute a nearest neighbor search against the index to retrieve the top-k most similar library spectra candidates."
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum. This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support.: "The Faiss installation depends on a specific GPU version. Please refer to the Faiss installation instructions for more information on OS and GPU support."
