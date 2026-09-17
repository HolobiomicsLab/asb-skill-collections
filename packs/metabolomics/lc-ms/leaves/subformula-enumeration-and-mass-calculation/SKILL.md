---
name: subformula-enumeration-and-mass-calculation
description: 'Use when when performing chemical denoising of MS/MS spectra: after
  modifying a master formula based on SMILES and adduct information, enumerate all
  possible subformulas to establish the set of chemically valid neutral losses.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - Python
  - RDkit
  - chemparse
  - molmass
  - pandas
  - scipy
  - prep_formula
  - get_all_subformulas
  - check_candidates
  - get_pmz_statistics
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

# Subformula enumeration and mass calculation

## Summary

Enumerate all chemically plausible subformulas derived from a master molecular formula, then calculate the neutral mass of each to create a searchable database of fragment candidates. This enables rapid lookup of which neutral losses are chemically valid when filtering MS/MS fragment ions.

## When to use

When performing chemical denoising of MS/MS spectra: after modifying a master formula based on SMILES and adduct information, enumerate all possible subformulas to establish the set of chemically valid neutral losses. For each observed fragment ion, you will later check whether its neutral mass matches one of these precomputed subformula masses (within mass tolerance). Skip this step only if you already possess a precomputed, validated subformula table for the same molecular formula and adduct context.

## When NOT to use

- Input spectrum contains only precursor and one or two dominant fragments (subformula enumeration provides no discrimination benefit; electronic denoising alone may suffice).
- Molecular formula is unknown or unreliable (subformula enumeration will generate spurious candidates; alternative filtering methods required).
- Adduct type is not specified or ambiguous (prep_formula cannot correctly modify the master formula; formula_denoising will produce misleading results).

## Inputs

- Master molecular formula (string; e.g. 'C5H4N4O') after modification by prep_formula based on SMILES and adduct information
- Precursor m/z (float)
- MS/MS fragment ion list (array of [m/z, intensity] pairs)
- Mass tolerance window (float, in Da; extracted from precursor ion statistics or empirically set)

## Outputs

- Sorted list of all possible subformulas (list of formula strings) with associated neutral masses
- Denoising tags for each fragment ion (boolean array: True = chemically valid, False = noise)
- Refined MS/MS spectrum retaining only True-tagged ions

## How to apply

Call get_all_subformulas on the master molecular formula (prepared via prep_formula to account for SMILES-derived structural constraints and adduct modifications). This function generates all possible chemical subformulas by systematically removing atoms while respecting valence and chemical rules. Sort the output by mass to enable fast binary search during fragment matching. For each observed fragment m/z in the spectrum, convert it to a neutral mass using the precursor m/z and charge state, then use check_candidates to locate a subformula loss mass within the established mass tolerance window (extracted via get_pmz_statistics, which may adaptively adjust the tolerance if the measured precursor error exceeds the initial threshold). Only fragment ions whose neutral mass corresponds to a subformula loss are tagged as chemically valid; others are marked for removal as noise.

## Related tools

- **prep_formula** (Modifies the master molecular formula based on SMILES and adduct information (e.g., adding atoms for rare adducts and benzene substructures) before subformula enumeration) — https://github.com/FanzhouKong/spectral_denoising
- **get_all_subformulas** (Core function that populates all possible subformulas from the master formula, sorted by mass for efficient lookup) — https://github.com/FanzhouKong/spectral_denoising
- **check_candidates** (For each observed fragment ion, searches the precomputed subformula mass list to find a plausible neutral loss within the mass tolerance window) — https://github.com/FanzhouKong/spectral_denoising
- **get_pmz_statistics** (Extracts precursor ion information and adaptively updates the mass tolerance threshold if measured mass error exceeds the initial tolerance) — https://github.com/FanzhouKong/spectral_denoising
- **molmass** (Python library used to calculate accurate neutral masses of formulas and subformulas) — https://pypi.org/project/molmass/
- **RDkit** (Chemistry toolkit used to validate chemical plausibility of subformulas (valence, bonding rules)) — https://www.rdkit.org/

## Examples

```
peak_denoised = sd.formula_denoising(peak, 'C1=CC=CC=C1', '[M+H]+')
```

## Evaluation signals

- Subformula list is non-empty, correctly sorted by ascending mass, and contains the master formula itself as the largest entry.
- All subformulas obey chemical valence rules and element constraints (verified via RDkit sanitization or manual inspection of a sample).
- Denoising tags correctly identify at least one precursor ion as True (the [M] peak or [M+adduct] peak after loss of 0 atoms).
- Entropy similarity between the denoised spectrum and a high-quality reference spectrum (calculated via entropy_similairty) is higher than the raw (noisy) spectrum's similarity, confirming that noise removal improves matching.
- No fragment ion with intensity >10% of the base peak is incorrectly tagged as False (i.e., significant peaks should rarely be removed unless they are genuine noise).

## Limitations

- Subformula enumeration assumes the input master formula and adduct type are correct; errors in SMILES parsing or adduct specification propagate directly to false negative/positive filtering.
- Mass tolerance window is fixed or adaptively set from precursor statistics; if the spectrum has systematic calibration drift or the mass analyzer has variable mass accuracy across the m/z range, some valid fragments may be outside the tolerance and incorrectly tagged as noise.
- Enumeration does not account for in-source fragmentation, isotope patterns, or multiply charged fragments; chemical validity alone does not guarantee observability.
- Computational cost scales with formula complexity (large molecules with many atoms generate exponentially more subformulas); for very large metabolites or proteins, enumeration may be slow or memory-intensive.

## Evidence

- [other] Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass.: "Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass."
- [other] For each fragment ion in the spectrum, use check_candidates to find a plausible subformula loss from the master formula within the mass tolerance window.: "For each fragment ion in the spectrum, use check_candidates to find a plausible subformula loss from the master formula within the mass tolerance window."
- [other] Step 0: Modify the master formula based on SMILES and adduct information: "Step 0: Modify the master formula based on SMILES and adduct information"
- [other] The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [readme] RDkit currently does not have a distribution compitable to python 3.13: "RDkit currently does not have a distribution compitable to python 3.13"
