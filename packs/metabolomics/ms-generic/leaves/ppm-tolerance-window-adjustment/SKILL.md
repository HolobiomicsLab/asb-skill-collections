---
name: ppm-tolerance-window-adjustment
description: Use when a mass spectrum calibration procedure initialized with a narrow ppm window (e.g., ±1.0 or ±5.0 ppm) finds fewer than 5 reference m/z matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# ppm-tolerance-window-adjustment

## Summary

An iterative calibration refinement technique that progressively widens the parts-per-million (ppm) error tolerance window when initial narrow thresholds fail to yield sufficient reference m/z matches. This skill is essential for robust mass spectrometry calibration when working with sparse or challenging reference lists.

## When to use

Apply this skill when a mass spectrum calibration procedure initialized with a narrow ppm window (e.g., ±1.0 or ±5.0 ppm) finds fewer than 5 reference m/z matches. This indicates the initial threshold is too stringent relative to the actual mass error distribution in the instrument or data, and systematic widening is needed to recover calibration points without manual intervention.

## When NOT to use

- Reference list is already filtered to high-confidence peaks (>10 matches at ±1.0 ppm) — standard calibration is sufficient.
- Spectrum is severely compromised (e.g., extremely low signal-to-noise, baseline distortion) — widening tolerance will introduce false matches.
- Goal is peak-by-peak validation rather than bulk recalibration — use targeted matching instead.

## Inputs

- Raw mass spectrum file (Bruker .d directory, ThermoFisher .raw, or centroid/profile m/z list)
- Reference m/z list file (e.g., SRFA.ref — tab- or comma-delimited m/z values)
- Initial ppm tolerance threshold (float, e.g., 1.0 or 5.0)
- Minimum calibration point count (integer, typically 5)

## Outputs

- Matched reference m/z indices or values paired with spectrum peaks
- Calibration coefficients (polynomial parameters: slope, intercept, and higher-order terms if quadratic)
- Residual errors (ppm or Δm/z for each matched point)
- Calibration metadata record (point count, final ppm window used, fitting quality metrics)

## How to apply

Initialize calibration matching with a standard ppm tolerance (e.g., ±1.0 ppm) and count matched reference points. If the count falls below the minimum threshold (typically 5 points for robust polynomial regression), iteratively widen the ppm window through a predefined sequence: ±1.5, ±3, ±5, ±7, and ±10 ppm. After each widening, recompute matches and recount; stop when the threshold is met. Use the final matched set to compute calibration coefficients via least-squares polynomial fitting (commonly linear or quadratic), then serialize the point count, coefficients, and residuals to a structured output record (CSV, Excel, or JSON).

## Related tools

- **CoreMS** (Encapsulates mass spectrometry data structures, provides calibration initialization, peak-reference matching, and polynomial fitting modules for tolerance window adjustment) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Performs polynomial coefficient computation and residual calculation via least-squares fitting routines)
- **pandas** (Serializes and exports calibration results (point count, coefficients, residuals) to structured tabular formats (CSV, Excel))
- **Docker** (Containerizes the CoreMS environment and dependencies for reproducible calibration workflows)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; spectrum = load_bruker('ESI_NEG_SRFA.d'); ref_list = pd.read_csv('SRFA.ref'); calibrator = MzCalibration(spectrum, ref_list, initial_ppm=1.0, min_points=5); calibrator.apply_iterative_window_adjustment(ppm_sequence=[1.5, 3, 5, 7, 10]); results = calibrator.to_dataframe(); results.to_csv('calibration_results.csv')
```

## Evaluation signals

- Calibration point count after final window adjustment meets or exceeds the minimum threshold (≥5 points).
- Residual errors for all matched points fall within the final ppm tolerance window used (no outliers beyond ±10 ppm if max window reached).
- Polynomial fit quality metrics (R² or sum of squared residuals) show monotonic improvement or plateau as window widens; final coefficients are numerically stable.
- Serialized output record contains valid, non-null entries for point count, coefficients (correct dimensionality for polynomial degree), and residuals with matching length.
- Spectrum peaks re-calibrated with resulting coefficients exhibit systematic error reduction compared to uncalibrated m/z values (e.g., mean absolute error decreases).

## Limitations

- Setting the minimum point threshold too low (<3) risks overfitting with too few calibration anchors; too high (>10) may cause the routine to fail on sparse reference lists.
- Fixed ppm widening sequence (1.0 → 1.5 → 3 → 5 → 7 → 10) may not be optimal for all instruments or sample types; context-dependent tuning may be necessary.
- If the reference list itself contains systematic bias or is incomplete, widening tolerance will match incorrect m/z values, contaminating calibration coefficients; validation against a secondary reference is recommended.
- The routine assumes a monotonic relationship between ppm window and match count; in rare cases (e.g., overlapping multiplet peaks), widening may introduce false positives without further filtering.

## Evidence

- [other] When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient reference m/z matches are located.: "When fewer than 5 calibration points are found within a given PPM error threshold, the procedure iteratively widens the threshold from ±1.0 ppm to ±1.5, ±3, ±5, ±7, and ±10 ppm until sufficient"
- [other] Count the number of matched reference points; if the count is fewer than 5, widen the PPM tolerance window (e.g., double to 10 ppm) and rematch reference m/z values. Compute calibration coefficients and residuals from the matched points using least-squares fitting or equivalent polynomial regression.: "Count the number of matched reference points; if the count is fewer than 5, widen the PPM tolerance window and rematch reference m/z values. Compute calibration coefficients and residuals from the"
- [other] Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules.: "Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules."
- [other] Serialize the results (point count, coefficients, residuals) into a structured record and write to output file.: "Serialize the results (point count, coefficients, residuals) into a structured record and write to output file."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
