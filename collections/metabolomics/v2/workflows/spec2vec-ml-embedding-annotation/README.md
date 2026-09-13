# spec2vec-ml-embedding-annotation-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess** — raw MS2 spectra -> filtered, normalized spectrum objects  →  `peak-filtering-and-preprocessing-lc-ms`, `spectral-peak-filtering-and-normalization`, `spectral-peak-filtering`, `spectrum-normalization-and-standardization`, `ms-ms-spectrum-parsing`
2. **document_conversion** — filtered spectra -> peak/neutral-loss "documents" for word-embedding training  →  `spectrum-document-conversion-peak-loss-representation`, `mass-spectrometry-spectrum-tokenization`, `neutral-loss-calculation-from-precursor`
3. **embed** — peak/loss documents -> Spec2Vec Word2Vec embedding model + query-spectrum embedding vectors  →  `corpus-size-coverage-scaling-analysis`, `spectral-peak-word-embedding-representation`, `missing-fraction-quality-filtering-for-embeddings`, `mass-spectral-missing-word-fraction-computation`
4. **retrieve_annotate** — query embeddings -> nearest-neighbour library matches -> embedding-based annotation table  →  `candidate-match-retrieval`, `embedding-vector-similarity-ranking`, `approximate-nearest-neighbor-search`, `spectral-similarity-scoring-computation`, `spectrum-embedding-indexing`, `embedding-similarity-computation`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
