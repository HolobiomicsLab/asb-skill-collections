---
name: peak-table-row-count-comparison
description: Use when you need to validate the reference-semantics behavior of mpactr filter functions, particularly when using copy_object=FALSE. Use it to confirm that a filtering operation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-row-count-comparison

## Summary

Compare peak table row counts before and after applying a filtering operation to verify whether the filter modifies the original data object in-place (reference semantics) or produces an independent filtered copy. This skill surfaces memory efficiency and object mutation behavior in metabolomics preprocessing workflows.

## When to use

Apply this skill when you need to validate the reference-semantics behavior of mpactr filter functions, particularly when using copy_object=FALSE. Use it to confirm that a filtering operation (e.g., filter_mispicked_ions) has mutated the original data object rather than creating an independent copy, or to troubleshoot unexpected row count outcomes after chaining multiple filters together.

## When NOT to use

- When the input is already a deeply copied or serialized object where reference semantics are not applicable.
- When copy_object=TRUE is used; row count comparison alone cannot distinguish true copy behavior from in-place mutation in that case.
- When the filtering operation is expected to remove zero features; the comparison will not fail but will not meaningfully demonstrate reference semantics.

## Inputs

- peak_table (data frame or matrix with rows representing MS1 features)
- metadata (sample annotation table compatible with Progenesis format)
- data object (imported via mpactr::import_data())
- filter function parameters (ringwin, isowin, trwin, max_iso_shift, merge_peaks, merge_method, copy_object)

## Outputs

- row_count_before (integer: peak table row count prior to filtering)
- row_count_after (integer: peak table row count after filtering)
- reference_semantics_validated (boolean: TRUE if original object was mutated in-place)

## How to apply

Import a raw peak table and metadata using mpactr's import_data function in Progenesis format. Create a reference copy of the imported data object. Extract and record the row count from get_peak_table() before filtering. Call the target filter function (e.g., filter_mispicked_ions) with copy_object=FALSE, assigning the result to a new variable. Extract and record the row count from get_peak_table() on the original object after filtering. Compare the row counts: if the original object's row count has decreased and matches the filtered result's row count, in-place mutation has occurred (reference semantics); if the original object's row count remains unchanged, the filter created an independent copy despite copy_object=FALSE. This comparison confirms whether reference semantics are working as intended and validates memory-efficient filter chaining.

## Related tools

- **mpactr** (provides import_data(), filter_mispicked_ions(), get_peak_table() functions and implements reference-semantics filtering with copy_object parameter) — https://github.com/mums2/mpactr
- **R** (execution environment for mpactr package and row count extraction/comparison logic)

## Examples

```
data2 <- import_data(peak_table_file, metadata_file, format='Progenesis'); before <- nrow(get_peak_table(data2)); data2_mispicked <- filter_mispicked_ions(data2, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); after <- nrow(get_peak_table(data2)); identical(after, nrow(get_peak_table(data2_mispicked)))
```

## Evaluation signals

- Original object's get_peak_table() row count decreases after filtering with copy_object=FALSE, matching the filtered result's row count.
- Both get_peak_table(original_object) and get_peak_table(filtered_result) return identical row counts, confirming reference to the same mutated object.
- Row count difference (before − after) is positive and equals the number of features removed by the specific filter's criteria (e.g., mispicked ions, group overrepresentation).
- Row count remains unchanged in the original object when copy_object=TRUE, demonstrating that the copy_object parameter controls mutation behavior.
- Chaining multiple filters produces cumulative row count reductions that sum correctly when using copy_object=FALSE throughout the pipeline.

## Limitations

- Row count comparison detects mutation but does not verify which specific rows were removed or validate that removal criteria were correctly applied.
- If a filter removes zero features, row count comparison will appear to succeed even if the filter failed to execute or copy_object parameter was ignored.
- This skill only works within the R environment where mpactr's data objects maintain reference semantics; exported or serialized objects lose reference behavior.
- Comparison of row counts is insufficient to detect partial or corrupted mutations; additional validation of data integrity (e.g., column structure, values) is needed.

## Evidence

- [other] Running filter_mispicked_ions with copy_object=FALSE reduces the original data2 object's peak table from the initial row count to a smaller row count, demonstrating in-place mutation rather than independent filtering of a copied object.: "Running filter_mispicked_ions with copy_object=FALSE reduces the original data2 object's peak table from the initial row count to a smaller row count, demonstrating in-place mutation rather than"
- [other] Verify that get_peak_table(data2) row count matches get_peak_table(data2_mispicked) row count, confirming in-place mutation of the original object.: "Verify that get_peak_table(data2) row count matches get_peak_table(data2_mispicked) row count, confirming in-place mutation of the original object."
- [abstract] We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [other] Extract and record the row count from get_peak_table(data2) before filtering. Call filter_mispicked_ions on data2 with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', and copy_object=FALSE, assigning result to data2_mispicked. Extract and record the row count from get_peak_table(data2) after filtering.: "Extract and record the row count from get_peak_table(data2) before filtering. Call filter_mispicked_ions on data2 with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3,"
