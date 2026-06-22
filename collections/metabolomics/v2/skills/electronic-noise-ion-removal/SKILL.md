---
name: electronic-noise-ion-removal
description: Use when working with raw MS/MS spectra that contain ions with repeated (identical) intensity values—a hallmark of electronic noise rather than true metabolite fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pandas
  - RDkit
  - spectral_denoising
  - ms_entropy
  - numpy
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- pandas==2.2.3
- '- ``pandas==2.2.3``'
- rdkit==2024.3.5
- smiles = 'O=c1nc[nH]c2nc[nH]c12'
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
---

# electronic-noise-ion-removal

## Summary

Remove spurious ions arising from instrument artifacts in MS/MS spectra by filtering peaks with identical intensities that exceed a statistical threshold, improving spectral quality for downstream matching and annotation. This addresses electronic noise as a major category of contamination in mass spectrometry data.

## When to use

Apply this skill when working with raw MS/MS spectra that contain ions with repeated (identical) intensity values—a hallmark of electronic noise rather than true metabolite fragments. Use it before spectral comparison or denoising search workflows when entropy-based similarity metrics must be reliable, or when high-confidence compound identification is required. The empirical threshold of >4 ions with identical intensities is applicable after validation on reference libraries like NIST23.

## When NOT to use

- Input spectra are already electronically cleaned or processed by vendor denoising software.
- Analysis goal does not require high-confidence spectral matching (e.g., exploratory, low-resolution screening).
- Spectrum originates from instruments with negligible electronic noise signatures (verify against instrument/method literature first).

## Inputs

- MS/MS peak array (numpy array of shape [n_peaks, 2] with columns [m/z, intensity])
- MSP-formatted spectrum file (containing peaks, precursor_mz, and molecular metadata)
- Single spectrum object or batch of spectra from sd.read_msp()

## Outputs

- Denoised peak array with electronic noise ions removed (same format as input)
- Peak array ready for downstream entropy_similarity() or formula_denoising() operations
- Batch of denoised spectra when operating in parallel mode

## How to apply

Load a peak array (m/z, intensity pairs) from an MSP file or spectrum object using sd.read_msp(). Pass the peak array to the electronic_denoising() function, which identifies and removes ions having identical intensities that occur more than 4 times in a single spectrum—a threshold determined to be statistically unlikely in real MS/MS data. The function returns a cleaned peak array with electronic noise removed but preserves the chemical signal. Apply this as a first-pass filter before formula_denoising() or spectral_denoising() to ensure clean input for entropy similarity calculations.

## Related tools

- **spectral_denoising** (Python package providing electronic_denoising() function and integrated spectral workflow) — https://github.com/FanzhouKong/spectral_denoising
- **ms_entropy** (Computes spectral entropy and entropy_similarity() for downstream validation of denoising efficacy)
- **numpy** (Array manipulation and storage of peak m/z and intensity data)

## Examples

```
import spectral_denoising as sd
import numpy as np
peak = np.array([[48.99, 154.0], [63.01, 265.0], [79.02, 521.0]], dtype=np.float32)
peak_denoised = sd.electronic_denoising(peak)
```

## Evaluation signals

- Output peak array contains fewer peaks than input; confirm that only ions with ≥5 identical intensity counts were removed.
- Entropy similarity between denoised spectrum and clean reference increases compared to raw spectrum (verify using entropy_similarity function).
- No fragment m/z values corresponding to known metabolite losses are removed; validate that chemical signal is preserved by comparing against reference library spectra.
- Precursor m/z and base peak m/z remain unchanged after denoising (electronic noise removal should not alter true fragment ions).
- Spectral entropy value of output spectrum is stable (does not artificially inflate due to peak removal artifacts).

## Limitations

- Threshold of >4 identical intensities is empirically derived from NIST23 and may not generalize to all instruments, acquisition methods, or mass ranges.
- Cannot distinguish between electronic noise and legitimate multiply-charged or isobaric fragment ions that coincidentally share intensity values.
- Removal is absolute and irreversible; spectra with naturally clustered intensity distributions (e.g., from isotope patterns) may suffer false-positive filtering.
- Requires peak arrays as input; does not handle raw binary vendor formats (.raw, .d) without prior conversion via standard MS data readers.

## Evidence

- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] The ``electronic_denoising`` function removes obvious electronic noise ions in MS/MS spectra: "The ``electronic_denoising`` function removes obvious electronic noise ions in MS/MS spectra"
- [other] According to empiracally tested on NIST23 database, in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely: "in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely"
- [other] Apply electronic_denoising() to remove ions with identical intensities >4.: "Apply electronic_denoising() to remove ions with identical intensities >4."
- [readme] peak_denoised = sd.electronic_denoising(peak): "Perform electronic denoising  [section=other; evidence='peak_denoised = sd.electronic_denoising(peak)']"
