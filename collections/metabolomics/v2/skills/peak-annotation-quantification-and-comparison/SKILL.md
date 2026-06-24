---
name: peak-annotation-quantification-and-comparison
description: Use when you have a tandem mass spectrum (MsmsSpectrum) from a known
  peptide and need to determine what fraction of observed peaks can be explained by
  expected fragment ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - ProForma 2.0
  - Unimod
  techniques:
  - LC-MS
  license_tier: restricted
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

# peak-annotation-quantification-and-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Annotate observed tandem mass spectrometry peaks against a known peptide sequence using ProForma 2.0 specification, quantify the fraction of peaks receiving interpretation, and compare annotation coverage under different settings (e.g., with and without neutral loss annotation). This skill measures how fragment annotation parameters modulate the interpretability of observed spectra.

## When to use

You have a tandem mass spectrum (MsmsSpectrum) from a known peptide and need to determine what fraction of observed peaks can be explained by expected fragment ions. Use this skill when optimizing annotation parameters or benchmarking whether enabling neutral loss annotation increases peak interpretation coverage.

## When NOT to use

- The input spectrum is from a non-proteolytic ion (e.g., metabolite or intact protein) where ProForma peptide annotation is not applicable.
- The peptide sequence is unknown or ambiguous; annotation requires a ground-truth sequence.
- The spectrum has already been annotated by an external tool and you only need to filter or visualize existing annotations rather than generate new ones.

## Inputs

- MsmsSpectrum object (from spectrum_utils or loaded via USI)
- ProForma 2.0 peptide string
- Fragment tolerance (mass in Da and mode, e.g., 10 ppm)

## Outputs

- Annotated MsmsSpectrum with fragment ion assignments
- Count of annotated peaks
- Fraction of observed peaks with interpretation (ratio)
- Comparative metric of annotation coverage (with vs. without neutral losses)

## How to apply

Load the spectrum using Universal Spectrum Identifier (USI) with spectrum_utils.MsmsSpectrum.from_usi(). Apply preprocessing: set m/z range to 100–1400, remove the precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance, filter low-intensity noise with filter_intensity() (min_intensity=0.05, max_num_peaks=50), and scale peak intensities by square root using scale_intensity('root'). Annotate fragment ions using annotate_proforma() with the ProForma peptide string and ion_types='aby', recording the count of annotated peaks. Repeat annotation with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled. Calculate and compare the fraction of observed peaks receiving interpretation in both conditions to quantify the effect of neutral loss annotation on coverage.

## Related tools

- **spectrum_utils** (Core library for spectrum loading, preprocessing (m/z range, precursor removal, intensity filtering and scaling), and fragment ion annotation using ProForma 2.0) — https://github.com/bittremieux/spectrum_utils/
- **ProForma 2.0** (Standard specification for expressing modified peptidoforms and their fragment annotations) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary for protein modifications referenced in ProForma annotation) — https://www.unimod.org/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
spectrum.set_mz_range(min_mz=100, max_mz=1400)
spectrum.remove_precursor_peak(fragment_tol_mass=10, fragment_tol_mode='ppm')
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50)
spectrum.scale_intensity('root')
spectrum.annotate_proforma('PEPTIDESEQ', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby')
baseline_count = sum(1 for peak in spectrum.peaks if peak.annotation)
spectrum.annotate_proforma('PEPTIDESEQ', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565})
neutral_loss_count = sum(1 for peak in spectrum.peaks if peak.annotation)
fraction_baseline = baseline_count / len(spectrum.peaks)
fraction_nl = neutral_loss_count / len(spectrum.peaks)
```

## Evaluation signals

- Annotated spectrum contains only peaks that fall within the specified fragment tolerance (10 ppm) of expected fragment m/z values for the peptide.
- Fraction of annotated peaks is non-negative and ≤ 1.0 (valid proportion).
- Enabling neutral loss annotation yields a higher or equal fraction of annotated peaks compared to the baseline condition (no neutral losses).
- The count of annotated peaks matches the length of the annotation list returned by annotate_proforma().
- Preprocessing steps (m/z range, precursor removal, intensity filtering, intensity scaling) are applied in the correct order and do not corrupt the spectrum object or introduce NaN values.

## Limitations

- Annotation accuracy depends critically on the correctness and completeness of the input ProForma peptide string; misspecified sequences or missed modifications will lead to undercounting of annotated peaks.
- Fragment tolerance (10 ppm in the example) is fixed; different mass spectrometers or ion types may require different tolerances, and no adaptive or machine-learning-based tolerance adjustment is provided.
- Neutral loss annotation is limited to a predefined set of losses (NH3 and H2O in the example); other common neutral losses (e.g., phosphoric acid, H3PO4) must be manually added to the dictionary.
- The skill does not account for isobaric peaks (e.g., multiple fragment ions with identical m/z); in such cases, the annotation may be ambiguous.

## Evidence

- [other] spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation to modulate peak interpretation coverage.: "spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks"
- [other] Retrieve spectrum from public repository using Universal Spectrum Identifier (USI) with spectrum_utils.MsmsSpectrum.from_usi(). Set m/z range to 100–1400 using set_mz_range(). Remove precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance. Filter low-intensity noise peaks using filter_intensity() with minimum intensity 0.05 and maximum 50 peaks. Scale peak intensities by square root using scale_intensity('root'). Annotate fragment ions using annotate_proforma() with ProForma peptide string, ion_types='aby', and neutral_losses disabled (default). Count annotated peaks and calculate fraction of observed peaks with interpretation. Repeat annotation step with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled.: "Set m/z range to 100–1400 using set_mz_range(). Remove precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance. Filter low-intensity noise peaks using filter_intensity() with"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms"
- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling)"
- [other] How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?: "enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation"
