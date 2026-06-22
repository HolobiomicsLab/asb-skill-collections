---
name: filter-output-interpretation
description: Use when after applying a filter function (filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions()) to an mpactr object, use this skill to inspect and document which features were retained versus removed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
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

# filter-output-interpretation

## Summary

Extract and interpret the named list structure returned by filter_summary() to understand which ions passed or failed a specific filter (e.g., mispicked, group, cv, insource). This skill enables systematic review of filter results, conversion to tabular format, and export for downstream analysis.

## When to use

After applying a filter function (filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions()) to an mpactr object, use this skill to inspect and document which features were retained versus removed. Trigger this when you need to validate filter decisions, audit feature loss, or prepare filtered results for publication or further statistical analysis.

## When NOT to use

- Filter has not yet been applied to the mpactr object (call the filter function first, e.g., filter_mispicked_ions())
- You only need a count summary; filter_summary() returns detailed ion-level data, not aggregated statistics
- Input is not an mpactr object (e.g., a raw peak table or external feature list)

## Inputs

- filtered mpactr object (R6 reference class with in-place updated state)
- filter name string ('mispicked', 'group', 'cv', or 'insource')

## Outputs

- named list with 'failed_ions' and 'passed_ions' vectors
- data.table(s) with compound identifiers and filter status columns
- CSV export files documenting ion fate per filter

## How to apply

Call filter_summary(data_object, filter_name) where filter_name is one of 'mispicked', 'group', 'cv', or 'insource'. This returns a named list with two components: failed_ions (those removed by the filter) and passed_ions (those retained). Convert each vector to a data.table by adding compound identifier and filter status columns using data.table operations. Use head() to inspect subset of records before exporting both tables to CSV format for validation, visualization, or integration into downstream metabolomics workflows. The rationale is that documenting filter decisions—which features were removed and why—is essential for reproducing analysis decisions and understanding feature loss across filter stages.

## Related tools

- **mpactr** (R package providing filter_summary() function and R6 mpactr class for in-place filtering and output interpretation) — https://github.com/mums2/mpactr
- **data.table** (R package for converting ion vectors to tabular format and exporting filtered results to CSV)
- **R** (Language and runtime for executing filter_summary() calls and data transformation pipelines)

## Examples

```
filter_summary(mpactr_object, 'mispicked')
```

## Evaluation signals

- filter_summary() returns a named list with exactly two components: 'failed_ions' and 'passed_ions'
- Sum of lengths of failed_ions and passed_ions equals total number of input features before filtering
- Data.table conversion preserves all ion identifiers and adds filter status column with consistent values ('failed' or 'passed')
- CSV exports contain no missing values in compound identifier or filter status columns
- head() output shows expected number of rows (default 6) and matches ion names and status in full tables

## Limitations

- filter_summary() only returns results for the single most recently applied filter; sequential application of multiple filters requires calling filter_summary() after each filter step to track cumulative feature loss
- Ion identifiers depend on input peak table structure and naming conventions; mismatches or special characters may affect downstream parsing or export
- No built-in visualization; practitioners must construct plots (e.g., via ggplot2) to display filter funnel or Upset diagrams across multiple filters

## Evidence

- [methods] filter_summary() returns a named list containing two components: failed_ions and passed_ions: "filter_summary() returns a named list containing two components: failed_ions and passed_ions, both of which can be displayed as data tables using head()"
- [methods] Convert each vector to a data.table with compound identifiers and filter status columns, then export to CSV: "Convert each vector to a data.table with compound identifiers and filter status columns. 4. Export both tables to CSV format for downstream analysis or visualization."
- [readme] All filters are independent and can be combined into a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
- [readme] Available filter types: mispicked, group, cv, insource: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing. filter_group(): removal of features overrepresented in a specific"
- [methods] R6 reference semantics enable in-place data updates without copying the entire object: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
