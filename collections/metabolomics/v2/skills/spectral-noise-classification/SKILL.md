---
name: spectral-noise-classification
description: Use when you have MS/MS spectra contaminated with noise ions and need to improve compound identification accuracy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RDkit
  - molmass
  - chemparse
  - spectral_denoising (Python package)
  - ms_entropy
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
- rdkit==2024.3.5
- smiles = 'O=c1nc[nH]c2nc[nH]c12'
- molmass==2021.6.18
- '- ``molmass==2021.6.18``'
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

# spectral-noise-classification

## Summary

Categorize and remove noise ions from MS/MS spectra by distinguishing electronic noise (instrumental artifacts with identical intensities) from chemical noise (implausible fragment ions). This skill integrates molecular structure and adduct information to enable high-confidence compound identification.

## When to use

Apply this skill when you have MS/MS spectra contaminated with noise ions and need to improve compound identification accuracy. Specifically, use it when you have: (1) a query MS/MS spectrum with precursor m/z and suspect noise contamination, (2) the compound's SMILES string or molecular formula, and (3) the ionization adduct type. The skill is especially valuable before spectral matching against reference libraries, where noise ions reduce entropy similarity scores and produce false negatives.

## When NOT to use

- Input spectrum is already confirmed to be noise-free or from a clean analytical source with inherently low artifact levels.
- Compound's SMILES or molecular formula is unknown or unreliable, as chemical noise classification depends critically on accurate molecular structure.
- Spectrum is from a non-MS/MS data type (e.g., full-scan MS1 or chromatographic data) where the fragmentation logic does not apply.

## Inputs

- MS/MS spectrum (numpy array with m/z and intensity columns)
- Compound SMILES string or molecular formula
- Ionization adduct type (e.g., '[M+H]+', '[M+Na]+')
- Precursor m/z (optional; can be calculated from SMILES and adduct)

## Outputs

- Denoised MS/MS spectrum (numpy array with m/z and intensity columns)
- Noise classification labels (valid vs. noise) for each ion
- Entropy similarity score (denoised spectrum vs. reference spectrum)

## How to apply

Classify and remove noise in two sequential stages: (1) Electronic denoising: identify and remove ions with identical intensities that occur ≥4 times in the spectrum, as this pattern is empirically rare in authentic MS/MS data (verified on NIST23 database). (2) Formula-based chemical denoising: extract the master molecular formula from the SMILES and adduct using prep_formula, enumerate all possible subformulas via get_all_subformulas, then for each fragment ion use check_candidates to test whether it could arise from a chemically plausible subformula loss. Tag ions as valid or noise via get_denoise_tag, retain only valid ions, and restore the precursor region. Validate denoising success by computing entropy_similarity between the denoised spectrum and a ground-truth reference spectrum; a higher score indicates effective noise removal.

## Related tools

- **spectral_denoising (Python package)** (Primary implementation of electronic_denoising and formula_denoising functions for noise classification and removal) — https://github.com/FanzhouKong/spectral_denoising
- **RDkit** (Parses SMILES strings and extracts molecular structure to derive formulas and subformula losses)
- **molmass** (Computes molecular weights and mass offsets for formula-based candidate validation)
- **ms_entropy** (Calculates entropy_similarity metric to evaluate denoising quality relative to reference spectra)
- **chemparse** (Parses and manipulates chemical formula strings for formula_denoising workflow)

## Examples

```
import spectral_denoising as sd; import numpy as np; peak_with_noise = sd.read_msp('sample_data/noisy_spectra.msp').iloc[0]['peaks']; peak_denoised = sd.spectral_denoising(peak_with_noise, 'O=c1nc[nH]c2nc[nH]c12', '[M+Na]+'); print(sd.entropy_similairty(peak_denoised, peak, pmz=pmz))
```

## Evaluation signals

- Electronic denoising removes all ions with identical intensities occurring ≥4 times; confirm removal by counting duplicate intensity values pre- and post-denoising.
- Chemical denoising removes only ions that cannot be explained by any subformula loss from the master formula; validate by checking that all retained ions have corresponding candidate losses in check_candidates output.
- Entropy similarity score between denoised spectrum and ground-truth reference is higher than between raw (noisy) spectrum and reference, indicating noise removal improved spectral match quality.
- Denoised spectrum retains the precursor ion region (verified by add_spectra function), maintaining biological relevance.
- Denoised spectrum has no zero-intensity ions and is sorted by m/z (confirmed by sanitize_spectrum wrapper).

## Limitations

- Electronic denoising threshold (≥4 identical intensities) is empirically derived from NIST23 and may not generalize to all instrumental platforms or noise regimes.
- Chemical denoising accuracy depends on the completeness and correctness of the master formula; errors in SMILES parsing or adduct specification propagate downstream.
- The algorithm assumes all chemically plausible subformula losses should be retained; spectra with unusual or instrument-specific fragmentation patterns may be over-denoised.
- Python version must be ≥3.8 and <3.13 due to RDkit compatibility constraints; deployment on other Python versions may fail.

## Evidence

- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra: "The ``electronic_denoising`` function removes obvious electronic noise ions in MS/MS spectra"
- [other] The formula_denoising function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] Apply electronic_denoising to remove ions with identical intensities (≥4 occurrences): "apply electronic_denoising to remove ions with identical intensities (≥4 occurrences)"
- [other] According to empiracally tested on NIST23 database, in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely: "According to empiracally tested on NIST23 database, in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely"
- [other] For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``): "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion"
- [other] Compute entropy_similarity between the input noisy spectrum and reference/ground-truth spectrum, and between the denoised spectrum and reference spectrum, and report both scores for comparison.: "Compute entropy_similarity between the input noisy spectrum and reference/ground-truth spectrum, and between the denoised spectrum and reference spectrum, and report both scores for comparison."
- [readme] Please use Python version between 3.8 to 3.12 for this package to work. RDkit currently does not have a distribution compitable to python 3.13: "Please use Python version between 3.8 to 3.12 for this package to work. RDkit currently does not have a distribution compitable to python 3.13"
