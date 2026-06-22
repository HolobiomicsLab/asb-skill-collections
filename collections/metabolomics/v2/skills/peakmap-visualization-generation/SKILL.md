---
name: peakmap-visualization-generation
description: Use when you have mass spectrometry data loaded into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity, and you need to visualize the complete 2D peak map landscape to identify co-eluting features, assess data quality, or explore retention time and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - Pandas
  - matplotlib
  - bokeh
  techniques:
  - ion-mobility-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peakmap-visualization-generation

## Summary

Generate interactive or static 2D and 3D peak map visualizations of mass spectrometry data from Pandas DataFrames using pyOpenMS-viz with multiple plotting backends. This skill enables researchers to render retention time (or ion mobility) versus m/z intensity maps, with optional marginal chromatograms and spectra.

## When to use

Use this skill when you have mass spectrometry data loaded into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity, and you need to visualize the complete 2D peak map landscape to identify co-eluting features, assess data quality, or explore retention time and mass-to-charge patterns interactively across multiple backends (matplotlib for static output, bokeh or plotly for interactive exploration).

## When NOT to use

- Input data is not a Pandas DataFrame or lacks required m/z, retention time, and intensity columns.
- You need to visualize only 1D data (single spectrum or chromatogram); use spectrum or chromatogram plot kinds instead.
- You require 3D visualization using the bokeh backend; bokeh does not support the plot3d=True parameter for peak maps.

## Inputs

- Pandas DataFrame with columns for m/z (x-axis)
- Pandas DataFrame with columns for retention time or ion mobility (y-axis)
- Pandas DataFrame with columns for intensity (z-axis, color scale)

## Outputs

- 2D peak map plot (matplotlib, bokeh, or plotly object)
- 3D peak map plot (matplotlib or plotly object, with plot3d=True)
- Interactive peak map with optional marginal chromatogram and spectrum plots

## How to apply

Load mass spectrometry data into a Pandas DataFrame with m/z, retention time (or ion mobility), and intensity columns. Set the Pandas plotting backend to the desired backend ('ms_matplotlib', 'ms_bokeh', or 'ms_plotly') using pd.set_option(). Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend parameter matching your chosen backend. Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra alongside the main 2D peak map. For 3D visualization, add plot3d=True (supported in matplotlib and plotly but not bokeh). Render and display the resulting plot object. The consistent API across backends allows seamless switching between static publication-quality plots and interactive web-based visualizations.

## Related tools

- **pyOpenMS-viz** (Primary visualization library providing the peakmap plot kind and multi-backend plotting interface for mass spectrometry data) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data container and manipulation library; DataFrames hold the m/z, retention time, and intensity data passed to the plotting API)
- **matplotlib** (Static plotting backend for generating publication-ready peak map visualizations)
- **bokeh** (Interactive plotting backend for browser-based, web-friendly peak map exploration with hover tooltips and pan/zoom)
- **plotly** (Interactive plotting backend supporting both 2D and 3D peak map visualizations with interactive controls)

## Examples

```
ms_data.plot(x="m/z", y="rt", z="intensity", kind="peakmap", backend="ms_bokeh", add_marginals=True)
```

## Evaluation signals

- Peak map renders without errors and displays m/z on x-axis, retention time (or ion mobility) on y-axis, and intensity encoded as color scale.
- If add_marginals=True is set, verify that marginal chromatogram and spectrum plots appear alongside the main 2D peak map.
- For 3D peak maps (plot3d=True), confirm that the plot is generated in matplotlib or plotly backend and displays as a 3D surface or scatter; verify it is not attempted in bokeh.
- Interactive features (zoom, pan, hover tooltips) function correctly when using bokeh or plotly backends; static image renders cleanly when using matplotlib.
- The plot integrates seamlessly with the Pandas plotting API using the consistent syntax: df.plot(x='m/z', y='rt', kind='peakmap', backend='ms_<backend>', add_marginals=True/False).

## Limitations

- Bokeh backend does not support 3D peak map visualization (plot3d=True parameter is ignored or raises an error).
- The skill requires mass spectrometry data to be pre-loaded and pre-formatted into a Pandas DataFrame; raw mass spectrometry file formats (mzML, mzXML, etc.) must be converted to DataFrame form prior to visualization.
- Performance may degrade with very large DataFrames (millions of data points) when using interactive backends; consider data subsampling or aggregation for real-time exploration.
- Marginal plots (add_marginals=True) require properly aligned retention time and m/z binning; irregular or sparse data may produce uninformative marginal visualizations.

## Evidence

- [other] Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity: "Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity."
- [other] Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh': "Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh'."
- [other] Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra: "Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra."
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
