---
name: mass-error-calculation-and-reporting
description: Use when after molecular formula assignment has been performed on calibrated
  m/z values. Apply this skill when you need to quantify the accuracy of formula-to-peak
  matching, validate mass calibration performance against reference standards (e.g.,
  SRFA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - EnviroMS
  techniques:
  - mass-spectrometry
  license_tier: open
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

# mass-error-calculation-and-reporting

## Summary

Calculate and report mass error metrics (ppm deviation, absolute mass difference) for assigned molecular formulas in FT-ICR and related high-resolution mass spectrometry workflows. Mass error quantification is essential for validating molecular formula assignments and assessing calibration quality.

## When to use

After molecular formula assignment has been performed on calibrated m/z values. Apply this skill when you need to quantify the accuracy of formula-to-peak matching, validate mass calibration performance against reference standards (e.g., SRFA.ref), or report formula confidence metrics for publication or downstream filtering.

## When NOT to use

- Input is uncalibrated or raw (non-calibrated) m/z data; perform MzDomainCalibration first.
- No molecular formula assignment has been performed yet; apply SearchMolecularFormulas before computing mass error.
- Mass spectrometry data comes from low-resolution instruments (e.g., unit-resolution quadrupole MS) where sub-ppm accuracy is not meaningful.

## Inputs

- calibrated m/z values (float array)
- assigned molecular formulas with elemental composition (e.g., C18H24O8)
- mass spectrometry raw data (e.g., ESI_NEG_SRFA.d FT-ICR transients)
- mass calibration reference file (e.g., SRFA.ref with known compound standards)

## Outputs

- mass error in ppm (parts per million)
- mass error in Da (absolute mass difference)
- formula score or confidence metric
- CSV export table with m/z, assigned formula, calculated m/z, and mass error columns

## How to apply

For each assigned molecular formula, calculate the mass error as the difference between the measured (calibrated) m/z and the theoretical m/z computed from the elemental composition. Report mass error in both absolute (Da) and relative (ppm) units. In the CoreMS FT-ICR pipeline, this calculation is performed automatically during SearchMolecularFormulas after MzDomainCalibration against a reference dataset (e.g., SRFA.ref standard compounds). Export the assigned peaks along with their calculated mass error and formula score metrics to CSV for downstream analysis, filtering, or quality control. Mass errors should be evaluated against the instrument's expected resolving power and calibration accuracy to determine assignment reliability.

## Related tools

- **CoreMS** (Main framework executing MzDomainCalibration and SearchMolecularFormulas with automatic mass error calculation and export) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data frame manipulation and CSV export of mass error metrics and assigned formula tables)
- **numpy** (Numerical computation of mass error differences and ppm conversion)
- **EnviroMS** (Workflow layer providing CLI and structured output of molecular formula tables with mass error columns) — https://github.com/EMSL-Computing/EnviroMS

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; import pandas as pd; mz_measured = [299.0876]; formula_string = 'C16H16O6'; theoretical_mz = 300.0947; mass_error_da = mz_measured[0] - theoretical_mz; mass_error_ppm = (mass_error_da / theoretical_mz) * 1e6; results_df = pd.DataFrame({'measured_mz': mz_measured, 'formula': [formula_string], 'theoretical_mz': [theoretical_mz], 'mass_error_da': [mass_error_da], 'mass_error_ppm': [mass_error_ppm]}); results_df.to_csv('mass_error_report.csv', index=False)
```

## Evaluation signals

- Mass error values fall within expected range for the instrument (typically < 5 ppm for FT-ICR after calibration with SRFA reference standards).
- CSV export contains all required columns: m/z, calibrated m/z, calculated m/z, assigned formula, mass error (Da and ppm), and formula score.
- Mass error distribution is centered near zero with no systematic bias, indicating successful calibration against reference standards.
- High-abundance peaks have lower mass errors than low-abundance peaks, consistent with signal-to-noise limitations.
- Comparison of mass error values between known reference compounds (SRFA.ref) and unknowns validates calibration accuracy.

## Limitations

- Mass error calculation assumes prior successful mass calibration; poor calibration will produce inflated or biased errors regardless of formula correctness.
- Extremely low abundance peaks may have higher apparent mass error due to peak-picking uncertainty, even if the formula is correct.
- Mass error alone does not guarantee formula correctness; isotopic pattern matching and chemical feasibility checks are required for confident assignment.
- The method is most accurate for FT-based instruments (FT-ICR, Orbitrap) with resolving power > 60,000; lower-resolution data will have larger inherent mass error.
- No changelog found for CoreMS, limiting traceability of changes to mass error calculation algorithms across versions.

## Evidence

- [other] Does the CoreMS FT-ICR data processing pipeline (Hanning apodization, log-based noise thresholding, MzDomainCalibration, and SearchMolecularFormulas) successfully assign molecular formulas to ESI_NEG_SRFA.d data with quantified mass error metrics?: "ESI_NEG_SRFA.d data with quantified mass error metrics"
- [other] The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and SearchMolecularFormulas with CHO constraints, producing assigned peaks with mass error and abundance metrics exportable to CSV.: "producing assigned peaks with mass error and abundance metrics exportable to CSV"
- [other] Perform mass-domain calibration using MzDomainCalibration against SRFA.ref reference data. Execute SearchMolecularFormulas with elemental constraints limited to C, H, O atoms. Export assigned molecular formulas with calculated mass error and formula score metrics to CSV format.: "Export assigned molecular formulas with calculated mass error and formula score metrics to CSV format"
- [readme] modern molecular formulae assignment algorithms: "modern molecular formulae assignment algorithms"
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
