---
name: hierarchical-clustering-dendrogram-generation
description: Use when you have a normalized and imputed metabolite abundance matrix (as a MultiAssayExperiment object) and want to identify groups of co-expressed metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0632
  - http://edamontology.org/topic_3407
  tools:
  - MetaboDiff
  - WGCNA
  - R
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder and Horvarth
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
---

# hierarchical-clustering-dendrogram-generation

## Summary

Build a hierarchical clustering dendrogram from a metabolite correlation matrix to organize and visualize co-expression relationships. This is applied after computing biweight midcorrelation similarity and soft-thresholded adjacency to reveal the hierarchical structure of metabolic modules before dynamic branch cutting.

## When to use

You have a normalized and imputed metabolite abundance matrix (as a MultiAssayExperiment object) and want to identify groups of co-expressed metabolites. Apply this skill after computing biweight midcorrelation similarity and soft-thresholding to adjacency, and before applying dynamic branch cutting to extract module assignments. Use it when you need to visualize the hierarchical relationships among metabolites and detect natural clustering hierarchies that are robust to constant-height cutoffs.

## When NOT to use

- Input metabolite data has not been normalized and imputed — apply normalization and imputation first.
- You have a pre-computed dissimilarity matrix from a different method (e.g., Euclidean distance, Pearson correlation) — dendrogram interpretation depends on the specific similarity measure used.
- The goal is exploratory 2D visualization only — use PCA or t-SNE instead; hierarchical clustering is designed for module discovery, not dimensionality reduction.

## Inputs

- Normalized and imputed MultiAssayExperiment object (norm_imputed assay)
- Biweight midcorrelation similarity matrix (metabolites × metabolites)
- Soft-thresholded adjacency matrix (power β=3)

## Outputs

- Dendrogram object encoding hierarchical metabolite clustering
- Module color vector and module assignment table (metabolite ID → module name/color)
- Dynamic tree cut branch assignments

## How to apply

Compute a dissimilarity matrix as 1 − adjacency from the soft-thresholded correlation matrix (where adjacency is derived from biweight midcorrelation with soft power β=3). Apply hierarchical clustering to this dissimilarity matrix using complete or average linkage to construct a dendrogram that orders metabolites by similarity. The dendrogram structure reveals nested clusters at multiple resolution levels. This hierarchical representation is then input to dynamic branch cutting (rather than fixed-height cutting) to automatically identify branches as distinct metabolic modules, filtering by a minimum module size threshold (e.g., 5 metabolites) to exclude spurious small clusters.

## Related tools

- **WGCNA** (Provides hierarchical clustering, soft thresholding, and dynamic tree cut algorithms for constructing dendrograms and identifying co-expression modules)
- **MetaboDiff** (R package that wraps WGCNA workflow and provides MultiAssayExperiment integration for metabolomics-specific module identification) — https://github.com/andreasmock/MetaboDiff
- **R** (Runtime environment and base statistical computing platform for hierarchical clustering and dendrogram manipulation)

## Examples

```
# Hierarchical clustering with dynamic tree cutting on normalized metabolites
met_clustered <- hclust(as.dist(1 - adjacency_matrix), method="average")
module_colors <- cutreeDynamic(dendro=met_clustered, distM=as.dist(1 - adjacency_matrix), minClusterSize=5)
# Map metabolite IDs to module colors
metabolite_modules <- data.frame(metabolite_id=rownames(adjacency_matrix), module=module_colors)
```

## Evaluation signals

- Dendrogram visual inspection: metabolites with high biweight midcorrelation cluster together at low branch heights; distinct branches correspond to biological pathways or metabolic modules.
- Module size distribution: after dynamic tree cut with minimum size 5, all modules contain ≥ 5 metabolites; no spurious singleton or very small clusters.
- Module pathway coherence: the most abundant SUB_PATHWAY annotation within each module is internally consistent (e.g., amino acid metabolism, lipid metabolism), validating biological relevance of dendrogram structure.
- Reproducibility: re-running hierarchical clustering on the same dissimilarity matrix and applying the same dynamic branch cut parameters produces identical module assignments across runs.
- Correlation structure: metabolite pairs within the same module exhibit higher average biweight midcorrelation than metabolite pairs in different modules, confirming that dendrogram structure reflects similarity.

## Limitations

- Dendrogram sensitivity to soft-thresholding power β: choice of β=3 affects adjacency values and thus dendrogram topology; alternative powers may yield different hierarchies and module assignments.
- Minimum module size filtering (e.g., 5 metabolites) is somewhat arbitrary; modules smaller than threshold are discarded, potentially losing biologically relevant small co-expression clusters.
- Hierarchical clustering assumes a tree structure and cannot represent metabolites with multiple strong associations to different groups; flat clustering methods may be more appropriate if metabolite membership is ambiguous.
- Biweight midcorrelation robustness to outliers depends on data quality upstream (imputation method, outlier removal); poor-quality normalization or imputation propagates into dendrogram structure and module assignments.

## Evidence

- [methods] Compute biweight midcorrelation similarity matrix across all metabolites.: "Compute biweight midcorrelation similarity matrix across all metabolites"
- [methods] Apply soft thresholding with power β=3 to convert similarity to adjacency, then compute dissimilarity as 1 − adjacency.: "Apply soft thresholding with power β=3 to convert similarity to adjacency, then compute dissimilarity as 1 − adjacency"
- [methods] Perform hierarchical clustering on the dissimilarity matrix to construct the dendrogram.: "Perform hierarchical clustering on the dissimilarity matrix to construct the dendrogram"
- [methods] Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers"
- [methods] We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms.: "We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms"
