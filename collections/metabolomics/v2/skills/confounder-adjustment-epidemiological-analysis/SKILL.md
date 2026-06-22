---
name: confounder-adjustment-epidemiological-analysis
description: Use when when testing associations between metabolic features (from NMR or MS) and a phenotype of interest (e.g., BMI, disease status) in a cohort where age, gender, or clinical confounders are known to correlate with both the metabolite and phenotype.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2269
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

# confounder-adjustment-epidemiological-analysis

## Summary

Adjust metabolite–phenotype associations for epidemiological confounders (age, gender, disease status) using partial correlations or generalized linear models to isolate true disease signals and prevent confounding bias. This is essential in metabolome-wide association studies (MWAS) where multivariate models alone fail to properly account for cofounding factors that distort observed associations.

## When to use

When testing associations between metabolic features (from NMR or MS) and a phenotype of interest (e.g., BMI, disease status) in a cohort where age, gender, or clinical confounders are known to correlate with both the metabolite and phenotype. Epidemiological confounding is a major source of spurious associations in MWAS; this skill is triggered when you have phenotype data including both the exposure/outcome and ≥1 known confounder variables.

## When NOT to use

- Input metabolomic data has not undergone cross-validation or quality control filtering; unfiltered, noisy features will inflate false-positive associations and confounder adjustment will not rescue poor data quality.
- Confounder variables are incomplete or missing for a substantial proportion of samples; partial correlation estimation becomes biased or uninterpretable with high missing-data rates.
- The phenotype of interest has a very low prevalence or extreme sample-size imbalance (e.g., <10 cases); confounder adjustment with small effective sample sizes will produce unstable coefficient estimates and inflated p-value variance.

## Inputs

- SummarizedExperiment object (metabo_SE) with metabolomic feature matrix and phenotype annotations
- Phenotype data table with columns: disease/outcome phenotype (e.g., BMI), confounder variables (age, gender, disease status), and sample identifiers
- CV-filtered metabolomic feature matrix (rows = ppm values/metabolite identifiers, columns = samples)
- Specification of confounder variables to adjust for (character vector, e.g. c('Age', 'Gender', 'T2D'))

## Outputs

- MWAS association matrix (3-column table or data.frame): rows = metabolic features (ppm values); columns = [r (partial correlation coefficient), p (raw p-value), pFDR (Benjamini-Hochberg corrected p-value)]
- Intermediate partial correlation test statistics and degrees of freedom
- Optional: bootstrapped confidence intervals or feature-wise effect size estimates (if bootstrapping workflow is invoked)

## How to apply

Load a SummarizedExperiment object containing CV-filtered metabolomic features and phenotype data (BMI, age, gender, disease status, etc.). Use MWASTools::MWAS_stats() with the disease_id parameter set to your phenotype of interest, explicitly specify confounders (e.g., Age, Gender, T2D), and select the correlation method (Spearman for rank-based, linear for parametric). The function computes partial correlations between each metabolite and the phenotype while statistically controlling for the specified confounders using regression residualization or partial correlation algebra. Calculate raw p-values from the test statistics, then apply Benjamini-Hochberg (BH) correction to generate adjusted p-values (pFDR). Assemble results into a three-column matrix with metabolite identifiers as row names and columns for correlation coefficient (r), raw p-value, and pFDR. The key decision point is confounder specification: include only variables that are epidemiologically causal (associated with both exposure and outcome) to avoid over-adjustment bias.

## Related tools

- **MWASTools** (R package providing MWAS_stats() function for confounder-adjusted univariate metabolite–phenotype association testing via partial correlations and generalized linear models) — github.com/AndreaRMICL/MWASTools
- **R** (Programming environment (≥3.3) required for executing MWASTools and performing statistical calculations)
- **Bioconductor** (Computational biology framework providing SummarizedExperiment class and associated packages for metabolomic data manipulation)

## Examples

```
MWAS_result <- MWAS_stats(metabo_SE, disease_id='BMI', confounder_vars=c('Age', 'Gender', 'T2D'), method='spearman'); MWAS_BMI <- data.frame(r=MWAS_result$estimate, p=MWAS_result$p_raw, pFDR=p.adjust(MWAS_result$p_raw, method='BH'))
```

## Evaluation signals

- Raw p-values are uniformly distributed under the null hypothesis (QQ-plot should follow diagonal at low p-values); inflation at small p-values indicates insufficient confounder adjustment or systematic bias.
- After Benjamini-Hochberg correction, the number of significant features (pFDR < 0.05) is substantially lower than raw p-value threshold (p < 0.05), confirming that multiple-testing correction was applied and controls false discovery rate.
- Partial correlation coefficients (r values) are smaller in magnitude than univariate (unadjusted) correlations for the same metabolite–phenotype pairs; larger adjustment indicates stronger confounding.
- Distribution of partial r values is centered near zero for the majority of features, indicating that confounding bias has been removed and most metabolites show no association with the phenotype after adjustment.
- Confounder-adjusted results are reproducible and stable across bootstrapped resamples (if bootstrapping workflow is run); high variance in r or p-values across resamples suggests overfitting or insufficient sample size.

## Limitations

- Multivariate models (e.g., OPLS-DA) do not properly account for confounding factors and may distort observed associations; MWASTools uses univariate hypothesis testing specifically to address this limitation, but univariate approaches lose multivariate interaction information.
- Partial correlation assumes linear relationships between metabolites, phenotype, and confounders; nonlinear confounding or interaction effects will not be fully captured.
- The choice of confounder set is epidemiological and subjective; over-adjustment (including colliders or mediators) can introduce bias, while under-adjustment (omitting true confounders) leaves residual confounding.
- Benjamini-Hochberg correction controls false discovery rate across features but does not account for population structure, relatedness between samples, or cryptic confounding (e.g., batch effects, population stratification).
- Small sample sizes or highly imbalanced phenotypes will produce unstable partial correlation estimates and inflated p-value variance, even with confounder adjustment.

## Evidence

- [intro] a major limitation of these multivariate models from the epidemiological perspective is that they do not properly account for cofounding factors (e.g. age, gender), which might distort the observed: "a major limitation of these multivariate models from the epidemiological perspective is that they do not properly account for cofounding factors (e.g. age, gender), which might distort the observed"
- [intro] we present a package to perform MWAS using univariate hypothesis testing with efficient handling of epidemiological confounders: "we present a package to perform MWAS using univariate hypothesis testing with efficient handling of epidemiological confounders"
- [intro] metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders: "metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders"
- [intro] Metabolome-wide association studies (MWAS) using univariate hypothesis testing with adjustment for epidemiological confounders can identify metabolites associated with phenotypes: "Metabolome-wide association studies (MWAS) using univariate hypothesis testing with adjustment for epidemiological confounders can identify metabolites associated with phenotypes"
- [other] Apply MWAS_stats function from MWASTools with disease_id='BMI', confounder specification (Age, Gender, T2D), and correlation method set to Spearman.: "Apply MWAS_stats function from MWASTools with disease_id='BMI', confounder specification (Age, Gender, T2D), and correlation method set to Spearman."
