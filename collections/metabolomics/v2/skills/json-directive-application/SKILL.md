---
name: json-directive-application
description: Use when when you have extracted intermediate JSON conforming to the Experiment Description Specification and need to restructure, filter, sort, or aggregate records (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
---

# json-directive-application

## Summary

Apply conversion directives (matrix, str, and other operations) to intermediate JSON representations to transform, filter, aggregate, and format experimental metadata for deposition into structured data repositories. This skill is essential when converting extracted tabular metadata into final repository formats like mwTab.

## When to use

When you have extracted intermediate JSON conforming to the Experiment Description Specification and need to restructure, filter, sort, or aggregate records (e.g., grouping measurement records by metabolite assignment, concatenating protocol descriptions, pivoting sample intensity matrices) before converting to a target repository format. Use this skill when directives are defined in your project's conversion schema and you have validated JSON input.

## When NOT to use

- Input JSON has not been validated against the Experiment Description Specification and project schema — validate first to catch structural errors early.
- Directive parameters (e.g., field names, test conditions, sort keys) do not exist in your input JSON structure — review your schema alignment before applying directives.
- Raw tabular data has not yet been extracted and tagged — use the extract command first to generate intermediate JSON from your CSV or Excel file.

## Inputs

- Intermediate JSON file conforming to Experiment Description Specification
- Conversion directive configuration (matrix or str directive with parameters)
- Validated metadata records with filterable and sortable fields

## Outputs

- Transformed JSON representation (aggregated, filtered, or concatenated)
- Structured data suitable for downstream conversion to repository format (e.g., mwTab)

## How to apply

Load your validated intermediate JSON file containing the records to be transformed. Identify the appropriate directive type (matrix for collation and pivoting, str for concatenation and filtering) based on your desired output structure. For matrix directives with collate='assignment', group records by the specified key field and merge their data fields into unified dictionaries. For str directives with for_each=True, apply optional test filtering (e.g., test='type=sample_prep'), sort the matched records by specified fields and order, and concatenate their string values using the specified delimiter. Execute the convert command with your JSON input and directive configuration, then verify that the resulting output matches the expected structure documented in your schema or format specification.

## Related tools

- **MESSES** (Provides the convert command and directive engine that applies matrix, str, and other transformation directives to intermediate JSON) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates directive output against JSON Schema before conversion to final format) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert desired_format your_data.json your_format_data
```

## Evaluation signals

- Output JSON structure matches the schema defined in your format specification (e.g., mwTab schema for Metabolomics Workbench).
- Filtered records in matrix collate output correctly group by the specified key (e.g., all measurements with the same assignment are in a single dictionary).
- Concatenated string in str directive output matches the expected summary (e.g., SAMPLEPREP_SUMMARY contains all six expected protocol descriptions in correct order with correct delimiter).
- Sorted records appear in the output in the order specified by sort_by and sort_order parameters (ascending/descending).
- No validation errors or schema violations when piping directive output through jsonschema validation against the target format schema.

## Limitations

- Directives depend on input JSON field names and structure being consistent with the Experiment Description Specification; misaligned or missing fields will cause filtering, sorting, or collation to fail silently or produce incomplete output.
- The collate directive requires a single key field to group by; complex multi-field grouping is not directly supported and may require custom directive extensions.
- String concatenation with str directives using delimiters assumes input values are scalar strings; nested objects or arrays in the matched records may produce unexpected serialization.
- Directive behavior is not validated until the convert command executes; errors in directive syntax or parameter mismatches are detected at runtime rather than during schema validation.

## Evidence

- [other] When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by assignment and merge their sample intensity data into a single dictionary?: "When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by"
- [other] When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records, does the output match the expected concatenated summary string?: "When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records, does the output match the expected concatenated summary string?"
- [intro] The convert command was designed to transform the JSON format described in the experiment_description_specification to the JSON version of any of the supported formats and then to the final niche: "The convert command was designed to transform the JSON format described in the experiment_description_specification to the JSON version of any of the supported formats"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [readme] The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized."
