---
name: spectral-library-similarity-matching
description: Use when you have an unknown experimental mass spectrum (e.g., from liquid chromatography–mass spectrometry) and need to retrieve the most structurally similar candidate molecules from a database of millions of predicted or experimental spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - hnswlib
  - Python
  - gensim
  - rdkit
  - FastEI
  techniques:
  - LC-MS
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

# spectral-library-similarity-matching

## Summary

Rapidly identify unknown mass spectra by matching them against a large-scale in-silico spectral library using Word2vec-embedded spectrum vectors and hierarchical navigable small world (HNSW) approximate nearest-neighbor indexing. This skill enables sub-second queries across million-scale spectrum databases while maintaining molecular identification accuracy.

## When to use

You have an unknown experimental mass spectrum (e.g., from liquid chromatography–mass spectrometry) and need to retrieve the most structurally similar candidate molecules from a database of millions of predicted or experimental spectra. Use this skill when library size or query latency constraints prohibit exhaustive similarity computation and when approximate nearest-neighbor retrieval is acceptable.

## When NOT to use

- Input spectrum is already structurally annotated or comes from a small, manually curated reference library where exhaustive similarity scoring is feasible.
- The query spectrum is of very poor quality (e.g., <5 peaks or <0.1 relative intensity after normalization) such that embedding-based retrieval will not improve over spectral dot-product matching.
- In-silico library coverage of chemical space is insufficient for your compounds of interest (e.g., custom synthetic scaffolds not present in the training data).

## Inputs

- Query mass spectrum (e.g., peak m/z and intensity pairs)
- Pre-computed Word2vec spectrum embedding vectors (gensim model file)
- Reference spectral library database (e.g., SQLite .db file with spectrum metadata)
- HNSW index binary file (references_index.bin)

## Outputs

- Ranked list of nearest-neighbor spectrum matches
- Cosine similarity scores for each match
- Associated metadata (compound name, inchikey, molecular formula, structure)

## How to apply

First, obtain or construct pre-computed Word2vec embedding vectors for all reference spectra in the library (or download the pre-trained references_word2vec.model). Initialize an HNSW index using hnswlib with default M and ef parameters, then add all spectrum embedding vectors with unique spectrum identifiers to the index. For each query spectrum, embed it using the same Word2vec model, then perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra ranked by cosine distance. Return the ranked list with similarity scores and associated metadata (e.g., inchikey, compound name) for downstream molecular identification filtering.

## Related tools

- **hnswlib** (Constructs and queries hierarchical navigable small world graph indexes for approximate nearest-neighbor retrieval on embedded spectrum vectors)
- **gensim** (Trains and applies Word2vec embeddings to transform spectrum peak patterns into dense vectors suitable for HNSW indexing)
- **rdkit** (Parses and manipulates chemical structures and inchikeys associated with matched spectra for downstream filtering)
- **FastEI** (Complete reference implementation combining Word2vec embedding and HNSW indexing for million-scale in-silico spectrum matching) — https://github.com/Qiong-Yang/FastEI

## Examples

```
import hnswlib; index = hnswlib.Index(space='cosine', dim=100); index.add_items(reference_vectors, vector_ids); labels, distances = index.knn_query(query_vector, k=10)
```

## Evaluation signals

- Verify that query spectrum embedding and all reference embeddings were generated using the same Word2vec model and dimensionality (e.g., all 100-dimensional vectors).
- Check that HNSW index was successfully populated with the expected number of spectrum vectors (e.g., ~1 million for the FastEI in-silico library) and returns non-empty result sets.
- Compare retrieved nearest-neighbor cosine similarity scores against a baseline (e.g., top-k matches should have similarity > 0.5 for reasonable chemical relatedness).
- Spot-check returned compound identities and structures for known true positives in your test set; precision and recall should exceed baseline spectral dot-product matching.
- Profile query latency; HNSW queries should complete in <100 ms per spectrum on commodity hardware, significantly faster than exhaustive dot-product search on million-scale libraries.

## Limitations

- HNSW provides approximate rather than exact nearest-neighbor results; setting higher ef parameters improves recall at the cost of query latency.
- Word2vec spectrum embedding accuracy depends on the training data; embeddings trained on experimental spectra (NIST, MassBank) may not generalize well to novel chemical space or in-silico predicted spectra.
- Installation and deployment currently limited to Windows 64-bit systems; no native Linux or macOS builds are available.
- Large-scale pre-built indexes (references_index.bin, IN_SILICO_LIBRARY.db) must be downloaded separately from Zenodo and are not included in the GitHub repository, adding setup friction.

## Evidence

- [other] FastEI implements HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries while maintaining accuracy.: "HNSW-based indexing to enable approximate nearest-neighbor search on Word2vec-embedded spectrum vectors, allowing rapid retrieval from million-scale in-silico libraries"
- [other] For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance).: "For a given query spectrum embedding, perform approximate nearest-neighbor search on the HNSW index to retrieve the k most similar candidate spectra (ranked by cosine distance)"
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph: "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph"
- [readme] The in-silico library with predicted spectra of large-scale molecules can extend the chemical space and increase the coverage immensely when compared with experimental libraries (e.g., NIST 2017 and MassBank libraries).: "in-silico library with predicted spectra of large-scale molecules can extend the chemical space and increase the coverage immensely when compared with experimental libraries"
- [other] Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). Add all spectrum embedding vectors to the HNSW index, assigning unique spectrum identifiers.: "Initialize an HNSW index using hnswlib with default parameters (M and ef settings for navigable small world graph construction). Add all spectrum embedding vectors to the HNSW index, assigning unique"
