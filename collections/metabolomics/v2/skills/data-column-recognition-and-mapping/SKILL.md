---
name: data-column-recognition-and-mapping
description: Use when when uploading a delimited CSV or similar tabular file to Punc'data containing high-resolution mass spectrometry results, and the column headers are present but their semantic roles (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Punc'data
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans:
- Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results.
- Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results
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

# data-column-recognition-and-mapping

## Summary

Automatically identify and assign semantic meaning to columns in mass spectrometry data files by matching column headers against known keywords (m/z, intensity, formula). This enables downstream analysis tools to correctly interpret numeric and categorical columns without manual configuration.

## When to use

When uploading a delimited CSV or similar tabular file to Punc'data containing high-resolution mass spectrometry results, and the column headers are present but their semantic roles (e.g., m/z value, intensity, molecular formula) are unknown or need to be validated before visualization or filtering.

## When NOT to use

- Input file lacks a header row (first row must contain column names for recognition to succeed).
- Column headers use non-standard or domain-specific terminology not in the Punc'data keyword lexicon, and manual correction is impractical.
- Data are already in a pre-processed format with column roles already established by prior curation.

## Inputs

- delimited text file (CSV, TSV, semicolon-separated) with first row containing column headers
- column header strings from mass spectrometry data (e.g., 'm/z', 'intensity', 'formula', 'H/C ratio', 'O/C ratio')

## Outputs

- column-to-semantic-role mapping (internal data structure)
- tagged columns available for filtering, visualization, and statistical operations in Canvas, Table, and Stats tabs
- optionally, manually corrected column assignments in the parameters tab

## How to apply

After uploading a file with column delimiters specified (semicolon, comma, etc.), Punc'data scans the first row (column headers) and matches them against a built-in keyword lexicon to infer column type and role. The system recognizes common patterns such as 'm/z', 'intensity', and 'formula' in header names. Recognized columns are automatically tagged and made available for use in downstream tabs (Tools, Canvas, Stats). If automatic recognition fails or is incorrect, columns can be manually reassigned or edited in the 'parameters' tab before proceeding to visualization or analysis.

## Related tools

- **Punc'data** (Interactive platform that performs keyword-based column recognition and provides manual override in the parameters tab for correcting or refining recognized column assignments before visualization.) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Recognized columns appear correctly labeled in the 'parameters' tab with their inferred semantic roles (m/z, intensity, formula).
- Columns can be selected and filtered appropriately in the Tools tab without errors or misaligned data types.
- Visualization in Canvas tab correctly plots numeric columns on axes and uses categorical/formula columns for grouping or color-coding.
- Manual correction of a misrecognized column in the parameters tab successfully updates downstream visualizations (regression, histogram, or scatter plots) without requiring re-upload.
- Export or downstream operations (PCA, matrix comparison, network generation) operate on the mapped columns without data type or schema errors.

## Limitations

- Recognition relies on keyword matching in column headers; non-standard header naming conventions may fail to auto-detect column roles, requiring manual intervention.
- No validation is documented for data quality, format consistency, or missing value handling within recognized columns.
- The keyword lexicon and recognition rules are not published; customization or extension for domain-specific column types (e.g., custom isotope ratios) is not documented.
- Recognition occurs only on the first row; if column headers are absent or malformed, the entire workflow may fail.

## Evidence

- [readme] Punc'data recognizes column information based on keywords such as m/z value, intensity, and formula.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] First row must be headers; columns represent m/z, intensity, formula and other data types.: "The first line of any uploaded file has to be the title of each column. Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula..."
- [readme] Manual reassignment of recognized columns is available.: "They can also be edited manually on tab "parameters"."
- [readme] Recognized columns enable use across all analysis tabs.: ""Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced."
