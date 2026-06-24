---
name: spectrum-chromatogram-mobilogram-rendering
description: Use when you have mass spectrometry data in a Pandas DataFrame with columns
  for m/z and intensity (spectrum), retention time and intensity (chromatogram), or
  drift time and intensity (mobilogram), and need to render 1D traces as static or
  interactive plots for exploratory analysis, quality control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-viz
  - plotly
  - Python
  - matplotlib
  - bokeh
  - Pandas
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from
  pandas dataframes
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-chromatogram-mobilogram-rendering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Render 1D mass spectrometry data (spectra, chromatograms, mobilograms) as static or interactive visualizations by plotting Pandas DataFrames with pyOpenMS-viz against x, y column dimensions. This skill bridges raw MS tabular data to publication-ready plots across matplotlib, bokeh, and plotly backends.

## When to use

You have mass spectrometry data in a Pandas DataFrame with columns for m/z and intensity (spectrum), retention time and intensity (chromatogram), or drift time and intensity (mobilogram), and need to render 1D traces as static or interactive plots for exploratory analysis, quality control, or publication.

## When NOT to use

- Input data is 2D or 3D (x, y, z required for peakmap); use peakmap plot type instead.
- You need to overlay multiple traces or perform complex layering; use low-level backend API directly.
- Input is not a Pandas DataFrame or columns are non-numeric or contain missing values without prior imputation.

## Inputs

- Pandas DataFrame with numeric x column (m/z, retention_time, or drift_time) and numeric y column (intensity)
- string specifying plot kind: 'spectrum', 'chromatogram', or 'mobilogram'
- string specifying column names for x and y axes

## Outputs

- matplotlib Figure object or bokeh/plotly interactive plot widget
- rendered visualization displayable in Jupyter, web app, or saved to static file (PNG, SVG, HTML)

## How to apply

Load your mass spectrometry data into a Pandas DataFrame with appropriate x (m/z, rt, or drift time) and y (intensity) columns. Call the .plot() method on the DataFrame with kind='spectrum' (for m/z vs. intensity), 'chromatogram' (for rt vs. intensity), or 'mobilogram' (for drift time vs. intensity), specifying the x and y column names. pyOpenMS-viz automatically dispatches to the configured backend (matplotlib for static output, bokeh or plotly for interactive). Choose your backend based on output context: matplotlib for static publication figures, bokeh or plotly for interactive Jupyter notebooks or web dashboards. Verify that all x and y values are numeric and contain no NaN across the target columns before plotting.

## Related tools

- **pyOpenMS-viz** (core plotting library; provides .plot() method on Pandas DataFrames for rendering spectrum, chromatogram, and mobilogram traces) — https://github.com/OpenMS/pyopenms_viz
- **matplotlib** (static rendering backend; produces publication-quality static PNG/SVG/PDF figures)
- **bokeh** (interactive rendering backend; produces interactive HTML widgets with pan, zoom, hover tools)
- **plotly** (interactive rendering backend; produces interactive HTML traces with zoom, selection, and export controls)
- **Pandas** (DataFrame container and column selection; holds x and y data and provides .plot() API)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum")
```

## Evaluation signals

- Plot renders without error and displays on screen or in Jupyter output cell.
- x-axis and y-axis labels match the specified column names and data range.
- All data points from the input DataFrame are visible in the trace (no silent truncation or filtering).
- Backend-specific interactivity works as expected (matplotlib: no interactivity; bokeh/plotly: zoom, pan, hover tooltips functional).
- Output file size and format match expected backend (matplotlib: small PNG/SVG; bokeh/plotly: larger HTML with embedded JS).

## Limitations

- 1D only; does not handle 2D peakmap or 3D peakmap data types (require z dimension).
- Requires well-formed Pandas DataFrame with no NaN in x or y columns; pre-filtering or imputation needed for sparse or incomplete data.
- Interactive backends (bokeh, plotly) produce larger output files and require browser or Jupyter kernel; matplotlib static output is lightweight but non-interactive.
- Column naming must be exact; no fuzzy matching or automatic detection of m/z, rt, intensity columns.

## Evidence

- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
- [readme] Chromatogram, Mobilogram, Spectrum with x, y required dimensions supported across Matplotlib, Bokeh, and Plotly: "| **Plot Type**   | **Required Dimensions** | **pyopenms_viz Name**                                     | **Matplotlib** | **Bokeh** | **Plotly** |
|-----------------|-------------------------|-------"
