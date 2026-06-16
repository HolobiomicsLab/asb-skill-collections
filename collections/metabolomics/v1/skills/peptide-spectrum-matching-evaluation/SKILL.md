---
name: peptide-spectrum-matching-evaluation
description: 'Use when when you have a tandem mass spectrum (MSMS) with known peptide sequence and wish to assess whether enabling neutral loss annotation (e.g., NH3: −17.026549, H2O: −18.010565) increases the proportion of observed m/z peaks that can be matched to predicted fragment ions.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - ProForma 2.0
  - Universal Spectrum Identifier (USI)
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
---

# Peptide-Spectrum Matching Evaluation

## Summary

Evaluate the quality and completeness of peptide-spectrum matches by quantifying the fraction of observed peaks that receive fragment ion annotations under different annotation strategies (e.g., with and without neutral losses). This skill measures how effectively fragment annotation settings improve peak interpretation coverage.

## When to use

When you have a tandem mass spectrum (MSMS) with known peptide sequence and wish to assess whether enabling neutral loss annotation (e.g., NH3: −17.026549, H2O: −18.010565) increases the proportion of observed m/z peaks that can be matched to predicted fragment ions. Use this skill to benchmark annotation parameter choices or validate that neutral loss annotation improves peak coverage against a reported baseline.

## When NOT to use

- The peptide sequence is unknown or unreliable — annotation requires correct sequence input.
- The spectrum is from a non-peptide analyte (e.g., small molecule, glycan) — ProForma annotation is designed for modified peptidoforms.
- You are evaluating de novo peptide sequencing or spectrum-to-spectrum similarity without a reference sequence.

## Inputs

- Universal Spectrum Identifier (USI) string
- ProForma 2.0 peptide sequence string
- Fragment mass tolerance (ppm)
- Ion types to annotate (e.g., 'aby')

## Outputs

- Fraction of peaks annotated without neutral losses
- Fraction of peaks annotated with neutral losses
- Difference in annotation coverage
- Count of annotated peaks (both conditions)

## How to apply

Load a spectrum from a public repository using the Universal Spectrum Identifier (USI) and the spectrum_utils.MsmsSpectrum.from_usi() method. Preprocess the spectrum by setting m/z range to 100–1400, removing the precursor peak (using 10 ppm fragment tolerance), filtering low-intensity noise peaks (minimum intensity 0.05, maximum 50 peaks), and scaling peak intensities by square root. Annotate fragment ions using spectrum_utils.annotate_proforma() with a ProForma peptide string and ion_types='aby', first with neutral_losses disabled (default). Count the number of annotated peaks and calculate the fraction of observed peaks with interpretation. Repeat the annotation step with neutral_losses enabled (e.g., {'NH3': -17.026549, 'H2O': -18.010565}). Compare the two fractions and verify the increase matches reported benchmarks.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum.from_usi(), spectrum preprocessing (set_mz_range, remove_precursor_peak, filter_intensity, scale_intensity), and annotate_proforma() for fragment annotation with ProForma 2.0 and optional neutral loss configuration) — https://github.com/bittremieux/spectrum_utils/
- **ProForma 2.0** (Specification for defining modified peptidoforms and interpreting fragment ions during annotation) — https://www.psidev.info/proforma
- **Universal Spectrum Identifier (USI)** (Mechanism for retrieving spectra from online proteomics and metabolomics data repositories)

## Examples

```
spectrum = spectrum_utils.MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.set_mz_range(100, 1400).remove_precursor_peak(10, 'ppm').filter_intensity(0.05, 50).scale_intensity('root'); frac_no_nl = len(spectrum.annotate_proforma('PEPTIDE', 10, 'ppm', ion_types='aby')) / len(spectrum.peaks); frac_with_nl = len(spectrum.annotate_proforma('PEPTIDE', 10, 'ppm', ion_types='aby', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565})) / len(spectrum.peaks); print(f'Increase: {frac_with_nl - frac_no_nl}')
```

## Evaluation signals

- The annotation fraction with neutral losses enabled must be greater than or equal to the fraction without neutral losses (monotonic increase).
- The absolute number of annotated peaks should increase when neutral losses are enabled, given the same observed spectrum.
- The difference in fractions should be statistically meaningful and comparable to reported benchmarks from the article or repository documentation.
- Verify that the ion_types parameter ('aby') is correctly applied and that only the specified ion types contribute to the annotation counts.
- Confirm that the spectrum preprocessing steps (m/z range 100–1400, precursor removal at 10 ppm, intensity filtering with min 0.05 and max 50 peaks) were applied before annotation.

## Limitations

- Evaluation depends on the accuracy of the input ProForma peptide sequence; incorrect sequences will produce misleading annotation fractions.
- The choice of ion_types ('aby') is fixed in the workflow; evaluation does not assess sensitivity to other ion type combinations (e.g., 'abyz').
- Neutral loss mass values (NH3: −17.026549, H2O: −18.010565) are hard-coded in the workflow; other neutral losses or custom modifications are not explored.
- No changelog is available in the repository, so version-specific behavior or parameter defaults are not documented.
- The skill evaluates only peak coverage (fraction annotated) and does not assess annotation correctness (false positives or mass accuracy errors).

## Evidence

- [other] How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?: "How does enabling neutral loss annotation in spectrum_utils.fragment_annotation affect the fraction of observed peaks that receive an interpretation?"
- [other] spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation to modulate peak interpretation coverage.: "spectrum_utils provides fragment annotation functionality using the ProForma 2.0 specification to interpret observed spectrum peaks, with the capability to enable or disable neutral loss annotation"
- [other] 1. Retrieve spectrum from public repository using Universal Spectrum Identifier (USI) with spectrum_utils.MsmsSpectrum.from_usi(). 2. Set m/z range to 100–1400 using set_mz_range(). 3. Remove precursor peak using remove_precursor_peak() with 10 ppm fragment tolerance. 4. Filter low-intensity noise peaks using filter_intensity() with minimum intensity 0.05 and maximum 50 peaks. 5. Scale peak intensities by square root using scale_intensity('root'). 6. Annotate fragment ions using annotate_proforma() with ProForma peptide string, ion_types='aby', and neutral_losses disabled (default). 7. Count annotated peaks and calculate fraction of observed peaks with interpretation. 8. Repeat annotation step 6 with neutral_losses={'NH3': -17.026549, 'H2O': -18.010565} enabled. 9. Count annotated peaks in neutral-loss condition and recalculate fraction. 10. Compare fractions and verify increase against reported benchmark.: "Annotate fragment ions using annotate_proforma() with ProForma peptide string, ion_types='aby', and neutral_losses disabled (default). 7. Count annotated peaks and calculate fraction of observed"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
