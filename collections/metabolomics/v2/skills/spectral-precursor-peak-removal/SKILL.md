---
name: spectral-precursor-peak-removal
description: Use when after loading a raw MsmsSpectrum object from a tandem mass spectrometry experiment (e.g., via USI) and before intensity filtering or scaling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - NumPy
  - Numba
  - spectrum_utils
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
- Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/)
- import numpy as np
- optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Precursor Peak Removal

## Summary

Remove the precursor ion peak from tandem mass spectrometry spectra using fragment ion tolerance thresholds. This operation is a critical early preprocessing step that eliminates the unfragmented parent ion, which would otherwise dominate the spectrum and interfere with downstream peak annotation and spectral matching.

## When to use

Apply this skill after loading a raw MsmsSpectrum object from a tandem mass spectrometry experiment (e.g., via USI) and before intensity filtering or scaling. The skill is essential when the precursor peak intensity is high relative to fragment peaks, or when performing fragment ion annotation that requires unambiguous peak-to-ion assignment. Use it whenever you need a clean fragment-only spectrum for spectral matching, library searching, or de novo interpretation.

## When NOT to use

- Input is a neutral loss spectrum or parent ion spectrum where the precursor peak is itself the analyte of interest.
- Spectrum has already been preprocessed by another tool and precursor peak removal has already been applied.
- Fragment ion tolerance is unknown or cannot be reliably estimated from the instrument specification.

## Inputs

- MsmsSpectrum object (loaded via USI or from existing data structure)
- Fragment ion tolerance mass (numeric, in Da)
- Fragment ion tolerance mode (string: 'Da' or 'ppm')

## Outputs

- MsmsSpectrum object with precursor peak(s) removed

## How to apply

Call the `remove_precursor_peak(fragment_tol_mass, fragment_tol_mode)` method on the MsmsSpectrum object, providing the fragment ion tolerance (in Da or ppm) that defines the mass window around the precursor m/z to be removed. The tolerance mode specifies whether the window is absolute (Da) or relative (ppm). The method identifies all peaks within this tolerance window of the precursor m/z and removes them, returning the cleaned spectrum. The choice of tolerance should match the mass accuracy of your instrument (typically 0.05–0.1 Da for high-resolution MS or 10–50 ppm for lower-resolution instruments). This operation should be performed early in the preprocessing pipeline, after m/z range restriction but before intensity filtering, to avoid re-introducing noise peaks in subsequent steps.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class and remove_precursor_peak() method for precursor peak removal with configurable tolerance.) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Underlying numerical computation library used by spectrum_utils for efficient peak filtering operations.) — https://www.numpy.org/
- **Numba** (JIT compilation library that optimizes spectrum_utils preprocessing operations for computational efficiency.) — http://numba.pydata.org/

## Examples

```
spectrum.remove_precursor_peak(fragment_tol_mass=0.05, fragment_tol_mode='Da')
```

## Evaluation signals

- Verify that the peak at or near the precursor m/z is no longer present in the output spectrum.
- Check that the number of peaks has decreased by at least 1 (or more if multiple precursor isotopologues were present).
- Confirm that all remaining peaks fall outside the tolerance window around the precursor m/z: |peak_mz - precursor_mz| > tolerance.
- Validate that fragment peaks in the expected m/z range for the identified peptide (typically m/z 100–1400 for proteomics) remain intact.
- Ensure the base peak intensity and total ion current (TIC) decrease relative to the input spectrum (since intensity was removed).

## Limitations

- If the precursor m/z is poorly calibrated or unknown, the tolerance window may be misaligned, either missing the true precursor or removing nearby fragment ions.
- High-abundance precursor isotopologues (13C, 15N) may also need removal; this method removes only peaks in the specified tolerance window, so a sufficiently wide window must be chosen.
- For overlapping precursor and fragment ion peaks (rare but possible at low resolution), the method will remove both, potentially losing valid fragment information.
- The method assumes a single precursor ion; multiply-charged or multiply-fragmented parent ions may require manual tuning of the tolerance window.

## Evidence

- [other] Call remove_precursor_peak(fragment_tol_mass, fragment_tol_mode) to remove the precursor peak with the specified tolerance.: "Call remove_precursor_peak(fragment_tol_mass, fragment_tol_mode) to remove the precursor peak with the specified tolerance."
- [other] These operations are applied sequentially to an MsmsSpectrum object to produce a cleaned and normalized spectrum suitable for downstream analysis.: "These operations are applied sequentially to an MsmsSpectrum object to produce a cleaned and normalized spectrum suitable for downstream analysis."
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba"
- [other] Remove the precursor peak: "Remove the precursor peak"
