---
name: quality-control-metric-threshold-configuration
description: Use when you have a SummarizedExperiment object from a metabolomics study with compound peak areas, internal standard assignments, and sample type annotations (QC, Study, Calibration, Blank), and you need to decide which samples and compounds are reportable.
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

# quality-control-metric-threshold-configuration

## Summary

Configure outlier detection and compound filtering thresholds in metabolomics quality control to flag non-reportable QC samples, mis-injected study samples, and unreliable compounds. This skill involves selecting and justifying parameter values (qcPercentage, backgroundPercentage, nonReportableRSD, Rosner Test statistics) that balance sensitivity and specificity for a given experiment.

## When to use

You have a SummarizedExperiment object from a metabolomics study with compound peak areas, internal standard assignments, and sample type annotations (QC, Study, Calibration, Blank), and you need to decide which samples and compounds are reportable. Apply this skill when your research question requires flagging outlier QC samples by Compound/Internal Standard ratio anomalies, detecting mis-injected study samples via Internal Standard area deviations, or removing compounds with high background contamination or poor reproducibility.

## When NOT to use

- Your metabolomics dataset lacks internal standard assignments or QC sample replicates; the thresholds depend on these for Compound/IS ratio calculation and batch correction.
- You are performing untargeted metabolomics feature detection where sample types are not clearly defined (no QC/Blank/Study annotations); the filtering relies on knowing sample roles.
- Your data has already been filtered by an external QC pipeline and you only need to export or visualize; re-configuring thresholds on pre-filtered data will compound filtering decisions.

## Inputs

- SummarizedExperiment object with compound peak areas in assay slot
- Internal Standard assignments in rowData or colData
- Sample type annotations (QC, Study Sample, Calibration, Blank) in colData
- Batch identifiers in colData
- Known internal standard areas for each sample

## Outputs

- SummarizedExperiment with 'use' column in rowData (TRUE/FALSE per compound)
- SummarizedExperiment with 'use' column in colData (TRUE/FALSE per sample)
- Tabulated outlier QC samples with aberrant Compound/Internal Standard ratios
- Tabulated removed compounds with RSD and background metrics
- Diagnostic plots (boxplots, PCA, violin plots) showing QC filtering outcome

## How to apply

Call the doAnalysis function on your SummarizedExperiment with four key parameter groups: (1) outlier removal flags (removeOutliers=TRUE, useWithinBatch=TRUE) to invoke statistical testing (Rosner Test) on QC sample ratios; (2) compound filtering thresholds (removeBadCompounds=TRUE, nonReportableRSD=30, qcPercentage=80, backgroundPercentage=40) that remove compounds failing reproducibility (RSD > 30% in QC samples) or present in fewer than 80% of QC replicates or with background signal exceeding 40% of study sample signal; and (3) internal standard-based mis-injection detection (automatic when removeOutliers=TRUE). The function adds a 'use' column to rowData (compounds) and colData (samples) with TRUE/FALSE values. Extract flagged samples and compounds, verify against diagnostic plots (boxplots of Compound/IS ratios, PCA of batch-corrected ratios, violin plots per sample type), and adjust thresholds upward (less stringent) if too many compounds or samples are rejected, or downward (more stringent) if unreliable data persist in the retained set.

## Related tools

- **mzQuality** (Primary R package that implements doAnalysis function and parameter configuration for threshold-based outlier detection and compound filtering) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny interface for configuring and visualizing threshold effects without programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **SummarizedExperiment** (Bioconductor container object that stores compound metadata (rowData), sample metadata and batch info (colData), and assays; required input and output format for mzQuality) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **R** (Execution environment for calling doAnalysis and threshold configuration; data wrangling and diagnostics)

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30); retained_exp <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- Verify that rowData(exp)$use and colData(exp)$use contain only TRUE or FALSE values after doAnalysis; no NAs or other values indicate schema integrity.
- Check that the number of compounds and samples retained matches the threshold intent: if nonReportableRSD=30 is intended to be strict, retained compounds should have median RSDQC ≤ ~25% and presence in QC ≥ 80%; if too many remain, lower the threshold.
- Generate boxplots of Compound/Internal Standard ratio by sample type and batch; outlier QC samples flagged as 'use'=FALSE should be visually anomalous (ratio >> or << median), confirming Rosner Test specificity.
- Tabulate background signal percentage (background_percentage in assay) for retained compounds; all values should be ≤ backgroundPercentage threshold (e.g., ≤ 40%), confirming compound contamination filtering.
- Verify internal standard area distributions across retained study samples are unimodal and centered; large outliers in Internal Standard area should correspond to colData 'use'=FALSE, confirming mis-injection detection.

## Limitations

- Thresholds are not data-adaptive; mzQuality applies user-specified fixed cutoffs (nonReportableRSD=30, qcPercentage=80, backgroundPercentage=40) regardless of study design, instrumentation, or matrix complexity. Users must manually adjust for different metabolite classes or sample matrices.
- Rosner Test for outlier QC samples assumes Gaussian distribution of log-transformed Compound/Internal Standard ratios; heavily skewed or multi-modal distributions may produce false negatives (missed outliers) or false positives (incorrectly flagged good QC replicates).
- The skill requires defined internal standards for every compound; if internal standard assignments are missing or incorrect, Compound/Internal Standard ratio calculation fails and outlier detection becomes unreliable.
- Background percentage calculation assumes blank sample availability; studies without blank injections cannot assess matrix contamination and backgroundPercentage filtering may not be applicable.
- Threshold configuration is a manual iterative process; no automated recommendation algorithm is documented in the README to suggest initial values based on data characteristics.

## Evidence

- [other] doAnalysis flags QC outliers by Compound/Internal Standard ratio, detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds.: "doAnalysis flags QC outliers by Compound/Internal Standard ratio, detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE,"
- [intro] The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio. Study Samples are tested for mis-injections using their Internal Standard areas. Filters for removing unreliable compounds.: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio. Study Samples are tested for mis-injections using their"
- [readme] It is likely that mzQuality deems some compounds and/or samples unreliable for reporting. It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in `doAnalysis`. For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples.: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [readme] mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [readme] The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC), 3. Calculate the percentage of background signal compared to the study samples.: "Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC), 3. Calculate the percentage of background"
