---
name: record-filtering-by-field-value
description: Use when when you have a table of JSON records and need to select a subset matching a specific condition—for example, filtering records where 'status=active' before building a string value, or filtering 'experiment_type=MS' before constructing a matrix of dictionary objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# record-filtering-by-field-value

## Summary

Filter JSON records by matching a single field against a specified value before downstream processing (e.g., string construction or matrix transformation). This skill selects only records meeting a field=value condition, reducing the input set to those relevant for the target conversion directive.

## When to use

When you have a table of JSON records and need to select a subset matching a specific condition—for example, filtering records where 'status=active' before building a string value, or filtering 'experiment_type=MS' before constructing a matrix of dictionary objects. Use this when the conversion directive (str, matrix, or section) should operate only on records satisfying a single field equality constraint.

## When NOT to use

- Input records are already pre-filtered by an earlier processing step and no additional field=value selection is needed
- The filter condition requires comparison operators other than equality (e.g., greater-than, less-than, regex pattern matching, or multiple OR conditions)
- The 'test' field specifies a complex boolean expression rather than a simple 'field=value' syntax

## Inputs

- JSON table object with array of records
- conversion directive containing 'test' field (string of form 'field=value')

## Outputs

- filtered array of record objects (subset of input records matching test condition)

## How to apply

Parse the 'test' field from the conversion directive as a string in the form 'field=value', where 'field' is a column name in the input JSON table and 'value' is the literal string to match. Iterate over all records in the table and retain only those where the named field equals the specified value (exact string match, case-sensitive). Pass the filtered record set to the downstream conversion operator (str directive for string building, matrix directive for dictionary array construction, or other handlers). If no 'test' field is specified, use all records unfiltered. This filtering step occurs before sorting (sort_by/sort_order) and grouping (collate) to ensure only matching records proceed through the full pipeline.

## Related tools

- **MESSES** (conversion framework that applies record filtering via 'test' field in str and matrix directives during JSON-to-format transformation) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (validates the structure of the conversion directive (including 'test' field format) and the JSON input table) — https://pypi.org/project/jsonschema/
- **Python** (runtime for parsing, iterating, and filtering JSON records according to 'test' condition)

## Examples

```
messes convert mwtab input.json output.mwtab --pds conversion_directives.json
# where conversion_directives.json contains: {"value_type": "str", "test": "experiment_type=MS", "override": "mass spectrometry"}
```

## Evaluation signals

- Output record count is less than or equal to input record count (filtering never adds records)
- Every record in the output has the specified field present and its value exactly equals the test value string
- Records not satisfying the field=value condition are absent from the output
- Downstream operations (str/matrix directives) receive only the filtered subset and produce output without errors or missing-field exceptions for records that passed the filter
- No records with null or missing values for the filter field appear in the output unless the test value is explicitly 'null' or empty string

## Limitations

- The 'test' syntax supports only exact string equality (field=value); complex comparisons, regex patterns, or logical operators (AND/OR) are not supported by this filter mechanism
- Filtering is case-sensitive; 'Status=active' will not match 'Status=Active'
- If the specified field does not exist in any record, all records are filtered out (empty result set), which may indicate a configuration error rather than a true filtering failure
- No null-handling or default-value specification is available; missing or null field values are treated as non-matching unless the test value is explicitly null

## Evidence

- [intro] test field enables filtering via field=value syntax: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value."
- [other] filtering occurs before sorting and building output: "Filter records using the 'test' field with field=value syntax to select only matching records. 3. Sort the filtered records by fields specified in 'sort_by'"
- [other] matrix directive also supports test-based filtering prior to grouping: "Apply the test filter to select only records matching the specified field=value condition. 4. Sort the filtered records by the fields listed in sort_by"
