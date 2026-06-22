---
name: ftms-raw-data-loading-and-parsing
description: Use when you have received raw FT-ICR transient data from Bruker Solarix or ThermoFisher instruments and need to perform signal processing, apodization, calibration, or molecular formula assignment in CoreMS. The data must be in native vendor format (.d directory with ser/fid files, or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - NumPy
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# FT-MS raw data loading and parsing

## Summary

Load vendor-specific Fourier Transform Mass Spectrometry raw transient files (Bruker .d, .ser, .fid; ThermoFisher .raw) and parse them into CoreMS hierarchical data structures with time-domain spectral data, calibration metadata, and instrument parameters intact. This is the essential entry point for any FT-ICR data processing workflow.

## When to use

You have received raw FT-ICR transient data from Bruker Solarix or ThermoFisher instruments and need to perform signal processing, apodization, calibration, or molecular formula assignment in CoreMS. The data must be in native vendor format (.d directory with ser/fid files, or .raw file) rather than centroided mass lists or pre-processed spectra.

## When NOT to use

- Input is already a processed mass list (CSV, Excel, mzML, or centroided peaks) — use direct dataframe/file readers instead
- Input is simulated or synthetic spectrum (use peak-shape simulation modules)
- Data is from vendor instruments not listed (GC-MS, LC-MS profile mode, or non-supported Bruker formats) — verify vendor/format support in CoreMS before attempting load

## Inputs

- Bruker Solarix raw data directory (.d with ser or fid files)
- ThermoFisher .raw file
- Instrument configuration (implicit in vendor file)

## Outputs

- CoreMS Transient object with time-domain spectral data
- Instrument metadata (magnetic field, acquisition frequency, resolving power)
- Calibration reference file path (optional, loaded separately)

## How to apply

Use the CoreMS data factory (MSParameters.encapsulation.factory) to instantiate a raw data object from the vendor file path. The factory automatically detects the instrument vendor and file format, then loads the time-domain transient, instrument configuration (magnetic field, acquisition parameters), and metadata. For Bruker Solarix, point to the .d directory; for ThermoFisher, point to the .raw file. The resulting object exposes the transient as a NumPy array (time-domain spectrum) and instrument parameters. Verify successful load by checking that the transient array has non-zero length and frequency/m/z domain calibration coefficients are present. Store the loaded object for downstream apodization, calibration, and formula search steps.

## Related tools

- **CoreMS** (Primary framework for FT-MS data factory, transient object instantiation, and vendor format detection/parsing) — https://github.com/EMSL-Computing/CoreMS
- **NumPy** (Underlying array data structure for transient time-domain spectral data)
- **Docker** (Container runtime for reproducible CoreMS environment and dependency isolation)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.data_source.ms_data_source import MSDataSource; raw_obj = MSDataSource.from_file(file_location='tests/tests_data/ftms/ESI_NEG_SRFA.d')
```

## Evaluation signals

- Transient object is instantiated without errors; vendor file path is recognized and format auto-detected correctly
- time_domain_spectrum array is non-empty and contains expected numeric range (typically ±1e4 to ±1e8 depending on gain/acquisition)
- Instrument metadata fields (magnetic_field, frequency, resolving_power) are populated with valid numeric values
- Subsequent apodization and FFT steps execute without shape/type mismatch errors, indicating transient is in correct time-domain format
- Loaded transient can be exported and round-tripped (saved and re-loaded) with no data loss

## Limitations

- Only Bruker Solarix (CompassXtract, .d with ser/fid), ThermoFisher .raw, and MagLab ICR .dat formats are supported for raw transients in FT mode; Bruker magnitude-mode is excluded
- Thermo .raw file access on Mac and Linux requires platform-specific handling and dependencies (see README for installation workarounds)
- Raw transient files are large (typically >100 MB); memory constraints may apply on low-resource systems
- Metadata (operator, method, date) varies by vendor and may be incomplete or absent in some file formats; calibration reference data must be supplied separately

## Evidence

- [other] Load ESI_NEG_SRFA.d FT-ICR raw data and SRFA.ref calibration reference using CoreMS data factory: "Load ESI_NEG_SRFA.d FT-ICR raw data and SRFA.ref calibration reference using CoreMS data factory."
- [readme] Bruker Solarix transients, ser and fid (FT magnitude mode only); ThermoFisher (.raw): "Bruker Solarix transients, ser and fid (FT magnitude mode only)
- ThermoFisher (.raw)"
- [readme] CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows from the raw signal to data annotation and curation: "CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows from the raw signal to data annotation and curation."
- [readme] The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations: "The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations."
- [results] file_location = 'tests/tests_data/ftms/ESI_NEG_SRFA.d': "file_location =  "tests/tests_data/ftms/ESI_NEG_SRFA.d""
