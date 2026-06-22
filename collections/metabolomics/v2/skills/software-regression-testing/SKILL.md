---
name: software-regression-testing
description: Use when after implementing code changes to MS2Query (e.g., modifying the workflow branching logic for true library matches vs. analog search results), before committing or pushing to the repository.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3047
  tools:
  - GitHub
  - Git
  - MS2Query
  - Python
  - pytest or unittest framework
  - GitHub Actions CI
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
- push your feature branch to (your fork of) the ms2query repository on GitHub
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query_cq
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-regression-testing

## Summary

Regression testing validates that code changes do not break existing functionality by running the full test suite after modifications. In MS2Query development, this ensures that new features or bug fixes maintain compatibility with the existing MS2Query spectral matching workflow.

## When to use

After implementing code changes to MS2Query (e.g., modifying the workflow branching logic for true library matches vs. analog search results), before committing or pushing to the repository. Also required during pull request reviews to verify that new contributions do not degrade existing MS2Query functionality.

## When NOT to use

- When you have not yet made any code changes (no changes to test).
- When working on documentation-only updates that do not modify any Python source code.
- Before first understanding what the existing test suite covers; review tests before making changes to ensure your modifications align with expected behavior.

## Inputs

- Modified Python source code (MS2Query codebase with feature branch changes)
- Existing unit test suite (located in the repository)

## Outputs

- Test execution report (pass/fail status for each test)
- Regression test log (stdout/stderr from test run)
- Confidence that no existing functionality was broken by the changes

## How to apply

Execute the full test suite using `python setup.py test` to verify that all existing tests pass after your code modifications. If any tests fail, inspect the failure output to identify which components were affected by your changes, then revise your implementation to restore passing status. This step should be performed locally before pushing your feature branch and again automatically during continuous integration when the pull request is created. The test results serve as the gate: only push when all tests pass.

## Related tools

- **Python** (Runtime environment for executing regression test suite via setup.py test command)
- **pytest or unittest framework** (Test execution framework invoked by setup.py to run unit tests)
- **GitHub Actions CI** (Continuous integration system that automatically runs regression tests on pull requests (CI_build.yml workflow)) — https://github.com/iomega/ms2query/actions/workflows/CI_build.yml
- **MS2Query** (Target library whose functionality is validated by regression testing) — https://github.com/iomega/ms2query

## Examples

```
python setup.py test
```

## Evaluation signals

- All tests return exit code 0 (successful completion) when running `python setup.py test`
- No test failures, errors, or skipped tests appear in the test execution output
- The test output confirms that the same number of tests pass before and after your code changes (or increased if you added new tests)
- GitHub Actions CI workflow completes with a green status (all checks pass) after your pull request is created
- Pull request can be merged without test-related blockers on the upstream iomega/ms2query repository

## Limitations

- Regression testing only validates existing test coverage; it cannot detect bugs or regressions in untested code paths or new features not covered by current unit tests.
- Test execution time may be lengthy for large codebases; developers should run tests locally before pushing to avoid slow feedback loops in CI.
- Tests may pass on the developer's machine but fail in CI if there are environment-specific dependencies or platform differences (e.g., Windows vs. Linux).
- Regression tests cannot catch performance regressions (e.g., slowdowns) unless explicit performance tests are included in the suite.

## Evidence

- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] Run existing tests with `python setup.py test` to verify no regression.: "Run existing tests with `python setup.py test` to verify no regression."
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
- [other] fork the repository to your own Github profile and create your own feature branch off of the latest master commit: "fork the repository to your own Github profile and create your own feature branch off of the latest master commit"
- [other] create the pull request, e.g. following the instructions [here](https://help.github.com/articles/creating-a-pull-request/): "create the pull request, e.g. following the instructions"
