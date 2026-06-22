---
name: mass-spectrometry-data-preparation
description: Use when you have raw mass spectrometry data in CSV or mzML format and need to visualize it using pyOpenMS-viz, or you are working with MS data that contains retention time (rt), m/z, intensity, and optionally ion mobility dimensions that must be structured as a Pandas DataFrame before plotting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-viz
  - Python
  - Pandas
  - OpenMS
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

# mass-spectrometry-data-preparation

## Summary

Load mass spectrometry data from CSV or mzML files into a Pandas DataFrame with properly named columns (m/z, retention time, intensity, ion mobility) to enable downstream visualization and analysis. This skill ensures data is in the standardized tabular format required by pyOpenMS-viz and other MS analysis libraries.

## When to use

You have raw mass spectrometry data in CSV or mzML format and need to visualize it using pyOpenMS-viz, or you are working with MS data that contains retention time (rt), m/z, intensity, and optionally ion mobility dimensions that must be structured as a Pandas DataFrame before plotting.

## When NOT to use

- Input data is already a properly formatted and named Pandas DataFrame — skip directly to visualization.
- You require preprocessing steps (e.g., peak picking, deisotoping, mass calibration) before visualization — use OpenMS algorithms upstream first.
- Data must remain in native mzML/raw format for compliance or archival — prepare a copy for visualization without modifying originals.

## Inputs

- CSV file containing mass spectrometry data with columns for m/z, retention time (or ion mobility), and intensity
- mzML file (mass spectrometry data file format)
- Pandas DataFrame (when data is already partially prepared but requires column name standardization)

## Outputs

- Pandas DataFrame with standardized column names (m/z, rt or ion_mobility, intensity)
- DataFrame ready for pyOpenMS-viz .plot() method calls

## How to apply

Load the mass spectrometry file (CSV or mzML) into a Pandas DataFrame ensuring it contains required columns: m/z (mass-to-charge ratio), retention time (rt) or ion mobility, and intensity values. Verify column names match the expected schema for your chosen plot type (e.g., 'chromatogram' requires x and y dimensions; 'peakmap' requires x, y, and z). Use versatile column selection to adapt to different data formats if column names differ from defaults. The DataFrame becomes the input object for all downstream pyOpenMS-viz plotting operations via the .plot() method, which dispatches to the selected backend (matplotlib, bokeh, or plotly).

## Related tools

- **Pandas** (DataFrame structure and data manipulation for loading and standardizing MS data column names) — https://pandas.pydata.org
- **pyOpenMS-viz** (Downstream plotting library that consumes prepared DataFrames and generates MS visualizations) — https://github.com/OpenMS/pyopenms_viz
- **OpenMS** (Source library for mzML file format support and MS data structure) — https://github.com/OpenMS/OpenMS

## Examples

```
import pandas as pd
ms_data = pd.read_csv('ms_data.csv')
ms_data.columns = ['m/z', 'rt', 'intensity']
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_matplotlib')
```

## Evaluation signals

- DataFrame contains all required columns (m/z, rt or ion_mobility, intensity) with no missing values in critical rows
- Column names match expected schema for the target plot kind (e.g., 'chromatogram' has 'rt' and 'intensity' columns)
- Data types are numeric (float or int) for all coordinate and intensity columns
- DataFrame.plot() method executes without column-not-found errors when passed x, y, and optionally z parameters
- Resulting plot renders correctly in the selected backend (matplotlib, bokeh, or plotly) with no data binding errors

## Limitations

- pyOpenMS-viz expects specific column naming conventions; if source data uses non-standard names (e.g., 'mz' instead of 'm/z'), manual column renaming is required.
- The library supports versatile column selection but assumes rectangular (2D) or 3D tabular structure; ragged or hierarchical MS data formats may require flattening.
- mzML file loading and MS-specific preprocessing (e.g., centroiding, smoothing) are outside the scope of this skill; use OpenMS algorithms or pyOpenMS for those steps.
- Large MS datasets (millions of scans) may encounter memory constraints in Pandas; consider subsampling or chunked loading for very high-dimensional data.

## Evidence

- [other] Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity.: "Load mass spectrometry data into a Pandas DataFrame with columns for m/z, retention time (or ion mobility), and intensity."
- [other] Load mass spectrometry data into a pandas DataFrame from a deposited CSV or mzML file containing retention time (rt) and intensity columns.: "Load mass spectrometry data into a pandas DataFrame from a deposited CSV or mzML file containing retention time (rt) and intensity columns."
- [readme] Versatile column selection for easy adaptation to different data formats: "Versatile column selection for easy adaptation to different data formats"
- [other] Plot directly from a pandas dataframe object: "Plot directly from a pandas dataframe object"
- [intro] provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data: "provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data"
