---
name: module-integration-verification
description: Use when after rewriting or refactoring a Python module (such as calculate_feature_overlap.py in a metabolomics pipeline) to improve performance, maintainability, or functionality, you need to confirm that the new implementation does not introduce regressions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pytest
  - FERMO
derived_from:
- doi: 10.1038/s41467-024-50111-8
  title: FERMO
- doi: 10.5281/zenodo.7565700
  title: ''
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
  - 10.5281/zenodo.7565700
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# module-integration-verification

## Summary

Verify that a rewritten or refactored Python module passes its existing pytest unit-test suite when executed against a specific version of a scientific software package. This skill ensures that module-level changes maintain backward compatibility and functional correctness within the broader codebase.

## When to use

After rewriting or refactoring a Python module (such as calculate_feature_overlap.py in a metabolomics pipeline) to improve performance, maintainability, or functionality, you need to confirm that the new implementation does not introduce regressions. Run this skill when the module has an established pytest test suite and you want to verify exit code 0 with no assertion failures before merging or deploying.

## When NOT to use

- The module does not have an existing pytest test suite — use manual testing or create a test suite first.
- The module is a new addition with no prior tests — write tests before applying this skill.
- You are testing the entire application end-to-end rather than verifying module-level correctness — use integration testing instead.

## Inputs

- Python module source code (e.g., calculate_feature_overlap.py)
- Existing pytest test suite (test_*.py files)
- Project dependency specification (pyproject.toml, requirements.txt, or setup.py)
- Repository version or tag (e.g., FERMO 0.8.7)

## Outputs

- pytest execution report (verbose output)
- Exit code (0 for success, non-zero for failure)
- Test result summary (number of passed/failed/skipped tests)
- Assertion and error logs (if any failures occur)

## How to apply

Clone or access the repository at the target version (e.g., FERMO 0.8.7 from Zenodo DOI 10.5281/zenodo.7565700). Install pytest and all dependencies listed in the project's requirements or setup configuration (e.g., pyproject.toml). Locate the pytest test suite targeting the rewritten module. Execute pytest with verbose output (e.g., `pytest -v`) to capture detailed test results. Verify that all tests pass with exit code 0 and that no assertion failures or errors are reported. Compare the test output against baseline results to confirm no regressions in module behavior.

## Related tools

- **pytest** (Execute unit tests targeting the rewritten module and report pass/fail status with detailed output) — https://github.com/pytest-dev/pytest
- **FERMO** (Scientific metabolomics package containing the module under verification) — https://github.com/fermo-metabolomics/FERMO

## Examples

```
pytest -v calculate_feature_overlap.py
```

## Evaluation signals

- pytest exits with code 0 (all tests passed)
- Verbose output reports zero assertion failures and zero errors
- Test count and pass rate match or exceed baseline expectations from prior test runs
- No new warnings or deprecation notices related to the rewritten module logic
- Module behavior on edge cases (boundary values, empty inputs, malformed data) remains consistent with prior test expectations

## Limitations

- Test suite must already exist; this skill verifies compliance, not test adequacy. If tests are incomplete or miss critical code paths, passing tests do not guarantee correctness.
- Passing pytest tests verify functional correctness at the unit level but do not guarantee that module changes will not cause issues in downstream dependencies or integration contexts.
- Test execution time and resource requirements are hardware-dependent; execution may be slow on resource-constrained systems (e.g., on standard hardware with limited memory, FERMO example execution took ~104 seconds).
- This skill assumes the pytest environment can be correctly provisioned; missing or conflicting dependencies will cause test failures unrelated to module quality.

## Evidence

- [other] Do the pytest tests for the calculate_feature_overlap.py module pass when executed against the rewritten implementation in FERMO 0.8.7?: "research_question: Do the pytest tests for the calculate_feature_overlap.py module pass when executed against the rewritten implementation in FERMO 0.8.7?"
- [other] Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results. Verify that all tests pass with exit code 0 and no assertion failures or errors.: "Locate and execute the pytest test suite targeting calculate_feature_overlap.py using pytest with verbose output to capture test results. Verify that all tests pass with exit code 0 and no assertion"
- [other] Install pytest and any dependencies listed in the project's requirements or setup configuration.: "Install pytest and any dependencies listed in the project's requirements or setup configuration."
- [readme] Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file.: "Dependencies including exact versions are specified in the [pyproject.toml](./fermo_gui/pyproject.toml) file."
