---
name: latent-group-discovery-from-omics-data
description: Use when you have a preprocessed metabolomics feature matrix and sample
  metadata but suspect hidden substructures or unknown groupings that are not explained
  by known experimental conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SMART
  license_tier: open
  provenance_tier: literature
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

# latent-group-discovery-from-omics-data

## Summary

Identify unknown latent groups (LGs) and hidden substructures in metabolomics datasets independent of known experimental conditions using unsupervised clustering and latent variable discovery methods. This skill distinguishes confounded batch sources from independent latent batch effects that would otherwise remain undetected in standard batch correction workflows.

## When to use

Apply this skill when you have a preprocessed metabolomics feature matrix and sample metadata but suspect hidden substructures or unknown groupings that are not explained by known experimental conditions. Triggers include: (1) unexplained variance in PCA or dimensionality reduction plots after accounting for known batch factors; (2) suspicion that samples cluster differently than documented experimental design; (3) need to comprehensively characterize all batch sources before statistical testing or classification; or (4) requirement to distinguish whether observed batch effects arise from recorded conditions or from latent confounders.

## When NOT to use

- Input data has not been preprocessed (raw instrument files, non-normalized features) — perform data import, visualization, peak analysis, and preprocessing first.
- You have already applied deterministic batch correction and want to verify correction quality — use quality control and post-hoc batch effect assessment instead.
- The goal is to remove or regress out known batch effects rather than discover unknown sources — use standard batch correction methods (e.g., ComBat, surrogate variable analysis) instead.

## Inputs

- Preprocessed metabolomics feature matrix (samples × features)
- Sample metadata with known experimental conditions and batch annotations

## Outputs

- Latent group assignments for each sample
- Batch-assignment record documenting sample memberships in known conditions and latent groups with supporting statistics
- Association statistics between latent groups and known experimental conditions
- Dimensionality reduction visualization (e.g., PCA plot) annotated with latent group memberships

## How to apply

Load the preprocessed feature matrix and sample metadata into R. First, perform dimensionality reduction (e.g., PCA) on the feature matrix to visualize existing batch structure and identify potential unknown groupings. Next, apply unsupervised clustering methods (k-means, hierarchical clustering, or mixture models) to discover latent groups independently of known experimental factors. Test each discovered latent group for association with known experimental conditions using appropriate statistical tests (e.g., PERMANOVA or linear models) to assess whether the latent groups are confounded with known factors or represent independent batch sources. Generate a batch-assignment record documenting each sample's membership in both known conditions and discovered latent groups, with supporting statistics. The workflow distinguishes confounded versus independent batch sources by contrasting the latent group structure against the known experimental design.

## Related tools

- **SMART** (Integrated R-based environment for executing the complete Batch Effect Analysis module, including dimensionality reduction (PCA), unsupervised clustering, statistical testing (PERMANOVA, linear models), and batch-assignment record generation) — github.com/YuJenL/SMART
- **R** (Programming environment in which SMART and clustering/dimensionality reduction functions (e.g., prcomp for PCA, kmeans, hclust, mixture models) are executed)

## Evaluation signals

- Latent group assignments are reproducible across runs of the unsupervised clustering algorithm (or confirmed via stability metrics such as silhouette score or Davies–Bouldin index).
- Dimensionality reduction plot (PCA) shows visual separation of discovered latent groups, confirming they represent meaningful variance structure in the feature matrix.
- Association statistics (p-values, effect sizes from PERMANOVA or linear models) between latent groups and known experimental conditions are computed and reported, clearly distinguishing confounded from independent batch sources.
- Batch-assignment record contains complete sample-level documentation: each sample has a row with known batch factor assignments and latent group membership labels with supporting statistic values.
- The total variance explained by known conditions plus discovered latent groups is higher than variance explained by known conditions alone, indicating latent groups capture previously unaccounted batch structure.

## Limitations

- The number and characteristics of latent groups depend on the choice of clustering algorithm and hyperparameters (e.g., k in k-means); sensitivity analysis or model selection criteria (e.g., elbow method, silhouette analysis) are necessary but not always definitive.
- Latent groups discovered may reflect biological heterogeneity rather than batch artifacts; domain knowledge and downstream validation (e.g., association with technical covariates) are required to distinguish true batch sources from biological substructure.
- Confounding between known experimental conditions and latent groups can obscure the true source of batch effects; careful interpretation of association statistics and potentially stratified analyses may be needed.

## Evidence

- [other] Apply unsupervised clustering or latent variable discovery (e.g., k-means, hierarchical clustering, or mixture models) to identify unknown latent groups (LGs) and hidden substructures independent of known factors.: "Apply unsupervised clustering or latent variable discovery (e.g., k-means, hierarchical clustering, or mixture models) to identify unknown latent groups (LGs) and hidden substructures independent of"
- [other] Assess association between identified latent groups and known experimental conditions to distinguish confounded versus independent batch sources.: "Assess association between identified latent groups and known experimental conditions to distinguish confounded versus independent batch sources."
- [intro] Batch Effect Analysis: Explore batch effects (e.g., known experimental conditions, unknown latent groups (LGs), or hidden substructures).: "Batch Effect Analysis: Explore batch effects (e.g., known experimental conditions, unknown latent groups (LGs), or hidden substructures)."
- [other] Generate batch-assignment record documenting each sample's batch source assignments (known conditions and latent group memberships) with supporting statistics.: "Generate batch-assignment record documenting each sample's batch source assignments (known conditions and latent group memberships) with supporting statistics."
- [other] Perform dimensionality reduction (e.g., PCA) on the feature matrix to visualize batch structure.: "Perform dimensionality reduction (e.g., PCA) on the feature matrix to visualize batch structure."
