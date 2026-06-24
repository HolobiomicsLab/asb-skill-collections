---
name: neutral-loss-peak-interpretation
description: Use when you have a tandem mass spectrum (MSMS) loaded via USI and wish
  to maximize the interpretability of observed peaks.
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

# neutral-loss-peak-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Enable neutral loss annotation in spectrum_utils.fragment_annotation to increase the fraction of observed tandem MS peaks that receive molecular ion interpretation via ProForma 2.0. This skill quantifies the improvement in peak coverage when neutral losses (e.g., NH₃, H₂O) are explicitly modeled alongside standard a/b/y fragment ions.

## When to use

You have a tandem mass spectrum (MSMS) loaded via USI and wish to maximize the interpretability of observed peaks. Use this skill when the default fragment annotation (a/b/y ions only) leaves a substantial fraction of peaks without interpretation, and you want to measure whether enabling neutral loss annotation increases coverage. This is especially relevant when analyzing peptidoforms with labile modifications or when fragment ion assignments are sparse.

## When NOT to use

- Input spectrum is a precursor (MS1) scan rather than a tandem (MSMS) fragmentation spectrum; neutral loss annotation applies only to fragment ion interpretation.
- ProForma peptide string is missing or invalid; annotate_proforma() requires a well-formed peptidoform sequence.
- Fragment tolerance (e.g., >50 ppm) is already so permissive that most peaks are annotated by default; neutral loss gains will be marginal.

## Inputs

- Universal Spectrum Identifier (USI) string
- ProForma 2.0 peptide string with optional modifications
- Fragment ion tolerance (mass and mode: ppm or Da)
- Intensity filtering thresholds (min_intensity, max_num_peaks)
- m/z range bounds (min_mz, max_mz)

## Outputs

- Annotated spectrum object with peak-to-ion assignments (default: no neutral losses)
- Annotated spectrum object with peak-to-ion assignments (neutral losses enabled)
- Fraction of observed peaks with interpretation (default condition)
- Fraction of observed peaks with interpretation (neutral loss condition)
- Comparison metric (e.g., absolute or relative increase in fraction)

## How to apply

Load a spectrum using spectrum_utils.MsmsSpectrum.from_usi() with a Universal Spectrum Identifier. Preprocess the spectrum by setting m/z range to 100–1400 with set_mz_range(), removing the precursor peak with remove_precursor_peak() using a 10 ppm fragment tolerance, filtering low-intensity noise peaks with filter_intensity(min_intensity=0.05, max_num_peaks=50), and scaling intensities by square root using scale_intensity('root'). Annotate fragment ions once with annotate_proforma() using the ProForma peptide string, ion_types='aby', and neutral_losses disabled (default state). Count the number of annotated peaks and compute the fraction of observed peaks with interpretation. Repeat the annotation step with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled, recount annotated peaks, and recalculate the fraction. Compare the two fractions to verify that enabling neutral losses increases peak coverage above a baseline benchmark.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum class, spectrum preprocessing methods (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity), and annotate_proforma() function for ProForma 2.0 fragment annotation with configurable neutral loss support.) — https://github.com/bittremieux/spectrum_utils
- **ProForma 2.0** (Specification for encoding peptide sequences with modifications and fragment ions; used as input format for annotate_proforma() and governs interpretation of annotated peaks.) — https://www.psidev.info/proforma
- **Python** (Programming language in which spectrum_utils is implemented; required for executing the skill workflow.)

## Examples

```
spectrum = spectrum_utils.MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.set_mz_range(min_mz=100, max_mz=1400); spectrum.remove_precursor_peak(10, 'ppm'); spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50); spectrum.scale_intensity('root'); annotated_default = spectrum.annotate_proforma('PEPTIDEK', 10, 'ppm', ion_types='aby'); annotated_nl = spectrum.annotate_proforma('PEPTIDEK', 10, 'ppm', ion_types='aby', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565}); frac_default = annotated_default.count() / len(spectrum); frac_nl = annotated_nl.count() / len(spectrum);
```

## Evaluation signals

- Fraction of observed peaks with interpretation increases when neutral_losses parameter is enabled compared to default (neutral_losses=None or False).
- Annotated peak count is strictly greater or equal in the neutral-loss condition than in the default condition (monotonic improvement).
- Neutral loss masses in the neutral_losses dictionary match expected chemical losses: -17.026549 Da for NH₃, -18.010565 Da for H₂O (or other specified losses).
- The fraction of annotated peaks in both conditions remains within [0, 1] and represents a valid proportion of the total observed peaks.
- Reported peak interpretation fractions match or exceed published benchmarks for the same spectrum (e.g., from the spectrum_utils documentation or the Bittremieux et al. 2019 article).

## Limitations

- The skill measures only fragment ion interpretation; it does not assess the correctness or biological relevance of those interpretations.
- Neutral loss gains are contingent on the peptidoform and spectrum quality; heavily fragmented or noise-dominated spectra may show minimal improvement.
- The fixed neutral loss dictionary {'NH3': -17.026549, 'H2O': -18.010565} covers only common losses; exotic modifications or non-standard fragmentation patterns require custom neutral loss definitions.
- No changelog is available in the spectrum_utils repository, limiting historical tracking of changes to neutral loss annotation behavior across versions.
- The skill requires valid USI identifiers and ProForma strings; invalid or corrupted input will cause runtime errors without informative fallback.

## Evidence

- [other] Fragment annotation with neutral losses: "Repeat annotation step 6 with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled."
- [other] ProForma specification for fragment interpretation: "fragment ions can be annotated based on the ProForma 2.0 specification"
- [other] Preprocessing workflow for spectrum normalization: "Set m/z range to 100–1400 using set_mz_range(). 3. Remove precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance. 4. Filter low-intensity noise peaks using filter_intensity()"
- [intro] Spectrum loading from online repositories via USI: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
- [other] Fragment annotation with configurable ion types: "Annotate fragment ions using annotate_proforma() with ProForma peptide string, ion_types='aby', and neutral_losses disabled (default)."
