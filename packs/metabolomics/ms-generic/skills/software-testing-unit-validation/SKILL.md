---
name: software-testing-unit-validation
description: Use when after making code modifications (bug fixes, new features, or refactoring) to the MS2Query codebase, or when contributing changes via pull request. The skill is essential before pushing feature branches to the repository or merging changes into master.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3807
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - MS2Query
  - Python
  - pytest or unittest
  - GitHub Actions
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-testing-unit-validation

## Summary

Implement and run automated unit tests to verify that code changes do not break existing functionality and that new features behave as expected. This skill ensures software reliability through continuous validation of individual components before integration.

## When to use

Apply this skill after making code modifications (bug fixes, new features, or refactoring) to the MS2Query codebase, or when contributing changes via pull request. The skill is essential before pushing feature branches to the repository or merging changes into master.

## When NOT to use

- When working on documentation-only changes that do not alter code logic
- For exploratory or prototyping code that is not intended for production
- If test infrastructure is not yet set up in the repository

## Inputs

- Modified Python source code (.py files)
- New or updated test cases (.py test files)
- setup.py configuration with test dependencies

## Outputs

- Test execution report (pass/fail status)
- Coverage metrics (optional)
- Error logs and assertion failures (if tests fail)

## How to apply

Run the existing test suite using `python setup.py test` to validate that your modifications did not break current functionality. If you added new features or modified core logic (such as spectrum preprocessing, MS2Deepscore scoring, or random forest re-ranking), write corresponding unit tests that cover the new code paths. Execute both the existing and new tests together to ensure cumulative correctness. Document test results and failures in your commit or pull request. Only after all tests pass should you proceed to update documentation and push your feature branch to GitHub.

## Related tools

- **Python** (Language in which tests are written and executed via setup.py)
- **pytest or unittest** (Test framework invoked by setup.py test command)
- **GitHub Actions** (Continuous integration platform that automatically runs tests on commits and pull requests) — https://github.com/iomega/ms2query
- **MS2Query** (Software project being tested) — https://github.com/iomega/ms2query

## Examples

```
python setup.py test
```

## Evaluation signals

- All existing tests pass without errors or deprecation warnings
- New tests execute successfully and cover the modified code paths
- Test coverage remains stable or increases after changes
- Continuous integration (GitHub Actions) reports successful builds across MacOS, Windows, and Ubuntu for Python 3.9 and 3.10
- No regressions in downstream functionality (e.g., MS2Query command-line tool still produces expected output on dummy_spectra.mgf matching expected_results_dummy_data.csv)

## Limitations

- Tests may not capture all edge cases or interactions with external libraries (e.g., matchms objects in different formats)
- Test suite does not validate large-scale performance or memory consumption with full GNPS library (>2GB download required)
- Tests are restricted to Python 3.9 and 3.10; compatibility with other Python versions is not continuously validated
- Manual testing on real-world spectra or with custom libraries may still be necessary to detect domain-specific issues

## Evidence

- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [methods] add your own tests (if necessary): "add your own tests (if necessary)"
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
- [readme] After downloading the library files, running on the dummy data is expected to take less than half a minute.: "After downloading the library files, running on the dummy data is expected to take less than half a minute."
- [readme] The expected results can be found in [expected_results_dummy_data.csv](https://github.com/iomega/ms2query/blob/main/dummy_data/expected_results_dummy_data.csv): "The expected results can be found in [expected_results_dummy_data.csv]"
