---
name: mispicked-ion-detection-and-merging
description: Use when immediately after importing raw LC-MS peak tables (e.g., Progenesis format) and before applying group or replicability filters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
---

# mispicked-ion-detection-and-merging

## Summary

Identify and merge isotopic patterns that were incorrectly split during MS1 peak picking, consolidating mispicked ions back into single high-quality features. This step corrects a systematic preprocessing error that inflates feature counts and reduces reproducibility in metabolomics datasets.

## When to use

Apply this skill immediately after importing raw LC-MS peak tables (e.g., Progenesis format) and before applying group or replicability filters. Use it when you suspect preprocessing artifacts have split authentic isotopic patterns into multiple detected features, resulting in artificially high feature counts or redundant m/z signals close in retention time.

## When NOT to use

- Input is already a fully curated feature table with manual verification of isotopic patterns
- Metabolomics data does not come from Progenesis or equivalent peak-picking software known to split isotopic patterns
- Analysis goal is to preserve all detected m/z signals for spectral matching against reference databases without preprocessing

## Inputs

- mpactr object (R6 class) imported from Progenesis peak table (.csv) and metadata (.csv)

## Outputs

- filtered mpactr object with mispicked isotopic patterns merged into single features
- reduced ion count (e.g., 1407 → 644 in task_004 example)

## How to apply

Call filter_mispicked_ions() on the imported mpactr object with merge_peaks=TRUE and merge_method='sum' to detect and merge isotopic pattern splitting artifacts. The function operates on reference semantics (in-place modification by default), so the original object is updated unless copy_object=TRUE is explicitly set. Peaks identified as part of the same mispicked isotopic cluster are consolidated into a single feature whose peak intensity is the sum of all merged components. This merging step should be the first filter applied in the workflow to avoid propagating artificial feature splits downstream into group and replicability filtering steps.

## Related tools

- **mpactr** (R6-based package providing filter_mispicked_ions() function with in-place reference semantics and configurable merge methods) — https://github.com/mums2/mpactr
- **data.table** (Underlying data structure for peak intensity summation and feature merging operations)
- **R** (Execution environment for mpactr and filter_mispicked_ions() invocation)

## Examples

```
data2_mispicked <- filter_mispicked_ions(data2, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE)
```

## Evaluation signals

- Row count of peak table decreases after filtering (e.g., 1407 → 644 ions); both original and result-assigned objects reflect same post-filter count when copy_object=FALSE, confirming in-place modification
- qc_summary() data.table shows no ions marked as 'failed' by the mispicked filter in subsequent fully-filtered workflow output
- Merged feature intensities equal the sum of component peaks before merging (verify via intermediate peak table snapshots)
- Retention time and m/z coordinates of merged feature fall within expected isotopic pattern tolerance (e.g., ±2 s in RT, ±5 ppm in m/z)
- Downstream group and replicability filter outcomes are reproducible and show reduced feature redundancy compared to unmerged workflows

## Limitations

- merge_method='sum' assumes additive peak intensities; alternative merge methods may be needed for non-linear detector responses or when absolute peak heights (not areas) are primary feature intensity metric
- Filter efficacy depends on Progenesis preprocessing parameters; datasets from other peak pickers (MS-DIAL, xcms) may exhibit different isotopic splitting patterns requiring parameter retuning or alternative approaches
- No published cluster_threshold or isotopic pattern tolerance parameters are documented in the article; default behavior not explicitly stated, requiring empirical validation on user datasets
- In-place modification by default (copy_object=FALSE) means original object cannot be recovered if merging produces unexpected results; use copy_object=TRUE for exploratory runs

## Evidence

- [readme] removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing: "removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing"
- [methods] filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"): "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"
- [abstract] operates on reference semantics in which data is updated *in-place*: "operates on reference semantics in which data is updated *in-place*"
- [other] after assigning the filtered result to data2_mispicked with copy_object=FALSE, both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification: "both data2_mispicked and the original data2 contain 644 ions, confirming in-place modification"
- [other] Apply filter_mispicked_ions() with merge_peaks=TRUE and merge_method='sum' to identify and merge isotopic pattern splitting artifacts.: "Apply filter_mispicked_ions() with merge_peaks=TRUE and merge_method='sum' to identify and merge isotopic pattern splitting artifacts"
