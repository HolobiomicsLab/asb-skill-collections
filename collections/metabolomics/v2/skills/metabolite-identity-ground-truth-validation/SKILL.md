---
name: metabolite-identity-ground-truth-validation
description: Use when after constructing candidate feature pair alignments and retention-time spline mappings in a multi-dataset LC-MS metabolomics integration workflow, when you have access to independent ground-truth annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3941
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - metabCombiner
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identity-ground-truth-validation

## Summary

Validate feature pair alignment scoring parameters by comparing predicted matches against known shared metabolite identities in reference metabolomics datasets. This skill ensures that the weighted similarity metric (combining retention time, m/z, and spectral similarity) correctly recovers ground-truth compound correspondences before applying it to the full dataset.

## When to use

After constructing candidate feature pair alignments and retention-time spline mappings in a multi-dataset LC-MS metabolomics integration workflow, when you have access to independent ground-truth annotations (e.g., known shared compound identities in reference plasma datasets) and need to optimize the three-component scoring weights (A for RT weight, B for m/z weight, C for spectral similarity weight) to maximize alignment accuracy on validated pairs.

## When NOT to use

- Feature pair candidates have not yet been generated or pre-aligned (run m/z grouping and pairwise alignment detection first)
- Retention-time spline mapping has not been established (perform anchor selection and RT mapping before scoring optimization)
- Ground-truth metabolite identity annotations are unavailable or unreliable in reference datasets (validation will be uninformative)

## Inputs

- fitted metabCombiner object (with pre-aligned feature pair candidates)
- retention-time spline mapping (from prior Anchor Selection and RT Mapping step)
- reference plasma datasets with known shared metabolite identity annotations (ground truth)

## Outputs

- scores table indexed by parameter triplet (A, B, C) with accuracy/F1-score metrics
- optimal parameter ranges: A, B, C coordinate regions with highest validation accuracy
- precision and count of correctly matched feature pairs for each parameter set

## How to apply

Load the fitted metabCombiner object containing pre-aligned feature pair candidates and retention-time spline mapping from prior anchor selection and RT mapping steps. Define a three-dimensional parameter grid (e.g., A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1)) representing the three scoring weights. Call evaluateParams() over the complete grid to compute pairwise similarity scores for each parameter combination using the weighted metric. For each parameter triplet, compare the predicted feature pair matches against ground-truth shared metabolite identities from the reference datasets, recording count and precision of correctly matched pairs. Generate a scores table indexed by parameter triplet with corresponding accuracy or F1-score metrics. Identify contiguous high-scoring regions to extract optimal parameter ranges that balance all three weight components; for plasma metabolomics, literature and empirical validation suggest A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4] as a starting point.

## Related tools

- **metabCombiner** (Provides evaluateParams() function and data structures (fitted metabCombiner object) for parameter grid evaluation and weighted similarity scoring of feature pair alignments) — https://github.com/hhabra/metabCombiner
- **R** (Execution language for parameter grid generation (seq, ranges), evaluateParams() function calls, and scores table aggregation)

## Examples

```
evaluateParams(metabCombiner_obj, A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1), ground_truth = shared_metabolites)
```

## Evaluation signals

- Scores table contains one entry for each triplet in the parameter grid (e.g., 8 × 11 × 11 = 968 entries for A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1))
- F1-score or accuracy metric values are in the range [0, 1] and increase/plateau as parameters approach optimal region, then decrease again
- Extracted optimal ranges (e.g., A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4]) form a contiguous high-scoring region in parameter space with consistent precision on ground-truth matches
- Precision of correctly matched feature pairs is substantially higher in optimal region than in low-scoring peripheral regions
- Optimal parameters produce F1-score or accuracy that exceeds baseline (e.g., equal weighting or uninformed guesses) by a measurable margin (e.g., >10 percentage points improvement)

## Limitations

- Validation depends critically on the quality and coverage of ground-truth metabolite identity annotations; sparse or incorrect annotations will mislead parameter optimization
- Parameter grid resolution (step size) affects the precision of optimal range extraction; finer grids improve accuracy but increase computational cost
- Optimal parameter ranges are dataset-specific and may not transfer directly to plasma samples acquired under different instrument conditions or ionization modes
- The three-component weighted metric assumes independence of RT, m/z, and spectral similarity scores; dependencies could bias the parameter search

## Evidence

- [intro] Defines the ground-truth evaluation approach: "Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs."
- [intro] Describes the parameter grid structure and optimal ranges found: "Define a three-dimensional parameter grid with A = seq(50, 120, 10), B = 5:15, and C = seq(0, 1, 0.1) representing RT weight, m/z weight, and similarity score weight respectively. ... Identify"
- [intro] Core scoring methodology using weighted metric: "Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity"
- [intro] Input requirements from prior workflow step: "Load the fitted metabCombiner object containing pre-aligned feature pair candidates and retention-time spline mapping from a prior Anchor Selection and RT Mapping step."
- [intro] Dataset context for validation: "We demonstrate each step on a pair of human plasma metabolomics datasets contained within the package."
