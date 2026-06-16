---
name: visualization-comparative-performance-metrics
description: Use when you have execution-time data for the same set of plotting operations (e.g., chromatogram, spectrum, peakmap rendering) across two or more backend implementations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pandas
  - matplotlib
  - Python
  - pyOpenMS-Viz
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
---

# visualization-comparative-performance-metrics

## Summary

Systematically extract, compute, and visualize execution-time metrics (median, min, max) across multiple plotting backends for mass spectrometry visualization plot types to identify performance leaders and bottlenecks. This skill enables quantitative backend comparison at the plot-type granularity, critical for choosing the optimal backend for interactive or static rendering workflows.

## When to use

You have execution-time data for the same set of plotting operations (e.g., chromatogram, spectrum, peakmap rendering) across two or more backend implementations (e.g., matplotlib, Bokeh, Plotly) and need to determine which backend achieves the fastest median execution time for each plot type, or to identify plot types where backend choice has the most impact on performance.

## When NOT to use

- Execution-time data is missing, incomplete, or not disaggregated by plot type and backend.
- You are comparing only one backend; median/ranking comparisons require ≥2 backends.
- Plot types in the data are not clearly labeled or differ from the canonical set (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots).

## Inputs

- Structured execution-time data (table or CSV) with columns: plot_type, backend, execution_time_ms
- Gallery script inventory mapping each script to plot type and backend used

## Outputs

- Summary statistics table (plot_type, backend, median_time, min_time, max_time, rank_within_category)
- Comparative visualization (bar chart or heatmap) showing median execution times across backends per plot type
- Ranked backend list per plot type

## How to apply

First, extract reported execution times from a structured data source (e.g., computation-times table in methods or supplementary materials) and categorize each timing observation by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend (matplotlib, Bokeh, Plotly). Group by plot type and backend, then compute three summary statistics for each group: median execution time (central tendency), minimum and maximum times (range). Rank backends within each plot-type category by median time to identify the fastest and slowest performer. Construct a summary table with columns [plot_type, backend, median_time, min_time, max_time, rank_within_category] and produce a comparative visualization (bar chart or heatmap) to surface patterns—e.g., whether one backend dominates across all plot types or whether performance varies by dimensionality (1D vs. 2D/3D). The ranking within category, not global ranking, is key: a backend might be fastest for spectra but slowest for peakmaps.

## Related tools

- **pandas** (Groupby, aggregation (median, min, max), and summary table construction from execution-time records)
- **matplotlib** (Static comparative visualization (bar charts, heatmaps) of backend performance metrics)
- **Python** (Scripting language for extracting, computing, and visualizing performance metrics)
- **pyOpenMS-Viz** (Reference implementation whose gallery scripts and computation times are the data source for this analysis) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
import pandas as pd; times = pd.read_csv('computation_times.csv'); summary = times.groupby(['plot_type', 'backend'])['execution_time_ms'].agg(['median', 'min', 'max']).reset_index(); summary['rank'] = summary.groupby('plot_type')['median'].rank(); print(summary); summary.pivot(index='plot_type', columns='backend', values='median').plot(kind='bar')
```

## Evaluation signals

- Summary table is complete: every plot type × backend combination present in raw data is represented; no rows are missing or duplicated.
- Median, min, and max times are computed correctly: verify a sample (e.g., plot_type='spectrum', backend='matplotlib') by manual calculation on the raw execution times.
- Ranking within each plot-type category is correct: for each plot type, the backend with the smallest median_time has rank=1; ties are handled consistently.
- Comparative visualization is legible and accurate: bar chart or heatmap axes are labeled correctly; color scale (if used) reflects numeric performance differences; legend distinguishes backends.
- Summary table can be used to answer the core research question: 'Which plotting backend exhibits the fastest median execution time for each mass spectrometry plot type?' — the answer should be readable directly from the rank column or visualization.

## Limitations

- Execution times are sensitive to system state (CPU load, memory pressure, Python interpreter version); a single pass of timing data may not be representative. Median is more robust than mean, but ideally multiple runs per plot type × backend should be collected.
- Timing does not capture quality attributes (interactivity, resolution, output file size, browser rendering overhead). A backend may be fastest in generation time but slowest in interactive responsiveness.
- Plot types must be clearly categorized in source data. If gallery scripts are not explicitly labeled by plot type, manual categorization introduces subjectivity and error.
- The analysis is snapshot-in-time: performance may change with backend version updates. Tracking backend version used in each timing run is important for reproducibility.

## Evidence

- [other] Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type and backend: "Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [other] Compute median execution time for each plot-type and backend combination: "Compute median execution time for each plot-type and backend combination."
- [other] Rank backends by median execution time within each plot category: "Rank backends by median execution time within each plot category to identify fastest and slowest."
- [other] Generate a structured summary table and produce a comparative visualization: "Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. 6. Produce a comparative visualization (bar chart or heatmap) showing"
- [readme] pyOpenMS-Viz integrates with multiple plotting backends (matplotlib, Bokeh, Plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [readme] Support for multiple plotting backends with different visualization characteristics: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
