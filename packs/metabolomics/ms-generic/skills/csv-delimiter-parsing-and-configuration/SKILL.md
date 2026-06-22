---
name: csv-delimiter-parsing-and-configuration
description: Use when when uploading a new mass spectrometry data file to Punc'data in CSV or delimited-text format, before attempting to map columns to their semantic roles (m/z value, intensity, formula).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - puncdata
  - Punc'data
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans:
- 'Source: github:github.com__WTVoe__puncdata'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_punc_data_cq
    doi: 10.1021/jasms.5c00151
    title: Punc’data
  dedup_kept_from: coll_punc_data_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00151
  all_source_dois:
  - 10.1021/jasms.5c00151
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CSV Delimiter Parsing and Configuration

## Summary

Detect and configure the column separator (semicolon, comma, tab, etc.) in a delimited text file prior to column-role mapping in high-resolution mass spectrometry data import. This skill ensures correct parsing of uploaded data files so that column headers can be reliably extracted and matched to semantic roles.

## When to use

When uploading a new mass spectrometry data file to Punc'data in CSV or delimited-text format, before attempting to map columns to their semantic roles (m/z value, intensity, formula). Use this skill whenever the input file's delimiter is unknown or non-standard, or when automatic delimiter detection has failed.

## When NOT to use

- Input file is already a parsed table or DataFrame (e.g., loaded in memory as a matrix or spreadsheet object); only raw delimited text files require this skill.
- Delimiter is already known and hardcoded in the import pipeline; use only when there is ambiguity or need for user control.
- File is in binary format (e.g., .mzML, .h5, .raw); this skill applies only to text-based delimited formats.

## Inputs

- Delimited text file (CSV, TSV, or custom-delimited format)
- File with first row containing column headers
- File path or binary stream uploaded to Punc'data data manager

## Outputs

- Delimiter character configuration (stored in session or parameters)
- Validated column-header row (extracted and separated by chosen delimiter)
- Ready-to-parse file state for downstream column-to-role mapping

## How to apply

Open the data manager tab and upload a data file (left column buttons). Access the gear icon (top right) to expose the delimiter configuration control. Test candidate delimiters (semicolon, comma, tab, space) against the first row of the file to verify that column headers are correctly separated. Select the delimiter that produces the correct number and content of column titles. Store the selected delimiter as part of the session configuration. Once delimiter is confirmed, the file is ready for column-header extraction and keyword-based semantic role assignment in the parameters tab.

## Related tools

- **Punc'data** (Interactive application hosting the delimiter configuration UI (gear icon) and data manager tab for file upload and delimiter selection) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Column headers are correctly separated and appear as distinct entries after delimiter parsing; no header text is truncated or merged.
- Number of columns extracted equals the intended number of data fields in the input file.
- Subsequent column-to-role mapping (keyword recognition step) correctly identifies at least m/z, intensity, and formula columns; if mapping fails, delimiter was incorrect.
- File can be re-loaded in multiple sessions using the stored delimiter configuration without re-parsing.
- Gear icon configuration persists in saved Punc'data sessions and produces identical column extraction on reload.

## Limitations

- Tool assumes first line of input file is always a header row; files with leading comments or metadata rows will fail or produce incorrect delimiter detection.
- No automatic delimiter detection is documented; user must manually test delimiters via the gear icon UI.
- Special characters (e.g., quoted fields, escaped delimiters, newlines within quoted strings) are not mentioned in the README; behavior on edge-case CSV syntax is unknown.
- Delimiter configuration is UI-driven only; no programmatic or command-line interface is provided for scripted or batch import.
- File encoding (UTF-8, Latin-1, etc.) is not discussed; files with non-ASCII headers or special characters may fail silently.

## Evidence

- [readme] To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
- [readme] The first line of any uploaded file has to be the title of each column.: "The first line of any uploaded file has to be the title of each column."
- [other] Parse the uploaded file delimiter (semicolon, comma, etc.) using the gear icon configuration.: "Parse the uploaded file delimiter (semicolon, comma, etc.) using the gear icon configuration."
- [readme] upload an already saved Punc'data session (top middle button), or data files (top left button, or all left buttons for each individual file): "upload an already saved Punc'data session (top middle button), or data files (top left button, or all left buttons for each individual file)"
