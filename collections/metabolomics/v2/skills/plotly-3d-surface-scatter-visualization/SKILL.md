---
name: plotly-3d-surface-scatter-visualization
description: Use when you have mass spectrometry data (m/z, retention time, intensity) loaded into a Pandas DataFrame and need to explore the full 3D structure of a peak map interactively, particularly when static 2D heatmaps obscure important intensity relationships or when stakeholders require browser-based.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Plotly
  - pyteomics
  - pyOpenMS-Viz
  - Pandas
  - PyOpenMS
  - pymzML
  - alphatims
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)
- 'Extension: PLOTLY'
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
---

# plotly-3d-surface-scatter-visualization

## Summary

Create interactive 3D peak-map visualizations of mass spectrometry data using the Plotly backend in pyOpenMS-Viz. This skill enables rendering of m/z, retention time, and intensity dimensions as an interactive 3D surface or scatter plot, suitable for exploratory analysis of complex MS datasets.

## When to use

Use this skill when you have mass spectrometry data (m/z, retention time, intensity) loaded into a Pandas DataFrame and need to explore the full 3D structure of a peak map interactively, particularly when static 2D heatmaps obscure important intensity relationships or when stakeholders require browser-based interactive inspection of MS data from mzML or Bruker .d format files.

## When NOT to use

- Input data lacks three required dimensions (m/z, retention time, intensity) — fall back to 2D peakmap or spectrum visualization.
- Dataset is extremely large (>1 million points) and Plotly rendering becomes prohibitively slow — consider 2D heatmap or downsampled subset.
- Target deployment environment cannot serve HTML or JavaScript (e.g., headless server without display) — use static matplotlib or Bokeh backend instead.

## Inputs

- Pandas DataFrame with columns for m/z, retention time, and intensity
- Mass spectrometry data file in mzML or Bruker .d format
- Plotly-compatible plotting backend configuration

## Outputs

- Interactive Plotly 3D figure object (plotly.graph_objects.Figure)
- HTML file containing the interactive 3D peak-map visualization
- Browser-renderable visualization with rotation, zoom, and hover capabilities

## How to apply

Load mass spectrometry data from mzML or Bruker .d files into a Pandas DataFrame with columns for m/z, retention time (rt), and intensity using PyOpenMS, pymzML, pyteomics, or alphatims. Set the Pandas plotting backend to 'plotly' and call the DataFrame.plot() method with parameters x='m/z', y='rt', z='intensity', kind='peakmap', and plot_3d=True. The Plotly rendering engine will generate an interactive HTML figure object; save it using fig.write_html() to produce a browser-viewable visualization. Verify that the 3D surface correctly maps all three dimensions and that interactivity (rotation, zoom, hover tooltips) functions without data loss.

## Related tools

- **pyOpenMS-Viz** (Primary library providing the peakmap plotting interface and 3D rendering support via Plotly backend) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data manipulation and DataFrame structure required as input to pyOpenMS-Viz plotting API)
- **Plotly** (Interactive 3D graphing backend responsible for rendering and interactivity of the visualization)
- **PyOpenMS** (Mass spectrometry data loading and preprocessing from OpenMS formats)
- **pymzML** (Alternative tool for loading mass spectrometry data from mzML format files)
- **pyteomics** (Alternative tool for loading mass spectrometry data from mzML format files)
- **alphatims** (Tool for loading mass spectrometry data from Bruker .d format files)

## Examples

```
import pandas as pd
from pyopenms import MSExperiment
ms_data = pd.read_csv('ms_peaks.csv')
pd.set_option('plotting.backend', 'plotly')
fig = ms_data.plot(x='m/z', y='rt', z='intensity', kind='peakmap', plot_3d=True)
fig.write_html('3d_peakmap.html')
```

## Evaluation signals

- The rendered 3D plot displays all three dimensions (m/z on x-axis, retention time on y-axis, intensity on z-axis or color) without data loss or dimension conflation.
- Interactive controls (rotation, zoom, pan, hover tooltips showing m/z/rt/intensity values) respond smoothly without lag or visual artifacts.
- The HTML output file is valid and opens in a standard web browser without JavaScript errors or missing dependencies.
- Intensity values are correctly mapped to the z-axis or color scale; verify by hovering over peak regions and comparing reported values to source DataFrame.
- No warnings or exceptions are raised during plotting backend selection (`pd.set_option('plotting.backend', 'plotly')`) and figure generation.

## Limitations

- Plotly 3D rendering supports peakmap plots but not mobilogram or chromatogram plots in 3D — those remain 2D only.
- Very large datasets (>1 million points) may experience slow interactivity or browser memory issues; downsampling may be required.
- The plot_3d=True flag is exclusive to Plotly backend; matplotlib and Bokeh backends do not support 3D peakmap rendering.
- Interactive HTML files require a modern web browser with JavaScript enabled; export to static image formats (PNG, SVG) is possible but loses interactivity.

## Evidence

- [other] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data."
- [other] Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format): "Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format)"
- [other] Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z for color mapping), `kind='peakmap'`, and `plot_3d=True` to invoke the Plotly 3D rendering engine.: "Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z for color mapping), `kind='peakmap'`, and `plot_3d=True` to invoke the Plotly 3D rendering engine."
- [other] Capture the returned Plotly figure object and save it as an interactive HTML file using `fig.write_html()` to verify successful 3D visualization and backend compatibility.: "Capture the returned Plotly figure object and save it as an interactive HTML file using `fig.write_html()` to verify successful 3D visualization and backend compatibility."
- [readme] PeakMap 3D requires x, y, z dimensions and is supported by matplotlib and Plotly but not Bokeh: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓"
