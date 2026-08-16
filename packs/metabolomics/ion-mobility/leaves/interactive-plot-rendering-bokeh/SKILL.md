---
name: interactive-plot-rendering-bokeh
description: Use when when you have mass spectrometry data in a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity, and you want to generate interactive (rather than static) visualizations for exploratory analysis, interactive drill-down, or deployment in web applications or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-viz
  - bokeh
  - Python
  - Pandas
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
- These examples are generated if `backend='ms_bokheh'
- Multiple backends supported including matplotlib, bokeh, and plotly
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

# interactive-plot-rendering-bokeh

## Summary

Render interactive mass spectrometry visualizations (chromatograms, spectra, peak maps) using the Bokeh backend through pyOpenMS-viz's Pandas DataFrame plotting API. This skill enables generation of web-ready, interactive plots suitable for exploratory analysis and interactive inspection of m/z, retention time, and intensity dimensions.

## When to use

When you have mass spectrometry data in a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity, and you want to generate interactive (rather than static) visualizations for exploratory analysis, interactive drill-down, or deployment in web applications or Jupyter notebooks.

## When NOT to use

- Input data is not in Pandas DataFrame format — use data loading/ingestion skill first
- You require 3D peak map visualization with true 3D rotation — use plotly backend instead (Bokeh does not support 3D peak maps per the supported plots table)
- You need static, publication-quality raster output — use matplotlib backend instead

## Inputs

- Pandas DataFrame with m/z and intensity columns (1D spectrum)
- Pandas DataFrame with retention time and intensity columns (1D chromatogram)
- Pandas DataFrame with m/z, retention time, and intensity columns (2D peak map)
- Pandas DataFrame with ion mobility and intensity columns (1D mobilogram)

## Outputs

- Interactive Bokeh plot object (peakmap, spectrum, chromatogram, or mobilogram)
- Renderable HTML-backed visualization with pan/zoom/hover interactivity
- Optional marginal plots (chromatogram/spectrum subplots)

## How to apply

Load mass spectrometry data into a Pandas DataFrame with required columns (x: m/z or retention time, y: intensity, z: intensity for 2D peak maps). Install pyOpenMS-viz via pip. Call df.plot(x='column_name', y='column_name', kind='peakmap'|'spectrum'|'chromatogram'|'mobilogram', backend='ms_bokeh') to render an interactive Bokeh plot. Optionally set add_marginals=True to display marginal chromatograms and spectra alongside the main plot. The Bokeh backend automatically provides interactive features including pan, zoom, hover tooltips, and save capabilities without additional configuration.

## Related tools

- **pyOpenMS-viz** (Core library providing the DataFrame.plot() extension method and Bokeh backend integration for mass spectrometry visualization) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data container (DataFrame) and plotting API entry point)
- **bokeh** (Underlying interactive visualization library generating HTML/JavaScript plots with pan/zoom/hover capabilities)
- **Python** (Execution environment for pyOpenMS-viz and Pandas)

## Examples

```
ms_data.plot(x='m/z', y='retention_time', z='intensity', kind='peakmap', backend='ms_bokeh', add_marginals=True)
```

## Evaluation signals

- Bokeh plot object is generated without errors and is displayable in Jupyter notebooks or web applications
- Interactive controls (pan, zoom, hover tooltip showing m/z, retention time, intensity) respond correctly to user input
- When add_marginals=True is set, marginal plots (chromatogram and spectrum) render alongside the main peakmap plot
- Plot dimensions and axis labels match the input DataFrame columns (x, y, z as specified)
- For 2D peak maps, heatmap intensities scale correctly across the m/z × retention time grid

## Limitations

- Bokeh backend does not support 3D peak map visualization; use plotly backend for 3D rotation capability
- Performance may degrade with very large DataFrames (millions of points); consider downsampling or aggregating before rendering
- Marginal plots (add_marginals=True) are currently available for peakmap plots; support may vary for other plot kinds

## Evidence

- [other] Integration capability: "Multiple backends supported including matplotlib, bokeh, and plotly"
- [readme] Plot types supported: "PeakMap 2D | x, y, z | peakmap | ✓ | ✓ | ✓"
- [readme] DataFrame-centric API: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [readme] Bokeh interactivity: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Use cases: "Suitable for use in scripts, Jupyter notebooks, and web applications"
- [other] Workflow from source card: "Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh'"
