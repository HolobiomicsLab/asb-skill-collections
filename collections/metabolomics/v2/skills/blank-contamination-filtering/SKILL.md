---
name: blank-contamination-filtering
description: Use when your peak table includes features flagged in blank control samples
  (e.g., solvent blanks, media blanks) at relative abundance above a project-specific
  threshold.
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

# blank-contamination-filtering

## Summary

Remove MS1 features that are overrepresented in blank control samples (solvent blanks, media blanks) using group-based relative abundance thresholds. This skill corrects for carryover contamination and background signals that confound biological signal in metabolomics peak tables.

## When to use

Apply this skill when your peak table includes features flagged in blank control samples (e.g., solvent blanks, media blanks) at relative abundance above a project-specific threshold. Use it after importing raw peak tables and before applying replicability or statistical filters, especially when carryover between samples or media/solvent contamination is suspected.

## When NOT to use

- Input peak table is already pre-filtered at the instrument level without blank controls recorded.
- No blank samples were collected or included in the experimental design; filtering requires a reference blank group.
- All features in blank samples are technical replicates of biological samples; applying group filter would remove authentic biology.

## Inputs

- mpactr object (R6 reference object post-import_data())
- peak intensity table (Progenesis CSV format or equivalent)
- sample metadata with group/batch annotations identifying blank controls

## Outputs

- filtered mpactr object with blank-contaminated features marked/removed
- data.table from qc_summary() indicating filter status per feature (passed or failed 'group' filter)

## How to apply

Call filter_group() on your mpactr object, specifying the blank sample group to remove (e.g., 'Solvent_Blank' or 'Media_Blank') and setting a relative_abundance_threshold (typical range 0.01–0.05, or 1–5%). The filter compares feature intensity in blank samples to biological samples and flags/removes features where blank intensity exceeds the threshold relative to sample intensity. Rationale: blank-dominated features are likely artifacts (carryover, leached solvents, media components) rather than authentic metabolites. Repeat filter_group() for each blank type in your study design (solvent blank, then media blank). The order matters: remove solvent contamination first, then media, to avoid masking media-only contaminants. After filtering, inspect the qc_summary() output to confirm the number of features removed per blank filter and verify that authentic biological signals are retained.

## Related tools

- **mpactr** (R6 package hosting filter_group() method for blank-group-based feature removal with in-place reference semantics) — https://github.com/mums2/mpactr
- **data.table** (Underlying tabular format returned by qc_summary() for inspection and downstream analysis of filter results)
- **R** (Language and runtime for mpactr package and filter_group() execution)

## Examples

```
library(mpactr); obj <- import_data('cultures_peak_table.csv', 'cultures_metadata.csv', format='Progenesis'); obj$filter_group(group_to_remove='Solvent_Blank', relative_abundance_threshold=0.01); obj$filter_group(group_to_remove='Media_Blank', relative_abundance_threshold=0.01); summary_table <- obj$qc_summary()
```

## Evaluation signals

- qc_summary() output shows reduced feature count post-filter_group(); inspect 'filter' column for 'group' entries confirming blank-contaminated features were flagged.
- Manual inspection of a subset of removed features confirms they exhibit high intensity in blank samples and near-zero or minimal intensity in biological samples.
- Relative abundance threshold was applied consistently: verify that no feature in the blank group exceeds the chosen threshold (e.g., 0.01 or 1%) relative to non-blank samples.
- Re-running filter_group() on already-filtered data produces no new removals (idempotency check).
- Downstream statistical tests (fold change, t-tests) show reduced false-positive candidates compared to unfiltered data, indicating removal of non-biological signals.

## Limitations

- Threshold selection (relative_abundance_threshold) is project-specific and depends on instrumental background, sample handling, and carryover rate; no universal default exists in the literature.
- filter_group() assumes that blank and biological samples are well-separated in intensity; features with intermediate blank–sample ratios may be ambiguous and prone to misclassification.
- If biological samples genuinely contain solvent or media (e.g., cells cultured in the same medium as blank), legitimate features may be incorrectly removed; domain knowledge of sample preparation is required to set appropriate thresholds.
- Multiple blank types (solvent, media, buffer) require separate filter_group() calls; cumulative removal may inadvertently eliminate true low-abundance metabolites if thresholds are not re-evaluated after each step.

## Evidence

- [methods] filter_group() with group removal and relative abundance threshold: "Apply filter_group() to remove Solvent_Blank contaminant features above relative abundance threshold of 0.01. Apply filter_group() to remove Media blank features above relative abundance threshold of"
- [readme] Purpose of group filter in the package: "filter_group(): removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover between samples."
- [methods] qc_summary() output structure for interpreting filter results: "The qc_summary() function returns a data.table with compound IDs and filtering status for each ion, where passing ions are marked as passed and failing ions report the name of the filter they failed."
- [abstract] R6 reference semantics enabling in-place updates: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
