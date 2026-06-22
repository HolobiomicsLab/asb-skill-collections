---
name: grid-search-evaluation-and-threshold-identification
description: Use when you have a fitted alignment model (e.g., metabCombiner object with pre-aligned feature pair candidates and RT spline mapping) and known shared compound identities (ground truth) from reference datasets, and you need to determine which combination of three or more continuous parameters (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metabCombiner
  - mgcv
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
---

# grid-search-evaluation-and-threshold-identification

## Summary

Systematically evaluate a multi-dimensional parameter space by computing similarity metrics across all combinations and validating results against ground-truth identities to identify optimal parameter ranges. This skill is essential when tuning weighted scoring functions in metabolomics feature alignment where the interplay of retention-time, m/z, and spectral similarity weights must be jointly optimized.

## When to use

You have a fitted alignment model (e.g., metabCombiner object with pre-aligned feature pair candidates and RT spline mapping) and known shared compound identities (ground truth) from reference datasets, and you need to determine which combination of three or more continuous parameters (e.g., RT weight A, m/z weight B, similarity weight C) maximizes correspondence accuracy. This is particularly applicable when scoring rules are agnostic to parameter values and you must empirically calibrate them against validated metabolite identities.

## When NOT to use

- No ground-truth compound identities are available; grid search requires validation against known shared metabolites to measure success.
- The scoring function is non-differentiable or has unknown discontinuities; numerical grid search is brittle in such cases.
- Parameter space is very high-dimensional (>5–6 parameters) without prior dimensionality reduction; exhaustive enumeration becomes computationally prohibitive.

## Inputs

- Fitted metabCombiner object containing pre-aligned feature pair candidates and retention-time spline mapping from prior Anchor Selection and RT Mapping step
- Three-dimensional parameter grid definition (ranges and step sizes for A, B, C)
- Ground-truth compound identity annotations (shared known metabolites across both datasets)

## Outputs

- Scores table indexed by parameter triplet (A, B, C) with corresponding accuracy or F1-score metrics
- Identified optimal parameter ranges (e.g., A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4])
- Visualization of high-scoring parameter regions (contiguous zones of good performance)

## How to apply

Define a discrete three-dimensional (or higher-dimensional) grid spanning plausible ranges for each parameter (e.g., A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1)). For each parameter triplet, invoke the scoring function (evaluateParams()) to compute pairwise similarity scores for all feature pair candidates using the weighted metric combining retention time, m/z, and cosine similarity components. After scoring, align predicted pairs against ground-truth shared metabolite identities and record precision, recall, or F1-score metrics for each parameter set. Generate a lookup table indexed by parameter triplets with corresponding accuracy metrics. Finally, identify contiguous regions of high-scoring parameters (e.g., local maxima or plateaus) and extract the optimal ranges by visual inspection or clustering. Report the ranges as closed intervals (e.g., A ∈ [50, 70], B ∈ [14, 15]) that balance performance and robustness.

## Related tools

- **metabCombiner** (Primary package providing evaluateParams() function for parallel evaluation of weighted similarity scoring across parameter grid and fitted alignment objects with pre-computed RT spline mappings.) — github.com/hhabra/metabCombiner
- **mgcv** (R package used internally by metabCombiner for generalized additive models (GAM) implementing the modified retention-time spline mapping used in parameter evaluation.)
- **R** (Host environment for executing evaluateParams() grid sweep, tabulating results, and identifying optimal parameter ranges.)

## Examples

```
evaluateParams(metabCombiner_object, A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1), ground_truth_identities = plasma_reference)
```

## Evaluation signals

- Precision and recall of matched feature pairs improve monotonically or plateau within the identified optimal ranges compared to boundary regions of the parameter grid.
- The optimal ranges are contiguous (not scattered isolated points), indicating a well-defined parameter space peak rather than noise.
- F1-score or accuracy metrics for parameter triplets within the optimal ranges exceed those outside the ranges by a statistically or practically significant margin (e.g., >10% improvement).
- The scores table is complete and non-sparse across the grid; missing or NaN entries indicate incomplete evaluation.
- When the optimal parameters are applied to held-out validation data (or cross-validation folds), the feature pair precision and recall remain consistent with training-set observations, indicating stable generalization.

## Limitations

- Grid search is computationally intensive and may not scale well if the parameter space is very large or step sizes are very fine; coarse-graining or adaptive refinement may be necessary.
- Optimal ranges are sensitive to the quality and representativeness of ground-truth compound identities; sparse or biased ground truth can lead to spurious optimal ranges.
- The identified ranges are specific to the pair of datasets and RT spline mapping used in the evaluation; transfer to new datasets or different preprocessing pipelines is not guaranteed.
- Local plateaus or ridges in the parameter space may result in ambiguous or multi-modal optimal ranges, complicating interpretation and reproducibility.

## Evidence

- [other] Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity components.: "Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity"
- [other] Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs.: "Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs."
- [other] Generate a scores table indexed by parameter triplet (A, B, C) with corresponding accuracy or F1-score metrics.: "Generate a scores table indexed by parameter triplet (A, B, C) with corresponding accuracy or F1-score metrics."
- [other] Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets.: "Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets."
- [intro] `metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score.: "`metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
