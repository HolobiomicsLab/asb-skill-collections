---
name: record-sorting-by-multiple-fields
description: Use when when applying str or matrix directives to JSON table data, and
  you need deterministic ordering of records before building output values—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3361
  tools:
  - Python
  - jsonschema
  - MESSES convert command
  license_tier: open
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_
  (`jsonschema <https://pypi.org/project/jsonschema/>`_)
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

# record-sorting-by-multiple-fields

## Summary

Sort JSON table records by one or more fields in ascending or descending order before transformation into string or matrix output formats. This preprocessing step is essential for controlling the order in which records are selected, aggregated, or iterated over during JSON-to-JSON conversion.

## When to use

When applying str or matrix directives to JSON table data, and you need deterministic ordering of records before building output values—e.g., selecting the first matching record after sorting by priority, or grouping records by a collate field that requires consistent ordering within each group.

## When NOT to use

- When the order of records is semantically meaningless or immaterial to the analysis goal (e.g., building an unordered set of unique values).
- When records must retain their original input order as part of the data contract or audit trail.
- When the sort_by fields do not exist or contain inconsistent data types across records (will produce unpredictable or erroring output).

## Inputs

- JSON table records (list of dictionaries with named fields)
- sort_by field specification (list of field names as strings)
- sort_order value ('ascending' or 'descending')

## Outputs

- Reordered list of JSON table records
- Sorted records ready for downstream selection, iteration, or grouping operations

## How to apply

Before building the final string or matrix output, parse the sort_by field (a list of field names) and sort_order field ('ascending' or 'descending') from the conversion directive. Apply the sort_by fields sequentially to reorder the input records; the first field in sort_by is the primary sort key, subsequent fields act as tiebreakers. Use the sort_order value to determine direction globally across all sort_by fields. Execute the sort operation after filtering (test field) but before record selection (first-record, for_each iteration) or grouping (collate). This ensures that downstream operations—such as extracting the first record or building a grouped dictionary—operate on consistently ordered data.

## Related tools

- **Python** (Language in which sort_by and sort_order logic is implemented; handles field extraction and comparator logic.)
- **jsonschema** (Validates sort_by and sort_order field specifications against the conversion directive schema before applying the sort.) — https://pypi.org/project/jsonschema/
- **MESSES convert command** (Orchestrates the full JSON-to-JSON conversion pipeline, applying sort_by and sort_order as preprocessing steps within str and matrix directive evaluation.) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
messes convert desired_format your_data.json output_data --conversion-directive '{"value_type": "str", "sort_by": ["priority", "date"], "sort_order": "descending", "for_each": {"field": "name", "delimiter": ", "}}'
```

## Evaluation signals

- Output records appear in the specified sort order (ascending or descending) according to the primary sort_by field, with tiebreaker fields maintaining secondary order.
- The first record after sorting matches the expected 'first' record for downstream first-record selection or iteration operations.
- Records are sorted before filtering or selection; verify that filtered records respect the sort order when used in for_each or collate grouping.
- sort_order value ('ascending' or 'descending') is correctly applied globally; spot-check that a descending sort reverses the order compared to ascending.
- When sort_by contains multiple fields, verify that ties in the primary field are resolved using secondary (tiebreaker) fields in the order specified.

## Limitations

- sort_by must reference fields that exist in all or most records; records with missing sort fields may sort unpredictably or be placed at the end depending on the Python sort implementation.
- Sorting is case-sensitive for string fields; 'Sample' and 'sample' will not sort together as expected without prior normalization.
- The sort_order parameter is global and applies to all sort_by fields equally; MESSES does not support per-field sort direction (e.g., ascending by field A, descending by field B simultaneously).
- Large tables with many records may incur computational overhead during sort; performance is O(n log n) in the number of records.

## Evidence

- [intro] sort_by and sort_order are used to preprocess records before str and matrix directive evaluation.: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] sort_by and sort_order are applied after filtering and before building the output value.: "Sort the filtered records by the fields listed in sort_by according to sort_order."
- [intro] Sorting is a preprocessing step in the str directive workflow.: "Sort the filtered records by fields specified in 'sort_by' with order determined by 'sort_order' (ascending or descending)."
- [intro] Sorting is a preprocessing step in the matrix directive workflow.: "Sort the filtered records by the fields listed in sort_by according to sort_order."
