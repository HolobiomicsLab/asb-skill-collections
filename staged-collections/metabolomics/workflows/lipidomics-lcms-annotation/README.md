# lipidomics-lcms-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **preprocess** — raw lipidomics mzML -> aligned feature table + MS/MS export  →  `mass-spectrometry-metadata-extraction`, `file-format-conversion-peak-picking-to-lipidmatch`, `lcms-peak-detection-and-alignment`, `feature-table-normalization`, `mass-spectrometry-data-column-mapping`
2. **lipid_identification** — identify lipids (class + species) from MS/MS fragmentation  →  `lipid-identification-scoring`, `fragment-ion-library-matching`, `multi-species-lipid-prediction`, `uhplc-hrms-ms-data-matching`, `lipid-library-format-schema`
3. **rule_validation** — validate lipid annotations by adduct / retention-time / class rules  →  `false-positive-annotation-filtering`, `lipid-retention-time-rule-application`, `lipid-identification-quality-filtering`, `lipid-species-annotation-assessment`
4. **statistics** — differential lipid analysis between sample groups  →  `multicontrast-statistical-testing-lipidomics`, `fold-change-calculation`, `lipid-abundance-differential-analysis`, `metabolite-feature-anova-analysis`, `enrichment-statistic-interpretation`
5. **fusion** — consolidate lipid annotations + stats into one master table  →  `lipid-class-feature-annotation`, `lipid-class-annotation-and-parsing`, `lipid-species-classification-mapping`, `structured-data-matrix-construction`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
