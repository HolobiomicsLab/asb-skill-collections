---
name: intensity-color-representation
description: Use when when visualizing 2D peak maps (x=m/z, y=retention time or ion mobility, z=intensity) using pyOpenMS-viz with any plotting backend (matplotlib, bokeh, plotly).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-viz
  - Python
  - Pandas
  - bokeh
  - matplotlib
  - plotly
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# intensity-color-representation

## Summary

Map mass spectrometry intensity values to a color scale in 2D peak map visualizations to enable intuitive perception of signal strength across m/z and retention time dimensions. This skill is essential for interactive and static peak map plots where color intensity conveys the third dimension (intensity/abundance) of the data.

## When to use

When visualizing 2D peak maps (x=m/z, y=retention time or ion mobility, z=intensity) using pyOpenMS-viz with any plotting backend (matplotlib, bokeh, plotly). The skill is triggered when you have mass spectrometry data in a Pandas DataFrame with three numeric columns representing m/z, retention time (or ion mobility), and intensity, and you need to render the intensity dimension as a color scale rather than as explicit z-axis height.

## When NOT to use

- Input data lacks a clear intensity dimension or has missing/invalid z values — intensity-to-color mapping requires complete, numeric intensity data.
- Visualization goal is 1D (chromatogram or spectrum only) — use 'chromatogram' or 'spectrum' plot kind instead of 'peakmap'.
- You need explicit numeric z-axis height (3D surface plot) rather than color; use peakmap with plot3d=True and plotly or matplotlib backends instead.

## Inputs

- Pandas DataFrame with three numeric columns: m/z (x), retention_time or ion_mobility (y), intensity (z)

## Outputs

- Interactive or static 2D peak map plot with intensity encoded as continuous color scale
- Optionally, marginal chromatogram and spectrum plots (if add_marginals=True)

## How to apply

Structure your mass spectrometry data as a Pandas DataFrame with columns for m/z (x-axis), retention time or ion mobility (y-axis), and intensity (z-axis). Call DataFrame.plot() with kind='peakmap', specifying x and y column names, and rely on pyOpenMS-viz's automatic color mapping of the z (intensity) column to a continuous color scale. The color representation uses intensity values directly; select a backend (matplotlib for static, bokeh or plotly for interactive) via the backend parameter. Optionally enable marginal plots with add_marginals=True to display integrated chromatograms and spectra alongside the main peak map. Verify that the color scale spans from low (cool) to high (warm) colors, matching the min/max intensity range in your data.

## Related tools

- **pyOpenMS-viz** (Primary plotting library that implements peak map visualization with automatic intensity-to-color mapping for Pandas DataFrames) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data manipulation and representation framework; holds mass spectrometry data as DataFrame with m/z, retention time, and intensity columns)
- **bokeh** (Interactive plotting backend for rendering peak maps with color-mapped intensity and hover tooltips)
- **matplotlib** (Static plotting backend for rendering peak maps with intensity-to-color mapping)
- **plotly** (Interactive plotting backend supporting both 2D and 3D peak maps with intensity color representation)

## Examples

```
ms_data.plot(x="m/z", y="rt", z="intensity", kind="peakmap", backend="ms_bokeh", add_marginals=True)
```

## Evaluation signals

- Color scale is continuous and monotonically maps low intensity → cool colors (blue) and high intensity → warm colors (red/yellow)
- Color bar or legend is present and labeled with intensity units (e.g., 'Intensity', '[counts]')
- All data points are rendered with no missing colors; NaN or zero intensity values do not cause rendering errors
- Marginal plots (if enabled) correctly reflect integrated intensity: chromatogram y-values match sum of intensities per RT bin; spectrum y-values match sum of intensities per m/z bin
- Interactive backends (bokeh, plotly) allow hover inspection of exact m/z, retention time, and intensity values corresponding to each colored pixel

## Limitations

- Color mapping is automatically determined by pyOpenMS-viz; custom colormaps or manual intensity scale adjustment is not documented in the provided README or workflow steps.
- 3D peak maps (with explicit z-axis height) are supported only in matplotlib and plotly backends, not in bokeh; intensity-color representation in bokeh is limited to 2D.
- Missing or zero intensity values may render as transparent or a default color; the handling is backend-dependent and not explicitly specified in the README.
- Very large datasets with millions of points may suffer performance degradation in interactive backends; static matplotlib is more efficient for large matrices.

## Evidence

- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [other] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [other] Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap': "Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap'"
- [other] Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra: "Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra"
