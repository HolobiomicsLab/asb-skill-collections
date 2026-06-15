---
name: categorical-ion-status-aggregation
description: Use when after running qc_summary() on a filtered mpactr object when you need to understand the distribution of ions across filter status categories (passed vs. failed filters) and want to visualize or report the count and percentage composition of each status group.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - mpactr
  - data.table
  - ggplot2
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`
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

# categorical-ion-status-aggregation

## Summary

Aggregate ion counts and percentages by filter status category from qc_summary() output to enable comparative visualization of filtering results across passed/failed filter states. This skill transforms QC summary data into categorical counts suitable for treemap or other categorical visualizations.

## When to use

Apply this skill after running qc_summary() on a filtered mpactr object when you need to understand the distribution of ions across filter status categories (passed vs. failed filters) and want to visualize or report the count and percentage composition of each status group.

## When NOT to use

- Ion status has not yet been computed via qc_summary() (run qc_summary() first)
- Goal is to visualize individual ion features rather than aggregate status categories (use ion-level plotting instead)
- No filtering has been applied to the mpactr object (status categories will be uninformative)

## Inputs

- mpactr filtered object (with qc_summary() method available)
- qc_summary() output data.table with ion status columns

## Outputs

- data.table or data.frame with columns: status (character), count (integer), percentage (numeric)

## How to apply

Extract the qc_summary() data.table output and use data.table syntax to group ions by their filter status (e.g., passed/failed). For each status category, compute the total count of ions and calculate the percentage as (count / total ions) × 100. The rationale is that qc_summary() reports ion-level pass/fail outcomes for each filter (mispicked, group, cv, insource), and aggregating these by status category yields the denominator and proportions needed for treemap area sizing and labeling. Store results in a data.frame or data.table with columns for status, count, and percentage for downstream visualization.

## Related tools

- **mpactr** (source of qc_summary() method and filtered ion objects with status annotations) — https://github.com/mums2/mpactr
- **data.table** (grouping and aggregation engine for ion counts and percentage calculations)
- **ggplot2** (visualization of aggregated status categories (downstream of aggregation))

## Examples

```
qc_dt <- qc_summary(mpactr_obj); status_agg <- qc_dt[, .(count = .N, percentage = 100 * .N / nrow(qc_dt)), by = status]; print(status_agg)
```

## Evaluation signals

- Sum of all status counts equals the total number of ions in the qc_summary() output
- Sum of all percentages across status categories equals 100 ± 0.01
- Each status category has count ≥ 0 and percentage ∈ [0, 100]
- No missing or NA values in the aggregated count or percentage columns
- Treemap or categorical plot uses the aggregated counts and percentages for area and label sizing without modification

## Limitations

- Aggregation is sensitive to the specific filters applied upstream; different filter combinations produce different status category distributions
- qc_summary() output structure may vary if the mpactr object was constructed with non-standard filter configurations; verify column names match expected status labels
- Percentage calculations assume all ions in qc_summary() have a defined status; missing or ambiguous status values should be handled or excluded before aggregation

## Evidence

- [other] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap"
- [other] qc_summary() data.table reporting ion status (passed/failed filters): "Load filtered mpactr object and extract qc_summary() data.table reporting ion status (passed/failed filters)"
- [other] Aggregate ion counts by status category and calculate percentage of total ions per status: "Aggregate ion counts by status category and calculate percentage of total ions per status"
