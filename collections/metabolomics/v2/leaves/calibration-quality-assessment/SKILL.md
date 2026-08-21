---
name: calibration-quality-assessment
description: Use when after applying polynomial m/z domain recalibration using a reference
  peak list (e.g., SRFA.ref) to a Bruker FT-ICR dataset. Use this skill to verify
  that calibration has converged and that mass error statistics support reliable downstream
  annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - numpy
  - pandas
  - Bruker Solarix reader (ReadBrukerSolarix)
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
- import numpy as np
- import pandas as pd
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

# calibration-quality-assessment

## Summary

Quantitatively evaluate mass calibration accuracy by computing mass error distributions, root-mean-square error (RMSE), and the count of matched calibration peaks against a reference standard. This skill determines whether a recalibrated FT-ICR mass spectrum meets acceptable accuracy thresholds for subsequent molecular formula assignment.

## When to use

After applying polynomial m/z domain recalibration using a reference peak list (e.g., SRFA.ref) to a Bruker FT-ICR dataset. Use this skill to verify that calibration has converged and that mass error statistics support reliable downstream annotation. Triggers include: (1) completion of MzDomainCalibration initialization and application, (2) need to decide if recalibrated spectrum is fit for formula search, or (3) comparison of calibration quality across multiple acquisition runs or instrument configurations.

## When NOT to use

- Spectrum has not yet undergone MzDomainCalibration or any recalibration step; use raw-spectrum assessment instead.
- Reference peak list is absent, empty, or in an unsupported format; no matched peaks can be computed.
- The goal is to assess signal-to-noise ratio or peak resolving power rather than calibration accuracy; use separate MS-parameter diagnostics.

## Inputs

- Processed mass spectrum object (CoreMS MassSpectrum or Transient, post-peak-picking)
- Reference peak list file (e.g., SRFA.ref, tab- or space-delimited format with reference m/z values)
- MzDomainCalibration object post-application (contains matched peak pairs and polynomial coefficients)

## Outputs

- Mass error distribution (array or histogram of ppm/Da values per matched peak)
- Root-mean-square error (RMSE) scalar, units ppm or Da
- Matched peak count (integer; number of reference peaks found within tolerance)
- Calibration report (tabular or JSON export with statistics, polynomial coefficients, and metadata)

## How to apply

Extract calibration statistics from the MzDomainCalibration object after recalibration is applied to the mass spectrum. Compute and report: (a) the mass error distribution (typically in ppm or Daltons) across all matched calibration peaks, (b) root-mean-square error (RMSE) as a single-number summary of calibration fit quality, and (c) the count of calibration peaks successfully matched within the specified mass error bounds (e.g., ±5 ppm tolerance). Evaluate acceptance using domain knowledge: RMSE typically should be <0.5 ppm for high-resolution FT-ICR work; fewer than ~10 matched peaks indicates weak calibration. Export statistics to a calibration report alongside the recalibrated spectrum for traceability and downstream QC.

## Related tools

- **CoreMS** (Provides MassSpectrum data structures, MzDomainCalibration class, and calibration statistics extraction methods; enables polynomial recalibration and RMSE/mass-error computation.) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix reader (ReadBrukerSolarix)** (Loads raw Bruker FT-ICR transient and processed spectrum data (.d directories) into CoreMS objects for downstream calibration assessment.) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Computes statistics (mean, std, RMS) over mass error arrays; enables numerical aggregation of calibration quality metrics.)
- **pandas** (Exports calibration statistics (peak matches, RMSE, mass errors) to tabular formats (CSV, Excel) for QC reporting and downstream analysis.)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('ESI_NEG_SRFA.d'); ms.load_reference_file('SRFA.ref'); ms.calibrate(); print(f'RMSE: {ms.calibration_rmse} ppm, Matched peaks: {ms.calibration_match_count}')
```

## Evaluation signals

- RMSE < 0.5 ppm for high-resolution FT-ICR instruments at 15 T or higher; > 1 ppm indicates poor calibration.
- Number of matched calibration peaks ≥ 10 (minimum threshold); fewer matches suggest incomplete coverage or weak reference fit.
- Mass error distribution is approximately centered at zero (mean close to 0 ± 0.1 ppm) and symmetric; systematic bias indicates residual polynomial mis-specification.
- Calibration statistics are reproducible across repeated runs on the same sample; large variance suggests instrumental drift or reference-list instability.
- Export files (calibration report, recalibrated spectrum) are non-empty and contain valid numeric values; schema validation (JSON or CSV headers) confirms proper serialization.

## Limitations

- Calibration quality is only as good as the reference peak list; SRFA.ref or equivalent must be accurate and representative of the m/z range analyzed. Poor or outdated reference lists yield inflated RMSE and reduced matched-peak counts.
- Polynomial recalibration (Linear, Quadratic, or LedFord equation) assumes smooth m/z-domain distortion; severe non-linear instrumental artifacts may not be fully corrected, limiting RMSE improvement.
- Mass error statistics computed at the time of calibration may not reflect long-term drift during a multi-sample acquisition sequence; periodic re-calibration or time-dependent quality checks are needed.
- RMSE and matched-peak count are sensitive to noise thresholding and peak-picking parameters; changes to MSParameters.mass_spectrum.noise_threshold_method or peak_min_prominence_percent can significantly alter reported statistics without changing true calibration accuracy.

## Evidence

- [other] extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks: "Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks."
- [other] MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and applying polynomial recalibration to the spectrum: "MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and"
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [readme] Self-containing Hierarchical Data Format (.hdf5) including raw data and time-series data-point for processed data-sets with all associated metadata stored as json attributes: "Self-containing Hierarchical Data Format (.hdf5) including raw data and time-series data-point for processed data-sets with all associated metadata stored as json attributes"
