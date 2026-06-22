---
name: subformula-enumeration
description: Use when when performing chemical noise removal on MS/MS spectra and you need to validate whether each fragment ion m/z is consistent with loss of a subformula from the precursor ion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RDkit
  - molmass
  - chemparse
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# subformula-enumeration

## Summary

Enumerate all chemically plausible subformulas that can be lost from a molecular precursor ion to form observed fragment ions in MS/MS spectra. This supports formula-based noise filtering by checking whether each detected peak could arise from a valid neutral loss.

## When to use

When performing chemical noise removal on MS/MS spectra and you need to validate whether each fragment ion m/z is consistent with loss of a subformula from the precursor ion. Use this when you have a SMILES string or molecular formula and precursor m/z, and want to reject ions that cannot be explained by any plausible neutral loss.

## When NOT to use

- When the precursor ion structure is unknown or no SMILES/formula is available; subformula enumeration requires molecular structure input.
- When performing electronic denoising only (ions with identical intensities ≥4 occurrences); use electronic_denoising instead.
- When the observed spectrum contains no fragment ions or only the precursor ion; subformula-based validation cannot filter a spectrum with negligible fragmentation.

## Inputs

- SMILES string or molecular formula (master formula)
- Adduct type (e.g., '[M+H]+', '[M+Na]+')
- Observed fragment ion m/z values from MS/MS spectrum
- Precursor m/z
- Spectrum intensity array (numpy array with m/z and intensity columns)

## Outputs

- List of valid subformula losses (neutral losses) from precursor
- Denoise tags (valid/noise classification) for each fragment ion
- Filtered spectrum with only ions matching valid subformula losses
- Denoised spectrum (numpy array with retained m/z and intensity)

## How to apply

First, extract the master formula from the SMILES string and adduct type using prep_formula, which adjusts the formula based on adduct ionization state. Next, compute precursor ion mass statistics using get_pmz_statistics to establish reference mass values. Then populate all possible subformulas from the master formula using get_all_subformulas, which generates candidate neutral losses. For each observed fragment ion m/z, call check_candidates to determine if any subformula loss can explain the ion within mass tolerance; the algorithm computes the expected m/z of the fragment if that subformula were lost and compares it against the observed m/z. Finally, tag ions as valid or noise using get_denoise_tag based on whether at least one chemically plausible subformula loss matches the observed fragment. Retain only ions tagged as valid.

## Related tools

- **RDkit** (Extract molecular structure information and compute molecular mass from SMILES strings) — https://www.rdkit.org/
- **molmass** (Calculate exact masses for molecular formulas and subformula losses)
- **chemparse** (Parse and manipulate chemical formulas for loss calculations)
- **spectral_denoising** (Package containing prep_formula, get_pmz_statistics, get_all_subformulas, check_candidates, and get_denoise_tag functions) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Handle spectrum arrays and mass/intensity data structures)

## Examples

```
peak = np.array([[79.02, 521.0], [81.01, 659.0]], dtype=np.float32); smiles = 'O=c1nc[nH]c2nc[nH]c12'; adduct = '[M+Na]+'; peak_denoised = sd.spectral_denoising(peak, smiles, adduct)
```

## Evaluation signals

- All retained fragment ions have at least one chemically plausible subformula loss that matches within mass tolerance; compute expected m/z = precursor_mz - loss_mass and verify |observed_mz - expected_mz| ≤ tolerance.
- Entropy similarity between denoised spectrum and reference/ground-truth spectrum is higher than entropy similarity of the raw noisy spectrum and the reference (entropy_similarity should increase after denoising).
- No fragment ions with identical m/z appear multiple times after denoising (if they did, they may be artifacts).
- The number of retained ions is substantially fewer than the input spectrum (confirming that chemical noise was removed), but the denoised spectrum retains the major diagnostic peaks.
- All removed ions either cannot be explained by any subformula loss or have no corresponding entry in the enumerated subformula list.

## Limitations

- Subformula enumeration assumes 100% accuracy of the input SMILES string or molecular formula; errors in chemical structure will propagate to incorrect subformula predictions.
- The method relies on a predefined mass tolerance for matching observed m/z to expected fragment m/z; the tolerance must be calibrated to the instrument's mass accuracy (e.g., ±5 ppm for Orbitrap).
- Complex molecules with many atoms generate exponentially many subformulas; enumeration may become computationally expensive for large precursor ions.
- The algorithm does not account for multi-step losses or rearrangements; fragment ions formed via complex fragmentation pathways may be incorrectly tagged as noise.
- Adduct type must be specified correctly; incorrect adduct assignment (e.g., '[M+H]+' vs '[M+Na]+') will produce incorrect precursor m/z and invalidate all downstream subformula checks.

## Evidence

- [other] Step2: Populate all possible subformulas from master formula: "Step2: Populate all possible subformulas from master formula using get_all_subformulas"
- [other] For any given fragment ion, the algorithm will try to find a plausible subformula loss: "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``)"
- [other] The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] Apply formula_denoising by extracting the master formula from SMILES and adduct using prep_formula, computing precursor ion statistics with get_pmz_statistics, populating all possible subformulas from the master formula using get_all_subformulas, checking each fragment ion against candidate subformula losses using check_candidates, and tagging ions as valid or noise using get_denoise_tag.: "Apply formula_denoising by: (a) extracting the master formula from SMILES and adduct using prep_formula, (b) computing precursor ion statistics with get_pmz_statistics, (c) populating all possible"
- [other] Step 0: Modify the master formula based on SMILES and adduct information: "Step 0: Modify the master formula based on SMILES and adduct information"
