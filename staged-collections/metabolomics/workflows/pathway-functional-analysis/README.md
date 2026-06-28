# pathway-functional-analysis-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **feature_prep** — prepare a ranked m/z feature list for functional analysis  →  `untargeted-metabolomics-feature-analysis`, `metabolomics-data-quality-assessment`, `metabolite-feature-column-mapping`, `metabolomic-feature-table-assembly`
2. **mummichog** — functional analysis directly from m/z (mummichog)  →  `pathway-activity-propagation-inference`, `metabolic-network-mapping`, `functional-module-inference-from-networks`, `network-based-functional-prediction`, `mass-feature-to-node-mapping`
3. **pathway_enrichment** — pathway + metabolite-set enrichment  →  `metabolite-set-analysis`, `metabolite-set-enrichment-analysis`, `comparative-enrichment-method-evaluation`, `untargeted-metabolomics-feature-interpretation`
4. **interpretation** — interpret + visualize enriched pathways  →  `pathway-metabolite-mapping-integration`, `pathway-enrichment-visualization`, `metabolite-kegg-pathway-enrichment`, `enrichment-score-computation`, `metabolomic-biomarker-pathway-association`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
