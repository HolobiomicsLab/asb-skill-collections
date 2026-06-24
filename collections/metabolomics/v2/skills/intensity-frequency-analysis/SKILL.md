---
name: intensity-frequency-analysis
description: Use when you have an MS/MS peak list and need to remove electronic noise—specifically
  when you observe suspiciously identical intensity values repeated across multiple
  peaks in a single spectrum, which is characteristic of instrument-generated artifacts
  rather than genuine analyte signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectral_denoising (Python package)
  - NumPy
  - ms_entropy
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_denoising_cq
    doi: 10.1038/s41592-025-02646-x
    title: Spectral Denoising
  dedup_kept_from: coll_spectral_denoising_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02646-x
  all_source_dois:
  - 10.1038/s41592-025-02646-x
  - 10.1038/s41592-023-02012-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Intensity-Frequency Analysis

## Summary

A noise-detection algorithm that identifies electronic artifacts in MS/MS spectra by counting the frequency of duplicate intensity values within a single peak list. Peaks whose intensity values occur more than 4 times are flagged as probable electronic noise and removed.

## When to use

Apply this skill when you have an MS/MS peak list and need to remove electronic noise—specifically when you observe suspiciously identical intensity values repeated across multiple peaks in a single spectrum, which is characteristic of instrument-generated artifacts rather than genuine analyte signals.

## When NOT to use

- Input spectrum already has chemical noise or formula-based artifacts; use formula_denoising instead.
- Peak list is already preprocessed or from instruments with known low electronic noise profiles.
- You need to distinguish between electronic and chemical noise simultaneously; use spectral_denoising (the wrapper) which combines electronic_denoising and formula_denoising.

## Inputs

- MS/MS peak list (2D NumPy array, shape [n, 2], dtype float32 with m/z and intensity columns)
- Peak frequency threshold (default: 4 occurrences per unique intensity value)

## Outputs

- Denoised MS/MS peak list (2D NumPy array, same shape as input, with electronic noise peaks removed)

## How to apply

Load the MS/MS peak list as a 2D NumPy array with shape [n, 2] containing m/z and intensity columns. Count the frequency of each unique intensity value across all peaks in the spectrum. Identify intensity values that occur more than 4 times; this threshold was empirically validated on the NIST23 database where such occurrences are <0.05% in genuine spectra, making them statistically unlikely to represent real signals. Filter the peak list to retain only peaks whose intensity values do not exceed this frequency threshold. Return the denoised spectrum as a NumPy array with the same shape as the input.

## Related tools

- **spectral_denoising (Python package)** (Implements electronic_denoising function alongside formula_denoising for comprehensive noise removal) — https://github.com/FanzhouKong/spectral_denoising
- **NumPy** (Underlying array manipulation and frequency counting operations)
- **ms_entropy** (Spectral entropy calculation for quality assessment of denoised spectra)

## Examples

```
peak_denoised = sd.electronic_denoising(peak)
```

## Evaluation signals

- Output peak list has fewer peaks than input (noise peaks removed) but shape is preserved as [n', 2]
- No peaks remain whose intensity value appears >4 times in the denoised spectrum
- Entropy similarity between denoised spectrum and reference spectrum increases compared to pre-denoising similarity
- Normalized entropy of denoised spectrum is lower than raw spectrum (reduced randomness)
- All remaining peaks have m/z and intensity values identical to input (no spurious modifications to genuine signals)

## Limitations

- Threshold of 4 intensity occurrences was empirically validated only on NIST23 database; generalization to other instruments or ionization methods untested
- Cannot distinguish between electronic noise and genuine isobaric peaks with legitimately identical intensities (rare but possible)
- Does not address chemical noise (neutral losses, in-source fragmentation); use formula_denoising for those
- Sensitive to input data type—requires float32 arrays; integer or other dtypes may behave unpredictably

## Evidence

- [other] The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list.: "The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list."
- [other] Count the frequency of each unique intensity value across all peaks. Identify intensity values that occur more than 4 times (a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra).: "Count the frequency of each unique intensity value across all peaks. Identify intensity values that occur more than 4 times (a threshold empirically validated on NIST23 database where such"
- [other] Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. Return the denoised spectrum as a numpy array with the same shape as input.: "Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. Return the denoised spectrum as a numpy array with the same shape as input."
- [other] Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns.: "Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns."
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [readme] perform electronic denoising: "peak_denoised = sd.electronic_denoising(peak)"
