---
name: backend-performance-benchmarking
description: Use when when you have execution time data for visualization scripts across multiple backends (matplotlib, Bokeh, Plotly) and need to determine which backend offers the fastest median performance for specific mass spectrometry plot types (chromatogram, mobilogram, peakmap, peakmap-marginals.
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

# backend-performance-benchmarking

## Summary

Measure and rank plotting backend execution times across multiple mass spectrometry visualization types to identify performance differences and optimal backend choice per plot category. This skill extracts gallery script timings, stratifies them by plot type and backend, and produces comparative performance metrics.

## When to use

When you have execution time data for visualization scripts across multiple backends (matplotlib, Bokeh, Plotly) and need to determine which backend offers the fastest median performance for specific mass spectrometry plot types (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots). Apply this when choosing a backend for production use or when documenting performance trade-offs between static and interactive visualization.

## When NOT to use

- Input lacks execution time measurements or computation-times data is incomplete / missing for one or more backends
- Plot type classification in input data is ambiguous or does not align with the six supported categories (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots)
- Performance analysis goal is to identify algorithmic bottlenecks within a single backend, rather than comparing backends; use profiling tools instead

## Inputs

- Computation-times table with columns: script_name, plot_type, backend, execution_time_seconds
- Gallery script metadata linking script identifiers to plot types and backend implementations

## Outputs

- Structured performance summary table (plot_type, backend, median_time, min_time, max_time, rank_within_category)
- Backend ranking per plot type (fastest to slowest)
- Comparative visualization (bar chart or heatmap) showing median execution times across backends per plot type

## How to apply

Extract execution times from a computation-times table (or similar source) for all gallery scripts, categorizing each by plot type and backend engine. Use pandas to organize the data into a structured table with plot_type, backend, and execution_time columns. Compute median, minimum, and maximum execution time for each plot-type–backend pair. Rank backends within each plot category by median execution time (lowest = best). Generate a summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. Produce a comparative visualization (bar chart or heatmap) showing median times across backends grouped by plot type to enable side-by-side performance inspection.

## Related tools

- **pandas** (Data organization and aggregation: groupby, median, and min/max calculations on execution times by plot_type and backend)
- **matplotlib** (Static comparative visualization (bar charts, heatmaps) of median execution times across backends per plot type)
- **pyOpenMS-Viz** (Source of gallery scripts and plot type definitions (chromatogram, mobilogram, peakmap, spectrum, etc.)) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
import pandas as pd
df = pd.read_csv('computation_times.csv')
medians = df.groupby(['plot_type', 'backend'])['execution_time_seconds'].agg(['median', 'min', 'max'])
medians['rank'] = medians.groupby('plot_type')['median'].rank()
print(medians)
```

## Evaluation signals

- All 19 gallery scripts are categorized into exactly 6 plot types; no script is missing or uncategorized
- Median execution time is computed from ≥1 observation per plot-type–backend pair; single-observation pairs are flagged or excluded
- Rank values within each plot type are contiguous integers (1, 2, 3) with no ties (use tiebreaker or explicit tie notation if needed)
- Bar chart or heatmap visually distinguishes backends (e.g., by color or position) and permits direct median-time comparison within each plot category
- Summary table includes only observed plot types from the input; no hypothetical or missing plot types are invented

## Limitations

- The provided article text does not report actual execution time metrics or a computation-times table; benchmark data must be extracted from an external methods section or supplementary materials not included in the source cards
- Backend performance depends on hardware, Python version, and dependency versions (especially for Bokeh and Plotly rendering); results are not portable across environments without re-measurement
- Median execution time alone does not capture outliers, variance, or failure modes; consider reporting quartiles, standard deviation, or timeout events if present
- Interactive backends (Bokeh, Plotly) may include rendering time in the client; reported timings reflect only script execution and plot object generation, not final display time

## Evidence

- [methods] Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend (ms_bokeh, ms_matplotlib, ms_plotly).: "Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [methods] Compute median execution time for each plot-type and backend combination. Compute min and max execution times (range) for each plot-type and backend combination. Rank backends by median execution time within each plot category to identify fastest and slowest.: "Compute median execution time for each plot-type and backend combination. Compute min and max execution times (range) for each plot-type and backend combination. Rank backends by median execution"
- [methods] Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. Produce a comparative visualization (bar chart or heatmap) showing median times across backends per plot type.: "Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. Produce a comparative visualization (bar chart or heatmap) showing median"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
