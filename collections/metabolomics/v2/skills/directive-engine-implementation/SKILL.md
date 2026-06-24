---
name: directive-engine-implementation
description: Use when when you have intermediate JSON data that must be selectively
  transformed or enriched according to declarative conversion rules—for example, when
  extracting experimental metadata from tabular spreadsheets, you need to map certain
  fields to computed or filtered values, apply conditional.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES
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

# directive-engine-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Implement a conversion directive engine that resolves str-type directives from JSON specification files by parsing override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters to transform tabular or JSON input data into structured JSONized output. This skill is essential for automating complex metadata extraction and format conversion workflows in data curation pipelines.

## When to use

When you have intermediate JSON data that must be selectively transformed or enriched according to declarative conversion rules—for example, when extracting experimental metadata from tabular spreadsheets, you need to map certain fields to computed or filtered values, apply conditional logic to decide whether to populate a field, or concatenate multiple records into a single output string based on sorting and iteration parameters.

## When NOT to use

- Input data is already in the final desired format and does not require field transformation, filtering, or concatenation.
- Conversion logic is too complex for declarative directives and requires imperative procedural code beyond Python eval() scope.
- Input JSON does not conform to the Experiment Description Specification schema required by the conversion engine.

## Inputs

- conversion directives JSON file (containing str-type directive definitions with override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields sub-parameters)
- target input JSON document

## Outputs

- resolved JSON output document with str fields populated according to directive specifications
- validation report against input schema

## How to apply

Parse the conversion directives JSON file to extract all str-type directive definitions and their sub-parameters (override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields). Load the target input JSON document against which directives will be resolved. Evaluate any conditional test sub-directive to determine whether to apply the str directive; skip resolution if test condition fails. If for_each is specified, iterate over the designated array or object collection in the input JSON and apply code transformations (via Python eval() with input_json variable) to each iteration; otherwise apply the directive once to the root or specified record_id target. For each iteration, extract the specified fields and concatenate their values using the delimiter. If sort_by and sort_order are present, sort the records before concatenation. Finally, if override is true, replace existing field values; otherwise preserve existing values and only populate missing fields. Validate the resolved output against the input schema using jsonschema.

## Related tools

- **Python** (language runtime for evaluating code sub-directives via eval() and implementing directive resolution logic)
- **jsonschema** (library for validating resolved JSON output against input schema specifications) — https://pypi.org/project/jsonschema/
- **MESSES** (parent command-line tool and library that orchestrates extract, validate, and convert workflows using the directive engine) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
messes convert desired_format your_data.json your_format_data
```

## Evaluation signals

- Resolved JSON output matches the expected schema structure defined by the input Experiment Description Specification.
- All str fields specified in directives are populated with correct values; fields that were not targeted by directives retain their original values (when override=false) or are overwritten (when override=true).
- Conditional test sub-directives correctly gate directive application: directives are applied only when test conditions evaluate true, and skipped when false.
- for_each iteration produces correctly concatenated field values in the specified delimiter-separated format, and sort_by/sort_order parameters correctly order records before concatenation.
- code sub-directives correctly evaluate Python expressions with the input_json variable in scope and produce expected transformed values.
- jsonschema validation of output against the specified schema returns no errors.

## Limitations

- Code sub-directives rely on eval() for Python expression evaluation, which carries security risks if directives come from untrusted sources and should be sandboxed in production.
- Complex nested record structures or recursive field dependencies may exceed the expressive power of the declarative directive syntax and require custom procedural handlers.
- The engine assumes input JSON conforms to the Experiment Description Specification schema; malformed or non-compliant input will cause resolution failures or validation errors.
- Performance may degrade on very large JSON documents with many records if for_each iteration is applied without efficient filtering (test condition) to reduce the iteration scope.

## Evidence

- [other] The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific record and extracts fields; for_each iterates over all records with optional test filtering and delimiter-separated concatenation; sort_by and sort_order control record ordering before selection or iteration.: "The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific"
- [other] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [other] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification: "The validation step ensures the data that was extracted is valid against the `Experiment Description Specification"
- [other] utilizing `JSON Schema` (`jsonschema`): "utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)"
