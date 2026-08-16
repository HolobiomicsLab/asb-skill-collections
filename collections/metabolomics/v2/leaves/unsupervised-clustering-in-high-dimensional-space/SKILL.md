---
name: unsupervised-clustering-in-high-dimensional-space
description: Use when you have a preprocessed feature matrix from metabolomics data
  and suspect unknown batch effects, hidden sample substructures, or latent groups
  not captured by experimental metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - SMART
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

# unsupervised-clustering-in-high-dimensional-space

## Summary

Apply unsupervised clustering (k-means, hierarchical clustering, or mixture models) to high-dimensional metabolomics feature matrices to identify latent groups and hidden substructures independent of known experimental conditions. This skill reveals batch effects and sample groupings not apparent from metadata alone.

## When to use

You have a preprocessed feature matrix from metabolomics data and suspect unknown batch effects, hidden sample substructures, or latent groups not captured by experimental metadata. This skill is especially indicated when you need to distinguish confounded batch sources (correlated with known conditions) from independent batch sources (orthogonal to metadata).

## When NOT to use

- Input feature matrix is already stratified by known batch; use supervised batch correction instead.
- Sample size is very small (< 10 samples); clustering becomes unreliable and overfits.
- The research goal is to remove batch effects for downstream analysis; use batch correction (ComBat, SVA) rather than discovery of latent structure.

## Inputs

- preprocessed feature matrix (samples × features, numeric)
- sample metadata with known experimental conditions
- optional: feature annotations or metadata

## Outputs

- latent group assignments (vector of cluster labels per sample)
- dimensionality-reduced coordinates (PCA or equivalent scores)
- batch-assignment record (data frame with sample ID, latent group, association statistics)
- visualizations (scatter plots of reduced dimensions colored by latent group)

## How to apply

First, perform dimensionality reduction (e.g., PCA) on the preprocessed feature matrix to visualize the batch structure in lower-dimensional space. Then apply unsupervised clustering algorithms (k-means, hierarchical clustering, or mixture models) to partition samples into latent groups without using known experimental conditions as input. After clustering converges, assess association between identified latent groups and known experimental conditions using statistical tests (e.g., chi-squared, Fisher's exact test) to determine whether each latent group is confounded with known factors or independent. Generate a batch-assignment record documenting each sample's latent group membership and association statistics. The rationale is that latent groups orthogonal to known conditions represent true hidden batch effects, while confounded groups may reflect systematic variation already captured by experimental design.

## Related tools

- **R** (statistical computing environment for dimensionality reduction, clustering algorithm implementation (k-means, hierarchical clustering, mixture models), and association testing)
- **SMART** (integrated metabolomics analysis platform providing Batch Effect Analysis module that wraps dimensionality reduction, unsupervised clustering, and latent group discovery with R backend and GUI) — github.com/YuJenL/SMART

## Examples

```
# In R with SMART or base functions:
# pca_result <- prcomp(t(feature_matrix), scale=TRUE); km <- kmeans(feature_matrix, centers=5, nstart=10); batch_record <- data.frame(sample_id=colnames(feature_matrix), latent_group=km$cluster)
```

## Evaluation signals

- Latent group assignments are stable across multiple random seeds or initialization strategies (if using k-means); silhouette scores or Davies-Bouldin index indicate well-separated clusters.
- PCA biplot or t-SNE projection shows clear visual separation of latent groups; samples within assigned clusters are spatially proximal in reduced space.
- Statistical tests (chi-squared, Fisher's exact) and p-values quantify association between latent groups and known conditions; independent latent groups show high p-values (low association); confounded groups show low p-values.
- Batch-assignment record is complete with no missing cluster labels; association statistics are non-negative and bounded appropriately (e.g., p-values ∈ [0,1]).
- When latent groups are projected onto known experimental conditions, orthogonal groups should be distributed across multiple condition levels; confounded groups should cluster in single or few condition levels.

## Limitations

- Unsupervised clustering is sensitive to algorithm choice (k-means vs. hierarchical) and parameter selection (number of clusters k, linkage method); multiple runs with different k and consensus clustering may be needed to ensure robustness.
- Interpretation of latent groups requires domain knowledge; algorithmic clusters may reflect technical noise, rare biological subpopulations, or true batch artifacts—statistical association with metadata helps distinguish, but cannot fully resolve ambiguity.
- High-dimensional feature matrices with many correlated features can inflate cluster separation artificially; feature pre-selection, PCA dimensionality reduction, or regularized clustering may be necessary before clustering.

## Evidence

- [intro] Apply unsupervised clustering or latent variable discovery (e.g., k-means, hierarchical clustering, or mixture models) to identify unknown latent groups (LGs) and hidden substructures independent of known factors.: "Apply unsupervised clustering or latent variable discovery (e.g., k-means, hierarchical clustering, or mixture models) to identify unknown latent groups (LGs) and hidden substructures independent of"
- [intro] Perform dimensionality reduction (e.g., PCA) on the feature matrix to visualize batch structure.: "Perform dimensionality reduction (e.g., PCA) on the feature matrix to visualize batch structure."
- [intro] Assess association between identified latent groups and known experimental conditions to distinguish confounded versus independent batch sources.: "Assess association between identified latent groups and known experimental conditions to distinguish confounded versus independent batch sources."
- [readme] Batch Effect Analysis: Explore batch effects (e.g., known experimental conditions, unknown latent groups (LGs), or hidden substructures): "Batch Effect Analysis: Explore batch effects (e.g., known experimental conditions, unknown latent groups (LGs), or hidden substructures)"
