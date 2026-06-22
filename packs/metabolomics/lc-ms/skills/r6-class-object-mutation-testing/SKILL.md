---
name: r6-class-object-mutation-testing
description: Use when when applying a series of mpactr filter functions (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) with copy_object=FALSE to confirm that the original peak table object is mutated as intended, not silently copied.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mpactr
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# r6-class-object-mutation-testing

## Summary

Verify that R6 class methods using reference semantics (copy_object=FALSE) correctly mutate the original data object in-place rather than operating on independent copies. This skill ensures that memory-efficient filtering workflows preserve expected object state changes across chained operations.

## When to use

When applying a series of mpactr filter functions (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) with copy_object=FALSE to confirm that the original peak table object is mutated as intended, not silently copied. This is especially critical when chaining filters to ensure row counts and feature membership change predictably and memory is not wasted on unintended deep copies.

## When NOT to use

- When copy_object=TRUE is explicitly set, as the filter is designed to return an independent copy and the original should NOT be modified.
- When the goal is to preserve the original unfiltered peak table for comparison; use copy_object=TRUE instead.
- When testing deep-copy semantics or isolation between independent filter runs.

## Inputs

- R6 data object (e.g., from import_data with Progenesis format)
- peak_table and metadata fields within the R6 object
- filter function with copy_object parameter

## Outputs

- mutated original R6 object with reduced peak table row count
- confirmation that original and returned object reference the same filtered state

## How to apply

Before filtering, record the row count from get_peak_table() on the original data object. Apply the filter function with copy_object=FALSE (e.g., filter_mispicked_ions with ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum'). After filtering, re-extract the row count from the same original object and verify it matches the row count of the returned filtered object. If both row counts are identical and reduced from the pre-filter state, the in-place mutation occurred as expected. If the original object's peak table remains unchanged, the copy_object=FALSE parameter failed to produce reference semantics.

## Related tools

- **mpactr** (Provides R6-based filter functions and get_peak_table() accessor for in-place mutation verification) — https://github.com/mums2/mpactr
- **R** (Runtime environment for executing R6 class methods and row count assertions)

## Examples

```
# Test in-place mutation with copy_object=FALSE
data2 <- import_data(example_path('cultures_peak_table.csv'), example_path('cultures_metadata.csv'), format='Progenesis')
row_count_before <- nrow(get_peak_table(data2))
data2_filtered <- filter_mispicked_ions(data2, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE)
row_count_after <- nrow(get_peak_table(data2))
stopifnot(row_count_after == nrow(get_peak_table(data2_filtered)) && row_count_after < row_count_before)
```

## Evaluation signals

- Row count of get_peak_table(data2) after filtering equals row count of get_peak_table(data2_mispicked), confirming both reference the same mutated object.
- Row count of original object decreases monotonically with each chained filter application, indicating persistent in-place state changes.
- Memory profiling shows no spike in RAM usage indicative of a deep copy operation during copy_object=FALSE filtering.
- Assigning the filter result back to the same variable (e.g., data2_mispicked <- filter_mispicked_ions(..., copy_object=FALSE)) yields identical peak table row counts in both data2 and data2_mispicked.
- Subsequent filters applied to the original object operate on the reduced feature set, not the pre-filtered feature set.

## Limitations

- Reference semantics rely on R's internal object aliasing; behavior may be fragile across package versions or if R6 class implementation changes.
- Peak table row count alone does not verify that the correct rows were retained; cross-check against expected feature identities (m/z, retention time, sample presence) to confirm filter correctness.
- In-place mutation means no undo is possible without re-importing or retaining a deep copy beforehand; users must plan the filter chain carefully.
- copy_object=FALSE performance advantage only materializes when chaining many filters; single-filter operations may not show measurable memory savings.

## Evidence

- [abstract] reference_semantics_recommendation: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [other] in_place_mutation_observed: "Running filter_mispicked_ions with copy_object=FALSE reduces the original data2 object's peak table from the initial row count to a smaller row count, demonstrating in-place mutation rather than"
- [other] test_methodology: "Verify that get_peak_table(data2) row count matches get_peak_table(data2_mispicked) row count, confirming in-place mutation of the original object."
- [abstract] filter_function_parameters: "filter_mispicked_ions(data2, ringwin = 0.5, isowin = 0.01, trwin = 0.005, max_iso_shift = 3, merge_peaks = TRUE, merge_method = "sum", copy_object = FALSE)"
