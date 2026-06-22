---
name: export-tag-syntax-validation
description: Use when you have a tabular file (CSV or Excel) that has been manually or semi-automatically tagged with export tags, and you need to verify tag correctness before running the extract command to convert the tagged table into intermediate JSON.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - Python
  - MESSES
  - jsonschema
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
---

# export-tag-syntax-validation

## Summary

Validates that tagged column headers in tabular export files conform to MESSES tag syntax (formats like #<table_name>.id and #.<field_name>) before attempting JSON conversion. This ensures malformed or inconsistent tags are caught early, preventing downstream JSON structure corruption.

## When to use

Apply this skill when you have a tabular file (CSV or Excel) that has been manually or semi-automatically tagged with export tags, and you need to verify tag correctness before running the extract command to convert the tagged table into intermediate JSON. Use it if you suspect tag syntax errors, inconsistent naming, or duplicate record identifiers within a table that could cause extraction failures.

## When NOT to use

- Input data is already in intermediate JSON form (validation should use JSON Schema instead)
- Tabular file has no export tags and is intended for direct import via a different extraction mechanism
- Tags have already been validated and extraction has completed successfully

## Inputs

- Tabular file with export tags in column headers (CSV or Excel format)
- Column header row containing # or #. prefixed tags

## Outputs

- Validation report listing syntax errors, malformed tags, and duplicate identifiers
- List of valid tagged columns ready for extraction
- Confirmation that tagged tabular file conforms to expected tag format

## How to apply

Scan all column headers in the tabular input file and identify those prefixed with # or #. (export tag markers). For each tagged column, extract and parse the tag to verify it matches one of two formats: #<table_name>.id (for record identifier columns) or #.<field_name> (for field value columns). Check that table names and field names follow valid naming conventions (typically alphanumeric with underscores). Validate that no duplicate record identifiers exist within any single table, as this would create ambiguous nested JSON structures. Report any malformed tags, missing table names, missing field names, or duplicate identifiers as errors that must be corrected in the source file before extraction proceeds.

## Related tools

- **MESSES** (Python package providing the extract command that consumes tagged tabular data; tag validation is a prerequisite step before calling extract) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (JSON Schema validator used downstream to validate the extracted intermediate JSON against the Experiment Description Specification and format-specific schemas) — https://pypi.org/project/jsonschema/

## Evaluation signals

- All tagged columns match one of the two valid syntax patterns (#<table_name>.id or #.<field_name>)
- No duplicate record identifiers exist within any table (uniqueness constraint satisfied)
- All extracted table names and field names follow alphanumeric naming conventions with no special characters
- Subsequent extract command completes without tag-parsing errors
- Resulting intermediate JSON structure correctly nests fields under their table and record identifiers with no malformed hierarchy

## Limitations

- Validation only checks syntax; it does not verify semantic correctness (e.g., whether the table names match an external schema or whether required fields are present)
- Duplicate detection works only within individual tables; cross-table identifier uniqueness is not validated at this stage
- Validation does not check for untagged columns that should have been tagged, nor does it auto-apply tags; the README notes that automated tagging and tag modification are separate features

## Evidence

- [other] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: "Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values"
- [other] Scan the tag syntax to extract table name, field name, and record identifier from each tagged column.: "Scan the tag syntax to extract table name, field name, and record identifier from each tagged column"
- [other] Validate that all tagged columns conform to the expected tag format and that no duplicate record identifiers exist within a table.: "Validate that all tagged columns conform to the expected tag format and that no duplicate record identifiers exist within a table"
- [other] The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data.: "The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data"
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats.: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats"
