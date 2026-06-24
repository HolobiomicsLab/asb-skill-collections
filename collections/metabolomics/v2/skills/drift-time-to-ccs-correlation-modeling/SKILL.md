---
name: drift-time-to-ccs-correlation-modeling
description: Use when you have tunemix or other reference standards with known m/z,
  drift-time, charge state, and CCS values, and you need to establish a predictive
  calibration model for your ion-mobility mass spectrometry instrument.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
  - numpy
  - deimos.load()
  - deimos.calibration.calibrate_ccs()
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Functionality includes feature detection, feature alignment, collision cross section
  (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- import numpy as np
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drift-time-to-ccs-correlation-modeling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fit a calibration model that converts ion mobility drift times and reference m/z values into collision cross section (CCS) values using the single-field calibration equation (Stow et al. 2017). This skill produces calibration coefficients (beta, tfix) that enable prediction of CCS for unknown ions in positive or negative ion-mobility spectrometry modes.

## When to use

Apply this skill when you have tunemix or other reference standards with known m/z, drift-time, charge state, and CCS values, and you need to establish a predictive calibration model for your ion-mobility mass spectrometry instrument. Use it at the start of an analysis workflow to validate instrument performance (target R² ≥ 0.9999) or to generate coefficients for routine CCS prediction on unknown compounds.

## When NOT to use

- Input data are already converted to CCS values; this skill requires raw drift times.
- Reference standards lack certified CCS values or charge state assignments are unknown.
- Multiple ionization modes are mixed in a single calibration attempt; calibrate positive and negative modes separately.

## Inputs

- HDF5 file containing tunemix reference data (example_tune_pos.h5 or equivalent)
- m/z array (reference standards)
- drift_time array (experimental, in milliseconds or instrument units)
- known CCS array (literature or calibrant values)
- charge state array (integer values, typically +1 or +2 for positive mode)
- buffer gas mass (e.g., 28.014 for N₂)

## Outputs

- Calibration coefficient beta (slope term in single-field equation)
- Calibration coefficient tfix (fixed drift time offset, in milliseconds)
- R² goodness-of-fit metric (scalar, target ≥ 0.9999)
- Fitted calibration model object (usable for CCS prediction on unknowns)

## How to apply

Load reference tunemix data (m/z, drift_time, known CCS, charge) from an HDF5 file using deimos.load(). Call deimos.calibration.calibrate_ccs() with the reference arrays, specifying the calibration mode (positive or negative), buffer gas mass (typically N₂), and any instrument-specific parameters. The routine applies the single-field calibration equation to solve for beta and tfix coefficients that minimize residual error. Extract and validate the returned R² metric against the paper threshold (R² ≥ 0.9999); if R² is below this threshold, investigate reference data quality, charge state assignments, or instrumental drift. Store the fitted coefficients for application to subsequent unknown samples in the same analytical run.

## Related tools

- **DEIMoS** (Python API and CLI for executing calibrate_ccs() routine and loading/managing MS data in HDF5 format) — https://github.com/pnnl/deimos
- **deimos.load()** (Loads tunemix reference data from HDF5 files into memory with column selection) — https://github.com/pnnl/deimos
- **deimos.calibration.calibrate_ccs()** (Core routine that applies single-field calibration equation to compute beta, tfix, and R² metric) — https://github.com/pnnl/deimos
- **numpy** (Array operations and numerical computations for reference data handling)
- **ProteoWizard msconvert** (Optional: converts raw vendor MS formats to mzML for loading into DEIMoS if HDF5 is not available)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); calibration = deimos.calibration.calibrate_ccs(tune_pos['mz'].values, tune_pos['drift_time'].values, tune_pos['ccs'].values, tune_pos['charge'].values, buffer_gas_mass=28.014, mode='positive'); print(f"R-squared: {calibration['r_squared']}"); print(f"beta: {calibration['beta']}, tfix: {calibration['tfix']}")
```

## Evaluation signals

- R² metric is ≥ 0.9999 (paper threshold for acceptable calibration fit)
- Residuals between predicted and known CCS values are normally distributed and centered near zero
- Calibration coefficients (beta, tfix) remain stable when re-fit on subsets of reference data (internal cross-validation)
- CCS predictions on independent validation standards (not used in fitting) fall within ±2% of literature values
- Fitted model generalizes without overfitting: hold-one-out or k-fold CV R² is within 0.0001 of full-fit R²

## Limitations

- Single-field equation assumes a specific buffer gas (e.g., N₂); changing buffer gas requires recalibration.
- Calibration is mode-specific (positive vs. negative); coefficients from positive mode cannot be applied to negative-mode data.
- Drift time measurement precision and reference CCS accuracy directly impact R²; poor-quality reference data will yield low R² even if the model is correct.
- Calibration coefficients may drift with instrument aging or tuning; periodic recalibration (e.g., weekly or monthly) is recommended.
- Isotope and multiply-charged species must be correctly assigned to reference m/z and charge state; misassignment will corrupt the calibration.

## Evidence

- [other] The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute calibration coefficients beta and tfix: "The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute"
- [other] r-squared of 0.9999784552958134 achieved on example tunemix data: "yielding calibration model fit with r-squared of 0.9999784552958134"
- [other] Workflow: Load tunemix positive-mode reference data from example_tune_pos.h5 using deimos.load(): "Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load()"
- [other] Call deimos.calibration.calibrate_ccs() with positive-mode tunemix m/z and drift-time arrays: "Call deimos.calibration.calibrate_ccs() with the positive-mode tunemix m/z and drift-time arrays as input, specifying the calibration mode (positive) and reference CCS standards"
- [other] Validation: confirm R-squared is ≥0.9999 (threshold criterion from paper examples): "Validation: confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples)"
- [readme] DEIMoS provides collision cross section (CCS) calibration functionality: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [readme] Algorithm implementations utilize all dimensions to increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
