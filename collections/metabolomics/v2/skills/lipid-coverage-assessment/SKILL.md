---
name: lipid-coverage-assessment
description: Use when after hierarchical fragmentation library matching has produced candidate lipid annotations for a multi-species LC-MS/MS dataset, and you have applied retention time–based filtering rules (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - XCMS
  - CAMERA
  - LipidIN (Expeditious Querying module)
  - LipidIN (Lipid Categories Intelligence module)
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-coverage-assessment

## Summary

Quantify the breadth and accuracy of lipid annotations by aggregating relative retention time (RRT)–filtered predictions across species cohorts and computing false discovery rate (FDR) and unique lipid identifications. This skill validates whether a lipid annotation workflow achieves acceptable coverage and specificity before downstream biomarker discovery.

## When to use

After hierarchical fragmentation library matching has produced candidate lipid annotations for a multi-species LC-MS/MS dataset, and you have applied retention time–based filtering rules (e.g., the Lipid Categories Intelligence model's three RRT rules) to classify candidates as true or false positives. Use this skill when you need to report both the number of distinct lipids confidently identified and the estimated error rate (FDR) across your cohort, to decide whether the annotation depth is sufficient for your biological research goal.

## When NOT to use

- Input is unannotated raw LC-MS/MS data without prior spectral library matching; use the Expeditious Querying (EQ) module first.
- Retention time calibration or alignment across chromatographic runs has not been performed; RRT values will be unreliable.
- Single-species or single-sample dataset with insufficient cohort structure; the three RRT rules leverage cross-species retention time patterns and will lack discriminative power.

## Inputs

- Spectral query results (candidate lipid annotations from hierarchical fragmentation library matching, e.g., MS1 m/z and MS2 fragment matches)
- Relative retention time (RRT) values and retention time intervals for each candidate lipid, computed across species cohorts
- Preprocessed mass spectrometry data in mzML or .rda format with MS1 and MS2 peaks extracted and normalized

## Outputs

- Filtered lipid predictions table (CSV format) with assigned true/false positive classification
- False discovery rate (FDR) metric (percentage or ratio)
- Lipid coverage statistic (count of unique lipid identifications)
- Aggregated coverage and accuracy statistics per species (optional)

## How to apply

Load the filtered spectral query results (candidate annotations post-RRT rule application). Extract and compute retention time intervals for each lipid across the species cohorts represented in your dataset. Apply the three RRT rules from the Lipid Categories Intelligence model to classify candidates; the model uses primary retention time information to re-evaluate high-scoring spectral matches and reduce false positives. Aggregate all predictions across all species and samples. Calculate false discovery rate as the ratio of predictions failing validation checks to total predictions, and count the number of unique lipid identifications (coverage). Export the filtered lipid predictions with FDR and coverage statistics. The workflow is designed to yield a 5.7% estimated FDR on the order of 8923 lipids across various species when applied to hierarchical library matches.

## Related tools

- **XCMS** (Peak alignment, matching, and retention time calibration for LC-MS metabolite profiling prior to lipid annotation)
- **CAMERA** (Compound spectra extraction and annotation of LC-MS data to group related peaks before lipid library matching)
- **LipidIN (Expeditious Querying module)** (Primary spectral library matching against 168.6 million lipid fragmentation hierarchical library to generate candidate annotations for downstream RRT filtering) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN (Lipid Categories Intelligence module)** (Applies three relative retention time rules to filter and classify candidate lipid annotations as true or false positives) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source(paste(getwd(),'/LCI.r',sep='')); env <- new.env(); LCI('QC_POS1.rda')
```

## Evaluation signals

- False discovery rate is ≤ 5.7% (or within project-specific acceptance threshold), indicating acceptable specificity of retained annotations.
- Coverage (unique lipid count) is ≥ 8900 lipids when applied to multi-species cohorts similar in size to the LipidIN validation dataset; lower values may indicate insufficient data or overly stringent RRT rules.
- Lipid predictions are stable across reruns: identical FDR and coverage values when input data and RRT parameters are unchanged.
- Retained lipids show systematic retention time ordering consistent with lipid class and chain composition; lipids of the same class cluster at similar RTs.
- Manual spot-check of high-confidence predictions (top-ranked by spectral entropy or match score) confirms expected lipid structures and fragmentation patterns.

## Limitations

- RRT-based filtering assumes retention time reproducibility across samples and instruments; poor chromatographic alignment or drift will inflate FDR and reduce coverage.
- The three RRT rules are optimized for the lipid categories and chain compositions in the LipidIN hierarchical library; novel or uncommon lipid structures may not be well-represented.
- FDR is estimated and depends on the quality and diversity of the input spectral library matches; very low-quality spectra or limited library coverage will inflate the true error rate.
- Coverage metrics are biased toward lipid classes well-represented in the hierarchical library (e.g., phospholipids, glycerolipids); minor or oxidized lipids may be undercovered.
- Multi-threading environment concurrency issues have been reported in earlier versions of the LCI module; ensure use of a patched version (September 3, 2024 or later) for large-scale multi-file processing.

## Evidence

- [other] Can the Lipid Categories Intelligence model, using three relative retention time rules, predict unannotated lipids with a 5.7% estimated false discovery rate across multiple species?: "Can the Lipid Categories Intelligence model, using three relative retention time rules, predict unannotated lipids with a 5.7% estimated false discovery rate across multiple species?"
- [other] The Lipid Categories Intelligence model achieves prediction of unannotated lipids with a 5.7% estimated false discovery rate, covering 8923 lipids across various species.: "The Lipid Categories Intelligence model achieves prediction of unannotated lipids with a 5.7% estimated false discovery rate, covering 8923 lipids across various species."
- [other] Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives. Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications).: "Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence"
- [readme] The Lipid Categories Intelligence (LCI) Module: Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches.: "The Lipid Categories Intelligence (LCI) Module: Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to"
- [readme] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [readme] Fixed: (1) Update the LCI module to resolve the issue of file accessibility in a multitasking environment: "Fixed: (1) Update the LCI module to resolve the issue of file accessibility in a multitasking environment"
