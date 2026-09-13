---
name: metabolomics-feature-extraction-and-export
description: 'Use when you have raw LC-MS data (mzXML format or pre-computed feature
  tables from external software) and need to: (1) detect both Gaussian and non-Gaussian
  shaped metabolic features across multiple samples, (2) align these features across
  samples, and (3) export EIC chromatograms with m/z.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
  - CAMERA
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-extraction-and-export

## Summary

Extract metabolic features from LC-MS data using JPA's peak picking and MS2 recognition algorithms, then export extracted ion chromatograms (EICs) with feature metadata to standard file formats. This skill bridges feature discovery and downstream validation by producing annotated EIC traces across aligned samples.

## When to use

Apply this skill when you have raw LC-MS data (mzXML format or pre-computed feature tables from external software) and need to: (1) detect both Gaussian and non-Gaussian shaped metabolic features across multiple samples, (2) align these features across samples, and (3) export EIC chromatograms with m/z, retention time, and sample metadata for manual validation or integration into publication-quality figures.

## When NOT to use

- Input is already an aligned feature table from another tool — skip directly to alignment validation or MS2 annotation; do not re-extract features
- Processing full-scan or DIA (data-independent acquisition) datasets — the MS2 recognition step (Part 3) explicitly should not be used for these modalities
- Raw data lacks time-of-flight or Orbitrap-level mass resolution — feature extraction reliability degrades below ~5 ppm mass accuracy required for m/z-based EIC extraction

## Inputs

- raw LC-MS data files in mzXML format (vendor-neutral, converted via MS-Convert)
- pre-computed feature table in CSV format (m/z, rt, rtmin, rtmax, intensity columns)
- aligned feature matrix from JPA sample alignment step
- feature metadata (m/z, retention time, sample assignments)

## Outputs

- feature table dataframe (mz, rt, rtmin, rtmax, maxo/intensity, sample, level columns)
- EIC chromatogram objects (time vs. intensity traces per feature per sample)
- exported EIC data files (CSV, netCDF, or mzML format with metadata headers)

## How to apply

First, load raw mzXML files or a pre-formatted CSV feature table (columns: m/z, retention time, rtmin, rtmax, intensity) into JPA using either XCMS.featureTable() for raw data or custom.featureTable() for external software outputs. Configure peak picking parameters (mz.tol, ppm tolerance, peakwidth, snthresh, prefilter thresholds) based on your instrument resolution and expected feature width. For multi-sample experiments, perform sample alignment (Part 5 in JPA workflow) to synchronize features across retention time drift. After optional MS2 annotation, extract EICs by querying the raw MS data at each feature's m/z value within a defined mass tolerance window, generating time-vs-intensity traces for each feature across selected samples. Export the resulting EIC objects to CSV, netCDF, or mzML-compatible formats, ensuring metadata headers include feature identifiers, m/z, retention time, and sample identifiers. Validate output files for correct row/column structure and presence of all required metadata fields.

## Related tools

- **JPA** (primary metabolomics processing framework; implements peak picking (XCMS), alignment, EIC extraction, and export) — https://github.com/HuanLab/JPA.git
- **XCMS** (embedded peak picking algorithm for MS1 feature detection; called by XCMS.featureTable() function) — https://rdrr.io/bioc/xcms/man/
- **CAMERA** (optional post-extraction adduct and isotope annotation module (Part 6 of JPA workflow))
- **R** (runtime environment and language for JPA package; requires version 4.0.0 or above)

## Examples

```
library(JPA); featureTable <- XCMS.featureTable(dir = "path/to/mzXML/files", mz.tol = 10, ppm=10, peakwidth=c(5,20), snthresh = 6, prefilter = c(3,100), noise = 100)
```

## Evaluation signals

- Feature table contains expected columns (mz, rt, rtmin, rtmax, maxo, sample, level) with non-null values and consistent numeric ranges (e.g., rt > 0, mz > 50, rtmin < rt < rtmax)
- Peak picking recovers known metabolite standards at expected m/z ± ppm tolerance and retention time ± drift window post-alignment
- EIC export files validate schema: correct row/column structure, feature identifiers match input feature table, m/z and rt metadata present and match source features
- Alignment corrects for inter-sample retention time drift (typically ±10–30 s); visual inspection of EIC traces shows aligned peaks across samples at consistent rt
- Output file integrity check passes: no truncated records, no missing metadata headers, CSV/netCDF format is parseable by downstream tools

## Limitations

- Peak picking is sensitive to parameter tuning (mz.tol, ppm, peakwidth, snthresh, prefilter); suboptimal values cause missed features or false positives; threshold estimation script provided on GitHub for DDA/DDA-only datasets
- MS2 recognition (Part 3) explicitly incompatible with full-scan and DIA data; attempting to use it on these modalities produces unreliable results
- EIC extraction accuracy depends on raw data availability and m/z calibration; if raw data files are absent or recalibration required, re-extraction may fail
- Alignment assumes sufficient feature overlap across samples; extreme sample-to-sample variability or small sample sets may produce poor alignment
- Custom feature table input requires strict column ordering (m/z, rt, rtmin, rtmax, intensity); helper script convertCSV.R provided only for MS-DIAL output format; other software outputs require manual format conversion

## Evidence

- [intro] JPA extracts both Gaussian and non-Gaussian shaped metabolic features and performs sample alignment, adduct and metabolite annotations.: "It extract both Gaussian and non-Gaussian shaped metabolic features. It also performs sample alignment, adduct and metabolite annotations."
- [readme] XCMS.featureTable() function accepts raw mzXML files with configurable peak picking parameters.: "featureTable <- XCMS.featureTable(dir = dir, mz.tol = 10, ppm=10, peakwidth=c(5,20), mzdiff = 0.01, snthresh = 6, integrate = 1, prefilter = c(3,100), noise = 100)"
- [other] EIC export is positioned after MS2 annotation in the processing pipeline with support for multiple output formats.: "JPA includes an EIC export capability as part of its comprehensive metabolomics data processing workflow, positioned after MS2 annotation in the processing pipeline."
- [other] EIC export generates time vs. intensity traces with required metadata for each feature across samples.: "Generate EIC chromatogram objects (time vs. intensity traces) for each feature across selected samples. Export EIC data to file format(s) supported by JPA (e.g., CSV, netCDF, or mzML-compatible"
- [readme] MS2 recognition step must not be used on full-scan or DIA data.: "Please do not use this function when processing full-scan or DIA data set!"
- [readme] Custom feature table input requires strict column format and per-sample CSV files.: "The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. For multi-sample analysis, a CSV feature table for each"
