---
name: batch-effect-assessment-via-quality-metrics
description: Use when when you have processed metabolomics LC-MS/MS data organized by batch and sample type (including pooled QC replicates), and you need to quantify whether batch-to-batch and matrix effects are acceptable for downstream reporting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
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

# batch-effect-assessment-via-quality-metrics

## Summary

Assess batch effects in metabolomics mass spectrometry data by calculating quality metrics (RSDQC, background signal percentage, matrix effect, presence in QC samples) on pooled study quality control (SQC) samples and applying configurable thresholds to flag unreliable compounds and samples. This skill identifies which analytes and injections are affected by systematic variation and aids in selecting reportable results.

## When to use

When you have processed metabolomics LC-MS/MS data organized by batch and sample type (including pooled QC replicates), and you need to quantify whether batch-to-batch and matrix effects are acceptable for downstream reporting. Specifically, when you have a SummarizedExperiment object with internal-standard-normalized peak areas and you need to decide which compounds meet quality thresholds (e.g., RSDQC ≤ 15–30%, background signal ≤ 40%) and which samples are statistical outliers.

## When NOT to use

- Input data lacks replicated QC samples or does not distinguish batch structure—batch effect assessment requires multiple QC injections per batch to estimate RSDQC.
- Sample data is already pre-filtered or subset to only high-confidence compounds—re-applying this skill will override prior curation and may reintroduce unreliable analytes.
- Input is already a feature abundance table without internal standards or IS-normalized ratios—the skill requires compound/IS ratios to calculate RSDQC and batch-corrected values.

## Inputs

- SummarizedExperiment object with normalized peak areas (assays), internal standard assignments (rowData), sample type and batch metadata (colData)
- Pooled study quality control (SQC) sample replicates within the experiment
- Known or estimated internal standard concentrations (optional, for absolute quantification)

## Outputs

- Updated SummarizedExperiment with new assays: ratio (compound/IS), ratio_corrected (batch-corrected ratio), background_percentage, matrix_effect, presence, and median_area
- rowData column 'use' (TRUE/FALSE) indicating compound reliability based on RSDQC, background, and presence thresholds
- colData column 'use' (TRUE/FALSE) indicating sample reliability based on Rosner Test outlier detection on QC ratios
- Quality metric summaries (RSDQC values, background percentages, matrix effects per compound)

## How to apply

First, compute batch-corrected compound/internal-standard ratios using pooled SQC samples as the reference, then calculate RSDQC (relative standard deviation of QC samples) for each compound to quantify batch variability. In parallel, compute the background signal percentage by comparing blank/matrix samples to study samples, and assess matrix effect and presence (frequency) of each compound in QC samples. Apply the Rosner Test to QC sample ratios to identify statistical outliers among samples. Use configurable thresholds—commonly RSDQC ≤ 15–30%, background ≤ 40%, and presence > 70% in QCs—to assign a `use` flag (TRUE/FALSE) in both rowData (compounds) and colData (samples). Compounds and samples flagged FALSE are considered unreliable and should be excluded from final reports.

## Related tools

- **mzQuality** (Core R package that implements doAnalysis() to compute all batch and quality metrics (RSDQC, background, matrix effect, presence) and assign use flags based on thresholds) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor object class used to store assays (peak areas, ratios, batch-corrected values), rowData (compound-level metrics and use flags), and colData (sample-level metadata and use flags))
- **R** (Scripting language for executing doAnalysis() and accessing rowData/colData use flags to subset the experiment)
- **mzQualityDashboard** (Interactive Shiny application for visualizing batch effect metrics, QC sample distributions, and setting/adjusting quality thresholds without programming) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE, removeBadCompounds = TRUE, cautionRSD = 15, nonReportableRSD = 30, backgroundPercent = 40); exp_filtered <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- The doAnalysis() call completes successfully and produces non-NA RSDQC, background_percentage, matrix_effect, and presence values in rowData for all compounds.
- The rowData 'use' column contains only TRUE/FALSE values; manually inspect that compounds flagged FALSE have RSDQC > threshold, background > threshold, or presence < threshold (verify consistency with thresholds passed to doAnalysis).
- The colData 'use' column contains only TRUE/FALSE values; QC samples flagged FALSE should correspond to statistical outliers detected by the Rosner Test on compound/IS ratios (e.g., values >2–3 SD from median).
- After subsetting via `exp[rowData(exp)$use, exp$use]`, the resulting experiment contains only compounds and samples meeting all quality criteria; verify dimensions match expected counts of reportable analytes and samples.
- RSDQC values for batch-corrected ratios should be lower than raw (uncorrected) ratios, confirming that batch correction via SQC samples improved reproducibility.

## Limitations

- In the current version of mzQuality, only one sample type can be used for calculating concentrations; absolute quantification is not compatible with mixed sample type designs.
- The Rosner Test for outlier detection requires sufficient QC replicates per batch; sparse QC sampling may reduce power to detect true outliers.
- Thresholds for RSDQC, background_percentage, and presence are user-configurable but not data-adaptive; poor threshold choices (e.g., too permissive) may pass unreliable compounds, and too strict thresholds may discard valid analytes.
- Batch-correction assumes that pooled SQC samples are representative of the entire batch and that their composition is consistent across batches; violations (e.g., instrument drift, QC prep variation) can lead to over- or under-correction.

## Evidence

- [intro] RSDQC calculation for internal standard recommendation: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's."
- [readme] doAnalysis workflow including batch correction and QC metrics: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
- [readme] Use flag assignment based on quality metrics: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [intro] Outlier detection on QC samples via Rosner Test: "For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples."
- [other] Task validation of directory structure and report files: "Verify that the output directory contains a Plots subdirectory with quality-control visualizations and a Reports subdirectory with tab-delimited text files and human-friendly Excel exports."
