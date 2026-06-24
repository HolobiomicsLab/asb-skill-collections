---
name: ccs-calibration-polynomial-fitting
description: Use when you have acquired tunemix or reference standard data in ion
  mobility spectrometry with known m/z, drift time, and CCS values, and you need to
  establish a drift-time-to-CCS mapping for a specific instrument, ionization mode
  (positive or negative), and buffer gas.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
  - numpy
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

# ccs-calibration-polynomial-fitting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fit a polynomial calibration model to convert ion mobility drift times and reference m/z values into collision cross section (CCS) coefficients using the single-field calibration equation. This skill produces calibration coefficients (beta and tfix) that enable downstream CCS prediction for unknown ions in positive- or negative-mode ion mobility spectrometry.

## When to use

Apply this skill when you have acquired tunemix or reference standard data in ion mobility spectrometry with known m/z, drift time, and CCS values, and you need to establish a drift-time-to-CCS mapping for a specific instrument, ionization mode (positive or negative), and buffer gas. The skill is necessary as the first step in any CCS-based feature characterization workflow.

## When NOT to use

- Do not use this skill if reference CCS standards are not available or not accurately characterized; the calibration will be unreliable.
- Do not use this skill if drift time and m/z data have not been properly preprocessed (e.g., baseline-subtracted, aligned) or contain significant instrumental noise; garbage input produces garbage calibration.
- Do not use this skill if switching between ionization modes or buffer gases without recalibrating; calibration coefficients are mode- and gas-specific.

## Inputs

- tunemix reference m/z values (numpy array or pandas Series)
- tunemix experimental drift times (numpy array or pandas Series, units: milliseconds)
- known CCS values for reference standards (numpy array, units: Ų)
- charge states (integer array or scalar)
- buffer gas mass (float, atomic mass units)
- calibration mode identifier (string: 'positive' or 'negative')

## Outputs

- calibration coefficient beta (float)
- calibration coefficient tfix (float)
- R-squared goodness-of-fit metric (float, range 0–1)
- fitted calibration model object (DEIMoS calibration model)

## How to apply

Load reference tunemix data (m/z, drift_time, known CCS values, charge states) from an HDF5 file using deimos.load(). Call deimos.calibration.calibrate_ccs() with the reference m/z and drift_time arrays, specifying the calibration mode (positive or negative), known CCS standards, and buffer gas mass. The function applies the single-field calibration equation (Stow et al. 2017) to solve for calibration coefficients beta and tfix. Extract the returned R-squared metric and polynomial coefficients. Validate that the R-squared value meets the threshold of ≥0.9999; values below this indicate poor model fit and may signal data quality issues, incorrect reference standards, or instrument miscalibration.

## Related tools

- **DEIMoS** (Python API providing calibrate_ccs() function and load() utility for HDF5 file I/O; applies single-field calibration equation to compute beta and tfix coefficients) — https://github.com/pnnl/deimos
- **numpy** (Numerical array operations for m/z, drift_time, and CCS value handling during calibration)
- **Python** (Execution environment and scripting language for DEIMoS API calls and calibration workflow)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); calibration = deimos.calibration.calibrate_ccs(tune_pos['mz'].values, tune_pos['drift_time'].values, known_ccs, charges, buffer_gas_mass, mode='positive')
```

## Evaluation signals

- R-squared metric ≥ 0.9999 (threshold from paper validation examples; values <0.99 indicate poor fit)
- Returned beta and tfix coefficients are finite, positive numbers and match expected physical ranges for the instrument and buffer gas
- Calibration model can be applied to independent test m/z and drift_time pairs and produce CCS predictions within ±5% of known standard values (typical IMS accuracy)
- Residual plot of predicted vs. observed drift times shows random scatter around zero with no systematic bias across m/z or drift_time ranges
- Model coefficients are reproducible when recalibrated with the same reference data (deterministic function)

## Limitations

- Calibration is specific to a single ionization mode (positive or negative) and buffer gas; switching modes requires recalibration.
- Accuracy depends critically on the quality and accuracy of reference CCS standards; contaminated or mislabeled standards will corrupt the model.
- The single-field calibration equation assumes ideal gas behavior and may not account for instrumental nonlinearities or space-charge effects at high ion currents.
- Extrapolation beyond the m/z and drift_time ranges covered by reference standards is not reliable; predictions are most trustworthy within the calibration domain.

## Evidence

- [other] The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute calibration coefficients beta and tfix: "The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute"
- [other] yielding calibration model fit with r-squared of 0.9999784552958134: "yielding calibration model fit with r-squared of 0.9999784552958134"
- [other] Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load(): "Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load()"
- [other] confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples): "confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples)"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
