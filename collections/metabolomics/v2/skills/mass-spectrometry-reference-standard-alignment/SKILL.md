---
name: mass-spectrometry-reference-standard-alignment
description: Use when you have positive- or negative-mode tunemix reference data (with
  known CCS values, m/z, and measured drift times) and need to establish a calibration
  model for converting observed drift times into CCS values for downstream feature
  annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# mass-spectrometry-reference-standard-alignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Align ion mobility spectrometry (IMS) data to reference standards using drift time and m/z calibration to compute collision cross section (CCS) calibration coefficients via the single-field method. This skill enables quantitative CCS determination and mass calibration accuracy assessment in LC-IMS-MS/MS workflows.

## When to use

Apply this skill when you have positive- or negative-mode tunemix reference data (with known CCS values, m/z, and measured drift times) and need to establish a calibration model for converting observed drift times into CCS values for downstream feature annotation. Use when validation of instrumental calibration quality is required (e.g., commissioning, method validation, or troubleshooting peak identity confidence).

## When NOT to use

- Input data are already calibrated or do not include reference standards with known CCS values.
- Drift time measurements are missing or contain more than negligible gaps/outliers; the single-field method assumes reliable reference-standard drift times.
- Data originate from a different ion mobility platform or buffer gas not represented in your reference standards (cross-platform extrapolation degrades accuracy).

## Inputs

- tunemix reference data file (.h5 format) containing m/z, drift_time, and known CCS values
- reference m/z array (numeric)
- observed drift_time array (numeric)
- known CCS values for reference standards (numeric)
- charge states of reference ions (integer)
- buffer gas mass (numeric, e.g., 28.01 for N₂)
- calibration mode identifier (string: 'positive' or 'negative')

## Outputs

- calibration coefficient beta (numeric)
- calibration coefficient tfix (numeric, fixed drift time offset)
- R-squared fit quality metric (numeric, expected ≥0.9999)
- fitted calibration model object for application to experimental data

## How to apply

Load the tunemix reference dataset (e.g., example_tune_pos.h5) containing reference m/z, drift_time, and known CCS values using deimos.load(). Call deimos.calibration.calibrate_ccs() with the reference m/z and drift_time arrays, specifying the calibration mode (positive or negative), reference CCS standards, charge states, and buffer gas mass. The routine applies the single-field calibration equation (Stow et al. 2017) to compute calibration coefficients beta and tfix. Evaluate calibration model quality by checking that the returned R-squared metric meets the threshold criterion (≥0.9999), confirming the polynomial fit describes the drift-time-to-CCS relationship with negligible residual error. Store the fitted coefficients for application to experimental feature data.

## Related tools

- **DEIMoS** (Primary library providing deimos.calibration.calibrate_ccs() routine and deimos.load() file I/O for tunemix reference data) — https://github.com/pnnl/deimos
- **Python** (Host language for DEIMoS API and calibration coefficient computation)
- **numpy** (Numerical array operations underlying drift-time and m/z array handling)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); calibration = deimos.calibration.calibrate_ccs(mz=tune_pos['mz'], drift_time=tune_pos['drift_time'], ccs=tune_pos['ccs'], charges=tune_pos['charge'], buffer_gas_mass=28.01, mode='positive'); print(f"R-squared: {calibration['r_squared']}"); print(f"beta={calibration['beta']}, tfix={calibration['tfix']}")
```

## Evaluation signals

- R-squared metric equals or exceeds 0.9999 (threshold from paper examples; reported value 0.9999784552958134 indicates excellent fit).
- Calibration coefficients (beta, tfix) are physically plausible: beta > 0 and tfix ≥ 0 (tfix represents fixed instrumental delay).
- Residual drift times (observed - predicted) form a random scatter with mean ≈ 0 and standard deviation < 0.1% of the drift-time range.
- When calibration model is applied to an independent validation set of reference ions, predicted CCS values agree with known values to within instrument tolerance (typically <2% for IMS).
- Calibration coefficients remain stable across repeated calibrations on the same instrument (low drift in beta and tfix across days/runs).

## Limitations

- The single-field calibration equation assumes linear drift-time–to-CCS relationship; nonlinear effects at extreme m/z or CCS ranges may not be captured.
- Calibration accuracy depends on the quality and purity of reference standards; contaminated or aged tunemix standards degrade coefficient reliability.
- Calibration is specific to the ion mode (positive or negative) and buffer gas used during acquisition; changing either requires recalibration.
- The method requires at least 3–4 reference standards spanning the m/z and CCS range of interest for robust polynomial fitting; sparse or clustered references yield high R² but poor extrapolation.

## Evidence

- [results] research_question: "How does the single-field calibration equation convert drift time and reference m/z values into collision cross section (CCS) calibration coefficients for positive-mode ion mobility spectrometry?"
- [results] calibration_workflow: "Load tunemix positive-mode reference data (m/z, drift_time, known CCS values) from example_tune_pos.h5 using deimos.load(). Call deimos.calibration.calibrate_ccs() with the positive-mode tunemix m/z"
- [results] calibration_output: "The calibrate_ccs routine accepts reference m/z values, known CCS values, charge states, experimental drift times, and buffer gas mass, then applies the single-field calibration equation to compute"
- [results] validation_criterion: "Validation: confirm the reported R-squared is ≥0.9999 (threshold criterion from paper examples)."
- [readme] functionality_scope: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] deimos_capability: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
