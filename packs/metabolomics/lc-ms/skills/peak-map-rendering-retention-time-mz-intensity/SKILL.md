---
name: peak-map-rendering-retention-time-mz-intensity
description: Use when when you have loaded mass spectrometry data (from mzML or Bruker .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyteomics
  - pyOpenMS-Viz
  - Pandas
  - Plotly
  - matplotlib
  - Bokeh
  - PyOpenMS
  - pymzML
  - alphatims
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- pyopenms ... pymzml ... pyteomics
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

# peak-map-rendering-retention-time-mz-intensity

## Summary

Render interactive 2D and 3D peak-map visualizations of mass spectrometry data by plotting m/z (x-axis), retention time (y-axis), and intensity (z-axis or color) using pyOpenMS-Viz with Pandas DataFrames and pluggable plotting backends (matplotlib, Bokeh, Plotly). This skill enables rapid visual assessment of peak distributions, separation quality, and data quality across LC-MS experiments.

## When to use

When you have loaded mass spectrometry data (from mzML or Bruker .d format files) into a Pandas DataFrame with columns for m/z, retention time, and intensity, and need to visualize the joint distribution of these three dimensions to assess peak separation, detect artifacts, or identify regions of interest in the chromatographic and mass domain.

## When NOT to use

- When data lacks one of the three required dimensions (m/z, retention time, intensity); use 1D spectrum or chromatogram plots instead.
- When the input is not tabular (e.g., raw binary instrument data without prior parsing into DataFrame format).
- For batch visualization of >10,000 individual peak-map plots; consider aggregation or summary statistics instead to avoid I/O and rendering overhead.

## Inputs

- Pandas DataFrame with numeric columns for m/z, retention time, and intensity
- mzML file (via pymzML or pyteomics)
- Bruker .d directory (via alphatims or pyOpenMS)
- Plotly/matplotlib/Bokeh backend specification

## Outputs

- Interactive 2D peak-map Plotly figure (HTML file or in-memory Figure object)
- Interactive 3D peak-map Plotly figure (HTML file or in-memory Figure object)
- Static 2D peak-map matplotlib figure (PNG, PDF, or display)
- Static 2D peak-map Bokeh figure (HTML with hover tools)

## How to apply

Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (rt), and intensity using PyOpenMS, pymzML, pyteomics, or alphatims. Set the Pandas plotting backend to your chosen visualization library (e.g., 'ms_plotly' for interactive Plotly output) using `pd.set_option('plotting.backend', 'ms_plotly')`. Call `DataFrame.plot()` with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z to map intensity to color), `kind='peakmap'`, and optionally `plot_3d=True` for 3D Plotly rendering (note: 3D is supported by matplotlib and Plotly but not Bokeh). Capture and save the returned figure object as interactive HTML using `fig.write_html()` for web-based inspection or static PNG/PDF for publication. The consistent API across backends allows switching between matplotlib for quick static plots and Plotly for interactive exploration without changing core plotting logic.

## Related tools

- **pyOpenMS-Viz** (Primary visualization library providing peakmap plot type and Pandas backend registration; handles dimension mapping and plot generation across matplotlib, Bokeh, and Plotly.) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data structure and plotting API entry point; DataFrame.plot() method dispatches to pyOpenMS-Viz backend.)
- **Plotly** (Interactive backend for 2D and 3D peak-map rendering; supports hover tooltips, zoom, and pan for exploration.)
- **matplotlib** (Static plotting backend for 2D peak maps; suitable for publication-quality static output.)
- **Bokeh** (Interactive plotting backend for 2D peak maps with hover and selection tools; does not support 3D.)
- **PyOpenMS** (Data loader for mzML and Bruker .d files; integrates with Pandas DataFrame construction.)
- **pymzML** (Alternative data loader for mzML files; parses m/z, retention time, and intensity into tabular format.)
- **alphatims** (Data loader for Bruker .d format (timsTOF) files; outputs m/z, retention time, and intensity.)

## Examples

```
import pandas as pd
import pyopenms_viz
pd.set_option('plotting.backend', 'ms_plotly')
ms_data = pd.read_csv('ms_data.csv')
fig = ms_data.plot(x='m/z', y='rt', z='intensity', kind='peakmap', plot_3d=True)
fig.write_html('peakmap_3d.html')
```

## Evaluation signals

- The returned figure object is a valid Plotly Figure, matplotlib Axes, or Bokeh figure (check type and non-null attributes).
- The HTML file (if saved) renders without JavaScript errors and displays interactive controls (zoom, pan, hover for Plotly; hover for Bokeh).
- The x-axis range matches the m/z column min/max; y-axis matches retention time min/max; z-axis or color scale matches intensity min/max.
- 3D mode is only enabled when `plot_3d=True` and backend is matplotlib or Plotly (verify 3D axes or Plotly 3D scene object).
- Peak density visually correlates with high-intensity regions in the DataFrame; isolated points correspond to low-intensity features.

## Limitations

- Bokeh backend does not support 3D peak-map rendering; only 2D is available.
- Very large DataFrames (>1 million rows) may cause Plotly 3D performance degradation due to WebGL rendering limits; consider downsampling or aggregation.
- Column naming must exactly match expected keys (m/z, rt, intensity); no automatic fuzzy matching is performed.
- The API assumes numeric, non-missing values in the dimension columns; NaN or non-numeric entries will cause rendering errors.

## Evidence

- [other] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data."
- [readme] The library's 2D and 3D peak-map visualization capabilities are documented in the supported plots table.: "PeakMap 2D | x, y, z | peakmap | ✓ | ✓ | ✓
PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓"
- [other] The recommended workflow for 3D peak-map visualization invokes Plotly as the backend.: "Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z for color mapping), `kind='peakmap'`, and `plot_3d=True` to invoke the Plotly 3D rendering engine."
- [other] Core data loading and integration steps for MS data.: "Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format), ensuring columns for m/z, retention time,"
- [readme] The library supports flexible backend switching without changing plotting logic.: "Consistent API across different plotting backends for easy switching between static and interactive plots"
