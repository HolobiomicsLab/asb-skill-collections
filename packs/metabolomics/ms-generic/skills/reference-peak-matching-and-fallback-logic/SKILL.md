---
name: reference-peak-matching-and-fallback-logic
description: Use when when performing m/z domain calibration on FT-ICR or high-resolution MS data and the initial calibration attempt finds fewer than 5 reference m/z matches within the standard PPM window (typically ±1–5 ppm).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
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

# Reference-Peak Matching and Fallback Logic

## Summary

An iterative mass calibration strategy that matches observed m/z peaks against known reference m/z values, progressively widening the PPM tolerance window when initial matches fall below a minimum threshold. This skill is essential for recovering calibration coefficients when sparse reference lists or high mass errors prevent sufficient matches at standard tolerances.

## When to use

When performing m/z domain calibration on FT-ICR or high-resolution MS data and the initial calibration attempt finds fewer than 5 reference m/z matches within the standard PPM window (typically ±1–5 ppm). This occurs frequently with sparse reference standards, degraded sample quality, or instruments with larger systematic mass errors.

## When NOT to use

- Input reference list contains fewer than 5 usable m/z values or all reference compounds are absent from the sample.
- Mass spectrum is severely corrupted, contains instrumental artifacts, or exhibits non-linear mass error patterns that require multivariate or instrument-specific correction rather than polynomial fitting.
- Calibration goal is isotope-resolution or fine structure rather than bulk m/z accuracy; fallback widening may conflate nearby peaks and degrade isotopic precision.

## Inputs

- Raw mass spectrum file (Bruker .d, ThermoFisher .raw, or other vendor format supported by CoreMS)
- Reference m/z list file (text or .ref format with known chemical or calibrant m/z values)
- Calibration parameters (initial PPM window width, minimum point threshold, tolerance widening schedule, polynomial order)

## Outputs

- Calibrated mass spectrum with recalculated m/z values
- Calibration coefficient set (slope, intercept, and higher-order terms if polynomial)
- Matched reference point pairs (observed m/z, reference m/z, mass error in ppm)
- Calibration residuals and fit statistics (RMS error, coefficient of determination)
- Metadata record (final PPM window used, matched point count, calibration timestamp)

## How to apply

Begin by loading the mass spectrum (e.g., ESI_NEG_SRFA.d in Bruker or .raw format) and reference m/z list using CoreMS data encapsulation modules. Initialize calibration with a narrow PPM window (e.g., ±1.0 ppm) and match detected peaks against reference m/z values. Count the matched calibration points; if fewer than 5 points are found, enter fallback mode: iteratively widen the PPM tolerance (±1.5, ±3, ±5, ±7, ±10 ppm) and rematch reference m/z values until the minimum point count is reached or the maximum tolerance is exhausted. Compute calibration coefficients (linear, quadratic, or Ledford polynomial) using least-squares regression on the matched point pairs, and calculate residuals to assess fit quality. Serialize the results (matched point count, coefficient set, residuals, tolerance used) into a structured output record and write to disk for downstream validation and reuse.

## Related tools

- **CoreMS** (Encapsulates mass spectrometry data, provides calibration routines (linear, quadratic, Ledford polynomial), peak matching, and least-squares fitting for m/z domain calibration) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Implements least-squares polynomial regression and residual calculations during coefficient computation)
- **pandas** (Organizes and serializes matched reference points, coefficients, and residuals into tabular output records)
- **Docker** (Containerizes CoreMS and dependencies for reproducible calibration workflows across platforms)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; spectrum = CoreMS.from_file('ESI_NEG_SRFA.d'); references = pd.read_csv('SRFA.ref'); calibration = spectrum.calibrate(references, ppm_tol=1.0, min_points=5, fallback_schedule=[1.5, 3, 5, 7, 10]); print(f'Matched {calibration.n_points} points at ±{calibration.ppm_tol} ppm; RMS error = {calibration.rms_error:.4f}')
```

## Evaluation signals

- Matched point count meets or exceeds the minimum threshold (5 points) before calibration proceeds; record the final PPM tolerance required to achieve this.
- Residual distribution (mass error in ppm for each matched pair) is unimodal, centered near zero, with standard deviation consistent with instrumental specifications (typically < 1 ppm for modern FT-ICR).
- Recalibrated m/z values show monotonic improvement in agreement with reference m/z: mean absolute error and RMS error decrease from initial to final calibration.
- Coefficient stability: if reference list is divided into subsets, coefficients computed from subsets should be within 1–2% of the full-set values, indicating robust convergence.
- Fallback tolerance is recorded and justified: if ±10 ppm was required, investigate whether sample preparation, instrument tuning, or reference standard purity contributed to the large initial error.

## Limitations

- Fallback strategy assumes mass error is approximately uniform across the m/z range; highly non-linear or m/z-dependent errors may require segmented or adaptive calibration rather than a single polynomial.
- Iterative widening can conflate true peaks with noise or artifacts at large tolerances (±7–10 ppm); validation should include visual inspection of matched peak pairs and quality metrics.
- Minimum point threshold of 5 is somewhat arbitrary; fewer points may be acceptable for linear calibration, but quadratic or Ledford fits require ≥ 3–4 well-distributed points and larger counts are strongly preferred for robust statistics.
- If reference m/z list is sparse or skewed toward high or low m/z, the polynomial fit may extrapolate poorly; use reference compounds distributed across the observed m/z range when possible.
- Fallback does not address systematic issues such as space-charge effects, magnetic field drift, or detector nonlinearity; it assumes the error is primarily an offset or simple scaling error.

## Evidence

- [other] How does the calibration procedure handle cases where the initial narrow PPM window fails to find sufficient reference m/z matches?: "When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient"
- [readme] CoreMS calibration workflows: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [other] Encapsulation and data handling: "Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules."
- [other] Least-squares fitting methodology: "Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression."
- [other] Output serialization: "Serialize the results (point count, coefficients, residuals) into a structured record and write to output file."
