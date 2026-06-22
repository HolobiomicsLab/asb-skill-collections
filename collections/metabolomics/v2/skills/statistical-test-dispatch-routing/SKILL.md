---
name: statistical-test-dispatch-routing
description: 'Use when after data preprocessing, quality control, and batch effect correction have produced a validated peak intensity matrix (feature table: samples × peaks) with associated sample metadata (phenotype, grouping, or class labels).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0634
  - http://edamontology.org/topic_3407
  tools:
  - R
  - SMART
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

# statistical-test-dispatch-routing

## Summary

Route preprocessed metabolomics peak tables to appropriate statistical test methods (ANCOVA, PLS/PLS-DA, or IOPA) based on the analysis question and sample metadata. This skill determines which analytical approach best addresses the biological research question and configures the corresponding statistical framework.

## When to use

After data preprocessing, quality control, and batch effect correction have produced a validated peak intensity matrix (feature table: samples × peaks) with associated sample metadata (phenotype, grouping, or class labels). Use this skill when you need to decide whether to perform association analysis (finding peaks correlated with continuous or categorical covariates), classification analysis (predicting group membership from peak patterns), or pathway-level integration (mapping peaks to metabolites and enriching pathway annotations).

## When NOT to use

- Input data is already a list of statistically significant peaks or a pre-filtered set; routing dispatches based on research question, not on existing results.
- Sample metadata is missing or incomplete (group assignment, phenotype, or class labels required for all three methods).
- Analysis type parameter is ambiguous or undefined; the skill requires an explicit ANCOVA/PLS/IOPA choice or a clear biological question that maps to one.

## Inputs

- preprocessed peak table (feature matrix: samples × peaks, intensities normalized and batch-corrected)
- sample metadata (phenotype information, group assignment, or class labels)
- analysis type parameter (ANCOVA, PLS/PLS-DA, or IOPA)
- continuous covariates (optional, for ANCOVA adjustment)
- metabolite identity map (peak → metabolite name; required for IOPA)
- metabolite-pathway associations (required for IOPA)

## Outputs

- aggregated results table indexed by peak identifier
- ANCOVA results: F-statistics, p-values, effect sizes per peak
- PLS/PLS-DA results: variable importance scores, classification accuracy, sensitivity, specificity
- IOPA results: pathway enrichment scores and significance p-values per pathway

## How to apply

Parse the research question and sample metadata to determine the analysis intent: if the goal is to test whether peak intensities associate with covariates or group membership, dispatch to ANCOVA (fits analysis-of-covariance models with group as fixed effect and continuous covariates, extracting F-statistics and p-values per peak); if the goal is to classify samples into predefined groups or predict class membership from peak signatures, dispatch to PLS/PLS-DA (builds partial least-squares discriminant models and computes variable importance scores and classification metrics); if the goal is systems-level interpretation, dispatch to IOPA (maps peaks to metabolite identities, constructs metabolite-pathway associations, and computes pathway enrichment significance). The routing decision is deterministic once the analysis type parameter is specified. Aggregate results from the selected method into a single results table indexed by peak identifier with test-specific metrics (p-values and effect sizes for ANCOVA; variable importance and accuracy for PLS/PLS-DA; pathway statistics for IOPA).

## Related tools

- **R** (Host language for implementing ANCOVA, PLS/PLS-DA, and IOPA statistical dispatchers; fits models, computes statistics, and aggregates results) — https://www.r-project.org
- **SMART** (Integrated metabolomics analysis platform that implements this routing logic within its Statistical Analysis module; wraps R implementations in a user-friendly R GUI) — https://github.com/YuJenL/SMART

## Evaluation signals

- Results table contains all peaks from input feature matrix, indexed consistently by peak identifier, with no missing or duplicate rows.
- ANCOVA output includes F-statistic, p-value, and effect size for every peak; PLS/PLS-DA output includes variable importance scores and ≥1 classification metric (accuracy, sensitivity, specificity); IOPA output includes ≥1 pathway with enrichment score and p-value.
- P-values are bounded in [0, 1]; effect sizes are positive and finite; variable importance scores are normalized or bounded (e.g., [0, 1] or summing to 1 per model).
- Metadata covariates and group assignments used in the dispatched test match the sample identifiers in the peak table (no samples dropped without explicit filtering).
- Statistical test assumptions documented (e.g., ANCOVA assumes normality of residuals; PLS/PLS-DA assumes sufficient sample count relative to peak dimensionality; IOPA requires valid metabolite ID mapping).

## Limitations

- Routing logic does not automatically detect or warn when sample metadata is incomplete or inconsistent with the selected test (e.g., continuous covariate missing for ANCOVA).
- IOPA results depend on the completeness and accuracy of metabolite identity mapping and pathway annotations; missing or incorrect mappings reduce enrichment sensitivity.
- No guidance provided in the article or README on how to choose between ANCOVA and PLS/PLS-DA when both appear applicable (e.g., multi-group design with continuous covariates); user must make this decision manually.
- Results table does not include confidence intervals or multiple comparison corrections; practitioners must apply post-hoc adjustments (e.g., Benjamini–Hochberg FDR) separately.

## Evidence

- [other] The Statistical Analysis module implements three distinct analytical approaches: ANCOVA for association analysis, PLS/PLS-DA for classification analysis, and IOPA for integrative omics pathway analysis.: "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
- [other] ANCOVA workflow: fit analysis-of-covariance models with peak intensity as response, group membership as fixed effect, and continuous covariates; extract F-statistics, p-values, and effect sizes for each peak.: "For ANCOVA: fit analysis-of-covariance models with peak intensity as response, group membership as fixed effect, and continuous covariates as needed; extract F-statistics, p-values, and effect sizes"
- [other] PLS/PLS-DA workflow: build partial least-squares or discriminant analysis models using peak features to predict class membership; compute variable importance scores and classification metrics.: "For PLS/PLS-DA: build partial least-squares or discriminant analysis models using peak features to predict class membership; compute variable importance scores and classification metrics (accuracy,"
- [other] IOPA workflow: map peaks to metabolite identities, construct metabolite-pathway associations, and compute pathway enrichment scores and significance.: "For IOPA: map peaks to metabolite identities, construct metabolite-pathway associations, and compute pathway enrichment scores and significance."
- [other] Results aggregation: aggregate results into a single results table with peak identifiers and test-specific metrics.: "Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics."
- [readme] SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis.: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis"
