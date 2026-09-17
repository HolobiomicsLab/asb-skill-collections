---
name: mass-calibration-coefficient-computation
description: Use when after successfully matching at least 5 reference m/z points
  (from a .ref file) to spectrum peaks within a PPM error window (starting at ±1.0
  ppm and widened iteratively to ±1.5, ±3, ±5, ±7, or ±10 ppm if needed).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# mass-calibration-coefficient-computation

## Summary

Compute polynomial calibration coefficients from matched reference m/z peaks using least-squares fitting, enabling conversion of measured frequency or m/z error to true m/z values in FT-MS workflows. This skill bridges peak-matching (with adaptive PPM tolerance) to downstream molecular formula assignment.

## When to use

After successfully matching at least 5 reference m/z points (from a .ref file) to spectrum peaks within a PPM error window (starting at ±1.0 ppm and widened iteratively to ±1.5, ±3, ±5, ±7, or ±10 ppm if needed). Apply when the initial narrow tolerance fails and you need calibration coefficients to correct systematic m/z drift across the entire spectrum.

## When NOT to use

- Fewer than 5 reference m/z matches found even after widening PPM tolerance to ±10 ppm — coefficient fitting on < 5 points is unreliable.
- Reference m/z list is missing, empty, or in an unsupported format — no ground truth to match against.
- Input spectrum is already pre-calibrated or in a processed/centroid-only format where access to raw peaks is unavailable.

## Inputs

- mass spectrum file in Bruker .d format (e.g., ESI_NEG_SRFA.d)
- reference m/z list (.ref file, e.g., SRFA.ref)
- matched peak pairs: (measured_mz, reference_mz) tuples from prior matching step
- PPM tolerance window (initial and widening increments: ±1.0, ±1.5, ±3, ±5, ±7, ±10 ppm)

## Outputs

- calibration coefficients (linear: [slope, intercept]; quadratic: [a, b, c])
- residuals: per-point fit errors (reference_mz - predicted_mz)
- match count: number of reference points used in regression
- structured calibration record (JSON or DataFrame) ready for serialization

## How to apply

Load the mass spectrum (e.g., ESI_NEG_SRFA.d in Bruker format) and reference m/z file (.ref format) using CoreMS data encapsulation modules. After matching reference points to spectrum peaks (repeating the match across widened PPM windows if the first pass yields < 5 points), extract the matched pairs as (measured_mz, reference_mz) tuples. Fit a polynomial model (typically linear or quadratic, via least-squares or equivalent regression) to these pairs, computing the calibration coefficients (slope, intercept, and optional quadratic term). Calculate residuals for each matched point to assess fit quality. Serialize the count of matched points, coefficient vector, and residual statistics into a structured record (e.g., JSON or pandas DataFrame) and write to output.

## Related tools

- **CoreMS** (Data encapsulation, peak loading, and least-squares fitting API for FT-MS spectrum and reference m/z handling) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Polynomial regression (np.polyfit) and residual calculation)
- **pandas** (Serialization of calibration results (coefficients, residuals, match count) to DataFrame/CSV/pickle)
- **Docker** (Containerized execution environment for reproducible calibration workflows)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; import numpy as np; from corems import MassSpec; spectrum = MassSpec.from_file('tests/tests_data/ftms/ESI_NEG_SRFA.d'); ref_mz = np.loadtxt('tests/tests_data/ftms/SRFA.ref'); matched_pairs = [(peak.mz, ref) for peak, ref in zip(spectrum.peaks[:5], ref_mz[:5])]; coeffs = np.polyfit([m[0] for m in matched_pairs], [m[1] for m in matched_pairs], 1); residuals = np.polyval(coeffs, [m[0] for m in matched_pairs]) - [m[1] for m in matched_pairs]; print({'point_count': len(matched_pairs), 'coefficients': coeffs.tolist(), 'residuals': residuals.tolist()})
```

## Evaluation signals

- Match count is ≥ 5 and recorded in output; residual mean and std are within expected bounds (e.g., mean ~0, std << 1 ppm).
- Calibration coefficients are finite and physically plausible (slope near 1.0 for linear, intercept near 0 for well-centered spectra).
- Residuals show no systematic trend across the m/z range (check scatter plot or autocorrelation).
- Serialized output file (JSON/CSV/pickle) is readable and contains all required fields: point_count, coefficients, residuals.
- Applied coefficients to a held-out test peak reduce its m/z error to < 1 ppm (validation against unused reference points).

## Limitations

- Requires at least 5 matched reference points; sparse or low-abundance spectra may fail to reach this threshold even with widened PPM tolerances (up to ±10 ppm).
- Linear and quadratic polynomial fits assume calibration error is polynomial in m/z; non-polynomial (e.g., time-dependent) drift will not be corrected.
- Reference m/z file must be curated and representative of the sample class; contaminated or out-of-date references produce biased coefficients.
- Iterative PPM widening may match incorrect peaks at high tolerance (±10 ppm), introducing outliers; robust regression (e.g., RANSAC or M-estimators) not mentioned in workflow.

## Evidence

- [other] When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient reference m/z matches are located.: "When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient"
- [other] Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression.: "Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression."
- [other] Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules.: "Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules."
- [other] Serialize the results (point count, coefficients, residuals) into a structured record and write to output file.: "Serialize the results (point count, coefficients, residuals) into a structured record and write to output file."
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
