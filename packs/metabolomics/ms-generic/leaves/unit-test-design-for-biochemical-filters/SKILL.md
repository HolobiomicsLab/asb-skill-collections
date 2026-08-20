---
name: unit-test-design-for-biochemical-filters
description: Use when after implementing a custom Filter subclass (e.g., MetabolomicsFilter, TanimotoFilter) in minedatabase/filters.py, you must write unit tests to validate that _choose_cpds_to_filter correctly identifies compounds to retain/remove.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3372
  tools:
  - pytest
  - RDKit
  - MINE-Database
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-design-for-biochemical-filters

## Summary

Design and implement pytest unit tests for custom biochemical compound filters in MINE-Database to verify filtering logic, edge cases, and parameter handling. This skill ensures filter implementations correctly retain or remove compounds based on mass tolerance, retention time windows, similarity thresholds, or other biochemical criteria.

## When to use

After implementing a custom Filter subclass (e.g., MetabolomicsFilter, TanimotoFilter) in minedatabase/filters.py, you must write unit tests to validate that _choose_cpds_to_filter correctly identifies compounds to retain/remove. Use this skill when you need to verify filtering correctness against known reference compounds, test edge cases (empty peak lists, out-of-tolerance masses, multiple adduct forms), and ensure the filter returns a set of compound IDs matching expected behavior.

## When NOT to use

- Filter code has not yet been written to minedatabase/filters.py—implement the filter first, then test it.
- You are testing the entire Pickaxe reaction network generation end-to-end on real metabolomics data—use integration tests and real database validation instead.
- The filter's _choose_cpds_to_filter logic is trivial or inherited unchanged from base class—minimal unit tests may suffice; this skill is most valuable for complex, custom filtering logic.

## Inputs

- Custom Filter subclass code (minedatabase/filters.py)
- Synthetic or reference compound dictionaries with SMILES strings, IDs, and properties
- Mock metabolomics peak-list CSV (m/z values, optional retention times)
- Filter parameter sets (mass_tolerance in Da, retention_time_tolerance, adduct list)
- Expected retention/removal sets for validation

## Outputs

- pytest unit test suite in tests/test_unit/test_filters.py
- Test pass/fail results with coverage metrics
- Validated filter behavior (set of retained/removed compound IDs)
- Edge-case verification report

## How to apply

Write pytest unit tests in tests/test_unit/test_filters.py that exercise the filter's _choose_cpds_to_filter method with synthetic or known-reference compound dictionaries and parameter sets. For metabolomics filters specifically: (1) create test compounds with known SMILES strings and compute their RDKit-derived molecular weights; (2) generate a mock metabolomics peak-list CSV with m/z values and optional retention time windows; (3) instantiate the filter with mass_tolerance (Da) and retention_time_tolerance parameters; (4) iterate through generation cycles and verify that compounds within the mass_tolerance and retention_time_tolerance of any peak are retained, and those outside are removed; (5) test boundary conditions (masses exactly at tolerance edge, empty peak lists, zero-tolerance scenarios); (6) validate that filter_name returns a string and _choose_cpds_to_filter returns a set of IDs. Use pytest fixtures to manage test compound data and peak-list files to keep tests reproducible and isolated.

## Related tools

- **pytest** (Unit test framework for validating filter _choose_cpds_to_filter method behavior, edge cases, and return types) — https://docs.pytest.org/en/stable/
- **RDKit** (Compute molecular weights from SMILES strings for mass tolerance comparison in filter tests) — https://rdkit.org/docs/api-docs.html
- **MINE-Database** (Framework containing Filter base class, fixtures, and test harness for custom filter validation) — https://github.com/tyo-nu/MINE-Database

## Examples

```
pytest tests/test_unit/test_filters.py::test_metabolomics_filter_mass_tolerance -v
```

## Evaluation signals

- All pytest tests pass with no warnings; filter_name returns a non-empty string
- _choose_cpds_to_filter returns a set (not list or None) of compound IDs
- Compounds with m/z values within mass_tolerance (Da) of any peak in the metabolomics CSV are retained in the output set; compounds outside tolerance are excluded
- Edge cases (empty peak list, zero tolerance, multiple adducts) behave as expected: empty peak list removes all compounds; zero tolerance only retains exact m/z matches; multiple adducts generate correct neutral mass variants
- Test coverage of _choose_cpds_to_filter is ≥80%; _pre_print and _post_print methods (if implemented) are invoked at correct lifecycle points

## Limitations

- Unit tests validate filter logic in isolation; they do not confirm that filters integrate correctly with Pickaxe's multi-generation expansion loop—integration testing required.
- Mock metabolomics peak-list files must accurately represent real CSV format (headers, columns, data types) or tests may not catch runtime errors in production.
- RDKit molecular weight computation assumes valid SMILES strings; malformed SMILES in test compounds will cause parsing failures, not filtering failures.
- Retention time prediction (if implemented) requires trained mordred descriptor models; unit tests cannot validate RT tolerance without pre-trained model data.

## Evidence

- [other] Write pytest unit tests in tests/test_unit/test_filters.py covering edge cases (empty peak-list, out-of-tolerance masses, multiple adduct forms).: "Write pytest unit tests in tests/test_unit/test_filters.py covering edge cases (empty peak-list, out-of-tolerance masses, multiple adduct forms)"
- [other] Validate: verify filter_name returns a string, _choose_cpds_to_filter returns a set of IDs, and test compounds are correctly retained/removed against known reference peaks.: "verify filter_name returns a string, _choose_cpds_to_filter returns a set of IDs, and test compounds are correctly retained/removed against known reference peaks"
- [other] We utilize pytest and have defined useful fixtures for use in the tests.: "We utilize [pytest](https://docs.pytest.org/en/stable/) and have defined useful fixtures for use in the tests"
- [other] _choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [intro] It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks: "It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
