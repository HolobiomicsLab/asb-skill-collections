---
name: metabdata-object-handling
description: Use when you have a raw peak-picked untargeted LC-MS dataframe with columns containing mass-to-charge (m/z), retention time (rt), feature identifiers, adduct annotations, and sample measurements in non-standard column names or mixed column sets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metabCombiner
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
---

# metabdata-object-handling

## Summary

Construct and validate metabData objects from untargeted LC-MS metabolomics dataframes by detecting and mapping required columns (m/z, retention time, feature ID, adduct, samples) and applying retention time, missingness, and duplicate filters. This is the foundational data formatting step that prepares raw peak-picked LC-MS tables for downstream feature alignment.

## When to use

You have a raw peak-picked untargeted LC-MS dataframe with columns containing mass-to-charge (m/z), retention time (rt), feature identifiers, adduct annotations, and sample measurements in non-standard column names or mixed column sets. Apply this skill before attempting feature alignment between two datasets.

## When NOT to use

- Input is already a formatted metabData object (apply filters directly instead)
- Column structure and naming conventions are already standardized and validated (skip to feature alignment)
- Data is from a targeted metabolomics assay with pre-identified compounds (different workflow applies)

## Inputs

- LC-MS metabolomics dataframe with raw peak-picked features
- Column name vectors or regex patterns for mz, rt, id, adduct, samples fields

## Outputs

- metabData object with standardized and filtered feature table
- Formatted columns: idx, mz, rt, id, adduct, Q, sample columns

## How to apply

Use the metabData() constructor function to auto-detect the required mz, rt, id, adduct, and samples columns by substring matching (for mz/rt/id/adduct/Q fields, the first matching column is selected; for samples and extra fields, all columns containing any keyword are selected, with regex support). Then apply three sequential filters: (1) retention time range filter with rtmin and rtmax arguments to restrict features to a biologically relevant window (e.g., 0–17.25 min); (2) missingness filter with misspc argument to eliminate features present in fewer than the threshold percentage of samples; (3) duplicate filter to detect and remove redundant features within specified m/z (e.g., 0.0025 Da) and retention time (e.g., 0.05 min) distances. The resulting metabData object standardizes column structure and ensures data quality before m/z grouping and pairwise alignment.

## Related tools

- **metabCombiner** (Provides metabData constructor and filter functions for column detection, formatting, and quality filtering) — https://github.com/hhabra/metabCombiner
- **R** (Execution environment for metabData object construction and manipulation)

## Examples

```
library(metabCombiner); plasma20_formatted <- metabData(plasma20, mz='mz', rt='rt', id='id', adduct='adduct', samples='CHEAR', rtmin=0, rtmax=17.25, misspc=50)
```

## Evaluation signals

- metabData object successfully instantiates without column-name errors and displays accessible mz, rt, id, adduct, and samples slots
- Feature count decreases monotonically after each filter (rt range, missingness, duplicates); verify expected reduction ratios align with filter thresholds
- Spot-check that all remaining features have m/z and rt values within specified ranges and missingness is below threshold
- Verify no duplicate features remain by checking m/z and rt pairwise distances in output; should be ≥ the specified exclusion tolerance
- Combined feature list from two independently formatted metabData objects can be aligned by metabCombiner() without column mismatch errors

## Limitations

- Column auto-detection via substring matching is brittle if column names are non-standard or lack expected keywords; requires manual inspection of raw dataframe column names before construction
- Retention time range, missingness percentage, and duplicate distance thresholds are user-specified and require domain knowledge or exploratory analysis to justify; no default guidance provided in documentation
- The duplicate filter assumes m/z and rt are the only features defining redundancy; may fail if isobars or isomers with identical m/z and similar rt exist
- No automatic handling of adduct annotations if adduct column is missing; requires either manual column addition or explicit NULL handling

## Evidence

- [intro] metabData column detection mechanism: "For mz, rt, id, adduct, and Q fields, metabData searches for the first column whose name contains the supplied keyword; for samples and extra fields, it searches for all columns containing any of the"
- [intro] retention time range filter: "The retention time range filter restricts features to those between the *rtmin* and *rtmax* arguments."
- [intro] missingness filter: "The missingness filter eliminates features below some threshold percentage indicated by the *misspc* argument."
- [intro] duplicate filter: "The duplicate filter detects and removes features within close m/z and RT distances (e.g 0.0025Da & 0.05 min)."
- [intro] data formatting is step 1 of 5-step workflow: "The workflow we outline here is composed of five major steps: 1) Data Formatting and Filtering"
