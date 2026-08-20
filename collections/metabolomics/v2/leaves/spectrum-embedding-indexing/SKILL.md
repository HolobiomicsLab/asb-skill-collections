---
name: spectrum-embedding-indexing
description: Use when you have pre-computed Word2vec embeddings of mass spectra and
  need to retrieve the k most similar spectra from a library of hundreds of thousands
  to millions of candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3473
  tools:
  - hnswlib
  - Python
  - gensim
  - rdkit
  techniques:
  - mass-spectrometry
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-embedding-indexing

## Summary

Build and query HNSW approximate nearest-neighbor indices over Word2vec-embedded mass spectra to enable rapid similarity-based retrieval from million-scale molecular libraries while maintaining matching accuracy. This skill accelerates spectrum matching workflows by replacing exhaustive similarity computation with hierarchical graph-based indexing.

## When to use

Use this skill when you have pre-computed Word2vec embeddings of mass spectra and need to retrieve the k most similar spectra from a library of hundreds of thousands to millions of candidates. It is appropriate when approximate nearest-neighbor search is acceptable (vs. exact search) and speed is a priority—typical in high-throughput metabolomics identification against in-silico libraries like the FastEI million-molecule library.

## When NOT to use

- Input spectra have not been embedded with Word2vec or compatible dense embedding; HNSW requires fixed-dimensional dense vectors, not sparse representations or raw m/z-intensity pairs.
- Library size is small (<10,000 spectra) or latency is not a bottleneck; exhaustive cosine similarity search is simpler and eliminates approximation error.
- Exact nearest neighbors are required and approximation error is unacceptable; HNSW is an approximate method and may miss the true global nearest neighbor due to the greedy graph traversal.

## Inputs

- Pre-computed Word2vec spectrum embedding vectors (float arrays, typically 100–300 dimensions)
- Spectrum metadata lookup table (spectrum ID → molecule ID, precursor m/z, adduct, etc.)
- Query spectrum embedding vector (single or batch of vectors in same embedding space)

## Outputs

- HNSW index object (serialized .bin file or in-memory graph)
- Ranked list of k nearest-neighbor spectrum candidates with cosine similarity scores
- Mapping of returned spectrum IDs to molecular structures and library metadata

## How to apply

Load pre-computed Word2vec spectrum embedding vectors from disk (typically .model files or serialized arrays). Initialize an HNSW index using hnswlib with standard parameters (default M and ef settings for navigable small world graph construction). Add all spectrum embeddings to the index sequentially, assigning unique spectrum identifiers that link back to metadata (molecule ID, precursor m/z, etc.). For a query spectrum embedding, call the HNSW index's approximate nearest-neighbor search method to retrieve the k candidate spectra ranked by cosine distance. The HNSW graph trades off small approximation error for orders-of-magnitude speedup over brute-force cosine similarity computation, which is critical at million-molecule scale. Return the ranked list with similarity scores for downstream scoring and filtering steps.

## Related tools

- **hnswlib** (Builds and queries the hierarchical navigable small world graph for approximate nearest-neighbor search on spectrum embeddings)
- **gensim** (Trains and loads Word2vec embedding models used to vectorize spectrum data before indexing)
- **rdkit** (Processes molecular structures associated with spectra in the library metadata)

## Examples

```
import hnswlib
index = hnswlib.Index(space='cosine', dim=300)
index.add_items(spectrum_embeddings, ids=spectrum_ids)
k_neighbors = index.knn_query(query_embedding, k=100)[0][0]
```

## Evaluation signals

- HNSW index file size and structure: confirm .bin file is created and contains expected spectrum count (no missing or duplicate IDs)
- Query latency: verify sub-second retrieval time for k=10–100 candidates from a million-scale library (vs. seconds for brute-force search)
- Rank preservation: spot-check that returned candidates have monotonically decreasing cosine similarity scores
- Recall at k: if ground truth similar spectra are available, verify that approximate HNSW neighbors overlap substantially (typically >95%) with exact nearest neighbors computed via brute-force
- Index load/query consistency: re-load persisted HNSW index and confirm identical candidate rankings and scores for same query vector

## Limitations

- HNSW is an approximate method; the retrieved k nearest neighbors may not be the true global k nearest neighbors, especially for distant or ambiguous query spectra.
- Index construction is one-time cost but cannot be incrementally updated; adding new spectra requires full index rebuild.
- Performance depends on HNSW hyperparameters (M and ef) which are set to defaults in FastEI; tuning may be needed for specific datasets or latency/accuracy trade-offs.
- Installation and deployment currently limited to Windows 64-bit systems as noted in the FastEI README; cross-platform support not documented.

## Evidence

- [other] FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while maintaining accuracy.: "HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries"
- [other] Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). Add all spectrum embedding vectors to the HNSW index, assigning unique spectrum identifiers.: "Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). Add all spectrum embedding vectors to the HNSW index, assigning unique"
- [other] For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance).: "perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance)"
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph: "improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph (HNSW)"
- [readme] a million-molecule scale *in-silico* library has been builded and an ultra-fast and accurate search method has been developed (FastEI).: "a million-molecule scale *in-silico* library has been builded and an ultra-fast and accurate search method has been developed (FastEI)"
