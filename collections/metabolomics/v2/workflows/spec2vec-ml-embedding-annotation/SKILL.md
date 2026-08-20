---
name: spec2vec-ml-embedding-annotation-workflow
description: 'Use when you want to annotate untargeted MS2 spectra with a machine-learned
  spectral embedding instead of raw cosine scoring — convert spectra into peak/neutral-loss
  "documents", train or load a Spec2Vec (Word2Vec-style) embedding model on a reference
  corpus, embed query spectra into that learned vector space, and retrieve/annotate
  nearest library neighbours by embedding similarity, as a deep-learning-adjacent
  second pass beyond modified-cosine matching.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  - GC-MS
  stage_count: 4
  member_skills:
  - peak-filtering-and-preprocessing-lc-ms
  - spectral-peak-filtering-and-normalization
  - spectral-peak-filtering
  - spectrum-normalization-and-standardization
  - ms-ms-spectrum-parsing
  - spectrum-document-conversion-peak-loss-representation
  - mass-spectrometry-spectrum-tokenization
  - neutral-loss-calculation-from-precursor
  - corpus-size-coverage-scaling-analysis
  - spectral-peak-word-embedding-representation
  - missing-fraction-quality-filtering-for-embeddings
  - mass-spectral-missing-word-fraction-computation
  - candidate-match-retrieval
  - embedding-vector-similarity-ranking
  - approximate-nearest-neighbor-search
  - spectral-similarity-scoring-computation
  - spectrum-embedding-indexing
  - embedding-similarity-computation
  member_tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - spec2vec
  - Word2Vec
  - RDKit
  - NumPy
  - gensim (Word2Vec, CBOW, Skip-gram)
  - NumPy, Pandas, SciPy
  - NumPy, Pandas
  - MS2Query
  - MS2Deepscore
  - MZMine
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Spec2Vec / ML Spectral-Embedding Annotation (peak-loss documents -> Word2Vec embedding -> nearest-neighbour ID)

## Summary

MS2 in, an embedding-based annotation table out: peak/loss document conversion, Spec2Vec (Word2Vec) model training or loading, query-spectrum embedding, and nearest-neighbour library retrieval and annotation.


## When to use

Use when you want to annotate untargeted MS2 spectra with a machine-learned spectral embedding instead of raw cosine scoring — convert spectra into peak/neutral-loss "documents", train or load a Spec2Vec (Word2Vec-style) embedding model on a reference corpus, embed query spectra into that learned vector space, and retrieve/annotate nearest library neighbours by embedding similarity, as a deep-learning-adjacent second pass beyond modified-cosine matching.


## When NOT to use

- The data is not LC-MS, GC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw MS2 spectra -> filtered, normalized spectrum objects

**EDAM operation:** operation_3630

**Inputs:** mzML · **Outputs:** mgf/sirius

**Candidate leaf skills:** `peak-filtering-and-preprocessing-lc-ms` (primary), `spectral-peak-filtering-and-normalization`, `spectral-peak-filtering`, `spectrum-normalization-and-standardization`, `ms-ms-spectrum-parsing`

**Tools (primary):** matchms, gensim, Numba, Pandas, scipy, spec2vec, Word2Vec

**Other candidate tools:** pubchempy, RDKit, Python, numpy, MS2Query, MZMine

**Grounding:** 5 KB(s); DOIs: 10.1038/s41467-023-37446-4, 10.1186/s13321-021-00558-4, 10.1186/s13321-024-00878-1, 10.1371/journal.pcbi.1008724 …

### Stage 2 — document_conversion

**Goal:** filtered spectra -> peak/neutral-loss "documents" for word-embedding training

**EDAM operation:** operation_3357

**Inputs:** mgf/sirius · **Outputs:** json/spectral-documents

**Candidate leaf skills:** `spectrum-document-conversion-peak-loss-representation` (primary), `mass-spectrometry-spectrum-tokenization`, `neutral-loss-calculation-from-precursor`

**Tools (primary):** Spec2Vec, matchms, gensim, RDKit, NumPy, Numba, Pandas, scipy, gensim (Word2Vec, CBOW, Skip-gram), NumPy, Pandas, SciPy

**Other candidate tools:** Word2Vec (gensim), Word2Vec, Python 3.8, MEMO, memo-ms, Python

**Grounding:** 2 KB(s); DOIs: 10.1371/journal.pcbi.1008724, 10.3389/fbinf.2022.842964

### Stage 3 — embed

**Goal:** peak/loss documents -> Spec2Vec Word2Vec embedding model + query-spectrum embedding vectors

**EDAM operation:** operation_3800

**Inputs:** json/spectral-documents · **Outputs:** json/spectrum-embeddings

**Candidate leaf skills:** `corpus-size-coverage-scaling-analysis` (primary), `spectral-peak-word-embedding-representation`, `missing-fraction-quality-filtering-for-embeddings`, `mass-spectral-missing-word-fraction-computation`

**Tools (primary):** Spec2Vec, matchms, gensim, NumPy, Numba, Pandas, Word2Vec, NumPy, Pandas

**Other candidate tools:** Word2Vec (gensim)

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1008724

### Stage 4 — retrieve_annotate

**Goal:** query embeddings -> nearest-neighbour library matches -> embedding-based annotation table

**EDAM operation:** operation_3767

**Inputs:** json/spectrum-embeddings · **Outputs:** tsv

**Candidate leaf skills:** `candidate-match-retrieval` (primary), `embedding-vector-similarity-ranking`, `approximate-nearest-neighbor-search`, `spectral-similarity-scoring-computation`, `spectrum-embedding-indexing`, `embedding-similarity-computation`

**Tools (primary):** MS2Query, MS2Deepscore, Spec2Vec, MZMine, RDKit

**Other candidate tools:** hnswlib, Python, gensim, Python 3.7, matchms, NumPy, Numba, Pandas, scipy, Word2Vec (gensim), NumPy, Pandas, SciPy, Numba, Anaconda, Git, MSBERT, PyTorch

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.4c02426, 10.1038/s41467-023-37446-4, 10.1038/s41467-023-39279-7, 10.1371/journal.pcbi.1008724

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
