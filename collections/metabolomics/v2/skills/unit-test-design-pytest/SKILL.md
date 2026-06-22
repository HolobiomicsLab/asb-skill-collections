---
name: unit-test-design-pytest
description: Use when after implementing a custom Filter subclass (e.g., Tanimoto threshold filter) in minedatabase/filters.py and before integrating it into a pickaxe_run.py workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pytest
  - RDKit
  - MINE-Database
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- We utilize [pytest](https://docs.pytest.org/en/stable/) and have defined useful fixtures for use in the tests.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
---

# unit-test-design-pytest

## Summary

Design and implement pytest unit tests for custom Filter subclasses in the MINE-Database Pickaxe workflow, verifying that filtering logic correctly enforces threshold values, handles edge cases, and produces expected compound retention/removal outcomes.

## When to use

After implementing a custom Filter subclass (e.g., Tanimoto threshold filter) in minedatabase/filters.py and before integrating it into a pickaxe_run.py workflow. Use this skill when you need to validate that your filter's _choose_cpds_to_filter method correctly identifies which compounds to retain or remove based on your filtering criteria.

## When NOT to use

- Filter logic has not yet been implemented—write the Filter subclass first before designing tests.
- You are testing end-to-end pickaxe runs on real large datasets—use integration tests or benchmarks instead; unit tests should use small synthetic fixture data.
- The filtering task is already validated by visual inspection or manual spot-checking—unit tests provide reproducible automated validation and should be added before deployment.

## Inputs

- Custom Filter subclass code (Python class with __init__, _choose_cpds_to_filter, _pre_print, _post_print methods)
- Target compound list (SMILES strings or file path)
- Candidate compound set with IDs and structures (as SMILES or molecule objects)
- Per-generation threshold value (float, 0.0–1.0)
- RDKit fingerprint type specification (e.g., Morgan, Tanimoto-compatible fingerprint)

## Outputs

- pytest test suite (test_*.py file with multiple test functions)
- Test report showing pass/fail status for threshold enforcement, edge cases, and fingerprint correctness
- Coverage metrics indicating which code paths in Filter._choose_cpds_to_filter are exercised

## How to apply

Write unit tests in tests/test_unit/test_filters.py using pytest fixtures that cover: (1) threshold enforcement—verify that compounds meeting or exceeding the threshold are retained and those below are filtered out; (2) edge cases—test boundary values (0.0, 1.0), empty compound sets, and single-compound scenarios; (3) fingerprint computation—confirm that RDKit fingerprints are generated correctly for target compounds; (4) maximum similarity calculation—validate that the maximum Tanimoto similarity across all targets is computed accurately per candidate compound; and (5) return value correctness—ensure _choose_cpds_to_filter returns the set of compound IDs to be filtered (not retained). Use pytest fixtures to set up test data (target SMILES, candidate compounds, thresholds) and parametrize tests across multiple threshold and compound scenarios to ensure robustness.

## Related tools

- **pytest** (Framework for writing and running unit tests, enabling parametrization and fixture management for Filter test suites) — https://docs.pytest.org/en/stable/
- **RDKit** (Computes molecular fingerprints and Tanimoto similarity scores used within the Filter under test) — https://rdkit.org/docs/api-docs.html
- **MINE-Database** (Provides the Filter base class and project structure in which tests are written and executed) — https://github.com/tyo-nu/MINE-Database

## Examples

```
pytest tests/test_unit/test_filters.py::TestTanimotoThresholdFilter -v --tb=short
```

## Evaluation signals

- All test functions pass without errors or warnings; pytest reports 0 failures.
- Threshold enforcement: compounds with Tanimoto similarity exactly at threshold value are correctly classified (retained if ≥ threshold); compounds just below and just above threshold transition correctly.
- Edge case coverage: tests cover empty compound lists, single-compound targets, threshold=0.0 (all retained), and threshold=1.0 (only perfect matches retained); tests verify behavior is defined for these.
- Return value invariant: _choose_cpds_to_filter returns only compound IDs that exist in the input candidate set; returned set is disjoint from the set of compounds the filter intends to retain.
- Fingerprint determinism: repeated calls to the filter with identical inputs produce identical output (no randomness in fingerprint generation or similarity computation).

## Limitations

- Unit tests exercise Filter logic in isolation and do not validate interaction with the broader Pickaxe expansion workflow (e.g., multi-generation compound accumulation, filter ordering); integration tests are needed for that.
- Test fixture data is typically small and synthetic; performance and memory behavior on real large compound sets (millions of compounds across many generations) may differ.
- Tests validate the filter's correctness given correct RDKit fingerprint inputs; they do not verify RDKit's fingerprint implementation itself—that responsibility lies with RDKit's own test suite.
- Threshold selection policy (how thresholds are set per generation) is outside the scope of unit tests; tests verify enforcement of a given threshold but not whether that threshold is optimal or biologically meaningful.

## Evidence

- [other] Write unit tests in tests/test_unit/test_filters.py to verify threshold enforcement and edge cases.: "Write unit tests in tests/test_unit/test_filters.py using pytest fixtures to verify threshold enforcement and edge cases."
- [other] We utilize pytest and have defined useful fixtures for use in the tests.: "We utilize [pytest](https://docs.pytest.org/en/stable/) and have defined useful fixtures for use in the tests."
- [other] The main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep.: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [intro] Compounds meeting or exceeding the threshold are retained for reaction in the next generation.: "compounds meeting or exceeding the threshold are retained for reaction in the next generation"
- [other] Creating a custom filter requires a working knowledge of python.: "Creating a custom filter requires a working knowledge of python."
