---
name: mass-trace-separation-by-grouping
description: Use when your pandas DataFrame contains mass spectrometry data with retention time (rt) and intensity columns AND a column representing different mass-to-charge (m/z) values or ion identifiers. This is particularly relevant when generating chromatogram plots from data with multiple mass traces (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - pyOpenMS-viz
  - pandas
  - matplotlib
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

# mass-trace-separation-by-grouping

## Summary

Separate multiple mass-to-charge (m/z) traces within a single chromatogram visualization by using the 'by' parameter to group data into faceted subplots. This skill is essential when a mass spectrometry dataset contains multiple ion traces and you need to visualize them as distinct chromatographic profiles rather than as an overlaid composite.

## When to use

Use this skill when your pandas DataFrame contains mass spectrometry data with retention time (rt) and intensity columns AND a column representing different mass-to-charge (m/z) values or ion identifiers. This is particularly relevant when generating chromatogram plots from data with multiple mass traces (e.g., selected ion monitoring or multiple reaction monitoring experiments) where overlaid traces would be difficult to interpret or where regulatory/publication standards require trace-by-trace visualization.

## When NOT to use

- When you have only a single mass trace in your data; use standard (non-grouped) chromatogram plotting instead.
- When your DataFrame does not contain a column suitable for grouping (i.e., no m/z, compound ID, or ion identifier column).
- When you intentionally want to overlay all traces on a single plot for direct intensity comparison across masses.

## Inputs

- pandas DataFrame with columns: retention_time (rt), intensity (y), and mass_trace_identifier (e.g., m/z or ion_id)

## Outputs

- matplotlib Figure object with multiple chromatogram subplots (one per unique mass trace)
- PNG file (optional, via savefig)

## How to apply

Load your mass spectrometry data into a pandas DataFrame with columns for retention time (x-axis), intensity (y-axis), and a grouping column (e.g., m/z or compound identifier). Set the pandas plotting backend to 'ms_matplotlib' using pd.set_option('plotting.backend', 'ms_matplotlib'). Call the .plot() method with parameters x='rt', y='intensity', kind='chromatogram', and crucially add the 'by' parameter set to the name of your grouping column (e.g., by='m_z' or by='ion_id'). pyOpenMS-viz will automatically generate separate chromatogram subplots—one for each unique value in the 'by' column—with aligned axes and consistent styling. The resulting figure can be saved as PNG using matplotlib's savefig() method. The rationale is that faceted visualization prevents visual overlap and makes it easier to assess peak shape, retention time shifts, and intensity patterns within each mass trace independently.

## Related tools

- **pyOpenMS-viz** (Core library providing the .plot() method with 'by' parameter for faceted mass trace separation in pandas DataFrames) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (Data container and manipulation library; provides the DataFrame and plotting backend integration mechanism)
- **matplotlib** (Backend renderer for static faceted chromatogram plots; handles figure layout, axis formatting, and file export)

## Examples

```
ms_data.plot(x="rt", y="intensity", kind="chromatogram", by="m_z")
```

## Evaluation signals

- Output figure contains N subplots, where N equals the count of unique values in the 'by' grouping column.
- Each subplot displays a chromatogram with the correct retention time and intensity values for that mass trace.
- All subplots share consistent axis limits and styling (legend, labels, grid) as per matplotlib conventions.
- PNG file is created without errors and displays readable subplots when opened.
- The 'by' parameter value correctly maps to an existing column name in the DataFrame; mismatched names should raise a KeyError or warning.

## Limitations

- The 'by' parameter requires an exact column name match; typos will cause the plotting call to fail or be silently ignored depending on pandas/pyOpenMS-viz version.
- Faceted layouts may become difficult to read if the number of unique mass traces exceeds ~9–12 (depending on figure size); in such cases, consider filtering or aggregating traces first.
- The matplotlib backend produces static (non-interactive) subplots; for interactive exploration of many traces, consider switching to the bokeh or plotly backend.
- Missing or NaN values in the grouping column may produce unexpected subplots or exclude rows from visualization; data cleaning is recommended beforehand.

## Evidence

- [other] Optionally use the 'by' parameter to separate different mass traces if multiple mass-to-charge values are present in the data.: "Optionally use the 'by' parameter to separate different mass traces if multiple mass-to-charge values are present in the data."
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [other] ms_data.plot(x="rt", y="intensity", kind="chromatogram"): "ms_data.plot(x="rt", y="intensity", kind="chromatogram")"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
