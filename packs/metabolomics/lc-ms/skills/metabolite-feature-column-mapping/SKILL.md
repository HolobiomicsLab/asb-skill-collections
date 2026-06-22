---
name: metabolite-feature-column-mapping
description: Use when you have peak-picked LC-MS metabolomics data in a tabular format (R data frame) with columns for mass-to-charge ratio, retention time, feature identifiers, adduct annotations, and sample measurements, but the column names do not follow a standard naming convention.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - metabCombiner
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-column-mapping

## Summary

Map and validate required LC-MS metabolomics feature columns (m/z, retention time, feature ID, adduct annotation, samples) from heterogeneous input data frames into a standardized metabData object. This is the mandatory first step before filtering and alignment, ensuring that disparate data sources conform to a common schema.

## When to use

You have peak-picked LC-MS metabolomics data in a tabular format (R data frame) with columns for mass-to-charge ratio, retention time, feature identifiers, adduct annotations, and sample measurements, but the column names do not follow a standard naming convention. Apply this skill when you need to ingest raw or semi-processed metabolomics tables into the metabCombiner workflow and must disambiguate column roles before filtering or alignment.

## When NOT to use

- Input is already a formatted metabData object; re-mapping is redundant.
- Feature table is already aligned across multiple datasets; use this skill only on individual source datasets before combining.
- Column roles are completely unknown or unmapped; manual curation is required before invoking the constructor.

## Inputs

- R data frame with peak-picked LC-MS features (one row per feature)
- Column name keywords or patterns for mz, rt, id, adduct, samples, and optional extra fields

## Outputs

- metabData object with formatted and filtered feature metadata
- Subset of original features passing retention time, missingness, and duplicate filters

## How to apply

Use the metabData constructor function with keyword-based column matching: for single-valued fields (mz, rt, id, adduct), specify a keyword and the function will locate the first column name containing that keyword; for multi-valued fields (samples, extra), supply a character vector of keywords and the function will match all columns containing any keyword, with regular expression support enabled for any field. Pass these mapped columns through three sequential filters: (1) retention time range filter (rtmin/rtmax arguments, e.g., rtmax=17.25 min) to restrict features to a valid LC window; (2) missingness filter (misspc argument) to remove features with sample coverage below a threshold percentage; (3) duplicate filter to detect and remove features within tight m/z (e.g., ±0.0025 Da) and retention time (e.g., ±0.05 min) distances. The result is a metabData object with validated, filtered feature metadata ready for m/z grouping and pairwise alignment.

## Related tools

- **metabCombiner** (R package providing the metabData constructor function and filtering methods for LC-MS metabolomics column mapping and feature validation) — https://github.com/hhabra/metabCombiner
- **R** (Programming language and runtime environment for executing metabData constructor and filter operations)

## Examples

```
library(metabCombiner); data(plasma20); mapped_data <- metabData(plasma20, mz='mz', rt='rt', id='id', adduct='adduct', samples=c('CHEAR'), rtmin=0.5, rtmax=17.25, misspc=50)
```

## Evaluation signals

- metabData object is created without errors, confirming all required fields were successfully mapped.
- Feature count decreases monotonically through the three filters (RT range, missingness, duplicates), with each step removing a non-negative number of features.
- Mapped columns contain expected data types: numeric for mz and rt; character/factor for id and adduct; numeric or logical for sample measurements.
- No NA or missing values appear in mz, rt, or id columns after filtering; sample columns may retain missingness as expected.
- Features within the retained set satisfy the specified rtmin/rtmax bounds, misspc threshold, and duplicate distance criteria (e.g., all pairwise m/z deltas > 0.0025 Da or RT deltas > 0.05 min).

## Limitations

- Column detection relies on substring or regex matching; ambiguous or non-standard naming schemes may cause misidentification or failure.
- The duplicate filter uses fixed distance thresholds (m/z and RT) that may not be appropriate for all instrument types, ionization methods, or metabolite classes.
- Missingness filter removes features based on a global percentage threshold; no per-sample or group-specific missing data handling.
- The metabData constructor does not validate chemical plausibility (e.g., whether adduct annotations are chemically sensible); it is a syntactic, not semantic, check.

## Evidence

- [intro] metabData searches for the first column whose name contains the supplied keyword; for samples and extra fields, it searches for all columns containing any of the keywords in the respective arguments, with regular expressions accepted for any indicated field.: "For mz, rt, id, adduct, and Q fields, metabData searches for the first column whose name contains the supplied keyword; for samples and extra fields, it searches for all columns containing any of the"
- [intro] The retention time range filter restricts features to those between rtmin and rtmax arguments; the missingness filter eliminates features below a threshold percentage indicated by the misspc argument; the duplicate filter detects and removes features within close m/z and RT distances.: "The retention time range filter restricts features to those between the *rtmin* and *rtmax* arguments. The missingness filter eliminates features below some threshold percentage indicated by the"
- [readme] metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their measurements to form a combined table.: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their"
- [intro] Data Formatting and Filtering is the first major step in the metabCombiner workflow.: "The workflow we outline here is composed of five major steps: 1) Data Formatting and Filtering"
