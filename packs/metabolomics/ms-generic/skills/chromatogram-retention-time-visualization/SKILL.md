---
name: chromatogram-retention-time-visualization
description: Use when you have mass spectrometry data loaded as a pandas DataFrame with at minimum two numeric columns representing retention time and intensity values, and you need to generate a chromatogram visualization for exploratory analysis, quality control, or publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pyOpenMS-viz
  - pandas
  - matplotlib
  - bokeh
  - plotly
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
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

# chromatogram-retention-time-visualization

## Summary

Generate static or interactive chromatogram plots from mass spectrometry data by mapping retention time (RT) to the x-axis and intensity to the y-axis using pyOpenMS-viz with a specified plotting backend. This skill enables publication-ready visualization of 1D chromatographic traces across multiple plotting backends (matplotlib, bokeh, plotly) while leveraging pandas DataFrames for flexible column mapping.

## When to use

Apply this skill when you have mass spectrometry data loaded as a pandas DataFrame with at minimum two numeric columns representing retention time and intensity values, and you need to generate a chromatogram visualization for exploratory analysis, quality control, or publication. Trigger conditions include: (1) data is already in or convertible to a pandas DataFrame from CSV, mzML, or similar MS data formats; (2) you want to inspect peak patterns across the retention time dimension; (3) you need to produce static (matplotlib) or interactive (bokeh/plotly) output suitable for notebooks or web applications.

## When NOT to use

- Input data lacks retention time or intensity dimensions — use spectrum or peakmap visualization instead.
- You need 2D or 3D mass spectrometry heatmap output (m/z vs. RT vs. intensity) — use peakmap kind instead.
- Your data is already pre-aggregated into a static image or bitmap — visualization skill is not needed.

## Inputs

- pandas DataFrame with numeric 'rt' (retention time) and 'intensity' columns
- mzML file (converted to pandas DataFrame via pyOpenMS or similar loader)
- CSV file with retention time and intensity traces (loaded as pandas DataFrame)

## Outputs

- static chromatogram figure (matplotlib.figure.Figure or saved PNG/PDF)
- interactive chromatogram visualization (bokeh Plot or plotly Figure object)
- saved chromatogram file (PNG, PDF, or HTML depending on backend)

## How to apply

First, load your mass spectrometry data into a pandas DataFrame, ensuring columns named or mapped to 'rt' (retention time) and 'intensity' exist. Second, select your target plotting backend and configure it via `pd.set_option('plotting.backend', 'ms_matplotlib')` or the equivalent for bokeh/plotly. Third, call `.plot(x='rt', y='intensity', kind='chromatogram')` on the DataFrame, optionally using the 'by' parameter to facet by mass-to-charge (m/z) value if multiple traces are present. Fourth, verify the resulting figure displays a line or area plot with retention time on the x-axis and intensity on the y-axis, with peaks corresponding to known compound elution times. Fifth, save the figure as PNG or vector format using matplotlib's `savefig()` or the backend's equivalent export method. The rationale is that pyOpenMS-viz abstracts backend differences into a unified pandas plotting API, avoiding boilerplate matplotlib/bokeh/plotly code while ensuring column names map correctly to MS semantics.

## Related tools

- **pyOpenMS-viz** (Primary visualization library providing unified pandas plotting API for chromatogram rendering across matplotlib, bokeh, and plotly backends) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (DataFrame container and manipulation library; .plot() method dispatches to pyOpenMS-viz backend)
- **matplotlib** (Static chromatogram rendering backend; handles figure generation and file export (PNG, PDF))
- **bokeh** (Interactive chromatogram rendering backend; enables hover tooltips and browser-based exploration)
- **plotly** (Interactive chromatogram rendering backend; supports both static and interactive output including 3D variants)

## Examples

```
import pandas as pd; ms_data = pd.read_csv('chromatogram.csv'); pd.set_option('plotting.backend', 'ms_matplotlib'); ms_data.plot(x='rt', y='intensity', kind='chromatogram'); plt.savefig('chromatogram.png', dpi=300)
```

## Evaluation signals

- Output figure displays a line or area plot with retention time values on x-axis and corresponding intensity values on y-axis
- Peak positions in the chromatogram align with expected retention times for known compounds in the sample
- When 'by' parameter is used, faceted subplots correctly separate traces by m/z or other grouping column without data loss
- Figure dimensions, axis labels, and title are readable and conform to publication standards (e.g., high DPI, legible fonts)
- Saved file format (PNG/PDF/HTML) is correct and opens without corruption; file size is appropriate for backend choice

## Limitations

- Requires retention time and intensity columns to be present and numeric; missing or null values may cause plot errors or distorted visualization.
- The 'by' parameter assumes a discrete grouping column (e.g., m/z); continuous variables will not facet meaningfully.
- Interactive backends (bokeh, plotly) have limited support for certain advanced matplotlib customizations (e.g., custom colormaps, complex annotations).
- Large datasets (millions of RT-intensity points) may render slowly or consume significant memory in interactive backends; consider downsampling or aggregation.
- Consistent axis scaling and labeling depend on correct column naming; typos or case mismatches will cause KeyError exceptions.

## Evidence

- [other] Load mass spectrometry data into pandas DataFrame with retention time (rt) and intensity columns: "Load mass spectrometry data into a pandas DataFrame from a deposited CSV or mzML file containing retention time (rt) and intensity columns."
- [other] Set pandas plotting backend and call .plot() with chromatogram kind parameter: "Set the pandas plotting backend to 'ms_matplotlib' using pd.set_option('plotting.backend', 'ms_matplotlib'). 3. Call the .plot() method on the DataFrame with parameters x='rt', y='intensity',"
- [other] Use 'by' parameter to facet by mass-to-charge when multiple traces present: "Optionally use the 'by' parameter to separate different mass traces if multiple mass-to-charge values are present in the data."
- [other] Save figure using matplotlib savefig for publication and archival: "Save the resulting static figure as a PNG file using matplotlib's savefig() method for publication or archival."
- [readme] pyOpenMS-viz supports multiple plotting backends for static and interactive chromatogram visualization: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Chromatogram is a supported plot type requiring x and y dimensions: "Chromatogram    | x, y                    | chromatogram                                              | ✓              | ✓         | ✓"
- [intro] pyOpenMS-viz integrates seamlessly with plotting backends and leverages pandas: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
