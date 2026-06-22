---
name: group-specification-and-subsetting
description: Use when when implementing a fold-change filter or similar feature-level metric that requires comparison across sample groups, and the analysis goal requires including or excluding specific groups (e.g., comparing only treated vs. control samples, or excluding low-quality replicates).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
---

# group-specification-and-subsetting

## Summary

Define and apply inclusion/exclusion criteria on sample groups to subset metabolomics feature tables during filtering operations. This skill enables comparative analysis by restricting fold-change calculations and other feature metrics to specified group combinations.

## When to use

When implementing a fold-change filter or similar feature-level metric that requires comparison across sample groups, and the analysis goal requires including or excluding specific groups (e.g., comparing only treated vs. control samples, or excluding low-quality replicates). Use this skill whenever group metadata must constrain which sample comparisons contribute to the filtered feature set.

## When NOT to use

- Input feature table is already filtered or subsetted to a single group (group specification would be redundant).
- No group metadata is available or sample-to-group mapping is incomplete or ambiguous.
- Analysis goal does not require group-relative metrics (e.g., absolute abundance thresholds where group identity is irrelevant).

## Inputs

- Feature intensity table (rows=features, columns=samples with quantitative values)
- Sample metadata mapping (sample IDs to group assignments)
- Group specification object (include list, exclude list)

## Outputs

- Subsetted feature table (features meeting fold-change + group criteria)
- Boolean mask or index set identifying which features passed filtering

## How to apply

First, define a group specification interface that accepts both a list of groups to include and optionally a list of groups to exclude. Pass this specification alongside the fold-change bounds (minimum and maximum) to the filter implementation. During fold-change calculation, restrict feature intensity comparisons to only the samples belonging to the included groups, and verify that excluded groups contribute no data to the metric. Apply the resulting filtered feature table to retain only features that simultaneously satisfy the fold-change threshold AND the group membership criteria. Validate by checking that the output feature table contains only features meeting both conditions, and that all retained rows involve only samples from the specified group set.

## Related tools

- **pytest** (Unit testing framework to validate filter correctness: verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied.)
- **fermo_core** (Core metabolomics data processing library that FERMO uses to perform data analysis and implement filtering logic) — https://github.com/fermo-metabolomics/fermo_core

## Evaluation signals

- Output feature table row count exactly matches the count of features in the input that satisfy both fold-change bounds AND group membership criteria (no false positives or negatives).
- All features retained in the output meet the specified fold-change threshold (verify by recalculating fold-change on output subset).
- All intensity comparisons used in fold-change calculation involve only samples from the include list (samples in exclude list are present in input metadata but absent from calculations).
- pytest assertions confirm: (a) excluded group samples do not appear in feature intensity comparisons, (b) included group samples are fully represented, (c) group specification is correctly serialized and applied consistently across multiple filter calls.
- Comparison of output vs. expected filtered set (e.g., manual or ground-truth subset) shows exact agreement in feature IDs and group assignments.

## Limitations

- Group specification logic depends on sample metadata quality; incomplete or misaligned sample-to-group mappings will produce incorrect subsetting.
- If a feature has missing or zero intensity values in all samples of a specified group, fold-change cannot be calculated for that feature even if it appears in other groups; the filtering behavior (retain vs. discard) must be explicitly defined.
- The skill does not handle hierarchical or overlapping group structures (e.g., nested experimental designs or samples belonging to multiple groups simultaneously); specification is assumed to be flat and mutually exclusive.

## Evidence

- [other] Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list).: "Define the filter interface to accept minimum and maximum fold-change bounds and a group specification (include/exclude list)."
- [other] Apply the fold-change filter to a test feature table, retaining only features within the specified fold-change range and group criteria.: "Apply the filter to a test feature table, retaining only features within the specified fold-change range and group criteria."
- [other] Verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied.: "verify output row count matches expected filtered set, check that all retained features meet the fold-change threshold, and confirm group inclusion/exclusion logic is correctly applied."
- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
