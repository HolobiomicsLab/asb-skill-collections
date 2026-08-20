---
name: feature-table-filtering-logic
description: Use when when you have a quantitative feature table (peak intensities across samples) and need to isolate molecular features that show differential abundance between defined sample groups within a specified fold-change range.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0203
  tools:
  - pytest
  - fermo_core
  techniques:
  - LC-MS
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

# feature-table-filtering-logic

## Summary

Implement and validate numeric range filtering on metabolomics feature tables with group-based inclusion/exclusion logic to retain features meeting specified fold-change thresholds. This skill applies parameterized filtering criteria to LC-MS peak intensity data, enabling hypothesis-driven feature prioritization in FERMO dashboard workflows.

## When to use

When you have a quantitative feature table (peak intensities across samples) and need to isolate molecular features that show differential abundance between defined sample groups within a specified fold-change range. Use this skill after loading LC-MS(/MS) metabolomics data into FERMO and before applying higher-level annotation or statistical filters (e.g., phenotype association scoring).

## When NOT to use

- Input is already a pre-filtered feature table without access to raw peak intensity values needed for fold-change recalculation.
- Sample grouping metadata is missing, incomplete, or cannot be reliably mapped to column names in the feature table.
- Fold-change thresholds are not biologically justified or have not been established a priori (avoid post-hoc threshold selection to prevent false discovery).

## Inputs

- Quantitative feature table (CSV format: rows=features/compounds, columns=sample intensities)
- Group specification metadata (sample-to-group mapping with include/exclude criteria)
- Fold-change range parameters (minimum and maximum bounds, numeric)

## Outputs

- Filtered feature table (subset of input rows meeting fold-change and group criteria)
- Filter validation report (row counts, fold-change distribution, group membership verification)

## How to apply

Define the filter interface to accept minimum and maximum fold-change bounds (numeric range specification) and a group specification list (samples to include or exclude from intensity comparison). Implement fold-change calculation logic by comparing feature intensities (e.g., median or mean peak heights) across the specified groups. Apply the filter to the feature table by iterating rows, computing fold-change for each feature, and retaining only features that fall within the specified range AND satisfy the group criteria. Use pytest-based validation: verify that output row count matches the expected filtered set, confirm all retained features have fold-change values within bounds, and check that group inclusion/exclusion logic is correctly applied by inspecting sample membership in calculations.

## Related tools

- **pytest** (Unit and integration testing framework for validating filter correctness, including row count assertions, fold-change threshold verification, and group logic validation)
- **fermo_core** (Underlying library providing metabolomics data structures and operations for fold-change calculation and feature table manipulation in FERMO workflows) — https://github.com/fermo-metabolomics/fermo_core

## Evaluation signals

- Output row count equals expected filtered set size (computed by manual filtering of input table with same parameters)
- All retained features have fold-change values within [min_fc, max_fc] range; no features outside bounds remain in output
- Group inclusion/exclusion logic correctly applied: verify that fold-change calculations use only samples in the specified group subset and exclude all others
- Peak intensity values used in fold-change computation match source table; no data corruption or NaN propagation in calculations
- Pytest assertions pass: `assert len(filtered_table) == expected_rows`, `assert all(min_fc <= fc_vals <= max_fc)`, group membership checks on sample indices

## Limitations

- Filter implementation requires well-formed group metadata; missing or misaligned sample labels will cause incorrect group assignment and invalid fold-change calculations.
- Fold-change calculation method (e.g., median vs. mean intensity comparison, log2 vs. linear scale) must be specified a priori; different methods will yield different retention sets.
- Features with zero or near-zero intensity in one or both groups may produce undefined or extreme fold-change values (infinity, NaN); edge case handling (pseudocount addition, exclusion rules) must be predefined.
- No guidance provided in README on how to handle tied or borderline fold-change values (features exactly at min_fc or max_fc thresholds).

## Evidence

- [other] Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list).: "Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list)."
- [other] Implement the fold-change calculation logic comparing feature intensities across specified groups.: "Implement the fold-change calculation logic comparing feature intensities across specified groups."
- [other] Apply the filter to a test feature table, retaining only features within the specified fold-change range and group criteria.: "Apply the filter to a test feature table, retaining only features within the specified fold-change range and group criteria."
- [other] Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied.: "Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group"
- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
