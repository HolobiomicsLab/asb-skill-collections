---
name: spectral-noise-synthesis-poisson-distribution
description: Use when when you have clean, baseline MS/MS spectra and need to create test datasets with known noise characteristics to benchmark denoising algorithms, compare denoising search performance, or validate that electronic and chemical noise removal functions correctly identify and remove injected.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - scipy
  - spectral-denoising (Python package)
  - numpy
  - RDkit
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

# spectral-noise-synthesis-poisson-distribution

## Summary

Synthesize electronic and chemical noise ions for MS/MS spectra using Poisson-distributed intensities to create realistic noisy test datasets for benchmarking denoising and spectral matching algorithms. This skill enables controlled injection of known noise types into clean baseline spectra to evaluate robustness of compound identification workflows.

## When to use

When you have clean, baseline MS/MS spectra and need to create test datasets with known noise characteristics to benchmark denoising algorithms, compare denoising search performance, or validate that electronic and chemical noise removal functions correctly identify and remove injected noise while preserving true fragment ions.

## When NOT to use

- Spectrum already contains real experimental noise that you wish to preserve or analyze—this skill replaces the spectrum with synthetic noise rather than augmenting real noise.
- You need to model noise characteristics from an existing contaminated spectrum—use denoising search or entropy similarity instead to reverse-engineer noise patterns.
- Input spectrum is in an unsupported format (not numpy array with [m/z, intensity] pairs)—convert or validate format first.

## Inputs

- clean spectrum (numpy array: shape [n, 2], dtype float32, columns [m/z, intensity])
- precursor m/z (float)
- lambda parameter for Poisson distribution (float, intensity scaling factor)
- number of electronic noise ions to inject (integer)
- number of chemical noise ions to inject (integer)
- formula database (pre-sorted by mass, list or array of molecular formulas)

## Outputs

- noisy spectrum (numpy array: shape [m, 2], dtype float32, merged and deduplicated [m/z, intensity] pairs)
- noise ion count validation report (integer: total ions after deduplication)

## How to apply

Generate electronic noise by uniformly sampling m/z values between 50 and the precursor m/z, drawing intensities from a Poisson distribution with a specified lambda parameter, and creating a user-defined number of noise ion pairs. For chemical noise, randomly sample m/z values from a pre-sorted formula database (sorted by mass) and assign intensities from the same Poisson distribution. Merge the generated noise arrays with the clean spectrum peak array, then remove duplicate m/z entries by keeping only the highest intensity for each m/z position. Validate the synthetic dataset by confirming the output arrays contain the expected total ion count (original + injected noise ions) and that m/z ranges match the specified bounds (50 to precursor_mz for electronic noise, formula_db range for chemical noise).

## Related tools

- **spectral-denoising (Python package)** (Host library containing generate_noise, generate_chemical_noise, and add_noise functions; also provides read_msp, write_msp, spectral_entropy, and normalized_entropy utilities for I/O and validation of synthetic datasets.) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Array creation, Poisson sampling (numpy.random.poisson), uniform sampling (numpy.random.uniform), and array merging for noise synthesis and deduplication.)
- **scipy** (Statistical distributions and array operations for Poisson parameter validation and optional intensity transformation.)
- **RDkit** (Optional: chemical formula parsing and validation if formula database requires on-the-fly structure checks.)

## Examples

```
import numpy as np
import spectral_denoising as sd
from spectral_denoising.noise import *
peak_clean = np.array([[48.99, 154.0], [63.01, 265.0]], dtype=np.float32)
electronic_noise = sd.generate_noise(precursor_mz=200.0, lambda_param=5.0, num_ions=10)
chemical_noise = sd.generate_chemical_noise(lambda_param=3.0, num_ions=15)
peak_noisy = sd.add_noise(peak_clean, electronic_noise + chemical_noise)
```

## Evaluation signals

- Output spectrum m/z range for electronic noise exactly matches [50, precursor_mz]; no synthetic ions fall outside this range.
- Output spectrum m/z range for chemical noise exactly matches the min and max masses in the pre-sorted formula_db.
- Output ion count equals input ion count plus the number of injected noise ions (after deduplication); deduplication removes fewer ions than the number of duplicate m/z keys introduced.
- Spectrum entropy of synthetic noisy spectrum is measurably higher than the clean baseline spectrum (entropy_similarity < 1.0); entropy_similarity(noisy, clean, pmz) < entropy_similarity(denoised, clean, pmz) after denoising.
- No duplicate m/z values remain in the output array; each m/z entry retains the highest intensity among collisions.

## Limitations

- Poisson distribution assumes random, uncorrelated intensity fluctuations; real electronic noise may show temporal correlations or systematic bias that this model does not capture.
- Chemical noise depends entirely on the completeness and accuracy of the pre-sorted formula_db; missing or incorrect formulas will not be represented in synthetic noise.
- Uniform m/z sampling for electronic noise does not account for instrument detection sensitivity variations across the m/z range.
- The deduplication step (keeping max intensity per m/z) may underestimate noise severity if real spectra exhibit m/z collisions with lower total intensity; use with caution for very high-noise benchmarking.

## Evidence

- [other] Define generate_noise function to synthesize electronic noise: sample m/z values uniformly between 50 and precursor m/z, generate intensities from Poisson distribution with parameter lambda, and create specified number of noise ion pairs.: "Define generate_noise function to synthesize electronic noise: sample m/z values uniformly between 50 and precursor m/z, generate intensities from Poisson distribution with parameter lambda, and"
- [other] Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson distribution with given lambda parameter, and create specified number of chemical noise ions.: "Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson"
- [other] Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity).: "Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity)."
- [other] Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges.: "Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges."
- [other] The formula_db can be found at: Formula_db. It is already sorted by mass.: "The formula_db can be found at: `Formula_db`. It is already sorted by mass."
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
