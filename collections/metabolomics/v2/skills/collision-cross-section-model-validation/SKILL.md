---
name: collision-cross-section-model-validation
description: Use when after applying deimos.calibration.tunemix() to positive-mode or negative-mode tune mix data with known CCS reference compounds (m/z range typically 118–1522), verify that the resulting calibration model achieves the expected r-squared coefficient.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - deimos
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
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
---

# collision-cross-section-model-validation

## Summary

Validate a collision cross section (CCS) calibration model by computing and verifying the goodness-of-fit metric (r-squared) against a known reference value. This skill ensures that the tunemix calibration function produces a single-field CCS model with sufficient accuracy for downstream ion mobility spectrometry analyses.

## When to use

After applying deimos.calibration.tunemix() to positive-mode or negative-mode tune mix data with known CCS reference compounds (m/z range typically 118–1522), verify that the resulting calibration model achieves the expected r-squared coefficient. Use this skill when you need to confirm that instrumental calibration meets performance thresholds (r² ≥ 0.9999) before applying CCS predictions to experimental samples.

## When NOT to use

- Input tune data contains fewer than the standard reference compounds or has m/z values outside the calibrated range (118–1522 m/z).
- The tune reference file is already known to be corrupted, or instrumental parameters (voltage, gas pressure) differ significantly from the calibration acquisition.
- You are validating feature detection or alignment results; this skill is specific to CCS calibration model quality, not peak calling or feature matching confidence.

## Inputs

- HDF5 tune reference file (example_tune_pos.h5 or equivalent negative-mode variant)
- tune mix data containing m/z and known CCS values for reference compounds
- expected r-squared reference value (e.g., 0.9999784552958121)

## Outputs

- r-squared coefficient from calibration model
- validation pass/fail status (boolean)
- calibration model object (usable for CCS prediction on experimental data)

## How to apply

Load the tune reference data from an HDF5 file (e.g., example_tune_pos.h5) using deimos.load() with the appropriate key (e.g., 'ms1'). Apply deimos.calibration.tunemix() to the loaded tune data to fit a single-field collision cross section calibration model using the reference compounds' known CCS values. Extract the r-squared coefficient from the calibration output and compare it to the expected value (typically 0.9999784552958121 for positive-mode tunemix data) to at least 12 decimal places. If the r-squared matches to this precision, the calibration is validated and ready for use; significant deviations indicate instrumental drift or data quality issues requiring recalibration.

## Related tools

- **deimos** (Python API for loading tune reference data and applying tunemix calibration function; extraction of r-squared metric from calibration model output) — https://github.com/pnnl/deimos
- **Python** (Programming environment for loading HDF5 files, invoking deimos functions, and comparing r-squared values to reference threshold)

## Examples

```
import deimos
tune_pos = deimos.load('example_tune_pos.h5', key='ms1')
calibration = deimos.calibration.tunemix(tune_pos)
r2 = calibration['r_squared']
assert abs(r2 - 0.9999784552958121) < 1e-12, f'r-squared {r2} does not match reference'
```

## Evaluation signals

- Computed r-squared value matches the expected reference value to at least 12 decimal places (e.g., 0.9999784552958121).
- Calibration model object is returned without errors or warnings from deimos.calibration.tunemix().
- m/z range of reference compounds spans the expected interval (118.086255–1521.971475 m/z for positive-mode tunemix).
- Single-field calibration model fit indicates excellent goodness-of-fit (r² > 0.9999), confirming linear or near-linear CCS–inverse reduced mobility relationship.
- No NaN or infinite values present in r-squared output; numerical precision is preserved in double-precision floating-point representation.

## Limitations

- Validation is specific to the tunemix reference compounds and acquisition parameters (ionization mode, drift voltage, buffer gas); transferability to different instruments or tune mixes is not guaranteed.
- The r-squared metric alone does not account for systematic bias or residual errors at the extremes of the m/z range; residual plots and outlier analysis are recommended for comprehensive model diagnostics.
- Comparison to 12 decimal places may be sensitive to floating-point rounding differences across operating systems, Python versions, or NumPy versions; a relative tolerance threshold (e.g., < 1e−10) may be more robust.
- No changelog available in the repository documentation; version-to-version changes in the tunemix calibration algorithm are not formally tracked.

## Evidence

- [other] research_question from task_002: "Does the deimos.calibration.tunemix function applied to positive-mode tune mix data produce a collision cross section (CCS) calibration with an r-squared goodness-of-fit of 0.9999784552958121?"
- [other] finding from task_002: "The tunemix calibration on positive-mode tune mix data (m/z 118.086255–1521.971475) with known CCS values yields r-squared: 0.9999784552958121, indicating excellent fit of the single-field"
- [other] workflow step 1 from task_002: "Load the positive-mode tune data from example_tune_pos.h5 using deimos.load() with key 'ms1'"
- [other] workflow step 2 from task_002: "Apply deimos.calibration.tunemix() to the loaded tune data to perform collision cross section calibration using the tune reference compounds."
- [other] workflow step 4 from task_002: "Verify that the computed r-squared value matches the reported value 0.9999784552958121 to at least 12 decimal places."
- [readme] article README intro: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [other] article findings on r-squared: "r-squared: 0.9999784552958121 [section=results; evidence='r-squared:	 0.9999784552958121']"
