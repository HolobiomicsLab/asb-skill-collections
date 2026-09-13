# sirius-denovo-structure-elucidation-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **formula** — molecular formula determination (SIRIUS + ZODIAC)  →  `energy-based-formula-scoring`, `molecular-formula-prediction-from-fragmentation`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`, `neural-network-based-molecular-formula-inference`
2. **custom_db** (optional) — (optional) build a custom structure database for the search space  →  `compound-structure-processing`, `chemical-structure-validation`, `molecular-structure-input-format-handling`, `structure-standardization-validation`, `chemical-structure-serialization`
3. **structure** — structure prediction (CSI:FingerID + COSMIC)  →  `de-novo-structure-candidate-ranking`, `molecular-fingerprint-prediction`, `molecular-fingerprint-parsing`, `web-service-api-integration`, `spectrum-query-formatting`
4. **compound_class** — compound class prediction (CANOPUS / NPClassifier)  →  `compound-class-annotation-parsing`, `natural-product-classifier-substitution`, `classification-workflow-parameter-toggling`, `chemical-ontology-mapping`, `consensus-classification-reconciliation`, `chemical-class-assignment-classyfire`
5. **confidence_filter** — filter annotations by ZODIAC / COSMIC confidence  →  `sirius-zodiac-score-filtering`, `annotation-table-quality-control`, `metabolite-annotation-validation`, `structural-annotation-integration`, `compound-candidate-ranking`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
