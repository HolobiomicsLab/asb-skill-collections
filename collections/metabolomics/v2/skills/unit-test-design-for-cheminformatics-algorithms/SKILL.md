---
name: unit-test-design-for-cheminformatics-algorithms
description: Use when you have implemented a custom Filter subclass (e.g., Tanimoto sampling, metabolomics matching, or target filtering) in minedatabase/filters.py and need to verify that similarity scoring, scaling transformations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3303
  tools:
  - pytest
  - RDKit
  - Python
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans: []
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-023-05149-8
  all_source_dois:
  - 10.1186/s12859-023-05149-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-design-for-cheminformatics-algorithms

## Summary

Design and implement pytest-based unit tests for custom cheminformatics filters in Pickaxe that verify correctness of molecular similarity calculations, weight scaling functions, and compound sampling logic. This skill ensures algorithmic correctness and reproducibility when extending reaction network generation with domain-specific filtering criteria.

## When to use

You have implemented a custom Filter subclass (e.g., Tanimoto sampling, metabolomics matching, or target filtering) in minedatabase/filters.py and need to verify that similarity scoring, scaling transformations (e.g., T^4 weighting), and compound selection logic produce correct outputs before integrating into a Pickaxe run.

## When NOT to use

- The filter is a built-in Pickaxe filter (e.g., default threshold filters) that already have existing test coverage — extend existing tests instead.
- The input is a Python script or configuration file rather than a Filter subclass implementation — unit testing is not the appropriate stage.
- You are still designing the filter algorithm and have not yet implemented the _choose_cpds_to_filter method — write pseudocode or design specifications first.

## Inputs

- Custom Filter subclass code (Python class inheriting from Filter abstract base class)
- Test compound set (SMILES strings or RDKit molecule objects)
- Filter parameters (sample_size, target fingerprints, thresholds, weighting exponent, mass/RT tolerances)
- Expected output data (annotated compound selections, similarity scores, weights)

## Outputs

- pytest test suite (Python file in tests/test_unit/test_filters.py)
- Test pass/fail report with assertion results
- Verification that _choose_cpds_to_filter returns correct filtered compound set
- Numerical validation of similarity calculations and weight scaling

## How to apply

Write pytest unit tests in tests/test_unit/test_filters.py that: (1) instantiate your Filter subclass with known test compounds and parameters (e.g., sample_size, target fingerprints, mass tolerance); (2) invoke the _choose_cpds_to_filter method on synthetic or curated compound sets with expected similarity scores or mass differences; (3) assert that returned compounds match expected selections, that similarity scaling (e.g., T^4 weighting) produces correct numerical results, and that sampling distributions follow the inverse complementary CDF method; (4) verify edge cases such as empty compound sets, tie-breaking in sampling, and boundary conditions (e.g., compounds at exact mass tolerance thresholds). Use RDKit fingerprints for reproducible molecular feature computation and pytest fixtures to avoid redundant test setup.

## Related tools

- **pytest** (Test framework for writing and executing unit tests with fixtures to verify filter logic, similarity calculations, and sampling behavior) — https://docs.pytest.org/en/stable/
- **RDKit** (Compute molecular fingerprints for Tanimoto similarity scoring and verify cheminformatic correctness of filter implementations) — https://rdkit.org/docs/api-docs.html
- **Python** (Language for implementing Filter subclasses and writing test code)

## Examples

```
pytest tests/test_unit/test_filters.py::test_tanimoto_sampling_filter -v
```

## Evaluation signals

- All pytest assertions pass: similarity calculations match hand-computed or reference values within numerical tolerance (e.g., 1e-10 for floating-point).
- Returned compound set size equals the specified sample_size or matches the expected filtered set for deterministic filters.
- Weight scaling (e.g., T^4) produces monotonic or expected distribution shapes; inverse complementary CDF sampling is reproducible with seeded random state.
- Edge cases are handled correctly: empty compound input, single compound, all compounds above/below threshold, and compounds at exact boundary tolerances.
- Test code follows pytest conventions (fixtures, parametrize decorators for multiple test cases, descriptive assertion messages) and runs without warnings.

## Limitations

- Unit tests verify algorithmic correctness in isolation but do not test integration with the full Pickaxe reaction generation pipeline or multi-generation filtering dynamics.
- Synthetic test compounds may not capture real-world edge cases (e.g., very large molecules, unusual functional groups, compounds near decision boundaries in multi-dimensional fingerprint space).
- Numerical stability of similarity scoring and weight scaling is not tested across the full range of possible fingerprint values or extreme parameter settings (e.g., very large or very small sample_size).
- Performance and scalability tests (e.g., filtering 1M compounds) are beyond the scope of unit testing; integration or benchmarking tests are required.

## Evidence

- [other] Workflow step for testing: "Write unit test(s) for this custom filter in tests/test_unit/test_filters.py"
- [intro] Tanimoto sampling filter algorithm: "This tanimoto score is scaled and then the distribution is sampled by inverse complementary distribution function sampling to select N compounds"
- [other] pytest and fixture usage: "We utilize [pytest](https://docs.pytest.org/en/stable/) and have defined useful fixtures for use in the tests."
- [other] Main filter method to implement: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [other] Verification of filter similarity and scaling: "verify correct similarity calculation, weight scaling, and sampling behavior"
