---
name: retention-time-mz-coordinate-mapping
description: Use when when you have mass-spectrometry data in tabular form (Pandas DataFrame) with columns for m/z, retention time or ion mobility, and intensity, and you need to visualize the 2D distribution of peaks to assess peak separation, detect co-elution, or examine chromatographic and mass resolution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-viz
  - Python
  - Pandas
  - bokeh
  - matplotlib
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
---

# retention-time-mz-coordinate-mapping

## Summary

Map mass-spectrometry data onto a two-dimensional coordinate system using retention time (or ion mobility) as one axis and m/z as the other, enabling interactive or static visualization of peak maps. This skill is essential for visualizing the joint distribution of analytes across time and mass dimensions.

## When to use

When you have mass-spectrometry data in tabular form (Pandas DataFrame) with columns for m/z, retention time or ion mobility, and intensity, and you need to visualize the 2D distribution of peaks to assess peak separation, detect co-elution, or examine chromatographic and mass resolution together.

## When NOT to use

- Input data lacks retention time or ion mobility information—use 1D spectrum visualization instead.
- You require 3D visualization with z-axis as a spatial dimension beyond intensity—use peakmap(plot3d=True) with plotly backend instead.
- Data is already aggregated to a feature table or intensity matrix without original m/z and time coordinates.

## Inputs

- Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity

## Outputs

- Interactive Bokeh plot object (when backend='ms_bokeh')
- Static matplotlib figure object (when backend='matplotlib' or default)
- 2D peak map visualization with optional marginal plots

## How to apply

Load mass-spectrometry data into a Pandas DataFrame with required columns: m/z, retention time (or ion mobility), and intensity. Set the Pandas plotting backend to 'ms_bokeh' (for interactive Bokeh plots) or keep matplotlib default (for static plots) using pd.set_option(). Call the DataFrame.plot() method with x and y parameters specifying the column names for m/z and retention time, kind='peakmap', and backend='ms_bokeh' (or omit backend for matplotlib). Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra on the axes. The resulting plot renders intensity as a third dimension (typically color or z-axis height) to create a 2D peak map visualization.

## Related tools

- **pyOpenMS-viz** (Primary library providing the plotting API and peakmap visualization kind for Pandas DataFrames) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data structure (DataFrame) that holds m/z, retention time, and intensity columns; provides plot() method interface)
- **bokeh** (Interactive plotting backend for rendering 2D peak maps with hover tooltips and zoom/pan interactions)
- **matplotlib** (Static plotting backend alternative for rendering 2D peak maps as raster images)

## Examples

```
ms_data.plot(x="m/z", y="rt", kind="peakmap", backend="ms_bokeh", add_marginals=True)
```

## Evaluation signals

- Verify that the resulting plot displays both m/z on one axis and retention time (or ion mobility) on the other axis with correct column labels.
- Check that intensity is encoded as a visual third dimension (e.g., color intensity or contour height) and matches expected peak magnitudes from the input DataFrame.
- If add_marginals=True, confirm that marginal plots on the axes correctly represent 1D chromatograms and spectra derived from projecting the 2D data.
- For interactive plots, test that hover tooltips reveal m/z, retention time, and intensity values for individual peaks.
- Confirm that peak positions in the 2D plot correspond to non-zero intensity rows in the input DataFrame and that no rows are dropped or misaligned.

## Limitations

- The peakmap plot requires exactly three dimensions (x, y, z); missing retention time or m/z will raise an error.
- 3D peakmap visualization (plot3d=True) is not supported by the bokeh backend—use plotly backend instead.
- Marginal plots (add_marginals=True) may reduce clarity when the 2D peak map is already dense; consider filtering or downsampling large datasets before visualization.
- Column names must be explicitly specified; the function does not auto-detect standard MS column names.

## Evidence

- [other] Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity.: "Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity."
- [other] Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh'.: "Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh'."
- [other] Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra.: "Optionally enable marginal plots by setting add_marginals=True to display marginal chromatograms and spectra."
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
