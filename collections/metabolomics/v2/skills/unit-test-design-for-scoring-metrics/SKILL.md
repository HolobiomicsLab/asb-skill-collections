---
name: unit-test-design-for-scoring-metrics
description: Use when when implementing new scoring components (inchikey score, neighbourhood score, or similar structural/spectral similarity metrics) that are integrated into an MS/MS candidate re-ranking pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - MS2Query
  - GitHub
  - Python unittest / pytest
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
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

# unit-test-design-for-scoring-metrics

## Summary

Design and implement unit tests to verify that scoring metric computations (e.g., average inchikey score, neighbourhood score) produce correct outputs for known candidate inputs in MS/MS library matching workflows. This ensures reliability of re-ranking and match confidence scoring before integration into production pipelines.

## When to use

When implementing new scoring components (inchikey score, neighbourhood score, or similar structural/spectral similarity metrics) that are integrated into an MS/MS candidate re-ranking pipeline. Unit tests should be written before or immediately after implementation to catch regressions in scoring logic before running full test suites and pushing feature branches.

## When NOT to use

- Do not use this skill in place of integration tests or end-to-end validation; unit tests verify individual scoring functions in isolation, not the full re-ranking pipeline or MS2Query workflow.
- Do not use when the scoring metric is already well-established in the literature and no new implementation changes have been made; focus testing effort on novel or modified components.
- Do not use for ad-hoc exploration or hypothesis testing; unit tests require defined inputs and expected outputs, which is incompatible with exploratory data analysis.

## Inputs

- Candidate match set (list of library spectra with metadata: inchikey, precursor m/z, structural similarity features)
- Query spectrum metadata (precursor m/z, mass spectral peaks)
- Known expected output scores or score ranges for validation

## Outputs

- Unit test code (Python test methods/functions)
- Test coverage report (% of scoring component code paths tested)
- Pass/fail results from `python setup.py test`
- Documented test cases with rationale and edge cases covered

## How to apply

Create unit tests in Python that cover both typical and edge-case inputs for each scoring component. For each test: (1) define a known set of candidate matches with their structural or spectral metadata; (2) call the scoring function with that input; (3) assert the output matches an expected score or score range; (4) test boundary conditions (e.g., single candidate, all identical candidates, precursor m/z differences of 0 vs. non-zero). Run tests locally using `python setup.py test` to verify no regression in existing functionality. Document each test with the rationale for the expected output (e.g., why a particular candidate set should yield a specific average inchikey score).

## Related tools

- **MS2Query** (Target system for which scoring metric unit tests are designed; provides the re-ranking pipeline and match scoring framework to be tested) — https://github.com/iomega/ms2query
- **Python unittest / pytest** (Testing framework for writing and executing unit tests of scoring components)

## Examples

```
python -m pytest tests/test_scoring_metrics.py::test_average_inchikey_score -v
```

## Evaluation signals

- All unit tests pass locally without errors (e.g., `python setup.py test` returns exit code 0).
- Test coverage report shows ≥80% coverage of scoring component code paths (branches and logic statements).
- Tests correctly identify regressions: if the scoring function is intentionally modified (e.g., changing a weighting factor), at least one test fails as expected.
- Edge case tests (single candidate, identical candidates, extreme precursor m/z differences) execute without crashes and produce scores within valid range [0, 1].
- Test assertions are deterministic and reproducible: re-running the test suite multiple times yields identical pass/fail results.

## Limitations

- Unit tests validate individual scoring functions in isolation; they do not verify that the combined scoring pipeline (average inchikey score + neighbourhood score + other features) ranks candidates correctly in realistic MS/MS datasets.
- Tests require manually curated expected outputs for known candidate sets, which may not cover all corner cases or real-world score distributions observed in large spectral libraries.
- MS2Query's random forest re-ranking model combines multiple features; unit tests for scoring components alone cannot predict or validate the final model prediction score (0–1 range), which depends on feature interactions and model weights.

## Evidence

- [other] Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity.: "Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity."
- [other] Write unit tests in Python to verify each scoring component produces correct outputs for known input candidates.: "Write unit tests in Python to verify each scoring component produces correct outputs for known input candidates."
- [other] Run existing test suite using `python setup.py test` to ensure no regression in core functionality.: "Run existing test suite using `python setup.py test` to ensure no regression in core functionality."
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1"
