---
name: hierarchical-cluster-analysis-dendrogram-generation
description: Use when you have a feature-by-sample matrix (finalData) of metabolomic intensities and sample group labels (finalLabel), and you want to visualize how samples cluster together based on their overall metabolomic similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - factoextra
  - ggplot2
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
- several R packages are utilized in the background processes, including factoextra, FSelector, genefilter
- several R packages are utilized in the background processes, including ggfortify, ggplot2, igraph
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

# hierarchical-cluster-analysis-dendrogram-generation

## Summary

Apply hierarchical clustering analysis (HCA) to metabolomic feature matrices to produce dendrograms that visualize sample groupings and separation by metabolic profile. This skill is used when you need to discover and display unsupervised clustering structure in high-dimensional metabolomic data without requiring prior knowledge of sample group labels.

## When to use

You have a feature-by-sample matrix (finalData) of metabolomic intensities and sample group labels (finalLabel), and you want to visualize how samples cluster together based on their overall metabolomic similarity. Use this when exploring batch effects, validating sample quality, or assessing whether experimental groups separate naturally in metabolic space before proceeding to marker identification.

## When NOT to use

- Sample size is very small (< 5 samples total) — dendrograms become uninformative and cluster assignments become unstable.
- Feature matrix contains many missing values or has not been batch-corrected — uncontrolled technical variation will dominate clustering and obscure true biological groupings.
- Your research question requires a supervised clustering method that incorporates known sample labels a priori (use Marker_Identify with PLS-DA or OPLS-DA instead).

## Inputs

- finalData (feature-by-sample matrix: rows = metabolic features, columns = samples, values = intensity or normalized measurements)
- finalLabel (vector of sample group labels or identifiers, length = number of samples)
- clusters (integer ≥ 2, specifying target number of clusters for interpretation)

## Outputs

- Hierarchical dendrogram visualization (tree plot showing sample merging hierarchy and cluster boundaries)
- Cluster assignments (vector mapping each sample to its assigned cluster)
- Distance matrix (computed from sample-to-sample metabolomic dissimilarity)

## How to apply

Load the feature matrix (finalData) and sample labels (finalLabel) from your integrated and batch-corrected metabolomic dataset. Call Sample_Separation() with method='HCA' and clusters=2 (or a higher integer if you expect more natural groupings). HCA computes a distance matrix between samples using hierarchical linkage (typically Euclidean or correlation distance), then constructs a dendrogram showing merging steps. Extract cluster assignments for each sample from the function output and examine the dendrogram to identify the height threshold at which samples separate. Validate cluster coherence by checking whether samples within each cluster share similar metabolomic profiles and whether known sample group labels align with dendrogram structure.

## Related tools

- **LargeMetabo** (Provides Sample_Separation() function for HCA dendrogram generation and cluster assignment extraction) — https://github.com/LargeMetabo/LargeMetabo
- **factoextra** (Used in background for visualization and extraction of cluster results from hierarchical objects)
- **ggplot2** (Used for rendering dendrogram and cluster boundary annotations)

## Examples

```
finalData <- MarkerData$finalData; finalLabel <- MarkerData$finalLabel; Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")
```

## Evaluation signals

- Dendrogram topology is interpretable: samples within known groups should predominantly cluster together before merging across group boundaries.
- Cluster assignments are reproducible: rerunning with the same input data and parameters yields identical cluster membership.
- Distance matrix is symmetric and satisfies triangle inequality; diagonal elements are zero.
- Dendrogram height values monotonically increase as you move from leaf nodes (individual samples) toward the root (all samples merged), indicating valid hierarchical structure.
- Visual separation in dendrogram aligns with batch/group metadata: if batch effects remain, samples from the same batch will cluster tightly regardless of biological group.

## Limitations

- HCA is sensitive to outliers and high-dimensional noise in metabolomic data; noisy or missing features can distort dendrogram structure. Pre-filtering low-abundance or high-variance features may be necessary.
- The choice of linkage method (single, complete, average, Ward) and distance metric (Euclidean, correlation, Manhattan) affects dendrogram shape and cluster assignments; the article does not specify which linkage is used in Sample_Separation().
- Dendrogram cut height for determining final cluster count is subjective. The clusters parameter influences interpretation but does not enforce hard boundaries — users must visually inspect the dendrogram to choose an appropriate threshold.
- HCA does not scale well to very large sample numbers (>10,000); computation time and memory increase quadratically with sample count.

## Evidence

- [readme] Sample_Separation function with method='HCA' parameter: "Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")"
- [readme] Purpose of Sample_Separation for visualization: "There are four sample separation methods for visualizing the clustering and separation of different samples."
- [other] Sample_Separation produces dendrogram output: "Generate hierarchical dendrogram visualization showing sample groupings and cluster boundaries."
- [readme] Input data structure for Sample_Separation: "finalData <- MarkerData$finalData; finalLabel <- MarkerData$finalLabel"
- [other] HCA operation on metabolomic data: "The Sample_Separation() function accepts finalData (feature matrix), finalLabel (sample group labels), clusters parameter (set to 2), and method parameter (set to 'HCA' for hierarchical clustering"
