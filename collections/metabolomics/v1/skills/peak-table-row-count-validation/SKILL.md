---
name: peak-table-row-count-validation
description: Use when when using mpactr filter functions (e.g., filter_mispicked_ions, filter_group, filter_cv) with R6 reference semantics and uncertain whether the copy_object parameter controls deep copying or in-place modification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - data.table
  - mpactr
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- library(data.table)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
---

# peak-table-row-count-validation

## Summary

Validates that filtering operations on LC-MS peak tables have correctly modified the original data object by comparing row counts before and after filtering. This skill is essential for detecting unintended in-place modifications or shallow-copy behavior in R6-based metabolomics data structures.

## When to use

When using mpactr filter functions (e.g., filter_mispicked_ions, filter_group, filter_cv) with R6 reference semantics and uncertain whether the copy_object parameter controls deep copying or in-place modification. Apply this skill to confirm that the original data object and assigned result object reflect the expected post-filter state, especially when reproducibility or memory efficiency depends on understanding reference vs. copy semantics.

## When NOT to use

- Input is a non-R6 data frame or matrix — this skill relies on reference semantics behavior specific to R6 classes.
- Peak table has already been exported to CSV or other external format — row counts on disk cannot detect in-memory reference modifications.
- Filtering operation is applied with copy_object=TRUE explicitly set — in that case, deep copy is guaranteed and row count validation alone does not test the intended behavior.

## Inputs

- mpactr data object (R6 class) with imported LC-MS peak table and metadata
- filter function call result (filtered mpactr object assigned to a variable)
- original mpactr object reference

## Outputs

- before-filter row count (integer)
- after-filter row count from original object (integer)
- after-filter row count from assigned result object (integer)
- validation report (boolean: counts match or do not match)

## How to apply

After calling a filter function on an mpactr data object, extract the peak table row count from both the original object and the assigned result object using mpactr::get_peak_table(), then compare the counts. If copy_object=FALSE (the default), both objects should report identical row counts after filtering, indicating in-place modification rather than independent copies. If counts differ, the function created a deep copy despite the parameter setting. Document the before-filter and after-filter counts to establish the ground truth for filtering efficacy and to detect silent failures or unexpected shallow-copy behavior.

## Related tools

- **mpactr** (Provides R6-based filter functions and get_peak_table() method for extracting row counts and validating in-place modifications) — https://github.com/mums2/mpactr
- **R** (Execution environment for mpactr, reference semantics evaluation, and row count comparison)
- **data.table** (Underlying data structure for peak tables, supporting fast row count operations)

## Examples

```
data2 <- mpactr::import_data(example_path('cultures_peak_table.csv')); before_count <- nrow(mpactr::get_peak_table(data2)); data2_mispicked <- data2$filter_mispicked_ions(merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); after_count <- nrow(mpactr::get_peak_table(data2)); result_count <- nrow(mpactr::get_peak_table(data2_mispicked)); all.equal(after_count, result_count)
```

## Evaluation signals

- Original object and assigned result object both report identical post-filter row count, confirming in-place modification with copy_object=FALSE
- Before-filter row count minus after-filter row count equals the number of rows removed by the filter (e.g., 1407 − 644 = 763 ions filtered)
- Row count change is consistent with the merge_method parameter (e.g., 'sum' merges isotopic patterns into single rows, reducing total count)
- Calling get_peak_table() on both objects at the same point in time yields the same count, ruling out asynchronous or lazy evaluation artifacts
- If copy_object=TRUE is used, assigned result object row count matches but original object row count remains unchanged, demonstrating deep copy behavior

## Limitations

- Row count validation alone does not detect partial or selective in-place modifications (e.g., row reordering or column-level changes without row deletion).
- This skill does not account for downstream operations that may further modify the object; counts must be extracted immediately after filtering.
- If the mpactr package updates its copy semantics or adds new filter parameters, the before/after row count relationship may change; always consult the function documentation.
- Row counts provide no information about data quality or correctness of the filtering logic itself — a filter may reduce row count but select the wrong ions.

## Evidence

- [other] Running filter_mispicked_ions with copy_object=FALSE (the default setting) updates the original data object in place: data2 had 1407 ions before filtering, and after assigning the filtered result to data2_mispicked with copy_object=FALSE, both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification rather than creation of independent copies.: "Running filter_mispicked_ions with copy_object=FALSE (the default setting) updates the original data object in place: data2 had 1407 ions before filtering, and after assigning the filtered result to"
- [other] Extract peak table row counts from both data2 and data2_mispicked using mpactr::get_peak_table(). Verify that both objects report the same post-filter row count, demonstrating in-place modification of the original object rather than a deep copy.: "Extract peak table row counts from both data2 and data2_mispicked using mpactr::get_peak_table(). Verify that both objects report the same post-filter row count"
- [abstract] operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [readme] filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing.: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing"
