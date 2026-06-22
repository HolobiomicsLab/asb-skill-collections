---
name: r6-reference-semantics-comparison
description: Use when you need to understand or validate whether calling filter_mispicked_ions() (or similar R6 filter methods) with different copy_object settings will mutate your original data object in memory or preserve it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - mpactr
  - data.table
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00997-24
  all_source_dois:
  - 10.1128/mra.00997-24
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compare R6 Reference vs. Copy Semantics in Data Filtering

## Summary

This skill verifies whether R6-based filter functions in mpactr apply in-place modification (reference semantics with copy_object=FALSE) or create independent copies (deep copy with copy_object=TRUE) by comparing row counts and object identity between the original and assigned result objects. It is essential for understanding memory efficiency and data mutation side effects in metabolomics peak filtering workflows.

## When to use

Apply this skill when you need to understand or validate whether calling filter_mispicked_ions() (or similar R6 filter methods) with different copy_object settings will mutate your original data object in memory or preserve it. This is critical before running large-scale filtering on datasets like the cultures peak table (1407 ions initially) to avoid unintended in-place modifications or unnecessary memory duplication.

## When NOT to use

- You are not modifying the filtering parameters or workflow—use this skill only if you are varying the copy_object parameter itself.
- Your peak table is already filtered and you are analyzing downstream results (e.g., fold change, volcano plots)—this skill applies only to the filter function call itself.
- You do not have access to reload the same dataset twice or cannot compare two independent filtering runs—the comparison requires fresh imports for each setting.

## Inputs

- Raw LC-MS peak table in Progenesis CSV format (e.g., cultures_peak_table.csv)
- Sample metadata in CSV format (e.g., cultures_metadata.csv)
- Imported mpactr data object (R6 instance with peak table and metadata)

## Outputs

- Comparison table with rows for each copy_object setting, columns: copy_object, original_object_rowcount, assigned_object_rowcount, object_identity_match
- Validated evidence that copy_object=FALSE causes in-place mutation or copy_object=TRUE creates independent copies

## How to apply

Load the same raw LC-MS peak table twice using mpactr::import_data() with format='Progenesis'. On the first copy, call filter_mispicked_ions() with copy_object=FALSE and merge_peaks=TRUE, merge_method='sum'; record the row count of both the original object and the newly assigned result object using get_peak_table(). Reload the data and on the second copy, call filter_mispicked_ions() with identical filtering parameters but copy_object=TRUE; again record row counts. Construct a comparison table with columns: copy_object setting, original_object_rowcount, assigned_object_rowcount, and object_identity_match. If copy_object=FALSE, the original and assigned object should have matching post-filter row counts (indicating in-place mutation); if copy_object=TRUE, they should differ (indicating independent deep copies). This empirical comparison reveals whether the R6 object's reference semantics are actually triggered by the parameter.

## Related tools

- **mpactr** (Provides R6-based filter_mispicked_ions() function with copy_object parameter and get_peak_table() method for extracting row counts) — https://github.com/mums2/mpactr
- **R** (Language runtime for executing import_data(), filter_mispicked_ions(), and get_peak_table() calls; environment for object identity tracking)
- **data.table** (Underlying data structure for peak table representation and row count extraction)

## Examples

```
data2 <- import_data(example_path('cultures_peak_table.csv'), format='Progenesis'); data2_filtered_FALSE <- filter_mispicked_ions(data2, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); nrow1_orig <- nrow(get_peak_table(data2)); nrow1_result <- nrow(get_peak_table(data2_filtered_FALSE)); print(paste('copy_object=FALSE: original=', nrow1_orig, ', result=', nrow1_result, sep=''))
```

## Evaluation signals

- When copy_object=FALSE, original_object_rowcount equals assigned_object_rowcount post-filter (both reflect the filtered state), confirming in-place mutation.
- When copy_object=TRUE, original_object_rowcount remains at pre-filter state while assigned_object_rowcount equals post-filter state, confirming independent deep copy.
- Row count reduction is consistent with the filtering operation (e.g., 1407 → 644 ions for mispicked filter with merge_peaks=TRUE, merge_method='sum').
- No errors or warnings from mpactr::get_peak_table() when extracting counts from both original and assigned objects.
- The comparison table shows one row with copy_object=FALSE and a second row with copy_object=TRUE, demonstrating both settings were tested on identical input data.

## Limitations

- This skill requires reloading the same dataset twice, which may be impractical for very large LC-MS datasets or in resource-constrained environments.
- The comparison is specific to filter_mispicked_ions(); other mpactr filters (filter_group, filter_cv, filter_insource_ions) may exhibit different R6 reference semantics behavior and should be validated separately.
- Row count alone does not capture whether nested data structures (e.g., metadata, feature annotations) are also mutated in place; a full object identity check or deep inspection of all slots may be needed for comprehensive validation.
- The copy_object parameter is specific to mpactr R6 filters; this skill does not apply to traditional R functions or copy-by-value workflows.

## Evidence

- [other] When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place; the raw data object with 7269 ions was reduced to 6625 ions, and the original data2 object was also updated despite assigning the result to a new variable data2_mispicked.: "When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place"
- [other] Running filter_mispicked_ions with copy_object=FALSE (the default setting) updates the original data object in place: data2 had 1407 ions before filtering, and after assigning the filtered result to data2_mispicked with copy_object=FALSE, both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification rather than creation of independent copies.: "both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification"
- [abstract] operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,: "operates on reference semantics in which data is updated *in-place*"
- [abstract] Memory usage really shines when you use R6 classes vs. a traditional workflow, such as copy by: "Memory usage really shines when you use R6 classes vs. a traditional workflow"
- [methods] filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"): "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"
- [methods] import_data(example_path("cultures_peak_table.csv"): "import_data(example_path("cultures_peak_table.csv")"
