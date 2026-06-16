---
name: formula-transformer-architecture-application
description: Use when you have tandem mass spectra (MS/MS) with unknown precursor formulas and need to rank chemical formula candidates conditioned on observed fragment m/z values and precursor mass. Use this skill when fragmentation tree computation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - MIST
  - MIST-CF
  - SCARF
  - SIRIUS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
---

# formula-transformer-architecture-application

## Summary

Apply a neural network formula transformer to rank candidate chemical formulas and adducts for unknown MS/MS spectra in a data-dependent fashion, using an internal subformula assignment protocol instead of pre-computed fragmentation trees. This end-to-end energy-based approach enables de novo formula annotation without spectrum database queries.

## When to use

You have tandem mass spectra (MS/MS) with unknown precursor formulas and need to rank chemical formula candidates conditioned on observed fragment m/z values and precursor mass. Use this skill when fragmentation tree computation (e.g., SIRIUS) is unavailable or too slow, and when you want the model to learn subformula assignments directly from spectrum peaks rather than relying on external tree inference.

## When NOT to use

- Input spectra are from negative ionization mode; the current model only supports positive mode
- You need fragment structure prediction or molecular fingerprints; this skill only ranks chemical formulas, not 2D/3D structures
- Precursor formula is unknown and SIRIUS decomposition is unavailable; the transformer requires a precursor formula constraint to condition peak assignments

## Inputs

- MS/MS spectra (peak lists with m/z and intensity)
- MS1 precursor masses
- Precursor chemical formula (from SIRIUS decomp or enumeration)
- Candidate chemical formula list
- Instrument type metadata (optional covariate)

## Outputs

- Ranked chemical formula assignments per spectrum
- Ranked adduct type assignments (e.g., [M+H]+, [M+Na]+)
- Per-peak subformula predictions with confidence scores
- Per-spectrum exact-match accuracy and top-k ranking metrics
- Per-peak assignment accuracy

## How to apply

Load MS/MS spectra and MS1 precursor masses into the formula transformer neural network, which ingests observed peak m/z values and the precursor formula constraint. The network assigns candidate subformulas to each fragment peak using sinusoidal formula embeddings (from SCARF) and learns ranking in a data-dependent fashion without computing SIRIUS fragmentation trees. For each spectrum, generate per-peak subformula predictions and rank overall formula-adduct candidates by aggregated model scores. Evaluate using exact-match accuracy per spectrum and per-peak ranking metrics (e.g., fraction of correct subformulas in top-k). The model considers multiple adduct types (positive mode) beyond [M+H]+ and can be conditioned on instrument type as a model covariate to improve generalization.

## Related tools

- **MIST-CF** (End-to-end neural network architecture implementing the formula transformer and internal subformula assignment protocol) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Provides dynamic programming algorithm (SIRIUS decomp) for formula enumeration; MIST-CF uses this to generate candidate formula lists but replaces SIRIUS fragmentation tree computation with internal neural network subformula assignment) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings used in the MIST-CF formula transformer to represent chemical formulas) — https://arxiv.org/abs/2303.06470

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Per-spectrum exact-match rate: fraction of spectra where the top-ranked formula matches the ground truth reference label
- Per-peak subformula accuracy: fraction of predicted subformulas that match reference labels across all peaks
- Top-k ranking metrics: fraction of correct subformulas appearing in top-k predictions (e.g., top-1, top-3, top-10)
- Comparison against baseline models (FFN, MS1-only, standard transformer): MIST-CF should show competitive or superior ranking performance on held-out test data
- Performance breakdown by instrument type: if instrument metadata is embedded as a covariate, accuracy should not degrade significantly for low-representativity instrument types in training data

## Limitations

- Only supports positive ionization mode; negative mode spectra require model retraining
- Requires ground-truth precursor formula or reliable formula enumeration from SIRIUS decomp; performance degrades if candidate formula list is incomplete or incorrect
- Model trained on NPLIB1 (public natural products) may be less performant on commercial datasets like NIST20; licensing required for NIST20 training data
- Peak ranking depends on accurate m/z measurement; low-resolution or miscalibrated spectra may reduce subformula assignment quality
- Internal subformula assignment protocol is learned end-to-end; interpretability of per-peak decisions is limited compared to explicit fragmentation tree methods

## Evidence

- [other] MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks in a data-dependent fashion without external fragmentation tree computation.: "MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [other] Apply the MIST-CF internal subformula assignment protocol (neural network-based formula transformer) to rank candidate subformulas for each observed fragment peak, conditioned on the precursor formula and observed m/z value.: "Apply the MIST-CF internal subformula assignment protocol (neural network-based formula transformer) to rank candidate subformulas for each observed fragment peak, conditioned on the precursor"
- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF: "Utilizing sinusoidal formula embeddings as developed in our previous work SCARF"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Embedding instrument type used to measure the MS/MS as an additional model covariate to help make predictions: "Embedding instrument type used to measure the MS/MS as an additional model covariate to help make predictions"
