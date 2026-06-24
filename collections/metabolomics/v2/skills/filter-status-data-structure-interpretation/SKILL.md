---
name: filter-status-data-structure-interpretation
description: Use when after applying a sequence of mpactr filters (filter_mispicked_ions,
  filter_group, filter_cv, filter_insource_ions) to an LC-MS/MS peak table in Progenesis
  or MS-DIAL format, call qc_summary() to obtain a structured report of per-ion filtering
  outcomes and use this skill to understand.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - data.table
  - mpactr
  - ggplot & plotly
  techniques:
  - LC-MS
  license_tier: restricted
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

# filter-status-data-structure-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret the data.table returned by qc_summary() to understand which ions passed or failed the complete mpactr filtering pipeline and which specific filter(s) caused rejection. This skill enables rapid identification of data quality outcomes and traceability of filtering decisions across mispicked, group, CV, and in-source filters.

## When to use

After applying a sequence of mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to an LC-MS/MS peak table in Progenesis or MS-DIAL format, call qc_summary() to obtain a structured report of per-ion filtering outcomes and use this skill to understand pass/fail patterns, count retained vs. rejected features, and diagnose which filters are most stringent in your dataset.

## When NOT to use

- Input mpactr object has not yet been filtered; qc_summary() will report no filtering outcomes.
- Peak table is in a format other than Progenesis or MS-DIAL; import_data() will fail or produce unexpected structures.
- Goal is to visualize filter failures interactively; use ggplot and plotly instead to create plots of features and their failed filters.

## Inputs

- mpactr object after sequential application of filter_mispicked_ions(), filter_group(), filter_cv(), and/or filter_insource_ions()
- cultures_peak_table.csv (Progenesis or MS-DIAL formatted LC-MS/MS feature table)

## Outputs

- data.table with columns: compound ID and filtering status (one row per ion)
- Summary statistics: count of passing ions, per-filter rejection counts, stratified tallies

## How to apply

Call qc_summary() on the fully-filtered mpactr object to extract a data.table with one row per ion (identified by compound ID). Each row contains a filtering status field that reports either 'passed' (ion passed all filters), or the name of the filter that caused rejection (e.g., 'mispicked', 'group', 'cv', 'insource'). Parse this table to count passing ions, tally ions rejected by each filter, and cross-tabulate filter failures to understand which filtering steps are most selective. Use data.table subsetting and grouping operations (e.g., .N for counts, by= for stratification) to summarize outcomes by filter type and by biological group if applicable. This output is the definitive record of which features qualify as 'high quality MS1 features' after preprocessing error correction.

## Related tools

- **mpactr** (Provides qc_summary() function and filter_* functions that populate filtering status; enables reference-semantic in-place filtering and structured output) — https://github.com/mums2/mpactr
- **data.table** (Underlying data structure returned by qc_summary(); enables fast subsetting, grouping, and counting of filter outcomes)
- **R** (Environment for executing mpactr functions and data.table queries)
- **ggplot & plotly** (Alternative downstream visualization of filter failures; can plot features and the filters they failed)

## Examples

```
qc_summary_table <- qc_summary(filtered_mpactr_obj); qc_summary_table[, .N, by = filtering_status]
```

## Evaluation signals

- qc_summary() output is a data.table with one row per ion and columns for compound ID and filtering status (schema check).
- Sum of all per-filter rejection counts plus passing ion count equals total input ion count (accounting check).
- Filtering status values match only the applied filter names (mispicked, group, cv, insource) or 'passed' (value validation).
- No NA or missing values in filtering status column; every ion has a deterministic outcome (completeness check).
- Cross-reference a random sample of ions marked 'failed' against the original peak table to confirm they were indeed rejected during the corresponding filter step (spot-check traceability).

## Limitations

- qc_summary() returns only the name of the first (most stringent) filter that rejected an ion; if an ion fails multiple filters, only one is reported.
- Filtering status does not capture the magnitude of failure (e.g., how far below a CV threshold, or what relative abundance in a blank); raw intensity and statistical metrics must be inspected separately.
- No built-in change log or version history of filtering parameters is available; reproducibility requires external documentation of filter thresholds and order of application.
- Output is specific to the mpactr object state at the time qc_summary() is called; applying additional filters after qc_summary() requires re-running the function.

## Evidence

- [methods] qc_summary() returns a data.table structure with compound IDs and per-ion filtering outcomes: "The qc_summary() function returns a data.table with compound IDs and filtering status for each ion"
- [methods] Passing ions are marked as 'passed'; failing ions report the name of the filter they failed: "where passing ions are marked as passed and failing ions report the name of the filter they failed"
- [methods] qc_summary() is called on a fully-filtered mpactr object after sequential application of multiple filters: "Call qc_summary() on the fully-filtered mpactr object to extract the data.table containing compound IDs and filter status"
- [readme] mpactr filters address mispicked ions, group-specific contamination, CV-based reproducibility, and in-source fragmentation: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing. filter_group(): removal of features overrepresented in a specific"
- [readme] mpactr filters are independent and can be combined in a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
