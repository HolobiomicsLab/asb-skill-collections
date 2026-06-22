---
name: sensitivity-threshold-stability-assessment
description: 'Use when you have labeled MS/MS spectra from replicate measurements and need to determine a frequency threshold for denoising that balances competing objectives: retaining true fragment signals while removing noise.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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
---

# sensitivity-threshold-stability-assessment

## Summary

This skill systematically evaluates the stability and robustness of a frequency threshold parameter across a spectrum of values (0.00–1.00 in 0.01 increments) using Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction in tandem mass spectrometry spectra. It combines multi-objective optimization with statistical significance testing to pinpoint threshold values that maximize denoising performance while minimizing signal loss.

## When to use

Apply this skill when you have labeled MS/MS spectra from replicate measurements and need to determine a frequency threshold for denoising that balances competing objectives: retaining true fragment signals while removing noise. Use it particularly when your denoising pipeline produces variable results across features or when domain knowledge does not clearly prescribe a single optimal threshold value. This skill is essential before applying a fixed frequency threshold in production denoising workflows.

## When NOT to use

- When a frequency threshold is already fixed by prior validation or domain standards (e.g., previous metabolomics cohort analysis)
- When replicate spectra are absent or too few (<3 replicates per feature) to establish reliable frequency distributions
- When input spectra have already been denoised or filtered by other pipelines, making signal/noise trade-off assessment invalid

## Inputs

- labeled MS/MS spectra per feature (from label_individual_spectrum output, l4)
- best-matching reference spectra for each feature (identified before denoising, l6)
- annotated fragment frequencies from consensus spectra (l3)
- feature metadata (feature ID, m/z, RT, ion mode)

## Outputs

- Pareto front analysis results: CSV files of all evaluated matches (threshold vs. signal/noise metrics)
- Pareto front plots per feature (PDF)
- Summary table with per-feature optimal frequency threshold, matching scores before/after denoising, signal reduction, noise reduction, fragment match rates
- Filtered dataframe containing features with improved similarity and selected optimal thresholds
- Percentage improvement metrics for post-denoising performance

## How to apply

Iterate over each matched feature and its annotated MS/MS spectra. Apply frequency-based denoising at 101 discrete threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra. Re-match all thresholded spectra against their best-matching reference spectrum (identified before denoising) using dot product-based metrics and fragment match rates. For each threshold, calculate two opposing metrics: signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments). Apply Pareto front analysis using rPref to identify the set of non-dominated solutions—thresholds where you cannot improve noise reduction without degrading signal retention—and use DEoptim as a backup optimization method if Pareto analysis identifies multiple equally valid solutions. Filter features showing improved similarity scores post-denoising with positive signal retention. Generate Pareto front plots per feature and compute percentage improvement metrics. The optimal threshold is typically one on the Pareto frontier that maximizes the combination of signal-to-noise improvement while maintaining acceptable fragment match counts.

## Related tools

- **rPref** (Multi-objective preference-based optimization to identify Pareto front solutions (non-dominated trade-offs between signal retention and noise reduction))
- **DEoptim** (Differential evolution optimization as backup method when Pareto front analysis does not uniquely determine optimal threshold)
- **dplyr** (Data manipulation and filtering of matches and metrics across threshold values)
- **ggplot2** (Visualization of Pareto front curves and signal/noise trade-off landscapes per feature)
- **pbapply** (Parallel iteration over features and thresholds with progress bar for large datasets)
- **data.table** (Efficient tabular storage and aggregation of threshold evaluation results)
- **stats** (Statistical summaries of signal/noise metrics across thresholds)

## Examples

```
l6 <- reconstruct_sensitivity_module(l5, l4, l3, folder_path = folder_path, ion_mode = 'pos')
```

## Evaluation signals

- Pareto front is non-empty and contains ≥1 threshold solution where no single threshold dominates all others on both signal retention and noise reduction
- Selected optimal threshold lies on the Pareto frontier and exhibits positive signal retention (>0) and quantifiable noise reduction compared to unthresholded baseline
- Similarity scores (dot product or matching score) improve post-denoising at the selected threshold relative to pre-denoising spectra for >50% of features
- Fragment match rates remain stable or improve at optimal threshold (no precipitous drop in matched fragment counts)
- Percentage improvement metric (calculated as relative gain in similarity score post-denoising) is positive and consistent across features with similar spectral complexity

## Limitations

- Pareto front analysis requires replicate spectra per feature; sparse replicates (<3) may yield unstable or uninformative trade-off curves.
- The 101-threshold grid (0.00–1.00 in 0.01 increments) is discrete; very fine-grained threshold optimization may require finer granularity or continuous methods.
- Optimal threshold may vary substantially between ionization modes or compound classes; a single global threshold may not be universally optimal across heterogeneous metabolomics datasets.
- Wilcoxon rank-sum tests used for significance assessment assume independent threshold evaluations; multiple comparisons correction may be needed when reporting p-values across all 101 thresholds.
- DEoptim backup optimization may be slow or diverge if the objective function (signal/noise trade-off surface) is multimodal or noisy.

## Evidence

- [methods] Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments): "Apply frequency-based denoising at 101 threshold values (0.00 to 1.00 in 0.01 increments) to generate thresholded subspectra"
- [methods] Calculate signal reduction and noise reduction for each threshold: "Calculate signal reduction (loss in matching fragments) and noise reduction (reduction in unmatched fragments) for each threshold."
- [methods] Apply rPref Pareto front analysis with DEoptim as backup: "Apply rPref Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction across all features; use DEoptim as a backup optimization strategy if applicable."
- [methods] Filter features showing improved similarity scores post-denoising: "Filter features showing improved similarity scores post-denoising with positive signal retention and compute percentage improvement."
- [methods] Generate CSV and PDF outputs of Pareto front results: "Generate CSV files of all evaluated matches in pareto_results/csv/ and Pareto front plots per feature in pareto_results/pdf/."
- [methods] Output summary with optimal threshold and denoising metrics: "Merge results into a summary table and return a filtered dataframe containing optimal frequency threshold, matching scores before/after denoising, signal/noise reduction metrics, fragment match"
- [readme] Pareto front analysis identifies optimal trade-offs: "Applies **Pareto front analysis** to identify optimal trade-offs between signal retention and noise reduction"
