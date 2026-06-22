---
name: semantic-role-assignment-for-mass-spectrometry-data
description: Use when you have uploaded a delimited data file (comma-, semicolon-, or tab-separated) with a header row into Punc'data and need to ensure that each column is correctly mapped to its semantic role (m/z, intensity, formula, or other mass spectrometry attributes) before proceeding to analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Punc'data
  - puncdata
  - puncdata (GitHub repository)
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans:
- Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results.
- Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results
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
---

# semantic-role-assignment-for-mass-spectrometry-data

## Summary

Automatically infer and assign semantic roles (m/z value, intensity, formula) to columns in high-resolution mass spectrometry data files by matching column headers against a keyword dictionary, with manual override capability. This skill bridges raw tabular import and downstream visualization/filtering in Punc'data.

## When to use

You have uploaded a delimited data file (comma-, semicolon-, or tab-separated) with a header row into Punc'data and need to ensure that each column is correctly mapped to its semantic role (m/z, intensity, formula, or other mass spectrometry attributes) before proceeding to analysis, visualization, or filtering. This is especially critical when column titles are non-standard or ambiguous, or when you want to validate auto-detected roles before committing to downstream operations.

## When NOT to use

- Data file lacks a header row: Punc'data requires the first line to contain column titles; files without headers cannot be processed by this skill.
- Columns have already been manually assigned roles and you are re-importing the same file: use the saved Punc'data session upload (top middle button) instead to preserve prior mappings.
- Input is a pre-structured, already-validated feature table or matrix: this skill is for initial column recognition during import, not for re-assignment of already-processed data.

## Inputs

- Delimited text file (CSV, TSV, semicolon-separated) with header row
- Column header strings (first row of uploaded file)
- Delimiter specification (semicolon, comma, tab, etc.)

## Outputs

- Column-to-semantic-role mapping (structured configuration)
- Parameters tab display showing inferred and manually-overridden roles
- Validated column assignments for downstream visualization and filtering

## How to apply

First, parse the uploaded file's delimiter using the gear icon configuration (top right) to correctly identify the column separator. Extract the header row—Punc'data scans each column title against an internal keyword dictionary to infer its semantic role based on recognized patterns (e.g., headers containing 'm/z' map to m/z value role, 'intensity' or 'I' to intensity role, 'formula' or 'C' to formula role). Assign each column to its inferred semantic role automatically and store the mapping. Expose the finalized column-to-role mapping on the Parameters tab, where you can manually override any auto-detected assignments that are incorrect or ambiguous. Confirm the mapping is correct by verifying that each intended data type appears in the correct column before proceeding to downstream tools (Table, Canvas, Stats, Network, etc.).

## Related tools

- **Punc'data** (Interactive web application that implements automatic column-to-role keyword recognition on file upload and exposes manual override on the Parameters tab) — https://wtvoe.github.io/puncdata/
- **puncdata (GitHub repository)** (Source code repository containing the implementation of semantic role assignment logic and keyword matching dictionary) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Each column header is correctly matched to one and only one semantic role (m/z, intensity, formula, or other defined role) with no ambiguous or null assignments.
- The Parameters tab displays the inferred mapping; spot-check a sample of headers against the assigned roles to confirm keyword matching is sensible (e.g., a column titled 'm/z_ppm' is assigned the m/z value role).
- Manual overrides on the Parameters tab persist and are reflected in downstream tools (Table, Canvas, Stats tabs) such that filtered or visualized data correctly uses the corrected roles.
- The file parses without errors after role assignment; downstream tools (e.g., Canvas A/B, Table, Network) can successfully render data using the assigned roles, confirming the mapping is valid and complete.
- No missing or unassigned columns: all columns in the input file appear in the Parameters tab role mapping, and none are silently dropped or left unclassified.

## Limitations

- Keyword recognition relies on predefined patterns in the tool's keyword dictionary; non-standard or domain-specific column titles (e.g., 'm_z_ratio', 'peak_intensity_au') may not be recognized and will require manual override.
- The tool does not validate semantic consistency (e.g., whether intensity values are numeric or whether m/z values fall in physically plausible ranges); role assignment is purely syntactic, based on header text matching.
- No specification of data formats accepted beyond CSV or delimited text; binary formats (mzML, mzXML, NetCDF) are not explicitly mentioned as supported inputs.
- Manual override is necessary for each file upload; the role mapping is not automatically propagated across multiple files in batch operations (each file must be re-assigned or a saved Punc'data session must be used).
- The keyword dictionary and matching rules are not publicly documented, so practitioners cannot predict or troubleshoot failed recognition without trial-and-error on the Parameters tab.

## Evidence

- [readme] Punc'data recognizes which column corresponds to which information based on keywords.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] The first line of any uploaded file has to be the title of each column. Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula... They can also be edited manually on tab "parameters".: "The first line of any uploaded file has to be the title of each column. Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula... They can also"
- [other] Parse the uploaded file delimiter (semicolon, comma, etc.) using the gear icon configuration. Extract column headers from the input file. Scan each header against a keyword dictionary to identify semantic roles (m/z value, intensity, formula, etc.) based on Punc'data recognition rules.: "Parse the uploaded file delimiter (semicolon, comma, etc.) using the gear icon configuration. Extract column headers from the input file. Scan each header against a keyword dictionary to identify"
- [readme] You can change the separator with the gear icon (top right).: "You can change the separator with the gear icon (top right)."
- [other] Expose the mapping on the parameters tab to allow manual override of auto-detected roles.: "Expose the mapping on the parameters tab to allow manual override of auto-detected roles."
