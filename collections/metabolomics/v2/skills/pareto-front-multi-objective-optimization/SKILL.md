---
name: pareto-front-multi-objective-optimization
description: Use when you have evaluated a parametric denoising strategy (e.g., frequency-based filtering) at multiple threshold values and computed two or more competing metrics (e.g., signal loss and noise reduction) for each threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rPref
  - DEoptim
  - dplyr
  - ggplot2
  - pbapply
  - magrittr
  - stats
  - data.table
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dures_cq
    doi: 10.1021/acs.analchem.5c01726
    title: DuReS
  dedup_kept_from: coll_dures_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01726
  all_source_dois:
  - 10.1021/acs.analchem.5c01726
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pareto-front-multi-objective-optimization

## Summary

Apply Pareto front analysis to identify optimal trade-offs between competing objectives (signal retention vs. noise reduction) across a parameter space, with differential evolution as a fallback when Pareto dominance is insufficient to select a single solution. This skill is essential when tuning frequency thresholds for MS/MS spectrum denoising where both false-positive and false-negative errors must be simultaneously minimized.

## When to use

Apply this skill when you have evaluated a parametric denoising strategy (e.g., frequency-based filtering) at multiple threshold values and computed two or more competing metrics (e.g., signal loss and noise reduction) for each threshold. The skill is triggered when no single threshold value dominates all others across all objectives—i.e., when trade-offs exist and a principled way to rank candidates by Pareto efficiency is needed to guide tuning.

## When NOT to use

- Single-objective optimization: if you need to optimize only one metric (e.g., maximize noise reduction without regard for signal loss), use univariate optimization or thresholding instead.
- Pre-defined threshold: if domain knowledge or prior validation has already fixed an optimal frequency threshold, skip Pareto analysis and apply that threshold directly.
- Sparse or unimodal search space: if one threshold clearly dominates all others across all metrics, Pareto analysis will return a trivial front; use simpler ranking methods instead.

## Inputs

- Denoised spectra generated across 101 frequency thresholds (0.00–1.00 in 0.01 increments)
- Dot product-based matching results and fragment match rates for all thresholded spectra vs. best reference spectrum
- Per-threshold signal reduction (loss of matched fragments) and noise reduction (reduction of unmatched fragments) metrics

## Outputs

- CSV files of all evaluated matches per feature in pareto_results/csv/
- Pareto front plots per feature in pareto_results/pdf/
- Summary dataframe with optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates, and selected features

## How to apply

First, compute signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each frequency threshold (0.00 to 1.00 in 0.01 increments, spanning 101 candidate values). Apply rPref Pareto front analysis to partition candidate thresholds into dominated and non-dominated sets; the Pareto front consists of all thresholds where no other threshold achieves better signal retention without sacrificing noise reduction, or vice versa. If the Pareto front remains ambiguous or too large, invoke DEoptim (differential evolution optimization) as a secondary step to identify a single point that optimizes a weighted combination or alternative criterion (e.g., maximum similarity score improvement). Filter the final set by requiring positive signal retention and improved similarity scores post-denoising. Output ranked thresholds, per-feature Pareto front plots, and a summary table linking each feature to its optimal threshold, signal/noise metrics, and matching scores before and after denoising.

## Related tools

- **rPref** (Pareto front identification: partitions candidate thresholds into dominated and non-dominated sets to identify Pareto-efficient frequency threshold values) — https://cran.r-project.org/web/packages/rPref/
- **DEoptim** (Secondary multi-objective optimization: differential evolution backup when Pareto front analysis does not uniquely identify an optimal threshold; selects single best threshold from front) — https://cran.r-project.org/web/packages/DEoptim/
- **ggplot2** (Visualization of Pareto front: generates per-feature 2D scatter plots showing trade-off between signal retention and noise reduction across frequency thresholds) — https://ggplot2.tidyverse.org/
- **dplyr** (Result wrangling: filters features by signal retention and similarity score improvement; merges metrics into summary table) — https://dplyr.tidyverse.org/
- **data.table** (High-performance storage and merging of matching results and signal/noise metrics across all 101 thresholds and multiple features) — https://rdatatable.gitlab.io/data.table/
- **pbapply** (Parallel iteration and progress reporting: applies threshold evaluation and metric computation across all features with progress bar) — https://cran.r-project.org/web/packages/pbapply/

## Examples

```
# After l5 (denoised spectra) and l6 (best-matching reference spectra) are generated:
# l6_tuning = reconstruct_sensitivity_tuning_module(l4, l5, l6, folder_path)
# This internally applies frequency thresholds 0.00–1.00, computes signal/noise metrics, runs rPref Pareto analysis, and outputs pareto_results/ with CSV and PDF summaries.
```

## Evaluation signals

- Pareto front size and composition: the front should contain fewer than ~20–30 non-dominated thresholds; if the entire 101-threshold set is non-dominated, the search space is too ambiguous or metrics are correlated.
- Threshold separation: selected optimal threshold (or thresholds) should lie within the Pareto front and not at the boundaries (0.00 or 1.00), indicating a genuine trade-off was identified.
- Metric improvement: all selected features in the output dataframe must show positive signal retention (fragments retained > 0) and improved similarity scores post-denoising compared to pre-denoising baseline.
- Per-feature reproducibility: Pareto plots should show clear separation of signal and noise reduction objectives; if all thresholds cluster in one region of the plot, the denoising effect is weak.
- DEoptim convergence (if used): if differential evolution is invoked, verify that its selected threshold aligns with or is near the highest-ranked Pareto front point, confirming secondary optimization is consistent with primary analysis.

## Limitations

- Trade-off sensitivity: Pareto optimality does not rank front members; if the front is large or contains many similar thresholds, DEoptim's weighting scheme must be specified a priori to break ties, risking arbitrary selection if weights are not empirically justified.
- Metric correlation: if signal retention and noise reduction are highly correlated (e.g., both improve monotonically with threshold), the Pareto front collapses to a single or few solutions, reducing the skill's utility.
- Feature heterogeneity: different features may have different optimal thresholds; the method returns per-feature solutions but does not automatically propagate a global threshold unless explicitly filtered or consensus is computed.
- Computational cost: evaluating 101 thresholds per feature with full spectral matching and Pareto analysis scales linearly with the number of features; large cohorts (>1000 features) may require subsetting or parallelization beyond pbapply.
- Parameter choice in DEoptim: if Pareto front is invoked as a backup, the objective function and bounds for differential evolution must be specified; the vignette does not provide explicit guidance on weighting competing metrics, potentially introducing subjectivity.

## Evidence

- [other] How can Pareto front analysis with DEoptim backup be used to systematically evaluate frequency thresholds and identify an optimal threshold value for fragment denoising?: "How can Pareto front analysis with DEoptim backup be used to systematically evaluate frequency thresholds and identify an optimal threshold value"
- [other] Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra: "Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra"
- [other] Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold.: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold"
- [other] Apply rPref Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across all features; use DEoptim as a backup optimization strategy if applicable.: "Apply rPref Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction; use DEoptim as a backup"
- [other] Generate CSV files of all evaluated matches in pareto_results/csv/ and Pareto front plots per feature in pareto_results/pdf/.: "Generate CSV files of all evaluated matches in pareto_results/csv/ and Pareto front plots per feature in pareto_results/pdf/"
- [readme] DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra.: "DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra"
