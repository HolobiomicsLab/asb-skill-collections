---
name: metadata-field-extraction-from-headers
description: 'Use when you have tabular data (CSV or Excel) with column headers annotated using MESSES tagging syntax (#<table_name>.id for record identifiers, #.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3307
  tools:
  - Python
  - MESSES (Metadata from Experimental SpreadSheets Extraction System)
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

# metadata-field-extraction-from-headers

## Summary

Extract nested metadata structures from tagged tabular column headers by parsing export tags (prefixed with # or #.) to identify table names, field names, and record identifiers, producing a hierarchical JSON representation suitable for downstream directive resolvers.

## When to use

Apply this skill when you have tabular data (CSV or Excel) with column headers annotated using MESSES tagging syntax (#<table_name>.id for record identifiers, #.<field_name> for field values) and need to convert those headers into a nested JSON structure for validation, conversion, or deposition into a repository like Metabolomics Workbench.

## When NOT to use

- Input tabular data has no tags or uses a non-MESSES tagging syntax (use automated tagging or manual re-annotation first)
- Column headers follow a flat, non-hierarchical structure unrelated to table/record/field decomposition
- Data is already in validated JSON form and does not require extraction from tabular headers

## Inputs

- Tagged tabular file (CSV or Excel format) with column headers annotated using #<table_name>.id and #.<field_name> syntax
- Column header row(s) containing export tags

## Outputs

- Nested JSON object with structure: {table_name: {record_id: {field_name: value, ...}, ...}, ...}
- Dictionary-like object ready for consumption by directive resolvers

## How to apply

Read the tabular file row-by-row and parse each column header to identify and extract export tags using the # and #. prefix syntax. For each tagged column, scan the tag syntax to extract the table name, field name, and record identifier components. Build a hierarchical JSON object by nesting field values under their corresponding table and record identifiers, ensuring that the tag format conforms to expectations and that no duplicate record identifiers exist within a table. Validate the resulting structure against the JSON Schema and the Experiment Description Specification before passing to downstream conversion directives. The rationale is that tagging adds a human-readable, automatable layer on top of raw tabular data, making it amenable to standardized extraction and schema-based validation.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Python package that implements the extract, validate, and convert workflow; the extract command uses tagging to convert tabular data into JSON) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the extracted JSON structure against the Experiment Description Specification and custom JSON schemas) — https://pypi.org/project/jsonschema/
- **Python** (Host language for MESSES package and tagging/parsing implementation)

## Examples

```
messes extract your_data.csv --output your_data.json
```

## Evaluation signals

- All tagged columns are successfully parsed and their table, record, and field components extracted without syntax errors
- The resulting JSON structure conforms to the Experiment Description Specification and passes jsonschema validation
- No duplicate record identifiers exist within any table in the output JSON
- Field values are correctly nested under the appropriate table and record identifier keys
- The JSON object can be successfully consumed by downstream conversion directives without transformation errors

## Limitations

- Initial steep learning curve required to understand the tagging syntax and Experiment Description Specification before data entry or manual tagging
- Requires that all column headers follow the #<table_name>.id or #.<field_name> format; malformed or inconsistent tags will cause parsing errors
- Assumes that tabular data has been pre-tagged either manually or through automated tagging features; untagged data must first be annotated
- Does not handle non-standard tag formats or legacy tagging schemes not aligned with MESSES specification

## Evidence

- [other] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: "Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing"
- [other] The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data.: "The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data."
- [other] Build a hierarchical JSON object structure by nesting field values under their corresponding table and record identifiers. Validate that all tagged columns conform to the expected tag format and that no duplicate record identifiers exist within a table.: "Build a hierarchical JSON object structure by nesting field values under their corresponding table and record identifiers. Validate that all tagged columns conform to the expected tag format and that"
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats.: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats."
- [readme] The expected workflow is to use the 'extract' command to transform your tabular data into JSON, then use the 'validate' command to validate the JSON based on your specific project schema: "The expected workflow is to use the 'extract' command to transform your tabular data into JSON, then use the 'validate' command to validate the JSON based on your specific project schema"
