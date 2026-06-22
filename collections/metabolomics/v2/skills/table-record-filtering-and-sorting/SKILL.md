---
name: table-record-filtering-and-sorting
description: Use when you have a table with multiple records (e.g., a protocol table with type, id, and description fields) and need to extract a subset of records matching a specific field criterion (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
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
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats
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

# Table Record Filtering and Sorting

## Summary

Apply field-based filtering and multi-field sorting to tabular records before aggregating or transforming them into derived values. This skill enables selective extraction and ordered traversal of protocol or experimental metadata tables when building concatenated strings, matrices, or other structured outputs.

## When to use

You have a table with multiple records (e.g., a protocol table with type, id, and description fields) and need to extract a subset of records matching a specific field criterion (e.g., type='sample_prep'), order them by one or more fields, and then aggregate or transform them into a single output value or matrix. Use this skill when the source data contains heterogeneous record types or when the order of records affects the semantic meaning or format of the output.

## When NOT to use

- The input is already a single record or a pre-filtered, pre-sorted subset; filtering and sorting add unnecessary overhead.
- The source table is empty or all records fail to match the filter criterion; the output will be undefined or empty.
- The sort_by field does not exist in the records or contains non-comparable types (e.g., mixing strings and numbers); sorting will fail or produce unexpected order.

## Inputs

- JSON table with records containing field-value pairs
- Filter specification (field name and value to match)
- Sort specification (list of field names and sort order)
- Delimiter specification (for string concatenation output)

## Outputs

- Filtered and sorted list of records
- Concatenated string value with delimiter-joined field values
- Matrix (list of dictionaries) with filtered and sorted rows

## How to apply

First, parse the input table and identify the filter criterion as a field=value pair (e.g., test='type=sample_prep'). Iterate through the table and retain only records where the specified field equals the given value. Next, sort the filtered records by the fields listed in the sort_by parameter in the order specified, using the sort_order value (either 'ascending' or 'descending') to determine direction. Once sorted, the filtered and ordered records are ready for downstream transformation—such as concatenation into a delimited string (using a delimiter field), conversion into a matrix of dictionaries, or extraction into a nested structure. The rationale is that biological and analytical workflows often depend on record provenance (captured via type fields) and sequence (captured via id fields); filtering isolates semantically coherent subsets while sorting ensures reproducible, workflow-aligned ordering before aggregation.

## Related tools

- **MESSES** (Applies str and matrix directives with for_each patterns to filter and sort protocol and sample preparation records before concatenation or matrix serialization) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Implements filtering and sorting logic via list comprehensions, lambda functions, and sorted() with key functions)
- **jsonschema** (Validates that filtered and sorted records conform to the Experiment Description Specification schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwtab extracted_data.json --directive '{"value_type": "str", "for_each": true, "test": "type=sample_prep", "sort_by": ["id"], "sort_order": "ascending", "delimiter": " ", "fields": ["description"]}' output_data
```

## Evaluation signals

- Verify that only records matching the filter criterion (e.g., type='sample_prep') are present in the output.
- Confirm that the filtered records are sorted in the expected order by the sort_by fields; spot-check the first, middle, and last records to ensure sort_order (ascending/descending) is respected.
- For string concatenation output, validate that the concatenated field values are joined with the specified delimiter and that the order of values matches the sorted record order.
- Check that no records present in the input table are unexpectedly absent from the output (unless they failed the filter); use a record count assertion.
- Compare the output against a known ground-truth or manually verified example (e.g., the SAMPLEPREP_SUMMARY reference value in the task specification) to ensure semantic correctness.

## Limitations

- Filtering and sorting require the specified fields to exist in all input records; missing or null fields may cause the operation to fail or skip records silently.
- Sort stability depends on the implementation; if multiple records have identical sort_by values, their relative order may not be deterministic across runs unless a tiebreaker field is specified.
- The delimiter for string concatenation is applied uniformly; if field values themselves contain the delimiter character, the output string may be ambiguous or unparseable.
- Filter matching is exact (field=value equality); partial matches, regex patterns, or inequality comparisons are not supported in the basic for_each str directive.
- Performance degrades on very large tables (thousands to millions of records); sorting adds O(n log n) complexity per sort_by field.

## Evidence

- [other] Filter criterion definition: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value."
- [other] Sort specification: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] For-each iteration pattern over filtered and sorted records: "The for_each directive iterates over records in the protocol table filtered by test=type=sample_prep, sorts them by id in ascending order, and concatenates their description fields with space"
- [intro] Workflow integration into MESSES convert command: "Apply str directives to produce single string values using override, code, record_id, or for_each patterns"
- [readme] README description of conversion workflow: "The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON based on your specific project schema, fix errors"
