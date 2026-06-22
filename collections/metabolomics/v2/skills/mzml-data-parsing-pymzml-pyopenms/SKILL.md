---
name: mzml-data-parsing-pymzml-pyopenms
description: Use when you have mzML-format mass spectrometry data files and need to load them into memory as structured data (pandas DataFrame) to prepare for visualization with pyOpenMS-Viz or other analysis pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-Viz
  - pymzml
  - pyOpenMS
  - AlphaTims
  - pandas
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames
- '.mzML ----- .. toctree:: :maxdepth: 1 pyopenms pymzml'
- pyopenms ... pymzml ... pyteomics
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

# mzML Data Parsing with pymzml and pyOpenMS

## Summary

Parse and load mass spectrometry data from mzML files into pandas DataFrames using pymzml or pyOpenMS libraries, enabling downstream visualization and analysis of chromatograms, spectra, and peak maps.

## When to use

You have mzML-format mass spectrometry data files and need to load them into memory as structured data (pandas DataFrame) to prepare for visualization with pyOpenMS-Viz or other analysis pipelines. This is the first step when working with open-format MS data that supports multiple parsing backends.

## When NOT to use

- Data is already in a pandas DataFrame or other structured format ready for plotting.
- Working with proprietary vendor formats (e.g., Bruker .d) — use AlphaTims instead.
- Data has already been processed and aggregated; you only need to visualize pre-computed summary statistics.

## Inputs

- mzML file (mass spectrometry data in open XML format)
- File path to mzML file (string)

## Outputs

- pandas DataFrame with columns for m/z, intensity, retention time (optional), and/or ion mobility (optional)
- Structured mass spectrometry data ready for visualization or downstream analysis

## How to apply

Install pymzml or pyOpenMS (or both) alongside pyOpenMS-Viz in your environment. Use pymzml.run.Reader() to stream mzML files and extract m/z, intensity, retention time, and ion mobility values, or use pyOpenMS.MSExperiment to load and access spectra programmatically. Extract the relevant dimensions (m/z and intensity for 1D plots, m/z + retention time + intensity for peak maps, or ion mobility + intensity for mobilograms) and load them into a pandas DataFrame with columns named to match your analysis workflow (e.g., 'm/z', 'intensity', 'rt', 'im'). Verify that column names and data types align with the expected inputs for downstream pyOpenMS-Viz plot functions (SpectrumPlot, ChromatogramPlot, MobilogramPlot, PeakMapPlot).

## Related tools

- **pymzml** (Primary mzML parser; streams mzML files and extracts m/z, intensity, retention time, and spectrum metadata)
- **pyOpenMS** (Alternative mzML parser; provides MSExperiment API for programmatic spectrum access and metadata extraction)
- **AlphaTims** (Alternative data loader for proprietary Bruker .d format files containing ion mobility and MS data)
- **pandas** (Data container and manipulation library; DataFrame output structure for parsed MS data)
- **pyOpenMS-Viz** (Downstream plotting library that accepts parsed DataFrames for visualization across multiple backends) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
import pandas as pd
from pymzml import run
reader = run.Reader('example.mzML')
ms_data = pd.DataFrame([(s['m/z array'], s['intensity array']) for s in reader], columns=['m/z', 'intensity'])
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_matplotlib')
```

## Evaluation signals

- DataFrame shape and column names match expected dimensions: at minimum ['m/z', 'intensity'] for spectrum plots; ['rt', 'intensity'] for chromatograms; ['im', 'intensity'] for mobilograms; ['m/z', 'rt', 'intensity'] for peak maps.
- No missing values (NaN) in required columns, or missing values are explicitly handled (forward-fill, interpolation, or row removal).
- Intensity values are numeric (int or float) and non-negative; m/z, retention time, and ion mobility values are numeric and within expected ranges (m/z > 0, rt ≥ 0, im ≥ 0).
- Downstream pyOpenMS-Viz plot function (e.g., df.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_matplotlib')) executes without error and produces a valid output figure.
- Row count and aggregate statistics (sum/mean intensity, m/z range) are consistent with the source mzML file when spot-checked against vendor software or external validation.

## Limitations

- pymzml and pyOpenMS may have different performance characteristics and memory footprints depending on file size and streaming vs. full-load strategy.
- Data quality depends on the mzML encoder; some vendor conversions may lose or distort metadata (e.g., ion mobility bins, scan order).
- No built-in filtering or quality control: peaks below detection threshold, contaminants, or noise must be handled post-parsing by the user.
- Ion mobility data is only available if the source mzML was converted from an instrument that recorded it (e.g., Bruker timsTOF); standard orbitrap or Q-TOF mzML files will lack im column.

## Evidence

- [other] Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame.: "Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame"
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
- [readme] Versatile column selection for easy adaptation to different data formats: "Versatile column selection for easy adaptation to different data formats"
