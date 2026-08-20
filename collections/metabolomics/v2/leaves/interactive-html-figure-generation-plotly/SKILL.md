---
name: interactive-html-figure-generation-plotly
description: Use when your mass spectrometry DataFrame contains m/z, retention time
  (or mobility), and intensity columns, and you need to generate an interactive HTML
  figure for exploration, web-based presentation, or interactive supplementary material.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Plotly
  - pyteomics
  - pyOpenMS-Viz
  - Pandas
  - PyOpenMS
  - pymzML
  - alphatims
  techniques:
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- integrates seamlessly with various plotting library backends (matpotlib, bokeh and
  plotly)
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

# interactive-html-figure-generation-plotly

## Summary

Generate interactive HTML visualizations of mass spectrometry data using Plotly as the pyOpenMS-Viz plotting backend, enabling 2D and 3D peak-map rendering with client-side interactivity. Use this skill when you need to produce publication-ready, browser-viewable figures that preserve dimensionality (m/z, retention time, intensity) and support pan/zoom/hover inspection.

## When to use

Your mass spectrometry DataFrame contains m/z, retention time (or mobility), and intensity columns, and you need to generate an interactive HTML figure for exploration, web-based presentation, or interactive supplementary material. Plotly is the right choice when matplotlib's static output is insufficient and Bokeh's capabilities do not meet your interactivity needs.

## When NOT to use

- You need only static, publication-quality figures without interactivity — use matplotlib backend instead.
- Your mass spectrometry data lacks a retention time dimension (single spectrum) and you do not need 2D/3D peak-map visualization.
- Your data volume exceeds ~100,000 points and browser rendering performance is critical — Plotly may struggle with very large datasets in interactive mode.

## Inputs

- pandas.DataFrame with columns for m/z, retention time (or mobility), and intensity
- mzML file (via PyOpenMS, pymzML, or pyteomics)
- Bruker .d directory (via alphatims or PyOpenMS)
- CSV file with mass spectrometry data (m/z, rt, intensity columns)

## Outputs

- Interactive HTML file (Plotly Figure object serialized with fig.write_html())
- Plotly Figure object (in-memory, for Jupyter notebooks or programmatic use)

## How to apply

Load or construct a pandas DataFrame with columns for m/z, retention time (or mobility), and intensity from mzML, Bruker .d, or other mass spectrometry formats using PyOpenMS, pymzML, pyteomics, or alphatims. Set the pandas plotting backend to 'ms_plotly' using `pd.set_option('plotting.backend', 'ms_plotly')`. Call DataFrame.plot() with parameters `kind='peakmap'` (or 'spectrum'/'chromatogram'/'mobilogram' for 1D/2D alternatives), specifying x, y, and optionally z axes; for 3D visualization, add `plot_3d=True`. Capture the returned Plotly figure object and serialize it to an interactive HTML file using `fig.write_html('output.html')` to verify successful rendering and backend compatibility. The HTML file can then be opened in any modern web browser for interactive inspection.

## Related tools

- **pyOpenMS-Viz** (Core library providing the pandas DataFrame plotting extension and integration with Plotly backend for mass spectrometry visualization) — https://github.com/OpenMS/pyopenms_viz
- **Plotly** (Plotting library backend that renders interactive HTML figures with client-side pan/zoom/hover and 3D surface support)
- **Pandas** (Data container (DataFrame) and plotting API that pyOpenMS-Viz extends for mass spectrometry data manipulation)
- **PyOpenMS** (Library for loading and parsing mass spectrometry data from mzML and Bruker .d formats into DataFrames)
- **pymzML** (Alternative mzML parser for loading mass spectrometry data into Python structures)
- **alphatims** (Library for loading Bruker .d format (TIMS) mass spectrometry data with ion mobility dimensions)

## Examples

```
import pandas as pd; from pyopenms_viz import *; pd.set_option('plotting.backend', 'ms_plotly'); ms_data = pd.read_csv('ms_data.csv'); fig = ms_data.plot(x='m/z', y='rt', z='intensity', kind='peakmap', plot_3d=True); fig.write_html('interactive_peakmap.html')
```

## Evaluation signals

- HTML file is generated without errors and opens in a web browser without JavaScript errors (check browser console).
- Interactive controls (pan, zoom, hover tooltip showing m/z, retention time, intensity) function as expected in the browser.
- For 3D peak-maps, the z-axis (intensity) is rendered as a 3D surface and can be rotated/tilted by mouse interaction.
- Figure title, axis labels, and legend match the DataFrame column names and data range (no NaN or inf values leak into the visualization).
- For 2D peak-maps, the heatmap color scale correctly maps intensity values across the retention time × m/z plane.

## Limitations

- Bokeh backend does not support 3D visualization (only matplotlib and Plotly do) — choose Plotly if 3D is required.
- Very large datasets (>1M points) may cause browser lag or memory issues due to client-side rendering; consider downsampling or binning before visualization.
- The Plotly backend requires modern JavaScript-enabled browsers; offline HTML files generated by fig.write_html() will not render in browsers with JavaScript disabled.
- Column selection is flexible but requires exact column name matches; if your DataFrame uses non-standard column names (e.g., 'm/z_ratio' instead of 'm/z'), the plot will fail or produce unexpected results.

## Evidence

- [other] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations"
- [readme] The README documents that Plotly supports 3D peak-map visualization with the plot_3d=True flag.: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓"
- [other] The workflow explicitly describes setting the pandas plotting backend and calling DataFrame.plot() with Plotly parameters.: "Set the pandas plotting backend to 'ms_plotly' using `pd.set_option('plotting.backend', 'ms_plotly')`. 3. Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or"
- [other] The task specifies serialization to HTML format for verification and sharing.: "Capture the returned Plotly figure object and save it as an interactive HTML file using `fig.write_html()` to verify successful 3D visualization and backend compatibility"
- [readme] The library supports multiple mass spectrometry data formats and input methods.: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
