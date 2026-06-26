---
name: python-unit-test-execution
description: Use when after rewriting or modifying a Python module (such as calculate_feature_overlap.py
  in a metabolomics analysis tool) and you need to verify that the refactored code
  maintains backward compatibility and correctness against the original test suite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3050
  tools:
  - pytest
  - FERMO
  license_tier: open
  provenance_tier: literature
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

# python-unit-test-execution

## Summary

Execute a pytest unit-test suite against a Python module to verify that all tests pass with exit code 0 and no assertion failures, confirming correctness of the implementation under test.

## When to use

After rewriting or modifying a Python module (such as calculate_feature_overlap.py in a metabolomics analysis tool) and you need to verify that the refactored code maintains backward compatibility and correctness against the original test suite.

## When NOT to use

- The module has no existing test suite — use test_driven_development or manual code review instead.
- Tests are known to be broken or outdated — fix or update the test suite first before executing.
- The testing environment cannot be replicated (e.g., missing system dependencies or conflicting package versions that cannot be resolved).

## Inputs

- Python module source code (e.g., calculate_feature_overlap.py)
- pytest test suite files (test_*.py)
- Project configuration (pyproject.toml or requirements.txt)
- Python environment with pytest installed

## Outputs

- pytest exit code (0 for success)
- Test execution report (verbose output listing all tests and pass/fail status)
- No assertion failures or errors in the test output

## How to apply

Clone or access the repository containing both the module under test and its pytest test suite. Install pytest and any dependencies listed in the project's requirements or setup configuration (e.g., pyproject.toml). Locate the test files targeting the module of interest. Execute pytest with verbose output to capture detailed test results using a command like `pytest path/to/test_file.py -v`. Verify that the exit code is 0 and that all assertions pass without errors. Review the verbose output to ensure 100% of tests passed and no skipped or xfailed tests unexpectedly occurred.

## Related tools

- **pytest** (Test runner and framework for executing unit tests and capturing pass/fail results with verbose reporting) — https://github.com/pytest-dev/pytest
- **FERMO** (Metabolomics analysis tool containing the calculate_feature_overlap.py module and associated test suite) — https://github.com/fermo-metabolomics/FERMO

## Examples

```
pytest fermo_gui/tests/test_calculate_feature_overlap.py -v
```

## Evaluation signals

- pytest exit code is exactly 0 (indicates all tests passed)
- Verbose output shows '== X passed in Y.XXs ==' with no failures, errors, or skipped tests
- All assertion statements in test files execute without raising AssertionError
- No ImportError, ModuleNotFoundError, or dependency resolution errors occur during test execution
- The module's public API and return types match the expectations encoded in the test suite (e.g., function signatures, output shapes for feature overlap calculations)

## Limitations

- Test execution only validates that the current implementation matches the test expectations; it does not validate that the tests themselves are correct or comprehensive.
- Exit code 0 confirms test passage but does not measure code coverage — all code paths may not be tested.
- pytest execution is environment-dependent; tests may pass locally but fail in CI/CD if dependencies or Python versions differ.
- Tests may be xfailed or skipped intentionally; a 'passing' run may include skipped tests that mask real issues.

## Evidence

- [other] Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results.: "Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results."
- [other] Verify that all tests pass with exit code 0 and no assertion failures or errors.: "Verify that all tests pass with exit code 0 and no assertion failures or errors."
- [other] Install pytest and any dependencies listed in the project's requirements or setup configuration.: "Install pytest and any dependencies listed in the project's requirements or setup configuration."
- [readme] Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file.: "Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file."
