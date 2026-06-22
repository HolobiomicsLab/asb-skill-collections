---
name: precursor-region-handling-and-m-z-tolerance-management
description: Use when when computing entropy_similarity() between experimental (noisy or denoised) MS/MS spectra and reference library spectra, if the precursor m/z value is known and available.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - RDkit
  - entropy_similarity
  - ms_entropy
  - spectral_denoising
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

# precursor-region-handling-and-m/z-tolerance-management

## Summary

Excludes or masks the precursor m/z region from spectral similarity calculations to prevent artificially inflated entropy similarity scores caused by dominant precursor ions. This is applied when comparing noisy or denoised MS/MS spectra against reference spectra to ensure fragment ion composition, not precursor ion abundance, drives the matching metric.

## When to use

When computing entropy_similarity() between experimental (noisy or denoised) MS/MS spectra and reference library spectra, if the precursor m/z value is known and available. Precursor masking is critical to avoid inflated similarity scores when the dominant peak in the spectrum is the intact precursor ion rather than informative fragment ions.

## When NOT to use

- Input spectra have already had precursor ions artificially removed or are known to be free of precursor contamination
- Precursor m/z value is unknown or unavailable from the spectrum metadata
- Analysis goal requires precursor ion intensity as part of the matching criterion (e.g., diagnostic isotope pattern matching)

## Inputs

- peaks array (m/z–intensity pairs, numpy.ndarray float32)
- reference spectrum peaks (m/z–intensity pairs, numpy.ndarray float32)
- precursor m/z value (float, Da)

## Outputs

- entropy_similarity score (float, 0–1 range; higher = more similar)

## How to apply

Pass the precursor m/z (pmz) parameter to the entropy_similarity() function. The function uses this value to exclude or down-weight the precursor region from the similarity calculation, ensuring that entropy-based metrics reflect fragment ion quality rather than precursor ion intensity dominance. The exact tolerance window around pmz is determined by the function's internal implementation. This step is mandatory when comparing spectra where precursor ions may artificially dominate the intensity profile, and optional when working with already-fragmented or pure fragment-ion spectra.

## Related tools

- **entropy_similarity** (Computes entropy-based spectral similarity metric with optional precursor region masking via pmz parameter) — https://github.com/FanzhouKong/spectral_denoising
- **ms_entropy** (Underlying library providing entropy and entropy_similarity function implementations)
- **spectral_denoising** (Python package wrapping entropy_similarity with precursor-aware denoising search workflows) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
from spectral_denoising import entropy_similairty
similarity = entropy_similairty(peak_denoised, peak_reference, pmz=199.0723)
```

## Evaluation signals

- Entropy similarity scores for denoised spectra are higher than for noisy spectra when compared against the same clean reference (indicating improved fragment match)
- Precursor region exclusion prevents artificially high similarity when precursor m/z dominates the spectrum intensity profile
- Reported entropy_similarity values match documented baselines for known test spectra pairs in the package's sample data
- pmz parameter is correctly extracted from spectrum metadata (precursor_mz field from MSP file) and passed without type errors
- Similarity scores remain consistent when pmz is re-supplied for the same spectrum pair in successive runs

## Limitations

- Precursor m/z must be accurately known; errors in pmz value will incorrectly mask or preserve precursor region, biasing similarity calculation
- Tolerance window around pmz for region exclusion is fixed by the entropy_similarity implementation and not user-configurable in the current API
- Function does not handle overlapping fragment ions near the precursor m/z; may inadvertently suppress informative low-abundance fragments in that region
- Python version must be between 3.8 and 3.12; RDkit dependency is incompatible with Python 3.13

## Evidence

- [other] entropy_similarity() between noisy spectrum and clean reference spectrum (removing precursor region if pmz provided): "Compute entropy_similarity() between noisy spectrum and clean reference spectrum (removing precursor region if pmz provided)"
- [other] entropy_similarity() between each denoised variant and the clean reference: "Compute entropy_similarity() between each denoised variant and the clean reference"
- [readme] entropy_similairty(peak_with_noise,peak,  pmz = pmz): "print(f'the entropy similarity of contaminated spectrum and the raw spectrum is {entropy_similairty(peak_with_noise,peak,  pmz = pmz):.2f}')"
- [readme] entropy_similairty(peak_denoised, peak, pmz = pmz): "print(f'the entropy similarity of denoised spectrum and the raw spectrum is {entropy_similairty(peak_denoised, peak, pmz = pmz):.2f}')"
