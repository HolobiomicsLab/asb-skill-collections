# lipidomics-lcms-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw lipidomics mzML -> aligned feature table + MS/MS export  →  `lcms-peak-detection-and-alignment`, `mass-spectrometry-metadata-extraction`, `file-format-conversion-peak-picking-to-lipidmatch`, `feature-table-normalization`, `mass-spectrometry-data-column-mapping`
2. **normalize** — normalize + batch-correct the lipid feature table  →  `batch-aware-normalization-workflows`, `batch-correction-quality-assessment`, `batch-effect-correction-in-metabolomics`, `batch-corrected-feature-table-validation`, `batch-effect-correction-workflow`
3. **lipid_identification** — identify lipids (class + species) from MS/MS fragmentation  →  `lipid-identification-scoring`, `fragment-ion-library-matching`, `multi-species-lipid-prediction`, `uhplc-hrms-ms-data-matching`, `lipid-structure-specification`
4. **rule_validation** — validate lipid annotations by adduct / retention-time / class rules  →  `false-positive-annotation-filtering`, `lipid-identification-quality-filtering`, `lipid-retention-time-rule-application`, `lipid-species-annotation-assessment`
5. **statistics** — differential lipid analysis between sample groups  →  `multicontrast-statistical-testing-lipidomics`, `fold-change-calculation`, `lipid-abundance-differential-analysis`, `differential-lipid-expression-analysis`, `metabolite-feature-anova-analysis`
6. **fusion** — consolidate lipid annotations + stats into one master table  →  `structured-data-matrix-construction`, `lipid-class-feature-annotation`, `lipid-class-annotation-and-parsing`, `lipid-species-classification-mapping`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
