---
name: calibration-coefficient-accuracy-assessment
description: Use when after applying deimos.calibration.tunemix() to positive-mode
  or negative-mode tune mix reference data (containing known CCS values across m/z
  range 118–1522), assess whether the single-field calibration model's r-squared coefficient
  meets the expected precision (typically ≥0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
  - NumPy
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
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

# calibration-coefficient-accuracy-assessment

## Summary

Verify that a collision cross section (CCS) calibration model applied to tuning reference compounds achieves a target goodness-of-fit (r-squared) by computing and comparing the calibration coefficient to a reference value at high precision. This skill ensures the calibration meets the statistical accuracy threshold required for reliable ion mobility–mass spectrometry workflows.

## When to use

After applying deimos.calibration.tunemix() to positive-mode or negative-mode tune mix reference data (containing known CCS values across m/z range 118–1522), assess whether the single-field calibration model's r-squared coefficient meets the expected precision (typically ≥0.9999) to validate that the instrumental tuning and calibration pipeline is functioning within specification.

## When NOT to use

- Input data do not contain reference compounds with independently verified CCS values.
- Tune data are already processed or aligned; this skill targets raw tune mix spectra only.
- The m/z range of the tune compounds falls outside the instrument's calibration range (typically 118–1522 m/z).

## Inputs

- Tune reference data (HDF5 format, e.g., example_tune_pos.h5)
- Tune reference compound library with known m/z and CCS values
- DEIMoS calibration configuration parameters

## Outputs

- Calibration model object with r-squared goodness-of-fit coefficient
- Numerical r-squared value (float, precision ≥12 decimal places)
- Pass/fail assessment (whether r-squared meets threshold)

## How to apply

Load the tune reference data (e.g., example_tune_pos.h5) using deimos.load() with the 'ms1' key; apply deimos.calibration.tunemix() to generate the calibration model; extract the r-squared coefficient from the model output; compare the computed r-squared to the reference value (0.9999784552958121 for positive mode) to at least 12 decimal places. The tunemix function leverages known m/z–CCS pairs in the reference compounds to fit a single-field calibration, and high r-squared (>0.9999) indicates the model captures the relationship with minimal residual variance, validating both the reference data quality and the calibration algorithm's stability.

## Related tools

- **DEIMoS** (Python API and command-line tool that provides deimos.load() for HDF5 ingestion and deimos.calibration.tunemix() for single-field CCS calibration model fitting) — https://github.com/pnnl/deimos
- **Python** (Runtime environment for executing deimos API calls and numerical comparison of calibration coefficients)
- **NumPy** (Optional numerical library for precision arithmetic and coefficient comparison)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); calibration = deimos.calibration.tunemix(tune_pos); r_squared = calibration.score; print(f'R-squared: {r_squared:.13f}'); assert abs(r_squared - 0.9999784552958121) < 1e-12, 'Calibration r-squared does not match expected value'
```

## Evaluation signals

- Computed r-squared matches reference value (0.9999784552958121 for positive-mode tunemix) to at least 12 decimal places.
- R-squared coefficient is ≥0.9999, indicating excellent fit of the single-field calibration model.
- No exceptions or data loading errors occur during deimos.load() and deimos.calibration.tunemix() execution.
- The m/z range of the tune compounds in the input data spans the expected range (118.086255–1521.971475 m/z).
- Output calibration model is serializable and can be applied downstream to experimental ion mobility–mass spectrometry data.

## Limitations

- The reference r-squared value (0.9999784552958121) is specific to positive-mode tune mix data; negative-mode or alternative tune compounds may yield different coefficients.
- Precision of r-squared comparison depends on floating-point arithmetic in Python and the underlying calibration library; minor deviations (<1e-13) due to platform or library version differences should be tolerated.
- The single-field calibration model assumes a linear or polynomial relationship between m/z (or drift time) and CCS; nonlinear or multi-field effects are not captured by this assessment alone.
- High r-squared does not guarantee that the calibration will perform well on diverse biological analytes; it only validates fit to the reference compounds.

## Evidence

- [other] The tunemix calibration on positive-mode tune mix data (m/z 118.086255–1521.971475) with known CCS values yields r-squared: 0.9999784552958121, indicating excellent fit of the single-field calibration model.: "The tunemix calibration on positive-mode tune mix data (m/z 118.086255–1521.971475) with known CCS values yields r-squared: 0.9999784552958121, indicating excellent fit of the single-field"
- [other] Load the positive-mode tune data from example_tune_pos.h5 using deimos.load() with key 'ms1'. Apply deimos.calibration.tunemix() to the loaded tune data to perform collision cross section calibration using the tune reference compounds. Extract the r-squared coefficient from the calibration model output. Verify that the computed r-squared value matches the reported value 0.9999784552958121 to at least 12 decimal places.: "Load the positive-mode tune data from example_tune_pos.h5 using deimos.load() with key 'ms1'. Apply deimos.calibration.tunemix() to the loaded tune data to perform collision cross section calibration"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation; algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
- [results] tune_pos = deimos.load('example_tune_pos.h5', key='ms1'): "tune_pos = deimos.load('example_tune_pos.h5', key='ms1')"
