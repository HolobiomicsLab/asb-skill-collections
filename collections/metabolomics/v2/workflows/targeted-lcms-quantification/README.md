# targeted-lcms-quantification-workflow

**Status:** published as an **outline** — the structure is validated, the execution is not.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

> Automatic grading of `workflow.yaml` (`asb solve-workflow`, checkpoint mode) is **not part of
> this release**: no released ASB version loads these files. Follow the stages yourself. The stage
> structure is validated by `validate_workflows.py` through `release_gate.py`.

## Stages

1. **integrate** — raw targeted LC-MS -> integrated peak areas for target transitions  →  `targeted-peak-detection-and-integration`, `chromatographic-peak-detection-and-integration`, `targeted-peak-detection-screening-and-validation`, `targeted-peak-extraction-ms1`, `m-z-and-retention-time-window-validation`
2. **calibrate** — calibrant standards -> calibration curves with internal-standard normalization  →  `calibration-curve-fitting-metabolomics`, `calibration-curve-validation`, `linear-regression-concentration-calibration`, `linear-regression-model-fitting`
3. **quantify** — apply calibration -> absolute / relative concentrations per sample  →  `concentration-prediction-from-calibration-model`, `linear-regression-absolute-quantification`, `concentration-prediction-from-calibration-curves`
4. **qc** (optional) — (optional) batch QC — response drift, QC-sample RSD, outlier flagging  →  `qc-sample-variability-assessment`, `qc-sample-reliability-evaluation`, `qc-sample-batch-drift-correction`, `batch-effect-assessment-via-quality-metrics`, `signal-trend-assessment-across-injections`
5. **report** — consolidate concentrations + QC into a reportable quantification table  →  `quality-control-report-generation`, `quality-control-metric-threshold-configuration`, `quality-control-metric-computation`, `qc-summary-table-extraction`, `compound-metric-tabulation`

`derived_from_workflows` in the frontmatter is a provenance record — the ASB per-paper workflows
whose structure corroborated this pipeline. No ablation experiment consuming it is released.
