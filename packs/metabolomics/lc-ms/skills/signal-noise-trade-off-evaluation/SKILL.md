---
name: signal-noise-trade-off-evaluation
description: 'Use when after generating consensus spectra with fragment recurrence frequencies, when you have replicate MS/MS spectra for features and need to choose a single frequency cutoff for denoising. Triggers include: (1) uncertainty about which frequency threshold to apply across all features;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3520
  tools:
  - rPref
  - DEoptim
  - dplyr
  - ggplot2
  - pbapply
  - magrittr
  - stats
  - data.table
  techniques:
  - LC-MS
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

# signal-noise-trade-off-evaluation

## Summary

Systematic evaluation of frequency thresholds for MS/MS spectrum denoising using Pareto front analysis to identify optimal trade-offs between signal retention (matched fragments preserved) and noise reduction (unmatched fragments removed). Applied after consensus spectrum generation to select a single frequency threshold that maximizes annotation quality without excessive signal loss.

## When to use

After generating consensus spectra with fragment recurrence frequencies, when you have replicate MS/MS spectra for features and need to choose a single frequency cutoff for denoising. Triggers include: (1) uncertainty about which frequency threshold to apply across all features; (2) requirement to quantify signal loss vs. noise reduction trade-offs; (3) need for objective, data-driven threshold selection rather than manual parameter choice.

## When NOT to use

- Input spectra do not have replicate MS/MS data — Pareto trade-off analysis requires variation across replicates to evaluate noise reduction meaningfully.
- Single-spectrum features or already pre-selected features — the skill requires a pool of candidate thresholds and multiple feature-spectrum pairings to construct meaningful trade-off surfaces.
- Denoising parameter is already fixed by protocol or prior publication — this skill is meant to derive optimal threshold systematically rather than validate a predetermined cutoff.

## Inputs

- List of matched features with annotated MS/MS spectra (l4 output from DuReS)
- Best-matching reference spectra per feature (from l6 spectral matching)
- Consensus spectrum fragment recurrence frequencies
- Replicate MS/MS spectra organized by feature

## Outputs

- CSV files of all evaluated threshold-feature combinations (pareto_results/csv/)
- Pareto front plots per feature (pareto_results/pdf/)
- Summary dataframe with optimal frequency threshold, dot products before/after denoising, signal retention %, noise reduction %, fragment match rates, and feature IDs
- Filtered feature set meeting positive signal retention and improved similarity criteria

## How to apply

For each matched feature, retrieve its annotated MS/MS spectra and apply frequency-based denoising across a range of 101 threshold values (0.00 to 1.00 in 0.01 increments). For each thresholded subspectra, re-match against the best-matching reference spectrum using dot product and fragment match rate metrics. Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) per threshold. Apply rPref Pareto front analysis to identify the set of non-dominated thresholds that represent optimal trade-offs; use DEoptim as a backup optimization method if Pareto analysis is insufficient. Filter features showing improved similarity scores post-denoising with positive signal retention. Generate CSV results and Pareto front plots per feature. Merge results into a summary table reporting optimal threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates, and selected features.

## Related tools

- **rPref** (Pareto front identification: identifies non-dominated threshold values that represent optimal signal-noise trade-offs across all features)
- **DEoptim** (Backup multi-objective optimization: differential evolution-based threshold optimization when rPref Pareto analysis is insufficient or requires validation)
- **dplyr** (Data manipulation and filtering: filters features by signal retention thresholds, merges results into summary tables)
- **ggplot2** (Visualization: generates Pareto front plots per feature showing signal vs. noise reduction trade-offs)
- **data.table** (High-performance tabular data processing: handles large matched spectra results and threshold evaluation tables)
- **pbapply** (Parallel application with progress tracking: iterates denoising evaluation across 101 thresholds per feature efficiently)
- **stats** (Statistical filtering: computes signal reduction, noise reduction, and retention metrics)

## Examples

```
# After l4 (labeled spectra) and l6 (reference matching), run sensitivity analysis:
l6_tuned <- reconstruct_sensitivity_tuning_module(
  l4_spectra = l4,
  l6_reference_matches = l6,
  threshold_range = seq(0.00, 1.00, by=0.01),
  output_dir = "pareto_results/",
  pareto_method = "rPref",
  backup_optim = "DEoptim"
)
# Returns: summary table with optimal_threshold, dot_product_before, dot_product_after, signal_reduction, noise_reduction per feature
```

## Evaluation signals

- Pareto front is non-empty and contains ≥1 threshold value; plot shows clear trade-off curve between signal retention and noise reduction axes.
- Optimal selected threshold improves dot product similarity score relative to undenoised spectra while maintaining ≥0 signal retention (no net loss of matched fragments).
- Summary table contains all 101 evaluated thresholds per feature with monotonic signal reduction and noise reduction metrics across threshold range.
- Filtered feature set (post-denoising) shows ≥1% median improvement in matching scores and fragment match rate relative to before denoising.
- CSV files and PDF plots are generated with consistent ordering and no missing threshold evaluations.

## Limitations

- Pareto front analysis assumes features share a common optimal threshold; heterogeneous feature sets may require per-feature or per-class threshold tuning.
- Trade-off evaluation is relative to the best-matching reference spectrum identified before denoising; circular reference-matching after threshold selection is not supported in the current workflow.
- DEoptim backup requires explicit specification of optimization objective; if Pareto front is large or ambiguous, automated threshold selection may not be reproducible.
- Evaluation is computationally expensive (101 threshold × number of features × re-matching step); runtime scales with spectrum count and complexity of reference library.

## Evidence

- [other] The sensitivity analysis module applies Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across frequency thresholds: "sensitivity analysis module applies Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across frequency thresholds, with DEoptim as a backup"
- [other] Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments): "Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra"
- [other] Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold.: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold"
- [readme] Pareto front analysis identifies optimal trade-offs between signal retention and noise reduction: "Applies **Pareto front analysis** to identify optimal trade-offs between signal retention and noise reduction"
- [other] Merge results into a summary table and return a filtered dataframe containing optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics: "Merge results into a summary table and return a filtered dataframe containing optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates"
