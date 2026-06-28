# sirius-denovo-structure-elucidation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **formula** — molecular formula determination (SIRIUS + ZODIAC)  →  `energy-based-formula-scoring`, `molecular-formula-prediction-from-fragmentation`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`, `neural-network-based-molecular-formula-inference`
2. **structure** — structure prediction (CSI:FingerID + COSMIC)  →  `molecular-fingerprint-prediction`, `molecular-fingerprint-parsing`, `web-service-api-integration`, `de-novo-structure-candidate-ranking`, `spectrum-query-formatting`
3. **compound_class** — compound class prediction (CANOPUS / NPClassifier)  →  `chemical-classification-scheme-validation`, `natural-product-classifier-substitution`, `classification-workflow-parameter-toggling`, `chemical-ontology-mapping`, `consensus-classification-reconciliation`
4. **custom_db** (optional) — (optional) build a custom structure database for the search space  →  `chemical-structure-validation`, `molecular-structure-input-format-handling`, `structure-standardization-validation`, `compound-structure-processing`, `chemical-structure-serialization`
5. **confidence_filter** — filter annotations by ZODIAC / COSMIC confidence  →  `sirius-zodiac-score-filtering`, `annotation-table-quality-control`, `spectral-annotation-filtering-by-similarity-metrics`, `metabolite-annotation-validation`, `structural-annotation-integration`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
