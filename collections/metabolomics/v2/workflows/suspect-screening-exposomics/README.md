# suspect-screening-exposomics-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess** — raw HRMS -> feature table + MS2 export  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-table-construction`, `mass-spectrometry-feature-detection-validation`, `non-targeted-preprocessing-tool-comparison`, `non-targeted-feature-detection-and-screening`
2. **suspect_match** — features -> suspect-list matches by exact mass / RT / MS2  →  `suspect-database-matching`, `ms1-feature-extraction`, `mass-spectrometry-screening-workflows`, `multi-criterion-scoring-integration`, `feature-annotation-with-chemical-descriptors`
3. **in_silico_fragment** — suspect hits -> in-silico fragmentation structure ranking (MetFrag / SIRIUS)  →  `in-silico-fragmentation-prediction`, `candidate-structure-ranking`, `candidate-rank-scoring`, `fragment-ion-scoring-and-ranking`, `candidate-structure-ranking-from-spectrum`
4. **confidence** — assign identification confidence levels (Schymanski 1-5) to hits  →  `compound-annotation-confidence-assessment`, `metabolite-annotation-confidence-assignment`, `annotation-confidence-assessment`, `annotation-scoring-and-ranking`, `bayesian-annotation-probability-inference`
5. **report** — consolidate suspect hits + structures + confidence into an annotated table  →  `feature-metadata-annotation`, `chemical-structure-validation`, `reference-compound-verification`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
