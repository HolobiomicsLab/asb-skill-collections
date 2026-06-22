---
name: metabolite-sample-clustering-visualization
description: Use when when you have a feature-by-sample metabolomic matrix (finalData) and corresponding sample group labels (finalLabel) and need to visualize how samples cluster together and separate by group using hierarchical clustering;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
---

# metabolite-sample-clustering-visualization

## Summary

Visualize the hierarchical clustering and separation of metabolomic samples using the Sample_Separation function with HCA (hierarchical clustering analysis) method to group samples by their metabolomic profiles and identify sample separation patterns.

## When to use

When you have a feature-by-sample metabolomic matrix (finalData) and corresponding sample group labels (finalLabel) and need to visualize how samples cluster together and separate by group using hierarchical clustering; typically after data integration and batch effect removal steps to assess whether sample groups are sufficiently separated in metabolomic space.

## When NOT to use

- When your data has already been reduced to pre-computed distances or dissimilarity matrices; Sample_Separation requires raw feature counts or intensities to compute hierarchical clustering de novo.
- When you have fewer than 2 samples; hierarchical clustering requires sufficient sample size to produce meaningful dendrograms.
- When sample group labels are unknown or unavailable; finalLabel is required to evaluate clustering quality against known group structure.

## Inputs

- finalData: feature-by-sample numeric matrix (metabolomic features as rows, samples as columns)
- finalLabel: character or factor vector of sample group labels (length equal to number of samples/columns)

## Outputs

- Hierarchical dendrogram visualization showing sample groupings and cluster boundaries
- Sample-to-cluster assignments for each sample
- Hierarchical clustering tree object

## How to apply

Load the feature matrix (finalData) and sample group label vector (finalLabel) into R. Call Sample_Separation() with method='HCA' to perform hierarchical clustering analysis and clusters=2 (or other k value) to specify the number of sample clusters. The function performs hierarchical clustering on samples based on their metabolomic profiles and generates a dendrogram visualization. Extract and record cluster assignments for each sample from the output. Evaluate separation quality by examining the dendrogram structure: well-separated groups should show distinct cluster branches with clear boundaries between sample groups.

## Related tools

- **LargeMetabo** (R package containing Sample_Separation() function for hierarchical clustering visualization of metabolomic samples) — https://github.com/LargeMetabo/LargeMetabo
- **factoextra** (R package used in background processes for cluster visualization and extraction of hierarchical clustering results)
- **ggplot2** (R package used for enhanced visualization and dendrogram plotting)

## Examples

```
Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")
```

## Evaluation signals

- Dendrogram visually shows distinct separation between known sample groups with minimal inter-group branches
- Cluster assignments recovered from the dendrogram match or closely align with the input finalLabel sample group labels
- All samples are successfully assigned to one of the k specified clusters with no missing or NA assignments
- Dendrogram height/distances between clusters are proportional to metabolomic differences; samples within the same group show shorter branch distances than samples from different groups

## Limitations

- HCA dendrogram interpretation can be subjective; different linkage methods may produce different tree topologies and cluster assignments.
- Hierarchical clustering is sensitive to outlier samples which may distort branch structure and mislead group separation assessment.
- Performance and visualization clarity may degrade with very large sample sizes (hundreds to thousands of samples); tree becomes dense and difficult to interpret.

## Evidence

- [other] Research question and method from task card: "Sample_Separation() function accepts finalData (feature matrix), finalLabel (sample group labels), clusters parameter (set to 2), and method parameter (set to 'HCA' for hierarchical clustering"
- [other] Workflow steps from task card: "Execute Sample_Separation() function with method='HCA' and clusters=2 parameters to perform hierarchical clustering on samples. Extract and record cluster assignments for each sample. Generate"
- [readme] README workflow description: "There are four sample separation methods for visualizing the clustering and separation of different samples. In the LargeMetabo package, the four methods are provided for sample separation."
- [readme] README example invocation: "finalData <- MarkerData$finalData; finalLabel <- MarkerData$finalLabel; Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")"
- [readme] Data preparation context from README: "Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass,"
