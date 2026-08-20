---
name: mpactr-filter-application
description: Use when you have a preprocessed peak table from tandem MS/MS data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - mpactr
  - MPACT
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
- library(mpactr)
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

# mpactr-filter-application

## Summary

Apply independent, chainable mpactr filters to MS1 peak tables to remove mispicked ions, group-specific contamination, non-reproducible features, and in-source fragments. This skill corrects preprocessing errors in tandem mass spectrometry data by selectively removing low-quality features while preserving the original biological signal.

## When to use

Use this skill when you have a preprocessed peak table from tandem MS/MS data (e.g., Progenesis CSV format) and need to remove systematic quality issues: isotopic patterns incorrectly split during peak picking, features present only in solvent/media blanks, features with coefficient of variation (CV) above a reproducibility threshold across technical replicates, or in-source fragment ions created during ionization. Apply filters in sequence based on which artifacts affect your dataset.

## When NOT to use

- Input is already a validated, curated feature table from a published metabolomics study (filters are redundant).
- You have only a single replicate per sample group; filter_cv() requires technical replicates to estimate reproducibility.
- You lack metadata assigning samples to groups or blank categories; filter_group() and filter_cv() require this information.

## Inputs

- peak_table (CSV format from Progenesis or MS-DIAL, with m/z, retention time, and abundance columns)
- metadata (CSV format with sample identifiers, group assignments, and technical replicate designations)
- filter parameters (merge_method, cv_threshold, group_to_remove, cluster_threshold)

## Outputs

- filtered_peak_table (reduced feature set with mispicked ions, blanks, low-CV, and in-source fragments removed)
- row_count_comparison (before/after counts per filter step for validation)

## How to apply

Load the peak table and metadata using import_data() with the appropriate format (e.g., format='Progenesis'). Apply filters independently and sequentially: filter_mispicked_ions() with merge_peaks=TRUE and merge_method='sum' to combine isotopic patterns; filter_group() to remove features overrepresented in blank/control samples (e.g., group_to_remove='Solvent_Blank'); filter_cv() with a CV threshold (e.g., cv_threshold=0.2) to remove features inconsistent across technical replicates; filter_insource_ions() with cluster_threshold (default 0.95) to remove fragment ions. Decide the copy_object parameter: set copy_object=TRUE to preserve the original data object in memory (deep copy), or copy_object=FALSE to update in-place and reduce memory usage when working with large datasets. Each filter returns a reduced feature table; record row counts before and after each step to track cumulative filtering effects.

## Related tools

- **mpactr** (R package providing independent filter functions (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) for correcting MS1 peak selection errors) — https://github.com/mums2/mpactr
- **MPACT** (GUI desktop application wrapping mpactr and related preprocessing, offering interactive peak table filtering and data visualization workflows) — https://github.com/BalunasLab/mpact
- **data.table** (R package used internally by mpactr for fast, memory-efficient tabular data manipulation during filtering operations)
- **R** (Runtime environment for executing mpactr filters and constructing custom filter chains)

## Examples

```
library(mpactr); data <- import_data('cultures_peak_table.csv', format='Progenesis'); data_filtered <- data$filter_mispicked_ions(merge_peaks=TRUE, merge_method='sum', copy_object=TRUE)$filter_group(group_to_remove='Solvent_Blank')$filter_cv(cv_threshold=0.2)
```

## Evaluation signals

- Row count decreases monotonically with each filter step; total reduction should match the sum of features removed by each filter (no double-counting).
- When copy_object=TRUE, the original data object row count remains unchanged after filtering; when copy_object=FALSE, the original is modified in-place, showing identical row counts to the assigned result.
- After filter_group(group_to_remove='Solvent_Blank'), the filtered table contains zero features unique to blank samples.
- After filter_cv(cv_threshold=0.2), all remaining features have CV ≤ 0.2 across technical replicates.
- After filter_mispicked_ions(merge_peaks=TRUE, merge_method='sum'), isotopic patterns that were previously split into separate rows are consolidated, reducing total feature count while preserving biological signal via summation.

## Limitations

- Filters are independent; the order of application can affect results. No canonical ordering is prescribed; workflows must be project-specific.
- filter_cv() requires technical replicates to estimate reproducibility; if absent, this filter cannot be applied.
- filter_group() removes all features present in a designated group; if that group contains both true signal and contaminants, true biological features may be lost.
- No changelog is maintained in the repository, making it difficult to track breaking changes between versions.
- The copy_object parameter affects both memory usage and code clarity; in-place modification (copy_object=FALSE) can lead to unintended side effects if the original object reference is needed downstream.

## Evidence

- [abstract] Reference semantics in R6 classes: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,"
- [readme] Filter independence and composability: "All filters are independent, meaning they can be used to create a project-specific workflow"
- [methods] filter_mispicked_ions() behavior and parameters: "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"
- [other] In-place modification with copy_object=FALSE: "When filter_mispicked_ions() is called with copy_object=FALSE, the original data object is updated in-place; the raw data object with 7269 ions was reduced to 6625 ions"
- [readme] filter_group() target and use case: "filter_group(): removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover between samples"
- [readme] filter_cv() purpose and parameter: "filter_cv(): removal of non-reproducible features, or those that are inconsistent between technical replicates"
- [readme] filter_insource_ions() purpose and clustering parameter: "filter_insource_ions(): removal of fragment ions created during the first ionization in the tandem MS/MS workflow"
