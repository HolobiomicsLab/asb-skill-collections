# ion-mobility-4d-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + deterministic selection).

## Stages

1. **preprocess_4d** — 4D LC-IMS-MS/MS feature extraction (with CCS)  →  `ion-mobility-feature-classification`, `multidimensional-feature-detection-and-alignment`, `ion-mobility-heatmap-visualization`, `ion-mobility-dimension-detection`, `multidimensional-coordinate-alignment`
2. **ccs_calibration** — collision cross section calibration + filtering  →  `collision-cross-section-calibration-ccs`, `collision-cross-section-calibration`, `collision-cross-section-calculation`, `collision-cross-section-measurement-quality-control`
3. **ccs_library_match** — CCS-aware spectral / library annotation  →  `collision-cross-section-matching-and-annotation`, `reference-library-alignment`, `ion-mobility-reference-matching`, `4d-lcimmsms-feature-extraction`, `fragmentation-pattern-spectral-matching`
4. **networking** (optional) — (optional) molecular networking of IM-resolved features  →  `molecular-networking-construction`, `spectral-library-molecular-networking`, `spectral-similarity-network-building`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `spectral-similarity-network-generation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
