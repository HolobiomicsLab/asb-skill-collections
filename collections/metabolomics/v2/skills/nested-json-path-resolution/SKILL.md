---
name: nested-json-path-resolution
description: Use when when applying str directives during JSON-to-JSON conversion and the source value is not a direct field but is nested within a table structure—specifically when you need to reference a specific record by record_id, or traverse a sequence of field names (table → fields → nested value) to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - jsonschema
  - MESSES convert command
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

# nested-json-path-resolution

## Summary

Resolve nested JSON paths using table/fields/record_id directives to extract values from deeply nested structures in intermediate JSON representations. This skill is essential when converting tabular experimental metadata into standardized formats like mwTab, where source values may be embedded within complex hierarchical JSON records.

## When to use

When applying str directives during JSON-to-JSON conversion and the source value is not a direct field but is nested within a table structure—specifically when you need to reference a specific record by record_id, or traverse a sequence of field names (table → fields → nested value) to locate the actual string or scalar to be extracted and concatenated into the output.

## When NOT to use

- Input source value is already specified via override (direct constant) or code (Python expression)—path resolution is unnecessary.
- The nested table or record does not exist in the input JSON; the directive will fail during validation.
- Source data is a list or array that should remain as-is; use matrix directives instead for array-to-list conversion.

## Inputs

- intermediate JSON representation with nested table structures
- str directive specification with table, fields, and optional record_id parameters
- input JSON records (may include arrays of nested objects)

## Outputs

- resolved scalar value (string, number, or boolean) extracted from the nested path
- concatenated string value (if part of for_each iteration with multiple records)

## How to apply

During the str directive evaluation phase (after filtering and sorting records), check whether the source is specified via override (direct value), code (Python expression), or nested reference (table/fields/record_id). If using nested reference, resolve the path by: (1) locating the named table within the input JSON structure, (2) if record_id is specified, look up that specific record; otherwise, use the current record context, (3) traverse the fields list in order as nested JSON keys to reach the target value, (4) extract the scalar value at that leaf node, and (5) return it for string concatenation. The rationale is that experimental metadata often organizes auxiliary data (e.g., sample metadata, instrument parameters) in separate nested tables, so path resolution allows flexible reuse without flattening the entire hierarchy.

## Related tools

- **jsonschema** (Validates the structure and schema of intermediate JSON before and after nested path resolution to ensure all referenced tables and fields exist) — https://pypi.org/project/jsonschema/
- **Python** (Executes the nested path traversal logic and evaluates code directives during str directive processing)
- **MESSES convert command** (Orchestrates the application of str directives with nested path resolution during JSON-to-JSON or JSON-to-mwTab conversion) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
messes convert mwTab your_data.json output_mwtab --pds your_schema.json
```

## Evaluation signals

- The resolved value matches the expected type (scalar, not array or object) specified by the schema for the output field.
- JSON schema validation of the final converted output passes without errors related to missing or incorrectly typed fields.
- Spot-check: manually navigate the input JSON using the table/fields/record_id path and verify the extracted value matches the output string.
- For for_each iteration with multiple records, the final concatenated string contains all expected values in the correct order separated by the specified delimiter.
- No null or undefined values appear in the output unless the source data explicitly contained them; missing nested fields should trigger a validation error.

## Limitations

- Nested path resolution assumes a well-formed, schema-compliant intermediate JSON structure; malformed or missing intermediate tables will cause extraction failures.
- The fields list must be traversed in exact order; typos or incorrect field names will fail silently or raise KeyError during execution.
- Record lookup by record_id requires the record_id to uniquely and correctly identify a record in the referenced table; ambiguous or non-existent record_id values are not automatically handled.
- Deep nesting (many levels of fields) may be inefficient for very large JSON structures; the article does not specify performance characteristics for highly nested hierarchies.
- The directive does not support conditional or optional path traversal; if any intermediate key is missing, the operation fails rather than falling back to a default.

## Evidence

- [intro] Nested path resolution via table/fields/record_id is a core mechanism of the str directive.: "table/fields/record_id (nested JSON path) directives"
- [intro] The str directive supports multiple mechanisms for source value specification, including nested reference.: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] During str directive application, record selection and table reference are part of the workflow.: "Select the appropriate source value using override (direct value), code (Python expression), or table/fields/record_id (nested JSON path) directives."
- [intro] The convert command uses directives to transform JSON; nested paths are one mechanism.: "The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives"
- [other] Validation with jsonschema is used to ensure schema compliance of the JSON before conversion.: "This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_), but validation beyond the"
