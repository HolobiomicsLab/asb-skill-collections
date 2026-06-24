---
name: pandas-dataframe-manipulation-ms-columns
description: Use when when you have raw mass spectrometry data (from mzML, Bruker
  .d, or CSV format) loaded into a Pandas DataFrame and need to ensure it has the
  correct column structure (m/z, retention time, intensity) before invoking pyOpenMS-Viz
  plotting functions like .plot(kind='spectrum'), .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Pandas
  - pyteomics
  - PyOpenMS
  - pymzML
  - alphatims
  - pyOpenMS-Viz
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- leverages the power of Pandas for data manipulation and representation
- ms_data = pd.read_csv("path/to/ms_data.csv")
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

# pandas-dataframe-manipulation-ms-columns

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and structure mass spectrometry data within Pandas DataFrames by organizing and selecting columns for m/z, retention time, and intensity dimensions required by pyOpenMS-Viz plotting methods. This skill ensures data is in the correct format and column names are compatible with the visualization backend.

## When to use

When you have raw mass spectrometry data (from mzML, Bruker .d, or CSV format) loaded into a Pandas DataFrame and need to ensure it has the correct column structure (m/z, retention time, intensity) before invoking pyOpenMS-Viz plotting functions like .plot(kind='spectrum'), .plot(kind='peakmap'), or .plot(kind='chromatogram').

## When NOT to use

- Data is already in a specialized mass spectrometry object format (e.g., pyOpenMS MSSpectrum, MSChromatogram) that does not need DataFrame conversion
- Column structure and naming are already validated and match pyOpenMS-Viz expectations
- Input is binary or proprietary mass spectrometry data that requires vendor-specific parsers before any DataFrame creation

## Inputs

- Pandas DataFrame with mass spectrometry data (loaded from mzML, Bruker .d, CSV, or similar format)
- Column names and data types present in the DataFrame
- Target plot type (spectrum, chromatogram, peakmap, mobilogram)

## Outputs

- Prepared Pandas DataFrame with correctly named and typed columns (m/z, retention time, intensity)
- DataFrame ready for input to pyOpenMS-Viz .plot() method

## How to apply

Load mass spectrometry data into a Pandas DataFrame using appropriate readers (PyOpenMS, pymzML, pyteomics for mzML, or alphatims for Bruker .d format), ensuring the resulting DataFrame contains columns for m/z (mass-to-charge ratio), retention time (rt), and intensity values. Inspect and rename columns as needed to match the expected names used by pyOpenMS-Viz (typically 'x', 'y', 'z' or domain-specific names like 'm/z', 'rt', 'intensity'). Use the 'versatile column selection' feature documented in pyOpenMS-Viz to map your DataFrame columns to the required dimensions for your chosen plot type. Verify column data types are numeric (float or int) before passing the DataFrame to the plotting method. This standardization enables seamless backend switching and ensures consistent API behavior across matplotlib, Bokeh, and Plotly backends.

## Related tools

- **Pandas** (DataFrame data structure and column manipulation for organizing m/z, retention time, and intensity columns)
- **PyOpenMS** (Loading and parsing mass spectrometry data from mzML and native OpenMS formats into Pandas-compatible structures)
- **pymzML** (Alternative parser for mzML mass spectrometry files into DataFrame-ready format)
- **pyteomics** (Alternative parser for mzML mass spectrometry files into DataFrame-ready format)
- **alphatims** (Parser for Bruker .d format mass spectrometry files into DataFrame-ready format)
- **pyOpenMS-Viz** (Visualization library that consumes prepared DataFrames with correctly named m/z, retention time, and intensity columns via the .plot() method) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
ms_data = pd.read_csv('path/to/ms_data.csv')
ms_data.plot(x='m/z', y='intensity', kind='spectrum')
```

## Evaluation signals

- DataFrame contains numeric columns for m/z (mass-to-charge ratio), retention time (rt), and intensity with appropriate float or int dtypes
- Column names match pyOpenMS-Viz expectations or are explicitly mapped to plot method parameters (x, y, z or specific dimension names)
- DataFrame.plot(x='m/z', y='intensity', kind='spectrum') or equivalent call executes without KeyError or TypeError exceptions
- Subsequent .plot(kind='peakmap', plot_3d=True) or other pyOpenMS-Viz plotting methods receive the DataFrame without schema validation errors
- Interactive HTML output from fig.write_html() or static plot objects are successfully generated without data dimension mismatches

## Limitations

- pyOpenMS-Viz 3D PeakMap visualization (plot_3d=True) is only supported by Plotly backend, not matplotlib or Bokeh, so DataFrame structure alone does not guarantee 3D rendering success
- Column selection flexibility requires manual mapping if input data uses non-standard column names; no automatic column detection is guaranteed across all input formats
- Data quality issues (missing values, outliers, non-numeric entries in intensity or m/z columns) are not automatically handled by DataFrame preparation and may cause visualization failures downstream

## Evidence

- [other] Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format), ensuring columns for m/z, retention time, and intensity are present.: "Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format), ensuring columns for m/z, retention time,"
- [readme] Versatile column selection for easy adaptation to different data formats: "Versatile column selection for easy adaptation to different data formats"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
