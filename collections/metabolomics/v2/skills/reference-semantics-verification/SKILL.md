---
name: reference-semantics-verification
description: Use when when applying sequential filters to a large metabolomics peak table (e.g., mispicked ions, group, CV, or in-source filters) and you need to confirm that setting copy_object=FALSE actually modifies the input object in-place rather than creating a hidden copy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mpactr
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

# reference-semantics-verification

## Summary

Verify that a data filtering function respects reference semantics (copy_object=FALSE) by confirming that the original data object is mutated in-place rather than independently copied. This skill ensures memory-efficient chaining of filters on metabolomics peak tables.

## When to use

When applying sequential filters to a large metabolomics peak table (e.g., mispicked ions, group, CV, or in-source filters) and you need to confirm that setting copy_object=FALSE actually modifies the input object in-place rather than creating a hidden copy. Use this skill after calling a filter function with copy_object=FALSE to validate that memory and performance gains are real, especially when chaining multiple filters on datasets with thousands of features.

## When NOT to use

- When copy_object=TRUE is explicitly set — the function is designed to create an independent copy, so verifying reference semantics is not applicable.
- When the filter function is called for the first time without prior knowledge of its semantics — establish baseline semantics documentation first rather than relying on verification for every call.
- When dealing with small peak tables (< 100 rows) where memory efficiency gains are negligible and verification overhead is not justified.

## Inputs

- metabolomics data object (mpactr object with peak table)
- filter function call with copy_object=FALSE parameter

## Outputs

- confirmation of in-place mutation (boolean: row counts match)
- documentation of peak table row count before and after filtering

## How to apply

Before calling the filter function, extract and record the peak table row count from the input data object using get_peak_table(). Call the filter function (e.g., filter_mispicked_ions) with copy_object=FALSE, storing the result in a new variable. Extract and record the peak table row count from the original input object again. Compare the row counts: if the original object's row count has decreased to match the filtered result's row count, the function is using reference semantics and mutating the original object in-place. If the original object's row count remains unchanged, the function is creating an independent copy despite copy_object=FALSE, indicating either a parameter misinterpretation or a bug. This verification is critical before committing to reference-semantic workflows in production pipelines.

## Related tools

- **mpactr** (provides filter functions with copy_object parameter and get_peak_table accessor for verification) — https://github.com/mums2/mpactr
- **R** (language environment for executing filter calls and row count comparisons)

## Examples

```
# Extract initial row count
initial_rows <- nrow(get_peak_table(data2))
# Call filter with copy_object=FALSE
data2_filtered <- filter_mispicked_ions(data2, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE)
# Verify in-place mutation: original object row count should match filtered result
final_rows <- nrow(get_peak_table(data2))
if (nrow(get_peak_table(data2_filtered)) == final_rows & final_rows < initial_rows) { print('Reference semantics confirmed') }
```

## Evaluation signals

- Peak table row count of the original input object decreases after filtering, matching the row count of the filtered result object
- get_peak_table(original_object) and get_peak_table(filtered_result) return identical row counts, confirming they reference the same underlying data
- Repeated calls to get_peak_table on the original object after filtering return consistent (mutated) row counts, ruling out transient state changes
- Memory profiling shows no spike in memory consumption during filtering (compared to deep copy scenario), validating the reference-semantic claim
- Assignment of filter result to a new variable does not prevent mutations to the original object, confirming aliasing rather than copying

## Limitations

- Row count comparison alone cannot detect selective column mutations; verify schema integrity separately if filter modifies peak table structure beyond row removal.
- This verification method assumes get_peak_table() is deterministic and reflects the true state of the underlying object; if the accessor itself creates copies or caches data, verification may be misleading.
- Reference semantics behavior may vary across filter functions (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions); verification must be performed independently for each filter type.
- Timing and memory profiling are environment-dependent (R garbage collection, OS memory management); verification via row count is more reliable than performance metrics alone.

## Evidence

- [methods] in-place mutation confirmation via row count change: "Verify that get_peak_table(data2) row count matches get_peak_table(data2_mispicked) row count, confirming in-place mutation of the original object"
- [abstract] reference-semantics rationale for memory efficiency: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [abstract] filter_mispicked_ions with copy_object=FALSE parameter: "filter_mispicked_ions(data2, ringwin = 0.5, isowin = 0.01, trwin = 0.005, max_iso_shift = 3, merge_peaks = TRUE, merge_method = "sum", copy_object = FALSE)"
- [methods] demonstration of peak table row count reduction: "Running filter_mispicked_ions with copy_object=FALSE reduces the original data2 object's peak table from the initial row count to a smaller row count"
