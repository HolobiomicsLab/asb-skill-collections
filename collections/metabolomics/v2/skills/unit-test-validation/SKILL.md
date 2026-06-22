---
name: unit-test-validation
description: Use when when you need to confirm that a research tool or package maintains a functioning test suite, especially before adopting it for downstream analysis or before contributing modifications. Triggered by the presence of a CI workflow badge (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MassQL
  - GitHub Actions
  - pytest
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02785-1
  all_source_dois:
  - 10.1038/s41592-025-02785-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-validation

## Summary

Validate that a software package's unit test suite executes successfully via its CI workflow to confirm functional correctness and stability. This skill is essential for confirming that a tool maintains passing tests as a marker of code quality and reproducibility.

## When to use

When you need to confirm that a research tool or package maintains a functioning test suite, especially before adopting it for downstream analysis or before contributing modifications. Triggered by the presence of a CI workflow badge (e.g., GitHub Actions) and the desire to verify that reported test status reflects actual current execution.

## When NOT to use

- The repository does not expose a CI workflow or test suite (no test-unit.yml or equivalent).
- You only need to verify that a badge is displayed; you do not need to independently confirm test execution.
- The tool is a published binary or pre-compiled package where source-level testing is not applicable.

## Inputs

- GitHub repository clone (URL or local path)
- CI workflow definition file (YAML, e.g. .github/workflows/test-unit.yml)
- Dependency specification files (requirements.txt, setup.py, pyproject.toml, or equivalent)
- Test suite source code (unit test files in tests/ directory or equivalent)

## Outputs

- Test execution report (structured log with pass/fail counts, error messages)
- CI workflow execution status (success/failure indicator)
- Environment metadata (Python version, OS, installed dependency versions)
- Validation verdict (pass badge status matches actual execution result: yes/no)

## How to apply

Clone the repository from GitHub and identify the CI workflow file (e.g., test-unit.yml in .github/workflows). Install all dependencies and runtime environment as specified in the repository's configuration files (e.g., requirements.txt, setup.py, Dockerfile). Execute the unit test suite via the same command or workflow used in CI (for MassQL: pytest or the test runner invoked in test-unit.yml). Collect structured output including test counts, pass/fail status, and error logs into a report. Cross-reference the workflow execution results with the reported badge status to confirm alignment; a passing badge should correspond to successful test execution. Document any environment-specific differences (Python version, OS, dependency versions) that may affect reproducibility.

## Related tools

- **MassQL** (Reference implementation whose unit test suite is validated; Python package installable via pip) — https://github.com/mwang87/MassQueryLanguage
- **GitHub Actions** (CI platform that runs the test-unit.yml workflow and reports pass/fail status via badge)
- **pytest** (Likely test runner for MassQL unit tests (inferred from standard Python testing practice))

## Examples

```
cd tests && sh ./get_data.sh && pip install -r requirements_test.txt && python -m pytest
```

## Evaluation signals

- Test execution completes without early exit or fatal errors.
- Reported test pass count matches the count in the workflow log output (no discrepancy).
- CI workflow badge status (passing or failing) aligns with the actual test execution result.
- All test dependencies specified in requirements_test.txt (or equivalent) install successfully.
- Test fixtures (if required, e.g., sh ./get_data.sh in tests/ directory) are properly downloaded and available before execution.

## Limitations

- Test results may vary by Python version (MassQL is tested in Python 3.9 and compatibility with other versions is not fully confirmed per README).
- Test fixtures must be downloaded separately (e.g., sh ./get_data.sh in tests/) and may have network or storage dependencies.
- A passing badge does not guarantee that the test suite reflects current main branch code if the badge was not recently updated.
- Environment-specific test failures (OS, dependency conflicts, resource limits) may not be caught by a single execution.

## Evidence

- [other] Does the MassQL repository's unit test suite pass successfully when executed via the test-unit.yml CI workflow?: "Does the MassQL repository's unit test suite pass successfully when executed via the test-unit.yml CI workflow?"
- [other] The MassQL repository maintains a unit testing CI workflow (test-unit.yml) with an associated passing badge, indicating that the unit test suite executes successfully.: "The MassQL repository maintains a unit testing CI workflow (test-unit.yml) with an associated passing badge, indicating that the unit test suite executes successfully."
- [other] Execute the unit test suite defined in the test-unit.yml CI workflow. Collect test execution results (pass/fail status, test counts, error logs) into a structured report file.: "Execute the unit test suite defined in the test-unit.yml CI workflow. Collect test execution results (pass/fail status, test counts, error logs) into a structured report file."
- [readme] To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: `cd tests && sh ./get_data.sh`: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: `cd tests && sh ./get_data.sh`"
- [readme] We currently test massql in python 3.9, but are figuring out other versions if they work or not.: "We currently test massql in python 3.9, but are figuring out other versions if they work or not."
