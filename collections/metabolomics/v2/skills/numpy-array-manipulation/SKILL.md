---
name: numpy-array-manipulation
description: Use when when you have raw MS/MS peak lists that need to be loaded, analyzed for intensity frequency patterns, or filtered based on noise characteristics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - numpy
  - spectral_denoising
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- peak = np.array([[69.071, 7.917962], [86.066, 1.021589], [86.0969, 100.0]], dtype=np.float32)
- numpy==2.1.1
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numpy-array-manipulation

## Summary

Manipulate mass spectrometry peak lists as 2D numpy arrays with [n, 2] structure (m/z and intensity columns) to enable efficient filtering, frequency analysis, and denoising of MS/MS spectra. This skill underpins electronic noise detection and removal in spectral preprocessing pipelines.

## When to use

When you have raw MS/MS peak lists that need to be loaded, analyzed for intensity frequency patterns, or filtered based on noise characteristics. Specifically, use this when you need to identify and remove electronic noise ions—characterized by identical intensity values occurring anomalously frequently within a single spectrum—before compound identification or spectral matching.

## When NOT to use

- When the input is already a high-level feature table (e.g., presence/absence matrix or aggregated metabolite abundances) rather than raw peak lists.
- When spectra have already been chemically validated using subformula loss rules; use electronic_denoising alone, not in combination with formula_denoising on pre-filtered data.
- When the spectrum contains genuine chemical ions with naturally high abundance that may coincidentally repeat; verify threshold appropriateness on your reference database first.

## Inputs

- 2D numpy array of shape [n, 2] containing m/z and intensity columns (dtype float32)
- Peak list from MSP file or programmatically generated spectrum

## Outputs

- Filtered 2D numpy array of shape [n, 2] with noise-flagged peaks removed
- Boolean mask or indices of peaks retained after denoising

## How to apply

Load peak data into a 2D numpy array of shape [n, 2] with m/z values in the first column and intensity values in the second. Use numpy operations to count the frequency of unique intensity values across all peaks in the spectrum. Compare intensity frequencies against an empirically validated threshold (e.g., >4 occurrences per unique intensity value); intensities exceeding this threshold are flagged as electronic noise. Filter the array to retain only rows whose intensity values fall below the threshold. Return the denoised spectrum as a numpy array maintaining the original [n, 2] shape. This approach exploits the observation that on the NIST23 database, genuine spectra contain <0.05% of ions with identical intensities repeated more than 4 times.

## Related tools

- **numpy** (Array creation, indexing, frequency counting (unique values), and conditional filtering for 2D peak list manipulation) — https://numpy.org
- **spectral_denoising** (High-level Python package providing electronic_denoising() and related spectral operations; wraps numpy array logic) — https://github.com/FanzhouKong/spectral_denoising
- **Python** (Scripting language for array operations; version >= 3.8 and < 3.13 required)

## Examples

```
import numpy as np; import spectral_denoising as sd; peak = np.array([[48.99, 154.0], [63.01, 265.0], [64.00, 663.0], [65.99, 596.0]], dtype=np.float32); peak_denoised = sd.electronic_denoising(peak)
```

## Evaluation signals

- Output array has same number of columns as input (2: m/z and intensity) and fewer or equal rows (peaks removed, never added).
- No peaks remain in the output whose intensity value appears >4 times in the denoised spectrum (validate by checking unique intensity frequencies post-filtering).
- Spectrum entropy metric calculated on denoised spectrum is equal to or lower than the raw spectrum (noise removal should not increase entropy).
- All m/z values in output array fall within expected chemical mass range for the precursor ion and known fragment ion space (sanity check).
- When compared to ground-truth spectra from reference databases, entropy similarity between denoised and reference spectrum increases relative to raw-spectrum entropy similarity.

## Limitations

- Threshold of >4 identical intensities is empirically derived from NIST23 database and may not generalize to all instrument types, ionization methods, or mass spectrometers (e.g., Orbitrap vs. TOF).
- Cannot distinguish electronic noise from genuine low-abundance chemical ions if they happen to have identical intensities; applies a frequency-based heuristic, not chemical validation.
- Does not address chemical noise (fragments from incorrect subformula losses); requires complementary formula_denoising for comprehensive denoising.
- Assumes intensity values are stored as floating-point numbers; rounding artifacts or intensity normalization schemes may affect frequency counting accuracy.

## Evidence

- [other] Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns. Count the frequency of each unique intensity value across all peaks. Identify intensity values that occur more than 4 times: "Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns. 2. Count the frequency of each unique intensity value across all peaks. 3. Identify intensity values that"
- [other] The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list.: "The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list."
- [other] Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. Return the denoised spectrum as a numpy array with the same shape as input.: "Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. 5. Return the denoised spectrum as a numpy array with the same shape as input."
- [other] a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra: "a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra"
- [readme] This repository in Python. A python version >= 3.8 is preferred, and must be < 3.13.: "This repository in Python. A python version >= 3.8 is preferred, and must be < 3.13."
