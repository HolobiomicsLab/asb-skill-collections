---
name: peak-list-filtering-and-cleaning
description: Use when you have acquired MS/MS spectra containing suspect noise ions—either
  electronic noise (ions with identical intensities occurring >4 times in a single
  peak list, a signature of detector artifacts) or chemical noise (fragment ions chemically
  implausible given the precursor molecule's.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectral_denoising Python package
  - numpy
  - RDkit
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

# peak-list-filtering-and-cleaning

## Summary

Remove electronic and chemical noise ions from MS/MS peak lists to improve spectral quality and compound identification confidence. This skill applies domain-specific filters (intensity-based for electronic noise, formula-based for chemical noise) to a 2D array of m/z and intensity values, returning a deduplicated, curated peak list suitable for library matching.

## When to use

Apply this skill when you have acquired MS/MS spectra containing suspect noise ions—either electronic noise (ions with identical intensities occurring >4 times in a single peak list, a signature of detector artifacts) or chemical noise (fragment ions chemically implausible given the precursor molecule's structure). Use it before spectral library searching or when entropy similarity between replicate analyses is low.

## When NOT to use

- Input spectrum has already been denoised or validated against a reference standard—applying the filter again may remove legitimate low-abundance peaks.
- Peak list contains fewer than 5 peaks total—the intensity-frequency threshold (>4 occurrences) is calibrated for typical-sized spectra and may not be meaningful for sparse data.
- Chemical structure (SMILES or formula) is unknown or unreliable—formula denoising cannot proceed without accurate precursor composition.

## Inputs

- 2D numpy array with shape [n, 2] containing m/z (column 0) and intensity (column 1) values
- SMILES string or chemical formula (for formula denoising)
- Ion adduct (e.g., '[M+H]+', '[M+Na]+') (for formula denoising)

## Outputs

- 2D numpy array with shape [m, 2] (m ≤ n) containing deduplicated m/z and intensity values
- Denoised peak list suitable for spectral library matching

## How to apply

Load your peak list as a 2D numpy array with shape [n, 2] where columns are m/z and intensity. Apply electronic denoising first by counting frequency of each unique intensity value and filtering peaks whose intensity occurs more than 4 times (an empirically validated threshold from NIST23 where such occurrences are <0.05% in genuine spectra). Then apply formula denoising by (1) preparing the master formula from SMILES and adduct information; (2) generating all chemically plausible subformula losses; (3) checking whether each observed peak corresponds to a valid fragment; (4) removing peaks without plausible assignments. Finally, sanitize the spectrum by removing zero-intensity ions and sorting by m/z. Return the deduplicated array in the same [n, 2] shape as input.

## Related tools

- **spectral_denoising Python package** (Implements electronic_denoising, formula_denoising, and spectral_denoising_batch functions for noise removal) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Core array manipulation for loading, filtering, and returning peak lists)
- **RDkit** (Parses SMILES strings and computes chemical formulas for formula denoising)
- **ms_entropy** (Computes spectral entropy and entropy similarity to evaluate denoising effectiveness)

## Examples

```
import numpy as np
import spectral_denoising as sd
peak = np.array([[48.99, 154.0], [63.01, 265.0], [79.02, 521.0]], dtype=np.float32)
peak_denoised = sd.electronic_denoising(peak)
peak_denoised = sd.formula_denoising(peak_denoised, 'O=c1nc[nH]c2nc[nH]c12', '[M+Na]+')
```

## Evaluation signals

- Intensity-frequency histogram post-denoising shows no intensity value occurring >4 times (electronic noise removed).
- Peak count decreases from input to output (m < n), confirming noise removal; verify the removed peaks were either high-frequency intensities or chemically implausible fragments.
- Entropy similarity between denoised spectrum and a clean reference improves relative to the raw spectrum (computed via entropy_similarity function).
- Denoised spectrum matches expected fragment pattern for the precursor molecule (e.g., common neutral losses like H2O, CO2 are present; artifact peaks are absent).
- Output array is sorted by m/z, contains no zero-intensity rows, and all m/z and intensity values are non-negative floats or integers within expected mass and intensity ranges.

## Limitations

- Electronic denoising threshold (>4 identical intensities) is empirically validated on NIST23 but may need adjustment for other instrument types, acquisition methods, or noise profiles not represented in NIST23.
- Formula denoising requires accurate SMILES or chemical formula input; misspecified precursor composition will cause false positives (legitimate fragments labeled as noise) or false negatives (noise not removed).
- Does not handle 'chemical noise' arising from in-source fragmentation, solvent adducts, or multiply-charged ions unless the precursor adduct is correctly specified.
- Spectral entropy and similarity metrics are relative; denoising success is best judged in conjunction with independent validation (e.g., replicate analysis, library search improvement) rather than entropy alone.

## Evidence

- [other] The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra: "The ``electronic_denoising`` function removes obvious electronic noise ions in MS/MS spectra"
- [other] Identify intensity values that occur more than 4 times (threshold empirically validated on NIST23): "Identify intensity values that occur more than 4 times (a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra)"
- [other] Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns: "Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns"
- [intro] Noise ions in MS/MS spectra are largely categorized as electronic noises and chemical noises: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] The formula_denoising function removes chemical noise ions by evaluating if a fragment could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] sanitize_spectrum is a wrapper function that removes zero-intensity ions and sorts the spectrum by mass: "``spectral_operations.sanitize_spectrum`` is just a wrapper function for ``spectral_operations.remove_zero_ions`` and ``spectral_operations.sort_spectrum``"
- [readme] Python version requirement for spectral denoising: "Spectral denoising requires ``Python >= 3.8`` installed on your system"
