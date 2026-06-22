---
name: mass-spectrum-peak-manipulation-merging
description: Use when after generating electronic noise (uniformly sampled m/z with Poisson-distributed intensities) and chemical noise (formula database-sampled m/z with Poisson intensities) and you need to combine both noise types with a clean baseline spectrum into a single unified peak array.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3714
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - scipy
  - spectral_denoising
  - numpy
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-manipulation-merging

## Summary

Combine electronic and chemical noise peaks with clean spectrum peaks by merging m/z arrays and resolving duplicate m/z entries to produce a consolidated peak array for benchmarking MS/MS spectra analysis. This skill is essential for creating synthetic noisy test datasets where peak intensities at identical m/z values must be reconciled by selecting the highest intensity.

## When to use

Apply this skill after generating electronic noise (uniformly sampled m/z with Poisson-distributed intensities) and chemical noise (formula database-sampled m/z with Poisson intensities) and you need to combine both noise types with a clean baseline spectrum into a single unified peak array. Use it during synthetic spectra generation for benchmarking denoising algorithms, when you must simulate realistic MS/MS noise contamination while preserving the highest-intensity peak at each m/z location.

## When NOT to use

- When input spectra are already denoised or do not contain duplicates—use this skill only when intentionally merging separate noise streams with a clean baseline.
- When m/z precision and rounding behavior differ between peak sources—inconsistent floating-point comparison may cause false negatives in duplicate detection; standardize m/z precision before merging.
- When you need to preserve all peak intensities for later statistical analysis—this merging operation discards sub-maximal intensity values, which may be required for uncertainty quantification or alternative noise models.

## Inputs

- clean baseline spectrum (numpy array of shape [n, 2] with m/z and intensity columns)
- electronic noise peaks (numpy array of shape [m, 2])
- chemical noise peaks (numpy array of shape [k, 2])

## Outputs

- merged and deduplicated peak array (numpy array of shape [p, 2] where p ≤ n+m+k, with duplicate m/z entries resolved to maximum intensity)

## How to apply

First, obtain three separate peak arrays: the clean baseline spectrum (m/z × intensity pairs), the generated electronic noise peaks, and the generated chemical noise peaks. Merge all three arrays into a single concatenated list of [m/z, intensity] pairs. Iterate through the merged array and identify duplicate m/z entries (treating m/z values as keys). For each duplicate m/z location, retain only the peak pair with the highest intensity value, discarding lower-intensity duplicates at that m/z. The rationale is that in real MS/MS spectra, a single m/z value produces one measured ion; by keeping the maximum intensity, the function preserves the strongest signal while eliminating redundant noise artifacts. Sort the deduplicated result by m/z to maintain standard spectral format.

## Related tools

- **spectral_denoising** (Python package providing add_noise and peak merging utilities; used to integrate generated electronic and chemical noise into clean spectra for creating test datasets) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Array manipulation and duplicate detection; enables efficient m/z grouping and intensity comparison operations)
- **scipy** (Statistical distributions (Poisson); used to generate noise intensities before merging)

## Examples

```
import numpy as np; from spectral_denoising.noise import add_noise; clean_peaks = np.array([[100.0, 500.0], [200.0, 300.0]], dtype=np.float32); electronic_noise = np.array([[150.0, 100.0]], dtype=np.float32); chemical_noise = np.array([[100.0, 50.0]], dtype=np.float32); merged_peaks = add_noise(clean_peaks, electronic_noise, chemical_noise)
```

## Evaluation signals

- Output array contains no duplicate m/z entries—verify by checking that all m/z values in the merged result are unique (no two rows share the same m/z within floating-point precision).
- Number of peaks in output does not exceed sum of input peaks: len(merged) ≤ len(clean) + len(electronic_noise) + len(chemical_noise).
- At each m/z location where duplicates existed in input, the retained intensity equals the maximum of all input intensities at that m/z.
- Output array is sorted by increasing m/z values—required for downstream spectral operations (comparison, visualization, database matching).
- Ion count and m/z range of output align with expected test dataset characteristics—verify against known baseline and noise parameters (Poisson lambda, m/z sampling bounds).

## Limitations

- Floating-point m/z precision: duplicate detection depends on exact or near-exact m/z matching; small measurement variations (e.g., rounding errors from different instruments or calculation pipelines) may cause false negatives in merging, leaving spurious duplicates in output.
- Loss of intensity diversity: by keeping only the maximum intensity at each m/z, the function discards information about competing noise sources; this simplification may not reflect complex multi-source noise in real spectra.
- No mass calibration or alignment: assumes all input peak arrays are already calibrated to the same m/z reference frame; if inputs use different mass calibrations or instrument resolutions, merging will create false duplicates or miss true ones.
- Scale dependence on Poisson parameter lambda: noise intensity distribution depends critically on lambda choice in generate_noise and generate_chemical_noise; inappropriately tuned lambda values produce unrealistic noise and may fail to create challenging test cases for denoising validation.

## Evidence

- [other] Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity).: "Define add_noise function to combine clean spectrum with generated noise by merging peak arrays and removing duplicate m/z entries (keeping highest intensity)."
- [other] Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges.: "Validate both functions by creating test spectra with known baseline, adding noise, and confirming output arrays contain expected ion counts and m/z ranges."
- [other] This project also provides useful tools to read, write, visualize and compare spectra.: "This project also provides useful tools to read, write, visualize and compare spectra."
- [readme] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
