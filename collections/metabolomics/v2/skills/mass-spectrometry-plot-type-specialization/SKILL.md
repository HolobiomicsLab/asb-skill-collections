---
name: mass-spectrometry-plot-type-specialization
description: Use when you have a Pandas DataFrame containing mass spectrometry data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-Viz
  - Pandas
  - Matplotlib
  - Bokeh
  - Plotly
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-plot-type-specialization

## Summary

Select and configure the appropriate visualization type (chromatogram, spectrum, mobilogram, or peakmap) based on the dimensionality and nature of mass spectrometry data, then dispatch it through pyOpenMS-viz's layered architecture to the chosen plotting backend. This skill ensures that the data's inherent structure (1D retention time × intensity, 2D m/z × intensity, or 3D m/z × retention time × intensity) is matched to a plot kind that faithfully represents it.

## When to use

You have a Pandas DataFrame containing mass spectrometry data (e.g., chromatogram, spectrum, mobilogram, or peak map) and need to decide which plot type (kind) to invoke and which backend (matplotlib for static output, bokeh or plotly for interactive exploration) to route the visualization request through. Use this skill when the data's dimensionality and analytical goal—e.g., visualizing intensity over retention time for a 1D chromatogram, or m/z × retention time intensity contours for a 2D peakmap—must drive the choice of plot kind and backend specialization.

## When NOT to use

- Data is already a pre-rendered image or bitmap; use this skill only when the input is a structured DataFrame with numerical columns.
- The data dimensionality does not match any supported plot kind (e.g., 4+ independent dimensions with no aggregation path to 1D, 2D, or 3D).
- Real-time streaming data that requires live update patterns; pyOpenMS-viz is designed for static or user-requested plotting on complete datasets in memory.

## Inputs

- Pandas DataFrame with mass spectrometry data (e.g., columns: m/z, intensity, retention time, or mobility)
- plot() method parameters: kind (string: 'chromatogram', 'spectrum', 'mobilogram', or 'peakmap'), backend (string: 'ms_matplotlib', 'ms_bokeh', or 'ms_plotly'), x (column name), y (column name), z (column name, optional for peakmap)

## Outputs

- Rendered visualization object (matplotlib Figure, Bokeh plot, or Plotly figure) displayed or saved according to backend capabilities
- Interactive or static plot suitable for inspection, publication, or further interactive exploration

## How to apply

Inspect the input DataFrame's column structure to determine dimensionality: if it has x and y columns, choose a 1D plot kind (chromatogram, mobilogram, or spectrum); if it has x, y, and z columns, select peakmap (and decide whether plot3d=True is needed for 3D rendering). For each plot kind, pyOpenMS-viz instantiates a configuration object (e.g., SpectrumConfig, ChromatogramConfig) in the Configuration Classes Layer that validates parameters like axis labels and styling. The orchestrator then inspects the backend parameter (ms_matplotlib, ms_bokeh, or ms_plotly) and routes the configuration to the appropriate Extension Layer, which inherits from both the core base class (BasePlot or BaseMSPlot) and a backend-specific mixin. The backend's rendering engine is selected based on whether static (matplotlib) or interactive (bokeh, plotly) output is desired. Finally, invoke .plot() on the DataFrame with the selected kind, backend, and axis parameters, allowing the architecture to dispatch to the correct implementation.

## Related tools

- **pyOpenMS-Viz** (Primary visualization dispatch and rendering framework; orchestrates routing of plot requests from Configuration and Core Base layers to backend-specific Extension layers) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Input data container and DataFrame interface for mass spectrometry data; provides the .plot() method entry point)
- **Matplotlib** (Backend for static visualization; renders static images of chromatograms, spectra, mobilograms, and 2D/3D peakmaps via MATPLOTLIBSpectrumPlot and related classes)
- **Bokeh** (Backend for interactive visualization; renders interactive HTML plots of chromatograms, spectra, mobilograms, and 2D peakmaps via BOKEHSpectrumPlot and related classes)
- **Plotly** (Backend for interactive visualization; renders interactive 3D and 2D plots of chromatograms, spectra, mobilograms, and peakmaps (including 3D) via PLOTLYSpectrumPlot and related classes)

## Examples

```
import pandas as pd
ms_data = pd.read_csv('ms_spectrum.csv')
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_bokeh')
```

## Evaluation signals

- The correct plot kind is instantiated: inspect the returned object's class name (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot) to confirm it matches the intended kind and backend.
- Configuration validation succeeds: the configuration object (e.g., SpectrumConfig) accepts the provided x, y, z column names and backend parameter without raising validation errors.
- Backend-specific rendering occurs: for Bokeh/Plotly, the plot is interactive (supports pan, zoom, hover); for Matplotlib, it is a static image that can be saved as .png or .pdf.
- Dimensionality mismatch detection: attempting to call .plot(kind='spectrum', ...) on data without required x and y columns, or kind='peakmap' without z, should raise a clear configuration error before rendering.
- Data integrity: the rendered visualization preserves the original DataFrame's data range and order; spot-check axis labels and value ranges against the input DataFrame.

## Limitations

- Peakmap 3D visualization is supported only in Matplotlib and Plotly; Bokeh does not render 3D plots (returning to 2D or raising an informative error).
- Column naming must be consistent across the DataFrame; if column names change or are missing, the configuration layer's validation will reject the request.
- Large datasets (millions of points) may render slowly in interactive backends (Bokeh, Plotly) or fail to fit in memory; no built-in downsampling or binning is mentioned in the article.
- Plot customization beyond x, y, z axis selection and backend choice requires direct access to backend-specific APIs; the unified pyOpenMS-viz interface does not expose all rendering parameters.

## Evidence

- [other] User invokes `.plot()` method on a pandas DataFrame with parameters including `backend='ms_bokeh'` (or `'ms_matplotlib'` or `'ms_plotly'`), `kind='spectrum'` (or other plot type), and axis names.: "User invokes `.plot()` method on a pandas DataFrame with parameters including `backend='ms_bokeh'` (or `'ms_matplotlib'` or `'ms_plotly'`), `kind='spectrum'` (or other plot type), and axis names."
- [other] The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding `MATPLOTLIBSpectrumPlot`), or `_plotly` (yielding `PLOTLYSpectrumPlot`).: "The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓"
