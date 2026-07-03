# targeted-lcms-quantification-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **integrate** — raw targeted LC-MS -> integrated peak areas for target transitions  →  `targeted-peak-detection-and-integration`, `chromatographic-peak-detection-and-integration`, `targeted-peak-detection-screening-and-validation`, `targeted-peak-extraction-ms1`, `m-z-and-retention-time-window-validation`
2. **calibrate** — calibrant standards -> calibration curves with internal-standard normalization  →  `calibration-curve-fitting-metabolomics`, `calibration-curve-validation`, `linear-regression-concentration-calibration`, `linear-regression-model-fitting`
3. **quantify** — apply calibration -> absolute / relative concentrations per sample  →  `concentration-prediction-from-calibration-model`, `linear-regression-absolute-quantification`, `concentration-prediction-from-calibration-curves`
4. **qc** (optional) — (optional) batch QC — response drift, QC-sample RSD, outlier flagging  →  `qc-sample-variability-assessment`, `qc-sample-reliability-evaluation`, `qc-sample-batch-drift-correction`, `batch-effect-assessment-via-quality-metrics`, `signal-trend-assessment-across-injections`
5. **report** — consolidate concentrations + QC into a reportable quantification table  →  `quality-control-report-generation`, `quality-control-metric-threshold-configuration`, `quality-control-metric-computation`, `qc-summary-table-extraction`, `compound-metric-tabulation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
