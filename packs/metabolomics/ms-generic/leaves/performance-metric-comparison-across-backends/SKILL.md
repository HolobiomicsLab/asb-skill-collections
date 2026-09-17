---
name: performance-metric-comparison-across-backends
description: Use when when you have access to a set of gallery or benchmark scripts
  executed across multiple plotting backends and need to quantify which backend delivers
  the fastest median execution time for specific mass spectrometry plot types (chromatogram,
  mobilogram, peakmap, peakmap-marginals, spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pandas
  - matplotlib
  - pyOpenMS-Viz
  - Python
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# Performance metric comparison across backends

## Summary

Systematically extract execution-time metrics from gallery scripts, stratify them by plot type and plotting backend (matplotlib, Bokeh, Plotly), compute summary statistics (median, min, max), and rank backends within each plot category to identify fastest and slowest implementations. This skill enables practitioners to make informed backend selection decisions for mass spectrometry visualization workloads.

## When to use

When you have access to a set of gallery or benchmark scripts executed across multiple plotting backends and need to quantify which backend delivers the fastest median execution time for specific mass spectrometry plot types (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots). Use this skill when the article or documentation reports computation times in a table or appendix and you want to compare backend performance objectively rather than relying on anecdotal impressions.

## When NOT to use

- The article or documentation contains no execution-time measurements or computation-times table; backend performance cannot be assessed from missing data.
- Execution times are reported only as aggregate or global figures (e.g., 'total library load time') rather than per-script or per-plot-type granularity; stratified comparison is impossible.
- The goal is to optimize absolute runtime performance; this skill compares backends but does not recommend code optimizations or algorithmic improvements within a backend.

## Inputs

- Computation-times table or appendix with script execution times (seconds or milliseconds) and associated metadata (script name, plot type, backend)
- Mapping or metadata linking each script to its plot type category (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend identifier

## Outputs

- Structured summary table (pandas DataFrame or CSV) with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category
- Comparative visualization (bar chart or heatmap) showing median execution times across backends for each plot type
- Ranked backend list per plot type, indicating fastest and slowest performer

## How to apply

First, extract all reported execution times from the computation-times table in the methods section, assigning each script to its plot type category and backend (ms_bokeh, ms_matplotlib, ms_plotly). Use pandas to organize these as a structured DataFrame with columns for plot_type, backend, and execution_time. Second, group by plot_type and backend, computing median, minimum, and maximum execution times for each combination. Third, rank backends within each plot category by median time (ascending), identifying the fastest and slowest for that plot type. Fourth, construct a summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. Finally, generate a comparative visualization—such as a grouped bar chart or heatmap—showing median times across backends per plot type, making performance differences visually apparent for stakeholder communication.

## Related tools

- **pandas** (DataFrame manipulation, grouping, and aggregation of execution-time data by plot type and backend)
- **matplotlib** (Static visualization of median execution times as bar charts or heatmaps for comparative display)
- **pyOpenMS-Viz** (Source of the gallery scripts and plot types (chromatogram, mobilogram, peakmap, spectrum, subplots) whose execution times are being compared) — https://github.com/OpenMS/pyopenms_viz
- **Python** (Scripting environment for data extraction, aggregation, and visualization pipeline)

## Examples

```
import pandas as pd; times_df = pd.read_csv('computation_times.csv'); summary = times_df.groupby(['plot_type', 'backend'])['execution_time'].agg(['median', 'min', 'max']).reset_index(); summary['rank'] = summary.groupby('plot_type')['median'].rank(); print(summary.sort_values(['plot_type', 'median']))
```

## Evaluation signals

- Each plot_type category has exactly three backend entries (ms_matplotlib, ms_bokeh, ms_plotly) with non-null median_time, min_time, and max_time values.
- Median execution times are monotonically non-negative and min_time ≤ median_time ≤ max_time for each row (invariant: no inverted ranges).
- Rank values within each plot_type are contiguous integers from 1 to 3 (no gaps or duplicates), and rank=1 corresponds to the lowest median_time for that plot type.
- Visualization clearly displays median times on a consistent scale across all plot types, with backends grouped or colored distinctly to enable visual comparison.
- Summary table and visualization agree: the backend marked rank=1 in the table is visually shortest in the chart for each plot_type.

## Limitations

- The article provides no reported timing metrics or execution time data for any plot types across the three backends, making backend performance comparison impossible from the available text.
- Execution-time measurements depend on hardware (CPU, memory, I/O speed), runtime environment (Python version, library versions), and data size; results may not generalize to other setups or larger datasets.
- Median execution time alone does not capture variability or outliers; practitioners should also inspect min/max range and consider variance or percentiles (e.g., p95) for stability assessment.

## Evidence

- [other] Which plotting backend (matplotlib, Bokeh, or Plotly) exhibits the fastest median execution time for each mass spectrometry plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots)?: "Which plotting backend (matplotlib, Bokeh, or Plotly) exhibits the fastest median execution time for each mass spectrometry plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [other] Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend (ms_bokeh, ms_matplotlib, ms_plotly).: "Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [other] Compute median execution time for each plot-type and backend combination. Compute min and max execution times (range) for each plot-type and backend combination.: "Compute median execution time for each plot-type and backend combination. Compute min and max execution times (range) for each plot-type and backend combination."
- [other] Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category.: "Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category."
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
