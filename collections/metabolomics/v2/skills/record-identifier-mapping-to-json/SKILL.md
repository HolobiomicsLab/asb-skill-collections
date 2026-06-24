---
name: record-identifier-mapping-to-json
description: 'Use when when you have a tagged tabular file (Excel or CSV) with columns
  marked using export tag syntax (e.g., #study.id, #subject.id, #.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES
  - jsonschema
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo13070842
  all_source_dois:
  - 10.3390/metabo13070842
  - 10.3390/metabo11030163
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# record-identifier-mapping-to-json

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Maps tagged tabular columns with record identifiers (using #<table_name>.id export tags) to their corresponding nested JSON structures, enabling conversion of spreadsheet-based experimental metadata into hierarchical JSON representations. This skill bridges tabular data formats and JSON-based interchange, critical for submission-ready scientific data curation.

## When to use

When you have a tagged tabular file (Excel or CSV) with columns marked using export tag syntax (e.g., #study.id, #subject.id, #.<field_name>), and you need to convert it to nested JSON structure for validation against the Experiment Description Specification or downstream conversion to mwTab or other repository formats. Specifically, apply this skill after tagging has identified record-level identifiers but before JSON schema validation.

## When NOT to use

- Tabular data has not yet been tagged with export tags — apply tagging first.
- Record identifiers are missing or inconsistently formatted across rows — validate tag coverage before applying this skill.
- Input is already in JSON format — use JSON-to-JSON conversion (convert command) instead.

## Inputs

- Tagged tabular file (CSV or Excel format) with #<table_name>.id and #.<field_name> columns
- Column header metadata (tag syntax and field names)
- Row-by-row tabular data with record identifier values

## Outputs

- Nested JSON object (Python dict or JSON-serialized string)
- Hierarchical structure: {table_name: {record_id: {field: value, ...}, ...}, ...}

## How to apply

Parse the tagged tabular file row-by-row, scanning column headers for export tags following the #<table_name>.id pattern (for record identifiers) and #.<field_name> pattern (for field names). For each row, extract the record identifier value from the #<table_name>.id column and use it as a nesting key in the output JSON. Collect all field values (from #.<field_name> columns) under that record identifier, organized by their table name. Validate that all record identifiers within a single table are unique and that the tag syntax conforms to the expected format (# prefix, dot notation). Output the result as a hierarchical Python dictionary (or JSON object) where the top level contains table names, second level contains record identifiers, and third level contains field key-value pairs.

## Related tools

- **MESSES** (Command-line package that implements the extract command to parse tagged tabular files and build the intermediate JSON representation) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Core language for implementing row-by-row parsing, tag extraction, and JSON object construction)
- **jsonschema** (Used to validate the output JSON structure against the Experiment Description Specification schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes extract your_data.csv --output your_data.json
```

## Evaluation signals

- All #<table_name>.id values map to unique keys at the second nesting level (no duplicate record identifiers within a table)
- Every #.<field_name> column value is correctly placed under its corresponding table and record identifier in the output
- Output JSON structure conforms to the Experiment Description Specification schema (validated via jsonschema)
- No tagged columns remain unmapped; all tag syntax is syntactically valid (# or #. prefix, valid table/field names)
- Hierarchical depth is exactly 3 levels (table → record_id → field:value) with no extraneous nesting or flattening

## Limitations

- The skill requires that tabular data be properly tagged with export tags beforehand; untagged data cannot be processed without automated tagging (a separate feature in MESSES).
- Duplicate record identifiers within the same table will cause data loss or merge errors; the skill cannot automatically resolve such conflicts.
- The tag syntax is case-sensitive and does not support malformed tags; any deviation from #<table_name>.id or #.<field_name> patterns will cause parsing failures.
- The skill produces intermediate JSON; subsequent validation against Protocol Dependent Schema or format-specific schemas (e.g., mwTab) is required before downstream use.

## Evidence

- [other] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: "Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values"
- [other] Read tagged tabular file and parse row-by-row, identifying export tags (prefixed with # or #.) in column headers. Scan the tag syntax to extract table name, field name, and record identifier from each tagged column. Build a hierarchical JSON object structure by nesting field values under their corresponding table and record identifiers. Validate that all tagged columns conform to the expected tag format and that no duplicate record identifiers exist within a table.: "parse row-by-row, identifying export tags (prefixed with # or #.) in column headers. Scan the tag syntax to extract table name, field name, and record identifier from each tagged column. Build a"
- [other] The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data.: "The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data."
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats.: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation"
