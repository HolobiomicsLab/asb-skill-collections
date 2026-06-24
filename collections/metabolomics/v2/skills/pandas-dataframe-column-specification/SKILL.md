---
name: pandas-dataframe-column-specification
description: Use when when you have mass spectrometry data in a Pandas DataFrame with
  column names that do not match pyOpenMS-viz's default expectations (e.g., 'm/z'
  vs 'mz' or 'retention_time' vs 'rt'), or when your data uses domain-specific column
  labels (e.g., 'mass_to_charge', 'scan_time', 'peak_intensity').
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pyOpenMS-viz
  - Python
  - Pandas
  - bokeh
  - matplotlib
  - plotly
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from
  pandas dataframes
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pandas-dataframe-column-specification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Specify and map Pandas DataFrame columns to mass spectrometry visualization dimensions (x, y, z axes) to enable flexible adaptation of diverse data formats to pyOpenMS-viz plotting functions. This skill decouples the plotting API from rigid column naming conventions, allowing reuse across different MS data schemas.

## When to use

When you have mass spectrometry data in a Pandas DataFrame with column names that do not match pyOpenMS-viz's default expectations (e.g., 'm/z' vs 'mz' or 'retention_time' vs 'rt'), or when your data uses domain-specific column labels (e.g., 'mass_to_charge', 'scan_time', 'peak_intensity'). Use this skill before calling DataFrame.plot() with kind='spectrum', 'chromatogram', 'mobilogram', or 'peakmap' to ensure the plotting function can locate and correctly interpret your x, y, and z dimensions.

## When NOT to use

- Your DataFrame columns are already named according to pyOpenMS-viz conventions ('m/z', 'rt', 'intensity') and you are not switching between multiple data sources with different schemas.
- You are working with data that has already been preprocessed and reshaped by another tool—verify column names first before applying this skill.
- The visualization does not require explicit column selection (e.g., simple plots with only x and y where column order is unambiguous).

## Inputs

- Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity values

## Outputs

- Column name mappings (string identifiers) ready for use in DataFrame.plot() method calls
- Validated x, y, z parameter assignments passed to plotting functions

## How to apply

Identify the column names in your DataFrame that correspond to the required dimensions for your chosen plot type. For 1D plots (spectrum, chromatogram, mobilogram), you need x and y columns; for 2D plots (peakmap), you need x, y, and z. Pass these column names explicitly as parameters to the DataFrame.plot() method using the x, y, and z arguments—do not rely on implicit column order or naming conventions. For example, if your DataFrame has columns named 'mass_to_charge', 'retention_time', and 'intensity', specify these explicitly when calling plot(x='mass_to_charge', y='retention_time', z='intensity', kind='peakmap'). This mapping isolates your data schema from the visualization backend, allowing seamless switching between matplotlib, bokeh, and plotly backends without rewriting column references.

## Related tools

- **Pandas** (Provides DataFrame structure and plot() method interface for column-aware visualization)
- **pyOpenMS-viz** (Accepts column name parameters (x, y, z) in plotting backend to map DataFrame columns to visualization dimensions) — https://github.com/OpenMS/pyopenms_viz
- **bokeh** (Interactive plotting backend that receives and renders column-specified data)
- **matplotlib** (Static plotting backend that receives and renders column-specified data)
- **plotly** (Interactive plotting backend that receives and renders column-specified data)

## Examples

```
ms_data.plot(x="mass_to_charge", y="retention_time", z="peak_intensity", kind="peakmap", backend="bokeh")
```

## Evaluation signals

- Column names passed to x, y, z parameters match exactly (case-sensitive) to existing DataFrame column names; no KeyError is raised when plot() is called.
- The resulting plot displays data on the correct axes—verify that m/z values appear on the expected axis (typically x for spectrum plots), retention time on the expected axis (typically x for chromatograms), and intensity on the y-axis.
- The plot renders without data corruption or axis label misalignment; visual inspection should show sensible ranges and scale.
- The same DataFrame can be re-plotted with different column specifications for different plot kinds (e.g., spectrum vs. chromatogram) without manual data transformation.
- Column specification successfully enables switching between plotting backends (matplotlib, bokeh, plotly) without changing the x, y, z parameter values.

## Limitations

- Column names are case-sensitive and must match exactly; misspellings or case mismatches will result in KeyError exceptions.
- The skill assumes columns are present in the DataFrame before plotting; it does not handle missing or NaN-filled columns gracefully.
- Z-column (intensity) specification is required for 2D peakmap plots but optional or absent for 1D plots; ensure you provide the correct number of dimensions for your chosen plot kind.
- Column selection does not validate data types or ranges; if a column contains non-numeric or malformed data, the plotting backend may fail or produce incorrect visualizations.
- Multi-index DataFrames or hierarchical column names may require additional handling not covered by simple x, y, z string parameters.

## Evidence

- [readme] Versatile column selection for easy adaptation to different data formats: "Versatile column selection for easy adaptation to different data formats"
- [other] Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names: "Call the DataFrame.plot() method with x and y parameters specifying the m/z and retention time column names, kind='peakmap', and backend='ms_bokeh'"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [other] Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity: "Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity"
