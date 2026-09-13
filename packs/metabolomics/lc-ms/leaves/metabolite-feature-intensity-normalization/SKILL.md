---
name: metabolite-feature-intensity-normalization
description: Use when after imputation and batch-effect correction (OUKS steps 3–4)
  have been completed on your LC-MS feature-intensity table, and before statistical
  hypothesis testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS (Omics Untargeted Key Script)
  - MAI package
  - MetCorR
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-intensity-normalization

## Summary

Normalize feature-intensity tables from LC-MS untargeted metabolomics by applying Adaptive Box-Cox Transformation to each metabolite feature independently, stabilizing variance across the intensity range and adjusting for biological variation before downstream statistical analysis.

## When to use

After imputation and batch-effect correction (OUKS steps 3–4) have been completed on your LC-MS feature-intensity table, and before statistical hypothesis testing. Apply this skill when raw metabolite intensities show heteroscedastic variance (intensity-dependent variance) and you need to normalize the distribution of each feature toward normality to meet assumptions for parametric statistical tests on potential biomarkers.

## When NOT to use

- Input intensities already follow a normal distribution (visual inspection or Shapiro-Wilk test p > 0.05); transformation may degrade interpretability without benefit.
- Feature contains zero or negative intensities without prior log-shift; Box-Cox transformation requires strictly positive values.
- Downstream analysis uses non-parametric methods (e.g., Mann-Whitney U, Kruskal-Wallis, Spearman correlation) that do not assume normality; normalization is unnecessary.

## Inputs

- Feature-intensity table (CSV or R data frame): rows=samples, columns=metabolite features, values=raw LC-MS intensities (typically after imputation and batch correction)
- Metadata table identifying sample class and batch (optional, for stratified λ estimation)

## Outputs

- Normalized feature-intensity table: same dimensions as input, with Box-Cox transformed intensity values replacing raw values
- Box-Cox λ parameter estimates: one λ per feature, documenting the transformation applied to each column

## How to apply

Load the feature-intensity table (rows=samples, columns=metabolite features, values=raw intensities) into R ≥4.1.2. For each feature column independently, estimate the Box-Cox λ parameter from the empirical distribution of intensity values. Apply the Adaptive Box-Cox Transformation to that column using the estimated λ, replacing raw intensities with transformed values. The transformation stabilizes variance and normalizes the distribution without requiring a priori specification of λ. Output the normalized feature-intensity table with transformed values. Verify that post-normalization intensity distributions appear more symmetric and homoscedastic across the range of normalized values.

## Related tools

- **R** (Execution environment for Box-Cox transformation implementation and statistical analysis) — https://cloud.r-project.org/
- **OUKS (Omics Untargeted Key Script)** (Complete LC-MS metabolomics pipeline; step 7 implements Adaptive Box-Cox Transformation normalization) — https://github.com/plyush1993/OUKS
- **MAI package** (Handles missing value imputation upstream of normalization (OUKS step 3))
- **MetCorR** (Implements QC-based signal drift and batch effect correction upstream of normalization (OUKS step 4)) — https://github.com/plyush1993/MetCorR

## Examples

```
source('7. Normalization.R'); normalized_table <- apply(raw_intensity_table, 2, function(x) { lambda <- forecast::BoxCox.lambda(x); forecast::BoxCox(x, lambda) })
```

## Evaluation signals

- Histogram or Q-Q plot of normalized feature intensities shows approximately symmetric, bell-shaped distribution (visual normality check) compared to right-skewed raw intensities.
- Shapiro-Wilk test p-value on normalized feature intensities > 0.05 indicates normality; compare to raw intensities.
- Variance homogeneity across intensity quartiles (Levene's test or Breusch-Pagan test) improves post-normalization compared to pre-normalization.
- Box-Cox λ estimates cluster around expected range (λ ≈ 0–1 for log-like transformations, λ ≈ 0.5 for square-root-like) and are stable across replicate samples of the same class.
- Downstream statistical tests (e.g., t-test, linear regression on biomarker discovery) report improved p-value distributions and fewer violations of normality assumptions.

## Limitations

- Box-Cox transformation is undefined for zero or negative intensities; missing values must be imputed and all values must be strictly positive (apply log-shift if necessary).
- Adaptive λ estimation is sensitive to outliers in the intensity distribution; outlier imputation or removal before normalization may be required.
- Transformation interpretability is reduced compared to raw intensities; effect sizes and fold-changes on normalized scale do not directly translate to original intensity units.
- No documentation provided on parameter selection criteria, sensitivity analysis, or guidance for tuning λ estimation (e.g., per-class vs. global λ, robust vs. maximum-likelihood estimation).
- Project OUKS is marked as inactive (no longer actively developed); maintenance and support are limited.

## Evidence

- [other] Adaptive Box-Cox Transformation normalization module in OUKS step 7 transforms feature-intensity tables into normalized values: "OUKS step 7 implements Adaptive Box-Cox Transformation normalization to normalize feature-intensity tables."
- [other] Step 7 workflow: load feature-intensity table, apply Adaptive Box-Cox per feature, output normalized values: "Load the feature-intensity table (rows: samples, columns: metabolite features, values: raw intensities) into R. 2. Apply the Adaptive Box-Cox Transformation to each feature column independently,"
- [readme] Normalization is step 7 of nine-step LC-MS profiling pipeline following imputation and correction: "comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox"
- [readme] R ≥4.1.2 is required to run OUKS normalization scripts: "The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), RStudio and R (≥ 4.1.2)."
- [readme] MetCorR provides QC-based drift correction preceding normalization: "# MetCorR - QC-based metabolomics LC-MS signal drift correction using GAMs"
