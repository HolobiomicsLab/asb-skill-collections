---
name: rendering-speed-profiling
description: Use when when you have implemented the same visualization (e.g., chromatogram,
  spectrum, peakmap, mobilogram) across multiple plotting backends in pyOpenMS-viz
  and need to determine which backend minimizes rendering latency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - Pandas
  - bokeh
  - matplotlib
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from
  pandas dataframes
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rendering-speed-profiling

## Summary

Measure and compare execution times across multiple plotting backends (matplotlib, bokeh, plotly) to identify which backend renders mass spectrometry visualizations fastest for a given data type and scale. This skill enables evidence-based backend selection for interactive vs. static visualization workflows.

## When to use

When you have implemented the same visualization (e.g., chromatogram, spectrum, peakmap, mobilogram) across multiple plotting backends in pyOpenMS-viz and need to determine which backend minimizes rendering latency. Use this skill if your analysis goal includes backend selection, performance optimization, or documentation of relative throughput for different visualization types.

## When NOT to use

- Input is a single static visualization or proof-of-concept; rendering speed profiling is overhead when backend choice is already determined or immaterial.
- Mass spectrometry data is pre-rendered or cached; execution-time measurement must occur on fresh rendering, not retrieval.
- Only one plotting backend is available or required by downstream infrastructure; comparative profiling requires ≥2 backends to be meaningful.

## Inputs

- Gallery example scripts exercising pyOpenMS-viz plotting API across bokeh, plotly, and matplotlib backends
- Sample mass spectrometry datasets (1D chromatograms, spectra, 2D peak maps, 3D peak maps, mobilograms)
- pyOpenMS-viz DataFrame-based visualization code with explicit backend specification

## Outputs

- Execution-time metrics table (rows: visualization types; columns: backend, render time in ms)
- Speedup ratio summary (e.g., bokeh vs. plotly comparison matrix with factor values)
- Backend recommendation summary by visualization category and interactivity requirement
- Aggregate and per-category rendering time statistics (mean, std dev)

## How to apply

Execute all 19 (or representative subset of) gallery examples that support multiple backends, isolating and recording the wall-clock rendering time for each backend-visualization-type pair. Separate execution times into bokeh, plotly, and matplotlib entries from a computation-times table. For visualization types supported by both interactive backends (bokeh and plotly), compute pairwise time comparisons and calculate the mean speedup ratio (plotly time / bokeh time) to determine consistent performance winners. Aggregate times by visualization category (e.g., 1D chromatogram, 2D peakmap, 3D peakmap) to identify whether backend performance varies with dimensionality or data cardinality. Generate a summary comparison table with rendering times in milliseconds and speedup factors (e.g., 1.2× faster) for each backend–category combination. Use these metrics to recommend backend selection based on interactivity vs. speed trade-offs.

## Related tools

- **pyOpenMS-viz** (Primary visualization API; backend abstraction layer that exposes plotting methods (spectrum, chromatogram, peakmap, mobilogram) with backend parameter for rendering speed measurement.) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data container for mass spectrometry records (m/z, intensity, retention time, mobility); enables consistent input interface across backends.)
- **Python** (Execution environment and timing measurement framework (e.g., timeit, time.perf_counter) for wall-clock profiling.)
- **bokeh** (Interactive backend candidate for rendering performance comparison; generates browser-based visualizations.)
- **plotly** (Interactive backend candidate for rendering performance comparison; generates JavaScript-based visualizations.)
- **matplotlib** (Static backend baseline for rendering performance comparison; generates static raster or vector output.)

## Examples

```
import pandas as pd; import pyopenms_viz; import time; data = pd.DataFrame({'m/z': [100.0, 101.0], 'intensity': [50, 100]}); start = time.perf_counter(); data.plot(x='m/z', y='intensity', kind='spectrum', backend='bokeh'); bokeh_time = time.perf_counter() - start; start = time.perf_counter(); data.plot(x='m/z', y='intensity', kind='spectrum', backend='plotly'); plotly_time = time.perf_counter() - start; print(f'Speedup (plotly/bokeh): {plotly_time/bokeh_time:.2f}x')
```

## Evaluation signals

- Rendering times are reproducible (low coefficient of variation across repeated runs, typically <10% for same backend–visualization pair).
- Speedup ratios for bokeh vs. plotly are consistent within visualization categories (e.g., all 1D visualizations show bokeh 1.1–1.5× faster than plotly).
- All gallery examples complete successfully with timing data recorded; no missing backends for examples that claim support (e.g., no bokeh time for peakmap if README lists peakmap as bokeh-supported).
- Aggregate per-category rendering times scale predictably with data cardinality (e.g., 3D peakmap slower than 2D peakmap when data size is held constant).
- Comparison table is reproducible by an independent user running the same examples in the same environment (Python version, backend library versions, OS).

## Limitations

- Rendering performance is hardware- and OS-dependent; profiling on one system (e.g., Linux + GPU) may not generalize to another (e.g., macOS + CPU). Recommend profiling on target deployment hardware.
- Execution-time measurements include I/O, data serialization, and browser/display latency, not pure algorithmic rendering; backend speedup may be masked by Pandas DataFrame overhead or network latency in remote environments.
- Gallery examples may use different data sizes or complexity; direct time comparison between unmatched examples is invalid. Ensure pairwise comparisons use identical or normalized dataset sizes.
- Interactive backends (bokeh, plotly) incur first-render overhead (JavaScript compilation, browser initialization) not present in matplotlib; single-run profiling may overestimate plotly/bokeh slowness if comparing warm vs. cold caches.
- The article's workflow assumes availability of all three backends; environments with only one or two backends available will produce incomplete comparisons.

## Evidence

- [other] Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries.: "Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries."
- [other] Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram).: "Perform pairwise time comparisons between bokeh and plotly for examples that exist in both backends (e.g., chromatogram, spectrum, peakmap, mobilogram)."
- [other] Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower.: "Compute the mean speedup ratio (plotly time / bokeh time) and verify that bokeh times are consistently lower."
- [readme] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
