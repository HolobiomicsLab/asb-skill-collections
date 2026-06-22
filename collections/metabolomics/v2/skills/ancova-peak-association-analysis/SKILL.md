---
name: ancova-peak-association-analysis
description: Use when when you have preprocessed metabolomics peak tables (feature matrix with samples × peaks) and sample metadata (phenotype/grouping information and optional continuous covariates), and your research question is to identify which peaks differ significantly between groups while accounting for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SMART
  - R GUI
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
---

# ancova-peak-association-analysis

## Summary

Apply analysis-of-covariance (ANCOVA) models to metabolomics peak intensity data to identify features associated with group membership while controlling for continuous covariates. This skill detects significant peaks by fitting linear models with group as a fixed effect and extracting test statistics, p-values, and effect sizes.

## When to use

When you have preprocessed metabolomics peak tables (feature matrix with samples × peaks) and sample metadata (phenotype/grouping information and optional continuous covariates), and your research question is to identify which peaks differ significantly between groups while accounting for confounding continuous variables (e.g., age, BMI). Use ANCOVA instead of PLS/PLS-DA when the goal is association analysis rather than classification or pathway enrichment.

## When NOT to use

- Input data are already a statistical summary table or p-value list — use downstream filtering/visualization instead.
- The research question is classification or prediction of group membership — use PLS/PLS-DA.
- The goal is pathway enrichment or integrative multi-omic analysis — use IOPA.
- Peak intensity data violate ANCOVA assumptions (normality, homogeneity of variance) severely and cannot be transformed — consider non-parametric alternatives.

## Inputs

- Preprocessed peak intensity table (feature matrix: samples × peaks, numeric)
- Sample metadata with group/phenotype labels (factor/categorical)
- Optional: continuous covariate data (e.g., age, BMI, batch effects)

## Outputs

- ANCOVA results table with peak identifiers, F-statistics, p-values, and effect sizes
- Multiple-testing corrected p-values (adjusted p-values)
- Optional: visualization of significant peaks by group

## How to apply

Load the preprocessed peak table (feature matrix) and sample metadata into R. Parse the group membership and any continuous covariate values from the phenotype file. For each peak, fit an analysis-of-covariance model with peak intensity as the response variable, group membership as the fixed effect, and continuous covariates as additional predictors. Extract the F-statistic, p-value, and effect size (e.g., eta-squared) for the group effect from each model. Aggregate results into a single output table with peak identifiers and test-specific metrics (F-statistics, p-values, effect sizes). Apply multiple-testing correction (e.g., FDR or Bonferroni) to p-values to control false discovery rate.

## Related tools

- **R** (Statistical computing environment used to implement ANCOVA model fitting and extract F-statistics, p-values, and effect sizes for each peak) — https://www.r-project.org/
- **SMART** (Integrated metabolomics analysis software that encapsulates ANCOVA as one of three statistical analysis dispatch methods) — https://github.com/YuJenL/SMART
- **R GUI** (User-friendly graphical interface to SMART that facilitates ANCOVA parameter specification and results visualization) — https://github.com/YuJenL/SMART

## Evaluation signals

- For each peak, verify that F-statistic, p-value, and effect size are numerically valid and within expected ranges (e.g., F ≥ 0, 0 ≤ p ≤ 1, 0 ≤ eta-squared ≤ 1).
- Check that adjusted p-values are monotonically non-decreasing with respect to unadjusted p-values (i.e., multiple-testing correction was applied correctly).
- Verify that peak count in results matches peak count in input feature matrix.
- For positive control peaks (known to differ between groups), confirm they appear in the top-ranked results by p-value.
- Compare results to univariate t-tests without covariates; ANCOVA p-values should be smaller (more significant) for peaks where covariates explain confounding variation.
- Inspect volcano plot or forest plot of effect sizes vs. p-values for expected patterns (e.g., high effect sizes corresponding to low p-values).

## Limitations

- ANCOVA assumes linear relationships between peak intensity and covariates; non-linear associations may be missed.
- Large imbalances in group sizes or covariate distributions can reduce statistical power and inflate type I error.
- ANCOVA assumes homogeneity of variance across groups; heteroscedastic peaks may violate this assumption and require transformation or Welch-type correction.
- Results are marginal associations for each peak in isolation; no interaction effects between peaks or pathway-level patterns are captured.
- Multiple testing on thousands of peaks inflates family-wise error; uncorrected p-values will lead to false positives.

## Evidence

- [other] For ANCOVA: fit analysis-of-covariance models with peak intensity as response, group membership as fixed effect, and continuous covariates as needed; extract F-statistics, p-values, and effect sizes for each peak.: "For ANCOVA: fit analysis-of-covariance models with peak intensity as response, group membership as fixed effect, and continuous covariates as needed; extract F-statistics, p-values, and effect sizes"
- [intro] Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA): "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
- [other] Load the preprocessed peak table (feature matrix with samples × peaks) into R.: "Load the preprocessed peak table (feature matrix with samples × peaks) into R."
- [other] Parse the analysis type parameter (ANCOVA, PLS/PLS-DA, or IOPA) and sample metadata (phenotype/grouping information).: "Parse the analysis type parameter (ANCOVA, PLS/PLS-DA, or IOPA) and sample metadata (phenotype/grouping information)."
- [other] Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics.: "Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics."
