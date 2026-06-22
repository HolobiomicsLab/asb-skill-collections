---
name: metabolite-ratio-batch-correction
description: Use when your input is a SummarizedExperiment containing multiple batches or injection sequences of metabolomics samples (study samples, QC replicates, calibration lines) with measured ion areas for compounds and assigned internal standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-ratio-batch-correction

## Summary

Batch-correct compound/internal-standard ratios in metabolomics LC-MS/MS data using pooled study quality control (SQC) samples as anchors. This corrects for systematic drift and matrix effects across injection sequences while preserving biological signal.

## When to use

Your input is a SummarizedExperiment containing multiple batches or injection sequences of metabolomics samples (study samples, QC replicates, calibration lines) with measured ion areas for compounds and assigned internal standards. Apply this skill when you need to harmonize compound/internal standard ratios across batches before downstream quantitation or statistical modeling, especially when pooled QC samples are available to estimate batch-specific correction factors.

## When NOT to use

- Input data lacks pooled quality control samples — batch correction requires QC replicates to estimate batch-specific factors.
- All samples are from a single batch or injection sequence — batch correction is not applicable; calculate uncorrected ratios instead.
- Only one sample type is present and you need to calculate absolute concentrations from multiple sample types simultaneously — mzQuality currently restricts concentration calculation to a single sample type per run.
- Input is already a batch-corrected feature table or ratio matrix — re-applying this skill will overwrite prior corrected values and recalculate from the raw ion areas.

## Inputs

- SummarizedExperiment object with assays containing ion areas (compound and internal standard)
- rowData with compound metadata (internal standard assignment, optional known concentrations for calibration lines)
- colData with sample metadata (sample type: study sample, QC, calibration line; batch/injection sequence identifier)
- Tab-delimited data file (alternative: passed through readData and buildExperiment functions)

## Outputs

- SummarizedExperiment object with ratio_corrected assay (batch-corrected compound/internal standard ratios)
- Updated rowData with quality metrics (RSDQC, background percentage, matrix effect, presence, median area, internal standard recommendation, use flag)
- Updated colData with quality flags (outlier status, mis-injection detection via internal standard areas, use flag)
- Optional: absolute concentration values (concentrations column in assays and rowData) if calibration lines and known concentrations supplied

## How to apply

First, invoke the `doAnalysis` function with `useWithinBatch=TRUE` to apply batch correction using pooled study quality control samples as anchors. The function calculates the ratio between each compound and its assigned internal standard, then applies a within-batch correction factor derived from the median ratio in each batch's pooled SQC samples. Set `removeOutliers=TRUE` to flag QC sample outliers (detected via Rosner test on Compound/Internal Standard ratios) before deriving batch factors; exclude flagged outliers from the correction calculation. Apply `qcPercentage=80`, `backgroundPercentage=40`, and `nonReportableRSD=30` thresholds to define acceptable analyte reliability and measurement variability and filter compounds that fail these thresholds. The output SummarizedExperiment will contain a `ratio_corrected` assay with batch-harmonized ratios, together with metadata annotations (rowData/colData `use` flag) marking detected outliers and mis-injected study samples (identified via internal standard areas falling outside acceptable range). If calibration-line samples with known concentrations are present in the input, `doAnalysis` will additionally calculate absolute concentrations via weighted linear regression restricted to a single sample type per run.

## Related tools

- **mzQuality** (Core R package providing doAnalysis function for batch correction, outlier detection, and quality filtering; manages SummarizedExperiment objects throughout the workflow) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor data container for storing assays (ion areas, corrected ratios), row metadata (compound quality metrics), and column metadata (sample quality flags))
- **mzQualityDashboard** (Interactive Shiny application wrapper for mzQuality; enables doAnalysis execution and visualization without direct R programming) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE, useWithinBatch = TRUE, removeBadCompounds = TRUE, qcPercentage = 80, backgroundPercentage = 40, nonReportableRSD = 30)
```

## Evaluation signals

- Output SummarizedExperiment contains a ratio_corrected assay with numeric values (batch-corrected compound/internal standard ratios) for all samples.
- rowData includes RSDQC (relative standard deviation of QC samples), background percentage, and matrix effect columns calculated from corrected ratios; compounds failing qcPercentage, backgroundPercentage, or nonReportableRSD thresholds have use=FALSE.
- colData includes outlier flags for QC samples (detected via Rosner test) and mis-injection flags for study samples (internal standard areas below or above acceptable range); outlier/mis-injected samples have use=FALSE.
- Median corrected ratio in pooled SQC samples per batch is closer to 1.0 (or other unified reference) compared to the uncorrected ratios, indicating successful batch harmonization across injection sequences.
- If calibration lines present: assays include a concentrations column with calculated absolute values (non-NA for samples in the calibration-line sample type, NA for others).

## Limitations

- Batch correction requires pooled study quality control (SQC) samples; analysis will fail or produce invalid results if QC replicates are absent or severely outlier-contaminated.
- Only one sample type can be used for absolute concentration calculation per analysis run; multiple sample types require separate invocations of doAnalysis.
- Outlier detection (Rosner test) is applied to QC samples; study samples are tested for mis-injections only via internal standard areas, not via a formal outlier test on compound ratios.
- Internal standard assignment must be specified a priori in the input data; mzQuality does not automatically infer optimal internal standard pairing.
- Correction factors are derived from median ratios in pooled SQC samples; sparse or highly variable QC data may yield unreliable batch factors.

## Evidence

- [other] doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio, tests Study Samples for mis-injections using Internal Standard areas, and produces a ratio_corrected assay in the output experiment.: "doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using"
- [intro] mzQuality features outlier detection, batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds, various plots for inspecting, and generating reports for further processing.: "batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds"
- [other] Invoke doAnalysis with parameters removeOutliers=TRUE to flag QC sample outliers based on Compound/Internal Standard ratios, useWithinBatch=TRUE to apply batch correction using pooled study quality control samples, and removeBadCompounds=TRUE to filter compounds failing quality thresholds.: "useWithinBatch=TRUE to apply batch correction using pooled study quality control samples"
- [readme] The function `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC): "Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC)"
- [other] Generate output SummarizedExperiment containing the 'ratio_corrected' assay with batch-corrected compound/internal-standard ratios and metadata annotations marking detected outliers and mis-injected study samples (identified via internal standard areas).: "Generate output SummarizedExperiment containing the 'ratio_corrected' assay with batch-corrected compound/internal-standard ratios"
- [other] Note that in the current version of mzQuality, only one sample type can be used for calculating concentrations.: "only one sample type can be used for calculating concentrations"
