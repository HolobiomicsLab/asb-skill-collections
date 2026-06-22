---
name: ion-filter-status-categorization
description: Use when after applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to a peak table, when you need to quantify how many ions passed or failed each filter and summarize the overall filtering impact by status distribution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - mpactr
  - data.table
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

# ion-filter-status-categorization

## Summary

Categorize ions by their pass/fail status across multiple quality-control filters (mispicked, group, replicability, insource) and aggregate counts and percentages per status category. This enables structured summarization of filtering outcomes prior to visualization or downstream statistical analysis.

## When to use

After applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to a peak table, when you need to quantify how many ions passed or failed each filter and summarize the overall filtering impact by status distribution. Use this skill when preparing data for treemap or tabular reporting of QC outcomes.

## When NOT to use

- Input is raw, unfiltered peak table — apply filters first before categorizing status.
- Goal is to identify individual ions that failed a specific filter — use per-ion qc_summary output directly instead of aggregating.
- Peak table has not been imported into mpactr format — use import_data() first.

## Inputs

- mpactr object (post-filtering)
- qc_summary() output (data frame with per-ion filter status columns)

## Outputs

- data frame with columns: status, count, percentage
- ion count and percentage distribution by filter status

## How to apply

Call qc_summary() on the filtered mpactr object to extract per-ion filter status (passed/failed for mispicked, group, replicability, and insource filters). Pivot or group the qc_summary output using data.table grouping operations to count the number of ions in each status category (e.g., 'passed_all', 'failed_mispicked', 'failed_group'). Calculate the percentage of total ions for each status by dividing category count by total ion count. Store results in a data frame with columns for status label, ion count, and percentage. The rationale is that aggregating pass/fail outcomes by filter type provides a quantitative summary of data quality and the selective impact of each filter stage, enabling both numerical reporting and area-proportional visualization.

## Related tools

- **mpactr** (Provides qc_summary() function to extract per-ion filter status and enables chaining of multiple filters whose outcomes are then categorized) — https://github.com/mums2/mpactr
- **data.table** (Used to group qc_summary output by status and compute aggregated counts and percentages)
- **ggplot2** (Renders treemap or other visualizations of the status-aggregated counts (optional downstream use))

## Examples

```
qc_summary_output <- qc_summary(filtered_mpactr_obj); status_counts <- qc_summary_output[, .(count = .N, percentage = 100 * .N / nrow(qc_summary_output)), by = status]
```

## Evaluation signals

- Sum of all category counts equals total number of ions in the input peak table.
- Sum of all category percentages equals 100% (within rounding error).
- Each status category label is present in exactly one row of the output data frame (no duplicates).
- Counts are non-negative integers; percentages are in range [0, 100].
- Status labels match the filter types available in qc_summary (mispicked, group, replicability, insource) or compound combinations thereof.

## Limitations

- qc_summary() output depends on which filters were applied to the mpactr object; if no filters are run, all ions will show 'passed' status, which may not reflect actual data quality.
- Categorization relies on correct interpretation of the qc_summary output structure; incorrect pivoting or grouping can produce misleading aggregates.
- Status categories may overlap or be hierarchical (e.g., an ion can fail multiple filters simultaneously); the aggregation strategy (e.g., counting as 'failed_any', 'failed_all', or per-filter) must be chosen before grouping.

## Evidence

- [methods] ion-status-extraction: "call qc_summary() to extract per-ion filter status (passed/failed for mispicked, group, replicability, insource filters)"
- [methods] data-aggregation: "Ion counts and percentages by status can be computed from qc_summary() output using data.table grouping"
- [abstract] filter-types: "filter = "mispicked", "group", "replicability", "insource""
- [methods] mpactr-capability: "The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data."
