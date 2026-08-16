---
name: spectrum-array-validation
description: Use when after applying any sequence of spectrum preprocessing operations (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity) to an MsmsSpectrum object, to confirm that the resulting arrays fall within specified m/z windows, intensity bounds, and peak count limits before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - Python (numpy)
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectrum Array Validation

## Summary

Verify that mass spectrometry spectrum m/z and intensity arrays conform to expected ranges, data types, and peak count constraints after preprocessing. This skill ensures data integrity and correct application of filtering operations in spectrum_utils workflows.

## When to use

After applying any sequence of spectrum preprocessing operations (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity) to an MsmsSpectrum object, to confirm that the resulting arrays fall within specified m/z windows, intensity bounds, and peak count limits before downstream analysis or visualization.

## When NOT to use

- Input spectrum has not yet undergone any preprocessing — apply preprocessing first before validation.
- Spectrum data is in a format other than MsmsSpectrum (e.g., raw mzML or mzXML files not yet parsed into spectrum_utils objects).
- The analysis goal does not require bounded m/z or intensity ranges (e.g., you are performing exploratory or instrument-agnostic analysis without predefined constraints).

## Inputs

- MsmsSpectrum object (from spectrum_utils.spectrum.MsmsSpectrum)
- m/z and intensity numpy arrays (post-preprocessing)
- preprocessing parameters (min_mz, max_mz, fragment_tol_mass, fragment_tol_mode, min_intensity, max_num_peaks, scale mode)

## Outputs

- Boolean validation result (pass/fail)
- List of validation errors (if any)
- Spectrum object with confirmed conformance to constraints

## How to apply

Load or construct an MsmsSpectrum object and apply the desired preprocessing chain (e.g., set_mz_range with min_mz=100 and max_mz=1400, remove_precursor_peak with fragment tolerance in ppm or Da, filter_intensity with min_intensity threshold as a fraction of base peak and max_num_peaks cap, scale_intensity with mode='root'). Then validate: (1) all m/z values in the spectrum's m/z array fall within [min_mz, max_mz]; (2) the precursor m/z is absent (or only appears if not within fragment tolerance); (3) intensity values are non-negative and do not exceed the base peak after scaling; (4) the number of peaks does not exceed max_num_peaks; (5) intensity scaling has been applied consistently (e.g., all intensities are square-root transformed if mode='root'). Compare the processed spectrum's arrays element-wise against these invariants using array membership and range checks.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum object model, preprocessing methods (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity), and array access for validation) — https://github.com/bittremieuxlab/spectrum_utils
- **Python (numpy)** (Enables efficient array comparison and range/membership checking operations on m/z and intensity arrays)

## Examples

```
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.set_mz_range(min_mz=100, max_mz=1400).remove_precursor_peak(10, 'ppm').filter_intensity(min_intensity=0.05, max_num_peaks=50).scale_intensity('root'); assert (spectrum.mz >= 100).all() and (spectrum.mz <= 1400).all() and len(spectrum.mz) <= 50
```

## Evaluation signals

- All m/z values in spectrum.mz satisfy min_mz ≤ mz[i] ≤ max_mz (or the specified m/z range).
- Precursor m/z is absent from the m/z array, or only present if outside the fragment tolerance window.
- All intensity values are non-negative and the maximum intensity equals or approximates the base peak intensity after scaling.
- Peak count len(spectrum.mz) ≤ max_num_peaks.
- If scale_intensity(mode='root') was applied, all non-zero intensities should satisfy intensity_scaled ≈ sqrt(intensity_original) (up to floating-point precision).

## Limitations

- Validation is sensitive to floating-point precision; near-boundary m/z or intensity values may fail strict equality checks due to rounding during preprocessing.
- The article does not specify a formal tolerance for intensity scaling verification; users must define acceptable epsilon for sqrt transformation checks.
- Validation cannot confirm correctness of the original precursor m/z or fragment tolerance parameters — it only checks that the removal result matches the input parameters.

## Evidence

- [other] Verify that the resulting spectrum object's m/z and intensity arrays contain only peaks within the expected range and that intensity values are properly scaled.: "Verify that the resulting spectrum object's m/z and intensity arrays contain only peaks within the expected range and that intensity values are properly scaled."
- [other] Apply set_mz_range with min_mz=100 and max_mz=1400 to restrict the m/z window.: "Apply set_mz_range with min_mz=100 and max_mz=1400 to restrict the m/z window."
- [other] Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count.: "Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count."
- [intro] Common spectrum processing operations including precursor & noise peak removal, intensity filtering, intensity scaling optimized for computational efficiency.: "Common spectrum processing operations including precursor & noise peak removal, intensity filtering, intensity scaling optimized for computational efficiency."
