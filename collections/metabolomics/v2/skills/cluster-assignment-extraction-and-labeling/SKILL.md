---
name: cluster-assignment-extraction-and-labeling
description: Use when after executing hierarchical clustering via Sample_Separation() with method='HCA' on a feature-by-sample metabolomic matrix, when you need to assign each sample to a discrete cluster group (typically k=2 clusters) for use in marker identification, batch effect assessment, or sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0769
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

# cluster-assignment-extraction-and-labeling

## Summary

Extract and record cluster assignments for individual samples after performing hierarchical clustering analysis (HCA) on metabolomic feature matrices. This skill captures the step of translating a dendrogram into discrete, labeled cluster memberships for downstream analysis.

## When to use

After executing hierarchical clustering via Sample_Separation() with method='HCA' on a feature-by-sample metabolomic matrix, when you need to assign each sample to a discrete cluster group (typically k=2 clusters) for use in marker identification, batch effect assessment, or sample phenotyping workflows.

## When NOT to use

- Input finalData is already a pre-computed distance or similarity matrix rather than a feature table; use distance-based clustering directly instead.
- Sample groups are not expected to separate into discrete clusters (e.g., continuous phenotypic gradients); consider ordination methods like PCA or OPLS-DA.
- You require soft cluster assignments (probability/membership scores) rather than hard labels; HCA produces hard assignments only.

## Inputs

- finalData: numeric matrix of metabolomic features (rows) × samples (columns)
- finalLabel: vector of sample group labels or phenotype identifiers (length = number of samples)
- clusters: integer specifying number of clusters (e.g., k=2)
- method: string set to 'HCA' for hierarchical clustering analysis

## Outputs

- cluster_assignments: vector of cluster IDs, one per sample, indexed to finalLabel
- hierarchical_dendrogram: visualization showing hierarchical tree structure and cluster boundaries
- cluster_membership_table: data frame mapping sample names/IDs to assigned cluster and original group label

## How to apply

Call Sample_Separation(finalData, finalLabel, clusters=k, method='HCA') where finalData is a feature-by-sample matrix and finalLabel contains sample group identifiers. The function performs hierarchical clustering and returns cluster assignments that can be extracted and cross-referenced with original sample labels and metadata. Record the cluster ID for each sample and verify that cluster boundaries align with biological or experimental groupings visible in the dendrogram. Use the extracted assignments as categorical labels for subsequent statistical tests or marker discovery steps.

## Related tools

- **LargeMetabo** (R package providing Sample_Separation() function that performs HCA clustering and enables cluster assignment extraction on metabolomic feature matrices) — https://github.com/LargeMetabo/LargeMetabo
- **factoextra** (R package used for extracting and visualizing hierarchical clustering dendrograms and cluster membership assignments)
- **ggplot2** (R package for generating customized dendrograms and cluster assignment visualizations)

## Examples

```
Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")
```

## Evaluation signals

- Each sample in finalLabel receives exactly one cluster assignment (no NAs, no duplicates, cardinality = nrow(finalData)).
- Cluster assignments correspond to cut heights in the dendrogram; verify by visual inspection that samples in the same cluster share high similarity in the tree.
- Cluster distribution aligns with expected biological groupings or phenotypic categories; use contingency tables to cross-tabulate assigned clusters vs. original finalLabel.
- Dendrogram visualization renders without errors and shows clear cluster boundaries at the specified k cutoff.
- Cluster assignments are reproducible: re-running Sample_Separation() with identical inputs yields identical cluster IDs.

## Limitations

- HCA is sensitive to outliers and single-linkage chaining; verify dendrogram structure before accepting assignments.
- k=2 is a rigid choice; the optimal number of clusters is not determined by this skill and must be selected a priori or validated separately (e.g., via dendrogram inspection or silhouette analysis).
- Hierarchical clustering assumes a tree-like structure; if sample relationships are non-hierarchical or modular, recovered clusters may not reflect true biological groupings.
- The method does not account for missing values in finalData; feature matrix must be complete or pre-imputed.

## Evidence

- [other] The Sample_Separation() function accepts finalData (feature matrix), finalLabel (sample group labels), clusters parameter (set to 2), and method parameter (set to 'HCA' for hierarchical clustering analysis) to produce a visualization of hierarchical clustering that separates and groups samples according to their metabolomic profiles.: "The Sample_Separation() function accepts finalData (feature matrix), finalLabel (sample group labels), clusters parameter (set to 2), and method parameter (set to 'HCA' for hierarchical clustering"
- [readme] There are four sample separation methods for visualizing the clustering and separation of different samples.: "There are four sample separation methods for visualizing the clustering and separation of different samples"
- [other] Extract and record cluster assignments for each sample. Generate hierarchical dendrogram visualization showing sample groupings and cluster boundaries.: "Extract and record cluster assignments for each sample. Generate hierarchical dendrogram visualization showing sample groupings and cluster boundaries"
- [readme] Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA"): "Sample_Separation(finalData, finalLabel, clusters = 2, method = "HCA")"
