---
name: filter-parameter-validation
description: Use when reconstructing or modifying dashboard filters (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pytest
  - fermo_core
derived_from:
- doi: 10.1038/s41467-024-50111-8
  title: FERMO
evidence_spans:
- No discussion section present in document
- See our organization-level document on [CONTRIBUTING]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fermo_2_cq
    doi: 10.1038/s41467-024-50111-8
    title: FERMO
  dedup_kept_from: coll_fermo_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-50111-8
  all_source_dois:
  - 10.1038/s41467-024-50111-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# filter-parameter-validation

## Summary

Validate that filter parameters (numeric ranges, group inclusion/exclusion criteria, thresholds) are correctly specified and enforced before applying them to feature tables. This skill ensures filter logic operates on well-formed inputs and produces reproducible, auditable results.

## When to use

Apply this skill when reconstructing or modifying dashboard filters (e.g., fold-change, phenotype score) that accept user-specified numeric bounds or group membership criteria, especially when those filters have not been formally tested or when filter behavior needs to be verified against a reference implementation.

## When NOT to use

- Input is already a feature table that has been filtered by a previously validated pipeline—skip re-validation unless filter logic has changed.
- Filter parameters are hard-coded constants in a mature, long-running production system—validate only if source code is modified or new data types are introduced.
- Numeric bounds or group criteria come from an external, certified data source with its own validation guarantees.

## Inputs

- Feature table (numeric matrix with features as rows, samples/groups as columns)
- Fold-change or phenotype-score filter specification (minimum bound, maximum bound, group list, inclusion/exclusion flag)
- Group metadata (sample-to-group mapping)

## Outputs

- Validated filter parameter set (confirmed numeric and logical consistency)
- Filtered feature table (rows retained after applying validated bounds and group criteria)
- pytest test report (pass/fail on row count, threshold compliance, and group logic)

## How to apply

Define the filter interface to accept minimum and maximum numeric bounds (e.g., fold-change thresholds) and a group specification (include/exclude list). Implement the filter calculation logic that compares feature intensities or scores across specified groups. Before applying the filter to a production feature table, use pytest to validate: (1) that output row count matches the expected filtered set size, (2) that all retained features numerically satisfy the fold-change threshold or other metric, and (3) that group inclusion/exclusion logic is correctly applied. This validation step prevents silent failures where filters silently pass wrong rows or drop correct ones.

## Related tools

- **pytest** (Unit testing framework used to validate filter correctness: verify output row count, confirm all retained features meet the fold-change threshold, and check group inclusion/exclusion logic.) — https://github.com/pytest-dev/pytest
- **fermo_core** (Core metabolomics data processing library that implements fold-change calculation and filtering logic for the FERMO dashboard.) — https://github.com/fermo-metabolomics/fermo_core

## Evaluation signals

- Output feature table row count exactly matches the expected count of features passing both the numeric threshold (fold-change range) and group criteria.
- All retained features in the output table have fold-change values (or phenotype scores) within the specified minimum and maximum bounds when calculated across the specified groups.
- Group inclusion/exclusion filtering correctly filters features: if 'include' is specified, only features from those groups appear; if 'exclude', no features from excluded groups appear.
- pytest assertions pass without error for all test cases covering boundary conditions (e.g., features at exactly the min/max threshold, single-group filters, empty group lists).
- Spot-check: manually verify 2–3 features from the filtered output table against the original unfiltered table to confirm the fold-change calculation and group selection are correct.

## Limitations

- The README provides only header content and overview; the technical specification of fold-change calculation (e.g., whether it is log2-fold-change, arithmetic ratio, or another metric) is not documented in the provided materials.
- Filter validation assumes that input group metadata is correctly formed and complete; validation does not detect missing or mislabeled samples.
- pytest validation is unit-level and does not account for edge cases in upstream data preparation (e.g., zero intensities, missing values) that may cause fold-change to be undefined or produce NaN/Inf.

## Evidence

- [other] Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied.: "Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group"
- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
- [other] Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list).: "Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list)."
- [other] Implement the fold-change calculation logic comparing feature intensities across specified groups.: "Implement the fold-change calculation logic comparing feature intensities across specified groups."
