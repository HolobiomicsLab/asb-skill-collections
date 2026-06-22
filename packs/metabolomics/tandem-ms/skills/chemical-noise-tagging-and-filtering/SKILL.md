---
name: chemical-noise-tagging-and-filtering
description: Use when you have MS/MS spectra contaminated with chemical noise (spurious fragment ions that do not correspond to real chemical bonds or rearrangements), a known or predicted molecular formula or SMILES structure for the precursor, the adduct type (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - RDkit
  - chemparse
  - molmass
  - pandas
  - scipy
  - ms_entropy
  - spectral-denoising (Python package)
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

# Chemical-noise tagging and filtering

## Summary

Remove chemical noise ions from MS/MS spectra by evaluating whether each fragment ion could arise from a chemically plausible subformula loss of the precursor molecule. This skill uses molecular formula constraints derived from SMILES and adduct information to tag ions as valid or noise, then retains only chemically justified fragments.

## When to use

Apply this skill when you have MS/MS spectra contaminated with chemical noise (spurious fragment ions that do not correspond to real chemical bonds or rearrangements), a known or predicted molecular formula or SMILES structure for the precursor, the adduct type (e.g., [M+H]+, [M+Na]+), and a mass tolerance window (typically derived from precursor mass error). Use it before compound library matching or spectral entropy comparison to improve signal-to-noise ratio and reduce false identifications.

## When NOT to use

- When the precursor molecular formula or SMILES is unknown or highly uncertain — the filtering relies entirely on formula constraints and will produce spurious results with incorrect input structures.
- When working with spectra from non-targeted or untargeted metabolomics without reliable compound annotation — chemical noise filtering requires a specific known structure per spectrum.
- When electronic noise dominates the spectrum (e.g., baseline artifacts, detector saturation) rather than chemical noise — use electronic_denoising as a preprocessing step instead, as formula-based filtering does not address instrumental artifacts.

## Inputs

- MS/MS spectrum as (m/z, intensity) array (numpy.float32)
- Precursor m/z value
- Molecular formula (string) or SMILES string
- Adduct type (string, e.g., '[M+H]+', '[M+Na]+')
- Mass tolerance threshold (in Da or ppm)

## Outputs

- Denoised spectrum: (m/z, intensity) array containing only chemically valid fragment ions
- Denoising tag array: boolean array indicating which ions were retained (True) or removed (False)
- Entropy similarity score (optional): numerical comparison against a reference spectrum to validate improvement

## How to apply

Begin by preparing the master molecular formula using the input SMILES and adduct information with prep_formula, which adjusts the formula for adduct atoms and known substructures (e.g., benzene rings). Extract precursor ion statistics using get_pmz_statistics to confirm the observed precursor m/z and refine the mass tolerance if the measured mass error exceeds the initial threshold. Generate all possible subformulas from the master formula using get_all_subformulas, sorted by mass. For each fragment ion in the spectrum, use check_candidates to search for a plausible subformula loss (i.e., master formula minus candidate subformula) that could form that ion within the mass tolerance window. Tag each ion using get_denoise_tag as True (chemically valid loss) or False (noise). Retain only True-tagged ions and add back precursor peaks using add_spectra, then sanitize with sanitize_spectrum to remove any zero-intensity ions and sort by m/z.

## Related tools

- **RDkit** (Parsing SMILES strings and computing molecular properties (formula extraction from structure)) — https://www.rdkit.org
- **chemparse** (Parsing and manipulating chemical formula strings) — https://pypi.org/project/chemparse/
- **molmass** (Computing exact molecular masses for formula fragments and loss calculations) — https://pypi.org/project/molmass/
- **ms_entropy** (Computing entropy similarity between raw and denoised spectra for validation) — https://pypi.org/project/ms-entropy/
- **spectral-denoising (Python package)** (Complete implementation of formula_denoising, prep_formula, get_all_subformulas, check_candidates, get_denoise_tag, and supporting spectral operations) — https://github.com/FanzhouKong/spectral_denoising

## Examples

```
peak_denoised = sd.spectral_denoising(peak_with_noise, 'C1=CC=CC=C1', '[M+H]+')
print(f'entropy similarity: {entropy_similairty(peak_denoised, peak, pmz=pmz):.2f}')
```

## Evaluation signals

- Entropy similarity between denoised spectrum and reference spectrum should increase compared to the raw spectrum (higher indicates better alignment with known chemistry).
- All retained fragment ions must correspond to chemically plausible neutral losses: for each ion, verify that (master_formula − ion_formula) exists in the populated subformula set within mass tolerance.
- Precursor ion ([M+H]+ or corresponding adduct peak) should be preserved in the output; check that add_spectra correctly re-inserts it.
- Output spectrum should have fewer or equal number of peaks than input; verify that at least one ion was tagged False (removed) if chemical noise was present.
- Mass sorting invariant: sanitize_spectrum should ensure output peaks are monotonically increasing by m/z, with no zero-intensity ions.

## Limitations

- Relies on correct SMILES/formula input; errors propagate through all downstream subformula generation, potentially removing valid ions or retaining noise.
- Mass tolerance window must be appropriately set based on instrument calibration; if too narrow, valid ions are removed; if too wide, noise ions pass through.
- Cannot distinguish between isomeric fragments (same formula, different structure) — the algorithm operates only on formula, not connectivity, so chemically plausible losses are overapproximated.
- Rare adducts or unusual rearrangements not captured by the master formula adjustment (prep_formula) will not be recognized; the method assumes common adducts and simple neutral losses.
- Performance depends on the completeness of the subformula database; if subformulas with large mass differences are missing, some valid losses may not be detected.

## Evidence

- [other] The formula_denoising function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss: "The ``formula_denoising`` function removes chemical noise ions in MS/MS spectra by evaluating if it could be formed from a chemically plausible subformula loss"
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] For each fragment ion, checking if a plausible subformula loss could form that ion, and tagging ions for removal based on whether they match chemically plausible losses.: "for each fragment ion, checking if a plausible subformula loss could form that ion, and (4) tagging ions for removal based on whether they match chemically plausible losses."
- [other] Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass.: "Populate all possible subformulas from the master formula using get_all_subformulas, generating candidate fragments sorted by mass."
- [other] For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``).: "For any given fragment ion, the algorithm will try to find a plausible subformula loss that could form this ion (function ``check_cnadidates``)."
- [other] Retain only True-tagged fragment ions and add back precursor ions using add_spectra, then sanitize the result with sanitize_spectrum.: "Retain only True-tagged fragment ions and add back precursor ions using add_spectra, then sanitize the result with sanitize_spectrum."
- [readme] Note: Even all functions have a default 'smiles' information column, the function would also accept formula as input.: "Even all functions have a default 'smiles' information column, the function would also accept formula as input."
