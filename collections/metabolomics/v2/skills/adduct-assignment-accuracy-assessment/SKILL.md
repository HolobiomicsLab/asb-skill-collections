---
name: adduct-assignment-accuracy-assessment
description: Use when you have a trained formula ranking model (such as MIST-CF) and
  want to measure the specific performance gain from incorporating multiple positive-mode
  adduct types (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) instead of restricting predictions
  to [M+H]+ only.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - MIST
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
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
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

# adduct-assignment-accuracy-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify the contribution of multi-adduct support to chemical formula ranking accuracy by comparing model performance in [M+H]+-only mode versus full multi-adduct mode. This skill isolates the performance delta attributable to adduct type diversity in MS/MS-based formula inference.

## When to use

Apply this skill when you have a trained formula ranking model (such as MIST-CF) and want to measure the specific performance gain from incorporating multiple positive-mode adduct types (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+) instead of restricting predictions to [M+H]+ only. Use it after model development but before deployment to quantify whether multi-adduct support is worth the added complexity.

## When NOT to use

- Your model only supports [M+H]+ ionization or has no multi-adduct architecture — the comparison will be meaningless.
- Ground-truth adduct assignments are missing or unreliable in your benchmark dataset — accuracy metrics will be invalid.
- You are only interested in negative-mode ionization; MIST-CF multi-adduct support is documented as positive-mode only.

## Inputs

- MS/MS spectra dataset with ground-truth chemical formula annotations
- Ground-truth adduct type labels (positive-mode ionization types)
- Trained MIST-CF model or equivalent energy-based formula ranking model
- Model configuration or mode selector for [M+H]+-only versus multi-adduct inference

## Outputs

- Top-1 ranking accuracy score for [M+H]+-only mode
- Top-k ranking accuracy scores for [M+H]+-only mode (k = 1, 5, 10, etc.)
- Top-1 ranking accuracy score for multi-adduct mode
- Top-k ranking accuracy scores for multi-adduct mode
- Performance delta report (accuracy improvement from multi-adduct support)
- Ranked formula–adduct pair predictions for both modes (for qualitative analysis)

## How to apply

Load a published benchmark dataset with MS/MS spectra that include ground-truth formula and adduct assignments. Run the model inference twice: once in [M+H]+-only mode (where the model ranks formulas without considering alternative adduct types) and once in full multi-adduct mode (using the complete energy-based modeling approach to rank formula–adduct pairs across all supported positive-mode adducts). For each mode, record ranked predictions and compute top-1 and top-k ranking accuracy metrics (the fraction of spectra where the correct formula–adduct pair is ranked at position 1 or within the top k). Calculate the performance delta as multi-adduct accuracy minus [M+H]+-only accuracy, disaggregated by rank threshold and optionally by dataset subset (e.g., compound class, instrument type). Document the magnitude and statistical significance of the improvement to justify the additional modeling complexity.

## Related tools

- **MIST-CF** (Energy-based neural network model that scores agreement between precursor formula candidates and MS/MS spectra; supports both [M+H]+-only and multi-adduct modes for ranking formula–adduct pairs) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Used for deterministic formula enumeration via the `SIRIUS decomp` dynamic programming algorithm to generate candidate formulas for a given precursor mass)

## Evaluation signals

- Top-1 ranking accuracy in multi-adduct mode is ≥ top-1 accuracy in [M+H]+-only mode (monotonic improvement or parity expected).
- Performance delta (multi-adduct minus [M+H]+-only) is positive and consistent across multiple evaluation splits or dataset subsets, indicating robust improvement rather than noise.
- The magnitude of the delta is sufficient to justify added model complexity (e.g., >1–2 percentage point improvement in top-1 accuracy).
- Ranked predictions include formula–adduct pairs where the correct adduct is not [M+H]+; spot-checking confirms these are ranked appropriately higher in multi-adduct mode than in [M+H]+-only mode.
- Top-k accuracy curves (k = 1, 5, 10, ...) show the multi-adduct curve dominates or converges faster than [M+H]+-only, indicating better ranking quality.

## Limitations

- MIST-CF multi-adduct support is restricted to positive-mode ionization; negative-mode or mixed-polarity experiments are not covered.
- The performance delta depends heavily on the composition of the benchmark dataset (e.g., abundance of non-[M+H]+ adducts in ground truth); gains may be smaller on datasets dominated by [M+H]+ annotations.
- The [M+H]+-only baseline may not be optimal (e.g., it may not fully suppress non-[M+H]+ adduct predictions); a truly isolated comparison would require architectural retraining, which is not always feasible.
- Ground-truth adduct assignments must be reliable; errors in labeling will inflate or deflate the observed delta.

## Evidence

- [intro] MIST-CF considers multiple adduct types beyond [M+H]+ in positive mode: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [other] Workflow involves running MIST-CF in two modes and computing ranking accuracy metrics: "Run MIST-CF inference in [M+H]+-only mode, restricting the model to rank formulas without multi-adduct support, and record ranked formula predictions and adduct assignments. 3. Run MIST-CF inference"
- [other] Performance delta is computed to isolate multi-adduct contribution: "Calculate the performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to isolate MULTI_ADDUCT_SUPPORT contribution and generate a comparison report"
- [intro] MIST-CF uses energy-based modeling to rank formula and adduct assignments: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [other] Top-k ranking accuracy is a standard evaluation metric: "Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes"
