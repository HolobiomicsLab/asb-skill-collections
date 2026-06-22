---
name: fragment-frequency-threshold-optimization
description: Use when you have replicate MS/MS spectra with labeled fragment recurrence frequencies and need to select an optimal frequency threshold (beyond the default 0.1) that maximizes spectral quality metrics while minimizing false positive noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - readr
  - dplyr
  - magrittr
  - pbapply
  - rPref
  - stats (Wilcoxon rank-sum test)
  - generate_denoised_spectra
  - Spectra
  - ggplot2
  - patchwork
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01726
  title: DuReS
evidence_spans:
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra"
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim", "patchwork", "S4Vectors", "Spectra", "BiocManager", "knitr", "markdown"),
- invisible(lapply(c("dplyr", "readr", "data.table", "pbapply", "magrittr", "utils", "stats", "rPref", "ggplot2", "DEoptim"
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

# fragment-frequency-threshold-optimization

## Summary

Optimize the frequency cutoff threshold applied during MS/MS spectrum denoising to balance signal retention and noise reduction. This skill determines the minimal recurrence frequency at which fragment ions should be retained in consensus spectra, using statistical and Pareto front analysis methods.

## When to use

Apply this skill when you have replicate MS/MS spectra with labeled fragment recurrence frequencies and need to select an optimal frequency threshold (beyond the default 0.1) that maximizes spectral quality metrics while minimizing false positive noise. Use it before the final generate_denoised_spectra step when tuning denoising performance for a new dataset or experimental condition.

## When NOT to use

- Input spectra do not have replicate measurements or fragment recurrence frequencies are not computed (l3/l4 outputs not available).
- The dataset is already heavily curated or manually verified and a standard frequency threshold (e.g., default 0.1) is acceptable.
- Computational resources are severely limited; performing a parameter sweep with Wilcoxon tests and Pareto analysis may be prohibitive for very large datasets.

## Inputs

- Labeled spectrum object (l4) with fragment recurrence frequencies
- Feature list with precursor m/z and RT annotations
- mzML files containing replicate MS/MS spectra
- Reference spectral library (library_positive.rds or library_negative.rds)

## Outputs

- Optimal frequency threshold value (numeric, typically 0.05–0.95)
- Pareto front analysis plot showing trade-offs between metrics
- Wilcoxon test results table (p-values for each threshold)
- Quality metric profiles (dot products, fragment counts, match scores) across thresholds
- Denoised mzML files generated using the optimal threshold

## How to apply

Conduct a parameter sweep across a range of frequency thresholds (e.g., 0.05–0.95 in increments of 0.05) on a representative subset of features. For each threshold, apply generate_denoised_spectra and compute quality metrics such as spectral match scores, fragment matching ratios, and metadata consistency. Identify the Pareto front of trade-offs between signal retention and noise reduction using rPref. Apply Wilcoxon rank-sum tests at each frequency relative to the optimal frequency to assess statistical significance of metric changes. Select the threshold that minimizes noise while maintaining signal fidelity, typically balancing forward/reverse dot products (>0.25 threshold) and matching fragment count (≥2 fragments). Verify the choice by checking that annotation consistency across replicate spectra reaches ≥30% and that the number of high-confidence matches increases relative to adjacent thresholds.

## Related tools

- **rPref** (Pareto front analysis to identify optimal trade-offs between signal retention and noise reduction metrics)
- **stats (Wilcoxon rank-sum test)** (Statistical significance testing of metric changes at each frequency threshold compared to optimal frequency)
- **generate_denoised_spectra** (Apply candidate frequency thresholds to produce denoised spectra for quality evaluation) — https://github.com/BiosystemEngineeringLab-IITB/dures
- **Spectra** (Store, access, and manipulate MS/MS spectral data during threshold evaluation)
- **ggplot2** (Visualize Pareto fronts, quality metric profiles, and statistical test results)
- **patchwork** (Combine multiple visualization panels for threshold tuning results)

## Examples

```
# R example using DuReS vignette workflow; tune optimal frequency threshold
l4 = label_individual_spectrum(l3, folder_path, 0.05)
# Sweep frequency thresholds 0.05–0.95 and evaluate quality metrics with rPref Pareto front
freq_sweep <- seq(0.05, 0.95, by=0.05); pareto_results <- lapply(freq_sweep, function(f) { l5_candidate <- generate_denoised_spectra(l4, folder_path, custom_threshold=f, ion_mode="pos"); compute_quality_metrics(l5_candidate, library_positive) })
# Identify Pareto front and optimal threshold using rPref package
```

## Evaluation signals

- Pareto front plot shows a clear trade-off curve with the selected threshold at a non-dominated point.
- Wilcoxon rank-sum test p-value at the optimal threshold is significantly lower (p < 0.05) than adjacent thresholds, indicating a local optimum.
- Denoised spectra from the optimal threshold yield ≥30% annotation consistency across replicate measurements, with forward/reverse dot products >0.25 and ≥2 matching fragments per annotation.
- Quality metrics (e.g., spectral match scores, fragment matching ratios) plateau or decline beyond the optimal threshold, confirming diminishing returns.
- Fragment reduction from original to denoised spectra is consistent with expectations; e.g., reduction from 98 to 81 fragments after grouping and from 81 to ~9–40 fragments after thresholding, proportional to the selected threshold value.

## Limitations

- Optimal threshold is dataset-specific and sample-dependent; results may not generalize across different ionization modes, metabolite classes, or MS instruments without re-tuning.
- Wilcoxon tests assume independent samples; replicate spectra from the same feature may violate independence assumptions, potentially inflating or deflating significance estimates.
- Pareto front analysis requires computation of multiple quality metrics across many features, which is time-intensive for large datasets (>10,000 features).
- The choice of frequency increment (e.g., 0.05 vs. 0.01) and the set of quality metrics included in the trade-off analysis can influence the identified optimal threshold; sensitivity analysis is recommended.
- Threshold optimization is most robust when applied to features with ≥20–30 replicate spectra; features with few replicates may yield unstable or unreliable frequency estimates.

## Evidence

- [other] Applies **Pareto front analysis** to identify optimal trade-offs between signal retention and noise reduction: "Applies **Pareto front analysis** to identify optimal trade-offs between signal retention and noise reduction"
- [other] Performs **Wilcoxon rank-sum tests** to assess significance of metric changes at each frequency compared to the optimal frequency: "Performs **Wilcoxon rank-sum tests** to assess significance of metric changes at each frequency compared to the optimal frequency"
- [other] Applies a user-defined frequency threshold (default = `0.1`) to retain **signal fragments**: "Applies a user-defined frequency threshold (default = `0.1`) to retain **signal fragments**"
- [readme] DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra.: "DuReS provides users with the ability to determine the optimal frequency cutoff for denoising MS/MS spectra."
- [readme] Annotations must occur in **≥30%** of replicate spectra: "Annotations must occur in **≥30%** of replicate spectra"
- [readme] Matches with fewer than **2 fragments** or **dot products < 0.25** are filtered out: "Matches with fewer than **2 fragments** or **dot products < 0.25** are filtered out"
