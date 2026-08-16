---
name: spectral-peak-annotation-using-proforma
description: Use when you have a tandem mass spectrum with observed m/z peaks and a known peptide sequence (as a ProForma string, optionally with post-translational modifications), and you want to determine which observed peaks correspond to expected fragment ions (b-type, y-type, a-type) within a specified.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - matplotlib
  - ProForma 2.0
  - spectrum_utils
  - Unimod
  - PSI-MOD
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- import matplotlib.pyplot as plt
- fig, ax = plt.subplots(figsize=(12, 6))
- Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/)
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
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

# spectral-peak-annotation-using-proforma

## Summary

Annotate observed mass spectrometry spectrum peaks with fragment ion types (b, y, a ions and neutral losses) using the ProForma 2.0 specification to interpret which peaks correspond to known peptide fragments. This skill quantifies the fraction of observed peaks receiving structural interpretation, enabling validation of fragmentation patterns and assessment of annotation coverage.

## When to use

You have a tandem mass spectrum with observed m/z peaks and a known peptide sequence (as a ProForma string, optionally with post-translational modifications), and you want to determine which observed peaks correspond to expected fragment ions (b-type, y-type, a-type) within a specified mass tolerance. Use this skill to measure how many peaks receive an annotation and whether enabling neutral loss interpretation (e.g., loss of H₂O at -18.010565 Da or NH₃ at -17.026549 Da) increases the fraction of interpreted peaks.

## When NOT to use

- Spectrum has no known peptide sequence or ProForma string available — annotation requires a reference sequence.
- Input spectrum is empty or contains only a single peak — annotation of multiple peaks is needed to meaningfully compute coverage.
- Fragment mass tolerance is extremely strict (e.g., <1 ppm) relative to instrument accuracy — may result in zero or near-zero annotation coverage due to systematic error rather than true lack of fragments.

## Inputs

- MsmsSpectrum object (with m/z and intensity arrays)
- ProForma 2.0 peptide string (e.g., '[Acetyl]-PEPTIDE-[Amidation]')
- Fragment mass tolerance (e.g., 10 ppm)
- Ion type specification (string: 'by', 'aby', etc.)
- Optional neutral loss dictionary (e.g., {'NH3': -17.026549, 'H2O': -18.010565})

## Outputs

- Annotated spectrum (MsmsSpectrum with peak-to-fragment ion mappings)
- Count of annotated peaks (integer)
- Fraction of annotated peaks (float, 0–1)
- Per-peak annotations (mapping of peak index to fragment ion type and mass error)

## How to apply

Load or construct a spectrum object (e.g., via MsmsSpectrum.from_usi() for USI-identified spectra). Pre-process the spectrum by setting the m/z range (typically 100–1400), removing the precursor peak using remove_precursor_peak() with a fragment tolerance (e.g., 10 ppm), filtering low-intensity noise using filter_intensity() with minimum intensity 0.05 and maximum 50 peaks, and scaling peak intensities using scale_intensity('root'). Call annotate_proforma() with the peptide sequence in ProForma format, specifying ion_types (e.g., 'by' for b and y ions, or 'aby' for a, b, and y ions), fragment_tol_mass and fragment_tol_mode (typically 10 ppm), and optionally enable neutral_losses as a dictionary mapping loss names to their mass shifts (e.g., {'NH3': -17.026549, 'H2O': -18.010565}). Count the number of annotated peaks and divide by the total number of peaks to obtain the fraction of interpreted spectrum. Repeat the annotation with and without neutral losses enabled to assess the improvement in annotation coverage.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class, annotate_proforma() method, and spectrum preprocessing functions (remove_precursor_peak, filter_intensity, scale_intensity, set_mz_range)) — https://github.com/bittremieux/spectrum_utils/
- **ProForma 2.0** (Specification for encoding peptide sequences with post-translational modifications used as input to fragment annotation) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary of protein modifications referenced in ProForma strings) — https://www.unimod.org/
- **PSI-MOD** (Controlled vocabulary of protein modifications compatible with ProForma annotation) — https://github.com/HUPO-PSI/psi-mod-CV/
- **matplotlib** (Used with spectrum_utils.plot.spectrum() to visualize annotated peaks post-annotation)

## Examples

```
spectrum.annotate_proforma(peptide='[Acetyl]-PEPTIDE[Phospho]-[Amidation]', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565}); annotated_count = sum(1 for peak in spectrum.peaks if peak.annotation); coverage = annotated_count / len(spectrum.peaks)
```

## Evaluation signals

- Annotated peaks match expected fragment ions: for a known peptide, verify that the highest-intensity peaks align with major b and y ions expected from complete digestion.
- Annotation coverage increases when neutral losses are enabled: the fraction of annotated peaks with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} must be ≥ the fraction without neutral losses.
- Mass error distribution is within tolerance: all annotated peaks must have |observed m/z − theoretical m/z| ≤ fragment_tol_mass (e.g., 10 ppm); inspect error distribution for systematic bias.
- Reproducibility check: repeated annotation of the same spectrum with identical parameters yields identical peak-to-ion assignments.
- Comparison to reference: if available, compare the annotated spectrum to a published reference spectrum of the same peptide; annotation coverage and peak assignments should align.

## Limitations

- Annotation accuracy depends critically on the correctness and completeness of the input ProForma string; misspecified modifications or incorrect sequence will produce misleading coverage metrics.
- Neutral loss annotation is only as effective as the provided loss dictionary; uncommon or instrument-specific losses not listed will be missed.
- Fragment tolerance (mass and ppm) must be calibrated to the mass spectrometer's accuracy; poorly calibrated instruments or spectra with significant m/z drift may show artificially low annotation coverage.
- Peptides with unusual charge states or incomplete fragmentation may exhibit low annotation coverage despite correct sequence and preprocessing; biological or instrumental factors beyond ProForma specification determine observable fragmentation patterns.
- No changelog is provided in the spectrum_utils repository, limiting traceability of changes to annotation algorithms across versions.

## Evidence

- [other] fragment ions can be annotated based on the ProForma 2.0 specification: "fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification"
- [other] annotate_proforma() method with ion_types parameter: ".annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types="aby")"
- [other] neutral loss annotation improves peak interpretation coverage: "Repeat annotation step 6 with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled. 9. Count annotated peaks in neutral-loss condition and recalculate fraction. 10. Compare fractions and"
- [other] spectrum preprocessing steps including filtering and scaling: "Filter low-intensity noise peaks using filter_intensity() with minimum intensity 0.05 and maximum 50 peaks. 5. Scale peak intensities by square root using scale_intensity('root'). 6. Annotate"
- [intro] loading spectra via Universal Spectrum Identifier: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
