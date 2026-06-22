---
name: filter-outcome-aggregation-and-counting
description: Use when after applying one or more mpactr filters (mispicked, group, cv, insource) to a feature table, you need to quantify the distribution of ions by their pass/fail status across filters to understand filtering impact, identify potential over-filtering, or communicate QC results via treemap or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - ggplot
  - mpactr
  - data.table
  - ggplot2
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

# filter-outcome-aggregation-and-counting

## Summary

Aggregate and count ion filtering outcomes (passed/failed status) across all ions and filter types to enable downstream summarization and visualization of quality control results. This skill transforms per-ion filter status into group counts and percentages, supporting transparent reporting of how many ions survive each filtering stage.

## When to use

After applying one or more mpactr filters (mispicked, group, cv, insource) to a feature table, you need to quantify the distribution of ions by their pass/fail status across filters to understand filtering impact, identify potential over-filtering, or communicate QC results via treemap or summary plots.

## When NOT to use

- Input data has not yet been filtered; apply at least one filter (e.g., filter_mispicked_ions, filter_group) before aggregating outcomes.
- You only need to report pass/fail counts for a single ion; this skill is for population-level aggregation, not per-ion inspection.
- qc_summary() output is unavailable or empty (indicates filtering workflow was not completed).

## Inputs

- filtered mpactr object (after applying one or more filters)
- qc_summary() output (per-ion filter status: passed/failed for mispicked, group, replicability, insource)

## Outputs

- aggregated summary data frame (status, count, percentage columns)
- treemap visualization (ggplot2 object or exported PNG)
- summary statistics (total ions, count by status)

## How to apply

Extract per-ion filter status from qc_summary() output, which reports whether each ion passed or failed each of the four filter types (mispicked, group, replicability, insource). Use data.table grouping operations to count ions per status category and calculate the percentage of total ions for each category. Construct a summary data frame with columns for status, count, and percentage. Render this aggregated result as a treemap using ggplot2's geom_treemap() and geom_treemap_text() to visualize tile areas proportional to ion counts and label each tile with status, count, and percentage. The treemap enables rapid visual assessment of filtering selectivity and identifies which filters are most stringent.

## Related tools

- **mpactr** (source of qc_summary() method and filtered feature table with per-ion filter status) — https://github.com/mums2/mpactr
- **data.table** (grouping and aggregation of ion counts by filter status)
- **ggplot2** (rendering treemap visualization with geom_treemap and geom_treemap_text layers)
- **R** (execution environment for qc_summary extraction, data.table operations, and ggplot rendering)

## Examples

```
qc_out <- qc_summary(filtered_mpactr_obj); summary_df <- qc_out[, .(count = .N), by = status][, percentage := 100 * count / sum(count)]; ggplot(summary_df, aes(area = count, fill = status, label = paste(status, count, percentage, sep = "\n"))) + geom_treemap() + geom_treemap_text()
```

## Evaluation signals

- Aggregated ion counts sum to the total number of ions in the filtered object (invariant check).
- All ions are assigned to exactly one status category (no missing or duplicate counts).
- Percentages sum to 100% or very close (allowing for rounding); spot-check one or two status percentages by hand calculation from counts.
- Treemap tiles are visually proportional to reported counts; larger counts occupy larger areas.
- Treemap labels are readable and include status name, count, and percentage for each tile; no labels are truncated or missing.

## Limitations

- qc_summary() reports cumulative pass/fail status for each ion across all applied filters; it does not isolate the contribution of individual filters, so you cannot determine which single filter is most selective from aggregated counts alone.
- If filters are applied with copy_object=TRUE (deep copying), memory usage may be high for large datasets; the article recommends copy_object=FALSE for efficiency, but this does not affect aggregation accuracy.
- Treemap visualization may become crowded if there are many filter status categories; consider filtering or grouping status labels if the number of unique categories is very high.

## Evidence

- [methods] qc_summary() output and per-ion filter status extraction: "Pivot qc_summary output to count ions per status category and calculate percentage of total ions for each status."
- [methods] data.table-based aggregation workflow: "Ion counts and percentages by status can be computed from qc_summary() output using data.table grouping"
- [methods] treemap rendering as visualization: "Render treemap using ggplot2 with geom_treemap() for tile areas (scaled by count) and geom_treemap_text() for status labels and percentages."
- [methods] filter types included in qc_summary: "per-ion filter status (passed/failed for mispicked, group, replicability, insource filters)"
- [readme] mpactr filter overview from README: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors"
