# suspect-screening-exposomics-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw HRMS -> feature table + MS2 export  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-table-construction`, `mass-spectrometry-feature-detection-validation`, `non-targeted-preprocessing-tool-comparison`, `non-targeted-feature-detection-and-screening`
2. **suspect_match** — features -> suspect-list matches by exact mass / RT / MS2  →  `suspect-database-matching`, `ms1-feature-extraction`, `mass-spectrometry-screening-workflows`, `multi-criterion-scoring-integration`, `feature-annotation-with-chemical-descriptors`
3. **in_silico_fragment** — suspect hits -> in-silico fragmentation structure ranking (MetFrag / SIRIUS)  →  `in-silico-fragmentation-prediction`, `candidate-structure-ranking`, `candidate-rank-scoring`, `fragment-ion-scoring-and-ranking`, `candidate-structure-ranking-from-spectrum`
4. **confidence** — assign identification confidence levels (Schymanski 1-5) to hits  →  `compound-annotation-confidence-assessment`, `metabolite-annotation-confidence-assignment`, `annotation-confidence-assessment`, `annotation-scoring-and-ranking`, `bayesian-annotation-probability-inference`
5. **report** — consolidate suspect hits + structures + confidence into an annotated table  →  `chemical-structure-validation`, `peak-extraction-rescue-algorithms`, `spectral-match-result-consolidation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
