---
name: ion-count-percentage-calculation
description: Use when after applying one or more mpactr filters (mispicked, group, cv, insource) to an mpactr object and generating a qc_summary() data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3208
  edam_topics:
  - http://edamontology.org/topic_3172
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-count-percentage-calculation

## Summary

Aggregate ion counts by filter status category and compute the percentage of total ions within each status using data.table operations on qc_summary() output. This calculation provides a quantitative breakdown of how many ions passed or failed each filtering step, enabling downstream visualization and quality assessment.

## When to use

After applying one or more mpactr filters (mispicked, group, cv, insource) to an mpactr object and generating a qc_summary() data.table, when you need to understand the distribution of ions across filter status categories (passed vs. failed) and quantify the proportion of the ion population affected by each filter decision.

## When NOT to use

- Input data is not from qc_summary() or does not contain filter status information (use alternative summary functions if available).
- Ion filtering has not yet been applied to the mpactr object (run filter_*() functions first).
- You only need pass/fail counts without percentages (simpler count aggregation may suffice).

## Inputs

- mpactr object (after filtering with filter_mispicked_ions(), filter_group(), filter_cv(), and/or filter_insource_ions())
- qc_summary() output (data.table with ion identifiers and filter status columns)

## Outputs

- data.table with columns: status (filter status category), count (number of ions), percentage (proportion of total ions)

## How to apply

Extract the qc_summary() data.table from a filtered mpactr object, which reports ion status (passed/failed) for each filtering step. Use data.table syntax to group ions by their filter status category and count the number of ions in each group. Calculate the percentage of total ions per status by dividing each status count by the sum of all ions and multiplying by 100. Store the aggregated counts and percentages in a new data.table suitable for visualization or reporting. The rationale is that qc_summary() already tracks pass/fail decisions; aggregation simply rolls these up to category-level summaries needed for treemaps or summary tables.

## Related tools

- **mpactr** (Source of qc_summary() output and filter status data; provides the mpactr object and its methods) — https://github.com/mums2/mpactr
- **data.table** (Aggregates ion counts by status and calculates percentages using efficient group-by operations)
- **ggplot2** (Visualizes the calculated ion counts and percentages (e.g., in treemaps or bar plots) downstream)

## Examples

```
qc_data <- qc_summary(mpactr_obj); ion_summary <- qc_data[, .(count = .N, percentage = round(100 * .N / nrow(qc_data), 2)), by = status]
```

## Evaluation signals

- Sum of all ion counts across status categories equals the total number of ions in qc_summary()
- Sum of all percentages across status categories equals 100% (or close, within floating-point precision)
- Each status category appears exactly once in the output data.table
- Counts are non-negative integers and percentages are between 0 and 100
- Ion counts and percentages match manual spot-checks on subset of the qc_summary() data

## Limitations

- qc_summary() must report filter status information; if status columns are missing or malformed, aggregation will fail or produce misleading results.
- Percentage calculation assumes all ions have a known status; missing or NA values in status columns will skew the total and percentage calculations unless explicitly handled.
- The calculation reflects only the ions present in qc_summary(); ions removed during preprocessing before filtering are not represented.

## Evidence

- [other] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap"
- [other] qc_summary() data.table reporting ion status (passed/failed filters): "extract qc_summary() data.table reporting ion status (passed/failed filters)"
- [other] Aggregate ion counts by status category and calculate percentage of total ions per status: "Aggregate ion counts by status category and calculate percentage of total ions per status."
- [readme] mpactr is a collection of filters for the purpose of identifying high quality MS1 features: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors"
