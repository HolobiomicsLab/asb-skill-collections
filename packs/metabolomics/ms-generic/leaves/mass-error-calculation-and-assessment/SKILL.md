---
name: mass-error-calculation-and-assessment
description: Use when after peak picking and before or after molecular formula assignment
  on FT-ICR data, especially when calibrating on a specific field strength (e.g.,
  12 T or 15 T).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - pandas
  - numpy
  - Bruker Solarix (ReadBrukerSolarix)
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import pandas as pd
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
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

# mass-error-calculation-and-assessment

## Summary

Quantifies the accuracy of molecular formula assignments by calculating the difference between theoretical m/z values and observed m/z values in FT-ICR mass spectra, expressed in ppm error. This assessment is essential for validating formula assignments and tuning calibration parameters on high-field instruments.

## When to use

After peak picking and before or after molecular formula assignment on FT-ICR data, especially when calibrating on a specific field strength (e.g., 12 T or 15 T). Apply this skill when you have detected m/z peaks and candidate molecular formulas and need to evaluate assignment quality or diagnose calibration drift.

## When NOT to use

- Input is centroid data without recalibration reference — mass error cannot be meaningfully assessed without proper calibration anchors.
- Peaks are below the noise threshold or have low signal-to-noise ratio — unreliable m/z positions will corrupt error statistics.
- No molecular formula candidates fall within the specified ppm tolerance — indicates calibration or parameter mismatch, not a valid use of this skill.

## Inputs

- Recalibrated FT-ICR mass spectrum (Bruker .d format or equivalent)
- Detected m/z peaks with apex positions
- Assigned molecular formulas with exact masses
- Field-strength-specific calibration parameters (12 T, 15 T, etc.)

## Outputs

- Per-peak mass error in ppm
- Mass error distribution (mean, std dev, min/max)
- Calibrated m/z and theoretical m/z columns in assignment table
- Diagnostic plots of mass error vs m/z or abundance

## How to apply

For each detected peak with an assigned molecular formula, calculate the theoretical m/z value from the formula's exact mass, then compute mass error as (observed_mz - theoretical_mz) / theoretical_mz × 10⁶ to express in ppm. Configure mass error tolerance parameters (min/max ppm error bounds) in SearchMolecularFormulas before assignment to filter candidates within acceptable accuracy windows. After assignment, extract and tabulate the calculated mass error for each peak to assess systematic calibration bias, residual scatter, and whether error clusters suggest recalibration is needed. Use noise thresholding method and calibration signal-to-noise threshold settings to ensure only high-confidence peaks are included in error statistics.

## Related tools

- **CoreMS** (Provides mass spectrum data structures, peak picking, calibration workflows, and SearchMolecularFormulas function for formula assignment with configurable mass error tolerance) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix (ReadBrukerSolarix)** (Loads raw FT-ICR transient data and metadata from Bruker .d format, enabling direct access to calibration parameters and field strength)
- **pandas** (Constructs and exports tabular results including m/z, assigned formula, theoretical m/z, and calculated mass error)
- **numpy** (Performs vectorized mass error calculations and statistical summaries)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('path/to/data.d'); ms.calibrate(); ms.molecular_search_settings.min_ppm_error = -2; ms.molecular_search_settings.max_ppm_error = 2; ms.run_molecular_search(); df = ms.to_dataframe()[['m/z', 'Calibrated m/z', 'Calculated m/z', 'mass_error_ppm']]; print(df)
```

## Evaluation signals

- Mass error distribution is centered near zero with no systematic bias across the m/z range, indicating successful calibration.
- All assigned peaks fall within the specified min/max ppm error bounds (e.g., ±2 ppm for 12 T field strength).
- Mass error remains <5 ppm across the full detected m/z range; larger errors suggest recalibration is needed.
- Error statistics are reproducible when reprocessed; high variability indicates unstable peak picking or calibration reference.
- Extracted mass error table matches expected schema with no NaN or out-of-range values for confident assignments.

## Limitations

- Mass error calculation depends critically on the quality and stability of the initial calibration; poorly calibrated spectra will show inflated errors regardless of formula correctness.
- High noise or low-abundance peaks may have inaccurate m/z centroids due to peak picking artifacts, inflating error for weak signals.
- Systematic mass error across m/z (e.g., parabolic drift) may indicate non-linear calibration effects requiring Ledford, quadratic, or higher-order calibration models rather than simple ppm tolerance adjustment.
- Mass error alone does not confirm molecular formula correctness — multiple formulae may fall within tolerance; isotopic pattern and chemical plausibility must also be considered.

## Evidence

- [other] mass error tolerance (min/max ppm error), element atom constraints (C, H, O, N, S): "mass error tolerance (min/max ppm error), element atom constraints (C, H, O, N, S), ionization mode"
- [other] Extract and export peak assignments including m/z, assigned molecular formula, and calculated mass error to a structured table format.: "Extract and export peak assignments including m/z, assigned molecular formula, and calculated mass error to a structured table format."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [readme] Prediction of mass error distribution: "Prediction of mass error distribution"
- [other] Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method (e.g., relative_abundance or log) and peak prominence thresholds.: "Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method (e.g., relative_abundance or log) and peak prominence thresholds."
