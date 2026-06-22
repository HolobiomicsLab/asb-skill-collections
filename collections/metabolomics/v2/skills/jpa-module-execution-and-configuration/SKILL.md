---
name: jpa-module-execution-and-configuration
description: Use when when you have raw LC-MS data in mzXML format (or vendor formats convertible via MS-Convert) and need to extract metabolic features as the first major step of untargeted metabolomics analysis. Choose MS1 peak picking for DDA/full-scan data;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - JPA
  - R
  - XCMS
  - CAMERA
  - MS-Convert
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

# JPA Module Execution and Configuration

## Summary

Execute JPA's modular feature extraction workflows (MS1 peak picking, MS2 recognition, or targeted list extraction) with appropriate parameter tuning and data format preparation. This skill ensures correct metabolomics feature identification by matching workflow choice to data type and configuring XCMS/JPA parameters for LC-MS raw data or pre-extracted feature tables.

## When to use

When you have raw LC-MS data in mzXML format (or vendor formats convertible via MS-Convert) and need to extract metabolic features as the first major step of untargeted metabolomics analysis. Choose MS1 peak picking for DDA/full-scan data; use MS2 recognition only after MS1 features are extracted and only for DDA datasets; use targeted list extraction when you have a predefined list of m/z and retention time targets. Do NOT apply these workflows to full-scan or DIA data using MS2 recognition, as the README explicitly warns against this.

## When NOT to use

- Do not use MS2 recognition when processing full-scan or DIA (data-independent acquisition) datasets; the README explicitly states 'Please do not use this function when processing full-scan or DIA data set!'
- Do not use custom.featureTable() if your input is already an aligned multi-sample feature table; this function is designed for single-sample CSV tables from external software (e.g., MS-DIAL)
- Do not apply these workflows if your data is in NetCDF or other non-mzXML formats without first converting via MS-Convert

## Inputs

- Raw LC-MS data files in mzXML format or vendor-native format (convertible via MS-Convert)
- CSV feature tables with columns: m/z, retention time (seconds), rtmin (seconds), rtmax (seconds), intensity
- MS2 spectral data (for MS2 recognition module, after MS1 extraction)

## Outputs

- Feature table (dataframe) with columns: mz, rt, rtmin, rtmax, maxo, sample, level (marked as 'PP' for peak picking or 'MR' for MS2 recognition)
- MSnbase object (R object containing mass spectrometry data and metadata)
- Structured feature table file (CSV or R object) suitable for downstream alignment and annotation

## How to apply

First, verify your raw data format and convert to mzXML if necessary using MS-Convert. Select the appropriate extraction module: for direct raw data processing, use XCMS.featureTable() with mz.tol (10 ppm typical), peakwidth (5–20 s range typical), snthresh (6 typical), prefilter thresholds, and noise floor parameters tuned to your instrument's baseline and expected peak width. For pre-existing feature tables in CSV format (mz, rt, rtmin, rtmax, intensity columns in seconds), use custom.featureTable() to standardize and re-pick peaks. MS2 recognition is optional and performed after MS1 features are extracted; it generates additional features (labeled 'MR') that can be added to the feature table. The README provides thresholdEstimate.R to estimate MR false-positive thresholds. Ensure all mzXML or CSV input files are in the same folder with no extraneous files. After feature extraction, alignment (Part 5) is mandatory for multi-sample analysis.

## Related tools

- **XCMS** (Embedded peak picking and feature detection algorithm for MS1 raw data processing; provides centWave and other peak-picking methods used internally by JPA) — https://rdrr.io/bioc/xcms/man/
- **CAMERA** (Adduct and metabolite annotation module invoked as Part 6 of the JPA workflow, post feature extraction)
- **MS-Convert** (Data format conversion tool to standardize vendor-native mass spectrometry raw data to mzXML format for JPA ingestion)
- **R** (Runtime environment for executing JPA functions and workflows; JPA is a pure R package)

## Examples

```
featureTable <- XCMS.featureTable(dir = "X:/Users/JPAtest_20210330/multiDDA", mz.tol = 10, ppm=10, peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100)
```

## Evaluation signals

- Feature table output contains the correct columns (mz, rt, rtmin, rtmax, maxo, sample, level) with no missing values in core columns
- Retention time values are in seconds (not minutes), and rtmin < rt < rtmax for every feature
- The 'level' column correctly marks MS1 peak-picked features as 'PP' and MS2-recognized features as 'MR'
- For multi-sample analyses, feature counts per sample are consistent with expected DDA complexity and instrument sensitivity; outlier samples can be flagged for troubleshooting
- Parameter choices (ppm tolerance, peakwidth, snthresh) match the instrument resolution and chromatographic gradient; verify via EIC inspection (Part 8) or manual peak review on representative features

## Limitations

- MS2 recognition cannot be used on full-scan or DIA datasets (incompatible scan type)
- All input mzXML files or CSV files must be in a single folder with no extraneous files, limiting flexibility in organizing large studies
- MS2 recognition threshold estimation requires external thresholdEstimate.R script (not shown in README truncation); threshold choice is empirical and dataset-dependent
- XCMS peak-picking parameters (ppm, peakwidth, snthresh, prefilter, noise) require prior knowledge of instrument response and may require manual tuning for new instruments or protocols
- The custom.featureTable() function requires input CSV files to follow a strict column order (mz, rt, rtmin, rtmax, intensity); conversion scripts (e.g., convertCSV.R for MS-DIAL) may be needed

## Evidence

- [readme] JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features.: "JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features."
- [readme] One or multiple mzXML files from LC-MS analyses can be read in and processed to extract MS1 PP features. 'JPA' accepts raw data in any vendor format that is compatible with MS-Convert.: "One or multiple mzXML files from LC-MS analyses can be read in and processed to extract MS1 PP features. 'JPA' accepts raw data in any vendor format that is compatible with MS-Convert."
- [readme] After PP features have been extracted, extracting features using MS2 recognition (labeled as 'MR') can be performed. This step is optional. Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set!"
- [readme] The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. Note: column 3 and column 4 are the retention time of the feature edges, and all three columns containing retention time information should be in seconds.: "all three columns containing retention time information should be in seconds"
- [readme] For multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "For multi-sample analysis, sample alignment is performed after feature extraction."
- [readme] The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The 'level' column shows the level of each feature.: "The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The 'level' column shows the level of each feature."
