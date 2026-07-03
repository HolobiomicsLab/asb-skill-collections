# compound-class-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw mzML -> feature table + SIRIUS-flavour MS2 export  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-table-construction`, `cross-sample-feature-alignment`, `lcms-feature-table-construction`, `mass-spectrometry-feature-annotation`
2. **formula** — MS2 spectra -> molecular formula (SIRIUS + ZODIAC re-ranking)  →  `molecular-formula-prediction-from-fragmentation`, `energy-based-formula-scoring`, `neural-network-based-molecular-formula-inference`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`
3. **fingerprint** — formula + MS2 -> molecular fingerprint (CSI:FingerID)  →  `molecular-fingerprint-parsing`, `molecular-fingerprint-prediction`, `spectrum-query-formatting`, `spectral-fingerprint-web-service-query`, `molecular-fingerprint-generation-and-encoding`
4. **classify** — fingerprint -> compound class (CANOPUS / NPClassifier: superclass/class/pathway)  →  `natural-product-classifier-substitution`, `natural-product-classification-prediction`, `classification-workflow-parameter-toggling`
5. **consolidate** — consolidate formula + fingerprint + class into a class-annotated feature table  →  `consensus-classification-reconciliation`, `spectral-feature-chemical-assignment`, `chemical-classification-scheme-validation`, `chemical-ontology-mapping`, `structural-annotation-integration`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
