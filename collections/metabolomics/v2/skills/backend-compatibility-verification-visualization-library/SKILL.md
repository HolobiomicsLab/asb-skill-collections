---
name: backend-compatibility-verification-visualization-library
description: Use when you have mass spectrometry data loaded into a pandas DataFrame with m/z, retention time, and intensity columns, and need to confirm that pyOpenMS-Viz can produce visualizations (spectra, chromatograms, or peak maps) using a specific plotting backend (matplotlib, Bokeh, or Plotly) on real.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - pyteomics
  - pyOpenMS-Viz
  - Pandas
  - Plotly
  - Bokeh
  - matplotlib
  - PyOpenMS
  - pymzML
  - alphatims
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

# Backend Compatibility Verification for Visualization Libraries

## Summary

Verify that a pandas-based mass spectrometry visualization library successfully renders output across multiple plotting backends (matplotlib, Bokeh, Plotly) by loading real MS data, configuring the backend, and validating the resulting interactive or static plots. This skill ensures that visualization code is portable and produces correct output regardless of the backend chosen.

## When to use

You have mass spectrometry data loaded into a pandas DataFrame with m/z, retention time, and intensity columns, and need to confirm that pyOpenMS-Viz can produce visualizations (spectra, chromatograms, or peak maps) using a specific plotting backend (matplotlib, Bokeh, or Plotly) on real data from mzML or Bruker .d format files.

## When NOT to use

- Input data is not in a pandas DataFrame format or lacks required m/z, retention time, intensity columns
- 3D peak map visualization is required but using Bokeh backend, which does not support plot_3d=True
- Mass spectrometry data is in an unsupported file format not readable by pyOpenMS, pymzML, pyteomics, or alphatims

## Inputs

- pandas DataFrame with m/z, retention time, and intensity columns
- mzML or Bruker .d format mass spectrometry data files
- selected plotting backend identifier (string: 'matplotlib', 'bokeh', or 'plotly')

## Outputs

- Static matplotlib figure or interactive Bokeh/Plotly figure object
- HTML file (for Plotly backend) or rendered plot displayed in notebook/script
- Verification confirmation that backend produced expected visualization without errors

## How to apply

Load mass spectrometry data from mzML or Bruker .d files into a pandas DataFrame ensuring it contains m/z, retention time, and intensity columns. Set the pandas plotting backend using `pd.set_option('plotting.backend', '<backend_name>')` where the backend is 'matplotlib', 'bokeh', or 'plotly'. Call `DataFrame.plot()` with appropriate parameters: for 1D plots use `kind='spectrum'` or `kind='chromatogram'` with x and y columns; for 2D peak maps use `kind='peakmap'` with x, y, z columns; for 3D peak maps add `plot_3d=True` (supported only in matplotlib and Plotly, not Bokeh). Capture the returned figure object and save or render it (e.g., using `fig.write_html()` for Plotly) to visually verify that the backend successfully renders the data without errors and produces the expected visualization type.

## Related tools

- **pyOpenMS-Viz** (Primary visualization library that extends pandas DataFrame plotting with mass spectrometry-specific plot types) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Provides DataFrame structure and plotting backend configuration interface)
- **Plotly** (Interactive plotting backend supporting 2D and 3D peak map rendering)
- **Bokeh** (Interactive plotting backend supporting 2D spectra, chromatograms, and peak maps)
- **matplotlib** (Static plotting backend supporting all plot types including 3D peak maps)
- **PyOpenMS** (Loads mass spectrometry data from mzML and .d format files)
- **pymzML** (Alternative library for parsing mzML format files into DataFrame)
- **pyteomics** (Alternative library for parsing mzML format files into DataFrame)
- **alphatims** (Library for loading Bruker .d format files into DataFrame)

## Examples

```
import pandas as pd; from pyopenms_viz import *; ms_data = pd.read_csv('ms_data.csv'); pd.set_option('plotting.backend', 'plotly'); fig = ms_data.plot(x='m/z', y='rt', z='intensity', kind='peakmap', plot_3d=True); fig.write_html('output.html')
```

## Evaluation signals

- Figure object is successfully created without exceptions when calling DataFrame.plot() with the specified backend
- For Plotly backend: HTML file is generated via fig.write_html() and opens without errors in a web browser
- Visual inspection confirms the expected plot type is rendered (spectrum shows m/z vs intensity, chromatogram shows RT vs intensity, peak map shows 2D or 3D representation of m/z, RT, intensity)
- No data points are missing or incorrectly mapped between the source DataFrame and the rendered visualization
- Backend-specific interactivity works as expected (pan, zoom, hover tooltips for interactive backends; static image export for matplotlib)

## Limitations

- Bokeh backend does not support 3D peak map visualization (plot_3d=True parameter is ignored or causes error)
- DataFrame column names must exactly match expected names (m/z, rt, intensity) or be explicitly specified during plotting
- Large datasets (thousands of spectra or very high-resolution peak maps) may have performance differences across backends; Plotly may produce larger interactive HTML files than matplotlib static output
- Backend compatibility testing must be performed separately for each backend; passing with matplotlib does not guarantee Plotly or Bokeh will render identically

## Evidence

- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [other] Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame: "Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics"
- [other] Set the pandas plotting backend to 'ms_plotly' using pd.set_option: "Set the pandas plotting backend to 'ms_plotly' using `pd.set_option('plotting.backend', 'ms_plotly')`"
- [other] Call the DataFrame.plot() method with parameters x, y, z and plot_3d=True: "Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z for color mapping), `kind='peakmap'`, and `plot_3d=True`"
- [other] Capture the returned Plotly figure object and save it as HTML: "Capture the returned Plotly figure object and save it as an interactive HTML file using `fig.write_html()` to verify successful 3D visualization and backend compatibility"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] PeakMap 3D is supported only in matplotlib and Plotly, not Bokeh: "PeakMap 3D      | x, y, z                 | peakmap (plot3d=True)                                     | ✓              |           | ✓"
