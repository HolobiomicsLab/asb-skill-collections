---
name: bruker-mass-spectrum-data-import
description: Use when you have received a Bruker Solarix FT-ICR raw data directory (.d format, containing CompassXtract output or native ser/fid transients) and need to import it into a Python-based analysis workflow for FT-MS signal processing, calibration, or molecular formula search.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - Bruker Solarix
  - pandas
  - numpy
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
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
---

# bruker-mass-spectrum-data-import

## Summary

Load and initialize Bruker Solarix FT-ICR mass spectrometry raw data (.d format) into CoreMS data structures, preparing transient or magnitude-mode spectra for subsequent noise thresholding, peak picking, and molecular formula assignment.

## When to use

You have received a Bruker Solarix FT-ICR raw data directory (.d format, containing CompassXtract output or native ser/fid transients) and need to import it into a Python-based analysis workflow for FT-MS signal processing, calibration, or molecular formula search. This skill is the mandatory first step when working with Bruker instrument output.

## When NOT to use

- Input is already a centroid mass list (CSV, Excel, or mzML) — use a generic mass list importer instead.
- Input is from a different vendor (Thermo, Spectroswiss, MagLab) — use vendor-specific readers.
- The .d directory is corrupted or missing mandatory calibration metadata — validate file integrity first.

## Inputs

- Bruker Solarix .d directory (containing ser, fid, or CompassXtract output files)
- MSParameters object with field-strength calibration constants

## Outputs

- CoreMS MassSpectrum object with m/z, intensity, and metadata
- Transient or magnitude-mode frequency-domain spectrum ready for noise and peak processing

## How to apply

Use CoreMS ReadBrukerSolarix to load the .d directory into a CoreMS mass spectrum object. Initialize MSParameters with field-strength-specific settings (e.g., 12 T or 15 T magnetic field calibration constants). Set noise thresholding method (relative_abundance, log, or signal_noise) and peak prominence thresholds (e.g., peak_min_prominence_percent = 1, noise_threshold_min_relative_abundance = 1) according to instrument resolution and expected dynamic range. The importer automatically handles FT magnitude-mode conversion and transient metadata extraction. Verify that m/z range, resolving power, and baseline noise floor are consistent with acquisition parameters before proceeding to peak picking.

## Related tools

- **CoreMS** (Provides ReadBrukerSolarix importer and MassSpectrum data structure for Bruker .d file parsing and FT-ICR metadata extraction) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix** (Source instrument and data acquisition platform generating .d directories with ser/fid transient or CompassXtract processed spectra)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('path/to/sample.d'); print(ms.number_of_peaks, ms.resolving_power_calculator())
```

## Evaluation signals

- MassSpectrum object is non-null and contains non-zero intensity array with matching m/z length.
- Metadata fields (scan_number, rt, polarity, resolving_power, field_strength) are populated and consistent with acquisition header.
- m/z range and mass resolution match Bruker instrument specifications (e.g., 50–1000 m/z at >100k resolving power for 12 T).
- Intensity baseline and dynamic range are appropriate for FT magnitude mode (no truncation or overflow).
- No exceptions or file-read errors are raised; ReadBrukerSolarix completes without timeout.

## Limitations

- Only FT magnitude mode is supported; phase-corrected time-domain data requires external preprocessing.
- CompassXtract output may lose transient metadata; ser/fid native import is more reliable for advanced signal processing.
- Bruker proprietary binary formats are reverse-engineered; future CompassXtract versions may cause read failures.
- Import performance degrades for very large transients (>1 GB); streaming mode not yet available.

## Evidence

- [other] Load the recalibrated FT-ICR mass spectrum data file (Bruker .d format) using CoreMS ReadBrukerSolarix.: "Load the recalibrated FT-ICR mass spectrum data file (Bruker .d format) using CoreMS ReadBrukerSolarix."
- [other] Import and process transient data is step 1 in FT-MS workflow.: "1. Import and process transient data"
- [readme] CoreMS supports direct access for almost all vendors' data formats.: "CoreMS supports direct access for almost all vendors' data formats"
- [readme] Bruker Solarix transients, ser and fid (FT magnitude mode only) are supported input formats.: "Bruker Solarix transients, ser and fid (FT magnitude mode only)"
- [other] Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method.: "Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method (e.g., relative_abundance or log) and peak prominence thresholds."
