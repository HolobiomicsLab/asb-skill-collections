---
name: unit-test-design-for-data-processing
description: Use when building or extending a data extraction and conversion system
  (such as MESSES) where tabular data is transformed via conversion directives into
  JSON intermediate formats and then into domain-specific schemas.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES
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

# unit-test-design-for-data-processing

## Summary

Design and implement unit tests to validate the correctness of data extraction, validation, and conversion operations in tabular-to-JSON pipelines. This skill ensures that directive handlers (e.g., str, code, record_id resolution) and schema-based transformations produce expected outputs before deploying them in production data curation workflows.

## When to use

Apply this skill when building or extending a data extraction and conversion system (such as MESSES) where tabular data is transformed via conversion directives into JSON intermediate formats and then into domain-specific schemas. Unit tests become essential before validating against JSON Schema and Protocol Dependent Schema, especially when directives support parameterized resolution paths (override, code evaluation, conditional test filtering, sorting, field concatenation) that require verification across multiple input scenarios.

## When NOT to use

- Input data is already validated against the Experiment Description Specification and Protocol Dependent Schema — integration testing or full-pipeline validation is more appropriate at that stage.
- Directive logic is trivial (e.g., a single override with no code, test, or iteration) — minimal test value unless it is part of a larger, complex directive composition.
- You are debugging a single failing data record in production — use logging and manual inspection first; unit tests are for systematic, repeatable verification.

## Inputs

- conversion_directives_json (JSON file defining str-type or other directive with sub-fields: override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields)
- input_json_document (target JSON record or collection against which directive is resolved)
- test_fixture_data (synthetic or representative input data covering parameter combinations and edge cases)
- expected_output_json (gold-standard resolved output for assertion and comparison)

## Outputs

- unit_test_suite (Python test module using unittest or pytest)
- test_execution_report (pass/fail results for each test case)
- resolved_json_output (directive-resolved JSON produced by handler under test)
- test_coverage_metrics (fraction of directive code paths exercised)

## How to apply

Design test cases that exercise each major directive resolution path independently: (1) parse a conversion directives JSON file and corresponding input JSON document; (2) write test cases for each parameter combination (override vs. dynamic code, record_id targeting vs. for_each iteration, conditional test evaluation, sort_by/sort_order application, delimiter-separated field concatenation); (3) execute the directive handler against synthetic or fixture input data with known expected outputs; (4) validate that the resolved JSON output matches the schema and logical invariants (e.g., correct field ordering after sort, correct delimiter usage, correct record selection); (5) use Python's unittest or pytest framework to organize and automate test execution; (6) ensure test coverage spans both happy-path cases (valid inputs, all parameters present) and edge cases (missing fields, empty arrays, null overrides, failed test conditions). The rationale is that conversion directives are core to the MESSES extraction-validate-convert workflow; bugs in directive resolution will propagate into downstream validation and format conversion, so unit testing at the directive handler level catches errors before they reach schema validation.

## Related tools

- **Python** (Language in which unit tests are written and conversion directive handlers are implemented; supports eval() for code directive testing and pytest/unittest test runners)
- **jsonschema** (Library used to validate resolved JSON output against schema during unit tests; ensures directive-resolved output conforms to Experiment Description Specification and Protocol Dependent Schema) — https://pypi.org/project/jsonschema/
- **MESSES** (Framework in which directive resolution and conversion occur; unit tests validate the extract, validate, and convert command behavior before deployment) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
import unittest
from messes.conversion import resolve_str_directive
import json

class TestStrDirectiveResolution(unittest.TestCase):
    def test_override_takes_precedence(self):
        directive = {"override": True, "value": "test_string"}
        result = resolve_str_directive(directive, {})
        self.assertEqual(result, "test_string")
    
    def test_for_each_with_delimiter(self):
        directive = {"for_each": "records", "fields": ["name"], "delimiter": ";"}
        input_data = {"records": [{"name": "A"}, {"name": "B"}]}
        result = resolve_str_directive(directive, input_data)
        self.assertEqual(result, "A;B")

if __name__ == "__main__":
    unittest.main()
```

## Evaluation signals

- All test cases pass and cover override, code, record_id, for_each, test, sort_by, sort_order, delimiter, and fields parameters in isolation and combination.
- Resolved JSON output matches expected_output_json exactly (field values, ordering, concatenation format) when compared via deep equality or jsonschema validation.
- Edge cases (null overrides, empty for_each arrays, failed test conditions, missing fields) are handled gracefully without exceptions or silent data loss.
- Code coverage of directive handler reaches ≥ 90% of conditional branches and parameter combinations.
- When test directives fail (e.g., conditional test evaluates to False), the handler correctly skips resolution and preserves or omits the field according to the override parameter.

## Limitations

- Unit tests cannot guarantee correctness of Python code specified in the code directive parameter; they verify only that eval() executes without error and produces a value. Semantic correctness of user-supplied code must be validated separately.
- Tests are isolated to single directives; interactions between multiple directives in a conversion specification (e.g., one directive feeding output into another) require integration testing beyond the scope of unit tests.
- The test suite is only as comprehensive as the fixtures provided; edge cases not represented in synthetic input data will not be caught until they appear in real data during validation or conversion.
- Unit tests validate directive resolution logic but do not test the full extract-validate-convert pipeline; downstream schema validation and format conversion errors may still occur even if directive unit tests pass.

## Evidence

- [other] The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific record and extracts fields; for_each iterates over all records with optional test filtering and delimiter-separated concatenation; sort_by and sort_order control record ordering before selection or iteration.: "The str directive handler supports multiple resolution paths: override directly specifies a string value; code evaluates Python code via eval() with input_json variable; record_id targets a specific"
- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a"
- [other] If override sub-directive is true, replace existing str field values; otherwise preserve existing values and only populate missing fields.: "If override sub-directive is true, replace existing str field values; otherwise preserve existing values and only populate missing fields."
- [readme] MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "MESSES breaks up the process into 3 steps: extract, validate, and convert. The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a"
