---
name: execution-time-metric-analysis
description: Use when you have computation-time metrics from a gallery or benchmark suite comparing multiple plotting backends on the same data types (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - Pandas
  - bokeh
  - matplotlib
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz_cq
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00873
  all_source_dois:
  - 10.1021/acs.jproteome.4c00873
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# execution-time-metric-analysis

## Summary

Extract, aggregate, and compare rendering execution times across multiple visualization backends (bokeh, plotly, matplotlib) for mass spectrometry data to quantify performance differences. This skill enables evidence-based backend selection by computing mean speedup ratios and identifying rendering bottlenecks across visualization types.

## When to use

You have computation-time metrics from a gallery or benchmark suite comparing multiple plotting backends on the same data types (e.g., chromatogram, spectrum, peakmap, mobilogram), and you need to determine which backend renders fastest for a given visualization category or to support a performance claim in a research finding.

## When NOT to use

- Execution times are measured on different hardware, operating systems, or Python versions without normalization—comparisons will be confounded.
- Only one backend is present in the data—no pairwise comparison is possible.
- Rendering times include network latency, I/O overhead, or data loading, not just the plotting library's rendering kernel—the metric conflates backend performance with system overhead.

## Inputs

- computation-times table or gallery benchmark results (CSV, TSV, or DataFrame)
- execution time measurements for ≥2 backends across ≥3 visualization types
- metadata mapping visualization type to backend (e.g., 'chromatogram-bokeh', 'spectrum-plotly')

## Outputs

- aggregate rendering times per backend and per visualization category (table)
- pairwise backend comparison table with speedup ratios and absolute time deltas
- mean speedup ratio summary (e.g., bokeh mean time / plotly mean time)
- backend performance ranking by visualization type

## How to apply

First, extract raw execution times from a computation-times table, separating entries by backend (bokeh, plotly, matplotlib) and visualization type. Aggregate times per-category and per-backend using Pandas groupby operations. For visualization types that exist in multiple backends (e.g., chromatogram rendered in both bokeh and plotly), perform pairwise time comparisons. Compute the mean speedup ratio as (slower_backend_time / faster_backend_time) and verify consistency across all shared examples. Generate a summary table with rendering times, speedup factors, and confidence that the faster backend exhibits lower times across the board. Use Python and Pandas for extraction, aggregation, and ratio calculation.

## Related tools

- **Pandas** (Data aggregation, groupby operations, time series manipulation, and summary table generation)
- **Python** (Scripting language for extraction, calculation, and visualization of speedup metrics)
- **bokeh** (Interactive visualization backend whose rendering times are extracted and compared) — https://github.com/OpenMS/pyopenms_viz
- **plotly** (Interactive visualization backend whose rendering times are extracted and compared) — https://github.com/OpenMS/pyopenms_viz
- **matplotlib** (Static visualization backend included in performance comparison for completeness) — https://github.com/OpenMS/pyopenms_viz
- **pyOpenMS-viz** (Visualization library whose gallery examples and execution times are benchmarked) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
import pandas as pd; times = pd.read_csv('gallery_execution_times.csv'); bokeh_times = times[times['backend']=='bokeh'].groupby('plot_type')['time_ms'].mean(); plotly_times = times[times['backend']=='plotly'].groupby('plot_type')['time_ms'].mean(); speedup = plotly_times / bokeh_times; print(speedup)
```

## Evaluation signals

- Execution times are successfully extracted from all 19 gallery examples and correctly partitioned by backend (bokeh, plotly, matplotlib) with no missing or NaN entries.
- Aggregate times per backend and visualization category are computed using Pandas groupby, and sums/means match manual spot-checks on ≥3 categories.
- Pairwise speedup ratios are calculated only for visualization types that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram); examples lacking both backends are excluded from ratio computation.
- Mean speedup ratio is computed as the average of per-category ratios and is >1.0 if the claimed faster backend truly has lower times across all shared types; if any shared type contradicts the claim, the finding is flagged.
- Summary table is generated in a reproducible, tabular format (CSV or markdown) with columns for visualization type, backend, execution time (ms or s), and speedup factor; table is human-readable and can be used to support a published research finding.

## Limitations

- No execution-time metrics comparing bokeh and plotly rendering performance are currently reported in the available abstract/intro/results text of the source article, so the skill must be applied prospectively to new benchmark data.
- Execution times are sensitive to hardware, Python version, and data size; comparisons across different systems or versions are not directly transferable.
- Interactive backends (bokeh, plotly) may have different rendering profiles in static export versus browser display, so metrics must specify the output modality.
- The 19 gallery examples cover only a subset of possible mass spectrometry data types and sizes; speedup ratios may not generalize to other data shapes or scales.

## Evidence

- [other] Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries.: "Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries."
- [other] Calculate aggregate and per-category rendering times for bokeh versus plotly backends.: "Calculate aggregate and per-category rendering times for bokeh versus plotly backends."
- [other] Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram).: "Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram)."
- [other] Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower.: "Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower."
- [other] No execution-time metrics comparing bokeh and plotly rendering performance are reported in the available abstract/intro/results text.: "No execution-time metrics comparing bokeh and plotly rendering performance are reported in the available abstract/intro/results text."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
