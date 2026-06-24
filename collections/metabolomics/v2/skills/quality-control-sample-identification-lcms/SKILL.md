---
name: quality-control-sample-identification-lcms
description: Use when when you have XCMS-preprocessed LC-MS metabolomics data with
  a peak table and an accompanying covariate/metadata file that contains a 'SampleType'
  column, and you plan to apply QC-based quality filters (such as RSD filtering) or
  train classifiers for peak quality assessment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetaClean
  - XCMS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- getEvalObj is called to extract the relevant data from the three objects provided
  by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
- MetaClean is a package for building classifiers to identify low quality integrations
  in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package
  `caret`) for building a predictive model.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-sample-identification-lcms

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and extract quality control (QC) sample column names from a metabolomics covariate file to enable downstream QC-based filtering and peak quality metric calculation in LC-MS workflows. This is a prerequisite step for optional RSD-based filtering and classifier training in MetaClean.

## When to use

When you have XCMS-preprocessed LC-MS metabolomics data with a peak table and an accompanying covariate/metadata file that contains a 'SampleType' column, and you plan to apply QC-based quality filters (such as RSD filtering) or train classifiers for peak quality assessment. QC samples are required to establish variability thresholds for extracted ion chromatograms.

## When NOT to use

- Input metabolomics data lacks a covariate/metadata file with SampleType annotations — QC identification requires explicit metadata.
- Study design includes no quality control replicates or all samples are of a single type — RSD-based filtering requires multiple QC measurements.
- Peak table is already filtered or collapsed to features — QC identification operates on raw per-sample peak columns.

## Inputs

- XCMS peakTable (data frame with peak-level measurements)
- covariate file (metadata file with SampleType column; delimited text format)

## Outputs

- vector of QC sample column names (character vector matching peak table column names)
- QC sample identifier list (for use in rsdFilter() and getPeakQualityMetrics())

## How to apply

Parse the covariate file (typically a comma- or tab-delimited file) and filter rows where the 'SampleType' column equals 'LQC' (label quality control sample). Extract the corresponding sample column names or identifiers from these rows. This vector of QC sample names is then passed to downstream MetaClean functions such as rsdFilter() to compute relative standard deviation across QC replicates and remove EICs exceeding a user-specified RSD threshold (default 0.3). The rationale is that QC samples represent technical replicates and their within-group variability indicates measurement reliability; EICs with high RSD in QC samples are flagged as unstable and removed before peak quality metric calculation and classifier training.

## Related tools

- **MetaClean** (Consumes QC sample identifiers in rsdFilter() and getPeakQualityMetrics() functions to filter and evaluate EICs based on QC replicate variability) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Upstream preprocessing tool that generates the peak table merged with sample columns; MetaClean integrates with XCMS output)
- **R** (Scripting environment in which covariate parsing and QC sample filtering are performed)

## Examples

```
# Load covariate file and extract QC sample names
covariate <- read.csv('covariate_file.csv')
qc_samples <- covariate$SampleName[covariate$SampleType == 'LQC']
# Pass to rsdFilter
filtered_peaks <- rsdFilter(peakTable = pqm, eicColumn = 'EICNo', qcSamples = qc_samples, rsdThreshold = 0.3)
```

## Evaluation signals

- QC sample vector length > 0 and all elements match column names in the peak table (schema validation).
- All retained QC sample rows have SampleType == 'LQC'; no samples with other SampleType values are included.
- Downstream rsdFilter() call accepts the QC vector without error and produces an output peak table with EICs retained/removed consistent with the RSD threshold.
- Peak quality metrics computed over QC samples show expected statistical properties (e.g., within-QC RSD < between-sample variation for stable analytes).
- QC sample count is consistent with study design (e.g., expected number of technical replicates per batch).

## Limitations

- QC sample identification depends on consistent and accurate SampleType labeling in the covariate file; mislabeled samples will be missed or incorrectly included.
- The skill assumes a single QC label ('LQC'); studies using multiple QC types (e.g., 'HQC', 'MQC', 'LQC') may require filtering on a subset or repeated application.
- QC sample identification alone does not validate peak quality; it only enables downstream QC-based filtering and metric calculation in MetaClean.
- If the covariate file is missing or incomplete, no QC samples can be identified and optional RSD filtering cannot be applied.

## Evidence

- [other] Identify quality control sample column names from the covariate file (samples with SampleType='LQC'): "Identify quality control sample column names from the covariate file (samples with SampleType='LQC')"
- [other] Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3): "Call rsdFilter() with the peak table, EIC column name, vector of QC sample column names, and RSD threshold (default 0.3)"
- [methods] the user can optionally filter out EICs by RSD % using the rsdFilter() function: "the user can optionally filter out EICs by RSD % using the rsdFilter() function"
- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [readme] can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
