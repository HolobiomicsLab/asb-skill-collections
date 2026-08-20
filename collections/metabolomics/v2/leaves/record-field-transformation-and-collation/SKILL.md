---
name: record-field-transformation-and-collation
description: Use when you have extracted tabular data into an intermediate JSON form
  and need to restructure records by mapping input fields to output dictionary keys,
  collating multiple records under a single grouping field, filtering records by test
  conditions or exclusion rules, or applying custom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3070
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES (Metadata from Experimental SpreadSheets Extraction System)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema
  <https://pypi.org/project/jsonschema/>`_)
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

# record-field-transformation-and-collation

## Summary

Transform and collate tabular records into structured dictionaries by mapping source fields to output headers, filtering, grouping, and optionally applying custom Python code. This skill is essential when converting raw experimental metadata from spreadsheets into clean, schema-compliant JSON-intermediate representations suitable for validation and format conversion.

## When to use

Apply this skill when you have extracted tabular data into an intermediate JSON form and need to restructure records by mapping input fields to output dictionary keys, collating multiple records under a single grouping field, filtering records by test conditions or exclusion rules, or applying custom transformations before validation or format conversion to a repository schema (e.g., mwTab for Metabolomics Workbench).

## When NOT to use

- Input records are already in target schema format and do not require field mapping or collation
- Conversion directives are missing or do not specify matrix-type transformation logic
- Records should be preserved in their original tabular structure without aggregation or field remapping

## Inputs

- intermediate JSON data (array of record objects)
- conversion directives file (JSON with matrix-type directive configuration including fields_to_headers, collate, exclusion_headers, sort_by, sort_order, test, values_to_str, and code sub-fields)

## Outputs

- list of transformed and collated dictionaries
- structured JSON records with mapped headers and optional groupings

## How to apply

Parse the conversion directives file to extract matrix-type directive configuration, including fields_to_headers mapping, collate grouping field, exclusion_headers, sort_by/sort_order, test filter conditions, and any custom Python code sub-fields. Load the input JSON and iterate over source records, applying field-to-header mapping to construct output dictionary keys. Filter records using the test condition and exclusion criteria to retain only qualifying records. If a collate field is specified, group multiple source records under a single output dictionary keyed by the collate value. Convert specified fields to string representation using values_to_str for type standardization. Sort the resulting list of dictionaries by the designated sort_by field(s) in ascending or descending order. Execute any custom transformation code in the code sub-field to apply user-defined logic. The rationale is to standardize and clean messy metadata into a well-structured intermediate JSON format that can be reliably validated against the Experiment Description Specification and Protocol Dependent Schema before final format conversion.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Provides the convert command that applies matrix-type conversion directives to transform JSON-intermediate data into target formats; the directive engine implements field mapping, collation, filtering, sorting, and custom code execution) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Execution engine for custom transformation code embedded in the code sub-field of conversion directives)
- **jsonschema** (Validates output records against the Experiment Description Specification and Protocol Dependent Schema before final format conversion) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert desired_format your_data.json your_format_data
```

## Evaluation signals

- Output contains the expected number of records after filtering and collation
- All specified headers (from fields_to_headers) are present in each output dictionary
- Records are sorted correctly according to sort_by field(s) and sort_order
- Collated records are properly grouped under the designated collate field key
- Custom transformation code executes without errors and produces expected field values
- Output JSON passes validation against the Experiment Description Specification and Protocol Dependent Schema

## Limitations

- The matrix directive handler requires explicit conversion directives; automatic field mapping is not supported without manual configuration
- Custom Python code execution introduces security and reproducibility risks; only trusted code should be executed
- Complex collation scenarios with multiple grouping criteria may require nested custom code rather than simple field-based grouping
- The collate operation expects a single grouping field; hierarchical or multi-level grouping is not natively supported

## Evidence

- [other] The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields; collate records by a grouping field; map record fields to dictionary keys via headers; exclude fields with exclusion_headers; convert values to strings with values_to_str; or execute custom Python code for complex transformations.: "The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test"
- [other] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [other] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [other] verify the output contains the expected number of records, all specified headers are present in each dictionary, and data types match the conversion directives configuration.: "verify the output contains the expected number of records, all specified headers are present in each dictionary, and data types match the conversion directives configuration."
- [readme] MESSES was created to make it easier. MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a"
