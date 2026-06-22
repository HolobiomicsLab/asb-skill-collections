---
name: polynomial-regression-quality-assessment
description: Use when after fitting a polynomial calibration model to tunemix reference data in DEIMoS, assess whether the model explains sufficient variance in the m/z–drift-time–CCS relationship.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - Python
  - numpy
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# polynomial-regression-quality-assessment

## Summary

Evaluate the goodness-of-fit of a polynomial calibration model by computing and validating the coefficient of determination (R²) against a predefined threshold, ensuring that the m/z–drift-time–CCS relationship meets required accuracy standards for collision cross section calibration.

## When to use

After fitting a polynomial calibration model to tunemix reference data in DEIMoS, assess whether the model explains sufficient variance in the m/z–drift-time–CCS relationship. Use this skill when you have established a tunemix calibration object with fitted coefficients and need to verify that the R² value meets or exceeds the ≥0.99997 threshold for positive or negative ion mode data before applying the calibration to unknown samples.

## When NOT to use

- Input is a feature table or aligned features rather than tunemix reference standards; R² assessment applies only to reference calibration data with known CCS values.
- Calibration model has not yet been fitted; R² is undefined before model.fit() is called.
- Goal is to evaluate prediction accuracy on held-out test samples rather than reference data; this skill assesses fit quality on the training set, not generalization.

## Inputs

- fitted DEIMoS calibration object (ccs_cal) with tunemix reference data
- known CCS values and m/z-to-CCS mapping for tunemix standards
- positive or negative ion mode tunemix data (e.g., example_tune_pos.h5 or equivalent)

## Outputs

- R² metric (scalar, range 0–1)
- pass/fail validation result against 0.99997 threshold
- fitted calibration coefficients (retained from calibration object)

## How to apply

Following calibration model fitting via deimos calibration.fit(), extract the R² metric from the fitted model by squaring the correlation coefficient (ccs_cal.fit['r'] ** 2). Compare the computed R² value directly against the threshold of 0.99997; if R² is equal to or greater than this threshold, the model is acceptable for downstream CCS prediction. The high threshold (≥0.99997) reflects the need for precise m/z–drift-time–CCS mapping in ion mobility-mass spectrometry workflows. Document both the R² value and its comparison outcome for each ion mode separately (positive and negative), as the calibration performance may differ between modes.

## Related tools

- **DEIMoS** (Python API and command-line tool for calibration object initialization, model fitting, and R² extraction from fitted polynomial coefficients) — http://github.com/pnnl/deimos
- **Python** (Programming language for arithmetic operations (squaring correlation coefficients) and threshold comparison logic)
- **numpy** (Numerical library for array operations and statistical calculations underlying R² computation)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); ccs_cal = deimos.CCSCalibration(tune_pos, known_ccs_values); ccs_cal.fit(); r_squared = ccs_cal.fit['r'] ** 2; print('R-squared:', r_squared); assert r_squared >= 0.99997, f'Calibration failed: R² = {r_squared}'
```

## Evaluation signals

- R² value is a scalar between 0 and 1 (inclusive) with no NaN or inf values.
- R² ≥ 0.99997 for positive ion mode tunemix data and R² ≥ 0.99997 for negative ion mode tunemix data independently.
- R² values computed from the same tunemix dataset are reproducible (same fitted coefficients yield identical R² on repeated extraction).
- R² is derived from a fitted polynomial model that maps m/z and drift_time to CCS using tunemix reference standards with known CCS values.
- Pass/fail decision is documented separately for each ion mode, confirming calibration quality before applying the model to unknown samples.

## Limitations

- R² measures goodness-of-fit on the training data (tunemix reference set) and does not directly assess generalization to unknown samples or different ion types.
- The 0.99997 threshold is specific to DEIMoS tunemix calibration and may not be appropriate for other calibration approaches or reference standards.
- R² is sensitive to polynomial degree; lower-degree polynomials may yield lower R² even if the relationship is adequately captured for practical purposes.
- Separate tunemix datasets (positive vs. negative ion mode) are required; a single ion mode's calibration cannot be directly applied to the other without re-assessment.

## Evidence

- [results] R-squared threshold and ion mode specificity: "Does the DEIMoS tunemix calibration function produce collision cross section (CCS) calibration coefficients that achieve R-squared values ≥0.99997 when applied to positive and negative ion mode tune"
- [results] Observed R² values meeting threshold: "The DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134, both exceeding"
- [results] Extraction method from fitted model: "Extract and record the R-squared value from the fitted model (ccs_cal.fit['r'] ** 2) to verify it meets the threshold of ≥0.99997."
- [results] Calibration workflow context: "Fit a polynomial calibration model to the tunemix data using the calibration.fit() method to establish the m/z–drift-time–CCS relationship."
- [readme] DEIMoS calibration capability: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
