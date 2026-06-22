---
name: mass-spectrum-de-novo-analysis
description: Use when you have an unknown MS/MS spectrum (m/z and intensity pairs) from positive-mode ionization and need to identify the most likely molecular formula and adduct type (e.g., [M+H]+, [M+Na]+) when no reference library match is available or desirable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MIST-CF
  - SIRIUS
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- MIST-CF ranks chemical formula and adduct assignments
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-de-novo-analysis

## Summary

Rank candidate chemical formula and adduct assignments for unknown tandem mass spectra using a data-driven transformer neural network without relying on spectral databases or fragmentation tree computation. MIST-CF learns end-to-end energy-based rankings directly from MS/MS peak patterns to infer precursor molecular identity in de novo settings.

## When to use

You have an unknown MS/MS spectrum (m/z and intensity pairs) from positive-mode ionization and need to identify the most likely molecular formula and adduct type (e.g., [M+H]+, [M+Na]+) when no reference library match is available or desirable. Use this when you have only a few MS/MS peaks (the method shows performance with as few as 5–10 fragment peaks) and want to avoid dependence on curated spectral databases.

## When NOT to use

- Input spectrum is from negative-mode ionization — MIST-CF currently supports only positive mode adducts.
- Precursor m/z is outside typical metabolite range (< 50 or > 2000 Da) — model was trained on natural products and metabolites in standard ranges.
- You have a very high-resolution spectrum where multiple formulas fit within measurement tolerance — formula enumeration can become intractable without additional filtering.

## Inputs

- Tandem mass spectrum (m/z and intensity pairs in MGF format or equivalent)
- Precursor m/z value
- Instrument type (optional but recommended: e.g., 'Orbitrap', 'Q-TOF')
- Ionization mode (positive mode only in current version)

## Outputs

- Ranked list of candidate chemical formulas with assigned adduct types
- Energy-based score for each candidate (higher = better agreement)
- Top-ranked chemical formula and adduct assignment for the unknown spectrum

## How to apply

Load a pre-trained MIST-CF formula transformer model and prepare input spectrum data as m/z and intensity pairs in MGF or similar format. Use an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees) to enumerate all candidate chemical formulas within the mass range of the precursor. For each candidate formula, enumerate multiple positive-mode adduct types beyond [M+H]+ (e.g., [M+Na]+, [M+K]+, [M+NH4]+). Feed each candidate formula–adduct pair and the MS/MS peak list through the transformer network to compute energy-based scores that reflect agreement between the proposed formula fragmentation patterns and observed peaks. Rank candidates by descending score. The model uses sinusoidal formula embeddings and optionally conditions on instrument type (e.g., Orbitrap, Q-TOF) to improve predictions. Return the top-ranked formula–adduct assignments with their scores.

## Related tools

- **SIRIUS** (Provides the deterministic dynamic programming algorithm (SIRIUS decomp) for chemical subformula enumeration given a precursor m/z; MIST-CF uses this for candidate formula generation but replaces SIRIUS's fragmentation tree scoring with learned transformer scores) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Core trained neural network model implementing formula transformer architecture for end-to-end energy-based ranking of formula–adduct pairs) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-ranked formula matches the true molecular formula (exact match or isotopic variant) in benchmarked datasets (e.g., NPLIB1, CASMI 2022).
- Assigned adduct type corresponds to known ionization conditions (e.g., [M+H]+ in standard positive-mode ESI).
- Energy score is substantially higher for correct formula than for the next-ranked candidate (score gap indicates confidence).
- Rank-1 accuracy (top candidate is correct) meets or exceeds reported performance on test splits (aim: >70% for NPLIB1; ~50–60% on CASMI 2022 prospective data).
- Model output includes only chemically valid formulas (no negative element counts, formulae consistent with molecular weight constraints within instrument mass accuracy).

## Limitations

- Negative-mode ionization not yet supported; only positive mode adducts ([M+H]+, [M+Na]+, [M+K]+, [M+NH4]+, etc.) are handled.
- Model performance may degrade on spectra from high-resolution instruments (e.g., Orbitrap) if trained predominantly on lower-resolution data (NIST20 models available upon request for better performance on Orbitrap data).
- Requires a trained model checkpoint; retraining on custom datasets requires access to annotated MS/MS spectra with known chemical formulas.
- Performance depends on sufficient MS/MS peak information — very low-abundance or few-peak spectra may have lower ranking reliability.
- Does not infer full structural connectivity or stereochemistry, only molecular formula and likely adduct; subsequent tools (e.g., structure elucidation) are needed for complete identification.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF](https://arxiv.org/abs/2303.06470); Embedding instrument type used to measure the MS/MS as an additional model 'covariate' to help make predictions; Embedding the neutral loss fragment formula for each peak in addition to the fragment formula: "Utilizing sinusoidal *formula* embeddings; Embedding instrument type used to measure the MS/MS; Embedding the neutral loss fragment formula for each peak"
- [readme] Model output will be saved in `quickstart/mist_cf_out/`. This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)."
