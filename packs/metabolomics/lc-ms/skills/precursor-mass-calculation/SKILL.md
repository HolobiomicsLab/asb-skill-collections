---
name: precursor-mass-calculation
description: Use when when you have a compound's SMILES string or molecular formula and need to determine the expected precursor ion m/z for comparison against observed spectra, particularly before applying formula-based denoising, entropy similarity scoring, or denoising search against reference libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RDkit
  - molmass
  - chemparse
  - pandas
  - scipy
  - spectral_denoising.chem_utils.calculate_precursormz
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-mass-calculation

## Summary

Calculate the theoretical precursor m/z value for a compound given its molecular structure (SMILES or formula) and ionization adduct type. This step is essential for anchoring MS/MS spectral analysis, noise filtering, and library searching workflows.

## When to use

When you have a compound's SMILES string or molecular formula and need to determine the expected precursor ion m/z for comparison against observed spectra, particularly before applying formula-based denoising, entropy similarity scoring, or denoising search against reference libraries.

## When NOT to use

- Input compound structure is already an observed precursor m/z from raw data (use directly instead)
- Adduct type is unknown or ambiguous; resolve ionization mode before calling this function
- Working with fragment ions or neutral losses rather than intact precursor ions

## Inputs

- SMILES string (compound molecular structure)
- molecular formula string (e.g., 'C5H4N4O')
- adduct type string (e.g., '[M+H]+', '[M+Na]+', '[M-H]-')

## Outputs

- precursor m/z (float): theoretical precursor ion mass-to-charge ratio

## How to apply

Call calculate_precursormz with the adduct type (e.g., '[M+H]+', '[M+Na]+', '[M-H]-') and either a SMILES string or molecular formula as input. The function computes the monoisotopic mass of the neutral molecule using the provided structure, applies the mass delta corresponding to the adduct (e.g., +1.00783 for [M+H]+, +22.98977 for [M+Na]+), and returns the theoretical precursor m/z. This value is then used downstream as a reference point for mass tolerance windows, precursor ion region retention, and entropy similarity calculations between observed and reference spectra.

## Related tools

- **RDkit** (parses SMILES strings and computes molecular masses)
- **molmass** (calculates atomic and molecular masses from chemical formulas)
- **chemparse** (parses and manipulates chemical formula strings)
- **spectral_denoising.chem_utils.calculate_precursormz** (main function implementing precursor m/z calculation) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
pmz = calculate_precursormz('[M+Na]+', 'O=c1nc[nH]c2nc[nH]c12')
```

## Evaluation signals

- Returned m/z value matches literature or database values for the same compound and adduct within <5 ppm mass error
- Precursor m/z lies within expected range for the molecular weight and charge state (e.g., m/z > 50 for singly charged ions of typical metabolites)
- Value is consistent when recalculated using both SMILES and derived molecular formula inputs
- Downstream entropy similarity scores improve when denoised spectra are compared using this precursor m/z as the mass reference point
- Precursor ion is correctly retained and not removed by electronic or formula-based denoising filters because its m/z matches the calculated value

## Limitations

- Assumes the adduct is correctly specified; incorrect adduct selection will produce an incorrect m/z and downstream filtering will fail
- Does not account for isotopic peaks ([M+1], [M+2]) or multiply-charged ions unless explicitly modeled
- SMILES parsing depends on RDkit correctness; malformed or non-standard SMILES will produce incorrect masses
- Adduct mass deltas are fixed based on standard ionization modes; unusual or custom adducts not in the adduct list will not be handled correctly

## Evidence

- [other] Extract the precursor m/z from the SMILES and adduct using calculate_precursormz: "Extract the precursor m/z from the SMILES and adduct using calculate_precursormz."
- [other] precursor m/z calculation is a foundational step in denoising and searching workflows: "pmz = calculate_precursormz(adduct,smiles)"
- [other] precursor m/z is used as a mass reference for entropy similarity scoring: "entropy_similairty(peak_with_noise,peak,  pmz = pmz)"
- [other] Precursor m/z is retained after denoising as part of precursor ion region: "Retain only ions tagged as valid, then add back the precursor ion region using add_spectra."
- [readme] Function accepts SMILES or formula as alternative inputs: "Note: Even all functions have a default 'smiles' information column, the function would also accept formula as input."
