---
name: spectral-peak-frequency-threshold-optimization
description: 'Use when you have MS/MS spectra with fragment frequency annotations (from consensus spectrum generation) and need to decide which fragments to retain versus remove. Trigger conditions: (1) you have replicate MS/MS spectra for the same feature with per-fragment recurrence frequencies calculated;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
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

# Spectral Peak Frequency Threshold Optimization

## Summary

Systematically identify the optimal frequency threshold for MS/MS fragment denoising by applying Pareto front analysis to evaluate trade-offs between signal retention and noise reduction across a range of threshold values. This skill determines which fragments to retain in tandem mass spectra based on their recurrence frequency across replicate spectra.

## When to use

Apply this skill when you have MS/MS spectra with fragment frequency annotations (from consensus spectrum generation) and need to decide which fragments to retain versus remove. Trigger conditions: (1) you have replicate MS/MS spectra for the same feature with per-fragment recurrence frequencies calculated; (2) you want to balance keeping authentic signal fragments while removing noise/artifacts; (3) you need a data-driven, reproducible threshold rather than a fixed default (e.g., the default 0.1 frequency threshold may not suit your experimental design or noise profile).

## When NOT to use

- Input lacks fragment recurrence frequency annotations or consensus spectrum data—this skill assumes frequencies have already been calculated in a prior aggregation step.
- You have only a single MS/MS spectrum per feature (no replicates)—Pareto optimization requires multiple threshold evaluations and comparative metrics across replicates.
- Your goal is to apply a fixed, pre-validated threshold uniformly across all features (e.g., 0.1 is known to be optimal for your instrumental setup)—use a simpler frequency filtering step instead of optimization.

## Inputs

- Annotated MS/MS spectra from replicate features (from label_individual_spectrum output, l4 in DuReS workflow)
- Best-matching reference spectrum identifier per feature (from prior spectral library matching, l6)
- Fragment frequency annotations (recurrence counts across replicate spectra)

## Outputs

- CSV files of all evaluated matches at each threshold (stored in pareto_results/csv/)
- Pareto front plots per feature (stored in pareto_results/pdf/)
- Summary table with optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match rates, and selected features
- Filtered dataframe of features with optimal thresholds and denoising improvements

## How to apply

Generate thresholded subspectra by applying frequency-based denoising at a range of threshold values (typically 101 values from 0.00 to 1.00 in 0.01 increments) to each matched feature's annotated MS/MS spectra. For each threshold, calculate two metrics: signal reduction (loss of matching fragments against the best reference spectrum) and noise reduction (reduction in unmatched fragments). Apply rPref package Pareto front analysis to identify the set of non-dominated thresholds that represent optimal trade-offs—thresholds where you cannot improve noise reduction without losing signal, or vice versa. Use DEoptim as a backup optimization method if Pareto analysis alone is insufficient to identify a single clear optimum. Filter features that show improved similarity scores post-denoising with positive signal retention, then compute percentage improvement. The optimal threshold is the one that maximizes the combined benefit (highest signal retention and noise reduction simultaneously, or ranked by domain-specific priority if multi-objective trade-offs exist).

## Related tools

- **rPref** (Performs Pareto front analysis to identify non-dominated frequency thresholds that represent optimal trade-offs between signal retention and noise reduction)
- **DEoptim** (Backup differential evolution optimization method used when Pareto front analysis is insufficient to identify a single optimal threshold)
- **dplyr** (Data frame manipulation and filtering of results across threshold evaluations)
- **ggplot2** (Visualization of Pareto front plots per feature showing trade-off between signal and noise reduction)
- **data.table** (Efficient storage and subsetting of large match result tables from all threshold iterations)
- **pbapply** (Parallel application of denoising and matching workflows across 101 threshold values and multiple features)

## Examples

```
# Reconstruct sensitivity/tuning module with Pareto front analysis (pseudocode from DuReS vignette): l6_tuning <- tune_frequency_threshold(l4, l6_best_matches, folder_path, thresholds = seq(0, 1, 0.01)); # Returns dataframe with optimal threshold, signal/noise metrics, and Pareto plots per feature
```

## Evaluation signals

- Pareto front is non-empty and contains at least one threshold with positive signal retention and noise reduction (no threshold should worsen both metrics).
- Summary output includes similarity scores before and after denoising; post-denoising similarity should be ≥ pre-denoising for selected features (or at minimum, show improved fragment matching ratio or reduced false-positive peaks).
- Signal reduction and noise reduction metrics are reported for the optimal threshold; noise reduction should be substantially greater than zero (e.g., >10% of unmatched fragments removed) while signal retention is high (e.g., <10% signal loss).
- CSV and PDF outputs are generated without errors; PDF Pareto plots clearly show the frontier of non-dominated points, with frequency threshold on one axis and combined signal/noise metrics on the other.
- Selected features pass the filtering criterion (improved similarity post-denoising with positive signal retention); percentage improvement statistic is computed and included in summary table.

## Limitations

- Pareto front analysis assumes that signal retention and noise reduction are two competing objectives; if your experimental design prioritizes one over the other, manual threshold selection post-Pareto may be necessary.
- DEoptim backup is stochastic and may not converge reproducibly on small datasets or with poor objective function definition; results should be validated on held-out test data.
- Fragment frequency thresholds are feature-specific; an optimal threshold for one compound may not generalize to others with different precursor m/z, ionization mode, or structural fragmentation patterns.
- The skill assumes that fragment frequency annotations are reliable; if consensus spectra are generated from too few replicates (e.g., <3), frequency estimates are noisy and optimal thresholds may be unstable.
- Computational cost scales with the number of thresholds evaluated (e.g., 101 thresholds × number of features × matching complexity); for large libraries, consider coarser threshold grids or parallel processing.

## Evidence

- [methods] Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra: "Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra"
- [methods] Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold"
- [methods] Apply rPref Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across all features; use DEoptim as a backup optimization strategy if applicable: "Apply rPref Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across all features; use DEoptim as a backup optimization strategy if applicable"
- [readme] DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra: "DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra"
- [methods] Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates: "Match all thresholded spectra against the best-matching reference spectrum (identified before denoising in l6) using dot product-based metrics and fragment match rates"
