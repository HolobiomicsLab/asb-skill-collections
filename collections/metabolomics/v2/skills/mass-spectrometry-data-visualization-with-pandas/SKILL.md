---
name: mass-spectrometry-data-visualization-with-pandas
description: Use when your input is a Pandas DataFrame containing mass spectrometry measurements (m/z and intensity columns for spectra, retention time and intensity for chromatograms, or x, y, z for 2D/3D peak maps) and you need to generate static plots (matplotlib) or interactive web-based visualizations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-viz
  - plotly
  - Python
  - pandas
  - Pandas
  - matplotlib
  - bokeh
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
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

# mass-spectrometry-data-visualization-with-pandas

## Summary

Create static or interactive visualizations of mass spectrometry data (chromatograms, spectra, peak maps) by extending Pandas DataFrame plotting capabilities with pyOpenMS-viz, which provides a unified API across matplotlib, bokeh, and plotly backends. Use this skill when raw or processed MS data is already loaded into a Pandas DataFrame and requires visual exploration or publication-quality figures across multiple output formats.

## When to use

Your input is a Pandas DataFrame containing mass spectrometry measurements (m/z and intensity columns for spectra, retention time and intensity for chromatograms, or x, y, z for 2D/3D peak maps) and you need to generate static plots (matplotlib) or interactive web-based visualizations (bokeh, plotly) without rewriting plotting code for each backend.

## When NOT to use

- Input MS data is not yet loaded into a Pandas DataFrame or lacks required column names (m/z, intensity, rt, etc.); use data import and preprocessing steps first.
- You need custom statistical overlays (e.g., confidence bands, regression lines) beyond the core MS visualization types supported by pyOpenMS-viz.
- Data is too large to fit in memory as a single Pandas DataFrame; consider filtering or chunking before calling `.plot()`.

## Inputs

- Pandas DataFrame with MS measurements (columns: m/z, intensity for spectra; rt, intensity for chromatograms; x, y, z for 2D/3D peak maps)
- Backend choice (matplotlib, bokeh, or plotly)
- Column names mapping (x_col, y_col, z_col as applicable)

## Outputs

- Static image file or interactive web plot (matplotlib.figure.Figure, bokeh.plotting.figure, or plotly.graph_objects.Figure)
- Rendered visualization in Jupyter notebook or exported as HTML/PNG/SVG

## How to apply

First, ensure your MS data is loaded as a Pandas DataFrame with columns matching the required dimensions (x, y for 1D plots; x, y, z for 2D peak maps). Install pyOpenMS-viz in a conda environment with Python 3.12 and call the `.plot()` method directly on the DataFrame, specifying the column names and plot kind (e.g., `kind="spectrum"`, `kind="chromatogram"`, or `kind="peakmap"`). Select the backend via the backend parameter to choose between matplotlib (static, suitable for publication) or bokeh/plotly (interactive, suitable for notebooks and web apps). The library handles backend-specific rendering internally, allowing consistent code across different output formats. Verify successful execution by checking that the returned plot object renders without errors and that the axes labels and data ranges match the input DataFrame columns.

## Related tools

- **pyOpenMS-viz** (Core library providing the unified `.plot()` API and backend abstraction for Pandas DataFrames) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data container and manipulation framework; MS data must be structured as a DataFrame)
- **matplotlib** (Backend for static, publication-quality MS visualizations)
- **bokeh** (Backend for interactive web-based MS visualizations with hover tooltips and zoom)
- **plotly** (Backend for interactive 3D peak maps and web-embeddable MS visualizations)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="matplotlib")
```

## Evaluation signals

- Plot renders without errors and displays all expected data points from the input DataFrame.
- Axis labels and column ranges match the specified x, y, (z) column names and their min/max values.
- Backend-specific features work as expected (e.g., matplotlib returns a Figure object; bokeh/plotly support interactivity).
- Plot type (spectrum, chromatogram, peakmap, mobilogram) correctly represents the dimensionality of the input data.
- Switching the backend parameter between matplotlib, bokeh, and plotly produces consistent visualizations with the same data ranges and labels.

## Limitations

- pyOpenMS-viz requires input data to be pre-formatted as a Pandas DataFrame with explicitly named columns; it does not perform raw MS file parsing (e.g., mzML, mzXML); use pyOpenMS or MSdata loaders first.
- 3D peak maps are supported only in matplotlib and plotly, not bokeh.
- The library is designed for single-plot visualization; complex multi-panel or faceted layouts require manual composition outside pyOpenMS-viz.

## Evidence

- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [other] Plot directly from a pandas dataframe object: "Plot directly from a pandas dataframe object"
