---
name: collision-cross-section-calibration
description: Use when you have LC-IMS-MS/MS data with drift_time measurements and need to convert raw drift times into calibrated CCS values for structural annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - Snakemake
  - HDF5 / h5py
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment with required dependencies.
- 'Install DEIMoS using `pip <https://pypi.org/project/pip/>`_: ``pip install -e .``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
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

# collision-cross-section-calibration

## Summary

Calibrate collision cross section (CCS) values for ion mobility spectrometry data by mapping observed drift times to reference CCS standards. This skill enables accurate structural characterization of detected features across multidimensional LC-IMS-MS datasets.

## When to use

Apply this skill when you have LC-IMS-MS/MS data with drift_time measurements and need to convert raw drift times into calibrated CCS values for structural annotation. Use it after feature detection has identified peaks in the mz-drift_time-retention_time space but before final feature characterization, particularly when comparing features across multiple samples or when CCS values are required for compound identification.

## When NOT to use

- Input data lacks drift time dimension (e.g., conventional LC-MS without ion mobility) — CCS calibration requires the separation axis that drift time provides.
- No appropriate reference standards are available or the reference dataset does not cover the mass range of analytes — calibration accuracy depends on reference compound coverage.
- Feature detection has not yet been completed and drift times are not assigned to detected peaks — CCS calibration operates downstream of peak picking and feature definition.

## Inputs

- Detected MS features with mz, drift_time, retention_time, and intensity columns (HDF5 format: .h5 files with 'ms1' or 'ms2' keys)
- Reference tuning dataset with known CCS standards and corresponding drift times (e.g., 'example_tune_pos.h5')
- Raw LC-IMS-MS/MS data in mzML.gz format with MS:1002476 (drift_time) accession fields

## Outputs

- Feature table with calibrated CCS values added as a column alongside mz, drift_time, retention_time, intensity
- Calibration curve parameters (polynomial or linear coefficients, r-squared goodness-of-fit)
- Aligned feature set with CCS-based cross-sample matching confidence

## How to apply

DEIMoS CCS calibration uses reference tuning compounds with known CCS values to establish a drift_time-to-CCS mapping function. Load reference data (e.g., 'example_tune_pos.h5') containing calibrant masses and their corresponding CCS values, then apply polynomial or linear regression to fit the relationship between observed drift times and reference CCS standards. The calibration function is applied to all detected features' drift_time values to produce calibrated CCS estimates. Verify calibration quality by checking r-squared values (DEIMoS reports values >0.999) and by confirming that features from replicate samples converge to similar CCS values after alignment, indicating successful cross-run calibration fidelity.

## Related tools

- **DEIMoS** (Provides CCS calibration API (deimos.calibrate_ccs) and CLI integration; loads mzML/HDF5 data and applies drift-time-to-CCS mapping) — https://github.com/pnnl/deimos
- **Python** (Language for implementing calibration fitting (numpy polyfit, scipy regression) and data manipulation)
- **Snakemake** (Workflow orchestration tool for integrating CCS calibration as a DAG rule step after feature detection and before alignment)
- **HDF5 / h5py** (File format and I/O library for storing and retrieving feature tables and reference calibration data)

## Examples

```
import deimos; tune = deimos.load('example_tune_pos.h5', key='ms1'); features = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'intensity']); ccs_calibrated = deimos.calibrate_ccs(features, tune_data=tune)
```

## Evaluation signals

- Calibration fit r-squared ≥ 0.999 (DEIMoS reports ~0.9999784552958134), indicating tight linear or polynomial relationship between drift_time and reference CCS.
- CCS values for replicate features across aligned samples converge to within expected tolerance (e.g., <2% variation), confirming cross-run calibration consistency.
- Calibrated CCS values fall within literature-reported ranges for known compounds (e.g., small molecules 100–400 Ų, peptides 300–800 Ų), validating physical plausibility.
- Feature alignment confidence increases post-calibration because CCS becomes an additional matching dimension, reducing false-positive feature associations.
- No systematic drift in calibration residuals across the mass or drift_time range, indicating the fitted model is not biased toward particular compound classes.

## Limitations

- CCS calibration accuracy depends critically on the availability and mass-range coverage of reference standards; sparse or poorly distributed calibrants lead to extrapolation errors outside their domain.
- Assumes a stable, instrument-specific drift-time-to-CCS relationship; instrumental drift or changes in gas/temperature conditions between reference and sample acquisition will degrade calibration fidelity.
- N-dimensional simultaneous utilization of all dimensions improves detection and alignment, but CCS calibration is sensitive to the quality of upstream feature detection; poor peak picking propagates into miscalibrated features.
- DEIMoS operates on N-dimensional data largely agnostic to acquisition instrumentation; however, the drift_time field naming and accession codes (MS:1002476) must be correctly mapped during mzML parsing, or calibration will fail silently.

## Evidence

- [intro] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [other] DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering and persistent homology-based peak detection: "DEIMoS loads mzML.gz files by parsing accession fields (e.g., 'MS:1000016' for retention_time, 'MS:1002476' for drift_time), then applies threshold filtering (threshold=500), index building from"
- [results] r-squared: 0.9999784552958134 demonstrating high-fidelity calibration fit: "r-squared:	 0.9999784552958134"
- [intro] algorithm implementations simultaneously utilize all dimensions to increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
