---
name: outlier-detection-qc-sample-ratio-analysis
description: Use when after building a SummarizedExperiment object from metabolomics
  LC-MS data with QC and Study Sample types defined, when you need to identify QC
  samples with aberrant Compound/Internal Standard ratios (indicating instrument drift,
  matrix effects, or sample degradation) and Study Samples with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
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

# outlier-detection-qc-sample-ratio-analysis

## Summary

Detects and flags outlier Quality Control (QC) samples in metabolomics datasets by analyzing Compound/Internal Standard ratios using statistical tests, and simultaneously identifies mis-injected Study Samples via Internal Standard area anomalies. This filtering step removes unreliable samples before downstream reporting and interpretation.

## When to use

Apply this skill after building a SummarizedExperiment object from metabolomics LC-MS data with QC and Study Sample types defined, when you need to identify QC samples with aberrant Compound/Internal Standard ratios (indicating instrument drift, matrix effects, or sample degradation) and Study Samples with anomalous Internal Standard areas (indicating injection or instrumental failures) before concentration estimation or compound reliability assessment.

## When NOT to use

- When QC samples are not available in the dataset (the method requires QC replicates to establish normal ratio distribution).
- When Internal Standards have not been assigned to compounds prior to doAnalysis() execution.
- When the SummarizedExperiment object lacks sample type annotations (must distinguish QC from Study Samples).

## Inputs

- SummarizedExperiment object with assay containing raw compound and internal standard peak areas
- Defined sample type annotations (QC, Study Sample, Calibration, Background)
- Internal Standard assignments per compound

## Outputs

- SummarizedExperiment object with colData$use column (TRUE/FALSE) indicating sample reliability
- Flagged outlier QC sample identifiers and their Compound/Internal Standard ratios
- Flagged mis-injected Study Sample identifiers and their Internal Standard areas
- Diagnostic summary table of outliers with statistical test results

## How to apply

Load the prepared SummarizedExperiment into R and call doAnalysis() with removeOutliers=TRUE to activate outlier detection. The function calculates Compound/Internal Standard ratios for all samples, then applies the Rosner Test (a statistical outlier detection method) on QC sample ratios to flag statistical outliers. Simultaneously, it examines Internal Standard areas in Study Samples to detect mis-injections. Extract flagged samples from the result using colData(exp)$use==FALSE to retrieve outlier/mis-injected samples. Set the qcPercentage threshold (typically 80) to control sensitivity of QC flagging. Rationale: QC samples should cluster tightly in ratio space; large deviations indicate systematic problems affecting data quality, while Study Sample Internal Standard area anomalies suggest sample-specific injection or detection failures that invalidate that sample's measurements.

## Related tools

- **mzQuality** (Core R package providing doAnalysis() function for Rosner Test-based outlier detection and mis-injection flagging on QC and Study samples) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor object class for storing assays (peak areas), colData (sample metadata and use flags), and rowData (compound metadata)) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny application providing visual inspection and manual override of automatically flagged outliers and mis-injected samples) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers=TRUE, qcPercentage=80); outlier_samples <- exp[, !exp$use]; print(colData(outlier_samples)[c('aliquot', 'type')])
```

## Evaluation signals

- colData(exp)$use contains only TRUE/FALSE values with no missing entries after doAnalysis() execution
- Flagged outlier QC samples have Compound/Internal Standard ratios that deviate >2–3 standard deviations from the median QC ratio (verify via diagnostic plots)
- Flagged Study Samples have Internal Standard areas below or above expected range relative to batch median (inspect aliquotPlot output)
- Summary statistics show qcPercentage threshold (e.g., 80%) and count of removed samples; retained QC samples show reduced RSDQC (Relative Standard Deviation) relative to input
- Diagnostic PCA plots show improved clustering and reduced outlier separation after outlier removal

## Limitations

- Rosner Test assumes approximately normal distribution of QC ratios; severe non-normality (e.g., bimodal distributions from two instrument states) may reduce outlier detection sensitivity.
- Method requires sufficient QC replicates (typically ≥5 per batch) to establish reliable baseline; small QC cohorts may incorrectly flag normal biological or technical variation.
- Internal Standard area thresholds are fixed per batch; compounds or samples with genuine but extreme (non-pathological) Internal Standard values may be over-flagged.
- Does not account for time-series drift within a batch; if instrument performance degrades monotonically, late QC samples may not be flagged if they remain within Rosner Test bounds.
- Manual override via colData(exp)$use is possible but requires domain expertise; users unfamiliar with metabolomics QC interpretation may retain unreliable or remove valid samples.

## Evidence

- [other] Outlier QC detection by Compound/Internal Standard ratio: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio"
- [other] Study Sample mis-injection flagging via Internal Standard areas: "Study Samples are tested for mis-injections using their Internal Standard areas"
- [readme] doAnalysis function with removeOutliers parameter: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards"
- [readme] Rosner Test for statistical outlier detection: "For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples."
- [readme] use column for sample retention/flagging: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [other] qcPercentage threshold parameter: "doAnalysis is called with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds"
