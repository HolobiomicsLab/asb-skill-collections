---
name: subformula-assignment-neural-networks
description: Use when when you have MS/MS spectra with assigned precursor formulas
  and need to annotate fragment peaks with their chemical subformulas, but want to
  avoid the computational overhead of generating full SIRIUS fragmentation trees or
  do not have access to spectrum databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MIST
  - MIST-CF
  - SCARF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
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

# Neural Network-Based Chemical Subformula Assignment for MS/MS Fragments

## Summary

Replace computationally expensive fragmentation tree enumeration (SIRIUS) with a learned neural network formula transformer that ranks candidate subformulas for each observed MS/MS fragment peak in a data-dependent fashion. This skill enables rapid, database-independent subformula prediction conditioned on precursor formula and observed m/z values.

## When to use

When you have MS/MS spectra with assigned precursor formulas and need to annotate fragment peaks with their chemical subformulas, but want to avoid the computational overhead of generating full SIRIUS fragmentation trees or do not have access to spectrum databases. Apply this skill when the goal is to rank subformula candidates for each peak independently using learned patterns from MS/MS data rather than deterministic rule-based fragmentation.

## When NOT to use

- Input spectra lack precursor formula assignments or reliable precursor mass determination—the neural network requires conditioned precursor formula as input.
- Dataset contains primarily low-resolution or noisy MS/MS spectra where m/z values cannot be reliably matched to fragment subformulas; model will struggle with m/z-formula correspondence learning.
- You require interpretable, rule-based fragmentation explanations (e.g., neutral loss rules, McLafferty rearrangements)—neural network predictions are learned patterns, not symbolic fragmentation rules.

## Inputs

- MS/MS spectra (m/z and intensity pairs for fragment peaks)
- MS1 precursor masses (neutral or adduct-assigned)
- Precursor chemical formulas (assigned or candidate list)
- Fragment peak m/z values
- Candidate subformula lists (from SIRIUS decomp or formula enumeration)

## Outputs

- Ranked subformula predictions per fragment peak
- Per-peak subformula accuracy scores
- Exact-match rate per spectrum (fraction of peaks assigned correct subformula)
- Top-k ranking metrics (e.g., fraction of correct subformulas in top-k predictions)
- Fragment peak assignment confidence scores

## How to apply

Train a formula transformer neural network on paired MS/MS spectra and fragment subformula labels using MIST-CF's architecture. For inference: (1) load MS/MS spectra and precursor masses from your dataset; (2) for each observed fragment peak, condition the transformer on the precursor chemical formula and the peak's m/z value; (3) use the network to rank candidate subformulas (enumerated via SIRIUS decomp or a similar formula generator) by learned probability; (4) report per-peak accuracy, top-k ranking metrics, and exact-match rates per spectrum. The formula transformer learns to assign subformulas in a data-dependent fashion without external tree computation, allowing integration into end-to-end energy-based scoring workflows.

## Related tools

- **MIST-CF** (Framework providing the formula transformer neural network architecture and end-to-end energy-based scoring for subformula-conditioned MS/MS ranking) — https://github.com/samgoldman97/mist-cf
- **MIST** (Parent model that MIST-CF extends; provides foundational formula transformer design for fingerprint prediction)
- **SIRIUS** (Used for deterministic formula enumeration (SIRIUS decomp) to generate candidate subformula lists for each m/z, replacing SIRIUS fragmentation trees in the pipeline) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings for encoding chemical formulas in the neural network input representation)

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Per-peak subformula accuracy on held-out test set (fraction of peaks assigned the correct subformula in rank 1).
- Exact-match rate per spectrum (fraction of spectra where all fragment peaks receive correct subformula assignments).
- Top-k ranking metrics (e.g., recall@5, recall@10: what fraction of correct subformulas appear in the network's top-k ranked candidates for each peak).
- Comparison against SIRIUS fragmentation tree subformula assignments on the same test set; MIST-CF should match or exceed SIRIUS accuracy without computing fragmentation trees.
- Prospective validation on benchmarks like CASMI 2022: formula ranking accuracy on challenge spectra with known ground-truth chemical formulas.

## Limitations

- Model is trained on positive-mode MS/MS data only (as stated in the README); extension to negative mode or mixed-mode datasets has not been demonstrated.
- Performance depends on reliable precursor mass annotation and formula assignment; errors in precursor formula propagate downstream to subformula predictions.
- Model trained on public NPLIB1 dataset may underperform on Orbitrap and high-resolution instrument data when compared to models trained on commercial NIST20 library (noted in README as available upon request).
- Subformula predictions are data-dependent and learned from MS/MS patterns; they do not encode explicit fragmentation chemistry rules, so predictions may not align with known fragmentation mechanisms in edge cases.
- Requires formula enumeration step (SIRIUS decomp) as preprocessing; if SIRIUS enumeration fails or is incomplete for a given m/z, candidate subformula ranking will be limited to available candidates.

## Evidence

- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [other] MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks in a data-dependent fashion without external fragmentation tree computation.: "MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks"
- [other] For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees or querying external spectrum databases. Compare predicted subformula assignments against reference labels and compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k predictions).: "For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees or querying external spectrum databases. Compare predicted subformula assignments against"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF: "Utilizing sinusoidal formula embeddings as developed in our previous work SCARF"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)"
