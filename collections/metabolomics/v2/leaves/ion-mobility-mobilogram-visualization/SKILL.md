---
name: ion-mobility-mobilogram-visualization
description: Use when when you have mass spectrometry data with ion mobility (drift
  time or 1/K₀) measurements as a continuous dimension and want to visualize intensity
  distributions across the ion mobility axis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - AlphaTims
  - pyOpenMS-Viz
  - pandas
  - matplotlib
  - Bokeh
  - Plotly
  - pymzml
  - pyOpenMS
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# ion-mobility-mobilogram-visualization

## Summary

Create 1D ion-mobility mobilogram visualizations from mass spectrometry data using pyOpenMS-Viz, supporting static (matplotlib) and interactive (Bokeh, Plotly) backends. This skill enables rapid exploration and publication of ion-mobility separation patterns across multiple plotting frameworks.

## When to use

When you have mass spectrometry data with ion mobility (drift time or 1/K₀) measurements as a continuous dimension and want to visualize intensity distributions across the ion mobility axis. Apply this skill when you need to compare mobilograms across multiple mass traces (using the optional 'by' parameter for grouping), or when you require switching between static publication-ready plots and interactive web-based visualizations without code restructuring.

## When NOT to use

- Input data lacks an ion-mobility dimension (e.g., only m/z and retention time present) — use chromatogram visualization instead.
- Visualizing 2D m/z vs. retention-time peak distributions — use peakmap visualization with 2D or 3D rendering.
- Data is already aggregated as a static image or summary plot — this skill requires raw numeric ion-mobility and intensity vectors in a DataFrame.

## Inputs

- pandas.DataFrame with ion mobility (drift time or 1/K₀) column (numeric, x-axis)
- pandas.DataFrame with intensity column (numeric, y-axis)
- Optional: pandas.DataFrame with mass trace identifier column (string or numeric, for 'by' grouping)
- Optional: MobilogramConfig parameters (axis labels, title, intensity normalization settings)

## Outputs

- Static matplotlib figure file (.png, .pdf, or in-memory matplotlib.figure.Figure object)
- Interactive Bokeh HTML widget or figure object
- Interactive Plotly figure object or HTML file
- Mobilogram with ion mobility on x-axis, intensity on y-axis, optionally color-coded or separated by mass trace

## How to apply

Load ion-mobility mass spectrometry data into a pandas DataFrame with columns for ion mobility (x-axis) and intensity (y-axis), optionally adding mass-to-charge (m/z) or compound identifiers for trace separation. Call the DataFrame's .plot() method with kind='mobilogram', specify x and y column names, and set the backend parameter to 'ms_matplotlib' (static output), 'ms_bokeh', or 'ms_plotly' (interactive). Use the optional 'by' parameter to split the mobilogram into separate traces per mass value or compound. Apply MobilogramConfig parameters to customize axis labels, titles, and intensity scaling. The consistent API across backends ensures identical data representation; choose backend based on downstream use (static figures for publications, interactive for exploratory notebooks). Verify output by checking that the generated figure file matches reference outputs in the gallery and visually inspects peak separation along the ion-mobility dimension.

## Related tools

- **pyOpenMS-Viz** (Provides the .plot() method extension and mobilogram rendering for pandas DataFrames across multiple backends) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (DataFrame container and data manipulation for ion-mobility and intensity columns)
- **matplotlib** (Static 2D mobilogram rendering via ms_matplotlib backend)
- **Bokeh** (Interactive 2D mobilogram rendering via ms_bokeh backend)
- **Plotly** (Interactive 2D mobilogram rendering via ms_plotly backend)
- **pymzml** (Parse mzML mass spectrometry data files into ion-mobility and intensity arrays for DataFrame construction)
- **pyOpenMS** (Alternative data loader for mzML files and ion-mobility mass spectrometry workflows)
- **AlphaTims** (Load Bruker .d format ion-mobility time-of-flight data into numerical form for DataFrame ingestion)

## Examples

```
ms_data.plot(x="ion_mobility", y="intensity", kind="mobilogram", backend="ms_plotly", by="mz")
```

## Evaluation signals

- Output figure file exists in the expected format (.png, .pdf, .html) with correct backend naming convention (ms_matplotlib, ms_bokeh, ms_plotly).
- Visual inspection confirms ion mobility axis spans the correct range (e.g., 0–150 drift-time units or 0.8–1.4 1/K₀), intensity axis shows correct peak heights, and x/y axis labels are set correctly.
- Generated figure matches the structure and peak position of the corresponding reference output in gallery_scripts/ subdirectories (ms_matplotlib/, ms_bokeh/, ms_plotly/).
- When 'by' parameter is used for mass-trace grouping, output mobilogram shows distinct traces, colors, or subplots per group with no missing or mislabeled categories.
- Interactive backends (Bokeh, Plotly) preserve hover tooltips, zoom, pan, and legend functionality; static matplotlib output renders cleanly without rendering errors or NaN artifacts.

## Limitations

- Bokeh does not support 3D peakmap rendering (only 2D mobilograms); use matplotlib or Plotly for 3D visualizations if required.
- MobilogramConfig customization is limited to built-in parameters; complex axis transforms or non-standard intensity scalings may require post-processing or custom matplotlib/Plotly code.
- Large DataFrames (>100k rows per trace) may incur slower interactive rendering in Bokeh/Plotly; consider downsampling or aggregation for real-time exploration.
- Ion-mobility data from different instrumentation (e.g., Bruker timsTOF, Waters Vion) may have different native units (1/K₀, drift time, collision cross-section); ensure column names and axis labels reflect the correct unit before visualization.

## Evidence

- [other] For mobilogram plots, use ion mobility on x-axis and intensity on y-axis with optional by parameter for mass trace separation and MobilogramConfig parameters.: "For mobilogram plots, use ion mobility on x-axis and intensity on y-axis with optional by parameter for mass trace separation and MobilogramConfig parameters."
- [other] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data.: "pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data."
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
