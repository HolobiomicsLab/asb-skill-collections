---
name: distance-matrix-computation-for-samples
description: Use when after batch effect removal and data integration, when you have
  a feature-by-sample matrix (finalData) and wish to separate and visualize sample
  groups by their metabolomic profiles using clustering methods such as hierarchical
  clustering analysis (HCA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - factoextra
  - ggplot2
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
- several R packages are utilized in the background processes, including factoextra,
  FSelector, genefilter
- several R packages are utilized in the background processes, including ggfortify,
  ggplot2, igraph
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# distance-matrix-computation-for-samples

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute pairwise distance matrices between metabolomic samples to quantify dissimilarity and enable downstream clustering and visualization. This is a foundational step in sample separation workflows where hierarchical or other clustering methods require inter-sample distances as input.

## When to use

After batch effect removal and data integration, when you have a feature-by-sample matrix (finalData) and wish to separate and visualize sample groups by their metabolomic profiles using clustering methods such as hierarchical clustering analysis (HCA). Use this skill when the input is a normalized feature matrix and you need to compute distances before applying Sample_Separation() with method='HCA' or similar clustering.

## When NOT to use

- Input data has not been batch-corrected or integrated — remove batch effects first
- Feature matrix contains missing values or negative intensities without prior imputation or transformation
- Sample count is very small (n < 3) such that distance computation or clustering is uninformative

## Inputs

- finalData: feature-by-sample matrix of metabolite intensities (rows = features/m/z, columns = samples)
- finalLabel: vector of sample group labels or class assignments

## Outputs

- Distance matrix: symmetric square matrix of pairwise inter-sample distances
- Hierarchical clustering dendrogram: tree visualization of sample groupings
- Cluster assignments: vector assigning each sample to one of k clusters

## How to apply

Extract the finalized feature-by-sample matrix (finalData) and corresponding sample group labels (finalLabel) from integrated and batch-corrected metabolomic data. Compute pairwise distances between all samples using an appropriate distance metric (e.g. Euclidean, which is standard for hierarchical clustering in metabolomics). The distance matrix becomes the input to hierarchical clustering algorithms, which then produce dendrograms and cluster assignments. Verify that the distance matrix is symmetric, has zero diagonal, and that all entries are non-negative. Choose the distance metric based on data characteristics: Euclidean distance is typical for continuous metabolite intensities. Pass the resulting distance matrix to clustering functions (e.g., hclust in R via factoextra) to generate sample dendrograms and separate samples into k clusters (e.g., k=2 for two-group comparisons).

## Related tools

- **factoextra** (Distance matrix computation and hierarchical clustering visualization for sample separation)
- **ggplot2** (Visualization of dendrograms and clustering results)
- **LargeMetabo** (Wrapper function Sample_Separation() that orchestrates distance computation, clustering, and dendrogram generation) — https://github.com/LargeMetabo/LargeMetabo

## Examples

```
Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")
```

## Evaluation signals

- Distance matrix is symmetric (dist[i,j] == dist[j,i]) and has zero diagonal
- All pairwise distances are non-negative and bounded within expected range for the metric
- Resulting dendrogram clearly separates samples by group label; intra-group distances are smaller than inter-group distances
- Cluster assignments (from k=2 or chosen k) match or closely correlate with biological group labels (finalLabel)
- Dendrogram height and branch structure reflect biological relatedness: samples from the same group cluster together before samples from different groups merge

## Limitations

- Distance computation is sensitive to feature scaling; unnormalized or differently-scaled features can dominate the metric
- Euclidean distance assumes linear relationships and can be affected by extreme outliers or highly skewed metabolite distributions
- Hierarchical clustering dendrogram topology can vary with linkage method (single, complete, average, Ward); choose linkage appropriate for metabolomic data structure
- Large feature matrices (thousands of features) can lead to high-dimensional distance artifacts; feature selection or dimensionality reduction may be necessary before distance computation

## Evidence

- [other] Research question and workflow context: "How does the Sample_Separation function with hierarchical clustering (HCA) method and k=2 clusters operate to visualize the clustering and separation of different sample groups in metabolomic data?"
- [readme] Function signature and parameters: "Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")"
- [readme] Purpose of sample separation workflow: "There are four sample separation methods for visualizing the clustering and separation of different samples."
- [readme] Input data format specification: "Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct. The first two columns provide the mass and retention time,"
- [other] Output dendrogram generation: "Generate hierarchical dendrogram visualization showing sample groupings and cluster boundaries."
