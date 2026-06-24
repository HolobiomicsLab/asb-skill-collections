---
name: linear-regression-concentration-calibration
description: Use when your metabolomics experiment includes calibration line samples
  with known concentrations for spiked compounds, and you have computed batch-corrected
  compound/internal-standard ratios (ratio_corrected assay) and wish to convert relative
  ratios into absolute quantitative values for pathway.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality is a user-friendly R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# linear-regression-concentration-calibration

## Summary

Estimate absolute compound concentrations in metabolomics samples by fitting linear regression models to calibration line samples with known spiked concentrations, applied to batch-corrected compound/internal-standard ratios. This enables quantitative downstream analysis when reference standards are available.

## When to use

Apply this skill when your metabolomics experiment includes calibration line samples with known concentrations for spiked compounds, and you have computed batch-corrected compound/internal-standard ratios (ratio_corrected assay) and wish to convert relative ratios into absolute quantitative values for pathway modeling or biomarker interpretation.

## When NOT to use

- Input data lacks calibration line samples or reference standards with known concentrations.
- Multiple sample types need simultaneous concentration calculation (current version supports only one sample type per analysis run).
- Relative quantification (ratios) is sufficient for your research question and absolute concentrations are not needed.

## Inputs

- SummarizedExperiment object with ratio_corrected assay (batch-corrected compound/internal-standard ratios)
- Calibration line sample metadata with known concentration values per compound
- colData and rowData annotations indicating sample type and compound identity

## Outputs

- SummarizedExperiment with concentration assay added (absolute compound concentrations)
- R² values per compound (stored in rowData) quantifying calibration model fit
- Metadata annotations flagging compounds with poor calibration fit

## How to apply

After running doAnalysis to generate the ratio_corrected assay, supply calibration line samples with known concentrations in the input data. The doAnalysis function will automatically detect the concentration column and fit weighted linear regression models separately for each compound, using the ratio_corrected values as the predictor and known concentrations as the response. The regression will be restricted to a single sample type per analysis run to avoid confounding batch or matrix effects. The fitted model produces both predicted concentrations and R² values that quantify goodness-of-fit. Only compounds with sufficient calibration points and acceptable R² should be retained for reporting.

## Related tools

- **mzQuality** (Core R package that implements doAnalysis wrapper function integrating linear regression concentration calibration into the QC workflow) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container class storing assays (ratio_corrected, concentration), rowData (R² values, compound metadata), and colData (sample annotations))
- **R** (Programming environment executing the doAnalysis function and underlying linear regression fitting)

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE)
```

## Evaluation signals

- Concentration assay is present in output SummarizedExperiment and contains numeric values for compounds with calibration data.
- R² values in rowData are between 0 and 1 and correlate positively with concentration prediction accuracy on hold-out calibration samples.
- Compounds lacking sufficient calibration points or exhibiting R² < user-defined threshold (e.g., 0.8) are marked FALSE in rowData(exp)$use.
- Predicted concentrations for calibration line samples fall within expected range and show monotonic relationship with input known concentrations.
- Only one sample type was included in the concentration calculation (verify via unique(exp$sample_type) in input).

## Limitations

- Only one sample type can be used for calculating concentrations per analysis run; multiple sample types require separate doAnalysis calls.
- This limitation will be addressed in a future version of mzQuality.
- Concentration calculation requires explicit supply of calibration line samples and known concentrations in the input data; regression will not be performed if this column is absent.
- Regression assumes linear relationship between batch-corrected ratio and concentration; nonlinear or matrix-dependent relationships are not modeled.

## Evidence

- [intro] Calibration requirement: "by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations"
- [other] Linear regression application: "Optionally calculate absolute concentrations via (weighted) linear regression if concentration column is present in the input data"
- [other] Single sample type constraint: "restricted to a single sample type per analysis run"
- [readme] Integration in doAnalysis workflow: "If known concentrations for calibration lines have been supplied, the `doAnalysis` function will also calculate the concentrations and the corresponding R2 value"
- [readme] Automated invocation: "This is automatically done when the `doAnalysis` function is called."
