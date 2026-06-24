---
name: multi-format-data-ingestion
description: Use when you have raw metabolomics data files in one or more of the supported
  formats (.raw from Thermo instruments, .d directories from Agilent, or mzXML open-format
  exports) and need to ingest them into SMART for preprocessing, visualization, or
  statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - R GUI / SMART
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-format-data-ingestion

## Summary

Load and parse metabolomics data files in heterogeneous formats (.raw, .d, mzXML) into a unified in-memory data structure, extracting metadata, mass-to-charge ratios, intensities, and retention times for downstream preprocessing and visualization. This skill bridges raw instrument outputs to standardized analytical workflows.

## When to use

Apply this skill when you have raw metabolomics data files in one or more of the supported formats (.raw from Thermo instruments, .d directories from Agilent, or mzXML open-format exports) and need to ingest them into SMART for preprocessing, visualization, or statistical analysis. Use it as the mandatory first step before any peak detection, quality control, or batch effect exploration.

## When NOT to use

- Input is already in a standardized, validated feature table (e.g., peak intensity matrix aligned across samples) — skip directly to preprocessing or statistical analysis.
- Data has already been processed through peak detection and aligned across multiple samples — use the peak table as input to quality control or statistical modules instead.
- Only summary statistics or already-aggregated results are available (no raw spectral arrays) — this skill requires raw or near-raw instrument output.

## Inputs

- Thermo .raw file
- Agilent .d directory (binary format)
- mzXML file (XML-based open format)
- Mass spectrometry metadata (instrument, acquisition parameters)

## Outputs

- Unified data structure (matrix or data frame) with extracted m/z, intensity, retention time columns
- Metadata annotations (instrument type, acquisition date, sample ID)
- Validated spectral data ready for downstream preprocessing

## How to apply

Identify the format of your input metabolomics file(s). Parse the file using R file-handling functions appropriate to the format: .raw files typically require vendor-specific parsers, .d directories contain binary subdirectories requiring specialized readers, and mzXML files can be parsed as XML. Extract metadata (instrument parameters, acquisition conditions) and spectral arrays (m/z values, intensities, retention times) into a unified data structure with consistent column names and value types. Validate the loaded structure for completeness (no missing m/z-intensity pairs), numeric type consistency, and retention time ordering. Export the in-memory representation in SMART's canonical format (typically a matrix or data frame indexed by m/z and retention time) to serve as input for the Data Visualization, Peak Analysis, or Data Preprocessing modules.

## Related tools

- **R** (Primary language for file parsing, data extraction, and structure validation using file-handling functions) — https://www.r-project.org
- **R GUI / SMART** (User-friendly interface and canonical target format for ingested metabolomics data; orchestrates downstream preprocessing and visualization) — https://github.com/YuJenL/SMART

## Evaluation signals

- All m/z-intensity pairs from the raw file are present in the output structure with no truncation or silent loss.
- Retention times are monotonically increasing (or at least consistently ordered) across the spectral array.
- Numeric values (m/z, intensity, retention time) are in expected ranges (e.g., m/z typically 50–1000 for small molecules, intensities ≥ 0, retention time ≥ 0).
- Metadata fields (instrument type, sample ID, acquisition date) are extracted and match the source file header or directory metadata.
- The output structure can be successfully read by the Data Visualization module without type errors or missing-value exceptions.

## Limitations

- Format support is limited to .raw, .d, and mzXML; other vendor formats (e.g., .ms, .raw from other instruments) are not supported.
- Vendor-specific binary formats (.raw, .d) may require proprietary or third-party parsing libraries not bundled with SMART; availability depends on OS and library installation.
- Large files (> 1 GB) may exhaust available memory during in-memory representation; no chunked or streaming ingestion is described.
- Metadata extraction fidelity depends on the completeness and consistency of headers in the source file; corrupted or non-standard files may yield incomplete annotations.

## Evidence

- [other] The Data Import module is designed to analyze different data file formats including .raw, .d, and mzXML formats.: "The Data Import module is designed to analyze different data file formats including .raw, .d, and mzXML formats."
- [other] Parse input metabolomics data file in one of the supported formats (.raw, .d, or mzXML) using R file-handling functions. Extract metadata and spectral data (mass-to-charge ratios, intensities, retention times) into a unified data structure. Validate the loaded data structure for completeness and format consistency. Export the in-memory representation in a canonical format suitable for downstream preprocessing and visualization modules.: "Parse input metabolomics data file in one of the supported formats (.raw, .d, or mzXML) using R file-handling functions. Extract metadata and spectral data (mass-to-charge ratios, intensities,"
- [intro] SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis"
- [readme] Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML).: "Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML)."
- [readme] SMART written in R and R GUI has been developed as user-friendly software for integrated analysis of metabolomics data.: "SMART written in R and R GUI has been developed as user-friendly software for integrated analysis of metabolomics data."
