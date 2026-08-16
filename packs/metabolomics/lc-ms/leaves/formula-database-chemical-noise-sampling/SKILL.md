---
name: formula-database-chemical-noise-sampling
description: Use when when you need to generate synthetic MS/MS spectra with chemical noise for validating denoising performance, benchmarking library matching algorithms, or testing edge cases where clean reference spectra exist but must be augmented with realistic contaminants.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - scipy
  - spectral-denoising
  - numpy
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- scipy==1.14.1
- '- ``scipy==1.14.1``'
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

# formula-database-chemical-noise-sampling

## Summary

Synthesize chemical noise ions for MS/MS spectra by randomly sampling m/z values from a pre-sorted formula database and assigning intensities from a Poisson distribution. This augments clean baseline spectra with chemically plausible but unwanted fragment ions to create realistic test datasets for benchmarking denoising algorithms.

## When to use

When you need to generate synthetic MS/MS spectra with chemical noise for validating denoising performance, benchmarking library matching algorithms, or testing edge cases where clean reference spectra exist but must be augmented with realistic contaminants. Apply this when you have a clean baseline spectrum (known ion composition) and require quantified reproducible noise injection to measure denoising robustness.

## When NOT to use

- Input spectra already contain real experimental noise or contamination — use only on clean reference spectra to avoid compounding artifacts.
- The goal is to denoise or filter an existing noisy spectrum — use denoising_search or electronic_denoising instead.
- Formula database is unavailable, unsorted, or not validated against the mass spectrometry platform used in your study.

## Inputs

- formula_db: pre-sorted chemical formula database indexed by m/z
- clean_spectrum: array of (m/z, intensity) pairs with shape (n_ions, 2)
- n_chemical_noise_ions: integer count of noise ions to inject
- lambda: Poisson distribution parameter for noise intensity generation
- precursor_m/z: mass-to-charge ratio of parent ion (for context/validation)

## Outputs

- noisy_spectrum: merged (m/z, intensity) array with deduplicated peaks
- noise_ion_pairs: array of synthesized (m/z, intensity) pairs from formula database
- spectrum_entropy: scalar entropy metric of resulting noisy spectrum

## How to apply

First, load or access a pre-sorted formula database (sorted by m/z mass, available via the project's shared drive) that contains chemically feasible fragment ion formulas. For each desired noise spectrum, randomly sample n formula entries from this database to obtain m/z values. For each sampled m/z, generate an intensity from a Poisson distribution with a specified lambda parameter (tunable to control noise magnitude). Merge the resulting noise ion pairs with the clean spectrum array, then remove duplicate m/z entries by keeping the highest intensity value. Validate the output by confirming (1) the noise ion count matches the requested n, (2) m/z ranges fall within plausible fragment space, and (3) entropy metrics shift predictably (e.g., normalized entropy should increase from clean to noisy spectrum).

## Related tools

- **spectral-denoising** (Python package providing generate_chemical_noise, add_noise, and validation utilities; wraps formula sampling and Poisson intensity generation) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Random sampling from formula database and Poisson distribution; array manipulation and deduplication)
- **scipy** (Poisson probability distribution sampling for noise intensity generation)

## Examples

```
from spectral_denoising.noise import generate_chemical_noise, add_noise; import numpy as np; noise_ions = generate_chemical_noise(formula_db, n=50, lambda_param=10.0); noisy_peak = add_noise(clean_peak, noise_ions)
```

## Evaluation signals

- Output noisy_spectrum contains exactly n_chemical_noise_ions + n_original_ions unique m/z entries (or fewer if collision occurred, with all collisions resolved by max-intensity rule).
- All sampled m/z values exist in the formula_db and fall within chemically plausible fragment m/z range (typically 50–precursor_m/z).
- Normalized entropy of noisy spectrum is strictly higher than clean spectrum and falls within expected range (e.g., 0.5–1.0).
- Poisson-sampled intensities follow expected distribution: mean ≈ lambda, all values ≥ 0, no negative or NaN entries.
- Entropy similarity (computed via entropy_similairty function) between noisy and clean spectra shows predictable degradation proportional to noise level and lambda parameter.

## Limitations

- Formula database must be pre-sorted by m/z for efficient random access; unsorted or incomplete databases will produce incorrect m/z distributions.
- Poisson sampling may generate very low intensities (near zero), which could be filtered out in downstream processing, reducing effective noise ion count.
- Chemical noise synthesis assumes uniform random sampling from formula_db; real chemical noise is often correlated with precursor structure and fragmentation pathway — this approach does not model those dependencies.
- Python version must be ≥ 3.8 and < 3.13 due to RDkit compatibility constraints (as of 2024-10-19).
- This skill generates synthetic noise only; it does not account for instrument-specific electronic noise patterns or systematic mass calibration errors.

## Evidence

- [other] Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson distribution with given lambda parameter, and create specified number of chemical noise ions.: "Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson"
- [other] Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity).: "Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity)."
- [other] Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges.: "Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges."
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] The formula_db can be found at: `Formula_db <https://drive.google.com/file/d/1pEXiGc5l0YjRGfCEZXW7-Wz6D1dOSBxA/view?usp=drive_link>`_. It is already sorted by mass.: "The formula_db can be found at: `Formula_db <https://drive.google.com/file/d/1pEXiGc5l0YjRGfCEZXW7-Wz6D1dOSBxA/view?usp=drive_link>`_. It is already sorted by mass."
- [intro] This project also provides useful tools to read, write, visualize and compare spectra.: "This project also provides useful tools to read, write, visualize and compare spectra."
