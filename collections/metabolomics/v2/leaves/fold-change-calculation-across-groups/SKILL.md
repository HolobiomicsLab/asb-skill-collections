---
name: fold-change-calculation-across-groups
description: Use when when you have a quantified peak table (LC-MS feature intensities)
  with sample metadata assigning samples to discrete groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pytest
  - fermo_core
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# fold-change-calculation-across-groups

## Summary

Calculate fold-change values for metabolomic features across user-specified sample groups to identify differentially abundant molecular features. This skill filters feature tables by numeric fold-change thresholds and group inclusion/exclusion criteria, enabling hypothesis-driven prioritization of phenotype-associated features in metabolomics dashboards.

## When to use

When you have a quantified peak table (LC-MS feature intensities) with sample metadata assigning samples to discrete groups (e.g., phenotype categories, treatment conditions), and you want to identify features that show consistent intensity changes between specified groups—for example, to prioritize antibiotic-active compounds by comparing metabolite abundance in high-activity vs. low-activity bacterial strains.

## When NOT to use

- Input is already a pre-filtered feature table and you need to apply a secondary filter—consider reapplying fold-change calculation to the original unfiltered peak table to avoid compounding selection biases.
- Sample sizes are extremely small (< 3 replicates per group)—fold-change estimates lack statistical power and may not be reliable without appropriate multiple-testing correction.
- You need statistical significance testing (p-value, q-value)—fold-change calculation alone does not provide uncertainty estimates; pair it with differential abundance tests (e.g., t-test, limma) for rigorous inference.

## Inputs

- Peak table (CSV format with feature IDs as rows, sample intensities as columns)
- Sample metadata table (assigning each sample to a group/phenotype category)
- Fold-change bounds (minimum and maximum threshold values)
- Group specification (list of group names to include or exclude)

## Outputs

- Filtered feature table (subset of input, retaining only features meeting fold-change and group criteria)
- Feature list with associated fold-change values and group assignments
- Test validation report (row counts, threshold confirmations, group logic verification)

## How to apply

Define the fold-change filter interface to accept minimum and maximum fold-change bounds (numeric range), a list of groups to include or exclude from comparison, and the feature intensity table. Implement fold-change calculation logic that compares mean or median feature intensities across the specified groups (typically as log2(group_A / group_B) or similar ratio). Apply the filter to the feature table, retaining only features whose fold-change falls within the user-specified range and whose group membership matches the inclusion/exclusion criteria. Use pytest to validate correctness: verify that the output row count matches the expected filtered set, confirm all retained features meet the fold-change threshold, and check that group inclusion/exclusion logic is correctly applied.

## Related tools

- **pytest** (Validation of filter correctness: verify output row count, check retained features meet fold-change threshold, confirm group inclusion/exclusion logic) — https://docs.pytest.org
- **fermo_core** (Core metabolomics data analysis library that implements fold-change calculation and feature filtering for FERMO dashboard) — https://github.com/fermo-metabolomics/fermo_core

## Evaluation signals

- Output feature count is equal to the number of features in the input table whose fold-change value falls within [min_threshold, max_threshold]
- All features in the filtered output have been assigned to groups matching the inclusion/exclusion specification
- Spot-check: manually calculate fold-change for 3–5 retained features and verify calculations match filter output
- Pytest assertions pass: `assert len(filtered_table) == expected_count`, `assert all(min_fc <= row['fold_change'] <= max_fc for row in filtered_table)`, and `assert all(row['group'] in included_groups for row in filtered_table)`
- No features are retained that do not meet both the fold-change range AND group criteria (AND logic, not OR)

## Limitations

- Fold-change calculation is sensitive to zero or near-zero intensities; implementation must handle log-scale transformation and pseudocount addition carefully to avoid division by zero or infinite values.
- Group-level fold-change (e.g., mean intensity ratio) masks within-group heterogeneity; features with high variance within a group may pass the filter despite inconsistent direction of change across replicates.
- No multiple-testing correction is applied; users should be aware that selecting features by fold-change alone inflates false-discovery rate and should be combined with statistical testing for high-confidence results.

## Evidence

- [other] Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list).: "Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list)."
- [other] Implement the fold-change calculation logic comparing feature intensities across specified groups.: "Implement the fold-change calculation logic comparing feature intensities across specified groups."
- [other] Apply the filter to a test feature table, retaining only features within the specified fold-change range and group criteria.: "Apply the filter to a test feature table, retaining only features within the specified fold-change range and group criteria."
- [other] Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied.: "Use pytest to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group"
- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
