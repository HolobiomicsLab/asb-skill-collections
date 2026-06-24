---
name: mass-spectrum-adduct-assignment
description: Use when when analyzing tandem mass spectra with unknown precursor adduct
  identity, especially for positive-mode data containing non-protonated adducts ([M+Na]+,
  [M+K]+, [M+NH4]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - SIRIUS
  - MIST-CF
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS
  fragmentation trees)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-adduct-assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank and assign multiple ionization adduct types (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) to tandem mass spectra using energy-based neural scoring, enabling chemical formula assignment without relying on fragmentation trees or spectrum databases.

## When to use

When analyzing tandem mass spectra with unknown precursor adduct identity, especially for positive-mode data containing non-protonated adducts ([M+Na]+, [M+K]+, [M+NH4]+). Adduct assignment is critical when spectra originate from diverse sample preparation or ionization conditions where [M+H]+ cannot be assumed.

## When NOT to use

- Input is negative-mode mass spectrometry data; MIST-CF currently supports only positive-mode ionization.
- Precursor m/z is unknown or not provided; adduct assignment requires a measured parent ion mass.
- Sample is already annotated with correct adduct identity; ranking and assignment are redundant.

## Inputs

- tandem mass spectrum (MGF format) with known precursor m/z
- trained MIST-CF formula transformer model checkpoint
- list of candidate positive-mode adduct types to consider (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+)

## Outputs

- ranked list of (adduct_type, chemical_formula) pairs with scores
- top-ranked adduct assignment and corresponding neutral formula
- ranking metrics (ground-truth adduct rank, recall@k for evaluation datasets)

## How to apply

Load a pre-trained MIST-CF formula transformer model and provide a tandem mass spectrum in MGF format with known precursor m/z. Use the internal chemical subformula assignment module (rather than SIRIUS fragmentation trees) to enumerate candidate adduct-formula pairs for multiple positive-mode adduct types. For each candidate pair, the formula transformer scores agreement between the precursor formula and observed MS/MS peaks using an end-to-end energy-based model trained on fragmentation patterns. Rank candidates by score and extract the top-ranked adduct assignment. Compute ranking metrics (e.g., rank of ground-truth adduct, recall@k) to assess whether multi-adduct consideration improves over single-adduct baselines.

## Related tools

- **SIRIUS** (Dynamic programming algorithm for enumerating candidate chemical formulae from observed m/z; used for formula candidate generation (though MIST-CF uses internal subformula assignment for adduct scoring rather than SIRIUS fragmentation trees).) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (End-to-end formula transformer neural network that scores and ranks adduct-formula pairs for tandem mass spectra; primary implementation for this skill.) — https://github.com/samgoldman97/mist-cf

## Examples

```
python src/mist_cf/mist_cf_score/predict_mgf.py --model_checkpoint quickstart/mist_cf_model.pt --input_spectra data/demo_specs.mgf --adduct_types '[M+H]+,[M+Na]+,[M+K]+,[M+NH4]+' --output_dir quickstart/mist_cf_out/
```

## Evaluation signals

- Ground-truth adduct appears in top-k ranks (recall@k metric) on evaluation dataset; higher recall indicates effective multi-adduct ranking.
- Ranking accuracy on spectra with non-protonated adducts ([M+Na]+, [M+K]+, [M+NH4]+) exceeds single-[M+H]+ baseline, confirming multi-adduct consideration improves performance.
- Score distribution is unimodal and concentrated on top-ranked pair; bimodal or diffuse distributions suggest model uncertainty or calibration issues.
- Precursor formula mass computed from top-ranked adduct matches observed m/z within instrument mass accuracy tolerance (typically <5 ppm for high-resolution data).
- Output adduct-formula pairs satisfy chemical validity constraints (e.g., positive charge, non-negative atom counts).

## Limitations

- MIST-CF currently supports positive-mode ionization only; negative-mode adducts ([M−H]−, [M+Cl]−, etc.) are not yet implemented.
- Model performance is calibrated on NPLIB1 (public natural products) and NIST20 (proprietary) spectral libraries; transfer to novel chemical classes or unusual ionization conditions may degrade ranking accuracy.
- Requires sufficient MS/MS fragment peaks (formula transformer shown to be robust to <10 peaks, but very sparse spectra may limit discrimination between candidate adducts).
- Internal chemical subformula assignment protocol is data-dependent; adduct ranking inherits any systematic biases in the training dataset or model parameterization.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Utilizing an internal chemical subformula assignment protocol rather than SIRIUS fragmentation trees for adduct assignment.: "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Multi-adduct support in positive mode beyond [M+H]+ adduct type.: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [other] Does extending MIST-CF to consider multiple positive-mode adduct types beyond [M+H]+ improve ranking accuracy for chemical formula and adduct assignments on spectra with non-protonated adducts?: "Does extending MIST-CF to consider multiple positive-mode adduct types beyond [M+H]+ improve ranking accuracy for chemical formula and adduct assignments on spectra with non-protonated adducts?"
- [other] For each spectrum, run the extended adduct-assignment protocol using the internal chemical subformula assignment method to score and rank candidate adduct-formula pairs.: "For each spectrum, run the extended adduct-assignment protocol using the internal chemical subformula assignment method to score and rank candidate adduct-formula pairs."
