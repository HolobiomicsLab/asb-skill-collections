---
name: test-suite-pass-fail-reporting
description: Use when when you need to verify that a research software package (e.g.,
  MassQL) maintains functional correctness over time, assess the reliability of a
  tool before integration into a workflow, or document test coverage and failure modes
  for reproducibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MassQL
  - GitHub Actions
  - pytest (inferred)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be
  a succinct way to express a query in a mass spectrometry centric fashion.
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

# test-suite-pass-fail-reporting

## Summary

Executes a repository's unit test suite via CI workflow and collects structured pass/fail results, error logs, and test counts into a report. This skill validates that a software package's core functionality is working as expected by reproducing the automated test pipeline.

## When to use

When you need to verify that a research software package (e.g., MassQL) maintains functional correctness over time, assess the reliability of a tool before integration into a workflow, or document test coverage and failure modes for reproducibility. Use this skill when CI badge status alone is insufficient and you need concrete test execution evidence.

## When NOT to use

- The repository does not define a CI workflow or automated test suite — manual test design would be needed instead.
- Test fixtures are extremely large or require external data sources not included in the repository — use lighter integration tests or mock-based unit tests.
- The CI workflow is known to be broken or pinned to an outdated dependency version that cannot be resolved in your environment.

## Inputs

- GitHub repository URL (e.g., mwang87/MassQueryLanguage)
- CI workflow definition file (e.g., .github/workflows/test-unit.yml)
- Repository dependencies specification (requirements.txt, setup.py, environment.yml, or equivalent)
- Test suite source code and fixtures

## Outputs

- Structured test report file (JSON, TSV, or plain text)
- Test execution status (pass/fail/error)
- Test count summary (total tests, passed, failed, skipped)
- Error logs and stack traces for failed tests
- Execution timestamp and environment metadata

## How to apply

Clone the target repository (e.g., mwang87/MassQueryLanguage) from GitHub. Install dependencies and the runtime environment as specified in the repository's configuration files (setup.py, requirements.txt, or equivalent). Locate and execute the unit test suite defined in the CI workflow file (e.g., test-unit.yml in .github/workflows/). Collect test execution results including pass/fail status, total test counts, and any error logs or stack traces. Structure the collected results into a machine-readable report file (e.g., JSON or TSV) that documents test status, execution timestamp, and failure details for downstream analysis or documentation.

## Related tools

- **MassQL** (The subject package whose unit test suite is executed and reported) — https://github.com/mwang87/MassQueryLanguage
- **GitHub Actions** (CI/CD platform hosting the test-unit.yml workflow definition)
- **pytest (inferred)** (Likely unit test framework used to execute and report test results)

## Examples

```
cd tests && sh ./get_data.sh && pip install -r requirements_test.txt && python -m pytest --tb=short -v 2>&1 | tee test_results.log
```

## Evaluation signals

- Report file exists and is valid JSON/TSV with required fields (test_status, total_tests, passed_count, failed_count)
- Test execution completes without environment errors (all dependencies resolved, runtime available)
- Pass/fail counts are consistent: passed + failed + skipped == total_tests
- Error logs for any failed tests include stack traces and assertion details sufficient to diagnose root cause
- Test status matches the CI badge status displayed in the repository README (e.g., passing badge ✓ if all tests pass)

## Limitations

- Test suite execution depends on availability of all declared dependencies; missing or incompatible versions will cause setup failures.
- Fixtures that reference external data sources (e.g., remote spectral databases) may not be available in all execution environments, causing tests to skip or fail.
- CI workflows may contain environment-specific configurations (e.g., Python version pinning to 3.9 as noted in the README) that constrain reproducibility across systems.
- Test execution time and resource requirements (disk, memory, network) are not quantified in the provided documentation and may be prohibitive for large-scale test suites.

## Evidence

- [other] research_question: "Does the MassQL repository's unit test suite pass successfully when executed via the test-unit.yml CI workflow?"
- [other] workflow_definition: "Execute the unit test suite defined in the test-unit.yml CI workflow. 4. Collect test execution results (pass/fail status, test counts, error logs) into a structured report file."
- [readme] ci_badge_evidence: "[![Unit Testing](https://github.com/mwang87/MassQueryLanguage/actions/workflows/test-unit.yml/badge.svg)](https://github.com/mwang87/MassQueryLanguage/actions/workflows/test-unit.yml)"
- [readme] dependency_management: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: `cd tests && sh ./get_data.sh`. You will also want to install the extra requirements for the test suite:"
- [readme] python_version_constraint: "We currently test massql in python 3.9, but are figuring out other versions if they work or not."
