---
name: annotation-benchmark-performance-evaluation
description: Use when after running an end-to-end annotation workflow (matching, clustering, filtering, and prioritization) on untargeted LC-MS peak tables, when you have access to a curated reference dataset (df.Ref) containing validated peak assignments for the same biological sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
- we will now use the sample graph provided by FELLA R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotation-benchmark-performance-evaluation

## Summary

Quantify the quality of untargeted LC-MS metabolite annotation workflows by computing precision, recall, and F1-score against curated reference peak benchmarks. This skill applies when you have both annotated peak predictions and a validated reference dataset, and need to assess whether the annotation pipeline recovers true metabolites and avoids false assignments.

## When to use

Apply this skill after running an end-to-end annotation workflow (matching, clustering, filtering, and prioritization) on untargeted LC-MS peak tables, when you have access to a curated reference dataset (df.Ref) containing validated peak assignments for the same biological sample. Use it to quantify top-K annotation performance (e.g., top-3 candidates) and verify that the pipeline achieves acceptable precision and recall before deploying it on new cohorts.

## When NOT to use

- The annotation workflow is still incomplete (e.g., clustering and filtering not yet applied)—evaluation requires fully prioritized results.
- No validated reference dataset exists for the sample—performance metrics cannot be computed without ground truth.
- Input is raw mass spectrometry data or a feature table before annotation—you need ranked candidates first.

## Inputs

- final ranked annotation table from mWISE.annotation wrapper (with candidate metabolites ordered by diffusion score)
- reference benchmark data frame (df.Ref) containing validated peak identities for the sample
- top.cmps parameter (integer: number of top candidates per peak to evaluate, e.g., 3)

## Outputs

- performance metrics table containing precision, recall, and F1-score
- per-peak evaluation results showing which reference peaks were recovered and which predictions were false positives

## How to apply

Execute the performanceEvaluation function on the final ranked annotation results, passing the benchmark reference data frame (df.Ref) and specifying the top.cmps argument to define how many top-ranked candidates per peak are considered correct. The function compares predicted annotations against reference peaks and computes three metrics: precision (fraction of predicted annotations matching reference), recall (fraction of reference peaks recovered by predictions), and F1-score (harmonic mean balancing precision and recall). Examine whether performance meets domain expectations—typically precision and recall both > 0.7 for metabolomics—before proceeding. If performance is poor, backtrack to the clustering or diffusion prioritization stages to adjust thresholds (e.g., frequency cutoffs, probability scoring parameters) and re-evaluate iteratively.

## Related tools

- **mWISE** (Provides the performanceEvaluation function and the complete annotation workflow context (matching, clustering, diffusion prioritization) whose output is evaluated) — https://dev.b2s.club/b2slab/mWISE
- **R** (Language and environment for executing performanceEvaluation and manipulating benchmark and result data frames)

## Examples

```
performanceEvaluation(results = finalAnnotations, df.Ref = df.Ref, top.cmps = 3)
```

## Evaluation signals

- Precision and recall values both lie in [0, 1] and sum-weighted averages are consistent with F1-score (harmonic mean).
- F1-score is ≥ 0.7 (typical threshold for acceptable metabolomics annotation quality) and does not degrade when top.cmps increases beyond optimal rank.
- Comparison of per-peak recovery: all reference peaks in df.Ref appear in the final ranked results, with no unexplained omissions.
- Precision does not decline unexpectedly as top.cmps increases, indicating stable candidate ranking and no artificial inflation from low-confidence predictions.
- Performance metrics are reproducible across multiple runs and are sensitive to changes in upstream parameters (e.g., diffusion input probability vs. binary scoring, cluster frequency thresholds).

## Limitations

- Performance depends critically on reference dataset quality and completeness; incomplete or noisy reference peaks (df.Ref) will inflate false-positive and false-negative rates.
- Evaluation is restricted to the top K candidates (top.cmps); if the true metabolite is ranked lower than K, it will not be counted as a recovery, even if present in the final results.
- Precision and recall metrics assume one-to-one matching between predicted and reference peaks; multi-annotation scenarios (one peak matching multiple metabolites, or vice versa) require post-hoc disambiguation logic.
- The Trypanosoma dataset used to demonstrate the skill is negative-mode LC-MS; performance on positive-mode or other ionization regimes may differ significantly.

## Evidence

- [other] The performanceEvaluation function computes performance metrics using the benchmark data frame df.Ref, with the top.cmps argument defining the top K candidates considered for the evaluation.: "The performanceEvaluation function computes performance metrics using the benchmark data frame df.Ref, with the top.cmps argument defining the top K candidates considered for the evaluation."
- [other] Evaluate annotation quality by computing top-3 performance metrics (precision, recall, F1-score) against df.Ref benchmark using performanceEvaluation function.: "Evaluate annotation quality by computing top-3 performance metrics (precision, recall, F1-score) against df.Ref benchmark using performanceEvaluation function."
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables through matching, clustering, filtering, and diffusion prioritization.: "mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii)"
- [intro] untargeted LC-MS data annotation is a major bottleneck in computational metabolomics that requires validation.: "Several computational strategies have been proposed to overcome untargeted LC-MS data annotation, which is still considered a major bottleneck."
