---
name: fragment-ion-mass-matching-with-tolerance
description: 'Use when denoising MS/MS spectra and you have: (1) a precursor ion with measured m/z and known molecular formula (from SMILES or direct formula input), (2) an adduct type ([M+H]+, [M+Na]+, etc.), (3) a list of fragment ions with observed m/z values, and (4) a need to distinguish chemically valid.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - RDkit
  - chemparse
  - molmass
  - pandas
  - scipy
  - prep_formula
  - get_pmz_statistics
  - get_all_subformulas
  - check_candidates
  - get_denoise_tag
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-mass-matching-with-tolerance

## Summary

Match observed fragment ions in MS/MS spectra against expected subformula losses from a master molecular formula, within a dynamically adjusted mass tolerance window. This skill identifies chemically plausible fragment ions by evaluating whether each observed m/z could result from loss of a valid subformula, enabling discrimination of true fragments from chemical noise.

## When to use

Apply this skill when denoising MS/MS spectra and you have: (1) a precursor ion with measured m/z and known molecular formula (from SMILES or direct formula input), (2) an adduct type ([M+H]+, [M+Na]+, etc.), (3) a list of fragment ions with observed m/z values, and (4) a need to distinguish chemically valid fragments from noise ions. Use it especially when the measured precursor mass error exceeds the initial mass tolerance threshold, triggering an adaptive tolerance adjustment.

## When NOT to use

- When the precursor ion m/z is not accurately measured or adduct type is unknown — the tolerance adjustment depends on knowing the true precursor mass error.
- When molecular formula or SMILES information is unavailable — subformula generation requires a valid master formula as input.
- When performing electronic noise removal only — this skill addresses chemical noise via formula plausibility, not instrumental artifacts like baseline noise or isolated spikes.

## Inputs

- observed fragment ion m/z array (float32 or float64, typically paired with intensity values)
- precursor m/z (float, measured from spectrum)
- master molecular formula (string, e.g., 'C5H4N4O')
- SMILES string (string, e.g., 'O=c1nc[nH]c2nc[nH]c12') or molecular formula
- adduct type (string, e.g., '[M+H]+', '[M+Na]+', '[M-H]-')
- initial mass tolerance threshold (float, in ppm or Da)

## Outputs

- boolean tag array matching input fragment ions (True=chemically valid, False=noise)
- filtered fragment ion m/z array (only True-tagged ions retained)
- filtered intensity array (paired with filtered m/z)
- updated mass tolerance threshold (float, if precursor error triggered adjustment)

## How to apply

First, call `get_pmz_statistics()` on the precursor ion to extract the real precursor m/z and compare against the theoretical mass; if the measured error exceeds the initial tolerance, update the tolerance threshold accordingly. Second, call `get_all_subformulas()` to populate all possible subformulas derivable from the master formula (prepared via `prep_formula()` to account for SMILES-based modifications and adduct-specific atom additions). Third, for each observed fragment ion, invoke `check_candidates()` to search within the updated tolerance window for a subformula loss that would yield that fragment's m/z. Fourth, use `get_denoise_tag()` to assign True (chemically valid) or False (noise) tags based on whether a plausible subformula loss was found. The tolerance window is the critical decision point: it dynamically adjusts if precursor mass error is large, preventing over-filtering or under-filtering of candidate fragments. Retain only True-tagged ions in the final denoised spectrum.

## Related tools

- **prep_formula** (Modifies the master molecular formula based on SMILES and adduct information, adding atoms for rare adducts and benzene substructures before subformula generation) — https://github.com/FanzhouKong/spectral_denoising
- **get_pmz_statistics** (Extracts precursor ion m/z and updates mass tolerance threshold if measured mass error exceeds initial tolerance) — https://github.com/FanzhouKong/spectral_denoising
- **get_all_subformulas** (Populates all possible subformulas derivable from the master formula, sorted by mass, for use in candidate matching) — https://github.com/FanzhouKong/spectral_denoising
- **check_candidates** (For each observed fragment ion, searches for a plausible subformula loss within the tolerance window that could form that ion's m/z) — https://github.com/FanzhouKong/spectral_denoising
- **get_denoise_tag** (Assigns True/False tags to fragment ions based on whether a plausible subformula loss was found by check_candidates) — https://github.com/FanzhouKong/spectral_denoising
- **RDkit** (Molecular structure parsing and SMILES canonicalization to derive chemical information for formula modification)
- **molmass** (Precise calculation of molecular masses for subformulas and precursor ions)
- **chemparse** (Chemical formula parsing and validation)

## Examples

```
peak_denoised = sd.spectral_denoising(peak_with_noise, 'O=c1nc[nH]c2nc[nH]c12', '[M+H]+')
```

## Evaluation signals

- Verify that the number of True-tagged ions is chemically reasonable (typically 5–30 fragments for small metabolites) — too many or too few suggests tolerance is miscalibrated.
- Compare entropy similarity of the denoised spectrum (True-tagged ions only) against a reference spectrum before and after filtering; improvement > 0.1–0.2 in entropy_similarity indicates successful noise removal.
- Check that no chemically impossible subformula losses are retained (e.g., loss of negative mass or atoms absent from the master formula); validate via mass balance (precursor mass = fragment mass + loss mass).
- Confirm that the precursor ion and major known diagnostic fragments remain tagged as True; loss of these indicates over-filtering or tolerance set too conservatively.
- Audit a sample of False-tagged ions to verify they lack a match within the tolerance window — inspect the closest subformula loss candidate and its mass error to confirm it exceeds the threshold.

## Limitations

- Assumes the input SMILES string or molecular formula is correct; errors in chemical structure will propagate through subformula generation and produce incorrect tags.
- Mass tolerance window adjustment relies on accurate precursor m/z measurement; poor-quality precursor peaks or systematic instrument miscalibration can lead to inappropriate thresholds.
- Does not account for isotope patterns or high-resolution artefacts (e.g., 13C satellites); these may be tagged as noise if they fall outside the tolerance window.
- Limited to detecting losses corresponding to valid subformulas; rearrangements, radical migrations, or other complex fragmentation pathways not representable as simple formula losses will be incorrectly flagged as noise.
- Performance degrades for very large molecules (>~1000 Da) where the number of possible subformulas becomes computationally expensive; see original paper for empirical mass limits on the NIST23 database.

## Evidence

- [other] For each fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``): "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``)"
- [other] The formula_denoising function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [other] Get precursor ion infrmation and update the mass tolerance threshold if the measured mass error exceeds the initial tolerance: "Step 1: Get precursor ion infrmation"
- [methods] Step 2: Populate all possible subformulas from master formula, generating candidate fragments sorted by mass: "Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass."
- [methods] Modifying the master formula based on SMILES and adduct information using prep_formula, adding atoms for rare adducts and benzene substructures: "Prepare the master molecular formula by modifying it based on SMILES and adduct information using prep_formula, adding atoms for rare adducts and benzene substructures."
- [methods] Generate denoising tags for each ion using get_denoise_tag, marking ions as True (chemically valid) or False (noise): "Generate denoising tags for each ion using get_denoise_tag, marking ions as True (chemically valid) or False (noise)."
