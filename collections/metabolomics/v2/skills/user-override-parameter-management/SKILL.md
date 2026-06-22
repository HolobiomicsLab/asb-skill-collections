---
name: user-override-parameter-management
description: Use when punc'data's automatic keyword-based column recognition produces incorrect semantic role assignments—for example, when a column header contains a non-standard keyword that the tool fails to recognize, or when a column's true semantic role (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - puncdata
  - Punc'data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# user-override-parameter-management

## Summary

Override auto-detected column semantic roles in Punc'data by manually editing parameter mappings on the parameters tab after automatic keyword recognition has assigned data columns to their roles (m/z value, intensity, formula, etc.). This skill ensures that misclassified columns are corrected before downstream analysis and visualization.

## When to use

Apply this skill when Punc'data's automatic keyword-based column recognition produces incorrect semantic role assignments—for example, when a column header contains a non-standard keyword that the tool fails to recognize, or when a column's true semantic role (e.g., m/z value, intensity, formula) does not match the auto-detected role. Triggered after file upload and inspection of the auto-generated column mapping.

## When NOT to use

- Column headers are already correctly recognized by Punc'data keyword matching—override is unnecessary overhead.
- Input file lacks a header row; semantic roles cannot be assigned by keyword recognition and manual override alone.
- The data format is not delimited text (e.g., binary mass spectrometry formats like .raw or .mzML)—Punc'data does not support direct import of these without prior conversion.

## Inputs

- Delimiter-separated data file (CSV, semicolon-delimited, or other) with column headers in the first row
- Auto-generated column-to-semantic-role mapping (produced by Punc'data keyword recognition)

## Outputs

- Finalized column-to-semantic-role mapping configuration (stored in Punc'data session or internal state)
- Corrected parameters available for use in downstream visualization and analysis tabs

## How to apply

After uploading a delimited data file (with column headers in the first row) and configuring the delimiter using the gear icon, Punc'data automatically scans each header against its keyword dictionary to infer semantic roles. Inspect the resulting column-to-role mapping on the parameters tab. For any column with an incorrect or missing role assignment, manually edit the role assignment in the parameters tab UI to reflect the true semantic role (m/z value, intensity, formula, or other recognized data type). The corrected mapping is then stored and used for all downstream table generation, chart production, and visualization steps. This override mechanism is necessary because keyword recognition alone may fail on non-standard or domain-specific column naming conventions.

## Related tools

- **Punc'data** (Interactive UI platform that performs automatic keyword-based column recognition, exposes auto-detected mappings on the parameters tab, and accepts manual overrides to reassign semantic roles before downstream visualization and analysis) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Each column in the input file is assigned to one and only one semantic role (m/z value, intensity, formula, or other); no conflicts or missing assignments remain.
- Manual edits on the parameters tab persist and are reflected in downstream tables, charts, and visualizations (e.g., intensity columns are plotted as y-axis in Canvas, m/z columns as x-axis).
- The corrected mapping can be exported or saved as part of a Punc'data session and re-loaded without loss of fidelity.
- Visualization outputs (Canvas, Stats, Table, Network tabs) correctly interpret the overridden semantic roles—for example, m/z values are not plotted as categorical data, and intensity values are treated as numeric.

## Limitations

- Punc'data's keyword dictionary is not user-extensible; custom or highly specialized column naming conventions may not be recognized even after override attempts, and the tool may not support arbitrary semantic roles beyond those built-in.
- Manual override is a UI-driven action with no documented API or programmatic interface; reproducibility and scripting are limited.
- No validation or warning system is described to alert users if an override produces inconsistent role assignments (e.g., multiple columns assigned to 'intensity' or none assigned to 'm/z value').
- The article does not document the complete list of recognized semantic roles or the keyword patterns used for matching; users must infer roles through trial and error or external documentation.

## Evidence

- [other] Punc'data recognizes column semantic role based on keywords in the header row, with manual override capability on the parameters tab.: "Punc'data recognizes which column corresponds to which information based on keywords. They can also be edited manually on tab "parameters"."
- [readme] The first line of an uploaded file must contain column titles, which are scanned against a keyword dictionary to infer semantic roles.: "The first line of any uploaded file has to be the title of each column. Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula... Punc'data"
- [readme] Column mappings are exposed and editable on the parameters tab, allowing practitioners to correct auto-detected roles.: "Column represent data : m/z value, intensity, formula... Punc'data recognizes which column corresponds to which information based on keywords. They can also be edited manually on tab "parameters"."
- [readme] File delimiter configuration is performed using the gear icon before column recognition occurs.: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
