---
name: spectral-denoising-formula-method
description: Use when you have a noisy MS/MS spectrum and need to identify and remove
  chemical noise ions (as opposed to electronic noise). You have the precursor compound's
  SMILES string or molecular formula and its adduct type.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - RDkit
  - molmass
  - chemparse
  - ms_entropy
  - spectral_denoising package
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# spectral-denoising-formula-method

## Summary

Formula-based denoising removes chemical noise ions from MS/MS spectra by evaluating whether each fragment ion could be formed from a chemically plausible subformula loss derived from the precursor compound's molecular formula and adduct state. This method improves high-confidence compound identification by retaining only ions consistent with the compound's structure.

## When to use

Apply this skill when you have a noisy MS/MS spectrum and need to identify and remove chemical noise ions (as opposed to electronic noise). You have the precursor compound's SMILES string or molecular formula and its adduct type. Your goal is to distinguish true fragment ions from chemical artifacts by checking whether each m/z value could plausibly arise from a neutral loss of a subformula derived from the parent ion.

## When NOT to use

- The input spectrum contains only electronic noise (identical peak intensities ≥4 occurrences); use electronic_denoising instead or apply it first.
- You lack reliable chemical structure information (SMILES or formula); formula_denoising requires accurate precursor formula to generate valid subformula candidates.
- The adduct type is unknown or ambiguous; incorrect adduct specification will produce incorrect master formula and lead to false noise tagging.

## Inputs

- noisy MS/MS spectrum as numpy array (m/z, intensity columns)
- compound SMILES string or molecular formula
- adduct type string (e.g., '[M+H]+', '[M+Na]+')

## Outputs

- denoised MS/MS spectrum (numpy array with m/z, intensity columns)
- denoise tags for each ion ('valid' or 'noise')
- entropy similarity score comparing denoised spectrum to reference spectrum

## How to apply

Extract the master molecular formula from the input SMILES string and adduct type using prep_formula, which adjusts the formula based on adduct ionization state. Compute precursor ion m/z statistics using get_pmz_statistics. Populate all chemically possible subformulas (representing all possible neutral losses) from the master formula using get_all_subformulas. For each fragment ion in the spectrum, call check_candidates to test whether a plausible subformula loss could produce that m/z value. Tag each ion as valid or noise using get_denoise_tag based on whether a candidate subformula loss was found. Retain only ions tagged as valid. This approach eliminates chemical noise while preserving genuine fragment ions consistent with the compound's structure.

## Related tools

- **RDkit** (Molecular formula extraction and manipulation from SMILES strings; chemical substructure enumeration) — https://www.rdkit.org/
- **molmass** (Molecular mass calculation and formula manipulation for m/z computation) — https://pypi.org/project/molmass/
- **ms_entropy** (Entropy similarity metric calculation between raw, denoised, and reference spectra for validation) — https://pypi.org/project/ms_entropy/
- **chemparse** (Parsing and standardizing chemical formula strings from SMILES and adduct information) — https://pypi.org/project/chemparse/
- **spectral_denoising package** (Core implementation of formula_denoising, prep_formula, get_pmz_statistics, get_all_subformulas, check_candidates, get_denoise_tag functions) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
peak_denoised = sd.spectral_denoising(peak_with_noise, 'O=c1nc[nH]c2nc[nH]c12', '[M+Na]+')
```

## Evaluation signals

- Entropy similarity score between denoised spectrum and ground-truth/reference spectrum should be higher than entropy similarity of raw noisy spectrum versus reference (indicating noise removal improved spectral quality).
- All retained ions (tagged 'valid') must correspond to m/z values explainable by neutral losses of subformulas from the master formula; no retained ion should lack a plausible subformula candidate.
- The number of ions removed should be consistent with the proportion of chemical noise in the original spectrum; compare ion count before and after denoising against known noise patterns from NIST23 database benchmarks.
- Spectrum entropy should not increase after denoising; normalized entropy of denoised spectrum should be ≤ normalized entropy of noisy spectrum, reflecting reduced randomness from noise removal.
- The precursor ion region should be preserved in the denoised spectrum; the precursor m/z should remain after denoising since it is always valid.

## Limitations

- Formula_denoising accuracy depends critically on correct SMILES input and accurate adduct specification; incorrect structural or ionization information will generate wrong subformula candidates and cause false noise tagging or false negatives.
- The method cannot distinguish between true fragment ions and chemical noise ions that happen to match subformula loss m/z values by coincidence, particularly for low-mass fragments common across many compounds.
- Performance has been empirically tested on NIST23 database; behavior on spectra from other instruments, ionization methods, or collision energies may differ.
- Computational cost scales with the complexity of the molecular formula; highly complex polymers or large biomolecules may generate prohibitively large subformula lists.

## Evidence

- [other] The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] Apply formula_denoising by: (a) extracting the master formula from SMILES and adduct using prep_formula, (b) computing precursor ion statistics with get_pmz_statistics, (c) populating all possible subformulas from the master formula using get_all_subformulas, (d) checking each fragment ion against candidate subformula losses using check_candidates, and (e) tagging ions as valid or noise using get_denoise_tag.: "Apply formula_denoising by: (a) extracting the master formula from SMILES and adduct using prep_formula, (b) computing precursor ion statistics with get_pmz_statistics, (c) populating all possible"
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``): "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion"
- [readme] peak_denoised = sd.spectral_denoising(peak_with_noise, smiles, adduct): "peak_denoised = sd.spectral_denoising(peak_with_noise, smiles, adduct)"
- [other] According to empiracally tested on NIST23 database, in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely: "According to empiracally tested on NIST23 database, in a given spectrum, the number of ions with identical intensities more than 4 is extremely unlikely"
