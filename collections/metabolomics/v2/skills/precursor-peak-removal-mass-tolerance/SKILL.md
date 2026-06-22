---
name: precursor-peak-removal-mass-tolerance
description: Use when after loading an MsmsSpectrum object but before intensity filtering or spectral annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
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
---

# precursor-peak-removal-mass-tolerance

## Summary

Remove the precursor (parent) ion peak from a tandem mass spectrum using a mass tolerance window, eliminating the dominant peak that would otherwise dominate intensity-based scoring in spectral matching and annotation. This preprocessing step is critical for peptide identification workflows where the precursor peak can mask weaker fragment ions.

## When to use

Apply this skill after loading an MsmsSpectrum object but before intensity filtering or spectral annotation. Use it when the spectrum contains an undesired precursor peak that could interfere with fragment ion matching, or when comparing spectra across different instruments where precursor peak intensity varies. Triggered by presence of the parent ion m/z in the spectrum and the need to focus on fragment ions for database matching.

## When NOT to use

- Input spectrum is already a processed feature table or peak list without precursor m/z annotation.
- Precursor peak has already been removed by the instrument or data acquisition software.
- Tolerance parameters are unknown or not calibrated for the instrument; using incorrect tolerance may remove valid fragment ions.

## Inputs

- MsmsSpectrum object (from spectrum_utils.spectrum.MsmsSpectrum) containing m/z and intensity arrays and a known precursor m/z value
- Fragment mass tolerance (float, in Da or ppm)
- Tolerance mode (string: 'Da' or 'ppm')

## Outputs

- MsmsSpectrum object with precursor peak and nearby peaks (within tolerance window) removed
- Modified m/z and intensity arrays with peaks in the isolation window excluded

## How to apply

Call the `remove_precursor_peak()` method on an MsmsSpectrum object, providing two parameters: `fragment_tol_mass` (the absolute mass tolerance in Daltons, e.g., 0.05) and `fragment_tol_mode` (either 'Da' for absolute or 'ppm' for parts-per-million relative tolerance, e.g., 10 ppm). The method removes all peaks within the mass tolerance window centered on the precursor m/z. Choose tolerance based on the instrument's mass accuracy: high-resolution instruments (Orbitrap, Q-TOF) typically use 5–10 ppm or 0.02–0.05 Da; lower-resolution instruments may use 0.1–0.5 Da. Apply this step immediately after `set_mz_range()` to avoid removing peaks already outside the observation window.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class and remove_precursor_peak() method for precursor ion removal with configurable mass tolerance) — https://github.com/bittremieux/spectrum_utils
- **Python** (Runtime environment for spectrum_utils and scripting the preprocessing workflow)

## Examples

```
spectrum.remove_precursor_peak(fragment_tol_mass=0.05, fragment_tol_mode='Da')
```

## Evaluation signals

- Verify that the m/z value corresponding to the precursor m/z ± tolerance window is absent from the output spectrum's m/z array.
- Confirm that the output spectrum has fewer peaks than the input (peak count decreased).
- Check that peaks outside the tolerance window remain unchanged (identical m/z and intensity in output).
- Validate that the highest-intensity peak in the output spectrum is a fragment ion, not the precursor.
- Inspect a plot of input vs. output spectrum to visually confirm the precursor peak region is cleared while other peaks are preserved.

## Limitations

- Tolerance window is centered on a single precursor m/z value; if the spectrum contains multiple co-isolated precursor ions, only one can be removed.
- Very small tolerance values (e.g., < 0.01 Da on low-resolution instruments) may fail to remove the precursor peak due to calibration drift; very large values (e.g., > 100 ppm) may incorrectly remove low-mass fragment ions.
- Does not account for isotopic peaks of the precursor (13C, 15N); use with intensity filtering to further suppress residual precursor isotopes.
- If the precursor m/z is not accurately known or recorded in the spectrum metadata, the method cannot locate the peak to remove.

## Evidence

- [other] Apply remove_precursor_peak using the specified fragment tolerance (e.g., 10 ppm or 0.05 Da) to remove the parent ion.: "Apply remove_precursor_peak using the specified fragment tolerance (e.g., 10 ppm or 0.05 Da) to remove the parent ion."
- [intro] spectrum_utils provides common spectrum processing operations including precursor & noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency.: "spectrum_utils provides common spectrum processing operations including precursor & noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency."
- [other] .remove_precursor_peak(fragment_tol_mass, fragment_tol_mode): ".remove_precursor_peak(fragment_tol_mass, fragment_tol_mode)"
