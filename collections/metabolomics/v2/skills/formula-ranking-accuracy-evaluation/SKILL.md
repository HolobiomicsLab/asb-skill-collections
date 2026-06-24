---
name: formula-ranking-accuracy-evaluation
description: Use when use this skill after training or fine-tuning a chemical formula
  transformer model on annotated tandem MS/MS spectra, when you need to measure whether
  the model's ranked formula candidates match ground truth.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0092
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
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

# formula-ranking-accuracy-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate the ranking quality of predicted chemical formulas and adduct assignments by computing top-k accuracy metrics (top-1, top-5, top-10) on held-out test spectra with annotated ground-truth formulas. This skill verifies whether a formula inference model (e.g., MIST-CF) correctly places the true molecular formula within the top-k candidates ranked by model confidence.

## When to use

Use this skill after training or fine-tuning a chemical formula transformer model on annotated tandem MS/MS spectra, when you need to measure whether the model's ranked formula candidates match ground truth. Apply it on a held-out test set to avoid overfitting bias, and especially when extending the model to a new ionisation mode (e.g., negative-mode adducts) or adduct type where no prior validation exists.

## When NOT to use

- Test set is not held-out or overlaps with training data—this will produce inflated accuracy estimates and fail to detect overfitting.
- Annotated formulas in test set are absent or ambiguous—ground truth is required to define a hit.
- Model has not been trained or fine-tuned on the target ionisation mode or adduct type—baseline accuracy will be near zero and not interpretable as a real performance limitation.

## Inputs

- held-out test set of annotated MS/MS spectra (MGF format or equivalent) with ground-truth molecular formulas and adduct assignments
- trained formula inference model (checkpoint or serialized neural network weights)
- ranked formula candidate lists output by the model, with confidence scores or energy-based model scores

## Outputs

- metrics table with top-1, top-5, and top-10 formula ranking accuracy per adduct type
- accuracy scores aggregated across all test spectra and stratified by adduct class
- failure analysis or confusion matrix identifying which formulas or adducts are most frequently misranked

## How to apply

Split your annotated MS/MS spectra into training and held-out test sets. Run the formula inference model (e.g., MIST-CF) on each test spectrum to generate a ranked list of candidate formulas with associated adduct assignments. For each spectrum, check whether the annotated ground-truth formula appears in the top-1, top-5, and top-10 positions of the ranked output. Compute the fraction of spectra where the true formula was recovered at each rank cutoff, storing results in a metrics table indexed by adduct type (e.g., [M-H]−, [M+Cl]−, [M+FA]−) to enable cross-adduct comparison and identify performance bottlenecks.

## Related tools

- **MIST-CF** (formula transformer model that generates ranked candidate formulas and adduct assignments from MS/MS spectra; primary inference engine being evaluated) — https://github.com/samgoldman97/mist-cf
- **SCARF** (provides sinusoidal formula embeddings used as input representation in MIST-CF formula transformer, maintaining consistency across formula tokenization)
- **SIRIUS** (used for deterministic formula enumeration (SIRIUS decomp) to generate candidate formula lists; baseline method for comparison in benchmarking experiments) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- Top-1 accuracy should be >0 for each adduct type; very low values (<5%) indicate model underfitting or data preprocessing errors.
- Top-1 accuracy should be substantially higher than random baseline (which depends on formula candidate space size); if top-1 ≈ 1/|candidate set|, the model is not learning.
- Accuracy should improve monotonically: top-1 ≤ top-5 ≤ top-10; violation indicates output ranking inconsistency or data leakage.
- Performance should be stratified and comparable across adduct types if training data is balanced; large disparities (e.g., >10% gap between [M-H]− and [M+Cl]−) suggest adduct-specific underfitting or dataset skew.
- Metrics table should be fully populated with no missing or NaN values; check for incomplete predictions or filtering that silently drops test spectra.

## Limitations

- Model-dependent performance: ranking accuracy reflects both the formula inference architecture and the quality of MS/MS spectra preprocessing (noise removal, intensity normalization); poor spectra will yield artificially low accuracy even with a well-trained model.
- Adduct assumption: evaluation assumes the true adduct type is known and present in the model's tokenization layer; if an observed spectrum is [M+Na]+ but the model only considers [M+H]+ and [M+NH4]+, accuracy will be zero regardless of correct molecular formula rank.
- Test set annotation quality: errors or ambiguities in ground-truth formula or adduct labels introduce noise; high-confidence annotations from validated repositories (MassIVE, MetaboLights) are essential.
- Generalization gap: models trained on NPLIB1 or NIST20 may show degraded accuracy on out-of-distribution spectra (e.g., different instruments, resolution, or compound classes); separate evaluation on prospective datasets (CASMI 2022) recommended to assess real-world utility.

## Evidence

- [other] Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy: "Evaluate the fine-tuned model on a held-out negative-mode test set by computing top-1, top-5, and top-10 formula ranking accuracy."
- [intro] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [other] Compile results in a metrics table comparing performance across negative adduct types: "Compile results in a metrics table comparing performance across negative adduct types."
- [intro] MIST-CF considers multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [intro] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
