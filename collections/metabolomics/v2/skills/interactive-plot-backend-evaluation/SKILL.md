---
name: interactive-plot-backend-evaluation
description: Use when you have mass spectrometry data (chromatograms, spectra, peak maps, mobilograms) that you want to visualize interactively using pyOpenMS-viz, and you need to select between bokeh and plotly backends based on execution time and feature parity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - bokeh
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
---

# interactive-plot-backend-evaluation

## Summary

Systematically compare rendering performance and feature support across interactive plotting backends (bokeh, plotly) for mass spectrometry visualizations. This skill identifies which backend best balances speed, interactivity, and plot-type coverage for a given visualization workload.

## When to use

You have mass spectrometry data (chromatograms, spectra, peak maps, mobilograms) that you want to visualize interactively using pyOpenMS-viz, and you need to select between bokeh and plotly backends based on execution time and feature parity. Apply this skill when choosing a backend for gallery examples, production dashboards, or batch visualization pipelines where rendering latency matters.

## When NOT to use

- Input is static matplotlib visualizations only; no interactive backends to compare.
- Only one backend is available or supported for your target plot type (e.g., 3D peakmap only works with plotly).
- Execution-time metrics are absent or incomplete; comparison cannot proceed without timing data.

## Inputs

- computation-times benchmark table with backend-specific execution times
- gallery examples list with plot types and backend assignments
- pyOpenMS-viz Supported Plots table (plot type, required dimensions, backend support matrix)

## Outputs

- comparison summary table with rendering times and speedup factors
- per-plot-type performance rankings (bokeh vs plotly)
- backend recommendation (bokeh for speed, plotly for 3D support)

## How to apply

Extract execution times from a computation-times benchmark table, separating bokeh, plotly, and matplotlib entries across all visualization examples (e.g., 19 gallery examples in pyOpenMS-viz). Group timings by plot type (chromatogram, spectrum, peakmap, mobilogram, peakmap 3D) and calculate aggregate rendering times per backend. For plot types supported by both bokeh and plotly, perform pairwise time comparisons and compute the mean speedup ratio (plotly_time / bokeh_time). Cross-reference supported plot types from the pyOpenMS-viz Supported Plots table to verify feature parity. Generate a comparison summary table showing rendering times, speedup factors, and supported dimensions; bokeh is preferred if times are consistently lower and feature coverage is equivalent, plotly if 3D peakmap support is required despite higher latency.

## Related tools

- **pyOpenMS-viz** (Provides multi-backend plotting API for mass spectrometry data; executes visualization with selected backend and yields execution times) — https://github.com/OpenMS/pyopenms_viz
- **bokeh** (Interactive plotting backend; candidate for rendering speed comparison)
- **plotly** (Interactive plotting backend with 3D support; candidate for rendering speed and feature coverage comparison)
- **Pandas** (Data manipulation and storage; input DataFrames to pyOpenMS-viz plotting methods)
- **Python** (Scripting and analysis environment for extracting, aggregating, and computing speedup ratios)

## Evaluation signals

- Computation-times table successfully parsed and split by backend (bokeh, plotly entries isolated).
- Aggregate rendering times per backend show consistent ordering across plot types (e.g., bokeh < plotly for 2D plots).
- Speedup ratio (plotly_time / bokeh_time) is >1.0 if bokeh is faster, confirming faster absolute times.
- Feature coverage matrix matches pyOpenMS-viz Supported Plots table; all claimed supported plot types appear in benchmark.
- Recommendation aligns with data: if bokeh times are consistently lower and cover required plot types, bokeh is recommended; if plotly is required for 3D or feature gaps exist in bokeh, plotly is recommended despite higher latency.

## Limitations

- No execution-time metrics comparing bokeh and plotly are reported in the article abstract, introduction, or results text; benchmark table must be derived from supplementary materials or source code runs.
- Gallery examples may not cover all mass spectrometry data sizes or complexity levels; rendering times on small synthetic datasets may not generalize to production data.
- Backend performance depends on data volume, system resources, and browser/renderer state; reported times are snapshot metrics, not universal guarantees.

## Evidence

- [other] Research question and workflow from task_id=task_004: "Does bokeh render faster than plotly when used as a backend for mass spectrometry visualizations in pyOpenMS-viz?"
- [readme] Supported plot types and backend matrix: "Supported Plots: Chromatogram, Mobilogram, Spectrum, PeakMap 2D, PeakMap 3D with Matplotlib, Bokeh, Plotly support columns."
- [readme] Multi-backend integration design: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [other] Workflow methodology for comparison: "Extract execution times from computation-times table, calculate aggregate and per-category rendering times, perform pairwise comparisons, compute mean speedup ratio."
