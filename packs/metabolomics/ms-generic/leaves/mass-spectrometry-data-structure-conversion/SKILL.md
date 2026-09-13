---
name: mass-spectrometry-data-structure-conversion
description: Use when when you have received metabolomics mass-spectrometry data in
  vendor-native or open formats (.raw, .d, mzXML) and need to ingest it into SMART
  for preprocessing, peak detection, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - R
  - SMART
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# mass-spectrometry-data-structure-conversion

## Summary

Convert raw mass-spectrometry metabolomics data files (.raw, .d, mzXML) into a unified in-memory data structure containing extracted metadata, spectral intensities, mass-to-charge ratios, and retention times. This enables downstream preprocessing, visualization, and statistical analysis within a consistent analytical framework.

## When to use

When you have received metabolomics mass-spectrometry data in vendor-native or open formats (.raw, .d, mzXML) and need to ingest it into SMART for preprocessing, peak detection, or statistical analysis. Apply this skill as the first step in the workflow before any data visualization, quality control, or downstream analysis.

## When NOT to use

- Data is already in a preprocessed, standardized matrix format (e.g., peak intensity table, feature abundance matrix); skip directly to quality control or statistical analysis.
- The input file format is not among the supported formats (.raw, .d, mzXML); custom parsing or format conversion is required first.
- Metadata and spectral information have already been extracted and validated in a prior analysis step.

## Inputs

- Raw mass-spectrometry data file in .raw format (vendor-native, e.g., Thermo)
- Raw mass-spectrometry data file in .d format (vendor-native, e.g., Agilent)
- Raw mass-spectrometry data file in mzXML format (open XML standard)

## Outputs

- Unified in-memory data structure with extracted metadata
- Spectral intensity matrix (m/z × retention time)
- Canonical export format compatible with downstream SMART modules

## How to apply

Using R file-handling functions, parse the input metabolomics data file in one of the supported formats (.raw, .d, or mzXML). Extract metadata and spectral data—specifically mass-to-charge ratios, intensities, and retention times—into a unified data structure. Validate the loaded data structure for completeness and format consistency to ensure all required fields are populated and conform to expected ranges. Export the in-memory representation in a canonical format suitable for the downstream preprocessing and visualization modules. The conversion ensures that heterogeneous vendor formats are reconciled into a single analytical schema, eliminating format-specific parsing logic in downstream steps.

## Related tools

- **R** (Language for file-handling functions to parse vendor-native and open mass-spectrometry data formats and construct unified data structures) — https://www.r-project.org
- **SMART** (Integrated metabolomics analysis platform that consumes the converted data structure for downstream preprocessing, visualization, and statistical analysis) — https://github.com/YuJenL/SMART

## Evaluation signals

- Verify that all records in the input file have been parsed without errors or data loss; check record count matches source file.
- Validate that metadata fields (e.g., sample ID, acquisition date, instrument parameters) are present and non-null.
- Confirm that mass-to-charge ratios (m/z) and retention times are within expected instrument ranges (e.g., m/z > 0, retention time ≥ 0).
- Check that intensity values are numeric, non-negative, and span appropriate dynamic range for the instrument.
- Ensure the canonical export format can be successfully loaded and processed by SMART's Data Visualization and Preprocessing modules without schema or type errors.

## Limitations

- Only three vendor/open formats are supported (.raw, .d, mzXML); other formats (NetCDF, .ms, proprietary binary) require separate parsing logic.
- Metadata extraction depends on the presence and structure of header information in the source file; malformed or incomplete headers may result in missing or partial metadata.
- No changelog available in the repository; version-specific format changes or parsing rule updates are not documented.
- The conversion assumes complete and valid spectral data; corrupted data points or incomplete scans may pass validation if individual fields are non-null.

## Evidence

- [other] Parse input metabolomics data file in one of the supported formats: "Parse input metabolomics data file in one of the supported formats (.raw, .d, or mzXML) using R file-handling functions."
- [other] Extract metadata and spectral data into unified structure: "Extract metadata and spectral data (mass-to-charge ratios, intensities, retention times) into a unified data structure."
- [other] Validate the loaded data structure: "Validate the loaded data structure for completeness and format consistency."
- [other] Export in canonical format for downstream modules: "Export the in-memory representation in a canonical format suitable for downstream preprocessing and visualization modules."
- [readme] Data Import module analyzes different formats: "Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML)."
- [readme] SMART streamlines complete analysis flow: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis"
