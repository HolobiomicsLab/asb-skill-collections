---
name: hnsw-graph-construction-and-optimization
description: Use when when you have pre-computed Word2vec spectrum embeddings and need to perform fast approximate nearest-neighbor retrieval from a library of millions of spectra (e.g., NIST 2017, MassBank, or in-silico predicted spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - hnswlib
  - Python
  - gensim
  - Python 3.7
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41467-023-39279-7
  title: FastEI
evidence_spans:
- conda install -c conda-forge hnswlib
- Anaconda for Python 3.7
- conda install -c conda-forge gensim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fastei_cq
    doi: 10.1038/s41467-023-39279-7
    title: FastEI
  dedup_kept_from: coll_fastei_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39279-7
  all_source_dois:
  - 10.1038/s41467-023-39279-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HNSW Graph Construction and Optimization

## Summary

Build and optimize hierarchical navigable small world (HNSW) indices on spectrum embedding vectors to enable approximate nearest-neighbor search across million-scale molecular spectral libraries. This skill accelerates spectrum matching by trading small accuracy loss for sub-linear query time.

## When to use

When you have pre-computed Word2vec spectrum embeddings and need to perform fast approximate nearest-neighbor retrieval from a library of millions of spectra (e.g., NIST 2017, MassBank, or in-silico predicted spectra). Use this when latency and throughput are critical and exact matching is not required; typical trigger: library size > 100k spectra and query latency must be < seconds per spectrum.

## When NOT to use

- Input spectra are not yet embedded into a vector space — use Word2vec spectrum embedding first.
- Library size is small (< 10k spectra) — linear exact nearest-neighbor search or simple indexing is simpler and sufficient.
- You require guaranteed exact nearest-neighbor results with no approximation trade-off — use exhaustive search instead.

## Inputs

- Pre-computed spectrum embedding vectors (Word2vec format, typically .model file)
- Unique spectrum identifiers (mapping to spectra in reference database)
- Query spectrum embedding vector (same embedding space as reference vectors)
- k parameter (number of nearest neighbors to retrieve)

## Outputs

- HNSW index binary file (serialized graph structure, e.g., .bin format)
- Ranked list of k nearest-neighbor spectrum matches
- Similarity scores (cosine distance) for each match

## How to apply

Initialize an HNSW index using hnswlib with default M and ef parameters for navigable small world graph construction. Load all pre-computed spectrum embedding vectors (Word2vec-based, typically from gensim) and add them to the index with unique spectrum identifiers. For each query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra ranked by cosine distance. The index construction phase is one-time; subsequent queries use the pre-built graph for O(log N) approximate retrieval. Validate that retrieval speed scales sub-linearly with library size and that the top-k matches maintain acceptable spectrum matching accuracy (measured by molecular identification correctness on test spectra).

## Related tools

- **hnswlib** (HNSW index construction and approximate nearest-neighbor search engine; core library for building and querying the navigable small world graph on spectrum embeddings) — https://github.com/nmslib/hnswlib
- **gensim** (Pre-computes Word2vec spectrum embedding vectors that serve as input to HNSW indexing)
- **Python 3.7** (Programming environment for hnswlib API calls and index I/O)

## Examples

```
import hnswlib
import numpy as np
index = hnswlib.Index(space='cosine', dim=100)
index.init_index(max_elements=1000000, ef_construction=200, M=16)
index.add_items(spectrum_embeddings, spectrum_ids)
labels, distances = index.knn_query(query_embedding, k=10)
```

## Evaluation signals

- HNSW index size and memory footprint scale sub-linearly or linearly with library size (not quadratically).
- Query latency (per spectrum) remains in millisecond range even for million-scale libraries, confirming O(log N) graph traversal.
- Top-k retrieved spectra contain correct molecular identifications at expected frequency (e.g., ≥ 80% accuracy for rank-1 matches on test spectra).
- Index serialization/deserialization to disk is lossless: re-loaded index produces identical query results on validation queries.
- HNSW index retrieval outperforms exhaustive cosine-distance search by ≥ 10× on benchmarks while maintaining ≥ 95% of exact nearest-neighbor recall.

## Limitations

- HNSW is an approximate algorithm; rare queries may miss the true nearest neighbor if the graph structure causes early termination in search layers. Accuracy-speed trade-off is controlled by ef parameter.
- Index construction is CPU-intensive and must be done once offline; update or insertion of new spectra into a static index is non-trivial.
- FastEI installation and pre-built indices are currently Windows 64-bit only (tested on Windows 7, Windows 10), limiting portability.
- Performance depends heavily on quality of Word2vec embeddings; poor or uncalibrated embeddings will degrade retrieval quality.

## Evidence

- [other] Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). Add all spectrum embedding vectors to the HNSW index, assigning unique spectrum identifiers.: "Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). 3. Add all spectrum embedding vectors to the HNSW index, assigning"
- [other] FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while maintaining accuracy.: "FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while"
- [other] For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance).: "For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance)."
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph (HNSW): "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph"
- [readme] a million-molecule scale in-silico library has been builded and an ultra-fast and accurate search method has been developed (FastEI).: "a million-molecule scale in-silico library has been builded and an ultra-fast and accurate search method has been developed (FastEI)."
