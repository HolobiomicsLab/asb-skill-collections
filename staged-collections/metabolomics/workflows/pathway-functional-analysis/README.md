# pathway-functional-analysis-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **feature_prep** — prepare a ranked m/z feature list for functional analysis  →  `untargeted-metabolomics-feature-analysis`, `metabolomics-data-quality-assessment`, `metabolite-feature-column-mapping`, `metabolomic-feature-table-assembly`
2. **mummichog** — functional analysis directly from m/z (mummichog)  →  `metabolic-network-mapping`, `pathway-activity-propagation-inference`, `functional-module-inference-from-networks`, `network-based-functional-prediction`, `mass-feature-to-node-mapping`
3. **pathway_enrichment** — pathway + metabolite-set enrichment  →  `metabolite-set-enrichment-analysis`, `pathway-metabolite-mapping-integration`, `metabolic-pathway-database-querying`, `metabolite-set-analysis`, `metabolite-kegg-pathway-enrichment`
4. **interpretation** — interpret + visualize enriched pathways  →  `pathway-enrichment-visualization`, `enrichment-score-computation`, `metabolomic-biomarker-pathway-association`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
