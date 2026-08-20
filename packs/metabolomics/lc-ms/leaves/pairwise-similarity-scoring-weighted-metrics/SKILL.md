---
name: pairwise-similarity-scoring-weighted-metrics
description: Use when after anchor selection and RT mapping spline fitting, when you have a fitted metabCombiner object with pre-aligned feature pair candidates and need to determine which parameter weights (A for RT, B for m/z, C for similarity score) discriminate true metabolite matches from false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - R
  - metabCombiner
  - mgcv
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pairwise-similarity-scoring-weighted-metrics

## Summary

Compute composite similarity scores for feature pair alignments in LC-MS metabolomics by combining weighted retention time, m/z, and cosine similarity components. This skill enables systematic parameter optimization to identify optimal weight ranges that maximize alignment accuracy against known compound identities.

## When to use

After anchor selection and RT mapping spline fitting, when you have a fitted metabCombiner object with pre-aligned feature pair candidates and need to determine which parameter weights (A for RT, B for m/z, C for similarity score) best discriminate true metabolite matches from false positives in your LC-MS dataset pair. Use this when you have ground truth shared compound identities available to validate parameter choices.

## When NOT to use

- When no ground truth / known shared compound identities are available to validate parameter choices against
- When your fitted metabCombiner object has not yet completed the Anchor Selection and RT Mapping Spline step
- When datasets have already been combined and reduced; this skill operates on pre-alignment candidate objects

## Inputs

- fitted metabCombiner object with pre-aligned feature pair candidates
- retention-time spline mapping from prior anchor selection step
- ground truth table of shared known compound identities across dataset pair
- parameter grid specification (A, B, C ranges and step sizes)

## Outputs

- scores table indexed by parameter triplet (A, B, C) with accuracy/F1-score metrics
- optimal parameter ranges (e.g., A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4])
- count and precision of correctly matched feature pairs per parameter set

## How to apply

Define a three-dimensional parameter grid spanning the full weight space: A ∈ [50, 120] in steps of 10 (RT weight), B ∈ [5, 15] (m/z weight), and C ∈ [0, 1] in steps of 0.1 (cosine similarity weight). Call evaluateParams() over the complete grid, computing pairwise similarity scores for each triplet using the weighted metric that combines retention time deviation, m/z distance, and cosine similarity components. For each parameter set, compare predicted feature pair alignments against known shared metabolite identities (ground truth from your reference datasets) and record accuracy or F1-score metrics. Generate a scores table indexed by parameter triplets and identify contiguous high-scoring regions to extract optimal ranges. For plasma metabolomics datasets, empirical evidence suggests smaller A values (50–70), higher B values (14–15), and average C values (0.3–0.4) yield best performance.

## Related tools

- **metabCombiner** (R package that provides the evaluateParams() function to compute similarity scores over a parameter grid and the data structures (fitted object, feature pair candidates) required for scoring) — https://github.com/hhabra/metabCombiner
- **R** (Programming language environment in which metabCombiner runs and parameter grid iteration/evaluation is implemented)
- **mgcv** (Underlying R package used for spline-based retention time mapping, which provides the RT component of the weighted similarity metric)

## Examples

```
evaluateParams(metabCombinerObj, A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1), groundTruth = knownCompounds) |> filter(F1_score > 0.8) |> group_by(A, B, C)
```

## Evaluation signals

- Scores table is non-empty, indexed by all (A, B, C) triplets in the defined grid, and contains numeric accuracy/F1-score values
- Optimal parameter ranges form contiguous regions in the grid (not scattered singleton values) and show monotonic or smooth score gradients across parameter space
- Precision of correctly matched feature pairs at optimal parameters exceeds baseline or random assignment; F1-score or accuracy is substantially higher in the extracted optimal region than at grid boundaries
- Parameter set optimizing shared known identities also maximizes count of true positive matches and minimizes false positive rate when compared against ground truth
- Extracted optimal ranges (e.g., A ∈ [50, 70]) are narrower and more specific than the initial search grid, indicating genuine convergence rather than grid-wide plateau

## Limitations

- Performance of optimal parameters is tightly coupled to the reference datasets and their shared compound identity annotations; parameters optimized on one pair of LC-MS datasets may not transfer directly to other conditions (e.g., different ionization, MS/MS resolution, or sample matrix)
- evaluateParams() requires ground truth labels of known shared metabolite identities; results are only as reliable as the completeness and accuracy of the reference compound list
- High-dimensional grid search (3D parameter space) is computationally expensive; runtime scales with grid resolution and number of feature pair candidates in the fitted object
- Optimal parameter ranges may exhibit local plateaus or multiple local optima; contiguous high-scoring regions should be validated visually or with independent test data before adoption

## Evidence

- [other] Define a three-dimensional parameter grid with A = seq(50, 120, 10), B = 5:15, and C = seq(0, 1, 0.1) representing RT weight, m/z weight, and similarity score weight respectively.: "Define a three-dimensional parameter grid with A = seq(50, 120, 10), B = 5:15, and C = seq(0, 1, 0.1) representing RT weight, m/z weight, and similarity score weight respectively."
- [other] Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity components.: "Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity"
- [other] Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs.: "Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs."
- [other] Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets.: "Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets."
- [intro] `metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score.: "`metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
