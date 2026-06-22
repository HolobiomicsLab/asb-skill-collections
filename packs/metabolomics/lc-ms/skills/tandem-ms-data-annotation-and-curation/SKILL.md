---
name: tandem-ms-data-annotation-and-curation
description: Use when you have an unknown tandem MS/MS spectrum (precursor m/z and fragment peaks) and need to infer the molecular formula and ionization mode (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) in a de novo setting without access to spectral libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - SIRIUS
  - MIST-CF model
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
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

# tandem-ms-data-annotation-and-curation

## Summary

Assign chemical formulas and ionization adducts to tandem mass spectra (MS/MS) using energy-based neural network scoring without spectrum database reference. This skill ranks candidate formula–adduct pairs for unknown precursor masses by learning from fragmentation patterns in an end-to-end fashion.

## When to use

You have an unknown tandem MS/MS spectrum (precursor m/z and fragment peaks) and need to infer the molecular formula and ionization mode (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) in a de novo setting without access to spectral libraries. Apply this skill when you need to rank multiple plausible formula–adduct hypotheses and score their consistency with the observed fragment pattern.

## When NOT to use

- Spectrum is in negative ionization mode (MIST-CF currently supports only positive mode; negative mode ionization is not yet supported)
- You have high-confidence spectral library matches already and only need confirmation rather than de novo ranking
- Input spectrum is a single MS1 (precursor mass only) without MS/MS fragment peaks; MIST-CF requires tandem mass spectrometry data

## Inputs

- Tandem mass spectrum (precursor m/z and fragment peaks in MGF format)
- Precursor neutral mass (derived from m/z and charge state)
- Trained MIST-CF formula transformer model checkpoint
- Known adduct type(s) for hypothesis enumeration (positive mode: [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+)

## Outputs

- Ranked list of candidate formula–adduct pairs with scores
- Top-ranked chemical formula and adduct assignment
- Ranking metrics (rank of ground-truth adduct, recall@k)
- Energy-based model score reflecting spectrum–formula agreement

## How to apply

Load a trained MIST-CF formula transformer model and prepare your spectrum in MGF format with precursor m/z and MS/MS fragment peaks. Use the internal chemical subformula assignment protocol to enumerate candidate formulas for the precursor mass (rather than SIRIUS fragmentation trees). For each candidate formula, consider multiple positive-mode adduct types ([M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) to generate formula–adduct hypotheses. Score each hypothesis by passing the spectrum peaks and candidate formula through the transformer model to predict consistency. Rank hypotheses by score and report rank of ground-truth adduct, recall@k metrics, and the top-ranked formula–adduct assignment as the annotation. The model learns to score agreement between precursor formula candidate and spectrum in a data-dependent fashion without relying on fragmentation tree decomposition.

## Related tools

- **SIRIUS** (Used to enumerate candidate chemical formulas via dynamic programming (`SIRIUS decomp`) for a given precursor m/z; MIST-CF uses an internal subformula assignment protocol instead of SIRIUS fragmentation trees for ranking) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF model** (Trained formula transformer neural network that scores and ranks formula–adduct hypotheses against tandem MS/MS spectra) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Rank of ground-truth formula–adduct pair in the scored candidate list; lower rank indicates better calibration
- Recall@k metric: fraction of spectra for which correct formula–adduct pair appears in top-k predictions
- Comparison of ranking accuracy against baseline single-adduct mode [M+H]+ to quantify improvement from multi-adduct consideration
- Spectrum–formula consistency score magnitude and distribution across correct vs. incorrect candidates; non-overlapping distributions indicate discrimination power
- Schema validation: all output pairs have valid chemical formulas, plausible adduct types, and scores in expected numeric range

## Limitations

- Currently supports only positive ionization mode; negative mode ionization is not yet supported
- Model performance may degrade on high-resolution instruments (e.g., Orbitrap) if trained only on public NPLIB1 dataset; NIST20-trained models are more performant but require license access
- Depends on SIRIUS for initial formula candidate enumeration; performance is upper-bounded by SIRIUS decomposition accuracy
- Assumes sufficient MS/MS peak information (experiments show few peaks are sufficient, but very low-abundance or sparse spectra may reduce ranking confidence)

## Evidence

- [readme] ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Considering multiple adduct types beyond [M+H]+ in positive mode to improve ranking: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Uses an internal chemical subformula assignment protocol rather than SIRIUS fragmentation trees: "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Formula transformer neural network architecture that learns in a data-dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [other] Test dataset should contain tandem mass spectra annotated with known non-protonated adduct types: "prepare a test dataset of tandem mass spectra annotated with known non-protonated adduct types (e.g., [M+Na]+, [M+K]+, [M+NH4]+)"
- [other] Compute ranking metrics including rank of ground-truth adduct and recall@k: "Compute ranking metrics (e.g., rank of ground-truth adduct, recall@k) and collate results in a structured table."
