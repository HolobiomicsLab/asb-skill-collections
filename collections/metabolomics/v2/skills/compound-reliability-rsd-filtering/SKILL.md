---
name: compound-reliability-rsd-filtering
description: Use when after batch correction and internal standard ratio calculation
  when you have pooled study quality control (SQC) or pooled quality control (QC)
  samples and need to determine which compounds are sufficiently reliable for downstream
  reporting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  - xcms
  license_tier: open
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

# compound-reliability-rsd-filtering

## Summary

Filter metabolomics compounds for reportability based on relative standard deviation (RSD) of quality control samples, background signal percentage, and compound presence thresholds. This skill identifies and removes unreliable compounds that fail to meet reproducibility and signal quality criteria across pooled QC samples.

## When to use

Apply this skill after batch correction and internal standard ratio calculation when you have pooled study quality control (SQC) or pooled quality control (QC) samples and need to determine which compounds are sufficiently reliable for downstream reporting. Use it when compound-level variation (RSDQC), background contamination, or sparse detection in QC samples raises concerns about data integrity.

## When NOT to use

- When QC samples are not available or are too few to calculate stable RSD estimates (RSDQC becomes unreliable with n < 3 QC replicates).
- When the input is raw, unbatch-corrected data — apply batch correction first using SQC samples before filtering compounds by RSD.
- When compounds are already pre-filtered or curated by external standards — this skill may redundantly flag known biomarkers if thresholds are not tuned to your experiment.

## Inputs

- SummarizedExperiment object after batch correction (output from doAnalysis with batch-corrected ratios and internal standard calculations)
- QC sample measurements (pooled study quality control or pooled quality control samples with known internal standards)
- Background/blank sample measurements (for background signal percentage calculation)

## Outputs

- Updated SummarizedExperiment with rowData$use column (TRUE/FALSE per compound)
- Subset SummarizedExperiment containing only reportable compounds
- Tabulated report of removed/unreliable compounds with RSDQC, background percentage, and presence metrics

## How to apply

After calling doAnalysis with removeBadCompounds=TRUE, extract the `use` column from rowData(experiment) to identify compounds flagged as reliable (TRUE) or unreliable (FALSE). The filtering logic combines three criteria: (1) RSDQC (relative standard deviation of batch-corrected ratios in QC samples, typically threshold nonReportableRSD=30%); (2) background signal percentage (set via backgroundPercentage parameter, typically 40% — compounds exceeding this are flagged); and (3) compound presence in QC samples. Compounds failing any threshold are marked use=FALSE. You can override these automatic flags by manually setting rowData(experiment)$use to TRUE or FALSE before subsetting. Finally, subset the experiment to retain only reliable compounds via exp[rowData(exp)$use, ].

## Related tools

- **mzQuality** (Core R package that implements RSD-based compound filtering via the doAnalysis function with removeBadCompounds, nonReportableRSD, and backgroundPercentage parameters) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny application providing GUI-based access to compound filtering and threshold tuning without requiring R scripting) — https://github.com/hankemeierlab/mzQualityDashboard
- **SummarizedExperiment** (Bioconductor container class used throughout mzQuality to store assays, rowData (compound metadata), and colData (sample metadata))
- **xcms** (R-based metabolomics processing pipeline that outputs SummarizedExperiment objects compatible with mzQuality filtering)

## Examples

```
exp <- doAnalysis(exp = exp, removeBadCompounds=TRUE, nonReportableRSD=30, backgroundPercentage=40); exp_filtered <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- Verify rowData(exp)$use contains only TRUE or FALSE values and no NAs (or expected NAs only in edge cases).
- Confirm that compounds marked use=FALSE have RSDQC values above the nonReportableRSD threshold (e.g., > 30%), background percentage above backgroundPercentage (e.g., > 40%), or presence below expected thresholds in QC samples.
- Check that the subset exp[rowData(exp)$use, ] has fewer rows (compounds) than the original experiment, proportional to the applied thresholds.
- Verify that retained compounds (use=TRUE) show lower median RSDQC and background percentages compared to removed compounds when plotted or tabulated.
- Confirm that diagnostic plots (e.g., boxplots, violin plots of batch-corrected ratios for retained compounds) show tighter distributions and lower outlier frequency than the full dataset.

## Limitations

- RSD thresholds are global and applied uniformly to all compounds; compounds with legitimate biological variability may be incorrectly flagged if thresholds are too stringent.
- Background signal percentage depends on blank/negative sample quality; if blanks are contaminated or absent, this criterion cannot reliably filter.
- RSDQC calculation requires sufficient QC replicates (typically ≥ 3); studies with sparse QC sampling may produce unstable RSD estimates.
- Compound presence thresholds are heuristic; presence in < N% of QC samples does not always indicate unreliability (e.g., low-abundance compounds may be sporadic).
- Manual override of use flags (setting rowData(exp)$use=TRUE or FALSE) is unsupervised; there is no built-in validation to prevent reinclusion of truly unreliable compounds.

## Evidence

- [intro] mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes: "mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes"
- [intro] The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio and filters for removing unreliable compounds: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio; filters for removing unreliable compounds"
- [intro] mzQuality can recommend internal standards by calculating Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratios: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's"
- [other] doAnalysis flags QC outliers by Compound/Internal Standard ratio, detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds: "doAnalysis flags QC outliers by Compound/Internal Standard ratio, detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE,"
- [readme] It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in doAnalysis.: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [readme] mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is"
