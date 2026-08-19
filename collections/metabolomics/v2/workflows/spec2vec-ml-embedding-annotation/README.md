# spec2vec-ml-embedding-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw MS2 spectra -> filtered, normalized spectrum objects  →  `peak-filtering-and-preprocessing-lc-ms`, `spectral-peak-filtering-and-normalization`, `spectral-peak-filtering`, `spectrum-normalization-and-standardization`, `ms-ms-spectrum-parsing`
2. **document_conversion** — filtered spectra -> peak/neutral-loss "documents" for word-embedding training  →  `spectrum-document-conversion-peak-loss-representation`, `mass-spectrometry-spectrum-tokenization`, `neutral-loss-calculation-from-precursor`
3. **embed** — peak/loss documents -> Spec2Vec Word2Vec embedding model + query-spectrum embedding vectors  →  `corpus-size-coverage-scaling-analysis`, `spectral-peak-word-embedding-representation`, `missing-fraction-quality-filtering-for-embeddings`, `mass-spectral-missing-word-fraction-computation`
4. **retrieve_annotate** — query embeddings -> nearest-neighbour library matches -> embedding-based annotation table  →  `candidate-match-retrieval`, `embedding-vector-similarity-ranking`, `approximate-nearest-neighbor-search`, `spectral-similarity-scoring-computation`, `spectrum-embedding-indexing`, `embedding-similarity-computation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
