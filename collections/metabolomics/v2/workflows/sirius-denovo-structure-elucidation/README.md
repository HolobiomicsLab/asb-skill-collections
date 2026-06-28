# sirius-denovo-structure-elucidation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **formula** — molecular formula determination (SIRIUS + ZODIAC)  →  `energy-based-formula-scoring`, `molecular-formula-prediction-from-fragmentation`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`, `neural-network-based-molecular-formula-inference`
2. **custom_db** (optional) — (optional) build a custom structure database for the search space  →  `compound-structure-processing`, `chemical-structure-validation`, `molecular-structure-input-format-handling`, `structure-standardization-validation`, `chemical-structure-serialization`
3. **structure** — structure prediction (CSI:FingerID + COSMIC)  →  `de-novo-structure-candidate-ranking`, `molecular-fingerprint-prediction`, `molecular-fingerprint-parsing`, `web-service-api-integration`, `spectrum-query-formatting`
4. **compound_class** — compound class prediction (CANOPUS / NPClassifier)  →  `compound-class-annotation-parsing`, `natural-product-classifier-substitution`, `classification-workflow-parameter-toggling`, `chemical-ontology-mapping`, `consensus-classification-reconciliation`, `chemical-class-assignment-classyfire`
5. **confidence_filter** — filter annotations by ZODIAC / COSMIC confidence  →  `sirius-zodiac-score-filtering`, `annotation-table-quality-control`, `metabolite-annotation-validation`, `structural-annotation-integration`, `compound-candidate-ranking`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
