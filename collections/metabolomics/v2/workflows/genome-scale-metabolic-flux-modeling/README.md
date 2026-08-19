# genome-scale-metabolic-flux-modeling-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **constrain** — generic GEM + omics data -> sample-constrained metabolic model  →  `metabolic-model-constraint-application`, `constraint-based-flux-balance-analysis`, `reaction-activity-score-computation-from-gpr`, `gene-expression-constraint-integration`, `transcriptomics-reaction-activity-scoring`
2. **sample_flux** — constrained model -> feasible flux distribution samples (optGpSampler)  →  `irreversible-model-conversion`, `feasible-flux-distribution-sampling`, `dimensionality-reduction-and-clustering-evaluation`
3. **interpret_flux** — sampled flux distributions -> normalized, compared flux-distribution report  →  `flux-distribution-segregation-visualization`, `flux-distribution-interpretation-across-cell-lines`, `flux-variability-analysis-interpretation`, `flux-variability-analysis-for-scaling`, `constraint-based-flux-sampling-and-analysis`
4. **community_consensus** — draft per-organism/community-member GEMs -> gap-filled consensus community model  →  `metabolic-model-merging-consensus-building`, `community-metabolic-reconstruction-synthesis`, `metabolic-model-consensus-integration`, `community-metabolic-pathway-integration`, `systems-biology-model-standardization`
5. **report** — consolidate sampled/interpreted flux states + consensus community model into a flux-state report  →  `constraint-based-model-sampling-and-flux-prediction`, `mass-action-law-flux-prediction`, `extracellular-flux-constraint-integration`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
