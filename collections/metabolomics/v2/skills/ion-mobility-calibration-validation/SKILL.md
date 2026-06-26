---
name: ion-mobility-calibration-validation
description: Use when when you have positive- or negative-mode ion mobility spectrometry
  data with tunemix reference standards (known m/z, drift times, and CCS values) and
  need to verify that the calibration model accurately captures the relationship between
  drift time, reference m/z, and collision cross.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DEIMoS
  - numpy
  - h5py / HDF5
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# ion-mobility-calibration-validation

## Summary

Validates collision cross section (CCS) calibration coefficients derived from ion mobility spectrometry data by applying the single-field calibration equation to reference standards and assessing model fit quality. This skill ensures that drift time and m/z reference measurements convert to reliable CCS calibration coefficients suitable for downstream ion characterization.

## When to use

When you have positive- or negative-mode ion mobility spectrometry data with tunemix reference standards (known m/z, drift times, and CCS values) and need to verify that the calibration model accurately captures the relationship between drift time, reference m/z, and collision cross section before applying it to unknown analytes.

## When NOT to use

- Input drift times or m/z values are missing, corrupted, or fall outside the instrument's valid range — validation cannot proceed without complete, clean reference data.
- Reference CCS values are not independently verified or traceable to published standards — the calibration will be no more reliable than the reference data itself.
- Calibration is intended for a different ion polarity (e.g., negative-mode coefficients applied to positive-mode unknowns) — the single-field equation is polarity-specific and cross-application will yield systematic bias.

## Inputs

- tunemix reference data file (.h5 format)
- reference m/z values (array)
- experimental drift times (array)
- known CCS values for reference standards (array)
- charge states (array)
- buffer gas mass (scalar, e.g., 28.014 for N2)

## Outputs

- calibration coefficient beta (scalar or array)
- calibration coefficient tfix (scalar)
- r-squared goodness-of-fit metric (scalar)
- fitted polynomial coefficients (array)
- calibration model object

## How to apply

Load tunemix reference data (m/z, drift_time, known CCS values, charge states) from .h5 format using deimos.load(). Call deimos.calibration.calibrate_ccs() with the reference m/z and drift-time arrays, specifying calibration mode (positive or negative) and buffer gas mass to compute calibration coefficients beta and tfix using the single-field calibration equation (Stow et al. 2017). Extract the returned r-squared metric and polynomial coefficients. Validate success by confirming r-squared ≥ 0.9999 (typical threshold from published examples); values below this threshold indicate poor calibration fit and warrant investigation of reference standard quality or instrumental drift. Store the validated coefficients for use in CCS prediction on unknowns.

## Related tools

- **DEIMoS** (Python API housing calibrate_ccs() routine and data loading via deimos.load(); performs single-field calibration equation computation and returns r-squared and coefficients) — http://github.com/pnnl/deimos
- **numpy** (Numerical array operations for handling reference m/z, drift_time, and CCS arrays; supports polynomial coefficient storage and arithmetic)
- **h5py / HDF5** (Underlying file format (.h5) for storing and retrieving tunemix reference data)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); calibration = deimos.calibration.calibrate_ccs(tune_pos['mz'], tune_pos['drift_time'], ccs=tune_pos['ccs'], charge=tune_pos['charge'], mode='positive', buffer_gas_mass=28.014); print(f'R-squared: {calibration.r_squared}')
```

## Evaluation signals

- R-squared value ≥ 0.9999 indicates excellent calibration model fit; r-squared < 0.9999 signals potential reference standard quality issues or instrumental drift requiring re-calibration.
- Calibration coefficients (beta, tfix) remain stable and reproducible across repeated calibration runs with the same reference data — instability suggests instrumental or software inconsistency.
- Residuals (observed drift time minus predicted drift time from calibration model) are randomly distributed around zero with no systematic trend; systematic deviation indicates non-linearity or instrumental artifact not captured by single-field model.
- Calibration coefficients produce CCS predictions on independent validation reference standards (not used to fit the model) that agree with published CCS values to within ±2–3% relative error, confirming external validity.
- Coefficient values and r-squared remain consistent when tunemix data are re-acquired on the same instrument under stable operating conditions; large shifts signal instrumental drift or calibration standard degradation.

## Limitations

- Single-field calibration equation assumes a linear relationship between inverse reduced mobility and CCS; deviations at very high or very low m/z or charge state may introduce systematic error.
- Calibration quality depends critically on the accuracy and stability of reference CCS standards; if reference values are incorrect or standards degrade, the fitted model will be unreliable despite high r-squared.
- The method is polarity-specific; separate calibrations must be performed and validated for positive-mode and negative-mode data — cross-polarity application will introduce systematic bias.
- R-squared ≥ 0.9999 is a typical but not absolute criterion; context-specific thresholds may differ based on instrument performance, sample complexity, or downstream analysis requirements.
- No changelog available in the DEIMoS repository — version-specific behavior or bug fixes are not explicitly documented, requiring careful cross-validation when upgrading.

## Evidence

- [other] The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute calibration coefficients beta and tfix: "calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute"
- [other] Validation: confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples): "confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples)"
- [other] Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load(): "Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load()"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [results] r-squared: 0.9999784552958134: "r-squared: 0.9999784552958134"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
