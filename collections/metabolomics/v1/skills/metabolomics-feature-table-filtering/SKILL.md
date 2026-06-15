---
name: metabolomics-feature-table-filtering
description: Use when when you have a raw LC-MS peak table imported from vendor software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - data.table
  - mpactr
  - MPACT
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

# metabolomics-feature-table-filtering

## Summary

Apply a chain of independent filter operations to LC-MS peak tables to remove artifactual or low-quality features (mispicked ions, carryover contaminants, non-reproducible peaks, and in-source fragments) while preserving biologically meaningful metabolite signals. Each filter operates via reference semantics on R6 objects, enabling memory-efficient in-place updates to the peak abundance matrix and metadata.

## When to use

When you have a raw LC-MS peak table imported from vendor software (e.g., Progenesis, Waters, or other pre-processed formats) that contains systematic artifacts introduced during feature detection—such as isotopic patterns incorrectly split into separate peaks, contamination from solvent blanks or carryover between samples, inconsistent peak detection across technical replicates, or in-source fragments—and you need to construct a high-confidence feature set for downstream statistical analysis (fold-change, correlation, differential abundance testing).

## When NOT to use

- Input is already a curated feature table from a published study (re-filtering may remove genuine signals that were previously validated).
- Peak table originates from targeted MS/MS methods where all detected features are pre-selected compounds (filters designed for untargeted discovery may be overly aggressive).
- Sample cohort lacks technical replicates or clear negative control groups (filter_cv() and filter_group() require replicate structure and control samples to be effective).

## Inputs

- Raw LC-MS peak table (CSV or vendor format: Progenesis, Waters, MS-DIAL, etc.)
- Sample metadata table (CSV with group assignments and technical replicate indicators)
- Imported mpactr R6 object containing peak abundance matrix and sample annotations

## Outputs

- Filtered mpactr R6 object with reduced feature count and updated peak abundance matrix
- filter_summary() named lists (failed_ions, passed_ions) as data.tables for each filter step
- CSV or tabular export of final high-confidence feature table for downstream analysis

## How to apply

Load the raw peak table and sample metadata using mpactr::import_data(), then apply a sequence of independent filters in order of decreasing biological impact: (1) filter_mispicked_ions() with merge_peaks=TRUE and merge_method='sum' to recombine isotopically split peaks; (2) filter_group() to remove features overrepresented in negative control groups (e.g., group_to_remove='Solvent_Blank'); (3) filter_cv() with a cv_threshold (e.g., 0.2) to remove non-reproducible features across technical replicates; (4) filter_insource_ions() with cluster_threshold (e.g., 0.95) to remove in-source fragment ions. Use copy_object=FALSE (the default) to enable in-place modification via R6 reference semantics, which reduces memory overhead. After each filter, optionally call filter_summary() with the filter name (e.g., 'mispicked', 'group') to extract and inspect the named lists of failed_ions and passed_ions. The rationale is that each filter targets a distinct type of artifact that would confound metabolomics interpretation if left uncorrected.

## Related tools

- **mpactr** (R package providing filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions(), filter_summary(), and import_data() functions; implements R6 reference semantics for memory-efficient peak table filtering) — https://github.com/mums2/mpactr
- **data.table** (Data manipulation and tabular export; used to convert filter_summary() output lists into queryable data.tables for inspection and CSV export)
- **R** (Programming language and runtime environment for all filtering operations and result export)
- **MPACT** (Graphical desktop tool (Python/Anaconda-based) that provides alternative GUI-driven workflow for feature filtering and visualization, supporting multiple vendor formats (Bruker Metaboscape, MS-DIAL, GNPS)) — https://github.com/BalunasLab/mpact

## Examples

```
library(mpactr); data <- import_data(example_path('cultures_peak_table.csv')); data$filter_mispicked_ions(merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); data$filter_group(group_to_remove='Solvent_Blank', copy_object=FALSE); data$filter_cv(cv_threshold=0.2, copy_object=FALSE); summary_mispicked <- filter_summary(data, 'mispicked')
```

## Evaluation signals

- Peak table row count decreases monotonically after each filter step; verify via mpactr::get_peak_table() that both the original object and result object reflect the same post-filter row count when copy_object=FALSE, confirming in-place modification.
- filter_summary() for each filter returns a named list with non-empty failed_ions and passed_ions vectors; the union of passed_ions across all filters matches the final feature count.
- After filter_mispicked_ions() with merge_method='sum', abundance values for merged isotopic patterns equal the sum of the original split peak abundances across all samples.
- After filter_group(), features present in 100% of negative control samples are removed; verify via filter_summary('group') that all retained features have zero or near-zero abundance in control samples.
- After filter_cv(), standard deviation of log-transformed abundances across technical replicates is below cv_threshold for all retained features; visual inspection of cv distribution before/after confirms removal of high-variance features.

## Limitations

- Filters are independent and order-dependent: applying them in different sequences may yield different final feature sets, particularly if filter thresholds are near decision boundaries (e.g., cv_threshold near the true coefficient of variation of marginal features).
- filter_group() requires a priori specification of which group(s) to remove; misidentification of control groups or presence of only biological groups without true negative controls will cause false negatives.
- filter_cv() assumes technical replicates are truly technical (same sample, independent preparation); if replicates include biological variation (e.g., biological pseudo-replicates), the filter may remove genuine features with real biological variance.
- No automated parameter selection or sensitivity analysis is provided; users must manually set merge_method, cv_threshold, and cluster_threshold based on prior knowledge or exploratory analysis.

## Evidence

- [readme] removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
- [readme] removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover: "filter_group(): removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover between samples."
- [readme] removal of non-reproducible features, or those that are inconsistent between technical replicates: "filter_cv(): removal of non-reproducible features, or those that are inconsistent between technical replicates."
- [readme] removal of fragment ions created during the first ionization in the tandem MS/MS workflow: "filter_insource_ions(): removal of fragment ions created during the first ionization in the tandem MS/MS workflow."
- [abstract] operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [other] filter_summary() returns a named list containing two components: failed_ions and passed_ions: "filter_summary() returns a named list containing two components: failed_ions and passed_ions, both of which can be displayed as data tables using head()"
- [readme] All filters are independent, meaning they can be used to create a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow, or you can learn more in [the Getting Started page]"
- [methods] filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"): "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"
