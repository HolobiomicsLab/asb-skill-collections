# lipidomics-lcms-annotation-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess** — raw lipidomics mzML -> aligned feature table + MS/MS export  →  `lcms-peak-detection-and-alignment`, `mass-spectrometry-metadata-extraction`, `file-format-conversion-peak-picking-to-lipidmatch`, `feature-table-normalization`, `mass-spectrometry-data-column-mapping`
2. **normalize** — normalize + batch-correct the lipid feature table  →  `batch-aware-normalization-workflows`, `batch-correction-quality-assessment`, `batch-effect-correction-in-metabolomics`, `batch-corrected-feature-table-validation`, `batch-effect-correction-workflow`
3. **lipid_identification** — identify lipids (class + species) from MS/MS fragmentation  →  `lipid-identification-scoring`, `fragment-ion-library-matching`, `multi-species-lipid-prediction`, `uhplc-hrms-ms-data-matching`, `lipid-structure-specification`
4. **rule_validation** — validate lipid annotations by adduct / retention-time / class rules  →  `false-positive-annotation-filtering`, `lipid-identification-quality-filtering`, `lipid-retention-time-rule-application`, `lipid-species-annotation-assessment`
5. **statistics** — differential lipid analysis between sample groups  →  `multicontrast-statistical-testing-lipidomics`, `fold-change-calculation`, `lipid-abundance-differential-analysis`, `differential-lipid-expression-analysis`, `metabolite-feature-anova-analysis`
6. **fusion** — consolidate lipid annotations + stats into one master table  →  `structured-data-matrix-construction`, `lipid-class-feature-annotation`, `lipid-class-annotation-and-parsing`, `lipid-species-classification-mapping`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
