---
name: approximate-nearest-neighbor-search
description: Use when when you have pre-computed spectrum embeddings (e.g., Word2vec vectors) and need to rapidly retrieve the most similar spectra from a large in-silico or experimental library (thousands to millions of spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - hnswlib
  - Python
  - gensim
  - Python 3.7
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
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# approximate-nearest-neighbor-search

## Summary

Build and query a hierarchical navigable small world (HNSW) graph index over spectrum embedding vectors to retrieve the k most similar candidate spectra from million-scale libraries in sub-second time. This skill accelerates spectrum matching by trading exact nearest-neighbor search for fast approximate retrieval with maintained accuracy.

## When to use

When you have pre-computed spectrum embeddings (e.g., Word2vec vectors) and need to rapidly retrieve the most similar spectra from a large in-silico or experimental library (thousands to millions of spectra). Typical trigger: query spectrum matching against NIST 2017, MassBank, or custom in-silico libraries where latency and throughput are critical for molecular identification.

## When NOT to use

- When you need guaranteed exact nearest-neighbor search; HNSW is approximate and may miss the true closest neighbor due to graph construction randomness and ef parameter settings.
- When spectrum embeddings have not been pre-computed; this skill assumes Word2vec or equivalent dense vector representation is already available.
- When the library size is very small (< 1000 spectra); exact brute-force search may be faster and simpler than index construction overhead.

## Inputs

- Pre-computed spectrum embedding vectors (Word2vec-based, numpy array or list of float vectors)
- Unique spectrum identifiers (integer or string)
- Query spectrum embedding vector (single float vector, same dimensionality as index vectors)
- Number of nearest neighbors k (integer, typically 1–100)

## Outputs

- Ranked list of k nearest-neighbor spectrum matches
- Similarity scores for each match (cosine distance or similarity metric)
- Spectrum identifiers corresponding to retrieved matches

## How to apply

Initialize an HNSW index using hnswlib with default M and ef parameters for navigable small world graph construction. Add all pre-computed spectrum embedding vectors to the index, assigning unique spectrum identifiers (e.g., compound IDs or accession numbers). For a given query spectrum embedding, invoke approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra, ranked by cosine distance. Return the ranked list with similarity scores. The HNSW algorithm trades exact distance computation for O(log n) approximate search complexity, maintaining high recall while achieving million-scale search in milliseconds.

## Related tools

- **hnswlib** (Core library for constructing and querying HNSW graph indices on spectrum embeddings; implements approximate nearest-neighbor search with configurable M and ef parameters.) — https://github.com/nmslib/hnswlib
- **gensim** (Pre-training and persistence of Word2vec spectrum embedding models (references_word2vec.model); provides the dense vector representations indexed by HNSW.) — https://github.com/RaRe-Technologies/gensim
- **Python 3.7** (Runtime environment for hnswlib and gensim integration; required for HNSW index I/O and query execution.)

## Examples

```
import hnswlib; idx = hnswlib.Index(space='cosine', dim=300); idx.init_index(max_elements=1000000, ef_construction=200, M=16); idx.add_items(embeddings, ids); labels, distances = idx.knn_query(query_embedding, k=10)
```

## Evaluation signals

- HNSW index initializes without error and index file size is proportional to number of vectors and embedding dimensionality.
- Query retrieval latency is < 100 ms for k=10 queries against million-scale index (validate via timing measurements).
- Returned k matches have cosine distances monotonically increasing or similarity scores monotonically decreasing from rank 1 to k.
- Recall against brute-force exact nearest-neighbor search is ≥ 0.95 for ef parameter tuned to data; compare top-10 matches between HNSW and exhaustive search.
- Spectrum identifiers in returned matches are valid entries in the original database (uniqueness and range check).

## Limitations

- HNSW is approximate: recall depends on M (graph connectivity) and ef (search extent) parameters; small M or ef may miss true nearest neighbors.
- Index construction and search assume Euclidean or cosine distance; other dissimilarity metrics require custom distance functions or re-embedding.
- Graph construction is stochastic; exact ranking of candidates may vary across multiple index builds on the same data unless random seed is fixed.
- Index must fit in memory; billion-scale spectrum libraries may require sharding or approximate vector quantization (not addressed in FastEI).
- Platform support: Windows 64-bit (7, 10) tested; cross-platform compatibility and GPU acceleration not documented.

## Evidence

- [other] Load pre-computed spectrum embedding vectors (Word2vec-based embeddings) from input file. 2. Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). 3. Add all spectrum embedding vectors to the HNSW index, assigning unique spectrum identifiers.: "Load pre-computed spectrum embedding vectors (Word2vec-based embeddings) from input file. 2. Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small"
- [other] For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance). 5. Return ranked list of nearest-neighbor matches with their similarity scores.: "For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance). 5. Return ranked list"
- [other] FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while maintaining accuracy.: "FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while"
- [readme] How to rapidly search an *in-silico* library of millions or even tens of millions of spectra while ensuring the accuracy of molecular identification is a new challenge.: "How to rapidly search an *in-silico* library of millions or even tens of millions of spectra while ensuring the accuracy of molecular identification is a new challenge."
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph (HNSW): "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph"
