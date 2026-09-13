---
name: peak-list-column-mapping
description: Use when when uploading a new peak list or complex sample data file with
  delimiter-separated columns to Punc'data, especially when column headers are ambiguous
  or use non-standard naming conventions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Punc'data
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans: []
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

# peak-list-column-mapping

## Summary

Automated recognition and manual assignment of semantic meaning to columns in high-resolution mass spectrometry peak lists. This skill enables Punc'data to map raw tabular columns (m/z, intensity, formula, etc.) to their analytical significance, enabling downstream visualization and filtering workflows.

## When to use

When uploading a new peak list or complex sample data file with delimiter-separated columns to Punc'data, especially when column headers are ambiguous or use non-standard naming conventions. Use this skill if you need to generate Kendrick mass plots, canvas visualizations, or comparative analyses (Matrix, Venn, PCA) that depend on correct identification of m/z values, intensity, and formula columns.

## When NOT to use

- Input is already a fully parsed Punc'data session file (.json or saved state) — use session upload instead.
- Column headers are completely missing or the first row contains data rather than labels — pre-process the file to add headers.
- Data is in a non-tabular format (e.g., raw instrument output in mzML or netCDF) — convert to delimited text first.

## Inputs

- Delimiter-separated peak list file (CSV, TSV, or custom delimiter)
- Column header row with semantic labels (m/z, intensity, formula, etc.)
- Previously saved Punc'data session file

## Outputs

- Parsed peak list with semantically annotated columns
- Column-to-data-type mapping (m/z → numeric vector, intensity → numeric vector, formula → string vector, etc.)
- Parameters table (editable in 'parameters' tab for manual override)

## How to apply

Load the input data file specifying the column delimiter (semicolon, comma, tab, or other). Punc'data will attempt automated keyword-based recognition of standard column types (m/z, intensity, formula) from the first row headers. If automated mapping fails or produces incorrect assignments, switch to the 'parameters' tab to manually edit column interpretations. Verify the mapped columns are semantically correct before proceeding to visualization or analysis tabs (Canvas, Stats, Tools, Network). The robustness of downstream analyses—especially Kendrick mass axis selection and PCA sample comparisons—depends on correct column assignment at this stage.

## Related tools

- **Punc'data** (Primary platform for column mapping, keyword-based recognition, and manual parameter editing; supports CSV upload and provides parameters tab for correcting automated assignments) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Automated keyword matching correctly identifies at least 2 of 3 standard columns (m/z, intensity, formula) in test datasets with standard naming conventions.
- Manual column reassignment in the 'parameters' tab persists across visualization and analysis operations without reverting or causing downstream errors.
- Kendrick mass plot axis selector (Canvas tab) receives correct m/z values and computes Normalized Kendrick Mass (NKM) = round(m/z × base mass) − (m/z × base mass rounded) accurately when base mass is 14.0157.
- Canvas, Table, Stats, and Matrix visualizations display data consistent with the mapped column assignments (e.g., correct intensity scaling, correct m/z range).
- Example dataset 'testdata_cellulose.csv' loads without mapping errors and generates Premade Canvas plots on first attempt.

## Limitations

- Keyword-based recognition depends on column headers matching expected naming patterns; non-English or highly abbreviated headers may fail automated mapping.
- No validation criteria or data quality metrics are documented; incorrect column assignments are not flagged with warnings or confidence scores.
- Manual parameter edits are stored per-session only; there is no export or schema definition to document the mapping for reproducibility across sessions.
- Delimiter detection is manual (gear icon); incorrect delimiter specification will prevent proper column parsing.

## Evidence

- [readme] Punc'data recognizes column information based on keywords such as m/z value, intensity, and formula.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] Manual column assignment via parameters tab: "They can also be edited manually on tab "parameters"."
- [readme] Delimiter specification is required: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
- [readme] First row must contain column headers: "The first line of any uploaded file has to be the title of each column."
- [other] Kendrick mass plot axis selection depends on correct m/z column recognition: "Punc'data recognizes m/z values from uploaded data files based on column keywords, which can be used as input parameters for generating interactive visualizations including canvas plots"
