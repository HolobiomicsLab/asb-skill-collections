---
name: mass-spectrometry-data-parsing-mzml-bruker
description: Use when you have raw mass spectrometry data in mzML or Bruker .d format
  and need to ingest it into a tabular format (pandas DataFrame) for visualization,
  statistical analysis, or integration with other Python-based mass spectrometry tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyteomics
  - pymzML
  - alphatims
  - PyOpenMS
  - pandas
  techniques:
  - mass-spectrometry
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-parsing-mzml-bruker

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and parse mass spectrometry data from mzML and Bruker .d format files into pandas DataFrames with properly mapped columns (m/z, retention time, intensity). This is a prerequisite for downstream visualization and analysis of mass spectrometry datasets.

## When to use

You have raw mass spectrometry data in mzML or Bruker .d format and need to ingest it into a tabular format (pandas DataFrame) for visualization, statistical analysis, or integration with other Python-based mass spectrometry tools. Use this skill when you need columns explicitly mapped to m/z, retention time, and intensity for downstream plotting or filtering operations.

## When NOT to use

- Data is already loaded into a pandas DataFrame with correctly named columns — skip parsing and proceed directly to visualization.
- You need raw binary or spectral metadata (e.g., precursor m/z, charge state, scan indices) that goes beyond peak-level m/z, RT, intensity — consider using lower-level APIs like pyOpenMS or mzML schema directly.
- Working with vendor-specific, proprietary formats other than mzML or Bruker .d — confirm your file format is supported by the chosen parser library.

## Inputs

- mzML file (XML-based mass spectrometry data format)
- Bruker .d directory (proprietary mass spectrometry data format)
- File path or directory path to raw mass spectrometry data

## Outputs

- pandas DataFrame with columns for m/z, retention time, and intensity
- Structured tabular representation of mass spectrometry peaks

## How to apply

Select the appropriate parser based on your file format: use pymzML or pyteomics for mzML files, or alphatims for Bruker .d format files. Load the raw file using the format-specific library's reader function, then extract the m/z, retention time (RT), and intensity values and organize them into a pandas DataFrame with clearly named columns ('m/z', 'rt', 'intensity'). Verify that numeric columns are properly typed (float64 for m/z and intensity, numeric for RT) and that no data loss occurred during parsing by spot-checking row counts and value ranges against the original file metadata. This structured DataFrame then serves as input to visualization backends (matplotlib, Bokeh, Plotly) or further analysis steps.

## Related tools

- **pymzML** (Parse mzML files and extract m/z, retention time, and intensity data)
- **pyteomics** (Parse mzML files as an alternative to pymzML)
- **alphatims** (Parse Bruker .d format files and extract mass spectrometry data)
- **PyOpenMS** (Alternative low-level interface for reading and manipulating OpenMS-compatible mass spectrometry data formats) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (Container and manipulation framework for the parsed mass spectrometry DataFrame)

## Examples

```
import pandas as pd; from pymzml import MzML; ms_data = pd.DataFrame([(s['m/z array'], s['intensity array'], s['scan time']) for s in MzML('file.mzML')]); ms_data.columns = ['m/z', 'intensity', 'rt']
```

## Evaluation signals

- DataFrame shape is non-empty and contains expected number of rows (peaks) matching file summary statistics or spot-check against original file viewer.
- Column names exactly match expected keys: 'm/z', 'rt' (or 'retention_time'), 'intensity' — case and underscores must be consistent with downstream visualization API.
- Data types are numeric (float64 or int64) for m/z, RT, and intensity; no NaN values in critical columns or NaNs are documented and handled.
- Value ranges are physically plausible: m/z typically 50–2000+; intensity > 0; retention time in expected range for your chromatography method.
- Random row sampling shows realistic peak triplets (e.g., m/z ≈ 500, RT ≈ 5.2 min, intensity ≈ 1e4) matching domain expectations for the sample type.

## Limitations

- Parser library must support your specific mzML dialect or Bruker .d version; older file formats may require vendor-specific tools or format conversion.
- Large files (>1 GB) may require streaming or chunked parsing to fit in memory; simple DataFrame loading may fail or be slow for gigantic datasets.
- Metadata beyond peak-level data (scan-level info, precursor m/z, collision energy, instrument config) is often discarded during parsing to the simple m/z–RT–intensity table — retrieve from raw file if advanced filtering is needed.
- Parsing performance and memory footprint depend on file size and parser efficiency; no benchmarks provided for specific file sizes or hardware.

## Evidence

- [other] Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format): "Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format)"
- [other] ensuring columns for m/z, retention time, and intensity are present: "ensuring columns for m/z, retention time, and intensity are present"
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] leverages the power of Pandas for data manipulation and representation: "leverages the power of Pandas for data manipulation and representation"
