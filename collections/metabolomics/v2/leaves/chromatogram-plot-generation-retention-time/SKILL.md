---
name: chromatogram-plot-generation-retention-time
description: Use when you have mass spectrometry data loaded as a Pandas DataFrame
  with retention time and intensity columns, and you need to visualize the overall
  or mass-trace-specific signal intensity distribution across the chromatographic
  separation.
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
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# chromatogram-plot-generation-retention-time

## Summary

Generate static or interactive chromatogram plots from mass spectrometry data using retention time (x-axis) and intensity (y-axis) columns in a Pandas DataFrame. This skill enables visualization of LC-MS signal intensity patterns across the chromatographic separation dimension, with support for multiple plotting backends (matplotlib, Bokeh, Plotly) and optional mass trace separation.

## When to use

You have mass spectrometry data loaded as a Pandas DataFrame with retention time and intensity columns, and you need to visualize the overall or mass-trace-specific signal intensity distribution across the chromatographic separation. Use this skill when exploring peak patterns, detecting coelution, or generating publication-ready chromatogram figures for inclusion in manuscripts or interactive analysis dashboards.

## When NOT to use

- Your data requires simultaneous visualization of m/z and retention time dimensions — use peakmap plots instead.
- You only have a single mass-to-charge value and need to visualize ion mobility separation — use mobilogram plots.
- Your input is already a pre-rendered figure or image file rather than tabular data.

## Inputs

- Pandas DataFrame with retention time (x) and intensity (y) columns
- mass spectrometry data in mzML format (converted to DataFrame via pymzml or pyOpenMS)
- mass spectrometry data in Bruker .d format (converted to DataFrame via AlphaTims)
- ChromatogramConfig object (optional, for customization)

## Outputs

- Static chromatogram figure (matplotlib .png/.pdf)
- Interactive chromatogram figure (Bokeh .html)
- Interactive chromatogram figure (Plotly .html)

## How to apply

Load your mass spectrometry data (from mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a Pandas DataFrame with retention time and intensity columns. Call the DataFrame .plot() method with x='rt' (or your retention time column name), y='intensity' (or equivalent intensity column), set kind='chromatogram', and specify backend as 'ms_matplotlib', 'ms_bokeh', or 'ms_plotly' depending on whether you need static or interactive output. Optionally, use the by parameter to separate chromatogram traces by mass-to-charge ratio or other grouping variable, and pass ChromatogramConfig parameters to customize axis labels, styling, and plot dimensions. The library will automatically render the figure and save it in the backend's native format.

## Related tools

- **pyOpenMS-Viz** (Primary library providing the .plot() DataFrame extension method and backend-agnostic chromatogram rendering API) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data structure (DataFrame) and method-chaining interface for specifying plot inputs)
- **matplotlib** (Backend for generating static chromatogram figures (ms_matplotlib backend))
- **Bokeh** (Backend for generating interactive chromatogram figures (ms_bokeh backend))
- **Plotly** (Backend for generating interactive chromatogram figures (ms_plotly backend))
- **pymzml** (Tool for reading mzML files and populating retention time and intensity columns in DataFrame)
- **pyOpenMS** (Tool for reading mzML files and populating retention time and intensity columns in DataFrame)
- **AlphaTims** (Tool for reading Bruker .d format files and populating retention time and intensity columns in DataFrame)

## Examples

```
ms_data.plot(x="rt", y="intensity", kind="chromatogram", backend="ms_matplotlib")
```

## Evaluation signals

- Verify that the generated figure file exists in the expected backend format (.png/.pdf for matplotlib, .html for Bokeh/Plotly) and matches the reference gallery output (gallery_scripts/ms_matplotlib/, gallery_scripts/ms_bokeh/, gallery_scripts/ms_plotly/)
- Check that the x-axis correctly displays retention time values with appropriate units and range matching the input data
- Confirm that the y-axis correctly displays intensity values with appropriate scaling and dynamic range matching the input data
- If using the by parameter for mass trace separation, verify that distinct chromatogram traces are rendered and visually or programmatically separable by color or legend
- For interactive backends (Bokeh, Plotly), verify that hover tooltips, zooming, panning, and other interactive affordances are functional and render correctly in a web browser or notebook environment

## Limitations

- The skill currently supports only 2D chromatograms (retention time × intensity); simultaneous visualization of a third dimension (e.g., ion mobility or m/z) requires switching to peakmap or mobilogram plot types.
- Performance may degrade for very large datasets (millions of retention time–intensity pairs) in interactive backends; static matplotlib plots are typically faster for such data.
- Column names must match exactly the parameters passed to x and y in the .plot() call; automatic column detection is not performed, so users must inspect their DataFrame columns first.
- Bruker .d format reading requires external installation of AlphaTims, which may not be available on all platforms or may require additional system dependencies.

## Evidence

- [other] For chromatogram plots, use retention time on x-axis and intensity on y-axis with optional by parameter for mass trace separation and ChromatogramConfig parameters.: "For chromatogram plots, use retention time on x-axis and intensity on y-axis with optional by parameter for mass trace separation and ChromatogramConfig parameters."
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [other] Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame.: "Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame."
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
