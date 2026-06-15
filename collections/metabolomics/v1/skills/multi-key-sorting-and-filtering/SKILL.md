---
name: multi-key-sorting-and-filtering
description: Use when when converting tabular data to JSON via the matrix directive, you need to exclude records that fail domain-specific validation (e.g., only retain records where a 'test' condition evaluates to true) and/or reorder the output list by one or more fields in ascending or descending order.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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
- utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes
schema_version: 0.2.0
---

# multi-key-sorting-and-filtering

## Summary

Apply multi-field sorting and record-level filtering to extracted JSON tabular data using sort_by, sort_order, and test directives in the matrix directive handler. This skill enables selective organization and subset extraction of records based on custom Boolean conditions and field-based ordering.

## When to use

When converting tabular data to JSON via the matrix directive, you need to exclude records that fail domain-specific validation (e.g., only retain records where a 'test' condition evaluates to true) and/or reorder the output list by one or more fields in ascending or descending order. This is typical after field-to-header mapping and collation, when the output record set requires both filtering and ranked presentation.

## When NOT to use

- Input records have not yet been mapped to output dictionary keys via fields_to_headers — apply field mapping first.
- The test condition logic is too complex for a simple Boolean expression and requires stateful or cross-record comparisons — use the custom code field instead.
- Records are already in the desired sort order and no filtering is needed — skip this step to avoid redundant processing.

## Inputs

- Conversion directives JSON file with matrix-type directive configuration (including sort_by, sort_order, test sub-fields)
- Input JSON data containing records to be filtered and sorted
- Field mapping configuration (fields_to_headers) and collation directives (if applicable)

## Outputs

- Filtered and sorted list of dictionaries (records) matching test conditions
- Ordered output JSON representation ready for custom code execution or final serialization

## How to apply

Within the matrix-type directive configuration, set the 'sort_by' field to specify the column(s) to order by, 'sort_order' to 'ascending' or 'descending', and 'test' to a Boolean expression that evaluates against record field values to determine inclusion. Parse the directives file to extract these sub-fields, load the input JSON records, apply the test condition to retain only qualifying records, then sort the filtered list using the specified sort_by field(s) and sort_order. The sort and filter operations are applied after field mapping and collation but before custom code execution, ensuring a clean, ordered, and validated record set for downstream transformations or output.

## Related tools

- **MESSES** (Command-line and library framework that implements the matrix directive handler with sort_by, sort_order, test, and fields_to_headers directives for tabular JSON conversion) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the converted JSON output against the Experiment Description Specification and Protocol Dependent Schema to ensure filtered and sorted records conform to schema constraints) — https://pypi.org/project/jsonschema/
- **Python** (Implementation language for iterating over records, evaluating test conditions, and applying multi-key sort operations in the matrix directive handler)

## Evaluation signals

- Output record count matches expected value after applying test filter (verify no records are dropped or duplicated unintentionally).
- All retained records satisfy the test condition (sample spot-check or full validation against test expression).
- Output list is correctly ordered according to sort_by field(s) and sort_order (ascending or descending), confirmed by inspecting the first and last records or by programmatic comparison.
- All specified headers from fields_to_headers are present in each output dictionary.
- Exclusion_headers fields are absent from output records, confirming field-level filtering was applied correctly.

## Limitations

- The test condition must be expressible as a simple Boolean evaluation against individual record fields; complex cross-record or stateful logic requires custom Python code execution instead.
- Sorting performance degrades with very large record counts in memory; no out-of-core or streaming sort options are documented.
- The sort_by and sort_order directives apply to the entire output list after collation, not to individual groups within collated records; use custom code for intra-group sorting.
- Field values used in sort_by must be comparable (strings, numbers, dates); mixed types may produce unpredictable sort order unless converted via the values_to_str directive first.

## Evidence

- [other] The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields: "iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields"
- [other] Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields.: "Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test,"
- [other] Filter records according to the test condition (if provided) and exclusion_headers criteria to retain only qualifying records.: "Filter records according to the test condition (if provided) and exclusion_headers criteria to retain only qualifying records"
- [other] Sort the resulting list of dictionaries according to sort_by field(s) in sort_order (ascending or descending).: "Sort the resulting list of dictionaries according to sort_by field(s) in sort_order (ascending or descending)"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
