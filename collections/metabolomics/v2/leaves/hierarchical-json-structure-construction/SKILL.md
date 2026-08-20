---
name: hierarchical-json-structure-construction
description: 'Use when your input is a tabular file (CSV or Excel) with column headers
  annotated using MESSES tagging syntax (#<table_name>.id for record identifiers and
  #.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES (Metadata from Experimental SpreadSheets Extraction System)
  - jsonschema
  license_tier: open
  provenance_tier: literature
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

# hierarchical-json-structure-construction

## Summary

Convert tagged tabular data (with export tags like #<table_name>.id and #.<field_name>) into a nested JSON structure suitable for directive resolvers and downstream processing. This skill is essential for transforming spreadsheet-based experimental metadata into interoperable, standardized JSON representations.

## When to use

Your input is a tabular file (CSV or Excel) with column headers annotated using MESSES tagging syntax (#<table_name>.id for record identifiers and #.<field_name> for field names), and you need to produce a nested JSON object where tables contain records with field key-value pairs, ready for validation against JSON Schema and conversion to repository formats.

## When NOT to use

- Input is already in JSON format or another structured format (use extract command only when raw tabular data with manual or auto-generated tags is present)
- Tabular data lacks any tagging layer — automatic tagging features must be applied first or data must be manually tagged
- Conversion target does not require nested record-based structure (e.g., simple flat CSV output)

## Inputs

- Tagged tabular file (CSV or Excel format with #<table_name>.id and #.<field_name> column headers)
- Tagging scheme specification defining tag syntax and nesting rules

## Outputs

- Nested JSON object with tables as keys, records as sub-objects, and field key-value pairs
- Intermediate JSON representation compliant with Experiment Description Specification

## How to apply

Parse the tabular file row-by-row, scanning column headers to identify and extract export tags prefixed with # or #. For each tagged column, extract the table name, field name, and record identifier from the tag syntax. Build a hierarchical JSON object by nesting field values under their corresponding table and record identifiers, ensuring no duplicate record identifiers exist within a table. Validate that all tagged columns conform to the expected tag format before outputting the nested JSON structure as a dictionary-like object. The resulting structure should be interoperable with the Experiment Description Specification schema and ready for consumption by conversion directives targeting formats like mwTab.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Python package providing the extract command to parse tagged tabular data and convert it to intermediate JSON; also provides validate and convert commands for downstream processing) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the resulting JSON structure against the Experiment Description Specification and Protocol Dependent Schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes extract your_data.csv --output your_data.json
```

## Evaluation signals

- All tagged columns are correctly parsed and no tag syntax errors remain (validated against expected tag format: #<table_name>.id and #.<field_name>)
- Resulting JSON structure is valid against the Experiment Description Specification schema using jsonschema validator
- No duplicate record identifiers exist within any table (checked during construction)
- Field values are correctly nested under their corresponding table and record identifiers (spot-check a sample record from each table)
- Output JSON can be successfully consumed by conversion directives without schema mismatch errors

## Limitations

- The tagging layer must be present or automatically applied before extraction; untagged tabular data cannot be converted without manual tagging or auto-tagging features
- Tag syntax is strict — malformed tags (e.g., missing table name, incorrect delimiters) will cause parsing errors and must be corrected in the source data
- The resulting JSON structure's interoperability depends on conformance to the Experiment Description Specification; custom schemas may require additional validation steps
- Complex data types (e.g., nested arrays, composite objects) may require extensions to the basic #<table_name>.id and #.<field_name> tagging syntax not covered by the core specification

## Evidence

- [other] Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing a JSON structure where table names contain records with field key-value pairs.: "Tagged tabular files are converted to nested JSON by mapping each table column with #<table_name>.id tags to record names and each column with #.<field_name> tags to field names and values, producing"
- [other] The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data.: "The extract command of MESSES supports turning tabular data into JSON. This is done by adding a layer of tags on top of the data."
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats.: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats."
- [readme] The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON based on your specific project schema: "The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON based on your specific project schema"
- [other] There are features for automatically applying tags to untagged data and features for modifying the names and values of data.: "There are features for automatically applying tags to untagged data and features for modifying the names and values of data."
