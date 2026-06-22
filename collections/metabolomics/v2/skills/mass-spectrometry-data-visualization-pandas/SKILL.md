---
name: mass-spectrometry-data-visualization-pandas
description: Use when when you have mass spectrometry data (mzML, Bruker .d, or CSV) loaded into a Pandas DataFrame with columns for m/z, retention time, ion mobility, or intensity values, and you need to render spectrum plots, chromatograms, mobilograms, or 2D peak maps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Pandas
  - AlphaTims
  - pyOpenMS-Viz
  - matplotlib
  - Bokeh
  - Plotly
  - pymzml
  - pyOpenMS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- leverages the power of Pandas for data manipulation and representation
- ms_data = pd.read_csv("path/to/ms_data.csv")
- '.d -- .. toctree:: :maxdepth: 1 alphatims'
- alphatims
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
---

# mass-spectrometry-data-visualization-pandas

## Summary

Visualize mass spectrometry data (spectra, chromatograms, mobilograms, peak maps) directly from Pandas DataFrames using pyOpenMS-Viz with support for multiple plotting backends (matplotlib, Bokeh, Plotly). This skill enables rapid prototyping and publication-ready rendering of 1D and 2D MS data across static and interactive output formats.

## When to use

When you have mass spectrometry data (mzML, Bruker .d, or CSV) loaded into a Pandas DataFrame with columns for m/z, retention time, ion mobility, or intensity values, and you need to render spectrum plots, chromatograms, mobilograms, or 2D peak maps. Use this skill when you need to switch between static (matplotlib) and interactive (Bokeh, Plotly) backends, or when you want a consistent Pandas-native plotting API without learning multiple visualization libraries.

## When NOT to use

- Input is not tabular or cannot be represented in a Pandas DataFrame (e.g., raw binary spectral data without parsing)
- You require real-time streaming visualization of live instrument data (pyOpenMS-Viz is designed for static/offline data)
- You need custom plot types not supported by the four core MS plot components (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot)

## Inputs

- Pandas DataFrame with MS data columns (m/z, intensity, retention time, ion mobility)
- mzML files (via pymzml or pyOpenMS)
- Bruker .d format files (via AlphaTims)
- CSV files containing parsed MS data

## Outputs

- Static matplotlib figure files (.png, .pdf, .svg)
- Interactive Bokeh HTML widgets and JSON representations
- Interactive Plotly HTML figures with hover tooltips and zooming
- Rendered spectrum plots, chromatogram plots, mobilogram plots, and 2D/3D peak map plots

## How to apply

Load MS data into a Pandas DataFrame with appropriate column names (e.g., m/z, intensity, retention time, ion mobility). Call the DataFrame `.plot()` method, specifying the x, y (and optionally z for peakmap) column names, set the `kind` parameter to one of: 'spectrum', 'chromatogram', 'mobilogram', or 'peakmap', and set the `backend` to 'ms_matplotlib', 'ms_bokeh', or 'ms_plotly'. For spectrum plots, use m/z on x-axis and intensity on y-axis with SpectrumConfig parameters. For chromatogram/mobilogram plots, use retention time or ion mobility on x-axis and intensity on y-axis, optionally using the `by` parameter to separate multiple mass traces. For peakmap plots, use m/z on x-axis, retention time on y-axis, and intensity on z-axis (or color channel), optionally enabling `add_marginals` and `plot_3d` with PeakMapConfig parameters. Verify output by comparing generated figure file formats and visual structure against reference gallery examples from the pyOpenMS-Viz repository.

## Related tools

- **pyOpenMS-Viz** (Primary visualization library providing Pandas DataFrame plotting interface for MS data) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data structure (DataFrame) that holds MS data and provides .plot() method extension)
- **matplotlib** (Backend for static figure rendering via ms_matplotlib backend parameter)
- **Bokeh** (Backend for interactive HTML widget rendering via ms_bokeh backend parameter)
- **Plotly** (Backend for interactive 3D and 2D figure rendering via ms_plotly backend parameter)
- **pymzml** (Optional upstream tool for parsing mzML files into Pandas DataFrames)
- **pyOpenMS** (Optional upstream tool for parsing mzML and MS data into Pandas DataFrames)
- **AlphaTims** (Optional upstream tool for parsing Bruker .d format files into Pandas DataFrames)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_matplotlib")
```

## Evaluation signals

- Generated figure files exist and match expected format (PNG/PDF/SVG for matplotlib, HTML for Bokeh/Plotly)
- Visual output structure is consistent with reference gallery outputs (gallery_scripts/ms_matplotlib/, ms_bokeh/, ms_plotly/)
- For spectrum plots: x-axis displays m/z range, y-axis displays intensity values with correct scale
- For chromatogram/mobilogram plots: x-axis displays retention time or ion mobility, y-axis shows intensity, optional mass traces are visually separated
- For peakmap plots: x-axis shows m/z, y-axis shows retention time, color intensity or z-axis represents signal intensity; optional 3D rendering renders correctly in Plotly backend only
- Interactive backends (Bokeh, Plotly) enable zoom, pan, and hover tooltips; static matplotlib output is non-interactive

## Limitations

- PeakMap 3D plots are only supported in matplotlib and Plotly backends, not in Bokeh
- The library requires data to be pre-loaded into a Pandas DataFrame with correctly named columns; it does not perform peak detection or data preprocessing
- Backend rendering performance may degrade with very large datasets (millions of data points); downsampling or filtering before visualization may be necessary
- Consistent API across backends means some advanced backend-specific features (e.g., WebGL rendering in Plotly) may not be exposed through the unified interface

## Evidence

- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
- [other] For each of the four plot kinds (spectrum, chromatogram, mobilogram, peakmap), call the DataFrame .plot() method with the appropriate x, y (and z for peakmap) column names, set kind parameter to the plot type, and set backend to ms_matplotlib, ms_bokeh, or ms_plotly sequentially.: "For each of the four plot kinds (spectrum, chromatogram, mobilogram, peakmap), call the DataFrame .plot() method with the appropriate x, y (and z for peakmap) column names, set kind parameter to the"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [other] Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame.: "Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame."
- [readme] PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓"
