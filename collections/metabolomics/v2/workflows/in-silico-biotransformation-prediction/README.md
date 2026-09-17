# in-silico-biotransformation-prediction-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess** — raw mzML -> feature table + MS2 export  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-table-construction`, `spectral-feature-table-generation`, `lcms-feature-detection-and-quantification`, `feature-alignment-metabolomics`
2. **biotransformation_prediction** — parent structure -> predicted metabolite/transformation-product structures (rule-based expansion)  →  `biotransformation-rule-application`, `biotransformation-prediction-across-microbiota-contexts`, `microbial-biotransformation-prediction`, `small-molecule-structure-input-preparation`, `metabolite-structure-prediction`
3. **candidate_filtering** — predicted candidates -> mass-plausible candidates (filter against the experimental peak list)  →  `adduct-mass-adjustment-calculation`, `exact-mass-database-matching`, `adduct-mass-shift-calculation`
4. **ms_matching** — mass-plausible candidates -> MS/MS-matched and ranked biotransformation products  →  `in-silico-fragmentation-prediction`, `candidate-metabolite-ranking`, `transformation-product-prediction`, `fragment-ion-scoring-and-ranking`, `structural-similarity-scoring-metabolites`
5. **report** — consolidate parent structure, predicted candidates, and MS/MS-matched hits into a biotransformation-product annotation table  →  `biotransformation-candidate-integration-with-networking`, `mass-spectrometry-compound-annotation-database-generation`, `transformation-product-parent-linkage`, `metabolite-structure-annotation-integration`, `parent-product-relationship-tracking`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
