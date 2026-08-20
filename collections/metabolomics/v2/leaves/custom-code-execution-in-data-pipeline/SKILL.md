---
name: custom-code-execution-in-data-pipeline
description: Use when when standard conversion directives (headers, collate, fields_to_headers,
  exclusion_headers, values_to_str, sort_by, test) cannot express the required transformation
  logic, or when domain-specific aggregation, conditional logic, or value derivation
  must be applied to records after field.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
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

# Custom Code Execution in Data Pipeline

## Summary

This skill enables the injection and execution of user-defined Python code within a data transformation pipeline to apply custom logic that cannot be expressed through declarative directives alone. It is essential for complex, non-standard data transformations in extract-validate-convert workflows where built-in field mapping, filtering, and collation are insufficient.

## When to use

When standard conversion directives (headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, test) cannot express the required transformation logic, or when domain-specific aggregation, conditional logic, or value derivation must be applied to records after field mapping and filtering but before final output. Trigger: the conversion specification includes a 'code' sub-field, or the output schema requires computed fields or context-dependent values.

## When NOT to use

- Input data does not require custom transformation logic; standard directives (headers, collate, test, sort_by) are sufficient.
- Code is computationally expensive or performs I/O operations; custom code execution blocks the pipeline synchronously and may not scale to large datasets.
- Transformation logic is proprietary or untrusted; executing arbitrary user-supplied Python code introduces security risk without sandboxing or code review.

## Inputs

- Partially-transformed record list (list of dictionaries) after field-to-header mapping, filtering, collation, and sorting
- Python code string from 'code' sub-field of conversion directive
- Conversion directive configuration (headers, fields_to_headers, collate, exclusion_headers, values_to_str, sort_by, sort_order, test)

## Outputs

- Final transformed record list (list of dictionaries) with custom code applied
- Each record may contain computed or modified fields not present in input JSON

## How to apply

After applying field-to-header mapping, filtering (via test conditions and exclusion_headers), collation, and sorting in the matrix directive handler, insert the user-provided Python code from the 'code' sub-field to execute custom transformations on each output record or the full result set. The code receives the partially-transformed records (dictionaries with mapped keys and excluded fields removed) as input and can modify values, add derived fields, or apply domain-specific logic. The code must be syntactically valid Python and should operate on the record structure produced by prior directive steps. Execution order matters: sorting and custom code are applied last, after collation and filtering, ensuring the code operates on the final pre-output state. Validate that the code does not raise exceptions on sample records and that output records match the expected schema after code execution.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Pipeline framework that orchestrates the extract-validate-convert workflow and executes custom code sub-fields within matrix directive handlers during JSON-to-format conversion) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime environment for parsing, validating, and executing custom code strings supplied in conversion directives)

## Examples

```
messes convert mwtab data.json output_data --directives conversion_directives.json
```

## Evaluation signals

- Custom code executes without runtime exceptions on all records in the input list.
- Output records contain all expected fields from prior directive steps plus any new fields added by custom code.
- Output records conform to the target schema specified in the conversion directive (e.g., mwTab format schema).
- Derived or modified field values in output records are logically consistent with the custom code logic (spot-check a sample of records).
- Record count and field cardinality remain within expected bounds; no records are dropped or duplicated unless explicitly intended by the code.

## Limitations

- Custom code is executed synchronously within the pipeline; performance scales linearly with record count and code complexity.
- No sandboxing or capability restriction; user-supplied code has full access to Python's standard library and system resources, posing security risk in untrusted environments.
- Errors in custom code (e.g., syntax errors, unhandled exceptions, type mismatches) halt the entire conversion pipeline; robust error handling and testing of custom code prior to pipeline execution is essential.
- Custom code sees only the partially-transformed record state after collation and filtering; it cannot access the original input JSON or intermediate transformation states if needed for validation or debugging.

## Evidence

- [other] The matrix directive handler operates by iterating over records in a specified input JSON table to build dictionaries, with capabilities to sort and filter records using sort_by, sort_order, and test fields; collate records by a grouping field; map record fields to dictionary keys via headers; exclude fields with exclusion_headers; convert values to strings with values_to_str; or execute custom Python code for complex transformations.: "or execute custom Python code for complex transformations"
- [other] 9. Validation: verify the output contains the expected number of records, all specified headers are present in each dictionary, and data types match the conversion directives configuration.: "Validation: verify the output contains the expected number of records, all specified headers are present in each dictionary, and data types match"
- [other] 8. Execute any custom transformation code provided in the code sub-field to apply user-defined logic to the output records.: "Execute any custom transformation code provided in the code sub-field to apply user-defined logic to the output records"
- [other] Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields.: "including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
