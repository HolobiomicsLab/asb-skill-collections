---
name: intensity-distribution-simulation
description: Use when when you need to create synthetic noisy MS/MS spectra from clean baseline spectra to validate denoising algorithms, compare denoising performance across noise levels, or generate ground-truth test datasets where the true signal and noise composition are known and controllable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - scipy
  - numpy
  - spectral_denoising (spectral-denoising package)
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

# Intensity-Distribution Simulation

## Summary

Synthesize realistic electronic and chemical noise ions by sampling m/z values and drawing intensities from Poisson distributions, enabling creation of benchmarking datasets with controlled noise characteristics for MS/MS spectrum denoising validation.

## When to use

When you need to create synthetic noisy MS/MS spectra from clean baseline spectra to validate denoising algorithms, compare denoising performance across noise levels, or generate ground-truth test datasets where the true signal and noise composition are known and controllable.

## When NOT to use

- When you need to denoise real experimental spectra—simulation adds synthetic noise but does not remove actual noise from measured data.
- When your goal is to assess denoising performance on authentic noise distributions—simulated Poisson-drawn intensities may not capture real electronic or chemical noise characteristics.
- When the input spectrum is already contaminated with real noise and you want to validate denoising on ground truth—use synthetic clean spectra instead.

## Inputs

- clean spectrum (m/z, intensity pairs as numpy array)
- precursor m/z value
- formula database (sorted by mass)
- lambda parameter for Poisson distribution
- desired number of electronic noise ions
- desired number of chemical noise ions

## Outputs

- noisy spectrum (m/z, intensity pairs with synthetic noise added)
- noise ion array (electronic noise component)
- chemical noise ion array (chemical noise component)

## How to apply

Define separate noise generation pipelines for electronic and chemical noise. For electronic noise: uniformly sample m/z values between 50 and the precursor m/z, then draw intensities from a Poisson distribution with a specified lambda parameter, creating a defined number of noise ion pairs. For chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from the same Poisson distribution, and create the desired number of chemical noise ions. Merge the generated noise peaks with the clean spectrum's peak array, removing duplicate m/z entries by retaining the highest intensity at each m/z. Validate the synthetic spectra by confirming the output arrays contain the expected ion counts and m/z ranges matching your simulation parameters.

## Related tools

- **numpy** (Array operations for m/z and intensity sampling and merging)
- **scipy** (Poisson distribution sampling for intensity generation)
- **spectral_denoising (spectral-denoising package)** (Implementation of generate_noise, generate_chemical_noise, and add_noise functions; spectrum validation and comparison) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
from spectral_denoising.noise import *; import numpy as np; peak_with_noise = add_noise(peak, precursor_mz=200.0, lambda_elec=0.5, num_elec=5, lambda_chem=0.8, num_chem=8); print(peak_with_noise.shape)
```

## Evaluation signals

- Output noise spectrum contains the sum of original peaks plus generated electronic and chemical noise ions, with no duplicate m/z entries.
- Generated electronic noise m/z values fall within [50, precursor_mz] range.
- Generated chemical noise m/z values exist in the formula_db and are chemically plausible fragment losses.
- Intensity values from both noise sources follow Poisson distribution with specified lambda; mean intensity ≈ lambda.
- Ion counts in output match expected total: original peak count + electronic noise count + chemical noise count (minus any m/z collisions retained as maximum intensity).

## Limitations

- Poisson-sampled intensities may not accurately represent the statistical properties of real electronic and chemical noise in actual MS/MS instruments.
- The approach assumes uniform m/z sampling for electronic noise, which may not reflect true instrument noise patterns across different mass ranges.
- Chemical noise generation relies on the completeness and accuracy of the pre-sorted formula_db; missing formulas will not be represented in synthetic noise.
- Noise intensity distribution is independent of m/z; real noise often exhibits m/z-dependent behavior not captured by this method.
- The method does not account for instrument-specific noise characteristics (e.g., detector saturation, baseline drift) and is best used for controlled benchmarking rather than realistic noise simulation.

## Evidence

- [other] Define generate_noise function to synthesize electronic noise: sample m/z values uniformly between 50 and precursor m/z, generate intensities from Poisson distribution with parameter lambda, and create specified number of noise ion pairs.: "Define generate_noise function to synthesize electronic noise: sample m/z values uniformly between 50 and precursor m/z, generate intensities from Poisson distribution with parameter lambda, and"
- [other] Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson distribution with given lambda parameter, and create specified number of chemical noise ions.: "Define generate_chemical_noise function to synthesize chemical noise: randomly sample m/z values from a pre-sorted formula database (formula_db), generate corresponding intensities from Poisson"
- [other] Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity).: "Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity)."
- [other] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [readme] generate some noise ions and add it to the peaks: "# generate some noise ions and add it to the peaks"
