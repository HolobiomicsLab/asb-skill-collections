---
name: json-data-structure-transformation
description: Use when when you have intermediate JSON data in the Experiment Description Specification schema and need to convert it to a different JSON structure or a repository-specific format (e.g., mwTab for Metabolomics Workbench submission).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes_cq
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes_cq
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

# json-data-structure-transformation

## Summary

Transform intermediate JSON data structures into alternative JSON schemas or formats by applying conversion directives (str, matrix, section) that selectively extract, filter, aggregate, and coerce field values. This skill enables conversion of validated experimental metadata into repository-ready formats such as mwTab.

## When to use

When you have intermediate JSON data in the Experiment Description Specification schema and need to convert it to a different JSON structure or a repository-specific format (e.g., mwTab for Metabolomics Workbench submission). Specifically: when str directives are needed to build single string values from table records, when matrix directives are needed to produce lists of dictionaries from tabular data with selective field inclusion/exclusion, or when record filtering, sorting, type coercion, or concatenation across multiple records is required.

## When NOT to use

- Input data is not in intermediate JSON format or does not conform to the Experiment Description Specification schema; use extract command first to convert raw tabular data to intermediate JSON.
- Target format requires structural transformations beyond field selection, filtering, sorting, and type coercion; consider manual schema mapping or custom code.
- Input JSON records lack the fields specified in conversion directives; validate schema conformance with the validate command before attempting conversion.

## Inputs

- Intermediate JSON data in Experiment Description Specification schema format
- Conversion directives specification (JSON configuration with value_type, override, code, record_id, test, sort_by, sort_order, headers, exclusion_headers, values_to_str fields)
- Table records within the input JSON containing fields to be transformed

## Outputs

- Converted JSON data in target schema format
- List of dictionaries (for matrix directives)
- Single string values (for str directives)
- Coerced field values (strings or other specified types)

## How to apply

Define conversion directives for each output field by specifying a value_type (str, matrix, or section). For str directives: select the source value using override (direct specification), code (Python expression), record_id (nested JSON path lookup), or for_each iteration; optionally filter records with test (field=value syntax) and sort with sort_by and sort_order (ascending/descending) before extraction. For matrix directives: specify headers to select columns, use collate to merge records, or use fields_to_headers to copy all fields; apply exclusion_headers to remove unwanted fields; use values_to_str to coerce all field values to strings. Load the intermediate JSON, apply each directive transformation in sequence to each record, aggregate the results, and write the output JSON. Validate the output conforms to the target schema before submission.

## Related tools

- **MESSES** (Python package providing the convert command to execute JSON-to-JSON and JSON-to-format transformations using conversion directives) — https://github.com/MoseleyBioinformaticsLab/MESSES
- **Python** (Runtime environment for loading, iterating over, and transforming JSON records; supports code-based value evaluation in str directives)
- **jsonschema** (Validation library used to validate converted JSON output against target schema before submission) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwtab your_data.json your_data_mwtab
```

## Evaluation signals

- Output JSON conforms to the target schema as validated by jsonschema against the format-specific schema (e.g., mwTab schema).
- All specified fields are present in output dictionaries; excluded fields (via exclusion_headers) are absent.
- String-type coercion is applied consistently: all field values in str and matrix outputs are strings or match the declared type.
- Filtered records (via test parameter) match the specified field=value condition; unmatched records are excluded from string concatenation or iteration.
- Sorted records (via sort_by and sort_order) appear in the output in the requested order (ascending or descending); first-record selection extracts only the first element from the sorted collection.
- Concatenated strings (from for_each iteration) use the specified delimiter correctly between values.
- Comparison of row counts and field names between input and output reveals expected differences based on applied exclusions and aggregations.

## Limitations

- Conversion directives rely on records conforming to the Experiment Description Specification schema; malformed or missing fields will cause directive evaluation to fail or produce incomplete output.
- The str directive assumes all information is contained within a single table; cross-table joins or hierarchical aggregations require custom code or manual preprocessing.
- The matrix directive produces only lists of dictionaries; more complex nested structures may require post-processing or multiple conversion passes.
- Type coercion via values_to_str converts all values to strings uniformly; selective per-field type conversion requires custom Python code expressions.
- Performance may degrade for very large JSON files with thousands of records due to record-by-record iteration; consider partitioning data or optimizing directives.
- Record filtering (test parameter) supports only simple equality checks (field=value); complex boolean logic requires code-based custom expressions.

## Evidence

- [intro] The convert command transforms JSON format to other supported formats using conversion directives: "The convert command was designed to transform the JSON format described in the :doc:`experiment_description_specification` to the JSON version of any of the supported formats"
- [intro] str directive converts input JSON fields into a single string value using override, code, record_id, or for_each patterns: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] matrix directive produces lists of dictionaries from table data using headers, collate, or fields_to_headers variants: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [intro] Conversion directives require value_type field specifying 'str', 'matrix', or 'section': "Every record must have a "value_type" field, and the value of this field determines the other required and meaningful fields the record can have. The allowed values for the "value_type" field are"
- [intro] test parameter filters records with field=value syntax before building string values: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to"
- [intro] sort_by and sort_order parameters sort records before extraction: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] exclusion_headers field removes specified fields from matrix output: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [intro] Convert command converts extracted and validated data from intermediate JSON form to final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] MESSES is a Python package that facilitates the conversion of tabular data into other formats: "MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats."
- [readme] The expected workflow includes extract, validate, and convert steps: "The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON based on your specific project schema, fix errors"
