---
name: object-state-mutation-detection
description: Use when when calling filter functions (e.g., filter_mispicked_ions(), filter_group(), filter_cv()) on R6-based metabolomics data objects in the mpactr package and you need to verify whether the original object's state is preserved.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0220
  tools:
  - R
  - mpactr
  - data.table
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# object-state-mutation-detection

## Summary

A technique to determine whether function calls operating on R6 reference objects modify the original data in-place or create independent deep copies. This is critical for metabolomics workflows where unintended mutation of peak tables can silently corrupt downstream analyses.

## When to use

When calling filter functions (e.g., filter_mispicked_ions(), filter_group(), filter_cv()) on R6-based metabolomics data objects in the mpactr package and you need to verify whether the original object's state is preserved. Specifically, apply this skill when: (1) a function accepts a copy_object parameter or similar semantics flag, (2) you assign the result to a new variable but suspect the original may also be modified, or (3) you need to establish baseline row counts before and after filtering to detect in-place mutations.

## When NOT to use

- When working with immutable data structures (e.g., base R data.frames with copy-by-value semantics) where mutation is not possible by design.
- When filter functions do not expose a copy_object or equivalent parameter; the skill requires explicit control over copy semantics.
- When the original data object is not needed for downstream analysis and in-place mutation is intentional and acceptable.

## Inputs

- R6 metabolomics data object (e.g., from import_data() with format='Progenesis')
- Peak table (CSV format, e.g., cultures_peak_table.csv)
- Metadata table (CSV format, e.g., cultures_metadata.csv)
- Function call with copy_object parameter (boolean)

## Outputs

- Comparison table with columns: copy_object setting, original_object_rowcount, assigned_object_rowcount, object_identity_match (boolean)
- Validated mutation behavior (in-place vs. deep-copy confirmation)

## How to apply

Load the same data object twice (or make explicit copies before and after each operation). Call the filter function on the first copy with copy_object=FALSE; record the row count of both the original and assigned objects. Reload or re-copy the data and call the same filter function with copy_object=TRUE; again record row counts for both objects. Construct a comparison table with columns: copy_object setting, original_object_rowcount, assigned_object_rowcount, and object_identity_match (TRUE if row counts diverge in-place, FALSE if they remain equal and independent). The rationale is that R6 reference semantics by default mutate objects in-place unless explicit deep-copy parameters are set; comparing row counts before/after and checking whether the original object was modified reveals the actual mutation behavior, which is essential for ensuring data integrity in automated metabolomics pipelines.

## Related tools

- **mpactr** (R6-based filtering library providing filter_mispicked_ions(), filter_group(), filter_cv(), and filter_insource_ions() with copy_object parameter control) — https://github.com/mums2/mpactr
- **R** (Runtime environment for loading data, calling filter functions, recording object state, and constructing comparison tables)
- **data.table** (Data structure for efficient row count comparison and construction of mutation detection results table)

## Examples

```
data <- import_data(example_path('cultures_peak_table.csv'), example_path('cultures_metadata.csv'), format='Progenesis'); data_filtered <- filter_mispicked_ions(data, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); cat('Original rows:', nrow(data), 'Assigned rows:', nrow(data_filtered), '\n')
```

## Evaluation signals

- Original object row count remains unchanged (copy_object=TRUE) or matches assigned object row count (copy_object=FALSE), confirming behavior matches parameter intent.
- Assigned object row count equals expected filtered result (e.g., 7269 → 6625 for mispicked ion removal) in both copy_object=TRUE and FALSE cases.
- object_identity_match column is FALSE when copy_object=TRUE (independent objects with potentially different row counts) and TRUE when copy_object=FALSE (original and assigned point to same mutated state).
- Row count divergence between original_object_rowcount and assigned_object_rowcount occurs only when copy_object=FALSE, never when copy_object=TRUE.
- Workflow is reproducible: reloading data and re-running with opposite copy_object settings yields consistent, inverse mutation patterns.

## Limitations

- This detection method requires explicit parameter control; not all filter functions may expose copy_object or similar flags, limiting applicability.
- In-place mutation detection is sensitive to R6 object implementation details; changes to the underlying class structure could alter mutation behavior unpredictably.
- Row count comparison alone does not detect mutations in non-row-count properties (e.g., annotation columns, metadata attributes); more granular object introspection may be needed for complete state validation.
- Reference semantics in R6 classes mean that shared references to the same object will all reflect mutations, potentially obscuring the source of unexpected data changes in complex workflows.

## Evidence

- [other] When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place; the raw data object with 7269 ions was reduced to 6625 ions, and the original data2 object was also updated despite assigning the result to a new variable data2_mispicked.: "When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place; the raw data object with 7269 ions was reduced to 6625 ions, and the original data2 object"
- [abstract] operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [other] Construct a comparison table with columns: copy_object setting, original_object_rowcount, assigned_object_rowcount, and object_identity_match (TRUE if both point to same data, FALSE if independent).: "Construct a comparison table with columns: copy_object setting, original_object_rowcount, assigned_object_rowcount, and object_identity_match (TRUE if both point to same data, FALSE if independent)."
- [other] Call filter_mispicked_ions() with merge_peaks=TRUE, merge_method='sum', and copy_object=FALSE on the first copy; record row count of original and assigned objects.: "Call filter_mispicked_ions() with merge_peaks=TRUE, merge_method='sum', and copy_object=FALSE on the first copy; record row count of original and assigned objects."
- [other] Validate that copy_object=FALSE shows matching row counts (in-place mutation) and copy_object=TRUE shows independent row counts (deep copy).: "Validate that copy_object=FALSE shows matching row counts (in-place mutation) and copy_object=TRUE shows independent row counts (deep copy)."
