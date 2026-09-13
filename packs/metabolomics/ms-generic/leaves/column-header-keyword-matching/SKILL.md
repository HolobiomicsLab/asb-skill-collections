---
name: column-header-keyword-matching
description: Use when importing a new delimited data file (CSV, semicolon-separated,
  or other formats) into Punc'data that contains high-resolution mass spectrometry
  results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - puncdata
  - Punc'data
  - puncdata (repository)
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# column-header-keyword-matching

## Summary

Automatically infers the semantic role (m/z value, intensity, formula, etc.) of each column in a mass spectrometry data file by scanning column headers against a keyword dictionary, with manual override capability. This step is essential for correctly mapping heterogeneous input formats to Punc'data's internal data model before visualization and analysis.

## When to use

Apply this skill when importing a new delimited data file (CSV, semicolon-separated, or other formats) into Punc'data that contains high-resolution mass spectrometry results. Use it whenever the column headers in your input file are present (as required by the tool) but their semantic roles are ambiguous or need validation before proceeding to visualization, filtering, or formula assignment workflows.

## When NOT to use

- Input file lacks column headers in the first row (Punc'data requires them by design).
- Data is already in a pre-processed Punc'data session format (use the session upload button instead).
- Column headers do not match any keywords in Punc'data's recognition dictionary and manual override is not feasible for your workflow.

## Inputs

- Delimited text file (CSV, semicolon-separated, or other delimiter) with column headers in the first row
- File delimiter specification (comma, semicolon, tab, or other character)
- Column header strings from the input file

## Outputs

- Column-to-semantic-role mapping (structured configuration)
- Finalized parameters tab state reflecting auto-detected and manually-overridden roles

## How to apply

First, parse the uploaded file's delimiter (comma, semicolon, or other) using the gear icon configuration. Extract the column headers from the first line of the file. Scan each header string against Punc'data's built-in keyword dictionary to identify semantic roles such as 'm/z value', 'intensity', or 'formula' based on keyword matching rules. Assign each column to its auto-detected semantic role and store the mapping. Then expose the complete mapping on the parameters tab, allowing users to manually override any incorrect auto-detections before finalizing the column-to-role configuration. The finalized mapping is stored as a structured configuration that drives all downstream tools (Tables, Canvas, Stats, Network, Matrix, Venn, PCA).

## Related tools

- **Punc'data** (Interactive visualization and attribution tool that implements column-header keyword matching during data import to map columns to m/z, intensity, formula, and other semantic roles for high-resolution mass spectrometry analysis) — https://wtvoe.github.io/puncdata/
- **puncdata (repository)** (Source code repository containing the keyword dictionary, header parsing logic, and parameters tab UI for manual override of semantic role assignments) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Each column header is assigned to exactly one semantic role (m/z value, intensity, formula, or other); no role is left unassigned or duplicated.
- The parameters tab displays the full column-to-role mapping and allows users to manually correct misclassified columns without error.
- Downstream visualization and analysis tools (Table, Stats, Canvas, Network, Matrix, Venn, PCA) correctly interpret and use the mapped roles (e.g., intensity columns are used for quantitative comparisons, m/z columns for mass windows).
- When a file is re-uploaded or a session is reloaded, the column mapping is consistently reproduced or restored.
- Keyword matching is case-insensitive and tolerant of variations (e.g., 'm/z', 'm_z', 'mass-to-charge' all match the m/z role).

## Limitations

- Column header keywords must be recognizable by Punc'data's built-in dictionary; non-standard or domain-specific column names may fail to auto-detect and require manual override.
- The tool does not validate the semantic correctness of the mapped roles against the actual data values (e.g., it will not reject a column labeled 'intensity' that contains text strings).
- Manual override is available but not scripted or batch-automated; large numbers of misclassified files require repeated manual intervention.
- No documentation is provided on the full list of keywords recognized by Punc'data's dictionary, limiting predictability for new users.

## Evidence

- [other] Punc'data recognizes column semantic role based on keywords in the header row, with manual override capability on the parameters tab.: "Punc'data recognizes which column corresponds to which information based on keywords. They can also be edited manually on tab "parameters"."
- [readme] The first line of the uploaded file must contain column titles, and the tool matches columns to data types using keyword recognition.: "The first line of any uploaded file has to be the title of each column. Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula... Punc'data"
- [readme] The file delimiter must be specified before header parsing can occur.: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon (top right)."
- [readme] Punc'data is used to process high-resolution mass spectrometry results with heterogeneous column structures.: "Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results. It is used to filter, select, observe, comment and transmit information on results"
