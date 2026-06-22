---
name: hierarchical-clustering-dendrogram-construction
description: 'Use when when you have a Metaboprep object after quality control filtering and need to visualize metabolite correlation structure to: (1) identify clusters of co-regulated features that may represent the same biological pathway or measurement artifact, (2) set tree-cutting height thresholds for.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - metaboprep
  - dendextend
  - ggplot2
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
---

# hierarchical-clustering-dendrogram-construction

## Summary

Construct a hierarchical dendrogram of metabolite features to identify correlated metabolites and assess feature independence within a metabolomics dataset. This skill is essential for quality control workflows to detect redundant or co-regulated features and inform outlier detection thresholds.

## When to use

When you have a Metaboprep object after quality control filtering and need to visualize metabolite correlation structure to: (1) identify clusters of co-regulated features that may represent the same biological pathway or measurement artifact, (2) set tree-cutting height thresholds for feature grouping, or (3) inform PCA outlier analysis by assessing feature independence before sample outlier detection.

## When NOT to use

- Input is a single metabolite or fewer than 3 features (dendrogram requires sufficient data for meaningful hierarchical relationships)
- Features are already known to be uncorrelated or independently measured (no clustering benefit)
- Goal is only univariate feature filtering without consideration of feature co-regulation or PCA-based outlier detection

## Inputs

- Metaboprep object containing raw or pre-filtered metabolite abundance matrix
- Quality control parameters: tree_cut_height (numeric, e.g., 0.5)

## Outputs

- Hierarchical clustering dendrogram object (hclust or dendextend class)
- Feature summary table with cluster assignments and feature independence flags
- Dendrogram visualization (plot object suitable for rendering)

## How to apply

The dendrogram is constructed during the quality_control() function execution by performing hierarchical clustering on features using a specified tree_cut_height parameter (e.g., 0.5). The clustering identifies groups of correlated metabolites; features within the same cluster are considered dependent for outlier analysis purposes. The tree structure is stored as an attribute of the feature_summary object and can be plotted to visualize feature relationships. The tree_cut_height threshold determines how aggressively features are grouped—lower values create more clusters (stricter independence assumption), while higher values merge more features together. This clustering output directly feeds into PCA outlier detection, where feature independence is re-assessed to avoid counting correlated features as independent PCs.

## Related tools

- **metaboprep** (R package that constructs dendrograms as part of the quality_control() pipeline and stores them as feature_summary attributes for visualization) — https://github.com/MRCIEU/metaboprep
- **dendextend** (R package for manipulating and visualizing dendrogram objects produced by hierarchical clustering)
- **ggplot2** (R package used for alternative dendrogram visualization and styling in metaboprep workflow)

## Examples

```
tree <- attr(mydata@feature_summary, "qc_tree"); plot(tree, hang = -1, cex = 0.75, main = "Feature Tree", sub = "", xlab = "")
```

## Evaluation signals

- Dendrogram is produced without errors and contains all features from the input Metaboprep object
- Tree structure reflects expected feature correlation patterns (metabolites from the same pathway or platform should cluster together)
- Feature independence is correctly re-assessed after tree-cutting; the number of independent features used in PCA matches the number of clusters at the specified tree_cut_height
- Downstream PCA outlier detection uses the corrected feature count and produces outlier flags consistent with sample quality (samples with high missingness or extreme peak areas should rank high in outlier scores)
- Dendrogram visualization is readable and branches are well-separated, indicating meaningful feature grouping

## Limitations

- Tree construction assumes feature abundance data are numeric and comparable across features; missing values (NAs) must be handled before clustering, or they will bias distance calculations.
- The tree_cut_height parameter is user-defined and data-dependent; optimal thresholds are not automatically determined and require domain knowledge or exploratory analysis.
- Hierarchical clustering is sensitive to the choice of distance metric and linkage method (the README and source do not explicitly state which metric or linkage is used, so results may vary with different implementations).
- Large feature sets (>10,000 metabolites) may be computationally expensive and produce dendrograms too large to visualize or interpret meaningfully.

## Evidence

- [methods] Perform hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers.: "Perform hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers."
- [methods] tree_cut_height parameter controls feature clustering granularity in QC pipeline.: "tree_cut_height = 0.5"
- [readme] Feature tree is stored and retrievable as an attribute of feature_summary for visualization.: "tree <- attr(mydata@feature_summary, "qc_tree")"
- [readme] Dendrogram output is a standard plot object that can be rendered with base R graphics.: "plot(tree, hang = -1, cex = 0.75, main = "Example Dataset Feature Tree", sub = "", xlab = "")"
- [methods] Sample PCA outlier analysis re-identifies feature independence based on hierarchical clustering.: "Sample PCA outlier analysis - re-identify feature independence and PC outlier"
