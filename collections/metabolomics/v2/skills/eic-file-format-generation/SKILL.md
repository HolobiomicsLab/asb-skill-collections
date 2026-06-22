---
name: eic-file-format-generation
description: Use when after completing MS2 annotation in the JPA metabolomics workflow, when you have aligned feature data (feature matrix with m/z, retention time, intensity, and sample assignments) and need to extract and export EIC traces for individual features or feature subsets for external validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - JPA
  - R
  - XCMS
  techniques:
  - tandem-MS
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

# eic-file-format-generation

## Summary

Export extracted ion chromatogram (EIC) data from JPA-aligned metabolomics features into standardized file formats (CSV, netCDF, mzML) with complete metadata headers. This skill enables downstream visualization, validation, and sharing of feature-level chromatographic traces across samples.

## When to use

After completing MS2 annotation in the JPA metabolomics workflow, when you have aligned feature data (feature matrix with m/z, retention time, intensity, and sample assignments) and need to extract and export EIC traces for individual features or feature subsets for external validation, visualization, or archival.

## When NOT to use

- Input is unaligned, single-sample feature data; EIC export is designed for multi-sample aligned features.
- Raw mass spectrometry data is not available or accessible; EIC extraction requires querying raw data at specified m/z values.
- Feature metadata lacks retention time boundaries (rtmin, rtmax) or m/z precision; export validation will fail without these fields.

## Inputs

- aligned feature table (feature matrix with m/z, retention time, intensity, sample assignments)
- raw or processed mass spectrometry data (mzXML, mzML, or vendor format compatible with MS-Convert)
- feature metadata (m/z values, retention time boundaries, sample identifiers)

## Outputs

- EIC export file (CSV, netCDF, or mzML format)
- EIC chromatogram objects (time vs. intensity traces)
- metadata-annotated EIC files with feature identifiers, m/z, retention time, and sample labels

## How to apply

Load the aligned feature data and feature metadata (m/z, retention time, intensity, sample identifiers) from the JPA feature table into the R environment using JPA data structures. For each feature or user-specified subset, query the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window (typically matching the ppm tolerance used in feature detection, e.g., 10 ppm). Extract ion chromatogram objects as time vs. intensity traces for each feature across selected samples. Generate EIC output by exporting the chromatogram data to JPA-supported file formats (CSV, netCDF, or mzML-compatible formats) with metadata headers including feature identifiers, m/z, retention time, and sample identifiers. Validate exported files for correct row/column structure, presence of all required metadata fields, and integrity before downstream use.

## Related tools

- **JPA** (comprehensive metabolomics data processing platform that contains the EIC export module and provides feature alignment, annotation, and chromatogram generation functions) — https://github.com/HuanLab/JPA.git
- **R** (runtime environment for executing JPA functions and data structures for feature loading, metadata parsing, and EIC generation)
- **XCMS** (embedded peak picking and chromatographic alignment engine within JPA used to generate the aligned features and retention time calibration) — https://rdrr.io/bioc/xcms/man/

## Evaluation signals

- Exported files contain all required metadata headers (feature ID, m/z, retention time, sample identifiers) and match the schema expected for the chosen format (CSV columns, netCDF dimensions, mzML XML structure).
- EIC chromatogram traces (time vs. intensity arrays) are non-empty and have valid numeric ranges for all selected features and samples; no NaN or infinite values are present.
- Row/column structure and row counts match the number of features exported and time points per chromatogram; file integrity passes format-specific validation tools (e.g., netCDF header checks, CSV row/column counts).
- m/z values in exported EICs match the feature table m/z ± mass tolerance window (e.g., ±10 ppm) and retention time boundaries align with rtmin/rtmax from input feature metadata.
- File size and content are consistent with expected data volume (number of features × number of samples × time points per chromatogram).

## Limitations

- EIC export requires raw or processed mass spectrometry data to be available; if raw data is inaccessible or in unsupported formats (not MS-Convert compatible), chromatogram extraction will fail.
- Mass tolerance window (ppm) and retention time boundaries must be correctly specified; mismatched or overly broad tolerance windows may yield noisy or artifact-contaminated EICs.
- Export is designed for post-MS2 annotation features in the JPA workflow; features generated from MS2 recognition (MR) or targeted list extraction (TL) may have incomplete metadata and cause validation failures.
- File format compatibility depends on downstream tools; netCDF and mzML exports may require specialized parsers and may not be readable in standard spreadsheet applications.

## Evidence

- [other] For each feature or user-specified subset, extract ion chromatograms by querying the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window.: "For each feature or user-specified subset, extract ion chromatograms by querying the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window."
- [other] Generate EIC chromatogram objects (time vs. intensity traces) for each feature across selected samples. Export EIC data to file format(s) supported by JPA (e.g., CSV, netCDF, or mzML-compatible formats) with metadata headers including feature identifiers, m/z, retention time, and sample identifiers.: "Export EIC data to file format(s) supported by JPA (e.g., CSV, netCDF, or mzML-compatible formats) with metadata headers including feature identifiers, m/z, retention time, and sample identifiers."
- [other] Validate output files for integrity, correct row/column structure, and presence of required metadata fields.: "Validate output files for integrity, correct row/column structure, and presence of required metadata fields."
- [readme] Part 8: Exporting EIC is positioned after Part 7: MS2 annotation in the workflow outline, confirming EIC export occurs post-annotation.: "Part 7: MS2 annotation ... Part 8: Exporting EIC"
- [other] Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures.: "Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures."
