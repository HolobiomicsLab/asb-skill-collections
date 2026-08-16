---
name: linear-model-design-matrix-specification
description: Use when when preparing to perform differential abundance analysis on
  batch-corrected lipid abundance matrices in designs with multiple factors (e.g.,
  treatment × time, multi-group comparisons), repeated measures, or blocking structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3672
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - ADViSELipidomics
  - limma
  - edgeR
  - ComBat
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration
  per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization
  of lipidomics data.
- allows the identification of differentially abundant lipids in simple and complex
  experimental designs
- dealing with batch effect correction.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# linear-model-design-matrix-specification

## Summary

Specification of design matrices for differential abundance testing in lipidomics that encode experimental factors (treatment groups, batch identifiers, repeated measures) to enable limma or edgeR to fit linear models across simple and complex experimental designs. This skill ensures statistical tests correctly account for all sources of biological and technical variation.

## When to use

When preparing to perform differential abundance analysis on batch-corrected lipid abundance matrices in designs with multiple factors (e.g., treatment × time, multi-group comparisons), repeated measures, or blocking structures. Use this skill before invoking limma or edgeR to ensure the model captures the full experimental structure and batch corrections are properly integrated.

## When NOT to use

- Input lipid abundance matrix has not yet undergone batch effect correction (ComBat or similar); design matrix specification assumes batch effects have been either removed or are explicitly modeled in the design itself.
- Experimental design is purely observational with no grouping or comparison structure; design matrix specification is oriented toward hypothesis-driven contrasts.
- Abundance data are not on a linear scale (e.g., raw counts without normalization); limma and edgeR assume either normalized continuous abundances or count-based input handled by appropriate transformations.

## Inputs

- batch-corrected lipid abundance matrix (samples × lipids, numeric)
- sample metadata including batch identifiers and experimental group assignments (data.frame or matrix)
- design formula or design matrix specifying experimental structure (e.g., ~treatment, ~treatment + batch + subject_id for repeated measures)

## Outputs

- design matrix (samples × model_terms, numeric)
- contrast matrix (model_terms × comparisons_of_interest, numeric)
- fitted model object (limma MArrayLM or edgeR DGEGLM) encoding coefficients, standard errors, and statistics per lipid

## How to apply

Construct a design matrix that encodes all experimental factors (treatment group, batch, and any repeated-measures or blocking variables) alongside the batch-corrected lipid abundance matrix. The design matrix rows correspond to samples and columns to model coefficients (intercept, treatment contrasts, batch effects if retained post-ComBat correction). For complex designs, specify contrast matrices to extract specific comparisons of interest (e.g., treatment A vs. control). Pass the design and contrast matrices to limma::lmFit() or edgeR::glmFit() to fit a linear model to each lipid's batch-corrected abundance across samples. The model's estimated coefficients, standard errors, and t/F-statistics are then used to compute fold-changes, p-values, and adjusted p-values (FDR correction) per lipid. Rationale: explicitly encoding the experimental structure allows the statistical framework to partition variance into biological signal (treatment effects) and residual noise, improving power and reducing false positives in high-dimensional lipidomics data.

## Related tools

- **limma** (Linear model fitting and differential abundance testing engine; accepts design and contrast matrices to fit per-lipid linear models and compute t-statistics and p-values.)
- **edgeR** (Generalized linear model framework for differential abundance; alternative to limma for complex designs; accepts design matrices to fit negative binomial models.)
- **ComBat** (Batch effect correction method applied upstream; design matrices can optionally re-encode remaining batch structure if post-ComBat batch adjustment is incomplete.)
- **ADViSELipidomics** (Shiny application providing end-to-end preprocessing, batch correction, design specification, and differential abundance testing for lipidomics data.) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- Design matrix dimensions match sample count (n_samples rows) and encode all experimental factors without aliasing or singularity.
- Contrast matrix correctly specifies the biological comparisons of interest (e.g., treatment A vs. control); column rank matches number of independent contrasts.
- Fitted model produces per-lipid t-statistics, standard errors, and residual variance estimates consistent with the experimental structure; no convergence failures or structural warnings.
- Fold-changes and p-values are computed for each lipid; p-value distribution under null (uniform on [0,1]) indicates no systematic bias; adjusted p-values (FDR) correctly control false discovery rate.
- Batch effects (if retained in model) show non-significant coefficients or are orthogonal to treatment comparisons, confirming biological signal is preserved after batch correction.

## Limitations

- Design matrix specification assumes samples are independent or repeated-measures structure is correctly encoded; violation (e.g., missing subject_id in mixed-effects context) leads to inflated test statistics.
- Linear model framework assumes constant variance across groups; heteroscedasticity or outliers can inflate error variance and reduce power; consider weighted models or robust methods if variance structure is highly unbalanced.
- Complex designs with many factors or interactions require sufficient sample size (n >> p, where p = number of model terms) to avoid overfitting and unstable coefficient estimates; sparse designs may yield singular or near-singular design matrices.
- ComBat batch correction, when applied, assumes batch effects are orthogonal to biological effects; if batch is confounded with treatment (e.g., all samples in batch 1 are treatment, all in batch 2 are control), batch correction can remove genuine signal.

## Evidence

- [other] Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures).: "Perform differential abundance testing using limma or edgeR for linear models supporting complex experimental designs (e.g., multi-factor, repeated measures)."
- [readme] allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction.: "allows the identification of differentially abundant lipids in simple and complex experimental designs, dealing with batch effect correction."
- [other] Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal.: "Apply batch effect correction using ComBat or similar method to remove systematic batch variation while preserving biological signal."
- [other] Load preprocessed and normalized lipid abundance matrix (with batch identifiers and experimental group assignments).: "Load preprocessed and normalized lipid abundance matrix (with batch identifiers and experimental group assignments)."
- [other] Export ranked differential lipid table as CSV with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means.: "Export ranked differential lipid table as CSV with columns: lipid_id, lipid_class, log2_fold_change, p_value, adjusted_p_value, batch_corrected_group_means."
