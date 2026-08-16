---
name: feature-pair-alignment-parameter-optimization
description: Use when after anchor selection and retention-time spline mapping have produced a candidate list of feature pair alignments, but before final scoring and reduction of the combined table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# feature-pair-alignment-parameter-optimization

## Summary

Systematically optimize the three-component weighted scoring function (retention time weight A, m/z weight B, similarity weight C) used to rank feature pair alignments in untargeted LC-MS metabolomics by grid search and validation against known shared metabolite identities. This skill is essential when combining disparately-acquired datasets where alignment quality directly determines downstream statistical power and metabolite identification accuracy.

## When to use

After anchor selection and retention-time spline mapping have produced a candidate list of feature pair alignments, but before final scoring and reduction of the combined table. Use this skill when you have access to ground-truth metabolite identities (shared known compounds) across both datasets that can serve as a validation benchmark, and when the default or previously-used parameter ranges produce suboptimal precision or recall in matching known metabolites.

## When NOT to use

- Input datasets lack ground-truth metabolite identities or shared known compound annotations — optimization cannot be validated without a benchmark.
- Feature pair candidates have not yet undergone anchor selection and RT spline mapping — evaluateParams() requires pre-aligned candidates as input.
- Datasets are already merged or the combined table has been reduced — parameter optimization must occur before final reduction step.

## Inputs

- fitted metabCombiner object with pre-aligned feature pair candidates
- retention-time spline mapping from prior Anchor Selection and RT Mapping step
- ground-truth metabolite identities (shared known compounds) from both plasma datasets

## Outputs

- scores table indexed by parameter triplet (A, B, C)
- accuracy or F1-score metrics for each parameter combination
- optimal parameter ranges (A, B, C intervals)
- contiguous high-scoring parameter regions

## How to apply

Construct a three-dimensional parameter grid: A (retention-time weight) = seq(50, 120, 10), B (m/z weight) = 5:15, and C (similarity score weight) = seq(0, 1, 0.1). For each triplet (A, B, C), invoke evaluateParams() on the pre-aligned metabCombiner object to recompute pairwise similarity scores using the weighted metric combining retention time, m/z, and cosine similarity components. Evaluate each parameter set by counting correctly matched feature pairs against ground-truth shared known compound identities from the plasma reference datasets, recording accuracy or F1-score for each triplet. Generate a scores table indexed by parameter triplet and identify contiguous high-scoring regions. Extract optimal ranges by locating parameter combinations that maximize both count and precision of correctly matched pairs; the article demonstrates that A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4] produce superior performance on human plasma metabolomics datasets.

## Related tools

- **metabCombiner** (R package providing evaluateParams() function to compute pairwise similarity scores over parameter grid and validate against known metabolite identities) — github.com/hhabra/metabCombiner
- **R** (host language for metabCombiner and grid construction (seq, : operators, data frame indexing))
- **mgcv** (underlying dependency for retention-time spline mapping (gam function) that feeds into parameter optimization)

## Examples

```
grid_params <- expand.grid(A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1)); scores <- evaluateParams(metabCombiner_object, A = grid_params$A, B = grid_params$B, C = grid_params$C, ground_truth = shared_metabolites)
```

## Evaluation signals

- Scores table contains entries for all parameter triplets in the grid with no missing combinations; each row corresponds to unique (A, B, C) tuple.
- Optimal parameter ranges form contiguous regions in 3D space (not scattered isolated points); identified ranges match known shared identity precision and recall.
- F1-score or accuracy metrics for optimal parameter set (e.g., A ∈ [50, 70], B ∈ [14, 15], C ∈ [0.3, 0.4]) exceed baseline or default-parameter performance by measurable margin.
- Correctly matched feature pairs (true positives against ground truth) are concentrated within the identified optimal ranges and sparse outside them.
- Parameter sensitivity analysis shows smooth gradient in performance across grid, not discontinuous jumps (indicating robust optimization rather than overfitting to noise).

## Limitations

- Optimization is specific to the reference datasets and their known metabolite annotations; optimal ranges may not transfer directly to datasets with different acquisition conditions, ionization modes, or metabolite coverage.
- Grid search is exhaustive and computationally expensive for fine-grained resolution; coarser grid spacing (e.g., A = seq(50, 120, 20)) may miss local optima but reduces runtime.
- Results depend critically on the completeness and accuracy of ground-truth metabolite identities; biased or incomplete reference annotations will bias parameter selection.
- No changelog or version history found in the repository, limiting assessment of parameter stability across metabCombiner releases.

## Evidence

- [full_text] parameter_grid_definition: "Define a three-dimensional parameter grid with A = seq(50, 120, 10), B = 5:15, and C = seq(0, 1, 0.1) representing RT weight, m/z weight, and similarity score weight respectively."
- [full_text] evaluateParams_call: "Call evaluateParams() over the complete grid, computing pairwise similarity scores for each parameter combination using the weighted metric combining retention time, m/z, and cosine similarity"
- [full_text] validation_against_known_compounds: "Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs."
- [full_text] optimal_ranges_identified: "Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets."
- [intro] metabcombiner_alignment_workflow: "metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
