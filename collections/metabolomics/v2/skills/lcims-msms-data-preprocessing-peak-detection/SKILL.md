---
name: lcims-msms-data-preprocessing-peak-detection
description: Use when you have loaded mzML.gz or HDF5-formatted raw LC-IMS-MS/MS data and need to identify discrete peaks before feature alignment. Use it if your goal is to reduce noise, increase signal-to-noise ratio, and prepare multi-dimensional data for cross-sample feature matching and CCS calibration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - conda
  - pip
  - Python
  - Snakemake
  - ProteoWizard
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
- import deimos
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
- is a Python application programming interface and command-line tool
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-IMS-MS/MS Data Preprocessing and Peak Detection

## Summary

Detect and characterize peaks in high-dimensional mass spectrometry data by applying intensity thresholding and leveraging simultaneous utilization of all acquisition dimensions (m/z, drift time, retention time) to improve detection sensitivity and separation between features. This preprocessing step converts raw or loaded spectral data into a peaked feature table suitable for downstream alignment and characterization.

## When to use

Apply this skill when you have loaded mzML.gz or HDF5-formatted raw LC-IMS-MS/MS data and need to identify discrete peaks before feature alignment. Use it if your goal is to reduce noise, increase signal-to-noise ratio, and prepare multi-dimensional data for cross-sample feature matching and CCS calibration.

## When NOT to use

- Input is already a feature table (aligned across samples) — proceed directly to feature characterization steps (CCS calibration, isotope detection)
- You require untargeted detection of very low-abundance features below your instrument's baseline noise — consider alternative noise modeling or MS/MS signal enhancement before peak detection
- Data lacks complete multi-dimensional metadata (e.g., drift_time or retention_time fields are missing) — first reconcile data format with DEIMoS accession requirements

## Inputs

- mzML.gz files (raw LC-IMS-MS/MS spectra with MS1 and MS2 data)
- HDF5 datasets (pre-loaded spectral data with keys ms1 or ms2, containing columns: m/z, drift_time, retention_time, intensity)
- Example files: example_data.mzML.gz, example_data.h5

## Outputs

- Peaked feature table (HDF5 format, key ms1_peaks or equivalent)
- Multi-dimensional peak array with columns: m/z, drift_time, retention_time, intensity
- Example file: example_data_peaks.h5

## How to apply

Load raw MS data (mzML.gz or HDF5 format) into the DEIMoS API with explicit dimension accessions (retention_time, drift_time, m/z). Apply intensity-based thresholding using `deimos.threshold()` with an appropriate threshold parameter (e.g., 500–1000 counts) to remove low-intensity noise and retain signal peaks. DEIMoS peak detection algorithms simultaneously utilize all dimensions to achieve greater separation between features and improved detection sensitivity compared to single-dimension approaches. Verify completion by confirming the output peaked table contains expected dimensions and has non-zero row counts with intensity values above the threshold. The exact threshold value should be empirically determined from your instrument's noise floor and calibration data.

## Related tools

- **DEIMoS** (Python API and CLI for multi-dimensional peak detection, thresholding, and feature preprocessing on N-dimensional MS data) — https://github.com/pnnl/deimos
- **Snakemake** (Workflow orchestration engine that executes DEIMoS peak detection rules within the complete feature alignment DAG)
- **ProteoWizard** (Pre-processing utility to convert raw MS formats to mzML for input to DEIMoS)
- **conda** (Environment and dependency manager for installing DEIMoS and its Python runtime prerequisites)
- **Python** (Runtime language for DEIMoS API; enables programmatic threshold filtering and data loading)

## Examples

```
ms1 = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'}); ms1_peaks = deimos.threshold(ms1, threshold=500)
```

## Evaluation signals

- Output HDF5 file is present in output/ directory and contains the 'ms1_peaks' (or equivalent) key with non-zero row count
- All peaks in output table have intensity values strictly greater than the applied threshold parameter (e.g., > 500 or > 1000)
- Dimensions (m/z, drift_time, retention_time, intensity) are present and non-null in the peaked feature table
- Peak count is lower than the raw spectral point count, confirming that thresholding removed noise points
- Downstream feature alignment (via deimos.alignment or Snakemake feature_alignment rule) proceeds without error, indicating the peaked data schema is compatible with next-stage processing

## Limitations

- Peak detection threshold is user-specified and instrument-dependent; incorrect threshold values may either remove true low-abundance features or retain excessive noise, affecting downstream alignment and detection sensitivity.
- Algorithm performance relies on complete multi-dimensional data; missing drift_time or retention_time fields will degrade feature separation and alignment confidence.
- N-dimensional peak detection does not inherently resolve isobaric or co-eluting species; isotope detection and MS/MS deconvolution are separate downstream steps required for full characterization.
- DEIMoS is agnostic to instrumentation, but raw data must be converted to mzML format with correct accession tags; unconventional or vendor-proprietary formats may require ProteoWizard pre-processing.

## Evidence

- [intro] Feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [intro] Multi-dimensional approach improves detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
- [results] Intensity threshold of 500 applied to raw data: "ms1 = deimos.threshold(ms1, threshold=500)"
- [results] Intensity threshold of 1000 applied to peaked data: "ms1_peaks = deimos.threshold(ms1_peaks, threshold=1000)"
- [intro] DEIMoS operates on N-dimensional data agnostic to instrument: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [results] Loading raw mzML.gz with dimension accessions: "data = deimos.load('example_data.mzML.gz', accession={'retention_time': 'MS:1000016', 'drift_time': 'MS:1002476'})"
- [other] Peak detection output formats: "ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])"
