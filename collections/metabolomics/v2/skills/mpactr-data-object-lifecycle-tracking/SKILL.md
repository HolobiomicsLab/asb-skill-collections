---
name: mpactr-data-object-lifecycle-tracking
description: Use when when chaining multiple mpactr filters on a peak table and you
  need to decide whether to preserve intermediate filtered objects or accept in-place
  mutation for memory efficiency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - mpactr
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
- The goal of mpactr is to correct for errors that occur during the pre-processing
  of raw tandem MS/MS data.
- Next, we need to extract the ion status with `mpactr` function `qc_summary()`.
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

# mpactr-data-object-lifecycle-tracking

## Summary

Track whether mpactr filter operations mutate the original data object in-place or return independent copies by inspecting the copy_object parameter and verifying row count changes in the peak table. This skill is essential for understanding memory efficiency, chaining filters, and avoiding unintended data loss in metabolomics preprocessing workflows.

## When to use

When chaining multiple mpactr filters on a peak table and you need to decide whether to preserve intermediate filtered objects or accept in-place mutation for memory efficiency. Specifically: (1) if your workflow requires independent snapshots of data at each filtering stage, you must use copy_object=TRUE; (2) if you want to minimize memory overhead while applying sequential filters (mispicked, group, CV, insource), use copy_object=FALSE with the understanding that the original object will be mutated.

## When NOT to use

- If you are working with a single filter operation and do not care about memory efficiency; the lifecycle choice becomes irrelevant.
- If your downstream analysis requires statistical comparison of pre- vs. post-filter peak abundances without explicit manual bookkeeping; in this case, always use copy_object=TRUE to preserve the pre-filter object.
- If you have already imported data in a non-Progenesis format or as a pre-built feature table; lifecycle tracking is specific to mpactr's data object abstraction.

## Inputs

- mpactr data object (imported via import_data with Progenesis format)
- peak table (accessible via get_peak_table())
- metadata table (required for group-based filtering)

## Outputs

- mutated or copied mpactr data object with updated peak table
- integer row count of peak table (before and after filtering)
- boolean confirmation of in-place mutation vs. independent copy

## How to apply

Before calling a filter function like filter_mispicked_ions, decide on your lifecycle strategy: if you need the pre-filter object preserved, either set copy_object=TRUE or assign the filtered result to a new variable. If using copy_object=FALSE (the default), understand that calling filter_mispicked_ions with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum' will mutate the input object in-place, reducing its peak table row count by removing mispicked ions and merging isotopic patterns. Verify the mutation occurred by comparing get_peak_table(data_object) before and after the call; if row counts match between the input and output, the original was modified in-place. For memory-constrained workflows with large peak tables, use copy_object=FALSE and chain filters sequentially; for exploratory workflows, use copy_object=TRUE to preserve intermediate states for comparison.

## Related tools

- **mpactr** (R package providing filter functions (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) with copy_object parameter to control data object lifecycle; import_data and get_peak_table are used to instantiate and inspect objects respectively) — https://github.com/mums2/mpactr
- **R** (Programming language and runtime for executing mpactr workflows, tracking object identity, and comparing row counts via data.table and base functions)

## Examples

```
data2 <- import_data('cultures_peak_table.csv', 'cultures_metadata.csv', format='Progenesis'); rows_before <- nrow(get_peak_table(data2)); data2_filtered <- filter_mispicked_ions(data2, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); rows_after <- nrow(get_peak_table(data2)); identical(rows_after, nrow(get_peak_table(data2_filtered)))
```

## Evaluation signals

- Peak table row count from get_peak_table(data_object) after filtering is strictly less than the pre-filter row count (confirming mispicked ions were removed and isotopic patterns were merged).
- When copy_object=FALSE, get_peak_table(original_object) row count equals get_peak_table(filtered_result) row count, confirming in-place mutation of the original.
- When copy_object=TRUE, get_peak_table(original_object) row count remains unchanged from pre-filter state, confirming the original was preserved and only the returned object was modified.
- Sequential chaining of filters with copy_object=FALSE produces cumulative row count reduction consistent with the union of filtering effects (mispicked removal + group removal + CV threshold + insource removal).
- Memory profiling or object size inspection via object.size() in R shows smaller total memory footprint when copy_object=FALSE is used on large peak tables.

## Limitations

- The copy_object parameter only controls deep vs. shallow copying at the R object level; it does not affect the underlying data.table structure's internal reference semantics, so users must rely on explicit row count comparisons rather than language-level object identity checks.
- In-place mutation with copy_object=FALSE is irreversible within a single R session; if the filter produces unexpected results, the pre-filter data cannot be recovered without re-importing.
- The speed and memory efficiency gains from copy_object=FALSE are most pronounced for large peak tables (e.g., tens of thousands of features); for small datasets (<1000 features), the overhead difference is negligible.
- Lifecycle tracking requires manual bookkeeping of variable names and pre/post row counts; there is no built-in audit trail or versioning system within mpactr to track which filters were applied and in what order.

## Evidence

- [abstract] in-place mutation confirmation: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [methods] research question and finding on reference semantics: "Running filter_mispicked_ions with copy_object=FALSE reduces the original data2 object's peak table from the initial row count to a smaller row count, demonstrating in-place mutation rather than"
- [methods] filter_mispicked_ions parameters and behavior: "Call filter_mispicked_ions on data2 with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', and copy_object=FALSE"
- [methods] verification workflow for lifecycle tracking: "Verify that get_peak_table(data2) row count matches get_peak_table(data2_mispicked) row count, confirming in-place mutation of the original object"
- [readme] filter independence in mpactr design: "All filters are independent, meaning they can be used to create a project-specific workflow"
