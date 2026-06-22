---
name: conversion-directive-parsing
description: Use when you have validated intermediate JSON data (conforming to the Experiment Description Specification) and need to configure how it should be converted to a supported output format (e.g., mwTab for Metabolomics Workbench submission).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
- This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  - build: coll_messes_cq
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

# conversion-directive-parsing

## Summary

Parse and extract configuration from MESSES conversion directives files to enable structured transformation of intermediate JSON data into target formats. This skill is essential for setting up the conversion pipeline that translates validated experimental metadata from the intermediate JSON representation into format-specific outputs like mwTab.

## When to use

Use this skill when you have validated intermediate JSON data (conforming to the Experiment Description Specification) and need to configure how it should be converted to a supported output format (e.g., mwTab for Metabolomics Workbench submission). The directives file specifies the mapping rules, field transformations, sorting, filtering, and collation logic required before format conversion.

## When NOT to use

- Input data is not in the intermediate JSON format conforming to the Experiment Description Specification; use the extract command first.
- Target format is not one of the supported formats (currently mwTab); directives are format-specific and cannot be reused across incompatible outputs.
- Directives file is malformed or missing required configuration; validate the file structure independently before proceeding to conversion.

## Inputs

- conversion directives file (JSON or YAML format)
- Experiment Description Specification schema reference
- target format specification (e.g., mwTab schema)

## Outputs

- parsed directives object (dict or structured configuration)
- validation report (fields, types, references, errors/warnings)
- transformation plan mapping source fields to target format

## How to apply

Load and parse the conversion directives file (typically JSON or YAML structured configuration) to extract all directive types (simple, matrix, array, conditional) and their sub-fields including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code parameters. Validate the directives against a JSON Schema that enforces required fields and type constraints for the target format. Map each directive to the corresponding input JSON table or record structure, resolving field references and building a transformation plan. For matrix-type directives, extract the collation grouping field, header mappings, and any custom Python code blocks that will be executed during transformation. Verify that all referenced input fields exist in the intermediate JSON and that the output field names (from headers or fields_to_headers) conform to the target format specification. The parsed directives object then serves as the configuration input to the matrix directive handler or other conversion engines.

## Related tools

- **jsonschema** (validation of conversion directives against JSON Schema to enforce format compliance and detect configuration errors) — https://pypi.org/project/jsonschema/
- **MESSES** (Python package that implements directive parsing and the convert command workflow for JSON-to-format transformation) — https://github.com/MoseleyBioinformaticsLab/messes

## Evaluation signals

- All required directive fields (headers, collate, fields_to_headers, etc.) are present and correctly typed according to the target format schema
- Every input field reference in the directives (e.g., in fields_to_headers, sort_by, test conditions) resolves to an existing field in the intermediate JSON structure
- Parsed directives pass JSON Schema validation without errors; warnings are logged for non-critical issues (e.g., optional fields, deprecated configurations)
- The directives object can be successfully passed to the matrix directive handler or other conversion engines without requiring re-parsing or correction
- Custom code sub-fields (if present) parse as valid Python syntax and contain no undefined variable references outside the expected transformation context

## Limitations

- Directives are tightly coupled to a specific target format and cannot be reused for different output formats without manual modification.
- Custom Python code in the code sub-field is executed without sandboxing; malformed or malicious code can cause runtime errors or data corruption.
- Field reference resolution is string-based and does not handle deeply nested JSON structures or array indexing automatically; complex transformations may require custom code.
- The parsing step does not validate that the parsed directives will produce semantically correct output for the target format; validation of the transformation result itself must be performed after conversion.

## Evidence

- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [other] Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test, and code sub-fields.: "Parse the conversion directives file to extract the matrix-type directive configuration, including headers, collate, fields_to_headers, exclusion_headers, values_to_str, sort_by, sort_order, test,"
- [other] utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_): "utilizing `JSON Schema` (`jsonschema`)"
- [intro] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
