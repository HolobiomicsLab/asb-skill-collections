---
name: qc-summary-table-extraction
description: Use when after applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to an mpactr object, call qc_summary() to obtain a structured report of which ions passed or failed each filter.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ggplot
  - data.table
  - mpactr
  - ggplot2
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`
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
---

# qc-summary-table-extraction

## Summary

Extract a data.table from an mpactr object that reports the pass/fail status of each ion across applied QC filters, enabling downstream aggregation and visualization of filtering outcomes. This skill transforms the in-memory filter state into a tabular, machine-readable summary suitable for statistical reporting and graphical display.

## When to use

After applying one or more mpactr filters (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to an mpactr object, call qc_summary() to obtain a structured report of which ions passed or failed each filter. Use this when you need to quantify filtering impact, audit which ions were removed and why, or prepare data for treemap or other visualizations of filter status distribution.

## When NOT to use

- Input mpactr object has no filters applied; qc_summary() will report all ions as 'passed' with no discrimination.
- You need raw peak intensity values or m/z information; qc_summary() reports filter status only, not chemical or abundance data.
- You want to re-filter or modify filter thresholds; qc_summary() is read-only and reflects the current state — create a new mpactr object to change filters.

## Inputs

- mpactr object (after one or more filter steps applied)
- filter state (stored in-memory in R6 reference class)

## Outputs

- data.table with one row per ion and columns reporting pass/fail status per filter
- aggregated ion count and percentage by filter status (via downstream data.table grouping)

## How to apply

Call qc_summary() on a filtered mpactr object; it returns a data.table with one row per ion and columns encoding the pass/fail status for each applied filter. The table uses reference semantics (R6 in-place updates), so subsetting or aggregating it does not copy the entire object into memory. Group by the filter status column(s) using data.table syntax (e.g., .SD, by=) to compute ion counts and percentages per status category. Verify that the table includes all ions present in the original mpactr object and that status values correspond exactly to the filters applied; missing rows or unexpected status codes indicate incomplete filtering or corrupted state.

## Related tools

- **mpactr** (R package providing the qc_summary() method and filter functions; stores filter state in R6 reference classes and returns status as data.table) — https://github.com/mums2/mpactr
- **data.table** (R package for efficient subsetting, grouping, and aggregation of qc_summary() output to compute ion counts and percentages by status)
- **ggplot2** (R package for downstream visualization of qc_summary() aggregates (e.g., via treemapify geom_treemap and geom_treemap_text))

## Examples

```
qc_dt <- qc_summary(mpactr_obj); qc_agg <- qc_dt[, .(count = .N, percent = 100 * .N / nrow(qc_dt)), by = filter_status]
```

## Evaluation signals

- qc_summary() output has one row per unique ion in the mpactr object; row count equals total ions minus any duplicates
- Status columns match the filter functions applied (e.g., 'mispicked', 'group', 'cv', 'insource'); unexpected or missing columns indicate incomplete filter state
- Aggregated ion counts by status sum to the total number of ions; percentage values sum to 100% per grouping
- Ion IDs in qc_summary() match those in the original peak table (import_data() input); no rows should be orphaned or unaccounted for
- Filtering is reproducible: re-running the same filter sequence on the same input yields identical qc_summary() output

## Limitations

- qc_summary() reflects only the filters applied at the time of the call; if filters are added or removed, the table must be re-generated.
- Filter thresholds (e.g., cv_threshold, cluster_threshold) are not stored in the qc_summary() output; external documentation or metadata is needed to interpret why an ion failed.
- Large datasets (tens of thousands of ions × many filters) may produce wide data.tables; subsetting or melting may be needed for efficient aggregation and visualization.
- No changelog or versioning is provided in the README, so filter logic or output schema changes across mpactr versions are not documented.

## Evidence

- [other] Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap: "Ion counts and percentages by status are computed from qc_summary() output using data.table syntax, then rendered as a treemap with geom_treemap() and geom_treemap_text()"
- [abstract] R6 reference semantics enable in-place data updates without copying the entire data object: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,"
- [readme] mpactr provides multiple independent filters for identifying high quality MS1 features: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data."
- [readme] Filters address mispicked ions, group overrepresentation, low replicability, and in-source fragmentation: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing. filter_group(): removal of features overrepresented in a specific"
- [readme] All filters are independent and can be composed into a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
