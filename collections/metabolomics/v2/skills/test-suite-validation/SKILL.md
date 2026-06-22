---
name: test-suite-validation
description: Use when after rewriting, refactoring, or updating a core computational module (e.g., calculate_feature_overlap.py in FERMO 0.8.7) to confirm that all existing unit tests pass with zero failures and that the rewritten code does not introduce regressions or break existing contracts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pytest
  - FERMO
derived_from:
- doi: 10.1038/s41467-024-50111-8
  title: FERMO
evidence_spans:
- No discussion section present in document
- See our organization-level document on [CONTRIBUTING]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fermo_2_cq
    doi: 10.1038/s41467-024-50111-8
    title: FERMO
  dedup_kept_from: coll_fermo_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-50111-8
  all_source_dois:
  - 10.1038/s41467-024-50111-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# test-suite-validation

## Summary

Execute a project's pytest test suite against a rewritten or refactored module to verify functional correctness and regression absence. This skill validates that implementation changes preserve expected behavior by running the full test harness with verbose diagnostics.

## When to use

After rewriting, refactoring, or updating a core computational module (e.g., calculate_feature_overlap.py in FERMO 0.8.7) to confirm that all existing unit tests pass with zero failures and that the rewritten code does not introduce regressions or break existing contracts.

## When NOT to use

- The module has no existing unit tests or the test suite does not cover the rewritten code paths.
- The rewritten implementation intentionally changes the module's public API or contract, requiring test suite updates before validation can pass.
- pytest dependencies or the test environment are unavailable or incompatible with the target Python version.

## Inputs

- rewritten or refactored Python module (e.g., calculate_feature_overlap.py)
- pytest test suite file(s) targeting the module
- project configuration (pyproject.toml, setup.py, or requirements.txt) specifying dependencies
- version-controlled repository snapshot (at the commit containing the rewritten implementation)

## Outputs

- pytest exit code (0 = all tests pass, non-zero = failures detected)
- verbose test execution report with individual test outcomes
- assertion failure or error messages (if any)
- test coverage summary and pass/fail counts

## How to apply

Clone or access the repository containing the rewritten module at the target version. Install pytest and all project dependencies specified in the requirements or setup configuration (e.g., pyproject.toml, setup.py, or requirements.txt). Locate and execute the pytest test suite targeting the rewritten module using `pytest` with verbose output (`-v` flag) to capture detailed test results and failure messages. Verify that all tests pass with exit code 0, that no assertion failures or errors are reported, and that the test coverage reflects the module's public API and edge cases. The verbose output provides traceability for any failures and confirms which test cases validated the implementation.

## Related tools

- **pytest** (test execution framework used to run unit tests with verbose output and capture exit codes and failure diagnostics) — https://docs.pytest.org/
- **FERMO** (metabolomics analysis tool containing the rewritten module (calculate_feature_overlap.py) subject to test validation) — https://github.com/fermo-metabolomics/FERMO

## Examples

```
pytest fermo_gui/tests/test_calculate_feature_overlap.py -v
```

## Evaluation signals

- pytest exit code is 0 with no assertion failures or errors reported.
- Verbose output shows 100% test pass rate with all individual test cases listed as PASSED.
- No exceptions, traceback messages, or timeout errors appear in test execution logs.
- Test execution completes without skipped or xfail (expected fail) tests that were previously passing.
- Test coverage metrics (if generated) confirm that critical code paths in the rewritten module are exercised by the passing tests.

## Limitations

- Test suite validation confirms only that existing tests pass; it does not guarantee absence of bugs in untested code paths or edge cases not covered by the original test suite.
- Test suite must be maintained and kept in sync with the rewritten module's API; if the rewrite intentionally changes behavior, tests must be updated first.
- Exit code 0 and passing tests do not verify performance characteristics, memory usage, or compatibility with upstream or downstream modules that depend on the rewritten code.

## Evidence

- [other] Do the pytest tests for the calculate_feature_overlap.py module pass when executed against the rewritten implementation in FERMO 0.8.7?: "Do the pytest tests for the calculate_feature_overlap.py module pass when executed against the rewritten implementation in FERMO 0.8.7?"
- [other] Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results. Verify that all tests pass with exit code 0 and no assertion failures or errors.: "Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results. Verify that all tests pass with exit code 0 and no assertion"
- [other] Clone or access the FERMO repository (fermo-metabolomics/FERMO) at the version containing the rewritten calculate_feature_overlap.py module. Install pytest and any dependencies listed in the project's requirements or setup configuration.: "Clone or access the FERMO repository (fermo-metabolomics/FERMO) at the version containing the rewritten calculate_feature_overlap.py module. Install pytest and any dependencies listed in the"
- [readme] Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file.: "Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file."
