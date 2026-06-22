---
name: background-contamination-threshold-assessment
description: Use when after batch correction of metabolomics data when you need to identify and remove compounds whose signal in background/blank samples exceeds a tolerable contamination level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-contamination-threshold-assessment

## Summary

Assess and filter metabolomics compounds based on background signal contamination levels relative to study samples. This skill applies a user-configurable background percentage threshold to flag compounds with excessive signal in blank/negative control samples, preventing false-positive identifications and ensuring reportable compound reliability.

## When to use

After batch correction of metabolomics data when you need to identify and remove compounds whose signal in background/blank samples exceeds a tolerable contamination level. Apply this skill when your SummarizedExperiment object contains assays with both study sample and background sample measurements, and you must decide which compounds are sufficiently clean to report.

## When NOT to use

- Your study design lacks background/blank sample measurements or control samples are not clearly designated in the data type column.
- You are working with non-targeted discovery metabolomics where background contamination is expected and not disqualifying (e.g., environmental samples without clean blanks).
- The background percentage threshold has already been applied in an upstream preprocessing pipeline and you are receiving pre-filtered compound lists.

## Inputs

- SummarizedExperiment object with batch-corrected assays from doAnalysis
- Assay matrix with background sample measurements
- Assay matrix with study sample measurements

## Outputs

- Updated rowData with backgroundPercentage values per compound
- Updated rowData 'use' column with TRUE/FALSE flags for compound reliability
- Tabulated report of removed compounds with background percentage values
- Diagnostic plots showing background signal distribution

## How to apply

Within the mzQuality `doAnalysis` workflow, set the `backgroundPercentage` threshold parameter (default and recommended: 40) to define the maximum tolerable background signal as a percentage of study sample signal. The function automatically calculates the ratio of background signal to study sample signal for each compound. Compounds exceeding this threshold are flagged by setting their `use` column in rowData to FALSE, indicating they are unreliable for reporting. The threshold filters compounds based on signal contamination alone; combine this filter with RSDQC and QC presence thresholds for comprehensive compound reliability assessment. Extract flagged compounds and generate diagnostic plots to verify that removed compounds genuinely show elevated background noise rather than true low-abundance metabolites.

## Related tools

- **mzQuality** (Performs background signal percentage calculation and applies backgroundPercentage threshold during compound filtering within doAnalysis function) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Container object storing assay matrices, rowData (compound-level metadata including use flags), and colData (sample-level metadata); required input/output format for mzQuality) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny interface for setting backgroundPercentage threshold, visualizing background contamination plots, and inspecting flagged compounds) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers=TRUE, removeBadCompounds=TRUE, backgroundPercentage=40); reportable_compounds <- exp[rowData(exp)$use, ]
```

## Evaluation signals

- Verify that rowData contains a new numeric column with background percentage values for all compounds (range 0–100).
- Confirm that rowData 'use' column is updated: compounds with backgroundPercentage ≤ threshold retain TRUE; compounds exceeding threshold are set to FALSE.
- Check diagnostic plots show clear separation between background-contaminated and clean compounds; flagged compounds should exhibit visibly elevated signal in blank/negative samples.
- Subset the SummarizedExperiment using `exp[rowData(exp)$use, exp$use]` and verify the remaining compound count decreases relative to input; tabulate the removed compounds with their background percentages to confirm they exceed the set threshold.
- Generate a report documenting the number of compounds removed by background contamination filtering and their background percentage distribution to confirm threshold was applied correctly.

## Limitations

- The backgroundPercentage threshold is compound-agnostic: a fixed cutoff (default 40%) applies uniformly across all compounds. Compounds with genuinely low abundance in study samples may be incorrectly flagged if background noise is high relative to weak true signal.
- Background contamination assessment depends on clear designation of background/blank sample types in the input data type column; mislabeled or missing background samples will produce unreliable filtering.
- The skill filters only on background contamination ratio and does not account for absolute signal intensity; a compound with 10 counts in background and 25 counts in study samples passes the 40% threshold but may still be near instrument noise floor.
- Interaction with other compound filters (RSDQC, QC presence thresholds) is multiplicative: applying strict backgroundPercentage in conjunction with stringent RSDQC (e.g., <20%) may eliminate too many compounds, especially in challenging matrices.
- No changelog or version history is published; threshold behavior and calculation method may change between package updates without explicit notification.

## Evidence

- [readme] Calculate the percentage of background signal compared to the study samples: "Calculate the percentage of background signal compared to the study samples"
- [other] Detection and filtering based on background thresholds: "removes bad compounds when called with removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40"
- [readme] It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples"
- [readme] The use column in rowData indicates if compound is reliable based on set thresholds: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [other] filters for removing unreliable compounds: "filters for removing unreliable compounds"
