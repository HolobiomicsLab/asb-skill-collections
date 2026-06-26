---
name: retention-time-and-mz-weight-tuning
description: Use when after anchor selection and RT mapping spline construction, when
  you have a fitted metabCombiner object with pre-aligned feature pair candidates
  and need to tune the scoring metric that combines retention time, m/z, and cosine
  similarity components.
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
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics
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

# retention-time-and-mz-weight-tuning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize weighted scoring parameters (retention-time weight A, m/z weight B, and similarity-score weight C) for feature pair alignment in LC-MS metabolomics by systematic grid search and validation against known shared compound identities. This skill determines the parameter ranges that maximize correct identification of overlapping features between disparately-acquired datasets.

## When to use

After anchor selection and RT mapping spline construction, when you have a fitted metabCombiner object with pre-aligned feature pair candidates and need to tune the scoring metric that combines retention time, m/z, and cosine similarity components. Use this skill when you have access to ground-truth known shared metabolite identities in your paired datasets to validate parameter performance.

## When NOT to use

- You lack ground-truth known shared metabolite identities to validate parameter combinations.
- Feature pair candidates have not yet been generated (Anchor Selection and RT Mapping step has not been completed).
- Your datasets have already been manually validated and merged; parameter tuning is only needed during initial alignment optimization.

## Inputs

- fitted metabCombiner object with pre-aligned feature pair candidates
- retention-time spline mapping from prior Anchor Selection and RT Mapping step
- known shared metabolite identities (ground truth) from paired reference datasets

## Outputs

- scores table indexed by parameter triplet (A, B, C) with corresponding accuracy or F1-score metrics
- optimal parameter ranges for A, B, and C
- contiguous high-scoring parameter regions

## How to apply

Construct a three-dimensional parameter grid with A (RT weight) = seq(50, 120, 10), B (m/z weight) = 5:15, and C (similarity-score weight) = seq(0, 1, 0.1). Call evaluateParams() over the complete grid, which computes pairwise similarity scores for each parameter combination using the weighted metric. Evaluate each parameter set against ground-truth known shared metabolite identities from your reference datasets, recording accuracy or F1-score metrics for each triplet (A, B, C). Identify contiguous high-scoring regions and extract the optimal parameter ranges. In the plasma metabolomics context, smaller A values (50–70), higher B values (14–15), and moderate C values (0.3–0.4) yielded the best precision on shared known identities.

## Related tools

- **metabCombiner** (R package for aligning disparately-acquired LC-MS metabolomics datasets; provides evaluateParams() function for grid-search parameter optimization over weighted similarity metrics) — https://github.com/hhabra/metabCombiner
- **mgcv** (R package providing generalized additive models (gam) functionality for retention-time spline mapping; used in prior RT mapping step that feeds into parameter tuning)

## Examples

```
evaluateParams(metabCombiner_obj, A = seq(50, 120, 10), B = 5:15, C = seq(0, 1, 0.1), known_ids = plasma_ground_truth)
```

## Evaluation signals

- Scores table contains an entry for each unique triplet (A, B, C) with no missing combinations.
- Optimal parameter ranges show a contiguous region of high-scoring values (not scattered isolated peaks), indicating robust parameter stability.
- Precision and F1-score on ground-truth shared identities within optimal ranges are higher than outside those ranges.
- The parameter ranges match the domain characteristics of your data: smaller A (RT weight) values dominate for datasets with tight RT reproducibility; larger B (m/z weight) values reflect higher confidence in m/z accuracy.
- Visualization of the scores table across the three-dimensional parameter space shows a clear peak or plateau corresponding to the reported optimal ranges.

## Limitations

- Parameter optimization requires access to high-quality ground-truth known shared metabolite identities; limited or erroneous reference compounds will bias the tuning.
- The optimal parameter ranges are specific to the pair of datasets and acquisition conditions used in tuning; transferability to other dataset pairs, instruments, or chromatographic modes is not guaranteed.
- Grid search is computationally expensive over large feature pair candidate sets; coarser grid resolution (e.g., larger step sizes) may miss finer optima but reduce runtime.
- The weighted metric assumes independence of RT, m/z, and cosine similarity components; correlation between these dimensions could confound parameter interpretation.

## Evidence

- [other] grid definition and evaluateParams workflow: "Define a three-dimensional parameter grid with A = seq(50, 120, 10), B = 5:15, and C = seq(0, 1, 0.1) representing RT weight, m/z weight, and similarity score weight respectively. Call"
- [other] optimal ranges for plasma datasets: "Smaller A values (50-70), higher B values (14-15), and average C values (0.3-0.4) are the best scores based on the shared known identities contained in the pair of plasma datasets."
- [other] input requirement: pre-fitted object and ground truth: "Load the fitted metabCombiner object containing pre-aligned feature pair candidates and retention-time spline mapping from a prior Anchor Selection and RT Mapping step."
- [other] validation against ground truth: "Evaluate each parameter set against known shared metabolite identities (ground truth) from the plasma reference datasets, recording the count and precision of correctly matched feature pairs."
- [intro] metabCombiner workflow step: "Feature Pair Alignment Scoring"
- [readme] core method in metabCombiner README: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features"
