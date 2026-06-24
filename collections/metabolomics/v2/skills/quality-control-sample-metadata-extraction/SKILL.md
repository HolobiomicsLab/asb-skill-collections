---
name: quality-control-sample-metadata-extraction
description: Use when you have txt files exported from Sciex MultiQuant (>v3.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Sciex MultiQuant
  - QComics
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
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

# quality-control-sample-metadata-extraction

## Summary

Parse and structure quality-control pool (QCpool) sample metadata and measurement values exported from Sciex MultiQuant (>v3.0.3) txt files into a machine-readable format suitable for downstream quality assessment workflows. This skill bridges instrument output and quality-control analytics by standardizing heterogeneous tabular data into validated, typed data frames.

## When to use

You have txt files exported from Sciex MultiQuant (>v3.0.3) containing QCpool sample measurements collected at regular intervals across one or more mass spectrometry sequences, and you need to ingest and validate that data into a structured format (R data frame or CSV) before performing quality overview analysis (e.g., trend detection, drift assessment) with the QComics package or equivalent quality-control tools.

## When NOT to use

- Input is already a structured, validated data frame or machine-readable format (e.g., already parsed CSV or R object) — extraction is not needed.
- Data originates from a different mass spectrometry instrument vendor or MultiQuant version ≤v3.0.3 — parsing schema and field positions may differ.
- QCpool samples were not measured at regular intervals or metadata/timestamps are missing — validation will fail and the workflow cannot proceed.

## Inputs

- Sciex MultiQuant (>v3.0.3) txt export file containing QCpool sample measurements
- Plain-text tabular data with QCpool identifiers, measurement values, and timestamps

## Outputs

- Structured R data frame or tibble with standardized column names and validated data types
- CSV or R serialized object (.rds) suitable for quality assessment workflows

## How to apply

Load the Sciex MultiQuant txt export using standard R file I/O (e.g., read.csv or readr::read_delim). Parse the tabular structure to identify and extract QCpool sample identifiers, measurement values, timestamps, and associated metadata fields. Validate that all required columns are present and that data types conform to specification (numeric values for measurements, proper date/time parsing for timestamps). Convert the parsed data into a standardized R data frame or tibble with consistent column naming and formatting conventions. Output the validated structure as CSV or R serialized object (.rds) for consumption by downstream QComics quality assessment workflows.

## Related tools

- **Sciex MultiQuant** (Source instrument software that exports QCpool measurement data in txt tabular format (>v3.0.3 required))
- **R** (Environment for parsing txt files, validating data types, and constructing standardized data frames for downstream QComics quality assessment)
- **QComics** (Downstream quality assessment package that consumes the parsed and structured QCpool data frame to generate quick overview reports of metabolomics/lipidomics study quality) — https://github.com/ricoderks/QComics

## Evaluation signals

- All required columns (QCpool identifiers, measurement values, timestamps, metadata) are present in the output data frame with no missing values in critical fields.
- Data types conform to specification: numeric columns parse without NA coercion, timestamps parse into a valid date/time class (POSIXct or equivalent).
- QCpool sample identifiers and timestamps are unique or properly grouped (no duplicates that suggest parsing errors).
- Output file can be successfully loaded by QComics or equivalent downstream tools without schema or type errors.
- Row count and column count match expected dimensions derived from the input txt file structure (sanity check for incomplete parsing).

## Limitations

- Parser is specific to Sciex MultiQuant (>v3.0.3) txt export format; other vendors or earlier MultiQuant versions may have different field orders, delimiters, or metadata layouts.
- QCpool samples must have been measured at regular intervals with complete timestamps; sparse or missing time metadata will cause validation to fail.
- No changelog available in the QComics repository; version-specific breaking changes in output schema or required columns are not documented.
- The skill assumes the txt file is well-formed and uncorrupted; malformed headers, irregular delimiters, or encoding issues are not handled gracefully.

## Evidence

- [intro] The QComics package accepts pooled QCpool samples that have been measured at regular intervals during one or more sequences, analyzed with Sciex MultiQuant (>v3.0.3) software, and exported to txt format as input data for downstream quality overview analysis.: "The QComics package accepts pooled QCpool samples that have been measured at regular intervals during one or more sequences, analyzed with Sciex MultiQuant (>v3.0.3) software, and exported to txt"
- [intro] Load the txt file exported from Sciex MultiQuant (>v3.0.3) using R file I/O functions. Parse the tabular structure to extract QCpool sample identifiers, measurement values, timestamps, and metadata fields. Validate that required columns are present and data types are correct (numeric values, date/time format). Convert parsed data into a structured R data frame or tibble with standardized column names and formats. Output the structured table in a machine-readable format (CSV or R serialized object) for use in downstream QComics quality assessment workflows.: "Parse the tabular structure to extract QCpool sample identifiers, measurement values, timestamps, and metadata fields. Validate that required columns are present and data types are correct (numeric"
- [intro] The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
