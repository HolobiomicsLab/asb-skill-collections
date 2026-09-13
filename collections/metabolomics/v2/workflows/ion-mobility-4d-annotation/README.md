# ion-mobility-4d-annotation-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **preprocess_4d** — 4D LC-IMS-MS/MS feature extraction (with CCS)  →  `multidimensional-feature-detection-and-alignment`, `ion-mobility-heatmap-visualization`, `ion-mobility-feature-classification`, `ion-mobility-dimension-detection`, `multidimensional-coordinate-alignment`
2. **ccs_calibration** — collision cross section calibration + filtering  →  `collision-cross-section-calibration-ccs`, `collision-cross-section-calibration`, `collision-cross-section-calculation`, `collision-cross-section-measurement-quality-control`
3. **ccs_library_match** — CCS-aware spectral / library annotation  →  `collision-cross-section-matching-and-annotation`, `reference-library-alignment`, `4d-lcimmsms-feature-extraction`, `fragmentation-pattern-spectral-matching`
4. **networking** (optional) — (optional) molecular networking of IM-resolved features  →  `feature-based-molecular-network-interpretation`, `spectral-similarity-network-building`, `molecular-networking-construction`, `feature-network-construction-from-mass-spectrometry`, `spectral-similarity-network-generation`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
