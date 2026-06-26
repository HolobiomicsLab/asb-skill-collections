---
name: ion-mode-specific-ccs-model-generation
description: Use when you have tunemix reference data acquired in both positive and
  negative ion modes and need to establish independent CCS calibration curves for
  each mode. The skill is required when downstream CCS assignments must achieve R²
  ≥ 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# ion-mode-specific-ccs-model-generation

## Summary

Build separate collision cross section (CCS) calibration models for positive and negative ion modes using tunemix reference data, fitting polynomial relationships between m/z, drift time, and CCS to achieve R² ≥ 0.99997. This skill ensures that ion-mode-specific calibration artifacts and response differences are captured in distinct models rather than conflated in a single universal model.

## When to use

Apply this skill when you have tunemix reference data acquired in both positive and negative ion modes and need to establish independent CCS calibration curves for each mode. The skill is required when downstream CCS assignments must achieve R² ≥ 0.99997, indicating that ion mode-specific chemistry (ionization efficiency, ion-neutral interaction potentials, or detector response) materially affects the m/z–drift-time–CCS relationship.

## When NOT to use

- Input is data from a single ion mode only; use single-mode calibration instead.
- Tunemix reference compounds or m/z-to-CCS mappings are not available; model fitting requires ground truth.
- R² threshold requirement is lower (e.g., 0.99) and mode-specific improvement is not scientifically motivated.

## Inputs

- tunemix reference data for positive ion mode (e.g., example_tune_pos.h5, key='ms1')
- tunemix reference data for negative ion mode (equivalent file structure)
- known m/z-to-CCS mapping for tunemix compounds (reference standard data)
- experimental m/z and drift_time columns from tunemix data

## Outputs

- positive ion mode CCS calibration model (fitted polynomial object with R² metric)
- negative ion mode CCS calibration model (fitted polynomial object with R² metric)
- calibration metadata including R² values for both modes (≥0.99997 threshold verification)

## How to apply

Load tunemix reference data separately for each ion mode (e.g., using deimos.load() with example_tune_pos.h5 for positive mode and corresponding negative mode file), specifying the ms1 key and known m/z-to-CCS mappings for the tunemix compounds. Initialize a DEIMoS calibration object for each mode with its respective tunemix data. Fit a polynomial calibration model to the m/z–drift-time pairs in each mode using calibration.fit(), which solves for coefficients that minimize the residuals between observed drift times and predicted CCS values. Extract the R² metric from each fitted model (ccs_cal.fit['r'] ** 2) and verify that both positive and negative mode models independently exceed the 0.99997 threshold. Save both calibration objects to the output directory with their respective R² values annotated by ion mode so that subsequent CCS assignments can select the appropriate mode-specific model.

## Related tools

- **DEIMoS** (Provides deimos.load() to ingest tunemix .h5 files, calibration.fit() method to fit polynomial m/z–drift-time–CCS models, and extraction of R² metrics from fitted objects) — http://github.com/pnnl/deimos
- **Python** (Execution environment for DEIMoS API calls and calibration object manipulation)
- **numpy** (Numerical operations underlying polynomial fitting and R² calculation in DEIMoS calibration routines)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); ccs_cal_pos = deimos.calibrate.CCSCalibration(tune_pos, known_ccs_values); ccs_cal_pos.fit(); print('positive mode r-squared:', ccs_cal_pos.fit['r'] ** 2)
```

## Evaluation signals

- Positive ion mode model R² = 0.9999784552958121 or higher (≥0.99997 threshold met)
- Negative ion mode model R² = 0.9999784552958134 or higher (≥0.99997 threshold met)
- Both calibration objects are saved to output directory and are loadable without errors
- Residuals between fitted and observed CCS values are normally distributed and centered near zero for each mode
- R² values differ slightly between modes, indicating ion-mode-specific model coefficients are captured (not identical models)

## Limitations

- Tunemix reference data must be of high quality and correctly annotated with known CCS values; erroneous reference standards will compromise model fit.
- The polynomial degree and form are assumed fixed; the article does not specify sensitivity to degree selection or alternative functional forms.
- R² ≥0.99997 is a strict threshold; datasets with lower signal-to-noise or fewer tunemix points may fail to achieve this criterion even with correct methodology.
- Ion mode-specific effects depend on instrument configuration and ionization source; results from one instrument may not transfer to different hardware.

## Evidence

- [results] Positive and negative ion mode R² metrics both meet threshold: "The DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134, both exceeding"
- [results] Workflow for loading and fitting mode-specific models: "Load tunemix reference data for positive ion mode using deimos.load() specifying the example_tune_pos.h5 file and ms1 key. Initialize a DEIMoS calibration object with the loaded tunemix data,"
- [results] R² extraction and threshold verification step: "Extract and record the R-squared value from the fitted model (ccs_cal.fit['r'] ** 2) to verify it meets the threshold of ≥0.99997. Repeat steps 1–4 for negative ion mode using the corresponding"
- [readme] CCS calibration as core DEIMoS functionality: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] Multi-dimensional utilization improves confidence: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
