---
name: pandas-dataframe-plotting-interface
description: Use when you have mass spectrometry data (retention time, m/z, intensity, or mobility dimensions) already loaded into a Pandas DataFrame and need to produce publication-ready or exploratory visualizations. Use this when you want to leverage Pandas' native .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - pyOpenMS-viz
  - Pandas
  - matplotlib
  - bokeh
  - plotly
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Plot directly from a pandas dataframe object
- provides a simple interface for extending the plotting capabilities of Pandas DataFrames
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
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

# pandas-dataframe-plotting-interface

## Summary

Use pyOpenMS-viz's Pandas plotting backend to generate static or interactive mass spectrometry visualizations (chromatograms, spectra, peak maps) directly from DataFrame objects with flexible backend selection (matplotlib, bokeh, plotly). This skill encapsulates the procedural interface for extending Pandas' native plotting API to handle multi-dimensional MS data without manual matplotlib figure construction.

## When to use

You have mass spectrometry data (retention time, m/z, intensity, or mobility dimensions) already loaded into a Pandas DataFrame and need to produce publication-ready or exploratory visualizations. Use this when you want to leverage Pandas' native .plot() method syntax rather than calling visualization libraries directly, or when you need to switch between static (matplotlib) and interactive (bokeh/plotly) outputs without rewriting plotting code.

## When NOT to use

- Your input is not tabular or not yet in a Pandas DataFrame (use a data loader or parser first).
- You need custom visual annotations or plot aesthetics beyond pyOpenMS-viz's standard templates (consider calling matplotlib/bokeh/plotly directly instead).
- Your DataFrame columns do not align with required dimensions (e.g., missing intensity column, or non-standard column naming); you must reshape or rename columns before calling .plot().

## Inputs

- Pandas DataFrame with mass spectrometry data (columns: retention time, m/z, intensity, or mobility)
- DataFrame column names matching visualization dimensions (e.g., 'rt', 'intensity', 'm/z')
- Optional: backend selection parameter (matplotlib, bokeh, or plotly)

## Outputs

- Static plot image (PNG, PDF, SVG) via matplotlib savefig()
- Interactive HTML widget (bokeh or plotly)
- matplotlib Figure object or bokeh/plotly figure object ready for further annotation or display

## How to apply

Install pyOpenMS-viz (e.g. `pip install pyopenms_viz --upgrade`) in a dedicated conda environment. Load your mass spectrometry data into a Pandas DataFrame with columns matching your visualization intent (e.g., 'rt' and 'intensity' for chromatograms, 'm/z' and 'intensity' for spectra, or 'rt', 'm/z', and 'intensity' for 2D peak maps). Call the .plot() method on the DataFrame, specifying the x and y columns and the kind parameter ('chromatogram', 'spectrum', 'mobilogram', or 'peakmap'), optionally with plot3d=True for 3D peak maps. The matplotlib backend is the default for static output; switch backends by configuring your Pandas environment or passing backend-specific parameters. Verify correct rendering by checking axis labels, data range alignment, and visual continuity of the trace.

## Related tools

- **pyOpenMS-viz** (Provides the Pandas plotting backend and plotting API for mass spectrometry data visualization with support for matplotlib, bokeh, and plotly backends) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (DataFrame container and native .plot() method interface for tabular data)
- **matplotlib** (Default static rendering backend for pyOpenMS-viz plots)
- **bokeh** (Interactive visualization backend for pyOpenMS-viz plots)
- **plotly** (Interactive visualization backend supporting 3D peak maps and alternative interactivity model)

## Examples

```
import pandas as pd; ms_data = pd.read_csv('chromatogram.csv'); ms_data.plot(x='rt', y='intensity', kind='chromatogram'); plt.savefig('chromatogram.png')
```

## Evaluation signals

- Plot renders without errors and displays correct data range (x and y axes span expected retention time/m/z/intensity ranges).
- Axis labels match the specified column names and are human-readable (e.g., 'Retention Time (min)', 'Intensity').
- Visual continuity of mass trace: no gaps, jumps, or unexplained discontinuities in the plotted line or peaks.
- Output file is created and is valid (file size > 0, can be opened in target application or viewer).
- Backend switch (e.g., from matplotlib to bokeh) produces semantically identical data visualization with appropriate interactivity (zooming, panning, hover tooltips for interactive backends).

## Limitations

- pyOpenMS-viz is designed for mass spectrometry data; column names and semantics must align with MS conventions (e.g., 'rt', 'm/z', 'intensity') or the .plot() call will fail or produce incorrect results.
- 3D peak map rendering (plot3d=True) is only supported by matplotlib and plotly backends, not bokeh.
- The library requires data to be already in a Pandas DataFrame; conversion from proprietary MS file formats (e.g., .raw, .d) requires upstream loader tools not included in pyOpenMS-viz.
- No built-in support for statistical overlays (e.g., confidence intervals, smoothing splines) or custom color palettes; users must post-process the returned figure object with matplotlib/bokeh/plotly APIs for advanced customization.

## Evidence

- [readme] pyOpenMS-Viz provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data: "pyOpenMS-Viz provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data"
- [readme] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [other] ms_data.plot(x="rt", y="intensity", kind="chromatogram"): "ms_data.plot(x="rt", y="intensity", kind="chromatogram")"
- [readme] PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)"
