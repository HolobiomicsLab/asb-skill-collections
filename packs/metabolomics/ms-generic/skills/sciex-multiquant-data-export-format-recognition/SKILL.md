---
name: sciex-multiquant-data-export-format-recognition
description: Use when you have txt files exported from Sciex MultiQuant (>v3.0.3) containing QCpool samples measured at regular intervals during mass spectrometry sequences, and you need to validate whether the file structure is compatible with the QComics package before parsing and quality assessment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Sciex Multiquant
  - R
  - Sciex Multiquant (> v3.0.3)
  - QComics
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format
- The goal of the `QComics` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics_cq
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03660
  all_source_dois:
  - 10.1021/acs.analchem.3c03660
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sciex-multiquant-data-export-format-recognition

## Summary

Identify and validate Sciex MultiQuant (>v3.0.3) txt export files containing QCpool sample measurements for downstream quality assessment. This skill ensures that exported metabolomics/lipidomics data meets structural and format requirements before parsing into QComics workflows.

## When to use

You have txt files exported from Sciex MultiQuant (>v3.0.3) containing QCpool samples measured at regular intervals during mass spectrometry sequences, and you need to validate whether the file structure is compatible with the QComics package before parsing and quality assessment.

## When NOT to use

- Input is already a structured R data frame or tibble with standardized column names — skip format recognition and proceed directly to downstream QComics analysis.
- Data was exported from Sciex MultiQuant version ≤3.0.3 — file structure may differ from the expected format.
- Input is in a non-txt format (e.g. CSV, mzML, NetCDF) — this skill is specific to Sciex MultiQuant txt exports.

## Inputs

- txt file exported from Sciex MultiQuant (>v3.0.3) software
- QCpool sample measurement data with identifiers, values, and timestamps

## Outputs

- Validation report (pass/fail) with identified schema issues
- Confirmed txt file ready for parsing into R data frame

## How to apply

Inspect the txt export file to confirm it contains tabular structure with QCpool sample identifiers, measurement values, timestamps, and metadata fields. Verify that required columns are present and data types match expectations (numeric values for measurements, valid date/time formats for timestamps). Check that the file encodes QCpool sample metadata consistently across rows. Validate row count and column alignment to detect truncation or export errors. Only proceed to parsing if all structural checks pass; this prevents downstream type coercion failures and nonsensical quality metrics in QComics analysis.

## Related tools

- **Sciex Multiquant (> v3.0.3)** (Source software that exports QCpool sample data in txt format for validation and downstream parsing)
- **R** (Host language for validation checks and file I/O operations prior to QComics import)
- **QComics** (Downstream R package that consumes validated and parsed QCpool data for quality assessment) — https://github.com/ricoderks/QComics

## Evaluation signals

- File parses without I/O errors and all rows are readable (no truncation or encoding issues).
- All required columns (QCpool identifiers, measurement values, timestamps, metadata) are present and non-empty.
- Data types validate correctly: numeric columns contain valid numbers, timestamp columns parse to recognized date/time format, identifiers are character strings.
- Column alignment is consistent across all rows (no ragged arrays or missing fields).
- Parsed data successfully converts to R data frame with standardized column names and is accepted by QComics downstream functions without type coercion warnings.

## Limitations

- Format recognition is specific to Sciex MultiQuant >v3.0.3 txt exports; earlier versions or other export formats are out of scope.
- This skill validates structural format only; it does not detect measurement errors, instrument artifacts, or problematic QCpool samples — those are addressed by QComics quality assessment.
- No changelog is available for QComics or Sciex MultiQuant to document breaking changes to txt export format between versions.

## Evidence

- [intro] analyzed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [other] QCpool sample identifiers, measurement values, timestamps, and metadata fields must be extracted and validated: "Parse the tabular structure to extract QCpool sample identifiers, measurement values, timestamps, and metadata fields"
- [other] Required columns must be present with correct data types before conversion to R data frame: "Validate that required columns are present and data types are correct (numeric values, date/time format)"
- [intro] a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [intro] The goal of the QComics package is quality assessment for metabolomics or lipidomics studies: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
