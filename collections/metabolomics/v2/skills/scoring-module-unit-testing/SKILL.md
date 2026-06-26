---
name: scoring-module-unit-testing
description: Use when after implementing or modifying the scoring module that computes
  average InChIKey scores and neighbourhood scores for candidate matches, or when
  integrating new scoring logic into an existing MS2Query pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - pytest
  - setuptools
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# scoring-module-unit-testing

## Summary

Validate the correctness of MS2Query scoring module outputs (InChIKey score and neighbourhood score) through automated unit tests that verify score computation, output record structure, and value ranges. This skill ensures that candidate match records are properly constructed and scores fall within expected bounds before deployment.

## When to use

Apply this skill after implementing or modifying the scoring module that computes average InChIKey scores and neighbourhood scores for candidate matches, or when integrating new scoring logic into an existing MS2Query pipeline. Use it as a gate before writing scored candidates to the output file to prevent propagation of malformed or out-of-range scores into downstream analyses.

## When NOT to use

- Scoring module has already been validated and deployed in production with stable, frozen parameters—unit tests are not a runtime skill.
- Input candidate matches lack InChIKey annotations or spectral metadata; tests will fail for missing data, not module logic.
- You are validating end-to-end MS2Query search performance (including ranking and recall); use integration tests or benchmark datasets instead.

## Inputs

- Candidate matches from library-matching step (with match identifiers and InChIKey annotations)
- Spectral similarity metrics (MS2Deepscore embeddings or related scoring data)
- Mock or real MS2 spectra with known ground-truth InChIKey labels

## Outputs

- Unit test results (pass/fail, coverage report)
- Validated candidate records with InChIKey score and neighbourhood score fields
- Test assertion logs documenting score range and structural validity

## How to apply

Write unit tests using Python pytest or setuptools that: (1) load mock candidate matches with known InChIKey annotations and spectral similarity metrics; (2) invoke the scoring module to compute average InChIKey score and neighbourhood score; (3) verify that output records contain all standardized fields (candidate ID, InChIKey score, neighbourhood score) with correct data types; (4) assert that computed scores fall within the valid range [0, 1]; (5) validate internal consistency (e.g., no NaN or infinity values); (6) run the full test suite before committing changes via `python setup.py test`. The rationale is that scoring is a critical bottleneck for match reliability—tests catch bugs in score aggregation logic, neighbourhood density calculations, or edge cases (empty candidate sets, tied scores) before results reach users.

## Related tools

- **pytest** (Framework for writing and executing unit tests to validate scoring module logic and output schema)
- **setuptools** (Python packaging and test runner for executing test suite via `python setup.py test`)
- **MS2Query** (Source tool containing the scoring module being tested) — https://github.com/iomega/ms2query

## Examples

```
python setup.py test
```

## Evaluation signals

- All pytest/setuptools tests pass with no assertion errors or exceptions
- Output records contain exactly the expected fields: candidate ID, InChIKey score, neighbourhood score, with correct data types (numeric for scores)
- Computed InChIKey and neighbourhood scores are in range [0.0, 1.0] and contain no NaN, infinity, or negative values
- Score aggregation logic (averaging across InChIKey layers, density computation) produces consistent results on repeated runs with identical inputs
- Test coverage includes edge cases: empty candidate sets, single candidate, tied scores, missing InChIKey annotations

## Limitations

- Unit tests validate internal correctness but do not guarantee that scores reflect true spectral similarity or analogue quality; integration testing against ground-truth matched libraries is needed for that.
- Tests depend on the availability and correctness of mock data or fixture candidate matches; if fixtures are outdated or incorrect, tests will produce false negatives.
- The provided README does not detail the exact formula for InChIKey score aggregation or neighbourhood density calculation, so test expectations must be inferred from code inspection or legacy documentation.

## Evidence

- [readme] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] Validate output record structure and score ranges using unit tests via Python pytest or setuptools.: "Validate output record structure and score ranges using unit tests via Python pytest or setuptools."
- [other] Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers.: "Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers."
- [other] Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score).: "Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score)."
- [readme] add your own tests (if necessary): "add your own tests (if necessary)"
