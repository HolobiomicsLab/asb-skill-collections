---
name: unit-test-coverage-for-conditional-workflows
description: Use when when refactoring or adding workflow branching logic that routes
  spectral results into separate processing paths (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - GitHub
  - Git
  - MS2Query
  - Python unittest / pytest
  - GitHub Actions / CI
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- fork the repository to your own Github profile and create your own feature branch
  off of the latest master commit
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-coverage-for-conditional-workflows

## Summary

Design and implement unit tests that verify conditional branching logic in spectral matching workflows, ensuring that query spectra are correctly routed to either library-match or analog-search pathways based on match classification criteria. This skill ensures regression-free refactoring and maintainability of complex workflow logic in mass spectrometry analysis tools.

## When to use

When refactoring or adding workflow branching logic that routes spectral results into separate processing paths (e.g., true library matches vs. analog search results in MS2Query), unit test coverage becomes critical to prevent regressions and validate that the classification criteria correctly separate result types before downstream analysis.

## When NOT to use

- Input spectral data is already pre-classified into library vs. analog cohorts; branching logic is bypassed.
- Workflow contains no conditional logic or result routing; all spectra follow a single deterministic path.
- Test infrastructure does not exist or cannot run unit tests (e.g., missing Python test harness, no mock data fixtures).

## Inputs

- spectral query data (MGF, mzML, JSON, or pickled matchms objects)
- library spectra with precursor m/z and MS2 spectral similarity scores
- MS2Query model prediction scores (0–1 range)
- precursor m/z differences between query and library matches
- conditional branching logic implementation (Python source code)

## Outputs

- unit test suite covering both workflow branches
- test execution report (pass/fail per branch)
- regression detection (changes in branch routing or result classification)
- code documentation describing branching criteria and test coverage

## How to apply

Identify the conditional criteria that determine workflow branch routing (e.g., precursor m/z difference thresholds, MS2Query model prediction score cutoffs, or match type flags). Write unit tests that exercise both branches: one test suite for spectra that should classify as library matches, and another for spectra that should classify as analog search results. Use concrete test fixtures representing edge cases (e.g., spectra with precursor m/z differences near zero vs. large differences, scores near decision thresholds). Run the test suite with `python setup.py test` before and after code changes to detect regressions. Each test should assert on both the branch taken and any intermediate state changes (e.g., result metadata fields, score calculations). Document the branching criteria and test rationale in code comments so future maintainers understand why each pathway must be verified separately.

## Related tools

- **MS2Query** (spectral matching tool whose workflow branching logic (library match vs. analog search classification) must be unit tested) — https://github.com/iomega/ms2query
- **Python unittest / pytest** (test framework for implementing and executing unit test suites covering both conditional branches)
- **Git** (version control for managing feature branches and PR review of test implementations)
- **GitHub Actions / CI** (continuous integration harness for running test suite on each commit) — https://github.com/iomega/ms2query/actions/workflows/CI_build.yml

## Examples

```
python -m pytest tests/test_workflow_branching.py::test_library_match_branch -v && python -m pytest tests/test_workflow_branching.py::test_analog_search_branch -v
```

## Evaluation signals

- Both workflow branches (library match and analog search classification) are executed by at least one test case; code coverage tools report >80% coverage of branching logic.
- Test suite passes on the original codebase and correctly detects regressions when conditional logic is intentionally broken or criteria thresholds are altered.
- Edge cases near decision boundaries (e.g., precursor m/z difference = 0 ± ε, MS2Query score = 0.7 ± ε) are explicitly tested and produce expected branch routing.
- Test execution time is <1 minute and does not require large data downloads; fixtures use representative subsample of library or synthetic spectra.
- Test output clearly documents which branch was taken for each test case and validates both the result type and any derived metadata (e.g., score, compound class).

## Limitations

- MS2Query produces a prediction for every spectrum regardless of prediction score; tests must enforce the same threshold logic used in production filtering (typically >0.7 for high-confidence matches) to avoid false branch routing.
- Branching logic depends on external data (library spectra, precalculated embeddings); test fixtures must remain synchronized with library versioning to prevent stale branch routing criteria.
- Unit tests can validate branch routing logic in isolation but cannot detect issues in downstream workflow stages (e.g., result interpretation, molecular class estimation) that occur after branching.

## Evidence

- [other] Workflow branching criteria separation: "Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type."
- [other] Test coverage requirement: "Add unit tests covering both library-match and analog-search branching pathways."
- [other] Regression detection via test suite: "Run existing tests with `python setup.py test` to verify no regression."
- [readme] Branch routing based on precursor m/z separation: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results"
- [readme] MS2Query score threshold for confidence: "To give a general indication, a score > 0,7 has many good analogues and exact matches."
