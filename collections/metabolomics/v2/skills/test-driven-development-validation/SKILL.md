---
name: test-driven-development-validation
description: 'Use when when you have implemented or modified a bioinformatic fingerprint generation function (or similar molecular computation module) and need to verify that: (1) the function accepts the correct input types (molecule objects from RDKit or equivalent), (2) it produces fixed-length numerical.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0602
  tools:
  - pip
  - pytest
  - RDKit
  - black
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# test-driven-development-validation

## Summary

Validate computational biology software by executing pytest test suites to ensure fingerprint computation, molecular object handling, and output schema correctness. This skill applies TDD principles to verify that bioinformatic tools produce valid, dimensionally consistent outputs before deployment.

## When to use

When you have implemented or modified a bioinformatic fingerprint generation function (or similar molecular computation module) and need to verify that: (1) the function accepts the correct input types (molecule objects from RDKit or equivalent), (2) it produces fixed-length numerical vector outputs, (3) output dimensionality and data types match the expected specification, and (4) all test cases pass before integrating into a pipeline or publishing results.

## When NOT to use

- Input data is already a pre-computed fingerprint matrix or feature table; validation should occur during fingerprint generation, not on downstream features.
- Test suite does not exist or lacks coverage for the specific fingerprint computation logic; TDD validation requires existing tests.
- The fingerprint function is not yet implemented or is still in design phase; defer testing until implementation is testable.

## Inputs

- Python package source code with test suite (pytest-compatible)
- Molecule object (RDKit Mol or equivalent chemoinformatics format)
- Fingerprint computation function implementing biosynformatic logic

## Outputs

- pytest test report (stdout, exit code)
- Validation status (pass/fail per test case)
- Fixed-length fingerprint numerical vector (if tests pass)
- Fingerprint array with verified dimensionality and data type

## How to apply

First, install the package in development mode using `pip install -e .[dev]` to enable editable installation and access to test dependencies. Identify the fingerprint computation function within the core module that accepts a molecule object as input. Execute the pytest command `pytest tests/` from the repository root to run all unit tests. Examine test output for any failures or errors; valid execution requires all tests to pass. Verify that the test suite covers input validation (e.g., molecule object structure), output schema (fixed-length array, correct dtype), and dimensionality consistency. If tests fail, inspect error messages to diagnose issues in the fingerprint implementation before proceeding to production use.

## Related tools

- **pytest** (Execute test suite to validate fingerprint computation correctness, dimensionality, and data type compliance)
- **pip** (Install package in development mode to enable test execution and access to test dependencies via `pip install -e .[dev]`)
- **RDKit** (Provide Mol object input type to fingerprint computation function; installed as dependency when installing biosynfoni)
- **black** (Format code before running tests to ensure code style consistency, improving test maintainability) — https://github.com/psf/black

## Examples

```
pytest tests/
```

## Evaluation signals

- pytest exits with code 0 (all tests passed); non-zero exit indicates test failure
- Fingerprint output is a fixed-length numerical vector with dimensionality matching expected specification
- Output data type (e.g., numpy array, Python list of floats) matches the function signature and test assertions
- Test coverage includes molecule object validation, null/invalid input handling, and edge cases (e.g., empty molecule, aromatic bonds)
- Pytest output shows 100% pass rate with no skipped or xfailed tests that are critical to fingerprint correctness

## Limitations

- Test suite validity depends on the quality and completeness of test cases; TDD validation cannot catch logic errors if tests themselves are flawed or incomplete.
- pytest execution validates only that the fingerprint function runs without crashing and produces the expected output schema; it does not validate the biochemical or bioinformatic quality of the fingerprint features.
- Passing tests does not guarantee that the fingerprint is suitable for downstream machine learning or classification tasks; external validation (e.g., cross-validation with biosynthetic class predictors) is required to assess predictive utility.

## Evidence

- [other] Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation.: "Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation."
- [other] Verify the output is a valid fingerprint array matching the expected dimensionality and data type.: "Verify the output is a valid fingerprint array matching the expected dimensionality and data type."
- [other] Run pytest tests/ to validate that all fingerprint computation tests pass successfully.: "Run pytest tests/ to validate that all fingerprint computation tests pass successfully."
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [readme] biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research.: "biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research."
