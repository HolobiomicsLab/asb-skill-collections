---
name: conditional-record-resolution
description: Use when converting JSON metadata and you need to populate a target field by selecting or iterating over records only when they satisfy a logical test condition (e.g., 'include this record only if a specific field has a particular value').
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3071
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
- utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
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

# Conditional Record Resolution

## Summary

Selectively resolve field values from input JSON records based on test conditions, applying code transformations and field extraction with optional sorting and concatenation. This skill enables intelligent record filtering and multi-value aggregation within the MESSES conversion directive framework, ensuring only records matching specified criteria contribute to the final output.

## When to use

Apply this skill when converting JSON metadata and you need to populate a target field by selecting or iterating over records only when they satisfy a logical test condition (e.g., 'include this record only if a specific field has a particular value'). Use it to avoid cluttering output with unwanted records, to conditionally aggregate multiple field values across matching records, or to apply code-based transformations selectively based on record properties.

## When NOT to use

- The input JSON is not yet extracted from tabular form — use the extract command first to add tagging and convert raw tabular data into intermediate JSON representation.
- No test condition is needed and all records should be unconditionally included — use simpler field mapping directives without conditional logic.
- The target field values are already present and consistent with the schema — override=false and the skill will only populate missing fields, which may not trigger resolution if all records already have the field.

## Inputs

- Conversion directives JSON file (containing str-type directive with test, override, code, record_id, for_each, sort_by, sort_order, delimiter, fields sub-directives)
- Input JSON document conforming to Experiment Description Specification
- Optional: custom JSON Schema for validation

## Outputs

- Resolved JSON output file with conditionally populated fields
- Validation report (schema compliance)

## How to apply

Parse the conversion directives JSON to extract the test sub-directive alongside override, code, record_id, for_each, sort_by, sort_order, delimiter, and fields parameters. Load the target input JSON document. Evaluate the conditional test sub-directive (if present) to determine whether to apply the str directive; skip resolution if the test condition fails. If for_each is specified, iterate over the designated array or object collection, applying the test filter to each element; otherwise apply the directive once to the root or specified record_id target. For each matching iteration, apply code transformation (if present) to resolve dynamic values via eval() with input_json context, extract the specified fields, and concatenate their values using the specified delimiter. Apply sort_by and sort_order to the results before selection or output. If override is true, replace existing field values; otherwise preserve existing values and only populate missing fields. Validate the resolved output against the Experiment Description Specification schema and any format-specific schema (e.g., mwTab schema) before writing to file.

## Related tools

- **jsonschema** (Validates resolved JSON output against Experiment Description Specification and format-specific schemas (e.g., mwTab schema) to ensure compliance before writing to file) — https://pypi.org/project/jsonschema/
- **MESSES** (Command-line package providing extract, validate, and convert commands; the convert command applies conversion directives (including conditional record resolution) to transform extracted JSON to target formats) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime for eval() execution within code sub-directives to resolve dynamic field values based on input_json context during record iteration)

## Examples

```
messes convert mwTab your_data.json your_output --directives conversion_directives.json
```

## Evaluation signals

- Resolved field values are present in the output JSON only for records where the test condition evaluated to true; records failing the test are absent or retain their original values.
- Output JSON validates successfully against the Experiment Description Specification schema and the format-specific schema for the target format (e.g., mwTab).
- For for_each iterations, the number of resolved values matches the count of records passing the test filter, and concatenated values are delimited correctly.
- When override=true, all matching records have updated field values; when override=false, existing values are preserved and only missing fields are populated.
- If sort_by and sort_order are specified, resolved values appear in the declared sort order within the output.

## Limitations

- The test condition relies on Python eval() for code-based logic; complex or malformed test expressions may raise exceptions or produce unexpected boolean results.
- The for_each iteration scope is limited to arrays or objects directly referenced in the JSON; nested or deeply referenced collections may require additional field path specification.
- The delimiter-based concatenation assumes field values are scalars (strings, numbers); nested objects or arrays within selected fields may not concatenate predictably.
- Performance may degrade if for_each iterates over very large record collections without efficient test filtering, as every record is evaluated.

## Evidence

- [other] test condition determination and filtering: "Evaluate conditional test sub-directive (if present) to determine whether to apply the str directive; skip resolution if test condition fails."
- [other] for_each iteration and field extraction: "If for_each is specified, iterate over the designated array or object collection in the input JSON; otherwise apply directive once to the root or specified record_id target."
- [other] code transformation and concatenation: "For each iteration, apply code transformation (if present) to resolve dynamic values, then concatenate selected field values using the specified delimiter and output to the resolved str field."
- [other] sort and override logic: "If sort_by and sort_order sub-directives are present, sort the concatenated or iterated results accordingly. If override sub-directive is true, replace existing str field values; otherwise preserve"
- [other] validation against schema: "Write resolved JSON output to file and validate against input schema."
- [readme] MESSES convert command applies conversion directives: "The convert command of MESSES supports converting JSON data to another JSON format or another supported format."
