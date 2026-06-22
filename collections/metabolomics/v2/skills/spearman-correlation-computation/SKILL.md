---
name: spearman-correlation-computation
description: 'Use when : (1) you have metabolomic data (NMR or MS-derived) and a continuous phenotype variable; (2) you need to quantify associations while controlling for known confounders (age, gender, disease status);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3768
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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

# Spearman Correlation Computation

## Summary

Compute partial Spearman rank correlations between metabolites and a continuous phenotype (e.g., BMI) while adjusting for epidemiological confounders, producing correlation coefficients, raw p-values, and multiple-testing corrected p-values. This skill is essential for metabolome-wide association studies (MWAS) where linear assumptions may be violated or robustness to outliers is required.

## When to use

Use this skill when: (1) you have metabolomic data (NMR or MS-derived) and a continuous phenotype variable; (2) you need to quantify associations while controlling for known confounders (age, gender, disease status); (3) the data may violate normality assumptions or contain outliers that would compromise Pearson correlations; (4) your goal is to produce a metabolome-wide association matrix with standardized effect sizes and p-values for hypothesis testing and multiple-comparison correction.

## When NOT to use

- Input phenotype is categorical or ordinal — use logistic or ordinal partial correlation instead.
- Metabolomic data has not undergone quality control (QC) filtering — apply QC analysis first to remove low-intensity or unreliable features.
- Sample size is very small (n < 30) — partial Spearman correlations may have inflated Type I error or low power; consider effect-size bootstrapping for stability assessment.

## Inputs

- SummarizedExperiment object containing metabolomic features (columns) and samples (rows) after CV filtering
- Phenotype data frame with columns: phenotype_variable (numeric, continuous), confounders (age, gender, disease_status), and sample identifiers

## Outputs

- MWAS_stats result object or matrix with 3 columns: [r (Spearman partial correlation coefficient), p (raw p-value), pFDR (Benjamini-Hochberg corrected p-value)]
- Row names: metabolite identifiers (ppm chemical shifts or feature names)

## How to apply

Load the quality-control filtered metabolomic SummarizedExperiment object and verify that the phenotype data includes the primary phenotype (e.g., BMI), all confounders (age, gender, type II diabetes status), and sample metadata. Invoke MWASTools::MWAS_stats with disease_id set to the phenotype name, specify all confounders in the confounder parameter, and set correlation method to 'Spearman'. The function computes partial Spearman rank correlations between each metabolite (rows) and the phenotype, conditioning on confounders via residualization or equivalent partial correlation algebra. Extract the raw p-values from the test statistics, then apply Benjamini-Hochberg (BH) correction to generate false-discovery-rate adjusted p-values (pFDR). Assemble results into a three-column matrix with metabolite identifiers (ppm values or feature names) as row names and columns [r, p, pFDR], where r is the partial Spearman coefficient.

## Related tools

- **MWASTools** (R/Bioconductor package providing MWAS_stats function to compute partial correlations (Spearman or Pearson), p-values, and multiple-testing correction for metabolite-phenotype associations) — https://github.com/AndreaRMICL/MWASTools
- **R** (Programming language environment (≥3.3) required to load and execute MWASTools)
- **Bioconductor** (R package repository and infrastructure for SummarizedExperiment objects and statistical genomics methods)

## Examples

```
MWAS_BMI <- MWAS_stats(metabo_SE, disease_id='BMI', confounders=c('Age', 'Gender', 'T2D'), method='Spearman'); MWAS_BMI_matrix <- cbind(r=MWAS_BMI$estimate, p=MWAS_BMI$p.value, pFDR=p.adjust(MWAS_BMI$p.value, method='BH'))
```

## Evaluation signals

- Matrix dimensions: 3 columns (r, p, pFDR) × number_of_metabolites rows; no missing values.
- Correlation coefficients r are in range [-1, 1]; p-values are in (0, 1] and pFDR values are monotonically non-decreasing when ordered by p.
- Benjamini-Hochberg correction is valid: pFDR[i] ≥ p[i] for all i, and min(pFDR) ≥ min(p).
- Row names match metabolite identifiers from the input SummarizedExperiment object (e.g., ppm values or feature IDs).
- Confounder adjustment is confirmed: partial correlations differ from marginal (unadjusted) Spearman correlations; magnitude of adjustment correlates with confounder strength and collinearity.

## Limitations

- Partial Spearman correlations assume monotonic relationships; non-monotonic associations will be attenuated or missed.
- Multiple testing correction via BH is conservative when metabolite correlations are highly structured (e.g., correlated due to shared metabolic pathways); resampling-based or hierarchical corrections may be more powerful.
- Multivariate models (e.g., OPLS-DA) do not properly account for confounding factors which might distort the observed associations between metabolites and conditions, whereas univariate partial correlations do; however, univariate methods ignore inter-metabolite structure.
- Sample size and confounder collinearity affect precision; sparse or collinear confounders can reduce effective degrees of freedom and inflate p-values.

## Evidence

- [other] MWAS_stats result object with partial Spearman coefficients, raw and BH-corrected p-values: "MWAS_BMI is a 3-column matrix containing metabolic features (ppm values) in rows with columns for estimates (r coefficients), raw p-values, and BH-corrected p-values (pFDR) from partial Spearman"
- [other] MWASTools MWAS_stats function with confounders and Spearman method: "Apply MWAS_stats function from MWASTools with disease_id='BMI', confounder specification (Age, Gender, T2D), and correlation method set to Spearman"
- [intro] Univariate hypothesis testing with confounder adjustment: "we present a package to perform MWAS using univariate hypothesis testing with efficient handling of epidemiological confounders"
- [intro] Partial correlations and generalized linear models for metabolite-phenotype associations: "metabolite-phenotype association models (partial correlations, generalized linear models) adjusted for epidemiological confounders"
- [intro] Confounding factors distort observed associations in multivariate models: "a major limitation of these multivariate models from the epidemiological perspective is that they do not properly account for cofounding factors (e.g. age, gender), which might distort the observed"
- [other] Benjamini-Hochberg correction for multiple testing: "Apply Benjamini-Hochberg correction to generate adjusted p-values (pFDR)"
