---
name: metabolite-phenotype-association-partial-correlation
description: Use when you have a SummarizedExperiment object containing NMR or MS metabolomic data with aligned phenotype information (BMI, disease status, age, gender), and you need to identify metabolites associated with a continuous or categorical outcome while controlling for known confounders that might.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3676
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3407
  tools:
  - MWASTools
  - R
  - Bioconductor
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
---

# metabolite-phenotype-association-partial-correlation

## Summary

Compute partial Spearman correlations between metabolic features and a phenotype of interest while simultaneously adjusting for epidemiological confounders (age, gender, disease status). This generates metabolome-wide association estimates, raw p-values, and multiple-testing corrected p-values suitable for hypothesis testing in metabolomic cohorts.

## When to use

You have a SummarizedExperiment object containing NMR or MS metabolomic data with aligned phenotype information (BMI, disease status, age, gender), and you need to identify metabolites associated with a continuous or categorical outcome while controlling for known confounders that might distort the observed associations.

## When NOT to use

- You have already computed univariate metabolite associations without confounder adjustment; partial correlation adds computational cost when confounding is negligible.
- Your phenotype data is missing confounder values for a large fraction of samples; partial correlation requires complete cases for all variables.
- Your outcome is binary and sample counts are extremely imbalanced; generalized linear models (logistic regression) may be more appropriate than Spearman correlation.

## Inputs

- SummarizedExperiment object with metabolomic data (rows=metabolic features, columns=samples)
- Phenotype data frame with outcome variable and confounder columns (age, gender, disease status)
- Cross-validation filter metadata (CV assignments)

## Outputs

- MWAS_BMI matrix: 3-column data frame with metabolite identifiers (ppm) as row names
- Column 1: r (Spearman partial correlation coefficient)
- Column 2: p (raw p-value from partial correlation test)
- Column 3: pFDR (Benjamini-Hochberg corrected p-value)

## How to apply

Load the cross-validated metabolomic SummarizedExperiment object and ensure the phenotype slot contains the outcome variable (e.g., BMI) and all confounders (age, gender, T2D status). Apply the MWAS_stats function from MWASTools with disease_id set to your outcome, specify confounders as a list, and set correlation method to 'Spearman'. The function computes partial correlations for each metabolite against the outcome, adjusting for confounders simultaneously, then calculates raw p-values from the partial correlation test statistics. Apply Benjamini-Hochberg correction to generate false discovery rate–adjusted p-values (pFDR). Assemble results into a three-column matrix with metabolite identifiers (ppm values) as row names and columns for correlation coefficient (r), raw p-value (p), and BH-corrected p-value (pFDR).

## Related tools

- **MWASTools** (R package providing MWAS_stats function to compute partial correlations and p-values with confounder adjustment) — github.com/AndreaRMICL/MWASTools
- **R** (Statistical computing environment; required version ≥3.3)
- **Bioconductor** (Infrastructure for SummarizedExperiment object classes and statistical methods)

## Examples

```
MWAS_stats(metabo_SE, disease_id='BMI', confounder=c('Age','Gender','T2D'), corr_method='Spearman')
```

## Evaluation signals

- Output matrix has exactly 3 columns (r, p, pFDR) with row names matching metabolite identifiers from input SummarizedExperiment
- Raw p-values are uniformly distributed on [0,1] under null hypothesis; pFDR values are ≥ corresponding raw p-values
- Number of rows equals number of metabolic features in input; no metabolites are dropped unless filtered by prior QC
- pFDR values satisfy monotonicity: features ranked by raw p-value also rank identically by pFDR
- Partial correlation coefficients r lie in [-1, 1] range; magnitude should reflect biological signal after confounder removal

## Limitations

- Assumes linearity of relationships between metabolites, outcome, and confounders; non-linear associations may be missed.
- Spearman correlation is non-parametric but less efficient than Pearson if data are jointly normal; choose based on NMR spectral preprocessing and normality assessment.
- Multiple testing correction (Benjamini-Hochberg) controls false discovery rate but not family-wise error; at FDR threshold α=0.05 expect ~5% of significant findings to be false positives.
- Requires complete case deletion if confounders are missing; large amounts of missing confounder data may substantially reduce effective sample size.
- Confounder specification is user-determined; omitting true confounders or including colliders can bias estimates or inflate type I error.

## Evidence

- [other] metabolite-phenotype-association-partial-correlation via partial Spearman correlations: "Reproduce the BMI metabolome-wide association matrix (MWAS_BMI) via partial Spearman correlations"
- [intro] confounder adjustment in MWAS: "a major limitation of these multivariate models from the epidemiological perspective is that they do not properly account for cofounding factors (e.g. age, gender), which might distort the observed"
- [intro] partial correlation and GLM methods: "metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders"
- [intro] MWASTools MWAS_stats function: "we present a package to perform MWAS using univariate hypothesis testing with efficient handling of epidemiological confounders"
- [other] output format: r, p, pFDR columns: "MWAS_BMI is a 3-column matrix containing metabolic features (ppm values) in rows with columns for estimates (r coefficients), raw p-values, and BH-corrected p-values (pFDR)"
- [other] Benjamini-Hochberg multiple testing correction: "Apply Benjamini-Hochberg correction to generate adjusted p-values (pFDR)"
