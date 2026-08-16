---
name: peakmap-heatmap-rendering-mz-rt
description: Use when when you have mass spectrometry data organized in a Pandas DataFrame
  with m/z values, retention time (RT), and intensity measurements, and you want to
  visualize the joint distribution and correlation of these three dimensions to identify
  peaks, assess separation, and detect patterns across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - AlphaTims
  - pyOpenMS-Viz
  - Pandas
  - matplotlib
  - Bokeh
  - Plotly
  - pymzml
  - pyOpenMS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
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

# peakmap-heatmap-rendering-mz-rt

## Summary

Render 2D and 3D mass spectrometry peak maps as heatmaps with m/z on the x-axis and retention time on the y-axis, using intensity or color intensity as the third dimension. This skill enables visual exploration of chromatographic and spectral separation across multiple plotting backends (matplotlib, Bokeh, Plotly).

## When to use

When you have mass spectrometry data organized in a Pandas DataFrame with m/z values, retention time (RT), and intensity measurements, and you want to visualize the joint distribution and correlation of these three dimensions to identify peaks, assess separation, and detect patterns across the m/z–RT plane. Use this skill specifically when exploring untargeted or data-dependent acquisition (DDA) mass spectrometry experiments where both chromatographic and mass spectral resolution matter.

## When NOT to use

- Data is already a pre-computed image or raster; use this skill only for tabular m/z, RT, intensity triplets.
- You need to visualize individual spectrum or chromatogram slices in isolation rather than the joint 2D distribution.
- Input is a single mass spectrum (no chromatographic dimension); use spectrum plot instead.

## Inputs

- Pandas DataFrame with columns for m/z values, retention time, and intensity
- Mass spectrometry data in mzML, Bruker .d, or CSV format (convertible to DataFrame via pymzml, pyOpenMS, or AlphaTims)

## Outputs

- 2D heatmap image (PNG, SVG, or HTML depending on backend)
- Interactive 2D peakmap plot (Bokeh or Plotly HTML widget)
- 3D surface plot (matplotlib or Plotly 3D visualization)
- Marginal 1D intensity distributions (when add_marginals=True)

## How to apply

Load your mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time, and intensity. Call the DataFrame's .plot() method with kind='peakmap', set x='m/z', y='rt' (or your corresponding column names), and z='intensity' or omit z to use color intensity by default. Specify the backend parameter as 'ms_matplotlib' for static output, 'ms_bokeh' or 'ms_plotly' for interactive plots. Optionally enable add_marginals=True to render 1D intensity distributions along the x and y axes, and plot_3d=True (supported by matplotlib and Plotly) to render a 3D surface. Configure visual parameters via PeakMapConfig, including color maps, intensity thresholds, and axis labels. Verify output by comparing the generated figure file against reference gallery outputs for format consistency and visual structure.

## Related tools

- **pyOpenMS-Viz** (Core library providing peakmap plotting API and multi-backend support (PeakMapPlot class and DataFrame.plot() extension)) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data structure (DataFrame) and method extension point for calling .plot(kind='peakmap'))
- **matplotlib** (Backend for static 2D and 3D peakmap rendering (ms_matplotlib))
- **Bokeh** (Backend for interactive 2D peakmap rendering (ms_bokeh))
- **Plotly** (Backend for interactive 2D and 3D peakmap rendering (ms_plotly))
- **pymzml** (Data loader for mzML mass spectrometry files into tabular format)
- **pyOpenMS** (Data loader for OpenMS-compatible mass spectrometry formats and algorithms)
- **AlphaTims** (Data loader for Bruker .d format mass spectrometry data)

## Examples

```
ms_data.plot(x='m/z', y='rt', z='intensity', kind='peakmap', backend='ms_plotly', add_marginals=True)
```

## Evaluation signals

- Output figure file exists and matches the expected format (PNG/SVG for matplotlib, HTML for Bokeh/Plotly)
- Visual structure matches reference gallery outputs: x-axis labeled with m/z values, y-axis with retention time, color intensity proportional to intensity values
- Marginal plots (when enabled) display correctly as 1D intensity traces along the top and right edges
- 3D surface plot (when enabled) renders without visual artifacts and rotates interactively (Plotly) or displays correctly (matplotlib)
- Axis limits and color scale match input data range and configuration parameters (no clipping or overflow beyond PeakMapConfig thresholds)

## Limitations

- Bokeh backend does not support 3D peakmap rendering; use matplotlib or Plotly for plot_3d=True.
- Performance degrades with very large DataFrames (>1 million rows); data aggregation or m/z binning may be needed for gigantic datasets.
- Interactive backends (Bokeh, Plotly) produce larger file sizes than static matplotlib output.
- Column naming must match x, y, z parameter values exactly; automatic detection of m/z, RT, intensity columns is not performed.

## Evidence

- [other] For peakmap plots, use m/z on x-axis and retention time on y-axis with intensity on z-axis (or color), optionally enabling add_marginals and plot_3d with PeakMapConfig parameters.: "For peakmap plots, use m/z on x-axis and retention time on y-axis with intensity on z-axis (or color), optionally enabling add_marginals and plot_3d with PeakMapConfig parameters."
- [other] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data.: "pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data."
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] PeakMap 2D | x, y, z | peakmap | ✓ | ✓ | ✓ | PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓: "PeakMap 2D | x, y, z | peakmap | ✓ | ✓ | ✓ | PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
