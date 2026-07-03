# ms2lda-substructure-discovery-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw MS2 spectra (mgf/mzML/msp) -> cleaned, intensity-normalized bag-of-fragments corpus  →  `mass-spectrometry-file-format-parsing`, `fragment-ion-peak-detection-and-normalization`, `mass-spectrometry-peak-filtering-and-noise-reduction`, `spectral-noise-filtering-and-artifact-removal`, `spectral-noise-filtering-and-quality-control`
2. **lda_modeling** — bag-of-fragments corpus -> Mass2Motifs (LDA topic model over spectral documents)  →  `probabilistic-topic-modeling-mass-spectrometry`, `mass2motif-parameter-optimization`, `lda-model-training-convergence`, `latent-dirichlet-allocation-topic-inference`, `mass-binning-and-tokenization-for-topic-modeling`
3. **motif_annotation** — Mass2Motifs -> putative substructure annotations (MotifDB + Spec2Vec embedding match)  →  `mass2motif-annotation-guidance-via-spectral-embeddings`, `motifdb-reference-library-querying`, `mass2motif-annotation-mapping`, `spectral-similarity-scoring-and-ranking`, `motif-metadata-annotation`
4. **network_mapping** — annotated Mass2Motifs + GNPS molecular network -> motif-enriched network nodes  →  `mass2motif-substructure-mapping`, `ms2lda-motif-to-network-mapping`, `molecular-network-annotation-integration`, `mass-spectral-network-annotation`, `substructure-annotation-integration`
5. **report** — consolidate motifs + annotations + motif-enriched network into a substructure discovery report  →  `json-structured-report-generation`, `mass2motif-network-construction`, `ms2lda-motif-mapping`, `ms2lda-substructure-assignment`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
