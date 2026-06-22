---
name: ms2-spectrum-feature-extraction
description: Use when you have DDA (data-dependent acquisition) LC-MS/MS data with MS2 spectra and want to discover metabolic features that may be missed by MS1-only peak picking, or when you need an alternative feature extraction workflow that leverages fragmentation patterns to identify true metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
  - thresholdEstimate.R
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2-spectrum-feature-extraction

## Summary

Extract metabolic features directly from MS2 (tandem mass spectrometry) spectra using the JPA MS2 recognition module, generating a feature table with m/z, retention time, and intensity—an alternative to MS1 peak picking when MS2 spectral data is available and full-scan or DIA datasets are not being processed.

## When to use

You have DDA (data-dependent acquisition) LC-MS/MS data with MS2 spectra and want to discover metabolic features that may be missed by MS1-only peak picking, or when you need an alternative feature extraction workflow that leverages fragmentation patterns to identify true metabolite signals.

## When NOT to use

- Input is full-scan or DIA (data-independent acquisition) data — the README explicitly states 'Please do not use this function when processing full-scan or DIA data set'
- Only MS1 peak-picked features are available and no MS2 spectral data is present
- Feature extraction goal is to reproduce results from a published MS1-only pipeline without MS2 validation

## Inputs

- mzXML files from DDA LC-MS/MS analysis (one or multiple files in a single folder)
- Existing MS1 peak-picked feature table (optional; CSV format with columns: m/z, retention time, rtmin, rtmax, intensity)
- Raw LC-MS/MS data in vendor format convertible via MS-Convert

## Outputs

- Feature table (dataframe) with columns: mz, rt, rtmin, rtmax, maxo (intensity), sample, level (labeled 'MR')
- Combined feature table integrating both MS1 PP and MS2 MR features
- Structured output file for downstream alignment and annotation workflows

## How to apply

Load raw mzXML files or an existing MS1 peak-picked feature table into JPA using R. Execute the MS2 recognition module to identify features from MS2 spectra by comparing spectral patterns and intensity thresholds. A threshold for determining true positive MR (MS2 recognition) features should be estimated using the provided thresholdEstimate.R code on your dataset to tune sensitivity. The module outputs a feature table with m/z, retention time (rtmin, rtmax), and intensity columns, labeled with 'MR' level designation. These MR features are then combined with any existing PP (peak picking) features for downstream alignment and annotation.

## Related tools

- **JPA** (Comprehensive metabolomics data processing software providing MS2 recognition module for feature extraction from tandem MS spectra) — https://github.com/HuanLab/JPA.git
- **R** (Programming language in which JPA is written and executed; R ≥ 4.0.0 required)
- **XCMS** (Embedded algorithm used by JPA for peak picking on MS1 or custom feature tables; referenced for parameter details) — https://rdrr.io/bioc/xcms/man/
- **thresholdEstimate.R** (Provided R code to estimate the threshold for determining whether MS2 recognition features are true positives on your specific dataset) — https://github.com/HuanLab/JPA

## Examples

```
# After installing JPA and loading demo data:
library(JPA)
dir <- "X:/Users/JPAtest_20210330/multiDDA"
featureTable_PP <- XCMS.featureTable(dir = dir, mz.tol = 10, ppm=10, peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100)
featureTable_combined <- MS2recognition(featureTable = featureTable_PP, dir = dir)
```

## Evaluation signals

- Output feature table contains all required columns (mz, rt, rtmin, rtmax, maxo, sample, level) with no missing values in retention time or m/z fields
- All extracted features are labeled with 'MR' level designation in the 'level' column
- MS2 MR feature m/z values fall within expected range (typically 50–1500 m/z for small-molecule metabolomics)
- MS2 MR features with intensity (maxo) above the user-estimated threshold show agreement with manual MS2 spectral inspection or orthogonal validation
- Combined PP + MR feature table shows a superset of features compared to MS1 peak picking alone, validating that MS2 recognition identified additional true metabolites

## Limitations

- MS2 recognition should not be applied to full-scan or DIA datasets, as MS2 spectral topology differs fundamentally from DDA fragmentation patterns
- True positive threshold must be empirically estimated per dataset using thresholdEstimate.R; a universal cutoff does not exist and suboptimal thresholds lead to false positives or false negatives
- MS2 recognition produces feature-level annotations only; subsequent adduct and metabolite identification require separate CAMERA and MS2 annotation workflows
- Performance depends on MS2 spectral quality and coverage; samples with poor fragmentation or low MS2 scan density may yield sparse MR feature tables

## Evidence

- [readme] After PP features have been extracted, extracting features using MS2 recognition (labeled as "MR") can be performed. This step is optional. Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set!"
- [other] JPA provides MS2 recognition as a distinct feature extraction workflow component, positioned separately from MS1 peak picking, to generate feature tables through alternative analytical pathways.: "JPA provides MS2 recognition as a distinct feature extraction workflow component, positioned separately from MS1 peak picking"
- [readme] The threshold used for determining whether the MR features are true positive can be estimated by using the R code "thresholdEstimate.R" provided on the GitHub.: "The threshold used for determining whether the MR features are true positive can be estimated by using the R code "thresholdEstimate.R""
- [intro] JPA extracts both Gaussian and non-Gaussian shaped metabolic features. It also performs sample alignment, adduct and metabolite annotations.: "JPA extracts both Gaussian and non-Gaussian shaped metabolic features"
- [readme] One or multiple mzXML files from LC-MS analyses can be read in and processed to extract MS1 PP features. 'JPA' accepts raw data in any vendor format that is compatible with MS-Convert.: "'JPA' accepts raw data in any vendor format that is compatible with MS-Convert"
