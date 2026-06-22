---
name: ccs-calibration-tunemix-execution
description: Use when you have positive-mode tune mix reference data (e.g., example_tune_pos.h5) with known CCS values spanning a wide m/z range (e.g., 118.086–1522 m/z) and need to establish a CCS calibration model to convert experimental drift times or collision cross sections for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - deimos
  techniques:
  - ion-mobility-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ccs-calibration-tunemix-execution

## Summary

Apply the DEIMoS tunemix calibration function to positive-mode tune mix mass spectrometry data to derive a collision cross section (CCS) calibration model. This skill validates that the resulting single-field calibration achieves high goodness-of-fit (r-squared ≥ 0.9999) across the m/z range of reference compounds.

## When to use

Use this skill when you have positive-mode tune mix reference data (e.g., example_tune_pos.h5) with known CCS values spanning a wide m/z range (e.g., 118.086–1522 m/z) and need to establish a CCS calibration model to convert experimental drift times or collision cross sections for downstream analysis. The skill is appropriate when the reference data contains tune compounds with precisely measured collision cross section values.

## When NOT to use

- Input tune data are in negative ionization mode without prior mode conversion
- Reference tune compounds lack reliable, independently measured CCS values
- Tune data spans fewer than 3 reference compounds or a m/z range < 100 Da
- Calibration r-squared falls below 0.999, indicating poor model fit

## Inputs

- Positive-mode tune mix reference file (.h5 format, e.g., example_tune_pos.h5)
- Tune reference data with known CCS values and m/z range (e.g., 118.086255–1521.971475 m/z)

## Outputs

- CCS calibration model object (single-field polynomial fit)
- Calibration r-squared coefficient (goodness-of-fit metric)
- Calibration model parameters for prediction on unknown samples

## How to apply

Load the positive-mode tune reference file using deimos.load() with the 'ms1' key to extract the multidimensional mass spectrometry data. Pass the loaded tune data to deimos.calibration.tunemix(), which applies a single-field calibration model using the reference compounds' known CCS values to fit the relationship between instrumental observables (e.g., drift time, m/z) and CCS. Extract the r-squared coefficient from the calibration model output and verify it matches the expected high-precision value (e.g., 0.9999784552958121) to at least 12 decimal places. The calibration quality is judged by r-squared ≥ 0.9999, indicating an excellent fit suitable for CCS prediction on unknown samples.

## Related tools

- **deimos** (Python library providing deimos.load() and deimos.calibration.tunemix() functions for CCS calibration) — https://github.com/pnnl/deimos
- **Python** (Runtime environment and scripting language for invoking DEIMoS API)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); cal = deimos.calibration.tunemix(tune_pos); r_squared = cal.model.score(...); print(f'r-squared: {r_squared}')
```

## Evaluation signals

- r-squared coefficient matches expected value to ≥ 12 decimal places (e.g., 0.9999784552958121)
- r-squared ≥ 0.9999, indicating excellent single-field model fit
- Calibration model output object is non-null and contains extractable coefficients
- Tune data m/z range and reference compound count are within expected bounds
- Prediction residuals on reference compounds are minimal (< 0.1% CCS error expected)

## Limitations

- Calibration is specific to positive ionization mode; negative-mode data require separate calibration with negative-mode tune reference
- Single-field calibration assumes a linear or low-order polynomial relationship; non-linear CCS behavior across wide m/z ranges may degrade fit quality
- Calibration quality depends on accuracy of reference compound CCS values and instrumental repeatability; systematic instrument drift post-calibration will reduce prediction accuracy
- r-squared alone does not guarantee physical validity of predictions outside the reference m/z range

## Evidence

- [results] Load and calibrate positive-mode tune data: "tune_pos = deimos.load('example_tune_pos.h5', key='ms1')"
- [results] Apply tunemix calibration function: "The tunemix calibration on positive-mode tune mix data (m/z 118.086255–1521.971475) with known CCS values yields r-squared: 0.9999784552958121, indicating excellent fit of the single-field"
- [intro] CCS calibration is a core DEIMoS workflow step: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] DEIMoS library and installation context: "DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool"
- [readme] Repository and version reference: "DEIMoS, version 1.6.2 http://github.com/pnnl/deimos"
