---
name: bruker-transient-data-import
description: Use when you have Bruker Solarix raw transient data (.d folders containing
  ser or fid files) from an FT-ICR instrument and need to load it into a Python environment
  for noise thresholding, peak picking, mass calibration, or molecular formula assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - Bruker Solarix
  - numpy
  - pandas
  - CoreMS ReadBrukerSolarix
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
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

# bruker-transient-data-import

## Summary

Import and load raw Bruker Solarix FT-ICR transient data (ser and fid files) from .d directories into CoreMS mass spectrum objects for downstream signal processing and calibration. This is the first step in FT-MS workflows, converting vendor binary formats into a unified Python object model.

## When to use

You have Bruker Solarix raw transient data (.d folders containing ser or fid files) from an FT-ICR instrument and need to load it into a Python environment for noise thresholding, peak picking, mass calibration, or molecular formula assignment. Use this when working directly with time-domain data rather than pre-processed peak lists or vendor-exported spectra.

## When NOT to use

- Input is already a centroided or profile peak list (e.g., mzML, .csv, or vendor-exported peak table)—use generic mass list importer instead.
- Data is from a non-Bruker vendor (Thermo .raw, MagLab .dat, Spectroswiss .hdf5)—use vendor-specific importer.
- You only need metadata without the raw transient signal—parse .d XML metadata directly.

## Inputs

- Bruker Solarix .d directory (containing ser and/or fid transient files)
- Bruker CompassXtract acquisition metadata (embedded in .d folder)

## Outputs

- CoreMS mass spectrum object (with raw transient data and metadata)
- Transient signal array (time-domain intensity values)
- Instrument parameters (magnetic field, calibration coefficients, acquisition settings)

## How to apply

Use CoreMS's ReadBrukerSolarix importer to load the transient data from the .d directory path. The importer automatically parses Bruker metadata (acquisition parameters, calibration history) and reconstructs the raw time-domain signal into a CoreMS mass spectrum object. No explicit FFT or apodization is required at import—these are applied in subsequent processing steps. The loaded object contains the transient signal, metadata, and calibration state, enabling direct access to mass spectral hierarchical data structures. Verify import success by confirming the object contains raw signal intensity values and valid frequency/m/z domain metadata.

## Related tools

- **CoreMS ReadBrukerSolarix** (Primary importer that parses Bruker Solarix binary transient files and reconstructs raw FT-ICR signal into CoreMS mass spectrum objects) — https://github.com/EMSL-Computing/CoreMS
- **CoreMS** (Framework providing hierarchical mass spectrometric data structures and downstream processing (apodization, FFT, calibration, peak picking) after transient import) — https://github.com/EMSL-Computing/CoreMS

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; spectrum = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d').get_mass_spectrum()
```

## Evaluation signals

- Returned object is a valid CoreMS mass spectrum instance with non-empty transient signal array and metadata fields populated.
- Transient signal intensity values are numeric (not NaN or null) and match expected data type (typically 32-bit or 64-bit float).
- Instrument metadata (magnetic field strength, acquisition frequency, calibration points) are correctly parsed and accessible via object attributes.
- Mass spectrum object can be passed to downstream CoreMS processing functions (apodization, noise threshold, peak picking) without schema errors.
- For validation datasets (e.g., ESI_NEG_SRFA.d), spectral statistics (peak count, m/z range after FFT) match literature or vendor reports.

## Limitations

- Only FT magnitude mode is supported; magnitude-mode reconstructed transients are required (not complex or phase-corrected data).
- Transient files (ser, fid) must be present and uncorrupted in the .d folder; missing or truncated files will cause import failure.
- Requires Bruker CompassXtract acquisition metadata to be embedded in the .d directory; standalone binary files without metadata cannot be loaded.
- Very large transient files (>1 GB) may require significant memory during loading; processing on systems with <8 GB RAM may be slow or fail.

## Evidence

- [results] The first workflow step in FT-MS signal processing is importing the raw transient data.: "1. Import and process transient data"
- [readme] CoreMS supports direct import of Bruker Solarix transients (ser and fid files) in FT magnitude mode.: "Bruker Solarix transients, ser and fid (FT magnitude mode only)"
- [results] The import is performed using the ReadBrukerSolarix module from CoreMS.: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [results] The ESI_NEG_SRFA dataset is a Bruker FTICR-MS dataset acquired on a 15 Tesla instrument and loaded via the importer.: "We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument"
- [readme] Hierarchical data structures in CoreMS organize access to imported mass spectrometry data.: "The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations."
