---
name: spectral-feature-table-generation
description: Use when you have raw LC-MS data in mzXML format (or vendor formats convertible via MS-Convert) and need to identify and quantify metabolic features before multi-sample alignment. Use MS1 peak picking for full-scan or DDA data to extract Gaussian and non-Gaussian shaped peaks;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
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

# spectral-feature-table-generation

## Summary

Extract metabolic features from LC-MS spectral data (MS1 or MS2) and organize them into a structured feature table containing m/z, retention time, and intensity values. This is a foundational preprocessing step in untargeted metabolomics that enables downstream alignment, annotation, and statistical analysis.

## When to use

Apply this skill when you have raw LC-MS data in mzXML format (or vendor formats convertible via MS-Convert) and need to identify and quantify metabolic features before multi-sample alignment. Use MS1 peak picking for full-scan or DDA data to extract Gaussian and non-Gaussian shaped peaks; use MS2 recognition only after MS1 peak picking is complete, and do NOT apply to full-scan or DIA datasets.

## When NOT to use

- Do not use MS2 recognition when processing full-scan or DIA (data-independent acquisition) datasets
- Do not apply this skill if you already have an aligned feature table from multi-sample analysis; feature extraction is performed on single-sample or raw data only
- Do not skip m/z tolerance and peak-width parameter configuration; default values may not suit your chromatographic resolution or mass accuracy

## Inputs

- mzXML file(s) from LC-MS analyses
- CSV feature table(s) with columns: m/z, retention time, min retention time, max retention time, intensity

## Outputs

- Feature table dataframe (columns: mz, rt, rtmin, rtmax, maxo, sample, level)
- Structured CSV feature table for downstream analysis

## How to apply

Load raw mzXML file(s) or user-prepared CSV feature tables into JPA using the XCMS.featureTable() function (for raw LC-MS data) or custom.featureTable() function (for pre-processed CSV input). Configure peak-picking parameters including m/z tolerance (ppm), peak width range (seconds), signal-to-noise threshold (snthresh), and prefilter criteria (minimum number of peaks, minimum intensity). The function outputs a dataframe with columns: m/z, retention time (rt), minimum/maximum retention time boundaries (rtmin, rtmax in seconds), maximum intensity (maxo), sample ID, and feature level (PP for peak picking or MR for MS2 recognition). For MS2 recognition, apply after PP features are obtained; estimate a threshold using the provided thresholdEstimate.R code to filter true positives. Save the resulting feature table as a structured CSV file for alignment and annotation workflows.

## Related tools

- **JPA** (R package that executes MS1 peak picking and MS2 recognition via XCMS.featureTable() and MS2.recognition() functions to extract metabolic features from raw LC-MS data) — https://github.com/HuanLab/JPA.git
- **XCMS** (Underlying algorithm for peak picking and feature detection embedded in JPA; provides configurable parameters for m/z tolerance, peak width, noise thresholds)
- **MS-Convert** (Tool for converting raw vendor-format MS files to mzXML format compatible with JPA)

## Examples

```
featureTable <- XCMS.featureTable(dir = "X:/Users/JPAtest_20210330/multiDDA", mz.tol = 10, ppm=10, peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100)
```

## Evaluation signals

- Output dataframe contains all required columns (mz, rt, rtmin, rtmax, maxo, sample, level) with no missing values
- Feature count and intensity distributions are consistent with expected metabolic complexity for the organism/tissue type
- m/z values fall within the expected mass range for the instrument (e.g., 50–1200 m/z for typical metabolomics); retention times span the full chromatographic gradient
- For MS2 recognition features, verify that threshold-filtered MR features have cosine similarity or spectral match scores exceeding the estimated threshold value
- Comparison of feature counts: PP features should be substantially more numerous than MR features (MR is optional supplementary extraction)

## Limitations

- MS2 recognition should NOT be used on full-scan or DIA data, only on DDA (data-dependent acquisition) datasets with MS2 spectra
- Peak picking performance depends critically on parameter tuning (mz.tol, ppm, peakwidth, snthresh, prefilter); suboptimal settings can result in missed features or false positives
- The method extracts features from individual samples; multi-sample alignment is a separate downstream step required before statistical comparison
- CSV input tables must follow strict column order (m/z, retention time, rtmin, rtmax, intensity) and all retention times must be in seconds; conversion helpers are provided for MS-DIAL output but other formats require custom adaptation

## Evidence

- [readme] JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features.: "JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features."
- [readme] JPA supports multiple ways to extract metabolic features (labeled as 'PP') using peak picking algorithms. Users can choose to extract metabolic features directly from raw LC-MS data using the embedded XCMS functions: "JPA supports multiple ways to extract metabolic features (labeled as "PP") using peak picking algorithms. Users can choose to extract metabolic features directly from raw LC-MS data using the"
- [readme] The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The 'level' column shows the level of each feature.: "The XCMS.featureTable() function outputs a dataframe formatted featuretable as well as an MSnbase object. The "level" column shows the level of each feature."
- [readme] Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set!"
- [readme] The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. Note: column 3 and column 4 are the retention time of the feature edges, and all three columns containing retention time information should be in seconds.: "The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. Note: all three columns containing retention time"
