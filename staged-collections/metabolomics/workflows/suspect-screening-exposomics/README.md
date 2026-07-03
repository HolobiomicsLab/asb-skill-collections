# suspect-screening-exposomics-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw HRMS -> feature table + MS2 export  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-table-construction`, `ms1-feature-extraction`, `mass-spectrometry-feature-detection-validation`, `non-targeted-preprocessing-tool-comparison`
2. **suspect_match** — features -> suspect-list matches by exact mass / RT / MS2  →  `suspect-database-matching`, `mass-spectrometry-screening-workflows`, `feature-annotation-with-chemical-descriptors`, `multi-criterion-scoring-integration`
3. **in_silico_fragment** — suspect hits -> in-silico fragmentation structure ranking (MetFrag / SIRIUS)  →  `in-silico-fragmentation-prediction`, `candidate-structure-ranking`, `candidate-rank-scoring`, `fragment-ion-scoring-and-ranking`, `candidate-structure-ranking-from-spectrum`
4. **confidence** — assign identification confidence levels (Schymanski 1-5) to hits  →  `compound-annotation-confidence-assessment`, `metabolite-annotation-confidence-assignment`, `annotation-confidence-assessment`, `annotation-scoring-and-ranking`, `lipid-species-identification`
5. **report** — consolidate suspect hits + structures + confidence into an annotated table  →  `suspect-list-format-conversion`, `inchikey-structural-similarity-computation`, `spectral-database-schema-validation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
