---
name: spectrum-plot-generation-mz-intensity
description: Use when you have mass spectrometry spectral data loaded into a Pandas DataFrame with columns representing m/z (mass-to-charge ratio) and intensity values, and you need to visualize the spectrum to inspect peak patterns, identify high-abundance ions, or compare spectral profiles across samples or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - AlphaTims
  - pyOpenMS-Viz
  - Pandas
  - matplotlib
  - Bokeh
  - Plotly
  - pymzml
  - pyOpenMS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- '.d -- .. toctree:: :maxdepth: 1 alphatims'
- alphatims
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
---

# spectrum-plot-generation-mz-intensity

## Summary

Generate static or interactive mass spectrometry spectrum plots with m/z values on the x-axis and intensity on the y-axis using pyOpenMS-Viz's Pandas DataFrame plotting interface. This skill enables rapid visualization of MS spectral data across multiple plotting backends (matplotlib, Bokeh, Plotly) without writing backend-specific code.

## When to use

Use this skill when you have mass spectrometry spectral data loaded into a Pandas DataFrame with columns representing m/z (mass-to-charge ratio) and intensity values, and you need to visualize the spectrum to inspect peak patterns, identify high-abundance ions, or compare spectral profiles across samples or conditions. Apply this skill for exploratory analysis, publication-quality static figures, or interactive web-based spectrum viewers.

## When NOT to use

- Data is already in a non-tabular format (e.g., mzML/raw binary) without prior loading into DataFrame — use pymzml or pyOpenMS to load first.
- You need to visualize 2D relationships (m/z vs. retention time with intensity as color/height) — use peakmap plot instead.
- Input lacks m/z or intensity columns, or columns are named differently — rename or extract relevant columns before plotting.

## Inputs

- Pandas DataFrame with m/z column (float, mass-to-charge values)
- Pandas DataFrame with intensity column (float, abundance values)
- Optional SpectrumConfig object with visualization parameters

## Outputs

- Static spectrum figure (matplotlib format: .png, .pdf, or in-memory axes object)
- Interactive HTML spectrum figure (Bokeh or Plotly format: .html file or embedded widget)

## How to apply

Load your mass spectrometry data (from mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a Pandas DataFrame with at minimum m/z and intensity columns. Call the DataFrame .plot() method with x='m/z', y='intensity', kind='spectrum', and set backend to one of ms_matplotlib, ms_bokeh, or ms_plotly. Apply SpectrumConfig parameters (e.g., title, axis labels, colors) to customize appearance. For multi-backend consistency, use the same column names and configuration objects across backends to enable easy switching between static (matplotlib) and interactive (Bokeh/Plotly) output formats without modifying core plotting logic.

## Related tools

- **pyOpenMS-Viz** (Provides the .plot() method extension for Pandas DataFrames to generate spectrum plots with multi-backend support) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Provides DataFrame structure and the base .plot() interface extended by pyOpenMS-Viz)
- **matplotlib** (Backend for rendering static spectrum plots when backend='ms_matplotlib' is specified)
- **Bokeh** (Backend for rendering interactive spectrum plots when backend='ms_bokeh' is specified)
- **Plotly** (Backend for rendering interactive spectrum plots when backend='ms_plotly' is specified)
- **pymzml** (Tool for loading mzML mass spectrometry files into Python data structures prior to DataFrame construction)
- **pyOpenMS** (Tool for loading and processing mzML files and mass spectrometry data prior to DataFrame construction)
- **AlphaTims** (Tool for loading Bruker .d format mass spectrometry data into Python structures prior to DataFrame construction)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_matplotlib")
```

## Evaluation signals

- Generated figure file exists in expected location and format (.png/.pdf for matplotlib, .html for Bokeh/Plotly)
- X-axis displays m/z values in correct numerical range matching input DataFrame min/max m/z
- Y-axis displays intensity values in correct scale and range matching input DataFrame intensity distribution
- All peaks present in input data are rendered visually without data loss or clipping (unless explicitly configured)
- Figure matches corresponding reference output from gallery (gallery_scripts/ms_matplotlib/, gallery_scripts/ms_bokeh/, or gallery_scripts/ms_plotly/) in terms of structure and labeling

## Limitations

- PeakMap 3D plots are not supported in Bokeh backend (only matplotlib and Plotly support 3D); restrict to 2D spectrum visualization with Bokeh or switch backends for 3D capability.
- Very large spectra (>100,000 peaks) may encounter rendering performance issues with interactive backends (Bokeh/Plotly); consider downsampling or using matplotlib for static output.
- Column names must exactly match expected naming (m/z, intensity) or be explicitly specified; ambiguous or missing columns will cause plot generation to fail.

## Evidence

- [other] For spectrum plots, use m/z on x-axis and intensity on y-axis with SpectrumConfig parameters.: "For spectrum plots, use m/z on x-axis and intensity on y-axis with SpectrumConfig parameters."
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [other] Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame.: "Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame."
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
