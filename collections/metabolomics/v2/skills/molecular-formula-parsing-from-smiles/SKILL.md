---
name: molecular-formula-parsing-from-smiles
description: Use when you have a query MS/MS spectrum with a SMILES string and adduct type (e.g., '[M+H]+', '[M+Na]+'), and you need to validate fragment ions against chemically plausible losses from the parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - RDkit
  - chemparse
  - molmass
  - pandas
  - scipy
  - prep_formula
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
- chemparse==0.3.1
- '- ``chemparse==0.3.1``'
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

# molecular-formula-parsing-from-smiles

## Summary

Extract and modify a molecular formula from SMILES notation and adduct information to establish a master formula for downstream chemical constraint validation. This is essential for formula-based noise filtering in MS/MS spectra, where the precise elemental composition must account for adduct modifications and structural features.

## When to use

You have a query MS/MS spectrum with a SMILES string and adduct type (e.g., '[M+H]+', '[M+Na]+'), and you need to validate fragment ions against chemically plausible losses from the parent compound. Formula parsing is the prerequisite: without an accurate master formula adjusted for the adduct, the subsequent subformula enumeration and plausibility checking will fail or produce spurious chemical noise tags.

## When NOT to use

- Input is an already-validated molecular formula from a spectral library (use directly without prep_formula).
- SMILES string is malformed or not parseable by RDkit (prep_formula will fail; validate SMILES first).
- You are performing only electronic denoising (intensity-based filtering) without chemical plausibility checks.

## Inputs

- SMILES string (e.g., 'C1=CC=CC=C1' for benzene)
- Adduct type string (e.g., '[M+H]+', '[M+Na]+', '[M+NH4]+')
- Optional: explicit molecular formula (chemparse-compatible string)

## Outputs

- Master molecular formula (dict or chemparse object with element counts)
- Adduct-adjusted formula ready for subformula enumeration

## How to apply

Use the prep_formula function to convert SMILES into a molecular formula, then modify it based on adduct information (e.g., adding H for [M+H]+ or Na for [M+Na]+, adding atoms for rare adducts, and incorporating benzene substructures detected in the SMILES). The resulting master formula becomes the reference set from which all possible subformulas are enumerated. This step must occur before get_all_subformulas is called, as the enumerated candidates are directly derived from the modified master formula. The output formula is validated implicitly when fragment ions are checked against subformula losses within the mass tolerance window established by get_pmz_statistics.

## Related tools

- **RDkit** (Parses SMILES strings into molecule objects; detects structural features (e.g., benzene rings) for formula modification.) — https://www.rdkit.org
- **chemparse** (Parses and manipulates molecular formula strings; version 0.3.1 required for compatibility.)
- **molmass** (Calculates exact monoisotopic mass from molecular formula for mass tolerance validation.)
- **prep_formula** (Core function that executes SMILES-to-formula conversion and adduct-based modification.) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
peak_denoised = sd.spectral_denoising(peak_with_noise, 'C1=CC=CC=C1', '[M+H]+')
```

## Evaluation signals

- Master formula element counts match the SMILES structure (e.g., benzene → C6H6, after [M+H]+ → C6H7).
- Adduct atoms are correctly added (e.g., +H for [M+H]+, +Na for [M+Na]+, +N+H4 for [M+NH4]+).
- Subsequent get_all_subformulas produces chemically valid subformulas with monotonically increasing mass.
- Fragment ions in denoised spectrum correspond to losses that can be represented as valid subformulas from the master formula within the measured mass tolerance.
- Entropy similarity between denoised and reference spectra improves after formula-based filtering, indicating reduced chemical noise.

## Limitations

- SMILES parsing requires RDkit, which is not compatible with Python ≥3.13; Python version must be between 3.8 and 3.12.
- Malformed or ambiguous SMILES strings will cause prep_formula to fail; no automatic SMILES validation is performed upstream.
- Rare or non-standard adducts may not have pre-defined atom additions in the prep_formula implementation; manual formula adjustment may be required.
- Formula denoising assumes the precursor mass accuracy is within the tolerance window (default updated if measured error exceeds initial threshold); extreme mass calibration errors may cause false negatives.

## Evidence

- [other] Modify the master formula based on SMILES and adduct information using prep_formula, adding atoms for rare adducts and benzene substructures.: "Prepare the master molecular formula by modifying it based on SMILES and adduct information using prep_formula, adding atoms for rare adducts and benzene substructures."
- [other] The formula_denoising function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss.: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass.: "Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass."
- [other] RDkit currently does not have a distribution compatible to python 3.13: "RDkit currently does not have a distribution compitable to python 3.13"
- [readme] Note: Even all functions have a default 'smiles' information column, the function would also accept formula as input. If wanted, just replace the the smiles with formula information.: "Even all functions have a default 'smiles' information column, the function would also accept formula as input. If wanted, just replace the the smiles with formula information"
