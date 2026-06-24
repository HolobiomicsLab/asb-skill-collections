---
name: multi-dimensional-data-loading-and-formatting
description: Use when you have raw or processed mass spectrometry data in HDF5 (.h5)
  or mzML format and need to ingest it into DEIMoS for multi-dimensional analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - numpy
  - ProteoWizard msconvert
  - pandas
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python
  application programming interface and command-line tool
- import deimos
- is a Python application programming interface and command-line tool
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-dimensional-data-loading-and-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and parse multi-dimensional mass spectrometry data from diverse file formats (HDF5, mzML) into DEIMoS-compatible data structures, preserving all acquisition dimensions (m/z, drift time, retention time, intensity) needed for downstream feature detection and CCS calibration.

## When to use

You have raw or processed mass spectrometry data in HDF5 (.h5) or mzML format and need to ingest it into DEIMoS for multi-dimensional analysis. Use this skill when your acquisition includes ion mobility or drift time data alongside m/z and retention time, or when you are preparing tunemix reference standards for CCS calibration.

## When NOT to use

- Input is already a feature table or alignment result; use this skill only for raw or minimally processed multi-dimensional spectra.
- Data lacks ion mobility or drift time information; single-dimensional m/z + RT data does not require this skill's multi-dimensional support.
- File format is not HDF5 or mzML; DEIMoS.load() does not handle other mass spec formats (e.g., raw vendor formats without prior conversion via ProteoWizard msconvert).

## Inputs

- HDF5 file (.h5) containing MS1 or MS2 data with key specification
- mzML or mzML.gz file with optional accession dictionary for dimension mapping
- Tunemix reference data in HDF5 format (example_tune_pos.h5, example_tune_neg.h5)

## Outputs

- pandas DataFrame or DEIMoS data structure containing multi-dimensional columns (mz, drift_time, retention_time, intensity)
- Validated data ready for feature detection, alignment, or CCS calibration

## How to apply

Use deimos.load() to read data files, specifying the file path and the HDF5 key (e.g., 'ms1' for MS1 data or 'ms2' for tandem spectra). For mzML files, provide an accession dictionary mapping dimension names to ontology terms (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time). Optionally filter columns to include only required dimensions (mz, drift_time, retention_time, intensity) to reduce memory footprint. Verify the loaded data shape and column names match your expected dimensions before downstream processing. This ensures all N-dimensional information is preserved for simultaneous utilization in alignment and calibration workflows.

## Related tools

- **DEIMoS** (Main API and loader for multi-dimensional mass spectrometry data; provides deimos.load() function for HDF5 and mzML ingestion) — http://github.com/pnnl/deimos
- **ProteoWizard msconvert** (Pre-processing utility to convert vendor mass spectrometry formats to mzML for DEIMoS compatibility)
- **Python** (Programming language in which DEIMoS API calls are executed)
- **pandas** (Underlying DataFrame structure returned by deimos.load() for storing and manipulating multi-dimensional columns)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
```

## Evaluation signals

- Loaded DataFrame contains all expected columns (mz, drift_time, retention_time, intensity) with no NaN values in critical dimensions.
- Data shape and row count match the expected number of scans or data points in the source file.
- m/z values fall within expected mass range (typically 50–2000 Da); drift_time and retention_time are non-negative and monotonically increasing or clustered as expected.
- For tunemix data: known CCS reference values can be paired with m/z and drift_time without missing correspondences.
- Downstream CCS calibration achieves R² ≥ 0.99997, confirming data integrity and correct dimension mapping.

## Limitations

- DEIMoS.load() is largely agnostic to acquisition instrumentation but requires correct accession ontology terms for mzML; mismatched terms will cause dimension mapping failure.
- HDF5 files require explicit key specification; incorrect or missing keys will return empty or null data.
- Large multi-dimensional datasets may exceed memory limits; selective column loading is recommended to reduce footprint.
- Vendor-proprietary formats (.raw, .d, etc.) must be pre-converted to mzML using ProteoWizard; DEIMoS does not directly read raw formats.

## Evidence

- [other] Load tunemix reference data for positive ion mode using deimos.load() specifying the example_tune_pos.h5 file and ms1 key.: "Load tunemix reference data for positive ion mode using deimos.load() specifying the example_tune_pos.h5 file and ms1 key."
- [results] tune_pos = deimos.load('example_tune_pos.h5', key='ms1'): "tune_pos = deimos.load('example_tune_pos.h5', key='ms1')"
- [results] ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']): "ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])"
- [results] data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'}): "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
- [intro] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [results] Conversion to mzML from several other formats can be performed using the free and open-source ProteoWizard msconvert utility.: "Conversion to mzML from several other formats can be performed using the free and open-source ProteoWizard msconvert utility."
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
