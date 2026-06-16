---
name: chemical-formula-ranking-evaluation
description: Use when after running formula inference on a benchmark dataset with known formula and adduct ground truth (e.g., NPLIB1, NIST20, or CASMI 2022). Apply this skill when you need to quantify ranking performance, isolate the contribution of specific model features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
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

# chemical-formula-ranking-evaluation

## Summary

Evaluate the ranking accuracy of predicted chemical formula and adduct assignments against ground truth annotations by computing top-k metrics and comparing performance across different model architectures or inference modes. This skill determines whether a formula prediction system correctly identifies the true molecular formula among candidates.

## When to use

After running formula inference on a benchmark dataset with known formula and adduct ground truth (e.g., NPLIB1, NIST20, or CASMI 2022). Apply this skill when you need to quantify ranking performance, isolate the contribution of specific model features (e.g., multi-adduct support vs. [M+H]+-only mode), or compare your method against baseline approaches like SIRIUS.

## When NOT to use

- Input dataset lacks ground-truth formula-adduct annotations; evaluation requires labeled reference data.
- Predictions are already aggregated or deduplicated by rank; this skill requires access to full ranked candidate lists per spectrum.
- Only evaluating mass accuracy or isotope pattern matching without considering chemical formula ranking; use alternative metrics for those dimensions.

## Inputs

- MS/MS spectra (in .mgf or vendor format) with precursor m/z
- Ground-truth chemical formula and adduct assignments per spectrum
- Ranked formula-adduct predictions from inference model (list of candidates with scores)

## Outputs

- Top-1, top-3, and top-k accuracy metrics (fraction of spectra with correct pair at or above rank threshold)
- Performance delta report (multi-adduct accuracy minus baseline accuracy)
- Ranking accuracy plots and comparison tables
- Per-spectrum ranking logs (true formula rank, predicted candidates, scores)

## How to apply

Load the benchmark MS/MS dataset with ground-truth chemical formula and adduct annotations. Run the formula prediction system (e.g., MIST-CF) to generate ranked formula-adduct candidate lists. For each spectrum, record the rank position of the true formula-adduct pair. Compute top-1 accuracy (1 if correct formula-adduct pair ranks first, 0 otherwise) and top-k accuracy (1 if true pair ranks within top k candidates) across all spectra. To isolate feature contributions (e.g., multi-adduct support), compute the performance delta by subtracting [M+H]+-only mode accuracy from full multi-adduct mode accuracy on the same test set. Generate a comparison report with accuracy metrics and confidence intervals if multiple evaluation splits are available.

## Related tools

- **MIST-CF** (Formula and adduct ranking system that generates ranked predictions to evaluate) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Baseline formula prediction method for comparative benchmarking against MIST-CF) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Previous work providing sinusoidal formula embeddings used in MIST-CF architecture) — https://arxiv.org/abs/2303.06470

## Examples

```
. run_scripts/benchmarking/eval_models.py
```

## Evaluation signals

- Top-1 and top-k accuracy values fall within 0.0–1.0 range and match expected performance envelope from literature (e.g., MIST-CF top-1 ≥ 70% on NPLIB1).
- Performance delta (multi-adduct minus [M+H]+-only) is non-negative and reflects ablation contribution without introducing logical inconsistencies.
- Accuracy metrics are computed consistently across all spectra in the test set with no missing or NaN values.
- Ranked candidate lists match the number of generated formula hypotheses per spectrum (e.g., output of SIRIUS decomp).
- Comparison plots show consistent ordering across baselines (e.g., if MIST-CF > SIRIUS on one split, hold across multiple evaluation splits).

## Limitations

- Evaluation depends on ground-truth annotations; mislabeled spectra or incorrect adduct assignments in reference data will bias metrics.
- Top-k accuracy is threshold-dependent; choice of k (e.g., k=1, 3, 10) affects conclusions—report multiple thresholds for completeness.
- Performance comparison with SIRIUS requires access to SIRIUS output on identical spectra; version mismatches or different formula enumeration parameters can confound results.
- Multi-adduct ablation (comparing [M+H]+-only vs. full multi-adduct mode) requires running inference twice on the same data, doubling computational cost.

## Evidence

- [intro] performance_comparison_intro: "Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes"
- [intro] delta_calculation: "Calculate the performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to isolate MULTI_ADDUCT_SUPPORT contribution"
- [intro] energy_based_workflow: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [intro] adduct_support_feature: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] benchmark_datasets: "Four key datasets were used in the process of this paper: 1. biomols: A dataset of biologically relevant molecules that we used to learn a fast filter model 2. NPLIB1: A public natural products"
