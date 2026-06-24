---
name: python-module-integration-and-pipeline-extension
description: Use when you have developed new scoring logic (e.g., average inchikey
  score, neighbourhood score) for an MS/MS spectral analogue search tool and need
  to embed these components into an existing production pipeline that uses a random
  forest to combine multiple features for candidate re-ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS2Query
  - Python
  - GitHub
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- make sure the existing tests still work by running ``python setup.py test``
- fork the repository to your own Github profile and create your own feature branch
  off of the latest master commit
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

# Python module integration and pipeline extension

## Summary

Integrate new Python-implemented scoring components into an existing MS/MS spectral matching pipeline by implementing scoring functions, composing them with existing similarity metrics via a random forest re-ranker, and validating through unit tests and regression testing. This skill enables extension of spectral library search tools with novel scoring logic without disrupting core functionality.

## When to use

You have developed new scoring logic (e.g., average inchikey score, neighbourhood score) for an MS/MS spectral analogue search tool and need to embed these components into an existing production pipeline that uses a random forest to combine multiple features for candidate re-ranking.

## When NOT to use

- Your new scoring logic is not yet validated or lacks a formal algorithm specification — prototype and validate independently first.
- The scoring component is intended to replace (not augment) the random forest re-ranker; this skill assumes composition with existing features, not replacement.
- You have not established unit test coverage expectations or do not have access to known test cases; the skill requires testability verification.

## Inputs

- Candidate match set (library spectra matched to query spectrum)
- Scoring algorithm specification (e.g., inchikey similarity rules, structural neighbourhood definitions)
- Existing MS2Query pipeline module with random forest re-ranker
- Unit test specifications for expected scoring outputs

## Outputs

- Scoring component functions (Python callables returning numeric scores)
- Updated MS2Query pipeline with new scoring features integrated into random forest
- Unit test suite validating each scoring component
- CHANGELOG.md entry documenting new scoring metrics
- Pull request on iomega/ms2query with integrated code and tests

## How to apply

First, implement each new scoring component as a Python function that computes a numeric score across a set of candidate matches, following the scoring algorithm specification (e.g., PR #78). Second, integrate the new scoring functions into the match ranking pipeline by adding them as features to the random forest re-ranker that combines the score with existing similarity metrics (MS2Deepscore, spectral similarity). Third, write unit tests in Python to verify each scoring component produces correct outputs for known input candidates. Fourth, run the existing test suite using `python setup.py test` to confirm no regression in core functionality. Fifth, update CHANGELOG.md documenting the new scoring metrics and their functionality. Finally, create a pull request documenting the integration.

## Related tools

- **MS2Query** (The spectral library matching pipeline into which scoring components are integrated; implements the random forest re-ranker that combines scoring features.) — https://github.com/iomega/ms2query
- **Python** (Implementation language for scoring component functions, unit tests, and integration into the MS2Query module.)
- **GitHub** (Version control and pull request workflow for submitting integrated code changes to the iomega/ms2query repository.) — https://github.com/iomega/ms2query

## Evaluation signals

- Each scoring component function returns numeric output (0–1 range or similar) for all candidate match inputs without error.
- Unit tests pass for known input candidates with expected output values; new tests document the scoring logic.
- Existing test suite runs without regression: `python setup.py test` passes all tests before and after integration.
- The random forest re-ranker successfully incorporates the new scoring features alongside existing metrics (MS2Deepscore, spectral similarity) and produces re-ranked candidate lists.
- CHANGELOG.md is updated with new scoring component names, descriptions, and functionality; pull request is accepted and merged into main branch.

## Limitations

- MS2Query does not perform peak picking or clustering of similar MS2 spectra; input spectra should be preprocessed (e.g., via MZMine) to reduce redundancy before pipeline integration.
- The random forest re-ranker combines features trained on a specific library (e.g., GNPS 2021-12-15); new scoring components may require retraining on new model data if performance degrades.
- Scoring components must be defined for both positive and negative ionization modes; separate model and embedding files are required for each mode.

## Evidence

- [other] Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity.: "Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity."
- [other] Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics.: "Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics."
- [other] Write unit tests in Python to verify each scoring component produces correct outputs for known input candidates.: "Write unit tests in Python to verify each scoring component produces correct outputs for known input candidates."
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
