---
name: multivariate-feature-importance-extraction
description: 'Use when you have a preprocessed peak table (feature matrix: samples
  × peaks) with known class labels or phenotype groupings, and you want to identify
  which individual peaks contribute most to classification or discrimination between
  groups.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2990
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SMART
  - R (base and statistical packages)
  techniques:
  - mass-spectrometry
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multivariate-feature-importance-extraction

## Summary

Extract and rank metabolomics features (peaks) by their discriminative or predictive importance using multivariate statistical models such as PLS/PLS-DA. This skill identifies which peaks drive class separation or prediction, enabling downstream peak annotation and pathway prioritization.

## When to use

Apply this skill when you have a preprocessed peak table (feature matrix: samples × peaks) with known class labels or phenotype groupings, and you want to identify which individual peaks contribute most to classification or discrimination between groups. Use it after data preprocessing and quality control, before peak identification or pathway analysis.

## When NOT to use

- Input peak table has not been preprocessed, normalized, or quality-filtered — perform those steps first.
- Sample metadata is missing or incomplete — VIP extraction requires valid class labels for all samples.
- You seek univariate feature selection only — use ANCOVA for single-peak association analysis instead.

## Inputs

- preprocessed peak table (feature matrix: samples × peaks, numeric intensity values)
- sample metadata (phenotype/grouping information, class labels)
- analysis parameters (number of latent components, cross-validation folds)

## Outputs

- variable importance scores table (peak identifier, VIP score, or equivalent importance metric)
- classification performance metrics (accuracy, sensitivity, specificity)
- ranked peak list sorted by importance

## How to apply

Build partial least-squares (PLS) or PLS discriminant analysis (PLS-DA) models using the peak intensity matrix as features and sample class membership or phenotype as the response variable. Compute variable importance in projection (VIP) scores or other importance metrics for each peak to quantify its contribution to the model's predictive power. Extract importance scores alongside peak identifiers and classification performance metrics (accuracy, sensitivity, specificity). Rank peaks by importance score to prioritize those with the strongest discriminative signal for downstream annotation or pathway enrichment.

## Related tools

- **SMART** (R-based metabolomics pipeline that implements PLS/PLS-DA models and computes variable importance scores for peak discrimination) — https://github.com/YuJenL/SMART
- **R (base and statistical packages)** (Environment for building PLS/PLS-DA models and computing importance metrics)

## Evaluation signals

- VIP scores are numeric, ranked in descending order, and span a reasonable range (typically 0–3+ in PLS-DA).
- Top-ranked peaks show biological plausibility (e.g., known metabolite m/z ratios or pathway associations).
- Classification metrics (accuracy, sensitivity, specificity) are consistent with model performance and match reported cross-validation results.
- Peaks flagged as high-importance show clear visual separation between classes in multivariate score plots (PC1 vs. PC2).
- Number of selected high-importance peaks (e.g., VIP > 1) is reasonable relative to sample size and feature dimensionality.

## Limitations

- VIP scores depend on model stability and number of latent components; over-fitting or poor component selection can inflate importance scores.
- PLS-DA can be biased toward high-abundance peaks; low-abundance biomarkers may be ranked lower despite biological significance.
- Importance scores reflect multivariate correlation structure, not causal relationships or individual peak–phenotype associations.
- Cross-validation fold size and random seed affect reproducibility; results may vary slightly across runs.

## Evidence

- [intro] PLS/PLS-DA model construction and VIP score extraction: "For PLS/PLS-DA: build partial least-squares or discriminant analysis models using peak features to predict class membership; compute variable importance scores and classification metrics (accuracy,"
- [intro] Input data type and sample metadata requirement: "Load the preprocessed peak table (feature matrix with samples × peaks) into R. Parse the analysis type parameter (ANCOVA, PLS/PLS-DA, or IOPA) and sample metadata (phenotype/grouping information)."
- [intro] Output aggregation and integration into results table: "Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics."
- [readme] Statistical Analysis module scope in SMART pipeline: "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
