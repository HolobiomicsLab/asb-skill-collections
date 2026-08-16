---
name: chemical-noise-subformula-loss-filtering
description: Use when you have MS/MS spectra with high chemical noise (spurious ions arising from incomplete ionization, in-source fragmentation, or instrument artifacts) and you possess accurate molecular formula or SMILES structure and adduct information for the precursor.
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
  - spectral_denoising (formula_denoising function)
  - ms_entropy
  - molmass
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

# Chemical-Noise Subformula Loss Filtering

## Summary

Remove chemically implausible fragment ions from MS/MS spectra by evaluating whether each detected peak could originate from a valid neutral loss of the parent molecule. This skill filters out chemical noise by rejecting ions that cannot be explained by known fragmentation chemistry derived from the molecular formula and adduct.

## When to use

Apply this skill when you have MS/MS spectra with high chemical noise (spurious ions arising from incomplete ionization, in-source fragmentation, or instrument artifacts) and you possess accurate molecular formula or SMILES structure and adduct information for the precursor. Use it when entropy-similarity matching against reference libraries is contaminated by implausible fragment peaks that reduce match confidence.

## When NOT to use

- Input spectrum lacks reliable molecular formula or SMILES annotation; subformula enumeration cannot proceed without accurate parent composition.
- Precursor ion is from a mixture or has ambiguous molecular weight; parent formula is indeterminate or multiply ionized, invalidating single-formula substructure logic.
- Fragment peaks are from post-source decay, in-source collision, or other non-standard fragmentation pathways not covered by neutral-loss chemistry (e.g., rearrangement ions or McLafferty products); valid fragments may be incorrectly flagged as noise.

## Inputs

- MS/MS spectrum (array of [m/z, intensity] pairs)
- parent molecular SMILES or formula string
- adduct type (e.g., '[M+H]+', '[M+Na]+')
- precursor m/z (calculated or observed)

## Outputs

- denoised MS/MS spectrum (array of [m/z, intensity] pairs with chemical noise removed)
- denoise tags array (boolean or enum per peak indicating chemical plausibility)

## How to apply

First, prepare the parent molecular formula by adjusting it based on SMILES and adduct information using prep_formula(). Second, enumerate all chemically valid subformulas (neutral losses) that could originate from the parent using get_all_subformulas(). Third, for each detected fragment ion peak, check whether it could be formed by subtracting one of the valid subformulas from the parent using check_candidates(). Fourth, tag peaks as noise or signal using get_denoise_tag() based on whether they match a plausible subformula loss and precursor m/z constraints. Finally, remove peaks marked as chemical noise, retaining only those explicable by valid neutral losses. The rationale is that chemical noise ions violate mass balance or cannot be derived from known fragmentation chemistry, whereas true fragment ions correspond to chemically plausible subformula losses.

## Related tools

- **spectral_denoising (formula_denoising function)** (Implements chemical noise filtering by evaluating plausible subformula losses and removing ions that cannot be chemically justified) — https://github.com/FanzhouKong/spectral_denoising
- **RDkit** (Parses SMILES strings and generates molecular formulas and subformula chemistry for valid neutral losses)
- **ms_entropy** (Computes entropy-similarity metrics to quantify improvement in spectral quality after chemical noise removal)
- **molmass** (Calculates precise m/z values for fragment ions and neutral losses to match peaks against subformula predictions)

## Examples

```
peak_denoised = sd.formula_denoising(peak_with_noise, 'O=c1nc[nH]c2nc[nH]c12', '[M+Na]+')
```

## Evaluation signals

- Entropy-similarity between denoised spectrum and clean reference should increase (typically 0.1–0.3 absolute increase) compared to raw noisy spectrum.
- Removed peaks must all fail check_candidates() — i.e., no plausible subformula loss explains them within mass tolerance.
- Retained peaks must each correspond to a valid subformula loss confirmed by prep_formula() and get_all_subformulas(); verify that (parent_mass - fragment_m/z) equals a known neutral loss mass (within ±5 ppm typical MS accuracy).
- Peak count should decrease; number of removed ions should align with expected chemical noise prevalence in the instrument/library (empirically, ions with identical intensities >4 are rare and may indicate electronic noise, not chemical noise, so chemical filtering should be orthogonal).
- Denoised spectrum should pass sanitize_spectrum() (zero-intensity removal and mass sorting) and match expected chemical fragmentation patterns for the molecule class (e.g., no fragment heavier than precursor, no loss exceeding parent mass).

## Limitations

- Requires accurate molecular formula or SMILES; errors in structure annotation will propagate to incorrect subformula enumeration and false-positive/negative filtering.
- Chemical noise filtering assumes fragmentation follows neutral-loss rules; non-classical fragmentations (rearrangements, multi-step losses, or cyclic scrambling) may be incorrectly rejected as implausible.
- Performance depends on precursor m/z accuracy; high mass error (>10 ppm) can cause valid subformula losses to fall outside acceptance windows, leading to loss of true signal.
- The approach is sensitive to incomplete or incorrect adduct specification; wrong adduct charge or modification will skew parent formula and render all subformula calculations incorrect.
- Computational cost scales with subformula diversity; large molecules with many functional groups may generate thousands of valid subformulas, increasing runtime and memory usage.

## Evidence

- [other] The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion: "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``)"
- [other] Step 0: Modify the master formula based on SMILES and adduct information: "Step 0: Modify the master formula based on SMILES and adduct information"
- [intro] Integrating such process into spectra matching process, we developed denoising search, which psudo-denoise spectra based on molecular information fetched from reference databases.: "Integrating such process into spectra matching process, we developed denoising search, which psudo-denoise spectra based on molecular information fetched from reference databases."
- [readme] peak_denoised = sd.formula_denoising(peak, 'C1=CC=CC=C1', '[M+H]+'): "peak_denoised = sd.formula_denoising(peak, 'C1=CC=CC=C1', '[M+H]+')"
