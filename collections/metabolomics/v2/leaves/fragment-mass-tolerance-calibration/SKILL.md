---
name: fragment-mass-tolerance-calibration
description: 'Use when when implementing fragment ion annotation in proteomics workflows
  and needing to determine whether neutral loss annotation (e.g., H2O: -18.010565,
  NH3: -17.026549) should be enabled to maximize peak interpretation.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectrum_utils
  - ProForma 2.0
  - Unimod
  - PSI-MOD
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# fragment-mass-tolerance-calibration

## Summary

Calibrate fragment mass tolerance parameters for spectrum annotation by measuring how neutral loss annotation affects peak interpretation coverage. This skill validates whether enabling neutral loss specification increases the fraction of observed peaks that receive ProForma 2.0 fragment ion interpretation.

## When to use

When implementing fragment ion annotation in proteomics workflows and needing to determine whether neutral loss annotation (e.g., H2O: -18.010565, NH3: -17.026549) should be enabled to maximize peak interpretation. Apply this skill after spectrum preprocessing (precursor removal, noise filtering, intensity scaling) and before final peak annotation, to verify that neutral losses actually improve coverage against a benchmark.

## When NOT to use

- Spectrum has already been extensively curated or annotated by a different annotation engine; this skill is designed to validate neutral loss contribution specifically.
- Fragment ion types other than 'aby' (a, b, y ions) are the analytical target; the workflow assumes standard proteolytic fragmentation ions.
- Input peptide sequence lacks ProForma 2.0 modification syntax or contains non-standard modifications outside Unimod/PSI-MOD vocabularies.

## Inputs

- Universal Spectrum Identifier (USI) string pointing to MSMS spectrum in public repository
- ProForma 2.0 peptide string with modification annotations
- Fragment mass tolerance (e.g., 10 ppm)
- Spectral preprocessing parameters (m/z range, intensity thresholds, scaling method)

## Outputs

- Annotated spectrum peaks with and without neutral loss interpretation
- Fraction of peaks with interpretation (neutral losses disabled)
- Fraction of peaks with interpretation (neutral losses enabled)
- Comparison metric confirming increase in peak coverage

## How to apply

Load a spectrum from a public repository using Universal Spectrum Identifier (USI) with spectrum_utils.MsmsSpectrum.from_usi(). Apply standard preprocessing: set m/z range to 100–1400, remove precursor peak with 10 ppm fragment tolerance, filter low-intensity noise peaks (minimum intensity 0.05, maximum 50 peaks), and scale peak intensities by square root. Annotate fragments using annotate_proforma() with ProForma peptide string and ion_types='aby', first with neutral_losses disabled (default), then repeat with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled. Count annotated peaks in each condition and calculate the fraction of observed peaks receiving interpretation. Compare the two fractions to verify the increase matches reported benchmarks, confirming that neutral loss annotation materially improves peak coverage for your instrument and peptide context.

## Related tools

- **spectrum_utils** (Core library for spectrum loading (from_usi), preprocessing (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity), and fragment annotation (annotate_proforma with ProForma 2.0 and neutral loss configuration)) — https://github.com/bittremieux/spectrum_utils
- **ProForma 2.0** (Specification for peptide string encoding and fragment ion annotation, including modification vocabularies) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary for protein modifications referenced in ProForma peptide strings) — https://www.unimod.org/
- **PSI-MOD** (Controlled vocabulary for post-translational modifications used in annotation) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
spectrum = SpectrumUtils.MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.set_mz_range(min_mz=100, max_mz=1400); spectrum.remove_precursor_peak(fragment_tol_mass=10, fragment_tol_mode='ppm'); spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50); spectrum.scale_intensity('root'); spec_no_loss = spectrum.annotate_proforma('PEPTIDE', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby'); spec_with_loss = spectrum.annotate_proforma('PEPTIDE', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565}); frac_no_loss = spec_no_loss.count_annotated_peaks() / len(spectrum); frac_with_loss = spec_with_loss.count_annotated_peaks() / len(spectrum); print(f'Coverage gain: {frac_with_loss - frac_no_loss:.3f}')
```

## Evaluation signals

- Annotated peak count with neutral_losses disabled is strictly less than or equal to count with neutral_losses enabled.
- Fraction increase (neutral_losses enabled minus disabled) is positive and matches or exceeds reported benchmark threshold.
- Peak annotation respects fragment ion type specification (ion_types='aby') and ProForma 2.0 syntax without parse errors.
- Neutral loss masses are correctly applied: H2O at -18.010565 Da and NH3 at -17.026549 Da, verified by inspecting annotated peaks in the m/z difference output.
- Preprocessing operations preserve spectrum integrity: m/z range 100–1400, precursor peak absence confirmed, intensity scaling monotonic.

## Limitations

- Neutral loss annotation is currently confined to H2O and NH3 in the provided workflow; other neutral losses (e.g., CO, phosphate loss) require manual extension or external tools.
- Fragment mass tolerance (10 ppm assumed) may require instrument-specific calibration; threshold may not generalize across different MS platforms or acquisition modes.
- ProForma 2.0 annotation coverage depends on completeness of input peptide modification syntax; incompletely or incorrectly specified modifications reduce interpretation coverage regardless of neutral loss enablement.
- Peak interpretation is limited to a, b, y ions; internal ions, immonium ions, and other fragment types are not scored by annotate_proforma in this workflow.

## Evidence

- [other] spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation to modulate peak interpretation coverage.: "spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency"
- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism"
- [other] spectrum.set_mz_range(min_mz=100, max_mz=1400): "spectrum.set_mz_range(min_mz=100, max_mz=1400)"
- [other] .filter_intensity(min_intensity=0.05, max_num_peaks=50): ".filter_intensity(min_intensity=0.05, max_num_peaks=50)"
- [other] .annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types="aby"): ".annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types="aby")"
