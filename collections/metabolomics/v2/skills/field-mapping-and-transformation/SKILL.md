---
name: field-mapping-and-transformation
description: Use when converting intermediate JSONized experimental metadata (extracted
  from tagged tabular data) to a target repository format (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - jsonschema
  - messes
  - Python eval()
  license_tier: restricted
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

# field-mapping-and-transformation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply conversion directives (str, override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields) to resolve dynamic field values from input JSON documents, supporting conditional filtering, iteration, Python code evaluation, and sorting. This skill bridges tabular experimental metadata and repository-ready JSON formats via structured directive specifications.

## When to use

Apply this skill when converting intermediate JSONized experimental metadata (extracted from tagged tabular data) to a target repository format (e.g., mwTab for Metabolomics Workbench) and field values must be derived from multiple input records, computed via Python expressions, selected conditionally, or concatenated with custom delimiters. Use when the mapping is not a simple one-to-one field copy but requires iteration, filtering, sorting, or dynamic code evaluation.

## When NOT to use

- Input data is already in the target format and requires no transformation
- Field mapping is a simple one-to-one copy with no conditional logic, iteration, or code evaluation required
- Input is untagged or raw tabular data (use extract command first to convert to intermediate JSON)

## Inputs

- Conversion directives JSON file (containing str-type directive definitions with override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields sub-parameters)
- Input JSON document (intermediate JSONized experimental metadata conforming to Experiment Description Specification)
- Target format schema (JSON Schema for validation of converted output)

## Outputs

- Resolved JSON document with transformed field values
- Validation report confirming output conforms to target format schema

## How to apply

Parse the conversion directives JSON file to extract all sub-parameters for each target field (override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields). Load the input JSON document and evaluate any test sub-directive to determine whether the directive applies (skip if test condition fails). If for_each is specified, iterate over the designated array or object collection; otherwise apply the directive once to the root or specified record_id target. For each iteration, apply code transformation via eval() (if present) to resolve dynamic values, then extract and concatenate the specified field values using the delimiter. Apply sort_by and sort_order (if present) to control record ordering before selection or concatenation. If override is true, replace existing field values; otherwise preserve existing values and only populate missing fields. Write the resolved JSON output and validate against both the input schema and the target format schema (e.g., mwTab schema).

## Related tools

- **messes** (Command-line tool and Python library for executing extract, validate, and convert operations on tabular experimental data; the convert command applies field-mapping-and-transformation directives to JSON documents) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validation library used to validate resolved JSON output against target format schema (e.g., mwTab schema) and Experiment Description Specification) — https://pypi.org/project/jsonschema/
- **Python eval()** (Evaluates code sub-directive expressions with input_json variable in scope to compute dynamic field values during transformation)

## Examples

```
messes convert desired_format your_data.json your_format_data
```

## Evaluation signals

- Resolved JSON document conforms to target format schema (e.g., mwTab) as verified by jsonschema validation
- All conditionally-mapped fields (where test conditions are met) contain expected derived values
- Iteratively-mapped fields (for_each) are concatenated with the correct delimiter and preserve sort_by/sort_order ordering
- Code-evaluated fields (code sub-directive) produce correct Python expression results with input_json in scope
- override=true fields replace existing values; override=false or absent fields preserve existing values and only populate missing fields
- No errors in validation report when output is validated against Experiment Description Specification and Protocol Dependent Schema

## Limitations

- Code evaluation via eval() is restricted to Python expressions and may pose security risks if directives are sourced from untrusted inputs; validate directive files before use
- Complex nested for_each iterations or multi-level field selections may require careful directive specification to avoid circular dependencies or infinite loops
- sort_by and sort_order parameters apply to the collection before field extraction; sorting after field concatenation is not supported
- Field mapping assumes input JSON conforms to Experiment Description Specification; malformed or non-conformant input JSON may produce incomplete or invalid output

## Evidence

- [other] The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific record and extracts fields; for_each iterates over all records with optional test filtering and delimiter-separated concatenation; sort_by and sort_order control record ordering before selection or iteration.: "The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [intro] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a"
- [other] utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_): "utilizing `JSON Schema` and `jsonschema` for validation"
