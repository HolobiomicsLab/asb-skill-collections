---
name: technical-replicate-reproducibility-assessment
description: Use when you have tandem MS data with technical replicates and need to
  remove features showing high variability between replicates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mpactr
  - data.table
  techniques:
  - LC-MS
  license_tier: open
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

# technical-replicate-reproducibility-assessment

## Summary

Assess the reproducibility of metabolomic features across technical replicates by filtering out non-reproducible compounds using coefficient of variation (CV) thresholds. This skill identifies high-quality, consistent MS1 features that warrant downstream analysis.

## When to use

Apply this skill when you have tandem MS data with technical replicates and need to remove features showing high variability between replicates. Use it after correcting peak selection errors (mispicked ions, in-source fragments) and removing contaminant groups (solvent blanks, media blanks), to ensure only reproducible compounds enter statistical analysis or fold-change calculations.

## When NOT to use

- Input data lacks technical replicates or replicate structure is not encoded in metadata
- Features have already been aggregated across replicates before calling filter_cv()
- Analysis goal requires retention of all detected features regardless of reproducibility (e.g., exploratory discovery with low-confidence candidates)

## Inputs

- mpactr object (post-import, with technical replicate structure preserved)
- Peak intensity matrix with replicate designations in metadata
- cv_threshold parameter (numeric, typically 0.1–0.5)

## Outputs

- Filtered mpactr object with replicability filter applied
- data.table from qc_summary() showing compound IDs and replicability pass/fail status
- Subset of compounds meeting reproducibility criterion

## How to apply

Call filter_cv() on the mpactr object with a cv_threshold parameter (typically 0.2 for 20% maximum coefficient of variation). The filter computes CV for each compound across all technical replicates within each sample and removes compounds exceeding the threshold. CV is calculated as (standard deviation / mean) for replicate measurements within each sample group. Set the threshold based on your instrument's and protocol's reproducibility expectations: lower thresholds (e.g., 0.1–0.15) retain only the most reproducible features, while higher thresholds (e.g., 0.3–0.5) are more permissive. After filtering, verify that the filter status in qc_summary() shows compounds marked as 'passed' or with 'replicability' filter status for those that failed.

## Related tools

- **mpactr** (R package implementing filter_cv() for CV-based replicability filtering of MS1 features) — https://github.com/mums2/mpactr
- **data.table** (R package used internally by qc_summary() to return and structure filter status output)
- **R** (Statistical computing environment for executing filter_cv() and qc_summary() workflows)

## Examples

```
library(mpactr); obj <- import_data('cultures_peak_table.csv', 'cultures_metadata.csv', format='Progenesis'); obj$filter_cv(cv_threshold=0.2); qc_summary_table <- obj$qc_summary()
```

## Evaluation signals

- qc_summary() output data.table contains 'replicability' or 'passed' status for each compound; no missing or NA values in filter status column
- Verify CV calculation is consistent: manually compute CV for a sample subset and confirm mpactr output matches (CV = std / mean for replicate intensities)
- Confirm that features failing replicability filter have CV values above cv_threshold; features passing have CV ≤ cv_threshold
- Downstream analyses (fold change, t-tests, volcano plots) use only compounds marked 'passed' in qc_summary(), indicating replicability filter was applied before statistical testing
- Document the cv_threshold chosen and the number/percentage of features retained vs. removed; report this in methods and results

## Limitations

- CV threshold is user-specified and sensitive to instrument performance and protocol variability; no universally optimal value—requires pilot data or literature precedent to justify choice
- Assumes technical replicates are correctly labeled in metadata; mislabeled replicates will produce spurious CV calculations
- Features with very low absolute intensity may have inflated CV values due to noise; consider coupling with intensity filtering or other QC steps
- Does not account for non-linear CV behavior across concentration ranges (e.g., higher CV at very low or very high intensities); may require stratified thresholds

## Evidence

- [methods] filter_cv() with cv_threshold=0.2 to flag non-reproducible compounds across technical replicates: "Apply filter_cv() with cv_threshold=0.2 to flag non-reproducible compounds across technical replicates."
- [readme] removal of non-reproducible features, or those that are inconsistent between technical replicates: "filter_cv(): removal of non-reproducible features, or those that are inconsistent between technical replicates."
- [methods] data.table with compound IDs and filtering status where passing ions are marked as passed: "The qc_summary() function returns a data.table with compound IDs and filtering status for each ion, where passing ions are marked as passed and failing ions report the name of the filter they failed."
- [readme] filters are independent, meaning they can be used to create a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
