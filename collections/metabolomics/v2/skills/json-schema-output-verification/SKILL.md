---
name: json-schema-output-verification
description: Use when after extracting tabular data into intermediate JSON form or after applying matrix conversion directives (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_3372
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

# json-schema-output-verification

## Summary

Validate converted JSON data against the Experiment Description Specification and format-specific JSON schemas to ensure structural and semantic correctness before repository submission. This skill catches extraction, tagging, and conversion errors early in the MESSES workflow.

## When to use

After extracting tabular data into intermediate JSON form or after applying matrix conversion directives (e.g., collate='assignment') to measurement records, verify that the resulting JSON conforms to the Experiment Description Specification and any protocol-dependent or format-specific schemas before proceeding to final format conversion or deposition.

## When NOT to use

- Input data is already in the target final format (e.g., already mwTab)—skip validation and proceed directly to deposition.
- JSON structure is known to deviate intentionally from the Experiment Description Specification and no schema is provided to accommodate the deviation.
- Validation is deferred: if raw tabular data has not yet been extracted or tagged, extract and validate before attempting to apply conversion directives.

## Inputs

- Intermediate JSON file (output of extract command)
- Converted JSON file (output of matrix conversion directives)
- Protocol Dependent Schema (PDS) JSON file
- Target format identifier (e.g., 'mwtab')
- Optional: additional custom JSON schemas

## Outputs

- Validation report (errors, warnings, pass/fail status)
- Validated JSON data (passed schema checks)
- Error/warning log for data correction

## How to apply

Use the MESSES validate command with the extracted or converted JSON file, specifying the Protocol Dependent Schema (PDS) and the target output format (e.g., 'mwtab'). The validator uses jsonschema to check structural compliance with the Experiment Description Specification, custom project schemas, and built-in format-specific schemas. Compare the validated output against expected schema structure—for example, when applying collate='assignment' to IC-FTMS measurement records, verify that records sharing the same metabolite assignment are correctly grouped into single dictionaries and that all sample intensity data is merged without loss. Address any reported errors or warnings by returning to the original tabular data, correcting tags or values, and re-extracting until validation passes without errors.

## Related tools

- **jsonschema** (Performs schema validation of JSON data against JSON Schema specifications) — https://pypi.org/project/jsonschema/
- **MESSES** (Provides validate command to execute JSON schema validation and report errors/warnings) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime environment for executing MESSES validate command and jsonschema validation)

## Examples

```
messes validate json your_data.json --pds your_schema.json --format mwtab
```

## Evaluation signals

- Validation exits with status 0 (no errors) and reports zero critical errors
- All extracted records conform to the Experiment Description Specification structure (required fields, data types, nested objects)
- Format-specific schema validation passes for the target format (e.g., mwTab schema compliance)
- When collate='assignment' is applied: verify grouped records merge sample intensity data correctly—e.g., two measurement records with the same assignment are consolidated into one dictionary containing both samples' intensity values
- Comparison of output JSON structure against documented schema examples in the MESSES documentation confirms expected field names, nesting, and value types match

## Limitations

- Validation catches structural and schema-level errors but does not verify semantic correctness of metabolite identifications, assignment accuracy, or biological plausibility.
- Custom schemas must be manually provided and maintained; the validator only enforces schemas explicitly supplied.
- Errors and warnings must be manually addressed by returning to the original tabular data and correcting tags or values—the validator does not auto-correct.
- The Experiment Description Specification and Protocol Dependent Schemas are fixed; deviations from the specification require custom schema overrides.

## Evidence

- [other] The validate command of MESSES supports validating JSON data. This is done largely through utilizing `JSON Schema`: "The validate command of MESSES supports validating JSON data. This is done largely through utilizing `JSON Schema`"
- [readme] The validation step ensures the data that was extracted is valid against the `Experiment Description Specification`, the `Protocol Dependent Schema`, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the `Experiment Description Specification`, the `Protocol Dependent Schema`, any additional JSON schema you wish to provide,"
- [other] When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by assignment and merge their sample intensity data into a single dictionary?: "matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by assignment"
- [other] Compare the resulting output against the expected JSON structure documented in the Collate section to verify correctness.: "Compare the resulting output against the expected JSON structure documented in the Collate section to verify correctness."
- [readme] The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized."
