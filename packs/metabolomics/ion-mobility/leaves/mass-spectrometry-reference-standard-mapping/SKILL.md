---
name: mass-spectrometry-reference-standard-mapping
description: Use when you have acquired tunemix data (positive or negative ion mode,
  in .h5 format) with known CCS reference values and need to construct a calibration
  function that will later predict CCS values for unknown analytes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - DEIMoS
  - Python
  - numpy
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# mass-spectrometry-reference-standard-mapping

## Summary

Establish the m/z–drift-time–collision cross section (CCS) relationship by mapping loaded tunemix reference data with known CCS values to a polynomial calibration model. This skill ensures that subsequent CCS predictions on unknown samples are anchored to validated reference standards and achieve high R² fit quality (≥0.99997).

## When to use

Apply this skill when you have acquired tunemix data (positive or negative ion mode, in .h5 format) with known CCS reference values and need to construct a calibration function that will later predict CCS values for unknown analytes. Use this skill as a prerequisite step before applying CCS calibration to experimental samples, especially when instrument-specific drift-time-to-CCS conversion coefficients are required.

## When NOT to use

- When tunemix reference data are unavailable or known CCS values are not reliably documented.
- When the acquired data are already processed features (not raw m/z–drift-time arrays); reference mapping requires raw multidimensional spectrometry data.
- When switching between fundamentally different ionization modes or mass spectrometers without re-validating the calibration model on new instrument-specific tunemix data.

## Inputs

- tunemix reference data file (.h5 format, e.g., example_tune_pos.h5)
- known CCS values for reference standards
- m/z-to-CCS mapping dictionary for tunemix compounds
- ion mode specification (positive or negative)

## Outputs

- fitted calibration model object (ccs_cal)
- polynomial calibration coefficients (m/z–drift-time–CCS relationship)
- R² goodness-of-fit metric (float, e.g., 0.9999784552958121)
- validated calibration object ready for deployment on unknown samples

## How to apply

Load tunemix reference data using deimos.load() with the appropriate .h5 file (e.g., example_tune_pos.h5) and ms1 key. Initialize a DEIMoS calibration object, specifying the known CCS values and the m/z-to-CCS mapping for your reference standards. Fit a polynomial calibration model to the tunemix data using calibration.fit() to establish the m/z–drift-time–CCS relationship. Extract the R² metric from the fitted model (ccs_cal.fit['r'] ** 2) and verify it meets or exceeds 0.99997. If the threshold is not met, review the reference data for outliers or instrument drift before proceeding to unknown sample analysis. Record both the calibration coefficients and their R² validation metric for reproducibility.

## Related tools

- **DEIMoS** (Load tunemix reference data, initialize and fit calibration model, extract and validate R² metric) — http://github.com/pnnl/deimos
- **Python** (Primary scripting language for invoking DEIMoS calibration API and manipulating calibration objects)
- **numpy** (Numerical operations on array data (m/z, drift time, CCS arrays) within calibration fitting)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); ccs_cal_pos = deimos.calibrate.CCSCalibration(tune_pos, known_ccs_dict); ccs_cal_pos.fit(); print('r-squared:', ccs_cal_pos.fit['r'] ** 2)
```

## Evaluation signals

- R² value from fitted calibration model ≥ 0.99997 (e.g., 0.9999784552958121 for positive ion mode).
- Calibration model object is instantiated and contains 'fit' dictionary with 'r' key accessible.
- Fitted polynomial coefficients are numerically stable and match known CCS–m/z–drift-time relationships within expected tolerances.
- Same calibration workflow applied to both positive and negative ion mode tunemix data yields consistent R² thresholds, demonstrating reproducibility across ionization modes.
- Calibration model can be serialized and later loaded to predict CCS on unknown samples without degradation of fit quality.

## Limitations

- Calibration quality is critically dependent on the accuracy and completeness of known CCS values for reference standards; contaminated or mislabeled tunemix data will degrade the R² metric.
- Polynomial calibration model assumes a smooth, continuous relationship between m/z, drift time, and CCS; highly nonlinear or multimodal responses may not be captured adequately.
- Separate calibration models are required for positive and negative ion modes; a single model cannot reliably predict CCS across both ionization modes simultaneously.
- DEIMoS operates on N-dimensional data largely agnostic to acquisition instrumentation, but instrument-specific drift-voltage settings, gas composition, and tuning may require separate calibration validation.

## Evidence

- [other] Does the DEIMoS tunemix calibration function produce collision cross section (CCS) calibration coefficients that achieve R-squared values ≥0.99997 when applied to positive and negative ion mode tune mix data?: "Does the DEIMoS tunemix calibration function produce collision cross section (CCS) calibration coefficients that achieve R-squared values ≥0.99997"
- [other] Initialize a DEIMoS calibration object with the loaded tunemix data, specifying known CCS values and m/z-to-CCS mapping.: "Initialize a DEIMoS calibration object with the loaded tunemix data, specifying known CCS values and m/z-to-CCS mapping"
- [other] Fit a polynomial calibration model to the tunemix data using the calibration.fit() method to establish the m/z–drift-time–CCS relationship.: "Fit a polynomial calibration model to the tunemix data using the calibration.fit() method to establish the m/z–drift-time–CCS relationship"
- [other] The DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134, both exceeding the 0.99997 threshold.: "The DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134"
- [readme] Collision cross section (CCS) calibration is among the core functionalities of DEIMoS, which operates on N-dimensional data largely agnostic to acquisition instrumentation.: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
