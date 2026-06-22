---
name: neural-network-scoring-ranking
description: Use when when you have an unknown MS/MS spectrum (m/z and intensity pairs), a set of candidate chemical formula–adduct pairs (enumerated via SIRIUS or another generator), and need to rank them by credibility without access to a spectrum library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MIST-CF
  - SIRIUS
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
---

# Neural-network-scoring-ranking

## Summary

Apply a learned neural network transformer architecture to score and rank candidate molecular assignments (formula–adduct pairs) for an unknown tandem mass spectrum without consulting reference spectral databases. This skill uses energy-based modeling on MS/MS fragment peaks to produce interpretable ranked lists suitable for chemical identification.

## When to use

When you have an unknown MS/MS spectrum (m/z and intensity pairs), a set of candidate chemical formula–adduct pairs (enumerated via SIRIUS or another generator), and need to rank them by credibility without access to a spectrum library. Use this skill in de novo metabolite identification workflows where database-driven matching is unavailable or inappropriate.

## When NOT to use

- Input spectrum is in negative ionization mode; MIST-CF currently supports only positive mode ([M+H]+ and related positive adducts).
- You require explicit fragmentation tree or mechanistic explanation; MIST-CF ranks candidates via learned energy models, not interpretable fragmentation rules.
- No pre-trained model is available for your instrument type or data domain (e.g., Orbitrap vs. QTOF); model performance may degrade without domain-matched training data.

## Inputs

- MS/MS spectrum (m/z and intensity pairs)
- Candidate chemical formula–adduct pairs (list of tuples: formula string, adduct type string)
- Pre-trained MIST-CF model checkpoint

## Outputs

- Ranked list of candidate formula–adduct assignments with scores (descending order)
- Top-ranked chemical formula and adduct assignment
- Energy-based confidence scores per candidate

## How to apply

Load a pre-trained MIST-CF formula transformer model and the corresponding input spectrum in m/z–intensity format. Pass each candidate formula–adduct pair (e.g., [M+H]+, [M+Na]+) through the transformer to compute an energy-based score reflecting the agreement between the precursor formula and the observed fragment peaks. The model learns this ranking in a data-dependent fashion by training on annotated MS/MS spectra, rather than explicitly computing fragmentation trees. Rank candidates by descending score and report the top-ranked formula–adduct assignment with its score. The score reflects the model's learned confidence that the candidate explains the observed spectrum.

## Related tools

- **MIST-CF** (Core neural network model for scoring and ranking formula–adduct assignments from MS/MS spectra) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Enumerates candidate chemical formulas via dynamic programming algorithm; used upstream to generate formula candidates before scoring) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-ranked formula–adduct pair matches the ground-truth annotation (if available); verify by inspection or database lookup.
- Score distribution across candidates is unimodal and well-separated (top candidate has substantially higher score than runners-up), indicating confident ranking.
- Output ranking is consistent across multiple runs with the same input (deterministic model behavior).
- Ranked list includes chemically plausible candidates (e.g., formulas within expected molecular weight range, adducts consistent with ionization mode).
- Model scores correlate with spectral quality metrics (e.g., number and intensity of MS/MS peaks); sparse or low-intensity spectra should produce lower confidence scores.

## Limitations

- Currently supports only positive ionization mode; negative mode MS/MS spectra cannot be ranked.
- Model performance is optimized for training data domains (NPLIB1, NIST20); transfer to novel instrument types (e.g., new Orbitrap configurations) may reduce accuracy.
- Requires pre-enumerated candidate formula–adduct pairs; does not generate de novo formulas without SIRIUS or equivalent upstream tool.
- Score interpretation is learned and data-dependent; absolute scores are not portable across models or datasets.
- Performance depends on MS/MS spectral quality; very few peaks (< 5) may limit model confidence.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [other] Feed candidate formula-adduct pairs through the formula transformer neural network to compute energy-based scores.: "Feed candidate formula-adduct pairs through the formula transformer neural network to compute energy-based scores."
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
