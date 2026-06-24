---
name: energy-based-model-inference
description: Use when when you have an unknown MS/MS spectrum (m/z and intensity pairs)
  and need to assign a chemical formula and ionization adduct to the precursor mass,
  particularly when spectrum database lookups are unavailable or when you want to
  exploit learned patterns in fragmentation rather than.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# energy-based-model-inference

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use a learned energy-based neural network model to score and rank candidate chemical assignments (formula–adduct pairs) for an unknown tandem mass spectrum without relying on spectral databases. This approach learns data-dependent scoring directly from MS/MS fragmentation patterns rather than computing deterministic fragmentation trees.

## When to use

When you have an unknown MS/MS spectrum (m/z and intensity pairs) and need to assign a chemical formula and ionization adduct to the precursor mass, particularly when spectrum database lookups are unavailable or when you want to exploit learned patterns in fragmentation rather than rule-based tree decomposition. Useful in de novo metabolomics workflows where the unknown compound is not in existing libraries.

## When NOT to use

- Input is negative-mode MS/MS data; MIST-CF currently supports only positive-mode ionization.
- You have a high-confidence spectral library match already available; database lookup is faster and more reliable in that case.
- Input spectrum has < ~5 major fragment peaks; energy-based models may not learn robust patterns from very sparse data.

## Inputs

- MS/MS spectrum as m/z–intensity pairs (MGF format or equivalent)
- Precursor m/z value
- Precursor charge state (typically +1 for positive mode)
- MIST-CF trained model weights (PyTorch or equivalent)
- SIRIUS binary or library for candidate formula enumeration

## Outputs

- Ranked list of (chemical_formula, adduct_type, energy_score) tuples
- Top-1 or top-k predictions with formula and adduct assignment

## How to apply

Load a pre-trained MIST-CF formula transformer model and prepare your MS/MS spectrum as m/z–intensity pairs. Use an internal chemical subformula assignment protocol (implemented via SIRIUS decomp) to enumerate all chemically feasible candidate formulas and adduct types (e.g., [M+H]+, [M+Na]+, [M+K]+ in positive mode) for the observed precursor m/z. Feed each formula–adduct candidate paired with the observed fragment peaks through the formula transformer neural network to compute an energy-based score reflecting agreement between the candidate and spectrum. Rank all candidates by descending score. The model learns to weight fragment patterns and neutral losses in a data-dependent fashion, making it more flexible than fixed fragmentation rules; higher scores indicate better candidate–spectrum fit.

## Related tools

- **MIST-CF** (Core formula transformer model that scores formula–adduct candidate pairs against an observed MS/MS spectrum) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Enumerates candidate chemical formulas via dynamic programming decomposition of the observed precursor m/z) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-1 accuracy: Correct chemical formula appears as rank-1 prediction in ≥70–80% of test spectra (baseline dataset-dependent).
- Top-k recall: Correct formula ranked within top-5 or top-10 predictions; compare against SIRIUS or other tree-based baseline methods.
- Score distribution: Higher-ranked candidates should have significantly higher energy scores than lower-ranked ones; check for monotonicity or large score gaps at rank transitions.
- Adduct detection: [M+H]+ and other adduct assignments should match known ionization modes for the dataset (e.g., all [M+H]+ for a standard ESI+ run).
- Consistency across MS instruments: Apply trained model to data from different instrument types (Orbitrap, Q-TOF, etc.); expect stable ranking if the model generalizes well.

## Limitations

- Model supports positive-mode ionization only; negative-mode spectra require retraining or a separate model.
- Performance may degrade on high-resolution data (e.g., Orbitrap) if trained on lower-resolution spectra; the paper notes that models trained on public NPLIB1 are 'less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)'.
- Relies on SIRIUS for candidate formula enumeration; if SIRIUS fails to enumerate the true formula, the model cannot rank it.
- Requires sufficient MS/MS peak intensity information; very low signal-to-noise or few peaks may limit model confidence.
- Energy-based scores are not directly calibrated to posterior probabilities; absolute score values are not interpretable without reference to the training distribution.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)."
- [other] Prepare input mass spectrum data in the required format (m/z and intensity pairs). Apply the internal chemical subformula assignment protocol to enumerate candidate formulas and adduct types (including [M+H]+ and other positive mode adducts). Feed candidate formula-adduct pairs through the formula transformer neural network to compute energy-based scores.: "Prepare input mass spectrum data in the required format (m/z and intensity pairs). Apply the internal chemical subformula assignment protocol to enumerate candidate formulas and adduct types"
