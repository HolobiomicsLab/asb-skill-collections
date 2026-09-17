---
name: calibration-residual-calculation
description: Use when after a mass spectrum has been matched against a reference m/z
  file (e.g., SRFA.ref) and a sufficient number of calibration points (≥5) have been
  identified within a given PPM tolerance window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters
  import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# calibration-residual-calculation

## Summary

Computation of mass calibration coefficients and residuals from matched reference m/z points using least-squares fitting or polynomial regression. This skill assesses the quality and accuracy of mass spectrum calibration by quantifying the deviation between theoretical and observed m/z values.

## When to use

Apply this skill after a mass spectrum has been matched against a reference m/z file (e.g., SRFA.ref) and a sufficient number of calibration points (≥5) have been identified within a given PPM tolerance window. Use it to finalize the calibration procedure and produce quantitative measures of calibration fit quality and point-specific errors.

## When NOT to use

- Fewer than 5 matched reference points are available — the procedure has not identified sufficient calibration anchors; return to PPM window widening or data quality assessment instead.
- Reference m/z file is absent or incompatible with the mass spectrum format.
- Spectrum is already fully calibrated and residuals are not required for downstream analysis.

## Inputs

- mass spectrum data object (e.g., from CoreMS Bruker .d or ThermoFisher .raw file)
- reference m/z file (e.g., SRFA.ref with theoretical m/z values)
- list of matched reference–observed m/z pairs with count ≥5
- PPM tolerance threshold used for matching

## Outputs

- calibration coefficients (linear, quadratic, or Ledford equation parameters)
- residual values for each matched calibration point
- calibration quality metrics (point count, fit statistics)
- structured output record (serialized to file: .csv, .txt, .hdf5, or pandas DataFrame)

## How to apply

After loading the mass spectrum (e.g., from ESI_NEG_SRFA.d) and matching reference m/z values against spectrum peaks, collect the matched reference–observed m/z pairs. Apply least-squares fitting or equivalent polynomial regression (linear, quadratic, or Ledford equation) to compute calibration coefficients that transform observed m/z to calibrated m/z. Calculate residuals as the difference between observed and fitted m/z values for each matched point. Serialize the results (point count, coefficients, residuals) into a structured record and write to output file. The quality of the calibration is reflected in the magnitude and distribution of residuals; smaller residuals and higher point counts indicate better calibration fidelity.

## Related tools

- **CoreMS** (Mass spectrometry data encapsulation and calibration framework; provides spectrum loading, reference m/z matching, and polynomial regression/coefficient calculation) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Numerical computing for polynomial fitting and least-squares regression)
- **pandas** (Data frame construction and serialization of calibration results)
- **Docker** (Containerization for reproducible calibration workflow execution)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.mass_spectrum import MassSpectrum; ms = MassSpectrum(file_path='tests/tests_data/ftms/ESI_NEG_SRFA.d'); ref_mz = load_reference_mz('tests/tests_data/ftms/SRFA.ref'); matched_pairs = match_reference_mz(ms, ref_mz, ppm_tolerance=5.0); coeffs, residuals = compute_calibration(matched_pairs, method='linear'); output_df = pd.DataFrame({'coefficients': coeffs, 'residuals': residuals, 'point_count': len(matched_pairs)}); output_df.to_csv('calibration_results.csv')
```

## Evaluation signals

- Point count matches the number of matched reference m/z values and is ≥5.
- Calibration coefficients are real numbers and have expected sign and magnitude relative to the PPM tolerance window used.
- Residuals are calculated for all matched points; the mean absolute residual should be smaller than the PPM window width used for matching.
- Output file is properly formatted (valid .csv, .txt, .hdf5, or .pkl) and contains all required fields: point count, coefficients, residuals.
- Residual distribution is approximately centered near zero with no systematic bias (e.g., large positive or negative skew) that would indicate a poor model fit.

## Limitations

- Calibration accuracy depends entirely on the quality and completeness of the reference m/z file; errors or outliers in the reference data will propagate to coefficients and residuals.
- Polynomial order (linear vs. quadratic vs. Ledford) must be chosen appropriately for the mass spectrometer's m/z error behavior; mismatched order will yield poor residual distributions.
- With fewer than 5 calibration points, polynomial fitting becomes unstable and residuals are unreliable; the procedure requires prior successful PPM window widening to ensure sufficient matches.
- Residuals reflect calibration fit quality for the specific mass range covered by matched reference points; m/z values outside this range may have larger uncalibrated errors.

## Evidence

- [other] When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient reference m/z matches are located.: "When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient"
- [other] Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression.: "Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [other] Serialize the results (point count, coefficients, residuals) into a structured record and write to output file.: "Serialize the results (point count, coefficients, residuals) into a structured record and write to output file."
- [readme] Self-containing Hierarchical Data Format (.hdf5) including raw data and time-series data-point for processed data-sets with all associated metadata stored as json attributes: "Self-containing Hierarchical Data Format (.hdf5) including raw data and time-series data-point for processed data-sets with all associated metadata stored as json attributes"
