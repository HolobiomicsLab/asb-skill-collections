---
name: ftms-transient-data-loading
description: Use when you have a Bruker Solarix FT-ICR transient file in .d format
  (e.g., ESI_NEG_SRFA.d containing ser and fid files in CompassXtract format) and
  need to programmatically load it into a Python environment for signal processing,
  calibration, and mass spectrum generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - numpy
  - matplotlib
  - Bruker Solarix
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import numpy as np
- from matplotlib import pyplot
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

# ftms-transient-data-loading

## Summary

Load and initialize Bruker Solarix FT-ICR transient raw data files (.d format) into a CoreMS transient object for downstream signal processing and mass spectrum generation. This is the first step in reproducible FT-ICR data workflows where raw time-domain signals must be imported before apodization, zero-filling, and Fourier transformation.

## When to use

You have a Bruker Solarix FT-ICR transient file in .d format (e.g., ESI_NEG_SRFA.d containing ser and fid files in CompassXtract format) and need to programmatically load it into a Python environment for signal processing, calibration, and mass spectrum generation. This is required as the mandatory first step before applying apodization windows, zero-filling, or frequency-domain analysis.

## When NOT to use

- Input is already a processed mass spectrum or centroided peak list—use transient loading only for raw time-domain data.
- Data is from a different vendor (Thermo .raw, MagLab .dat, or Spectroswiss .hdf5)—use the appropriate vendor-specific reader instead.
- Transient file is corrupted or metadata is missing—transient loading requires intact Bruker directory structure and binary headers.

## Inputs

- Bruker Solarix .d directory (containing ser/fid binary files and metadata)
- File path string pointing to the .d directory

## Outputs

- CoreMS ReadBrukerSolarix transient object (in-memory representation)
- Access to raw time-domain signal array
- Access to acquisition metadata (magnetic field, frequency offset, number of data points)

## How to apply

Import the ReadBrukerSolarix class from CoreMS's transient.input.brukerSolarix module and instantiate it with the file path to the .d directory. The loader automatically parses the binary transient data (ser or fid files) and metadata from the Bruker directory structure. Once loaded, the transient object exposes attributes for configurable signal processing: set apodization window functions (e.g., Hanning), zero-fill parameters, and averaging settings before calling the processing pipeline. Verify successful loading by checking that the transient object contains the expected metadata (acquisition parameters, frequency, calibration constants) and that the raw time-domain signal array has non-zero length and finite values.

## Related tools

- **CoreMS** (Framework providing ReadBrukerSolarix class for loading and parsing Bruker Solarix transient binary files) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix** (FT-ICR instrument that acquires and stores transient data in .d directory format)
- **numpy** (Underlying array structure for time-domain signal representation after loading)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix
lt = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d')
print(lt.number_of_data_points, lt.calibration_frequency)
```

## Evaluation signals

- ReadBrukerSolarix object instantiates without file I/O or parsing errors and reports successful load status.
- Transient object exposes metadata attributes (frequency, number of data points, calibration constants) that match Bruker CompassXtract metadata.
- Raw time-domain signal array is non-empty, contains finite numeric values (not NaN or inf), and matches expected data point count from metadata.
- Subsequent apodization and FFT operations on the loaded transient produce a mass spectrum with detected peaks spanning an expected m/z range (e.g., m/z 155–999 for ESI-negative SRFA).

## Limitations

- Supports only Bruker Solarix transients in FT magnitude mode; phase correction and time-domain phase data are not currently extracted.
- Requires intact Bruker .d directory structure with ser and fid files; corrupted or partially deleted directories will cause load failure.
- No automatic vendor format detection—user must select the correct reader (ReadBrukerSolarix vs. Thermo vs. MagLab) before calling the loader.
- Loading does not validate transient quality or flag acquisition anomalies; inspection of metadata and raw signal statistics must follow loading.

## Evidence

- [results] Import and process transient data: "1. Import and process transient data"
- [results] ReadBrukerSolarix class instantiation with file path: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [results] ESI_NEG_SRFA Bruker Solarix dataset: "file_location =  "tests/tests_data/ftms/ESI_NEG_SRFA.d""
- [readme] Supports Bruker Solarix transient formats: "Bruker Solarix transients, ser and fid (FT magnitude mode only)"
- [readme] CoreMS as comprehensive framework for MS data handling: "Data handling and software development for modern mass spectrometry (MS) is an interdisciplinary endeavor requiring skills in computational science and a deep understanding of MS."
