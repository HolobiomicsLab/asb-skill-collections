---
name: qc-summary-data-extraction
description: Use when after applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to a feature table, use qc_summary() to extract the pass/fail status of each ion across all applied filters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - data.table
  - mpactr
  - ggplot2
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
- creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`
- library(data.table)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# qc-summary-data-extraction

## Summary

Extract per-ion filter status summaries from mpactr filtering operations to obtain counts and pass/fail outcomes for each filter (mispicked, group, replicability, insource). This skill enables structured analysis of which ions passed or failed quality control, forming the basis for downstream visualization and reporting of filtering efficacy.

## When to use

After applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to a feature table, use qc_summary() to extract the pass/fail status of each ion across all applied filters. This is necessary before summarizing filtering results by status category, visualizing filter distribution, or generating QC reports that account for multiple filter outcomes.

## When NOT to use

- Input is an unfiltered (raw) mpactr object—filters must be applied first to generate meaningful pass/fail status.
- Goal is to examine individual ion properties (m/z, retention time, intensity) rather than aggregate filter outcomes—use the raw feature table instead.
- Only one filter has been applied and pass/fail outcome is trivial—qc_summary is most valuable when multiple filters have been chained.

## Inputs

- mpactr object (filtered with one or more filter functions: filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions)

## Outputs

- qc_summary data frame (status, count, percentage columns)
- pivoted/grouped summary table of ion counts by filter status

## How to apply

Call qc_summary() on the filtered mpactr object to retrieve a structured output containing per-ion filter status (passed or failed for each of mispicked, group, replicability, and insource filters). Pivot or group the qc_summary output by filter status to count total ions per category and calculate the percentage of the total ion count for each status. The output is a data frame with columns for status, ion count, and percentage, suitable for downstream visualization (e.g., treemap) or tabular reporting. The rationale is that qc_summary() aggregates the binary pass/fail decisions made by individual filters into a single, queryable data structure that enables comparative analysis of filtering impact.

## Related tools

- **mpactr** (Provides qc_summary() function to extract filter status for each ion; orchestrates application of mispicked, group, replicability, and insource filters.) — https://github.com/mums2/mpactr
- **data.table** (Used to pivot and group qc_summary output by filter status and compute aggregated counts and percentages.)
- **ggplot2** (Downstream visualization of qc_summary-derived counts (e.g., treemaps with geom_treemap, bar charts); not required for extraction but commonly paired.)

## Examples

```
qc_summary_output <- qc_summary(filtered_mpactr_obj); summary_table <- qc_summary_output[, .(ion_count = .N, pct = 100*.N/nrow(qc_summary_output)), by = status]
```

## Evaluation signals

- qc_summary output contains one row per ion with filter status columns for mispicked, group, replicability, and insource filters, each populated with 'pass' or 'fail'.
- Sum of ion counts across all status categories equals the total number of ions in the input mpactr object (no loss or duplication).
- Percentage calculations sum to 100% across all status categories (or close to 100% accounting for rounding).
- No missing (NA) values in status or count columns for ions that were processed by at least one filter.
- Pivot/grouping operation correctly stratifies ions so that each ion appears in exactly one status category (e.g., 'passed_all_filters', 'failed_mispicked', 'failed_group_and_replicability').

## Limitations

- qc_summary output reflects only the filters that were actually applied; ions not subjected to a particular filter will have NA or a default status for that filter dimension.
- The pass/fail threshold for each filter (e.g., cv_threshold = 0.2 for filter_cv) must be chosen by the analyst before filtering; qc_summary does not allow post-hoc threshold adjustment.
- Large feature tables (>100k ions) may produce large qc_summary data frames; memory-efficient grouping with data.table and copy_object = FALSE is recommended.
- qc_summary aggregates binary outcomes and does not retain the underlying feature properties (m/z, RT, intensity, coefficient of variation) needed for diagnostic visualization—query the original feature table separately if those are needed.

## Evidence

- [methods] Extract per-ion filter status and count ions by outcome: "call qc_summary() to extract per-ion filter status (passed/failed for mispicked, group, replicability, insource filters)"
- [methods] Pivot output and compute aggregates: "Pivot qc_summary output to count ions per status category and calculate percentage of total ions for each status"
- [methods] Output schema: "Create a data frame with status, count, and percentage columns"
- [abstract] Filter types captured by qc_summary: "mispicked, group, replicability, insource filters"
- [abstract] Recommended use of memory-efficient operations: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
