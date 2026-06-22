---
name: backend-performance-comparison
description: Use when you have execution-time metrics (from a benchmark table or profiling logs) across multiple visualization backends for the same set of plots (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - bokeh
  - matplotlib
  - Pandas
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

# backend-performance-comparison

## Summary

Systematically compare rendering performance across multiple plotting backends (matplotlib, bokeh, plotly) for mass spectrometry visualizations by extracting execution times from a computation-times table, aggregating them by backend and visualization type, and calculating speedup ratios. This skill identifies which backend delivers faster interactive or static rendering for specific MS data types.

## When to use

You have execution-time metrics (from a benchmark table or profiling logs) across multiple visualization backends for the same set of plots (e.g., chromatogram, spectrum, peakmap, mobilogram) and need to determine which backend renders fastest for your use case, or to quantify performance trade-offs when choosing between static (matplotlib) and interactive (bokeh/plotly) backends for MS data.

## When NOT to use

- No execution-time metrics are available (e.g., only abstract/intro text is provided with no benchmark table or profiling data).
- Comparing backends on fundamentally different datasets or plot types (speedup ratios are only meaningful when the same data and visualization parameters are used across backends).
- Performance comparison is not the research question; e.g., if the goal is to evaluate correctness, visual fidelity, or feature coverage of backends rather than rendering speed.

## Inputs

- computation-times table with execution times for multiple gallery examples
- backend identifier for each row (e.g., 'matplotlib', 'bokeh', 'plotly')
- plot type/category label (e.g., 'chromatogram', 'spectrum', 'peakmap', 'mobilogram')
- execution time value (seconds or milliseconds per render)

## Outputs

- backend comparison summary table with rendering times per plot type
- speedup ratio matrix (e.g., plotly_time / bokeh_time for each plot category)
- aggregate rendering time by backend across all or filtered plot types
- consistency assessment (flagged outliers or plot types with unexpected speedup trends)

## How to apply

Extract execution times from the computation-times table for all gallery examples, separating entries by backend (bokeh, plotly, matplotlib). Aggregate rendering times by backend and by plot category (chromatogram, spectrum, peakmap, mobilogram, etc.). For examples that exist in multiple backends, perform pairwise time comparisons and compute the mean speedup ratio (slower_backend_time / faster_backend_time). Verify consistency of the speedup across plot types; plot categories with extreme outliers should be flagged. Generate a summary table with rendering times (in milliseconds or seconds) and speedup factors. The rationale is that backend choice affects interactivity trade-offs (interactive backends like bokeh and plotly add overhead compared to static matplotlib), so rendering speed must be measured concretely for your data scale and visualization type.

## Related tools

- **pyOpenMS-viz** (visualization library that integrates multiple plotting backends and generates the gallery examples with execution-time metrics) — https://github.com/OpenMS/pyopenms_viz
- **bokeh** (interactive plotting backend whose rendering time is measured and compared against plotly)
- **plotly** (interactive plotting backend whose rendering time is measured and compared against bokeh)
- **matplotlib** (static plotting backend included in performance comparisons as baseline or reference)
- **Pandas** (data manipulation and aggregation tool for extracting, grouping, and summarizing rendering times by backend and plot type)
- **Python** (programming language for automating time extraction, aggregation, and speedup ratio calculation)

## Examples

```
import pandas as pd; times = pd.read_csv('computation_times.csv'); bokeh_times = times[times['backend']=='bokeh'].groupby('plot_type')['time_ms'].mean(); plotly_times = times[times['backend']=='plotly'].groupby('plot_type')['time_ms'].mean(); speedup = plotly_times / bokeh_times; print(speedup)
```

## Evaluation signals

- Speedup ratios are consistent (within a reasonable range, e.g., 0.8–1.5×) across multiple plot types of the same backend pair; large outliers (>2× difference) signal potential measurement noise or data-specific edge cases and should be investigated.
- All 19 gallery examples (or the full set of examples in the computation-times table) are successfully parsed and assigned to a backend and plot-type category; no rows are dropped or misclassified.
- The summary table includes aggregate statistics (mean, median, std) for rendering time per backend, allowing practitioners to make informed backend selection decisions.
- Speedup factors are positive and non-zero; a ratio < 1.0 indicates the numerator backend is faster, and a ratio > 1.0 indicates the denominator backend is faster; verify the labeling matches the intended comparison direction.
- The comparison accounts for plot-type-specific rendering complexity (e.g., 3D peakmaps may show different speedup ratios than 1D spectra); the summary table stratifies results by plot type so users can select the backend appropriate for their specific visualization needs.

## Limitations

- Execution-time metrics depend on hardware (CPU, memory), software versions (bokeh, plotly, matplotlib), and system load; results are not portable across machines or over time without re-benchmarking.
- The article abstract/intro does not report execution-time metrics directly; the workflow requires access to the full computation-times table (likely in results or supplementary material) to proceed; if this table is unavailable, the skill cannot be applied.
- Rendering time alone does not capture other backend trade-offs such as interactivity features, file size, or visual fidelity; backend selection should also consider use case (e.g., static PDF export favors matplotlib, web-based exploration favors bokeh/plotly).
- Gallery examples may not be representative of user data scales; rendering times on smaller or larger MS datasets may differ, so results should be validated on realistic data before deployment.

## Evidence

- [other] Does bokeh render faster than plotly when used as a backend for mass spectrometry visualizations in pyOpenMS-viz?: "Does bokeh render faster than plotly when used as a backend for mass spectrometry visualizations in pyOpenMS-viz?"
- [other] Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries.: "Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries."
- [other] Calculate aggregate and per-category rendering times for bokeh versus plotly backends.: "Calculate aggregate and per-category rendering times for bokeh versus plotly backends."
- [other] Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram).: "Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram)."
- [other] Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower.: "Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
