---
name: peak-intensity-normalization-method-selection
description: Use when after peak filtering (by m/z, isotopic presence, formula assignment error, and sample prevalence) and before multivariate analysis (PCA, NMDS, PERMANOVA) when comparing peak abundance patterns across samples with potential differences in ionization efficiency, ion suppression, or total ion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0592
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MetaboDirect
  - Python 3.8
  - R 4.0.2
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - vegan
  - SYNCSA
  - pmartR
  - statsmodels
  - Formularity
  - SPANS
  - pmartR (R package)
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
- It requires the Python dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# peak-intensity-normalization-method-selection

## Summary

Selection and application of appropriate peak-intensity normalization methods for FT-ICR MS datasets to correct for systematic bias and enable valid multivariate statistical comparison across samples. This skill ensures that downstream chemodiversity and ordination analyses reflect true biochemical differences rather than technical artifacts.

## When to use

After peak filtering (by m/z, isotopic presence, formula assignment error, and sample prevalence) and before multivariate analysis (PCA, NMDS, PERMANOVA) when comparing peak abundance patterns across samples with potential differences in ionization efficiency, ion suppression, or total ion current. Use this skill when the same molecular formulas appear across multiple samples but with variable detected intensities that may reflect technical rather than biological variation.

## When NOT to use

- Input is already a distance matrix (e.g., Bray-Curtis, Euclidean) — normalization applies only to raw or semi-processed abundance tables.
- Analysis goal is solely univariate (e.g., fold-change in a single molecular formula between two groups) — normalization is most critical for multivariate statistics.
- Raw FT-ICR MS spectra have not yet undergone signal processing and molecular formula assignment — normalization assumes post-assignment peak abundance data.
- Data are already processed by external preprocessing software (e.g., CoreMS, Formularity) with unclear or undocumented normalization — double normalization can introduce artifacts.

## Inputs

- Peak abundance matrix (samples × molecular formulas) after filtering by m/z, isotopic presence, formula assignment error (≤0.5 ppm), and sample prevalence thresholds
- Compound class assignments for each molecular formula
- Sample metadata (experimental conditions, batch information if applicable)

## Outputs

- Normalized peak intensity matrix (samples × molecular formulas) ready for PCA, NMDS, and PERMANOVA
- Documentation of normalization method selected and parameters applied
- Optional: transformed intensity values (log-scale or other) if requested by downstream analysis

## How to apply

Within the MetaboDirect pipeline, peak intensity normalization is performed as a dedicated step after compound class determination and before ordination and statistical testing. The article indicates that 'peak intensities are normalized in this step' but does not specify which single method is mandatory; the choice depends on the nature of your data and analysis goal. Common approaches in the R environment (via vegan and pmartR packages) include total-sum normalization (dividing each sample's peak intensities by the sample total), log transformation (to stabilize variance), or quantile normalization (to align intensity distributions). Document which method was selected and justify it based on whether your goal is to preserve relative abundance relationships, correct for ion suppression effects, or meet assumptions of downstream statistical tests (e.g., PERMANOVA assumes homogeneous multivariate variance). Apply the selected normalization uniformly across all samples before passing the normalized matrix to ordination and significance testing functions.

## Related tools

- **vegan** (R package providing multivariate analysis and ordination functions (NMDS, PCA, PERMANOVA) that operate on normalized intensity matrices)
- **pmartR** (R package for normalization tests to evaluate and select appropriate normalization methods for mass spectrometry data)
- **MetaboDirect** (Command-line pipeline that integrates peak intensity normalization as step (ii) of its six-step analytical workflow, before multivariate statistics) — https://github.com/Coayala/MetaboDirect
- **statsmodels** (Python library used within MetaboDirect for statistical tests and transformations that may be applied during or after normalization)

## Examples

```
metabodirect -i peak_abundance.csv -f molecular_formulas.csv -m normalized -o ./output_dir
```

## Evaluation signals

- Normalized peak intensity matrix has no missing values and all sample totals or distributions are comparable across samples (check histogram or boxplot of per-sample sums or quantiles).
- Downstream ordination (NMDS, PCA) separates samples by experimental treatment or biological condition as expected; ordination stress is <0.2 (good fit) and explained variance aligns with published benchmarks for similar datasets.
- PERMANOVA on normalized data yields statistically significant differences (p<0.05) between treatment groups if the biological hypothesis predicts they should differ; effect sizes (R²) are consistent with literature or prior analysis.
- Reproducibility check: applying the same normalization method to the same dataset (e.g., bacterium-phage with 36 samples) produces identical numerical results and identical downstream figures (Van Krevelen diagrams, elemental composition plots).
- No systematic bias remains: if samples are from the same biological condition, principal components or NMDS axes should not cluster them by technical covariates (e.g., batch, run order, total ion current).

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; normalization assumes input peak abundance and molecular formula data are already generated by external signal processing software (e.g., CoreMS, Formularity), introducing dependency on upstream quality.
- The article does not specify a single mandatory normalization method, leaving practitioners to select from common approaches (total-sum, log, quantile, or others); this flexibility increases reproducibility risk if the choice is not documented.
- Peak intensity normalization does not address ion suppression or signal enhancement effects that occur during mass spectrometry analysis itself — these confound downstream interpretation even after normalization.
- Normalization is sensitive to outlier samples with extremely high or low total ion current; robust methods (e.g., quantile or geometric mean normalization) may be needed but are not explicitly discussed in the article.

## Evidence

- [methods] peak intensities are normalized in this step: "peak intensities are normalized in this step"
- [methods] permutational analysis of variance (PERMANOVA), non-metric multidimensional scaling (NMDS), and Principal Component Analysis (PCA): "permutational analysis of variance (PERMANOVA), non-metric multidimensional scaling (NMDS), and Principal Component Analysis (PCA)"
- [methods] MetaboDirect pipeline consists of six main steps: "data pre-processing (i) data diagnostics (ii) data exploration (iii) chemodiversity analysis (iv)"
- [intro] signal suppression or enhancement that can confound downstream data analysis: "signal suppression or enhancement that can confound downstream data analysis due to ion suppression"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] pmartR (for normalization tests): "pmartR (for normalization tests)"
