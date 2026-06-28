# statistics-biomarker-discovery-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **clean_normalize** — clean + normalize the feature table  →  `metabolite-feature-normalization-across-batches`, `metabolite-feature-intensity-normalization`, `metabolomics-feature-transformation`, `metabolomics-data-normalization`, `metabolite-feature-matrix-manipulation`
2. **multivariate** — multivariate analysis (PCA / PLS-DA / OPLS-DA, VIP)  →  `multivariate-statistical-analysis-metabolomics`, `multivariate-ordination-analysis`, `metabolomics-feature-selection-significance-filtering`, `multivariate-ordination-analysis-nmds-pca`, `principal-component-analysis-for-metabolomics`
3. **differential** — differential feature analysis (univariate, volcano, FDR)  →  `metabolite-feature-anova-analysis`, `fold-change-calculation`, `multiple-testing-correction-and-p-value-adjustment`, `fold-change-calculation-metabolomics`, `fold-change-calculation-across-groups`
4. **enrichment_pathway** — enrichment + pathway / functional analysis  →  `metabolite-set-enrichment-analysis`, `metabolite-kegg-pathway-enrichment`, `untargeted-metabolomics-feature-analysis`, `metabolic-network-mapping`, `pathway-metabolite-mapping-integration`
5. **biomarker** — biomarker selection + ROC / importance  →  `feature-importance-ranking`, `model-performance-evaluation-roc-curves`, `variable-importance-ranking-and-interpretation`, `random-forest-classification-for-metabolite-prediction`, `metabolomic-biomarker-pathway-association`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
