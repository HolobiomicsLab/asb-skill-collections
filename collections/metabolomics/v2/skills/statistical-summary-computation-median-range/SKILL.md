---
name: statistical-summary-computation-median-range
description: Use when when you have a table of execution times or performance metrics
  indexed by two or more categorical dimensions (e.g., plot_type × backend, or sample
  × condition), and you need to compare central tendency and spread across groups
  to rank or benchmark alternatives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - matplotlib
  - Python
  - pyOpenMS-Viz
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00873
  all_source_dois:
  - 10.1021/acs.jproteome.4c00873
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-summary-computation-median-range

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute median and range (min/max) statistics across grouped categorical dimensions (e.g., plot types and plotting backends) from execution-time or performance measurements. This skill transforms raw timing observations into ranked summary tables and comparative visualizations to identify fastest and slowest performers within each category.

## When to use

When you have a table of execution times or performance metrics indexed by two or more categorical dimensions (e.g., plot_type × backend, or sample × condition), and you need to compare central tendency and spread across groups to rank or benchmark alternatives. Specifically useful when the source data is a multi-row observation table (e.g., 19 gallery scripts with timing measurements) that must be aggregated by category to isolate the effect of each dimension.

## When NOT to use

- Input is already a pre-aggregated summary statistic (e.g., mean or median reported in a published table); re-computing from such compressed data introduces bias and loss of information.
- The timing observations have extreme outliers driven by system state (e.g., cache misses, GC pauses) that warrant robust trimming or removal before aggregation; median alone may still mask bimodal distributions.
- The categorical dimensions are continuous or have natural orderings that should be preserved in the analysis (e.g., parameter sweep); use regression or ANOVA-based approaches instead.

## Inputs

- Raw timing observation table (e.g., pandas DataFrame or CSV with columns: plot_type, backend, execution_time_ms)
- Categorical grouping dimensions (e.g., plot_type: [chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots]; backend: [matplotlib, bokeh, plotly])

## Outputs

- Structured summary table (pandas DataFrame or CSV) with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category
- Comparative visualization (bar chart or heatmap) showing median execution times across backends per plot type
- Ranked list of backends by median performance within each plot category

## How to apply

Load the raw timing observations into a pandas DataFrame, grouping by the categorical axes (e.g., plot_type and backend). For each group, compute the median execution time as the central performance estimate, and the min/max values to characterize the range of variability. Rank backends within each plot type by median time to establish a performance hierarchy. Organize results into a structured summary table with columns: category_1, category_2, median_time, min_time, max_time, rank_within_category. Finally, produce a comparative visualization (bar chart or heatmap) to expose patterns across groups. The median is robust to outliers and single slow runs; the min/max pair shows the spread without assuming normality.

## Related tools

- **pandas** (Group timing observations by plot_type and backend; compute median, min, and max for each group; construct and export summary DataFrame)
- **matplotlib** (Generate comparative bar chart or heatmap visualization of median execution times across backends per plot type)
- **Python** (Execute the statistical aggregation and visualization pipeline using pandas groupby, agg, and matplotlib plotting routines)
- **pyOpenMS-Viz** (Provides the gallery scripts and execution-time measurements that serve as the raw input data for this aggregation skill) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
import pandas as pd
df = pd.read_csv('gallery_execution_times.csv')
summary = df.groupby(['plot_type', 'backend'])['execution_time_ms'].agg(['median', 'min', 'max']).reset_index()
summary['rank'] = summary.groupby('plot_type')['median'].rank()
print(summary)
summary.to_csv('execution_summary.csv', index=False)
```

## Evaluation signals

- Summary table rows equal the number of (plot_type, backend) pairs; all numeric columns (median_time, min_time, max_time) are positive and min_time ≤ median_time ≤ max_time for every row.
- Rank_within_category is an integer in [1, num_backends], with no ties unless median times are identical; ranking is consistent within each plot_type group.
- Visualization (bar chart or heatmap) visually renders the summary table without distortion, with axis labels matching the original categorical values and color/height encoding median times.
- The summary table can be reconstructed by grouping the original raw timing table on (plot_type, backend) and applying pandas .agg({execution_time_ms: ['median', 'min', 'max']}).
- No rows are duplicated in the summary table, and the total observation count across all groups equals the input table row count.

## Limitations

- Median and range ignore the frequency and distribution shape of observations; if sample sizes per group are very small (n < 3), the median may be unstable and should be reported with confidence intervals.
- The min and max values are vulnerable to single-run anomalies (e.g., system interference); consider trimming extreme 5% of observations or reporting quantiles (e.g., 0.25, 0.5, 0.75) for more robust spread estimates.
- Ranking backends by median time within a plot type does not account for statistical significance or interaction effects; overlapping confidence intervals between backends may indicate no practically meaningful difference.
- The skill assumes the raw timing data are drawn from the same execution environment and hardware; cross-platform or cross-machine comparisons require normalization or stratified analysis.

## Evidence

- [other] Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type and backend.: "Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [other] Compute median execution time and range for each group, then rank backends and tabulate results.: "Compute median execution time for each plot-type and backend combination. Compute min and max execution times (range) for each plot-type and backend combination. Rank backends by median execution"
- [other] Produce a comparative visualization showing median times across backends per plot type.: "Produce a comparative visualization (bar chart or heatmap) showing median times across backends per plot type."
- [other] Generate a structured summary table documenting the aggregated statistics.: "Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category."
- [readme] pyOpenMS-Viz integrates with pandas for data manipulation and multiple plotting backends.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
